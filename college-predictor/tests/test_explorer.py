"""EduPulse-Explorer (Grades 7 to 10): bank integrity, generators, test composition, server-side marking, spaced-review cards, tracker, interests, access.
Run from college-predictor/:  python tests/test_explorer.py"""
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
from app.extensions import bcrypt, db  # noqa: E402
from app.models import User  # noqa: E402
from app.models_pulse import PulseExpCard, PulseExpResult  # noqa: E402
from app.services import explorer as ex  # noqa: E402
from app.services import explorer_gen as gen  # noqa: E402

# ---- bank --------------------------------------------------------------------------------------------------------------------------------
bank = ex.bank()
assert len(bank) >= 380 and len({q['id'] for q in bank}) == len(bank)
for q in bank:
    assert q['skill'] in ex.SKILLS and q['grade'] in ('7-8', '9-10', 'all') and q['diff'] in (1, 2, 3) and q['why'] and set(q['fam']) <= set(ex.FAMILIES), q['id']
    assert len(q['opts']) == 4 and 0 <= q['ans'] < 4, q['id']
    assert len({json.dumps(o, sort_keys=True) for o in q['opts']}) == 4, q['id']
    if q['src'] == 'visual':
        assert q.get('svg') or any(o.get('svg') for o in q['opts']), q['id']
blob = json.dumps(bank, ensure_ascii=False).lower()
for bad in ('collegedekho', 'careers360', 'collegedunia', 'shiksha', 'getmyuni', 'toprankers', 'creativedge', 'whatsapp'):
    assert bad not in blob, bad
for sk in ex.SKILLS:
    for band in ('7-8', '9-10'):
        assert len([q for q in bank if q['skill'] == sk and q['grade'] in (band, 'all')]) >= 12 or sk in ('MAT', 'LOG'), (sk, band)
pos = [sum(1 for q in bank if q['ans'] == k) for k in range(4)]
assert min(pos) > 0.15 * len(bank), pos
cr = ex.creative()
assert len(cr) == 12 and all(sum(r['marks'] for r in c['rubric']) == 10 for c in cr)

# ---- generators: every seed gives four distinct options and a rebuildable id --------------------------------------------------------------
for name in gen.GENERATORS:
    for s in range(120):
        q = gen.build(name, s)
        assert len(set(q['opts'])) == 4 and 0 <= q['ans'] < 4 and q['why'], (name, s)
        again = gen.from_id(q['id'])
        assert again['q'] == q['q'] and again['ans'] == q['ans'] and again['opts'] == q['opts']
assert gen.from_id('g:nope:1') is None and gen.from_id('junk') is None and gen.from_id('g:clock:x') is None
for s in range(120):                                              # independent arithmetic for a few generators
    q = gen.build('clock', s)
    h, m = [int(x) for x in re.search(r'at (\d+):(\d\d)', q['q']).groups()]
    a = abs(30 * (h % 12) - 5.5 * m)
    assert float(q['opts'][q['ans']]) == min(a, 360 - a)
    q = gen.build('lin', s)
    a_, b_, r_ = [int(x) for x in re.search(r'by (\d+), add (\d+) and get (\d+)', q['q']).groups()]
    assert int(q['opts'][q['ans']]) * a_ + b_ == r_
    q = gen.build('avg', s)
    nums = [int(x) for x in re.findall(r'\d+', q['q'].split('quiz are')[1].split('and one more')[0])]
    n_, av = [int(x) for x in re.search(r'of (\d+) students.*?average of all \d+ is (\d+)', q['q']).groups()] if False else (len(nums) + 1, int(re.search(r'is (\d+)\. What', q['q']).group(1)))
    assert int(q['opts'][q['ans']]) + sum(nums) == n_ * av

# ---- composition: fresh, valid, level-appropriate ----------------------------------------------------------------------------------------
for g in (7, 8, 9, 10):
    cat = ex.catalogue(g)
    assert {c['id'] for c in cat} >= {'X-JEE', 'X-UCD', 'X-NAT', 'X-IAT'} | {'K-' + s for s in ex.SKILLS} and any(c['kind'] == 'discovery' for c in cat)
    for c in cat:
        t = ex.compose(c['id'], g, 1, 0)
        assert t['qids'] and len(set(t['qids'])) == len(t['qids']) and len(t['qids']) <= ex.MAX_Q, (g, c['id'])
        assert all(ex.get(i) for i in t['qids']), c['id']
        band = ex.band_of(g)
        assert all(ex.get(i)['grade'] in (band, 'all') for i in t['qids'] if not i.startswith('g:')), c['id']
        assert t['qids'] == ex.compose(c['id'], g, 1, 0)['qids']                                   # same attempt: same paper
