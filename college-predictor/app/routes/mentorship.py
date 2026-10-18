"""Mentorship Portal — one student record, three coordinated dashboards.

Routes (all under /mentorship):
    GET  /                          dispatcher: staff → mentor dashboard, student/parent → their workspace
    GET  /mentor                    mentor dashboard (KPI cards, filterable student table)
    GET  /e/<eid>/<tab>             workspace tab (home, sessions, weekly, kpis, reviews, branch, prefs,
                                    calendar, messages, reports, history) — content varies by role
    POST /e/<eid>/...               every write; permission is checked on the server for each one
    GET/POST /admin/...             programmes, session templates, enrolment, parents, rules, branches (admin)

Access is decided by services.mentorship.role_for(): admin | assigned EA mentor | the student (must be
Premium) | a linked parent.  Anyone else gets 404, so record ids cannot be probed.
"""
from datetime import timedelta

from flask import (Blueprint, Response, abort, flash, redirect, render_template, request, url_for)
from flask_login import current_user, login_required

from app.decorators import admin_required, staff_required
from app.extensions import db
from app.models import User
from app.models_membership import Setting
from app.models_mentorship import (
    ACTION_STATUSES, ADMISSION_ROUTES, ELIGIBILITY, EVENT_CATEGORIES, KPI_DIRECTIONS, PREF_LIST_STATUSES,
    REVIEW_STATUSES, SESSION_STATUSES, MsAction, MsAudit, MsBranch, MsBranchFit, MsBranchRating, MsCheckin,
    MsEnrolment, MsEvent, MsKpi, MsKpiObs, MsMessage, MsMessageRead, MsParentLink, MsPrefEntry, MsPrefList,
    EXAM_STATUSES, MsAlert, MsExam, MsExamFocus, MsProgramme, MsReport, MsReview, MsSession, MsSessionTemplate,
)
from app.services import exam_calendar as xc
from app.services import mailer
from app.services import mentorship as svc

mentorship_bp = Blueprint('mentorship', __name__, url_prefix='/mentorship')

STUDENT_ACTION_STATUSES = ('Not Started', 'In Progress', 'Completed', 'Needs Help')
PRIORITIES = ('High', 'Medium', 'Low')
KPI_CATEGORIES = ('Preparation', 'Performance', 'Mentorship', 'Readiness')


# --------------------------------------------------------------------------- #
# small helpers
# --------------------------------------------------------------------------- #
def _s(name, n=2000):
    return (request.form.get(name) or '').strip()[:n]


def _int(name, lo=None, hi=None):
    try:
        v = int(request.form.get(name))
    except (TypeError, ValueError):
        return None
    if lo is not None and v < lo:
        return None
    if hi is not None and v > hi:
        return None
    return v


def _float(name):
    try:
        v = request.form.get(name)
        return float(v) if v not in (None, '') else None
    except ValueError:
        return None


def _ctx(eid, need=None):
    """Load an enrolment and the caller's role, or 404/403. Students must hold Premium."""
    e = db.session.get(MsEnrolment, eid) or abort(404)
    role = svc.role_for(e, current_user)
    if role is None:
        abort(404)
    if need and role not in need:
        abort(403)
    return e, role


def _back(e, tab, anchor=''):
    return redirect(url_for('mentorship.workspace', eid=e.id, tab=tab) + (('#' + anchor) if anchor else ''))


STAFF = ('mentor', 'admin')


def _premium_gate(role):
    """A student's access depends on live Premium status; parents/staff are not gated by it."""
    return role == 'student' and not current_user.is_premium


# --------------------------------------------------------------------------- #
# entry points
# --------------------------------------------------------------------------- #
@mentorship_bp.route('/')
@login_required
def index():
    if current_user.is_admin or current_user.is_ea_mentor:
        return redirect(url_for('mentorship.mentor_home'))
    as_student = MsEnrolment.query.filter_by(student_id=current_user.id).all()
    parent_eids = [x.enrolment_id for x in MsParentLink.query.filter_by(parent_id=current_user.id).all()]
    as_parent = MsEnrolment.query.filter(MsEnrolment.id.in_(parent_eids)).all() if parent_eids else []
    mine = as_student + [e for e in as_parent if e not in as_student]
    if not mine:
        return render_template('mentorship/not_enrolled.html')
    if as_student and not as_parent and not current_user.is_premium:
        return render_template('premium_locked.html'), 403
    if len(mine) == 1:
        return redirect(url_for('mentorship.workspace', eid=mine[0].id, tab='home'))
    return render_template('mentorship/choose.html', enrolments=mine)


def _staff_enrolments():
    q = MsEnrolment.query
    if not current_user.is_admin:
        q = q.filter(MsEnrolment.mentor_id == current_user.id)
    return q.order_by(MsEnrolment.id.desc()).all()


def _row(e):
    ss, ast = svc.session_stats(e), svc.action_stats(e)
    rows, cur = svc.journey(e)
    level, reasons = svc.attention(e)
    nxt = svc.next_session(e)
    kp = [svc.kpi_view(k)['status'] for k in e.kpis_q().filter(MsKpi.status == 'Active').all()]
    last_done = e.sessions.filter(MsSession.actual_at != None).order_by(MsSession.actual_at.desc()).first()  # noqa: E711
    last_msg = (MsMessage.query.filter(MsMessage.enrolment_id == e.id, MsMessage.sender_id == e.mentor_id)
                .order_by(MsMessage.created_at.desc()).first()) if e.mentor_id else None
    last_contact = max([d for d in (last_done.actual_at if last_done else None, last_msg.created_at if last_msg else None) if d], default=None)
    ev = next((i for i in svc.events_for(e) if i['kind'] == 'event' and i['date'] >= svc.today()), None)
    return {'e': e, 'ss': ss, 'ast': ast, 'stage': cur.title if cur else ('All core sessions done' if ss['core_total'] else '—'),
            'next': nxt, 'level': level, 'reasons': reasons, 'last_contact': last_contact, 'event': ev,
            'kpi_attn': sum(1 for s in kp if s in ('Needs attention', 'Out of range')), 'kpi_n': len(kp)}


def _filters(rows):
    t = svc.today()
    wk = svc.week_start()
    f = {k: set() for k in ('all', 'upcoming', 'document', 'followup', 'overdue', 'attention', 'review', 'parent_report',
                            'checkin_review', 'deadline')}
    now = svc.utcnow()
    for r in rows:
        e = r['e']
        f['all'].add(e.id)
        if r['next'] and r['next'].planned_at <= now + timedelta(days=14):
            f['upcoming'].add(e.id)
        if e.sessions.filter(MsSession.status.in_(['Planned', 'Rescheduled']), MsSession.planned_at < now - timedelta(hours=2)).count():
            f['document'].add(e.id)
        if e.status == 'Active' and not MsCheckin.query.filter(MsCheckin.enrolment_id == e.id, MsCheckin.week_start == wk,
                                                               MsCheckin.status != 'Draft').count():
            f['followup'].add(e.id)
        if r['ast']['overdue']:
            f['overdue'].add(e.id)
        if r['level'] != 'ok':
            f['attention'].add(e.id)
        recent = e.reviews.filter(MsReview.status.in_(['Finalised', 'Shared'])).order_by(MsReview.finalised_at.desc()).first()
        base = (recent.finalised_at.date() if recent and recent.finalised_at else e.start_date)
        if e.status == 'Active' and base and (t - base).days >= 90:
            f['review'].add(e.id)
        if not MsReport.query.filter_by(enrolment_id=e.id, status='Shared').count() and r['ss']['core_done'] >= 1:
            f['parent_report'].add(e.id)
        if (MsCheckin.query.filter_by(enrolment_id=e.id, status='Submitted').count()
                or MsBranchFit.query.filter_by(enrolment_id=e.id, status='Submitted').count()):
            f['checkin_review'].add(e.id)
        if MsEvent.query.filter(db.or_(MsEvent.enrolment_id == e.id, MsEvent.programme_id == e.programme_id),
                                MsEvent.category.in_(['Admission deadline', 'Counselling', 'Choice filling', 'Documents']),
                                MsEvent.starts_on >= t, MsEvent.starts_on <= t + timedelta(days=14), MsEvent.done == False).count():  # noqa: E712
            f['deadline'].add(e.id)
    return f


FILTER_LABELS = [
    ('all', 'Assigned students'), ('upcoming', 'Upcoming sessions (14 d)'), ('document', 'Sessions awaiting documentation'),
    ('followup', 'Weekly follow-ups due'), ('overdue', 'Overdue student actions'), ('attention', 'Needing attention'),
    ('review', 'Quarterly reviews due'), ('parent_report', 'Parent reports pending'),
    ('checkin_review', 'Submissions awaiting review'), ('deadline', 'Admission deadlines near'),
]


