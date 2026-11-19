"""EduPulse App (/app/): role sign-in, student / parent / mentor dashboards, privacy between roles, PWA files.

Hermetic (sqlite). Run from college-predictor/:  python tests/test_edupulse_app.py
"""
import os
import sys
import tempfile
from datetime import date, datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_fd, _db = tempfile.mkstemp(suffix='.db')
os.close(_fd)
os.environ.update(DATABASE_URL='sqlite:///' + _db, SECRET_KEY='test', FLASK_DEBUG='0')

from app import create_app
from app.extensions import db, bcrypt
from app.models import Announcement, User
from app.models_mentorship import MsAction, MsParentLink, MsSession
from app.services import mentorship as ms

app = create_app()
app.config['TESTING'] = True
pw = lambda: bcrypt.generate_password_hash('x').decode()
with app.app_context():
    db.create_all()
    users = dict(
        admin=User(name='Admin One', email='admin@ea.com', tier='admin', password_hash=pw()),
        maya=User(name='Maya Mentor', email='maya@ea.com', tier='ea_mentor', password_hash=pw()),
        other=User(name='Omar Mentor', email='omar@ea.com', tier='ea_mentor', password_hash=pw()),
        guide=User(name='Alum Guide', email='guide@college.edu', tier='mentor', password_hash=pw()),
        ravi=User(name='Ravi Kumar', email='ravi@ex.com', tier='elite', password_hash=pw()),
        priya=User(name='Priya Kumar', email='priya@ex.com', tier='free', password_hash=pw()),
        stranger=User(name='Sam Stranger', email='sam@ex.com', tier='free', password_hash=pw()),
    )
    db.session.add_all(users.values())
    db.session.commit()
    prog = ms.ensure_default_programme()
    e = ms.enrol(users['ravi'], users['maya'], prog, start=date.today())
    db.session.add(MsParentLink(enrolment_id=e.id, parent_id=users['priya'].id))
    s = MsSession(enrolment_id=e.id, title='Branch fit review', status='Planned', position=99,
                  planned_at=datetime.utcnow() + timedelta(days=2), parent_visible=True)
    db.session.add(s)
    db.session.add_all([
        MsAction(enrolment_id=e.id, title='Shortlist ten NITs', owner='student', due_date=date.today() - timedelta(days=1)),
        MsAction(enrolment_id=e.id, title='Private practice log', owner='student', due_date=date.today() + timedelta(days=3), parent_visible=False),
        MsAction(enrolment_id=e.id, title='Collect income certificate', owner='parent', due_date=date.today() + timedelta(days=5)),
    ])
    db.session.add(Announcement(title='Parents webinar on JoSAA', body='Sunday 7 pm.', audience='parents'))
    db.session.add(Announcement(title='Student mock week', body='Three mocks this week.', audience='students'))
    db.session.commit()
    EID = e.id


def client(email=None, role='student', expect=302):
    c = app.test_client()
    if email:
        r = c.post('/app/login', data={'email': email, 'password': 'x', 'role': role})
        assert r.status_code == expect, (email, role, r.status_code)
    return c


# --- public screens and PWA ----------------------------------------------------
anon = client()
w = anon.get('/app/')
assert w.status_code == 200
html = w.get_data(as_text=True)
assert 'Sign in to EduPulse' in html and 'name="role"' in html and 'value="parent"' in html and 'value="mentor"' in html
assert anon.get('/app/home').status_code == 302                       # login required
m = anon.get('/app/manifest.webmanifest')
assert m.status_code == 200 and m.mimetype == 'application/manifest+json' and '"scope": "/app/"' in m.get_data(as_text=True)
sw = anon.get('/app/sw.js')
assert sw.status_code == 200 and sw.headers.get('Service-Worker-Allowed') == '/app/' and 'caches' in sw.get_data(as_text=True)
assert anon.get('/app/offline').status_code == 200
assert 'value="parent" checked' in anon.get('/app/?as=parent').get_data(as_text=True)   # homepage role links preselect the door
home = anon.get('/').get_data(as_text=True)
assert 'id="awApp"' in home and '/app/?as=parent' in home and '/app/?as=mentor' in home   # homepage promotes the app
assert 'href="/app/" class="nav__link">App<' in home                                       # site menu link

