"""Orchestration: single streaming decode pass, per-stage per-chunk checkpoints, merge, coverage v2, measurements v2."""
import os, sys, time, json, shutil, glob, platform, subprocess, inspect
import numpy as np
from . import VERSION, common as C, probe as P, decode as D, reconcile as R, motion as MO, shots as SH, stats as ST
from . import audio as AU, sheets as SHT, schema as SC

FRAME_STAGES = ["motion", "shots", "color", "edges", "sharpness"]
SPEC = {"motion": ("motion.csv", MO.FIELDS), "shots": ("shot_features.csv", SH.FIELDS),
        "color": ("color.csv", ST.COLOR_FIELDS), "edges": ("edges.csv", ST.EDGE_FIELDS),
        "sharpness": ("sharpness.csv", ST.SHARP_FIELDS)}
ALL_STAGES = ["probe", "decode"] + FRAME_STAGES + ["audio", "sheets"]
DEFAULT_MANIFEST = os.path.join(C.REPO, "knowledge", "dataset", "MANIFEST.json")


class SimulatedInterrupt(Exception):
    pass


def resolve_dataset(key, dataset=None, manifest_path=None):
    """Return (dataset, manifest_sha256|None). Refuses: keys that do not match the key grammar; a dataset label that
    contradicts the key prefix (e.g. SYN-x labelled RC30); RC30 without an existing manifest (no manifest_sha256 =>
    no RC30 record). RC30 rules are never relaxed for SYN/OUR."""
    import re
    if not re.match(SC.KEY_RE, key or ""):
        raise ValueError(f"invalid video key {key!r} (RC30-01..30, OUR-<prod>-<render>, SYN-<id>)")
    implied = SC.key_dataset(key)
    if dataset is not None and dataset != implied:
        raise ValueError(f"refused: key {key!r} belongs to dataset {implied}, not {dataset}")
    if implied == "RC30":
        mp = manifest_path or DEFAULT_MANIFEST
        if not os.path.isfile(mp):
            raise ValueError(f"refused: dataset RC30 requires the frozen manifest ({mp} not found, so no manifest_sha256)")
        return "RC30", C.sha256_file(mp)
    return implied, None


def config_params(key, dataset, proxy_width, mk, sheets_every):
    """All parameters that affect output VALUES/IDs (not chunk size, not the stage selection)."""
    def defaults(fn):
        return {k: v.default for k, v in inspect.signature(fn).parameters.items() if v.default is not inspect.Parameter.empty}
    return {"pipeline_version": VERSION, "key": key, "dataset": dataset, "proxy_width": proxy_width,
            "motion": {**defaults(MO.motion_pair), **mk}, "shots": defaults(SH.detect_candidates),
            "shots_small_width": 160, "dark_thr": ST.DARK_THR, "sheets_every": sheets_every,
            "decode": {"fps_mode": "passthrough", "pix_fmt": "bgr24", "scaler_when_proxy": "swscale flags=area"},
            "audio": {"sr": AU.SR, "hop": AU.HOP, "af": AU.AF_CHAIN}}


def stage_resolutions(video, proxy_width, mk):
    """Working resolution per pixel stage. Any stage that works below native size is `proxy` (including the
    internal downscales of motion (max_w) and shots (160 px))."""
    nw, nh = D.frame_shape(video)
    dw, dh = D.frame_shape(video, proxy_width)
    dec_scaled = (dw, dh) != (nw, nh)

    def mk_res(w, h, extra_scaler):
        r = {"mode": "native" if (w, h) == (nw, nh) else "proxy", "width": int(w), "height": int(h),
             "native_width": int(nw), "native_height": int(nh)}
        sc = ["ffmpeg swscale flags=area"] * dec_scaled + ([extra_scaler] if extra_scaler and (w, h) != (dw, dh) else [])
        if r["mode"] == "proxy":
            r["scaler"] = " + ".join(sc) or "unspecified"
        return r

    def internal(tw, label):
        if dw > tw:
            s = tw / dw
            return tw, int(round(dh * s)), label
        return dw, dh, None
    out = {}
    for st in ("color", "edges", "sharpness"):
        out[st] = mk_res(dw, dh, None)
    w, h, lab = internal(int(mk.get("max_w", 320)), "cv2.resize INTER_AREA (motion estimator)")
    out["motion"] = mk_res(w, h, lab)
    w, h, lab = internal(160, "cv2.resize INTER_AREA (shot features)")
    out["shots"] = mk_res(w, h, lab)
    out["decode"] = mk_res(dw, dh, None)
    return out