@mentorship_bp.route('/mentor')
@staff_required
def mentor_home():
    rows = [_row(e) for e in _staff_enrolments()]
    f = _filters(rows)
    key = request.args.get('f', 'all')
    key = key if key in f else 'all'
    q = (request.args.get('q') or '').strip().lower()
    stage = request.args.get('stage', '')
    level = request.args.get('level', '')
    prog = request.args.get('programme', type=int)
    shown = [r for r in rows if r['e'].id in f[key]]
    if q:
        shown = [r for r in shown if q in (r['e'].student.name or '').lower() or q in (r['e'].student.email or '').lower()]
    if stage:
        shown = [r for r in shown if r['stage'] == stage]
    if level:
        shown = [r for r in shown if r['level'] == level]
    if prog:
        shown = [r for r in shown if r['e'].programme_id == prog]
    sort = request.args.get('sort', 'attention')
    order = {'attention': lambda r: {'attention': 0, 'watch': 1, 'ok': 2}[r['level']], 'name': lambda r: (r['e'].student.name or '').lower(),
             'progress': lambda r: r['ss']['pct'], 'next': lambda r: (r['next'].planned_at if r['next'] else svc.utcnow() + timedelta(days=9999))}
    shown.sort(key=order.get(sort, order['attention']))
    stages = sorted({r['stage'] for r in rows})
    return render_template('mentorship/mentor_home.html', alerts=xc.unread_alerts(current_user), rows=shown, counts={k: len(v) for k, v in f.items()},
                           filter_labels=FILTER_LABELS, active=key, q=q, stage=stage, level=level, prog=prog, sort=sort,
                           stages=stages, programmes=MsProgramme.query.all(), fmt_dt=svc.fmt_dt)


# --------------------------------------------------------------------------- #
# workspace (GET)
# --------------------------------------------------------------------------- #
@mentorship_bp.route('/e/<int:eid>/<tab>')
@login_required
def workspace(eid, tab):
    e, role = _ctx(eid)
    if _premium_gate(role):
        return render_template('premium_locked.html'), 403
    tabs = svc.tabs_for(role)
    if tab not in {t[0] for t in tabs}:
        abort(404)
    ctx = dict(e=e, role=role, tab=tab, tabs=tabs, svc=svc, fmt_dt=svc.fmt_dt, today=svc.today(),
               alerts=xc.unread_alerts(current_user), xc=xc,
               followed_ids={f.exam_id for f in MsExamFocus.query.filter_by(enrolment_id=e.id).all()},
               unread=svc.unread_count(e, current_user, role), staff=role in STAFF,
               SESSION_STATUSES=SESSION_STATUSES, PRIORITIES=PRIORITIES)
    ctx.update(globals()['_tab_' + tab](e, role))
    return render_template(f'mentorship/tab_{tab}.html', **ctx)


def _visible_actions(e, role):
    q = e.actions
    if role == 'parent':
        q = q.filter(MsAction.parent_visible == True)  # noqa: E712
    return q


def _tab_home(e, role):
    rows, cur = svc.journey(e)
    ss = svc.session_stats(e)
    ast = svc.action_stats(e, only_visible_to_parent=(role == 'parent'))
    t = svc.today()
    week = (_visible_actions(e, role).filter(MsAction.status != 'Cancelled')
            .filter(db.or_(MsAction.due_date <= t + timedelta(days=7), MsAction.due_date == None))  # noqa: E711
            .filter(db.or_(MsAction.status != 'Completed', MsAction.completed_at >= svc.utcnow() - timedelta(days=7)))
            .order_by(MsAction.due_date).all())
    if role == 'parent':
        week = [a for a in week if a.parent_visible]
    kpis = [(k, svc.kpi_view(k)) for k in e.kpis_q().filter(MsKpi.status == 'Active').all()][:6]
    upcoming = [i for i in svc.events_for(e) if i['date'] >= t and (role != 'parent' or i['kind'] != 'action')][:6]
    ci = (MsCheckin.query.filter(MsCheckin.enrolment_id == e.id, MsCheckin.status != 'Draft')
          .order_by(MsCheckin.week_start.desc()).first())
    priority = None
    for a in week:
        if a.priority == 'High' and a.status != 'Completed':
            priority = a
            break
    level, reasons = svc.attention(e) if role in STAFF else (None, [])
    msgs = (MsMessage.query.filter(MsMessage.enrolment_id == e.id, MsMessage.audience.in_(svc.visible_audiences(role)))
            .order_by(MsMessage.created_at.desc()).limit(3).all())
    review = e.reviews.filter(MsReview.status.in_(['Shared'])).order_by(MsReview.shared_at.desc()).first()
    # plain queries: `e.sessions` carries an ORDER BY position, which PostgreSQL rejects next to max()
    last_update = max([x for x in (
        db.session.query(db.func.max(MsSession.updated_at)).filter(MsSession.enrolment_id == e.id).scalar(),
        db.session.query(db.func.max(MsAction.updated_at)).filter(MsAction.enrolment_id == e.id).scalar()) if x], default=None)
    return dict(timeline=rows, current=cur, ss=ss, ast=ast, week=week, kpis=kpis, upcoming=upcoming, last_checkin=ci,
                priority=priority, nxt=svc.next_session(e), level=level, reasons=reasons, msgs=msgs, shared_review=review,
                last_update=last_update, action_state=svc.action_state)


def _tab_sessions(e, role):
    rows = e.sessions.order_by(MsSession.position).all()
    if role in ('student', 'parent'):
        rows = [s for s in rows if role == 'student' or s.parent_visible]
    return dict(core=[s for s in rows if s.kind == 'core'], extra=[s for s in rows if s.kind != 'core'],
                ss=svc.session_stats(e), can_extra=svc.can_add_extra(e, role), used=svc.extras_used(e),
                to_input=svc.to_input, actions_by_session={s.id: e.actions.filter_by(session_id=s.id).all() for s in rows})


def _tab_weekly(e, role):
    wk = svc.week_start()
    ci = MsCheckin.query.filter_by(enrolment_id=e.id, week_start=wk).first()
    prev = MsCheckin.query.filter(MsCheckin.enrolment_id == e.id, MsCheckin.week_start < wk).order_by(MsCheckin.week_start.desc()).first()
    open_actions = e.actions.filter(MsAction.status.notin_(['Cancelled'])).order_by(MsAction.due_date).all()
    cur = [a for a in open_actions if a.status != 'Completed' or (a.completed_at and a.completed_at.date() >= wk)]
    history = MsCheckin.query.filter(MsCheckin.enrolment_id == e.id, MsCheckin.status != 'Draft').order_by(MsCheckin.week_start.desc()).limit(12).all()
    return dict(checkin=ci, prev=prev, actions=cur, week=wk, history=history, ACTION_STATUSES=ACTION_STATUSES,
                STUDENT_ACTION_STATUSES=STUDENT_ACTION_STATUSES, action_state=svc.action_state,
                outcomes=svc.jload(ci.outcomes_json) if ci else {}, outcome_notes=svc.jload(ci.outcome_notes_json) if ci else {},
                sessions_for_link=e.sessions.order_by(MsSession.position).all(), cal_actions=cur)


def _tab_kpis(e, role):
    ks = e.kpis_q().order_by(MsKpi.category, MsKpi.id).all()
    if role == 'parent':
        ks = [k for k in ks if k.status == 'Active']
    return dict(kpis=[(k, svc.kpi_view(k)) for k in ks], presets=svc.PRESET_KPIS, KPI_DIRECTIONS=KPI_DIRECTIONS,
                KPI_CATEGORIES=KPI_CATEGORIES, ss=svc.session_stats(e), ast=svc.action_stats(e))


def _tab_reviews(e, role):
    q = e.reviews.order_by(MsReview.id.desc())
    rows = q.all()
    if role in ('student', 'parent'):
        rows = [r for r in rows if r.status == 'Shared' or (r.status == 'Awaiting input' and (role == 'student' or r.parent_requested))]
    return dict(reviews=rows, REVIEW_STATUSES=REVIEW_STATUSES, jload=svc.jload)


def _tab_branch(e, role):
    svc.ensure_branches()
    fit = e.branchfit()
    branches = MsBranch.query.filter_by(active=True).order_by(MsBranch.position, MsBranch.id).all()
    ratings = {r.branch: r for r in MsBranchRating.query.filter_by(enrolment_id=e.id).all()}
    w = {'interest': 1, 'readiness': 1, 'feasibility': 1, 'family': 1}
    w.update(svc.jload(fit.weights_json) if fit and fit.weights_json else {})
    matrix = []
    for b in branches:
        r = ratings.get(b.name)
        vals = [getattr(r, k) if r else None for k in ('interest', 'readiness', 'feasibility', 'family')]
        total = sum(w[k] for k, v in zip(('interest', 'readiness', 'feasibility', 'family'), vals) if v)
        score = (sum(w[k] * v for k, v in zip(('interest', 'readiness', 'feasibility', 'family'), vals) if v) / total) if total else None
        matrix.append({'b': b, 'r': r, 'score': round(score, 2) if score else None})
    matrix_sorted = sorted([m for m in matrix if m['score']], key=lambda m: -m['score'])
    return dict(fit=fit, branches=branches, ratings=ratings, weights=w, matrix=matrix, ranked=matrix_sorted)


