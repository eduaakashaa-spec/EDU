"""Elite role, mentorship portal access, and per-person tool access (allow / block).
Run from college-predictor/:  python tests/test_tool_access.py"""
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
from app.models_membership import UserToolAccess  # noqa: E402
from app.services import member_hub as mh, mentorship as svc, tool_access  # noqa: E402

app = create_app()
app.config['TESTING'] = True
pw = lambda: bcrypt.generate_password_hash('x').decode()
past = datetime.utcnow() - timedelta(days=3)
with app.app_context():
    db.create_all()
    for n, e, t in (('Admin', 'a@x.com', 'admin'), ('EA', 'ea@x.com', 'ea_mentor'), ('Elite', 'el@x.com', 'elite'), ('Prem', 'pr@x.com', 'premium'),
                    ('Prem2', 'pr2@x.com', 'premium'), ('Free', 'fr@x.com', 'free'), ('Guide', 'g@x.com', 'mentor')):
        db.session.add(User(name=n, email=e, tier=t, password_hash=pw()))
    db.session.add(User(name='OldElite', email='old@x.com', tier='elite', tier_expires_at=past, password_hash=pw()))
    db.session.commit()
    svc.ensure_default_programme()
    prog = svc.ensure_default_programme()
    U = lambda e: User.query.filter_by(email=e).one()
    E = {k: svc.enrol(U(e), U('ea@x.com'), prog).id for k, e in (('el', 'el@x.com'), ('pr', 'pr@x.com'), ('pr2', 'pr2@x.com'), ('old', 'old@x.com'))}
    db.session.commit()
    uid = {e: U(e).id for e in ('el@x.com', 'pr@x.com', 'pr2@x.com', 'fr@x.com', 'ea@x.com', 'g@x.com', 'a@x.com')}


def login(email):
    c = app.test_client()
    assert c.post('/login', data={'email': email, 'password': 'x'}).status_code == 302
    return c


admin, ea, el, pr, pr2, fr, guide, old = (login(e) for e in ('a@x.com', 'ea@x.com', 'el@x.com', 'pr@x.com', 'pr2@x.com', 'fr@x.com', 'g@x.com', 'old@x.com'))

# --- the role -------------------------------------------------------------------------------------------------------------------------------------------------
with app.app_context():
    el_u, pr_u, old_u = U('el@x.com'), U('pr@x.com'), U('old@x.com')
    assert el_u.is_premium and el_u.is_elite and not el_u.is_admin
    assert pr_u.is_premium and not pr_u.is_elite                          # premium never gets the mentorship portal by itself
    assert not old_u.is_premium and not old_u.is_elite                    # an expired Elite membership closes both
    assert U('ea@x.com').is_elite and U('a@x.com').is_elite and not U('fr@x.com').is_elite

# --- mentorship portal: Elite yes, Premium no ----------------------------------------------------------------------------------------------------------
assert el.get('/mentorship/e/%d/home' % E['el']).status_code == 200
assert el.get('/mentorship/').status_code == 302
r = pr.get('/mentorship/e/%d/home' % E['pr'])
assert r.status_code == 403 and b'Elite' in r.data
assert pr.get('/mentorship/').status_code == 403
assert pr.post('/mentorship/e/%d/sessions/add' % E['pr'], data={'title': 'x'}).status_code == 403
assert old.get('/mentorship/e/%d/home' % E['old']).status_code == 403
assert ea.get('/mentorship/e/%d/home' % E['pr']).status_code == 200      # staff still see every enrolment
assert admin.get('/mentorship/e/%d/home' % E['pr']).status_code == 200

# --- member home: the tile follows the role ------------------------------------------------------------------------------------------------------------
with app.test_request_context():
    def tile(user, title):
        for c in mh.build(user):
            for t in c['tiles']:
                if t['title'] == title:
                    return t
    with app.app_context():
        assert tile(U('pr@x.com'), 'My Mentorship')['locked'] is True
        assert tile(U('el@x.com'), 'My Mentorship')['locked'] is False
        assert tile(U('pr@x.com'), 'Smart Study Planner')['locked'] is False

