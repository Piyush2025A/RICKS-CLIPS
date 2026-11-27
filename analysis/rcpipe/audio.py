"""Stage 9: audio extraction, EBU R128 loudness (ffmpeg ebur128), RMS envelope, spectral features, onsets."""
import re, subprocess, os
import numpy as np

ENV_FIELDS = ["t", "rms_dbfs", "centroid_hz", "band_low_db", "band_mid_db", "band_high_db", "dom_freq_hz",
              "onset_strength"]
SR = 48000
HOP = 480  # 10 ms


def extract_wav(path, wav, sr=SR):
    os.makedirs(os.path.dirname(wav), exist_ok=True)
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", path, "-map", "0:a:0", "-vn", "-ac", "1",
                    "-ar", str(sr), "-c:a", "pcm_f32le", wav], check=True)


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


def analyse(wav):
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
    rows = [{"t": float(t[i]), "rms_dbfs": float(20 * np.log10(rms[i] + eps)), "centroid_hz": float(cen[i]),
             "band_low_db": float(band(0, 250)[i]), "band_mid_db": float(band(250, 4000)[i]),
             "band_high_db": float(band(4000, 1e9)[i]), "dom_freq_hz": float(dom[i]),
             "onset_strength": float(oenv[i])} for i in range(n)]
    return rows, [float(x) for x in on], {"sr": sr, "n_samples": int(len(y)), "duration_s": len(y) / sr,
                                          "hop_s": HOP / sr, "bands_hz": {"low": [0, 250], "mid": [250, 4000],
                                                                          "high": [4000, sr / 2]}}