def _tab_prefs(e, role):
    lists = MsPrefList.query.filter_by(enrolment_id=e.id).order_by(MsPrefList.id).all()
    return dict(lists=lists, PREF_LIST_STATUSES=PREF_LIST_STATUSES, ADMISSION_ROUTES=ADMISSION_ROUTES, ELIGIBILITY=ELIGIBILITY,
                allowed_status=_allowed_pref_status(role),
                hist=MsAudit.query.filter(MsAudit.enrolment_id == e.id, MsAudit.action.like('pref.%')).order_by(MsAudit.id.desc()).limit(25).all())


def _tab_calendar(e, role):
    cat = request.args.get('cat', '')
    items = [i for i in svc.events_for(e) if role != 'parent' or i['kind'] != 'action']
    cats = sorted({i['category'] for i in items})
    if cat:
        items = [i for i in items if i['category'] == cat]
    months = {}
    for i in items:
        months.setdefault(i['date'].strftime('%B %Y'), []).append(i)
    # catalogue of exams to choose from (search / category / status filters)
    q = (request.args.get('q') or '').strip().lower()
    xcat, xstatus = request.args.get('xcat', ''), request.args.get('xstatus', '')
    exams = MsExam.query.filter_by(active=True).order_by(MsExam.starts_on, MsExam.name).all()
    xcats = sorted({x.category for x in exams})
    if q:
        exams = [x for x in exams if q in x.name.lower() or q in (x.stream or '').lower()]
    if xcat:
        exams = [x for x in exams if x.category == xcat]
    if xstatus:
        exams = [x for x in exams if x.status == xstatus]
    return dict(months=months, cats=cats, cat=cat, EVENT_CATEGORIES=EVENT_CATEGORIES, exams=exams, xcats=xcats,
                xq=q, xcat=xcat, xstatus=xstatus, EXAM_STATUSES=EXAM_STATUSES,
                mail_ready=mailer.is_configured())


def _tab_messages(e, role):
    msgs = (MsMessage.query.filter(MsMessage.enrolment_id == e.id, MsMessage.audience.in_(svc.visible_audiences(role)))
            .order_by(MsMessage.created_at.desc()).limit(100).all())
    ids = [m.id for m in msgs if m.sender_id != current_user.id]
    already = {r.message_id for r in MsMessageRead.query.filter(MsMessageRead.user_id == current_user.id, MsMessageRead.message_id.in_(ids))} if ids else set()
    for mid in set(ids) - already:
        db.session.add(MsMessageRead(message_id=mid, user_id=current_user.id))
    db.session.commit()
    return dict(msgs=msgs, was_unread=set(ids) - already)


def _tab_reports(e, role):
    q = MsReport.query.filter_by(enrolment_id=e.id).order_by(MsReport.id.desc())
    if role in ('student', 'parent'):
        q = q.filter(MsReport.status == 'Shared')
    return dict(reports=q.all())


def _tab_history(e, role):
    return dict(log=MsAudit.query.filter_by(enrolment_id=e.id).order_by(MsAudit.id.desc()).limit(200).all())


# --------------------------------------------------------------------------- #
# sessions
# --------------------------------------------------------------------------- #
@mentorship_bp.route('/e/<int:eid>/sessions/add', methods=['POST'])
@login_required
def session_add(eid):
    e, role = _ctx(eid, STAFF)
    title = _s('title', 200)
    kind = request.form.get('kind') if request.form.get('kind') in ('extra', 'intervention', 'follow-up') else 'extra'
    if not title:
        flash('Give the session a title.', 'danger')
        return _back(e, 'sessions')
    if not svc.can_add_extra(e, role):
        flash(f'This package includes {e.extra_quota or 0} extra session(s) and all are used. '
              'An administrator must raise the allowance before another can be scheduled.', 'danger')
        return _back(e, 'sessions')
    s = MsSession(enrolment_id=e.id, kind=kind, position=svc.next_position(e), title=title, agenda=_s('agenda'),
                  planned_at=svc.from_local(request.form.get('planned_at'), e.timezone), duration_min=_int('duration_min', 5, 480) or 60)
    db.session.add(s)
    svc.audit(e, 'session.added', f'{kind}: {title}', role)
    db.session.commit()
    flash('Extra session added.', 'success')
    return _back(e, 'sessions')


@mentorship_bp.route('/e/<int:eid>/sessions/<int:sid>/update', methods=['POST'])
@login_required
def session_update(eid, sid):
    e, role = _ctx(eid, STAFF)
    s = db.session.get(MsSession, sid)
    if not s or s.enrolment_id != e.id:
        abort(404)
    old = s.status
    status = request.form.get('status')
    if status in SESSION_STATUSES:
        s.status = status
    s.title = _s('title', 200) or s.title
    s.agenda = _s('agenda')
    s.deliverable = _s('deliverable', 300)
    planned = svc.from_local(request.form.get('planned_at'), e.timezone)
    if request.form.get('planned_at') is not None:
        s.planned_at = planned
    actual = svc.from_local(request.form.get('actual_at'), e.timezone)
    if s.status in ('Completed', 'Partially completed'):
        s.actual_at = actual or s.actual_at or svc.utcnow()          # actual date is separate from the planned date
    else:
        s.actual_at = None
    s.duration_min = _int('duration_min', 5, 480) or s.duration_min
    s.participants = _s('participants', 300)
    s.shared_summary = _s('shared_summary')
    s.mentor_notes = _s('mentor_notes')
    s.next_review_date = svc.parse_date(request.form.get('next_review_date'))
    s.deliverable_url = _s('deliverable_url', 500)
    s.parent_visible = request.form.get('parent_visible') == '1'
    svc.audit(e, 'session.updated', f'#{s.position} {s.title}: {old} → {s.status}', role)
    db.session.commit()
    flash('Session saved.', 'success')
    return _back(e, 'sessions', f's{s.id}')


@mentorship_bp.route('/e/<int:eid>/sessions/<int:sid>/move', methods=['POST'])
@login_required
def session_move(eid, sid):
    e, role = _ctx(eid, STAFF)
    s = db.session.get(MsSession, sid)
    if not s or s.enrolment_id != e.id:
        abort(404)
    rows = [x for x in e.sessions.order_by(MsSession.position, MsSession.id).all() if (x.kind == 'core') == (s.kind == 'core')]
    i = rows.index(s)
    j = i - 1 if request.form.get('dir') == 'up' else i + 1
    if 0 <= j < len(rows):
        s.position, rows[j].position = rows[j].position, s.position
        if s.position == rows[j].position:
            s.position += 1
        svc.audit(e, 'session.reordered', s.title, role)
        db.session.commit()
    return _back(e, 'sessions', f's{s.id}')


# --------------------------------------------------------------------------- #
# actions and weekly check-ins
# --------------------------------------------------------------------------- #
@mentorship_bp.route('/e/<int:eid>/actions/add', methods=['POST'])
@login_required
def action_add(eid):
    e, role = _ctx(eid, STAFF)
    title = _s('title', 240)
    if not title:
        flash('Give the action a title.', 'danger')
        return _back(e, request.form.get('back') or 'weekly')
    a = MsAction(enrolment_id=e.id, session_id=_int('session_id'), title=title, instruction=_s('instruction'), purpose=_s('purpose', 300),
                 priority=request.form.get('priority') if request.form.get('priority') in PRIORITIES else 'Medium',
                 owner=request.form.get('owner') if request.form.get('owner') in ('student', 'mentor', 'parent') else 'student',
                 est_minutes=_int('est_minutes', 1, 1440), start_date=svc.parse_date(request.form.get('start_date')),
                 due_date=svc.parse_date(request.form.get('due_date')), recurrence=_s('recurrence', 20),
                 parent_visible=request.form.get('parent_visible') == '1')
    db.session.add(a)
    svc.audit(e, 'action.added', title, role)
    db.session.commit()
    flash('Action added.', 'success')
    return _back(e, request.form.get('back') or 'weekly')


