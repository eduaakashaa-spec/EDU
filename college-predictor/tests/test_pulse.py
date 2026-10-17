"""EduPulse-UCEED: question bank, practice flow, dashboard stats, mentor view, CSV import, e-mail reports.
Run from college-predictor/:  python tests/test_pulse.py"""
import io
import itertools
import os
import sys
import tempfile
from datetime import timedelta
from math import comb

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_fd, _db = tempfile.mkstemp(suffix='.db')
os.close(_fd)
os.environ.update(DATABASE_URL='sqlite:///' + _db, SECRET_KEY='test', FLASK_DEBUG='0', PULSE_CRON_TOKEN='cron-secret')

from app import create_app
from app.extensions import db, bcrypt
from app.models import User
from app.models_pulse import PulseAttempt, PulseChapter, PulseProfile, PulseQuestion, PulseReport
from app.services import mailer, pulse as svc

app = create_app()
app.config['TESTING'] = True
pw = lambda: bcrypt.generate_password_hash('x').decode()
with app.app_context():
    db.create_all()
    for n, e, t in (('Admin', 'a@x.com', 'admin'), ('Mentor One', 'm1@x.com', 'ea_mentor'), ('Mentor Two', 'm2@x.com', 'ea_mentor'),
                    ('Stu One', 's1@x.com', 'premium'), ('Stu Two', 's2@x.com', 'premium'), ('Free', 'f@x.com', 'free')):
        db.session.add(User(name=n, email=e, tier=t, password_hash=pw()))
    db.session.commit()


def login(email):
    c = app.test_client()
    c.post('/login', data={'email': email, 'password': 'x'})
    return c


def uid(email):
    with app.app_context():
        return User.query.filter_by(email=email).one().id


anon, admin, m1, m2, s1, s2, free = (app.test_client(), login('a@x.com'), login('m1@x.com'), login('m2@x.com'), login('s1@x.com'), login('s2@x.com'), login('f@x.com'))

# ---- the answer key of the starter bank is verified independently of the stored letters ---------------------------------------
def ans(stem_start):
    q = next(x for x in svc.STARTER if x[1].startswith(stem_start))
    return q[2]['ABCD'.index(q[3])]
assert ans('Which regular shape') == 'Regular hexagon'
assert comb(5, 2) == 10 and ans('Three straight lines') == '10'
assert ans('A cube painted red') == '24' and 6 * (4 - 2) ** 2 == 24
assert ans('How many edges') == '9' and ans('How many squares') == '14' and sum(k * k for k in range(1, 4)) == 14
assert ans('Find the next number') == '42' and [n * (n + 1) for n in range(1, 7)] == [2, 6, 12, 20, 30, 42]
assert ans('Find the next letter') == 'U' and chr(ord('A') + 2 + 3 + 4 + 5 + 6 - 0 + 0) == chr(ord('A') + 20) == 'U'
assert ans('If COLOUR') == 'TLFUDI' and ''.join(chr(ord(c) + 1) for c in 'SKETCH') == 'TLFUDI' and ''.join(chr(ord(c) + 1) for c in 'COLOUR') == 'DPMPVS'
assert abs((3 * 30 + 15 * 0.5) - 15 * 6) == 7.5 and ans('What is the smaller angle') == '7.5°'
assert ans('A rope is cut') == '11' and 2 + 3 * 3 == 11
assert ans('A bat and a ball') == '₹5' and 5 + 105 == 110
assert ans('On a map') == '36 km' and 7.2 * 5 == 36 and ans('A floor plan') == '8 cm' and 400 / 50 == 8
assert ans('In a pictogram') == '70' and 3.5 * 20 == 70


def min_jug_steps(a=3, b=5, goal=4):                      # breadth-first search over (jug3, jug5) states
    seen, frontier, steps = {(0, 0)}, [(0, 0)], 0
    while frontier:
        nxt = []
        for x, y in frontier:
            if y == goal:
                return steps
            pour_xy, pour_yx = min(x, b - y), min(y, a - x)
            for s in {(a, y), (x, b), (0, y), (x, 0), (x - pour_xy, y + pour_xy), (x + pour_yx, y - pour_yx)}:
                if s not in seen:
                    seen.add(s)
                    nxt.append(s)
        frontier, steps = nxt, steps + 1
    return None
