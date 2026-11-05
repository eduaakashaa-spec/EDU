"""Class 12 PCM Analytics: data, eligibility judgement, levels, chapter priority, the study plan, the four supplied pages, access and saving.
Run from college-predictor/:  python tests/test_pcm12.py"""
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
from app.extensions import bcrypt, db  # noqa: E402
from app.models import User  # noqa: E402
from app.models_pulse import Class12Profile  # noqa: E402
from app.services import pcm12  # noqa: E402

# ---- data --------------------------------------------------------------------------------------------------------------------------------
ch = pcm12.chapters()
assert len(ch) == 37 and len({c['id'] for c in ch}) == 37
assert {s: round(sum(c['marks'] for c in ch if c['subj'] == s)) for s in 'PCM'} == {'P': 70, 'C': 70, 'M': 80}      # unit-group theory marks add up
assert {s: sum(1 for c in ch if c['subj'] == s) for s in 'PCM'} == {'P': 14, 'C': 10, 'M': 13}
for c in ch:
    assert c['name'] and c['marks'] > 0 and len(c['levels']) == 4 and set(c['levels']) <= {'Core', 'Build', 'Later'} and c['rules'] and c['hook'] and c['trap'], c['id']
rt = pcm12.routes()
assert len(rt) == 17 and {r['id'] for r in rt} >= {'josaa', 'bitsat', 'tnea', 'keam', 'mht', 'ap_eapcet_eng', 'dl_ipu_btech', 'dl_jac_btech_nsut_dtu', 'nri_maha', 'nri_vit', 'bits_isa'}
for r in rt:
    assert set(r['th']) == {'g', 's', 'b'} and all(lo <= hi for lo, hi in r['th'].values()), r['id']
    if r['id'] in ('dasa', 'keam', 'mht', 'ap_eapcet_eng', 'dl_ipu_btech', 'dl_jac_btech_nsut_dtu', 'nri_maha', 'nri_vit', 'bits_isa'):
        assert r['source'].startswith('https://') and r['confidence'].startswith('official page') and r['note'], r['id']

# ---- eligibility -------------------------------------------------------------------------------------------------------------------
m = {'Pt': 56, 'Pp': 27, 'Ct': 56, 'Cp': 27, 'Mt': 64, 'Mi': 18, 'En': 80, 'Fi': 80}
e = pcm12.eligibility(m, 'g')
assert e['entered'] and e['pcm_sum'] == 248 and abs(e['pcm'] - 82.7) < 0.05 and abs(e['agg'] - 81.6) < 0.05 and abs(e['tnea'] - (82 + 83 / 1.0 * 0 + (83 + 83) / 2.0)) < 0.5
by = {r['id']: r for r in e['routes']}
assert by['josaa']['status'] == 'meets' and by['bitsat']['status'] == 'meets' and by['tnea']['status'] == 'meets'
lo = pcm12.eligibility({'Pt': 35, 'Pp': 20, 'Ct': 35, 'Cp': 20, 'Mt': 40, 'Mi': 12, 'En': 50, 'Fi': 50}, 'g')
lb = {r['id']: r for r in lo['routes']}
assert lb['josaa']['status'] == 'short' and lb['josaa']['add'] > 0 and lb['bitsat']['status'] == 'short'
# BITSAT: a subject floor of 60 each makes a high PCM with one weak subject short
sub = pcm12.eligibility({'Pt': 40, 'Pp': 15, 'Ct': 70, 'Cp': 30, 'Mt': 80, 'Mi': 20}, 'g')
bs = {r['id']: r for r in sub['routes']}['bitsat']
assert bs['status'] == 'short' and bs['floor'] and bs['floor'][0]['subject'] == 'Physics'
# state routes read from official pages: 52% PCM meets AP EAPCET (45), Kerala (45) and MHT-CET Open (45); is short of GGSIPU (55) and DTU/NSUT (60)
st = {r['id']: r for r in pcm12.eligibility({'Pt': 36, 'Pp': 16, 'Ct': 36, 'Cp': 16, 'Mt': 42, 'Mi': 10}, 'g')['routes']}
assert abs(st['keam']['have'] - 52.0) < 0.1 and st['keam']['status'] == 'meets' and st['ap_eapcet_eng']['status'] == 'meets' and st['mht']['status'] == 'meets'
assert st['dl_ipu_btech']['status'] == 'short' and st['dl_ipu_btech']['add'] > 0 and st['dl_jac_btech_nsut_dtu']['status'] == 'short'
sr = {r['id']: r for r in pcm12.eligibility({'Pt': 36, 'Pp': 16, 'Ct': 36, 'Cp': 16, 'Mt': 42, 'Mi': 10}, 's')['routes']}
assert sr['dl_jac_btech_nsut_dtu']['status'] == 'check' and sr['mht']['status'] == 'meets'      # SC/ST at DTU: 50% to 55% depending on category, so Check
sf = pcm12.state_facts()
assert [s['state'] for s in sf['states']] == ['Maharashtra', 'Delhi', 'Kerala', 'Andhra Pradesh'] and all(s['facts'] for s in sf['states']) and sf['notes']
assert all(f['source'].startswith('https://') for s in sf['states'] for f in s['facts'])
# NRI routes: DASA 75% over five subjects; Maharashtra NRI/OCI 45%; VIT 55 to 60 shows Check between; BITS ISA needs 60 in each subject
nr = {r['id']: r for r in pcm12.eligibility({'Pt': 40, 'Pp': 17, 'Ct': 40, 'Cp': 17, 'Mt': 46, 'Mi': 11, 'En': 60, 'Fi': 60}, 'g')['routes']}
assert nr['nri_maha']['status'] == 'meets' and nr['nri_vit']['status'] == 'check' and nr['bits_isa']['status'] == 'short' and nr['dasa']['status'] == 'short'
nf = pcm12.nri_facts()
assert nf['pcm'] and nf['pcb'] and nf['notes_pcm'] and nf['notes_pcb'] and all(f['source'].startswith('https://') for f in nf['pcm'] + nf['pcb'])
# a conflicting rule (DASA 60 to 75) shows Check between the two figures
mid = {r['id']: r for r in pcm12.eligibility({'Pt': 46, 'Pp': 20, 'Ct': 46, 'Cp': 20, 'Mt': 52, 'Mi': 14, 'En': 66, 'Fi': 66}, 'g')['routes']}
assert mid['dasa']['status'] == 'short' and mid['dasa']['basis'] == '5-subject'      # DASA UG: 75% aggregate in five subjects (official brochure, no longer a 60-75 range)
assert not pcm12.eligibility({}, 'g')['entered']
assert pcm12.eligibility({'Pt': 999, 'Pp': -4}, 'zz')['totals']['P'] == 70.0          # capped, bad category falls back

