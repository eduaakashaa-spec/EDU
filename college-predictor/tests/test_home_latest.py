"""Homepage: the New on EduAakashaA section (EduPulse practice, guides and analytics) and the extra engine cards link to pages that work.
Run from college-predictor/:  python tests/test_home_latest.py"""
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

app = create_app()
c = app.test_client()
page = c.get('/').get_data(as_text=True)
sec = page[page.index('id="awNew"'):page.index('id="awEng"')]
links = re.findall(r'<a class="aw-ix" href="([^"]+)"', sec)
assert len(links) == 13 and len(set(links)) == 13, links
for want in ('/edupulse-free-mock-tests/', '/neet-mock/', '/sat-mock/', '/olympiad-mock/', '/class12-pcm/', '/class12-pcb/', '/school', '/sat-exam-guidelines', '/olympiad-exam-guide', '/neet-papers-analysis', '/josaa-2026-analytics'):
    assert want in links, want
for href in links:
    assert c.get(href).status_code in (200, 301, 302, 401, 403), href              # public pages open; member pages send visitors to log in or join
eng = page[page.index('id="awTrack"'):page.index('id="awProof"')]
for want in ('/class12-pcm/', '/class12-pcb/', '/edupulse-free-mock-tests/'):
    assert want in eng, want
assert page.count('class="hc-slide"') == 12
try:
    os.remove(_db)
except OSError:
    pass
print('home latest checks passed')
