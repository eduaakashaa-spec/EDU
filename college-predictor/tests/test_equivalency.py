"""Entrance exam equivalency: data integrity (every rule has a source, every verdict key is valid), the verdict engine, the public pages and the menu link.
Run from college-predictor/:  python tests/test_equivalency.py"""
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
_fd, _db = tempfile.mkstemp(suffix='.db')
os.close(_fd)
os.environ.update(DATABASE_URL='sqlite:///' + _db, SECRET_KEY='test', FLASK_DEBUG='0')

from app import create_app  # noqa: E402
from app.data import equivalency as D  # noqa: E402
from app.services import equivalency as eq  # noqa: E402

# ---- data ----------------------------------------------------------------------------------------------------------------------------------
ids = [e['id'] for e in D.EXAMS]
assert len(ids) == len(set(ids)) and {'jee-main', 'jee-advanced', 'josaa-nit', 'nata', 'neet-ug', 'uceed', 'nid_bdes', 'nift', 'cuet-ug', 'clat-ug'} <= set(ids), ids
qkeys = {k for k, _ in D.QUALS}
gkeys = {k for k, _ in D.GROUPS}
for e in D.EXAMS:
    assert e['group'] in gkeys and e['level'] in ('ug', 'pg') and e['rules'] and e['summary'] and e['cycle'], e['id']
    for r in e['rules']:
        assert r['text'] and r['topic'], e['id']
        assert r['source'].startswith('https://'), (e['id'], r)                                     # every rule carries an official link
        assert 'coaching' not in r['source'] and 'careers360' not in r['source'] or r['text'].startswith('Press report'), (e['id'], r)
    for k, v in e['quals'].items():
        assert k in qkeys and v[0] in ('yes', 'equiv', 'check', 'no') and v[1], (e['id'], k)
    for n in e['needs']:
        assert n['label'] and set(n['any']) <= set(D.SUBJECTS), (e['id'], n)
    if e['level'] == 'ug':
        assert set(e['quals']) == qkeys, (e['id'], qkeys - set(e['quals']))                          # every qualification has a verdict
assert D.FRAMEWORKS and all(f['text'] for f in D.FRAMEWORKS)

# ---- engine --------------------------------------------------------------------------------------------------------------------------------
def v(exam_id, qual, subs):
    return eq.verdict(eq.exam(exam_id), qual, subs)


assert v('neet-ug', 'cbse', ['Physics', 'Chemistry', 'Biology', 'English'])['status'] == 'yes'
assert v('neet-ug', 'cbse', ['Physics', 'Chemistry', 'Biotechnology', 'English'])['status'] == 'yes'      # Biotechnology can stand for Biology
r = v('neet-ug', 'cbse', ['Physics', 'Chemistry', 'Mathematics', 'English'])
assert r['status'] == 'subjects' and 'Biology or Biotechnology' in r['missing']
assert v('neet-ug', 'ib', ['Physics', 'Chemistry', 'Biology', 'English'])['status'] == 'equiv'
assert v('neet-ug', 'nios', ['Physics', 'Chemistry', 'Biology', 'English'])['status'] == 'check'          # not named in the bulletin: never claimed as accepted
assert v('jee-advanced', 'cbse', ['Physics', 'Chemistry', 'Mathematics'])['status'] == 'yes'
assert v('jee-advanced', 'cbse', ['Physics', 'Biology', 'Mathematics'])['status'] == 'subjects'
assert v('jee-main', 'cbse', ['Physics', 'Biotechnology', 'Mathematics'])['status'] == 'yes'              # one of Chemistry, Biology, Biotechnology
assert v('nata', 'diploma', [])['status'] == 'yes'                                                       # 10+3 diploma with Maths: its own subject rule
assert v('nata', 'cbse', ['Physics', 'Mathematics', 'Computer Science'])['status'] == 'yes'
assert v('uceed', 'cbse', [])['status'] == 'yes'                                                         # any stream
assert v('uceed', 'foreign', [])['status'] == 'equiv'
assert eq.verdict(eq.exam('uceed'), 'nope', [])['status'] == 'check'                                      # unknown qualification
rows = eq.check('nios', ['Physics', 'Chemistry', 'Mathematics'])
assert all(r['exam']['level'] == 'ug' for r in rows) and [r['status'] for r in rows] == sorted((r['status'] for r in rows), key=lambda s: eq.STATUS_ORDER[s])
assert len(eq.check('cbse', [], 'design')) == 3 and {r['exam']['group'] for r in eq.check('cbse', [], 'design')} == {'design'}

# ---- pages ---------------------------------------------------------------------------------------------------------------------------------
app = create_app()
c = app.test_client()
r = c.get('/entrance-equivalency/')
t = r.get_data(as_text=True)
assert r.status_code == 200 and 'data-how="eq-hub"' in t and 'Entrance Exam Equivalency Checker' in t and 'id="qual"' in t and 'Equivalence frameworks' in t
r = c.get('/entrance-equivalency/?qual=nios&sub=Physics&sub=Chemistry&sub=Biology&sub=English&group=med')
t = r.get_data(as_text=True)
assert r.status_code == 200 and 'NEET UG' in t and 'data-st="check"' in t and 'class="eq-r fi"' in t
assert c.get('/entrance-equivalency/?qual=bogus&group=zzz').status_code == 200                           # junk input is ignored, not an error
for e in D.EXAMS:
    page = c.get('/entrance-equivalency/' + e['id'])
    assert page.status_code == 200, e['id']
    body = page.get_data(as_text=True)
    assert e['rules'][0]['source'] in body and 'Rules and sources' in body
assert c.get('/entrance-equivalency/not-an-exam').status_code == 404
home = c.get('/').get_data(as_text=True)
assert '/entrance-equivalency/' in home                                                                   # in the Colleges and Exams menu
low = (t + home).lower()
assert 'office hours' not in low and 'working hours' not in low
print('equivalency checks passed')
