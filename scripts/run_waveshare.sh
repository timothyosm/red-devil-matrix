#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

PYTHON="${PYTHON:-./.venv/bin/python3}"
if [[ ! -x "$PYTHON" ]]; then
  PYTHON="$(command -v python3)"
fi

exec "$PYTHON" devil_matrix.py \
  --source assets/source/portrait.png \
  --output /tmp/red-devil-matrix-64.png \
  --hardware-mapping regular \
  --no-hardware-pulse \
  --rows 64 \
  --cols 64 \
  --gpio-slowdown 5 \
  --brightness 80 \
  --pwm-bits 8 \
  --contrast 1.6 \
  --gamma 1.45 \
  --black-point 8 \
  --white-point 96 \
  --min-red 1 \
  --max-red 255 \
  "$@"
