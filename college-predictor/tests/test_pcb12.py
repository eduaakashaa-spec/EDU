"""Class 12 PCB Analytics: Biology and PCB chapter data, entrance-route judgement, the PCB plan, the public hub, access, and saving (kept apart from the PCM profile).
Run from college-predictor/:  python tests/test_pcb12.py"""
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
from app.data import pcb12  # noqa: E402
from app.extensions import bcrypt, db  # noqa: E402
from app.models import User  # noqa: E402
from app.models_pulse import Class12Profile  # noqa: E402
from app.services import pcm12  # noqa: E402

# ---- chapters ----------------------------------------------------------------------------------------------------------------------------
ch = pcm12.chapters('pcb')
assert len(ch) == 37 and len({c['id'] for c in ch}) == 37 and {s: sum(1 for c in ch if c['subj'] == s) for s in 'PCB'} == {'P': 14, 'C': 10, 'B': 13}
assert {s: round(sum(c['marks'] for c in ch if c['subj'] == s)) for s in 'PCB'} == {'P': 70, 'C': 70, 'B': 70}
units = {}
for c in ch:
    if c['subj'] == 'B':
        units[c['unit']] = units.get(c['unit'], 0) + c['marks']
assert {u: round(v) for u, v in units.items()} == {'Unit VI': 16, 'Unit VII': 20, 'Unit VIII': 12, 'Unit IX': 12, 'Unit X': 10}      # CBSE 2026-27 Biology unit marks
for c in ch:
    assert c['name'] and len(c['levels']) == 4 and set(c['levels']) <= {'Core', 'Build', 'Later'} and len(c['rules']) >= 2 and c['hook'] and c['trap'] and c['why'], c['id']
bio = [c for c in ch if c['subj'] == 'B']
assert all(len(c['rules']) == 3 for c in bio) and all('Excellent' not in c['levels'] and 'Later' not in c['levels'][3] for c in bio)
blob = json.dumps(ch, ensure_ascii=False).lower()
for bad in ('http', 'www.', 'careers360', 'whatsapp'):
    assert bad not in blob, bad
eco = next(c for c in bio if c['name'] == 'Ecosystem')
assert 'less than 50 per cent' in ' '.join(eco['rules'])                      # the reviewer's correction on PAR is in

# ---- routes ------------------------------------------------------------------------------------------------------------------------------
rt = pcm12.routes('pcb')
assert {r['id'] for r in rt} == {'neet_ug', 'bds', 'bvsc', 'bsc_nursing', 'bsc_agri', 'mh_neet_mbbs', 'mh_cet_pcb_eng', 'mh_agri', 'kl_neet_mbbs', 'kl_neet_agri', 'kl_neet_bvsc', 'ap_eapcet_bpharm_bipc', 'dl_ipu_mbbs', 'dl_ipu_bsc_nursing', 'dl_ipu_bpt'}
for r in rt:
    assert set(r['th']) == {'g', 's', 'b'} and all(lo is not None and lo <= hi for lo, hi in r['th'].values()) and r['confidence'] and r['source'].startswith('https://'), r['id']
assert next(r for r in rt if r['id'] == 'neet_ug')['confidence'] == 'not confirmed' and next(r for r in rt if r['id'] == 'mh_neet_mbbs')['confidence'].startswith('not confirmed')          # the NEET bulletin could not be read, and the page must say so
good = {'Pt': 50, 'Pp': 25, 'Ct': 45, 'Cp': 24, 'Bt': 55, 'Bp': 27, 'En': 70, 'Fi': 70}
e = pcm12.eligibility(good, 'g', 'pcb')
assert e['entered'] and e['label'] == 'PCB' and e['core_sum'] == 226 and abs(e['core'] - 75.3) < 0.05 and e['tnea'] is None and set(e['totals']) == {'P', 'C', 'B'}
assert all(r['status'] == 'meets' for r in e['routes'])
low = pcm12.eligibility({'Pt': 28, 'Pp': 15, 'Ct': 28, 'Cp': 15, 'Bt': 30, 'Bp': 15, 'En': 40, 'Fi': 40}, 'g', 'pcb')
lb = {r['id']: r for r in low['routes']}
assert lb['neet_ug']['status'] == 'short' and lb['neet_ug']['add'] > 0 and lb['bvsc']['basis'] == 'PCB and English' and lb['bsc_agri']['basis'] == '5-subject'
mid = {r['id']: r for r in pcm12.eligibility({'Pt': 40, 'Pp': 20, 'Ct': 38, 'Cp': 19, 'Bt': 40, 'Bp': 20, 'En': 55, 'Fi': 55}, 's', 'pcb')['routes']}      # about 59% PCB, 56.5% with English
assert mid['neet_ug']['status'] == 'meets' and mid['bsc_nursing']['status'] == 'meets'
chk = {r['id']: r for r in pcm12.eligibility({'Pt': 30, 'Pp': 14, 'Ct': 30, 'Cp': 14, 'Bt': 30, 'Bp': 14, 'En': 40, 'Fi': 40}, 's', 'pcb')['routes']}
assert chk['bsc_nursing']['status'] == 'check' and chk['bsc_nursing']['add'] > 0           # between the 40% corrigendum and the 45% INC page: check
assert not pcm12.eligibility({}, 'g', 'pcb')['entered']

