"""EduPulse-NIFT: bank integrity, composition, marking (+1 / -0.25), spaced-review cards, Daily Review, tracker, studio, access and the public page.
Run from college-predictor/:  python tests/test_nift.py"""
import json
import os
import re
import sys
import tempfile
from datetime import date, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
_fd, _db = tempfile.mkstemp(suffix='.db')
os.close(_fd)
os.environ.update(DATABASE_URL='sqlite:///' + _db, SECRET_KEY='test', FLASK_DEBUG='0')

from app import create_app  # noqa: E402
from app.data import nift_exam  # noqa: E402
from app.extensions import bcrypt, db  # noqa: E402
from app.models import User  # noqa: E402
from app.models_pulse import PulseNiftCard, PulseNiftResult, PulseNiftStudio  # noqa: E402
from app.services import nift  # noqa: E402

# ---- bank --------------------------------------------------------------------------------------------------------------------------------
bank = nift.bank()
assert len(bank) >= 1300 and len({q['id'] for q in bank}) == len(bank)
for q in bank:
    assert q['sec'] in nift.SEC and q['q'].strip() and q['why'] and q['topic'], q['id']
    assert len(q['opts']) == 4 and all(o.strip() for o in q['opts']) and 0 <= q['ans'] < 4, q['id']
    assert len({o.lower() for o in q['opts']}) == 4, q['id']
    assert q['src'] and all(len(s) == 3 and 2016 <= s[0] <= 2023 and s[1] in nift.PROGS.values() for s in q['src']), q['id']
    assert '�' not in json.dumps(q, ensure_ascii=False), q['id']
blob = json.dumps(bank, ensure_ascii=False).lower()
for bad in ('prepp', 'collegedekho', 'careers360', 'collegedunia', 'shiksha', 'getmyuni', 'toprankers', 'whatsapp'):
    assert bad not in blob, bad
secs = {s: sum(1 for q in bank if q['sec'] == s) for s in nift.SEC}
assert all(n >= 150 for n in secs.values()), secs
pos = [sum(1 for q in bank if q['ans'] == k) for k in range(4)]
assert min(pos) > 0.15 * len(bank), pos
for q in bank:
    if q['sec'] == 'CMP':
        assert q['ctx'] or len(q['q']) > 40, q['id']
st = nift.studio()
assert len(st) == 22 and len({t['id'] for t in st}) == 22 and all(sum(r['max'] for r in t['rubric']) == 10 and len(t['rubric']) == 4 for t in st)
ana = nift.analysis()
assert ana['read'] > 1500 and set(ana['topics']) == set(nift.SEC) and ana['mix']

app = create_app()
app.config['TESTING'] = True
pw = lambda: bcrypt.generate_password_hash('x').decode()
with app.app_context():
    db.create_all()
    db.session.add_all([User(name='Free', email='f@x.com', tier='free', password_hash=pw()), User(name='Prem', email='p@x.com', tier='premium', password_hash=pw())])
    db.session.commit()
    prem_id = User.query.filter_by(email='p@x.com').one().id
_ctx = app.app_context()
_ctx.push()

# ---- catalogue and composition -----------------------------------------------------------------------------------------------------------
cat = nift.catalogue()
ids = [t['id'] for t in cat]
assert len(ids) == len(set(ids))
for need in ('M-BDES', 'M-BFTECH', 'M-BFTECH-B', 'M-MDES', 'M-MFM', 'M-MFTECH', 'S-QA', 'S-ENG', 'S-CMP', 'S-ANA', 'S-GK', 'Y-2023-BDES', 'Y-2022-MFTECH', 'Y-2016-BDES'):
    assert need in ids, need
assert {t['count'] for t in cat if t['id'] == 'M-BDES'} == {100} and {t['minutes'] for t in cat if t['id'] == 'M-BDES'} == {120}
m1 = nift.compose('M-BDES', 5, 0)
m1b = nift.compose('M-BDES', 5, 0)
m2 = nift.compose('M-BDES', 5, 1)
assert m1['qids'] == m1b['qids'] and m1['qids'] != m2['qids'] and len(m1['qids']) == 100 and len(set(m1['qids'])) == 100
mix = {}
for i in m1['qids']:
    q = nift.get(i)
    assert q and q['sec'] in nift.SEC
    mix[q['sec']] = mix.get(q['sec'], 0) + 1
assert mix == {'ENG': 25, 'CMP': 15, 'QA': 20, 'ANA': 15, 'GK': 25}, mix
for pid, (title, spec, _) in nift.MOCKS.items():
    t = nift.compose('M-' + pid, 1, 0)
    assert len(t['qids']) == sum(n for _, n in spec), pid
