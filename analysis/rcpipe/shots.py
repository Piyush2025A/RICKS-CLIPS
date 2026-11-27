"""Stage 5: shot-boundary / transition CANDIDATES (not semantic labels).

Per-pair features (cur vs prev): hist_dist (max of luma and BGR-channel Bhattacharyya), mad (mean abs gray diff),
ssim_dist (1-SSIM), edge_change, plus luma_mean. Candidate rules in detect_candidates()."""
import numpy as np
import cv2
from skimage.metrics import structural_similarity

FIELDS = ["frame_index", "hist_luma", "hist_bgr", "hist_dist", "mad", "ssim_dist", "edge_change", "luma_mean",
          "candidate"]
NAN = float("nan")


def _small(img, w=160):
    s = w / img.shape[1]
    return cv2.resize(img, (w, int(round(img.shape[0] * s))), interpolation=cv2.INTER_AREA) \
        if img.shape[1] > w else img


def _hists(bgr):
    """luma (32 bins) and per-channel BGR (16 bins x3) normalised histograms. (An HS histogram was tried first and
    rejected: sparse bins made Bhattacharyya jumpy, see knowledge FAILED.md F-A27-001.)"""
    g = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    hl = cv2.calcHist([g], [0], None, [32], [0, 256])
    cv2.normalize(hl, hl, 1, 0, cv2.NORM_L1)
    hc = []
    for c in range(3):
        h = cv2.calcHist([bgr], [c], None, [16], [0, 256])
        cv2.normalize(h, h, 1, 0, cv2.NORM_L1)
        hc.append(h)
    return hl, hc, g


def pair_features(prev, cur):
    a, b = _small(prev), _small(cur)
    hl0, hh0, g0 = _hists(a)
    hl1, hh1, g1 = _hists(b)
    dl = cv2.compareHist(hl0, hl1, cv2.HISTCMP_BHATTACHARYYA)
    dh = float(np.mean([cv2.compareHist(x, y, cv2.HISTCMP_BHATTACHARYYA) for x, y in zip(hh0, hh1)]))
    mad = float(np.abs(g0.astype(np.float32) - g1.astype(np.float32)).mean())
    ss = 1.0 - float(structural_similarity(g0, g1, data_range=255))
    e0, e1 = cv2.Canny(g0, 50, 150), cv2.Canny(g1, 50, 150)
    ec = float(np.abs(e0.astype(np.int16) - e1.astype(np.int16)).mean() / 255.0)
    return {"hist_luma": float(dl), "hist_bgr": float(dh), "hist_dist": float(max(dl, dh)), "mad": mad,
            "ssim_dist": ss, "edge_change": ec, "luma_mean": float(g1.mean())}


def first_features(cur):
    g = cv2.cvtColor(_small(cur), cv2.COLOR_BGR2GRAY)
    return {"hist_luma": NAN, "hist_bgr": NAN, "hist_dist": NAN, "mad": NAN, "ssim_dist": NAN,
            "edge_change": NAN, "luma_mean": float(g.mean()), "status": "ok:reference_frame_no_previous_pair"}


def _rolling_median(x, win):
    n, hw = len(x), win // 2
    return np.array([np.median(x[max(0, i - hw): i + hw + 1]) for i in range(n)])


def detect_candidates(rows, cut_hist=0.3, cut_mad=15.0, cut_ratio=2.5, grad_low_floor=0.03, grad_min_len=4,
                      grad_max_len=60, flash_dev=20.0, flash_max_len=6, win=13):
    """rows: list of dicts with floats hist_dist, mad, luma_mean (index 0 has NaN pair features).
    Returns candidates [{type, start, end, score, ...}] where start is the FIRST NEW frame index (cut) or the
    first/last frame of the range. Types: hard_cut_candidate, gradual_candidate, flash_candidate."""
    n = len(rows)
    h = np.array([r["hist_dist"] for r in rows], float)
    m = np.array([r["mad"] for r in rows], float)
    L = np.array([r["luma_mean"] for r in rows], float)
    h0, m0 = np.nan_to_num(h), np.nan_to_num(m)
    cands, used = [], np.zeros(n, bool)  # used[i]: pair (i-1,i) explained by an earlier candidate
    # flash: luma pulse relative to a rolling median, short run
    if n >= 5:
        dev = L - _rolling_median(L, 2 * win + 1)
        for sign, name in ((1, "white"), (-1, "dark")):
            on = sign * dev > flash_dev
            i = 0
            while i < n:
                if on[i]:
                    j = i
                    while j + 1 < n and on[j + 1]:
                        j += 1
                    if j - i + 1 <= flash_max_len and i > 0 and j < n - 1:
                        cands.append({"type": "flash_candidate", "start": i, "end": j, "polarity": name,
                                      "score": float(np.max(sign * dev[i:j + 1]))})
                        used[i:min(n, j + 2)] = True
                    i = j + 1
                else:
                    i += 1
    # hard cuts
    for i in range(1, n):
        if used[i] or not (h0[i] > cut_hist and m0[i] > cut_mad):
            continue
        lo, hi = max(1, i - 6), min(n, i + 7)
        nb = [k for k in range(lo, hi) if k != i and not used[k]]
        base = max(np.median(h0[nb]) if nb else 0.0, 1e-3)
        if h0[i] / base >= cut_ratio and h0[i] >= np.max(h0[max(1, i - 2):min(n, i + 3)]):
            cands.append({"type": "hard_cut_candidate", "start": i, "end": i, "score": float(h0[i])})
            used[i] = True
    # gradual: runs of moderately elevated pair distance not already explained
    base_h = np.median(h0[1:][~used[1:]]) if n > 2 else 0.0
    low = max(grad_low_floor, 4.0 * base_h)
    i = 1
    while i < n:
        if not used[i] and h0[i] > low:
            j, gap = i, 0
            while j + 1 < n and not used[j + 1] and (h0[j + 1] > low or gap < 1):
                gap = 0 if h0[j + 1] > low else gap + 1
                j += 1
            while j > i and h0[j] <= low:
                j -= 1
            ln = j - i + 1
            if grad_min_len <= ln <= grad_max_len:
                cands.append({"type": "gradual_candidate", "start": i - 1, "end": j, "score": float(h0[i:j + 1].sum()),
                              "len": ln})
            i = j + 1
        else:
            i += 1
    cands.sort(key=lambda c: (c["start"], c["type"]))
    return cands
