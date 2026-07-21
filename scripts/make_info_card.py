"""
make_info_card.py
Builds a neofetch-style "system info" SVG card populated with resume /
profile data (role, current + previous roles, stack, top projects).
Static SVG (no animation) so it always renders instantly next to the
ASCII portrait.

Usage:
    python3 make_info_card.py assets/info_card.svg
"""
import argparse

FG = "#c9d1d9"
ACCENT = "#39ff88"
LABEL = "#7ee787"
BG = "#0d1117"
FONT_SIZE = 13
LINE_H = 19
PAD_X = 18
PAD_TOP = 26

USER = "muhammadsaami"
HOST = "github"

FIELDS = [
    ("OS", "Backend Systems 22.6 LTS"),
    ("Role", "AI Backend Developer"),
    ("Now", "HeyBobo.AI \u2014 RAG pipelines & AI agent workflows"),
    ("Prev", "Roorq.com (backend) \u00b7 Phemsoft (AI + Healthcare)"),
    ("Shell", "FastAPI / Node.js / Express"),
    ("Stack", "Python \u00b7 LangChain \u00b7 LlamaIndex \u00b7 Pinecone \u00b7 React.js"),
    ("DB", "PostgreSQL \u00b7 MongoDB \u00b7 Supabase \u00b7 Pinecone"),
    ("Education", "M.Tech AI, UPES \u00b7 B.Tech, AMU"),
]

PROJECTS = [
    ("documind", "RAG-powered document Q&A platform"),
    ("MERN-Ecommerce-App", "Full-stack store with Stripe checkout"),
    ("MediCare-project", "Healthcare data + ML treatment planning"),
    ("Virtual-Mouse-Using-hand-gestures", "Real-time hand-gesture PC control"),
]


def esc(s):
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def build_svg(width=560):
    lines = []
    y = PAD_TOP

    lines.append((f"{USER}@{HOST}", "header"))
    lines.append(("-" * 34, "rule"))
    for label, value in FIELDS:
        lines.append((f"{label}: {value}", "field", label))
    lines.append(("", "spacer"))
    lines.append(("Top repos:", "subheader"))
    for name, desc in PROJECTS:
        lines.append((f"  {name} \u2014 {desc}", "project"))

    height = PAD_TOP + LINE_H * len(lines) + 18

    svg = []
    svg.append(
        f'<svg viewBox="0 0 {width} {height}" width="{width}" height="{height}" '
        f'xmlns="http://www.w3.org/2000/svg">'
    )
    svg.append(f'<rect width="{width}" height="{height}" rx="10" fill="{BG}"/>')
    svg.append(
        f'<style>'
        f'text {{ font-family: "Courier New", monospace; font-size: {FONT_SIZE}px; }}'
        f'.header {{ fill: {ACCENT}; font-weight: bold; }}'
        f'.rule {{ fill: #30363d; }}'
        f'.label {{ fill: {LABEL}; font-weight: bold; }}'
        f'.value {{ fill: {FG}; }}'
        f'.subheader {{ fill: {ACCENT}; font-weight: bold; }}'
        f'.project {{ fill: {FG}; }}'
        f'</style>'
    )

    cur_y = PAD_TOP
    for entry in lines:
        kind = entry[1]
        if kind == "field":
            label = entry[2]
            full_text = entry[0]
            value_text = full_text[len(label) + 2:]
            svg.append(
                f'<text x="{PAD_X}" y="{cur_y}">'
                f'<tspan class="label">{esc(label)}: </tspan>'
                f'<tspan class="value">{esc(value_text)}</tspan>'
                f'</text>'
            )
        else:
            text = entry[0]
            cls = kind if kind in ("header", "rule", "subheader") else "project"
            svg.append(f'<text x="{PAD_X}" y="{cur_y}" class="{cls}">{esc(text)}</text>')
        cur_y += LINE_H

    svg.append("</svg>")
    return "\n".join(svg)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("dst_svg")
    args = parser.parse_args()
    svg = build_svg()
    with open(args.dst_svg, "w") as f:
        f.write(svg)
    print(f"Saved {args.dst_svg}")
