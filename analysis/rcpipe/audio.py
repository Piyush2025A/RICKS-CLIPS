"""Stage 9: audio extraction, EBU R128 loudness (ffmpeg ebur128), RMS envelope, spectral features, onsets."""
import re, subprocess, os
import numpy as np

ENV_FIELDS = ["t", "rms_dbfs", "centroid_hz", "band_low_db", "band_mid_db", "band_high_db", "dom_freq_hz",
              "onset_strength", "valid"]
SR = 48000
HOP = 480  # 10 ms


AF_CHAIN = "ashowinfo,aresample=async=1000:min_hard_comp=0.01:first_pts=0"
_AS = re.compile(r"pts_time:(-?[\d.]+)\s.*?rate:(\d+)\s+nb_samples:(\d+)")
_ERR = re.compile(r"(error|invalid|corrupt|failed|truncat|unsupported|not found)", re.I)


def extract_wav(path, wav, sr=SR):
    """Decode audio stream 0 to mono float WAV on the media timeline (leading/inner gaps are zero-filled by
    aresample, so the wav time axis == the stream pts axis). Returns {frames:[(pts_s, dur_s)], errors:[...], rc}.
    Never raises on undecodable audio: failures are returned in `errors` / rc."""
    os.makedirs(os.path.dirname(wav), exist_ok=True)
    if os.path.exists(wav):
        os.remove(wav)
    p = subprocess.run(["ffmpeg", "-nostdin", "-v", "info", "-y", "-i", path, "-map", "0:a:0", "-vn", "-af", AF_CHAIN,
                        "-ac", "1", "-ar", str(sr), "-c:a", "pcm_f32le", wav], capture_output=True, text=True,
                       errors="replace")
    frames, errs = [], {}
    for ln in p.stderr.splitlines():
        if "ashowinfo" in ln and " n:" in ln:
            m = _AS.search(ln)
            if m:
                frames.append((float(m.group(1)), int(m.group(3)) / int(m.group(2))))
        elif _ERR.search(ln) and ln.startswith(("[", "Error")) and "Parsed_ashowinfo" not in ln:  # decoder/demuxer messages only (not banners/paths)
            k = re.sub(r"0x[0-9a-f]+", "0x..", ln.strip())[:200]
            errs[k] = errs.get(k, 0) + 1
    errors = [{"stage": "decode", "message": f"{k} (x{n})" if n > 1 else k} for k, n in list(errs.items())[:10]]
    if p.returncode != 0:
        errors.append({"stage": "decode", "message": f"ffmpeg exit {p.returncode}"})
    if not os.path.exists(wav) or os.path.getsize(wav) < 100:
        errors.append({"stage": "decode", "message": "no decodable audio samples produced"})
        if os.path.exists(wav):
            os.remove(wav)
    return {"frames": frames, "errors": errors, "rc": p.returncode}


def coverage_intervals(frames, timeline_end, tol=0.001):
    """Complement of the decoded-frame intervals inside [0, timeline_end]. Returns (covered_s, missing[(a,b,why)])."""
    iv = sorted((max(0.0, a), min(timeline_end, a + d)) for a, d in frames if a + d > 0 and a < timeline_end)
    merged = []
    for a, b in iv:
        if merged and a - merged[-1][1] <= tol:
            merged[-1][1] = max(merged[-1][1], b)
        else:
            merged.append([a, b])
    miss, cur = [], 0.0
    for a, b in merged:
        if a - cur > tol:
            miss.append((cur, a, "leading: audio starts after t=0" if cur == 0.0 else
                         "timestamp gap or undecodable packets between decoded audio frames"))
        cur = max(cur, b)
    if timeline_end - cur > tol:
        miss.append((cur, timeline_end, "audio stream ends before the end of the media timeline"
                     if merged else "no decodable audio"))
    return sum(b - a for a, b in merged), miss


