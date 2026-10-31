"""EduPulse-JEE Mock Test Centre: question-bank integrity, answer verification, members-only serving, saving, negative-marking/confidence analysis,
reports, mentor access and the previous-year answer-key tooling.
Run from college-predictor/:  python tests/test_jee_mock.py"""
import csv
import itertools
import json
import math
import os
import random
import sys
import tempfile
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, 'tools', 'jee_mock'))
_fd, _db = tempfile.mkstemp(suffix='.db')
os.close(_fd)
os.environ.update(DATABASE_URL='sqlite:///' + _db, SECRET_KEY='test', FLASK_DEBUG='0')

DATA = os.path.join(ROOT, 'app', 'data', 'jee_mock', 'data')

# ---- the shipped mocks -----------------------------------------------------------------------------------------------------------------
stems = Counter()
for i in range(1, 6):
    d = json.load(open(os.path.join(DATA, 'M%d.json' % i), encoding='utf-8'))
    assert d['mins'] == 180 and d['max'] == 300 and len(d['qs']) == 75
    assert [(s['subj'], s['type'], s['lo'], s['hi']) for s in d['sections']] == [('MATH', 'MCQ', 1, 20), ('MATH', 'NAT', 21, 25), ('PHY', 'MCQ', 26, 45), ('PHY', 'NAT', 46, 50), ('CHEM', 'MCQ', 51, 70), ('CHEM', 'NAT', 71, 75)]
    assert all(s['right'] == 4 and s['wrong'] == -1 for s in d['sections'])                           # negative marking in both sections
    for q in d['qs']:
        stems[q['stem']] += 1
        assert q['steps'] and q['cat'] and q['subj'] in ('MATH', 'PHY', 'CHEM')
        if q['t'] == 'MCQ':
            assert len(q['opts']) == 4 and len(set(q['opts'])) == 4, (i, q['n'], q['opts'])
            assert q['disp'] in 'ABCD' and q['acc'] == {'sets': [q['disp']]}
        else:
            v = float(q['disp'])
            assert v == int(v) and v >= 0 and q['acc']['ranges'] == [[v, v]]
assert max(stems.values()) == 1, 'a question repeats across the mocks'

# ---- generator: every template, many seeds; answers independently re-checked for a sample ------------------------------------------------
import kit, math_t, phys_t, chem_t  # noqa: E402
for subj in kit.REG:
    for e in kit.REG[subj]:
        for want in ([False, True] if e['nat'] else [False]):
            for s in range(25):
                q = kit.build_question(e, random.Random(s * 13 + 5), want)
                assert q['steps'] and q['stem']
                if want:
                    assert isinstance(q['ans'], int) and q['ans'] >= 0
                else:
                    assert len(set(q['opts'])) == 4 and 0 <= q['ans'] < 4
assert len(kit.REG['MATH']) >= 30 and len(kit.REG['PHY']) >= 25 and len(kit.REG['CHEM']) >= 25

det_entry = next(e for e in kit.REG['MATH'] if e['name'] == 'det3')
for s in range(40):
    it = det_entry['fn'](random.Random(s))
    # parse the matrix back out of the stem and recompute the determinant by the permutation (Leibniz) formula
    import re as _re
    rows = [[int(x.replace('−', '-')) for x in part.split()] for part in _re.findall(r'\[([^\]]+)\]', it.stem)]
    leib = sum(math.prod(rows[i][p[i]] for i in range(3)) * (1 if sum(1 for a in range(3) for b in range(a + 1, 3) if p[a] > p[b]) % 2 == 0 else -1) for p in itertools.permutations(range(3)))
    assert leib == it.ans, (rows, leib, it.ans)
w_entry = next(e for e in kit.REG['MATH'] if e['name'] == 'word_arrangements')
for s in range(30):
    it = w_entry['fn'](random.Random(s))
    word = it.stem.split('word ')[1]
    if len(word) <= 7:
        assert len(set(itertools.permutations(word))) == it.ans, (word, it.ans)
