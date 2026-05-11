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
  --brightness 85 \
  --pwm-bits 8 \
  --contrast 1.15 \
  --gamma 0.5 \
  --black-point 1 \
  --white-point 92 \
  --detail 1.3 \
  --detail-radius 2 \
  --sharpen 130 \
  --crop 70,30,1120,1080 \
  --min-red 1 \
  --max-red 255 \
  "$@"
