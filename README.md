# Red Devil Matrix

Static 64x64 Raspberry Pi HUB75 matrix display for a portrait image.

The image is rendered as red pixels only. Depth/shading comes from LED brightness: each source pixel is converted to `(red, 0, 0)`.

## Raspberry Pi Setup

```bash
cd ~
git clone https://github.com/timothyosm/red-devil-matrix.git
cd red-devil-matrix
./scripts/install_pi.sh
sudo ./scripts/run_waveshare.sh
```

## Manual Run

```bash
sudo ./.venv/bin/python3 devil_matrix.py \
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
  --sharpen 90 \
  --crop 70,30,1120,1080 \
  --min-red 1 \
  --max-red 245
```

## Preview

```bash
python3 devil_matrix.py --preview assets/processed/devil-red-preview.png
```

## Tuning

Show more face detail:

```bash
sudo ./scripts/run_waveshare.sh --tone-slope 4 --gamma 0.75 --detail 1.3
```

Push the contrast harder:

```bash
sudo ./scripts/run_waveshare.sh --tone-slope 8 --gamma 1.0 --max-red 255
```

Make it dimmer:

```bash
sudo ./scripts/run_waveshare.sh --brightness 45 --max-red 180
```

Use a different source image:

```bash
cp /path/to/image.png assets/source/portrait.png
python3 devil_matrix.py --source assets/source/portrait.png --output assets/processed/devil-red-64.png --preview assets/processed/devil-red-preview.png
sudo ./scripts/run_waveshare.sh
```

## systemd

```bash
sudo cp systemd/red-devil-matrix.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now red-devil-matrix
```