yr = nift.compose('Y-2023-BDES', 1, 0)
nums = [next(n for y, p, n in nift.get(i)['src'] if y == 2023 and p == 'B.Des') for i in yr['qids']]
assert nums == sorted(nums) and len(nums) >= nift.YEAR_MIN
sets = nift.compose('S-CMP', 1, 0)
assert len(sets['qids']) == 15
g = [i for i in nift.compose('S-QA', 1, 0)['qids'] if i.startswith('g:')]
assert g and nift.get(g[0])['sec'] == 'QA' and nift.get(g[0])['opts'] and nift.get(g[0]) is not None
assert nift.get('g:series:5')['sec'] == 'ANA'
assert nift.get('nope') is None and nift.get('g:zz:1') is None
assert nift.compose('NOPE', 1, 0) is None

# ---- the app -----------------------------------------------------------------------------------------------------------------------------


_ctx.pop()


def compose(tid, uid, attempt):
    with app.app_context():
        return nift.compose(tid, uid, attempt)


def login(em):
    c = app.test_client()
    assert c.post('/login', data={'email': em, 'password': 'x'}).status_code == 302
    return c


anon, free, prem = app.test_client(), login('f@x.com'), login('p@x.com')

# public page
page = anon.get('/nift-papers-analysis')
h = page.get_data(as_text=True)
assert page.status_code == 200 and 'dg-alert' in h and 'What the NIFT papers' in h and 'Six free questions' in h and 'nfSamples' in h
for bad in ('prepp', 'collegedekho', 'careers360', 'collegedunia', 'toprankers'):
    assert bad not in h.lower(), bad
assert len(nift_exam.samples()) == 6
for u in ('/nift-previous-papers', '/nift-mock-test', '/nift-gat-papers'):
    assert anon.get(u).status_code == 301

# access
assert anon.get('/nift-mock/').status_code == 302 and free.get('/nift-mock/').status_code == 403
assert free.get('/nift-mock/test/M-BDES').status_code == 403 and free.get('/nift-mock/daily').status_code == 403 and free.get('/nift-mock/studio').status_code == 403
home = prem.get('/nift-mock/').get_data(as_text=True)
assert prem.get('/nift-mock/').status_code == 200 and 'EduPulse-NIFT' in home and 'GAT mock, B.Des' in home and 'Previous-year papers' in home
assert prem.get('/nift-mock/studio').status_code == 200 and prem.get('/nift-mock/studio/C03').status_code == 200 and prem.get('/nift-mock/studio/NOPE').status_code == 404
assert prem.get('/nift-mock/test/NOPE').status_code == 404

# marking: +1, -0.25, blank 0
r = prem.get('/nift-mock/test/S-ANA')
body_html = r.get_data(as_text=True)
assert r.status_code == 200 and '"ans"' not in body_html and '"why"' not in body_html
qids = compose('S-ANA', prem_id, 0)['qids']
qs = [nift.get(i) for i in qids]
answers = {}
for k, q in enumerate(qs):
    answers[qids[k]] = {'a': q['ans'] if k < 8 else (q['ans'] + 1) % 4 if k < 12 else None, 'c': 'H' if k % 3 else 'G'}
j = prem.post('/nift-mock/submit/S-ANA', json={'qids': qids, 'answers': answers, 'timed': True, 'seconds': 600}).get_json()
assert j['ok'] and j['url'].startswith('/nift-mock/result/')
with app.app_context():
    row = db.session.get(PulseNiftResult, j['id'])
    assert (row.right, row.wrong, row.blank) == (8, 4, 3) and row.score == 7.0 and row.max_score == 15, (row.right, row.wrong, row.blank, row.score)
    assert row.sure_wrong == sum(1 for k in range(8, 12) if k % 3)
rep = prem.get(j['url'])
rh = rep.get_data(as_text=True)
assert rep.status_code == 200 and 'Explanation:' in rh and 'Question review' in rh and 'NIFT 20' in rh or 'practice question (generated)' in rh
assert free.get(j['url']).status_code in (403, 404) and anon.get(j['url']).status_code == 302
assert prem.post('/nift-mock/submit/NOPE', json={'qids': qids, 'answers': {}}).status_code == 404
assert prem.post('/nift-mock/submit/S-ANA', json={'answers': 'x'}).status_code == 400
assert prem.post('/nift-mock/submit/S-ANA', json={'qids': ['zzz'], 'answers': {}}).status_code == 400
assert prem.post('/nift-mock/submit/S-ANA', json={'qids': [], 'answers': {}}).status_code == 400
# a tampered payload cannot award itself marks: a chosen option outside 0..3 is treated as blank
rows, err = nift.grade_paper({'qids': qids[:2], 'answers': {qids[0]: {'a': 9, 'c': 'H'}, qids[1]: {'a': True, 'c': 'X'}}})
assert not err and rows[0]['chosen'] is None and rows[1]['chosen'] is None and rows[1]['conf'] is None and nift.marks_of(rows) == 0

