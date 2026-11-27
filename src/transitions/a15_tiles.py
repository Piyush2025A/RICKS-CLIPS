"""A15 helper: extract per-frame tiles from rcpipe contact sheets and compose candidate strips (private outputs).
Usage as module. Sheets: 8 cols x 6 rows, tile 120 wide, row pitch 214 px (label band on top ~28 px)."""
import os, json, glob, re
import numpy as np, cv2
ROOT = os.path.expanduser('~/ricks-clips-private/analysis-data/rc30')
PITCH_Y, W = 214, 120
def tiles(key):
    out = {}
    for f in sorted(glob.glob(f'{ROOT}/v0.2.0/{key}/sheets/*.png')):
        a, b = map(int, re.search(r'_f(\d+)-f(\d+)\.png', f).groups())
        im = cv2.imread(f)
        for k, fi in enumerate(range(a, b + 1)):
            r, c = divmod(k, 8)
            out[fi] = im[r * PITCH_Y:(r + 1) * PITCH_Y, c * W:(c + 1) * W]
    return out
def content(t): return t[30:214]
def compose(T, rows, path, cols=10):
    """rows: list of lists of frame indices; each row placed on one tile-row (padded)."""
    H = len(rows) * PITCH_Y
    img = np.zeros((H, cols * W, 3), np.uint8)
    for r, fr in enumerate(rows):
        for c, fi in enumerate(fr[:cols]):
            if fi in T: img[r * PITCH_Y:(r + 1) * PITCH_Y, c * W:(c + 1) * W] = T[fi]
    cv2.imwrite(path, img)
def pick(a, b, n=10):
    fr = list(range(a, b + 1))
    if len(fr) <= n: return fr
    idx = np.linspace(0, len(fr) - 1, n).round().astype(int)
    return [fr[i] for i in idx]
