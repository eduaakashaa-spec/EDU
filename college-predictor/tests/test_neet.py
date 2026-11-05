"""EduPulse-NEET: bank integrity, composition, marking (+4 / -1), spaced-review cards, Daily Review, tracker, access, free sample and the public page.
Run from college-predictor/:  python tests/test_neet.py"""
import json
import os
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
from app.data import neet_exam  # noqa: E402
from app.extensions import bcrypt, db  # noqa: E402
from app.models import PageLead, User  # noqa: E402
from app.models_pulse import PulseNeetCard, PulseNeetResult  # noqa: E402
from app.services import free_mock, neet  # noqa: E402

# ---- bank --------------------------------------------------------------------------------------------------------------------------------
bank = neet.bank()
assert len(bank) >= 1400 and len({q['id'] for q in bank}) == len(bank)
for q in bank:
    assert q['sec'] in neet.SEC and q['q'].strip() and q['why'] and q['topic'], q['id']
    assert len(q['opts']) == 4 and all(o.strip() for o in q['opts']) and len(set(q['opts'])) == 4 and 0 <= q['ans'] < 4, q['id']
    assert q['src'] and all(len(s) == 2 and 2018 <= s[0] <= 2026 for s in q['src']), q['id']
    assert '�' not in json.dumps(q, ensure_ascii=False), q['id']
blob = json.dumps(bank, ensure_ascii=False).lower()
for bad in ('prepp', 'collegedekho', 'careers360', 'collegedunia', 'shiksha', 'getmyuni', 'toprankers', 'whatsapp', 'www.', 'http'):
    assert bad not in blob, bad
secs = {s: sum(1 for q in bank if q['sec'] == s) for s in neet.SEC}
assert all(n >= 250 for n in secs.values()), secs
pos = [sum(1 for q in bank if q['ans'] == k) for k in range(4)]
assert min(pos) > 0.15 * len(bank), pos
years = {y for q in bank for y, _ in q['src']}
assert years == set(range(2018, 2027)), years
assert {y['year'] for y in neet.year_papers()} == years

an = neet.analysis()
assert an['questions'] == len(bank) and set(an['years']) == {str(y) for y in years}
for y, v in an['years'].items():
    assert v['paper_questions'] in (180, 200) and 100 <= v['kept'] <= v['paper_questions'], (y, v)
    assert v['kept'] == sum(v['by_sec'].values()) or v['kept'] >= sum(v['by_sec'].values()) - 2, y

assert an['years']['2026']['key'] == 'provisional' and all(v['key'] == 'final' for y, v in an['years'].items() if y != '2026')   # only the 2026 key is provisional
assert an['years']['2026']['paper_questions'] == 180 and an['years']['2026']['kept'] >= 140

# ---- composition -------------------------------------------------------------------------------------------------------------------------
cat = neet.catalogue()
assert {t['id'] for t in cat if t['kind'] == 'mock'} == {'M-FULL', 'M-PC', 'M-BIO'}
full = [t for t in cat if t['id'] == 'M-FULL'][0]
assert full['count'] == 180 and full['minutes'] == 180
app = create_app()
with app.app_context():
    db.create_all()
    t = neet.compose('M-FULL', 1, 0)
    assert len(t['qids']) == 180 and len(set(t['qids'])) == 180 and t['minutes'] == 180
    for sec in neet.SEC:
        assert sum(1 for i in t['qids'] if neet.get(i)['sec'] == sec) == 45, sec
    assert neet.compose('M-FULL', 1, 0)['qids'] == t['qids'] and neet.compose('M-FULL', 1, 1)['qids'] != t['qids']
    assert len(neet.compose('M-PC', 1, 0)['qids']) == 90 and len(neet.compose('S-PHY', 1, 0)['qids']) == 20
    yp = neet.compose('Y-2022', 1, 0)
    assert len(yp['qids']) >= 100
    ns = [next(n for y, n in neet.get(i)['src'] if y == 2022) for i in yp['qids']]
    assert ns == sorted(ns)
    assert neet.compose('nope', 1, 0) is None

    # ---- marking and cards ---------------------------------------------------------------------------------------------------------------
    pw = lambda: bcrypt.generate_password_hash('x').decode()  # noqa: E731
    db.session.add_all([User(name='Free', email='f@x.com', tier='free', password_hash=pw()), User(name='Prem', email='p@x.com', tier='premium', password_hash=pw())])
    db.session.commit()
    uid = User.query.filter_by(email='p@x.com').first().id
    qids = neet.compose('S-BOT', uid, 0)['qids'][:10]
    ans = {}
    for k, qid in enumerate(qids):
        q = neet.get(qid)
        if k < 5:
            ans[qid] = {'a': q['ans'], 'c': 'H'}                       # right, sure
        elif k < 7:
            ans[qid] = {'a': (q['ans'] + 1) % 4, 'c': 'H'}             # wrong, sure
        elif k == 7:
            ans[qid] = {'a': q['ans'], 'c': 'G'}                       # right but a guess
        elif k == 8:
            ans[qid] = {'a': (q['ans'] + 2) % 4, 'c': 'L'}             # wrong, unsure
    rows, err = neet.grade_paper({'qids': qids, 'answers': ans})
    assert err is None and neet.marks_of(rows) == 4 * 6 - 3, neet.marks_of(rows)
    assert neet.grade_paper({'qids': ['N9999'], 'answers': {}})[1] and neet.grade_paper('x')[1]
    res, err = neet.save_result(uid, {'id': 'S-BOT', 'title': 'Botany set'}, {'qids': qids, 'answers': ans, 'timed': True, 'seconds': 400})
    assert err is None and res.score == 21 and res.max_score == 40 and res.right == 6 and res.wrong == 3 and res.blank == 1
    assert res.sure_wrong == 2 and res.lucky == 1
    cards = {c.qkey: c for c in PulseNeetCard.query.filter_by(user_id=uid).all()}
    assert len(cards) == 4 and all(cards[q].box == 0 for q in (qids[5], qids[6], qids[8])) and cards[qids[7]].box >= 1
    assert neet.tracker(uid)['due'] >= 3
    dq = neet.daily(uid)
    assert len(dq['qids']) == neet.DAILY_N and dq['cards'] >= 3 and qids[5] in dq['qids']
    # a right, confident answer on a card moves it up
    q5 = neet.get(qids[5])
    neet.save_result(uid, {'id': 'DAILY', 'title': 'Daily Review'}, {'qids': [qids[5]], 'answers': {qids[5]: {'a': q5['ans'], 'c': 'H'}}})
    assert PulseNeetCard.query.filter_by(user_id=uid, qkey=qids[5]).first().box == 1
    an1 = neet.analyse([res])
    assert an1['right'] == 6 and an1['wrong'] == 3 and an1['pat']['P4'] == 2
    tr = neet.tracker(uid)
    assert tr['attempts'] == 2 and tr['answers'] >= 10 and set(tr['secs']) == set(neet.SEC)

