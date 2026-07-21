"""
render_heatmap_svg.py
Turns the JSON produced by fetch_contributions.py into a GitHub-style
contribution heatmap SVG (weeks as columns, days as rows), colored with
the same green scale GitHub uses, plus a small streak/total summary line.

Usage:
    python3 render_heatmap_svg.py assets/contributions.json assets/heatmap.svg
"""
import argparse
import json
from datetime import datetime

BG = "#0d1117"
FG = "#c9d1d9"
CELL = 11
GAP = 3
MARGIN_LEFT = 30
MARGIN_TOP = 30

# GitHub's 5-step green scale (empty -> most active)
SCALE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]


def level_for(count, max_count):
    if count == 0:
        return 0
    if max_count == 0:
        return 1
    ratio = count / max_count
    if ratio > 0.75:
        return 4
    if ratio > 0.5:
        return 3
    if ratio > 0.25:
        return 2
    return 1


def build_svg(calendar):
    weeks = calendar["weeks"]
    total = calendar["totalContributions"]
    max_count = max(
        (day["contributionCount"] for week in weeks for day in week["contributionDays"]),
        default=0,
    )

    n_weeks = len(weeks)
    width = MARGIN_LEFT + n_weeks * (CELL + GAP) + 10
    height = MARGIN_TOP + 7 * (CELL + GAP) + 30

    svg = []
    svg.append(
        f'<svg viewBox="0 0 {width} {height}" width="{width}" height="{height}" '
        f'xmlns="http://www.w3.org/2000/svg">'
    )
    svg.append(f'<rect width="{width}" height="{height}" rx="10" fill="{BG}"/>')
    svg.append(
        f'<style>text {{ font-family: "Courier New", monospace; fill: {FG}; }}</style>'
    )
    svg.append(
        f'<text x="{MARGIN_LEFT}" y="20" font-size="13">'
        f'contributions (last 12 months): {total}</text>'
    )

    for wi, week in enumerate(weeks):
        for day in week["contributionDays"]:
            weekday = day["weekday"]
            count = day["contributionCount"]
            level = level_for(count, max_count)
            x = MARGIN_LEFT + wi * (CELL + GAP)
            y = MARGIN_TOP + weekday * (CELL + GAP)
            svg.append(
                f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="2" '
                f'fill="{SCALE[level]}"><title>{day["date"]}: {count}</title></rect>'
            )

    legend_y = height - 12
    legend_x = MARGIN_LEFT
    svg.append(f'<text x="{legend_x}" y="{legend_y}" font-size="11">Less</text>')
    lx = legend_x + 38
    for level, color in enumerate(SCALE):
        svg.append(
            f'<rect x="{lx}" y="{legend_y - 10}" width="{CELL}" height="{CELL}" '
            f'rx="2" fill="{color}"/>'
        )
        lx += CELL + GAP
    svg.append(f'<text x="{lx + 4}" y="{legend_y}" font-size="11">More</text>')

    svg.append("</svg>")
    return "\n".join(svg)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("src_json")
    parser.add_argument("dst_svg")
    args = parser.parse_args()

    with open(args.src_json) as f:
        calendar = json.load(f)

    svg = build_svg(calendar)
    with open(args.dst_svg, "w") as f:
        f.write(svg)
    print(f"Saved {args.dst_svg}")
