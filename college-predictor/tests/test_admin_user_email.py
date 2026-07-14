"""Self-check: admin-created members get a welcome email with login details,
and the 'Email login details' checkbox controls it. Hermetic sqlite, email stubbed.
Run from college-predictor/:  ../.venv/bin/python tests/test_admin_user_email.py
"""
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

_fd, _db = tempfile.mkstemp(suffix='.db')
os.close(_fd)
os.environ['DATABASE_URL'] = 'sqlite:///' + _db
os.environ['SECRET_KEY'] = 'test'
for k in ('SMTP_HOST', 'SMTP_USER', 'SMTP_PASS'):
    os.environ.pop(k, None)

from app import create_app
from app.extensions import db, bcrypt
from app.models import User
from app.routes import admin_portal as AP

sent = []
AP.send_async = lambda *a, **k: sent.append(a)   # (to, subject, text, html)

app = create_app()
app.config['TESTING'] = True
with app.app_context():
    db.create_all()
    db.session.add(User(name='Admin', email='admin@ea.com', tier='admin',
                        password_hash=bcrypt.generate_password_hash('x').decode()))
    db.session.commit()

ac = app.test_client()
ac.post('/login', data={'email': 'admin@ea.com', 'password': 'x'}, follow_redirects=True)

# 1) create a member WITH the notify box checked -> welcome email queued
sent.clear()
ac.post('/admin/users/add', data={
    'name': 'Priya Sharma', 'email': 'priya@ex.com', 'tier': 'premium',
    'password': 'S3cretPass', 'tier_expires_at': '', 'notify': '1'},
    follow_redirects=True)
with app.app_context():
    assert User.query.filter_by(email='priya@ex.com').first() is not None
assert len(sent) == 1, sent
to, subject, text, html = sent[0]
assert to == 'priya@ex.com', to
assert 'S3cretPass' in text and 'priya@ex.com' in text        # credentials in the email
assert 'S3cretPass' in html and '/login' in text
assert 'EduAakashaa' in subject

# 2) create another member WITHOUT the box (unchecked -> field absent) -> no email
sent.clear()
ac.post('/admin/users/add', data={
    'name': 'Ravi Kumar', 'email': 'ravi@ex.com', 'tier': 'free',
    'password': 'anotherpw', 'tier_expires_at': ''},   # no 'notify'
    follow_redirects=True)
with app.app_context():
    assert User.query.filter_by(email='ravi@ex.com').first() is not None
assert len(sent) == 0, 'unchecked box must not email'

# 3) password stored hashed, not plaintext
with app.app_context():
    u = User.query.filter_by(email='priya@ex.com').first()
    assert u.password_hash != 'S3cretPass' and bcrypt.check_password_hash(u.password_hash, 'S3cretPass')

os.unlink(_db)
print('all admin-user-email checks passed')