# ---- review cards (Leitner) --------------------------------------------------------------------------------------------------------------
with app.app_context():
    cards = {c.qkey: c for c in PulseNiftCard.query.filter_by(user_id=prem_id).all()}
    wrong_ids = [nift.key_of(qids[k]) for k in range(8, 12)]
    assert all(w in cards and cards[w].box == 0 for w in wrong_ids)
    unsure_right = [nift.key_of(qids[k]) for k in range(8) if k % 3 == 0]
    assert all(u in cards and cards[u].box in (1, 2) for u in unsure_right)
    sure_right = [nift.key_of(qids[k]) for k in range(8) if k % 3]
    assert not any(s in cards for s in sure_right)
    n_cards = len(cards)
    key = wrong_ids[0]
    q = nift.get(key if not key.startswith('g:') else qids[8])
    # right and sure, over time: the card climbs and its due date moves out
    today = date.today()
    for step, box in enumerate((1, 2, 3, 4, 5, 5)):
        nift._update_cards(prem_id, [{'qid': qids[8], 'sec': 'ANA', 'topic': 't', 'chosen': 1, 'right': True, 'conf': 'H'}], False, today)
        db.session.commit()
        c = PulseNiftCard.query.filter_by(user_id=prem_id, qkey=wrong_ids[0]).one()
        assert c.box == box and c.due == today + timedelta(days=nift.INTERVALS[box]), (step, c.box)
    nift._update_cards(prem_id, [{'qid': qids[8], 'sec': 'ANA', 'topic': 't', 'chosen': 1, 'right': False, 'conf': 'H'}], True, today)
    db.session.commit()
    c = PulseNiftCard.query.filter_by(user_id=prem_id, qkey=wrong_ids[0]).one()
    assert c.box == 0 and c.due == today + timedelta(days=1)
    # Daily Review: due cards first (a generated idea returns with a new seed), then new questions
    for c in PulseNiftCard.query.filter_by(user_id=prem_id).all():
        c.due = today
    db.session.commit()
    d = nift.daily(prem_id)
    assert len(d['qids']) == nift.DAILY_N and len(set(d['qids'])) == nift.DAILY_N and d['cards'] >= 1
    due_keys = {c.qkey for c in nift.due_cards(prem_id)}
    assert all(nift.key_of(i) in due_keys for i in d['qids'][:d['cards']])
    gen_cards = [c for c in nift.due_cards(prem_id) if c.qkey.startswith('g:')]
    if gen_cards:
        assert any(i.startswith(gen_cards[0].qkey + ':') for i in d['qids'])
    tr = nift.tracker(prem_id)
    assert tr['cards'] == n_cards and tr['due'] >= 1 and tr['answers'] == 12 and set(tr['secs']) == set(nift.SEC) and tr['secs']['ANA']['n'] == 12
assert prem.get('/nift-mock/daily').status_code == 200
dj = prem.post('/nift-mock/submit/DAILY', json={'qids': d['qids'], 'answers': {i: {'a': 0, 'c': 'L'} for i in d['qids']}, 'timed': False, 'seconds': 60}).get_json()
assert dj['ok']

# a full mock: composition over HTTP, marking of a complete paper
mock_q = compose('M-BDES', prem_id, 0)
ans = {i: {'a': nift.get(i)['ans'], 'c': 'M'} for i in mock_q['qids']}
mj = prem.post('/nift-mock/submit/M-BDES', json={'qids': mock_q['qids'], 'answers': ans, 'timed': True, 'seconds': 7000}).get_json()
with app.app_context():
    row = db.session.get(PulseNiftResult, mj['id'])
    assert row.score == 100 and row.right == 100 and row.prog == 'BDES'
    an = nift.analyse([row])
    assert an['acc'] == 100 and {s['sec'] for s in an['secs']} == set(nift.SEC)
    yrs = nift.tracker(prem_id)['mocks']
    assert yrs and yrs[-1]['score'] == 100
assert prem.get('/nift-mock/progress').status_code == 200 and 'Section levels' in prem.get('/nift-mock/progress').get_data(as_text=True)
assert free.get('/nift-mock/progress').status_code == 403
assert prem.get('/nift-mock/student/%d' % prem_id).status_code == 404       # not a mentor of this student

# ---- studio -------------------------------------------------------------------------------------------------------------------------------
r = prem.post('/nift-mock/studio/C03', data={'s0': '3', 's1': '2', 's2': '3', 's3': '2', 'note': 'More contrast'})
assert r.status_code == 302
with app.app_context():
    row = PulseNiftStudio.query.filter_by(user_id=prem_id, tid='C03').one()
    assert row.total == 10 and row.note == 'More contrast'
r = prem.post('/nift-mock/studio/C03', data={'s0': '9', 's1': '2', 's2': '3', 's3': '2'}, follow_redirects=True)
assert 'Please mark every line' in r.get_data(as_text=True)
assert nift.save_studio(prem_id, 'NOPE', [1, 1, 1, 1], '') is None and nift.save_studio(prem_id, 'C03', [1, 1, 1], '') is None

# ---- member home, menu --------------------------------------------------------------------------------------------------------------------
mh = prem.get('/member-home').get_data(as_text=True)
assert 'EduPulse-NIFT Mock Test Centre' in mh
assert 'NIFT Papers Analysed' in anon.get('/').get_data(as_text=True)
print('nift checks passed')
