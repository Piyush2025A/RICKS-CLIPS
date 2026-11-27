"""Synthetic test media generators (numpy + OpenCV + system ffmpeg). Deterministic (fixed seeds). Output outside the
repo or in git-ignored dirs only. Ground truth is returned/stored as JSON next to each clip."""
import json, os, subprocess
import numpy as np
import cv2
import soundfile as sf

W, H = 360, 640


def smooth_noise(rng, h, w, sigmas=(1.5, 4.0, 10.0)):
    acc = np.zeros((h, w), np.float32)
    for s in sigmas:
        n = rng.standard_normal((h, w)).astype(np.float32)
        n = cv2.GaussianBlur(n, (0, 0), s)
        acc += n / (n.std() + 1e-6)
    acc = (acc - acc.min()) / (acc.max() - acc.min())
    return acc


def colorize(g, dark, light):
    dark, light = np.array(dark, np.float32), np.array(light, np.float32)
    return np.clip(dark + (light - dark) * g[..., None], 0, 255).astype(np.uint8)


def gray_texture(seed, h=2 * H, w=2 * W):
    g = smooth_noise(np.random.default_rng(seed), h, w)
    return colorize(g, (30, 40, 50), (220, 200, 190))


def put_barcode(img, idx, bits=16, bs=16):
    for b in range(bits):
        v = 255 if (idx >> b) & 1 else 0
        img[0:bs, b * bs:(b + 1) * bs] = v
    return img


def read_barcode(img, bits=16, bs=16):
    g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    v = 0
    for b in range(bits):
        if g[2:bs - 2, b * bs + 2:(b + 1) * bs - 2].mean() > 127:
            v |= 1 << b
    return v


