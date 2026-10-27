"""Smart Study Planner: level definitions, plan generation, progress statistics, EduPulse links and activity, reports and motivational quotes.

Levels (what the planner is built around):
  beginner  - building the base: lighter days, one chapter every 3 days, concept first, every concept followed by examples and a short check
  average   - steady progress: balanced learn / practise / revise, an error log, a mock every week
  top       - scoring higher: practice and timed work lead, daily error-log, two mocks a week, last weeks mock-heavy
Everything is rule-based and explainable: a student can see why each task is there.
"""
import csv
import io
import json
from collections import defaultdict
from datetime import date, datetime, timedelta

from flask import url_for

from app.extensions import db
from app.models_planner import SpPlan, SpTask

EXAMS = {'JEE': 'JEE Main / Advanced', 'UCEED': 'UCEED (design)', 'NEET': 'NEET UG (medicine)'}
LEVELS = ('beginner', 'average', 'top')

LEVEL_INFO = {
    'beginner': {'label': 'Beginner', 'tagline': 'Building the base', 'hours': 2.5, 'days_per_chapter': 3, 'mock_every': 14, 'mocks_per_week': 0,
                 'who': 'You are new to the syllabus, or your marks are below your target and basics feel shaky.',
                 'how': 'Short days, one subject at a time, concepts explained with examples before any practice. A mock only every two weeks, so confidence grows first.',
                 'mix': [('learn', .45), ('practice', .30), ('revise', .25)],
                 'example_day': [('6:30 - 7:15', 'Learn', 'Read one topic and write 5 key points in your own words'), ('7:15 - 7:30', 'Break', 'Walk, water, no phone'),
                                 ('17:00 - 17:50', 'Practice', '8 easy questions on the same topic; check each answer at once'), ('20:00 - 20:30', 'Revise', 'Re-read your 5 key points; fix one mistake')]},
    'average': {'label': 'Average', 'tagline': 'Steady progress', 'hours': 4.5, 'days_per_chapter': 2, 'mock_every': 7, 'mocks_per_week': 1,
                'who': 'You know most of the syllabus but your scores are uneven or you lose marks to slips and weak chapters.',
                'how': 'Balanced days of learning, practice and revision, a daily error log, and a weekly mock reviewed in full.',
                'mix': [('learn', .30), ('practice', .35), ('revise', .20), ('error', .15)],
                'example_day': [('6:00 - 7:00', 'Learn', 'New chapter: read, then solve the worked examples yourself'), ('17:00 - 18:30', 'Practice', '20 mixed questions, timed; mark the ones you guessed'),
                                ('19:30 - 20:15', 'Revise', 'Yesterday\'s chapter: formulas, diagrams, short quiz'), ('21:00 - 21:25', 'Error log', 'Write each mistake, the reason and the fix')]},
    'top': {'label': 'Top scorer', 'tagline': 'Scoring higher', 'hours': 6.5, 'days_per_chapter': 1.5, 'mock_every': 4, 'mocks_per_week': 2,
            'who': 'You have finished most of the syllabus and want to move from good to excellent: accuracy, speed and rank.',
            'how': 'Practice and timed work lead the day, a short fast learn block for gaps, a daily error log, two mocks a week and mock-heavy final weeks.',
            'mix': [('learn', .15), ('practice', .45), ('revise', .20), ('error', .20)],
            'example_day': [('5:30 - 6:15', 'Learn', 'Fast pass on one weak chapter; skip what you already know'), ('16:30 - 18:30', 'Practice', '35 hard questions in two timed sets; rate your confidence on each'),
                            ('19:30 - 20:30', 'Revise', 'Formula sheet, then retry yesterday\'s wrong questions'), ('21:00 - 21:30', 'Error log', 'Sort mistakes: concept, careless, guess; plan the fix')]},
}

