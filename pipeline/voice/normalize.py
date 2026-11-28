#!/usr/bin/env python3
"""Loudness normalisation and the T5 mix (A20 tool, FFmpeg based). Never overwrites or modifies inputs.

 vo      <in> <out.wav>   high-pass 100 Hz -> two-pass loudnorm (I=-14, TP=-2, LRA=3, linear) -> 48 kHz MONO 24-bit WAV
 mix     <vo> <bed> <out.wav>  static bed at -20 dB re VO (400-2000 Hz, voiced frames) -> two-pass loudnorm master
                                -> 48 kHz STEREO (mono duplicated, centre) 24-bit WAV
 measure <in>             integrated LUFS, LRA, true peak (ebur128)

Format choice: the narration stem is MONO (reference side channel is ~27 dB under mid, F-A20-008; halves the size,
no phase issues); the delivered master is stereo-duplicated because the platform expects stereo.
The bed is looped/trimmed to the VO length from t=0 (static, no sidechain; T5 / F-A22-100).
"""
import argparse, json, os, re, subprocess, sys, tempfile
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import decode_audio

I_T, TP_T, LRA_T, HP_HZ, BED_DB, SR = -14.0, -2.0, 3.0, 100, -20.0, 48000

def _run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode: raise RuntimeError(f"ffmpeg failed: {' '.join(cmd)}\n{r.stderr[-800:]}")
    return r.stderr

def measure(path):
    """Integrated loudness (LUFS), LRA (LU), true peak (dBTP) via ebur128."""
    err = _run(["ffmpeg", "-nostats", "-hide_banner", "-i", path, "-af", "ebur128=peak=true", "-f", "null", "-"])
    s = err[err.rindex("Summary:"):]
    g = lambda pat: float(re.search(pat, s).group(1))
    return {"I": g(r"I:\s+(-?[\d.]+|-inf) LUFS"), "LRA": g(r"LRA:\s+([\d.]+) LU"), "TP": g(r"Peak:\s+(-?[\d.]+|-inf) dBFS")}