@mentorship_bp.route('/e/<int:eid>/actions/<int:aid>/update', methods=['POST'])
@login_required
def action_update(eid, aid):
    e, role = _ctx(eid)
    if _premium_gate(role):
        abort(403)
    a = db.session.get(MsAction, aid)
    if not a or a.enrolment_id != e.id:
        abort(404)
    old = a.status
    if role in STAFF:
        a.title = _s('title', 240) or a.title
        a.instruction = _s('instruction') if 'instruction' in request.form else a.instruction
        a.priority = request.form.get('priority') if request.form.get('priority') in PRIORITIES else a.priority
        a.due_date = svc.parse_date(request.form.get('due_date')) if 'due_date' in request.form else a.due_date
        a.mentor_feedback = _s('mentor_feedback') if 'mentor_feedback' in request.form else a.mentor_feedback
        if 'parent_visible_present' in request.form:
            a.parent_visible = request.form.get('parent_visible') == '1'
        status = request.form.get('status')
        allowed = ACTION_STATUSES
    elif (role == 'student' and a.owner == 'student') or (role == 'parent' and a.owner == 'parent'):
        a.student_comment = _s('student_comment') if 'student_comment' in request.form else a.student_comment
        a.evidence_url = _s('evidence_url', 500) if 'evidence_url' in request.form else a.evidence_url
        status = request.form.get('status')
        allowed = STUDENT_ACTION_STATUSES
        if a.status in ('Blocked', 'Cancelled'):
            allowed = ()
    else:
        abort(403)
    if status in allowed:
        a.status = status
        a.completed_at = svc.utcnow() if status == 'Completed' and old != 'Completed' else (a.completed_at if status == 'Completed' else None)
    svc.audit(e, 'action.updated', f'{a.title}: {old} → {a.status}', role)
    db.session.commit()
    flash('Action updated.', 'success')
    return _back(e, request.form.get('back') or 'weekly', f'a{a.id}')


@mentorship_bp.route('/e/<int:eid>/checkin', methods=['POST'])
@login_required
def checkin_save(eid):
    e, role = _ctx(eid, ('student',))
    if _premium_gate(role):
        abort(403)
    wk = svc.week_start()
    ci = MsCheckin.query.filter_by(enrolment_id=e.id, week_start=wk).first()
    if ci and ci.status != 'Draft':
        flash('This week\'s check-in is already submitted.', 'info')
        return _back(e, 'weekly')
    ci = ci or MsCheckin(enrolment_id=e.id, week_start=wk)
    ci.confidence = _int('confidence', 1, 5)
    ci.went_well, ci.difficult = _s('went_well'), _s('difficult')
    ci.barriers, ci.help_needed = _s('barriers'), _s('help_needed')
    ci.next_priority = _s('next_priority', 300)
    ci.urgent_help = request.form.get('urgent_help') == '1'
    outcomes, notes = {}, {}
    for a in e.actions.filter(MsAction.status != 'Cancelled').all():
        v = request.form.get(f'out_{a.id}')
        if v in ('completed', 'partial', 'not', 'blocked'):
            outcomes[str(a.id)] = v
        if request.form.get(f'note_{a.id}'):
            notes[str(a.id)] = request.form.get(f'note_{a.id}')[:500]
    ci.outcomes_json, ci.outcome_notes_json = svc.jdump(outcomes), svc.jdump(notes)
    submit = request.form.get('submit') == '1'
    if submit:
        ci.status, ci.submitted_at = 'Submitted', svc.utcnow()
        for aid, v in outcomes.items():                                  # reflect the self-report on the action itself
            a = db.session.get(MsAction, int(aid))
            if a and a.owner == 'student' and a.status not in ('Cancelled', 'Completed'):
                if v == 'completed':
                    a.status, a.completed_at = 'Completed', svc.utcnow()
                elif v == 'blocked':
                    a.status = 'Blocked'
                elif v == 'partial':
                    a.status = 'In Progress'
            if a and notes.get(aid):
                a.student_comment = notes[aid]
    db.session.add(ci)
    svc.audit(e, 'checkin.submitted' if submit else 'checkin.draft', f'week {wk}', role)
    db.session.commit()
    flash('Check-in submitted to your mentor.' if submit else 'Draft saved.', 'success')
    return _back(e, 'weekly')


@mentorship_bp.route('/e/<int:eid>/checkin/<int:cid>/review', methods=['POST'])
@login_required
def checkin_review(eid, cid):
    e, role = _ctx(eid, STAFF)
    ci = db.session.get(MsCheckin, cid)
    if not ci or ci.enrolment_id != e.id:
        abort(404)
    ci.mentor_comment = _s('mentor_comment')
    ci.share_parent = request.form.get('share_parent') == '1'
    ci.parent_summary = _s('parent_summary')
    ci.status, ci.reviewed_at = 'Reviewed', svc.utcnow()
    svc.audit(e, 'checkin.reviewed', f'week {ci.week_start}', role)
    db.session.commit()
    flash('Review saved.', 'success')
    return _back(e, 'weekly', 'history')


# --------------------------------------------------------------------------- #
# KPIs
# --------------------------------------------------------------------------- #
@mentorship_bp.route('/e/<int:eid>/kpis/add', methods=['POST'])
@login_required
def kpi_add(eid):
    e, role = _ctx(eid, STAFF)
    name = _s('name', 200)
    if not name:
        flash('Name the KPI.', 'danger')
        return _back(e, 'kpis')
    direction = request.form.get('direction') if request.form.get('direction') in KPI_DIRECTIONS else 'higher'
    k = MsKpi(enrolment_id=e.id, category=request.form.get('category') if request.form.get('category') in KPI_CATEGORIES else 'Preparation',
              name=name, definition=_s('definition'), method=_s('method', 300), unit=_s('unit', 30), direction=direction,
              baseline=_float('baseline'), target=_float('target'), target_high=_float('target_high'), frequency=_s('frequency', 30) or 'Weekly',
              owner=_s('owner', 60) or (e.student.name if e.student else ''), notes=_s('notes'),
              outcome_metric=svc.OUTCOME_HINT in name.lower() or request.form.get('outcome_metric') == '1')
    k.current = k.baseline
    db.session.add(k)
    db.session.flush()
    if k.baseline is not None:
        db.session.add(MsKpiObs(kpi_id=k.id, value=k.baseline, note='Baseline', by_user=current_user.id))
    svc.audit(e, 'kpi.created', name, role)
    db.session.commit()
    flash('KPI added.', 'success')
    return _back(e, 'kpis')


@mentorship_bp.route('/e/<int:eid>/kpis/<int:kid>/update', methods=['POST'])
@login_required
def kpi_update(eid, kid):
    e, role = _ctx(eid, STAFF)
    k = db.session.get(MsKpi, kid)
    if not k or k.enrolment_id != e.id:
        abort(404)
    k.name = _s('name', 200) or k.name
    k.definition, k.method, k.notes = _s('definition'), _s('method', 300), _s('notes')
    k.target, k.target_high = _float('target'), _float('target_high')
    k.frequency = _s('frequency', 30) or k.frequency
    k.qualitative = _s('qualitative', 300) or k.qualitative
    if request.form.get('status') in ('Active', 'Paused', 'Archived'):
        k.status = request.form.get('status')
    svc.audit(e, 'kpi.updated', k.name, role)
    db.session.commit()
    flash('KPI updated.', 'success')
    return _back(e, 'kpis', f'k{k.id}')


@mentorship_bp.route('/e/<int:eid>/kpis/<int:kid>/observe', methods=['POST'])
@login_required
def kpi_observe(eid, kid):
    e, role = _ctx(eid, STAFF)
    k = db.session.get(MsKpi, kid)
    if not k or k.enrolment_id != e.id:
        abort(404)
    val, text = _float('value'), _s('text', 300)
    if val is None and not text:
        flash('Enter a value or a qualitative note.', 'danger')
        return _back(e, 'kpis', f'k{k.id}')
    db.session.add(MsKpiObs(kpi_id=k.id, value=val, text=text, note=_s('note', 300), by_user=current_user.id,
                            observed_on=svc.parse_date(request.form.get('observed_on')) or svc.today()))
    if val is not None:
        k.current = val                         # only an authorised entry ever changes a KPI value
    if text:
        k.qualitative = text
    svc.audit(e, 'kpi.observed', f'{k.name}: {val if val is not None else text}', role)
    db.session.commit()
    flash('Progress recorded.', 'success')
    return _back(e, 'kpis', f'k{k.id}')


# --------------------------------------------------------------------------- #
# quarterly reviews
# --------------------------------------------------------------------------- #
@mentorship_bp.route('/e/<int:eid>/reviews/new', methods=['POST'])
@login_required
def review_new(eid):
    e, role = _ctx(eid, STAFF)
    n = e.reviews.count() + 1
    r = MsReview(enrolment_id=e.id, label=_s('label', 60) or f'Quarter {n}', snapshot_json=svc.jdump(svc.build_snapshot(e)))
    db.session.add(r)
    svc.audit(e, 'review.created', r.label, role)
    db.session.commit()
    flash('Review created and pre-filled from current records. Verify and add your observations.', 'success')
    return _back(e, 'reviews', f'r{r.id}')