def _fields(stage):
    f = list(SPEC[stage][1])
    return f if "status" in f else f + ["status"]


def _compute(stage, prev, cur, i, mk):
    if stage == "motion":
        return MO.first_row() if prev is None else MO.motion_pair(prev, cur, **mk)
    if stage == "shots":
        return SH.first_features(cur) if prev is None else SH.pair_features(prev, cur)
    if stage == "color":
        return ST.color_stats(cur)
    if stage == "edges":
        return ST.edge_stats(cur)
    return ST.sharp_stats(cur)


def _cls(status):
    if status.startswith("error"):
        return "failed"
    if status.startswith("uncertain"):
        return "uncertain"
    return "ok"


ORDER = {"ok": 0, "uncertain": 1, "failed": 2, "missing": 3}


def run(input_path, key, out, proxy_width=None, chunk=150, stages=None, sheets_every=0, stop_after_chunks=None,
        fault_inject=None, motion_kwargs=None, log=print, dataset=None, manifest_path=None):
    dataset, manifest_sha = resolve_dataset(key, dataset, manifest_path)  # raises ValueError: refusals
    t_start = time.time()
    stages = [s for s in (stages or ALL_STAGES)]
    mk = dict(motion_kwargs or {})
    vd = os.path.join(out, key)
    sha = C.sha256_file(input_path)
    params = config_params(key, dataset, proxy_width, mk, sheets_every)
    cfp = C.config_fingerprint(params)
    # checkpoints are keyed by config fingerprint + input bytes + chunk size; any other key dir is stale
    ck_name = f"{cfp[:16]}-{sha[:12]}-c{chunk}"
    root = os.path.join(vd, "_chunks")
    cdir = os.path.join(root, ck_name)
    os.makedirs(root, exist_ok=True)
    for old in os.listdir(root):
        if old != ck_name:
            log(f"[ckpt] stale checkpoint set {old} (config/input/chunk changed) -> discarding")
            shutil.rmtree(os.path.join(root, old), ignore_errors=True) if os.path.isdir(os.path.join(root, old)) else os.remove(os.path.join(root, old))
    os.makedirs(cdir, exist_ok=True)
    C.write_json(os.path.join(cdir, "fingerprint.json"), {"config_fingerprint": cfp, "input_sha256": sha, "chunk": chunk,
                                                          "params": params})
    timing, info = {}, {"chunks_processed": {}, "chunks_skipped": {}}

    # ---- stage 1: probe (cached)
    t0 = time.time()
    pc = os.path.join(cdir, "probe_cache.json")
    if os.path.exists(pc):
        pr = json.load(open(pc))
        log("[probe] cached")
    else:
        pr = P.probe(input_path)
        C.write_json(pc, pr)
    timing["probe"] = time.time() - t0
    video = pr["video"]
    pts = [float(x) if x is not None else float("nan") for x in pr["pts_time"]]
    pr_out = {k: v for k, v in pr.items() if k != "pts_time"}
    pr_out["pts_time_file"] = "frames.csv"
    C.write_json(os.path.join(vd, "probe.json"), pr_out)
    res = stage_resolutions(video, proxy_width, mk)

    # ---- stages 2,4-8: one streaming pass
    fstages = [s for s in FRAME_STAGES if s in stages]
    rows_buf = {s: [] for s in fstages}
    for s in fstages:
        os.makedirs(os.path.join(cdir, s), exist_ok=True)
    cpath = lambda s, c: os.path.join(cdir, s, f"c{c:06d}.csv")
    fault = {s: set(v) for s, v in (fault_inject or {}).items()}
    written = 0
    decoded = 0
    decode_error = None
    prev = None
    t_dec = time.time()
    tstage = {s: 0.0 for s in fstages}

    def flush(c):
        nonlocal written
        did = False
        for s in fstages:
            if rows_buf[s]:
                C.write_csv(cpath(s, c), rows_buf[s], _fields(s))
                rows_buf[s] = []
                info["chunks_processed"][s] = info["chunks_processed"].get(s, 0) + 1
                did = True
        if did:
            written += 1
            if stop_after_chunks and written >= stop_after_chunks:
                raise SimulatedInterrupt(f"stopped after {written} chunks (test hook)")

    if fstages or "decode" in stages:
        cur_chunk = 0
        try:
            for i, fr in D.iter_frames(input_path, video, proxy_width):
                c = i // chunk
                if c != cur_chunk:
                    flush(cur_chunk)
                    cur_chunk = c
                for s in fstages:
                    if os.path.exists(cpath(s, c)):
                        if i % chunk == 0:
                            info["chunks_skipped"][s] = info["chunks_skipped"].get(s, 0) + 1
                        continue
                    t0 = time.perf_counter()
                    try:
                        if i in fault.get(s, ()):
                            raise RuntimeError("injected fault (test)")
                        row = _compute(s, prev, fr, i, mk)
                        row.setdefault("status", "ok")
                    except Exception as e:  # frame is accounted as FAILED, never silently dropped
                        row = {"status": f"error:{type(e).__name__}:{e}"[:200]}
                    row["frame_index"] = i
                    rows_buf[s].append(row)
                    tstage[s] += time.perf_counter() - t0
                prev = fr
                decoded = i + 1
        except SimulatedInterrupt:
            raise
        except RuntimeError as e:  # decoder died mid-stream: keep what was decoded, account the rest as missing
            decode_error = str(e)[:300]
            log(f"[decode] ERROR after {decoded} frames: {decode_error}")
        flush(cur_chunk)
        timing["decode_and_stages_total"] = time.time() - t_dec
        timing.update({f"stage_{s}": v for s, v in tstage.items()})
    rss_stream = C.peak_rss_mb()

    # ---- stage 3: frames.csv + reconciliation
    if decoded == 0 and ("decode" in stages or fstages) and decode_error is None:
        raise RuntimeError("decoded 0 frames")
    rec = R.reconcile(pr, decoded) if decoded else None
    frows = [{"frame_id": C.frame_id(key, i), "frame_index": i,
              "pts_time": f"{pts[i]:.6f}" if i < len(pts) else "nan"} for i in range(decoded)]
    if decoded:
        C.write_csv(os.path.join(vd, "frames.csv"), frows, ["frame_id", "frame_index", "pts_time"])
        C.write_json(os.path.join(vd, "reconcile.json"), rec)
        log(f"[reconcile] {rec['status']} counts={rec['counts']}")

    # ---- merge stage files
    merged = {}
    for s in fstages:
        rows = []
        c = 0
        while os.path.exists(cpath(s, c)):
            rows += C.read_csv(cpath(s, c))
            c += 1
        for r in rows:
            r["frame_id"] = C.frame_id(key, int(r["frame_index"]))
        merged[s] = rows
    cands = []
    if "shots" in merged and merged["shots"]:
        rr = [{k: C.tofloat(v) for k, v in r.items() if k not in ("status", "frame_id", "candidate")}
              for r in merged["shots"]]
        cands = SH.detect_candidates(rr)
        flag = [""] * len(rr)
        for cd in cands:
            for k in range(cd["start"], cd["end"] + 1):
                flag[k] = (flag[k] + "|" if flag[k] else "") + cd["type"]
        for r, f in zip(merged["shots"], flag):
            r["candidate"] = f
        for cd in cands:
            cd["frame_id"] = C.frame_id(key, cd["start"])
            cd["pts_time"] = pts[cd["start"]] if cd["start"] < len(pts) else None
        C.write_json(os.path.join(vd, "shot_candidates.json"),
                     {"note": "CANDIDATES from histogram/MAD/SSIM thresholds; not semantic shot labels",
                      "analysis_resolution": res["shots"], "candidates": cands})
        if "motion" in merged:  # motion across a boundary is not a camera move
            for cd in cands:
                for k in range(cd["start"], min(cd["end"] + 1, len(merged["motion"]))):
                    mr = merged["motion"][k]
                    mr["confidence"], mr["status"] = "low", f"uncertain:{cd['type']}"
    for s, rows in merged.items():
        fn, _ = SPEC[s]
        C.write_csv(os.path.join(vd, fn), rows, ["frame_id"] + _fields(s) + (["candidate"] if s == "shots" else []))

    # ---- stage 9: audio (never aborts the run; failures become coverage-audio errors)
    audio_res, audio_cov, audio_state = None, None, None
    if "audio" in stages and pr["audio"]:
        t0 = time.time()
        acov_f = os.path.join(vd, "audio.coverage.jsonl")
        done = os.path.join(cdir, "audio.done")
        if os.path.exists(done) and os.path.exists(os.path.join(vd, "audio.json")) and os.path.exists(acov_f):
            log("[audio] cached")
            audio_res = json.load(open(os.path.join(vd, "audio.json")))
            audio_cov = json.loads(open(acov_f).readline())
        else:
            audio_res, audio_cov = _audio_stage(input_path, key, dataset, manifest_sha, pr, sha, params, commit=C.git_commit(),
                                                cdir=cdir, vd=vd, run_at=C.now_iso())
            C.write_json(os.path.join(vd, "audio.json"), audio_res)
            C.atomic_write_text(acov_f, json.dumps(audio_cov, sort_keys=True) + "\n")
            open(done, "w").write("ok\n")
        timing["audio"] = time.time() - t0
    elif "audio" in stages:
        audio_state = "no_audio_stream"
        audio_cov = AU.build_absent_coverage(key=key, dataset=dataset, manifest_sha256=manifest_sha, probe=pr, input_sha256=sha,
                                             cfp=C.config_fingerprint({"pipeline_version": VERSION, "audio": params["audio"]}),
                                             commit=C.git_commit(), version=VERSION, run_at=C.now_iso(),
                                             analysis_id=f"rcpipe-audio-v{VERSION}")
        C.atomic_write_text(os.path.join(vd, "audio.coverage.jsonl"), json.dumps(audio_cov, sort_keys=True) + "\n")
        log("[audio] no audio stream: audio_present=false record written")

    # ---- stage 11: sheets
    sheets = []
    if "sheets" in stages and sheets_every:
        sj = os.path.join(vd, "sheets.json")
        if os.path.exists(sj):
            sheets = json.load(open(sj))
        else:
            t0 = time.time()
            sheets = SHT.make_sheets(D.iter_frames(input_path, video, proxy_width), key, pts,
                                     os.path.join(vd, "sheets"), lambda i: i % sheets_every == 0)
            for s_ in sheets:
                s_["file"] = os.path.relpath(s_["file"], vd)
            C.write_json(sj, sheets)
            timing["sheets"] = time.time() - t0

    # ---- coverage v2 + measurements v2
    run_at = C.now_iso()
    commit = C.git_commit()
    cov = None
    if "decode" in stages or fstages:
        cov = build_coverage(key, dataset, manifest_sha, sha, cfp, commit, run_at, video, rec, pr, pts, decoded,
                             fstages, merged, res, decode_error, proxy_width)
        C.atomic_write_text(os.path.join(vd, "coverage.jsonl"), json.dumps(cov, sort_keys=True) + "\n")
    meas = build_measurements(key, dataset, manifest_sha, sha, cfp, decoded, rec, pr, merged, cands, cov, audio_res,
                              commit, params, res)
    C.write_json(os.path.join(vd, "measurements.json"), meas)
    verr = []
    if cov:
        verr += [f"coverage: {e}" for e in SC.validate_coverage(cov)]
    if audio_cov:
        verr += [f"audio coverage: {e}" for e in SC.validate_audio_coverage(audio_cov)]
    for m in meas:
        verr += [f"measurement {m['metric']}: {e}" for e in SC.validate_measurement(m)]

    man = {"pipeline_version": VERSION, "config_fingerprint": cfp, "dataset": dataset, "manifest_sha256": manifest_sha,
           "commit": commit, "input_sha256": sha, "key": key, "run_at": run_at, "params": params, "chunk": chunk,
           "stages": stages, "analysis_resolution": res, "checkpoint_set": ck_name,
           "timing_s": {k: round(v, 3) for k, v in timing.items()},
           "wall_s": round(time.time() - t_start, 3), "peak_rss": C.peak_rss_mb(), "peak_rss_after_stream_pass": rss_stream, "chunks": info,
           "frames_decoded": decoded, "decode_error": decode_error, "audio_state": audio_state or ("analysed" if audio_cov else None),
           "sheets": [s_["file"] for s_ in sheets], "validation_errors": verr,
           "versions": versions(), "argv": sys.argv}
    C.write_json(os.path.join(vd, "run_manifest.json"), man)
    if verr:
        raise RuntimeError("emitted records failed schema validation: " + "; ".join(verr[:5]))
    return {"dir": vd, "decoded": decoded, "reconcile": rec, "coverage": cov, "ledger": [cov] if cov else [],
            "manifest": man, "candidates": cands, "audio_coverage": audio_cov}