# ---- levels and priority -----------------------------------------------------------------------------------------------------------
tests = pcm12.clean_tests([{'subj': 'P', 'date': '2026-10-01', 'got': 30, 'max': 70}, {'subj': 'P', 'date': '2026-10-15', 'got': 35, 'max': 70}, {'subj': 'C', 'date': '2026-10-02', 'got': 60, 'max': 70},
                           {'subj': 'M', 'date': '2026-10-03', 'got': 50, 'max': 80}, {'subj': 'X', 'got': 1, 'max': 2}, {'subj': 'M', 'got': 90, 'max': 80}, 'junk'])
assert len(tests) == 4 and tests[0]['pct'] == 42.9
lv = pcm12.subject_levels(tests, {})
assert lv['P']['band'] == 0 and lv['C']['band'] == 3 and lv['M']['band'] == 1 and lv['P']['source'].startswith('last 2')
assert pcm12.subject_levels([], {'Pt': 63})['P']['band'] == 3 and pcm12.subject_levels([], {})['P']['source'] == 'not enough data'
assert pcm12.subject_levels(tests, {}, {'P': 3})['P']['band'] == 3
pr = pcm12.priorities(lv, {'P01': 1, 'P02': 5})
assert len(pr) == 37 and pr[0]['score'] >= pr[-1]['score'] and [p['rank'] for p in pr] == list(range(1, 38))
assert next(p for p in pr if p['id'] == 'P01')['rating'] == 1 and next(p for p in pr if p['id'] == 'P03')['rating'] == 3 and not next(p for p in pr if p['id'] == 'P03')['rated']

# ---- the plan ----------------------------------------------------------------------------------------------------------------------
today = date(2026, 11, 5)
info, weeks, todo = pcm12.build_plan(lv, pr, '2027-02-17', 2, 5, today)
assert info['weeks'] == 15 and sum(info['phase_weeks']) == 15 and info['hours_week'] == 20.0 and info['weakest'] == 'Physics'
assert abs(sum(info['subject_hours'].values()) - info['hours_week']) < 0.3
assert len(weeks) == 15 and [w['n'] for w in weeks] == list(range(1, 16)) and {w['phase'] for w in weeks} == {1, 2, 3, 4}
ids = [t['id'] for w in weeks for t in w['tasks']]
assert len(ids) == len(set(ids))
p1 = {t['chapter'] for w in weeks if w['phase'] == 1 for t in w['tasks']}
p2 = {t['chapter'] for w in weeks if w['phase'] == 2 for t in w['tasks']}
assert p1 == p2 and len(p1) == len(todo) and all(w['tasks'] for w in weeks)
assert pcm12.build_plan(lv, pr, '', 2, 5, today)[1] == [] and pcm12.build_plan(lv, pr, '2026-11-01', 2, 5, today)[1] == []
short = pcm12.build_plan(lv, pr, '2026-12-03', 2, 5, today)
assert short[0]['weeks'] == 4 and sum(short[0]['phase_weeks']) == 4 and len(short[1]) == 4
a = pcm12.analyse({'exam_date': '2027-02-17', 'marks': m, 'tests': tests, 'ratings': {'P01': 2, 'ZZ': 3, 'P02': 9}, 'done': {'p1-P01': True}, 'hours_wd': 2, 'hours_we': 5}, today)
assert a['rated'] == 1 and a['progress']['done'] == 1 and a['progress']['tasks'] == sum(len(w['tasks']) for w in a['weeks']) and a['elig']['entered']
assert pcm12.analyse({}, today)['weeks'] == [] and pcm12.analyse('x', today)['plan']['weeks'] == 0
q = pcm12.quick_plan(2, '2027-02-17', 2, 5, today)
assert q['level'] == 'Good' and len(q['first']) == 8 and q['plan']['weeks'] == 15 and pcm12.quick_plan(9, '', 2, 5, today)['level'] == 'Average'