@mentorship_bp.route('/e/<int:eid>/reviews/<int:rid>/update', methods=['POST'])
@login_required
def review_update(eid, rid):
    e, role = _ctx(eid, STAFF)
    r = db.session.get(MsReview, rid)
    if not r or r.enrolment_id != e.id:
        abort(404)
    for f in ('mentor_observations', 'strengths', 'challenges', 'goal_changes', 'interventions', 'next_targets'):
        setattr(r, f, _s(f))
    r.parent_requested = request.form.get('parent_requested') == '1'
    r.next_review_date = svc.parse_date(request.form.get('next_review_date'))
    if request.form.get('refresh') == '1':
        r.snapshot_json = svc.jdump(svc.build_snapshot(e))
    st = request.form.get('status')
    if st in REVIEW_STATUSES:
        if st in ('Finalised', 'Shared') and not r.finalised_at:
            r.finalised_at = svc.utcnow()
        if st == 'Shared':
            r.shared_at = svc.utcnow()
        r.status = st
    svc.audit(e, 'review.updated', f'{r.label} → {r.status}', role)
    db.session.commit()
    flash('Review saved.', 'success')
    return _back(e, 'reviews', f'r{r.id}')


@mentorship_bp.route('/e/<int:eid>/reviews/<int:rid>/input', methods=['POST'])
@login_required
def review_input(eid, rid):
    e, role = _ctx(eid, ('student', 'parent'))
    r = db.session.get(MsReview, rid)
    if not r or r.enrolment_id != e.id or r.status != 'Awaiting input':
        abort(404)
    if role == 'student':
        r.student_reflection = _s('text')
    elif r.parent_requested:
        r.parent_feedback = _s('text')
    else:
        abort(403)
    svc.audit(e, 'review.input', r.label, role)
    db.session.commit()
    flash('Thank you — your input was saved for your mentor.', 'success')
    return _back(e, 'reviews', f'r{r.id}')


# --------------------------------------------------------------------------- #
# branch fit
# --------------------------------------------------------------------------- #
@mentorship_bp.route('/e/<int:eid>/branch/profile', methods=['POST'])
@login_required
def branch_profile(eid):
    e, role = _ctx(eid, ('student', 'mentor', 'admin'))
    fit = e.branchfit() or MsBranchFit(enrolment_id=e.id)
    if role == 'student':
        for f in ('interests', 'activities', 'strengths', 'environments', 'career_areas', 'family_constraints', 'assessment_notes'):
            setattr(fit, f, _s(f))
        fit.openness = _int('openness', 1, 5)
        w = {k: (_int('w_' + k, 0, 5) if _int('w_' + k, 0, 5) is not None else 1) for k in ('interest', 'readiness', 'feasibility', 'family')}
        fit.weights_json = svc.jdump(w)
        if request.form.get('submit') == '1':
            fit.status = 'Submitted'
    else:
        fit.mentor_summary = _s('mentor_summary')
        if request.form.get('reviewed') == '1':
            fit.status = 'Reviewed'
    db.session.add(fit)
    svc.audit(e, 'branch.profile', fit.status, role)
    db.session.commit()
    flash('Saved.', 'success')
    return _back(e, 'branch')


@mentorship_bp.route('/e/<int:eid>/branch/rate', methods=['POST'])
@login_required
def branch_rate(eid):
    e, role = _ctx(eid)
    name = _s('branch', 120)
    if not name:
        abort(400)
    r = MsBranchRating.query.filter_by(enrolment_id=e.id, branch=name).first() or MsBranchRating(enrolment_id=e.id, branch=name)
    if role == 'student':
        r.interest, r.family, r.student_note = _int('interest', 1, 5), _int('family', 1, 5) or r.family, _s('student_note')
    elif role == 'parent':
        r.family, r.family_concern = _int('family', 1, 5), _s('family_concern')
    elif role in STAFF:
        r.readiness, r.feasibility, r.mentor_note = _int('readiness', 1, 5), _int('feasibility', 1, 5), _s('mentor_note')
    else:
        abort(403)
    db.session.add(r)
    svc.audit(e, 'branch.rated', name, role)
    db.session.commit()
    flash('Rating saved.', 'success')
    return _back(e, 'branch', 'matrix')


# --------------------------------------------------------------------------- #
# college preferences & choice-filling workspace
# --------------------------------------------------------------------------- #
def _allowed_pref_status(role):
    if role == 'parent':
        return ('Approved by family',)
    if role == 'student':
        return tuple(s for s in PREF_LIST_STATUSES if s != 'Ready for official portal entry')
    return PREF_LIST_STATUSES


def _pref_list(e, lid):
    lst = db.session.get(MsPrefList, lid)
    if not lst or lst.enrolment_id != e.id:
        abort(404)
    return lst


@mentorship_bp.route('/e/<int:eid>/prefs/list/new', methods=['POST'])
@login_required
def pref_list_new(eid):
    e, role = _ctx(eid, ('student', 'mentor', 'admin'))
    name = _s('name', 160) or f'Draft list {MsPrefList.query.filter_by(enrolment_id=e.id).count() + 1}'
    lst = MsPrefList(enrolment_id=e.id, name=name, status='Draft created')
    db.session.add(lst)
    svc.audit(e, 'pref.list_created', name, role)
    db.session.commit()
    return _back(e, 'prefs', f'l{lst.id}')


@mentorship_bp.route('/e/<int:eid>/prefs/<int:lid>/status', methods=['POST'])
@login_required
def pref_list_status(eid, lid):
    e, role = _ctx(eid)
    lst = _pref_list(e, lid)
    st = request.form.get('status')
    if st not in _allowed_pref_status(role):
        abort(403)
    lst.status = st
    lst.notes = _s('notes') if role != 'parent' else lst.notes
    if role != 'parent':
        lst.evidence = _s('evidence', 300) or lst.evidence
    if request.form.get('is_final') == '1' and st in ('Approved by family', 'Ready for official portal entry',
                                                       'Entered in official portal', 'Submitted and verified'):
        MsPrefList.query.filter_by(enrolment_id=e.id).update({'is_final': False})
        lst.is_final = True
    svc.audit(e, 'pref.status', f'{lst.name} → {st}', role)
    db.session.commit()
    flash('List status updated.', 'success')
    return _back(e, 'prefs', f'l{lst.id}')


@mentorship_bp.route('/e/<int:eid>/prefs/<int:lid>/entry/add', methods=['POST'])
@login_required
def pref_entry_add(eid, lid):
    e, role = _ctx(eid, ('student', 'mentor', 'admin'))
    lst = _pref_list(e, lid)
    college = _s('college', 200)
    if not college:
        flash('Enter a college name.', 'danger')
        return _back(e, 'prefs', f'l{lst.id}')
    pos = (lst.entries.order_by(MsPrefEntry.position.desc()).first().position + 1) if lst.entries.count() else 1
    x = MsPrefEntry(list_id=lst.id, position=pos, college=college, branch=_s('branch', 160),
                    route=request.form.get('route') if request.form.get('route') in ADMISSION_ROUTES else None,
                    tier=request.form.get('tier') if request.form.get('tier') in ('Aspirational', 'Target', 'Backup') else None,
                    interest=_int('interest', 1, 5), eligibility=request.form.get('eligibility') if request.form.get('eligibility') in ELIGIBILITY else 'Not checked',
                    data_note=_s('data_note'), data_source=_s('data_source', 200), data_year=_s('data_year', 20),
                    fee_note=_s('fee_note', 300), location=_s('location', 160), reason=_s('reason'))
    db.session.add(x)
    svc.audit(e, 'pref.entry_added', f'{lst.name}: {college} / {x.branch}', role)
    db.session.commit()
    return _back(e, 'prefs', f'l{lst.id}')


def _entry(e, xid):
    x = db.session.get(MsPrefEntry, xid)
    if not x or x.plist.enrolment_id != e.id:
        abort(404)
    return x


@mentorship_bp.route('/e/<int:eid>/prefs/entry/<int:xid>/update', methods=['POST'])
@login_required
def pref_entry_update(eid, xid):
    e, role = _ctx(eid)
    x = _entry(e, xid)
    if role == 'parent':
        x.parent_comment = _s('parent_comment')
    elif role == 'student':
        x.interest, x.reason = _int('interest', 1, 5), _s('reason')
        if request.form.get('request_review') == '1':
            x.review_status = 'Review requested'
    else:
        x.mentor_reco, x.review_status = _s('mentor_reco'), _s('review_status', 20) or x.review_status
        x.eligibility = request.form.get('eligibility') if request.form.get('eligibility') in ELIGIBILITY else x.eligibility
        x.data_note, x.data_source, x.data_year = _s('data_note'), _s('data_source', 200), _s('data_year', 20)
    svc.audit(e, 'pref.entry_updated', f'{x.college} / {x.branch}', role)
    db.session.commit()
    return _back(e, 'prefs', f'l{x.list_id}')


@mentorship_bp.route('/e/<int:eid>/prefs/entry/<int:xid>/move', methods=['POST'])
@login_required
def pref_entry_move(eid, xid):
    e, role = _ctx(eid, ('student', 'mentor', 'admin'))
    x = _entry(e, xid)
    rows = x.plist.entries.order_by(MsPrefEntry.position, MsPrefEntry.id).all()
    i = rows.index(x)
    j = i - 1 if request.form.get('dir') == 'up' else i + 1
    if 0 <= j < len(rows):
        rows[i], rows[j] = rows[j], rows[i]
        for n, r in enumerate(rows, 1):
            r.position = n
        svc.audit(e, 'pref.reordered', f'{x.college} / {x.branch}', role)
        db.session.commit()
    return _back(e, 'prefs', f'l{x.list_id}')


