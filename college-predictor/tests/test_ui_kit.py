"""UI kit and weekly EduPulse choice: how-panels on the key pages, filter markup, option sources, choose / withdraw / decide and who may do them.
Run from college-predictor/:  python tests/test_ui_kit.py"""
import json
import os
import sys
import tempfile
from datetime import date, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
_fd, _db = tempfile.mkstemp(suffix='.db')
os.close(_fd)
os.environ.update(DATABASE_URL='sqlite:///' + _db, SECRET_KEY='test', FLASK_DEBUG='0')

from app import create_app  # noqa: E402
from app.extensions import bcrypt, db  # noqa: E402
from app.models import User  # noqa: E402
from app.models_mentorship import MsAction, MsParentLink  # noqa: E402
from app.models_pulse import Class12Profile  # noqa: E402
from app.models_reinforce import RfChoice  # noqa: E402
from app.services import mentorship as svc, rf_choice  # noqa: E402

app = create_app()
app.config['WTF_CSRF_ENABLED'] = False
with app.app_context():
    db.create_all()
    pw = bcrypt.generate_password_hash('x').decode()
    for n, e, t in (('Admin', 'a@t.test', 'admin'), ('Mentor', 'm@t.test', 'ea_mentor'), ('Stu', 's@t.test', 'elite'), ('Par', 'p@t.test', 'free'), ('Other', 'o@t.test', 'elite')):
        db.session.add(User(name=n, email=e, tier=t, password_hash=pw))
    db.session.commit()
    U = lambda e: User.query.filter_by(email=e).one()  # noqa: E731
    enr = svc.enrol(U('s@t.test'), U('m@t.test'), svc.ensure_default_programme(), preferred_name='Stu')
    db.session.add(MsParentLink(enrolment_id=enr.id, parent_id=U('p@t.test').id, relation='Mother'))
    db.session.add(MsAction(enrolment_id=enr.id, title='Do the chapter test', owner='student', due_date=date.today() - timedelta(days=1), priority='High', status='Not Started', parent_visible=True))
    db.session.add(Class12Profile(user_id=U('s@t.test').id, stream='pcm', data_json=json.dumps({'ratings': {'P01': 1, 'C02': 2}})))
    from app.models_reinforce import RfStudent
    from app.services import reinforce as rf
    rf.seed_taxonomy()
    db.session.add(RfStudent(user_id=U('s@t.test').id, mentor_id=U('m@t.test').id, exam='JEE', grade='Class 12'))
    db.session.commit()
    from app.services import planner
    planner.generate_plan(U('s@t.test'), 'JEE', 'average', planner.week_start(date.today()), 4, mentor_id=U('m@t.test').id, created_by=U('s@t.test').id)
    db.session.commit()
    EID, SID = enr.id, U('s@t.test').id


def login(email):
    c = app.test_client()
    r = c.post('/login', data={'email': email, 'password': 'x'}, follow_redirects=False)
    assert r.status_code in (302, 303), (email, r.status_code)
    return c


# ---- how panels and filter markup ----------------------------------------------------------------------------------------------------------------
st = login('s@t.test')
with app.test_request_context():
    from flask import url_for
    RF, PL, TR = url_for('reinforce.home'), url_for('planner.plan_view'), url_for('mentorship.action_tracker')
for url, marker in (('/mentorship/e/%d/weekly' % EID, 'data-how="ms-weekly"'), ('/mentorship/e/%d/actions' % EID, 'data-how="ms-actions"'),
                    ('/class12-pcm/dashboard', 'data-how="pd-pcm"'), ('/class12-pcb/dashboard', 'data-how="pd-pcb"'), (RF, 'data-how="rf-home"'),
                    ('/study-planner/', 'data-how="sp-home"'), (PL, 'data-how="sp-plan"')):
    r = st.get(url, follow_redirects=True)
    t = r.get_data(as_text=True)
    assert r.status_code == 200 and marker in t, (url, r.status_code, marker)
    for word in ('Student', 'Parent', 'Mentor', 'Outcome'):
        assert word in t, (url, word)
    low = t.lower()
    assert 'office hours' not in low and 'working hours' not in low, url