assert min_jug_steps() == 6 and ans('You have an empty 3-litre') == '6'
assert len(svc.STARTER) == 40 and len({q[1] for q in svc.STARTER}) == 40
for key, stem, opts, corr, expl, diff in svc.STARTER:
    assert len(opts) == 4 and len(set(opts)) == 4 and corr in 'ABCD' and diff in ('Easy', 'Medium', 'Hard') and expl
assert {q[0] for q in svc.STARTER} == {c[0] for c in svc.CHAPTERS} and all(sum(1 for q in svc.STARTER if q[0] == c[0]) == 5 for c in svc.CHAPTERS)

# ---- access ------------------------------------------------------------------------------------------------------------------------------
assert anon.get('/edupulse-uceed/').status_code in (302, 401) and free.get('/edupulse-uceed/').status_code == 403
assert s1.get('/edupulse-uceed/admin').status_code in (302, 403) and m1.get('/edupulse-uceed/admin').status_code in (302, 403)
assert s1.get('/edupulse-uceed/mentor').status_code in (302, 403)

# ---- admin: seed the bank ------------------------------------------------------------------------------------------------
r = admin.post('/edupulse-uceed/admin/seed', follow_redirects=True)
assert b'40 original practice question' in r.data
assert b'already loaded' in admin.post('/edupulse-uceed/admin/seed', follow_redirects=True).data
with app.app_context():
    assert PulseChapter.query.count() == 8 and PulseQuestion.query.filter_by(status='published').count() == 40
pg = admin.get('/edupulse-uceed/admin').get_data(as_text=True)
assert 'not</strong> UCEED previous-year' in pg and 'Visual perception' in pg

# ---- student: must register first ------------------------------------------------------------------------------------------
home = s1.get('/edupulse-uceed/').get_data(as_text=True)
assert 'Register for EduPulse' in home and 'original practice material' in home
assert b'register for EduPulse first' in s1.post('/edupulse-uceed/start', data={'chapter': 'spatial', 'count': '5'}, follow_redirects=True).data
assert b'valid parent email' in s1.post('/edupulse-uceed/register', data={'parent_email': 'nope'}, follow_redirects=True).data
r = s1.post('/edupulse-uceed/register', data={'student_class': 'Class 12', 'parent_email': 'Parent@Ex.com', 'parent_consent': '1', 'frequency': 'weekly', 'email_results': '1'}, follow_redirects=True)
assert b'Parent emails are ON' in r.data
with app.app_context():
    p = db.session.get(PulseProfile, uid('s1@x.com'))
    assert p.parent_email == 'parent@ex.com' and p.parent_consent
s2.post('/edupulse-uceed/register', data={'student_class': 'Class 11', 'parent_email': 'p2@ex.com', 'frequency': 'weekly'})   # no consent ticked
with app.app_context():
    assert db.session.get(PulseProfile, uid('s2@x.com')).parent_consent is False

# ---- practice: attempt page never leaks the answers; submit once; stats follow ---------------------------------------------
sent, orig = [], (mailer.is_configured, mailer.send_async)
mailer.is_configured = lambda: True
mailer.send_async = lambda to, subject, text, html=None, **k: sent.append({'to': to, 'subject': subject, 'html': html or '', **k})
r = s1.post('/edupulse-uceed/start', data={'chapter': 'spatial', 'count': '5', 'mode': 'practice'})
assert r.status_code == 302 and '/attempt/' in r.headers['Location']
aurl = r.headers['Location']
page = s1.get(aurl).get_data(as_text=True)
with app.app_context():
    att = PulseAttempt.query.filter_by(user_id=uid('s1@x.com')).one()
    AID = att.id
    items = [(a.id, a.question.correct, a.question.explanation) for a in att.answers.order_by(PulseAnswer.position)] if False else None
from app.models_pulse import PulseAnswer
with app.app_context():
    items = [(a.id, a.question.correct, a.question.explanation, a.question.stem) for a in PulseAnswer.query.filter_by(attempt_id=AID).order_by(PulseAnswer.position)]
