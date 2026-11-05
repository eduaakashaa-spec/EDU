"""EduPulse-Olympiad: bank integrity, composition, marking (+3 / -1 multiple choice, +3 integer answers), spaced-review cards, Daily Review, tracker, access, free sample and the public guide.
Run from college-predictor/:  python tests/test_olympiad.py"""
import json
import os
import sys
import tempfile
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
_fd, _db = tempfile.mkstemp(suffix='.db')
os.close(_fd)
os.environ.update(DATABASE_URL='sqlite:///' + _db, SECRET_KEY='test', FLASK_DEBUG='0')

from app import create_app  # noqa: E402
from app.data import olympiad_exam  # noqa: E402
from app.extensions import bcrypt, db  # noqa: E402
from app.models import PageLead, User  # noqa: E402
from app.models_pulse import PulseOlyCard  # noqa: E402
from app.services import free_mock, olympiad  # noqa: E402

# ---- bank --------------------------------------------------------------------------------------------------------------------------------
bank = olympiad.bank()
assert len(bank) >= 500 and len({q['id'] for q in bank}) == len(bank)
for q in bank:
    assert q['sec'] in olympiad.SEC and q['q'].strip() and q['why'].strip() and q['kind'] in ('mcq', 'int'), q['id']
    if q['kind'] == 'mcq':
        assert len(q['opts']) == 4 and len(set(q['opts'])) == 4 and all(o.strip() for o in q['opts']) and 0 <= q['ans'] <= 3, q['id']
    else:
        assert isinstance(q['ans'], int) and 0 <= q['ans'] <= 999 and q['sec'] == 'MATH', q['id']
    assert q['src'] is None or (len(q['src']) == 3 and 2009 <= q['src'][1] <= 2026), q['id']
    assert '�' not in json.dumps(q, ensure_ascii=False), q['id']
blob = json.dumps(bank, ensure_ascii=False).lower()
for bad in ('prepp', 'careers360', 'collegedunia', 'shiksha', 'whatsapp', 'www.', 'http'):
    assert bad not in blob, bad
counts = {s: sum(1 for q in bank if q['sec'] == s) for s in olympiad.SEC}
assert all(n >= 60 for n in counts.values()), counts
assert any(q['src'] for q in bank) and any(not q['src'] for q in bank)
pos = [sum(1 for q in bank if q['kind'] == 'mcq' and q['ans'] == k) for k in range(4)]
assert min(pos) > 0.15 * sum(pos), pos
assert olympiad.secs_available() == list(olympiad.SEC)

