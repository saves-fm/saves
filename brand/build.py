"""Build every saves.fm logo, icon and favicon from the pixel definitions below.

The marks are 16x16 pixel art, so the pixel grids in this file are the masters.
SVGs are written straight from them; PNGs are rendered from the SVGs with
rsvg-convert. The wordmark is Pixelify Sans Bold, converted to outlines so the
lockup files don't need the font installed.

usage (from this folder):
  python3 -m venv .venv && .venv/bin/pip install fonttools
  .venv/bin/python build.py
Social images are rendered separately: node render-social.mjs
"""
import json
import struct
import subprocess
from pathlib import Path

from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

HERE = Path(__file__).resolve().parent
TOKENS = json.loads((HERE / 'tokens.json').read_text())
C = {k: v['value'] for k, v in TOKENS['color'].items()}

# Pixel roles -> colors, for marks on dark and on light backgrounds
ON_DARK = {'P': C['cloud'], 'A': C['gold'], 'D': C['periwinkle'], 'F': C['slot']}
ON_LIGHT = {'P': C['navy'], 'A': C['gold-deep'], 'D': C['periwinkle-deep'], 'F': C['mist-line']}

N = 16


# ── pixel helpers ────────────────────────────────────────────────────────────
def blank():
    return [['.'] * N for _ in range(N)]


def put(g, x, y, c):
    if 0 <= x < N and 0 <= y < N:
        g[y][x] = c


def rect(g, x0, y0, x1, y1, c):
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            put(g, x, y, c)


def slot(g, x0, y0, x1, y1, c, fill=True):
    """A rectangle with its four corner pixels cut, filled or outlined."""
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            corner = x in (x0, x1) and y in (y0, y1)
            edge = x in (x0, x1) or y in (y0, y1)
            if not corner and (fill or edge):
                put(g, x, y, c)


def stamp(g, x0, y0, pattern, c):
    for y, row in enumerate(pattern):
        for x, ch in enumerate(row):
            if ch == '#':
                put(g, x0 + x, y0 + y, c)


def ring(g, cx, cy, r, th, c, keep=lambda a: True):
    import math
    for y in range(N):
        for x in range(N):
            dx, dy = x - cx, cy - y
            a = math.degrees(math.atan2(dy, dx)) % 360
            if abs(math.hypot(dx, dy) - r) < th and keep(a):
                put(g, x, y, c)


def arc(g, cx, cy, r, th, a0, a1, c):
    inside = (lambda a: a0 <= a <= a1) if a0 <= a1 else (lambda a: a >= a0 or a <= a1)
    ring(g, cx, cy, r, th, c, inside)


SPARK5 = ['..#..', '.###.', '#####', '.###.', '..#..']
SPARK6 = ['..##..', '.####.', '######', '.####.', '..##..']
SPARK7 = ['...#...', '...#...', '..###..', '#######', '..###..', '...#...', '...#...']


# ── the marks ────────────────────────────────────────────────────────────────
def logo():
    """H1 · Chart slots, the main logo: save slots that double as a top chart."""
    g = blank()
    slot(g, 0, 1, 15, 4, 'A')
    stamp(g, 1, 1, ['.#.', '###', '###', '.#.'], 'P')
    slot(g, 0, 6, 11, 9, 'P')
    slot(g, 0, 11, 7, 14, 'D')
    return g


def charts():
    g = blank()
    rect(g, 1, 10, 4, 15, 'D')
    rect(g, 6, 7, 9, 15, 'P')
    rect(g, 11, 6, 14, 15, 'A')
    stamp(g, 10, 0, SPARK5, 'A')
    return g


def library():
    g = blank()
    slot(g, 0, 1, 15, 5, 'A')
    stamp(g, 2, 2, ['.#.', '###', '.#.'], 'P')
    rect(g, 7, 3, 13, 3, 'P')
    slot(g, 0, 7, 15, 10, 'P', fill=False)
    rect(g, 2, 8, 9, 9, 'D')
    slot(g, 0, 12, 15, 15, 'D', fill=False)
    return g


def now_playing():
    g = blank()
    arc(g, 3, 12, 6.5, 0.85, 12, 78, 'P')
    arc(g, 3, 12, 10.5, 0.85, 14, 76, 'D')
    stamp(g, 0, 9, SPARK7, 'A')
    return g


