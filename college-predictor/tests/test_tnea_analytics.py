"""TNEA analytics page and data. Run from college-predictor/:  python tests/test_tnea_analytics.py"""
import json, os, re, sys, tempfile
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
_fd, _db = tempfile.mkstemp(suffix='.db'); os.close(_fd)
os.environ.update(DATABASE_URL='sqlite:///' + _db, SECRET_KEY='test', FLASK_DEBUG='0')
from app import create_app  # noqa: E402
from app.services import tnea_analytics as T  # noqa: E402
app = create_app(); app.config['TESTING'] = True
c = app.test_client()

d = T.cutoffs()
assert d['rounds'] == [1, 2, 3] and d['comms'] == ['OC', 'BC', 'BCM', 'MBC', 'SC', 'SCA', 'ST']
assert len(d['colleges']) >= 400 and len(d['rows']) > 3000
OC = 0
def row(col, br):
    return next(r for r in d['rows'] if r['c'] == col and r['b'] == br)
# closing marks worked out from the official TNEA 2026 allotment lists
assert T.final(row(1, 'CS'), OC)[0] == 200.0
assert [v[0] if v else None for v in row(1, 'CS')['r']['1']] == [200.0, 199.0, 199.0, 199.0, 197.5, 193.5, None]
assert T.final(row(4, 'CS'), OC)[0] == 197.667
# allotment counts match the official lists (24,674 + 49,984 + 52,915)
s = T.summary()
assert s['seatsRound'] == {1: 24674, 2: 49984, 3: 52915} and s['n_seats'] == 127573
assert len(s['top']) == 20 and s['top'][0]['c'] == 1
ranks = [t['best']['fin'][1] for t in s['top']]
assert ranks == sorted(ranks)
# every college has a district that exists in the map file and a known type
geo = json.load(open(os.path.join(ROOT, 'app', 'static', 'data', 'tamilnadu-districts.geojson'), encoding='utf-8'))
names = {f['properties']['district'] for f in geo['features']}
assert all(r[2] in names for r in s['map']), sorted({r[2] for r in s['map']} - names)
assert all(r[3] in ('U', 'G', 'T1', 'T2', 'T3', 'N') for r in s['map'])
# branch names are cleaned (no glued brackets, no shouting)
assert all(not re.search(r'\w\(', n) and not n.isupper() for n in d['branches'].values())
# mark -> rank curve falls as the mark falls
cv = [r for _, r in d['curve']]
assert cv == sorted(cv) and d['curve'][0][0] == 200.0

h = c.get('/tnea-analytics')
t = h.get_data(as_text=True)
assert h.status_code == 200 and 'TNEA 2027 Analytics' in t and 'tnea_analytics.js' in t and 'window.EA_TNEA' in t and 'tnea-banner.webp' in t
assert 'TNEA Analytics &amp; Predictor' in t   # menu link
j = c.get('/tnea-analytics/cutoffs.json')
assert j.status_code == 200 and len(json.loads(j.get_data())['rows']) == len(d['rows'])
assert c.get('/static/data/tamilnadu-districts.geojson').status_code == 200
assert c.get('/static/img/tnea-banner.webp').status_code == 200
assert not re.search(r'(^|\})\s*(html|body)\s*\{', c.get('/static/css/tnea_analytics.css').get_data(as_text=True))
print('tnea analytics checks passed')