# --- sign-in rules ---------------------------------------------------------------
client('ravi@ex.com', 'mentor', expect=403)                            # a student cannot open the mentor door
bad = app.test_client().post('/app/login', data={'email': 'ravi@ex.com', 'password': 'nope', 'role': 'student'})
assert bad.status_code == 401
r = app.test_client().post('/app/login?next=//evil.com', data={'email': 'ravi@ex.com', 'password': 'x', 'role': 'student'})
assert r.status_code == 302 and 'evil.com' not in r.headers['Location']  # no open redirect

# --- student ---------------------------------------------------------------------
st = client('ravi@ex.com', 'student')
h = st.get('/app/home').get_data(as_text=True)
assert 'Hi Ravi' in h and 'Shortlist ten NITs' in h and 'Overdue' in h
assert 'Private practice log' in h                                     # students see all their own actions
assert 'Branch fit review' in h
assert 'Student mock week' in h and 'Parents webinar' not in h
for path in ('/app/plan', '/app/practice', '/app/explore', '/app/me'):
    assert st.get(path).status_code == 200, path
assert 'Branch fit review' in st.get('/app/plan').get_data(as_text=True)
assert 'Mentor &amp; Staff Tools' not in st.get('/app/explore').get_data(as_text=True)

# --- parent ----------------------------------------------------------------------
pa = client('priya@ex.com', 'parent')
h = pa.get('/app/home').get_data(as_text=True)
assert 'Welcome, Priya' in h and 'Ravi' in h
assert 'Collect income certificate' in h and 'Shortlist ten NITs' in h
assert 'Private practice log' not in h                                 # hidden from parents by the mentor
assert 'Parents webinar' in h and 'Student mock week' not in h
assert h.index('Collect income certificate') < h.index('Shortlist ten NITs') or 'Overdue' in h   # parent's own first unless something is overdue

# an unlinked parent sees the empty state, not someone else's child
lone = client('sam@ex.com', 'parent')
h = lone.get('/app/home').get_data(as_text=True)
assert 'Ravi' not in h and 'Shortlist ten NITs' not in h

# --- mentor ----------------------------------------------------------------------
me = client('maya@ea.com', 'mentor')
h = me.get('/app/home').get_data(as_text=True)
assert "Maya's students" in h and 'Ravi' in h and 'overdue actions' in h
assert 'Attention' in h or 'Watch' in h                                # overdue action flags the student
assert 'Mentor &amp; Staff Tools' in me.get('/app/explore').get_data(as_text=True)

ot = client('omar@ea.com', 'mentor')
h = ot.get('/app/home').get_data(as_text=True)
assert 'Ravi' not in h and 'No students are assigned' in h             # other mentors see only their own roster

ad = client('admin@ea.com', 'mentor')
assert 'Ravi' in ad.get('/app/home').get_data(as_text=True)            # admins see every active enrolment

gd = client('guide@college.edu', 'mentor')
assert 'College Guide account' in gd.get('/app/home').get_data(as_text=True)

# --- role switching: an account with two roles ----------------------------------
with app.app_context():
    db.session.add(MsParentLink(enrolment_id=EID, parent_id=User.query.filter_by(email='maya@ea.com').one().id))
    db.session.commit()
me = client('maya@ea.com', 'mentor')
assert 'Switch view' in me.get('/app/me').get_data(as_text=True)
me.post('/app/role', data={'role': 'parent'})
assert 'Welcome, Maya' in me.get('/app/home').get_data(as_text=True)
me.post('/app/role', data={'role': 'student'})                         # not one of her roles: ignored
assert 'Welcome, Maya' in me.get('/app/home').get_data(as_text=True)

# --- sign out --------------------------------------------------------------------
assert st.post('/app/logout').status_code == 302
assert st.get('/app/home').status_code == 302

print('EduPulse App: all checks passed')
