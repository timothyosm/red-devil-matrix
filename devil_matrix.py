#!/usr/bin/env python3
"""Display an image as red-only brightness on a 64x64 HUB75 matrix."""

from __future__ import annotations

import argparse
import hashlib
import signal
import sys
import time
from pathlib import Path

try:
    from PIL import Image, ImageEnhance
except ImportError as error:
    raise SystemExit("Pillow is required. Install it with: sudo apt install python3-pil") from error


SIZE = 64
DEFAULT_SOURCE = Path(__file__).parent / "assets/source/portrait.png"
DEFAULT_PROCESSED = Path("/tmp/red-devil-matrix-64.png")


def clamp(value: float, lower: int = 0, upper: int = 255) -> int:
    return max(lower, min(upper, round(value)))


def parse_color(value: str) -> tuple[int, int, int]:
    parts = value.split(",")
    if len(parts) != 3:
        raise argparse.ArgumentTypeError("color must be R,G,B")

    try:
        color = tuple(clamp(int(part)) for part in parts)
    except ValueError as error:
        raise argparse.ArgumentTypeError("color must be numeric R,G,B") from error

    return color  # type: ignore[return-value]


def trim_transparency(image: Image.Image) -> Image.Image:
    alpha = image.getchannel("A")
    bbox = alpha.getbbox()

    if bbox is None:
        return image

    return image.crop(bbox)


def fit_square(image: Image.Image, size: int, padding: int) -> Image.Image:
    image = trim_transparency(image.convert("RGBA"))
    available = size - padding * 2
    image.thumbnail((available, available), Image.Resampling.LANCZOS)

    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    x_pos = (size - image.width) // 2
    y_pos = (size - image.height) // 2
    canvas.alpha_composite(image, (x_pos, y_pos))
    return canvas


def red_depth_image(
    source: Path,
    size: int,
    padding: int,
    gamma: float,
    contrast: float,
    min_red: int,
    max_red: int,
    black_point: float,
    white_point: float,
    alpha_threshold: int,
    background_red: int,
) -> Image.Image:
    image = Image.open(source)
    image = fit_square(image, size, padding)

    if contrast != 1.0:
        rgb = ImageEnhance.Contrast(image.convert("RGB")).enhance(contrast)
        image = Image.merge("RGBA", (*rgb.split(), image.getchannel("A")))

    source_pixels = list(image.getdata())
    luminance_values = [
        0.2126 * red + 0.7152 * green + 0.0722 * blue
        for red, green, blue, alpha in source_pixels
        if alpha > alpha_threshold
    ]
    luminance_values.sort()
    low_index = clamp(len(luminance_values) * black_point / 100, 0, max(0, len(luminance_values) - 1))
    high_index = clamp(len(luminance_values) * white_point / 100, 0, max(0, len(luminance_values) - 1))
    low = luminance_values[low_index] if luminance_values else 0
    high = luminance_values[high_index] if luminance_values else 255
    spread = max(1, high - low)

    pixels = []
    for red, green, blue, alpha in source_pixels:
        if alpha <= alpha_threshold:
            pixels.append((background_red, 0, 0))
            continue

        luminance = (0.2126 * red + 0.7152 * green + 0.0722 * blue - low) / spread
        luminance = max(0.0, min(1.0, luminance))
        alpha_ratio = alpha / 255
        level = (luminance ** gamma) * alpha_ratio
        output_red = min_red + level * (max_red - min_red)
        pixels.append((clamp(output_red), 0, 0))

    output = Image.new("RGB", (size, size))
    output.putdata(pixels)
    return output


