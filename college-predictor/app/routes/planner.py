"""Smart Study Planner: student dashboard and plan, mentor cohort view, admin overview, reports and PDF downloads."""
import calendar
import json
from datetime import datetime, timedelta

from flask import Blueprint, Response, abort, flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.decorators import admin_required, premium_required, staff_required
from app.extensions import db
from app.models import User
from app.models_planner import SpAssessment, SpPlan, SpTask
from app.services import jee_gap as G
from app.services import planner as P

planner_bp = Blueprint('planner', __name__, url_prefix='/study-planner')


def _date(s, default=None):
    try:
        return datetime.strptime(s or '', '%Y-%m-%d').date()
    except ValueError:
        return default


def _next_monday(d=None):
    d = d or P.today()
    return d + timedelta(days=(7 - d.weekday()) % 7)


def _linked_student_ids(user):
    """Students a mentor works with, from every place a mentor link exists; an admin sees every student who has a plan."""
    if user.is_admin:
        return {u for (u,) in db.session.query(SpPlan.user_id).distinct()}
    ids = {u for (u,) in db.session.query(SpPlan.user_id).filter(SpPlan.mentor_id == user.id).all()}
    for model, mcol, scol in (('app.models_reinforce:RfStudent', 'mentor_id', 'user_id'), ('app.models_pulse:PulseProfile', 'mentor_id', 'user_id'), ('app.models_mentorship:MsEnrolment', 'mentor_id', 'student_id')):
        try:
            mod, name = model.split(':')
            cls = getattr(__import__(mod, fromlist=[name]), name)
            ids |= {getattr(r, scol) for r in cls.query.filter(getattr(cls, mcol) == user.id).all()}
        except Exception:
            continue
    return ids


def _can_see(user_id):
    return current_user.is_admin or user_id == current_user.id or (current_user.is_staff and user_id in _linked_student_ids(current_user))


def _task_or_404(tid):
    t = db.session.get(SpTask, tid) or abort(404)
    if not _can_see(t.plan.user_id):
        abort(404)
    return t


@planner_bp.app_context_processor
def _inject():
    return {'sp_quote': P.quote_of_the_day, 'sp_levels': P.LEVEL_INFO, 'sp_types': P.TASK_TYPES, 'sp_link': P.link_url, 'sp_task_link': P.task_link}


# =================================================================================================================================
# student
# =================================================================================================================================
@planner_bp.route('/')
@premium_required
def home():
    plan = P.active_plan(current_user.id)
    if not plan:
        return render_template('planner/intro.html')
    st = P.plan_stats(plan)
    act = P.edupulse_activity(current_user.id, datetime.combine(P.week_start(P.today()), datetime.min.time()))
    weak = P.weak_chapters(current_user.id, plan.exam)
    quote, key = P.quote_of_the_week()
    try:
        from app.services import reinforce as rf
        rf.notify(current_user.id, 'motivation', 'This week\'s thought: ' + quote, url_for('planner.home'), 'mq-' + key)      # one weekly in-portal notice, never repeated
    except Exception:
        pass
    return render_template('planner/home.html', plan=plan, st=st, act=act, weak=weak, today=P.today())


@planner_bp.route('/how-it-works')
@login_required
def levels():
    return render_template('planner/levels.html', quiz=P.QUIZ)


@planner_bp.route('/new', methods=['GET', 'POST'])
@premium_required
def new():
    return _new_plan(current_user, mentor_view=False)