@mentorship_bp.route('/e/<int:eid>/prefs/entry/<int:xid>/delete', methods=['POST'])
@login_required
def pref_entry_delete(eid, xid):
    e, role = _ctx(eid, ('student', 'mentor', 'admin'))
    x = _entry(e, xid)
    lid = x.list_id
    svc.audit(e, 'pref.entry_removed', f'{x.college} / {x.branch}', role)
    db.session.delete(x)
    db.session.flush()
    for n, r in enumerate(db.session.get(MsPrefList, lid).entries.order_by(MsPrefEntry.position, MsPrefEntry.id).all(), 1):
        r.position = n
    db.session.commit()
    return _back(e, 'prefs', f'l{lid}')


# --------------------------------------------------------------------------- #
# calendar, messages, reports
# --------------------------------------------------------------------------- #
@mentorship_bp.route('/e/<int:eid>/events/add', methods=['POST'])
@login_required
def event_add(eid):
    e, role = _ctx(eid, ('student', 'mentor', 'admin'))
    d = svc.parse_date(request.form.get('starts_on'))
    title = _s('title', 240)
    if not d or not title:
        flash('Enter a title and a date.', 'danger')
        return _back(e, 'calendar')
    cat = request.form.get('category') if request.form.get('category') in EVENT_CATEGORIES else 'Other'
    ev = MsEvent(enrolment_id=e.id, title=title, category=cat, starts_on=d, ends_on=svc.parse_date(request.form.get('ends_on')),
                 notes=_s('notes'), source=_s('source', 300) if role in STAFF else 'Added by student',
                 verified_on=svc.parse_date(request.form.get('verified_on')) if role in STAFF else None, created_by=current_user.id)
    db.session.add(ev)
    svc.audit(e, 'event.added', f'{title} {d}', role)
    db.session.commit()
    flash('Added to the calendar.', 'success')
    return _back(e, 'calendar')


@mentorship_bp.route('/e/<int:eid>/events/<int:evid>/toggle', methods=['POST'])
@login_required
def event_toggle(eid, evid):
    e, role = _ctx(eid, ('student', 'mentor', 'admin'))
    ev = db.session.get(MsEvent, evid)
    if not ev or ev.enrolment_id != e.id:
        abort(404)                              # programme-level events are admin-maintained
    ev.done = not ev.done
    svc.audit(e, 'event.toggled', ev.title, role)
    db.session.commit()
    return _back(e, 'calendar')


@mentorship_bp.route('/e/<int:eid>/messages/post', methods=['POST'])
@login_required
def message_post(eid):
    e, role = _ctx(eid)
    if _premium_gate(role):
        abort(403)
    body = _s('body', 4000)
    if not body:
        return _back(e, 'messages')
    if role == 'student':
        aud, kind = 'student', 'message'
    elif role == 'parent':
        aud, kind = 'parent', 'message'
    else:
        aud = request.form.get('audience') if request.form.get('audience') in ('student', 'parent', 'all', 'internal') else 'student'
        kind = 'note' if aud == 'internal' else ('announcement' if request.form.get('announcement') == '1' else 'message')
    db.session.add(MsMessage(enrolment_id=e.id, sender_id=current_user.id, audience=aud, kind=kind, body=body))
    svc.audit(e, 'message.posted', f'{aud}/{kind}', role)
    db.session.commit()
    flash('Message saved in the portal. (Email / WhatsApp notification is not connected — recipients see it when they open the portal.)', 'success')
    return _back(e, 'messages')


@mentorship_bp.route('/e/<int:eid>/reports/generate', methods=['POST'])
@login_required
def report_generate(eid):
    e, role = _ctx(eid, STAFF)
    d = svc.report_data(e)
    rep = MsReport(enrolment_id=e.id, status='Draft', data_json=svc.jdump(d), data_through=svc.today(), generated_by=current_user.id)
    db.session.add(rep)
    svc.audit(e, 'report.generated', f'through {svc.today()}', role)
    db.session.commit()
    flash('Draft report generated from current records. Review it, then approve and share.', 'success')
    return _back(e, 'reports')


@mentorship_bp.route('/e/<int:eid>/reports/<int:rid>/<step>', methods=['POST'])
@login_required
def report_step(eid, rid, step):
    e, role = _ctx(eid, STAFF)
    rep = db.session.get(MsReport, rid)
    if not rep or rep.enrolment_id != e.id or step not in ('approve', 'share', 'delete'):
        abort(404)
    if step == 'approve' and rep.status == 'Draft':
        rep.status, rep.approved_by, rep.approved_at = 'Approved', current_user.id, svc.utcnow()
    elif step == 'share' and rep.status == 'Approved':
        rep.status, rep.shared_at = 'Shared', svc.utcnow()
    elif step == 'delete' and rep.status != 'Shared':
        db.session.delete(rep)
    else:
        flash('That step is not available for this report yet (approve before sharing).', 'danger')
        return _back(e, 'reports')
    svc.audit(e, f'report.{step}', f'#{rid}', role)
    db.session.commit()
    flash('Report updated.', 'success')
    return _back(e, 'reports')


def _report_for(eid, rid):
    e, role = _ctx(eid)
    rep = db.session.get(MsReport, rid)
    if not rep or rep.enrolment_id != e.id:
        abort(404)
    if role in ('student', 'parent') and rep.status != 'Shared':
        abort(404)
    return e, role, rep


@mentorship_bp.route('/e/<int:eid>/reports/<int:rid>')
@login_required
def report_view(eid, rid):
    e, role, rep = _report_for(eid, rid)
    return render_template('mentorship/report_view.html', e=e, role=role, rep=rep, d=svc.jload(rep.data_json), na=svc.na)


@mentorship_bp.route('/e/<int:eid>/reports/<int:rid>.pdf')
@login_required
def report_pdf(eid, rid):
    e, role, rep = _report_for(eid, rid)
    pdf = svc.report_pdf(svc.jload(rep.data_json), rep.status)
    if pdf is None:
        flash('PDF generation needs the ReportLab package on the server — use Print → Save as PDF from this page.', 'info')
        return redirect(url_for('mentorship.report_view', eid=e.id, rid=rep.id))
    return Response(pdf, mimetype='application/pdf', headers={
        'Content-Disposition': f'attachment; filename="mentorship-report-{e.id}-{rep.id}.pdf"'})


# --------------------------------------------------------------------------- #
# administrator controls
# --------------------------------------------------------------------------- #
@mentorship_bp.route('/admin')
@admin_required
def admin_home():
    progs = MsProgramme.query.order_by(MsProgramme.id).all()
    return render_template('admin/mentorship_admin.html', admin_tab='mentorship', programmes=progs,
                           enrolments=MsEnrolment.query.order_by(MsEnrolment.id.desc()).all(),
                           mentors=User.query.filter(User.tier.in_(['ea_mentor', 'admin'])).order_by(User.name).all(),
                           branches=MsBranch.query.order_by(MsBranch.position, MsBranch.id).all(),
                           rules=[(k, svc.rule(k), svc.RULE_HELP[k]) for k in svc.RULES],
                           prog_events=MsEvent.query.filter(MsEvent.programme_id != None).order_by(MsEvent.starts_on).all(),  # noqa: E711
                           EVENT_CATEGORIES=EVENT_CATEGORIES, links=MsParentLink.query.all(), today=svc.today(),
                           exams=MsExam.query.order_by(MsExam.active.desc(), MsExam.starts_on).all(), EXAM_STATUSES=EXAM_STATUSES,
                           fmt_range=xc.fmt_range)


@mentorship_bp.route('/admin/load-default', methods=['POST'])
@admin_required
def admin_load_default():
    svc.ensure_default_programme()
    svc.ensure_branches()
    flash('Standard 10-session programme and branch catalogue are available.', 'success')
    return redirect(url_for('mentorship.admin_home'))


@mentorship_bp.route('/admin/programme/new', methods=['POST'])
@admin_required
def admin_programme_new():
    name = _s('name', 160)
    if not name:
        flash('Name the programme.', 'danger')
        return redirect(url_for('mentorship.admin_home'))
    db.session.add(MsProgramme(name=name, description=_s('description'), tier=_s('tier', 60)))
    db.session.commit()
    flash('Programme created. Add its core sessions below.', 'success')
    return redirect(url_for('mentorship.admin_home'))