t = st.get('/mentorship/e/%d/weekly' % EID).get_data(as_text=True)
assert 'class="fwrap"' in t and 'fchip' in t and 'details class="citem' in t and 'id="edupulse"' in t and 'id="checkin-form"' in t
t = st.get('/class12-pcm/dashboard').get_data(as_text=True)
assert 'id="cCls"' in t and 'id="wFlt"' in t and 'id="pdRf"' in t and '/mentorship/e/%d/weekly#edupulse' % EID in t
t2 = st.get(PL).get_data(as_text=True)
assert 'data-key="day"' in t2 and 'class="sp-day fi' in t2
assert 'css/uikit.css' in t and 'js/uikit.js' in t

# ---- options: sources, not offered when not applicable --------------------------------------------------------------------------------------------
with app.app_context():
    opts = rf_choice.options(User.query.get(SID))
    keys = [o['key'] for o in opts]
    assert len(opts) <= rf_choice.MAX_OPTIONS and len(set(keys)) == len(keys)
    assert any(k.startswith('d:pcm:') for k in keys), keys              # dashboard ratings of 1 and 2 are offered
    assert all(o['state'] == '' for o in opts)

# ---- choose / withdraw / decide and permissions ---------------------------------------------------------------------------------------------------
key = keys[0]
ot = login('o@t.test')
assert ot.post('/mentorship/e/%d/edupulse/choose' % EID, data={'key': key}).status_code in (403, 404)         # not their enrolment
par = login('p@t.test')
assert par.post('/mentorship/e/%d/edupulse/choose' % EID, data={'key': key}).status_code in (403, 404)       # a parent cannot choose
r = st.post('/mentorship/e/%d/edupulse/choose' % EID, data={'key': 'not-an-option'}, follow_redirects=True)
with app.app_context():
    assert RfChoice.query.count() == 0                                                                        # unknown keys are refused
r = st.post('/mentorship/e/%d/edupulse/choose' % EID, data={'key': key}, follow_redirects=True)
assert r.status_code == 200
with app.app_context():
    rows = RfChoice.query.all()
    assert len(rows) == 1 and rows[0].status == 'requested' and rows[0].user_id == SID
    CID = rows[0].id
st.post('/mentorship/e/%d/edupulse/choose' % EID, data={'key': key})                                          # same option again: no duplicate
with app.app_context():
    assert RfChoice.query.count() == 1
for k in keys[1:5]:
    st.post('/mentorship/e/%d/edupulse/choose' % EID, data={'key': k})
with app.app_context():
    assert RfChoice.query.filter_by(user_id=SID).count() <= rf_choice.MAX_PER_WEEK                           # weekly cap
t = par.get('/mentorship/e/%d/weekly' % EID).get_data(as_text=True)
assert 'Add to my week' not in t                                                                              # the parent only sees what was chosen
assert st.post('/mentorship/e/%d/edupulse/%d/decide' % (EID, CID), data={'decision': 'approve'}).status_code in (403, 404)   # a student cannot approve
mt = login('m@t.test')
t = mt.get('/mentorship/e/%d/weekly' % EID).get_data(as_text=True)
assert 'Approve' in t and 'Decline' in t
r = mt.post('/mentorship/e/%d/edupulse/%d/decide' % (EID, CID), data={'decision': 'approve', 'note': 'Good pick'}, follow_redirects=True)
assert r.status_code == 200
with app.app_context():
    c = RfChoice.query.get(CID)
    assert c.status == 'approved' and c.mentor_note == 'Good pick' and c.decided_at
assert mt.post('/mentorship/e/%d/edupulse/%d/decide' % (EID, CID), data={'decision': 'decline'}).status_code in (403, 404)   # already decided
t = st.get('/mentorship/e/%d/weekly' % EID).get_data(as_text=True)
assert 'Open practice' in t

# ---- the staff tracker ----------------------------------------------------------------------------------------------------------------------------
t = mt.get(TR).get_data(as_text=True)
assert 'data-how="ms-tracker"' in t and 'class="rt"' in t and 'data-l="Owner"' in t
print('ui kit ok')
