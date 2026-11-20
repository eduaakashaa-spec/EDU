"""NIRF architecture ranking analytics page. Run from college-predictor/:  python tests/test_nirf_arch.py"""
import os, re, sys, tempfile
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
_fd, _db = tempfile.mkstemp(suffix='.db'); os.close(_fd)
os.environ.update(DATABASE_URL='sqlite:///' + _db, SECRET_KEY='test', FLASK_DEBUG='0')
from app import create_app  # noqa: E402
app = create_app(); app.config['TESTING'] = True
c = app.test_client()
h = c.get('/nirf-architecture-ranking')
t = h.get_data(as_text=True)
assert h.status_code == 200 and 'NIRF Architecture Ranking Analytics' in t and 'nirf_arch.js' in t and 'nirf_arch_data.js' in t
js = c.get('/static/js/nirf_arch_data.js').get_data(as_text=True)
rows = re.findall(r'^\[(\d+),"IR-A', js, re.M)
ranks = [int(r) for r in rows]
assert len(ranks) == 40 and ranks == sorted(ranks) and ranks[0] == 1 and ranks[-1] == 40 and True
scores = [float(x) for x in re.findall(r'^\[\d+,"[^"]+","[^"]+","[^"]*","[^"]*",([\d.]+),', js, re.M)]
assert len(scores) == 40 and scores == sorted(scores, reverse=True) and scores[0] == 83.95 and scores[-1] == 47.61
assert 'NIRF Architecture Analytics' in t
assert not re.search(r'(^|\})\s*(html|body)\s*\{', c.get('/static/css/nirf_arch.css').get_data(as_text=True))
print('nirf architecture checks passed')