# ---- composition -------------------------------------------------------------------------------------------------------------------------
cat = olympiad.catalogue()
mocks = {t['id']: t for t in cat if t['kind'] == 'mock'}
assert set(mocks) == {'M-' + s for s in olympiad.SEC} and mocks['M-MATH']['count'] == 30 and mocks['M-MATH']['minutes'] == 180 and mocks['M-PHY']['minutes'] == 60
papers = [t for t in cat if t['kind'] == 'paper']
assert any(p['id'] == 'P-IOQM-2024' and p['count'] == 30 for p in papers)
app = create_app()
with app.app_context():
    db.create_all()
    t = olympiad.compose('M-CHEM', 1, 0)
    assert len(t['qids']) == 30 and len(set(t['qids'])) == 30 and all(olympiad.get(i)['sec'] == 'CHEM' for i in t['qids'])
    assert olympiad.compose('M-CHEM', 1, 0)['qids'] == t['qids'] and olympiad.compose('M-CHEM', 1, 1)['qids'] != t['qids']
    assert len(olympiad.compose('S-PHY', 1, 0)['qids']) == 15
    p = olympiad.compose('P-IOQM-2024', 1, 0)
    ns = [olympiad.get(i)['src'][2] for i in p['qids']]
    assert ns == sorted(ns) and len(ns) == 30
    assert olympiad.compose('nope', 1, 0) is None
    assert all('ans' not in v and 'why' not in v for v in olympiad.paper_for_browser(t['qids']))
    assert all(v['spr'] for v in olympiad.paper_for_browser(p['qids']))

    # ---- marking and cards ---------------------------------------------------------------------------------------------------------------
    pw = lambda: bcrypt.generate_password_hash('x').decode()  # noqa: E731
    db.session.add_all([User(name='Free', email='f@x.com', tier='free', password_hash=pw()), User(name='Prem', email='p@x.com', tier='premium', password_hash=pw())])
    db.session.commit()
    uid = User.query.filter_by(email='p@x.com').first().id
    qids = olympiad.compose('S-PHY', uid, 0)['qids'][:10]
    ans = {}
    for k, qid in enumerate(qids):
        q = olympiad.get(qid)
        if k < 5:
            ans[qid] = {'a': q['ans'], 'c': 'H'}
        elif k < 7:
            ans[qid] = {'a': (q['ans'] + 1) % 4, 'c': 'H'}
        elif k == 7:
            ans[qid] = {'a': q['ans'], 'c': 'G'}
        elif k == 8:
            ans[qid] = {'a': (q['ans'] + 2) % 4, 'c': 'L'}
    rows, err = olympiad.grade_paper({'qids': qids, 'answers': ans})
    assert err is None and olympiad.marks_of(rows) == 3 * 6 - 3, olympiad.marks_of(rows)
    assert olympiad.grade_paper({'qids': ['oly:9999'], 'answers': {}})[1] and olympiad.grade_paper('x')[1]
    res, err = olympiad.save_result(uid, {'id': 'S-PHY', 'title': 'Physics set'}, {'qids': qids, 'answers': ans, 'timed': True, 'seconds': 400})
    assert err is None and res.score == 15 and res.max_score == 30 and res.right == 6 and res.wrong == 3 and res.blank == 1 and res.sure_wrong == 2 and res.lucky == 1
    cards = {c.qkey: c for c in PulseOlyCard.query.filter_by(user_id=uid).all()}
    assert len(cards) == 4 and all(cards[q].box == 0 for q in (qids[5], qids[6], qids[8])) and cards[qids[7]].box >= 1
    dq = olympiad.daily(uid)
    assert len(dq['qids']) == olympiad.DAILY_N and dq['cards'] >= 3 and qids[5] in dq['qids']
    q5 = olympiad.get(qids[5])
    olympiad.save_result(uid, {'id': 'DAILY', 'title': 'Daily Review'}, {'qids': [qids[5]], 'answers': {qids[5]: {'a': q5['ans'], 'c': 'H'}}})
    assert PulseOlyCard.query.filter_by(user_id=uid, qkey=qids[5]).first().box == 1

    # integer answers: no negative marking, leading zeros and spaces accepted, junk ignored
    mq = [i for i in olympiad.compose('S-MATH', uid, 0)['qids']][:4]
    right = int(olympiad.get(mq[0])['ans'])
    typed = (' 0%d ' % right) if right < 10 else str(right)
    wrong3 = (int(olympiad.get(mq[3])['ans']) + 1) % 1000
    rows, err = olympiad.grade_paper({'qids': mq, 'answers': {mq[0]: {'a': typed}, mq[1]: {'a': '-5'}, mq[2]: {'a': 'abc'}, mq[3]: {'a': wrong3}}})
    assert err is None and rows[0]['right'] and olympiad.marks_of(rows) == 3 and rows[2]['chosen'] is None and not rows[3]['right']
    an1 = olympiad.analyse([res])
    assert an1['right'] == 6 and an1['wrong'] == 3 and an1['pat']['P4'] == 2
    tr = olympiad.tracker(uid)
    assert tr['attempts'] == 2 and set(tr['secs']) == set(olympiad.SEC) and tr['due'] >= 2


# ---- access and HTTP ---------------------------------------------------------------------------------------------------------------------
def login(em):
    c = app.test_client()
    assert c.post('/login', data={'email': em, 'password': 'x'}).status_code == 302
    return c