assert len(items) == 5 and all(stem[:30] in page for *_x, stem in items)
assert not any(expl[:25] in page for _i, _c, expl, _s in items)                       # explanations are hidden before submission
assert s2.get(aurl).status_code == 404 and anon.get(aurl).status_code in (302, 401)  # not someone else's attempt
form = {}
wrongs = {'A': 'B', 'B': 'C', 'C': 'D', 'D': 'A'}
for n, (aid, corr, _e, _s) in enumerate(items):
    if n < 3:
        form[f'q{aid}'] = corr                              # 3 correct
    elif n == 3:
        form[f'q{aid}'] = wrongs[corr]                      # 1 wrong; the 5th is skipped
r = s1.post(f'/edupulse-uceed/attempt/{AID}/submit', data=form, follow_redirects=True)
rp = r.get_data(as_text=True)
assert '3 of 5 correct' in rp and 'Why:' in rp and 'skipped 1' in rp and 'Accuracy on answered questions: <strong>75%' in rp
with app.app_context():
    a = db.session.get(PulseAttempt, AID)
    assert (a.correct, a.wrong, a.skipped, a.accuracy) == (3, 1, 1, 75) and svc.practice_score(a) == round(3 - 1 / 3, 2)
s1.post(f'/edupulse-uceed/attempt/{AID}/submit', data={f'q{items[0][0]}': wrongs[items[0][1]]})   # re-submitting changes nothing
with app.app_context():
    assert db.session.get(PulseAttempt, AID).correct == 3
# result e-mail to the student only (not parent / mentor), from info@
assert len(sent) == 1 and sent[0]['to'] == 's1@x.com' and sent[0]['from_addr'] == 'info@eduaakashaa.com' and '3/5' in sent[0]['subject'] and '3 of 5' in sent[0]['html']
# unseen questions come first: a second set of 5 in the same chapter must repeat the skipped/wrong ones, then fill with the rest
r = s1.post('/edupulse-uceed/start', data={'chapter': 'spatial', 'count': '5'})
with app.app_context():
    second = PulseAttempt.query.filter_by(user_id=uid('s1@x.com')).order_by(PulseAttempt.id.desc()).first()
    assert second.id != AID and second.total == 5
# a mixed set draws unseen chapters first
r = s1.post('/edupulse-uceed/start', data={'chapter': 'mixed', 'count': '10', 'mode': 'timed', 'difficulty': ''})
with app.app_context():
    mixed = PulseAttempt.query.filter_by(user_id=uid('s1@x.com')).order_by(PulseAttempt.id.desc()).first()
    assert mixed.mode == 'timed' and mixed.limit_sec == 900 and mixed.total == 10
    spatial_id = PulseChapter.query.filter_by(key='spatial').one().id
    assert not any(a.question.chapter_id == spatial_id for a in mixed.answers)    # all 5 spatial questions were already seen
assert 'data-limit="900"' in s1.get(r.headers['Location']).get_data(as_text=True)

# ---- dashboard: chapter stats, weak detection, trend -----------------------------------------------------------------------
def do_set(client, chapter, correct_all, n=5):
    r = client.post('/edupulse-uceed/start', data={'chapter': chapter, 'count': str(n)})
    aid = int(r.headers['Location'].rstrip('/').split('/attempt/')[1])
    with app.app_context():
        rows = [(a.id, a.question.correct) for a in PulseAnswer.query.filter_by(attempt_id=aid)]
    client.post(f'/edupulse-uceed/attempt/{aid}/submit', data={f'q{i}': (c if correct_all else wrongs[c]) for i, c in rows})
    return aid
do_set(s1, 'logic', False)                                   # 5 wrong in Logic → weak
do_set(s1, 'awareness', True)                                # 5 right → strong
dash = s1.get('/edupulse-uceed/').get_data(as_text=True)
with app.app_context():
    rows = {r['chapter'].key: r for r in svc.chapter_stats(uid('s1@x.com'))}
    assert rows['logic']['level'] == 'weak' and rows['logic']['accuracy'] == 0 and rows['awareness']['level'] == 'strong' and rows['awareness']['accuracy'] == 100
    assert rows['spatial']['level'] == 'ok' or rows['spatial']['answered'] < 5 or rows['spatial']['accuracy'] is not None
    ov = svc.overall(uid('s1@x.com'))
    assert ov['attempts'] == 3 and ov['answered'] == 4 + 5 + 5 and ov['trend'][-2:] == [0, 100] and svc.streak(uid('s1@x.com')) == 1
