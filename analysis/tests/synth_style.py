"""Synthetic clips resembling the TARGET STYLE (flat colour fills, thin black outlines, simple geometric characters,
multi-layer parallax, camera pan/zoom, independent character motion) and their degraded encodings.
Deterministic, no randomness. 360x640. Ground truth is returned per clip.

Layers are periodic (period divides W) and shifted with np.roll by an INTEGER number of pixels per frame, so the
true per-layer motion is exact. Encodings of the same rendered frames: clean (yuv444p, CRF 0 = lossless),
q14 (yuv420p CRF 14), q35 (yuv420p CRF 35, preset veryfast), q45 (yuv420p CRF 45, ultrafast: harsh)."""
import json, os
import numpy as np
import cv2
import synth

W, H = synth.W, synth.H
BLK = (0, 0, 0)
VARIANTS = {"clean": dict(pix_fmt="yuv444p", crf=0), "q14": dict(pix_fmt="yuv420p", crf=14),
            "q35": dict(pix_fmt="yuv420p", crf=35, preset="veryfast"),
            "q45": dict(pix_fmt="yuv420p", crf=45, preset="ultrafast")}
PAL1 = dict(sky=(235, 200, 160), far=(170, 140, 120), mid=(120, 170, 200), near=(90, 170, 80), post=(60, 100, 150),
            body=(60, 60, 200), skin=(170, 200, 240))
PAL2 = dict(sky=(60, 40, 30), far=(110, 60, 90), mid=(80, 90, 150), near=(40, 90, 120), post=(150, 110, 60),
            body=(60, 200, 60), skin=(120, 160, 220))
PAL3 = dict(sky=(150, 230, 240), far=(100, 180, 120), mid=(200, 120, 160), near=(180, 150, 60), post=(60, 60, 60),
            body=(200, 100, 40), skin=(190, 210, 250))
LAYER_FACTORS = (0.25, 0.5, 1.0)  # far, mid, near parallax factors


def _layer(kind, pal, off=0):
    """-> (img BGR, mask bool) full-frame periodic layer. Flat fills + 2-3 px black outlines (cv2 LINE_8, no AA)."""
    img = np.zeros((H, W, 3), np.uint8)
    m = np.zeros((H, W), np.uint8)
    if kind == "far":  # mountains, period 120
        for x0 in range(-120 + off % 120, W + 120, 120):
            tri = np.array([[x0, 420], [x0 + 60, 300], [x0 + 120, 420]], np.int32)
            cv2.fillPoly(m, [tri], 255)
            cv2.fillPoly(img, [tri], pal["far"])
            cv2.polylines(img, [tri[:3]], False, BLK, 2)
        m[420:] = 255
        img[420:] = pal["far"]
    elif kind == "mid":  # buildings, period 180
        for x0 in range(-180 + off % 180, W + 180, 180):
            for (a, b, top) in ((20, 90, 380), (100, 160, 340)):
                cv2.rectangle(m, (x0 + a, top), (x0 + b, 520), 255, -1)
                cv2.rectangle(img, (x0 + a, top), (x0 + b, 520), pal["mid"], -1)
                cv2.rectangle(img, (x0 + a, top), (x0 + b, 520), BLK, 2)
    else:  # near: ground + fence posts, period 90
        m[520:] = 255
        img[520:] = pal["near"]
        cv2.line(img, (0, 520), (W, 520), BLK, 3)
        for x0 in range(-90 + off % 90, W + 90, 90):
            cv2.rectangle(m, (x0 + 10, 470), (x0 + 30, 520), 255, -1)
            cv2.rectangle(img, (x0 + 10, 470), (x0 + 30, 520), pal["post"], -1)
            cv2.rectangle(img, (x0 + 10, 470), (x0 + 30, 520), BLK, 2)
    return img, m > 0


_CACHE = {}


def layers(pal_name, pal, off=0):
    k = (pal_name, off)
    if k not in _CACHE:
        _CACHE[k] = [_layer(n, pal, off) for n in ("far", "mid", "near")]
    return _CACHE[k]


