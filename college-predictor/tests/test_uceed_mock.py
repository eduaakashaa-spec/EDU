"""UCEED Mock Test Centre inside EduPulse-UCEED: members-only serving, results saving, confidence analysis, reports and mentor access.
Run from college-predictor/:  python tests/test_uceed_mock.py"""
import json
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_fd, _db = tempfile.mkstemp(suffix='.db')
os.close(_fd)
os.environ.update(DATABASE_URL='sqlite:///' + _db, SECRET_KEY='test', FLASK_DEBUG='0')

from app import create_app
from app.extensions import bcrypt, db
from app.models import User
from app.models_pulse import PulseMockResult, PulseProfile
from app.services import pulse_mock as pm

app = create_app()
app.config['TESTING'] = True
pw = lambda: bcrypt.generate_password_hash('x').decode()
with app.app_context():
    db.create_all()
    for n, e, t in (('Admin', 'a@x.com', 'admin'), ('Mentor', 'm@x.com', 'ea_mentor'), ('Other Mentor', 'm2@x.com', 'ea_mentor'),
                    ('Stu One', 's1@x.com', 'premium'), ('Stu Two', 's2@x.com', 'premium'), ('Free Kid', 'f@x.com', 'free')):
        db.session.add(User(name=n, email=e, tier=t, password_hash=pw()))
    db.session.commit()
    S1 = User.query.filter_by(email='s1@x.com').one().id


def login(email):
    c = app.test_client()
    assert c.post('/login', data={'email': email, 'password': 'x'}).status_code == 302
    return c


admin, mentor, mentor2, s1, s2, free = (login(x) for x in ('a@x.com', 'm@x.com', 'm2@x.com', 's1@x.com', 's2@x.com', 'f@x.com'))
anon = app.test_client()
BASE = '/edupulse-uceed/mock'

# ---- the bundled papers are all there and well-formed ------------------------------------------------------------------------------
root = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'app', 'data', 'uceed_mock', 'data')
files = sorted(os.listdir(root))
assert files == sorted([f'{y}.json' for y in range(2018, 2027)] + [f'M{i}.json' for i in range(1, 6)]), files
for f in ('2026.json', 'M1.json'):
    d = json.load(open(os.path.join(root, f), encoding='utf-8'))
    assert d['qs'] and d['sections'] and all(q.get('disp') is not None for q in d['qs'])

# ---- members only --------------------------------------------------------------------------------------------------------------------
for u in (f'{BASE}', f'{BASE}/app', f'{BASE}/data/2026.json'):
    r = anon.get(u)
    assert r.status_code in (302, 401, 403), (u, r.status_code)
    r = free.get(u)
    assert r.status_code != 200 or b'UCEED mock' not in r.data, u         # a free account never gets the centre or the papers
assert s1.get(f'{BASE}/data/2026.json').status_code == 200 and s1.get(f'{BASE}/data/M3.json').status_code == 200
assert s1.get(f'{BASE}/data/..%2fapp.html').status_code == 404 and s1.get(f'{BASE}/data/2017.json').status_code == 404 and s1.get(f'{BASE}/data/x.json').status_code == 404
r = s1.get(f'{BASE}/app')
html = r.get_data(as_text=True)
assert r.status_code == 200 and '"memberName": "Stu One"' in html and 'resultsEndpoint' in html and BASE + '/results' in html and '/data/' in html
assert 'Cache-Control' in r.headers and 'no-store' in r.headers['Cache-Control']
page = s1.get(BASE).get_data(as_text=True)
assert 'UCEED Mock Test Centre' in page and '<iframe' in page and 'IIT Bombay material' in page

# ---- saving results ---------------------------------------------------------------------------------------------------------------------
def attempt(paper='2026', mode='mock', score=120.5, conf=None):
    # 12 answered questions: topic OBS and SPA, confidence mix
    qs = {}
    spec = conf or [('right', 'H'), ('right', 'H'), ('wrong', 'H'), ('wrong', 'H'), ('right', 'M'), ('wrong', 'M'), ('right', 'L'), ('right', 'L'), ('right', 'G'), ('wrong', 'G'), ('wrong', 'G'), ('blank', None)]
    for i, (st, cf) in enumerate(spec, 1):
        qs[str(i)] = {'type': 'MCQ', 'topic': 'OBS' if i <= 6 else 'SPA', 'answer': 'A', 'official': 'A', 'status': st, 'marks': 3 if st == 'right' else -1 if st == 'wrong' else 0, 'confidence': cf}
    return {'memberId': 'EA1', 'name': 'x', 'paper': paper, 'paperTitle': 'UCEED ' + paper, 'mode': mode, 'score': score, 'max': 200,
            'sections': [{'type': 'MCQ', 'score': 30, 'max': 84, 'right': 6, 'partial': 0, 'wrong': 5, 'blank': 1}], 'startedAt': '2026-10-24T10:00:00.000Z',
            'finishedAt': '2026-10-24T11:58:00.000Z', 'autoSubmitted': False, 'questions': qs}