assert ex.compose('D78', 8, 1, 0)['qids'] != ex.compose('D78', 8, 1, 1)['qids']                    # next attempt: fresh paper
assert len(ex.compose('D78', 7, 1, 0)['qids']) == 28 and len(ex.compose('D910', 9, 1, 0)['qids']) == 35
assert ex.compose('NOPE', 8, 1, 0) is None
pb = ex.paper_for_browser(ex.compose('D910', 10, 1, 0)['qids'])
assert pb and all('ans' not in q and 'why' not in q for q in pb)
ir = ex.interest_result([5] * 16)
assert ir and len(ir['rows']) == 10 and ex.interest_result([5] * 15) is None and ex.interest_result([6] * 16) is None and ex.interest_result(['a'] * 16) is None
ir2 = ex.interest_result([5, 1, 1, 1, 1, 1, 5, 1, 5, 1, 1, 1, 1, 1, 1, 5])
assert ir2['lean'] == 'engineering' and ir2['eng'][0]['key'] in ('ELE', 'COM', 'MEC')

# ---- app: access, marking, cards, tracker ------------------------------------------------------------------------------------------------
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


anon, free = app.test_client(), login('f@x.com')
assert anon.get('/explorer/').status_code == 302
h = free.get('/explorer/').get_data(as_text=True)
assert 'Which grade are you in?' in h
assert free.get('/explorer/test/D78').status_code == 302                              # grade first
assert free.post('/explorer/grade', data={'grade': '5'}).status_code == 302 and 'Which grade' in free.get('/explorer/').get_data(as_text=True)
assert free.post('/explorer/grade', data={'grade': '8', 'goal': '4'}).status_code == 302
home = free.get('/explorer/').get_data(as_text=True)
assert 'Discovery Test, Grades 7 to 8' in home and 'Daily 10' in home and 'JEE-style taster' in home
page = free.get('/explorer/test/D78').get_data(as_text=True)
assert 'EduPulse-Explorer' in page and '"ans"' not in page and '"why"' not in page
with app.app_context():
    uid = User.query.filter_by(email='f@x.com').one().id
t = ex.compose('D78', 8, uid, 0)
qs = [ex.get(i) for i in t['qids']]
body = {'qids': t['qids'], 'answers': {q['id']: {'a': q['ans'], 'c': 'H'} for q in qs}, 'timed': True, 'seconds': 600}
j = free.post('/explorer/submit/D78', json=body).get_json()
assert j['ok'] and j['url'].startswith('/explorer/result/')
with app.app_context():
    row = PulseExpResult.query.one()
    assert (row.score, row.max_score, row.right, row.wrong) == (28, 28, 28, 0) and PulseExpCard.query.count() == 0
# some wrong (sure), some right but a guess, some blank
ans = {}
for k, q in enumerate(qs):
    if k < 6:
        ans[q['id']] = {'a': (q['ans'] + 1) % 4, 'c': 'H'}
    elif k < 10:
        ans[q['id']] = {'a': q['ans'], 'c': 'G'}
    elif k < 14:
        pass
    else:
        ans[q['id']] = {'a': q['ans'], 'c': 'M'}
j2 = free.post('/explorer/submit/D78', json={'qids': t['qids'], 'answers': ans, 'timed': False, 'seconds': 300}).get_json()
with app.app_context():
    row = db.session.get(PulseExpResult, j2['id'])
    assert (row.right, row.wrong, row.blank, row.sure_wrong, row.lucky) == (18, 6, 4, 6, 4), (row.right, row.wrong, row.blank, row.sure_wrong, row.lucky)
    cards = PulseExpCard.query.all()
    assert len(cards) == 10 and sum(1 for c in cards if c.box == 0) == 6 and sum(1 for c in cards if c.box == 1) == 4
    assert all(c.due <= date.today() + timedelta(days=1) for c in cards)
    gen_cards = [c for c in cards if c.qkey.startswith('g:')]
    assert all(c.qkey.count(':') == 1 for c in gen_cards)
