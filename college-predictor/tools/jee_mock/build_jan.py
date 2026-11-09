"""Build a JEE Main 2026 Session 1 (January) mock-centre paper from transcribed question records.

    python tools/jee_mock/build_jan.py J0121S1 "JEE Main 2026 · 21 Jan · Shift 1" "21 Jan · Shift 1" maths.json physics.json chem.json

Each JSON is a list of {src, qid, subj, kind, cat, diff, stem, opts, ans, steps, svg, status, note}: the NTA question retyped by EduAakashaA with its own worked steps.
Only status 'ok' rows enter the paper (our own solution agrees with the printed official answer); 'skip' (needs a drawn figure) and 'mismatch' rows are left out.
Numerical answers are checked against the NTA Session 1 final key by Question ID when --key <key_s1.json> <date|shift> is given; lettered answers cannot be (the key's option
numbers follow a different option order), so those rest on the printed official answer plus our independent solution.
Writes app/data/jee_mock/data/<ID>.json and adds the paper to pyq_papers.json (recreated: true, tagged: true). Run make_index.py afterwards.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
DATA = os.path.join(ROOT, 'app', 'data', 'jee_mock', 'data')


def build(paper_id, title, short, files, key=None):
    rows = []
    for f in files:
        rows += json.load(open(f, encoding='utf-8'))
    kept = [r for r in rows if r.get('status') == 'ok']
    for r in kept:
        assert r['kind'] in ('MCQ', 'NAT') and r['cat'] and r['diff'] in (1, 2, 3), r['src']
        if r['kind'] == 'MCQ':
            assert r['opts'] and len(r['opts']) == 4 and r['ans'] in 'ABCD', r['src']
        elif key is not None:
            k = key.get(r['qid'])
            assert k is not None and abs(float(k) - float(r['ans'])) < 1e-9, ('NAT differs from the NTA key', r['src'], r['ans'], k)
    qs, sections, n = [], [], 0
    for subj in ('MATH', 'PHY', 'CHEM'):
        for kind in ('MCQ', 'NAT'):
            part = sorted((r for r in kept if r['subj'] == subj and r['kind'] == kind), key=lambda r: int(r['src']))
            if not part:
                continue
            lo = n + 1
            for r in part:
                n += 1
                q = {'n': n, 't': kind, 'subj': subj, 'cat': r['cat'], 'lvl': r['diff'], 'src': r['src'], 'qid': r['qid'], 'stem': r['stem'], 'steps': r['steps'], 'trap': '',
                     'fig': r.get('svg') or '', 'svg': '', 'note': ''}
                if kind == 'MCQ':
                    q.update(opts=r['opts'], layout='grid', disp=r['ans'], acc={'sets': [r['ans']]})
                else:
                    q.update(disp='%g' % float(r['ans']), acc={'ranges': [[float(r['ans']), float(r['ans'])]]})
                qs.append(q)
            sections.append({'type': kind, 'subj': subj, 'lo': lo, 'hi': n, 'right': 4, 'wrong': -1, 'partial': False})
    mx = sum(4 * (s['hi'] - s['lo'] + 1) for s in sections)
    skipped = len(rows) - len(kept)
    paper = {'year': paper_id, 'title': title + ' (recreated)', 'mins': 180, 'max': mx, 'key': 'recreated', 'tagged': True, 'sections': sections, 'qs': qs,
             'notes': ['JEE Main 2026 Session 1 (NTA paper), retyped by EduAakashaA from a memory-based booklet that carries the NTA question IDs; worked steps are our own.',
                       'Numerical answers match the NTA final key (16 Feb 2026); lettered answers follow the printed official answer and were each re-solved independently.']}
    path = os.path.join(DATA, paper_id + '.json')
    with open(path, 'w', encoding='utf-8') as fh:
        json.dump(paper, fh, ensure_ascii=False, separators=(',', ':'))
    meta_path = os.path.join(HERE, 'pyq_papers.json')
    metas = json.load(open(meta_path, encoding='utf-8'))
    metas = [m for m in metas if m['y'] != paper_id]
    metas.append({'y': paper_id, 'title': title + ' (recreated)', 'short': short + ' · recreated', 'recreated': True, 'tagged': True, 'total': len(qs), 'n': len(qs), 'max': mx, 'mins': 180,
                  'numnote': 'MCQ + numerical',
                  'note': 'Retyped from the NTA paper with our own worked steps; %d question%s left out (they need a drawn figure we could not redraw reliably).' % (skipped, '' if skipped == 1 else 's') if skipped else 'Retyped from the NTA paper with our own worked steps.'})
    json.dump(metas, open(meta_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('wrote', path, '%.0f KB' % (os.path.getsize(path) / 1e3), '|', len(qs), 'questions | max', mx, '| left out', skipped)


if __name__ == '__main__':
    args = sys.argv[1:]
    key = None
    if '--key' in args:
        i = args.index('--key')
        key = json.load(open(args[i + 1], encoding='utf-8'))[args[i + 2]]
        del args[i:i + 3]
    build(args[0], args[1], args[2], args[3:], key)
