"""Top engineering colleges by city and state: data integrity and rendering.
Run from college-predictor/:  python tests/test_eng_cities.py"""
import json
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
from app.data import eng_cities as d  # noqa: E402

ctx = d.context()
cols, cities, states = ctx['colleges'], ctx['cities'], ctx['states']
assert len(cities) >= 20 and len(states) >= 25 and len(cols) >= 150
for g in cities + states:
    assert 1 <= len(g['ids']) <= 10 and all(k in cols for k in g['ids']), g['key']
    pos = [(cols[k]['rank'] or 100 + 25 * (1 + ['Rank 101-150', 'Rank 151 to 200', 'Rank 201 to 300'].index(cols[k]['band']))) for k in g['ids']]
    assert pos == sorted(pos), g['key']
keys = {g['key'] for g in cities}
for want in ('mumbai', 'pune', 'chennai', 'coimbatore', 'tiruchirappalli', 'kozhikode', 'delhi', 'ahmedabad', 'bengaluru', 'hyderabad'):
    assert want in keys, want
# tile for every college, no source links stored, fees are plain numbers
for k, c in cols.items():
    assert os.path.exists(os.path.join(ROOT, 'app', 'static', 'img', 'colleges', k + '.svg')), k
    assert c.get('fee') is None or (isinstance(c['fee'], int) and 10000 <= c['fee'] <= 2000000), (k, c.get('fee'))
    assert not any(x in c for x in ('evidence', 'sources', 'source_urls'))
text = json.dumps(cols).lower()
for bad in ('collegedekho', 'careers360', 'collegedunia', 'shiksha', 'getmyuni', 'aggregat', 'whatsapp'):
    assert bad not in text, bad
iitm = cols['indian-institute-of-technology-madras']
assert iitm['rank'] == 1 and iitm['fee'] == 200000 and iitm['type'] == 'IIT' and not iitm.get('dasa')
nitt = cols['national-institute-of-technology-tiruchirappalli']
assert nitt['rank'] == 9 and nitt['dasa']['seats'] > 100 and 'JoSAA' in nitt['eligibility']
assert 'jaypee-institute-of-information-technology' not in [k for k, c in cols.items() if c.get('dasa')]

app = create_app()
app.config['TESTING'] = True
cl = app.test_client()
r = cl.get('/engineering-colleges-by-city')
assert r.status_code == 200
h = r.get_data(as_text=True)
for t in ('Top engineering colleges', 'dg-alert', 'ecRail', 'window.ENG', 'eng_cities.js', 'How the NRI quota works', 'Eligibility, by kind of college'):
    assert t in h, t
for u in ('/top-engineering-colleges', '/engineering-colleges-by-state', '/engineering-colleges-city'):
    assert cl.get(u).status_code == 301
assert cl.get('/static/js/eng_cities.js').status_code == 200
assert cl.get('/static/img/colleges/indian-institute-of-technology-madras.svg').status_code == 200
print('engineering cities: ok')
