"""Mentor login: dedicated page, mentors only, role-based landing. Run: python tests/test_mentor_login.py"""
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_fd, _db = tempfile.mkstemp(suffix='.db')
os.close(_fd)
os.environ.update(DATABASE_URL='sqlite:///' + _db, SECRET_KEY='test', FLASK_DEBUG='0')

from app import create_app
from app.extensions import db, bcrypt
from app.models import User

app = create_app()
app.config['TESTING'] = True
pw = lambda: bcrypt.generate_password_hash('x').decode()
with app.app_context():
    db.create_all()
    db.session.add_all([User(name='EA', email='ea@ea.com', tier='ea_mentor', password_hash=pw()),
                        User(name='Alum', email='alum@ea.com', tier='mentor', password_hash=pw()),
                        User(name='Stu', email='stu@ea.com', tier='free', password_hash=pw())])
    db.session.commit()


def login(email, password='x'):
    c = app.test_client()
    return c, c.post('/mentor-login', data={'email': email, 'password': password})


pub = app.test_client()
assert pub.get('/mentor-login').status_code == 200
assert '/mentor-login' in pub.get('/').get_data(as_text=True)          # link on the homepage header
assert '/mentor-login' in pub.get('/login').get_data(as_text=True)

c, r = login('ea@ea.com')
assert r.status_code == 302 and '/mentor-desk' in r.headers['Location']
c, r = login('alum@ea.com')
assert r.status_code == 302 and 'mentor' in r.headers['Location'] and 'login' not in r.headers['Location']

c, r = login('stu@ea.com')                                              # members cannot use it
assert r.status_code == 200 and b'not registered as a mentor' in r.data
assert c.get('/profile', follow_redirects=False).status_code in (302, 401)    # and were not signed in

c, r = login('ea@ea.com', 'wrong')
assert r.status_code == 200 and b'Invalid email or password' in r.data

try:
    os.unlink(_db)
except OSError:
    pass
print('all mentor-login checks passed')
