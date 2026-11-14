"""B.Planning Planner 2027 page (public + members, full access for both).
Run from college-predictor/:  python tests/test_bplanning_planner.py"""
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
from app.models import User  # noqa: E402

app = create_app()
app.config['TESTING'] = True
pw = lambda: bcrypt.generate_password_hash('x').decode()
with app.app_context():
    db.create_all()
    db.session.add_all([User(name='Free', email='f@x.com', tier='free', password_hash=pw()),
                        User(name='Prem', email='p@x.com', tier='premium', password_hash=pw())])
    db.session.commit()

URL = '/bplanning-planner-2027'
c = app.test_client()

# public: full page, nothing gated, join call to action
r = c.get(URL)
h = r.get_data(as_text=True)
assert r.status_code == 200
for sec in ('id="paper"', 'id="map"', 'id="check"', 'id="goal"', 'id="plan"', 'id="tips"', 'id="faq"'):
    assert sec in h, sec
assert 'Join Premium Membership' in h and 'Join the Members Group' in h
assert 'Premium access is active' not in h and 'premium_locked' not in h
assert 'data:image' not in h, 'no inline base64 in the page'
assert 'css/bplanning_planner.css' in h and 'js/bplanning_planner.js' in h and 'data-no-rail' in h

# aliases redirect
for a in ('/bplanning-planner', '/jee-paper-2b-planner'):
    rr = c.get(a)
    assert rr.status_code == 301 and rr.headers['Location'].endswith(URL), a

# a free member sees the same page with the join prompt, a premium member sees their status and the mock centre
def login(email):
    cl = app.test_client()
    with app.app_context():
        uid = User.query.filter_by(email=email).first().id
    with cl.session_transaction() as s:
        s['_user_id'] = str(uid)
        s['_fresh'] = True
    return cl

free = login('f@x.com').get(URL)
assert free.status_code == 200 and 'id="goal"' in free.get_data(as_text=True)
prem = login('p@x.com').get(URL)
ph = prem.get_data(as_text=True)
assert prem.status_code == 200 and 'Premium access is active' in ph and 'Open the Paper 2 mock centre' in ph and 'id="goal"' in ph

# assets
css = c.get('/static/css/bplanning_planner.css').get_data(as_text=True)
assert '.bpl{' in css and not re.search(r'(^|\})\s*(html|body)\s*\{', css), 'rules must be scoped under .bpl'
js = c.get('/static/js/bplanning_planner.js').get_data(as_text=True)
assert "querySelector('.bpl')" in js and 'eduaak-planner-' in js

# discoverable: menu and the Paper 2 guide link to it
assert 'B.Planning Planner (Paper 2B)' in h
assert URL in c.get('/jee-main-2027-paper-2-barch-bplanning').get_data(as_text=True)
print('bplanning planner checks passed')