def alerts():
    g = blank()
    slot(g, 0, 8, 15, 15, 'A')
    stamp(g, 1, 9, SPARK5, 'P')
    rect(g, 7, 10, 13, 10, 'P')
    rect(g, 7, 13, 11, 13, 'P')
    arc(g, 3, 9, 4.5, 0.62, 30, 80, 'P')
    arc(g, 3, 9, 7.6, 0.62, 28, 82, 'D')
    return g


def rewind():
    g = blank()
    ring(g, 7.5, 7.5, 6.3, 0.8, 'P', lambda a: not 98 < a < 160)
    for x, y in [(4, 2), (5, 1), (5, 2), (5, 3), (6, 0), (6, 1), (6, 2), (6, 3), (6, 4)]:
        put(g, x, y, 'P')
    stamp(g, 5, 5, ['..##..', '.####.', '######', '######', '.####.', '..##..'], 'A')
    return g


def player2():
    g = blank()
    slot(g, 0, 3, 15, 12, 'P', fill=False)
    stamp(g, 3, 5, ['###', '..#', '###', '#..', '###'], 'A')
    stamp(g, 8, 5, ['###.', '#..#', '###.', '#...', '#...'], 'P')
    return g


def finder():
    g = blank()
    ring(g, 6, 6.5, 4.6, 0.8, 'P')
    for i in range(5):
        rect(g, 10 + i, 10 + i, 11 + i, 11 + i, 'P')
    stamp(g, 4, 4, SPARK5, 'A')
    return g


def aotw():
    g = blank()
    slot(g, 0, 2, 15, 15, 'P', fill=False)
    rect(g, 1, 3, 14, 4, 'P')
    rect(g, 4, 0, 4, 2, 'P')
    rect(g, 11, 0, 11, 2, 'P')
    stamp(g, 5, 7, SPARK6, 'A')
    return g


def profile():
    g = blank()
    slot(g, 5, 1, 10, 6, 'P')
    slot(g, 2, 8, 13, 15, 'P')
    rect(g, 2, 15, 13, 15, 'P')
    stamp(g, 11, 9, ['.#.', '###', '.#.'], 'A')
    return g


def settings():
    g = blank()
    for y, kx, c in [(3, 4, 'P'), (8, 10, 'A'), (13, 6, 'P')]:
        rect(g, 0, y, 15, y, 'D')
        rect(g, kx - 1, y - 1, kx + 1, y + 1, c)
    return g


ICONS = {
    'home': logo, 'charts': charts, 'library': library, 'now-playing': now_playing,
    'alerts': alerts, 'rewind': rewind, 'player-2': player2, 'finder': finder,
    'achievement-of-the-week': aotw, 'profile': profile, 'settings': settings,
}


# ── SVG writers ──────────────────────────────────────────────────────────────
def pixel_paths(g, colors, scale=1.0, ox=0.0, oy=0.0):
    """One <path> per color, each row's runs merged into rectangles."""
    by_color = {}
    for y, row in enumerate(g):
        x = 0
        while x < N:
            c = row[x]
            if c == '.':
                x += 1
                continue
            start = x
            while x < N and row[x] == c:
                x += 1
            w = x - start
            by_color.setdefault(colors[c], []).append(
                f'M{fmt(ox + start * scale)} {fmt(oy + y * scale)}h{fmt(w * scale)}v{fmt(scale)}h{fmt(-w * scale)}z')
    return ''.join(f'<path fill="{col}" d="{"".join(d)}"/>' for col, d in by_color.items())


def fmt(n):
    return f'{n:.3f}'.rstrip('0').rstrip('.')


def svg_doc(w, h, body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {fmt(w)} {fmt(h)}" width="{fmt(w)}" height="{fmt(h)}" '
            f'shape-rendering="crispEdges" role="img" aria-label="{title}"><title>{title}</title>{body}</svg>\n')


def mark_svg(g, colors, title):
    return svg_doc(16, 16, pixel_paths(g, colors), title)


def tile_svg(g, bg, colors, title, size=512, radius=0.22, mark=0.62):
    m = size * mark
    s = m / 16
    off = (size - m) / 2
    shape = (f'<rect width="{size}" height="{size}" rx="{fmt(size * radius)}" fill="{bg}"/>' if radius
             else f'<rect width="{size}" height="{size}" fill="{bg}"/>')
    return svg_doc(size, size, shape + pixel_paths(g, colors, s, off, off), title)


