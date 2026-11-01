"""Render IAT paper questions (stem and each option) as trimmed WebP images using the layout of the PDF.

For the one-question-per-page papers (2023 to 2026). The options are cut out separately (label removed) so the mock can shuffle them:
in these answer-key editions the correct option is always printed first, (a).
Usage: python tools/iat/render_papers.py <pdf> <year> <out_dir>
Writes <out_dir>/<year>/<subj><nn>_s.webp, _o0.._o3.webp (or _full0.. when the options are bare pictures) and <out_dir>/<year>.json.
"""
import io
import json
import os
import re
import sys
import warnings

warnings.filterwarnings('ignore')
import fitz  # noqa: E402
from PIL import Image, ImageChops  # noqa: E402

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from layout import split  # noqa: E402

SUBJ = ['Biology', 'Chemistry', 'Mathematics', 'Physics']
ZOOM = 2.0
MARK = re.compile(r'^\(([a-d])\)$')


def trim(img, pad=6):
    bg = Image.new(img.mode, img.size, (255, 255, 255))
    box = ImageChops.difference(img, bg).getbbox()
    if not box:
        return None
    x0, y0, x1, y1 = box
    return img.crop((max(0, x0 - pad), max(0, y0 - pad), min(img.width, x1 + pad), min(img.height, y1 + pad)))


def strip_slivers(img):
    return img


def grab(page, rect):
    pix = page.get_pixmap(matrix=fitz.Matrix(ZOOM, ZOOM), clip=rect, alpha=False)
    return Image.open(io.BytesIO(pix.tobytes('png'))).convert('RGB')


def save(parts, path):
    parts = [p for p in parts if p is not None]
    if not parts:
        return False
    w = max(p.width for p in parts)
    c = Image.new('RGB', (w, sum(p.height for p in parts)), (255, 255, 255))
    y = 0
    for p in parts:
        c.paste(p, (0, y))
        y += p.height
    c = trim(c)
    if c is None:
        return False
    c.save(path, 'WEBP', quality=72, method=6)
    return True


def main(pdf, year, out):
    doc = fitz.open(pdf)
    d = os.path.join(out, str(year))
    os.makedirs(d, exist_ok=True)
    items, cur, subj = [], None, None
    for pi, page in enumerate(doc):
        words = page.get_text('words')
        text = page.get_text()
        first = text.strip().split('\n')[0].strip()
        if first in SUBJ:
            subj = first
        title = None
        for w in words:
            if w[4] == 'Question' and w[0] < 220:
                nxt = [x for x in words if abs(x[1] - w[1]) < 3 and x[0] > w[2]]
                if nxt and nxt[0][4].isdigit():
                    title = w
                    break
        if title:
            m = re.search(r'(\d+)\.\s*Question', text)
            cur = dict(subj=subj, n=int(m.group(1)), pages=[], lm=title[0] - 15)
            items.append(cur)
        if cur is not None and text.strip() and not text.startswith('English Answer Key'):
            cur['pages'].append(pi)
    res = []
    for q in items:
        pre = '%s%02d' % (q['subj'][:3].lower(), q['n'])
        lm = q['lm']
        stem_parts, opt_imgs = [], []
        pages_info = []
        for k, pi in enumerate(q['pages']):
            page = doc[pi]
            words = page.get_text('words')
            tl = [w for w in words if w[4] == 'Question' and w[0] < 220]
            top = (tl[0][3] + 3) if (k == 0 and tl) else 40
            ms = sorted([w for w in words if MARK.match(w[4]) and w[0] < lm + 70], key=lambda w: w[1])
            foot = [w for w in words if w[1] > 680 and re.fullmatch(r'\d+', w[4])]
            bottom = min([w[1] for w in foot], default=700) - 4
            pages_info.append((pi, top, bottom, ms))
        allm = [m for _p, _t, _b, ms in pages_info for m in ms]
        letters = [MARK.match(m[4]).group(1) for m in allm]
        ok = letters == ['a', 'b', 'c', 'd']
        stem_files, opt_files, full_files = [], [], []
        if ok:
            for pi, top, bottom, ms in pages_info:
                if ms:
                    first = all(not x[3] for x in pages_info[:pages_info.index((pi, top, bottom, ms))])
                    _s, _o, lay = split(doc[pi], top, bottom, lm, [fitz.Rect(m[:4]) for m in ms], 575, first_page=first)
                    if not lay:
                        ok = False
        if ok:
            seen_first = False
            for pi, top, bottom, ms in pages_info:
                page = doc[pi]
                if not ms:
                    if not seen_first:
                        stem_parts.append(grab(page, fitz.Rect(lm - 10, top, 575, bottom)))
                    continue
                mrects = [fitz.Rect(m[:4]) for m in ms]
                s_rect, o_rects, _lay = split(page, top, bottom, lm, mrects, 575, first_page=not seen_first)
                if not seen_first and s_rect is not None:
                    stem_parts.append(grab(page, s_rect))
                seen_first = True
                for m, r in zip(mrects, o_rects):
                    if r is None:
                        opt_imgs.append(None)
                        continue
                    r.x0 = max(r.x0, m.x1 + 1)
                    opt_imgs.append(grab(page, r))
            sp = os.path.join(d, pre + '_s.webp')
            if save(stem_parts, sp):
                stem_files.append(os.path.basename(sp))
            for i, im in enumerate(opt_imgs):
                f = os.path.join(d, '%s_o%d.webp' % (pre, i))
                opt_files.append(os.path.basename(f) if save([im], f) else '')
        else:                                         # options are bare pictures: keep the whole page(s); these questions are not shuffled
            for j, (pi, top, bottom, _ms) in enumerate(pages_info):
                fp = os.path.join(d, '%s_full%d.webp' % (pre, j))
                if save([grab(doc[pi], fitz.Rect(lm - 10, top, 575, bottom))], fp):
                    full_files.append(os.path.basename(fp))
        good = ok and bool(stem_files) and len(opt_files) == 4 and '' not in opt_files
        res.append(dict(subj=q['subj'], n=q['n'], ok=good, stem=stem_files, opts=opt_files if good else [], full=full_files if not good else [], pages=[p + 1 for p in q['pages']]))
    json.dump(res, open(os.path.join(out, '%s.json' % year), 'w', encoding='utf-8'), indent=1)
    print(year, len(res), 'questions; problems:', [(r['subj'][:3], r['n']) for r in res if not r['ok']])


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3])
