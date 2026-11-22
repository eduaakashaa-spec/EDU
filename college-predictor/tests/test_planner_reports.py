"""Planner monthly and whole-plan PDF reports (calendar with infographics). Run from college-predictor/:  python tests/test_planner_reports.py [outdir]"""
import io
import os
import sys
import tempfile
from datetime import date, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
_fd, _db = tempfile.mkstemp(suffix='.db')
os.close(_fd)
os.environ.update(DATABASE_URL='sqlite:///' + _db, SECRET_KEY='test', FLASK_DEBUG='0')

from pypdf import PdfReader  # noqa: E402

from app import create_app  # noqa: E402
from app.data import darsh_jee_plan as plan_data  # noqa: E402
from app.extensions import bcrypt, db  # noqa: E402
from app.models import User  # noqa: E402
from app.models_planner import SpPlan, SpTask  # noqa: E402
from app.services import planner_cal_pdf as C  # noqa: E402

out = sys.argv[1] if len(sys.argv) > 1 else None
app = create_app()
app.config['TESTING'] = True
pw = lambda: bcrypt.generate_password_hash('x').decode()  # noqa: E731


def login(email):
    cl = app.test_client()
    assert cl.post('/login', data={'email': email, 'password': 'x'}).status_code == 302
    return cl


with app.app_context():
    db.create_all()
    db.session.add_all([User(name='Darsh Agarwal', email='d@x.com', tier='elite', password_hash=pw()), User(name='Other', email='o@x.com', tier='elite', password_hash=pw())])
    db.session.commit()
    stu = User.query.filter_by(email='d@x.com').one()
    STU = stu.id
    p = SpPlan(user_id=stu.id, title='Darsh: JEE Main 2027 and CBSE Grade 12 plan', exam='JEE', level='average', start_date=plan_data.START, weeks=20, exam_date=date(2027, 1, 20), hours_per_day=5, status='active')
    db.session.add(p)
    db.session.flush()
    for i, t in enumerate(plan_data.build()):
        done = t['day'] < date(2026, 12, 20) and i % 4 != 0                 # most early tasks done, some missed
        db.session.add(SpTask(plan_id=p.id, day=t['day'], subject=t.get('subject'), chapter=t.get('chapter'), task_type=t['task_type'], title=t['title'][:200], minutes=t['minutes'],
                              status='done' if done else 'todo', done_at=datetime(2026, 12, 1) if done else None))
    db.session.commit()
    months = C.plan_months(p)
    assert months[0] == (2026, 11) and months[-1][0] == 2027 and len(months) >= 5, months

    today = date(2026, 12, 20)
    m = C.month_pdf(p, stu.name, 2026, 12, today)
    w = C.plan_report_pdf(p, stu.name, today)
    if out:
        open(os.path.join(out, 'month.pdf'), 'wb').write(m)
        open(os.path.join(out, 'whole.pdf'), 'wb').write(w)
    rm, rw = PdfReader(io.BytesIO(m)), PdfReader(io.BytesIO(w))
    assert len(rm.pages) == 4, len(rm.pages)                                   # cover, calendar, infographics, contact
    assert len(rw.pages) == 7, len(rw.pages)                                   # cover, overview, 3 calendar pages (two months each), topics and key dates, contact
    mt = ''.join(pg.extract_text() or '' for pg in rm.pages)
    assert 'DECEMBER 2026' in mt.upper() and 'MON' in mt and 'time went' in mt
    assert 'CALENDAR' in ''.join(pg.extract_text() or '' for pg in rw.pages)

# flask-login keeps current_user on the app context, so each person gets a context of their own
with app.app_context():
    c = login('d@x.com')
    r1 = c.get('/study-planner/download/month.pdf?month=2027-01')
    assert r1.status_code == 200 and r1.mimetype == 'application/pdf' and r1.data[:4] == b'%PDF', r1.status_code
    assert 'monthly-report-2027-01' in r1.headers['Content-Disposition']
    assert c.get('/study-planner/download/month.pdf?month=2030-05').status_code == 200            # outside the plan: nearest month, not an error
    r3 = c.get('/study-planner/download/plan-report.pdf')
    assert r3.status_code == 200 and r3.mimetype == 'application/pdf'
    rep = c.get('/study-planner/reports')
    assert rep.status_code == 200 and b'Whole plan report (PDF)' in rep.data and b'2026-12' in rep.data

with app.app_context():
    c2 = login('o@x.com')
    assert c2.get('/study-planner/download/plan-report.pdf?uid=%d' % STU).status_code == 404
    assert c2.get('/study-planner/download/month.pdf?uid=%d' % STU).status_code == 404
print('planner reports checks passed')
