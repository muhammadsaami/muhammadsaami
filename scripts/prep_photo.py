"""
prep_photo.py
Preprocess a portrait photo so it converts cleanly into ASCII art:
- crop to a centered square (face-focused)
- convert to grayscale
- resize to a small dense grid (ASCII width x height)
- apply slight contrast boost so ASCII shading reads well in a terminal

Usage:
    python3 prep_photo.py assets/portrait.png assets/portrait_small.png --width 60
"""
import argparse
from PIL import Image, ImageOps, ImageEnhance


def prep(src_path, dst_path, width=60, aspect_correction=0.55):
    img = Image.open(src_path).convert("RGB")

    # Center-crop to square using the shorter side
    w, h = img.size
    side = min(w, h)
    left = (w - side) // 2
    top = (h - side) // 2
    img = img.crop((left, top, left + side, top + side))

    # Grayscale + autocontrast so ASCII shading has full range
    img = ImageOps.grayscale(img)
    img = ImageOps.autocontrast(img, cutoff=1)

    # Slight contrast + sharpness boost helps facial features survive
    # the drop to a coarse character grid
    img = ImageEnhance.Contrast(img).enhance(1.25)
    img = ImageEnhance.Sharpness(img).enhance(1.5)

    # Terminal/monospace characters are taller than they are wide, so
    # we shrink the height relative to width to avoid a squashed look
    height = int(width * aspect_correction)
    img = img.resize((width, height), Image.LANCZOS)

    img.save(dst_path)
    print(f"Saved {dst_path} ({width}x{height})")
    return img


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("src")
    parser.add_argument("dst")
    parser.add_argument("--width", type=int, default=60)
    args = parser.parse_args()
    prep(args.src, args.dst, width=args.width)
