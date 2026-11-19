"""NIRF medical ranking analytics page. Run from college-predictor/:  python tests/test_nirf_medical.py"""
import os, re, sys, tempfile
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
_fd, _db = tempfile.mkstemp(suffix='.db'); os.close(_fd)
os.environ.update(DATABASE_URL='sqlite:///' + _db, SECRET_KEY='test', FLASK_DEBUG='0')
from app import create_app  # noqa: E402
app = create_app(); app.config['TESTING'] = True
c = app.test_client()
h = c.get('/nirf-medical-ranking')
t = h.get_data(as_text=True)
assert h.status_code == 200 and 'NIRF Medical Ranking Analytics' in t and 'nirf_medical.js' in t and 'nirf_medical_data.js' in t
js = c.get('/static/js/nirf_medical_data.js').get_data(as_text=True)
rows = re.findall(r'^\[(\d+),"IR-D', js, re.M)
assert [int(r) for r in rows] == list(range(1, 51)), 'expected ranks 1..50'
scores = [float(x) for x in re.findall(r'^\[\d+,"[^"]+","[^"]+","[^"]*","[^"]*",([\d.]+),', js, re.M)]
assert len(scores) == 50 and scores == sorted(scores, reverse=True) and scores[0] == 91.8 and scores[-1] == 50.91
assert 'AIIMS' in c.get('/medicine').get_data(as_text=True) or 'NIRF Medical Ranking Analytics' in c.get('/medicine').get_data(as_text=True)
assert not re.search(r'(^|\})\s*(html|body)\s*\{', c.get('/static/css/nirf_medical.css').get_data(as_text=True))
print('nirf medical checks passed')
