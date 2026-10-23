"""Student assessment page: site theme, banner image, membership calls to action. Run: python tests/test_student_assessment_page.py"""
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_fd, _db = tempfile.mkstemp(suffix='.db')
os.close(_fd)
os.environ.update(DATABASE_URL='sqlite:///' + _db, SECRET_KEY='test', FLASK_DEBUG='0')
from app import create_app

app = create_app()
app.config['TESTING'] = True
c = app.test_client()
r = c.get('/student-assessment')
t = r.get_data(as_text=True)
assert r.status_code == 200 and 'class="sa-hero"' in t and 'img/hub/journey.webp' in t
assert t.count('/members-registration') >= 2 and 'Join EduAakashaa for membership' in t        # hero + closing call to action
assert 'id="sa-start"' in t and 'js/student_assessment.js' in t and 'id="inName"' in t          # the assessment itself is intact
css = c.get('/static/css/student_assessment.css').get_data(as_text=True)
assert '--accent2:#0E3A8A' in css and '--bg:#FBF7EE' in css and '#ea7c0e' not in css.lower()            # site palette, old blue/amber palette gone
assert c.get('/static/img/hub/journey.webp').status_code == 200
try:
    os.unlink(_db)
except OSError:
    pass
print('student assessment page checks passed')
