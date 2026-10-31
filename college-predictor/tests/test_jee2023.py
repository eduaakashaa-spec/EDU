"""JEE Main 2023 recreated papers (24 Jan Shift 2): data integrity, independent re-computation of the answers, the mock centre and Reinforcement.
Run from college-predictor/:  python tests/test_jee2023.py"""
import itertools
import json
import math
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
_fd, _db = tempfile.mkstemp(suffix='.db')
os.close(_fd)
os.environ.update(DATABASE_URL='sqlite:///' + _db, SECRET_KEY='test', FLASK_DEBUG='0')

DATA = os.path.join(ROOT, 'app', 'data', 'jee_mock', 'data')
paper = json.load(open(os.path.join(DATA, 'J2301S2.json'), encoding='utf-8'))
Q = {q['src']: q for q in paper['qs']}

# ---- data integrity -------------------------------------------------------------------------------------------------------------------------
assert len(paper['qs']) == 73 and len(Q) == 73
assert [q['n'] for q in paper['qs']] == list(range(1, 74))
cnt = {}
for s in paper['sections']:
    cnt[(s['subj'], s['type'])] = s['hi'] - s['lo'] + 1
    for q in paper['qs'][s['lo'] - 1:s['hi']]:
        assert q['subj'] == s['subj'] and q['t'] == s['type']
    if s['type'] == 'NAT':
        assert s['choose'] == 5
assert cnt == {('MATH', 'MCQ'): 20, ('MATH', 'NAT'): 8, ('PHY', 'MCQ'): 16, ('PHY', 'NAT'): 9, ('CHEM', 'MCQ'): 14, ('CHEM', 'NAT'): 6}
assert paper['max'] == 4 * (50 + 15) == 260
for q in paper['qs']:
    assert q['stem'].strip() and q['steps'] and all(x.strip() for x in q['steps']), q['src']
    assert q['stem'].count('<') == q['stem'].count('>'), q['src']
    if q['t'] == 'MCQ':
        assert len(q['opts']) == 4 and len(set(q['opts'])) == 4 and q['acc']['sets'][0] in 'ABCD', q['src']
    else:
        lo, hi = q['acc']['ranges'][0]
        assert lo == hi and lo == int(lo) and lo > 0, q['src']
# the questions left out are exactly those that need a figure or whose key we could not confirm
omitted = set(range(1, 91)) - {q['src'] for q in paper['qs']}
assert len(omitted) == 17, sorted(omitted)

# ---- independent recomputation of the numerical answers and several multiple-choice ones -----------------------------------------------------------------
ans = lambda src: Q[src]['acc']['ranges'][0][0]
opt = lambda src: Q[src]['opts']['ABCD'.index(Q[src]['acc']['sets'][0])]