anon, free, prem = app.test_client(), login('f@x.com'), login('p@x.com')
assert anon.get('/olympiad-mock/').status_code in (301, 302, 401, 403)
assert free.get('/olympiad-mock/').status_code in (301, 302, 403)
home = prem.get('/olympiad-mock/')
assert home.status_code == 200 and b'EduPulse-Olympiad' in home.data and b'Mathematics full mock' in home.data and b'IOQM 2024' in home.data
page = prem.get('/olympiad-mock/test/M-MATH')
assert page.status_code == 200 and b'"ans"' not in page.data and b'ttData' in page.data
assert prem.get('/olympiad-mock/test/nope').status_code == 404
assert prem.get('/olympiad-mock/daily').status_code == 200
assert prem.get('/olympiad-mock/test/P-IOQM-2024').status_code == 200

with app.app_context():
    uid = User.query.filter_by(email='p@x.com').first().id
    t = olympiad.compose('S-CHEM', uid, 5)
    payload = {'qids': t['qids'], 'answers': {i: {'a': olympiad.get(i)['ans'], 'c': 'M'} for i in t['qids']}, 'timed': True, 'seconds': 600}
    pt = olympiad.compose('P-IOQM-2024', uid, 0)
    ppay = {'qids': pt['qids'], 'answers': {i: {'a': olympiad.get(i)['ans'], 'c': 'M'} for i in pt['qids']}, 'timed': True, 'seconds': 900}
r = prem.post('/olympiad-mock/submit/S-CHEM', json=payload)
j = r.get_json()
assert r.status_code == 200 and j['ok'], r.data
rep = prem.get(j['url'])
assert rep.status_code == 200 and b'45 / 45' in rep.data and b'Explanation' in rep.data
assert anon.get(j['url']).status_code in (301, 302, 401, 403) and free.get(j['url']).status_code == 404
j2 = prem.post('/olympiad-mock/submit/P-IOQM-2024', json=ppay).get_json()
rep2 = prem.get(j2['url'])
assert j2['ok'] and b'90 / 90' in rep2.data and b'Correct answer' in rep2.data
assert prem.post('/olympiad-mock/submit/S-CHEM', json={'qids': ['x'], 'answers': {}}).status_code == 400
assert prem.get('/olympiad-mock/progress').status_code == 200

# ---- public page, free sample, tile ------------------------------------------------------------------------------------------------------
pub = anon.get('/olympiad-exam-guide')
assert pub.status_code == 200 and b'HBCSE' in pub.data and b'Free sample mock test' in pub.data and b'Not confirmed' in pub.data
assert pub.data.count(b'class="nf-q"') == 6
for alias in ('/olympiad-exams', '/olympiads', '/olympiad-mock-test'):
    assert anon.get(alias).status_code == 301
tl = olympiad_exam.timeline(date(2026, 11, 5))
kinds = {r['label']: r['kind'] for r in tl}
assert kinds['IOQM 2026 (maths, stage 1)'] == 'past' and kinds['RMO 2026 (maths, stage 2)'] == 'soon' and kinds['INMO 2027 (maths, stage 3)'] == 'later'
assert [r['start'] for r in tl] == sorted(r['start'] for r in tl)
s = free_mock.sample('olympiad')
assert len(s) == 10 and len({q['id'] for q in s}) == 10 and all(len(q['opts']) == 4 for q in s)
assert 'olympiad' in free_mock.BY_KEY and len(free_mock.EXAMS) == 9
a = anon.post('/edupulse-free-mock-tests/start', data={'email': 'oly-t@example.com', 'phone': '9876543210'})
assert a.status_code == 302 and anon.get('/edupulse-free-mock-tests/olympiad').status_code == 200
with app.app_context():
    PageLead.query.filter_by(email='oly-t@example.com').delete()
    db.session.commit()
from app.data.mentorship_addons import ADDONS  # noqa: E402
assert {'olympiad-jr', 'olympiad-sr'} <= {a['key'] for a in ADDONS}
from app.services import member_hub  # noqa: E402
titles = [t['title'] for cat in member_hub.CATEGORIES for t in cat['tiles']] if hasattr(member_hub, 'CATEGORIES') else []
assert not titles or {'EduPulse-Olympiad Practice Centre', 'Olympiad foundation mentorship', 'Olympiad senior mentorship'} <= set(titles)
try:
    os.remove(_db)
except OSError:
    pass
print('olympiad checks passed')
