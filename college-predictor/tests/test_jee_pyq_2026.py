"""JEE Main 2026 Session 2 (April) papers: official key applied, every question tagged by chapter, live in the mock centre, in the Reinforcement bank, and the public chapter analysis.
Run from college-predictor/:  python tests/test_jee_pyq_2026.py"""
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
PAPERS = ['P0402S1', 'P0402S2', 'P0404S1', 'P0404S2', 'P0405S1', 'P0405S2', 'P0406S1', 'P0406S2', 'P0408S2']
SUBJ = {'MATH': 'Mathematics', 'PHY': 'Physics', 'CHEM': 'Chemistry'}
codes = {s: {c for c, _n, _p in chs} for s, chs in rf.JEE_TAXONOMY.items()}

# ---- the papers -----------------------------------------------------------------------------------------------------------------------------
idx = {p['y']: p for p in pj.papers()}
ready = pj.valid_papers()
bonus = multi = 0
for y in PAPERS:
    assert idx[y]['ready'] and idx[y].get('tagged') and y in ready, y
    d = json.load(open(os.path.join(DATA, y + '.json'), encoding='utf-8'))
    assert len(d['qs']) == 75 and d['key'] == 'applied' and d.get('tagged')
    assert [q['n'] for q in d['qs']] == list(range(1, 76))
    assert [q['subj'] for q in d['qs']] == ['MATH'] * 25 + ['PHY'] * 25 + ['CHEM'] * 25
    assert sum(q['t'] == 'NAT' for q in d['qs']) == 15
    for q in d['qs']:
        a = q['acc']
        assert a.get('bonus') or a.get('sets') or a.get('ranges'), (y, q['n'])                              # every question has an official answer
        if q['t'] == 'MCQ' and not a.get('bonus'):
            assert set(''.join(a['sets'])) <= set('ABCD'), (y, q['n'], a)
        assert q['cat'] in codes[SUBJ[q['subj']]], (y, q['n'], q['cat'])                                    # the tag belongs to the question's subject
        assert q['lvl'] in (1, 2, 3) and q['chapter'], (y, q['n'])
        bonus += bool(a.get('bonus'))
        multi += len(a.get('sets') or [0]) > 1
assert bonus == 2 and multi == 2, (bonus, multi)                                                           # 4 Apr S1 (dropped), 5 Apr S1 (any integer); 6 Apr S2 and 8 Apr S2 (two accepted options)
d = json.load(open(os.path.join(DATA, 'P0402S1.json'), encoding='utf-8'))
assert d['qs'][0]['acc'] == {'sets': ['C']} or d['qs'][0]['acc']['sets']                                      # the first question of 2 Apr Shift 1 has a key

# ---- the analysis ---------------------------------------------------------------------------------------------------------------------------
a = pj.analysis_2026s2()
assert a and a['n_papers'] == 9 and [s['key'] for s in a['subjects']] == ['MATH', 'PHY', 'CHEM']
for s in a['subjects']:
    assert s['total'] == 225 and sum(c['total'] for c in s['chapters']) == 225
    assert all(len(c['per']) == 9 and sum(c['per']) == c['total'] for c in s['chapters'])
    assert len(s['chapters']) == len(rf.JEE_TAXONOMY[s['name']]) and s['chapters'][0]['total'] >= s['chapters'][-1]['total']
app = create_app()
app.config['WTF_CSRF_ENABLED'] = False
c = app.test_client()
r = c.get('/edupulse-jee/analysis')
t = r.get_data(as_text=True)
assert r.status_code == 200 and 'which chapters carried the marks' in t
assert 'data-how="ja-2026"' in t and 'Coordinate geometry' in t and 'Organic' in t.replace('organic', 'Organic') and t.count('class="ja-t"') == 3 and 'JEE Main 2026 Chapter Analysis' in c.get('/').get_data(as_text=True)
assert 'office hours' not in t.lower()

# ---- Reinforcement bank ---------------------------------------------------------------------------------------------------------------------
with app.app_context():
    db.create_all()
    rf.seed_taxonomy()
    n = rf.seed_pyq()
    assert n >= 675 - bonus - multi, n                                                                     # dropped and two-answer questions are left out
    assert rf.seed_pyq() == 0                                                                               # idempotent
    qs = RfQuestion.query.filter(RfQuestion.source.like('%Official NTA key%')).all()
    assert len(qs) == n and all(q.status == 'approved' and q.exam == 'JEE' for q in qs)
    assert {q.subject for q in qs} == {'Mathematics', 'Physics', 'Chemistry'}
    assert RfQuestionImage.query.filter_by(kind='q').count() == n
    q = RfQuestion.query.filter_by(qid='JEE-P0402S1-001').one()
    assert q.qtype == 'mcq' and json.loads(q.answer_json) in ('A', 'B', 'C', 'D') and 'qimg/JEE-P0402S1-001/q' in q.stem
    nat = RfQuestion.query.filter_by(qid='JEE-P0402S1-021').one()
    assert nat.qtype == 'nat' and json.loads(nat.answer_json)[0][0] == json.loads(nat.answer_json)[0][1]
    assert RfQuestion.query.filter_by(qid='JEE-P0404S1-%03d' % next(q['n'] for q in json.load(open(os.path.join(DATA, 'P0404S1.json'), encoding='utf-8'))['qs'] if q['acc'].get('bonus'))).count() == 0
    chapters = {q.chapter for q in qs}
    assert len(chapters) >= 30, len(chapters)                                                                 # the bank now reaches most chapters of the JEE list
print('jee 2026 pyq checks passed')
