#!/usr/bin/env python3
"""Generate the README badges as local SVG files in the same style as GitHub's own workflow badges.

Static badges are always rewritten. The two live badges (latest release, stars) are refreshed from the
GitHub API when --repo is given. If the API is not reachable, an existing file is kept.

    python .github/scripts/make_badges.py --repo jakubcurik/nano-banana
"""
import argparse
import json
import os
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE.parent.parent / "assets" / "badges"
WIDTHS = json.loads((HERE / "verdana_widths.json").read_text(encoding="utf-8"))

STATIC = {
    "license-mit.svg": ("license", "MIT"),
    "claude-code-plugin.svg": ("Claude Code", "plugin"),
    "agent-skills.svg": ("Agent Skills", "compatible"),
    "python.svg": ("python", "3.11+"),
    "gemini-api.svg": ("Gemini API", "Nano Banana"),
}


def text_width(text):
    return sum(WIDTHS.get(ch, 7.0) for ch in text)


def esc(text):
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def badge(label, value):
    """The same look as GitHub's workflow badges: dark gradient label, green gradient value, 3 px corners."""
    lw = round(text_width(label) + 11, 2)
    vw = round(text_width(value) + 8, 2)
    total = round(lw + vw, 2)
    lx, vx = round(lw / 2, 2), round(lw + vw / 2, 2)
    ltw, vtw = round(text_width(label), 2), round(text_width(value), 2)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{total}" height="20" role="img" aria-label="{esc(label)}: {esc(value)}">
  <title>{esc(label)}: {esc(value)}</title>
  <defs>
    <linearGradient id="l" x1="50%" y1="0%" x2="50%" y2="100%"><stop stop-color="#444D56" offset="0%"/><stop stop-color="#24292E" offset="100%"/></linearGradient>
    <linearGradient id="v" x1="50%" y1="0%" x2="50%" y2="100%"><stop stop-color="#34D058" offset="0%"/><stop stop-color="#28A745" offset="100%"/></linearGradient>
  </defs>
  <g fill="none" fill-rule="evenodd" font-family="'DejaVu Sans',Verdana,Geneva,sans-serif" font-size="11" text-anchor="middle">
    <path d="M0,3 C0,1.343 1.343,0 3,0 L{lw},0 L{lw},20 L3,20 C1.343,20 0,18.657 0,17 Z" fill="url(#l)"/>
    <path d="M{lw},0 L{total - 3},0 C{total - 1.343},0 {total},1.343 {total},3 L{total},17 C{total},18.657 {total - 1.343},20 {total - 3},20 L{lw},20 Z" fill="url(#v)"/>
    <text x="{lx}" y="15" fill="#010101" fill-opacity=".3" textLength="{ltw}" lengthAdjust="spacingAndGlyphs" aria-hidden="true">{esc(label)}</text>
    <text x="{lx}" y="14" fill="#FFFFFF" textLength="{ltw}" lengthAdjust="spacingAndGlyphs">{esc(label)}</text>
    <text x="{vx}" y="15" fill="#010101" fill-opacity=".3" textLength="{vtw}" lengthAdjust="spacingAndGlyphs" aria-hidden="true">{esc(value)}</text>
    <text x="{vx}" y="14" fill="#FFFFFF" textLength="{vtw}" lengthAdjust="spacingAndGlyphs">{esc(value)}</text>
  </g>
</svg>
"""


def github_api(repo, path):
    request = urllib.request.Request(f"https://api.github.com/repos/{repo}{path}",
                                     headers={"Accept": "application/vnd.github+json", "User-Agent": "nano-banana-badges"})
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        request.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(request, timeout=20) as response:
        return json.load(response)


def write(name, label, value):
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / name).write_text(badge(label, value), encoding="utf-8", newline="\n")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo", help="owner/name; refreshes the release and stars badges from the GitHub API")
    args = ap.parse_args()
    for name, (label, value) in STATIC.items():
        write(name, label, value)
    if args.repo:
        for name, label, fetch in (
            ("release.svg", "release", lambda: github_api(args.repo, "/releases/latest")["tag_name"]),
            ("stars.svg", "stars", lambda: str(github_api(args.repo, "")["stargazers_count"])),
        ):
            try:
                write(name, label, fetch())
            except Exception as error:  # keep the existing file when the API is not reachable
                print(f"{name}: keeping the existing file ({error})")
                if not (OUT / name).exists():
                    write(name, label, "n/a")
    print("badges written to", OUT)


if __name__ == "__main__":
    main()
