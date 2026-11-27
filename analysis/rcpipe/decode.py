"""Stage 2: native decode through an ffmpeg rawvideo pipe, no resampling of time (passthrough)."""
import subprocess, tempfile
import numpy as np


def frame_shape(video, proxy_width=None):
    w, h = video["width"], video["height"]
    if abs(video.get("rotation", 0)) in (90, 270):  # ffmpeg autorotates
        w, h = h, w
    if proxy_width and proxy_width < w:
        h = int(2 * round(h * proxy_width / w / 2))
        w = int(proxy_width)
    return w, h


def decode_cmd(path, w, h, scale):
    cmd = ["ffmpeg", "-nostdin", "-v", "error", "-i", path, "-map", "0:v:0", "-fps_mode", "passthrough"]
    if scale:
        cmd += ["-vf", f"scale={w}:{h}:flags=area"]
    return cmd + ["-f", "rawvideo", "-pix_fmt", "bgr24", "-"]


def iter_frames(path, video, proxy_width=None):
    """Yield (index, BGR uint8 HxWx3). Streams; never holds more than one frame."""
    w, h = frame_shape(video, proxy_width)
    scale = bool(proxy_width and proxy_width < frame_shape(video)[0])
    n = w * h * 3
    err = tempfile.TemporaryFile()
    p = subprocess.Popen(decode_cmd(path, w, h, scale), stdout=subprocess.PIPE, stderr=err, bufsize=n * 2)
    i = 0
    finished = False
    try:
        while True:
            buf = p.stdout.read(n)
            if len(buf) == 0:
                finished = True
                break
            if len(buf) < n:
                raise RuntimeError(f"truncated frame at index {i}: {len(buf)}/{n} bytes")
            yield i, np.frombuffer(buf, np.uint8).reshape(h, w, 3)
            i += 1
    finally:
        if not finished:  # consumer stopped early (or error): do not wait for the whole stream
            p.kill()
        p.stdout.close()
        rc = p.wait()
        err.seek(0)
        msg = err.read().decode(errors="replace").strip()
        err.close()
        if finished and rc != 0:
            raise RuntimeError(f"ffmpeg exit {rc}: {msg[:500]}")
