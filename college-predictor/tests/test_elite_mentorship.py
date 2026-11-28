"""Public page /elite-mentorship-grade-11-12: content, assets, menu and School page links. Run from college-predictor/:  python tests/test_elite_mentorship.py"""
import os
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
_fd, _db = tempfile.mkstemp(suffix='.db')
os.close(_fd)
os.environ.update(DATABASE_URL='sqlite:///' + _db, SECRET_KEY='test', FLASK_DEBUG='0')

from app import create_app  # noqa: E402
from app.extensions import db  # noqa: E402

app = create_app()
app.config['TESTING'] = True
with app.app_context():
    db.create_all()
    c = app.test_client()
    for url in ('/elite-mentorship-grade-11-12', '/elite-mentorship'):
        r = c.get(url)
        assert r.status_code == 200, (url, r.status_code)                                  # open to everyone, no login
    html = r.get_data(as_text=True)
    for text in ('Coaching builds the marks', 'Grade 11 track', 'Grade 12 track', '₹25,000', '₹75,000', '₹50,000', '4 online one-to-one sessions',
                 'Who owns your decisions today?', 'The 5A method'.split(' ')[1], 'Student roadmap', 'Download the brochure', 'Download the poster',
                 'cannot and does not guarantee a rank or a seat', 'wa.me/918015722706', 'js/elite_mentorship.js', 'css/elite_mentorship.css'):
        assert text in html, text
    for banned in ('+971', 'Dubai', '74,999 including', '6 virtual'):
        assert banned not in html, banned                                                  # India-only contact details; agreed fee and session count
    static = os.path.join(ROOT, 'app', 'static')
    for f in ['img/elite/brochure-%d.jpg' % i for i in range(1, 10)] + ['img/elite/poster.jpg']:
        p = os.path.join(static, *f.split('/'))
        assert os.path.exists(p) and open(p, 'rb').read(2) == b'\xff\xd8' and os.path.getsize(p) < 450000, f
        assert c.get('/static/' + f).status_code == 200, f
    pdf = os.path.join(static, 'docs', 'EduAakashaA-Elite-Mentorship-Brochure.pdf')
    assert open(pdf, 'rb').read(4) == b'%PDF' and os.path.getsize(pdf) < 4000000
    js = open(os.path.join(static, 'js', 'elite_mentorship.js'), encoding='utf-8').read()
    assert js.count("['Months") == 4 and "'Late Jul–Aug'" in js                            # 4 Grade 11 gates, 6 Grade 12 gates
    assert 'href="/elite-mentorship' in c.get('/').get_data(as_text=True)            # School menu link
    school = c.get('/school').get_data(as_text=True)
    assert school.count('Elite Mentorship for Grade 11 and 12') >= 2                       # PCM and PCB tabs
print('elite mentorship checks passed')
