"""School (Class 8 to 12) grouping: the /school page, the top menu groups, the Member Home category and the PCM/PCB cross-links.
Run from college-predictor/:  python tests/test_school.py"""
import os
import re
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
_fd, _db = tempfile.mkstemp(suffix='.db')
os.close(_fd)
os.environ.update(DATABASE_URL='sqlite:///' + _db, SECRET_KEY='test', FLASK_DEBUG='0')

from app import create_app  # noqa: E402
from app.services import member_hub  # noqa: E402

app = create_app()
c = app.test_client()
page = c.get('/school')
assert page.status_code == 200 and c.get('/school-class-8-12').status_code == 200
h = page.get_data(as_text=True)
assert 'Which class are you in?' in h and h.count('class="sc-panel"') == 3 and 'Class 11 and 12: PCM' in h and 'Class 11 and 12: PCB' in h
links = re.findall(r'<a class="sc-c" href="([^"]+)"', h)
assert len(links) >= 25, len(links)
for href in set(links):
    assert c.get(href).status_code in (200, 301, 302, 401, 403), href
for want in ('/class12-pcm/', '/class12-pcb/', '/class12-pcm/eligibility', '/class12-pcm/thumb-rules', '/olympiad-exam-guide', '/neet-ug-2027', '/sat-exam-guidelines', '/edupulse-free-mock-tests/'):
    assert any(l.startswith(want) for l in links), want
assert any('#olympiad-jr' in l for l in links) and any('#olympiad-sr' in l for l in links) and any('#neet' in l for l in links)       # add-on anchors are kept

# top menu: School and Study Abroad groups exist, and Colleges & Exams no longer carries the school-stage pages
home = c.get('/').get_data(as_text=True)
nav = home[home.index('class="nav__list"'):home.index('class="nav__mobile-auth"') if 'class="nav__mobile-auth"' in home else None]
assert 'School (Class 8&ndash;12)' in nav and 'Study Abroad' in nav and 'Class 8&ndash;10' in nav and 'All school tools' in nav
colleges = nav[nav.index('Colleges &amp; Exams'):nav.index('School (Class 8&ndash;12)')]
for gone in ('Class 12 PCM Analytics', 'Class 12 PCB Analytics', 'Grade 7&ndash;10 Explorer', 'Olympiad Exams Guide', 'SAT Exam Guidelines'):
    assert gone not in colleges, gone
for kept in ('NIRF Rankings', 'NEET Papers Analysed', 'EduPulse Free Mock Tests', 'CAT'):
    assert kept in colleges, kept
school = nav[nav.index('School (Class 8&ndash;12)'):nav.index('Study Abroad')]
for want in ('Class 12 PCM Analytics', 'Class 12 PCB Analytics', 'Grade 7&ndash;10 Explorer', 'Olympiad Exams Guide', 'Board Score Playbook'):
    assert want in school, want
abroad = nav[nav.index('Study Abroad'):nav.index('>Medicine<')]
assert 'SAT Exam Guidelines' in abroad and 'EduPulse-SAT' in abroad

# Member Home: a School category holds the school tiles, and they left the old groups
cat = {x['key']: [t['title'] for t in x['tiles']] for x in member_hub.CATEGORIES}
assert 'school' in cat and len(cat['school']) == 8
for t in ('EduPulse-Explorer (Grades 7 to 10)', 'EduPulse-TN Class 10 Mock Test Centre', 'Class 12 PCM Analytics', 'Class 12 PCB Analytics', 'EduPulse-Olympiad Practice Centre', 'Olympiad foundation mentorship', 'Olympiad senior mentorship'):
    assert t in cat['school'], t
    assert all(t not in v for k, v in cat.items() if k != 'school'), t
assert any(t.startswith('FutureReady') for t in cat['school']) and 'Stream selection' in cat['journey']
assert 'EduPulse-NEET Mock Test Centre' in cat['edupulse'] and 'NEET (UG) mentorship' in cat['mentorship']

# the PCM and PCB hubs point onward
pcm = c.get('/class12-pcm/').get_data(as_text=True)
pcb = c.get('/class12-pcb/').get_data(as_text=True)
assert 'Aiming for JEE?' in pcm
assert 'Aiming for NEET?' in pcb and '/neet-ug-2027' in pcb and '/school' in pcb and '/school' in pcm
try:
    os.remove(_db)
except OSError:
    pass
print('school checks passed')