def _new_plan(student, mentor_view):
    if request.method == 'POST':
        f = request.form
        exam = f.get('exam') if f.get('exam') in P.EXAMS else 'JEE'
        level = f.get('level') if f.get('level') in P.LEVELS else 'average'
        start = _date(f.get('start'), _next_monday())
        exam_date = _date(f.get('exam_date'))
        weeks = max(2, min(26, int(f.get('weeks') or 8))) if f.get('weeks', '').isdigit() else 8
        if exam_date and exam_date > start:
            weeks = max(2, min(26, ((exam_date - start).days // 7) + 1))
        try:
            hours = max(1.0, min(10.0, float(f.get('hours') or P.LEVEL_INFO[level]['hours'])))
        except ValueError:
            hours = P.LEVEL_INFO[level]['hours']
        for old in SpPlan.query.filter_by(user_id=student.id, status='active').all():
            old.status = 'archived'
        try:
            asm = _latest_assessment(student.id) if exam == 'JEE' and f.get('use_gap') == '1' else None
            plan = P.generate_plan(student, exam, level, start, weeks, exam_date, hours, f.getlist('focus'), mentor_id=current_user.id if mentor_view else None, created_by=current_user.id,
                                   gap_order=G.plan_order(G.analyse(asm.ratings)) if asm else None)
        except ValueError as e:
            db.session.rollback()
            flash('Could not build the plan: %s' % e, 'danger')
            return redirect(request.url)
        flash('Your %s plan is ready: %d weeks, starting %s.' % (P.LEVEL_INFO[level]['label'], weeks, start.strftime('%d %b')), 'success')
        return redirect(url_for('planner.mentor_student', uid=student.id) if mentor_view else url_for('planner.home'))
    chapters = {e: P.subjects_and_chapters(e) for e in P.EXAMS}
    return render_template('planner/new.html', student=student, mentor_view=mentor_view, has_assessment=_latest_assessment(student.id) is not None, quiz=P.QUIZ, chapters=chapters, default_start=_next_monday(), exams=P.EXAMS,
                           pre_level=request.args.get('level') if request.args.get('level') in P.LEVELS else '', pre_exam=request.args.get('exam') if request.args.get('exam') in P.EXAMS else 'JEE')


@planner_bp.route('/plan')
@premium_required
def plan_view():
    plan = P.active_plan(current_user.id)
    if not plan:                                              # no plan yet: send the student to the welcome page instead of an error
        flash('Build your plan first, then it will appear here.', 'info')
        return redirect(url_for('planner.new'))
    w0 = P.week_start(_date(request.args.get('week'), P.today()))
    days = [w0 + timedelta(days=i) for i in range(7)]
    tasks = {d: [] for d in days}
    for t in plan.tasks.filter(SpTask.day >= days[0], SpTask.day <= days[-1]).order_by(SpTask.id).all():
        tasks[t.day].append(t)
    return render_template('planner/plan.html', plan=plan, days=days, tasks=tasks, prev=w0 - timedelta(days=7), nxt=w0 + timedelta(days=7), today=P.today(), w0=w0)


def _edit_guard(plan_user_id):
    if not _can_see(plan_user_id):
        abort(404)


@planner_bp.route('/task/<int:tid>/toggle', methods=['POST'])
@login_required
def task_toggle(tid):
    t = _task_or_404(tid)
    d = request.get_json(silent=True) or request.form
    new = d.get('status') if d.get('status') in ('todo', 'done', 'skipped') else ('todo' if t.status == 'done' else 'done')
    try:
        mins = max(0, min(600, int(d.get('minutes_done') or 0)))
    except (TypeError, ValueError):
        mins = 0
    t.status = new
    t.minutes_done = (mins or t.minutes or 0) if new == 'done' else 0
    t.done_at = datetime.utcnow() if new == 'done' else None
    db.session.commit()
    st = P.plan_stats(t.plan)
    return jsonify(ok=True, status=t.status, week_pct=st['week_pct'], pct=st['pct_due'], streak=st['streak'])


@planner_bp.route('/plan/add', methods=['POST'])
@login_required
def task_add():
    plan = db.session.get(SpPlan, request.form.get('plan_id', type=int) or 0) or abort(404)
    _edit_guard(plan.user_id)
    title = (request.form.get('title') or '').strip()[:200]
    day = _date(request.form.get('day'), P.today())
    ttype = request.form.get('task_type') if request.form.get('task_type') in P.TASK_TYPES else 'practice'
    try:
        minutes = max(5, min(480, int(request.form.get('minutes') or 30)))
    except ValueError:
        minutes = 30
    if title:
        db.session.add(SpTask(plan_id=plan.id, day=day, task_type=ttype, title=title, minutes=minutes, subject=(request.form.get('subject') or '')[:40] or None,
                              link_kind=P.link_for(plan.exam, ttype, True), added_by='mentor' if current_user.id != plan.user_id else 'student'))
        db.session.commit()
        flash('Task added.', 'success')
    return redirect(request.referrer or url_for('planner.home'))


@planner_bp.route('/plan/<int:pid>/suggest', methods=['POST'])
@login_required
def suggest(pid):
    plan = db.session.get(SpPlan, pid) or abort(404)
    _edit_guard(plan.user_id)
    weak = P.weak_chapters(plan.user_id, plan.exam)
    n = P.add_suggested_revision(plan, weak)
    flash('Added %d revision task(s) from your EduPulse practice.' % n if n else 'No new weak chapters found in EduPulse yet. Answer some practice questions first.', 'success' if n else 'info')
    return redirect(request.referrer or url_for('planner.home'))


@planner_bp.route('/plan/<int:pid>/archive', methods=['POST'])
@login_required
def archive(pid):
    plan = db.session.get(SpPlan, pid) or abort(404)
    _edit_guard(plan.user_id)
    plan.status = 'archived'
    db.session.commit()
    flash('Plan archived. You can start a new one any time.', 'info')
    return redirect(url_for('planner.mentor_student', uid=plan.user_id) if current_user.id != plan.user_id else url_for('planner.home'))


# ---- reports and downloads ---------------------------------------------------------------------------------------------------------------------------------
@planner_bp.route('/reports')
@premium_required
def reports():
    plan = P.active_plan(current_user.id)
    if not plan:
        return redirect(url_for('planner.home'))
    days = 30 if request.args.get('period') == 'month' else 7
    since = datetime.combine(P.today() - timedelta(days=days - 1), datetime.min.time())
    st = P.plan_stats(plan)
    from app.services import planner_cal_pdf as C
    months = [('%04d-%02d' % ym, '%s %d' % (calendar.month_name[ym[1]], ym[0])) for ym in C.plan_months(plan)]
    t0 = P.today()
    return render_template('planner/reports.html', plan=plan, st=st, months=months, this_month='%04d-%02d' % (t0.year, t0.month), act=P.edupulse_activity(current_user.id, since), days=days, past=[p for p in SpPlan.query.filter_by(user_id=current_user.id, status='archived').order_by(SpPlan.id.desc()).limit(5)])


@planner_bp.route('/templates')
@login_required
def templates():
    return render_template('planner/templates.html')


def _pdf(data, name):
    return Response(data, mimetype='application/pdf', headers={'Content-Disposition': 'inline; filename=%s' % name})


@planner_bp.route('/download/template/<level>.pdf')
@login_required
def dl_template(level):
    if level not in P.LEVELS:
        abort(404)
    from app.services import planner_pdf
    exam = request.args.get('exam') if request.args.get('exam') in P.EXAMS else 'JEE'
    return _pdf(planner_pdf.template_pdf(level, exam), 'study-planner-template-%s.pdf' % level)


@planner_bp.route('/download/week.pdf')
@premium_required
def dl_week():
    from app.services import planner_pdf
    plan = P.active_plan(current_user.id)
    if not plan:
        flash('Build your plan first, then you can download it.', 'info')
        return redirect(url_for('planner.new'))
    return _pdf(planner_pdf.week_pdf(plan, current_user.name, _date(request.args.get('week'))), 'weekly-study-plan.pdf')


@planner_bp.route('/download/progress.pdf')
@login_required
def dl_progress():
    from app.services import planner_pdf
    uid = request.args.get('uid', type=int) or current_user.id
    if not _can_see(uid):
        abort(404)
    plan = P.active_plan(uid)
    if not plan:
        flash('No active plan yet, so there is no progress report to download.', 'info')
        return redirect(url_for('planner.home') if uid == current_user.id else url_for('planner.mentor_student', uid=uid))
    since = datetime.combine(P.today() - timedelta(days=6), datetime.min.time())
    return _pdf(planner_pdf.progress_pdf(P.plan_stats(plan), plan.user.name, P.edupulse_activity(uid, since)), 'study-progress-report.pdf')


def _report_plan(uid):
    """The plan a report is built from, or a redirect when there is none."""
    if not _can_see(uid):
        abort(404)
    plan = P.active_plan(uid)
    if not plan:
        flash('No active plan yet, so there is no report to download.', 'info')
        return None, redirect(url_for('planner.home') if uid == current_user.id else url_for('planner.mentor_student', uid=uid))
    return plan, None


@planner_bp.route('/download/month.pdf')
@login_required
def dl_month():
    """Monthly report as a calendar with infographics. ?month=YYYY-MM (default: this month, or the nearest month the plan covers)."""
    from app.services import planner_cal_pdf as C
    uid = request.args.get('uid', type=int) or current_user.id
    plan, back = _report_plan(uid)
    if back:
        return back
    months = C.plan_months(plan)
    if not months:
        flash('The plan has no tasks yet.', 'info')
        return redirect(url_for('planner.reports'))
    try:
        y, m = [int(x) for x in (request.args.get('month') or '').split('-')]
        if not 1 <= m <= 12:
            raise ValueError
    except ValueError:
        t = P.today()
        y, m = t.year, t.month
    if (y, m) not in months:
        y, m = min(months, key=lambda ym: abs((ym[0] - y) * 12 + ym[1] - m))
    return _pdf(C.month_pdf(plan, plan.user.name, y, m), 'study-plan-monthly-report-%04d-%02d.pdf' % (y, m))


@planner_bp.route('/download/plan-report.pdf')
@login_required
def dl_plan_report():
    """Whole-plan report: every month as a calendar, weekly hours, topics and key dates."""
    from app.services import planner_cal_pdf as C
    uid = request.args.get('uid', type=int) or current_user.id
    plan, back = _report_plan(uid)
    if back:
        return back
    return _pdf(C.plan_report_pdf(plan, plan.user.name), 'study-plan-whole-report.pdf')


@planner_bp.route('/download/plan.csv')
@login_required
def dl_plan_csv():
    uid = request.args.get('uid', type=int) or current_user.id
    if not _can_see(uid):
        abort(404)
    plan = P.active_plan(uid)
    if not plan:
        flash('No active plan yet.', 'info')
        return redirect(url_for('planner.home') if uid == current_user.id else url_for('planner.mentor_student', uid=uid))
    return Response(P.tasks_csv(plan), mimetype='text/csv', headers={'Content-Disposition': 'attachment; filename=study-plan.csv'})


# =================================================================================================================================
# mentor and admin
# =================================================================================================================================
def _cohort():
    ids = _linked_student_ids(current_user)
    q = SpPlan.query.filter(SpPlan.status == 'active', SpPlan.user_id.in_(ids or [0]))
    level, exam = request.args.get('level'), request.args.get('exam')
    if level in P.LEVELS:
        q = q.filter(SpPlan.level == level)
    if exam in P.EXAMS:
        q = q.filter(SpPlan.exam == exam)
    rows = P.summary_rows(q.order_by(SpPlan.id.desc()).all())
    flt = request.args.get('status')
    if flt == 'behind':
        rows = [r for r in rows if not r['on_track']]
    elif flt == 'inactive':
        cut = datetime.utcnow() - timedelta(days=7)
        rows = [r for r in rows if not r['last_done'] or r['last_done'] < cut]
    return ids, rows


@planner_bp.route('/mentor')
@staff_required
def mentor_home():
    ids, rows = _cohort()
    unplanned = User.query.filter(User.id.in_(ids or [0]), ~User.id.in_(db.session.query(SpPlan.user_id).filter(SpPlan.status == 'active'))).order_by(User.name).all()
    return render_template('planner/mentor_home.html', rows=rows, unplanned=unplanned, f={'level': request.args.get('level', ''), 'exam': request.args.get('exam', ''), 'status': request.args.get('status', '')})


@planner_bp.route('/mentor/export.csv')
@staff_required
def mentor_export():
    return Response(P.rows_csv(_cohort()[1]), mimetype='text/csv', headers={'Content-Disposition': 'attachment; filename=study-planner-cohort.csv'})


@planner_bp.route('/mentor/student/<int:uid>')
@staff_required
def mentor_student(uid):
    if not _can_see(uid):
        abort(404)
    u = db.session.get(User, uid) or abort(404)
    plan = P.active_plan(uid)
    st = P.plan_stats(plan) if plan else None
    act = P.edupulse_activity(uid, datetime.combine(P.week_start(P.today()), datetime.min.time()))
    recent = plan.tasks.filter(SpTask.day >= P.today() - timedelta(days=6), SpTask.day <= P.today() + timedelta(days=2)).order_by(SpTask.day, SpTask.id).all() if plan else []
    return render_template('planner/mentor_student.html', u=u, plan=plan, st=st, act=act, recent=recent, weak=P.weak_chapters(uid, plan.exam) if plan else [], today=P.today())


@planner_bp.route('/mentor/new/<int:uid>', methods=['GET', 'POST'])
@staff_required
def mentor_new(uid):
    if not _can_see(uid):
        abort(404)
    return _new_plan(db.session.get(User, uid) or abort(404), mentor_view=True)


# =================================================================================================================================
# JEE self-assessment and gap map
# =================================================================================================================================
def _latest_assessment(uid):
    return SpAssessment.query.filter_by(user_id=uid).order_by(SpAssessment.id.desc()).first()


def _assess(student, mentor_view):
    topics = G.topics()
    prev = _latest_assessment(student.id)
    values = dict(prev.ratings) if prev else {}
    if request.method == 'POST':
        values = G.clean({t['code']: request.form.get(t['code']) for t in topics})
        left = len(topics) - len(values)
        if left:
            flash('%d topic%s still to rate. Every topic needs a rating from 0 to 4 (leave nothing blank).' % (left, '' if left == 1 else 's'), 'danger')
        else:
            db.session.add(SpAssessment(user_id=student.id, entered_by=current_user.id, ratings_json=json.dumps(values), note=(request.form.get('note') or '')[:300] or None))
            db.session.commit()
            flash('Assessment saved. Here is your gap map.' if not mentor_view else 'Assessment saved for %s.' % student.name, 'success')
            return redirect(url_for('planner.mentor_gap', uid=student.id) if mentor_view else url_for('planner.gap_map'))
    return render_template('planner/assessment.html', student=student, mentor_view=mentor_view, topics=topics, values=values, subjects=G.SUBJECTS, prev=prev, tier_label=G.TIER_LABEL,
                           words=G.RATING_WORDS)


def _gap_view(student, mentor_view):
    asm = _latest_assessment(student.id)
    if not asm:
        flash('Rate the topics first: the gap map is built from your ratings.', 'info')
        return redirect(url_for('planner.mentor_assessment', uid=student.id) if mentor_view else url_for('planner.self_assessment'))
    a = G.analyse(asm.ratings)
    plan = P.active_plan(student.id)
    return render_template('planner/gap.html', student=student, mentor_view=mentor_view, asm=asm, a=a, plan=plan, subjects=G.SUBJECTS, tier_label=G.TIER_LABEL, words=G.RATING_WORDS,
                           need=G.NEED, history=SpAssessment.query.filter_by(user_id=student.id).count())


def _rebuild_with_gaps(student, mentor_view):
    asm = _latest_assessment(student.id) or abort(404)
    if request.form.get('confirm') != '1':
        flash('Tick the box to confirm: your current plan is archived (not deleted) and a new one is built.', 'danger')
        return redirect(url_for('planner.mentor_gap', uid=student.id) if mentor_view else url_for('planner.gap_map'))
    old = P.active_plan(student.id)
    today = P.today()
    level = old.level if old else 'average'
    weeks = old.weeks if old and old.weeks else 8
    exam_date = old.exam_date if old and old.exam_date and old.exam_date > today else None
    hours = old.hours_per_day if old and old.hours_per_day else None
    for o in SpPlan.query.filter_by(user_id=student.id, status='active').all():
        o.status = 'archived'
    try:
        P.generate_plan(student, 'JEE', level, today, weeks, exam_date, hours, mentor_id=(old.mentor_id if old else None) or (current_user.id if mentor_view else None), created_by=current_user.id,
                        title='JEE plan from the gap map (%s)' % today.strftime('%d %b %Y'), gap_order=G.plan_order(G.analyse(asm.ratings)))
    except ValueError as e:
        db.session.rollback()
        flash('Could not build the plan: %s' % e, 'danger')
        return redirect(url_for('planner.mentor_gap', uid=student.id) if mentor_view else url_for('planner.gap_map'))
    flash('New plan built from the gap map: the topics with the most marks within reach come first.', 'success')
    return redirect(url_for('planner.mentor_student', uid=student.id) if mentor_view else url_for('planner.plan_view'))


@planner_bp.route('/self-assessment', methods=['GET', 'POST'])
@premium_required
def self_assessment():
    return _assess(current_user, False)


@planner_bp.route('/gap-map')
@premium_required
def gap_map():
    return _gap_view(current_user, False)


@planner_bp.route('/gap-map/rebuild', methods=['POST'])
@premium_required
def gap_rebuild():
    return _rebuild_with_gaps(current_user, False)


@planner_bp.route('/mentor/student/<int:uid>/self-assessment', methods=['GET', 'POST'])
@staff_required
def mentor_assessment(uid):
    if not _can_see(uid):
        abort(404)
    return _assess(db.session.get(User, uid) or abort(404), True)


@planner_bp.route('/mentor/student/<int:uid>/gap-map')
@staff_required
def mentor_gap(uid):
    if not _can_see(uid):
        abort(404)
    return _gap_view(db.session.get(User, uid) or abort(404), True)


@planner_bp.route('/mentor/student/<int:uid>/gap-map/questions', methods=['POST'])
@staff_required
def mentor_gap_questions(uid):
    """Assign the default EduPulse Reinforcement question sets built from the student's gap map."""
    if not _can_see(uid):
        abort(404)
    from app.services import rf_gap
    student = db.session.get(User, uid) or abort(404)
    r = rf_gap.assign_defaults(student, current_user)
    if r['no_assessment']:
        flash('Rate the topics first: the question sets are built from the gap map.', 'danger')
    else:
        bits = ['%d question set%s assigned' % (len(r['made']), '' if len(r['made']) == 1 else 's')]
        if r['skipped']:
            bits.append('%d already assigned' % len(r['skipped']))
        if r['thin']:
            bits.append('too few questions in the bank for: ' + ', '.join(r['thin']))
        if r['missing']:
            bits.append('no bank chapter yet for: ' + ', '.join(r['missing'][:6]))
        flash('EduPulse Reinforcement for %s: %s.' % (student.name, '; '.join(bits)), 'success' if r['made'] else 'info')
    return redirect(url_for('planner.mentor_gap', uid=uid))


@planner_bp.route('/mentor/student/<int:uid>/gap-map/rebuild', methods=['POST'])
@staff_required
def mentor_gap_rebuild(uid):
    if not _can_see(uid):
        abort(404)
    return _rebuild_with_gaps(db.session.get(User, uid) or abort(404), True)



@planner_bp.route('/admin')
@admin_required
def admin():
    plans = SpPlan.query.filter_by(status='active').order_by(SpPlan.id.desc()).all()
    rows = P.summary_rows(plans)
    cut = datetime.utcnow() - timedelta(days=7)
    by_level = {lv: [r for r in rows if r['level'] == lv] for lv in P.LEVELS}
    avg = lambda xs: round(sum(xs) / len(xs)) if xs else None
    stats = {'plans': len(rows), 'archived': SpPlan.query.filter_by(status='archived').count(), 'on_track': sum(1 for r in rows if r['on_track']),
             'inactive': [r for r in rows if not r['last_done'] or r['last_done'] < cut],
             'level': {lv: {'n': len(v), 'avg': avg([r['pct_due'] for r in v if r['pct_due'] is not None]), 'hours': round(sum(r['hours_done'] for r in v), 1)} for lv, v in by_level.items()},
             'exam': {e: len([r for r in rows if r['exam'] == e]) for e in P.EXAMS}, 'questions': sum(r['questions_week'] for r in rows)}
    return render_template('planner/admin.html', rows=rows, stats=stats)


@planner_bp.route('/admin/export.csv')
@admin_required
def admin_export():
    rows = P.summary_rows(SpPlan.query.filter_by(status='active').order_by(SpPlan.id.desc()).all())
    return Response(P.rows_csv(rows), mimetype='text/csv', headers={'Content-Disposition': 'attachment; filename=study-planner-all.csv'})