def _loudnorm_two_pass(src, dst, pre="", I=I_T, TP=TP_T, LRA=LRA_T, channels=None):
    base = f"loudnorm=I={I}:TP={TP}:LRA={LRA}"
    chain = (pre + "," if pre else "")
    err = _run(["ffmpeg", "-nostats", "-hide_banner", "-i", src, "-af", f"{chain}{base}:print_format=json", "-f", "null", "-"])
    m = json.loads(err[err.rindex("{"):err.rindex("}") + 1])
    meas = (f":measured_I={m['input_i']}:measured_LRA={m['input_lra']}:measured_TP={m['input_tp']}"
            f":measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
    cmd = ["ffmpeg", "-nostdin", "-n", "-hide_banner", "-i", src, "-af", f"{chain}{base}{meas}", "-ar", str(SR)]
    if channels: cmd += ["-ac", str(channels)]
    _run(cmd + ["-c:a", "pcm_s24le", dst])
    return m

def _guard(src, dst):
    if os.path.abspath(src) == os.path.abspath(dst) or os.path.exists(dst):
        raise FileExistsError(f"refusing to overwrite {dst}")

def _gain_limit(src, dst, gain_db, TP=TP_T, pre="", channels=None):
    """Fallback when linear loudnorm cannot reach I without exceeding TP (it then under-shoots by the TP headroom):
    static gain, then a peak limiter run at 4x oversampling (192 kHz) as a true-peak approximation, ceiling TP-0.8 dB.
    Added 2026-11-28 by the director after the first real TTS test (linear pass gave -15.3 LUFS for a -14 target)."""
    ceiling = 10 ** ((TP - 0.8) / 20)   # 0.8 dB margin: AAC encoding overshoot measured +0.4 dB (TEST6S, 2026-11-28)
    chain = (pre + "," if pre else "") + (f"volume={gain_db:.2f}dB,aresample=192000,"
                                          f"alimiter=limit={ceiling:.4f}:attack=1:release=50:level=false,aresample={SR}")
    cmd = ["ffmpeg", "-nostdin", "-n", "-hide_banner", "-i", src, "-af", chain, "-ar", str(SR)]
    if channels: cmd += ["-ac", str(channels)]
    _run(cmd + ["-c:a", "pcm_s24le", dst])


def normalize_vo(src, dst, **kw):
    _guard(src, dst)
    m = _loudnorm_two_pass(src, dst, pre=f"highpass=f={HP_HZ}", channels=1, **kw)
    res = measure(dst)
    out = {"pass1": m, "result": res, "method": "loudnorm-linear"}
    I = kw.get("I", I_T); TP = kw.get("TP", TP_T)
    if abs(res["I"] - I) > 0.5:
        # linear mode was TP-limited: redo with gain + oversampled limiter, keep the linear file as *_linear.wav
        lin = dst[:-4] + "_linear.wav"; os.replace(dst, lin)
        g = I - float(m["input_i"])
        for _ in range(6):                       # small correction loop: limiter reduces loudness slightly
            if os.path.exists(dst): os.remove(dst)
            _gain_limit(src, dst, g, TP=TP, pre=f"highpass=f={HP_HZ}", channels=1)
            res = measure(dst)
            if abs(res["I"] - I) <= 0.3: break
            g += I - res["I"]
        out.update({"linear_result": measure(lin), "linear_file": lin, "result": res,
                    "method": "gain+oversampled-limiter", "gain_db": round(g, 2)})
    return out

def _band(x, lo=400, hi=2000):
    from scipy.signal import butter, sosfilt
    return sosfilt(butter(4, [lo, hi], btype="band", fs=SR, output="sos"), x)

def band_level_db(x, mask=None):
    b = _band(x)
    if mask is not None: b = b[mask[:len(b)]]
    return 10 * np.log10(max(float(np.mean(b.astype(np.float64) ** 2)), 1e-18))

def mix_with_bed(vo_path, bed_path, dst, bed_db=BED_DB):
    _guard(vo_path, dst); _guard(bed_path, dst)
    vo, _ = decode_audio(vo_path, SR); bed, _ = decode_audio(bed_path, SR)
    n = len(vo)
    bed = np.tile(bed, int(np.ceil(n / len(bed))))[:n]
    hop = SR // 100; m = n // hop
    fdb = 20 * np.log10(np.maximum(np.sqrt(np.mean(vo[:m*hop].reshape(m, hop).astype(np.float64)**2, axis=1)), 1e-9))
    mask = np.repeat(fdb >= -45.0, hop); mask = np.pad(mask, (0, n - len(mask)))
    vo_lvl, bed_lvl = band_level_db(vo, mask), band_level_db(bed, mask)
    gain_db = vo_lvl + bed_db - bed_lvl
    mixed = vo + bed * (10 ** (gain_db / 20))
    with tempfile.TemporaryDirectory() as td:
        tmp = os.path.join(td, "premix.wav")
        raw = np.repeat(mixed.astype("<f4")[:, None], 2, axis=1).tobytes()
        subprocess.run(["ffmpeg", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-", "-c:a", "pcm_f32le", tmp],
                       input=raw, check=True)
        m1 = _loudnorm_two_pass(tmp, dst, channels=2)
    res = measure(dst)
    chk = decode_audio(dst, SR)[0]
    return {"bed_gain_db": round(gain_db, 2), "vo_band_db": round(vo_lvl, 2), "bed_band_db": round(bed_lvl + gain_db, 2),
            "bed_re_vo_db": round(bed_db, 2), "premix_pass1": m1, "result": res}

def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    v = sub.add_parser("vo"); v.add_argument("src"); v.add_argument("dst")
    x = sub.add_parser("mix"); x.add_argument("vo"); x.add_argument("bed"); x.add_argument("dst"); x.add_argument("--bed-db", type=float, default=BED_DB)
    me = sub.add_parser("measure"); me.add_argument("src")
    a = ap.parse_args(argv)
    out = {"vo": lambda: normalize_vo(a.src, a.dst), "mix": lambda: mix_with_bed(a.vo, a.bed, a.dst, a.bed_db),
           "measure": lambda: measure(a.src)}[a.cmd]()
    print(json.dumps(out, indent=2)); return 0

if __name__ == "__main__":
    sys.exit(main())