rep = free.get(j2['url'])
txt = rep.get_data(as_text=True)
assert rep.status_code == 200 and 'Explanation:' in txt and 'How exams ask this' in txt and 'review card' in txt
assert anon.get(j2['url']).status_code == 302
other = login('p@x.com')
assert other.get(j2['url']).status_code == 404                                                   # not someone else's report
# bad submissions
assert free.post('/explorer/submit/NOPE', json=body).status_code == 404
assert free.post('/explorer/submit/D78', json={'qids': ['g:evil:1'], 'answers': {}}).status_code == 400
assert free.post('/explorer/submit/D78', json={'qids': [], 'answers': {}}).status_code == 400
assert free.post('/explorer/submit/D78', json={'qids': 'x', 'answers': {}}).status_code == 400
assert free.post('/explorer/submit/D78', json={'qids': ['T1-000'] * 3 + [q['id'] for q in qs], 'answers': 'x'}).status_code == 400
# the Daily 10 serves the due cards, fresh numbers for generated ones, and a right answer promotes the card
with app.app_context():
    d = ex.daily(uid, 8)
    assert len(d['qids']) == 10 and d['cards'] >= 6 and len(set(d['qids'])) == 10
    due_keys = {c.qkey for c in ex.due_cards(uid)}
    assert {ex.key_of(i) for i in d['qids'][:d['cards']]} <= due_keys
dq = d['qids']
ok = free.post('/explorer/submit/DAILY', json={'qids': dq, 'answers': {i: {'a': ex.get(i)['ans'], 'c': 'H'} for i in dq}, 'timed': False, 'seconds': 200}).get_json()
assert ok['ok']
with app.app_context():
    cards = PulseExpCard.query.all()
    moved = [c for c in cards if c.box >= 1 and c.right_run]
    assert len(moved) >= 5, len(moved)
    assert all(c.due >= date.today() for c in moved if c.box >= 1)
assert free.get('/explorer/daily').status_code == 200
# tracker, progress, mentor view
with app.app_context():
    tr = ex.tracker(uid)
    assert tr['attempts'] == 3 and tr['streak'] == 1 and tr['week'] == 1 and tr['goal'] == 4 and sum(tr['boxes']) == tr['cards']
    assert tr['skills']['SPA']['acc'] is not None and any(b['id'] == 'first' and b['got'] for b in tr['badges'])
pg = free.get('/explorer/progress')
assert pg.status_code == 200 and 'Review boxes' in pg.get_data(as_text=True)
assert free.get('/explorer/student/%d' % uid).status_code == 404                                  # a student cannot open the mentor view
# interests and creative
ia = {('q%d' % i): '4' for i in range(16)}
assert free.post('/explorer/interests', data=ia).status_code == 302
assert 'You lean towards' in free.get('/explorer/interests').get_data(as_text=True)
assert free.post('/explorer/interests', data={'q0': '4'}).status_code == 302
assert free.get('/explorer/make').status_code == 200 and free.get('/explorer/make/C01').status_code == 200 and free.get('/explorer/make/ZZ').status_code == 404
c1 = cr[0]
form = {('s%d' % i): str(r['marks']) for i, r in enumerate(c1['rubric'])}
assert free.post('/explorer/make/C01', data=form).status_code == 302
form['s0'] = '99'
assert free.post('/explorer/make/C01', data=form, follow_redirects=True).status_code == 200
with app.app_context():
    from app.models_pulse import PulseExpCreative
    assert PulseExpCreative.query.one().total == 10
assert 'EduPulse-Explorer' in free.get('/member-home').get_data(as_text=True)
# public page
pub = anon.get('/explorer-test')
ph = pub.get_data(as_text=True)
assert pub.status_code == 200 and 'dg-alert' in ph and ph.count('class="ex-q"') == 6 and 'Six free practice questions' in ph and 'Spaced review' in ph
assert 'collegedekho' not in ph.lower() and 'whatsapp group chat' not in ph.lower()
for u in ('/grade-7-10-mock-test', '/discovery-test-grade-7-10'):
    assert anon.get(u).status_code == 301
print('explorer checks passed')
