#!/usr/bin/env bash
# Reproducible, idempotent setup of the reference-analysis Python environment.
# PROPOSED FOR REVIEW (Phase 2). Not yet run; not saved as the cloud environment's setup script.
#
# Usage: bash setup/setup-analysis.sh [--with-audio]
#   Creates .venv-analysis/ at the repo root (git-ignored) from hash-pinned lock files.
#   Re-running is a no-op when the lock file is unchanged.
# Scope: reference analysis only (Phase 3). Rendering dependencies (Node/Remotion/three) are separate and are
# pinned later in package.json by A25 after approval. Installs nothing system-wide, downloads no tools.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV="$ROOT/.venv-analysis"
LOCK="$ROOT/setup/requirements-analysis.lock"
[[ "${1:-}" == "--with-audio" ]] && LOCK="$ROOT/setup/requirements-analysis-audio.lock"
PY="${PYTHON:-python3}"

# 1. Preconditions (fail early, change nothing)
"$PY" -c 'import sys; assert sys.version_info[:2] == (3, 13), f"need Python 3.13, found {sys.version.split()[0]}"'
command -v ffmpeg >/dev/null && command -v ffprobe >/dev/null || { echo "ffmpeg/ffprobe missing" >&2; exit 1; }

# 2. Skip if this exact lock is already installed
STAMP="$VENV/.lock-sha256"
WANT="$(sha256sum "$LOCK" | cut -d' ' -f1)"
if [[ -f "$STAMP" && "$(cat "$STAMP")" == "$WANT" ]]; then
  echo "analysis venv up to date ($(basename "$LOCK"))"; exit 0
fi

# 3. Create venv (isolated from system site-packages) and install hash-pinned binary wheels only
[[ -x "$VENV/bin/python" ]] || "$PY" -m venv "$VENV"
"$VENV/bin/python" -m pip install --disable-pip-version-check --no-input --quiet \
  --require-hashes --only-binary=:all: --no-deps -r "$LOCK"
"$VENV/bin/python" -m pip check

# 4. Smoke test (imports + versions), then stamp
"$VENV/bin/python" -I - <<'PYEOF'
import cv2, numpy, scipy, skimage, soundfile, matplotlib, PIL
print("cv2", cv2.__version__, "| numpy", numpy.__version__, "| scipy", scipy.__version__,
      "| skimage", skimage.__version__, "| soundfile", soundfile.__version__, "| libsndfile", soundfile.__libsndfile_version__)
try:
    import librosa; print("librosa", librosa.__version__)
except ImportError:
    print("librosa not installed (core tier)")
PYEOF
echo "$WANT" > "$STAMP"
echo "analysis venv ready: $VENV"
