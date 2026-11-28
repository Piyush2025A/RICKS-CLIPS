"""Shared helpers for the voice pipeline (A20). Stdlib + numpy only; audio via the ffmpeg binary."""
import hashlib, json, subprocess
import numpy as np

SCHEMA_VERSION = "1.0"

def frames(t, fps):
    """Seconds -> frame index by time (round half up), never by copying frame numbers across rates."""
    return int(np.floor(t * fps + 0.5))

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
