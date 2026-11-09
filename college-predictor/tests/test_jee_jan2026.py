"""JEE Main 2026 Session 1 (January) 21 Jan Shift 1: retyped from the NTA paper, own worked steps, numerical answers equal to the NTA final key, live in the mock centre and the bank.
Run from college-predictor/:  python tests/test_jee_jan2026.py"""
import json
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
_fd, _db = tempfile.mkstemp(suffix='.db')
os.close(_fd)
os.environ.update(DATABASE_URL='sqlite:///' + _db, SECRET_KEY='test', FLASK_DEBUG='0')

from app import create_app  # noqa: E402
from app.extensions import db  # noqa: E402
from app.models_reinforce import RfQuestion  # noqa: E402
from app.services import pulse_jee as pj, reinforce as rf  # noqa: E402

DATA = os.path.join(ROOT, 'app', 'data', 'jee_mock', 'data')
codes = {s: {c for c, _n, _p in chs} for s, chs in rf.JEE_TAXONOMY.items()}
SUBJ = {'MATH': 'Mathematics', 'PHY': 'Physics', 'CHEM': 'Chemistry'}

meta = {p['y']: p for p in pj.papers()}['J0121S1']
assert meta['ready'] and meta['recreated'] and 'J0121S1' in pj.valid_papers()
d = json.load(open(os.path.join(DATA, 'J0121S1.json'), encoding='utf-8'))
qs = d['qs']
assert len(qs) == 71 and d['max'] == 4 * 71 and [q['n'] for q in qs] == list(range(1, 72)) and d['tagged']
assert sum(q['t'] == 'NAT' for q in qs) == 15 and len({q['qid'] for q in qs}) == 71
for q in qs:
    assert q['cat'] in codes[SUBJ[q['subj']]] and q['lvl'] in (1, 2, 3) and q['stem'] and len(q['steps']) >= 2, q['n']
    if q['t'] == 'MCQ':
        assert len(q['opts']) == 4 and q['acc']['sets'][0] in 'ABCD'
    else:
        lo, hi = q['acc']['ranges'][0]
        assert lo == hi
assert sum(1 for q in qs if q['fig']) >= 5 and all(q['fig'].lstrip().startswith('<svg') for q in qs if q['fig'])
assert [(s['subj'], s['type'], s['hi'] - s['lo'] + 1) for s in d['sections']] == [('MATH', 'MCQ', 20), ('MATH', 'NAT', 5), ('PHY', 'MCQ', 20), ('PHY', 'NAT', 5), ('CHEM', 'MCQ', 16), ('CHEM', 'NAT', 5)]
blob = json.dumps(d, ensure_ascii=False).lower()
assert not any(w in blob for w in ('matrixedu', 'matrix jee', 'matrix academy', 'official answer nta'))              # no third-party branding or booklet text carried over
app = create_app()
app.config['WTF_CSRF_ENABLED'] = False
with app.app_context():
    db.create_all()
    rf.seed_taxonomy()
    n = rf.seed_recreated()
    jq = RfQuestion.query.filter(RfQuestion.qid.like('JEE-J0121S1-%')).all()
    nofig = [q for q in qs if not q['fig']]
    assert len(jq) == len(nofig) and all(q.status == 'approved' for q in jq)                                    # questions with a redrawn figure stay out of the bank
    assert rf.seed_recreated() == 0
print('jee jan 2026 checks passed')
