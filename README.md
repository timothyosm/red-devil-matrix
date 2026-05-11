# Red Devil Matrix

Static 64x64 Raspberry Pi HUB75 matrix display for a devil-face image.

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
  --source assets/source/devil.png \
  --hardware-mapping regular \
  --no-hardware-pulse \
  --rows 64 \
  --cols 64 \
  --gpio-slowdown 5 \
  --brightness 80 \
  --pwm-bits 8
```

## Preview

```bash
python3 devil_matrix.py --preview assets/processed/devil-red-preview.png
```

## Tuning

Increase contrast:

```bash
sudo ./scripts/run_waveshare.sh --contrast 1.35 --gamma 0.8
```

Make it dimmer:

```bash
sudo ./scripts/run_waveshare.sh --brightness 45 --max-red 180
```

Use a different source image:

```bash
cp /path/to/image.png assets/source/devil.png
python3 devil_matrix.py --preview assets/processed/devil-red-preview.png
sudo ./scripts/run_waveshare.sh
```

## systemd

```bash
sudo cp systemd/red-devil-matrix.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now red-devil-matrix
```

