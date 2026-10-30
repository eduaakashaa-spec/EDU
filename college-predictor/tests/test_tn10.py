"""EduPulse-TN Class 10: question bank, mock centre and Reinforcement track.
Run from college-predictor/:  python tests/test_tn10.py"""
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
from app.data.tn10 import maths, science  # noqa: E402
from app.extensions import bcrypt, db  # noqa: E402
from app.models import User  # noqa: E402
from app.models_pulse import PulseProfile, PulseTn10Result  # noqa: E402
from app.models_reinforce import RfQuestion, RfTaxonomy  # noqa: E402
from app.services import reinforce as rf, tn10  # noqa: E402

# ---- the bank ---------------------------------------------------------------------------------------------------------------------------------------------
b = tn10.bank()
assert len(b) == len(maths.Q) + len(science.Q) == 310
assert len({q['qid'] for q in b}) == 310
units = tn10.units()
assert len([u for u in units if u.startswith('M')]) == 8 and len([u for u in units if u.startswith('S')]) == 22
for q in b:
    assert len(q['options']) == 4 and len(set(q['options'])) == 4, q['qid']              # four different options
    assert 0 <= q['ans'] < 4 and q['options'][q['ans']], q['qid']
    assert q['stem'].strip() and q['why'].strip() and q['diff'] in (1, 2, 3), q['qid']
    assert '&lt;' not in q['stem'] and '&lt;' not in ''.join(q['options']), q['qid']     # entities are decoded for display
per = {}
for q in b:
    per[q['unit']] = per.get(q['unit'], 0) + 1
assert all(per[u] >= 8 for u in units), {u: per.get(u) for u in units if per.get(u, 0) < 8}
assert [q['ans'] for q in b] == [q['ans'] for q in tn10.bank()]                          # stable
assert len(set(q['ans'] for q in b)) == 4 and max(sum(1 for q in b if q['ans'] == k) for k in range(4)) < 0.4 * len(b)   # the right option is spread over A-D

# ---- mocks ----------------------------------------------------------------------------------------------------------------------------------------------
ms = tn10.mocks()
full = [m for m in ms if m['kind'] == 'full']
assert len(full) == 6 and len([m for m in ms if m['kind'] == 'unit']) == 30
for subj in ('M', 'S'):
    seen = [q for m in full if m['id'].startswith(subj) for q in m['qids']]
    assert len(seen) == len(set(seen))                                                    # no question appears in two full mocks of a subject
    assert {tn10.by_id()[q]['unit'] for q in seen} == {u for u in units if u.startswith(subj)}     # every unit is covered
assert tn10.mock('M-F1')['minutes'] == 60 and len(tn10.mock('M-F1')['qids']) == 40
assert tn10.mock('nope') is None
assert 'ans' not in tn10.paper_for_browser(tn10.mock('M-U1'))[0] and 'why' not in tn10.paper_for_browser(tn10.mock('M-U1'))[0]

app = create_app()
app.config['TESTING'] = True
pw = lambda: bcrypt.generate_password_hash('x').decode()
with app.app_context():
    db.create_all()
    for n, e, t in (('Admin', 'a@x.com', 'admin'), ('Mentor', 'm@x.com', 'ea_mentor'), ('Stu', 's@x.com', 'premium'), ('Other', 'o@x.com', 'premium'), ('Free', 'f@x.com', 'free')):
        db.session.add(User(name=n, email=e, tier=t, password_hash=pw()))
    db.session.commit()
    db.session.add(PulseProfile(user_id=User.query.filter_by(email='s@x.com').one().id, mentor_id=User.query.filter_by(email='m@x.com').one().id, frequency='off'))
    db.session.commit()


def login(em):
    c = app.test_client()
    assert c.post('/login', data={'email': em, 'password': 'x'}).status_code == 302
    return c


admin, mentor, stu, other, free, anon = login('a@x.com'), login('m@x.com'), login('s@x.com'), login('o@x.com'), login('f@x.com'), app.test_client()

# ---- access ----------------------------------------------------------------------------------------------------------------------------------------------
assert anon.get('/edupulse-tn10/').status_code == 302
assert free.get('/edupulse-tn10/').status_code == 403 and free.get('/edupulse-tn10/test/M-F1').status_code == 403
assert free.post('/edupulse-tn10/submit/M-F1', json={'answers': {}}).status_code == 403
home = stu.get('/edupulse-tn10/')
assert home.status_code == 200 and b'Mathematics Full Mock 1' in home.data and b'Unit 22: Environmental Management' in home.data
page = stu.get('/edupulse-tn10/test/M-U1')
assert page.status_code == 200 and b'Relations and Functions' in page.data
for q in tn10.bank():
    if q['unit'] == 'M1':
        assert q['why'].encode() not in page.data                                         # explanations are not in the test page
assert stu.get('/edupulse-tn10/test/X-ZZ').status_code == 404

# ---- taking and marking a test ---------------------------------------------------------------------------------------------------------------------------
m = tn10.mock('M-U3')
ans = {}
for k, qid in enumerate(m['qids']):
    right = tn10.by_id()[qid]['ans']
    ans[qid] = {'a': right if k < 10 else (right + 1) % 4, 'c': 'H' if k < 5 else 'L' if k < 8 else 'G' if k < 10 else 'H', 'sec': 12}
ans[m['qids'][14]] = {'a': None, 'c': 'H', 'sec': 3}                                      # left blank (a stray rating is ignored)
r = stu.post('/edupulse-tn10/submit/M-U3', json={'answers': ans, 'timed': True, 'seconds': 400})
j = r.get_json()
assert r.status_code == 200 and j['ok'] and '/edupulse-tn10/result/' in j['url']
with app.app_context():
    row = PulseTn10Result.query.one()
    assert (row.score, row.total, row.attempted) == (10, 15, 14) and row.rated == 14
    assert row.sure_wrong == 4 and row.lucky == 5, (row.sure_wrong, row.lucky)         # questions 10-13 wrong and rated High; 5-9 right but rated Low or Guess
    rid = row.id
assert stu.post('/edupulse-tn10/submit/M-U3', json={'nope': 1}).status_code == 400
assert stu.post('/edupulse-tn10/submit/M-U3', data='x', content_type='text/plain').status_code == 400

# the report: owner, mentor and admin only
rep = stu.get(j['url'])
assert rep.status_code == 200 and b'Question review' in rep.data and b'10 / 15' in rep.data
assert mentor.get(j['url']).status_code == 200 and admin.get(j['url']).status_code == 200
assert other.get(j['url']).status_code == 404 and anon.get(j['url']).status_code == 302

# ---- EduPulse Reinforcement: exam track TN10 --------------------------------------------------------------------------------------------------------------------
with app.app_context():
    assert tn10.seed_reinforcement() == 310 and tn10.seed_reinforcement() == 0
    assert RfQuestion.query.filter_by(exam='TN10', status='approved').count() == 310
    assert RfTaxonomy.query.filter_by(exam='TN10').count() == 30 and set(rf.subjects_of('TN10')) == {'Mathematics', 'Science'}
    q = RfQuestion.query.filter_by(qid='TN10-M1-001').one()
    assert q.qtype == 'mcq' and q.marks == 1 and q.neg_marks == 0 and q.answer in list('ABCD') and len(q.options) == 4
    assert rf.exam_of('TN10') == 'TN10' and rf.exam_of('x') == 'JEE'
rf_home = mentor.get('/edupulse-reinforce/mentor/bank?exam=TN10')
assert rf_home.status_code == 200 and b'TN10' in rf_home.data

print('tn10 checks passed')