TASK_TYPES = {
    'learn': {'label': 'Learn', 'colour': '#0E3A8A', 'how': 'Read or watch one topic, then close the book and write the key points in your own words. If you cannot explain it simply, read it again.',
              'example': 'Example: Kinematics. Write v = u + at in words ("final speed = starting speed + acceleration x time"), then solve 2 worked examples without looking at the answer.'},
    'practice': {'label': 'Practice', 'colour': '#FF6B0A', 'how': 'Solve questions on the topic you just learned. Check every answer straight away, mark the ones you guessed, and rate your confidence.',
                 'example': 'Example: 20 questions on Kinematics. 15 right, but 6 of those were guesses: revise those 6 as if they were wrong.'},
    'revise': {'label': 'Revise', 'colour': '#1F8B5C', 'how': 'Go back to an earlier chapter for 20 to 40 minutes: formulas, diagrams, a short self-quiz. Spaced revision (after 1, 7 and 30 days) is what makes it stick.',
               'example': 'Example: Monday you studied Laws of Motion. On Tuesday, Sunday and next month you spend 20 minutes on it again.'},
    'mock': {'label': 'Mock test', 'colour': '#C23A3A', 'how': 'Sit a full or half paper at exam time, in exam conditions. The real work is the review afterwards: spend at least as long on review as on the test.',
             'example': 'Example: score 140/300. Review shows 30 marks lost to guesses and 20 to careless slips. Next week\'s plan targets exactly those.'},
    'error': {'label': 'Error log', 'colour': '#8A4B00', 'how': 'For every wrong or guessed question write three things: what you did, why it was wrong (concept / careless / guess) and the fix. Review the log weekly.',
              'example': 'Example: "Used wrong sign for work done by gas. Reason: careless. Fix: write the sign convention at the top of every thermodynamics question."'},
    'rest': {'label': 'Rest', 'colour': '#5A6278', 'how': 'A planned rest day is part of the plan. Sleep, exercise, family time. Rested students remember more.', 'example': 'Example: Sunday. Light 20-minute review of the week if you want, then switch off.'},
}

NEET_SUBJECTS = {
    'Physics': ['Units and measurement', 'Kinematics', 'Laws of motion', 'Work, energy and power', 'Rotational motion', 'Gravitation', 'Properties of matter', 'Thermodynamics and kinetic theory',
                'Oscillations and waves', 'Electrostatics', 'Current electricity', 'Magnetism and EMI', 'Optics', 'Modern physics'],
    'Chemistry': ['Mole concept', 'Atomic structure', 'Chemical bonding', 'Thermodynamics', 'Equilibrium', 'Electrochemistry', 'Chemical kinetics', 'Periodic table', 'Coordination compounds',
                  'General organic chemistry', 'Hydrocarbons', 'Biomolecules'],
    'Biology': ['Diversity of living organisms', 'Cell structure and function', 'Plant physiology', 'Human physiology', 'Reproduction', 'Genetics and evolution', 'Ecology', 'Biotechnology'],
}

QUOTES = [
    'Small steps every day beat big plans you never start.', 'You do not have to be perfect today. You only have to begin.', 'A tired day studied is still a day ahead of a day skipped.',
    'Every question you get wrong now is a mark you will not lose in the exam.', 'Consistency is quiet. It looks like ordinary days, repeated.', 'Your plan is a promise to your future self. Keep it small, keep it daily.',
    'Confidence is built the same way as marks: one honest practice session at a time.', 'Do not compare your chapter 1 with someone else\'s chapter 20.', 'Progress is not a straight line. Come back after a bad day and continue.',
    'The best time to start was earlier. The second best time is the next 25 minutes.', 'Understanding beats memorising: explain it aloud as if teaching a friend.', 'Rest is part of the plan, not a break from it.',
    'You are not behind. You are exactly where today\'s effort puts you, and tomorrow can be better.', 'A mistake you write in your error log is a mistake you will not repeat.', 'Focus for 25 minutes. Then stop and breathe. Then again.',
    'Marks come from habits you can keep, not from nights you cannot repeat.', 'Ask the question you are afraid is silly. Someone else needs the answer too.', 'Today\'s hard chapter is next month\'s easy one.',
    'Good students ask what they got wrong. Great students ask why.', 'Switch off one distraction today and see what you finish.', 'Finish the task you planned, then enjoy the rest of the evening.',
    'Your mentor can only help with what you show them. Share the messy notes too.', 'Sleep is the cheapest revision technique there is.', 'You are building a skill, not just preparing for a day.',
    'Even a 15-minute session counts. Zero never does.', 'Look at how far you have come, then take the next step.', 'Doubt is normal. Practice is how you answer it.', 'The syllabus is big. A single day is small. Win the day.',
    'Be kind to yourself and strict with your schedule.', 'When you feel stuck, change the topic, not the goal.', 'Every expert was once a beginner who kept going.', 'Do the hard thing first; the rest of the day gets lighter.',
    'Write your goal where you can see it. Then do one thing toward it today.', 'A calm mind solves faster than a worried one.', 'Revise before you forget, not after.', 'Do not wait to feel ready. Start and let readiness catch up.',
    'You do not need motivation every day. You need a plan and a first step.', 'Celebrate a finished week. You earned it.', 'Mocks are practice for the real day, not a verdict on you.',
    'If you can explain your mistake, you are already fixing it.', 'Hard work is invisible until the result day. Keep going anyway.',
]

