"""Stage 4: global (camera) motion + dense flow + residual (local) motion, per consecutive frame pair.

Convention (all values in analysis-frame pixels, i.e. the decoded resolution):
  tx,ty   displacement of CONTENT prev->cur at the image centre (x right, y down)
  scale   content scale factor per frame (>1 = zoom in)
  rot_deg atan2(M10, M00) of the fitted similarity, y-down => positive = clockwise on screen
Global model: LK tracks of Shi-Tomasi corners + RANSAC similarity (estimateAffinePartial2D).
Residual: Farneback flow minus the global-model flow, over textured pixels only.
"""
import math
import numpy as np
import cv2

FIELDS = ["frame_index", "tx", "ty", "scale", "rot_deg", "n_feat", "n_inliers", "inlier_frac", "texture_lapvar",
          "tex_frac", "pc_dx", "pc_dy", "pc_response", "flow_mean_dx", "flow_mean_dy", "flow_mean_mag",
          "res_mean_mag", "res_p95_mag", "res_active_frac", "res_cx", "res_cy", "confidence", "status"]
NAN = float("nan")


def _gray_proxy(img, max_w):
    g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    s = 1.0
    if g.shape[1] > max_w:
        s = max_w / g.shape[1]
        g = cv2.resize(g, (max_w, int(round(g.shape[0] * s))), interpolation=cv2.INTER_AREA)
    return g, s


def motion_pair(prev, cur, max_w=320, exclude_top=0.0, exclude_bottom=0.0, seed=0, flow=True,
                active_thr=0.7, min_inliers=12):
    """prev,cur: BGR uint8 frames. exclude_*: fraction of height masked out (e.g. caption band)."""
    cv2.setRNGSeed(seed)
    g0, s = _gray_proxy(prev, max_w)
    g1, _ = _gray_proxy(cur, max_w)
    h, w = g0.shape
    up = 1.0 / s
    row = {k: NAN for k in FIELDS}
    mask = np.full((h, w), 255, np.uint8)
    if exclude_top > 0:
        mask[: int(h * exclude_top)] = 0
    if exclude_bottom > 0:
        mask[h - int(h * exclude_bottom):] = 0
    row["texture_lapvar"] = float(cv2.Laplacian(g1, cv2.CV_32F).var())
    # --- phase correlation (whole frame, Hann window); sign: shift of content prev->cur
    win = cv2.createHanningWindow((w, h), cv2.CV_32F)
    (pdx, pdy), resp = cv2.phaseCorrelate(np.float32(g0), np.float32(g1), win)
    row.update(pc_dx=pdx * up, pc_dy=pdy * up, pc_response=float(resp))
    # --- feature affine
    M = None
    p0 = cv2.goodFeaturesToTrack(g0, 400, 0.01, 6, mask=mask)
    n_feat = 0 if p0 is None else len(p0)
    row["n_feat"] = n_feat
    if n_feat >= 6:
        p1, st, _ = cv2.calcOpticalFlowPyrLK(g0, g1, p0, None, winSize=(21, 21), maxLevel=4)
        ok = st.ravel() == 1
        if ok.sum() >= 6:
            M, inl = cv2.estimateAffinePartial2D(p0[ok], p1[ok], method=cv2.RANSAC, ransacReprojThreshold=0.8,
                                                 maxIters=3000, confidence=0.995, refineIters=20)
            if M is not None:
                ni = int(inl.sum())
                row["n_inliers"] = ni
                row["inlier_frac"] = ni / float(ok.sum())
                cx, cy = w / 2.0, h / 2.0
                row["tx"] = float((M[0, 0] * cx + M[0, 1] * cy + M[0, 2]) - cx) * up
                row["ty"] = float((M[1, 0] * cx + M[1, 1] * cy + M[1, 2]) - cy) * up
                row["scale"] = float(math.hypot(M[0, 0], M[1, 0]))
                row["rot_deg"] = float(math.degrees(math.atan2(M[1, 0], M[0, 0])))
    # --- dense flow + residual
    gx = cv2.Sobel(g0, cv2.CV_32F, 1, 0)
    gy = cv2.Sobel(g0, cv2.CV_32F, 0, 1)
    tex = cv2.boxFilter(gx * gx + gy * gy, -1, (9, 9)) > 400.0  # textured pixels
    tex &= mask > 0
    row["tex_frac"] = float(tex.mean())
    if flow:
        f = cv2.calcOpticalFlowFarneback(g0, g1, None, 0.5, 4, 21, 3, 5, 1.1, 0)
        mag = np.hypot(f[..., 0], f[..., 1])
        yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
        if M is not None:
            mx = M[0, 0] * xx + M[0, 1] * yy + M[0, 2] - xx
            my = M[1, 0] * xx + M[1, 1] * yy + M[1, 2] - yy
        else:
            mx = my = np.zeros_like(xx)
        r = np.hypot(f[..., 0] - mx, f[..., 1] - my)
        if tex.any():
            row["flow_mean_dx"] = float(f[..., 0][tex].mean()) * up
            row["flow_mean_dy"] = float(f[..., 1][tex].mean()) * up
            row["flow_mean_mag"] = float(mag[tex].mean()) * up
            rt = r[tex]
            row["res_mean_mag"] = float(rt.mean()) * up
            row["res_p95_mag"] = float(np.percentile(rt, 95)) * up
            act = (r > active_thr) & tex
            row["res_active_frac"] = float(act.sum()) / float(tex.sum())
            if act.sum() > 0:
                ys, xs = np.nonzero(act)
                row["res_cx"] = float(xs.mean()) * up
                row["res_cy"] = float(ys.mean()) * up
    # --- confidence: uncertain on low texture / few inliers / poor consistency
    ni = row["n_inliers"]
    if M is None or ni != ni or ni < min_inliers or row["tex_frac"] < 0.05:
        row["confidence"], row["status"] = "low", "uncertain:low_texture_or_few_inliers"
    elif row["inlier_frac"] < 0.5:
        row["confidence"], row["status"] = "medium", "ok:low_inlier_frac"
    else:
        row["confidence"], row["status"] = "high", "ok"
    return row


def first_row():
    r = {k: NAN for k in FIELDS}
    r["confidence"], r["status"] = "none", "first_frame_no_previous"
    return r
