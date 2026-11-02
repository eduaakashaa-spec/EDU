"""Architecture and Planning pages: data integrity and rendering.
Run from college-predictor/:  python tests/test_arch_planning.py"""
import json
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
_fd, _db = tempfile.mkstemp(suffix='.db')
os.close(_fd)
os.environ.update(DATABASE_URL='sqlite:///' + _db, SECRET_KEY='test', FLASK_DEBUG='0')

from app import create_app  # noqa: E402
from app.data import arch_planning as d  # noqa: E402
from app.extensions import db  # noqa: E402

# NIRF list: 40 rows, ranks 1..40, score = weighted parameters (0.40, 0.20, 0.20, 0.10, 0.10) to within rounding
assert len(d.NIRF) == 40 and [r[0] for r in d.NIRF] == list(range(1, 41))
w = [p[2] for p in d.NIRF_PARAMS]
assert abs(sum(w) - 1) < 1e-9
for r in d.NIRF:
    assert abs(sum(a * b for a, b in zip(r[5], w)) - r[4]) < 0.06, r[1]
assert [r[4] for r in d.NIRF] == sorted([r[4] for r in d.NIRF], reverse=True)

# JoSAA 2026 rows
j = d.josaa()
assert len(j['institutes']) == 20 and len(j['rows']) > 250
assert all(0 <= r['i'] < 20 and r['p'] in 'AP' and r['q'] in ('AI', 'HS', 'OS') and len(r['c']) == 5 for r in j['rows'])
assert all(o <= c for r in j['rows'] for o, c in zip(r['o'], r['c']) if o is not None and c is not None)
assert set(j['institutes']) == set(d.INST_META)
assert len(j['dasa']) == 16

# college directory
cd = d.colleges()
cols = cd['colleges']
assert len(cols) >= 60 and len({c['name'] for c in cols}) == len(cols)
assert sum(1 for c in cols if c['nirf_rank']) == 40 and len({c['nirf_rank'] for c in cols if c['nirf_rank']}) == 40
for c in cols:
    assert c['state'] and c['name']
    if c.get('tuition'):
        assert c.get('fee_text') and 'unverified' not in c['fee_text'] and c['sources'], c['name']
    if 'unverified' in (c.get('fee_text') or ''):
        assert not c.get('tuition')
assert any(c.get('placement_text') for c in cols)
text = json.dumps(cd).lower()
assert 'whatsapp' not in text

g = d.guide_context()
assert g['states'] == sorted(g['states']) and sum(len(v) for v in g['by_state'].values()) == len(cols)
assert all(r['c5'] for r in g['josaa_rows'])
a = d.analytics_context()
assert a['findings'] and len(a['dasa_rows']) == 16

app = create_app()
app.config['TESTING'] = True
with app.app_context():
    db.create_all()
cl = app.test_client()
r = cl.get('/architecture-planning-india')
assert r.status_code == 200
h = r.get_data(as_text=True)
for t in ('Colleges by state', 'NIRF India Rankings 2025', 'NRI quota', 'dg-alert', 'Common questions', 'Indian Institute of Technology Roorkee', 'Not found'):
    assert t in h, t
r = cl.get('/architecture-planning-analytics')
assert r.status_code == 200
h = r.get_data(as_text=True)
for t in ('Rank finder', 'window.ARCH', 'arch_analytics.js', 'dg-alert', 'DASA 2025'):
    assert t in h, t
for u in ('/architecture-colleges', '/barch-colleges', '/architecture-planning'):
    assert cl.get(u).status_code == 301
assert cl.get('/static/js/arch_analytics.js').status_code == 200
print('arch planning: ok')
