#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["pillow>=10"]
# ///
"""Finish a generated image for the web: exact size, web format, transparent background.

Run it with uv, which installs Pillow on the fly:
    uv run --script finish.py image.png --size 1200x630 --format webp
    uv run --script finish.py logo.png --transparent --format png

Steps, in this order (each one optional):
  --transparent [COLOR]  make a flat background transparent. Without COLOR the color is taken from the
                         corners. Only background connected to the image border is removed, so the same
                         color inside the subject stays. It is a color key, not a matting model: soft
                         shadows, gradients and fine hair are not separated cleanly.
  --size WxH             scale and crop to exactly W x H pixels (cover fit). "1200x" or "x630" scales
                         to that width or height and keeps the aspect ratio.
  --keep                 which part to keep when cropping: center (default), top, bottom, left, right,
                         top-left, top-right, bottom-left, bottom-right.
  --format               webp, jpeg, png, avif (default: the input's format; png for a transparent JPEG).

The result goes next to the input as <name>-<size>.<ext> unless -o gives a path. Nothing is written
into the skill's own folder.
"""
import argparse
import re
import sys
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageOps, features

SKILL_DIR = Path(__file__).resolve().parent.parent
KEEP = {
    "center": (0.5, 0.5), "top": (0.5, 0.0), "bottom": (0.5, 1.0), "left": (0.0, 0.5), "right": (1.0, 0.5),
    "top-left": (0.0, 0.0), "top-right": (1.0, 0.0), "bottom-left": (0.0, 1.0), "bottom-right": (1.0, 1.0),
}
FORMATS = {"webp": "WEBP", "jpeg": "JPEG", "jpg": "JPEG", "png": "PNG", "avif": "AVIF"}
EXTENSIONS = {"WEBP": ".webp", "JPEG": ".jpg", "PNG": ".png", "AVIF": ".avif"}
ALPHA_FORMATS = {"WEBP", "PNG", "AVIF"}


def parse_size(text):
    """'1200x630' -> (1200, 630); '1200x' -> (1200, None); 'x630' -> (None, 630)."""
    m = re.fullmatch(r"\s*(\d*)\s*[xX×]\s*(\d*)\s*", text or "")
    if not m or not (m.group(1) or m.group(2)):
        raise ValueError(f"Size must look like 1200x630, 1200x or x630, not {text!r}.")
    width, height = (int(v) if v else None for v in m.groups())
    if (width is not None and width < 1) or (height is not None and height < 1):
        raise ValueError("Width and height must be at least 1 pixel.")
    return width, height


def parse_color(text):
    """'#f0f0f0', 'f0f0f0' or '240,240,240' -> (240, 240, 240)."""
    text = text.strip()
    hex_match = re.fullmatch(r"#?([0-9a-fA-F]{6})", text)
    if hex_match:
        value = hex_match.group(1)
        return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))
    parts = [p.strip() for p in text.split(",")]
    if len(parts) == 3 and all(p.isdigit() and int(p) <= 255 for p in parts):
        return tuple(int(p) for p in parts)
    raise ValueError(f"Color must look like #f0f0f0 or 240,240,240, not {text!r}.")


def resize(image, width, height, keep="center"):
    """Cover fit to exactly width x height, or a proportional scale when one side is None."""
    if width and height:
        return ImageOps.fit(image, (width, height), Image.Resampling.LANCZOS, centering=KEEP[keep])
    if width:
        height = max(1, round(image.height * width / image.width))
    else:
        width = max(1, round(image.width * height / image.height))
    return image.resize((width, height), Image.Resampling.LANCZOS)


def corner_color(image):
    """The background color guessed from the four corners (their per-channel median)."""
    rgb = image.convert("RGB")
    w, h = rgb.size
    corners = [rgb.getpixel(xy) for xy in ((0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1))]
    return tuple(sorted(c[i] for c in corners)[1] for i in range(3))


def distance_map(rgb, color):
    """Per pixel, the largest channel difference to `color` (0 = same color), as an L image."""
    flat = Image.new("RGB", rgb.size, color)
    r, g, b = ImageChops.difference(rgb, flat).split()
    return ImageChops.lighter(ImageChops.lighter(r, g), b)


