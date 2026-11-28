"""Shared helpers for the voice pipeline (A20). Stdlib + numpy only; audio via the ffmpeg binary."""
import hashlib, json, math, subprocess
import numpy as np

SCHEMA_VERSION = "1.0"

def seconds_to_frame(t, fps):
    """Canonical seconds -> frame (CONTRACT.md): round half up on integer microseconds, exact integer arithmetic.
    us = floor(t*1e6 + 0.5); frame = (us*fps + 500000) // 1000000. Must match src/contracts/time.ts bit-for-bit."""
    if isinstance(fps, bool) or not isinstance(fps, int) or fps <= 0:
        raise ValueError(f"fps must be a positive integer, got {fps!r}")
    t = float(t)
    if not math.isfinite(t) or t < 0:
        raise ValueError(f"t must be finite and >= 0, got {t!r}")
    us = math.floor(t * 1_000_000 + 0.5)
    return (us * fps + 500_000) // 1_000_000

def duration_frames_covering(t, fps):
    """Duration rule (D039): smallest integer N with N/fps >= t, so media is never truncated. Exact integer ceil on
    integer microseconds: us = floor(t*1e6 + 0.5); N = -((-us*fps) // 1_000_000). t == 0 -> 0.
    Event timestamps keep seconds_to_frame. Must match durationFramesCovering in src/contracts/time.ts."""
    if isinstance(fps, bool) or not isinstance(fps, int) or fps <= 0:
        raise ValueError(f"fps must be a positive integer, got {fps!r}")
    t = float(t)
    if not math.isfinite(t) or t < 0:
        raise ValueError(f"t must be finite and >= 0, got {t!r}")
    us = math.floor(t * 1_000_000 + 0.5)
    return -((-us * fps) // 1_000_000)

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()

def decode_audio(path, sr=48000):
    """Decode any audio file to mono float32 at sr via ffmpeg. Returns (samples, sr)."""
    cmd = ["ffmpeg", "-v", "error", "-i", path, "-f", "f32le", "-ac", "1", "-ar", str(sr), "-"]
    out = subprocess.run(cmd, capture_output=True, check=True).stdout
    return np.frombuffer(out, dtype="<f4").astype(np.float32), sr

def audio_duration(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                       capture_output=True, text=True, check=True)
    return float(r.stdout.strip())

def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def dump_json(obj, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)
        f.write("\n")
