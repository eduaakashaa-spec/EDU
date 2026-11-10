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

JAN = ['J0121S1', 'J0121S2', 'J0122S1', 'J0122S2', 'J0123S1', 'J0123S2', 'J0124S1', 'J0124S2', 'J0128S1', 'J0128S2']
metas = {p['y']: p for p in pj.papers()}
valid = pj.valid_papers()
total = nat_multi = 0
all_qs = {}
for y in JAN:
    assert metas[y]['ready'] and metas[y]['recreated'] and y in valid, y
    d = json.load(open(os.path.join(DATA, y + '.json'), encoding='utf-8'))
    qs = d['qs']
    assert 60 <= len(qs) <= 75 and d['max'] == 4 * len(qs) and [q['n'] for q in qs] == list(range(1, len(qs) + 1)) and d['tagged'], y
    assert [q['subj'] for q in qs] == sorted((q['subj'] for q in qs), key=['MATH', 'PHY', 'CHEM'].index)
    assert 12 <= sum(q['t'] == 'NAT' for q in qs) <= 15, y
    for q in qs:
        assert q['cat'] in codes[SUBJ[q['subj']]] and q['lvl'] in (1, 2, 3) and q['stem'] and len(q['steps']) >= 2, (y, q['n'])
        if q['t'] == 'MCQ':
            assert len(q['opts']) == 4 and q['acc']['sets'][0] in 'ABCD'
        else:
            nat_multi += len(q['acc']['ranges']) > 1
            assert all(lo == hi for lo, hi in q['acc']['ranges'])
        assert not q['fig'] or q['fig'].lstrip().startswith('<svg')
    blob = json.dumps(d, ensure_ascii=False).lower()
    assert not any(w in blob for w in ('matrixedu', 'matrix jee', 'matrix academy', 'official answer nta')), y        # no third-party branding or booklet text carried over
    assert len({q['qid'] for q in qs}) >= len(qs) - 1, y                                                           # one booklet misprints a repeated id
    all_qs[y] = qs
    total += len(qs)
assert total >= 640 and nat_multi == 1, (total, nat_multi)                                                           # 23 Jan Shift 1 Chemistry Q72: the key accepts 3 or 6
assert not any(q['qid'] in ('8606541395',) for q in all_qs['J0123S1'])                                               # a question the key shows as dropped is not in the paper
app = create_app()
app.config['WTF_CSRF_ENABLED'] = False
with app.app_context():
    db.create_all()
    rf.seed_taxonomy()
    n = rf.seed_recreated()
    for y in JAN:
        qs = all_qs[y]
        jq = RfQuestion.query.filter(RfQuestion.qid.like('JEE-%s-%%' % y)).all()
        keep = [q for q in qs if not q['fig'] and not any('<svg' in o for o in (q.get('opts') or []))]
        assert len(jq) == len(keep) and all(q.status == 'approved' for q in jq), y                             # figure questions stay out of the bank
    assert rf.seed_recreated() == 0
print('jee jan 2026 checks passed')