def save_processed(args: argparse.Namespace) -> Image.Image:
    image = red_depth_image(
        source=args.source,
        size=args.size,
        padding=args.padding,
        gamma=args.gamma,
        contrast=args.contrast,
        min_red=args.min_red,
        max_red=args.max_red,
        black_point=args.black_point,
        white_point=args.white_point,
        alpha_threshold=args.alpha_threshold,
        background_red=args.background_red,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    image.save(args.output)
    return image


def image_fingerprint(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:12]


def save_preview(args: argparse.Namespace) -> None:
    image = save_processed(args)
    print(
        f"source={args.source} sha256={image_fingerprint(args.source)} "
        f"output={args.output} size={image.size}",
        flush=True,
    )
    preview = image.resize((args.size * args.preview_scale, args.size * args.preview_scale), Image.Resampling.NEAREST)
    args.preview.parent.mkdir(parents=True, exist_ok=True)
    preview.save(args.preview)


def run_matrix(args: argparse.Namespace) -> None:
    try:
        from rgbmatrix import RGBMatrix, RGBMatrixOptions
    except ImportError as error:
        raise SystemExit(
            "rgbmatrix is not installed. Run ./scripts/install_pi.sh on the Pi first."
        ) from error

    image = save_processed(args)

    options = RGBMatrixOptions()
    options.rows = args.rows
    options.cols = args.cols
    options.chain_length = args.chain_length
    options.parallel = args.parallel
    options.hardware_mapping = args.hardware_mapping
    options.gpio_slowdown = args.gpio_slowdown
    options.brightness = args.brightness
    options.pwm_bits = args.pwm_bits
    options.pwm_dither_bits = args.pwm_dither_bits
    options.pwm_lsb_nanoseconds = args.pwm_lsb_nanoseconds
    options.scan_mode = args.scan_mode
    options.multiplexing = args.multiplexing
    options.row_address_type = args.row_address_type
    options.led_rgb_sequence = args.rgb_sequence
    options.pixel_mapper_config = args.pixel_mapper
    options.panel_type = args.panel_type
    options.disable_hardware_pulsing = args.no_hardware_pulse
    options.limit_refresh_rate_hz = args.limit_refresh_rate_hz

    matrix = RGBMatrix(options=options)
    canvas = matrix.CreateFrameCanvas()
    running = True

    def stop(_signum: int, _frame: object) -> None:
        nonlocal running
        running = False

    signal.signal(signal.SIGINT, stop)
    signal.signal(signal.SIGTERM, stop)

    canvas.SetImage(image)
    canvas = matrix.SwapOnVSync(canvas)

    try:
        while running:
            time.sleep(0.25)
    finally:
        canvas.Clear()
        matrix.SwapOnVSync(canvas)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Display an image as red-only brightness on a 64x64 HUB75 matrix.")
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--output", type=Path, default=DEFAULT_PROCESSED)
    parser.add_argument("--preview", type=Path)
    parser.add_argument("--preview-scale", type=int, default=8)
    parser.add_argument("--size", type=int, default=64)
    parser.add_argument("--padding", type=int, default=1)
    parser.add_argument("--gamma", type=float, default=1.45)
    parser.add_argument("--contrast", type=float, default=1.6)
    parser.add_argument("--min-red", type=int, default=1)
    parser.add_argument("--max-red", type=int, default=255)
    parser.add_argument("--black-point", type=float, default=8.0)
    parser.add_argument("--white-point", type=float, default=96.0)
    parser.add_argument("--background-red", type=int, default=0)
    parser.add_argument("--alpha-threshold", type=int, default=10)
    parser.add_argument("--rows", type=int, default=64)
    parser.add_argument("--cols", type=int, default=64)
    parser.add_argument("--chain-length", type=int, default=1)
    parser.add_argument("--parallel", type=int, default=1)
    parser.add_argument("--hardware-mapping", default="regular")
    parser.add_argument("--gpio-slowdown", type=int, default=5)
    parser.add_argument("--brightness", type=int, default=80)
    parser.add_argument("--pwm-bits", type=int, default=8)
    parser.add_argument("--pwm-dither-bits", type=int, default=0)
    parser.add_argument("--pwm-lsb-nanoseconds", type=int, default=130)
    parser.add_argument("--scan-mode", type=int, default=0)
    parser.add_argument("--multiplexing", type=int, default=0)
    parser.add_argument("--row-address-type", type=int, default=0)
    parser.add_argument("--rgb-sequence", default="RGB")
    parser.add_argument("--pixel-mapper", default="")
    parser.add_argument("--panel-type", default="")
    parser.add_argument("--limit-refresh-rate-hz", type=int, default=120)
    parser.add_argument("--no-hardware-pulse", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()

    if args.preview:
        save_preview(args)
        return 0

    run_matrix(args)
    return 0


if __name__ == "__main__":
    sys.exit(main())
