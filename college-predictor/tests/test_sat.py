"""EduPulse-SAT: bank integrity, Math generator, composition, marking (no negative marking, typed answers), spaced-review cards, Daily Review, tracker, access, free sample and the public page.
Run from college-predictor/:  python tests/test_sat.py"""
import json
import os
import random
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
from app.data import sat_exam  # noqa: E402
from app.extensions import bcrypt, db  # noqa: E402
from app.models import PageLead, User  # noqa: E402
from app.models_pulse import PulseSatCard  # noqa: E402
from app.services import free_mock, sat, sat_gen  # noqa: E402

# ---- Reading and Writing bank ------------------------------------------------------------------------------------------------------------
bank = sat.bank()
assert len(bank) >= 190 and len({q['id'] for q in bank}) == len(bank)
for q in bank:
    assert q['sec'] == 'RW' and q['domain'] in sat.RW_DOMAINS and q['passage'].strip() and q['stem'].strip() and q['why'].strip() and q['skill'], q['id']
    assert len(q['opts']) == 4 and len(set(q['opts'])) == 4 and all(o.strip() for o in q['opts']) and 0 <= q['ans'] < 4, q['id']
    assert '�' not in json.dumps(q, ensure_ascii=False), q['id']
blob = json.dumps(bank, ensure_ascii=False).lower()
for bad in ('collegeboard', 'khan', 'whatsapp', 'www.', 'http'):
    assert bad not in blob, bad
for d in sat.RW_DOMAINS:
    assert sum(1 for q in bank if q['domain'] == d) >= 40, d
pos = [sum(1 for q in bank if q['ans'] == k) for k in range(4)]
assert min(pos) > 0.15 * len(bank), pos

# ---- Math generator ----------------------------------------------------------------------------------------------------------------------
assert set(sat_gen.BY_DOMAIN) == set(sat.MATH_DOMAINS) and all(len(v) >= 5 for v in sat_gen.BY_DOMAIN.values())
kinds = {'mcq': 0, 'spr': 0}
for fam in sat_gen.FAMILIES:
    for seed in range(1, 60):
        q = sat_gen.build(fam, seed)
        assert q == sat_gen.build(fam, seed) and q['id'] == 'g:%s:%d' % (fam, seed) and q['sec'] == 'MATH' and q['why'].strip() and q['stem'].strip(), (fam, seed)
        kinds[q['kind']] += 1
        if q['kind'] == 'mcq':
            assert len(q['opts']) == 4 and len(set(q['opts'])) == 4 and 0 <= q['ans'] < 4, (fam, seed, q['opts'])
        else:
            assert sat_gen.is_correct(q, q['ans_text']) and not sat_gen.is_correct(q, 'abc'), (fam, seed)
assert kinds['spr'] > 0.15 * sum(kinds.values()) and kinds['mcq'] > 0.4 * sum(kinds.values()), kinds
assert str(sat_gen.parse_response('3/4')) == '3/4' and sat_gen.parse_response('.5') == sat_gen.parse_response('1/2') == sat_gen.parse_response('0.50')
assert sat_gen.parse_response('') is None and sat_gen.parse_response('1/0') is None and sat_gen.parse_response('x') is None
assert sat.get('g:nope:1') is None and sat.get('rw:999') is None and sat.get(5) is None