# ---- pages, access and saving ------------------------------------------------------------------------------------------------------
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
hub = anon.get('/class12-pcm/')
assert hub.status_code == 200 and b'Eligibility Gap Closer' in hub.data and b'Generate a study plan' in hub.data and b'id="states"' in hub.data and b'id="nri"' in hub.data and b'Andhra Pradesh' in hub.data and b'Kerala' in hub.data
for path, needle in (('eligibility', b'Eligibility Gap Closer'), ('board-playbook', b'Board Score Playbook'), ('thumb-rules', b'Thumb Rules Handbook'), ('answer-lab', b'Answer Sheet Lab')):
    r = anon.get('/class12-pcm/' + path)
    assert r.status_code == 200 and needle in r.data and b'claude.ai/artifact' not in r.data and b'EduAakashaA home' in r.data and b'./eduaakashaa_logo.png' not in r.data, path
assert b'/class12-pcm/board-playbook' in anon.get('/class12-pcm/eligibility').data
assert anon.get('/class12-pcm/nope').status_code == 404
qp = anon.post('/class12-pcm/quick-plan', json={'level': 1, 'exam_date': '2099-02-17', 'hours_wd': 2, 'hours_we': 5}).get_json()
assert qp['ok'] and qp['plan']['weeks'] > 100 and len(qp['first']) == 8
assert anon.post('/class12-pcm/quick-plan', json={'level': 'x', 'exam_date': 'bad'}).get_json()['plan']['weeks'] == 0
assert anon.get('/class12-pcm/dashboard').status_code in (301, 302, 401, 403)
assert free.get('/class12-pcm/dashboard').status_code in (301, 302, 403)
assert anon.post('/class12-pcm/dashboard/save', json={}).status_code in (301, 302, 401, 403)
dash = prem.get('/class12-pcm/dashboard')
assert dash.status_code == 200 and b'My PCM Analytics dashboard' in dash.data and b'pdInit' in dash.data
body = {'exam_date': '2099-02-17', 'hours_wd': 2, 'hours_we': 5, 'cat': 's', 'marks': m, 'tests': [{'subj': 'P', 'date': '2026-10-01', 'got': 35, 'max': 70}, {'subj': 'Z', 'got': 1, 'max': 2}],
        'levels': {'P': 2, 'X': 1}, 'ratings': {'P01': 2, 'P02': 7, 'ZZ': 3}, 'done': {'p1-P01': True, 'p9': False}}
r = prem.post('/class12-pcm/dashboard/save', json=body).get_json()
assert r['ok'] and r['analysis']['rated'] == 1 and r['analysis']['levels']['P']['band'] == 2 and r['analysis']['progress']['done'] == 1 and len(r['analysis']['tests']) == 1
with app.app_context():
    row = Class12Profile.query.filter_by(user_id=User.query.filter_by(email='p@x.com').first().id, stream='pcm').first()
    saved = json.loads(row.data_json)
    assert saved['cat'] == 's' and saved['ratings'] == {'P01': 2} and saved['levels'] == {'P': 2} and saved['done'] == {'p1-P01': True} and len(saved['tests']) == 1
assert prem.post('/class12-pcm/dashboard/save', json=dict(body, hours_we=6)).get_json()['ok']
with app.app_context():
    assert Class12Profile.query.count() == 1                                      # saving again updates the one row
assert prem.post('/class12-pcm/dashboard/save', data='nope', content_type='text/plain').status_code == 400
assert b'2099-02-17' in prem.get('/class12-pcm/dashboard').data                  # the saved profile comes back
assert free.get('/class12-pcm/dashboard').status_code in (301, 302, 403)
try:
    os.remove(_db)
except OSError:
    pass
print('pcm12 checks passed')
