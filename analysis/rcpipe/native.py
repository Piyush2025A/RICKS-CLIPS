"""Retrieve exact NATIVE-resolution frames by frame ID (for specialist visual inspection).

Frame ID `<key>-f<index>` = decode index in the native passthrough decode (no scaling, no fps filter). The frame is
re-decoded with the same command as the pipeline minus the scaler, saved as lossless PNG, and described in a JSON
sidecar (index, pts_time, native size, sha256 of the raw BGR bytes, input sha256, optional independent cross-check).
Nothing here is ever a proxy: proxy pipeline runs record `analysis_resolution.mode = proxy`, this tool is how a
specialist gets the native pixels behind any row."""
import os, re, subprocess
import numpy as np
import cv2
from . import probe as P, decode as D, common as C

_ID = re.compile(r"^(?P<key>.+)-f(?P<idx>\d{6})$")


def parse_ids(key, ids):
    out = []
    for x in ids:
        if isinstance(x, int):
            out.append(x)
            continue
        m = _ID.match(str(x))
        if not m or m.group("key") != key:
            raise ValueError(f"frame id {x!r} does not belong to key {key!r}")
        out.append(int(m.group("idx")))
    return out


def decode_select(path, video, index):
    """Independent decoder path: ffmpeg select filter (different code path from the streaming iterator)."""
    w, h = D.frame_shape(video)
    p = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", path, "-map", "0:v:0", "-vf", f"select=eq(n\\,{index})",
                        "-fps_mode", "passthrough", "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "bgr24", "-"],
                       capture_output=True, check=True)
    if len(p.stdout) != w * h * 3:
        raise RuntimeError(f"select decode of frame {index} returned {len(p.stdout)} bytes")
    return np.frombuffer(p.stdout, np.uint8).reshape(h, w, 3)


def get_frames(input_path, key, ids, out_dir, barcode_reader=None, cross_check=False, probe=None):
    """Write PNG + JSON for each requested frame. Returns list of sidecar dicts (and arrays under '_array').
    barcode_reader(img)->int: optional (synthetic media only) check that the pixels carry the requested index."""
    idx = sorted(set(parse_ids(key, ids)))
    pr = probe or P.probe(input_path)
    video, pts = pr["video"], pr["pts_time"]
    n = len(pts)
    bad = [i for i in idx if i < 0 or i >= n]
    if bad:
        raise IndexError(f"frame index {bad} out of range 0..{n - 1}")
    os.makedirs(out_dir, exist_ok=True)
    sha = C.sha256_file(input_path)
    want, res = set(idx), []
    last = max(idx) if idx else -1
    for i, fr in D.iter_frames(input_path, video, None):
        if i in want:
            fid = C.frame_id(key, i)
            png = os.path.join(out_dir, fid + ".png")
            cv2.imwrite(png, fr, [cv2.IMWRITE_PNG_COMPRESSION, 3])
            h, w = fr.shape[:2]
            side = {"frame_id": fid, "frame_index": i, "pts_time": pts[i], "png": os.path.basename(png),
                    "analysis_resolution": {"mode": "native", "width": w, "height": h, "native_width": w, "native_height": h},
                    "frame_bgr_sha256": __import__("hashlib").sha256(fr.tobytes()).hexdigest(), "input_sha256": sha,
                    "verified": {"decode_index": True}}
            if barcode_reader is not None:
                side["verified"]["barcode"] = bool(barcode_reader(fr) == i)
            if cross_check:
                side["verified"]["select_filter_bit_exact"] = bool(np.array_equal(decode_select(input_path, video, i), fr))
            C.write_json(os.path.join(out_dir, fid + ".json"), side)
            side["_array"] = fr.copy()
            res.append(side)
        if i >= last:
            break
    if len(res) != len(idx):
        raise RuntimeError(f"decoded only {len(res)} of {len(idx)} requested frames")
    return res
