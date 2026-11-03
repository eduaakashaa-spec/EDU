"""NID pages and the EduPulse-NID mock centre: data integrity, test composition, server-side marking, access and reports.
Run from college-predictor/:  python tests/test_nid.py"""
import json
import os
import re
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
_fd, _db = tempfile.mkstemp(suffix='.db')
os.close(_fd)
os.environ.update(DATABASE_URL='sqlite:///' + _db, SECRET_KEY='test', FLASK_DEBUG='0')

from app import create_app  # noqa: E402
from app.data import nid_papers as np_  # noqa: E402
from app.extensions import bcrypt, db  # noqa: E402
from app.models import User  # noqa: E402
from app.services import nid  # noqa: E402

# ---- the bank ----------------------------------------------------------------------------------------------------------------------------
bank = nid.bank()
assert len(bank) >= 380 and len({q['id'] for q in bank}) == len(bank)
for q in bank:
    assert q['sec'] in nid.SEC and len(q['opts']) == 4 and 0 <= q['ans'] < 4 and q['marks'] in (1, 2) and q['why'] and q['level'] in ('B', 'M', 'BM'), q['id']
    texts = [json.dumps(o, sort_keys=True) for o in q['opts']]
    assert len(set(texts)) == 4, q['id']
blob = json.dumps(bank, ensure_ascii=False).lower()
for bad in ('collegedekho', 'careers360', 'collegedunia', 'shiksha', 'getmyuni', 'toprankers', 'creativedge', 'creative edge', 'whatsapp'):
    assert bad not in blob, bad
pos = [sum(1 for q in bank if q['ans'] == k) for k in range(4)]
assert min(pos) > 0.15 * len(bank), pos                                                    # answers are spread over A to D
assert sum(1 for q in bank if q['src'] == 'visual') >= 120 and sum(1 for q in bank if q['sec'] == 'SPA') >= 40
# every generated visual question has the figures it needs
for q in bank:
    if q['src'] == 'visual':
        assert (q.get('svg') or any(o.get('svg') for o in q['opts'])), q['id']
# computed answers: spot-check the generators with independent arithmetic
for q in bank:
    if q['id'].startswith('V-SQUAR'):
        n = int(re.search(r'(\d) by', q['q']).group(1))
        assert q['opts'][q['ans']]['t'] == str(sum(k * k for k in range(1, n + 1))), q['id']
    if q['id'].startswith('V-CLOCK'):
        h, m = [int(x) for x in re.search(r'(\d+):(\d\d)', q['q']).groups()]
        ang = abs(30 * (h % 12) - 5.5 * m)
        ang = min(ang, 360 - ang)
        assert float(q['opts'][q['ans']]['t'].split()[0]) == ang, q['id']

# ---- tests and official papers -----------------------------------------------------------------------------------------------------------
ts = nid.tests()
ids = [t['id'] for t in ts]
assert len(set(ids)) == len(ids)
full = {t['id']: t for t in ts if t['kind'] == 'full'}
assert set(full) == {'B1', 'B2', 'B3', 'B4', 'M1', 'M2', 'M3', 'M4'}
for k in ('B1', 'B2', 'B3', 'B4'):
    t = full[k]
    qs = [nid.by_id()[i] for i in t['qids']]
    assert len(qs) == 20 and sum(q['marks'] for q in qs) == 25 and sum(1 for q in qs if q['marks'] == 2) == 5 and len(set(t['qids'])) == 20      # as in NID's B.Des sample: 15 x 1 + 5 x 2
    assert all('B' in q['progs'] for q in qs)
for k in ('M1', 'M2', 'M3', 'M4'):
    t = full[k]
    qs = [nid.by_id()[i] for i in t['qids']]
    assert len(qs) == 18 and sum(q['marks'] for q in qs) == 20 and sum(1 for q in qs if q['marks'] == 2) == 2                                     # as in the CDAT Paper 1 sample: 16 x 1 + 2 x 2
bseen = [i for k in ('B1', 'B2', 'B3', 'B4') for i in full[k]['qids']]
assert len(bseen) == len(set(bseen))                                                           # B.Des mocks never repeat a question
off = nid.official()
assert [p['code'] for p in off['papers']] == ['BDES25', 'BDES24', 'MDES25', 'MDES24'] and sum(p['questions'] for p in off['papers']) == 72
usable = [q for q in off['questions'] if q['usable']]
assert 50 <= len(usable) <= 72 and all(q['ans'] in (0, 1, 2, 3) and q['why'] and os.path.exists(os.path.join(ROOT, 'app', 'static', q['img'])) for q in usable)
assert not [q for q in usable if q['paper'] == 'MDES25' and q['n'] == 1]                      # the printed options of that sample question contain no correct code
otests = [t for t in ts if t['kind'] == 'official']
assert len(otests) == 4 and all(t['source'] == 'official' for t in otests)
assert len([t for t in ts if t['kind'] == 'section']) >= 30
tk = nid.tasks()
assert len(tk) == 30 and all(sum(r['marks'] for r in t['rubric']) == t['marks'] for t in tk) and {t['stage'] for t in tk} == {'Prelims', 'Studio'}

