"""Admin "View as" a student or mentor, and the diagnose page.
Run from college-predictor/:  python tests/test_view_as.py"""
import os
import sys
import tempfile
from datetime import datetime, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
_fd, _db = tempfile.mkstemp(suffix='.db')
os.close(_fd)
os.environ.update(DATABASE_URL='sqlite:///' + _db, SECRET_KEY='test', FLASK_DEBUG='0')

from app import create_app  # noqa: E402
from app.extensions import bcrypt, db  # noqa: E402
from app.models import User  # noqa: E402
from app.models_pulse import PulseTn10Result  # noqa: E402
from app.models_security import AdminImpersonation  # noqa: E402

app = create_app()
app.config['TESTING'] = True
pw = lambda: bcrypt.generate_password_hash('x').decode()
past = datetime.utcnow() - timedelta(days=5)
with app.app_context():
    db.create_all()
    for n, e, t in (('Admin', 'a@x.com', 'admin'), ('Admin Two', 'a2@x.com', 'admin'), ('Prem Student', 'p@x.com', 'premium'), ('Free Student', 'f@x.com', 'free'),
                    ('Elite Student', 'e@x.com', 'elite'), ('EA Mentor', 'm@x.com', 'ea_mentor')):
        db.session.add(User(name=n, email=e, tier=t, password_hash=pw()))
    db.session.add(User(name='Lapsed', email='l@x.com', tier='premium', tier_expires_at=past, password_hash=pw()))
    db.session.commit()
    ID = {u.email: u.id for u in User.query.all()}


def login(em):
    c = app.test_client()
    assert c.post('/login', data={'email': em, 'password': 'x'}).status_code == 302
    return c


admin, prem, anon = login('a@x.com'), login('p@x.com'), app.test_client()
V = lambda em: '/admin/users/%d/view-as' % ID[em]

# only admins can use it
assert anon.get('/admin/view-as').status_code == 302
assert prem.get('/admin/view-as').status_code == 403 and prem.post(V('f@x.com')).status_code == 403
pick = admin.get('/admin/view-as?role=student&q=Student')
assert pick.status_code == 200 and b'Prem Student' in pick.data and b'EA Mentor' not in pick.data
assert b'EA Mentor' in admin.get('/admin/view-as?role=mentor').data

# never another admin, never yourself
assert b'only view as a member' in admin.post(V('a2@x.com'), follow_redirects=True).data
assert b'only view as a member' in admin.post(V('a@x.com'), follow_redirects=True).data

# ---- read-only view as a premium student --------------------------------------------------------------------------------------------------------------------------
r = admin.post(V('p@x.com'), follow_redirects=True)
assert r.status_code == 200 and b'Admin view as' in r.data and b'Prem Student' in r.data and b'read-only' in r.data
assert admin.get('/member-home').status_code == 200 and b'impBar' in admin.get('/member-home').data
assert admin.get('/admin/users').status_code == 403                                      # as the student, the admin area is closed
assert admin.get('/edupulse-tn10/').status_code == 200                                    # but premium tools open, exactly as for the student
home = admin.get('/member-home').get_data(as_text=True)
assert 'Mentor dashboard' not in home and 'Elite Mentorship members' in home            # a Premium student sees the mentorship tile locked
w = admin.post('/edupulse-tn10/submit/M-U1', json={'answers': {}})
assert w.status_code == 403 and 'Read-only' in w.get_json()['error']                      # changes are refused
assert admin.post('/edupulse-tn10/submit/M-U1', data={'x': 1}).status_code == 403
assert b'Nothing was changed' in admin.post('/edupulse-tn10/submit/M-U1', data={'x': 1}).data
assert admin.post(V('f@x.com')).status_code in (302, 403)                                  # no nesting
with app.app_context():
    assert PulseTn10Result.query.count() == 0

# stop: back to the admin account
back = admin.post('/impersonate/stop', follow_redirects=True)
assert back.status_code == 200 and b'Back to your admin account' in back.data and b'impBar' not in back.data
assert admin.get('/admin/users').status_code == 200
with app.app_context():
    log = AdminImpersonation.query.one()
    assert log.admin_id == ID['a@x.com'] and log.target_id == ID['p@x.com'] and log.readonly and log.ended_at is not None

# ---- changes allowed ------------------------------------------------------------------------------------------------------------------------------------------------
admin.post(V('p@x.com'), data={'allow_changes': '1'})
ok = admin.post('/edupulse-tn10/submit/M-U1', json={'answers': {}, 'timed': False, 'seconds': 5})
assert ok.status_code == 200 and ok.get_json()['ok']
with app.app_context():
    assert PulseTn10Result.query.one().user_id == ID['p@x.com']                           # saved against the student, not the admin
assert admin.post('/login', data={'email': 'a2@x.com', 'password': 'x'}).status_code == 403   # sign-in and password changes stay blocked
admin.post('/impersonate/stop')
assert admin.get('/admin/users').status_code == 200

# ---- as a mentor, a free member, a lapsed member ---------------------------------------------------------------------------------------------------------------
admin.post(V('m@x.com'))
assert b'Mentor dashboard' in admin.get('/member-home').data
assert admin.get('/mentorship/mentor').status_code in (200, 302)
admin.post('/impersonate/stop')
admin.post(V('f@x.com'))
assert admin.get('/edupulse-tn10/').status_code == 403                                    # a free member is locked out, as the student would see
admin.post('/impersonate/stop')

# stopping when not viewing is harmless; signing out while viewing clears the session
assert admin.post('/impersonate/stop').status_code == 302
admin.post(V('f@x.com'))
admin.get('/logout')
assert admin.get('/member-home').status_code in (200, 302)
assert b'impBar' not in admin.get('/').data

# ---- diagnose ------------------------------------------------------------------------------------------------------------------------------------------------------
admin = login('a@x.com')
d = admin.get('/admin/users/%d/diagnose' % ID['f@x.com'])
assert d.status_code == 200 and b'Locked: needs Premium (plan is free)' in d.data and b'Team tool: hidden' in d.data
d = admin.get('/admin/users/%d/diagnose' % ID['e@x.com']).get_data(as_text=True)
assert 'Open: Elite plan' in d and 'Locked: needs Elite' not in d
d = admin.get('/admin/users/%d/diagnose' % ID['l@x.com']).get_data(as_text=True)
assert 'expired on' in d and 'Premium access: <b class="dg-no">no</b>' in d
d = admin.get('/admin/users/%d/diagnose' % ID['m@x.com']).get_data(as_text=True)
assert 'Open: team account' in d
assert prem.get('/admin/users/%d/diagnose' % ID['f@x.com']).status_code == 403
assert admin.get('/admin/users').status_code == 200 and b'View as' in admin.get('/admin/users').data

print('view-as checks passed')
