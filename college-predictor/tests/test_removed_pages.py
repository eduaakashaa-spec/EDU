"""Pages that were taken off the live portal stay gone and are not linked. Run: python tests/test_removed_pages.py"""
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_fd, _db = tempfile.mkstemp(suffix='.db')
os.close(_fd)
os.environ.update(DATABASE_URL='sqlite:///' + _db, SECRET_KEY='test', FLASK_DEBUG='0')

from app import create_app
from app.extensions import bcrypt, db
from app.models import User

app = create_app()
app.config['TESTING'] = True
with app.app_context():
    db.create_all()
    db.session.add_all([User(name='A', email='a@x.com', tier='admin', password_hash=bcrypt.generate_password_hash('x').decode()),
                        User(name='P', email='p@x.com', tier='premium', password_hash=bcrypt.generate_password_hash('x').decode())])
    db.session.commit()


def login(e):
    c = app.test_client()
    c.post('/login', data={'email': e, 'password': 'x'})
    return c


GONE = ('/expert-portaldasa',)
for who in (app.test_client(), login('p@x.com'), login('a@x.com')):
    for path in GONE:
        assert who.get(path).status_code == 404, path
prem, adm = login('p@x.com'), login('a@x.com')
for page in ('/', '/member-home', '/exam-schedule'):
    body = prem.get(page).get_data(as_text=True)
    assert 'expert-portaldasa' not in body and 'Expert Portal' not in body, page
assert adm.get('/dasa2026-expert-report').status_code == 200 and b'expert-portaldasa' not in adm.get('/dasa2026-expert-report').data
assert 'DASA expert portal' not in prem.get('/member-home').get_data(as_text=True)
try:
    os.unlink(_db)
except OSError:
    pass
print('removed pages checks passed')
