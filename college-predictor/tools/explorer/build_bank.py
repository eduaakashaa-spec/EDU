"""Build app/data/explorer/bank.json and creative.json for EduPulse-Explorer (Grades 7 to 10).
Inputs: the authored, independently re-solved text questions (E1..E5 JSON files from the scratch folder given as argv[1]) and the visual questions of the NID bank (built by code).
Run from college-predictor/:  python tools/explorer/build_bank.py <folder with bank_E1..E5.json and creative.json>"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
OUT = os.path.join(ROOT, 'app', 'data', 'explorer')
SRC = sys.argv[1]
SKILLS = {'MAT', 'SCI', 'ENG', 'LOG', 'SPA', 'DES', 'LAN'}
FAMS = {'JEE', 'UCD', 'NAT', 'IAT', 'APT'}
BAD = ('collegedekho', 'careers360', 'collegedunia', 'shiksha', 'getmyuni', 'toprankers', 'creativedge', 'whatsapp')

out = []
for k in range(1, 6):
    for i, q in enumerate(json.load(open(os.path.join(SRC, 'bank_E%d.json' % k), encoding='utf-8'))):
        assert q['skill'] in SKILLS and len(q['opts']) == 4 and 0 <= q['ans'] < 4 and len(set(q['opts'])) == 4 and q['why'], (k, i)
        assert q['grade'] in ('7-8', '9-10', 'all') and q['diff'] in (1, 2, 3), (k, i)
        fam = [f for f in q['fam'] if f in FAMS]
        assert fam, (k, i)
        d = {'id': 'T%d-%03d' % (k, i), 'skill': q['skill'], 'topic': q['topic'], 'grade': q['grade'], 'diff': q['diff'], 'fam': fam, 'q': q['q'],
             'opts': [{'t': o} for o in q['opts']], 'ans': q['ans'], 'why': q['why'], 'style': q.get('style', ''), 'src': 'auth'}
        if q.get('passage'):
            d['passage'] = q['passage']
            d['group'] = q.get('group')
        out.append(d)

nid = json.load(open(os.path.join(ROOT, 'app', 'data', 'nid', 'bank.json'), encoding='utf-8'))
DIFF = {'mirror': 1, 'rotate': 2, 'chiral': 3, 'fold': 3, 'cube': 3, 'matrix': 2, 'analogy': 2, 'series': 1, 'oddsize': 1, 'oddshade': 1, 'clock': 2, 'symmetry': 1, 'squares': 2, 'wheel': 1}
for q in nid:
    if q.get('src') != 'visual':
        continue
    gen = q.get('gen', '')
    sk = 'DES' if q['sec'] == 'CLR' else 'SPA' if q['sec'] == 'SPA' or gen in ('symmetry', 'squares') else 'LOG'
    fam = ['UCD'] if sk == 'DES' else ['UCD', 'NAT'] if sk == 'SPA' else ['UCD', 'APT']
    out.append({'id': 'X' + q['id'], 'skill': sk, 'topic': ('Spatial: ' if sk == 'SPA' else 'Visual reasoning: ' if sk == 'LOG' else 'Colour: ') + q['topic'].lower(),
                'grade': 'all', 'diff': DIFF.get(gen, 2), 'fam': fam, 'q': q['q'], 'svg': q.get('svg'), 'opts': q['opts'] if isinstance(q['opts'][0], dict) else [{'t': o} for o in q['opts']],
                'ans': q['ans'], 'why': q['why'], 'style': 'Design and aptitude exams show a figure and ask what it becomes, matches or continues.', 'src': 'visual'})
ids = [q['id'] for q in out]
assert len(set(ids)) == len(ids)
blob = json.dumps(out, ensure_ascii=False).lower()
assert not [b for b in BAD if b in blob]
os.makedirs(OUT, exist_ok=True)
json.dump(out, open(os.path.join(OUT, 'bank.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
cr = json.load(open(os.path.join(SRC, 'creative.json'), encoding='utf-8'))
for c in cr:
    assert sum(r['marks'] for r in c['rubric']) == 10, c['id']
json.dump(cr, open(os.path.join(OUT, 'creative.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
import collections
print(len(out), collections.Counter(q['skill'] for q in out), collections.Counter(q['grade'] for q in out), len(cr))