def loudness(path):
    """ffmpeg ebur128 on the original (all channels, K-weighted per BS.1770). Returns summary + short-term stats."""
    p = subprocess.run(["ffmpeg", "-nostdin", "-nostats", "-v", "verbose", "-i", path, "-map", "0:a:0", "-af",
                        "ebur128=peak=true:framelog=verbose", "-f", "null", "-"], capture_output=True, text=True)
    txt = p.stderr
    fl = re.findall(r"t:\s*([\d.]+)\s+TARGET:\S+ LUFS\s+M:\s*(\S+)\s+S:\s*(\S+)\s+I:\s*(\S+) LUFS\s+LRA:\s*(\S+) LU", txt)
    summ = txt[txt.rfind("Summary:"):] if "Summary:" in txt else ""

    def g(pat):
        m = re.search(pat, summ)
        return float(m.group(1)) if m else None
    S = np.array([float(x[2]) for x in fl if float(x[0]) >= 3.0 and x[2] not in ("-inf", "nan")], float)
    M = np.array([float(x[1]) for x in fl if x[1] not in ("-inf", "nan")], float)
    return {"integrated_lufs": g(r"I:\s+(-?[\d.]+) LUFS"), "lra_lu": g(r"LRA:\s+(-?[\d.]+) LU"),
            "true_peak_dbtp": g(r"(?s)True peak:.*?Peak:\s+(-?[\d.]+) dBFS") if "True peak" in summ else None,
            "short_term_max_lufs": float(S.max()) if S.size else None,
            "short_term_median_lufs": float(np.median(S)) if S.size else None,
            "momentary_max_lufs": float(M.max()) if M.size else None,
            "n_short_term": int(S.size), "note": "short-term (3 s window) values exist only for t>=3 s"}


def analyse(wav, missing=()):
    import soundfile as sf, librosa
    y, sr = sf.read(wav, dtype="float32")
    if y.ndim > 1:
        y = y.mean(1)
    eps = 1e-10
    rms = librosa.feature.rms(y=y, frame_length=1200, hop_length=HOP, center=True)[0]
    S = np.abs(librosa.stft(y, n_fft=4096, hop_length=HOP, center=True)) ** 2
    fr = librosa.fft_frequencies(sr=sr, n_fft=4096)
    tot = S.sum(0) + eps
    cen = (S * fr[:, None]).sum(0) / tot
    band = lambda lo, hi: 10 * np.log10(S[(fr >= lo) & (fr < hi)].sum(0) / tot + eps)
    k = S.argmax(0)
    # parabolic interpolation of the peak bin in log power
    dom = fr[k].copy()
    for i, kk in enumerate(k):
        if 0 < kk < len(fr) - 1:
            a, b, c = np.log(S[kk - 1, i] + eps), np.log(S[kk, i] + eps), np.log(S[kk + 1, i] + eps)
            den = a - 2 * b + c
            if den != 0:
                dom[i] = fr[kk] + 0.5 * (a - c) / den * (fr[1] - fr[0])
    oenv = librosa.onset.onset_strength(y=y, sr=sr, hop_length=HOP)
    on = librosa.onset.onset_detect(onset_envelope=oenv, sr=sr, hop_length=HOP, units="time", backtrack=False)
    n = min(len(rms), S.shape[1], len(oenv))
    t = np.arange(n) * HOP / sr
    valid = np.ones(n, int)
    for a, b, _ in missing:
        valid[(t >= a) & (t < b)] = 0
    suppressed = [float(x) for x in on if any(a - 0.03 <= x <= b + 0.05 for a, b, _ in missing)]
    on = np.array([x for x in on if x not in suppressed])
    bl, bm, bh = band(0, 250), band(250, 4000), band(4000, 1e9)
    rows = [{"t": float(t[i]), "rms_dbfs": float(20 * np.log10(rms[i] + eps)), "centroid_hz": float(cen[i]),
             "band_low_db": float(bl[i]), "band_mid_db": float(bm[i]),
             "band_high_db": float(bh[i]), "dom_freq_hz": float(dom[i]),
             "onset_strength": float(oenv[i]), "valid": int(valid[i])} for i in range(n)]
    return rows, [float(x) for x in on], {"sr": sr, "n_samples": int(len(y)), "duration_s": len(y) / sr,
                                          "hop_s": HOP / sr, "onsets_suppressed_at_gap_edges": suppressed, "bands_hz": {"low": [0, 250], "mid": [250, 4000],
                                                                          "high": [4000, sr / 2]}}


