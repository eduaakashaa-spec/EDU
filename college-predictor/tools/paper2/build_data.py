"""Assemble the JEE Paper 2 mock-centre data from extracted papers (extract_p2.py) and keys (keys.py).

    python tools/paper2/build_data.py <scratch dir>   (reads <scratch>/out/<id>/{meta.json,key.json,qNNN.webp})

Copies the question pictures to app/static/img/jee_p2/<id>/ and writes app/data/jee_p2/papers.json and keys.json. A question is left out (`skip`) when it has no picture, no key, or
accepts several options; the drawing questions of Paper 2A are marked by hand and are not in the mocks.
"""
import glob
import json
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
IMG = os.path.join(ROOT, 'app', 'static', 'img', 'jee_p2')
DATA = os.path.join(ROOT, 'app', 'data', 'jee_p2')

PAPERS = [
    # id, paper, date label, shift, year, sittings detail, numerical rule
    ('A2401S2', '2A', '24 Jan 2024', 'Shift 2', 2024, 5),
    ('B2401S2', '2B', '24 Jan 2024', 'Shift 2', 2024, 5),
    ('A2501S2', '2A', '30 Jan 2025', 'Shift 2', 2025, None),
    ('B2504S1', '2B', '9 Apr 2025', 'Shift 1', 2025, None),
]


def main(scratch):
    os.makedirs(DATA, exist_ok=True)
    papers, keys = {}, {}
    for pid, paper, date, shift, year, choose in PAPERS:
        src = os.path.join(scratch, 'out', pid)
        meta = json.load(open(os.path.join(src, 'meta.json')))
        key = json.load(open(os.path.join(src, 'key.json')))
        skip, why = [], {}
        for q in meta['qs']:
            if q['t'] == 'DRAW':
                continue
            n = str(q['n'])
            if not q.get('ok'):
                skip.append(q['n']); why[q['n']] = 'no picture'
            elif n not in key:
                skip.append(q['n']); why[q['n']] = 'no key or several accepted options'
        secs = []
        for s in meta['sections']:
            if s['sec'] == 'DRAW':
                continue
            row = {'sec': s['sec'], 't': s['t'], 'lo': s['lo'], 'hi': s['hi']}
            if s['t'] == 'NAT' and choose and s['n'] > choose:
                row['choose'] = choose                         # attempt any 5 of 10: only the first 5 answered are marked
            secs.append(row)
        n_all = max(q['n'] for q in meta['qs'] if q['t'] != 'DRAW')
        papers[pid] = {'paper': paper, 'year': year, 'date': date, 'shift': shift, 'n': n_all, 'sections': secs, 'skip': sorted(skip),
                       'title': 'JEE Main %d · %s · %s · Paper %s (%s)' % (year, date, shift, paper, 'B.Arch' if paper == '2A' else 'B.Planning'),
                       'minutes': 120 if paper == '2A' else 180,
                       'types': {str(q['n']): q['t'] for q in meta['qs'] if q['t'] != 'DRAW'}}
        keys[pid] = {k: v for k, v in key.items()}
        dest = os.path.join(IMG, pid)
        shutil.rmtree(dest, ignore_errors=True)
        os.makedirs(dest)
        for f in glob.glob(os.path.join(src, 'q*.webp')):
            shutil.copy(f, dest)
        print(pid, paper, n_all, 'questions; sections', [(s['sec'], s['t'], s['lo'], s['hi'], s.get('choose')) for s in secs], '; left out', why, '; dropped', sorted(int(k) for k, v in key.items() if v == 'bonus'))
    json.dump(papers, open(os.path.join(DATA, 'papers.json'), 'w'), indent=0)
    json.dump(keys, open(os.path.join(DATA, 'keys.json'), 'w'), separators=(',', ':'))


if __name__ == '__main__':
    main(sys.argv[1])
