"""Recruitment email template (admin Email templates) and the Join our Team register-interest form it links to.
Run from college-predictor/:  python tests/test_recruit_email.py"""
import json
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
_fd, _db = tempfile.mkstemp(suffix='.db')
os.close(_fd)
os.environ.update(DATABASE_URL='sqlite:///' + _db, SECRET_KEY='test', FLASK_DEBUG='0')

from PIL import Image  # noqa: E402

from app import create_app  # noqa: E402
from app.extensions import bcrypt, db  # noqa: E402
from app.models import PageLead, User  # noqa: E402
from app.services import email_templates as E  # noqa: E402

# ---- the template ------------------------------------------------------------------------------------------------------------------------
tpl = next(t for t in E.EMAIL_TEMPLATES if t['key'] == 'recruit_invite')
assert tpl['category'] == 'Recruitment' and [v['key'] for v in tpl['versions']] == ['both', 'tutor', 'mentor']
for v in tpl['versions']:
    assert {f['key'] for f in v['fields']} >= {'name', 'link'} and v['subject'] and v['text'] and v['html']
    subject, text, html = E.render_email('recruit_invite', {'name': 'Asha', 'link': E.JOIN_LINK, 'subjects': 'Maths and Physics'}, v['key'])
    assert 'Asha' in text and E.JOIN_LINK in text and E.JOIN_LINK.replace('&', '&amp;') in html
    assert 'src="' + E.LOGO_URL + '"' in html                                            # logo in the branded header
    assert '/static/img/email/hiring-' in html and '.jpg' in html and 'alt="' in html     # banner image, absolute URL, with alt text
    assert 'Register your interest' in html and 'ref=email#register' in html
    assert '{name}' not in html and '{link}' not in html and '{subjects}' not in html and '{' not in text.replace('{link}', '')
    for bad in ('guarantee', 'salary of', 'Rs ', '₹'):
        assert bad not in text and bad not in html, bad                                # no invented pay figures
assert 'Maths and Physics' in E.render_email('recruit_invite', {'name': 'A', 'link': E.JOIN_LINK, 'subjects': 'Maths and Physics'}, 'tutor')[2]
for f in ('hiring-both.jpg', 'hiring-tutors.jpg', 'hiring-mentors.jpg'):
    path = os.path.join(ROOT, 'app', 'static', 'img', 'email', f)
    im = Image.open(path)
    assert im.format == 'JPEG' and im.size == (1120, 630) and os.path.getsize(path) < 150_000, f

# ---- the register-interest form ------------------------------------------------------------------------------------------------------------
app = create_app()
with app.app_context():
    db.create_all()
    pw = bcrypt.generate_password_hash('x').decode()
    db.session.add(User(name='Admin', email='a@x.com', tier='admin', password_hash=pw))
    db.session.commit()
c = app.test_client()
page = c.get('/join-our-team').get_data(as_text=True)
assert 'id="register"' in page and 'action="/join-our-team/interest"' in page and 'Register my interest' in page and 'hiring-1.webp' in page
assert 'Thank you. We have your details.' in c.get('/join-our-team?sent=1').get_data(as_text=True)
good = {'name': 'Asha Rao', 'email': 'asha@example.com', 'phone': '+91 98765-43210', 'role': 'Tutor', 'city': 'Chennai', 'qualification': 'MSc Physics', 'experience': '6',
        'focus': 'CBSE Physics, JEE', 'availability': 'evenings', 'linkedin': '', 'message': 'Hello', 'ref': 'email'}
assert c.post('/join-our-team/interest', data={**good, 'email': 'bad'}).status_code == 400
assert c.post('/join-our-team/interest', data={**good, 'phone': 'abc'}).status_code == 400
assert c.post('/join-our-team/interest', data={**good, 'role': ''}).status_code == 400
assert c.post('/join-our-team/interest', data={**good, 'name': ' '}).status_code == 400
r400 = c.post('/join-our-team/interest', data={**good, 'email': 'bad'}).get_data(as_text=True)
assert 'valid email address' in r400 and 'Asha Rao' in r400                                # the form keeps what was typed
with app.app_context():
    assert PageLead.query.filter_by(source='join-team').count() == 0
assert c.post('/join-our-team/interest', data={**good, 'website': 'spam'}).status_code == 302
with app.app_context():
    assert PageLead.query.filter_by(source='join-team').count() == 0                      # honeypot saves nothing
r = c.post('/join-our-team/interest', data=good)
assert r.status_code == 302 and r.headers['Location'].endswith('/join-our-team?sent=1#register')
with app.app_context():
    lead = PageLead.query.filter_by(source='join-team').one()
    assert lead.name == 'Asha Rao' and lead.email == 'asha@example.com' and lead.phone == '+919876543210'
    pl = json.loads(lead.payload_json)
    assert pl['role'] == 'Tutor' and pl['focus'] == 'CBSE Physics, JEE' and pl['ref'] == 'email'

# ---- admin sees both ---------------------------------------------------------------------------------------------------------------------
adm = app.test_client()
assert adm.post('/login', data={'email': 'a@x.com', 'password': 'x'}).status_code == 302
tp = adm.get('/admin/templates')
assert tp.status_code == 200 and b'recruit_invite' in tp.data and b'Invite tutors and mentors to register' in tp.data and b'Recruitment' in tp.data
lp = adm.get('/admin/leads')
assert lp.status_code == 200 and b'join-team' in lp.data and b'Asha Rao' in lp.data
try:
    os.remove(_db)
except OSError:
    pass
print('recruit email checks passed')