def build_coverage(key, dataset, manifest_sha, sha, cfp, commit, run_at, video, rec, pr, pts, decoded, fstages, merged,
                   res, decode_error, proxy_width):
    container = rec["frames_container"] if rec else (pr["video"]["nb_frames"] or pr["video"]["nb_read_packets"] or decoded)
    expected = max(decoded, container)
    per_frame = [{} for _ in range(expected)]  # stage -> class
    reasons = {}  # (stage, i) -> reason
    stage_counts = {}

    def put(stage, i, cls, why=None):
        per_frame[i][stage] = cls
        if why:
            reasons[(stage, i)] = why
    # decode + pts stage
    for i in range(expected):
        if i >= decoded:
            put("decode", i, "missing", decode_error or "frame never decoded (container count exceeds decoded frames)")
        elif not (i < len(pts) and pts[i] == pts[i]):
            put("decode", i, "failed", "pts_time missing")
        else:
            put("decode", i, "ok")
    for s in fstages:
        rows = merged[s]
        for i in range(expected):
            if i >= len(rows):
                put(s, i, "missing", "no row produced (frame not decoded or stage incomplete)" if i >= decoded else
                    "no row produced (stage incomplete)")
            else:
                st = rows[i]["status"]
                c = _cls(st)
                put(s, i, c, st if c != "ok" else None)
    names = ["decode"] + fstages
    for s in names:
        cnt = {k: 0 for k in ORDER}
        for i in range(expected):
            cnt[per_frame[i][s]] += 1
        stage_counts[s] = {**cnt, "analysis_resolution": res[s]}
    overall = {k: 0 for k in ORDER}
    miss = []
    for i in range(expected):
        worst = max((per_frame[i][s] for s in names), key=lambda c: ORDER[c])
        overall[worst] += 1
        if worst in ("failed", "missing"):
            for s in names:
                if per_frame[i][s] in ("failed", "missing"):
                    miss.append({"frame": C.frame_id(key, i), "stage": s, "status": per_frame[i][s],
                                 "reason": reasons.get((s, i), "")})
    # record-level resolution = the FINEST resolution any stage used (schema v2 rule); per-stage values are in stages[*]
    pix = [res[s] for s in fstages] or [res["decode"]]
    top = dict(max(pix, key=lambda r: r["width"]))
    note0 = (f"container count source: {rec['frames_container_source']}; reconcile={rec['status']}; " + "; ".join(rec["notes"])) if rec else ""
    notes = (f"proxy_width={proxy_width}; stage resolutions in stages[*].analysis_resolution (record level = finest stage); "
             f"first frame of pair stages (motion, shots) has no previous frame: counted ok with status "
             f"ok:reference_frame_no_previous_pair; frame class = worst stage (ok<uncertain<failed<missing); "
             + (f"decode error: {decode_error}; " if decode_error else "") + note0)
    r = {"schema_version": "2", "dataset": dataset, "analysis_id": f"rcpipe-v{VERSION}", "video_key": key,
         "native_fps": video["avg_frame_rate"], "frames_container": int(container), "frames_decoded": int(decoded),
         "frames_expected": int(expected), "frames_processed": overall["ok"] + overall["uncertain"],
         "frames_ok": overall["ok"], "frames_uncertain": overall["uncertain"], "frames_failed": overall["failed"],
         "frames_missing": overall["missing"], "stages": stage_counts, "missing": miss,
         "script": f"analysis/rcpipe/pipeline.py@{VERSION}", "pipeline_version": VERSION, "config_fingerprint": cfp,
         "commit": commit, "input_sha256": sha, "analysis_resolution": top, "run_at": run_at, "notes": notes}
    if manifest_sha:
        r["manifest_sha256"] = manifest_sha
    return r


