"""Sign-up bot protection and admin bulk delete.
Run from college-predictor/:  python tests/test_signup_guard.py"""
import os
import re
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
from app.models import Prediction, User  # noqa: E402
from app.models_security import SignupLog  # noqa: E402
from app.services import signup_guard as sg  # noqa: E402

app = create_app()
app.config['TESTING'] = True
pw = lambda: bcrypt.generate_password_hash('x').decode()

# ---- heuristics ---------------------------------------------------------------------------------------------------------------------------------
assert sg.looks_random('FoSkRKDmUEHTyqAjYtSepBJ') and sg.looks_random('wSzYjDMyaIguYwljXfjsTj') and sg.looks_random('LCDaPGbSGClkIljJsH')
assert not any(sg.looks_random(n) for n in ('Aarav Kumar', 'McDonald', 'DeShawn', 'Priya', 'Venkatasubramanian', 'Mary Ann O\'Neil'))
assert sg.name_problem('https://spam.example') and sg.name_problem('a') and not sg.name_problem('Aarav Kumar')
assert sg.email_problem('x@mailinator.com') and not sg.email_problem('x@gmail.com')

with app.app_context():
    db.create_all()
    db.session.add_all([User(name='Admin', email='a@x.com', tier='admin', password_hash=pw()), User(name='Pay', email='pay@x.com', tier='premium', password_hash=pw())])
    db.session.commit()


def token(c):
    html = c.get('/register').get_data(as_text=True)
    m = re.search(r'name="ft" value="([^"]+)"', html)
    assert m and 'name="website"' in html                                   # hidden token and honeypot are on the form
    return m.group(1)


def post(c, ft, **over):
    d = {'name': 'Aarav Kumar', 'email': 'aarav@school.in', 'password': 'secret1', 'confirm': 'secret1', 'ft': ft, 'website': ''}
    d.update(over)
    return c.post('/register', data=d, headers={'X-Forwarded-For': '10.0.0.1'})


def users():
    with app.app_context():
        return sorted(u.email for u in User.query.all())


c = app.test_client()
before = users()
r = post(c, 'garbage')                                                       # forged token
assert users() == before and b'check your details' in r.data
r = post(c, token(c))                                                        # too fast: a real person takes more than a few seconds
assert users() == before
sg.MIN_SECONDS = 0                                                           # the rest of the tests are not about timing
r = post(c, token(c), website='http://spam.example')                         # honeypot filled: silent redirect, nothing created
assert r.status_code == 302 and users() == before
r = post(c, token(c), name='FoSkRKDmUEHTyqAjYtSepBJ')
assert users() == before and b'real full name' in r.data
r = post(c, token(c), email='bot@mailinator.com')
assert users() == before and b'permanent e-mail' in r.data
r = post(c, token(c))                                                        # a normal sign-up works
assert r.status_code == 302 and 'aarav@school.in' in users()
with app.app_context():
    reasons = {x.reason for x in SignupLog.query.all()}
    assert {'honeypot', 'bad_name', 'disposable', 'created', 'too_fast', 'expired'} <= reasons

c2 = app.test_client()
for i in range(2, 4):                                                        # up to 3 accounts per address per hour
    r = post(c2, token(c2), email='kid%d@school.in' % i)
    assert r.status_code == 302, i
    c2 = app.test_client()
r = post(c2, token(c2), email='kid9@school.in')
assert b'Too many sign-up attempts' in r.data and 'kid9@school.in' not in users()

# ---- admin: suspects, selection and bulk delete ---------------------------------------------------------------------------------------------
with app.app_context():
    junk = ['FoSkRKDmUEHTyqAjYtSepBJ', 'wSzYjDMyaIguYwljXfjsTj', 'LCDaPGbSGClkIljJsH', 'aSHBqaxTRleBAuORNpf']
    for i, n in enumerate(junk):
        db.session.add(User(name=n, email='bot%d@gmail.com' % i, tier='free', password_hash=pw()))
    db.session.add(User(name='i.s.m.a.el.s.gu.er.o', email='i.s.m.a.el.s.algu.er.o@gmail.com', tier='free', password_hash=pw()))
    keep = User(name='ZxCvBnMqWeRtYuIoPaSd', email='botwithdata@gmail.com', tier='free', password_hash=pw())        # looks like a bot but owns a prediction
    paid = User(name='QwErTyUiOpAsDfGhJkLz', email='botpaid@gmail.com', tier='premium', password_hash=pw())          # not free: never touched
    db.session.add_all([keep, paid])
    db.session.commit()
    kid, pid = keep.id, paid.id
    db.session.add(Prediction(user_id=kid, predictor='josaa', query_json='{}', results_json='[]'))
    db.session.commit()


def login(email):
    cl = app.test_client()
    assert cl.post('/login', data={'email': email, 'password': 'x'}).status_code == 302
    return cl


admin = login('a@x.com')
student = login('pay@x.com')
page = admin.get('/admin/users').get_data(as_text=True)
assert 'Delete all suspected bots' in page and 'name="ids"' in page and 'suspect</span>' in page
assert 'suspect</span>' in admin.get('/admin/users?suspect=1').get_data(as_text=True)
assert student.post('/admin/users/bulk-delete', data={'mode': 'suspects'}).status_code in (302, 403)               # only admins
with app.app_context():
    n_before = User.query.count()
    sus = [u.id for u in User.query.filter_by(tier='free').all() if sg.suspect_reason(u)]
assert len(sus) >= 6 and student.get('/admin/users').status_code in (302, 403)

with app.app_context():
    one = User.query.filter_by(email='bot0@gmail.com').one().id
r = admin.post('/admin/users/bulk-delete', data={'mode': 'selected', 'ids': [str(one), str(pid)]}, follow_redirects=True)   # a free bot and a premium account
assert b'Deleted 1 account' in r.data and b'not a free account' in r.data
with app.app_context():
    assert User.query.filter_by(email='bot0@gmail.com').first() is None and User.query.get(pid) is not None

r = admin.post('/admin/users/bulk-delete', data={'mode': 'suspects'}, follow_redirects=True)
with app.app_context():
    left = [u.email for u in User.query.all()]
    assert not any(e.startswith('bot') and e.endswith('@gmail.com') and e not in ('botwithdata@gmail.com', 'botpaid@gmail.com') for e in left), left
    assert 'i.s.m.a.el.s.algu.er.o@gmail.com' not in left                                                          # many-dot address also removed
    assert 'botpaid@gmail.com' in left and 'a@x.com' in left and 'aarav@school.in' in left                           # paid, admin and real members stay
    assert 'botwithdata@gmail.com' in left                                                                          # accounts with activity are kept
assert admin.post('/admin/users/bulk-delete', data={'mode': 'selected'}, follow_redirects=True).status_code == 200  # nothing ticked: no error

print('signup guard checks passed')
