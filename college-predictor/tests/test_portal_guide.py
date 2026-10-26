"""Portal guide: every Member Home tile and every blueprint is documented, every link resolves, role tabs are enforced.
Run from college-predictor/:  python tests/test_portal_guide.py"""
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
from app.services import member_hub, portal_guide as pg  # noqa: E402

app = create_app()
app.config['TESTING'] = True

# ---- the rule that keeps the guide current ---------------------------------------------------------------------------------------------------
tiles = {t['title'] for c in member_hub.CATEGORIES for t in c['tiles'] if t.get('endpoint')}
missing = sorted(tiles - pg.covered_tiles())
assert not missing, 'Member Home tiles with no entry in app/services/portal_guide.py (add them to an entry\'s `tiles`): %s' % missing
unknown = sorted(set(app.blueprints) - set(pg.COVERED_BLUEPRINTS))
assert not unknown, 'blueprints not listed in portal_guide.COVERED_BLUEPRINTS (document the feature and add the blueprint): %s' % unknown
assert pg.CHANGELOG and pg.CHANGELOG[0][0] == pg.UPDATED, 'add a line at the top of CHANGELOG and set UPDATED to its date whenever the guide changes'

# ---- content sanity -----------------------------------------------------------------------------------------------------------------------------
ids = [e['id'] for e in pg.GUIDE]
assert len(ids) == len(set(ids))
for e in pg.GUIDE:
    assert e['role'] in ('student', 'parent', 'mentor', 'admin', 'all') and e['steps'] and e['title'] and e['summary'] and e['added'] and e['updated'], e['id']
for r in ('student', 'parent', 'mentor', 'admin'):
    assert len(pg.entries_for(r)) >= 2, r
with app.test_request_context():
    from flask import url_for
    for e in pg.GUIDE:
        for label, ep in e.get('where', []):
            url_for(ep)                                                    # raises if the page the guide points to has been renamed or removed

# ---- the page ---------------------------------------------------------------------------------------------------------------------------------
pw = lambda: bcrypt.generate_password_hash('x').decode()
with app.app_context():
    db.create_all()
    for n, e, t in (('Admin', 'a@x.com', 'admin'), ('Mentor', 'm@x.com', 'ea_mentor'), ('Stu', 's@x.com', 'premium'), ('Free', 'f@x.com', 'free')):
        db.session.add(User(name=n, email=e, tier=t, password_hash=pw()))
    db.session.commit()


def login(email):
    c = app.test_client()
    assert c.post('/login', data={'email': email, 'password': 'x'}).status_code == 302
    return c


admin, mentor, student, free = (login(x) for x in ('a@x.com', 'm@x.com', 's@x.com', 'f@x.com'))
assert app.test_client().get('/portal-guide/').status_code in (302, 401)
h = admin.get('/portal-guide/').get_data(as_text=True)
assert 'How to use the portal' in h and 'Admins' in h and 'Mentors' in h and 'Students &amp; members' in h and 'id="a-members"' in h and 'Needs documenting' not in h
assert 'id="m-reinforce-assign"' in admin.get('/portal-guide/?role=mentor').get_data(as_text=True)
hm = mentor.get('/portal-guide/').get_data(as_text=True)
assert 'id="m-desk"' in hm and 'id="a-members"' not in hm and '>Admins<' not in hm                       # mentors do not get the admin section
assert 'id="a-members"' not in mentor.get('/portal-guide/?role=admin').get_data(as_text=True)            # and cannot ask for it
hs = student.get('/portal-guide/').get_data(as_text=True)
assert 'id="s-register"' in hs and 'id="m-desk"' not in hs and '>Mentors<' not in hs and 'id="roles"' in hs
assert 'id="s-free"' in free.get('/portal-guide/').get_data(as_text=True)
nav = admin.get('/admin').get_data(as_text=True)
assert '/portal-guide/' in nav and '/portal-guide/' in mentor.get('/mentor-desk').get_data(as_text=True)
assert '/portal-guide/' in student.get('/member-home').get_data(as_text=True)                              # Member Home tile

print('portal guide checks passed')
