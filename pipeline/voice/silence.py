#!/usr/bin/env python3
"""Silence analysis and trim plan for TTS output (A20). Analysis only: never modifies the audio.

10 ms frames; level = RMS dBFS; silent if below --threshold-db (default -45 dBFS, absolute).
Plan: keep <= 0.20 s head and <= 0.30 s tail; internal pauses >= --min-pause (0.25 s) are listed, pauses > 0.60 s
raise a warning (reference max ~0.75 s, F-A20-103). Internal pauses are reported, not cut.
"""
import argparse, json, os, sys, shlex
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import decode_audio, dump_json

HOP = 0.010

def frame_db(x, sr):
    n = int(sr * HOP); m = len(x) // n
    r = np.sqrt(np.mean(x[:m * n].reshape(m, n).astype(np.float64) ** 2, axis=1))
    return 20 * np.log10(np.maximum(r, 1e-9))

def runs(mask):
    """[(start, end_exclusive)] of True runs."""
    d = np.diff(np.concatenate([[0], mask.astype(np.int8), [0]]))
    return list(zip(np.where(d == 1)[0], np.where(d == -1)[0]))

def analyse(x, sr, threshold_db=-45.0, min_pause=0.25, warn_pause=0.60, keep_head=0.20, keep_tail=0.30):
    db = frame_db(x, sr); dur = len(x) / sr
    voiced = db >= threshold_db
    rep = {"duration_s": round(dur, 4), "threshold_db": threshold_db, "frame_hop_s": HOP}
    if not voiced.any():
        rep.update(voiced=False, warnings=["no audio above threshold"]); return rep
    first, last = int(np.argmax(voiced)), len(voiced) - 1 - int(np.argmax(voiced[::-1]))
    lead = first * HOP; tail = dur - (last + 1) * HOP
    pauses = []
    for a, b in runs(~voiced[first:last + 1]):
        a, b = a + first, b + first
        if (b - a) * HOP >= min_pause - 1e-9:
            pauses.append({"start_s": round(a * HOP, 3), "end_s": round(b * HOP, 3), "dur_s": round((b - a) * HOP, 3)})
    start, end = max(0.0, lead - keep_head), dur - max(0.0, tail - keep_tail)
    warnings = [f"pause {p['dur_s']:.2f}s at {p['start_s']:.2f}s exceeds {warn_pause}s" for p in pauses if p["dur_s"] > warn_pause]
    rep.update(voiced=True, lead_silence_s=round(lead, 3), tail_silence_s=round(tail, 3),
               first_voiced_s=round(first * HOP, 3), last_voiced_s=round((last + 1) * HOP, 3),
               internal_pauses=pauses, pause_total_s=round(sum(p["dur_s"] for p in pauses), 3),
               voiced_fraction=round(float(voiced[first:last + 1].mean()), 3),
               trim_plan={"keep_head_s": keep_head, "keep_tail_s": keep_tail, "trim_start_s": round(start, 3),
                          "trim_end_s": round(end, 3), "new_duration_s": round(end - start, 3),
                          "note": "shift word timings by -trim_start_s after trimming"},
               warnings=warnings)
    return rep

def ffmpeg_trim_cmd(src, dst, plan):
    return f"ffmpeg -n -i {shlex.quote(src)} -ss {plan['trim_start_s']} -to {plan['trim_end_s']} {shlex.quote(dst)}"

def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("audio"); ap.add_argument("--threshold-db", type=float, default=-45.0)
    ap.add_argument("--min-pause", type=float, default=0.25); ap.add_argument("--warn-pause", type=float, default=0.60)
    ap.add_argument("-o", "--out"); a = ap.parse_args(argv)
    x, sr = decode_audio(a.audio)
    rep = analyse(x, sr, a.threshold_db, a.min_pause, a.warn_pause)
    if a.out:
        if os.path.exists(a.out): print("refusing to overwrite", a.out, file=sys.stderr); return 2
        dump_json(rep, a.out)
    print(json.dumps(rep, indent=2))
    if rep.get("voiced"): print("# trim:", ffmpeg_trim_cmd(a.audio, "<out.wav>", rep["trim_plan"]))
    return 0

if __name__ == "__main__":
    sys.exit(main())
