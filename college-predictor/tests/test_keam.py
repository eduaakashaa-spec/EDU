"""KEAM analytics page and data. Run from college-predictor/:  python tests/test_keam.py"""
import json, os, re, sys, tempfile
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
_fd, _db = tempfile.mkstemp(suffix='.db'); os.close(_fd)
os.environ.update(DATABASE_URL='sqlite:///' + _db, SECRET_KEY='test', FLASK_DEBUG='0')
from app import create_app  # noqa: E402
from app.services import keam as K  # noqa: E402
app = create_app(); app.config['TESTING'] = True
c = app.test_client()

d = K.lastranks()
assert [r['id'] for r in d['rounds']] == ['2025-1', '2025-2', '2026-1', '2026-2']
assert len(d['colleges']) >= 140 and len(d['rows']) > 800
C = d['cats']
def lr(code, course, rid, cat='SM'):
    for r in d['rows']:
        if r['c'] == code and r['n'] == course:
            v = r['r'].get(rid)
            return v[C.index(cat)] if v else None
# values checked against the official CEE last-rank PDFs
assert lr('TVE', 'Computer Science and Engineering', '2025-1') == 343
assert lr('TVE', 'Computer Science and Engineering', '2025-1', 'EZ') == 804
assert lr('TVE', 'Computer Science and Engineering', '2026-2') == 584
assert lr('TCR', 'Computer Science and Engineering', '2026-2') == 947
assert lr('MDL', 'Computer Science and Engineering', '2025-1') == 1217
assert lr('KKE', 'Applied Electronics and Instrumentation', '2026-1') == 8302
assert not any('Allotment' in r['n'] or r['n'].isupper() for r in d['rows'])   # no page titles taken as courses
# every college has a district
assert all(K.district(x['n']) for x in d['colleges'])
s = K.summary()
assert len(s['top']) == 20 and s['top'][0]['c'] == 'TVE'
ref = [t['best']['sm']['2026-1'] for t in s['top']]
assert ref == sorted(ref)

h = c.get('/keam-analytics')
t = h.get_data(as_text=True)
assert h.status_code == 200 and 'KEAM 2027 Analytics' in t and 'keam.js' in t and 'window.EA_KEAM' in t
assert 'KEAM Analytics &amp; Predictor' in t   # menu link
j = c.get('/keam-analytics/lastranks.json')
assert j.status_code == 200 and len(json.loads(j.get_data())['rows']) == len(d['rows'])
assert c.get('/static/data/kerala-districts.geojson').status_code == 200
assert not re.search(r'(^|\})\s*(html|body)\s*\{', c.get('/static/css/keam.css').get_data(as_text=True))
print('keam checks passed')
