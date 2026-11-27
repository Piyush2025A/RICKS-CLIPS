"""Orchestration: single streaming decode pass, per-stage per-chunk checkpoints, merge, ledger, measurements."""
import os, sys, time, json, shutil, glob, platform, subprocess
import numpy as np
from . import VERSION, common as C, probe as P, decode as D, reconcile as R, motion as MO, shots as SH, stats as ST
from . import audio as AU, sheets as SHT

FRAME_STAGES = ["motion", "shots", "color", "edges", "sharpness"]
SPEC = {"motion": ("motion.csv", MO.FIELDS), "shots": ("shot_features.csv", SH.FIELDS),
        "color": ("color.csv", ST.COLOR_FIELDS), "edges": ("edges.csv", ST.EDGE_FIELDS),
        "sharpness": ("sharpness.csv", ST.SHARP_FIELDS)}
ALL_STAGES = ["probe", "decode"] + FRAME_STAGES + ["audio", "sheets"]


class SimulatedInterrupt(Exception):
    pass


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


def run(input_path, key, out, proxy_width=None, chunk=150, stages=None, sheets_every=0, stop_after_chunks=None,
        fault_inject=None, motion_kwargs=None, log=print):
    t_start = time.time()
    stages = [s for s in (stages or ALL_STAGES)]
    mk = dict(motion_kwargs or {})
    vd = os.path.join(out, key)
    cdir = os.path.join(vd, "_chunks")
    os.makedirs(vd, exist_ok=True)
    sha = C.sha256_file(input_path)
    fp = {"version": VERSION, "sha256": sha, "proxy_width": proxy_width, "chunk": chunk, "motion": mk, "key": key}
    fpf = os.path.join(cdir, "fingerprint.json")
    if os.path.exists(fpf) and json.load(open(fpf)) != fp:
        log("[ckpt] fingerprint changed -> discarding old checkpoints")
        shutil.rmtree(cdir)
    os.makedirs(cdir, exist_ok=True)
    C.write_json(fpf, fp)
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

    # ---- stages 2,4-8: one streaming pass
    fstages = [s for s in FRAME_STAGES if s in stages]
    rows_buf = {s: [] for s in fstages}
    errors = {s: [] for s in fstages}  # (index, reason)
    for s in fstages:
        os.makedirs(os.path.join(cdir, s), exist_ok=True)
    cpath = lambda s, c: os.path.join(cdir, s, f"c{c:06d}.csv")
    fault = {s: set(v) for s, v in (fault_inject or {}).items()}
    written = 0
    decoded = 0
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
        flush(cur_chunk)
        timing["decode_and_stages_total"] = time.time() - t_dec
        timing.update({f"stage_{s}": v for s, v in tstage.items()})
    rss_stream = C.peak_rss_mb()
    # NOTE: `prev` aliases the previous decoded buffer; iter_frames yields a fresh array per frame, so it is safe.

    # ---- stage 3: frames.csv + reconciliation
    if decoded == 0 and ("decode" in stages or fstages):
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
                      "candidates": cands})
        if "motion" in merged:  # motion across a boundary is not a camera move
            for cd in cands:
                for k in range(cd["start"], min(cd["end"] + 1, len(merged["motion"]))):
                    mr = merged["motion"][k]
                    mr["confidence"], mr["status"] = "low", f"uncertain:{cd['type']}"
    for s, rows in merged.items():
        fn, _ = SPEC[s]
        C.write_csv(os.path.join(vd, fn), rows, ["frame_id"] + _fields(s) + (["candidate"] if s == "shots" else []))
        for r in rows:
            if r["status"].startswith("error"):
                errors[s].append((int(r["frame_index"]), r["status"]))

    # ---- stage 9: audio
    audio_res = None
    if "audio" in stages and pr["audio"]:
        done = os.path.join(cdir, "audio.done")
        t0 = time.time()
        if os.path.exists(done) and os.path.exists(os.path.join(vd, "audio.json")):
            log("[audio] cached")
            audio_res = json.load(open(os.path.join(vd, "audio.json")))
        else:
            wav = os.path.join(cdir, "audio_mono48k.wav")  # git-ignored (*.wav) and deleted after analysis
            AU.extract_wav(input_path, wav)
            env, onsets, ainfo = AU.analyse(wav)
            os.remove(wav)
            audio_res = {"loudness": AU.loudness(input_path), "onsets_s": onsets, "analysis": ainfo,
                         "stream": pr["audio"], "video_start_time": video["start_time"],
                         "av_start_offset_s": (None if pr["audio"]["start_time"] is None or video["start_time"] is None
                                               else pr["audio"]["start_time"] - video["start_time"])}
            C.write_csv(os.path.join(vd, "audio_env.csv"), env, AU.ENV_FIELDS)
            C.write_json(os.path.join(vd, "audio.json"), audio_res)
            open(done, "w").write("ok\n")
        timing["audio"] = time.time() - t0
    elif "audio" in stages:
        log("[audio] no audio stream")

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

    # ---- ledger + measurements
    ledger = []
    run_at = C.now_iso()
    commit = C.git_commit()
    base = {"video_key": key, "native_fps": video["avg_frame_rate"], "frames_container": rec["frames_container"] if rec else 0,
            "frames_decoded": decoded, "frames_expected": decoded, "script": f"analysis/rcpipe/pipeline.py@{VERSION}",
            "commit": commit, "input_sha256": sha, "run_at": run_at}
    note0 = (f"container count source: {rec['frames_container_source']}; reconcile={rec['status']}; "
             + "; ".join(rec["notes"])) if rec else ""
    if decoded:
        miss = [{"frame": C.frame_id(key, i), "reason": "pts_time missing"} for i in range(decoded)
                if not (i < len(pts) and pts[i] == pts[i])]
        ledger.append({**base, "analysis_id": f"rcpipe-decode-pts-v{VERSION}", "frames_processed": decoded - len(miss),
                       "missing": miss, "notes": note0})
    for s in fstages:
        n_ok = len(merged[s]) - len(errors[s])
        miss = [{"frame": C.frame_id(key, i), "reason": r} for i, r in errors[s]]
        miss += [{"frame": C.frame_id(key, i), "reason": "no row produced (stage incomplete)"}
                 for i in range(len(merged[s]), decoded)]
        n_ok = decoded - len(miss)
        ledger.append({**base, "analysis_id": f"rcpipe-{s}-v{VERSION}", "frames_processed": n_ok, "missing": miss,
                       "notes": f"proxy_width={proxy_width}; chunk={chunk}; " + note0})
    with open(os.path.join(vd, "coverage.jsonl"), "w") as f:
        for r in ledger:
            f.write(json.dumps(r, sort_keys=True) + "\n")

    meas = build_measurements(key, decoded, rec, pr, merged, cands, ledger, audio_res, commit, proxy_width, mk)
    C.write_json(os.path.join(vd, "measurements.json"), meas)

    man = {"pipeline_version": VERSION, "commit": commit, "input_sha256": sha, "key": key, "run_at": run_at,
           "params": fp, "stages": stages, "timing_s": {k: round(v, 3) for k, v in timing.items()},
           "wall_s": round(time.time() - t_start, 3), "peak_rss": C.peak_rss_mb(), "peak_rss_after_stream_pass": rss_stream, "chunks": info,
           "frames_decoded": decoded, "sheets": [s_["file"] for s_ in sheets],
           "versions": versions(), "argv": sys.argv}
    C.write_json(os.path.join(vd, "run_manifest.json"), man)
    return {"dir": vd, "decoded": decoded, "reconcile": rec, "ledger": ledger, "manifest": man, "candidates": cands}


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


