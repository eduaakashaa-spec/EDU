"""Build a JEE mock-centre paper from a hand-recreated question set (tools/jee_mock/recreated/<module>.py).

    python tools/jee_mock/build_recreated.py j2301s2 J2301S2 "JEE Main 2023 · 24 Jan · Shift 2" "24 Jan · Shift 2"

Writes app/data/jee_mock/data/<ID>.json (text questions with worked steps; answers lettered A-D or numeric) and adds the paper to tools/jee_mock/pyq_papers.json with `recreated: true`.
Run make_index.py afterwards. Questions keep the order Mathematics, Physics, Chemistry, MCQ before numerical; `n` is renumbered 1..N.
"""
import importlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(HERE, 'recreated'))
DATA = os.path.join(ROOT, 'app', 'data', 'jee_mock', 'data')
CHOOSE = 5


def build(modname, paper_id, title, short):
    mod = importlib.import_module(modname)
    rows = mod.Q
    order = [(s, k) for s in ('MATH', 'PHY', 'CHEM') for k in ('MCQ', 'NAT')]
    qs, sections, n = [], [], 0
    for subj, kind in order:
        part = sorted((r for r in rows if r[1] == subj and r[2] == kind), key=lambda r: r[0])
        if not part:
            continue
        lo = n + 1
        for src, _s, _k, cat, stem, opts, ans, steps in part:
            n += 1
            q = {'n': n, 't': kind, 'subj': subj, 'cat': cat, 'src': src, 'stem': stem, 'steps': steps, 'trap': '', 'fig': '', 'svg': '', 'note': ''}
            if kind == 'MCQ':
                assert opts and len(opts) == 4 and ans in 'ABCD', (src, ans)
                q.update(opts=opts, layout='grid', disp=ans, acc={'sets': [ans]})
            else:
                q.update(disp='%g' % ans, acc={'ranges': [[float(ans), float(ans)]]})
            qs.append(q)
        sec = {'type': kind, 'subj': subj, 'lo': lo, 'hi': n, 'right': 4, 'wrong': -1, 'partial': False}
        if kind == 'NAT':
            sec['choose'] = min(CHOOSE, n - lo + 1)
        sections.append(sec)
    mx = sum(s['right'] * (s['choose'] if s.get('choose') else s['hi'] - s['lo'] + 1) for s in sections)
    mcq = {s['subj']: s['hi'] - s['lo'] + 1 for s in sections if s['type'] == 'MCQ'}
    nat = {s['subj']: s['hi'] - s['lo'] + 1 for s in sections if s['type'] == 'NAT'}
    paper = {'year': paper_id, 'title': title + ' (recreated)', 'mins': 150, 'max': mx, 'key': 'recreated', 'sections': sections, 'qs': qs,
             'notes': [mod.SOURCE, 'Answers are not the NTA final key; each was checked by an independent EduAakashaA solution.']}
    os.makedirs(DATA, exist_ok=True)
    path = os.path.join(DATA, paper_id + '.json')
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(paper, f, ensure_ascii=False, separators=(',', ':'))
    meta_path = os.path.join(HERE, 'pyq_papers.json')
    metas = json.load(open(meta_path, encoding='utf-8')) if os.path.exists(meta_path) else []
    metas = [m for m in metas if m['y'] != paper_id]
    metas.append({'y': paper_id, 'title': title + ' (recreated)', 'short': short + ' · recreated', 'recreated': True, 'total': len(qs), 'n': mx // 4, 'max': mx, 'mins': 150,
                  'numnote': '%d + any 5 of %d' % (max(mcq.values()), max(nat.values())) if len(set(mcq.values())) == 1 and len(set(nat.values())) == 1 else 'MCQ + any 5 numerical',
                  'note': 'Questions retyped from the NTA paper; figure-based questions left out. Answers checked by EduAakashaA, not the NTA final key.'})
    json.dump(metas, open(meta_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('wrote', path, '%.0f KB' % (os.path.getsize(path) / 1e3), '|', len(qs), 'questions | max', mx, '| MCQ', mcq, 'NAT', nat)


if __name__ == '__main__':
    build(*sys.argv[1:5])
