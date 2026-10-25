"""Turn an NTA 'question paper' PDF export (questions and options are images) into a paper JSON for the JEE mock centre.

    python tools/jee_mock/extract_pyq.py "B Tech 2nd Apr 2026 Shift 1.pdf" P0402S1 [OUT_DIR]

Each question becomes one WebP image: the stem, then the four options labelled A-D (NTA prints option ids, not letters; the ids are kept
as `oids` so an answer key given as option ids can be applied). The PDF carries NO answer key, so the output has no `acc`/`disp`;
use apply_key.py to add the official key. A paper without a key is shown to members as "not yet available".
"""
import base64
import io
import json
import os
import re
import sys

import pdfplumber
import pypdfium2 as pdfium
from PIL import Image, ImageDraw, ImageFont

SCALE = 2.0
MAX_W = 900


def font(size):
    for f in ('arialbd.ttf', 'arial.ttf', 'DejaVuSans-Bold.ttf', 'DejaVuSans.ttf'):
        try:
            return ImageFont.truetype(f, size)
        except OSError:
            continue
    return ImageFont.load_default()


def events(pdf):
    """Walk the document in reading order and yield ('Q', n, qid, type) / ('OPTS',) / ('RESP',) / ('SEC', title) / ('IMG', page, bbox)."""
    ev = []
    for pi, page in enumerate(pdf.pages):
        for ln in page.extract_text_lines():
            t = ln['text'].strip()
            m = re.match(r'Question Number\s*:\s*(\d+)\s+Question Id\s*:\s*(\d+)\s+Question Type\s*:\s*(\w+)', t)
            if m:
                ev.append((pi, ln['top'], 0, ('Q', int(m.group(1)), m.group(2), m.group(3))))
            elif t.startswith('Options :'):
                ev.append((pi, ln['top'], 0, ('OPTS',)))
            elif t.startswith('Response Type'):
                ev.append((pi, ln['top'], 0, ('RESP',)))
            elif re.match(r'^(Mathematics|Physics|Chemistry) Section [AB]', t):
                ev.append((pi, ln['top'], 0, ('SEC', t)))
            else:
                m = re.match(r'^(\d{6,})\.\s*$', t)
                if m:
                    ev.append((pi, ln['top'], 1, ('OID', m.group(1))))
        for im in page.images:
            ev.append((pi, im['top'], 2, ('IMG', pi, (im['x0'], im['top'], im['x1'], im['bottom']))))
    ev.sort(key=lambda e: (e[0], e[1], e[2]))
    return [e[3] for e in ev]


def parse(pdf):
    qs, cur, region, sec = [], None, None, None
    secs = []
    for e in events(pdf):
        k = e[0]
        if k == 'SEC':
            region = None
            sec = e[1]
            secs.append(sec)
        elif k == 'Q':
            cur = {'n': e[1], 'qid': e[2], 't': 'NAT' if e[3] == 'SA' else 'MCQ', 'stem': [], 'opts': [], 'oids': [], 'sec': sec}
            qs.append(cur)
            region = 'stem'
        elif k == 'OPTS':
            region = 'opts'
        elif k == 'RESP':
            region = None
        elif k == 'OID' and cur is not None and region == 'opts':
            cur['oids'].append(e[1])
        elif k == 'IMG' and cur is not None and region in ('stem', 'opts'):
            cur['stem' if region == 'stem' else 'opts'].append((e[1], e[2]))
    return qs, secs


def compose(q, pages):
    def crop(item):
        pi, (x0, t, x1, b) = item
        return pages[pi].crop((int(x0 * SCALE), int(t * SCALE), int(x1 * SCALE), int(b * SCALE))).convert('RGB')
    stems = [crop(i) for i in q['stem']]
    opts = [crop(i) for i in q['opts']]
    pad, gap, lab_w = 8, 10, 46
    f = font(30)
    w = max([im.width for im in stems] + [im.width + lab_w for im in opts] + [200]) + 2 * pad
    h = pad + sum(im.height + gap for im in stems) + sum(max(im.height, 40) + gap for im in opts) + pad
    canvas = Image.new('RGB', (w, h), 'white')
    y = pad
    for im in stems:
        canvas.paste(im, (pad, y))
        y += im.height + gap
    d = ImageDraw.Draw(canvas)
    for i, im in enumerate(opts):
        hh = max(im.height, 40)
        d.text((pad + 2, y + (hh - 30) // 2), '(%s)' % 'ABCD'[i], fill=(14, 58, 138), font=f)
        canvas.paste(im, (pad + lab_w, y + (hh - im.height) // 2))
        y += hh + gap
    if canvas.width > MAX_W:
        k = MAX_W / canvas.width
        canvas = canvas.resize((MAX_W, int(canvas.height * k)), Image.LANCZOS)
    return canvas


def main(pdf_path, paper_id, out_dir=None):
    out_dir = out_dir or os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'app', 'data', 'jee_mock', 'data')
    with pdfplumber.open(pdf_path) as pdf:
        qs, secs = parse(pdf)
    doc = pdfium.PdfDocument(pdf_path)
    pages = [doc[i].render(scale=SCALE).to_pil() for i in range(len(doc))]
    problems = []
    for q in qs:
        if not q['stem']:
            problems.append('Q%d has no stem image' % q['n'])
        if q['t'] == 'MCQ' and (len(q['opts']) != 4 or len(q['oids']) != 4):
            problems.append('Q%d has %d option images / %d ids' % (q['n'], len(q['opts']), len(q['oids'])))
    subj_of = lambda s: 'MATH' if s.startswith('Mathematics') else 'PHY' if s.startswith('Physics') else 'CHEM'
    out_qs, sections = [], []
    for q in sorted(qs, key=lambda x: x['n']):
        im = compose(q, pages)
        buf = io.BytesIO()
        im.save(buf, 'WEBP', quality=80, method=6)
        d = {'n': q['n'], 't': q['t'], 'subj': subj_of(q['sec']), 'cat': None, 'qid': q['qid'], 'img': 'data:image/webp;base64,' + base64.b64encode(buf.getvalue()).decode(), 'w': im.width, 'h': im.height}
        if q['t'] == 'MCQ':
            d['oids'] = q['oids']
        out_qs.append(d)
    for s in dict.fromkeys(secs):
        nums = [q['n'] for q in qs if q['sec'] == s]
        sections.append({'type': 'MCQ' if 'Section A' in s else 'NAT', 'subj': subj_of(s), 'lo': min(nums), 'hi': max(nums), 'right': 4, 'wrong': -1, 'partial': False})
    paper = {'year': paper_id, 'mins': 180, 'max': 300, 'sections': sections, 'qs': out_qs, 'key': 'pending'}
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, paper_id + '.json')
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(paper, f, separators=(',', ':'))
    print(os.path.basename(pdf_path), '->', path, '|', len(out_qs), 'questions,', len(sections), 'sections,', os.path.getsize(path) // 1024, 'KB', '| PROBLEMS: ' + '; '.join(problems) if problems else '| ok')
    return paper, problems


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None)
