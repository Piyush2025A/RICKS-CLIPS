"""Stage 1: ffprobe metadata + per-frame pts + VFR detection."""
import json, subprocess
from fractions import Fraction


def _run(cmd):
    return subprocess.run(cmd, check=True, capture_output=True, text=True).stdout


def _frac(s):
    try:
        return float(Fraction(s))
    except Exception:
        return None


def _f(x):
    try:
        return float(x)
    except Exception:
        return None


def _i(x):
    try:
        return int(x)
    except Exception:
        return None


def probe(path):
    base = ["ffprobe", "-v", "error", "-of", "json"]
    meta = json.loads(_run(base + ["-show_streams", "-show_format", path]))
    cnt = json.loads(_run(base + ["-count_frames", "-count_packets", "-select_streams", "v:0", "-show_entries",
                                  "stream=nb_read_frames,nb_read_packets,nb_frames", path]))["streams"][0]
    fr = json.loads(_run(base + ["-select_streams", "v:0", "-show_frames", "-show_entries",
                                 "frame=pts,pts_time,best_effort_timestamp_time,pkt_dts_time,duration_time,pict_type",
                                 path]))["frames"]
    v = next((s for s in meta["streams"] if s["codec_type"] == "video"), None)
    a = next((s for s in meta["streams"] if s["codec_type"] == "audio"), None)
    out = {"file": path.split("/")[-1], "format": {k: meta["format"].get(k) for k in
           ("format_name", "duration", "size", "bit_rate", "start_time", "nb_streams")}}
    if v is None:
        raise RuntimeError("no video stream")
    rot = 0
    for sd in v.get("side_data_list", []) or []:
        if "rotation" in sd:
            rot = int(sd["rotation"])
    pts, n_missing = [], 0
    for fdict in fr:
        t = _f(fdict.get("pts_time"))
        if t is None:
            t = _f(fdict.get("best_effort_timestamp_time"))
        if t is None:
            n_missing += 1
            t = float("nan")
        pts.append(t)
    out["video"] = {
        "codec": v.get("codec_name"), "profile": v.get("profile"), "pix_fmt": v.get("pix_fmt"),
        "width": v["width"], "height": v["height"], "rotation": rot,
        "r_frame_rate": v.get("r_frame_rate"), "avg_frame_rate": v.get("avg_frame_rate"),
        "r_fps": _frac(v.get("r_frame_rate")), "avg_fps": _frac(v.get("avg_frame_rate")),
        "time_base": v.get("time_base"), "start_time": _f(v.get("start_time")), "duration": _f(v.get("duration")),
        "nb_frames": _i(cnt.get("nb_frames")), "nb_read_frames": _i(cnt.get("nb_read_frames")),
        "nb_read_packets": _i(cnt.get("nb_read_packets")),
        "color_space": v.get("color_space"), "color_range": v.get("color_range"),
    }
    out["audio"] = None if a is None else {
        "codec": a.get("codec_name"), "sample_rate": _i(a.get("sample_rate")), "channels": a.get("channels"),
        "start_time": _f(a.get("start_time")), "duration": _f(a.get("duration")), "time_base": a.get("time_base")}
    out["pts_time"] = pts
    out["pts_missing"] = n_missing
    out["timing"] = vfr_analysis(pts, v.get("time_base"))
    return out


def vfr_analysis(pts, time_base):
    """VFR detection from per-frame pts. CFR if every delta is within max(1.5*time_base, 0.2 ms) of the median.

    Also reports non-monotonic pts, gaps (> 1.5x median delta) and the set of distinct rates observed."""
    import numpy as np
    p = np.array(pts, dtype=float)
    if len(p) < 2 or np.isnan(p).any():
        return {"vfr": None, "note": "insufficient/missing pts"}
    d = np.diff(p)
    med = float(np.median(d))
    tb = _frac(time_base) or 0.0
    tol = max(1.5 * tb, 2e-4)
    irregular = np.abs(d - med) > tol
    clusters = []  # greedy clustering of deltas within 2*tol
    for x in sorted(d[d > 0]):
        if clusters and abs(x - np.mean(clusters[-1])) <= 2 * tol:
            clusters[-1].append(x)
        else:
            clusters.append([x])
    rates = [round(1.0 / float(np.mean(c)), 2) for c in clusters]
    return {"vfr": bool(irregular.any()), "median_delta_s": med, "median_fps": 1.0 / med if med > 0 else None,
            "tolerance_s": tol, "pts_irregular_deltas": int(irregular.sum()),
            "pts_gaps": int((d > 1.5 * med).sum()), "nonmonotonic": int((d <= 0).sum()),
            "distinct_rates_hz": rates[:12], "n_distinct_rates": len(rates),
            "min_delta_s": float(d.min()), "max_delta_s": float(d.max())}
