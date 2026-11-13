"""Google Analytics 4 tag: on public pages in production, off in debug/tests, for admins/staff and when switched off. Run from college-predictor/:  python tests/test_analytics.py"""
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
_fd, _db = tempfile.mkstemp(suffix='.db')
os.close(_fd)
os.environ.update(DATABASE_URL='sqlite:///' + _db, SECRET_KEY='test', FLASK_DEBUG='0')

from app import create_app  # noqa: E402
from app.extensions import bcrypt, db  # noqa: E402
from app.models import User  # noqa: E402

app = create_app()
with app.app_context():
    db.create_all()
    pw = bcrypt.generate_password_hash('x').decode()
    db.session.add_all([User(name='Adm', email='a@x.com', tier='admin', password_hash=pw), User(name='Free', email='f@x.com', tier='free', password_hash=pw)])
    db.session.commit()


def page(testing, email=None, path='/', env=None):
    app.testing = testing
    if env is None:
        os.environ.pop('GA_MEASUREMENT_ID', None)
    else:
        os.environ['GA_MEASUREMENT_ID'] = env
    c = app.test_client()
    if email:
        assert c.post('/login', data={'email': email, 'password': 'x'}).status_code == 302
    return c.get(path).get_data(as_text=True)


TAG = 'googletagmanager.com/gtag/js?id=G-L5HRKWL888'
assert TAG not in page(True)                                             # tests and debug runs never count
live = page(False)
assert TAG in live and "gtag('config','G-L5HRKWL888'" in live and 'allow_google_signals:false' in live and live.count('googletagmanager.com/gtag/js') == 1
assert TAG in page(False, 'f@x.com')                                     # members are counted
assert TAG not in page(False, 'a@x.com')                                 # admins and staff are not
assert 'googletagmanager.com/gtag/js' not in page(False, env='')         # switched off
assert 'id=G-TESTID123' in page(False, env='G-TESTID123')                # overridable
print('analytics checks passed')