def _audio_stage(input_path, key, dataset, manifest_sha, pr, sha, params, commit, cdir, vd, run_at):
    from . import audio as A
    wav = os.path.join(cdir, "audio_mono48k.wav")  # git-ignored (*.wav) and deleted after analysis
    errors, st = [], {}
    ext = A.extract_wav(input_path, wav)
    errors += ext["errors"]
    vdur = pr["video"]["duration"] or float(pr["format"]["duration"] or 0.0)
    aend = max((a + d for a, d in ext["frames"]), default=0.0)
    ade = pr["audio"]["duration"] or 0.0
    timeline_end = max(vdur, aend, ade if not ext["frames"] else 0.0)
    have_wav = os.path.exists(wav) and bool(ext["frames"])
    if os.path.exists(wav) and not have_wav:
        os.remove(wav)
    env, onsets, ainfo, pcm_sha = [], [], {}, None
    covered, miss = A.coverage_intervals(ext["frames"], timeline_end)
    if have_wav:
        pcm_sha = C.sha256_file(wav)
        try:
            env, onsets, ainfo = A.analyse(wav, miss)
            st["spectral"] = {"status": "uncertain" if miss else "ok",
                              "detail": "envelope rows inside missing intervals carry valid=0" if miss else ""}
            st["onsets"] = {"status": "uncertain" if miss else "ok",
                            "detail": f"{len(ainfo.get('onsets_suppressed_at_gap_edges', []))} onsets suppressed at gap edges" if miss else ""}
        except Exception as e:
            errors.append({"stage": "spectral", "message": f"{type(e).__name__}: {e}"[:300]})
            st["spectral"] = {"status": "failed", "detail": str(e)[:200]}
            st["onsets"] = {"status": "failed", "detail": "analysis failed"}
        os.remove(wav)
    else:
        st["spectral"] = {"status": "failed", "detail": "no decoded samples"}
        st["onsets"] = {"status": "failed", "detail": "no decoded samples"}
    try:
        if not ext["frames"]:
            raise RuntimeError("no decodable audio: loudness not reported")
        loud = A.loudness(input_path)
        if loud["integrated_lufs"] is None:
            raise RuntimeError("ebur128 produced no integrated loudness")
        st["loudness"] = {"status": "uncertain" if miss else "ok",
                          "detail": "measured on the original stream; gaps are not zero-filled there" if miss else ""}
    except Exception as e:
        loud = {"integrated_lufs": None, "lra_lu": None, "true_peak_dbtp": None}
        errors.append({"stage": "loudness", "message": f"{type(e).__name__}: {e}"[:300]})
        st["loudness"] = {"status": "failed", "detail": str(e)[:200]}
    st["decode"] = {"status": "failed" if not ext["frames"] else ("uncertain" if (miss or ext["errors"]) else "ok"),
                    "detail": f"{len(ext['frames'])} decoded frames; {len(miss)} missing interval(s)"}
    if env:
        C.write_csv(os.path.join(vd, "audio_env.csv"), env, A.ENV_FIELDS)
    video = pr["video"]
    ares = {"loudness": loud, "onsets_s": onsets, "analysis": ainfo, "stream": pr["audio"],
            "video_start_time": video["start_time"],
            "av_start_offset_s": (None if pr["audio"]["start_time"] is None or video["start_time"] is None
                                  else pr["audio"]["start_time"] - video["start_time"])}
    ap = params["audio"]
    afp = C.config_fingerprint({"pipeline_version": VERSION, "audio": ap})
    cov = A.build_coverage(key=key, dataset=dataset, manifest_sha256=manifest_sha, probe=pr, input_sha256=sha, cfp=afp,
                           commit=commit, version=VERSION, ext=ext, timeline_end=timeline_end, stages=st, errors=errors,
                           pcm_sha256=pcm_sha, run_at=run_at, analysis_id=f"rcpipe-audio-v{VERSION}")
    return ares, cov


