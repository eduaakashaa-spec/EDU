"""NEET 2023-2025 trends page and its data. Run from college-predictor/:  python tests/test_neet_trends.py"""
import json, os, re, sys, tempfile
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT); sys.path.insert(0, os.path.join(ROOT, 'tools', 'neet_trends'))
_fd, _db = tempfile.mkstemp(suffix='.db'); os.close(_fd)
os.environ.update(DATABASE_URL='sqlite:///' + _db, SECRET_KEY='test', FLASK_DEBUG='0')
import data as d
for y in d.YEARS:  # figures must add up
    reg, app_, ab, q = d.HEADLINE[y]
    assert reg >= app_ and app_ >= q and abs(app_ + ab - reg) <= 140, y
    assert sum(v[2] for v in d.CATEGORY[y].values()) == q, ('category', y)
    assert sum(v[2] for v in d.GENDER[y].values()) == q, ('gender', y)
    assert sum(v[0] for v in d.CATEGORY[y].values()) == reg, ('category reg', y)
assert sum(n for _, n in d.BANDS_2025) <= d.CUTOFF['UR / EWS'][1][2025][2]
tot = [sum(v[i] for v in d.STATE_SEATS.values()) for i in range(3)]
for i, y in enumerate(d.YEARS):
    assert abs(tot[i] - d.SEAT_TOTAL[y]['seats']) / d.SEAT_TOTAL[y]['seats'] < 0.01, (y, tot[i])
    assert d.SEAT_TOTAL[y]['govt_colleges'] + d.SEAT_TOTAL[y]['pvt_colleges'] == d.SEAT_TOTAL[y]['colleges']
from build import build_xlsx, build_json  # noqa: E402
build_xlsx(); json.dumps(build_json())
from openpyxl import load_workbook
assert len(load_workbook(os.path.join(ROOT, 'app', 'static', 'data', 'neet_trends_2023_2025.xlsx')).sheetnames) == 18
from app import create_app
app = create_app(); app.config['TESTING'] = True
c = app.test_client()
r = c.get('/neet-trends-2023-2025'); t = r.get_data(as_text=True)
assert r.status_code == 200 and 'neet_trends.js' in t and 'neet_trends_2023_2025.xlsx' in t
assert c.get('/static/data/neet_trends_2023_2025.xlsx').status_code == 200
assert c.get('/static/js/neet_trends_data.js').get_data(as_text=True).startswith('/* NEET UG 2023-2025')
assert 'NEET 2023-2025 Trends' in c.get('/medicine').get_data(as_text=True)
print('neet trends checks passed')