def _meas(metric, value, unit, n, key, decoded, commit, params, dist=None, conf="high", lim="", excl=None):
    m = {"metric": metric, "agent": "A27", "label": "MEASURED", "confidence": conf, "value": value, "unit": unit,
         "n": int(n), "evidence": [f"{key}-f{0:06d}..f{max(decoded - 1, 0):06d}"],
         "method": {"script": f"analysis/rcpipe/pipeline.py@{VERSION}", "commit": commit, "params": params,
                    "exclusions": excl or []}, "per_video": {key: value if isinstance(value, (int, float)) else 0},
         "limitations": lim}
    if dist:
        m["distribution"] = dist
    return m


def build_measurements(key, decoded, rec, pr, merged, cands, ledger, audio_res, commit, proxy, mk):
    out = []
    p = {"proxy_width": proxy, **mk}
    if rec:
        out.append(_meas("frames_decoded", decoded, "count", decoded, key, decoded, commit, p))
        out.append(_meas("frames_expected", rec["frames_container"], "count", decoded, key, decoded, commit, p,
                         lim=f"container count from {rec['frames_container_source']}; reconcile {rec['status']}"))
        t = pr["timing"]
        out.append(_meas("pts_gaps", t.get("pts_irregular_deltas", 0), "count", decoded, key, decoded, commit, p,
                         lim=f"vfr={t.get('vfr')}; irregular = |delta-median| > {t.get('tolerance_s')} s"))
    for r in ledger:
        cov = 100.0 * r["frames_processed"] / r["frames_decoded"] if r["frames_decoded"] else 0.0
        out.append(_meas("coverage_comp", round(cov, 4), "%", r["frames_decoded"], key, decoded, commit, p,
                         lim=r["analysis_id"]))
    col = lambda s, k: [C.tofloat(r[k]) for r in merged.get(s, []) if not r["status"].startswith("error")]
    for s, ks, unit in (("color", ["luma_mean", "luma_std", "sat_mean"], "gray/1"), ("sharpness", ["lap_var"], "a.u."),
                        ("edges", ["canny_density", "edge_width_px"], "ratio/px")):
        for k in ks:
            v = col(s, k)
            d = C.dist(v)
            if d:
                out.append(_meas(k, d["median"], unit, len(v), key, decoded, commit, p, dist=d,
                                 lim="per-frame values at analysis resolution; no semantic interpretation"))
    if "motion" in merged:
        hi = [r for r in merged["motion"] if r["confidence"] == "high"]
        for k in ("tx", "ty", "scale", "rot_deg", "res_active_frac"):
            v = [C.tofloat(r[k]) for r in hi]
            d = C.dist(v)
            if d:
                out.append(_meas("motion_" + k, d["median"], "px/frame" if k in ("tx", "ty") else "a.u.", len(v), key,
                                 decoded, commit, p, dist=d, conf="medium",
                                 lim="high-confidence pairs only; camera/local separation is an estimate"))
    if cands:
        for ty in sorted({c["type"] for c in cands}):
            nn = sum(1 for c in cands if c["type"] == ty)
            out.append(_meas("n_" + ty, nn, "count", nn, key, decoded, commit, p, conf="low",
                             lim="threshold candidates, not semantic shot labels"))
    if audio_res and audio_res["loudness"]["integrated_lufs"] is not None:
        L = audio_res["loudness"]
        out.append(_meas("integrated_lufs", L["integrated_lufs"], "LUFS", 1, key, decoded, commit, {}, conf="high"))
        if L["true_peak_dbtp"] is not None:
            out.append(_meas("true_peak_dbtp", L["true_peak_dbtp"], "dBTP", 1, key, decoded, commit, {}))
        if L["lra_lu"] is not None:
            out.append(_meas("lra", L["lra_lu"], "LU", 1, key, decoded, commit, {}))
    return out
