"""JEE Main 2025 and 2024 previous-year B.Tech papers (official NTA paper images, official final key, chapter tags): live in the mock centre and the Reinforcement bank, grouped by year.
Run from college-predictor/:  python tests/test_jee_pyq_2425.py"""
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
from app.models_reinforce import RfQuestion, RfQuestionImage  # noqa: E402
from app.services import pulse_jee as pj, reinforce as rf  # noqa: E402

DATA = os.path.join(ROOT, 'app', 'data', 'jee_mock', 'data')
P25 = ['P250402S1', 'P250403S1', 'P250403S2', 'P250404S2', 'P250407S1', 'P250407S2', 'P250408S2']
P24 = ['P240406S1', 'P240406S2', 'P240408S1', 'P240408S2', 'P240409S2']
SUBJ = {'MATH': 'Mathematics', 'PHY': 'Physics', 'CHEM': 'Chemistry'}
codes = {s: {c for c, _n, _p in chs} for s, chs in rf.JEE_TAXONOMY.items()}

metas = {p['y']: p for p in pj.papers()}
valid = pj.valid_papers()
expect_bank = 0
chapters = set()
for y in P25 + P24:
    assert metas[y]['ready'] and metas[y].get('tagged') and y in valid, y
    d = json.load(open(os.path.join(DATA, y + '.json'), encoding='utf-8'))
    qs = d['qs']
    n = 75 if y in P25 else 90
    assert len(qs) == n and d['key'] == 'applied' and d.get('tagged') and len({q['qid'] for q in qs}) == n, y   # one English copy of each question
    assert [q['n'] for q in qs] == list(range(1, n + 1))
    per = n // 3
    assert [q['subj'] for q in qs] == ['MATH'] * per + ['PHY'] * per + ['CHEM'] * per
    assert sum(q['t'] == 'NAT' for q in qs) == (15 if n == 75 else 30)
    if n == 90:
        assert metas[y]['total'] == 90 and metas[y]['n'] == 75 and all(s.get('choose') == 5 for s in d['sections'] if s['type'] == 'NAT')
    for q in qs:
        a = q['acc']
        assert a.get('bonus') or a.get('sets') or a.get('ranges'), (y, q['n'])
        if q['t'] == 'MCQ' and not a.get('bonus'):
            assert set(''.join(a['sets'])) <= set('ABCD'), (y, q['n'])
        assert q['cat'] in codes[SUBJ[q['subj']]] and q['lvl'] in (1, 2, 3) and q['chapter'], (y, q['n'])
        assert q['img'].startswith('data:image/webp') and len(q.get('oids') or []) == (4 if q['t'] == 'MCQ' else 0), (y, q['n'])
        if not a.get('bonus') and (q['t'] == 'NAT' or len(a['sets']) == 1):
            expect_bank += 1
            chapters.add(q['chapter'])
# dropped questions in the key become full marks to all
assert json.load(open(os.path.join(DATA, 'P250403S1.json'), encoding='utf-8'))['qs'][36]['acc'] == {'bonus': True}
assert json.load(open(os.path.join(DATA, 'P240406S1.json'), encoding='utf-8'))['qs'][5]['acc'] == {'bonus': True}

app = create_app()
app.config['WTF_CSRF_ENABLED'] = False
with app.app_context():
    db.create_all()
    rf.seed_taxonomy()
    n = rf.seed_pyq()
    mine = RfQuestion.query.filter(RfQuestion.qid.op('GLOB')('JEE-P2[45]*')).all()
    assert len(mine) == expect_bank and all(q.status == 'approved' and q.exam == 'JEE' for q in mine), (len(mine), expect_bank)
    assert RfQuestionImage.query.filter(RfQuestionImage.qid.op('GLOB')('JEE-P2[45]*'), RfQuestionImage.kind == 'q').count() == expect_bank
    assert rf.seed_pyq() == 0
js = open(os.path.join(ROOT, 'app', 'data', 'jee_mock', 'app.html'), encoding='utf-8').read()
assert 'class="yfilter"' in js and "case 'yf'" in js and 'function pyqBlock' in js                                   # papers are grouped by year with a filter
print('jee 2025/2024 checks passed')
