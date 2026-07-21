"""
fetch_contributions.py
Pulls the last 12 months of contribution-calendar data for a GitHub user
via the GraphQL API and writes it to a small JSON file that
render_heatmap_svg.py turns into an SVG.

Requires a GitHub token with at least public read access, passed via the
GITHUB_TOKEN environment variable (the GitHub Actions workflow supplies
this automatically as ${{ secrets.GITHUB_TOKEN }}).

Usage:
    export GITHUB_TOKEN=ghp_xxx
    python3 fetch_contributions.py muhammadsaami assets/contributions.json
"""
import argparse
import json
import os
import sys
import urllib.request

QUERY = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks {
          contributionDays {
            date
            contributionCount
            weekday
          }
        }
      }
    }
  }
}
"""


def fetch(login, token):
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": login}}).encode(),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "profile-readme-heatmap",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        payload = json.loads(resp.read().decode())

    if "errors" in payload:
        raise RuntimeError(payload["errors"])

    calendar = payload["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    return calendar


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("login")
    parser.add_argument("dst_json")
    args = parser.parse_args()

    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("GITHUB_TOKEN env var not set.", file=sys.stderr)
        sys.exit(1)

    calendar = fetch(args.login, token)
    with open(args.dst_json, "w") as f:
        json.dump(calendar, f)
    print(f"Saved {args.dst_json}: {calendar['totalContributions']} total contributions")