TIME_SLOT = {'learn': 'Morning', 'practice': 'Afternoon', 'revise': 'Evening', 'error': 'Night', 'mock': 'Morning', 'rest': 'All day'}
LINKS = {'reinforce': ('EduPulse Reinforcement', 'reinforce.home'), 'pulse': ('EduPulse-UCEED practice', 'pulse.home'), 'jee_mock': ('EduPulse-JEE mock centre', 'pulse_jee.home'),
         'uceed_mock': ('UCEED mock centre', 'pulse.mock_home')}


def today():
    return (datetime.utcnow() + timedelta(hours=5, minutes=30)).date()


def quote_of_the_day(d=None):
    d = d or today()
    return QUOTES[d.toordinal() % len(QUOTES)]


def quote_of_the_week(d=None):
    d = d or today()
    y, w, _ = d.isocalendar()
    return QUOTES[(y * 53 + w) % len(QUOTES)], '%d-W%02d' % (y, w)


# ---- plan generation -------------------------------------------------------------------------------------------------------------------------------
def subjects_and_chapters(exam):
    """{subject: [chapter, ...]} in teaching order. JEE and UCEED come from the Reinforcement taxonomy, NEET from the indicative list above."""
    if exam == 'NEET':
        return {k: list(v) for k, v in NEET_SUBJECTS.items()}
    from app.models_reinforce import RfTaxonomy
    out = defaultdict(list)
    for t in RfTaxonomy.query.filter_by(exam=exam).order_by(RfTaxonomy.id).all():
        out[t.subject].append(t.chapter)
    return dict(out)


def link_for(exam, task_type, student_on_roster):
    if task_type == 'mock':
        return {'JEE': 'jee_mock', 'UCEED': 'uceed_mock'}.get(exam)
    if task_type in ('practice', 'error'):
        if exam == 'JEE':
            return 'reinforce' if student_on_roster else 'jee_mock'
        if exam == 'UCEED':
            return 'pulse'
    return None


def _minutes(total, share, floor=15):
    return max(floor, int(round(total * share / 5.0)) * 5)


