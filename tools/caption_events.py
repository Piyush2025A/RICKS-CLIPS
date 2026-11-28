#!/usr/bin/env python3
"""Caption-event detector for burned-in single-word captions (director tool, Phase 3 completion, v0.1).

Decodes every native frame of one RC30 video (ffmpeg, crop to the caption band only), builds an "outlined bright
text" mask per frame, segments the video into stable caption segments, and writes PRIVATE outputs:
  <out>/<KEY>/caption_frames.csv   per frame: frame_index, ink (mask px), x0,x1,y0,y1 (band coords, half res)
  <out>/<KEY>/caption_segments.csv per segment: seg, f_start, f_end, n_frames, t_start, t_end, bbox, mid_frame
  <out>/<KEY>/sheets/<KEY>_cap_NNN.png  one crop per segment (mid frame), 4 x 15 tiles, segment id printed
Text is NOT recognised here; reading the tiles is a visual task (logged in the visual ledger).
Band: y 0.60-0.80 of frame height (A14 F-a14-003: caption band 0.689-0.717). Half resolution processing.
Usage: .venv-analysis/bin/python -I tools/caption_events.py VIDEO.mp4 --key RC30-nn --out DIR
Read-only on the source video."""
import argparse, csv, os, subprocess, sys
import numpy as np
import cv2

W, H = 1080, 1920
Y0, Y1 = int(0.60 * H), int(0.80 * H)          # 1152..1536
BH = Y1 - Y0
SW, SH = W // 2, BH // 2                         # processing size 540 x 192
MIN_INK = 60                                     # mask pixels (half res) for "caption present"
IOU_SAME = 0.55                                  # consecutive masks with IoU >= this are the same caption
MIN_SEG = 2                                      # frames


R0, R1 = 40, 160          # caption rows in the half-res band (frame y 0.642-0.767)
SHIFT = 7                 # max half-width of a white caption stroke (half-res px)


def _near(dark, axis, sign):
    acc = np.zeros_like(dark)
    for s in range(1, SHIFT + 1):
        acc |= np.roll(dark, sign * s, axis=axis)
    return acc


