"""No office working hours (Mon-Fri 9:00-22:00, weekends 9:00-16:00 and the like) appear on any public page, script or PDF.
Every page that can be fetched without arguments is requested, so a template that broke when a block was removed shows up as a server error.
Run from college-predictor/:  python tests/test_no_office_hours.py"""
import glob
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

HOURS = [re.compile(p, re.I) for p in (r'Mon\w*\s*[–-]\s*Fri\w*\s*[:·|]?\s*\d', r'Mon to Fri', r'Sat\w*\s*(&amp;|&#x26;|&|and|-|–)\s*Sun\w*\s*[:·|]?\s*\d', r'9:00\s*[–-]\s*(16|22)', r'(?<![\d-])9-22(?!\d)', r'9am–10pm',
                                       r'Office hours', r'Offices? (&amp;|&#x26;|&) hours', r'Opening hours', r'திங்கள்-வெள்ளி', r'class="k">Hours \(IST\)', r'Locations (&amp;|&) Hours', r'Mentoring hours are')]


def clean(s):
    s = re.sub(r'data:[a-z/+-]+;base64,[A-Za-z0-9+/=]+', '', s)
    return re.sub(r'[A-Za-z0-9+/=]{300,}', '', s)


hits = []
for pat in ('app/templates/**/*.html', 'app/static/js/*.js', 'app/data/pcm12/pages/*.html', 'app/data/gulf/*.html', 'app/services/*.py'):
    for f in glob.glob(os.path.join(ROOT, pat), recursive=True):
        s = clean(open(f, encoding='utf-8', errors='ignore').read())
        for h in HOURS:
            m = h.search(s)
            if m:
                hits.append((os.path.relpath(f, ROOT), s[max(0, m.start() - 30):m.end() + 40].replace('\n', ' ')))
assert not hits, hits[:6]

app = create_app()
c = app.test_client()
bad = []
n = 0
for rule in app.url_map.iter_rules():
    if 'GET' not in rule.methods or rule.arguments or rule.endpoint == 'static':
        continue
    r = c.get(rule.rule)
    n += 1
    if r.status_code >= 500:
        bad.append((rule.rule, r.status_code))
    elif r.status_code == 200 and 'text/html' in (r.mimetype or ''):
        t = clean(r.get_data(as_text=True))
        for h in HOURS:
            if h.search(t):
                bad.append((rule.rule, 'hours text: ' + h.pattern))
assert not bad, bad[:8]
assert n > 100, n
for u in ('/contact', '/career-path', '/tnea-2026'):
    assert c.get(u).status_code in (200, 301, 302), u
page = c.get('/contact').get_data(as_text=True)
assert 'Coimbatore, Tamil Nadu' in page and 'Office Hours' not in page
try:
    os.remove(_db)
except OSError:
    pass
print('no office hours checks passed (%d pages)' % n)
