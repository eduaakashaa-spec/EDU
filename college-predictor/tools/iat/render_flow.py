"""Render IAT paper questions as images for the older papers where questions flow down the page (2017, 2019, 2021, 2022).

Questions are numbered 1 to 60 straight through: 1-15 Biology, 16-30 Chemistry, 31-45 Mathematics, 46-60 Physics.
Option markers are 'A.' to 'D.' (2017: 'A' to 'D'). Stem and each option are cut out as separate images so the mock can shuffle them.
Usage: python tools/iat/render_flow.py <pdf> <year> <out_dir>
"""
import collections
import json
import os
import re
import sys
import warnings

warnings.filterwarnings('ignore')
import fitz  # noqa: E402
from PIL import Image  # noqa: E402

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render_papers import ZOOM, strip_slivers, trim  # noqa: E402
from layout import split  # noqa: E402
import io  # noqa: E402

SUBJ = ['Biology', 'Chemistry', 'Mathematics', 'Physics']


def grab(page, rect):
    pix = page.get_pixmap(matrix=fitz.Matrix(ZOOM, ZOOM), clip=rect, alpha=False)
    return Image.open(io.BytesIO(pix.tobytes('png'))).convert('RGB')


def save(parts, path):
    """parts: PIL images stacked top to bottom."""
    parts = [p for p in parts if p is not None]
    if not parts:
        return False
    w = max(p.width for p in parts)
    h = sum(p.height for p in parts)
    c = Image.new('RGB', (w, h), (255, 255, 255))
    y = 0
    for p in parts:
        c.paste(p, (0, y))
        y += p.height
    c = trim(c)
    if c is None:
        return False
    c = trim(strip_slivers(c)) or c
    c.save(path, 'WEBP', quality=72, method=6)
    return True