@mentorship_bp.route('/admin/programme/<int:pid>/session', methods=['POST'])
@admin_required
def admin_template_add(pid):
    p = db.session.get(MsProgramme, pid) or abort(404)
    title = _s('title', 200)
    if not title:
        flash('Give the session a title.', 'danger')
        return redirect(url_for('mentorship.admin_home'))
    last = p.templates.order_by(MsSessionTemplate.position.desc()).first()
    db.session.add(MsSessionTemplate(programme_id=p.id, position=(last.position if last else 0) + 1, title=title, topics=_s('topics'),
                                     deliverable=_s('deliverable', 300), duration_min=_int('duration_min', 5, 480) or 60))
    db.session.commit()
    flash('Core session added to the programme template (applies to newly enrolled students).', 'success')
    return redirect(url_for('mentorship.admin_home') + f'#p{p.id}')


@mentorship_bp.route('/admin/template/<int:tid>/<op>', methods=['POST'])
@admin_required
def admin_template_op(tid, op):
    t = db.session.get(MsSessionTemplate, tid) or abort(404)
    if op == 'save':
        t.title, t.topics, t.deliverable = _s('title', 200) or t.title, _s('topics'), _s('deliverable', 300)
        t.duration_min = _int('duration_min', 5, 480) or t.duration_min
        t.active = request.form.get('active') == '1'
    elif op in ('up', 'down'):
        rows = t.programme.templates.order_by(MsSessionTemplate.position, MsSessionTemplate.id).all()
        i = rows.index(t)
        j = i - 1 if op == 'up' else i + 1
        if 0 <= j < len(rows):
            rows[i], rows[j] = rows[j], rows[i]
            for n, r in enumerate(rows, 1):
                r.position = n
    else:
        abort(404)
    db.session.commit()
    return redirect(url_for('mentorship.admin_home') + f'#p{t.programme_id}')


@mentorship_bp.route('/admin/enrol', methods=['POST'])
@admin_required
def admin_enrol():
    student = User.query.filter_by(email=_s('student_email', 200).lower()).first()
    prog = db.session.get(MsProgramme, _int('programme_id') or 0)
    if not student or not prog:
        flash('Student account (by email) and programme are required. The student must register on the site first.', 'danger')
        return redirect(url_for('mentorship.admin_home'))
    mentor = User.query.filter_by(email=_s('mentor_email', 200).lower()).first() if _s('mentor_email') else None
    if mentor and not (mentor.is_ea_mentor or mentor.is_admin):
        flash('That mentor account does not have the EA Mentor role.', 'danger')
        return redirect(url_for('mentorship.admin_home'))
    if MsEnrolment.query.filter_by(student_id=student.id, programme_id=prog.id, status='Active').first():
        flash('This student is already enrolled in that programme.', 'info')
        return redirect(url_for('mentorship.admin_home'))
    e = svc.enrol(student, mentor, prog, start=svc.parse_date(request.form.get('start_date')),
                  end=svc.parse_date(request.form.get('end_date')), extra_quota=_int('extra_quota', 0, 99) or 0)
    e.grade = _s('grade', 40) or e.grade
    db.session.commit()
    flash(f'{student.name} enrolled with {prog.templates.filter_by(active=True).count()} core sessions.', 'success')
    return redirect(url_for('mentorship.admin_home') + f'#e{e.id}')


@mentorship_bp.route('/admin/enrolment/<int:eid>/update', methods=['POST'])
@admin_required
def admin_enrolment_update(eid):
    e = db.session.get(MsEnrolment, eid) or abort(404)
    mem = _s('mentor_email', 200).lower()
    if mem:
        m = User.query.filter_by(email=mem).first()
        if not m or not (m.is_ea_mentor or m.is_admin):
            flash('That mentor account does not have the EA Mentor role.', 'danger')
            return redirect(url_for('mentorship.admin_home'))
        e.mentor_id = m.id
    e.extra_quota = _int('extra_quota', 0, 99) or 0
    e.status = request.form.get('status') if request.form.get('status') in ('Active', 'Paused', 'Completed') else e.status
    e.start_date = svc.parse_date(request.form.get('start_date')) or e.start_date
    e.end_date = svc.parse_date(request.form.get('end_date'))
    e.timezone = _s('timezone', 60) or e.timezone
    svc.audit(e, 'enrolment.updated', f'mentor={e.mentor_id} quota={e.extra_quota} status={e.status}', 'admin')
    db.session.commit()
    flash('Enrolment updated.', 'success')
    return redirect(url_for('mentorship.admin_home') + f'#e{e.id}')


@mentorship_bp.route('/admin/parent', methods=['POST'])
@admin_required
def admin_parent_link():
    import re
    import secrets
    e = db.session.get(MsEnrolment, _int('enrolment_id') or 0)
    email = _s('parent_email', 200).lower()
    parent = User.query.filter(db.func.lower(User.email) == email).first() if email else None
    created_pw = None
    if e is None:
        flash('That student record was not found — refresh the page and try again.', 'danger')
        return redirect(url_for('mentorship.admin_home'))
    if not re.fullmatch(r'[^@\s]+@[^@\s]+\.[^@\s]+', email):
        flash('Enter a valid parent email address.', 'danger')
        return redirect(url_for('mentorship.admin_home') + f'#e{e.id}')
    if parent is None and request.form.get('create') == '1':
        from app.extensions import bcrypt
        created_pw = secrets.token_urlsafe(9)
        parent = User(name=_s('parent_name', 120) or email.split('@')[0].replace('.', ' ').title(), email=email, tier='free',
                      password_hash=bcrypt.generate_password_hash(created_pw).decode())
        db.session.add(parent)
        db.session.flush()
    if parent is None:
        flash(f'{email} has no EduAakashaA account yet. Tick “Create the parent account” and link again — they will be emailed their login details.', 'danger')
    elif parent.id == e.student_id:
        flash('The parent account cannot be the student’s own account.', 'danger')
        db.session.rollback()
    elif MsParentLink.query.filter_by(enrolment_id=e.id, parent_id=parent.id).first():
        flash('That parent is already linked.', 'info')
    else:
        db.session.add(MsParentLink(enrolment_id=e.id, parent_id=parent.id, relation=_s('relation', 40) or 'Parent'))
        svc.audit(e, 'parent.linked', parent.email + (' (account created)' if created_pw else ''), 'admin')
        db.session.commit()
        msg = 'Parent linked to the student record.'
        if created_pw:
            from app.routes.admin_portal import _email_new_member
            from app.services.mailer import is_configured as _mail_ok
            _email_new_member(parent, created_pw)
            msg = (f'Parent account created for {parent.email} and linked. ' +
                   ('Login details were emailed to them.' if _mail_ok() else f'Email is not configured, so share these login details yourself — email {parent.email}, temporary password {created_pw}'))
        flash(msg, 'success')
    return redirect(url_for('mentorship.admin_home') + f'#e{e.id}')


@mentorship_bp.route('/admin/parent/<int:lid>/remove', methods=['POST'])
@admin_required
def admin_parent_unlink(lid):
    link = db.session.get(MsParentLink, lid) or abort(404)
    svc.audit(db.session.get(MsEnrolment, link.enrolment_id), 'parent.unlinked', link.parent.email, 'admin')
    db.session.delete(link)
    db.session.commit()
    return redirect(url_for('mentorship.admin_home'))


@mentorship_bp.route('/admin/rules', methods=['POST'])
@admin_required
def admin_rules():
    for k in svc.RULES:
        v = _int(k, 0, 365)
        if v is not None:
            row = db.session.get(Setting, 'ms_rule_' + k) or Setting(key='ms_rule_' + k)
            row.value = str(v)
            db.session.add(row)
    db.session.commit()
    flash('Attention rules saved.', 'success')
    return redirect(url_for('mentorship.admin_home') + '#rules')


@mentorship_bp.route('/admin/event', methods=['POST'])
@admin_required
def admin_event():
    p = db.session.get(MsProgramme, _int('programme_id') or 0)
    d = svc.parse_date(request.form.get('starts_on'))
    title = _s('title', 240)
    if not p or not d or not title:
        flash('Programme, title and date are required.', 'danger')
    else:
        db.session.add(MsEvent(programme_id=p.id, title=title, category=request.form.get('category') if request.form.get('category') in EVENT_CATEGORIES else 'Other',
                               starts_on=d, ends_on=svc.parse_date(request.form.get('ends_on')), source=_s('source', 300),
                               verified_on=svc.parse_date(request.form.get('verified_on')), notes=_s('notes'), created_by=current_user.id))
        db.session.commit()
        flash('Calendar event added for every student in the programme.', 'success')
    return redirect(url_for('mentorship.admin_home') + '#calendar')


@mentorship_bp.route('/admin/event/<int:evid>/delete', methods=['POST'])
@admin_required
def admin_event_delete(evid):
    ev = db.session.get(MsEvent, evid) or abort(404)
    db.session.delete(ev)
    db.session.commit()
    return redirect(url_for('mentorship.admin_home') + '#calendar')