cp_entry = next(e for e in kit.REG['MATH'] if e['name'] == 'cond_prob_dice')
for s in range(20):
    it = cp_entry['fn'](random.Random(s))
    sm_, k_ = [int(x) for x in __import__('re').findall(r'sum is (\d+) given that at least one die shows (\d+)', it.stem)[0]]
    both = sum(1 for i in range(1, 7) for j in range(1, 7) if (i == k_ or j == k_) and i + j == sm_)
    given = sum(1 for i in range(1, 7) for j in range(1, 7) if i == k_ or j == k_)
    assert it.ans == (str(both // math.gcd(both, given)) + '/' + str(given // math.gcd(both, given)) if given // math.gcd(both, given) != 1 else str(both // given)), (it.ans, both, given)

# ---- previous-year answer-key tooling ---------------------------------------------------------------------------------------------------
import apply_key  # noqa: E402
tmp = tempfile.mkdtemp()
paper = {'year': 'PX', 'qs': [{'n': 1, 't': 'MCQ', 'oids': ['11', '12', '13', '14'], 'qid': '900'}, {'n': 2, 't': 'MCQ', 'oids': ['21', '22', '23', '24'], 'qid': '901'},
                              {'n': 3, 't': 'NAT', 'qid': '902'}, {'n': 4, 't': 'MCQ', 'oids': ['41', '42', '43', '44'], 'qid': '903'}]}
pp = os.path.join(tmp, 'PX.json')
json.dump(paper, open(pp, 'w'))
kp = os.path.join(tmp, 'k.csv')
with open(kp, 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['qid', 'answer'])
    w.writerows([['900', '13'], ['901', 'B|C'], ['902', '12'], ['903', 'BONUS']])
apply_key.main(pp, kp)
got = json.load(open(pp))
assert got['qs'][0]['acc'] == {'sets': ['C']} and got['qs'][1]['acc'] == {'sets': ['B', 'C']} and got['qs'][2]['acc'] == {'ranges': [[12.0, 12.0]]} and got['qs'][3]['acc'] == {'bonus': True} and got['key'] == 'applied'
with open(kp, 'w', newline='') as f:
    csv.writer(f).writerows([['qid', 'answer'], ['900', 'A']])
try:
    apply_key.main(pp, kp)
    raise AssertionError('a partial key must be refused')
except SystemExit as e:
    assert 'No key for questions' in str(e)

# ---- the web portal -----------------------------------------------------------------------------------------------------------------------
from app import create_app  # noqa: E402
from app.extensions import bcrypt, db  # noqa: E402
from app.models import User  # noqa: E402
from app.models_pulse import PulseJeeResult, PulseProfile  # noqa: E402
from app.services import pulse_jee as pj  # noqa: E402

app = create_app()
app.config['TESTING'] = True
pw = lambda: bcrypt.generate_password_hash('x').decode()
with app.app_context():
    db.create_all()
    for n_, e, t in (('Admin', 'a@x.com', 'admin'), ('Mentor', 'm@x.com', 'ea_mentor'), ('Other Mentor', 'm2@x.com', 'ea_mentor'), ('Stu One', 's1@x.com', 'premium'), ('Stu Two', 's2@x.com', 'premium'), ('Free Kid', 'f@x.com', 'free')):
        db.session.add(User(name=n_, email=e, tier=t, password_hash=pw()))
    db.session.commit()
    S1 = User.query.filter_by(email='s1@x.com').one().id


def login(email):
    c = app.test_client()
    assert c.post('/login', data={'email': email, 'password': 'x'}).status_code == 302
    return c


admin, mentor, mentor2, s1, s2, free = (login(x) for x in ('a@x.com', 'm@x.com', 'm2@x.com', 's1@x.com', 's2@x.com', 'f@x.com'))
anon = app.test_client()
B = '/edupulse-jee'
for u in (B + '/', B + '/app', B + '/data/M1.json', B + '/data/index.json'):
    assert anon.get(u).status_code in (302, 401, 403), u
    r = free.get(u)
    assert r.status_code != 200 or b'JEE Main' not in r.data, u                      # a free account gets neither the centre nor the papers
assert s1.get(B + '/data/M1.json').status_code == 200 and s1.get(B + '/data/index.json').status_code == 200
idx = s1.get(B + '/data/index.json').get_json()['papers']
assert [p['y'] for p in idx if p['ready']] == ['M1', 'M2', 'M3', 'M4', 'M5', 'J2401S1', 'J2301S2'] and sum(1 for p in idx if p['kind'] == 'pyq') == 11 and all(not p['ready'] for p in idx if p['kind'] == 'pyq' and p['y'] not in ('J2401S1', 'J2301S2'))
# the solved 2024 paper: 90 image questions, key present, "attempt any 5" numerical sections, a worked-solution image for every question
r24 = s1.get(B + '/data/J2401S1.json')
assert r24.status_code == 200
g = r24.get_json()
assert len(g['qs']) == 90 and g['lab'] == '1234' and g['max'] == 300
assert [s.get('choose') for s in g['sections']] == [None, 5, None, 5, None, 5]
assert all(q.get('acc') and q['img'].startswith('data:image/webp') and q['sol'].startswith('data:image/webp') and q.get('qid') and q.get('cat') for q in g['qs'])
assert g['qs'][47]['acc'] == {'bonus': True}                                      # Q48: no printed option is correct
assert g['qs'][0]['acc'] == {'sets': ['B']} and g['qs'][20]['acc']['ranges'] == [[46, 46]]

for bad in ('P0402S1.json', 'M9.json', '..%2fapp.html', 'x.json', 'app.html'):
    assert s1.get(B + '/data/' + bad).status_code == 404, bad                         # papers awaiting an answer key are never served
html = s1.get(B + '/app').get_data(as_text=True)
assert '"memberName": "Stu One"' in html and B + '/results' in html and 'no-store' in s1.get(B + '/app').headers['Cache-Control']
page = s1.get(B + '/').get_data(as_text=True)
assert 'EduPulse-JEE Mock Test Centre' in page and '<iframe' in page and 'do not predict' in page

# ---- saving and analysis ----------------------------------------------------------------------------------------------------------------------
def attempt(paper='M1', mode='mock'):
    # 12 attempts + 3 blanks: confidence mix chosen so every number below can be checked by hand
    spec = [('MATH', 'MCQ', 'right', 'H'), ('MATH', 'MCQ', 'right', 'H'), ('MATH', 'MCQ', 'wrong', 'H'), ('MATH', 'MCQ', 'wrong', 'G'), ('MATH', 'NAT', 'wrong', 'L'),
            ('PHY', 'MCQ', 'right', 'M'), ('PHY', 'MCQ', 'wrong', 'M'), ('PHY', 'MCQ', 'right', 'L'), ('PHY', 'NAT', 'wrong', None),
            ('CHEM', 'MCQ', 'right', 'G'), ('CHEM', 'MCQ', 'wrong', 'G'), ('CHEM', 'NAT', 'right', 'H'), ('CHEM', 'MCQ', 'blank', None), ('PHY', 'MCQ', 'blank', None), ('MATH', 'MCQ', 'blank', None)]
    qs = {}
    for i, (sb, ty, st, cf) in enumerate(spec, 1):
        qs[str(i)] = {'type': ty, 'subj': sb, 'topic': {'MATH': 'CNQ', 'PHY': 'KIN', 'CHEM': 'MOL'}[sb], 'answer': '1', 'official': '1', 'status': st, 'marks': 4 if st == 'right' else -1 if st == 'wrong' else 0, 'confidence': cf, 'sec': 40 + i}
    return {'paper': paper, 'paperTitle': 'x', 'mode': mode, 'score': 20, 'max': 300, 'sections': [{'type': 'MCQ', 'subj': 'MATH', 'score': 7, 'max': 80, 'right': 2, 'wrong': 2, 'blank': 1}],
            'startedAt': '2026-10-25T10:00:00.000Z', 'finishedAt': '2026-10-25T12:55:00.000Z', 'autoSubmitted': False, 'questions': qs}

assert anon.post(B + '/results', json=attempt()).status_code in (302, 401, 403)
assert s1.post(B + '/results', json={'paper': 'P0402S1'}).status_code == 400            # a paper without its key cannot be submitted
assert s1.post(B + '/results', json={'paper': '1999'}).status_code == 400
assert s1.post(B + '/results', data='nope', content_type='application/json').status_code == 400
r = s1.post(B + '/results', json=attempt())
assert r.status_code == 200 and r.get_json()['ok']
RID = r.get_json()['id']
with app.app_context():
    row = PulseJeeResult.query.get(RID)
    assert (row.attempted, row.right, row.wrong, row.blank) == (12, 6, 6, 3)
    assert row.gained == 24 and row.lost == 6 and row.avoidable == 3 and row.sure_wrong == 1 and row.rated == 11
    assert (row.math_score, row.phy_score, row.chem_score) == (5, 6, 7)
    assert PulseProfile.query.get(S1).frequency == 'off'                              # visible to mentors; no e-mail digests switched on
    bad = attempt()
    bad['questions']['1']['confidence'] = 'Z'; bad['questions']['2']['topic'] = '<script>'; bad['questions']['3']['status'] = 'hacked'; bad['score'] = 'abc'
    p, err = pj.clean_payload(bad)
    assert err is None and p['questions']['1']['confidence'] is None and p['questions']['2']['topic'] is None and p['questions']['3']['status'] == 'blank' and p['score'] == 0

# analysis, checked by hand against attempt()
with app.app_context():
    an = pj.analyse([PulseJeeResult.query.get(RID)])
    c = an['conf']
    assert (c['H']['n'], c['H']['right'], c['H']['wrong'], c['H']['pct'], c['H']['net'], c['H']['ev']) == (4, 3, 1, 75, 11, 2.75)
    assert (c['M']['n'], c['M']['pct'], c['M']['net']) == (2, 50, 3) and (c['L']['n'], c['L']['net']) == (2, 3)
    assert (c['G']['n'], c['G']['right'], c['G']['wrong'], c['G']['pct'], c['G']['net'], c['G']['ev']) == (3, 1, 2, 33, 2, 0.67)
    assert an['gain'] == 24 and an['loss'] == 6 and an['avoidable'] == 3 and an['sure_wrong'] == 1 and an['gl_n'] == 5 and an['gl_net'] == 5 and an['unrated_wrong'] == 1 and an['enough']
    assert an['subj']['MATH'] == {'att': 5, 'right': 2, 'wrong': 3, 'blank': 1, 'gain': 8.0, 'loss': 3.0, 'acc': 40}
    assert an['subj']['PHY']['loss'] == 2.0 and an['subj']['CHEM']['acc'] == 67
    assert an['kind']['MCQ'] == {'att': 9, 'wrong': 4, 'loss': 4.0} and an['kind']['NAT'] == {'att': 3, 'wrong': 2, 'loss': 2.0}
    assert any('Negative marking took 6 marks (25%' in n for n in an['notes']) and any('Guess/Low answers scored +5' in n for n in an['notes']) and any('2 wrong numerical answers cost 2' in n for n in an['notes'])
    assert pj.ev(0.2) == 0 and pj.ev(0.25) == 0.25 and pj.ev(0) == -1                    # break-even is 20% at +4/-1
    assert not pj.analyse([])['enough']

# reports and access
rep = s1.get(B + '/result/%d' % RID).get_data(as_text=True)
assert 'By subject: gains and negative marks' in rep and 'Q3' in rep and 'avoidable' in rep and 'do not predict' in rep and 'Avg per answer' in rep
pdf = s1.get(B + '/result/%d.pdf' % RID)
assert pdf.status_code == 200 and pdf.data[:5] == b'%PDF-' and len(pdf.data) > 1500
assert s2.get(B + '/result/%d' % RID).status_code == 404 and s2.get(B + '/result/%d.pdf' % RID).status_code == 404 and anon.get(B + '/result/%d' % RID).status_code in (302, 401, 403)
assert admin.get(B + '/result/%d' % RID).status_code == 200 and mentor.get(B + '/result/%d' % RID).status_code == 404
with app.app_context():
    PulseProfile.query.get(S1).mentor_id = User.query.filter_by(email='m@x.com').one().id
    db.session.commit()
assert mentor.get(B + '/result/%d' % RID).status_code == 200 and mentor2.get(B + '/result/%d' % RID).status_code == 404
ms = mentor.get('/edupulse-uceed/mentor/%d' % S1).get_data(as_text=True)
assert 'JEE Main mocks' in ms and 'Report' in ms
mh = mentor.get('/edupulse-uceed/mentor').get_data(as_text=True)
assert 'JEE mocks' in mh and 'Lost to negatives' in mh

# history and totals over two attempts
s1.post(B + '/results', json=attempt('M2', 'practice'))
page = s1.get(B + '/').get_data(as_text=True)
assert 'My mock history' in page and page.count('/edupulse-jee/result/') == 4
with app.app_context():
    sm = pj.summary(S1)
    assert sm['attempts'] == 2 and sm['loss_total'] == 12 and sm['avoidable_rate'] == round(100 * 6 / 24) and sm['avg_pct'] == round(100 * 20 / 300)

# hub tile and EduPulse link
assert 'EduPulse-JEE Mock Test Centre' in s1.get('/member-home').get_data(as_text=True)
assert 'Open JEE mocks' in s1.get('/edupulse-uceed/').get_data(as_text=True)
print('EduPulse-JEE checks passed')
