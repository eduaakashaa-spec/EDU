"""JEE self-assessment, gap map against the 2026 chapter Tiers, and the study plan built from it. Run from college-predictor/:  python tests/test_jee_gap.py"""
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
from app.data.jee_topics import SUBJECTS, TOPICS  # noqa: E402
from app.extensions import bcrypt, db  # noqa: E402
from app.models import User  # noqa: E402
from app.models_planner import SpAssessment, SpPlan, SpTask  # noqa: E402
from app.services import jee_gap as G  # noqa: E402
from app.services.reinforce import seed_taxonomy  # noqa: E402

# ---- the data: every chapter of the 2026 analysis belongs to a topic, question weights add up, Tiers read correctly ----
chs, shifts, nq = G._syllabus()
used = {c for t in TOPICS for c in t[3]}
assert len(TOPICS) == 69 and {s: sum(1 for t in TOPICS if t[1] == s) for s in SUBJECTS} == {'Physics': 22, 'Chemistry': 26, 'Mathematics': 21}
assert used == set(chs), (set(chs) - used, used - set(chs))
tp = G.topics()
assert abs(sum(t['q'] for t in tp) - nq) < 0.01 and shifts == 19
by = {t['code']: t for t in tp}
assert by['C17']['tier'] == 1 and by['C04']['tier'] == 0 and by['C13']['tier'] == 0 and by['M21']['tier'] == 0 and by['P01']['tier'] == 1
assert by['P07']['need'] == 3 and by['C04']['need'] == 1

# ---- the maths ----
all4 = {t['code']: 4 for t in tp}
a = G.analyse(all4)
assert a['readiness'] == 100 and a['total_risk'] == 0 and all(x['bucket'] in ('Maintain', 'Park') for x in a['rows'])
all0 = G.analyse({t['code']: 0 for t in tp})
assert all0['readiness'] == 0 and all0['total_risk'] > 100 and all0['rows'][0]['risk'] >= all0['rows'][-1]['risk']
mixed = dict(all4, P07=1, C04=0)                                              # a Tier 2 gap against a no-question topic
am = G.analyse(mixed)
buckets = {x['code']: x['bucket'] for x in am['rows']}
assert buckets['P07'] == 'Fix first' and buckets['C04'] == 'Park'
assert am['rows'][0]['code'] == 'P07' and 'Tier 2' in am['rows'][0]['why'] and 'marks per paper' in am['rows'][0]['why']
assert G.clean({'P01': '3', 'P02': '9', 'ZZ': 1, 'P03': 'x'}) == {'P01': 3}
order = G.plan_order(am)
assert order['Physics'][0][0].startswith('Elasticity') and sum(1 for c in order['Physics'] if c[0].startswith('Elasticity')) == 2 and order['Chemistry'][-1][1] == 'Park'

# ---- the pages and the plan ----
app = create_app()
app.config['TESTING'] = True
pw = lambda: bcrypt.generate_password_hash('x').decode()  # noqa: E731
with app.app_context():
    db.create_all()
    seed_taxonomy()
    for n, em, t in (('Admin', 'a@x.com', 'admin'), ('Mentor', 'm@x.com', 'ea_mentor'), ('Stu Dent', 's@x.com', 'elite'), ('Free User', 'f@x.com', 'free')):
        db.session.add(User(name=n, email=em, tier=t, password_hash=pw()))
    db.session.commit()
    SID = User.query.filter_by(email='s@x.com').one().id


def login(em):
    c = app.test_client()
    assert c.post('/login', data={'email': em, 'password': 'x'}).status_code == 302
    return c


stu, adm, free = login('s@x.com'), login('a@x.com'), login('f@x.com')
assert free.get('/study-planner/self-assessment').status_code in (302, 403)                         # members only
r = stu.get('/study-planner/self-assessment')
assert r.status_code == 200 and b'69 topics' in r.data and r.data.count(b'<select') == 69
assert stu.get('/study-planner/gap-map').status_code == 302                                         # no assessment yet: sent to the form
form = {t['code']: str(mixed[t['code']]) for t in tp}
partial = dict(form)
partial.pop('M21')
r = stu.post('/study-planner/self-assessment', data=partial)
assert r.status_code == 200 and b'1 topic still to rate' in r.data
with app.app_context():
    assert SpAssessment.query.count() == 0
r = stu.post('/study-planner/self-assessment', data=dict(form, note='thermo is weak'), follow_redirects=True)
assert r.status_code == 200 and b'My JEE gap map' in r.data and b'Why this matters' in r.data and b'Elasticity' in r.data and b'Tier 2' in r.data and b'Fix first' in r.data
with app.app_context():
    assert SpAssessment.query.count() == 1 and SpAssessment.query.one().ratings['P07'] == 1
# rebuild needs the tick, then archives the old plan and writes gap notes
assert stu.post('/study-planner/new', data={'exam': 'JEE', 'level': 'average', 'start': '2026-11-23', 'weeks': '6', 'hours': '4'}).status_code == 302
r = stu.post('/study-planner/gap-map/rebuild', data={}, follow_redirects=True)
assert b'Tick the box' in r.data
r = stu.post('/study-planner/gap-map/rebuild', data={'confirm': '1'}, follow_redirects=True)
assert r.status_code == 200
with app.app_context():
    plans = SpPlan.query.filter_by(user_id=SID).order_by(SpPlan.id).all()
    assert len(plans) == 2 and plans[0].status == 'archived' and plans[1].status == 'active' and 'gap map' in plans[1].title
    t = plans[1].tasks.filter(SpTask.subject == 'Physics').order_by(SpTask.day, SpTask.id).first()
    assert t.chapter.startswith('Elasticity') and t.note and 'JEE Main needs 3' in t.note
    chap = [x.chapter for x in plans[1].tasks.filter(SpTask.subject == 'Chemistry').order_by(SpTask.day, SpTask.id).all() if x.chapter]
    assert chap and not chap[0].startswith('States of matter')                                           # a parked topic is not first
# a new plan can use the gap map from the form
r = stu.post('/study-planner/new', data={'exam': 'JEE', 'level': 'top', 'start': '2026-12-07', 'weeks': '4', 'use_gap': '1'})
assert r.status_code == 302
with app.app_context():
    pid = SpPlan.query.filter_by(user_id=SID, status='active').one().id
    assert 'Gap map' in SpTask.query.filter(SpTask.plan_id == pid, SpTask.note.isnot(None)).first().note
# a mentor or admin sees the gap map and can enter ratings for a student
assert adm.get('/study-planner/mentor/student/%d/gap-map' % SID).status_code == 200
assert adm.get('/study-planner/mentor/student/%d/self-assessment' % SID).status_code == 200
page = adm.get('/study-planner/mentor/student/%d' % SID)
assert page.status_code == 200 and b'JEE gap map' in page.data
print('jee gap checks passed')
