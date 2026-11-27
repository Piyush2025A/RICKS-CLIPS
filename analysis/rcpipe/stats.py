"""Stages 6-8: colour/brightness, edge/outline, sharpness. One pure function per measure (frame -> dict)."""
import numpy as np
import cv2

NAN = float("nan")
COLOR_FIELDS = (["frame_index", "luma_mean", "luma_std", "luma_p1", "luma_p5", "luma_p50", "luma_p95", "luma_p99",
                 "L_mean", "L_std", "a_mean", "a_std", "b_mean", "b_std", "sat_mean", "sat_std", "val_mean",
                 "hue_circ_mean_deg", "chroma_frac"] + [f"hue{k:02d}" for k in range(12)])
EDGE_FIELDS = ["frame_index", "canny_density", "dark_frac", "dark_line_ratio", "edge_width_px", "edge_width_n"]
SHARP_FIELDS = ["frame_index", "lap_var", "tenengrad", "grad_energy"]
DARK_THR = 60  # gray level below which a pixel counts as dark ink


def color_stats(bgr):
    g = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    p = np.percentile(g, [1, 5, 50, 95, 99])
    lab = cv2.cvtColor(bgr, cv2.COLOR_BGR2Lab).astype(np.float32)
    Lc, ac, bc = lab[..., 0] * (100.0 / 255.0), lab[..., 1] - 128.0, lab[..., 2] - 128.0
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    H, S, V = hsv[..., 0].astype(np.float32) * 2.0, hsv[..., 1] / 255.0, hsv[..., 2] / 255.0  # H in degrees
    sel = (S > 0.15) & (V > 0.15)
    hist = np.histogram(H[sel], bins=12, range=(0, 360))[0].astype(float)
    hist = hist / max(1, hist.sum())
    if sel.any():
        ang = np.deg2rad(H[sel])
        hm = float(np.degrees(np.arctan2(np.sin(ang).mean(), np.cos(ang).mean())) % 360)
    else:
        hm = NAN
    r = {"luma_mean": float(g.mean()), "luma_std": float(g.std()), "luma_p1": p[0], "luma_p5": p[1],
         "luma_p50": p[2], "luma_p95": p[3], "luma_p99": p[4], "L_mean": float(Lc.mean()), "L_std": float(Lc.std()),
         "a_mean": float(ac.mean()), "a_std": float(ac.std()), "b_mean": float(bc.mean()), "b_std": float(bc.std()),
         "sat_mean": float(S.mean()), "sat_std": float(S.std()), "val_mean": float(V.mean()),
         "hue_circ_mean_deg": hm, "chroma_frac": float(sel.mean())}
    for k in range(12):
        r[f"hue{k:02d}"] = float(hist[k])
    return r


def edge_stats(bgr):
    """canny_density: edge pixels/total. dark_line_ratio: share of dark pixels (<DARK_THR) belonging to thin
    structures (local half-thickness <= 8 px). edge_width_px: 2*median(ridge distance)-0.5 over the dark mask,
    +-0.5 px for straight lines (odd w: +0.5, even w: -0.5), approximate otherwise (see README)."""
    g = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    dens = float((cv2.Canny(g, 50, 150) > 0).mean())
    dark = (g < DARK_THR).astype(np.uint8)
    nd = int(dark.sum())
    out = {"canny_density": dens, "dark_frac": nd / dark.size, "dark_line_ratio": NAN, "edge_width_px": NAN,
           "edge_width_n": 0}
    if nd < 20:
        return out
    dt = cv2.distanceTransform(dark, cv2.DIST_L2, 5)
    ridge = (dt > 0.5) & (dt >= cv2.dilate(dt, np.ones((3, 3), np.uint8)) - 1e-6)
    r = dt[ridge]
    thin = dt <= 8.0
    out["dark_line_ratio"] = float((dark.astype(bool) & thin).sum()) / nd
    out["edge_width_px"] = float(2.0 * np.median(r) - 0.5)
    out["edge_width_n"] = int(r.size)
    return out


def sharp_stats(bgr):
    g = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY).astype(np.float32)
    lap = cv2.Laplacian(g, cv2.CV_32F)
    gx, gy = cv2.Sobel(g, cv2.CV_32F, 1, 0), cv2.Sobel(g, cv2.CV_32F, 0, 1)
    g2 = gx * gx + gy * gy
    return {"lap_var": float(lap.var()), "tenengrad": float(g2.mean()), "grad_energy": float(np.sqrt(g2).mean())}
