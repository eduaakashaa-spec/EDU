"""NIRF management ranking analytics page. Run from college-predictor/:  python tests/test_nirf_management.py"""
import os, re, sys, tempfile
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
_fd, _db = tempfile.mkstemp(suffix='.db'); os.close(_fd)
os.environ.update(DATABASE_URL='sqlite:///' + _db, SECRET_KEY='test', FLASK_DEBUG='0')
from app import create_app  # noqa: E402
app = create_app(); app.config['TESTING'] = True
c = app.test_client()
h = c.get('/nirf-management-ranking')
t = h.get_data(as_text=True)
assert h.status_code == 200 and 'NIRF Management Ranking Analytics' in t and 'nirf_management.js' in t and 'nirf_management_data.js' in t
js = c.get('/static/js/nirf_management_data.js').get_data(as_text=True)
rows = re.findall(r'^\[(\d+),"IR-M', js, re.M)
ranks = [int(r) for r in rows]
assert len(ranks) == 100 and ranks == sorted(ranks) and ranks[0] == 1 and ranks[-1] == 100 and ranks.count(46) == 2 and ranks.count(57) == 2 and 47 not in ranks and 58 not in ranks, 'expected 100 rows, ranks 46 and 57 shared'
scores = [float(x) for x in re.findall(r'^\[\d+,"[^"]+","[^"]+","[^"]*","[^"]*",([\d.]+),', js, re.M)]
assert len(scores) == 100 and scores == sorted(scores, reverse=True) and scores[0] == 83.29 and scores[-1] == 44.53
assert 'NIRF Management Analytics' in t
assert not re.search(r'(^|\})\s*(html|body)\s*\{', c.get('/static/css/nirf_management.css').get_data(as_text=True))
print('nirf management checks passed')
