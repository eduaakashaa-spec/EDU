"""MHT CET analytics page and data. Run from college-predictor/:  python tests/test_mhtcet.py"""
import json, os, re, sys, tempfile
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
_fd, _db = tempfile.mkstemp(suffix='.db'); os.close(_fd)
os.environ.update(DATABASE_URL='sqlite:///' + _db, SECRET_KEY='test', FLASK_DEBUG='0')
from app import create_app  # noqa: E402
from app.services import mhtcet as M  # noqa: E402
app = create_app(); app.config['TESTING'] = True
c = app.test_client()

d = M.cutoffs()
assert d['years'] == [2023, 2024, 2025, 2026] and len(d['inst']) > 380
cats = d['cats']
I = {i['c']: i for i in d['inst']}
def cut(code, name, y, cat='GOPEN', lv='S'):
    for b in I[code]['br']:
        if b['n'] == name:
            for ci, p in b['y'].get(str(y), {}).get(lv, []):
                if cats[ci] == cat:
                    return p / 1e4
# values checked against the official CAP Round I PDFs
assert abs(cut('03012', 'Computer Engineering', 2025) - 99.9522882) < 1e-3          # VJTI
assert abs(cut('16006', 'Computer Science and Engineering', 2024) - 99.9666110) < 1e-3  # COEP (code changed from 06006)
assert abs(cut('16006', 'Civil Engineering', 2023) - 98.1917154) < 1e-3              # COEP 2023 merged under the new code
assert abs(cut('06007', 'Computer Science and Engineering', 2025, 'GOBC') - 99.3868490) < 1e-3  # Walchand OBC
assert abs(cut('06271', 'Computer Engineering', 2023, 'GOPEN', 'H') - 99.6779262) < 1e-3       # PICT home university 2023
assert abs(cut('03185', 'Computer Engineering', 2023, 'TFWS') - 98.5247194) < 1e-3   # VESIT (minority header with MI)
assert abs(cut('01002', 'Civil Engineering', 2026) - 91.7858261) < 1e-3       # 2026 list (official PDF)
assert abs(cut('01002', 'Civil Engineering', 2026, 'GSC') - 85.6921506) < 1e-3
# rank curve is monotonic
for y, t in d['curve'].items():
    ranks = [r for _p, r in t]
    assert ranks == sorted(ranks), y
s = M.summary()
assert len(s['top']) == 20 and s['top'][0]['c'] == '03012'
cuts = [t['best']['cut'][str(s['years'][-1])] for t in s['top']]
assert cuts == sorted(cuts, reverse=True)
assert any(t['c'] == '16006' and t['nirf'] == '90' for t in s['top'])

# official websites: one per institute code, http(s) only, none listed as missing, and the page receives them
from app.data import mhtcet as MD  # noqa: E402
icodes = {i['c'] for i in d['inst']}
assert len(MD.SITES) >= 300 and set(MD.SITES) <= icodes
assert all(re.match(r'^https?://[^\s"<>]+$', u) for u in MD.SITES.values())
assert set(MD.SITES_MISSING) <= icodes and not (set(MD.SITES_MISSING) & set(MD.SITES))
assert len(MD.SITES) + len(MD.SITES_MISSING) == len(icodes)
assert M.payload()['sites'] == MD.SITES

h = c.get('/mht-cet-analytics')
t = h.get_data(as_text=True)
assert h.status_code == 200 and 'MHT CET 2027 Analytics' in t and 'mhtcet.js' in t and 'window.EA_MHT' in t
assert 'MHT CET Analytics &amp; Predictor' in t   # menu link
j = c.get('/mht-cet-analytics/cutoffs.json')
assert j.status_code == 200 and j.mimetype == 'application/json' and len(json.loads(j.get_data())['inst']) == len(d['inst'])
assert not re.search(r'(^|\})\s*(html|body)\s*\{', c.get('/static/css/mhtcet.css').get_data(as_text=True))
print('mhtcet checks passed')