# ---- composition -------------------------------------------------------------------------------------------------------------------------
cat = sat.catalogue()
assert {t['id'] for t in cat if t['kind'] == 'mock'} == {'M-FULL', 'M-RW', 'M-MATH'} and len([t for t in cat if t['kind'] == 'set']) == 8
app = create_app()
with app.app_context():
    db.create_all()
    t = sat.compose('M-FULL', 1, 0)
    assert len(t['qids']) == 98 and len(set(t['qids'])) == 98 and t['minutes'] == 134
    assert sum(1 for i in t['qids'] if sat.get(i)['sec'] == 'RW') == 54 and sum(1 for i in t['qids'] if sat.get(i)['sec'] == 'MATH') == 44
    for dom, n in sat.FULL_RW + sat.FULL_MATH:
        assert sum(1 for i in t['qids'] if sat.get(i)['domain'] == dom) == n, dom
    assert sat.compose('M-FULL', 1, 0)['qids'] == t['qids'] and sat.compose('M-FULL', 1, 1)['qids'] != t['qids']
    assert len(sat.compose('M-RW', 1, 0)['qids']) == 54 and sat.compose('M-RW', 1, 0)['minutes'] == 64
    assert len(sat.compose('M-MATH', 1, 0)['qids']) == 44 and sat.compose('M-MATH', 1, 0)['minutes'] == 70
    for code in sat.DOM_CODE:
        assert len(sat.compose('S-' + code, 1, 0)['qids']) == sat.SET_N, code
    assert sat.compose('nope', 1, 0) is None
    v = [sat.view(sat.get(i)) for i in t['qids']]
    assert all('ans' not in x and 'why' not in x for x in v) and any(x['spr'] for x in v)

    # ---- marking and cards ---------------------------------------------------------------------------------------------------------------
    pw = lambda: bcrypt.generate_password_hash('x').decode()  # noqa: E731
    db.session.add_all([User(name='Free', email='f@x.com', tier='free', password_hash=pw()), User(name='Prem', email='p@x.com', tier='premium', password_hash=pw())])
    db.session.commit()
    uid = User.query.filter_by(email='p@x.com').first().id
    qids = sat.compose('S-ALG', uid, 0)['qids'][:10]
    # make sure the set has both a typed-answer and a choice question
    extra = []
    rng = random.Random(4)
    while not any(sat.get(i).get('kind') == 'spr' for i in qids + extra):
        extra.append(sat_gen.pick('Algebra', rng))
    qids = (qids[:9] + extra[:1]) if extra else qids
    ans = {}
    for k, qid in enumerate(qids):
        q = sat.get(qid)
        right = q['ans_text'] if q['kind'] == 'spr' else q['ans']
        wrong = 'zzz' if q['kind'] == 'spr' else (q['ans'] + 1) % 4
        if k < 5:
            ans[qid] = {'a': right, 'c': 'H'}
        elif k < 7:
            ans[qid] = {'a': wrong, 'c': 'H'}
        elif k == 7:
            ans[qid] = {'a': right, 'c': 'G'}
        elif k == 8:
            ans[qid] = {'a': wrong, 'c': 'L'}
    rows, err = sat.grade_paper({'qids': qids, 'answers': ans})
    assert err is None and sum(1 for r in rows if r['right']) == 6 and sum(1 for r in rows if r['chosen'] is None) == 1
    assert sat.grade_paper({'qids': ['g:nope:1'], 'answers': {}})[1] and sat.grade_paper('x')[1]
    res, err = sat.save_result(uid, {'id': 'S-ALG', 'title': 'Algebra set'}, {'qids': qids, 'answers': ans, 'timed': True, 'seconds': 400})
    assert err is None and res.score == 6 and res.max_score == 10 and res.right == 6 and res.wrong == 3 and res.blank == 1 and res.sure_wrong == 2 and res.lucky == 1
    cards = {c.qkey: c for c in PulseSatCard.query.filter_by(user_id=uid).all()}
    keys = {sat.card_key(q) for q in (qids[5], qids[6], qids[7], qids[8])}
    assert set(cards) == keys, (set(cards), keys)                  # a generated question is reviewed as its family, so two of one family share a card
    assert all(cards[sat.card_key(q)].box == 0 for q in (qids[5], qids[6], qids[8]))
    assert sat.tracker(uid)['due'] >= 2
    dq = sat.daily(uid)
    assert len(dq['qids']) == sat.DAILY_N and dq['cards'] >= 2 and len(set(dq['qids'])) == sat.DAILY_N
    # a typed answer: fractions and decimals are equal, spaces are ignored
    sprq = next(sat.get(i) for i in qids if sat.get(i).get('kind') == 'spr')
    r2, _ = sat.grade_paper({'qids': [sprq['id']], 'answers': {sprq['id']: {'a': ' ' + sprq['ans_text'] + ' '}}})
    assert r2[0]['right']
    an1 = sat.analyse([res])
    assert an1['right'] == 6 and an1['wrong'] == 3 and an1['pat']['P4'] == 2 and an1['doms'][0]['dom'] in sat.MATH_DOMAINS + sat.RW_DOMAINS
    tr = sat.tracker(uid)
    assert tr['attempts'] == 1 and tr['answers'] >= 9 and set(tr['secs']) == set(sat.SEC)

