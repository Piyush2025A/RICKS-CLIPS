"""Shared helpers: ids, hashing, atomic IO, CSV, resource usage."""
import csv, hashlib, json, os, resource, subprocess, datetime
from . import VERSION

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def git_commit():
    try:
        return subprocess.check_output(["git", "-C", REPO, "rev-parse", "HEAD"], text=True,
                                       stderr=subprocess.DEVNULL).strip()
    except Exception:
        return "unknown"


def sha256_file(path, bufsize=1 << 20):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            b = f.read(bufsize)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def frame_id(prefix, idx):
    return f"{prefix}-f{idx:06d}"


def now_iso():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def peak_rss_mb():
    """Peak resident set (MB): self from /proc/self/status VmHWM (reset at exec; ru_maxrss is inherited across
    fork+exec from the parent, which inflated it when launched from a big parent), and waited-for children
    (ffmpeg/ffprobe) from ru_maxrss of RUSAGE_CHILDREN."""
    self_mb = None
    try:
        for ln in open("/proc/self/status"):
            if ln.startswith("VmHWM:"):
                self_mb = int(ln.split()[1]) / 1024.0
    except OSError:
        pass
    if self_mb is None:
        self_mb = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0
    c = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss / 1024.0
    return {"self_mb": round(self_mb, 1), "children_max_mb": round(c, 1)}


def atomic_write_text(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        f.write(text)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, path)


def write_json(path, obj):
    atomic_write_text(path, json.dumps(obj, indent=1, sort_keys=True) + "\n")


def _fmt(v):
    if isinstance(v, float):
        if v != v:
            return "nan"
        return format(v, ".7g")
    return str(v)


def write_csv(path, rows, fields):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(fields)
        for r in rows:
            w.writerow([_fmt(r.get(k, "")) for k in fields])
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, path)


def read_csv(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def tofloat(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return float("nan")


def dist(values):
    """n/median/IQR/min/max over finite values (measurement.schema 'distribution')."""
    import numpy as np
    a = np.array([v for v in values if v == v and abs(v) != float("inf")], dtype=float)
    if a.size == 0:
        return {}
    return {"median": float(np.median(a)), "p25": float(np.percentile(a, 25)),
            "p75": float(np.percentile(a, 75)), "min": float(a.min()), "max": float(a.max())}


def canonical_json(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False)


def config_fingerprint(params):
    """sha256 of the canonical JSON of all output-affecting parameters (floats NaN are not allowed)."""
    return hashlib.sha256(canonical_json(params).encode()).hexdigest()
