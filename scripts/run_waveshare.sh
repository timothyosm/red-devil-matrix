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
  --padding 0 \
  --contrast 1.08 \
  --gamma 0.9 \
  --black-point 2 \
  --white-point 94 \
  --tone-slope 6 \
  --detail 1.1 \
  --detail-radius 2 \
  --sharpen 90 \
  --crop 70,30,1120,1080 \
  --min-red 1 \
  --max-red 245 \
  "$@"