# ---- access and HTTP ---------------------------------------------------------------------------------------------------------------------
def login(em):
    c = app.test_client()
    assert c.post('/login', data={'email': em, 'password': 'x'}).status_code == 302
    return c


anon, free, prem = app.test_client(), login('f@x.com'), login('p@x.com')
assert anon.get('/sat-mock/').status_code in (301, 302, 401, 403)
assert free.get('/sat-mock/').status_code in (301, 302, 403)
home = prem.get('/sat-mock/')
assert home.status_code == 200 and b'EduPulse-SAT' in home.data and b'Full practice SAT' in home.data
page = prem.get('/sat-mock/test/M-MATH')
assert page.status_code == 200 and b'"ans"' not in page.data and b'ans_text' not in page.data and b'ttData' in page.data
assert prem.get('/sat-mock/test/nope').status_code == 404
assert prem.get('/sat-mock/daily').status_code == 200

with app.app_context():
    uid = User.query.filter_by(email='p@x.com').first().id
    t = sat.compose('S-GEO', uid, 5)
    pa = {}
    for i in t['qids']:
        q = sat.get(i)
        pa[i] = {'a': q['ans_text'] if q.get('kind') == 'spr' else q['ans'], 'c': 'M'}
    payload = {'qids': t['qids'], 'answers': pa, 'timed': True, 'seconds': 600}
r = prem.post('/sat-mock/submit/S-GEO', json=payload)
j = r.get_json()
assert r.status_code == 200 and j['ok'], r.data
rep = prem.get(j['url'])
assert rep.status_code == 200 and b'15 / 15' in rep.data and b'Explanation' in rep.data and b'100%' in rep.data
assert anon.get(j['url']).status_code in (301, 302, 401, 403)
assert free.get(j['url']).status_code == 404
assert prem.post('/sat-mock/submit/S-GEO', json={'qids': ['x'], 'answers': {}}).status_code == 400
assert prem.get('/sat-mock/progress').status_code == 200

# ---- public page, free sample, tile ------------------------------------------------------------------------------------------------------
pub = anon.get('/sat-exam-guidelines')
assert pub.status_code == 200 and b'134' in pub.data and b'Free sample mock test' in pub.data and b'$68' in pub.data and b'Aadhaar PVC' in pub.data
assert pub.data.count(b'class="nf-q"') == 8
for alias in ('/sat-exam', '/sat-guidelines', '/sat-mock-test'):
    assert anon.get(alias).status_code == 301
ds = sat_exam.dates(date(2026, 11, 5))
assert [x['kind'] for x in ds] == ['closed', 'open', 'open', 'open', 'open']        # the 7 Nov test is closed on 5 Nov; later dates are open
assert sat_exam.dates(date(2026, 11, 8))[0]['kind'] == 'past' and sat_exam.dates(date(2026, 11, 21))[1]['kind'] == 'late' and sat_exam.dates(date(2026, 11, 25))[1]['kind'] == 'closed'
assert all(r[1] < r[2] < r[0] < r[3] for r in sat_exam.DATES)
s = free_mock.sample('sat')
assert len(s) == 10 and len({q['id'] for q in s}) == 10 and all(len(q['opts']) == 4 for q in s) and sum(1 for q in s if q['sec'] == 'Math') == 5
assert 'sat' in free_mock.BY_KEY and len(free_mock.EXAMS) == 8
a = anon.post('/edupulse-free-mock-tests/start', data={'email': 'sat-t@example.com', 'phone': '9876543210'})
assert a.status_code == 302 and anon.get('/edupulse-free-mock-tests/sat').status_code == 200
with app.app_context():
    PageLead.query.filter_by(email='sat-t@example.com').delete()
    db.session.commit()
from app.services import member_hub  # noqa: E402
titles = [t['title'] for cat in member_hub.CATEGORIES for t in cat['tiles']] if hasattr(member_hub, 'CATEGORIES') else []
assert not titles or 'EduPulse-SAT Practice Centre' in titles
try:
    os.remove(_db)
except OSError:
    pass
print('sat checks passed')