assert anon.post(f'{BASE}/results', json=attempt()).status_code in (302, 401, 403)
assert s1.post(f'{BASE}/results', json={'paper': '1999'}).status_code == 400
assert s1.post(f'{BASE}/results', data='nope', content_type='application/json').status_code == 400
r = s1.post(f'{BASE}/results', json=attempt())
assert r.status_code == 200 and r.get_json()['ok']
RID = r.get_json()['id']
with app.app_context():
    row = PulseMockResult.query.get(RID)
    assert row.user_id == S1 and row.right == 6 and row.wrong == 5 and row.rated == 11 and row.sure_wrong == 2 and row.answered == 11
    assert PulseProfile.query.get(S1) is not None and PulseProfile.query.get(S1).frequency == 'off'     # visible to mentors, no unrequested e-mails
    bad = attempt()
    bad['questions']['1']['confidence'] = 'Z'; bad['questions']['2']['topic'] = '<script>'; bad['score'] = 'abc'
    p, err = pm.clean_payload(bad)
    assert err is None and p['questions']['1']['confidence'] is None and p['questions']['2']['topic'] is None and p['score'] == 0

# ---- confidence analysis -------------------------------------------------------------------------------------------------------------------
with app.app_context():
    an = pm.analyse([PulseMockResult.query.get(RID)])
    assert an['conf']['H'] == {'n': 4, 'right': 2, 'wrong': 2, 'pct': 50} and an['conf']['G']['wrong'] == 2 and an['conf']['L']['right'] == 2
    assert an['sure_wrong'] == 2 and an['unsure_right'] == 3 and an['rated'] == 11 and an['enough']
    assert an['topics']['OBS']['sure_wrong'] == 2 and an['topics']['OBS']['pct'] == 50
    assert any('High-confidence answers were right only 50%' in n for n in an['notes'])
    assert any('unsure about were right' in n for n in an['notes'])
    assert an['risky_topics'][0][1] == 'Observation'
    few = pm.analyse([])
    assert not few['enough'] and 'Too few' in few['notes'][0]

# ---- reports and access ---------------------------------------------------------------------------------------------------------------------
rep = s1.get(f'{BASE}/result/{RID}').get_data(as_text=True)
assert 'Confidence vs results' in rep and 'Observation' in rep and 'Sure but wrong' in rep and 'Q3' in rep and 'do not predict' in rep
pdf = s1.get(f'{BASE}/result/{RID}.pdf')
assert pdf.status_code == 200 and pdf.data[:5] == b'%PDF-' and len(pdf.data) > 1500
assert s2.get(f'{BASE}/result/{RID}').status_code == 404 and s2.get(f'{BASE}/result/{RID}.pdf').status_code == 404       # another student
assert anon.get(f'{BASE}/result/{RID}').status_code in (302, 401, 403)
assert admin.get(f'{BASE}/result/{RID}').status_code == 200
assert mentor.get(f'{BASE}/result/{RID}').status_code == 404                                                            # not their student yet
with app.app_context():
    PulseProfile.query.get(S1).mentor_id = User.query.filter_by(email='m@x.com').one().id
    db.session.commit()
assert mentor.get(f'{BASE}/result/{RID}').status_code == 200 and mentor2.get(f'{BASE}/result/{RID}').status_code == 404
ms = mentor.get(f'/edupulse-uceed/mentor/{S1}').get_data(as_text=True)
assert 'UCEED mock tests' in ms and 'UCEED 2026' in ms
assert 'Mocks' in mentor.get('/edupulse-uceed/mentor').get_data(as_text=True)

# second attempt: history, averages and trend
s1.post(f'{BASE}/results', json=attempt('M2', 'practice', 150))
page = s1.get(BASE).get_data(as_text=True)
assert 'UCEED M2' in page and 'My mock history' in page
with app.app_context():
    sm = pm.summary(S1)
    assert sm['attempts'] == 2 and sm['avg_pct'] == round((round(100 * 120.5 / 200) + 75) / 2) and sm['sure_wrong_rate'] == round(100 * 4 / 22)

# member hub tile and EduPulse link
assert 'UCEED Mock Test Centre' in s1.get('/member-home').get_data(as_text=True)
assert 'Open mock tests' in s1.get('/edupulse-uceed/').get_data(as_text=True)
print('UCEED mock centre checks passed')