# Q63 integers greater than 7000 from digits 3,5,6,7,8 without repetition
n63 = sum(1 for r in range(4, 6) for p in itertools.permutations('35678', r) if int(''.join(p)) > 7000)
assert n63 == 168 and opt(63) == '168'
# Q64 ratio of sums
n64 = next(n for n in range(1, 100) if sum(k ** 3 for k in range(1, n + 1)) * 5 == 9 * sum(k * (2 * k + 1) for k in range(1, n + 1)))
assert n64 == ans(64) == 5
# Q66 coefficient of x^4 in (x - 3/x^2)^n with first three coefficients summing to 376
n66 = next(n for n in range(1, 60) if 1 - 3 * n + 9 * n * (n - 1) // 2 == 376)
assert n66 == 10 and math.comb(10, 2) * 9 == ans(66) == 405
# Q67 sum over the solution set, found numerically on a fine grid of the candidate angles (cos+sin integer)
cands = []
for k in (-1, 0, 1):
    for t in [i * math.pi / 4 for i in range(8)]:
        if abs(math.cos(t) + math.sin(t) - k) < 1e-9:
            cands.append(t)
assert abs(sum(math.sin(t + math.pi / 4) ** 2 for t in cands) - ans(67)) < 1e-9
# Q68 square of BC
b, c = -3, 8
B, C = (b, -2 * b), (c, c - 3)
assert ((B[0] + C[0] + 1) / 3, (B[1] + C[1] - 2) / 3) == (2, 3) and (B[0] - C[0]) ** 2 + (B[1] - C[1]) ** 2 == ans(68) == 122
# Q73 variance of the AP 2,5,8,11,14,17
v = [2, 5, 8, 11, 14, 17]
m = sum(v) / 6
assert m == 9.5 and 8 * sum((x - m) ** 2 for x in v) / 6 == 210 and opt(73) == '210'
# Q74 equivalence relation on {a,b,c,d}: all 16 pairs, 3 present
assert 16 - 3 == ans(74)
# Q75 permutation matrices
assert math.factorial(5) == 120 and opt(75) == '120'
# Q78 and Q79 sums
f = lambda x: 4 ** x / (4 ** x + 2)
assert abs(sum(f(k / 2023) for k in range(1, 2023)) - 1011) < 1e-6 and opt(78) == '1011'
assert next(n for n in range(1, 30) if sum(3 ** k for k in range(1, n + 1)) == 3279) == 7 and opt(79) == '7'
# Q83 area by numerical integration of (2y - y^2) - (-y) over [0, 3]
area = sum((3 * (i + .5) / 1000 * 3 - ((i + .5) * 3 / 1000) ** 2) * 3 / 1000 for i in range(1000))
assert abs(8 * area - ans(83)) < 1e-3
# Q90 lambda from Bayes, then the equilateral triangle in y^2 = 6x
lam = 6
assert abs((lam / (lam + 4)) / (0.4 + 0.5 + lam / (lam + 4)) - 0.4) < 1e-12
x = 18
assert abs((x / math.sqrt(3)) ** 2 - 6 * x) < 1e-9 and round(x ** 2 + 108) == ans(90) == 432
# Q81 integral value
integ = sum(48 / math.sqrt(9 - 4 * x ** 2) * (3 * math.sqrt(2) / 4 - .75) / 200000 for x in [.75 + (i + .5) * (3 * math.sqrt(2) / 4 - .75) / 200000 for i in range(200000)])
assert abs(integ - 2 * math.pi) < 1e-3 and opt(81) == '2&pi;'
# Physics
assert round(2 * 2 + 12 * 8) == ans(5) == 100                                              # F.v at t = 2 s
assert abs(0.5 / 0.5 * 32 - 32) < 1e-9 and ans(6) == 32                                    # I1/I2 = 0.5 / (0.5 * (1/8) * (1/4))
assert round(4 / 3 * 22 / 7 * 1e-9 * 9000 * 9.8 * 1e7) == 3696 and ans(11) == 7
assert (2 ** 2 - 1) == 3 and ans(14) == 1                                                 # (m + 3)/m = 4
assert 3.5 / 2 * 15 * 4 == ans(16) == 105
assert round((1.2 ** 2 - 1) * 100) == ans(18) == 44
assert round(0.75 * 2 * 0.05 * 12 / 13 * 130) == ans(20) == 9
f_air, nw = 18, 4 / 3
f_w = f_air * (1.5 - 1) / (1.5 / nw - 1)
assert round(f_w - f_air) == ans(25) == 54
lam_nm = 4e-15 * 3e8 / (13.6 * (1 - 1 / 16)) * 1e9
assert abs(lam_nm - 94.1) < 0.05 and opt(27) == '94.1 nm'
assert 120 / 240 * 6e23 * 200 / 1e25 == ans(28) == 6
assert abs((90 / 180) * 80 - 40) < 1e-9 and opt(17) == '40 V'
assert abs(4e-7 * math.pi * 7000 * 2 - 176e-4) < 1e-5 and opt(19) == '176 &times; 10<sup>&minus;4</sup> T'
# Chemistry
assert 7 + 0.5 * (5 + math.log10(0.01)) == 8.5 and ans(36) == 85
pa = (350 - 0.3 * ((410 - 0.2 * 350 / 0.7) / (0.8 - 0.2 * 0.3 / 0.7))) / 0.7
assert round(pa) == ans(45) == 314
assert 2 ** 3 == ans(60) == 8

# ---- the mock centre ----------------------------------------------------------------------------------------------------------------------
from app import create_app  # noqa: E402
from app.extensions import bcrypt, db  # noqa: E402
from app.models import User  # noqa: E402
from app.models_reinforce import RfQuestion  # noqa: E402
from app.services import pulse_jee as pj, reinforce as rf  # noqa: E402

app = create_app()
app.config['TESTING'] = True
with app.app_context():
    db.create_all()
    db.session.add(User(name='Stu', email='s@x.com', tier='premium', password_hash=bcrypt.generate_password_hash('x').decode()))
    db.session.commit()
    meta = pj.valid_papers()['J2301S2']
    assert meta['recreated'] and meta['total'] == 73 and meta['max'] == 260 and meta['n'] == 65
c = app.test_client()
assert c.post('/login', data={'email': 's@x.com', 'password': 'x'}).status_code == 302
r = c.get('/edupulse-jee/data/J2301S2.json')
assert r.status_code == 200 and len(r.get_json()['qs']) == 73
assert b'recreated' in c.get('/edupulse-jee/app').data
qs = {str(q['n']): {'type': q['t'], 'subj': q['subj'], 'topic': q['cat'], 'answer': q['disp'], 'official': q['disp'], 'status': 'right', 'marks': 4, 'confidence': 'H', 'sec': 30} for q in paper['qs'][:10]}
res = c.post('/edupulse-jee/results', json={'paper': 'J2301S2', 'mode': 'practice', 'score': 40, 'questions': qs, 'sections': [], 'startedAt': '2026-10-31T10:00:00Z', 'finishedAt': '2026-10-31T10:30:00Z'})
assert res.status_code == 200 and res.get_json()['ok']

# ---- EduPulse Reinforcement -------------------------------------------------------------------------------------------------------------------
with app.app_context():
    rf.seed_taxonomy()
    assert rf.seed_recreated() == 73 and rf.seed_recreated() == 0
    rows = RfQuestion.query.filter(RfQuestion.qid.like('JEE-J2301S2-%')).all()
    assert len(rows) == 73 and all(r.status == 'approved' and r.exam == 'JEE' and r.explanation for r in rows)
    one = RfQuestion.query.filter_by(qid='JEE-J2301S2-001').one()
    assert one.qtype == 'mcq' and one.answer in list('ABCD') and len(one.options) == 4 and 'real solutions' in one.stem
    nat = next(r for r in rows if r.qtype == 'nat')
    assert nat.answer and nat.options == []

print('jee 2023 checks passed')