# --- admin: Tool access page -------------------------------------------------------------------------------------------------------------------------
assert pr.get('/admin/users/%d/access' % uid['pr@x.com']).status_code == 403
page = admin.get('/admin/users/%d/access' % uid['pr@x.com'])
assert page.status_code == 200 and b'My Mentorship' in page.data and b'JEE Main syllabus map' in page.data and b'Follow plan' in page.data
assert 'my-mentorship' in tool_access.keys() and len(tool_access.tools()) >= 20


def setmodes(user_email, **modes):
    data = {'m_' + k.replace('_', '-'): v for k, v in modes.items()}
    return admin.post('/admin/users/%d/access' % uid[user_email], data=data, follow_redirects=True)


JEE = '/jee-main-2026-syllabus-map'
# allow: a premium member gets the mentorship portal, a free member gets a premium tool
assert b'1 custom setting' in setmodes('pr2@x.com', my_mentorship='allow').data
assert pr2.get('/mentorship/e/%d/home' % E['pr2']).status_code == 200
assert fr.get(JEE).status_code == 403
setmodes('fr@x.com', jee_main_syllabus_map_formulas='allow')
assert fr.get(JEE).status_code == 200
# block: a premium member loses one tool, keeps the rest; an elite member can be shut out of the portal
setmodes('pr@x.com', jee_main_syllabus_map_formulas='deny')
r = pr.get(JEE)
assert r.status_code == 403 and b'not available' in r.data
assert pr.get('/study-planner/').status_code in (200, 302)
setmodes('el@x.com', my_mentorship='deny')
assert el.get('/mentorship/e/%d/home' % E['el']).status_code == 403
assert el.get(JEE).status_code == 200
with app.test_request_context():
    with app.app_context():
        assert tile(U('pr@x.com'), 'JEE Main syllabus map & formulas')['locked'] is True
        assert tile(U('fr@x.com'), 'JEE Main syllabus map & formulas')['locked'] is False
# mentors: a team tool can be blocked for an EA mentor, an alumni guide can be given a premium tool; allow never opens a team-only tool
assert ea.get('/mentorship/actions').status_code == 200
setmodes('ea@x.com', action_tracker='deny')
assert ea.get('/mentorship/actions').status_code == 403
assert guide.get(JEE).status_code == 403
setmodes('g@x.com', jee_main_syllabus_map_formulas='allow', action_tracker='allow')
assert guide.get(JEE).status_code == 200
assert guide.get('/mentorship/actions').status_code == 403
with app.app_context():
    assert UserToolAccess.query.filter_by(user_id=uid['g@x.com']).count() == 1             # the team-tool allow was not stored
# admins are never restricted; reset clears everything
assert b'nothing to customise' in admin.post('/admin/users/%d/access' % uid['a@x.com'], data={'m_my-mentorship': 'deny'}, follow_redirects=True).data
assert b'follows the plan' in admin.post('/admin/users/%d/access' % uid['pr@x.com'], data={'reset': '1'}, follow_redirects=True).data
assert pr.get(JEE).status_code == 200
with app.app_context():
    assert UserToolAccess.query.filter_by(user_id=uid['pr@x.com']).count() == 0

# --- payment grants the right tier -----------------------------------------------------------------------------------------------------------------------
from app.models_membership import ELITE_TIERS, PORTAL_ACCESS_TIERS  # noqa: E402
assert 'Elite Mentorship' in ELITE_TIERS and ELITE_TIERS <= PORTAL_ACCESS_TIERS

# --- the users screen offers the role and shows the custom count --------------------------------------------------------------------------------------
page = admin.get('/admin/users')
assert page.status_code == 200 and b'value="elite"' in page.data and b'Tool access' in page.data and b'custom' in page.data
assert admin.get('/admin/users?tier=elite').status_code == 200
assert admin.post('/admin/users/%d/update' % uid['fr@x.com'], data={'tier': 'elite'}, follow_redirects=True).status_code == 200
with app.app_context():
    assert U('fr@x.com').tier == 'elite'

print('tool access checks passed')