# ---- levels, plan -----------------------------------------------------------------------------------------------------------------------
tests = pcm12.clean_tests([{'subj': 'B', 'date': '2026-10-01', 'got': 60, 'max': 70}, {'subj': 'P', 'date': '2026-10-02', 'got': 30, 'max': 70}, {'subj': 'M', 'got': 3, 'max': 4}], 'pcb')
assert len(tests) == 2                                                                      # Maths is not a PCB subject
lv = pcm12.subject_levels(tests, {'Ct': 40}, None, 'pcb')
assert set(lv) == {'P', 'C', 'B'} and lv['B']['band'] == 3 and lv['P']['band'] == 0 and lv['C']['band'] == 1 and lv['C']['source'] == 'marks entered'
pr = pcm12.priorities(lv, {'B01': 1}, 'pcb')
assert len(pr) == 37 and next(p for p in pr if p['id'] == 'B01')['rating'] == 1
info, weeks, todo = pcm12.build_plan(lv, pr, '2027-02-17', 2, 5, date(2026, 11, 5), None, 'pcb')
assert info['weeks'] == 15 and set(info['subject_hours']) == {'P', 'C', 'B'} and abs(sum(info['subject_hours'].values()) - info['hours_week']) < 0.3 and info['weakest'] == 'Physics'
assert len(weeks) == 15 and any('labelled-diagram' in t['text'] for w in weeks for t in w['tasks'])
ids = [t['id'] for w in weeks for t in w['tasks']]
assert len(ids) == len(set(ids))
q = pcm12.quick_plan(2, '2027-02-17', 2, 5, date(2026, 11, 5), 'pcb')
assert q['level'] == 'Good' and len(q['first']) == 8 and all(f['subj'] in ('Physics', 'Chemistry', 'Biology') for f in q['first'])
a = pcm12.analyse({'exam_date': '2027-02-17', 'marks': good, 'tests': tests, 'ratings': {'B01': 2, 'M01': 3}, 'done': {'p1-B01': True}}, date(2026, 11, 5), 'pcb')
assert a['rated'] == 1 and a['elig']['label'] == 'PCB' and a['progress']['done'] <= 1 and set(a['levels']) == {'P', 'C', 'B'}

# ---- the playbook content ---------------------------------------------------------------------------------------------------------------
ctx = pcb12.context()
d = ctx['data']
assert len(d['levels']) == 4 and len(d['sheets']) == 6 and {s['subject'] for s in d['sheets']} == {'Biology', 'Chemistry', 'Physics'}
for s in d['sheets']:
    assert len(s['scheme']) == 3 and sum(v['marks'] for v in s['scheme']) == s['marks'] == 3 and [x['style'] for x in s['sheets']] == ['Needs support', 'Good', 'Excellent']
    assert [x['score'] for x in s['sheets']][2] == 3 and all(0 <= x['score'] <= 3 and x['lines'] and x['note'] for x in s['sheets']), s['q'][:30]
    assert s['sheets'][0]['score'] < s['sheets'][1]['score'] < s['sheets'][2]['score']
