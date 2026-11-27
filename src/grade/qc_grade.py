#!/usr/bin/env python3
"""A11 grade QC: compare our render stats with RC30 targets (knowledge/visual/a11-color-grading-specialist/data/).
Usage: python3 qc_grade.py <video-or-image> [--mood day_cool_sky] [--fps 1]
Decode: ffmpeg -> rgb24 270x480, frames at --fps, limited->full BT.709 expansion ONLY if the source is limited range
(pass --full-range for PNG/full-range renders). Caption band (y 0.60-0.76) is masked. Exit 1 if any check fails.
Checks (RC30 per-video distributions: median of per-frame stats across 30 videos; tolerance = reference IQR across videos)."""
import sys, subprocess, json, numpy as np, cv2, argparse
W, H = 270, 480
T = {  # MEASURED targets: [q25, q50, q75] across the 30 RC30 videos (video medians of per-frame stats)
 "y_p1": [0.075, 0.099, 0.117], "y_p50": [0.347, 0.430, 0.516], "y_p99": [0.906, 0.938, 0.957],
 "contrast_p95_p5": [0.613, 0.643, 0.694], "C_p50": [19.6, 24.9, 29.6], "C_p90": [43.4, 47.2, 54.5]}
MOOD = {  # per-mood frame medians (IQR where listed in data/tone_chroma_hue_summary.json): p1,p50,p99,C_p90
 "day_cool_sky": (0.113, 0.540, 0.954, 44.3), "warm_day_sunset": (0.137, 0.622, 0.941, 51.6),
 "night_blue": (0.075, 0.289, 0.920, 43.9), "dark_low_key": (0.029, 0.164, 0.874, 25.3),
 "warm_interior_lamp": (0.087, 0.364, 0.938, 44.3), "violet_dusk_neon": (0.070, 0.270, 0.807, 70.8),
 "red_orange_glow": (0.098, 0.399, 0.948, 60.8), "neutral_mid": (0.097, 0.486, 0.964, 39.0),
 "bright_neutral_interior": (0.146, 0.673, 0.966, 50.2)}
def frames(path, fps, full):
    rng = "in_range=full" if full else "in_range=limited"
    vf = f"fps={fps},scale={W}:{H}:flags=area:{rng}:out_range=full:in_color_matrix=bt709"
    p = subprocess.Popen(["ffmpeg","-v","error","-i",path,"-vf",vf,"-pix_fmt","rgb24","-f","rawvideo","-"], stdout=subprocess.PIPE)
    while True:
        b = p.stdout.read(W*H*3)
        if len(b) < W*H*3: break
        yield np.frombuffer(b, np.uint8).reshape(H, W, 3)
def stats(rgb):
    m = np.ones((H, W), bool); m[int(.6*H):int(.76*H)] = False
    f = rgb.astype(np.float32)/255; Y = (.2126*f[...,0]+.7152*f[...,1]+.0722*f[...,2])[m]
    lab = cv2.cvtColor(rgb, cv2.COLOR_RGB2LAB).astype(np.float32); C = np.hypot(lab[...,1]-128, lab[...,2]-128)[m]
    p = np.percentile(Y, [1,5,50,95,99])
    return dict(y_p1=p[0], y_p50=p[2], y_p99=p[4], contrast_p95_p5=p[3]-p[1], C_p50=np.percentile(C,50), C_p90=np.percentile(C,90))
if __name__ == "__main__":
    a = argparse.ArgumentParser(); a.add_argument("src"); a.add_argument("--mood"); a.add_argument("--fps", default="1"); a.add_argument("--full-range", action="store_true")
    o = a.parse_args()
    S = [stats(x) for x in frames(o.src, o.fps, o.full_range)]
    med = {k: float(np.median([s[k] for s in S])) for k in S[0]}
    ok = True; rep = {}
    for k, (lo, mid, hi) in T.items():
        good = lo <= med[k] <= hi; ok &= good; rep[k] = dict(value=round(med[k],4), ref_iqr=[lo,hi], ok=good)
    if o.mood:
        p1, p50, p99, c90 = MOOD[o.mood]
        for k, ref, tol in (("y_p1",p1,0.04),("y_p50",p50,0.08),("y_p99",p99,0.05),("C_p90",c90,10)):
            good = abs(med[k]-ref) <= tol; ok &= good; rep["mood_"+k] = dict(value=round(med[k],4), ref=ref, tol=tol, ok=good)
    # shot continuity proxy: 1-fps step in median luma (RC30 p90 = 0.20; flag larger unintended jumps)
    d = np.abs(np.diff([s["y_p50"] for s in S])) if len(S) > 1 else np.array([0.0])
    rep["max_abs_dY50_step"] = dict(value=round(float(d.max()),3), note="RC30 p90 step 0.20; allow only at intentional mood cuts")
    rep["black_clip_frames_pct"] = dict(value=round(100*float(np.mean([s["y_p1"] <= 2/255 for s in S])),1), ref="RC30 pooled 7.2% of frames have >1% pixels <=2/255; <=1% p1 outside low-key videos")
    print(json.dumps(rep, indent=1)); sys.exit(0 if ok else 1)
