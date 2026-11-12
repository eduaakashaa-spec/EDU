"""EduPulse-JEE Paper 2 mock centre (2A B.Arch / 2B B.Planning): bank integrity, key, marking (+4/-1, numerical, attempt-any-5, dropped question), reports, access.
Run from college-predictor/:  python tests/test_jee_p2.py"""
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
from app.extensions import bcrypt, db  # noqa: E402
from app.models import User  # noqa: E402
from app.services import jeep2  # noqa: E402

# ---- bank ---------------------------------------------------------------------------------------------------------------------------------
meta = json.load(open(os.path.join(ROOT, 'app', 'data', 'jee_p2', 'papers.json'), encoding='utf-8'))
assert len(meta) >= 4 and {m['paper'] for m in meta.values()} == {'2A', '2B'}
us = jeep2.usable()
assert len(us) >= 340, len(us)
img = os.path.join(ROOT, 'app', 'static', 'img', 'jee_p2')
for q in us:
    assert os.path.exists(os.path.join(img, q['paper_id'], 'q%03d.webp' % q['n'])), q['qid']
    assert q['key'] == 'bonus' or (q['t'] == 'MCQ' and q['key'] in (0, 1, 2, 3)) or (q['t'] == 'NAT' and isinstance(q['key'], float)), q['qid']
assert any(q['key'] == 'bonus' for q in us)                                               # the question NTA dropped in 9 April 2025 Paper 2B
for pid, m in meta.items():
    secs = {s['sec'] for s in m['sections']}
    assert secs == ({'MATH', 'APT'} if m['paper'] == '2A' else {'MATH', 'APT', 'PLAN'}), pid          # the 2A Drawing test is never a question
ts = jeep2.tests()
ids = [t['id'] for t in ts]
assert len(set(ids)) == len(ids) and any(t['kind'] == 'paper' for t in ts) and any(t['kind'] == 'section' for t in ts) and any(t['kind'] == 'mix' for t in ts)
for t in ts:
    assert all(jeep2.by_id()[i]['usable'] for i in t['qids']) and len(set(t['qids'])) == len(t['qids'])
assert jeep2.max_marks(jeep2.test('P-B2401S2')) == 400 and jeep2.max_marks(jeep2.test('P-A2401S2')) == 300       # 10 numerical questions, attempt any 5

# ---- app ----------------------------------------------------------------------------------------------------------------------------------
app = create_app()
app.config['TESTING'] = True
pw = lambda: bcrypt.generate_password_hash('x').decode()
with app.app_context():
    db.create_all()
    db.session.add_all([User(name='Free', email='f@x.com', tier='free', password_hash=pw()), User(name='Prem', email='p@x.com', tier='premium', password_hash=pw())])
    db.session.commit()


def login(em):
    c = app.test_client()
    assert c.post('/login', data={'email': em, 'password': 'x'}).status_code == 302
    return c


anon, free, prem = app.test_client(), login('f@x.com'), login('p@x.com')
assert anon.get('/jee-paper2-mock/').status_code == 302 and free.get('/jee-paper2-mock/').status_code == 403
h = prem.get('/jee-paper2-mock/').get_data(as_text=True)
assert 'EduPulse-JEE Paper 2 Mock Test Centre' in h and 'Whole papers' in h and 'Drawing' in h
t = jeep2.test('P-B2401S2')
page = prem.get('/jee-paper2-mock/test/P-B2401S2').get_data(as_text=True)
assert '"key"' not in page and '.webp' in page and '"t": "NAT"' in page.replace('"t":"NAT"', '"t": "NAT"')


def answers(fn):
    return {'answers': {qid: fn(jeep2.by_id()[qid], k) for k, qid in enumerate(t['qids'])}, 'timed': True, 'seconds': 900}


def perfect(q, k):
    return {'a': q['key'] if q['t'] == 'MCQ' and q['key'] != 'bonus' else (str(int(q['key'])) if q['t'] == 'NAT' and q['key'] != 'bonus' and q['key'] == int(q['key']) else str(q['key'])), 'c': 'H'}


j = prem.post('/jee-paper2-mock/submit/P-B2401S2', json=answers(perfect)).get_json()
assert j['ok'] and j['url'].startswith('/jee-paper2-mock/result/')
from app.models_pulse import PulseJeeP2Result  # noqa: E402
with app.app_context():
    row = PulseJeeP2Result.query.one()
    assert row.score == 400 and row.max_score == 400 and row.wrong == 0, (row.score, row.right, row.wrong)      # attempt-any-5: the other 5 numerical answers are not marked and cost nothing
# a wrong numerical answer costs 1; a blank costs nothing; every answer wrong by one position costs 1
mcq = [qid for qid in t['qids'] if jeep2.by_id()[qid]['t'] == 'MCQ'][:6]
body = {'answers': {qid: {'a': (jeep2.by_id()[qid]['key'] + 1) % 4, 'c': 'H'} for qid in mcq[:3]}, 'timed': True, 'seconds': 60}
body['answers'][mcq[3]] = {'a': jeep2.by_id()[mcq[3]]['key'], 'c': 'M'}
nat = next(qid for qid in t['qids'] if jeep2.by_id()[qid]['t'] == 'NAT')
body['answers'][nat] = {'a': '999999', 'c': 'G'}
j2 = prem.post('/jee-paper2-mock/submit/P-B2401S2', json=body).get_json()
with app.app_context():
    row = db.session.get(PulseJeeP2Result, j2['id'])
    assert (row.right, row.wrong, row.score, row.sure_wrong) == (1, 4, 4 - 4, 3), (row.right, row.wrong, row.score, row.sure_wrong)
rep = prem.get(j2['url'])
txt = rep.get_data(as_text=True)
assert rep.status_code == 200 and 'Key: ' in txt and 'numerical' in txt and free.get(j2['url']).status_code in (404, 403)
# the question NTA dropped is right for everyone, even left blank
tb = jeep2.test('P-B2504S1')
bonus_q = next(qid for qid in tb['qids'] if jeep2.by_id()[qid]['key'] == 'bonus')
j3 = prem.post('/jee-paper2-mock/submit/P-B2504S1', json={'answers': {}, 'timed': False, 'seconds': 5}).get_json()
with app.app_context():
    row = db.session.get(PulseJeeP2Result, j3['id'])
    assert row.score == 4 and row.right == 1 and row.wrong == 0, (row.score, row.right)
assert prem.post('/jee-paper2-mock/submit/NOPE', json=body).status_code == 404 and prem.post('/jee-paper2-mock/submit/P-B2401S2', json={'answers': 'x'}).status_code == 400

# ---- public page and Member Home ---------------------------------------------------------------------------------------------------------
page = anon.get('/jee-main-2027-paper-2-barch-bplanning').get_data(as_text=True)
assert 'id="mock"' in page and 'Join to open the mock centre' in page
assert 'Open the Paper 2 mock centre' in prem.get('/jee-main-2027-paper-2-barch-bplanning').get_data(as_text=True)
assert 'EduPulse-JEE Paper 2 Mock Test Centre' in prem.get('/member-home').get_data(as_text=True)
print('jee paper 2 mock checks passed')