# ---- access and HTTP ---------------------------------------------------------------------------------------------------------------------
def login(em):
    c = app.test_client()
    assert c.post('/login', data={'email': em, 'password': 'x'}).status_code == 302
    return c


anon, free, prem = app.test_client(), login('f@x.com'), login('p@x.com')
assert anon.get('/neet-mock/').status_code in (301, 302, 401, 403)
assert free.get('/neet-mock/').status_code in (301, 302, 403)
home = prem.get('/neet-mock/')
assert home.status_code == 200 and b'EduPulse-NEET' in home.data and b'NEET full mock' in home.data
page = prem.get('/neet-mock/test/M-BIO')
assert page.status_code == 200 and b'"ans"' not in page.data and b'ttData' in page.data
assert prem.get('/neet-mock/test/nope').status_code == 404
assert prem.get('/neet-mock/daily').status_code == 200

with app.app_context():
    uid = User.query.filter_by(email='p@x.com').first().id
    t = neet.compose('S-PHY', uid, 5)
    payload = {'qids': t['qids'], 'answers': {i: {'a': neet.get(i)['ans'], 'c': 'M'} for i in t['qids']}, 'timed': True, 'seconds': 600}
r = prem.post('/neet-mock/submit/S-PHY', json=payload)
j = r.get_json()
assert r.status_code == 200 and j['ok'], r.data
rep = prem.get(j['url'])
assert rep.status_code == 200 and b'80 / 80' in rep.data and b'Why' in rep.data
assert anon.get(j['url']).status_code in (301, 302, 401, 403)
assert free.get(j['url']).status_code == 404
assert prem.post('/neet-mock/submit/S-PHY', json={'qids': ['x'], 'answers': {}}).status_code == 400
assert prem.get('/neet-mock/progress').status_code == 200

# ---- public page, free sample, tile ------------------------------------------------------------------------------------------------------
pub = anon.get('/neet-papers-analysis')
assert pub.status_code == 200 and b'NEET' in pub.data and b'Free sample mock test' in pub.data
assert pub.data.count(b'class="nf-q"') == 6
for alias in ('/neet-previous-papers', '/neet-mock-test', '/neet-question-papers'):
    assert anon.get(alias).status_code == 301
ctx = neet_exam.context()
assert len(ctx['samples']) == 6 and all(len(s['opts']) == 4 for s in ctx['samples'])
s = free_mock.sample('neet')
assert len(s) == 10 and len({q['id'] for q in s}) == 10 and all(len(q['opts']) == 4 for q in s)
assert 'neet' in free_mock.BY_KEY and len(free_mock.EXAMS) == 8
a = anon.post('/edupulse-free-mock-tests/start', data={'email': 'neet-t@example.com', 'phone': '9876543210'})
assert a.status_code == 302 and anon.get('/edupulse-free-mock-tests/neet').status_code == 200
with app.app_context():
    PageLead.query.filter_by(email='neet-t@example.com').delete()
    db.session.commit()
from app.services import member_hub  # noqa: E402
titles = [t['title'] for cat in member_hub.CATEGORIES for t in cat['tiles']] if hasattr(member_hub, 'CATEGORIES') else []
assert b'provisional key' in pub.data and b'Is the 2026 answer key final?' in pub.data
with app.app_context():
    y26 = neet.compose('Y-2026', 1, 0)
    assert len(y26['qids']) >= 140 and all(any(y == 2026 for y, _ in neet.get(i)['src']) for i in y26['qids'])
assert not titles or 'EduPulse-NEET Mock Test Centre' in titles
try:
    os.remove(_db)
except OSError:
    pass
print('neet checks passed')
