"""
make_ascii_svg.py
Converts a small grayscale image into monochrome ASCII art, then wraps it
in an SVG where each row "types" itself in one after another using SMIL
animation (<set>/<animate>). This works inside GitHub READMEs because
GitHub renders SVGs as <img> and browsers still run SMIL animations on
image-embedded SVGs.

Usage:
    python3 make_ascii_svg.py assets/portrait_small.png assets/ascii_portrait.svg
"""
import argparse
from PIL import Image

# Darkest -> lightest. Fewer, chunkier characters read better at small
# terminal font sizes than a long fine-grained ramp.
RAMP = "@%#*+=-:. "


def image_to_ascii_rows(path):
    img = Image.open(path).convert("L")
    w, h = img.size
    pixels = list(img.getdata())
    rows = []
    for y in range(h):
        row_chars = []
        for x in range(w):
            p = pixels[y * w + x]
            idx = int((p / 255) * (len(RAMP) - 1))
            row_chars.append(RAMP[idx])
        rows.append("".join(row_chars))
    return rows


def escape_xml(s):
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def build_svg(rows, char_w=8.6, char_h=15, font_size=13,
              fg="#39ff88", bg="#0d1117", row_delay=0.09,
              type_speed=0.012):
    n_rows = len(rows)
    n_cols = max(len(r) for r in rows)
    width = int(n_cols * char_w) + 20
    height = int(n_rows * char_h) + 20

    svg_parts = []
    svg_parts.append(
        f'<svg viewBox="0 0 {width} {height}" width="{width}" height="{height}" '
        f'xmlns="http://www.w3.org/2000/svg">'
    )
    svg_parts.append(f'<rect width="{width}" height="{height}" rx="10" fill="{bg}"/>')
    svg_parts.append(
        f'<style>text {{ font-family: "Courier New", monospace; '
        f'font-size: {font_size}px; fill: {fg}; white-space: pre; }}</style>'
    )

    # Each row is its own <text>, hidden until its reveal time via
    # <set attributeName="opacity">. A thin cursor rect blinks at the
    # currently-typing row to sell the "typing" illusion, then disappears.
    cursor_total = n_rows * row_delay + 0.6

    for i, row in enumerate(rows):
        y = 22 + i * char_h
        reveal_time = round(i * row_delay, 3)
        safe_row = escape_xml(row)
        svg_parts.append(
            f'<text x="12" y="{y}" opacity="0">{safe_row}'
            f'<set attributeName="opacity" to="1" begin="{reveal_time}s" fill="freeze"/>'
            f'</text>'
        )

    # Blinking cursor block that walks down the left edge while typing,
    # then fades out once the portrait is fully drawn.
    svg_parts.append(
        f'<rect x="12" y="{22 - font_size}" width="{char_w:.1f}" height="{font_size + 2}" fill="{fg}">'
        f'<animate attributeName="y" '
        f'values="{22 - font_size};{22 - font_size + (n_rows - 1) * char_h}" '
        f'dur="{n_rows * row_delay}s" begin="0s" fill="freeze"/>'
        f'<animate attributeName="opacity" values="1;0;1;0" dur="0.5s" '
        f'repeatCount="{int(n_rows * row_delay / 0.5) + 1}" begin="0s" '
        f'end="{cursor_total}s"/>'
        f'<set attributeName="opacity" to="0" begin="{cursor_total}s" fill="freeze"/>'
        f'</rect>'
    )

    svg_parts.append("</svg>")
    return "\n".join(svg_parts)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("src_image")
    parser.add_argument("dst_svg")
    parser.add_argument("--fg", default="#39ff88")
    parser.add_argument("--bg", default="#0d1117")
    args = parser.parse_args()

    rows = image_to_ascii_rows(args.src_image)
    svg = build_svg(rows, fg=args.fg, bg=args.bg)
    with open(args.dst_svg, "w") as f:
        f.write(svg)
    print(f"Saved {args.dst_svg} ({len(rows)} rows x {max(len(r) for r in rows)} cols)")
