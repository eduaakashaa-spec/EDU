"""EduPulse-IAT mock centre: bank integrity, shuffling, marking (+4/-1), reports, access. Run from college-predictor/:  python tests/test_iat_mock.py"""
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
from app.services import iat  # noqa: E402

bank = iat.bank()
assert len(bank) >= 55 and all(q['sj'] in ('BIO', 'CHE', 'MAT', 'PHY') for q in bank)
us = iat.usable()
assert len(us) >= 40 and all(len(q['opts']) == 4 and q['stem'] and q['why'] for q in us)
assert all(sorted(q['order']) == [0, 1, 2, 3] and q['order'][q['ans']] == 0 for q in us)       # the printed first option is the right one, wherever it lands
assert len({q['ans'] for q in us}) == 4 and max(sum(1 for q in us if q['ans'] == k) for k in range(4)) < 0.4 * len(us)    # the answer is spread over all four positions
for q in bank:
    assert os.path.exists(os.path.join(ROOT, 'app', 'static', 'img', 'iat', str(q['year']), (q['stem'] or q['full'])[0])), q['qid']
ts = iat.tests()
ids = [t['id'] for t in ts]
assert len(set(ids)) == len(ids) and any(t['kind'] == 'full' for t in ts) and any(t['kind'] == 'year' for t in ts) and any(t['kind'] == 'section' for t in ts)
for t in ts:
    assert all(iat.by_id()[i]['usable'] for i in t['qids']) and len(set(t['qids'])) == len(t['qids']) and t['minutes'] == len(t['qids']) * 3
full = [t for t in ts if t['kind'] == 'full']
seen = [i for t in full for i in t['qids']]
assert len(seen) == len(set(seen)) and all(len(t['qids']) == 60 for t in full)                    # full mocks never repeat a question
for t in full:
    assert {iat.by_id()[i]['sj'] for i in t['qids']} == {'BIO', 'CHE', 'MAT', 'PHY'} and sum(1 for i in t['qids'] if iat.by_id()[i]['sj'] == 'BIO') == 15

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
assert anon.get('/iiser-mock/').status_code == 302 and free.get('/iiser-mock/').status_code == 403
h = prem.get('/iiser-mock/').get_data(as_text=True)
assert prem.get('/iiser-mock/').status_code == 200 and 'EduPulse-IAT Mock Test Centre' in h and 'Solved papers' in h
t = next(x for x in ts if x['kind'] == 'section')
r = prem.get('/iiser-mock/test/' + t['id'])
page = r.get_data(as_text=True)
assert r.status_code == 200 and '"ans"' not in page and 'why' not in page.split('ttData')[1][:20000].lower().replace('whyte', '')
# a perfect attempt, a half-wrong attempt and a blank one are marked +4 / -1 / 0 on the server
qs = [iat.by_id()[i] for i in t['qids']]
body = {'answers': {q['qid']: {'a': q['ans'], 'c': 'H'} for q in qs}, 'timed': True, 'seconds': 600}
j = prem.post('/iiser-mock/submit/' + t['id'], json=body).get_json()
assert j['ok'] and j['url'].startswith('/iiser-mock/result/')
from app.models_pulse import PulseIatResult  # noqa: E402
with app.app_context():
    row = PulseIatResult.query.one()
    assert row.score == 4 * len(qs) and row.right == len(qs) and row.wrong == 0 and row.max_score == 4 * len(qs)
body['answers'] = {q['qid']: {'a': (q['ans'] + 1) % 4 if k < 5 else q['ans'] if k < 8 else None, 'c': 'H'} for k, q in enumerate(qs)}
j2 = prem.post('/iiser-mock/submit/' + t['id'], json=body).get_json()
with app.app_context():
    row = db.session.get(PulseIatResult, j2['id'])
    assert (row.right, row.wrong, row.blank, row.score, row.sure_wrong) == (3, 5, len(qs) - 8, 12 - 5, 5)
rep = prem.get(j2['url'])
assert rep.status_code == 200 and 'Solution:' in rep.get_data(as_text=True) and free.get(j2['url']).status_code in (404, 403)
assert prem.post('/iiser-mock/submit/NOPE', json=body).status_code == 404 and prem.post('/iiser-mock/submit/' + t['id'], json={'answers': 'x'}).status_code == 400
yr = bank[0]['year']
sol = prem.get('/iiser-mock/solutions/%d' % yr)
assert sol.status_code == 200 and sol.get_data(as_text=True).count('class="rv"') == len([q for q in bank if q['year'] == yr]) and free.get('/iiser-mock/solutions/%d' % yr).status_code == 403
assert 'EduPulse-IAT Mock Test Centre' in prem.get('/member-home').get_data(as_text=True)
page = anon.get('/iiser-aptitude-test').get_data(as_text=True)
assert 'id="mock"' in page and 'Join to open the mock centre' in page
print('iat mock checks passed')