def versions():
    """Package versions via importlib.metadata (no heavy imports, so peak RSS is not distorted)."""
    from importlib.metadata import version
    ff = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True).stdout.splitlines()[0]
    v = {"python": platform.python_version(), "ffmpeg": ff}
    for k, pkg in (("numpy", "numpy"), ("opencv", "opencv-python-headless"), ("scipy", "scipy"),
                   ("skimage", "scikit-image"), ("librosa", "librosa"), ("soundfile", "soundfile")):
        try:
            v[k] = version(pkg)
        except Exception:
            v[k] = "unknown"
    return v


def _meas(metric, value, unit, n, key, dataset, manifest_sha, sha, cfp, decoded, commit, params, dist=None, conf="high",
          lim="", excl=None, resolution=None):
    num = isinstance(value, (int, float)) and not isinstance(value, bool) and value == value
    method = {"script": f"analysis/rcpipe/pipeline.py@{VERSION}", "commit": commit, "params": params,
              "exclusions": excl or [], "pipeline_version": VERSION, "config_fingerprint": cfp}
    if resolution:
        method["analysis_resolution"] = resolution
    m = {"schema_version": "2", "dataset": dataset, "metric": metric, "agent": "A27", "label": "MEASURED",
         "confidence": conf, "value": value if num else None, "unit": unit, "n": int(n),
         "evidence": [f"{key}-f{0:06d}..f{max(decoded - 1, 0):06d}"], "method": method,
         "per_video": {key: float(value) if num and isinstance(value, float) else (value if num else None)},
         "input_sha256": {key: sha}, "limitations": lim}
    if manifest_sha:
        m["manifest_sha256"] = manifest_sha
    if dist:
        m["distribution"] = dist
    return m