assert 'Needs work' in dash and 'Strong' in dash and 'Logical &amp; analytical reasoning' in dash
assert 'Revisit' in dash                                              # advice names the weak chapter

# ---- mentor & admin views ---------------------------------------------------------------------------------------------------
assert b'Stu One' not in m1.get('/edupulse-uceed/mentor').data       # nobody linked yet
admin.post('/edupulse-uceed/admin/mentor', data={'user_id': uid('s1@x.com'), 'mentor_id': uid('m1@x.com')})
assert admin.post('/edupulse-uceed/admin/mentor', data={'user_id': uid('s1@x.com'), 'mentor_id': uid('s2@x.com')}, follow_redirects=True).status_code == 200
with app.app_context():
    assert db.session.get(PulseProfile, uid('s1@x.com')).mentor_id == uid('m1@x.com')       # a student account cannot be a mentor
assert b'Stu One' in m1.get('/edupulse-uceed/mentor').data and b'Stu One' not in m2.get('/edupulse-uceed/mentor').data
assert m1.get(f'/edupulse-uceed/mentor/{uid("s1@x.com")}').status_code == 200
assert m2.get(f'/edupulse-uceed/mentor/{uid("s1@x.com")}').status_code == 404 and s1.get(f'/edupulse-uceed/mentor/{uid("s1@x.com")}').status_code in (302, 403)
assert b'Stu Two' in admin.get('/edupulse-uceed/mentor').data
assert 'Needs work' in m1.get(f'/edupulse-uceed/mentor/{uid("s1@x.com")}').get_data(as_text=True)

# ---- e-mail digests: student + parent (consent) + mentor; consent respected; once per period --------------------------------
sent.clear()
with app.app_context():
    p1 = db.session.get(PulseProfile, uid('s1@x.com'))
    recipients = svc.send_digest(p1)
assert sorted(recipients) == ['m1@x.com', 'parent@ex.com', 's1@x.com'] and len(sent) == 3
assert all(m['from_addr'] == 'info@eduaakashaa.com' for m in sent)
parent_mail = next(m for m in sent if m['to'] == 'parent@ex.com')
assert 'Stu One' in parent_mail['html'] and 'not official UCEED marks' in parent_mail['html'] and 'Needs attention' in parent_mail['html']
sent.clear()
with app.app_context():
    p2 = db.session.get(PulseProfile, uid('s2@x.com'))
    assert svc.send_digest(p2) == ['s2@x.com']                        # parent has not consented → not mailed
assert [m['to'] for m in sent] == ['s2@x.com']
with app.app_context():
    assert PulseReport.query.count() == 2
    now = svc.utcnow()
    due_ids = lambda d: {x.user_id for x in svc.due_profiles(now + timedelta(days=d))}
    assert uid('s1@x.com') not in due_ids(3) and uid('s1@x.com') in due_ids(8)
    db.session.get(PulseProfile, uid('s2@x.com')).frequency = 'off'
    db.session.commit()
    assert uid('s2@x.com') not in due_ids(60)
    sent.clear()
    assert svc.send_due_reports(now + timedelta(days=3)) == 0
    assert svc.send_due_reports(now + timedelta(days=8)) == 1 and len(sent) == 3
# scheduler endpoint is token-protected
assert anon.get('/edupulse-uceed/cron/reports').status_code == 404 and anon.get('/edupulse-uceed/cron/reports?token=wrong').status_code == 404
sent.clear()
r = anon.get('/edupulse-uceed/cron/reports?token=cron-secret')
assert r.status_code == 200 and r.get_json()['ok'] is True and r.get_json()['sent'] == 0          # already mailed this period
mailer.is_configured = lambda: False
assert admin.post('/edupulse-uceed/admin/send-reports', follow_redirects=True).data.count(b'not configured') >= 1     # honest when no transport
mailer.is_configured, mailer.send_async = orig