assert all(l['target'].startswith('Aim') for l in d['levels'])                               # no promised results
assert ctx['n_routes'] == 15 and any('Not confirmed' or n for n in ctx['facts']['notes']) and ctx['facts']['facts'] and ctx['sources']

# ---- pages, access and saving -----------------------------------------------------------------------------------------------------------
app = create_app()
with app.app_context():
    db.create_all()
    pw = bcrypt.generate_password_hash('x').decode()
    db.session.add_all([User(name='Free', email='f@x.com', tier='free', password_hash=pw), User(name='Prem', email='p@x.com', tier='premium', password_hash=pw)])
    db.session.commit()


def login(em):
    c = app.test_client()
    assert c.post('/login', data={'email': em, 'password': 'x'}).status_code == 302
    return c


anon, free, prem = app.test_client(), login('f@x.com'), login('p@x.com')
hub = anon.get('/class12-pcb/')
assert hub.status_code == 200 and b'Class 12 PCB' in hub.data and b'Answer Sheet Lab' in hub.data and b'Not confirmed' in hub.data and b'pbData' in hub.data and b'Generate a study plan' in hub.data
r = anon.post('/class12-pcb/eligibility', json={'marks': good, 'cat': 'g'}).get_json()
assert r['ok'] and r['elig']['entered'] and len(r['elig']['routes']) == 15 and all(x['source'] for x in r['elig']['routes'])
assert not anon.post('/class12-pcb/eligibility', json={'marks': 'x'}).get_json()['elig']['entered']
qp = anon.post('/class12-pcb/quick-plan', json={'level': 1, 'exam_date': '2099-02-17', 'hours_wd': 2, 'hours_we': 5}).get_json()
assert qp['ok'] and qp['plan']['weeks'] > 100 and set(qp['plan']['subject_hours']) == {'P', 'C', 'B'}
assert anon.get('/class12-pcb/dashboard').status_code in (301, 302, 401, 403) and free.get('/class12-pcb/dashboard').status_code in (301, 302, 403)
assert anon.post('/class12-pcb/dashboard/save', json={}).status_code in (301, 302, 401, 403)
dash = prem.get('/class12-pcb/dashboard')
assert dash.status_code == 200 and b'My PCB Analytics dashboard' in dash.data and b'Biology' in dash.data
body = {'exam_date': '2099-02-17', 'hours_wd': 2, 'hours_we': 5, 'cat': 's', 'marks': good, 'tests': [{'subj': 'B', 'date': '2026-10-01', 'got': 40, 'max': 70}, {'subj': 'M', 'got': 1, 'max': 2}],
        'levels': {'B': 2, 'M': 1}, 'ratings': {'B01': 2, 'P02': 7, 'M01': 3}, 'done': {'p1-B01': True}}
j = prem.post('/class12-pcb/dashboard/save', json=body).get_json()
assert j['ok'] and j['analysis']['rated'] == 1 and len(j['analysis']['tests']) == 1 and j['analysis']['levels']['B']['band'] == 2 and j['analysis']['elig']['label'] == 'PCB'
# the PCM dashboard of the same member is separate
assert prem.post('/class12-pcm/dashboard/save', json={'exam_date': '2098-01-01', 'marks': {'Mt': 60}}).get_json()['ok']
with app.app_context():
    uid = User.query.filter_by(email='p@x.com').first().id
    rows = {r.stream: json.loads(r.data_json) for r in Class12Profile.query.filter_by(user_id=uid).all()}
    assert set(rows) == {'pcm', 'pcb'} and rows['pcb']['ratings'] == {'B01': 2} and rows['pcb']['levels'] == {'B': 2} and rows['pcm']['exam_date'] == '2098-01-01'
assert prem.post('/class12-pcb/dashboard/save', json=dict(body, hours_we=6)).get_json()['ok']
with app.app_context():
    assert Class12Profile.query.filter_by(user_id=uid, stream='pcb').count() == 1
assert prem.post('/class12-pcb/dashboard/save', data='x', content_type='text/plain').status_code == 400
assert b'2099-02-17' in prem.get('/class12-pcb/dashboard').data and b'2098-01-01' in prem.get('/class12-pcm/dashboard').data
try:
    os.remove(_db)
except OSError:
    pass
print('pcb12 checks passed')