def build_measurements(key, dataset, manifest_sha, sha, cfp, decoded, rec, pr, merged, cands, cov, audio_res, commit,
                       params, res):
    out = []
    mk = lambda metric, value, unit, n, **kw: out.append(_meas(metric, value, unit, n, key, dataset, manifest_sha, sha,
                                                               cfp, decoded, commit, params, **kw))
    if rec:
        mk("frames_decoded", decoded, "count", decoded)
        mk("frames_expected", rec["frames_container"], "count", decoded,
           lim=f"container count from {rec['frames_container_source']}; reconcile {rec['status']}")
        t = pr["timing"]
        mk("pts_gaps", t.get("pts_irregular_deltas", 0), "count", decoded,
           lim=f"vfr={t.get('vfr')}; irregular = |delta-median| > {t.get('tolerance_s')} s")
    if cov:
        exp = cov["frames_expected"]
        for name, d in [("overall", {"ok": cov["frames_ok"], "uncertain": cov["frames_uncertain"]})] + \
                list(cov["stages"].items()):
            mk("coverage_comp", round(100.0 * (d["ok"] + d["uncertain"]) / exp, 4) if exp else None, "%", exp,
               lim=f"{name}: (ok+uncertain)/frames_expected; computational only")
    col = lambda s, k: [C.tofloat(r[k]) for r in merged.get(s, []) if not r["status"].startswith("error")]
    for s, ks, unit in (("color", ["luma_mean", "luma_std", "sat_mean"], "gray/1"), ("sharpness", ["lap_var"], "a.u."),
                        ("edges", ["canny_density", "edge_width_px"], "ratio/px")):
        for k in ks:
            v = col(s, k)
            d = C.dist(v)
            if d:
                mk(k, d["median"], unit, len(v), dist=d, resolution=res[s],
                   lim=f"per-frame values at {res[s]['mode']} resolution {res[s]['width']}x{res[s]['height']}; no semantic interpretation")
    if "motion" in merged:
        hi = [r for r in merged["motion"] if r["confidence"] == "high"]
        for k in ("tx", "ty", "scale", "rot_deg", "res_active_frac"):
            v = [C.tofloat(r[k]) for r in hi]
            d = C.dist(v)
            if d:
                mk("motion_" + k, d["median"], "px/frame" if k in ("tx", "ty") else "a.u.", len(v), dist=d, conf="medium",
                   resolution=res["motion"], excl=["pairs with confidence != high"],
                   lim="high-confidence pairs only; camera/local separation is an estimate; with several depth layers the "
                       "estimate locks onto one layer (see README)")
    if cands:
        for ty in sorted({c["type"] for c in cands}):
            nn = sum(1 for c in cands if c["type"] == ty)
            mk("n_" + ty, nn, "count", nn, conf="low", resolution=res["shots"],
               lim="threshold candidates, not semantic shot labels")
    if audio_res and audio_res["loudness"]["integrated_lufs"] is not None:
        L = audio_res["loudness"]
        mk("integrated_lufs", L["integrated_lufs"], "LUFS", 1)
        if L["true_peak_dbtp"] is not None:
            mk("true_peak_dbtp", L["true_peak_dbtp"], "dBTP", 1)
        if L["lra_lu"] is not None:
            mk("lra", L["lra_lu"], "LU", 1)
    return out
