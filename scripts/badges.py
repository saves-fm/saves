"""Generate the committed README badges in docs/badges/.

Badges are committed SVGs (not shields.io links) so they load even when
shields.io doesn't. Same flat style as the Sprout and ClearPath repos.

usage: python3 scripts/badges.py   (or: pnpm badges)
"""
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / 'docs' / 'badges'
COLOR = '#16205C'  # brand navy (brand/tokens.json)

# Store icons, 14x14 white glyphs (Simple Icons, CC0)
APPLE = ('data:image/svg+xml;base64,PHN2ZyBmaWxsPSJ3aGl0ZSIgcm9sZT0iaW1nIiB2aWV3Qm94PSIwIDAgMjQgMjQiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PHRpdGxlPkFwcGxlPC90aXRsZT48cGF0aCBkPSJNMTIuMTUyIDYuODk2Yy0uOTQ4IDAtMi40MTUtMS4wNzgtMy45Ni0xLjA0LTIuMDQuMDI3LTMuOTEgMS4xODMtNC45NjEgMy4wMTQtMi4xMTcgMy42NzUtLjU0NiA5LjEwMyAxLjUxOSAxMi4wOSAxLjAxMyAxLjQ1NCAyLjIwOCAzLjA5IDMuNzkyIDMuMDM5IDEuNTItLjA2NSAyLjA5LS45ODcgMy45MzUtLjk4NyAxLjgzMSAwIDIuMzUuOTg3IDMuOTYuOTQ4IDEuNjM3LS4wMjYgMi42NzYtMS40OCAzLjY3Ni0yLjk0OCAxLjE1Ni0xLjY4OCAxLjYzNi0zLjMyNSAxLjY2Mi0zLjQxNS0uMDM5LS4wMTMtMy4xODItMS4yMjEtMy4yMi00Ljg1Ny0uMDI2LTMuMDQgMi40OC00LjQ5NCAyLjU5Ny00LjU1OS0xLjQyOS0yLjA5LTMuNjIzLTIuMzI0LTQuMzktMi4zNzYtMi0uMTU2LTMuNjc1IDEuMDktNC42MSAxLjA5ek0xNS41MyAzLjgzYy44NDMtMS4wMTIgMS40LTIuNDI3IDEuMjQ1LTMuODMtMS4yMDcuMDUyLTIuNjYyLjgwNS0zLjUzMiAxLjgxOC0uNzguODk2LTEuNDU0IDIuMzM4LTEuMjczIDMuNzE0IDEuMzM4LjEwNCAyLjcxNS0uNjg4IDMuNTU5LTEuNzAxIi8+PC9zdmc+')
GOOGLE_PLAY = ('data:image/svg+xml;base64,PHN2ZyBmaWxsPSJ3aGl0ZSIgcm9sZT0iaW1nIiB2aWV3Qm94PSIwIDAgMjQgMjQiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PHRpdGxlPkdvb2dsZSBQbGF5PC90aXRsZT48cGF0aCBkPSJNMjIuMDE4IDEzLjI5OGwtMy45MTkgMi4yMTgtMy41MTUtMy40OTMgMy41NDMtMy41MjEgMy44OTEgMi4yMDJhMS40OSAxLjQ5IDAgMCAxIDAgMi41OTR6TTEuMzM3LjkyNGExLjQ4NiAxLjQ4NiAwIDAgMC0uMTEyLjU2OHYyMS4wMTdjMCAuMjE3LjA0NS40MTkuMTI0LjZsMTEuMTU1LTExLjA4N0wxLjMzNy45MjR6bTEyLjIwNyAxMC4wNjVsMy4yNTgtMy4yMzhMMy40NS4xOTVhMS40NjYgMS40NjYgMCAwIDAtLjk0Ni0uMTc5bDExLjA0IDEwLjk3M3ptMCAyLjA2N2wtMTEgMTAuOTMzYy4yOTguMDM2LjYxMi0uMDE2LjkwNi0uMTgzbDEzLjMyNC03LjU0LTMuMjMtMy4yMXoiLz48L3N2Zz4=')

# Approximate Verdana 11px advance widths, enough to size the boxes
WIDTHS = {
    **dict.fromkeys('ABCDEFGHKNOPRSTUVXYZ', 7.0), **dict.fromkeys('JL', 6.2),
    'I': 4.2, 'M': 8.5, 'W': 10.5, 'Q': 7.8,
    **dict.fromkeys('abcdeghnopquvxyz', 6.6), 'f': 3.9, 'i': 3.1, 'j': 3.4,
    'l': 3.1, 'm': 10.6, 'r': 4.7, 's': 5.7, 't': 4.3, 'w': 9.0, 'k': 6.2,
    **dict.fromkeys('0123456789', 7.0), ' ': 3.9, '.': 3.9, ':': 4.5,
    '-': 4.6, '(': 4.5, ')': 4.5,
}


def text_width(text):
    return sum(WIDTHS.get(c, 6.6) for c in text)


def badge(name, label, value, icon=None):
    icon_w = 17 if icon else 0
    label_w = round(text_width(label) + 10 + icon_w)
    value_w = round(text_width(value) + 10)
    image = (f'<image x="5" y="3" width="14" height="14" href="{icon}"/>'
             if icon else '')
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{label_w + value_w}" height="20" role="img" aria-label="{label}: {value}">'
        f'<title>{label}: {value}</title>'
        f'<g shape-rendering="crispEdges"><rect width="{label_w}" height="20" fill="#555"/>'
        f'<rect x="{label_w}" width="{value_w}" height="20" fill="{COLOR}"/></g>'
        '<g fill="#fff" text-anchor="middle" font-family="Verdana,Geneva,DejaVu Sans,sans-serif" text-rendering="geometricPrecision" font-size="110">'
        f'{image}'
        f'<text x="{(icon_w + (label_w - icon_w) / 2) * 10:.0f}" y="140" textLength="{text_width(label) * 10:.0f}" transform="scale(.1)">{label}</text>'
        f'<text x="{(label_w + value_w / 2) * 10:.0f}" y="140" textLength="{text_width(value) * 10:.0f}" transform="scale(.1)">{value}</text>'
        '</g></svg>'
    )
    (OUT / f'{name}.svg').write_text(svg)


def release_label():
    """The release badge's value: the version in package.json, or 'none yet' before v0.1.0."""
    version = json.loads((OUT.parent.parent / 'package.json').read_text())['version']
    return 'none yet' if version == '0.0.0' else f'v{version}'


if __name__ == '__main__':
    OUT.mkdir(parents=True, exist_ok=True)
    # Regenerated on every version bump; scripts/release-badge.test.mjs checks it matches package.json
    badge('release', 'release', release_label())
    badge('status-planning', 'status', 'planning')
    badge('web-v1', 'web', 'planned for v1.0')
    badge('app-store-v2', 'App Store', 'planned for v2.0', APPLE)
    badge('google-play-v2', 'Google Play', 'planned for v2.0', GOOGLE_PLAY)
    badge('license-agpl-3.0', 'license', 'AGPL v3')