def build_coverage(*, key, dataset, manifest_sha256, probe, input_sha256, cfp, commit, version, ext, timeline_end,
                   stages, errors, pcm_sha256=None, run_at, analysis_id):
    """coverage-audio.schema record. `ext` = extract_wav() result (frames, errors) or None if extraction never ran.
    analyzed_s = seconds covered by decoded audio frames; missing_intervals = the complement inside [0, duration_s],
    so analyzed_s + sum(missing) == duration_s (+-1 ms per interval) by construction and is re-checked by the validator."""
    a = probe["audio"]
    frames = ext["frames"] if ext else []
    covered, miss = coverage_intervals(frames, timeline_end)
    rec = {"schema_version": "1", "dataset": dataset, "analysis_id": analysis_id, "video_key": key, "audio_present": True,
           "stream": {k: v for k, v in {"index": a.get("index", 0) or 0, "codec_name": a["codec"] or "unknown",
                                        "sample_rate": a["sample_rate"] or 0, "channels": a["channels"] or 0,
                                        "channel_layout": a.get("channel_layout"), "start_time_s": a.get("start_time"),
                                        "stream_sha256": pcm_sha256}.items() if v is not None},
           "analysis_sample_rate": SR, "duration_s": round(timeline_end, 6), "analyzed_s": round(covered, 6),
           "hop_s": HOP / SR,
           "missing_intervals": [{"start_s": round(x, 6), "end_s": round(y, 6), "reason": why} for x, y, why in miss],
           "stages": stages, "errors": errors, "script": f"analysis/rcpipe/audio.py@{version}",
           "pipeline_version": version, "config_fingerprint": cfp, "commit": commit, "input_sha256": input_sha256,
           "run_at": run_at,
           "notes": f"timeline end = max(video duration, audio end); decoded with ffmpeg -af {AF_CHAIN} (zero-fill of gaps "
                    f"so the wav axis equals the pts axis; filled samples are flagged valid=0 in audio_env.csv); "
                    f"timeline origin t=0 = stream pts 0; resampler swresample"}
    if manifest_sha256:
        rec["manifest_sha256"] = manifest_sha256
    return rec


def build_absent_coverage(*, key, dataset, manifest_sha256, probe, input_sha256, cfp, commit, version, run_at, analysis_id):
    """Record for a container without an audio stream: audio_present false, stream null, analyzed 0 s, whole duration
    missing with reason 'no audio stream'."""
    vdur = probe["video"]["duration"] or float(probe["format"]["duration"] or 0.0)
    rec = {"schema_version": "1", "dataset": dataset, "analysis_id": analysis_id, "video_key": key, "audio_present": False,
           "stream": None, "duration_s": round(vdur, 6), "analyzed_s": 0, "hop_s": HOP / SR,
           "missing_intervals": [{"start_s": 0.0, "end_s": round(vdur, 6), "reason": "no audio stream"}],
           "stages": {}, "errors": [], "script": f"analysis/rcpipe/audio.py@{version}", "pipeline_version": version,
           "config_fingerprint": cfp, "commit": commit, "input_sha256": input_sha256, "run_at": run_at,
           "notes": "container has no audio stream"}
    if manifest_sha256:
        rec["manifest_sha256"] = manifest_sha256
    return rec
