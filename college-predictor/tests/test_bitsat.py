"""BITSAT: public guide page and the EduPulse-BITSAT mock centre (bank integrity, tests, marking +3/-1, reports, access). Run from college-predictor/:  python tests/test_bitsat.py"""
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
from app.extensions import bcrypt, db  # noqa: E402
from app.models import User  # noqa: E402
from app.services import bitsat  # noqa: E402

# ---- bank integrity -----------------------------------------------------------------------------------------------------------------------
bank = bitsat.bank()
us = bitsat.usable()
assert len(bank) >= 600 and len(us) >= 550, (len(bank), len(us))
assert all(q['sj'] in dict(bitsat.SUBJECTS) for q in us) and all(q['ans'] in (0, 1, 2, 3) for q in us)
img = os.path.join(ROOT, 'app', 'static', 'img', 'bitsat')
for q in us:
    assert os.path.exists(os.path.join(img, str(q['year']), q['img'])), q['qid']
    assert q['passage'] is None or os.path.exists(os.path.join(img, str(q['year']), q['passage'])), q['qid']
assert max(sum(1 for q in us if q['ans'] == k) for k in range(4)) < 0.4 * len(us) and len({q['ans'] for q in us}) == 4      # the key uses all four letters
for p in bitsat.papers():
    meta = json.load(open(os.path.join(ROOT, 'app', 'data', 'bitsat', 'papers.json'), encoding='utf-8'))[str(p['year'])]
    counts = {}
    for code, lo, hi in meta['sections']:
        counts[code] = counts.get(code, 0) + hi - lo + 1
    assert set(counts) == {'PHY', 'CHE', 'ENG', 'LR', 'MAT'} and sum(counts.values()) == p['total'], (p['year'], counts)
    if p['total'] == 150:
        assert (counts['PHY'], counts['CHE'], counts['MAT'], counts['ENG'] + counts['LR']) == (40, 40, 45, 25), (p['year'], counts)
ts = bitsat.tests()
ids = [t['id'] for t in ts]
assert len(set(ids)) == len(ids) and any(t['kind'] == 'full' for t in ts) and any(t['kind'] == 'year' for t in ts) and any(t['kind'] == 'section' for t in ts)
for t in ts:
    assert all(bitsat.by_id()[i]['usable'] for i in t['qids']) and len(set(t['qids'])) == len(t['qids'])
full = [t for t in ts if t['kind'] == 'full']
seen = [i for t in full for i in t['qids']]
assert len(seen) == len(set(seen)) and all(len(t['qids']) == 130 and t['minutes'] == 180 for t in full)            # full mocks follow the 130-question pattern and never repeat a question
for t in full:
    n = {sj: sum(1 for i in t['qids'] if bitsat.by_id()[i]['sj'] == sj) for sj, _n in bitsat.SUBJECTS}
    assert n == bitsat.PATTERN, n

# ---- app ----------------------------------------------------------------------------------------------------------------------------------
app = create_app()
app.config['TESTING'] = True
pw = lambda: bcrypt.generate_password_hash('x').decode()
with app.app_context():
    db.create_all()
    db.session.add_all([User(name='Free', email='f@x.com', tier='free', password_hash=pw()), User(name='Prem', email='p@x.com', tier='premium', password_hash=pw())])
    db.session.commit()


def login(em):
    c = app.test_client()
    assert c.post('/login', data={'email': em, 'password': 'x'}).status_code == 302
    return c


anon, free, prem = app.test_client(), login('f@x.com'), login('p@x.com')
assert anon.get('/bitsat-mock/').status_code == 302 and free.get('/bitsat-mock/').status_code == 403
h = prem.get('/bitsat-mock/').get_data(as_text=True)
assert prem.get('/bitsat-mock/').status_code == 200 and 'EduPulse-BITSAT Mock Test Centre' in h and 'Previous-year papers' in h and 'memory-based' in h
t = next(x for x in ts if x['kind'] == 'section')
r = prem.get('/bitsat-mock/test/' + t['id'])
page = r.get_data(as_text=True)
assert r.status_code == 200 and '"ans"' not in page and '.webp' in page
qs = [bitsat.by_id()[i] for i in t['qids']]
body = {'answers': {q['qid']: {'a': q['ans'], 'c': 'H'} for q in qs}, 'timed': True, 'seconds': 600}
j = prem.post('/bitsat-mock/submit/' + t['id'], json=body).get_json()
assert j['ok'] and j['url'].startswith('/bitsat-mock/result/')
from app.models_pulse import PulseBitsatResult  # noqa: E402
with app.app_context():
    row = PulseBitsatResult.query.one()
    assert row.score == 3 * len(qs) and row.right == len(qs) and row.wrong == 0 and row.max_score == 3 * len(qs)
body['answers'] = {q['qid']: {'a': (q['ans'] + 1) % 4 if k < 5 else q['ans'] if k < 8 else None, 'c': 'H'} for k, q in enumerate(qs)}
j2 = prem.post('/bitsat-mock/submit/' + t['id'], json=body).get_json()
with app.app_context():
    row = db.session.get(PulseBitsatResult, j2['id'])
    assert (row.right, row.wrong, row.blank, row.score, row.sure_wrong) == (3, 5, len(qs) - 8, 9 - 5, 5)       # +3 x 3 right, -1 x 5 wrong
rep = prem.get(j2['url'])
txt = rep.get_data(as_text=True)
assert rep.status_code == 200 and 'Key: ' in txt and free.get(j2['url']).status_code in (404, 403)
assert prem.post('/bitsat-mock/submit/NOPE', json=body).status_code == 404 and prem.post('/bitsat-mock/submit/' + t['id'], json={'answers': 'x'}).status_code == 400

# ---- public page and Member Home ----------------------------------------------------------------------------------------------------------
page = anon.get('/bitsat').get_data(as_text=True)
assert anon.get('/bitsat').status_code == 200 and 'id="pattern"' in page and 'id="mock"' in page and 'Join to open the mock centre' in page
assert '130 multiple-choice questions' in page and '75% in aggregate' in page.replace('At least ', '') or '75%' in page
assert anon.get('/bitsat-guide').status_code == 301 and 'BITS Pilani (BITSAT)' in anon.get('/').get_data(as_text=True)
assert 'Open the BITSAT mock centre' in prem.get('/bitsat').get_data(as_text=True)
hub = prem.get('/member-home').get_data(as_text=True)
assert 'EduPulse-BITSAT Mock Test Centre' in hub and 'BITSAT guide' in hub
assert b'/bitsat' in anon.get('/sitemap.xml').data
print('bitsat checks passed')