def main(pdf, year, out):
    doc = fitz.open(pdf)
    d = os.path.join(out, str(year))
    os.makedirs(d, exist_ok=True)
    nums = collections.Counter()
    for page in doc:
        for w in page.get_text('words'):
            if re.fullmatch(r'\d{1,2}\.', w[4]) and w[0] < 110:
                nums[round(w[0])] += 1
    lm = nums.most_common(1)[0][0]
    LM = {}
    for pi, page in enumerate(doc):
        c = collections.Counter(round(w[0]) for w in page.get_text('words') if re.fullmatch(r'\d{1,2}\.', w[4]) and w[0] < 110)
        LM[pi] = c.most_common(1)[0][0] if c else lm
    # question starts in document order: (page, y0, running index). Numbering may run 1 to 60 or restart at 1 in every subject.
    starts, prev = [], 0
    for pi, page in enumerate(doc):
        for w in sorted(page.get_text('words'), key=lambda w: (round(w[1]), w[0])):
            if re.fullmatch(r'\d{1,2}\.', w[4]) and abs(w[0] - LM[pi]) <= 9:
                n = int(w[4][:-1])
                if n == prev + 1 or (n == 1 and prev > 0 and prev % 15 == 0):
                    starts.append((pi, w[1] - 3, len(starts) + 1))
                    prev = n
    # the third value is the running position in the paper (1 to 60)
    items = []
    for k, (pi, y0, n) in enumerate(starts):
        segs = []
        if k + 1 < len(starts):
            npi, ny0, _ = starts[k + 1]
        else:
            npi, ny0 = len(doc) - 1, None
        for p in range(pi, npi + 1):
            top = y0 if p == pi else 40
            words = doc[p].get_text('words')
            ph = doc[p].rect.height
            lm = LM[p]
            foot = [w[1] for w in words if w[1] > ph - 90 and (w[4] == 'Page' or re.fullmatch(r'\d+', w[4]))]
            bottom = (min(foot) - 3) if foot else ph - 30
            if p == npi and ny0 is not None:
                bottom = min(bottom, ny0 - 2)
            # a subject heading alone on a line ends the region
            for w in words:
                if w[4] in SUBJ and w[1] > top + 6 and abs(w[0] - lm) > 4 and w[1] < bottom:
                    line = [x for x in words if abs(x[1] - w[1]) < 3]
                    if len(line) == 1:
                        bottom = min(bottom, w[1] - 3)
            segs.append((p, top, bottom))
        items.append((n, segs))
    res = []
    for n, segs in items:
        subj = SUBJ[min(3, (n - 1) // 15)]
        pre = '%s%02d' % (subj[:3].lower(), (n - 1) % 15 + 1)
        marks = []
        for si, (p, top, bottom) in enumerate(segs):
            words = doc[p].get_text('words')
            lm = LM[p]
            for w in words:
                m = re.fullmatch(r'([A-D])\.?', w[4])
                if m and top - 1 <= w[1] <= bottom and lm + 4 <= w[0] <= lm + 70:
                    line = [x for x in words if abs(x[1] - w[1]) < 3 and x[0] < w[0] - 2]
                    if not line:
                        marks.append((si, p, w[0], w[2], w[1], m.group(1)))
        marks.sort(key=lambda m: (m[0], m[4]))
        letters = ''.join(m[5] for m in marks)
        ok = letters == 'ABCD'
        if ok:
            _seen = False
            _bs = {}
            for mk in marks:
                _bs.setdefault(mk[0], []).append(mk)
            for si, (p, top, bottom) in enumerate(segs):
                ms = _bs.get(si)
                if ms:
                    _s, _o, lay = split(doc[p], top, bottom, LM[p], [fitz.Rect(m[2], m[4], m[3], m[4] + 11) for m in ms], doc[p].rect.width - 20, first_page=not _seen)
                    _seen = True
                    if not lay:
                        ok = False
        right = max([s[2] for s in segs] + [0])
        stem_parts, opts, full = [], [], []
        if ok:
            by_seg = {}
            for mk in marks:
                by_seg.setdefault(mk[0], []).append(mk)
            seen = False
            for si, (p, top, bottom) in enumerate(segs):
                page = doc[p]
                right = page.rect.width - 20
                ms = by_seg.get(si)
                if not ms:
                    if not seen:
                        stem_parts.append(grab(page, fitz.Rect(LM[p] - 6, top, right, bottom)))
                    continue
                mrects = [fitz.Rect(m[2], m[4], m[3], m[4] + 11) for m in ms]
                s_rect, o_rects, _lay = split(page, top, bottom, LM[p], mrects, right, first_page=not seen)
                if not seen and s_rect is not None:
                    stem_parts.append(grab(page, s_rect))
                seen = True
                for m, r in zip(mrects, o_rects):
                    if r is None:
                        opts.append(None)
                        continue
                    r.x0 = max(r.x0, m.x1 + 1)
                    opts.append(grab(page, r))
        stem_f = os.path.join(d, pre + '_s.webp')
        has_stem = save(stem_parts, stem_f) if ok else False
        ofiles = []
        if ok:
            for i, im in enumerate(opts):
                f = os.path.join(d, '%s_o%d.webp' % (pre, i))
                ofiles.append(os.path.basename(f) if save([im], f) else '')
        full_f = ''
        if not ok:
            f = os.path.join(d, pre + '_full0.webp')
            if save([grab(doc[p], fitz.Rect(LM[p] - 6, t, doc[p].rect.width - 20, b)) for p, t, b in segs], f):
                full_f = os.path.basename(f)
        res.append(dict(subj=subj, n=(n - 1) % 15 + 1, qn=n, ok=ok and has_stem and '' not in ofiles, stem=[os.path.basename(stem_f)] if has_stem else [],
                        opts=ofiles, full=[full_f] if full_f else [], pages=sorted({s[0] + 1 for s in segs})))
    json.dump(res, open(os.path.join(out, '%s.json' % year), 'w', encoding='utf-8'), indent=1)
    print(year, len(res), 'questions; problems:', [(r['subj'][:3], r['n']) for r in res if not r['ok']])


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3])