# ── wordmark outlines ────────────────────────────────────────────────────────
def load_pixelify_bold():
    font = TTFont(HERE / 'fonts' / 'PixelifySans-Variable.ttf')
    return instantiateVariableFont(font, {'wght': 700})


def text_paths(font, text, size):
    """Return [(char, svg path d)], advance width and ink bounds, at font size `size` with baseline at y=0."""
    gs = font.getGlyphSet()
    cmap = font.getBestCmap()
    upm = font['head'].unitsPerEm
    k = size / upm
    x = 0.0
    out = []
    ymin, ymax = 0.0, 0.0
    for ch in text:
        name = cmap[ord(ch)]
        glyph = gs[name]
        pen = SVGPathPen(gs)
        glyph.draw(TransformPen(pen, (k, 0, 0, -k, x, 0)))
        bp = BoundsPen(gs)
        glyph.draw(bp)
        if bp.bounds:
            ymin = min(ymin, -bp.bounds[3] * k)
            ymax = max(ymax, -bp.bounds[1] * k)
        out.append((ch, pen.getCommands()))
        x += glyph.width * k
    return out, x, (ymin, ymax)


def lockup_svg(font, theme, stacked=False):
    colors = ON_DARK if theme == 'dark' else ON_LIGHT
    ink = C['cloud'] if theme == 'dark' else C['navy']
    accent = C['gold'] if theme == 'dark' else C['gold-deep']
    title = 'saves.fm'
    glyphs, adv, (ymin, ymax) = text_paths(font, 'saves.fm', 100)
    text_h = ymax - ymin
    split = 'saves'
    d_main = ''.join(d for ch, d in glyphs[:len(split)])
    d_fm = ''.join(d for ch, d in glyphs[len(split):])
    pad = 12
    if not stacked:
        mark = text_h * 1.55
        gap = mark * 0.32
        w = pad + mark + gap + adv + pad
        h = pad * 2 + max(mark, text_h)
        my = (h - mark) / 2
        ty = (h - text_h) / 2 - ymin
        tx = pad + mark + gap
    else:
        mark = text_h * 2.6
        gap = mark * 0.22
        w = pad * 2 + max(mark, adv)
        h = pad + mark + gap + text_h + pad
        my = pad
        ty = pad + mark + gap - ymin
        tx = (w - adv) / 2
    mx = pad if not stacked else (w - mark) / 2
    body = pixel_paths(logo(), colors, mark / 16, mx, my)
    body += (f'<g transform="translate({fmt(tx)} {fmt(ty)})" shape-rendering="geometricPrecision">'
             f'<path fill="{ink}" d="{d_main}"/><path fill="{accent}" d="{d_fm}"/></g>')
    return svg_doc(round(w), round(h), body, title)


# ── PNG + ICO ────────────────────────────────────────────────────────────────
def png(svg_path, out, width, height=None):
    out.parent.mkdir(parents=True, exist_ok=True)
    cmd = ['rsvg-convert', '-w', str(width)]
    if height:
        cmd += ['-h', str(height)]
    subprocess.run(cmd + ['-o', str(out), str(svg_path)], check=True)


def ico(pngs, out):
    """Write a .ico holding PNG-compressed images (supported by every current browser)."""
    datas = [p.read_bytes() for p in pngs]
    sizes = [struct.unpack('>II', d[16:24]) for d in datas]
    header = struct.pack('<HHH', 0, 1, len(datas))
    offset = 6 + 16 * len(datas)
    entries = b''
    for (w, h), d in zip(sizes, datas):
        entries += struct.pack('<BBBBHHII', w % 256, h % 256, 0, 0, 1, 32, len(d), offset)
        offset += len(d)
    out.write_bytes(header + entries + b''.join(datas))


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    return path


