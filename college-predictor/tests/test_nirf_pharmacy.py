"""NIRF pharmacy ranking analytics page. Run from college-predictor/:  python tests/test_nirf_pharmacy.py"""
import os, re, sys, tempfile
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
_fd, _db = tempfile.mkstemp(suffix='.db'); os.close(_fd)
os.environ.update(DATABASE_URL='sqlite:///' + _db, SECRET_KEY='test', FLASK_DEBUG='0')
from app import create_app  # noqa: E402
app = create_app(); app.config['TESTING'] = True
c = app.test_client()
h = c.get('/nirf-pharmacy-ranking')
t = h.get_data(as_text=True)
assert h.status_code == 200 and 'NIRF Pharmacy Ranking Analytics' in t and 'nirf_pharmacy.js' in t and 'nirf_pharmacy_data.js' in t
js = c.get('/static/js/nirf_pharmacy_data.js').get_data(as_text=True)
rows = re.findall(r'^\[(\d+),"IR-P', js, re.M)
ranks = [int(r) for r in rows]
assert len(ranks) == 100 and ranks == sorted(ranks) and ranks[0] == 1 and ranks[-1] == 100 and ranks.count(83) == 2 and 84 not in ranks, 'expected 100 rows, rank 83 shared'
scores = [float(x) for x in re.findall(r'^\[\d+,"[^"]+","[^"]+","[^"]*","[^"]*",([\d.]+),', js, re.M)]
assert len(scores) == 100 and scores == sorted(scores, reverse=True) and scores[0] == 86.59 and scores[-1] == 41.48
assert 'NIRF Pharmacy Ranking Analytics' in c.get('/medicine').get_data(as_text=True)
assert not re.search(r'(^|\})\s*(html|body)\s*\{', c.get('/static/css/nirf_pharmacy.css').get_data(as_text=True))
print('nirf pharmacy checks passed')