def remove_background(image, color=None, tolerance=24):
    """Make the background transparent: pixels within `tolerance` of `color` that connect to the border.

    Edge pixels next to the removed area get partial transparency, which softens the outline a little.
    Returns (RGBA image, color used, share of pixels removed).
    """
    color = color or corner_color(image)
    rgba = image.convert("RGBA")
    distance = distance_map(rgba.convert("RGB"), color)
    close = distance.point(lambda v: 255 if v <= tolerance else 0)
    w, h = close.size
    border = [(x, y) for x in range(w) for y in (0, h - 1)] + [(x, y) for y in range(h) for x in (0, w - 1)]
    for xy in border:
        if close.getpixel(xy) == 255:
            ImageDraw.floodfill(close, xy, 128)
    background = close.point(lambda v: 255 if v == 128 else 0)
    edge = ImageChops.subtract(background.filter(ImageFilter.MaxFilter(3)), background)
    ramp = distance.point(lambda v: 0 if v <= tolerance else min(255, (v - tolerance) * 255 // max(tolerance, 1)))
    alpha = rgba.getchannel("A")
    alpha = Image.composite(ImageChops.multiply(alpha, ramp), alpha, edge)
    alpha = Image.composite(Image.new("L", alpha.size, 0), alpha, background)
    rgba.putalpha(alpha)
    removed = background.histogram()[255] / (w * h)
    return rgba, color, removed


def output_path(source, out, fmt, size_label, transparent):
    if out:
        return Path(out)
    suffix = "-".join(part for part in (size_label, "transparent" if transparent else None) if part) or "web"
    return source.with_name(f"{source.stem}-{suffix}{EXTENSIONS[fmt]}")


def save(image, path, fmt, quality):
    if fmt == "JPEG":
        if image.mode in ("RGBA", "LA", "P"):
            image = image.convert("RGBA")
            flat = Image.new("RGB", image.size, (255, 255, 255))
            flat.paste(image, mask=image.getchannel("A"))
            image = flat
        image.convert("RGB").save(path, "JPEG", quality=quality, optimize=True, progressive=True)
    elif fmt == "PNG":
        image.save(path, "PNG", optimize=True)
    elif fmt == "WEBP":
        image.save(path, "WEBP", quality=quality, method=6)
    else:
        image.save(path, fmt, quality=quality)


def build_parser():
    ap = argparse.ArgumentParser(description="Finish an image for the web: exact size, web format, transparency.")
    ap.add_argument("input", help="image to finish")
    ap.add_argument("-o", "--out", help="output file (default: next to the input, e.g. hero-1200x630.webp)")
    ap.add_argument("--size", help="WxH for an exact size (cover fit and crop), or 1200x / x630 to scale")
    ap.add_argument("--keep", choices=KEEP, default="center", help="which part to keep when cropping")
    ap.add_argument("--format", choices=sorted(FORMATS), help="output format (default: the input's)")
    ap.add_argument("--quality", type=int, default=82, help="quality for webp, jpeg and avif, 1-100 (default 82)")
    ap.add_argument("--transparent", nargs="?", const="auto", metavar="COLOR",
                    help="make a flat background transparent (color from the corners, or e.g. #f0f0f0)")
    ap.add_argument("--tolerance", type=int, default=24,
                    help="how far a pixel may differ from the background color, 0-255 per channel (default 24)")
    return ap


def main(argv=None):
    a = build_parser().parse_args(argv)
    source = Path(a.input)
    if not source.is_file():
        sys.exit(f"Input image not found: {source}")
    if not 1 <= a.quality <= 100:
        sys.exit("--quality must be between 1 and 100.")
    if not 0 <= a.tolerance <= 255:
        sys.exit("--tolerance must be between 0 and 255.")
    try:
        width, height = parse_size(a.size) if a.size else (None, None)
        key = parse_color(a.transparent) if a.transparent not in (None, "auto") else None
    except ValueError as exc:
        sys.exit(str(exc))

    image = Image.open(source)
    image.load()
    out_suffix = Path(a.out).suffix.lower().lstrip(".") if a.out else ""
    if a.format and out_suffix in FORMATS and FORMATS[out_suffix] != FORMATS[a.format]:
        sys.exit(f"-o {a.out} does not match --format {a.format}.")
    if a.format:
        fmt = FORMATS[a.format]
    elif out_suffix in FORMATS:
        fmt = FORMATS[out_suffix]
    else:
        fmt = image.format or "PNG"
    if fmt not in EXTENSIONS:
        fmt = "PNG"
    if a.transparent and fmt not in ALPHA_FORMATS:
        if a.format or out_suffix in FORMATS:
            sys.exit("JPEG cannot store transparency; use png, webp or avif.")
        fmt = "PNG"
    if fmt == "AVIF" and not features.check("avif"):
        sys.exit("This Pillow build cannot write AVIF; use webp, or install Pillow 11.3 or newer.")

    if a.transparent:
        image, used, removed = remove_background(image, key, a.tolerance)
        print(f"Background #{used[0]:02x}{used[1]:02x}{used[2]:02x} made transparent: {removed:.0%} of the pixels.")
        if removed < 0.05:
            print("Warning: hardly anything was removed. The background may not be one flat color; try "
                  "--transparent with the exact color or a higher --tolerance.", file=sys.stderr)
    if width or height:
        image = resize(image, width, height, a.keep)

    path = output_path(source, a.out, fmt, a.size and f"{image.width}x{image.height}", bool(a.transparent))
    if path.resolve() == source.resolve():
        sys.exit("The output would overwrite the input; pass another path with -o.")
    if path.resolve().is_relative_to(SKILL_DIR):
        sys.exit(f"Refusing to write into the skill's folder ({SKILL_DIR}); pass -o with a project path.")
    path.parent.mkdir(parents=True, exist_ok=True)
    save(image, path, fmt, a.quality)
    print(f"Saved: {path} ({image.width}x{image.height}, {fmt}, {path.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
