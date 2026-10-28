"""JEE Main 2026 syllabus map and formula sheet (members page).
Run from college-predictor/:  python tests/test_jee_syllabus_map.py"""
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

from app import create_app  # noqa: E402
from app.data.jee_formulas import FORMULAS  # noqa: E402
from app.extensions import bcrypt, db  # noqa: E402
from app.models import User  # noqa: E402

app = create_app()
app.config['TESTING'] = True
pw = lambda: bcrypt.generate_password_hash('x').decode()
with app.app_context():
    db.create_all()
    db.session.add_all([User(name='Stu', email='s@x.com', tier='premium', password_hash=pw()), User(name='Free', email='f@x.com', tier='free', password_hash=pw())])
    db.session.commit()


def login(email):
    c = app.test_client()
    assert c.post('/login', data={'email': email, 'password': 'x'}).status_code == 302
    return c


URL = '/jee-main-2026-syllabus-map'
# every formula chapter exists in the data, and no formula is blank or has unbalanced braces
data = json.load(open(os.path.join(ROOT, 'app', 'data', 'jee_syllabus_2026.json'), encoding='utf-8'))
names = {c['ch'] for c in data['chs']}
assert len(names) == 92 and data['stats']['NQ'] == 1424
assert not [k for k in FORMULAS if k not in names], [k for k in FORMULAS if k not in names]
for ch, rows in FORMULAS.items():
    assert rows, ch
    for label, tex in rows:
        assert label and tex.strip(), ch
        assert tex.count('{') == tex.count('}'), (ch, label)
        assert tex.count('\\begin') == tex.count('\\end'), (ch, label)
        assert '\x08' not in tex and '\x07' not in tex and '\x0c' not in tex, (ch, label)          # a mangled backslash escape

# access: members only
assert app.test_client().get(URL).status_code in (302, 401, 403)
free = login('f@x.com').get(URL)
assert b'92 chapters' not in free.data
page = login('s@x.com').get(URL)
assert page.status_code == 200
h = page.get_data(as_text=True)
assert h.count('<details class="ch"') == 92
assert '1,424' in h and 'katex.min.js' in h and 'auto-render' in h
assert 'Sequences &amp; Series' in h and '\\dfrac{a}{1-r}' in h and '\\oint' in h
assert 'Join Premium' not in h or 'Premium access is active' not in h

print('jee syllabus map checks passed')
