"""Cut every question of a BITSAT previous-year paper PDF into one image (stem + options as printed), numbered 1..N.

    python tools/bitsat/crop.py <pdf> <year> <style: num|q> <out dir> [top_margin footer_margin]

style 'num': questions start with '12.' at the left of a column (one or two columns per page). style 'q': a 'Question 12' heading block (one column).
A question runs from its marker to the next marker, across columns and pages; running page headers/footers are cut off, and a section heading
(PHYSICS, CHEMISTRY, ENGLISH, LOGICAL, MATHEMATICS) ends the question above it. Writes <out>/q001.webp ... and <out>/meta.json (page, size per question).
"""
import io
import json
import os
import re
import sys

import fitz
from PIL import Image, ImageChops

HEAD = re.compile(r'^\s*(PART\s*[-–:]*\s*[IVX]+|PHYSICS|CHEMISTRY|ENGLISH\s+PROFICIENCY|LOGICAL\s+REASONING|MATHEMATICS|BIOLOGY)\b', re.I)
DPI = 130


def markers(doc, style):
    """Question markers in reading order as the chain 1, 2, 3, ... -> [(n, page, col, x, y)]."""
    cand, bare = [], []
    for pi, page in enumerate(doc):
        w = page.rect.width
        if style == 'q':
            for blk in page.get_text('dict')['blocks']:
                for ln in blk.get('lines', []):
                    m = re.fullmatch(r'\s*Question (\d+)\s*', ''.join(sp['text'] for sp in ln['spans']))
                    if m:
                        cand.append((int(m.group(1)), pi, 0, ln['bbox'][0], ln['bbox'][1]))
        else:
            for wd in page.get_text('words'):
                m = re.fullmatch(r'(\d{1,3})\.', wd[4])
                if m:
                    cand.append((int(m.group(1)), pi, 0 if wd[0] < w * 0.45 else 1, wd[0], wd[1]))
                elif re.fullmatch(r'\d{1,3}', wd[4]):          # a number printed without its full stop: only used to fill a gap in the chain
                    bare.append((int(wd[4]), pi, 0 if wd[0] < w * 0.45 else 1, wd[0], wd[1]))
    cand.sort(key=lambda c: (c[1], c[2], c[4]))
    left = {}
    for n, pi, col, x, y in cand:                   # the usual left edge of a marker in each column
        left.setdefault(col, []).append(round(x))
    edge = {c: max(set(v), key=v.count) for c, v in left.items()}
    chain, cur = [], 1
    key = lambda c: (c[1], c[2], c[4])
    pool = sorted(cand + [b for b in bare if abs(b[3] - edge.get(b[2], -999)) < 8], key=key)   # bare numbers only when they sit exactly where markers do
    for c in pool:
        if c[0] == cur and abs(c[3] - edge[c[2]]) < 25:
            # a bare number is accepted only if no real marker for this number exists later in the page order
            if c in cand or not any(k[0] == cur for k in cand if key(k) > key(c)):
                chain.append(c)
                cur += 1
    return chain


def dir_lines(page):
    """Lines that start a DIRECTION(S) instruction: (y, x0, text)."""
    out = []
    for blk in page.get_text('dict')['blocks']:
        for ln in blk.get('lines', []):
            t = ''.join(sp['text'] for sp in ln['spans']).strip()
            if re.match(r'(DIRECTIONS?|Directions?)\s*[\(\[:\d]', t):
                out.append((ln['bbox'][1], ln['bbox'][0], t))
    return out


def headings(page):
    """y positions of section headings and direction lines on a page: (y, x0)."""
    out = []
    for b in page.get_text('blocks'):
        first = b[4].strip().split(chr(10))[0] if b[4].strip() else ''
        if HEAD.match(first) and len(first) < 140 and not re.match(r'^\d', first):
            out.append((b[1], b[0]))
    out += [(y, x) for y, x, _t in dir_lines(page)]
    return out


def page_top(page, default):
    """Bottom of the running header: the lowest long thin rule in the top part of the page, else the default."""
    try:
        ys = [d['rect'].y0 for d in page.get_drawings() if d['rect'].width > page.rect.width * 0.4 and d['rect'].height < 4 and d['rect'].y0 < 140]
    except Exception:
        ys = []
    return max(ys) + 3 if ys else default


