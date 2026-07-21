# Setup guide

This turns your GitHub profile README into a terminal-style page: an ASCII
portrait that types itself in, a neofetch-style info card, and a
contribution heatmap that refreshes daily on its own.

## 1. Create (or reuse) your profile repo

GitHub profile READMEs live in a special repo named exactly like your
username:

```
https://github.com/muhammadsaami/muhammadsaami
```

If it doesn't exist yet, create a new **public** repo with that exact name.

## 2. Copy these files in

Copy the whole contents of this folder into that repo:

```
README.md
SETUP.md
requirements-portrait.txt
requirements-daily.txt
assets/
  ascii_portrait.svg
  info_card.svg
  heatmap.svg
  contributions.json      (placeholder — Actions overwrites this)
scripts/
  prep_photo.py
  make_ascii_svg.py
  make_info_card.py
  fetch_contributions.py
  render_heatmap_svg.py
.github/
  workflows/
    update-heatmap.yml
```

## 3. Push it

```bash
cd muhammadsaami
git init   # if it's a fresh repo
git add .
git commit -m "feat: terminal-style profile README"
git branch -M main
git remote add origin https://github.com/muhammadsaami/muhammadsaami.git
git push -u origin main
```

## 4. Let the workflow take over

The included workflow (`.github/workflows/update-heatmap.yml`) runs once a
day and on manual trigger. It uses the repo's built-in `GITHUB_TOKEN`
(no secret setup needed) to pull your real contribution calendar and
re-render `assets/heatmap.svg`, then commits the change automatically.

To confirm it works right away instead of waiting for the schedule: open
the repo → **Actions** tab → **Update contribution heatmap** → **Run workflow**.

Two things to check first:
- Repo **Settings → Actions → General → Workflow permissions** is set to
  **"Read and write permissions"** (needed so the workflow can commit
  the refreshed heatmap back to the repo).
- The `login` argument in the workflow's fetch step matches your GitHub
  username (`muhammadsaami` — already set).

## 5. Regenerating the portrait or info card later

These two are static and only need to be rebuilt if you change your photo
or update your role/stack/projects — they are **not** touched by the
daily workflow.

```bash
pip install -r requirements-portrait.txt

# 1. Preprocess a new photo (crop, grayscale, resize)
python3 scripts/prep_photo.py assets/portrait.png assets/portrait_small.png --width 64

# 2. Re-render the typing ASCII portrait
python3 scripts/make_ascii_svg.py assets/portrait_small.png assets/ascii_portrait.svg

# 3. Edit the FIELDS / PROJECTS lists at the top of make_info_card.py,
#    then regenerate the card
python3 scripts/make_info_card.py assets/info_card.svg
```

Commit and push the updated SVGs — no Actions run needed for these.

## Notes

- The typing animation on the ASCII portrait uses SMIL (`<set>`/`<animate>`
  inside the SVG), which GitHub's image renderer supports even though the
  README itself has no JavaScript.
- If GitHub ever changes how it sanitizes embedded SVGs and the animation
  stops, the portrait still displays correctly as a static image — it just
  won't animate.
- Colors (`fg`/`bg` in `make_ascii_svg.py`, and the palette constants at
  the top of `make_info_card.py`/`render_heatmap_svg.py`) are easy to swap
  if you want a different terminal theme.