def generate_plan(user, exam, level, start, weeks, exam_date=None, hours=None, focus=None, mentor_id=None, created_by=None, title=None):
    """Create a plan with a task for every study day. Rule: one subject per day in rotation; a chapter lasts `days_per_chapter` days; Sunday is rest;
    a weekly (or two-weekly for beginners) mock on Saturday; with an exam date the last 2 weeks are mock-heavy for average and top students."""
    info = LEVEL_INFO[level]
    hours = float(hours or info['hours'])
    total = int(hours * 60)
    subs = subjects_and_chapters(exam)
    if not subs:
        raise ValueError('no syllabus for this exam yet')
    names = list(subs)
    on_roster = False
    try:
        from app.models_reinforce import RfStudent
        on_roster = RfStudent.query.filter_by(user_id=user.id, active=True).first() is not None
    except Exception:
        pass
    focus = [f for f in (focus or []) if f]
    plan = SpPlan(user_id=user.id, mentor_id=mentor_id, created_by=created_by or user.id, title=title or '%s plan (%s)' % (EXAMS[exam].split(' ')[0], info['label']), exam=exam, level=level,
                  start_date=start, weeks=weeks, exam_date=exam_date, hours_per_day=hours, focus_json=json.dumps(focus))
    db.session.add(plan)
    db.session.flush()
    pointer = {s: 0.0 for s in names}
    last = {s: None for s in names}
    n_days = weeks * 7
    for i in range(n_days):
        d = start + timedelta(days=i)
        week_no = i // 7
        weeks_left = ((exam_date - d).days // 7) if exam_date else None
        final = exam_date is not None and weeks_left is not None and 0 <= weeks_left < 2 and level != 'beginner'
        if exam_date and d > exam_date:
            break
        if d.weekday() == 6:                                                       # Sunday
            db.session.add(SpTask(plan_id=plan.id, day=d, task_type='rest', title='Rest day: sleep well, light 20-minute review if you like', minutes=0, subject=None))
            continue
        subj = names[i % len(names)]
        chapters = subs[subj]
        if focus and any(c in chapters for c in focus) and i % 4 == 0:             # stress a chapter the student asked for
            fc = [c for c in focus if c in chapters]
            chapter = fc[(i // 4) % len(fc)]
        else:
            chapter = chapters[int(pointer[subj]) % len(chapters)]
            pointer[subj] += 1.0 / info['days_per_chapter']               # a chapter lasts `days_per_chapter` study days of that subject
        mock_day = d.weekday() == 5 and (level != 'beginner' or week_no % 2 == 1)
        two_mock = level == 'top' and d.weekday() == 2
        if mock_day or two_mock or (final and d.weekday() in (1, 3, 5)):
            mt = max(60, min(total, 180))
            db.session.add(SpTask(plan_id=plan.id, day=d, task_type='mock', title='Mock test (%s) and full review' % ('half paper' if level == 'beginner' else 'timed'), minutes=mt, subject=None,
                                  link_kind=link_for(exam, 'mock', on_roster), note='Review time should be at least as long as the test.'))
            remaining = max(0, total - mt)
            if remaining < 30:
                continue
            total_today = remaining
        else:
            total_today = total
        for tt, share in info['mix']:
            if tt == 'error' and level == 'average' and d.weekday() not in (1, 3, 5):
                continue
            mins = _minutes(total_today, share)
            if tt == 'revise' and last[subj]:
                title_ = 'Revise: %s (formulas, diagrams, 5-question quiz)' % last[subj]
                ch = last[subj]
            else:
                ch = chapter
                title_ = {'learn': 'Learn: %s (read, write 5 key points, solve 2 worked examples)', 'practice': 'Practise: %s (check each answer, rate your confidence)',
                          'revise': 'Revise: %s (formulas and quick quiz)', 'error': 'Error log: %s (write mistake, reason, fix)'}[tt] % ch
            db.session.add(SpTask(plan_id=plan.id, day=d, subject=subj, chapter=ch, task_type=tt, title=title_, minutes=mins, link_kind=link_for(exam, tt, on_roster)))
        last[subj] = chapter
    db.session.commit()
    return plan


def add_suggested_revision(plan, weak, start=None, limit=3):
    """Add revision tasks (linked to EduPulse where the exam has it) for weak chapters, spread over the next days. Returns the number added."""
    start = start or today()
    n = 0
    for k, (subject, chapter) in enumerate(weak[:limit]):
        d = start + timedelta(days=k + 1)
        if SpTask.query.filter_by(plan_id=plan.id, day=d, chapter=chapter, added_by='suggestion').first():
            continue
        db.session.add(SpTask(plan_id=plan.id, day=d, subject=subject, chapter=chapter, task_type='revise', title='Revise (suggested): %s, flagged as weak in EduPulse' % chapter, minutes=40,
                              link_kind=link_for(plan.exam, 'practice', True), added_by='suggestion', note='Added because your EduPulse practice shows this chapter needs work.'))
        n += 1
    db.session.commit()
    return n


# ---- EduPulse links and activity ------------------------------------------------------------------------------------------------------------------
def link_url(kind):
    if kind in LINKS:
        try:
            return LINKS[kind][0], url_for(LINKS[kind][1])
        except Exception:
            return None
    return None


def weak_chapters(user_id, exam):
    """[(subject, chapter)] that EduPulse practice marks as priority or needing revision (Reinforcement for JEE/UCEED)."""
    try:
        from app.models_reinforce import RfStudent
        from app.services import reinforce as rf
        rs = RfStudent.query.filter_by(user_id=user_id, active=True).first()
        if rs and exam in ('JEE', 'UCEED'):
            return [(r['subject'], r['chapter']) for r in rf.chapter_table(rs.id, exam) if r['status'] in ('priority', 'revise')]
    except Exception:
        pass
    return []


def edupulse_activity(user_id, since, until=None):
    """Counts of EduPulse work in the period: Reinforcement answers, UCEED practice answers, mock tests."""
    until = until or (datetime.utcnow() + timedelta(days=1))
    out = {'reinforce_answers': 0, 'pulse_answers': 0, 'mocks': 0}
    try:
        from app.models_reinforce import RfAttempt, RfStudent
        rs = RfStudent.query.filter_by(user_id=user_id).first()
        if rs:
            out['reinforce_answers'] = RfAttempt.query.filter(RfAttempt.student_id == rs.id, RfAttempt.answered_at >= since, RfAttempt.answered_at < until).count()
    except Exception:
        pass
    try:
        from app.models_pulse import PulseAnswer, PulseAttempt, PulseJeeResult, PulseMockResult
        out['pulse_answers'] = (db.session.query(db.func.count(PulseAnswer.id)).join(PulseAttempt, PulseAttempt.id == PulseAnswer.attempt_id)
                                .filter(PulseAttempt.user_id == user_id, PulseAttempt.submitted_at >= since, PulseAttempt.submitted_at < until, PulseAnswer.chosen != None).scalar() or 0)  # noqa: E711
        out['mocks'] = (PulseMockResult.query.filter(PulseMockResult.user_id == user_id, PulseMockResult.finished_at >= since, PulseMockResult.finished_at < until).count()
                        + PulseJeeResult.query.filter(PulseJeeResult.user_id == user_id, PulseJeeResult.finished_at >= since, PulseJeeResult.finished_at < until).count())
    except Exception:
        pass
    out['questions'] = out['reinforce_answers'] + out['pulse_answers']
    return out


# ---- statistics and reports ---------------------------------------------------------------------------------------------------------------------------
def week_start(d):
    return d - timedelta(days=d.weekday())


def plan_stats(plan, upto=None):
    """Everything the dashboards and reports show for one plan, up to `upto` (default today)."""
    upto = upto or today()
    tasks = plan.tasks.order_by(SpTask.day, SpTask.id).all()
    work = [t for t in tasks if t.task_type != 'rest']
    due = [t for t in work if t.day <= upto]
    done = [t for t in work if t.status == 'done']
    wk0 = week_start(upto)
    this_week = [t for t in work if wk0 <= t.day < wk0 + timedelta(days=7)]
    wk_due = [t for t in this_week if t.day <= upto]
    by_subj, by_type = defaultdict(lambda: {'planned': 0, 'done': 0, 'tasks': 0, 'completed': 0}), defaultdict(lambda: {'planned': 0, 'done': 0, 'tasks': 0, 'completed': 0})
    for t in due:
        for bucket, key in ((by_subj, t.subject or 'Mock / general'), (by_type, t.task_type)):
            b = bucket[key]
            b['planned'] += t.minutes or 0
            b['tasks'] += 1
            if t.status == 'done':
                b['done'] += t.minutes_done or t.minutes or 0
                b['completed'] += 1
    days_done = {t.day for t in done}
    streak, d = 0, upto
    if d not in days_done:
        d -= timedelta(days=1)
    while d in days_done:
        streak += 1
        d -= timedelta(days=1)
    heat = {}
    for k in range(27, -1, -1):
        day = upto - timedelta(days=k)
        heat[day] = sum(1 for t in done if t.day == day)
    overdue = [t for t in due if t.status == 'todo' and t.day < upto]
    pct = lambda a, b: round(100 * a / b) if b else None
    return {'plan': plan, 'total': len(work), 'due': len(due), 'done': len(done), 'pct_due': pct(len([t for t in due if t.status == 'done']), len(due)), 'pct_all': pct(len(done), len(work)),
            'week_total': len(this_week), 'week_due': len(wk_due), 'week_done': len([t for t in this_week if t.status == 'done']),
            'week_pct': pct(len([t for t in this_week if t.status == 'done']), len(this_week)),
            'planned_min': sum(t.minutes or 0 for t in due), 'done_min': sum((t.minutes_done or t.minutes or 0) for t in due if t.status == 'done'),
            'by_subject': dict(by_subj), 'by_type': dict(by_type), 'streak': streak, 'heat': heat, 'overdue': overdue, 'today': [t for t in tasks if t.day == upto],
            'on_track': (pct(len([t for t in due if t.status == 'done']), len(due)) or 0) >= 70, 'last_done': max((t.done_at for t in done if t.done_at), default=None)}


def active_plan(user_id):
    return SpPlan.query.filter_by(user_id=user_id, status='active').order_by(SpPlan.id.desc()).first()


def summary_rows(plans):
    """One row per plan for cohort tables and CSV."""
    rows = []
    for p in plans:
        s = plan_stats(p)
        act = edupulse_activity(p.user_id, datetime.combine(week_start(today()), datetime.min.time()))
        rows.append({'plan': p, 'name': p.user.name, 'email': p.user.email, 'exam': p.exam, 'level': p.level, 'pct_due': s['pct_due'], 'week_pct': s['week_pct'], 'streak': s['streak'],
                     'overdue': len(s['overdue']), 'hours_done': round(s['done_min'] / 60, 1), 'hours_planned': round(s['planned_min'] / 60, 1), 'questions_week': act['questions'], 'mocks_week': act['mocks'],
                     'last_done': s['last_done'], 'on_track': s['on_track']})
    return rows


def rows_csv(rows):
    out = io.StringIO()
    w = csv.writer(out)
    w.writerow(['student', 'email', 'exam', 'level', 'plan', 'completion_to_date_pct', 'this_week_pct', 'streak_days', 'overdue_tasks', 'hours_done', 'hours_planned', 'edupulse_questions_this_week', 'mocks_this_week', 'last_activity', 'on_track'])
    for r in rows:
        w.writerow([r['name'], r['email'], r['exam'], r['level'], r['plan'].title, r['pct_due'] if r['pct_due'] is not None else '', r['week_pct'] if r['week_pct'] is not None else '', r['streak'], r['overdue'],
                    r['hours_done'], r['hours_planned'], r['questions_week'], r['mocks_week'], r['last_done'].strftime('%Y-%m-%d') if r['last_done'] else '', 'yes' if r['on_track'] else 'no'])
    return out.getvalue()


def tasks_csv(plan):
    out = io.StringIO()
    w = csv.writer(out)
    w.writerow(['date', 'subject', 'chapter', 'type', 'task', 'minutes_planned', 'minutes_done', 'status'])
    for t in plan.tasks.order_by(SpTask.day, SpTask.id).all():
        w.writerow([t.day.isoformat(), t.subject or '', t.chapter or '', t.task_type, t.title, t.minutes, t.minutes_done, t.status])
    return out.getvalue()


def level_quiz(answers):
    """Five answers each scored 0 (struggling) to 2 (strong). Returns a recommended level."""
    s = sum(max(0, min(2, int(a))) for a in answers)
    return 'beginner' if s <= 3 else 'average' if s <= 7 else 'top'


QUIZ = [
    ('How much of the syllabus have you completed once?', ['Less than a quarter', 'About half', 'Almost all of it']),
    ('In practice sets, how many of your answers are right?', ['Under 40%', '40 to 70%', 'Over 70%']),
    ('When you get a question wrong, what do you usually do?', ['Move on, I am not sure why', 'Look at the answer and note it', 'Find the reason and write it in an error log']),
    ('How do your timed mock scores compare with your target?', ['Far below', 'Close but uneven', 'At or above']),
    ('How many hours a day can you study regularly (besides school)?', ['Up to 2', '3 to 5', '6 or more']),
]
