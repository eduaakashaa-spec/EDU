"""Generate a banner illustration for every Member Home tile (app/static/img/tiles/<slug>.svg).

Original vector art in one style (blue to violet scene, soft clouds, a glowing path up a hill, a glass dome holding the tile's icon on a lit platform), tinted per category.
Run:  python tools/make_tile_banners.py      Replace any file with artwork from a design tool (same file name) and it is used instead; nothing else to change.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
os.environ.setdefault('SECRET_KEY', 'x')

from app.services import member_hub as mh  # noqa: E402

OUT = os.path.join(ROOT, 'app', 'static', 'img', 'tiles')
PAL = {  # (gradient start, gradient end, accent glow)
    'journey': ('#1E40AF', '#7C3AED', '#60A5FA'), 'mentorship': ('#3730A3', '#BE4B1A', '#FDBA74'), 'intel': ('#1E3A8A', '#B45309', '#FCD34D'), 'edupulse': ('#312E81', '#C2410C', '#FDBA74'),
    'medicine': ('#115E59', '#1E3A8A', '#5EEAD4'), 'gulf': ('#0E7490', '#4338CA', '#67E8F9'), 'tools': ('#047857', '#3730A3', '#6EE7B7'), 'insights': ('#5B21B6', '#1D4ED8', '#C4B5FD'),
    'free': ('#0369A1', '#6D28D9', '#7DD3FC'), 'support': ('#9D174D', '#4338CA', '#F9A8D4'),
}


def icons():
    """{name: inner svg markup} from the dashboard's own icon set."""
    s = open(os.path.join(ROOT, 'app', 'templates', 'members', '_md_icons.html'), encoding='utf-8').read()
    out = {}
    parts = re.split(r"\{%-?\s*(?:el)?if name == '([a-z-]+)'\s*%\}", s)
    for i in range(1, len(parts), 2):
        body = parts[i + 1]
        body = re.split(r"\{%-?\s*(?:elif|else|endif)", body)[0].strip()
        out[parts[i]] = body
    return out


def slug(title):
    return mh.slugify(title)


def sparkle(x, y, r, op):
    return '<path d="M%g %g l%g %g l%g %g l%g %g l%g %g l%g %g l%g %g z" fill="#fff" fill-opacity="%g"/>' % (x, y - r, r * .22, r * .78, r * .78, r * .22, -r * .78, r * .22, -r * .22, r * .78, -r * .22, -r * .78, -r * .78, -r * .22, op)


def banner(title, icon_markup, cat):
    a, b, glow = PAL.get(cat, PAL['journey'])
    h = sum(map(ord, title)) % 7                                          # small variation so neighbouring tiles do not look identical
    dx = 560 + h * 14
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 330" preserveAspectRatio="xMidYMid slice" role="img" aria-label="{title}">
<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{a}"/><stop offset="1" stop-color="{b}"/></linearGradient>
<radialGradient id="gl" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="{glow}" stop-opacity=".75"/><stop offset="1" stop-color="{glow}" stop-opacity="0"/></radialGradient>
<linearGradient id="dome" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".30"/><stop offset="1" stop-color="#fff" stop-opacity=".08"/></linearGradient>
<filter id="blur"><feGaussianBlur stdDeviation="3"/></filter>
</defs>
<rect width="960" height="330" fill="url(#bg)"/>
<circle cx="820" cy="40" r="260" fill="#fff" fill-opacity=".06"/><circle cx="120" cy="330" r="200" fill="#fff" fill-opacity=".05"/>
<g fill="#fff" fill-opacity=".12"><path d="M70 90q4-34 38-34 14-22 44-12 20-10 36 8 26 2 26 26 0 14-12 18H84q-16-2-14-6z"/><path d="M760 70q3-24 28-24 10-16 32-8 15-7 26 6 19 1 19 19 0 10-9 13h-84q-12-2-12-6z"/><path d="M380 40q2-14 18-14 6-10 19-5 9-4 15 4 11 0 11 11 0 6-5 8h-50q-8-1-8-4z" fill-opacity=".09"/></g>
<path d="M0 330V250C120 215 230 232 330 205c110-30 190-100 330-95 120 4 210 60 300 40v180z" fill="#0B1550" fill-opacity=".22"/>
<path d="M0 330V282c140-30 260-8 380-40 120-33 190-70 340-62 90 5 170 30 240 12v138z" fill="#0B1550" fill-opacity=".18"/>
<circle cx="{dx}" cy="168" r="170" fill="url(#gl)"/>
<path d="M-10 304C100 298 170 272 250 268S{dx - 120} 292 {dx - 40} 272" fill="none" stroke="{glow}" stroke-opacity=".55" stroke-width="9" stroke-linecap="round" stroke-dasharray="1 24" filter="url(#blur)"/>
<path d="M-10 304C100 298 170 272 250 268S{dx - 120} 292 {dx - 40} 272" fill="none" stroke="#fff" stroke-opacity=".95" stroke-width="7" stroke-linecap="round" stroke-dasharray="1 24"/>
<ellipse cx="{dx}" cy="268" rx="130" ry="24" fill="#fff" fill-opacity=".14" stroke="{glow}" stroke-opacity=".9" stroke-width="3"/>
<ellipse cx="{dx}" cy="262" rx="92" ry="15" fill="{glow}" fill-opacity=".28"/>
<circle cx="{dx}" cy="165" r="104" fill="url(#dome)" stroke="#fff" stroke-opacity=".55" stroke-width="3"/>
<path d="M{dx - 78} 120a96 96 0 0 1 70 -48" fill="none" stroke="#fff" stroke-opacity=".6" stroke-width="5" stroke-linecap="round"/>
<g transform="translate({dx - 60} 105) scale(5)" fill="none" stroke="#fff" stroke-width="1.55" stroke-linecap="round" stroke-linejoin="round">{icon_markup}</g>
<circle cx="{dx - 232}" cy="226" r="40" fill="url(#dome)" stroke="#fff" stroke-opacity=".4" stroke-width="2"/><circle cx="{dx - 232}" cy="226" r="12" fill="{glow}" fill-opacity=".8"/>
<circle cx="{dx + 215}" cy="205" r="32" fill="url(#dome)" stroke="#fff" stroke-opacity=".4" stroke-width="2"/><path d="M{dx + 200} 205l11 11 20 -22" fill="none" stroke="#fff" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
{sparkle(dx - 130, 70, 11, .9)}{sparkle(dx + 150, 60, 8, .8)}{sparkle(dx + 260, 130, 7, .7)}{sparkle(dx - 300, 120, 6, .6)}{sparkle(dx + 20, 28, 6, .7)}
</svg>
'''


def main():
    os.makedirs(OUT, exist_ok=True)
    ic = icons()
    n = 0
    for cat in mh.CATEGORIES:
        for t in cat['tiles']:
            if t.get('access') == 'soon' or not t.get('endpoint'):
                continue
            d = mh._decorate(dict(t), None)
            markup = ic.get(d['ic']) or ic.get('grid') or ''
            path = os.path.join(OUT, slug(t['title']) + '.svg')
            if os.path.exists(path) and '--keep' in sys.argv and 'role="img"' not in open(path, encoding='utf-8').read(400):
                continue                                                   # a hand-made replacement: leave it
            open(path, 'w', encoding='utf-8').write(banner(t['title'].replace('&', '&amp;'), markup, cat['key']))
            n += 1
    print('wrote', n, 'banners to', OUT)


if __name__ == '__main__':
    main()