def encode(frames, path, fps=30, vf=None, audio=None, crf=14, w=W, h=H, extra=(), pix_fmt="yuv420p", acodec=None,
           shortest=True, afilter=None, preset="fast"):
    """frames: iterable of BGR uint8. audio: wav path (muxed; mp4 -> aac, mkv -> pcm_s16le). vf: ffmpeg -vf string."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    cmd = ["ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{w}x{h}",
           "-framerate", str(fps), "-i", "-"]
    if audio:
        cmd += ["-i", audio]
    if vf:
        cmd += ["-vf", vf]
    cmd += ["-fps_mode", "passthrough", "-c:v", "libx264", "-preset", preset, "-crf", str(crf), "-pix_fmt", pix_fmt]
    if audio:
        if afilter:
            cmd += ["-af", afilter]
        ac = acodec or ("aac" if path.endswith(".mp4") else "pcm_s16le")
        cmd += ["-c:a", ac] + (["-b:a", "192k"] if ac == "aac" else [])
        cmd += ["-shortest"] if shortest else []
    cmd += list(extra) + [path]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    n = 0
    for f in frames:
        p.stdin.write(np.ascontiguousarray(f).tobytes())
        n += 1
    p.stdin.close()
    if p.wait() != 0:
        raise RuntimeError("ffmpeg encode failed " + path)
    return n


def hom(A, t):
    M = np.eye(3)
    M[:2, :2] = A
    M[:2, 2] = t
    return M


def camera_frames(n, tx=0.0, ty=0.0, scale=1.0, rot_deg=0.0, seed=1, tex=None, w=W, h=H):
    """Frame k = texture warped by cumulative step transform. Step (prev->cur): p' = c + A (p-c) + t,
    A = scale*R(rot) (rot positive = clockwise on screen, y down). Centre displacement per frame == (tx,ty)."""
    T = gray_texture(seed, 2 * h, 2 * w) if tex is None else tex
    th = np.deg2rad(rot_deg)
    A = scale * np.array([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]])
    step = hom(A, np.array([tx, ty]))
    cF = np.array([w / 2.0, h / 2.0])
    cT = np.array([T.shape[1] / 2.0, T.shape[0] / 2.0])
    Tr_in = hom(np.eye(2), -cT)
    Tr_out = hom(np.eye(2), cF)
    Mk = np.eye(3)
    for k in range(n):
        Mtot = Tr_out @ Mk @ Tr_in
        yield cv2.warpAffine(T, Mtot[:2], (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
        Mk = step @ Mk


def make_all(d):
    """Generate every test clip into directory d. Returns {name: {'path':..., 'truth':{...}}}."""
    os.makedirs(d, exist_ok=True)
    out = {}
    P = lambda n: os.path.join(d, n)

    def reg(name, path, truth):
        out[name] = {"path": path, "truth": truth}
        json.dump(truth, open(path + ".truth.json", "w"), indent=1)

    # 1. CFR 30 fps, exact count, barcode of decode index, slow pan
    n = 90
    fr = (put_barcode(f.copy(), k) for k, f in enumerate(camera_frames(n, tx=0.6, seed=11)))
    encode(fr, P("cfr30.mp4"), fps=30)
    reg("cfr30", P("cfr30.mp4"), {"frames": n, "fps": 30})

    # 2. VFR: frames 0-29 @24 Hz, 30-59 @30 Hz, 60-119 @60 Hz (timescale 90000)
    n = 120
    expr = "if(lt(N\\,30)\\,N/24\\,if(lt(N\\,60)\\,30/24+(N-30)/30\\,30/24+1+(N-60)/60))/TB"
    fr = (put_barcode(f.copy(), k) for k, f in enumerate(camera_frames(n, tx=0.6, seed=12)))
    encode(fr, P("vfr.mp4"), fps=30, vf=f"settb=1/90000,setpts={expr}", extra=["-enc_time_base:v", "1/90000", "-video_track_timescale", "90000", "-bf", "2"])
    pts = [k / 24 if k < 30 else (30 / 24 + (k - 30) / 30 if k < 60 else 30 / 24 + 1 + (k - 60) / 60) for k in range(n)]
    reg("vfr", P("vfr.mp4"), {"frames": n, "pts": pts})

    # 3. camera motion clips (24 frames each)
    cams = {"pan_x3": dict(tx=3.0, ty=0.0), "pan_xy": dict(tx=-2.5, ty=1.5), "zoom": dict(scale=1.01),
            "rot": dict(rot_deg=0.5), "still": dict(), "pan_sub": dict(tx=0.5, ty=-0.25),
            "combo": dict(tx=2.0, ty=-1.0, scale=1.005, rot_deg=-0.3)}
    for i, (nm, kw) in enumerate(cams.items()):
        encode(camera_frames(24, seed=20 + i, **kw), P(f"cam_{nm}.mp4"), fps=30)
        reg(f"cam_{nm}", P(f"cam_{nm}.mp4"), {"frames": 24, **{"tx": 0, "ty": 0, "scale": 1.0, "rot_deg": 0, **kw}})
    # low-texture clip: flat grey with a faint gradient, pan 3 px (motion must be flagged uncertain)
    flat = (np.linspace(100, 110, 2 * W, dtype=np.float32)[None, :, None] * np.ones((2 * H, 1, 3), np.float32)).astype(np.uint8)
    encode(camera_frames(24, tx=3.0, tex=flat), P("cam_flat.mp4"), fps=30)
    reg("cam_flat", P("cam_flat.mp4"), {"frames": 24, "tx": 3.0, "ty": 0.0, "low_texture": True})

    # 4. moving object over static / panning background
    def obj_clip(name, bg_tx, vel, seed):
        n, R = 30, 40
        bgf = list(camera_frames(n, tx=bg_tx, seed=seed))
        ot = colorize(smooth_noise(np.random.default_rng(seed + 100), 2 * R, 2 * R, (1.0, 3.0)), (0, 0, 120), (80, 255, 255))
        mask = np.zeros((2 * R, 2 * R), np.uint8)
        cv2.circle(mask, (R, R), R, 255, -1)
        cs, frames = [], []
        for k in range(n):
            cx, cy = 110 + vel[0] * k, 250 + vel[1] * k
            f = bgf[k].copy()
            x0, y0 = int(round(cx - R)), int(round(cy - R))
            roi = f[y0:y0 + 2 * R, x0:x0 + 2 * R]
            roi[mask > 0] = ot[mask > 0]
            frames.append(f)
            cs.append([x0 + R, y0 + R])
        encode(frames, P(name + ".mp4"), fps=30)
        reg(name, P(name + ".mp4"), {"frames": n, "bg_tx": bg_tx, "obj_vel": list(vel), "obj_centres": cs, "radius": R,
                                     "residual_expected_mag": float(np.hypot(vel[0] - bg_tx, vel[1]))})
    obj_clip("obj_static", 0.0, (4, 1), 31)
    obj_clip("obj_pan", -3.0, (4, 1), 32)

    # 5. shots: A | hard cut | B | crossfade | C ; flash frames. Clip 'shots' was used to tune thresholds;
    #    'shots2' (different seeds/palettes/positions/durations) was generated AFTER tuning as a hold-out.
    def shots_clip(name, n, cut, dz0, dz1, flash, seeds, pal, tx):
        gens = [list(camera_frames(n, tx=tx, tex=colorize(smooth_noise(np.random.default_rng(sd), 2 * H, 2 * W), *p)))
                for sd, p in zip(seeds, pal)]
        A, B, Cc = gens
        frames = []
        for k in range(n):
            if k < cut:
                f = A[k]
            elif k <= dz0:
                f = B[k]
            elif k < dz1:
                f = cv2.addWeighted(B[k], 1 - (k - dz0) / (dz1 - dz0), Cc[k], (k - dz0) / (dz1 - dz0), 0)
            else:
                f = Cc[k]
            for fk, al in flash:
                if k == fk:
                    f = cv2.addWeighted(f, 1 - al, np.full_like(f, 255), al, 0)
            frames.append(f)
        encode(frames, P(name + ".mp4"), fps=30)
        reg(name, P(name + ".mp4"), {"frames": n, "hard_cuts": [cut], "dissolve": {"start": dz0, "end": dz1},
                                     "flash": {"start": flash[0][0], "end": flash[-1][0]}})
    pal1 = [((60, 20, 10), (255, 160, 90)), ((10, 40, 90), (90, 170, 255)), ((30, 70, 20), (170, 255, 140))]
    shots_clip("shots", 120, 30, 59, 70, [(90, 0.9), (91, 0.5)], (40, 41, 42), pal1, 0.5)
    pal2 = [((80, 10, 60), (230, 120, 255)), ((60, 60, 10), (200, 230, 90)), ((10, 30, 120), (60, 120, 250))]
    shots_clip("shots2", 130, 20, 54, 67, [(100, 0.8)], (60, 61, 62), pal2, -0.7)

    # 6. colour: ramp (30 flat grey frames 20..220), solids (4 x 5), contrast (3 x 5, two-level halves)
    fr, truth = [], {"ramp": [], "solids": [], "contrast": []}
    for k in range(30):
        v = int(round(20 + 200 * k / 29))
        fr.append(np.full((H, W, 3), v, np.uint8))
        truth["ramp"].append(v)
    for nm, bgr in (("red", (0, 0, 220)), ("green", (0, 200, 0)), ("blue", (220, 0, 0)), ("gray", (128, 128, 128))):
        for _ in range(5):
            fr.append(np.full((H, W, 3), bgr, np.uint8))
        truth["solids"].append({"name": nm, "bgr": bgr, "n": 5})
    for dv in (10, 30, 60):
        for _ in range(5):
            f = np.full((H, W, 3), 100 + dv, np.uint8)
            f[:, : W // 2] = 100 - dv
            fr.append(f)
        truth["contrast"].append({"levels": [100 - dv, 100 + dv], "expected_std": float(dv)})
    encode(fr, P("color.mp4"), fps=30, crf=10)
    reg("color", P("color.mp4"), {**truth, "frames": len(fr)})

    # 7. blur series
    base = camera_frames(1, seed=50).__next__().copy()
    for k in range(6):
        cv2.rectangle(base, (30 + 50 * k, 100), (60 + 50 * k, 400 + 20 * k), (10, 10, 10) if k % 2 else (240, 240, 240), -1)
    sig = [0, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 6.0]
    fr = [base if s == 0 else cv2.GaussianBlur(base, (0, 0), s) for s in sig]
    encode(fr, P("blur.mp4"), fps=30, crf=10)
    reg("blur", P("blur.mp4"), {"frames": len(sig), "sigmas": sig})

    # 8. outlines of known width: black lines on white + 80x80 filled square
    widths = [1, 2, 3, 4, 5, 6, 8]
    fr, truth = [], []
    for w_ in widths:
        f = np.full((H, W, 3), 255, np.uint8)
        px, length = 0, 0
        for r in range(4):  # horizontal
            y = 60 + r * 40
            f[y:y + w_, 30:330] = 0
            px += w_ * 300
            length += 300
        for c in range(3):  # vertical
            x = 60 + c * 100
            f[300:600, x:x + w_] = 0
            px += w_ * 300
            length += 300
        f[400:460, 290:350] = 0  # 60x60 filled square, clear of the lines
        fr.append(f)
        truth.append({"w": w_, "line_px": px, "length": length})
    # recompute exact line pixels / square from the images (square may overlap the 3rd vertical line)
    for f, t in zip(fr, truth):
        t["dark_px"] = int((cv2.cvtColor(f, cv2.COLOR_BGR2GRAY) < 60).sum())
    encode(fr, P("outline.mp4"), fps=30, crf=8)
    reg("outline", P("outline.mp4"), {"frames": len(fr), "items": truth, "square": 60, "H": H, "W": W})

    # 9. audio clips (video: tiny flat 64x112 at 30 fps)
    sr = 48000
    tiny = lambda n: (np.full((112, 64, 3), 60, np.uint8) for _ in range(n))
    t = lambda sec: np.arange(int(sec * sr)) / sr
    seg = np.concatenate([0.1 * np.sin(2 * np.pi * 440 * t(1.5)), 0.1 * np.sin(2 * np.pi * 1000 * t(1.5)),
                          0.1 * np.sin(2 * np.pi * 2500 * t(1.5))]).astype(np.float32)
    sf.write(P("tones.wav"), seg, sr, subtype="FLOAT")
    encode(tiny(135), P("aud_tones.mkv"), fps=30, audio=P("tones.wav"), w=64, h=112)
    reg("aud_tones", P("aud_tones.mkv"), {"segments": [[0, 1.5, 440], [1.5, 3.0, 1000], [3.0, 4.5, 2500]],
                                          "tone_amp": 0.1})
    rng = np.random.default_rng(7)
    y = (rng.standard_normal(int(4.0 * sr)) * 1e-4).astype(np.float32)  # ~ -80 dBFS floor
    clicks = [0.5, 1.3, 2.1, 3.0]
    for c in clicks:
        i0 = int(c * sr)
        n_ = int(0.005 * sr)
        y[i0:i0 + n_] += (rng.standard_normal(n_) * np.exp(-np.arange(n_) / (0.001 * sr)) * 0.8).astype(np.float32)
    sf.write(P("clicks.wav"), y, sr, subtype="FLOAT")
    encode(tiny(120), P("aud_clicks.mkv"), fps=30, audio=P("clicks.wav"), w=64, h=112)
    reg("aud_clicks", P("aud_clicks.mkv"), {"clicks_s": clicks})
    for nm, lufs, ext in (("loud23", -23.0, "mkv"), ("loud16", -16.0, "mkv"), ("loud23_aac", -23.0, "mp4")):
        amp = 10 ** ((lufs + 3.01) / 20)  # 997 Hz sine: LUFS = 20log10(A) - 3.01
        y = (amp * np.sin(2 * np.pi * 997 * t(8.0))).astype(np.float32)
        sf.write(P(nm + ".wav"), y, sr, subtype="FLOAT")
        encode(tiny(240), P(f"aud_{nm}.{ext}"), fps=30, audio=P(nm + ".wav"), w=64, h=112)
        reg(f"aud_{nm}", P(f"aud_{nm}.{ext}"), {"expected_lufs": lufs, "amp": amp,
                                                  "expected_tp_dbtp": 20 * np.log10(amp), "expected_rms_dbfs": 20 * np.log10(amp / 2 ** .5)})
    # 10. audio coverage faults (video: tiny flat 64x112 at 30 fps)
    # 10a audio shorter than video: 3.0 s of tones under 5.0 s of video
    sf.write(P("short.wav"), seg[: int(3.0 * sr)], sr, subtype="FLOAT")
    encode(tiny(150), P("aud_short.mkv"), fps=30, audio=P("short.wav"), w=64, h=112, shortest=False)
    reg("aud_short", P("aud_short.mkv"), {"video_s": 5.0, "audio_s": 3.0, "missing": [[3.0, 5.0]]})
    # 10b gap: tones with 1.0-1.6 s of audio frames DROPPED but timestamps kept (pts discontinuity)
    encode(tiny(135), P("aud_gap.mkv"), fps=30, audio=P("tones.wav"), w=64, h=112,
           afilter="aselect='not(between(t,1.0,1.6))'")
    reg("aud_gap", P("aud_gap.mkv"), {"video_s": 4.5, "gap": [1.0, 1.6]})
    # 10c video without any audio stream
    encode(tiny(90), P("aud_none.mkv"), fps=30, w=64, h=112)
    reg("aud_none", P("aud_none.mkv"), {})
    # 10d corrupt audio: AAC-in-mkv whose packet payload bytes between 1.0 and 2.0 s (partial) or everywhere (full)
    # are overwritten with seeded random bytes (container structure stays intact, video untouched)
    encode(tiny(135), P("aud_aac_clean.mkv"), fps=30, audio=P("tones.wav"), w=64, h=112, acodec="aac")
    pk = json.loads(subprocess.run(["ffprobe", "-v", "error", "-of", "json", "-select_streams", "a:0", "-show_entries",
                                    "packet=pts_time,pos,size", P("aud_aac_clean.mkv")], capture_output=True, text=True).stdout)["packets"]
    for nm, lo, hi in (("partial", 1.0, 2.0), ("full", -1.0, 99.0)):
        b = bytearray(open(P("aud_aac_clean.mkv"), "rb").read())
        r_ = np.random.default_rng(5)
        n_hit = 0
        for q in pk:
            if lo <= float(q["pts_time"]) < hi:
                a = int(q["pos"]) + 4  # skip matroska block header (track vint, 2 B timecode, flags)
                z = a + int(q["size"])
                b[a:z] = r_.integers(0, 256, z - a, dtype=np.uint8).tobytes()
                n_hit += 1
        open(P(f"aud_corrupt_{nm}.mkv"), "wb").write(bytes(b))
        reg(f"aud_corrupt_{nm}", P(f"aud_corrupt_{nm}.mkv"), {"corrupt_packets": n_hit, "of": len(pk), "window": [lo, hi]})
    return out


if __name__ == "__main__":
    import sys
    r = make_all(sys.argv[1])
    print(len(r), "clips in", sys.argv[1])
