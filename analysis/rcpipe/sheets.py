"""Stage 11: contact sheets (AIDS for visual inspection; producing them is NOT visual inspection)."""
import os
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont

FOOT = "contact-sheet aid (computational output) - not a visual inspection record"


def _tile(img_bgr, label, tw):
    s = tw / img_bgr.shape[1]
    im = cv2.resize(img_bgr, (tw, int(round(img_bgr.shape[0] * s))), interpolation=cv2.INTER_AREA)
    pil = Image.fromarray(cv2.cvtColor(im, cv2.COLOR_BGR2RGB))
    d = ImageDraw.Draw(pil)
    font = ImageFont.load_default()
    for line_i, line in enumerate(label):
        y = 2 + line_i * 11
        d.rectangle([0, y - 1, tw, y + 10], fill=(0, 0, 0))
        d.text((2, y), line, fill=(255, 255, 0), font=font)
    return np.asarray(pil)


def make_sheets(frame_iter, key, pts, outdir, select, tile_w=120, cols=8, per_sheet=48):
    """frame_iter yields (idx, bgr). select(idx)->bool. Streams; keeps only one sheet's tiles in memory.
    Returns list of {file, frame_indices, tile_width}."""
    os.makedirs(outdir, exist_ok=True)
    tiles, idxs, made = [], [], []

    def flush():
        if not tiles:
            return
        th = tiles[0].shape[0]
        rows = (len(tiles) + cols - 1) // cols
        canvas = np.zeros((rows * th + 14, cols * tile_w, 3), np.uint8)
        for k, t in enumerate(tiles):
            r, c = divmod(k, cols)
            canvas[r * th:(r + 1) * th, c * tile_w:(c + 1) * tile_w] = t
        pil = Image.fromarray(canvas)
        ImageDraw.Draw(pil).text((2, rows * th + 2), FOOT, fill=(200, 200, 200), font=ImageFont.load_default())
        fn = os.path.join(outdir, f"{key}_sheet_f{idxs[0]:06d}-f{idxs[-1]:06d}.png")
        pil.save(fn, optimize=True, compress_level=9)
        made.append({"file": fn, "frame_indices": list(idxs), "tile_width": tile_w, "cols": cols})
        tiles.clear()
        idxs.clear()

    for i, f in frame_iter:
        if select(i):
            t = pts[i] if i < len(pts) else float("nan")
            tiles.append(_tile(f, [f"{key}-f{i:06d}", f"t={t:.3f}s"], tile_w))
            idxs.append(i)
            if len(tiles) == per_sheet:
                flush()
    flush()
    return made
