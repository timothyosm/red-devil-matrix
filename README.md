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
  --contrast 1.15 \
  --gamma 0.5 \
  --black-point 1 \
  --white-point 92 \
  --detail 1.3 \
  --sharpen 130 \
  --crop 70,30,1120,1080
```

## Preview

```bash
python3 devil_matrix.py --preview assets/processed/devil-red-preview.png
```

## Tuning

Show more face detail:

```bash
sudo ./scripts/run_waveshare.sh --gamma 0.45 --detail 1.6 --contrast 1.0
```

Push the contrast harder:

```bash
sudo ./scripts/run_waveshare.sh --gamma 0.9 --black-point 4 --white-point 88
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
