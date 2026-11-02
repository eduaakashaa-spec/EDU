"""Generate an original tile illustration for every college in app/data/eng_cities.json: app/static/img/colleges/<key>.svg
Not photographs: a coloured gradient by institution type, a light blueprint grid, a stylised campus silhouette (three motifs, picked by the college key)
and the college's initials. Replace any file with a real photograph or logo (same name) and the page uses it.
Run: python tools/cities/make_tiles.py"""
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.join(HERE, '..', '..', 'app')
OUT = os.path.join(APP, 'static', 'img', 'colleges')
PAL = {  # type: (gradient start, gradient end, accent)
    'IIT': ('#1E3A8A', '#6D28D9', '#93C5FD'), 'NIT': ('#0F766E', '#1D4ED8', '#99F6E4'), 'IIIT': ('#3730A3', '#BE185D', '#FBCFE8'),
    'BITS': ('#92400E', '#B45309', '#FDE68A'), 'University': ('#166534', '#0E7490', '#BBF7D0'), 'Private': ('#9A3412', '#BE123C', '#FED7AA'),
}
CONNECT = {'of', 'and', 'the', 'for', 'in', 'a', 'to', 'deemed', 'be', 'university,', 'at'}


def initials(name, typ):
    """(big text, small text): IIT/NIT show the place under the letters, others their initials."""
    n = re.sub(r'\(.*?\)', ' ', name)
    low = n.lower()
    for key, pre in (('indian institute of technology', 'IIT'), ('national institute of technology', 'NIT')):
        if key in low:
            place = re.sub('(?i)' + key + r'|,|\.', ' ', n).split()
            return pre, (place[-1] if place else '')
    if 'birla institute of technology' in low and 'pilani' in low:
        return 'BITS', 'Pilani'
    words = [w for w in re.findall(r"[A-Za-z]+", n) if w.lower() not in CONNECT]
    ini = ''.join(w[0] for w in words).upper()
    if len(ini) > 5:
        ini = ''.join(w[0] for w in words if w.lower() not in ('university', 'institute', 'college', 'technology', 'engineering'))[:5].upper() or ini[:5]
    return (ini or n[:3].upper()), ''


def motif(kind, accent):
    if kind == 0:   # dome and columns
        return ('<path d="M120 190V120h160v70z" fill="#fff" fill-opacity=".14"/><path d="M150 120a50 50 0 0 1 100 0z" fill="#fff" fill-opacity=".22"/><rect x="196" y="58" width="8" height="24" fill="#fff" fill-opacity=".3"/>'
                '<g fill="#fff" fill-opacity=".28"><rect x="132" y="128" width="10" height="62"/><rect x="160" y="128" width="10" height="62"/><rect x="190" y="128" width="10" height="62"/><rect x="218" y="128" width="10" height="62"/><rect x="246" y="128" width="10" height="62"/></g>')
    if kind == 1:   # tall blocks
        return ('<g fill="#fff" fill-opacity=".2"><rect x="96" y="110" width="52" height="80"/><rect x="156" y="70" width="60" height="120"/><rect x="224" y="96" width="48" height="94"/><rect x="280" y="128" width="40" height="62"/></g>'
                '<g fill="%s" fill-opacity=".55"><rect x="168" y="84" width="10" height="10"/><rect x="190" y="84" width="10" height="10"/><rect x="168" y="106" width="10" height="10"/><rect x="190" y="106" width="10" height="10"/><rect x="168" y="128" width="10" height="10"/><rect x="190" y="128" width="10" height="10"/></g>' % accent)
    return ('<path d="M80 190V140q60-70 120-20t120 20v50z" fill="#fff" fill-opacity=".18"/><path d="M130 190v-34q20-30 40 0v34zM230 190v-34q20-30 40 0v34z" fill="#fff" fill-opacity=".3"/><circle cx="200" cy="92" r="14" fill="%s" fill-opacity=".7"/>' % accent)


def main():
    d = json.load(open(os.path.join(APP, 'data', 'eng_cities.json'), encoding='utf-8'))
    os.makedirs(OUT, exist_ok=True)
    n = 0
    for c in d['colleges']:
        a, b, acc = PAL.get(c['type'], PAL['Private'])
        h = int(hashlib.md5(c['key'].encode()).hexdigest(), 16)
        ini, sub = initials(c['name'], c['type'])
        fs = 58 if len(ini) <= 3 else 46 if len(ini) == 4 else 38
        svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 220" role="img" aria-label="%s">'
               '<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="%s"/><stop offset="1" stop-color="%s"/></linearGradient>'
               '<pattern id="p" width="20" height="20" patternUnits="userSpaceOnUse"><path d="M20 0H0V20" fill="none" stroke="#fff" stroke-opacity=".07"/></pattern></defs>'
               '<rect width="400" height="220" fill="url(#g)"/><rect width="400" height="220" fill="url(#p)"/>'
               '<circle cx="%d" cy="%d" r="90" fill="#fff" fill-opacity=".06"/>%s'
               '<rect y="190" width="400" height="30" fill="#000" fill-opacity=".18"/>'
               '<text x="24" y="%d" font-family="Fraunces,Georgia,serif" font-size="%d" font-weight="700" fill="#fff">%s</text>'
               '<text x="24" y="92" font-family="Fraunces,Georgia,serif" font-size="24" font-weight="600" fill="#fff" fill-opacity=".92">%s</text>'
               '<text x="24" y="206" font-family="Plus Jakarta Sans,Arial,sans-serif" font-size="13" font-weight="600" fill="#fff" fill-opacity=".85">%s</text></svg>') % (
            c['name'].replace('&', 'and').replace('"', ''), a, b, 40 + h % 300, 30 + (h >> 8) % 60, motif(h % 3, acc), 60, fs, ini.replace('&', 'and'), sub.replace('&', 'and')[:14], c['city'].replace('&', 'and')[:28])
        with open(os.path.join(OUT, c['key'] + '.svg'), 'w', encoding='utf-8') as f:
            f.write(svg)
        n += 1
    print(n, 'tiles in', OUT)


if __name__ == '__main__':
    main()