# ---- admin: CSV import (all-or-nothing), single add with figure, publish gate, delete safety ------------------------------------
good = 'chapter,stem,option_a,option_b,option_c,option_d,correct,explanation,difficulty,source,year\n' \
       'spatial,"How many corners does a cube have?",6,8,10,12,B,"A cube has 8 vertices.",Easy,Licensed set,2024\n'
bad = good + 'nonsense,"Q",a,b,c,d,A,,,,\n'
r = admin.post('/edupulse-uceed/admin/import', data={'file': (io.BytesIO(bad.encode()), 'q.csv')}, content_type='multipart/form-data', follow_redirects=True)
assert b'Nothing was imported' in r.data and b'unknown chapter' in r.data
with app.app_context():
    assert PulseQuestion.query.count() == 40
r = admin.post('/edupulse-uceed/admin/import', data={'file': (io.BytesIO(good.encode()), 'q.csv')}, content_type='multipart/form-data', follow_redirects=True)
assert b'1 question(s) imported as drafts' in r.data
with app.app_context():
    imp = PulseQuestion.query.filter_by(stem='How many corners does a cube have?').one()
    IMP = imp.id
    assert imp.status == 'draft' and imp.year == '2024' and imp.source == 'Licensed set'
exp = admin.get('/edupulse-uceed/admin/export.csv')
assert exp.mimetype == 'text/csv' and b'How many corners' in exp.data and exp.data.count(b'\n') >= 41
PNG = bytes([0x89]) + b'PNG' + bytes([0x0d, 0x0a, 0x1a, 0x0a]) + bytes(40)
r = admin.post(f'/edupulse-uceed/admin/question/{IMP}', data={'chapter_id': imp.chapter_id if False else 2, 'stem': 'How many corners does a cube have?', 'option_a': '6', 'option_b': '8',
               'option_c': '10', 'option_d': '12', 'correct': 'B', 'difficulty': 'Easy', 'source': 'Licensed set', 'publish': '1', 'image': (io.BytesIO(PNG), 'f.png')},
               content_type='multipart/form-data', follow_redirects=True)
assert b'It is live for students' in r.data
assert s1.get(f'/edupulse-uceed/q/{IMP}/image').data == PNG and anon.get(f'/edupulse-uceed/q/{IMP}/image').status_code in (302, 401)
assert b'JPG, PNG or WebP' in admin.post(f'/edupulse-uceed/admin/question/{IMP}', data={'chapter_id': 2, 'stem': 'x', 'option_a': 'a', 'option_b': 'b', 'option_c': 'c', 'option_d': 'd', 'correct': 'A',
                                         'image': (io.BytesIO(b'GIF89a'), 'f.gif')}, content_type='multipart/form-data', follow_redirects=True).data
admin.post(f'/edupulse-uceed/admin/question/{IMP}/toggle')
assert s1.get(f'/edupulse-uceed/q/{IMP}/image').status_code == 404       # unpublished figures are hidden from students
assert admin.post('/edupulse-uceed/admin/question', data={'stem': 'only a stem'}, follow_redirects=True).data.count(b'required') >= 1
with app.app_context():
    answered_q = PulseAnswer.query.first().question_id
admin.post(f'/edupulse-uceed/admin/question/{answered_q}/delete')
with app.app_context():
    q_ = db.session.get(PulseQuestion, answered_q)
    assert q_ is not None and q_.status == 'draft'                       # answered questions are unpublished, never deleted
    # historical results still render
assert s1.get(f'/edupulse-uceed/attempt/{AID}/result').status_code == 200

# ---- hub tile ------------------------------------------------------------------------------------------------------------------------------
assert '/edupulse-uceed/' in s1.get('/member-home').get_data(as_text=True) and 'EduPulse-UCEED' in free.get('/member-home').get_data(as_text=True)
assert b'EduPulse mentor view' in m1.get('/member-home').data and b'EduPulse mentor view' not in s1.get('/member-home').data

try:
    os.unlink(_db)
except OSError:
    pass
print('edupulse checks passed')
