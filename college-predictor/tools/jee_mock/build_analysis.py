"""Build app/data/jee_mock/analysis_2026s2.json: chapter-wise analysis of the tagged JEE Main 2026 Session 2 (April) B.Tech papers.

    python tools/jee_mock/build_analysis.py

Reads the paper JSONs (cat, chapter, lvl, t, subj on each question) and writes a small file the public analysis page reads, so the page never loads the
1.5 MB paper files. Chapter tags and difficulty are EduAakashaA's reading of the official papers, not NTA data.
"""
import json
import os
import re
import sys
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)
DATA = os.path.join(ROOT, 'app', 'data', 'jee_mock', 'data')
SUBJ = {'MATH': 'Mathematics', 'PHY': 'Physics', 'CHEM': 'Chemistry'}
MON = {'01': 'Jan', '02': 'Feb', '03': 'Mar', '04': 'Apr'}


def main():
    from app.services.reinforce import JEE_TAXONOMY
    idx = json.load(open(os.path.join(DATA, 'index.json'), encoding='utf-8'))['papers']
    metas = [p for p in idx if re.match(r'P\d{4}S\d$', p['y']) and p.get('tagged') and p.get('ready')]
    names = {c: n for chs in JEE_TAXONOMY.values() for c, n, _p in chs}
    order = {c: i for chs in JEE_TAXONOMY.values() for i, (c, _n, _p) in enumerate(chs)}
    papers, table = [], {s: defaultdict(lambda: {'per': [0] * len(metas), 'mcq': 0, 'nat': 0, 'lvl': [], 'topics': Counter()}) for s in SUBJ}
    diff = {s: Counter() for s in SUBJ}
    for j, m in enumerate(metas):
        d = json.load(open(os.path.join(DATA, m['y'] + '.json'), encoding='utf-8'))
        papers.append({'y': m['y'], 'short': m['short'].replace(' · ', ' ')})
        for q in d['qs']:
            subj = q['subj']
            r = table[subj][q['cat']]
            r['per'][j] += 1
            r['mcq' if q['t'] == 'MCQ' else 'nat'] += 1
            r['lvl'].append(q.get('lvl') or 2)
            r['topics'][q.get('chapter') or names[q['cat']]] += 1
            diff[subj][q.get('lvl') or 2] += 1
    n_papers = len(metas)
    out = {'title': 'JEE Main 2026 Session 2 (April) chapter analysis', 'papers': papers, 'n_papers': n_papers, 'subjects': []}
    for subj, name in SUBJ.items():
        rows, total = [], sum(sum(r['per']) for r in table[subj].values())
        for code, r in table[subj].items():
            t = sum(r['per'])
            rows.append({'code': code, 'name': names[code], 'per': r['per'], 'total': t, 'avg': round(t / n_papers, 1), 'share': round(100.0 * t / total, 1) if total else 0,
                         'mcq': r['mcq'], 'nat': r['nat'], 'lvl': round(sum(r['lvl']) / len(r['lvl']), 2), 'in_every': all(x > 0 for x in r['per']),
                         'topics': [[k, v] for k, v in r['topics'].most_common(6)]})
        rows.sort(key=lambda x: (-x['total'], order.get(x['code'], 99)))
        seen = {r['code'] for r in rows}
        for code, cname in ((c, n) for c, n, _p in JEE_TAXONOMY[name] if c not in seen):
            rows.append({'code': code, 'name': cname, 'per': [0] * n_papers, 'total': 0, 'avg': 0, 'share': 0, 'mcq': 0, 'nat': 0, 'lvl': 0, 'in_every': False, 'topics': []})
        out['subjects'].append({'key': subj, 'name': name, 'total': total, 'chapters': rows, 'diff': {str(k): diff[subj][k] for k in (1, 2, 3)},
                                'avg_lvl': round(sum(k * v for k, v in diff[subj].items()) / max(1, sum(diff[subj].values())), 2)})
    path = os.path.join(ROOT, 'app', 'data', 'jee_mock', 'analysis_2026s2.json')
    json.dump(out, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('papers', n_papers, 'questions', sum(s['total'] for s in out['subjects']), '->', path)


if __name__ == '__main__':
    main()