def cut(pdf, year, style, outdir, top=48, foot=45):
    doc = fitz.open(pdf)
    ch = markers(doc, style)
    os.makedirs(outdir, exist_ok=True)
    two = {pi: any(c[1] == pi and c[2] == 1 for c in ch) for pi in range(len(doc))}
    # a page's text columns: two if it carries markers in the right column, or sits between two-column pages
    meta = []
    keyed = [((c[1], c[2], c[4]), c) for c in ch]

    def build(p, c, y0, nxt):
        segs = []
        while True:
            page = doc[p]
            w, h = page.rect.width, page.rect.height
            if two.get(p):
                xa, xb = (0, w * 0.5) if c == 0 else (w * 0.5, w)
            else:
                xa, xb = 0, w
            ybot = h - foot
            done = False
            if nxt and nxt[1] == p and (nxt[2] == c or not two.get(p)):
                ybot, done = min(ybot, nxt[4] + 1), True
            hs = [hy for hy, hx in headings(page) if hy > y0 + 12 and hy < ybot and xa - 5 <= hx < xb + 5]
            if hs:
                ybot, done = min(hs) - 2, True
            if ybot - y0 > 4:
                segs.append((p, fitz.Rect(xa, y0, xb, ybot)))
            if done:
                break
            if two.get(p) and c == 0:
                c, y0 = 1, page_top(page, top)
            else:
                p, c = p + 1, 0
                if p >= len(doc):
                    break
                y0 = page_top(doc[p], top)
            if nxt and (p > nxt[1] or (p == nxt[1] and c > nxt[2])):
                break
        return segs

    def render(segs, path):
        imgs = []
        for p, r in segs:
            pm = doc[p].get_pixmap(clip=r, dpi=DPI)
            im = Image.open(io.BytesIO(pm.tobytes('png'))).convert('RGB')
            bb = ImageChops.difference(im, Image.new('RGB', im.size, 'white')).getbbox()
            if bb:
                imgs.append(im.crop((0, max(bb[1] - 3, 0), im.width, min(bb[3] + 3, im.height))))
        if not imgs:
            return None
        W = max(i.width for i in imgs)
        H = sum(i.height for i in imgs)
        sheet = Image.new('RGB', (W, H), 'white')
        yy = 0
        for i in imgs:
            sheet.paste(i, (0, yy))
            yy += i.height
        bbox = ImageChops.difference(sheet, Image.new('RGB', sheet.size, 'white')).getbbox()
        if bbox:
            sheet = sheet.crop((max(bbox[0] - 6, 0), max(bbox[1] - 4, 0), min(bbox[2] + 6, W), min(bbox[3] + 4, H)))
        if sheet.height > 4000:                              # a runaway region (a missing marker): not a question image
            return None
        sheet.save(path, 'WEBP', quality=82, method=6)
        return sheet.size

    # instructions and reading passages: a 'DIRECTIONS (Qs. 86-90)' line runs to the next question marker (or the next direction) and belongs to the questions it names
    passages = []
    for pi, page in enumerate(doc):
        w = page.rect.width
        for dy, dx, text in dir_lines(page):
            m = re.match(r'DIRECTIONS?\s*[\(\[:]?\s*(?:Questions?|Qs?)?\.?\s*(\d{1,3})\s*(?:(?:-|–|&|,|to|and)\s*(\d{1,3}))?', text, re.I)
            if not m:
                continue
            lo = int(m.group(1))
            hi = int(m.group(2)) if m.group(2) else lo
            if hi < lo or hi - lo > 12:
                continue
            c = (0 if dx < w * 0.45 else 1) if two.get(pi) else 0
            pos = (pi, c, dy)
            nx = next((cc for key, cc in keyed if key > pos), None)
            segs = build(pi, c, dy - 3, nx)
            size = render(segs, os.path.join(outdir, 'p%03d_%03d.webp' % (lo, hi)))
            if size:
                passages.append(dict(lo=lo, hi=hi, w=size[0], h=size[1]))
    for k, (n, pi, col, x, y) in enumerate(ch):
        nxt = ch[k + 1] if k + 1 < len(ch) else None
        segs = build(pi, col, y - 1.5, nxt)
        size = render(segs, os.path.join(outdir, 'q%03d.webp' % n))
        if not size:
            meta.append(dict(n=n, ok=False))
            continue
        txt = ' '.join(doc[sp_].get_text(clip=r_) for sp_, r_ in segs)
        labs = sum(1 for L in 'abcd' if re.search(r'\(\s*%s\s*\)|(?m:^\s*%s[\.\)]\s)' % (L, L.upper()), txt, re.I))
        meta.append(dict(n=n, ok=True, page=pi + 1, w=size[0], h=size[1], parts=len(segs), opts=labs))
    json.dump(dict(year=year, pdf=os.path.basename(pdf), n=len(ch), q=meta, passages=passages), open(os.path.join(outdir, 'meta.json'), 'w'), indent=0)
    return meta


if __name__ == '__main__':
    a = sys.argv[1:]
    m = cut(a[0], a[1], a[2], a[3], *[float(x) for x in a[4:6]])
    bad = [q for q in m if not q['ok'] or q['h'] > 900 or q['h'] < 45]
    print(len(m), 'questions;', len(bad), 'to check:', [(q['n'], q.get('h')) for q in bad][:20])