def background(pal_name, pal, k, cam_tx=0.0, factors=LAYER_FACTORS, zoom=1.0, off=0, parallax_layers=True):
    """Composite at frame k. cam_tx px/frame content motion (negative = content moves left) times factor per layer."""
    bg = np.full((H, W, 3), pal["sky"], np.uint8)
    for (img, m), f in zip(layers(pal_name, pal, off), factors):
        s = int(round(cam_tx * f * k))
        bg[np.roll(m, s, axis=1)] = np.roll(img, s, axis=1)[np.roll(m, s, axis=1)]
    if zoom != 1.0:
        z = zoom ** k
        M = np.array([[z, 0, (1 - z) * W / 2], [0, z, (1 - z) * H / 2]], np.float32)
        bg = cv2.warpAffine(bg, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
    return bg


def character(f, k, pal, x0=40, vx=2.0, base_y=520):
    """Simple geometric character (outlined flat shapes), moving in SCREEN space. Returns centre (cx, cy)."""
    cx = int(round(x0 + vx * k))
    by = base_y - int(round(3 * abs(np.sin(k * 0.5))))
    sw = int(round(7 * np.sin(k * 0.5)))
    for dx in (-8, 8):  # legs
        cv2.rectangle(f, (cx + dx - 5 + (sw if dx < 0 else -sw), by - 22), (cx + dx + 5 + (sw if dx < 0 else -sw), by), pal["post"], -1)
        cv2.rectangle(f, (cx + dx - 5 + (sw if dx < 0 else -sw), by - 22), (cx + dx + 5 + (sw if dx < 0 else -sw), by), BLK, 2)
    cv2.rectangle(f, (cx - 18, by - 80), (cx + 18, by - 20), pal["body"], -1)
    cv2.rectangle(f, (cx - 18, by - 80), (cx + 18, by - 20), BLK, 2)
    cv2.circle(f, (cx, by - 102), 22, pal["skin"], -1)
    cv2.circle(f, (cx, by - 102), 22, BLK, 2)
    cv2.circle(f, (cx - 7, by - 106), 2, BLK, -1)
    cv2.circle(f, (cx + 7, by - 106), 2, BLK, -1)
    return cx, by - 60


def scene_frames(n, pal_name="P1", cam_tx=0.0, factors=LAYER_FACTORS, zoom=1.0, char=True, char_vx=2.0, off=0, char_x0=40):
    pal = {"P1": PAL1, "P2": PAL2, "P3": PAL3}[pal_name]
    cs = []
    for k in range(n):
        f = background(pal_name, pal, k, cam_tx, factors, zoom, off)
        c = character(f, k, pal, x0=char_x0, vx=char_vx) if char else None
        cs.append(c)
        yield f, c


def encode_variants(frames, d, name, extra_fps=30, w=W, h=H):
    """Encode the SAME frame list in every variant -> {variant: path}."""
    frames = list(frames)
    out = {}
    for v, kw in VARIANTS.items():
        p = os.path.join(d, f"{name}__{v}.mp4")
        synth.encode(frames, p, fps=extra_fps, w=w, h=h, **kw)
        out[v] = p
    return out


def make_style(d):
    """Generate every style clip x variant. Returns {clip: {'truth':{...}, 'paths': {variant: path}}}."""
    os.makedirs(d, exist_ok=True)
    out = {}

    def reg(name, frames, truth):
        paths = encode_variants(frames, d, name)
        out[name] = {"truth": truth, "paths": paths}
        json.dump(truth, open(os.path.join(d, name + ".truth.json"), "w"), indent=1)

    n = 30
    # parallax: camera 4 px/frame (content moves left) with layer factors 0.25/0.5/1 -> -1/-2/-4 px per layer
    g = list(scene_frames(n, "P1", cam_tx=-4.0, char=False))
    reg("sty_par", [f for f, _ in g], {"frames": n, "layer_tx": {"far": -1.0, "mid": -2.0, "near": -4.0}})
    # rigid pan (all layers same depth) -3 px/frame + character walking independently +2 px/frame in screen space
    g = list(scene_frames(n, "P1", cam_tx=-3.0, factors=(1, 1, 1), char=True, char_vx=2.0))
    reg("sty_pan", [f for f, _ in g], {"frames": n, "tx": -3.0, "ty": 0.0, "scale": 1.0, "char_vel_x": 2.0,
                                       "char_centres": [list(c) for _, c in g]})
    # static camera, character only
    g = list(scene_frames(n, "P1", cam_tx=0.0, char=True, char_vx=2.0))
    reg("sty_static", [f for f, _ in g], {"frames": n, "tx": 0.0, "ty": 0.0, "scale": 1.0,
                                          "char_centres": [list(c) for _, c in g]})
    # zoom in 1.01 per frame (all layers), character walking in screen space
    g = list(scene_frames(n, "P1", zoom=1.01, char=True, char_vx=2.0))
    reg("sty_zoom", [f for f, _ in g], {"frames": n, "tx": 0.0, "ty": 0.0, "scale": 1.01})
    # shots: A(P1) | hard cut @30 | B(P2) | dissolve 59-70 -> C(P3) | white flash @90,91
    nn, cut, dz0, dz1 = 120, 30, 59, 70
    A = [f for f, _ in scene_frames(nn, "P1", cam_tx=-2.0, factors=(1, 1, 1))]
    B = [f for f, _ in scene_frames(nn, "P2", cam_tx=-2.0, factors=(1, 1, 1), off=37, char_x0=200)]
    Cc = [f for f, _ in scene_frames(nn, "P3", cam_tx=-2.0, factors=(1, 1, 1), off=71, char_x0=120)]
    fr = []
    for k in range(nn):
        if k < cut:
            f = A[k]
        elif k <= dz0:
            f = B[k]
        elif k < dz1:
            a = (k - dz0) / (dz1 - dz0)
            f = cv2.addWeighted(B[k], 1 - a, Cc[k], a, 0)
        else:
            f = Cc[k]
        for fk, al in ((90, 0.9), (91, 0.5)):
            if k == fk:
                f = cv2.addWeighted(f, 1 - al, np.full_like(f, 255), al, 0)
        fr.append(f)
    reg("sty_cut", fr, {"frames": nn, "hard_cuts": [cut], "dissolve": {"start": dz0, "end": dz1}, "flash": {"start": 90, "end": 91}})
    # hard cut between two scenes of the SAME palette (different layout): histograms almost identical
    A = [f for f, _ in scene_frames(60, "P1", cam_tx=-2.0, factors=(1, 1, 1))]
    B = [f for f, _ in scene_frames(60, "P1", cam_tx=-2.0, factors=(1, 1, 1), off=53, char_x0=220)]
    reg("sty_cut_same", A[:30] + B[30:], {"frames": 60, "hard_cuts": [30]})
    # outlines of known width on flat colour: coloured rectangles with black outline w = 1,2,3 (LINE_8, exact)
    fr, items = [], []
    for w_ in (1, 2, 3):
        f = np.full((H, W, 3), (200, 180, 120), np.uint8)
        for r_ in range(4):
            for c_ in range(2):
                x0, y0 = 30 + c_ * 160, 60 + r_ * 140
                f[y0:y0 + 100, x0:x0 + 120] = BLK  # exact w-px outline: black block, then inner fill
                f[y0 + w_:y0 + 100 - w_, x0 + w_:x0 + 120 - w_] = (90, 140, 220)
        gdark = int((cv2.cvtColor(f, cv2.COLOR_BGR2GRAY) < 60).sum())
        items.append({"w": w_, "dark_px": gdark, "perimeter": 8 * (2 * (120 + 100) - 4 * w_)})
        fr += [f] * 5
    reg("sty_outline", fr, {"items": items, "frames_per_item": 5, "H": H, "W": W})
    # flat colour patches (full frame) + a red|blue boundary frame (chroma subsampling bleed)
    fr, items = [], []
    for nm, bgr in (("red", (40, 40, 210)), ("green", (60, 190, 60)), ("blue", (200, 60, 40)), ("yellow", (30, 210, 220)),
                    ("gray", (128, 128, 128))):
        fr += [np.full((H, W, 3), bgr, np.uint8) for _ in range(5)]
        items.append({"name": nm, "bgr": bgr})
    f = np.full((H, W, 3), (40, 40, 210), np.uint8)
    f[:, W // 2:] = (200, 60, 40)
    fr += [f] * 5
    reg("sty_colour", fr, {"items": items, "boundary": {"left": (40, 40, 210), "right": (200, 60, 40)}})
    return out


if __name__ == "__main__":
    import sys
    r = make_style(sys.argv[1])
    print(len(r), "style clips in", sys.argv[1])
