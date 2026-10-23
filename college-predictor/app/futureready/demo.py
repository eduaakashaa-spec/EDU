"""Clearly-labelled demonstration workspace. Demo profiles are flagged `demo=True`, named "Demo …", use *.test e-mail addresses, and are excluded from exports.
Passwords are random and shown once to the administrator who creates the workspace."""
import json
import random
import secrets
from datetime import date, timedelta

from app.extensions import bcrypt, db
from app.futureready import engine, reco, reports
from app.futureready.models import (FrAction, FrAssessment, FrAttempt, FrBranch, FrGoal, FrNote, FrParentLink, FrProfile, FrProject, FrSession, FrShortlist, _now)
from app.models import User

STRONG = {'math', 'numerical', 'logical', 'patterns', 'data', 'sci_reason', 'science', 'reading'}
WEAK = {'spatial', 'decomposition', 'verify', 'ai_use'}


def _answer(q, rng):
    if q.qtype == 'mcq':
        p = 0.9 if q.skill in STRONG else 0.3 if q.skill in WEAK else 0.65
        if rng.random() < p:
            return q.answer
        wrong = [i for i in range(len(q.options)) if i != q.answer]
        return rng.choice(wrong)
    if q.qtype == 'multi':
        return q.answer if q.answer is not None and rng.random() < 0.5 else ([0, 1, 2][:3] if q.answer is None else [0])
    if q.qtype == 'likert':
        base = 4 if q.skill in ('tech', 'puzzle', 'build', 'investigate', 'curiosity', 'analytical') else 2 if q.skill in ('revision', 'planning', 'time') else 3
        return max(1, min(5, base + rng.choice([-1, 0, 0, 1])))
    if q.qtype == 'choice':
        return rng.choice(range(len(q.options)))
    return 'Sample answer written for demonstration purposes.'


def _fill(p, key, rng, audience='student', set_key=None):
    a = FrAssessment.query.filter_by(key=key).first()
    if not a:
        return None
    n = FrAttempt.query.filter_by(profile_id=p.id, assessment_id=a.id, audience=audience, set_key=set_key).count()
    at = FrAttempt(profile_id=p.id, assessment_id=a.id, audience=audience, set_key=set_key, attempt_no=n + 1, version=a.version, status='submitted', submitted_at=_now())
    db.session.add(at)
    db.session.flush()
    resp = {q.code: _answer(q, rng) for q in engine.questions_for(at)}
    at.responses_json = json.dumps(resp)
    engine.score_attempt(at)
    return at


def create_demo(admin):
    engine.seed_content()
    rng = random.Random(8)
    tag = secrets.token_hex(2)
    pw_s, pw_p = secrets.token_urlsafe(9), secrets.token_urlsafe(9)
    su = User(name='Demo Aarav (sample student)', email=f'demo.student.{tag}@futureready.test', password_hash=bcrypt.generate_password_hash(pw_s).decode(), tier='free')
    pu = User(name='Demo Parent (sample)', email=f'demo.parent.{tag}@futureready.test', password_hash=bcrypt.generate_password_hash(pw_p).decode(), tier='free')
    db.session.add_all([su, pu])
    db.session.flush()
    p = FrProfile(user_id=su.id, mentor_id=None, grade=9, curriculum='CBSE', school='Sample School (demo)', interests_text='Robots, drawing and cricket statistics (sample).',
                  learning_prefs='Hands-on projects, Watching videos', student_goals='Understand maths better and build a robot (sample).', parent_goals='Build confidence and good study habits (sample).',
                  tier='Standard', meetings_per_month=2, onboarding_step=10, onboarding_done_at=_now(), consent_at=_now(), consent_by='Demo Parent (sample)', demo=True)
    db.session.add(p)
    db.session.flush()
    db.session.add(FrParentLink(profile_id=p.id, parent_id=pu.id))
    for k in ('academic', 'habits', 'reasoning', 'per', 'interests', 'creativity', 'ai_literacy', 'communication', 'selfmgmt', 'alignment', 'eng_interest', 'entrance_check'):
        _fill(p, k, rng)
    _fill(p, 'alignment', rng, 'parent')
    _fill(p, 'sampler', rng, set_key='numerical:1')
    _fill(p, 'sampler', rng, set_key='spatial:1')
    cr = engine.latest_attempt(p.id, 'creativity')
    if cr:
        engine.rate_rubric(cr, {'understand': 3, 'ideas': 3, 'creativity': 4, 'practical': 2, 'reasoning': 3, 'reflection': 2, 'feedback': 'Lovely original idea (demo feedback). Next: test it with real materials.'})
    g = FrGoal(profile_id=p.id, title='Raise my spatial-reasoning practice score', metric='Sampler spatial level 2, % correct', baseline=33, target=67, current=33, unit='%',
               due_date=date.today() + timedelta(days=60), set_by='mentor')
    db.session.add(g)
    db.session.flush()
    db.session.add_all([
        FrAction(profile_id=p.id, goal_id=g.id, title='Build a paper bridge and test two designs', owner='student', due_date=date.today() + timedelta(days=10), source='mentor', why='Hands-on practice for spatial reasoning'),
        FrAction(profile_id=p.id, title='Share what you noticed at the next session', owner='parent', due_date=date.today() + timedelta(days=14), source='mentor'),
        FrAction(profile_id=p.id, title='Prepare the monthly review', owner='mentor', due_date=date.today() + timedelta(days=5), source='mentor'),
        FrAction(profile_id=p.id, title='Weekly reflection (2 entries)', owner='student', status='Done', completed_at=_now(), source='recommendation')])
    db.session.add_all([
        FrNote(profile_id=p.id, kind='session', basis='mentor', visibility='mentor', body='PRIVATE (demo): Aarav is quiet in groups but lights up when building things. Check confidence in the next session.'),
        FrNote(profile_id=p.id, kind='observation', basis='mentor', visibility='shared', body='Great curiosity about how things work (demo). Keep building small projects.'),
        FrSession(profile_id=p.id, kind='initial', title='Initial session (demo)', held_at=_now() - timedelta(days=7), status='Held', summary='Reviewed onboarding and agreed first goals (demo).'),
        FrSession(profile_id=p.id, kind='monthly', title='Monthly session (demo)', planned_at=_now() + timedelta(days=7), status='Planned', agenda='Review actions; plan next project.'),
        FrProject(profile_id=p.id, title='Line-following robot (demo)', description='Sample project.', status='In progress')])
    for k in ('mechatronics', 'cse'):
        b = FrBranch.query.filter_by(key=k).first()
        if b:
            db.session.add(FrShortlist(profile_id=p.id, branch_id=b.id, note='Looks exciting (demo).'))
    db.session.commit()
    for r in reco.generate(p):
        r.approved = True
    db.session.commit()
    rep = reports.save(p, 'starting_point', admin)
    rep.status = 'Shared'
    rep.shared_at = _now()
    db.session.commit()
    return f'Demo workspace created. Student login {su.email} / {pw_s}; parent login {pp(pu)} / {pw_p}. These sample accounts are labelled demo and are excluded from exports. Save the passwords now: they are not shown again.'


def pp(u):
    return u.email
