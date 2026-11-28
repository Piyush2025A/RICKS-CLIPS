#!/usr/bin/env bash
# Wrapper: normalize.sh vo|mix|measure ...   (see normalize.py --help). Uses the analysis venv, isolated mode.
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
exec "$here/../../.venv-analysis/bin/python" -I "$here/normalize.py" "$@"