# ---- the public page and its data --------------------------------------------------------------------------------------------------------
ana = np_.analysis()
assert ana['papers_analysed'] >= 15 and ana['questions_tagged'] > 300 and len(ana['formats']) == 11 and [f['year'] for f in ana['formats']] == list(range(2015, 2026))
f25 = [f for f in ana['formats'] if f['year'] == 2025][0]
assert (f25['total'], f25['mcq_marks'], f25['subj_marks']) == (100, 25, 75)
assert len(np_.samples()) == 6

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
page = anon.get('/nid-papers-analysis')
h = page.get_data(as_text=True)
assert page.status_code == 200 and 'dg-alert' in h and 'What the NID papers' in h and 'npFmt' in h and 'Six free practice questions' in h
assert 'collegedekho' not in h.lower() and 'toprankers' not in h.lower() and 'creativedge' not in h.lower()
for u in ('/nid-previous-papers', '/nid-mock-test', '/nid-dat-papers'):
    assert anon.get(u).status_code == 301
assert anon.get('/nid').status_code == 200 and 'nid-papers-analysis' in anon.get('/nid').get_data(as_text=True)

# ---- access and marking ------------------------------------------------------------------------------------------------------------------
assert anon.get('/nid-mock/').status_code == 302 and free.get('/nid-mock/').status_code == 403
home = prem.get('/nid-mock/').get_data(as_text=True)
assert prem.get('/nid-mock/').status_code == 200 and 'EduPulse-NID Mock Test Centre' in home and 'B.Des Prelims mock 1' in home and 'Studio and drawing practice' in home
assert prem.get('/nid-mock/studio').status_code == 200 and free.get('/nid-mock/studio').status_code == 403
assert prem.get('/nid-mock/studio/T01').status_code == 200 and prem.get('/nid-mock/studio/NOPE').status_code == 404
t = full['B1']
r = prem.get('/nid-mock/test/B1')
page = r.get_data(as_text=True)
assert r.status_code == 200 and '"ans"' not in page and '"why"' not in page
qs = [nid.by_id()[i] for i in t['qids']]
body = {'answers': {q['id']: {'a': q['ans'], 'c': 'H'} for q in qs}, 'timed': True, 'seconds': 700}
j = prem.post('/nid-mock/submit/B1', json=body).get_json()
assert j['ok'] and j['url'].startswith('/nid-mock/result/')
from app.models_pulse import PulseNidResult  # noqa: E402
with app.app_context():
    row = PulseNidResult.query.one()
    assert row.score == 25 and row.max_score == 25 and row.right == 20 and row.wrong == 0
# some wrong, some blank: marks are the question marks, nothing is deducted
body['answers'] = {q['id']: {'a': (q['ans'] + 1) % 4 if k < 5 else q['ans'] if k < 9 else None, 'c': 'H'} for k, q in enumerate(qs)}
j2 = prem.post('/nid-mock/submit/B1', json=body).get_json()
with app.app_context():
    row = db.session.get(PulseNidResult, j2['id'])
    exp = sum(q['marks'] for k, q in enumerate(qs) if 5 <= k < 9)
    assert (row.right, row.wrong, row.blank, row.score, row.sure_wrong) == (4, 5, 11, exp, 5), (row.right, row.wrong, row.blank, row.score, exp)
rep = prem.get(j2['url'])
assert rep.status_code == 200 and 'Explanation:' in rep.get_data(as_text=True) and free.get(j2['url']).status_code in (404, 403)
assert prem.post('/nid-mock/submit/NOPE', json=body).status_code == 404 and prem.post('/nid-mock/submit/B1', json={'answers': 'x'}).status_code == 400
# an official-paper attempt: option letters sit in the picture
ot = otests[0]
op = prem.get('/nid-mock/test/' + ot['id'])
assert op.status_code == 200 and '/static/img/nid/' in op.get_data(as_text=True)
oq = [nid.off_by_id()[i] for i in ot['qids']]
j3 = prem.post('/nid-mock/submit/' + ot['id'], json={'answers': {q['id']: {'a': q['ans'], 'c': 'M'} for q in oq}, 'timed': False, 'seconds': 300}).get_json()
assert j3['ok'] and 'Correct answer' in prem.get(j3['url']).get_data(as_text=True)
assert 'EduPulse-NID Mock Test Centre' in prem.get('/member-home').get_data(as_text=True)
print('nid checks passed')
