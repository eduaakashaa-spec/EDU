"""TN Board Class 12 syllabus analytics page. Run from college-predictor/:  python tests/test_tn_board.py"""
import json, os, re, sys, tempfile
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
_fd, _db = tempfile.mkstemp(suffix='.db'); os.close(_fd)
os.environ.update(DATABASE_URL='sqlite:///' + _db, SECRET_KEY='test', FLASK_DEBUG='0')
from app import create_app  # noqa: E402
from app.data import tn_board as D  # noqa: E402
from app.services import tn_board as S  # noqa: E402
app = create_app(); app.config['TESTING'] = True
c = app.test_client()

# every JEE Main 2026 chapter is mapped, with a valid status
with open(os.path.join(ROOT, 'app', 'data', 'jee_syllabus_2026.json'), encoding='utf-8') as f:
    names = {ch['ch'] for ch in json.load(f)['chs']}
assert names == set(D.JEE_MAP), names ^ set(D.JEE_MAP)
assert all(v[0] in S.WEIGHT for v in D.JEE_MAP.values()) and all(r[4] in S.WEIGHT for r in D.NEET)
# NEET paper about 45 questions a subject (Biology 90)
for sub, want in (('Physics', 45), ('Chemistry', 45), ('Biology', 90)):
    tot = sum(r[3] for r in D.NEET if r[0] == sub)
    assert abs(tot - want) <= 4, (sub, tot)
# assessment areas only name real chapters
jee_ch = set(D.JEE_MAP); neet_ch = {r[2] for r in D.NEET}
for sub, areas in D.AREAS.items():
    for name, js, ns in areas:
        assert set(js) <= jee_ch, (name, set(js) - jee_ch)
        assert set(ns) <= neet_ch, (name, set(ns) - neet_ch)
# coverage figures are sane: board share below TN 11+12 share
cov = S.coverage()
for ex in ('jee', 'neet'):
    a = cov[ex]['all']
    assert 0 < a['board12'] < a['tn11_12'] <= 100 and abs(a['tn11_12'] + a['gap'] - 100) < 0.2
assert {r['tier'] for r in S.jee_rows()} == {1, 2, 3, 4}
# calendar has the TN board window and is sorted
cal = S.calendar()
ids = [e['id'] for e in cal]
assert 'tn-12-theory' in ids and 'jee-main-s1' in ids and 'neet-ug' in ids
assert [e['start'] for e in cal] == sorted(e['start'] for e in cal)
th = next(e for e in cal if e['id'] == 'tn-12-theory')
assert th['start'] == '2027-03-03' and th['end'] == '2027-03-29'

h = c.get('/tn-board-12-analytics')
t = h.get_data(as_text=True)
assert h.status_code == 200 and 'TN Board Class 12 Syllabus Analytics' in t and 'tn_board.js' in t and 'window.EA_TNB' in t
assert 'TN Board 12 vs JEE &amp; NEET' in t   # menu link
assert c.get('/static/js/tn_board.js').status_code == 200
assert not re.search(r'(^|\})\s*(html|body)\s*\{', c.get('/static/css/tn_board.css').get_data(as_text=True))
print('tn board checks passed')
