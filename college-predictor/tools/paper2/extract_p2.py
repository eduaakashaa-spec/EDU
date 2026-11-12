"""Cut a JEE (Main) Paper 2 (B.Arch = 2A, B.Planning = 2B) NTA question-paper export into one picture per question.

    python tools/paper2/extract_p2.py "<export.pdf>" <paper id e.g. A2401S2> <out dir>

Reuses tools/jee_mock/extract_pyq.py (events, compose). Sections of a Paper 2 export: 'Mathematics Section A' (MCQ), 'Mathematics Section B' (numerical, type SA),
'Aptitude Test' (MCQ), 'Planning' (MCQ, 2B only) and 'Drawing' (type SUBJECTIVE, marked by hand: left out of the mocks). Writes <out>/<id>/qNNN.webp and <out>/<id>/meta.json:
{id, qs: [{n, qid, t: MCQ|NAT|DRAW, sec: MATH|APT|PLAN|DRAW, oids: [4 option ids] (MCQ), w, h}], sections: [{sec, t, lo, hi, n}]}.
"""
import io
import json
import os
import re
import sys

import pdfplumber
import pypdfium2 as pdfium

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'jee_mock'))
import extract_pyq as E  # noqa: E402

SECTION = re.compile(r'^(Mathematics Section [AB]|Aptitude Test|Planning|Drawing)\s*$')


def events(pdf):
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
            elif SECTION.match(t):
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
    for e in events(pdf):
        k = e[0]
        if k == 'SEC':
            region, sec = None, e[1]
        elif k == 'Q':
            t = {'SA': 'NAT', 'MCQ': 'MCQ'}.get(e[3], 'DRAW')
            cur = {'n': e[1], 'qid': e[2], 't': t, 'stem': [], 'opts': [], 'oids': [], 'sec': sec}
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
    seen, first = set(), []                                  # every question is printed twice (English, Hindi): keep the first
    for q in qs:
        if q['qid'] not in seen:
            seen.add(q['qid'])
            first.append(q)
    return first


CODE = {'Mathematics Section A': ('MATH', 'MCQ'), 'Mathematics Section B': ('MATH', 'NAT'), 'Aptitude Test': ('APT', 'MCQ'), 'Planning': ('PLAN', 'MCQ'), 'Drawing': ('DRAW', 'DRAW')}


def main(pdf_path, pid, out_root):
    with pdfplumber.open(pdf_path) as pdf:
        qs = parse(pdf)
    doc = pdfium.PdfDocument(pdf_path)
    pages = [doc[i].render(scale=E.SCALE).to_pil() for i in range(len(doc))]
    out = os.path.join(out_root, pid)
    os.makedirs(out, exist_ok=True)
    rows, problems = [], []
    for q in sorted(qs, key=lambda x: x['n']):
        sec, typ = CODE[q['sec']]
        row = {'n': q['n'], 'qid': q['qid'], 't': typ, 'sec': sec}
        if typ == 'DRAW':
            rows.append(row)
            continue
        if not q['stem']:
            problems.append('Q%d has no stem image' % q['n'])
            row['ok'] = False
        elif typ == 'MCQ' and (len(q['opts']) != 4 or len(q['oids']) != 4):
            problems.append('Q%d has %d option images / %d ids' % (q['n'], len(q['opts']), len(q['oids'])))
            row['ok'] = False
        else:
            row['ok'] = True
            im = E.compose(q, pages)
            im.save(os.path.join(out, 'q%03d.webp' % q['n']), 'WEBP', quality=80, method=6)
            row.update(w=im.width, h=im.height)
        if typ == 'MCQ':
            row['oids'] = q['oids']
        rows.append(row)
    sections = []
    for q in rows:
        if not sections or sections[-1]['sec'] != q['sec'] or sections[-1]['t'] != q['t']:
            sections.append({'sec': q['sec'], 't': q['t'], 'lo': q['n'], 'hi': q['n']})
        sections[-1]['hi'] = q['n']
    for s in sections:
        s['n'] = s['hi'] - s['lo'] + 1
    json.dump({'id': pid, 'pdf': os.path.basename(pdf_path), 'qs': rows, 'sections': sections}, open(os.path.join(out, 'meta.json'), 'w'), separators=(',', ':'))
    print(pid, len(rows), 'questions', sections, '| PROBLEMS: ' + '; '.join(problems) if problems else '| ok', flush=True)


if __name__ == '__main__':
    main(*sys.argv[1:4])