def main():
    g = logo()
    # Marks
    m_dark = write(HERE / 'saves-mark.svg', mark_svg(g, ON_DARK, 'saves.fm logo, for dark backgrounds'))
    m_light = write(HERE / 'saves-mark-light.svg', mark_svg(g, ON_LIGHT, 'saves.fm logo, for light backgrounds'))
    png(m_dark, HERE / 'saves-mark-512.png', 512)
    png(m_light, HERE / 'saves-mark-light-512.png', 512)

    # Rounded icon tiles (README headers, docs, anywhere a contained logo is needed)
    i_dark = write(HERE / 'saves-icon.svg', tile_svg(g, C['navy'], ON_DARK, 'saves.fm icon'))
    i_light = write(HERE / 'saves-icon-light.svg', tile_svg(g, C['mist'], ON_LIGHT, 'saves.fm icon, light'))
    for s in (1024, 512, 400):
        png(i_dark, HERE / f'saves-icon-{s}.png', s)
    png(i_light, HERE / 'saves-icon-light-512.png', 512)

    # Full-bleed avatar for GitHub, Bluesky, Discord and other circle/square crops
    av = write(HERE / 'build' / 'avatar.svg', tile_svg(g, C['navy'], ON_DARK, 'saves.fm avatar', radius=0, mark=0.56))
    png(av, HERE / 'saves-avatar-500.png', 500)

    # Lockups
    font = load_pixelify_bold()
    for stacked in (False, True):
        for theme in ('dark', 'light'):
            name = 'saves-lockup' + ('-stacked' if stacked else '') + ('-light' if theme == 'light' else '')
            p = write(HERE / f'{name}.svg', lockup_svg(font, theme, stacked))
            png(p, HERE / f'{name}.png', 1200 if not stacked else 640)

    # App icons: full bleed (the OS applies its own mask), dark and light
    a_dark = write(HERE / 'build' / 'app-icon.svg', tile_svg(g, C['navy'], ON_DARK, 'saves.fm app icon', radius=0))
    a_light = write(HERE / 'build' / 'app-icon-light.svg', tile_svg(g, C['mist'], ON_LIGHT, 'saves.fm app icon, light', radius=0))
    png(a_dark, HERE / 'app-icon' / 'app-icon-1024.png', 1024)
    png(a_light, HERE / 'app-icon' / 'app-icon-light-1024.png', 1024)
    # macOS: rounded tile inside the 1024 canvas with Apple's ~10% margin
    mac = (f'<rect x="100" y="100" width="824" height="824" rx="185" fill="{C["navy"]}"/>'
           + pixel_paths(g, ON_DARK, 512 / 16, 256, 256))
    mac_svg = write(HERE / 'build' / 'app-icon-macos.svg', svg_doc(1024, 1024, mac, 'saves.fm macOS app icon'))
    png(mac_svg, HERE / 'app-icon' / 'app-icon-macos-1024.png', 1024)
    # Android adaptive icon: foreground mark inside the 66dp safe zone of a 108dp canvas, xxxhdpi
    fg = write(HERE / 'build' / 'android-foreground.svg',
               svg_doc(432, 432, pixel_paths(g, ON_DARK, 240 / 16, 96, 96), 'saves.fm adaptive icon foreground'))
    png(fg, HERE / 'app-icon' / 'android-adaptive-foreground-432.png', 432)

    # Favicons: the small rounded tile reads on light and dark browser chrome
    fav = write(HERE / 'favicon' / 'favicon.svg', tile_svg(g, C['navy'], ON_DARK, 'saves.fm', size=32, radius=0.2, mark=0.75))
    small = []
    for s in (16, 32, 48):
        out = HERE / 'favicon' / f'favicon-{s}.png'
        png(fav, out, s)
        small.append(out)
    ico(small, HERE / 'favicon' / 'favicon.ico')
    apple = write(HERE / 'build' / 'apple-touch.svg', tile_svg(g, C['navy'], ON_DARK, 'saves.fm', size=180, radius=0, mark=0.6))
    png(apple, HERE / 'favicon' / 'apple-touch-icon-180.png', 180)

    # Icon family
    for name, make in ICONS.items():
        label = name.replace('-', ' ')
        write(HERE / 'icons' / 'dark' / f'{name}.svg', mark_svg(make(), ON_DARK, label))
        write(HERE / 'icons' / 'light' / f'{name}.svg', mark_svg(make(), ON_LIGHT, label))
    print('built', sum(1 for _ in HERE.rglob('*') if _.is_file() and 'fonts' not in _.parts and '.venv' not in _.parts), 'files')


if __name__ == '__main__':
    main()