def mask_of(rgb):
    """White caption strokes: near-white, unsaturated pixels with a dark outline pixel within SHIFT px on BOTH sides
    (horizontally or vertically). White scenery regions (wide) and dark-on-white print fail the two-sided test."""
    small = cv2.resize(rgb, (SW, SH), interpolation=cv2.INTER_AREA)
    mx = small.max(axis=2).astype(np.int16); mn = small.min(axis=2).astype(np.int16)
    white = (mn >= 215) & (mx - mn <= 35)
    dark = mx <= 55
    stroke = white & ((_near(dark, 1, 1) & _near(dark, 1, -1)) | (_near(dark, 0, 1) & _near(dark, 0, -1)))
    stroke[:R0] = False; stroke[R1:] = False
    m = stroke.astype(np.uint8)
    n, lab, st, cen = cv2.connectedComponentsWithStats(m, connectivity=8)
    keep = np.zeros(n, bool)
    for i in range(1, n):
        x, y, w, h, a = st[i]
        if a >= 8 and 6 <= h <= 60 and w <= 200:
            keep[i] = True
    k = keep[lab]
    if k.sum() == 0:
        return k, small
    # caption is one horizontally centred line: keep the row-cluster with most ink, then components chained from centre
    rows = k.sum(axis=1); cy = int(np.argmax(np.convolve(rows, np.ones(31), "same")))
    for i in range(1, n):
        if keep[i] and abs(cen[i][1] - cy) > 30:
            keep[i] = False
    k = keep[lab]
    return k, small


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video"); ap.add_argument("--key", required=True); ap.add_argument("--out", required=True)
    a = ap.parse_args()
    od = os.path.join(a.out, a.key); os.makedirs(os.path.join(od, "sheets"), exist_ok=True)
    cmd = ["ffmpeg", "-nostdin", "-hide_banner", "-loglevel", "error", "-i", a.video,
           "-vf", f"crop={W}:{BH}:0:{Y0}", "-fps_mode", "passthrough", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    fsz = W * BH * 3
    rows, masks, crops = [], [], {}
    prev = None; seg_id = -1; segs = []; i = 0
    while True:
        buf = p.stdout.read(fsz)
        if len(buf) < fsz:
            break
        rgb = np.frombuffer(buf, np.uint8).reshape(BH, W, 3)
        m, small = mask_of(rgb)
        ink = int(m.sum())
        if ink >= MIN_INK:
            ys, xs = np.nonzero(m); bb = (int(xs.min()), int(xs.max()), int(ys.min()), int(ys.max()))
        else:
            bb = (-1, -1, -1, -1)
        rows.append((i, ink) + bb)
        present = ink >= MIN_INK
        if present:
            same = False
            if prev is not None:
                inter = np.logical_and(prev, m).sum(); uni = np.logical_or(prev, m).sum()
                same = uni > 0 and inter / uni >= IOU_SAME
            if not same:
                seg_id += 1; segs.append([seg_id, i, i])
            else:
                segs[-1][2] = i
            prev = m
            s = segs[-1]
            # keep the crop of the segment's 4th frame (after any pop-in scale animation), else the latest
            if i - s[1] <= 3:
                crops[s[0]] = (i, small.copy(), bb)
        else:
            prev = None
        i += 1
    p.wait()
    nframes = i
    with open(os.path.join(od, "caption_frames.csv"), "w", newline="") as f:
        w = csv.writer(f); w.writerow(["frame_index", "ink", "x0", "x1", "y0", "y1"]); w.writerows(rows)
    segs = [s for s in segs if s[2] - s[1] + 1 >= MIN_SEG]
    with open(os.path.join(od, "caption_segments.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["seg", "f_start", "f_end", "n_frames", "t_start", "t_end", "crop_frame", "x0", "x1", "y0", "y1"])
        for s in segs:
            cf, _, bb = crops[s[0]]
            w.writerow([s[0], s[1], s[2], s[2] - s[1] + 1, f"{(s[1] + 1) / 30:.3f}", f"{(s[2] + 2) / 30:.3f}", cf] + list(bb))
    # tile sheets
    TW, TH, LAB, COLS, ROWS = 360, 72, 16, 4, 15
    tiles = []
    for s in segs:
        cf, small, (x0, x1, y0, y1) = crops[s[0]]
        if x0 < 0:
            continue
        pad = 6
        c = small[max(0, y0 - pad):y1 + pad + 1, max(0, x0 - pad):x1 + pad + 1]
        sc = min((TW - 4) / c.shape[1], (TH - LAB - 2) / c.shape[0])
        c = cv2.resize(c, (max(1, int(c.shape[1] * sc)), max(1, int(c.shape[0] * sc))), interpolation=cv2.INTER_AREA)
        t = np.full((TH, TW, 3), 90, np.uint8)
        oy = LAB + (TH - LAB - c.shape[0]) // 2; ox = (TW - c.shape[1]) // 2
        t[oy:oy + c.shape[0], ox:ox + c.shape[1]] = c
        cv2.putText(t, f"s{s[0]} f{s[1]}-{s[2]}", (3, 12), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 255), 1, cv2.LINE_AA)
        tiles.append(cv2.cvtColor(t, cv2.COLOR_RGB2BGR))
    per = COLS * ROWS
    for k in range(0, len(tiles), per):
        ch = tiles[k:k + per]; r = (len(ch) + COLS - 1) // COLS
        sheet = np.zeros((r * TH, COLS * TW, 3), np.uint8)
        for j, t in enumerate(ch):
            rr, cc = divmod(j, COLS); sheet[rr * TH:(rr + 1) * TH, cc * TW:(cc + 1) * TW] = t
        cv2.imwrite(os.path.join(od, "sheets", f"{a.key}_cap_{k // per + 1:03d}.png"), sheet)
    print(a.key, "frames", nframes, "segments", len(segs), "sheets", (len(tiles) + per - 1) // per, flush=True)


if __name__ == "__main__":
    main()
