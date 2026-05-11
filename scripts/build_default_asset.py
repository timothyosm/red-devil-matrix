#!/usr/bin/env python3
"""Build the bundled source image from a simple high-resolution drawing."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets/source/devil.png"


def ellipse_layer(size: int, bbox: tuple[int, int, int, int], fill: tuple[int, int, int, int], blur: int = 0) -> Image.Image:
    layer = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    draw.ellipse(bbox, fill=fill)
    return layer.filter(ImageFilter.GaussianBlur(blur)) if blur else layer


def polygon_layer(size: int, points: list[tuple[int, int]], fill: tuple[int, int, int, int], blur: int = 0) -> Image.Image:
    layer = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    draw.polygon(points, fill=fill)
    return layer.filter(ImageFilter.GaussianBlur(blur)) if blur else layer


def main() -> None:
    size = 640
    image = Image.new("RGBA", (size, size), (0, 0, 0, 0))

    left_horn = [(8, 8), (222, 130), (60, 250), (8, 92)]
    right_horn = [(632, 8), (418, 130), (580, 250), (632, 92)]
    image.alpha_composite(polygon_layer(size, left_horn, (128, 15, 158, 255), 3))
    image.alpha_composite(polygon_layer(size, right_horn, (128, 15, 158, 255), 3))
    image.alpha_composite(polygon_layer(size, [(34, 26), (184, 112), (76, 204)], (205, 87, 231, 110), 18))
    image.alpha_composite(polygon_layer(size, [(606, 26), (456, 112), (564, 204)], (205, 87, 231, 110), 18))

    image.alpha_composite(ellipse_layer(size, (36, 32, 604, 610), (116, 0, 145, 255)))
    image.alpha_composite(ellipse_layer(size, (62, 64, 578, 586), (182, 39, 205, 255)))
    image.alpha_composite(ellipse_layer(size, (128, 156, 512, 520), (239, 163, 239, 210), 34))
    image.alpha_composite(ellipse_layer(size, (92, 194, 246, 360), (143, 0, 153, 95), 24))
    image.alpha_composite(ellipse_layer(size, (396, 194, 548, 360), (143, 0, 153, 95), 24))
    image.alpha_composite(ellipse_layer(size, (154, 58, 486, 96), (122, 0, 151, 255)))

    shadow = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw_shadow = ImageDraw.Draw(shadow)
    draw_shadow.arc((166, 318, 474, 520), 28, 152, fill=(23, 0, 30, 190), width=44)
    shadow = shadow.filter(ImageFilter.GaussianBlur(3))
    image.alpha_composite(shadow)

    features = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(features)
    draw.ellipse((220, 318, 278, 420), fill=(36, 0, 56, 245))
    draw.ellipse((362, 318, 420, 420), fill=(36, 0, 56, 245))
    draw.line((170, 288, 238, 300, 278, 332), fill=(31, 0, 48, 248), width=20)
    draw.line((470, 288, 402, 300, 362, 332), fill=(31, 0, 48, 248), width=20)
    draw.arc((180, 320, 460, 500), 35, 145, fill=(31, 0, 48, 248), width=18)
    features = features.filter(ImageFilter.GaussianBlur(1))
    image.alpha_composite(features)

    shine = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw_shine = ImageDraw.Draw(shine)
    draw_shine.ellipse((168, 82, 494, 236), fill=(255, 204, 255, 72))
    draw_shine.ellipse((426, 28, 588, 170), fill=(255, 202, 255, 44))
    shine = shine.filter(ImageFilter.GaussianBlur(22))
    image.alpha_composite(shine)

    SOURCE.parent.mkdir(parents=True, exist_ok=True)
    image.save(SOURCE)


if __name__ == "__main__":
    main()