@mentorship_bp.route('/admin/branch', methods=['POST'])
@admin_required
def admin_branch():
    name = _s('name', 120)
    if not name:
        flash('Name the branch.', 'danger')
        return redirect(url_for('mentorship.admin_home') + '#branches')
    b = db.session.get(MsBranch, _int('id') or 0) if _int('id') else MsBranch.query.filter_by(name=name).first()
    b = b or MsBranch(name=name, position=MsBranch.query.count() + 1)
    b.name = name
    for f in ('studies', 'subjects', 'skills', 'projects', 'careers', 'questions'):
        setattr(b, f, _s(f))
    b.active = request.form.get('active', '1') == '1'
    db.session.add(b)
    db.session.commit()
    flash('Branch saved.', 'success')
    return redirect(url_for('mentorship.admin_home') + '#branches')


# --------------------------------------------------------------------------- #
# exam focus, calendar invitations, alerts
# --------------------------------------------------------------------------- #
def _focused_exams(e):
    ids = [f.exam_id for f in MsExamFocus.query.filter_by(enrolment_id=e.id).all()]
    return MsExam.query.filter(MsExam.id.in_(ids), MsExam.active == True).order_by(MsExam.starts_on).all() if ids else []  # noqa: E712


@mentorship_bp.route('/e/<int:eid>/exams/<int:xid>/focus', methods=['POST'])
@login_required
def exam_focus(eid, xid):
    e, role = _ctx(eid, ('student', 'mentor', 'admin'))
    if _premium_gate(role):
        abort(403)
    x = db.session.get(MsExam, xid)
    if not x or not x.active:
        abort(404)
    f = MsExamFocus.query.filter_by(enrolment_id=e.id, exam_id=x.id).first()
    want = request.form.get('on')
    if f and want != '1':
        db.session.delete(f)
        svc.audit(e, 'exam.unfollowed', x.name, role)
        flash(f'Stopped following {x.name}.', 'info')
    elif not f:
        db.session.add(MsExamFocus(enrolment_id=e.id, exam_id=x.id, created_by=current_user.id))
        svc.audit(e, 'exam.followed', x.name, role)
        flash(f'Now following {x.name} — it is on the calendar and you will be alerted if its schedule changes.', 'success')
    aid = request.form.get('alert_id', type=int)
    if aid:
        xc.mark_read(current_user, [aid])
    db.session.commit()
    return _back(e, 'calendar', 'exams')


@mentorship_bp.route('/e/<int:eid>/calendar.ics')
@login_required
def calendar_ics(eid):
    e, role = _ctx(eid)
    if _premium_gate(role):
        abort(403)
    exams = _focused_exams(e)
    if not exams:
        flash('Follow at least one exam first, then download the invitation.', 'info')
        return _back(e, 'calendar', 'exams')
    return Response(xc.make_ics(exams), mimetype='text/calendar', headers={
        'Content-Disposition': 'attachment; filename="eduaakashaa-exams.ics"'})


@mentorship_bp.route('/e/<int:eid>/exams/<int:xid>.ics')
@login_required
def exam_ics(eid, xid):
    e, role = _ctx(eid)
    if _premium_gate(role):
        abort(403)
    x = db.session.get(MsExam, xid)
    if not x or not x.active:
        abort(404)
    return Response(xc.make_ics([x], x.name), mimetype='text/calendar', headers={
        'Content-Disposition': f'attachment; filename="exam-{x.id}.ics"'})


@mentorship_bp.route('/e/<int:eid>/calendar/email', methods=['POST'])
@login_required
def calendar_email(eid):
    """Email the invitation (.ics attached) to any personal address. Limited to 5 sends/hour per user."""
    e, role = _ctx(eid)
    if _premium_gate(role):
        abort(403)
    to = _s('email', 200).lower()
    import re
    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", to):
        flash('Enter a valid email address.', 'danger')
        return _back(e, 'calendar', 'share')
    exams = _focused_exams(e)
    if not exams:
        flash('Follow at least one exam first, then email the invitation.', 'info')
        return _back(e, 'calendar', 'exams')
    from datetime import timedelta as _td
    since = svc.utcnow() - _td(hours=1)
    if MsAudit.query.filter(MsAudit.user_id == current_user.id, MsAudit.action == 'calendar.emailed', MsAudit.created_at >= since).count() >= 5:
        flash('You have sent several invitations this hour — please try again later, or download the .ics file instead.', 'danger')
        return _back(e, 'calendar', 'share')
    if not mailer.is_configured():
        flash('Email sending is not configured on this server yet, so nothing was sent. Download the .ics file instead '
              '(it opens in Google, Apple and Outlook calendars).', 'danger')
        return _back(e, 'calendar', 'share')
    rows = ''.join(f'<li><strong>{xc._esc(x.name)}</strong> — {xc._esc(xc.fmt_range(x))} ({xc._esc(x.status)})</li>' for x in exams)
    text = 'Your EduAakashaA exam calendar (attached as an .ics invitation):\n' + '\n'.join(
        f'- {x.name}: {xc.fmt_range(x)} ({x.status})' for x in exams) + '\n\nTentative or expected dates can change — confirm on the official notice.'
    html = xc.branded_shell('<h2 style="margin:0 0 8px;color:#0E3A8A;font-family:Georgia,serif">Your exam calendar</h2>'
                            f'<ul style="line-height:1.6">{rows}</ul><p style="font-size:13px">Open the attached .ics file to add these to your calendar. '
                            'Tentative or expected dates can change — confirm on the official notice.</p>')
    mailer.send_async(to, 'Your EduAakashaA exam calendar', text, html, from_addr=mailer.INFO_FROM, reply_to=mailer.INFO_FROM,
                      attachments=[('eduaakashaa-exams.ics', xc.make_ics(exams), 'text/calendar')])
    svc.audit(e, 'calendar.emailed', f'{len(exams)} exam(s)', role)
    db.session.commit()
    flash(f'Invitation queued to {to}. Check your inbox (and spam) in a minute.', 'success')
    return _back(e, 'calendar', 'share')


@mentorship_bp.route('/alerts/read', methods=['POST'])
@login_required
def alerts_read():
    ids = request.form.getlist('alert_id', type=int)
    if request.form.get('all') == '1':
        ids = [a.id for a in xc.unread_alerts(current_user, limit=200)]
    if ids:
        xc.mark_read(current_user, ids)
        db.session.commit()
    nxt = request.form.get('next', '')
    return redirect(nxt if nxt.startswith('/mentorship/') else url_for('mentorship.index'))


# --- admin: exam catalogue ----------------------------------------------------------------------------------
@mentorship_bp.route('/admin/exams/load-default', methods=['POST'])
@admin_required
def admin_exams_default():
    n = xc.ensure_default_exams()
    flash(f'{n} exam(s) added to the catalogue (members are not alerted for the starter list).', 'success')
    return redirect(url_for('mentorship.admin_home') + '#exams')


@mentorship_bp.route('/admin/exams/save', methods=['POST'])
@admin_required
def admin_exam_save():
    name, d = _s('name', 200), svc.parse_date(request.form.get('starts_on'))
    if not name or not d:
        flash('Exam name and a start date are required.', 'danger')
        return redirect(url_for('mentorship.admin_home') + '#exams')
    exam = db.session.get(MsExam, _int('id')) if _int('id') else None
    before = xc.snapshot(exam) if exam else None
    exam = exam or MsExam(name=name, starts_on=d)
    exam.name, exam.starts_on = name, d
    exam.ends_on = svc.parse_date(request.form.get('ends_on'))
    exam.category = request.form.get('category') if request.form.get('category') in EVENT_CATEGORIES else (exam.category or 'Other')
    exam.stream = _s('stream', 40)
    exam.status = request.form.get('status') if request.form.get('status') in EXAM_STATUSES else 'Expected'
    exam.window_note, exam.source, exam.notes = _s('window_note', 200), _s('source', 300), _s('notes')
    exam.verified_on = svc.parse_date(request.form.get('verified_on'))
    exam.active = request.form.get('active', '1') == '1'
    db.session.add(exam)
    db.session.flush()
    alert = xc.record_change(exam, before)
    db.session.commit()
    if not alert:
        flash('Exam saved (no schedule change, so nobody was alerted).' if before else 'Exam saved.', 'success')
    else:
        queued = xc.email_alert(alert)
        db.session.commit()
        flash(f'Saved. Alert posted in every member portal' + (f' and {queued} email(s) queued from info@.' if queued
              else '. (Email not sent: no mail transport configured.)'), 'success')
    return redirect(url_for('mentorship.admin_home') + '#exams')


@mentorship_bp.route('/admin/exams/<int:xid>/delete', methods=['POST'])
@admin_required
def admin_exam_delete(xid):
    exam = db.session.get(MsExam, xid) or abort(404)
    before = xc.snapshot(exam)
    exam.active = False                                         # soft-remove so followers get an alert and history stays
    alert = xc.record_change(exam, before)
    db.session.commit()
    if alert:
        xc.email_alert(alert)
    flash('Exam removed from the catalogue; members who follow it were alerted.', 'success')
    return redirect(url_for('mentorship.admin_home') + '#exams')
