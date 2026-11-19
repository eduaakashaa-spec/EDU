"""EduPulse App: one mobile-first app for students, parents and mentors over the existing portal data.

Nothing here owns data. It reads the mentorship enrolments (sessions, actions, calendar, messages), the Member Home tile
registry (practice centres and tools) and the admin announcements and schedule, and decides what each role may see:

  student  own enrolments; every action that is not cancelled
  parent   enrolments they are linked to (MsParentLink); only parent-visible sessions and actions
  mentor   EA mentors: enrolments assigned to them; admins: every enrolment; alumni College Guides: none (their own portal)

Access is decided again by the full portal when a deep link is opened, so the app never widens what a person can see.
"""
from datetime import timedelta

from flask import url_for

from app.extensions import db
from app.models import Announcement, ScheduleEvent
from sqlalchemy.orm import selectinload

from app.models_mentorship import (MsAction, MsCheckin, MsEnrolment, MsEvent, MsExam, MsExamFocus, MsMessage,
                                   MsMessageRead, MsParentLink, MsPrefDates, MsPrefEntry, MsPrefList, MsReview, MsSession)
from app.services import member_hub
from app.services import mentorship as ms

ROLES = ('student', 'parent', 'mentor')
ROLE_LABEL = {'student': 'Student', 'parent': 'Parent', 'mentor': 'Mentor'}
UPCOMING_DAYS = 45


# --------------------------------------------------------------------------- #
# Roles
# --------------------------------------------------------------------------- #
def is_mentor_user(user):
    return bool(user.is_ea_mentor or user.is_mentor or user.is_admin)


def parent_enrolments(user):
    eids = [x.enrolment_id for x in MsParentLink.query.filter_by(parent_id=user.id).all()]
    if not eids:
        return []
    return (MsEnrolment.query.filter(MsEnrolment.id.in_(eids), MsEnrolment.status != ms.REMOVED)
            .order_by(MsEnrolment.id).all())


def student_enrolments(user):
    return (MsEnrolment.query.filter(MsEnrolment.student_id == user.id, MsEnrolment.status != ms.REMOVED)
            .order_by(MsEnrolment.id.desc()).all())


def mentor_enrolments(user):
    opts = (selectinload(MsEnrolment.student), selectinload(MsEnrolment.programme), selectinload(MsEnrolment.mentor))
    if user.is_admin:
        return MsEnrolment.query.options(*opts).filter(MsEnrolment.status == 'Active').order_by(MsEnrolment.id.desc()).all()
    if user.is_ea_mentor:
        return (MsEnrolment.query.options(*opts).filter(MsEnrolment.mentor_id == user.id, MsEnrolment.status != ms.REMOVED)
                .order_by(MsEnrolment.id.desc()).all())
    return []


def roles_for(user):
    """Views this account may switch between, most specific first."""
    out = []
    if is_mentor_user(user):
        out.append('mentor')
    if parent_enrolments(user):
        out.append('parent')
    if not user.is_staff and not user.is_mentor:
        out.append('student')
    return out or ['student']


def resolve_role(user, wanted):
    roles = roles_for(user)
    return wanted if wanted in roles else roles[0]


def login_allowed(user, role):
    """(ok, message) for the role picked on the sign-in screen."""
    if role == 'mentor' and not is_mentor_user(user):
        return False, 'This account is not registered as a mentor. Choose Student or Parent to sign in.'
    if role == 'parent' and not parent_enrolments(user) and not user.is_staff:
        return True, 'Signed in. No student is linked to this parent account yet; your mentor or our team can link one.'
    return True, ''


# --------------------------------------------------------------------------- #
# Enrolment cards
# --------------------------------------------------------------------------- #
def _name(e):
    return e.preferred_name or (e.student.name if e.student else 'Student')


def _first(name):
    return (name or '').split(' ')[0] or name


def _visible_sessions(e, role):
    rows = ms._sessions(e)
    return [s for s in rows if s.parent_visible] if role == 'parent' else rows


def _next_session(e, role):
    now = ms.utcnow()
    for s in sorted((s for s in _visible_sessions(e, role) if s.status in ('Planned', 'Rescheduled') and s.planned_at),
                    key=lambda s: s.planned_at):
        if s.planned_at >= now - timedelta(hours=1):
            return {'title': s.title, 'when': ms.fmt_dt(s.planned_at, e.timezone), 'agenda': s.agenda,
                    'days': (ms.to_local(s.planned_at, e.timezone).date() - ms.today()).days}
    return None


def _actions(e, role, limit=6):
    """Open actions for this role, most urgent first (overdue, due today, due soon, then the rest by date)."""
    audience = 'parent' if role == 'parent' else 'student'
    rank = {'Overdue': 0, 'Requires mentor attention': 1, 'Blocked': 1, 'Due today': 2, 'Due soon': 3, 'Open': 4}
    rows = []
    for a in ms._actions(e):            # one cached read per enrolment (pre-loaded in bulk for the mentor list)
        if a.status in ('Completed', 'Closed', 'Cancelled') or (audience == 'parent' and not a.parent_visible):
            continue
        state = ms.action_state(a)
        rows.append({'id': a.id, 'title': a.title, 'owner': ms.OWNER_LABEL.get(a.owner or 'student', 'Student'),
                     'mine': (a.owner or 'student') == ('parent' if role == 'parent' else 'student'),
                     'due': a.due_date, 'state': state, 'priority': a.priority or 'Medium',
                     'tone': {'Overdue': 'bad', 'Blocked': 'bad', 'Requires mentor attention': 'bad',
                              'Due today': 'warn', 'Due soon': 'warn'}.get(state, 'ok')})
    rows.sort(key=lambda r: (rank.get(r['state'], 5), not r['mine'], r['due'] or ms.today() + timedelta(days=3650)))
    return rows[:limit], len(rows)


def _upcoming(e, days=UPCOMING_DAYS, limit=6):
    start, end = ms.today(), ms.today() + timedelta(days=days)
    out = []
    for i in ms.events_for(e):
        if i.get('done') or not i.get('date') or not (start <= i['date'] <= end):
            continue
        if i['kind'] == 'action':           # actions already have their own list
            continue
        out.append({'date': i['date'], 'title': i['title'], 'category': i.get('category') or '',
                    'days': (i['date'] - start).days, 'who': _first(_name(e))})
    return out[:limit]


def card(e, role, user):
    ss = ms.session_stats(e)
    ast = ms.action_stats(e, only_visible_to_parent=(role == 'parent'))
    acts, open_n = _actions(e, role)
    c = {'id': e.id, 'name': _name(e), 'first': _first(_name(e)), 'grade': e.grade or '', 'status': e.status,
         'programme': e.programme.name if e.programme else 'Mentorship',
         'mentor': e.mentor.name if e.mentor else 'To be assigned',
         'sessions': ss, 'actions': ast, 'open_actions': acts, 'open_n': open_n,
         'next': _next_session(e, role), 'upcoming': [] if role == 'mentor' else _upcoming(e),
         'unread': ms._memo(('ep_unread', e.id), lambda: ms.unread_count(e, user, _msg_role(user, role))),
         'url': url_for('mentorship.workspace', eid=e.id, tab='home'),
         'url_actions': url_for('mentorship.workspace', eid=e.id, tab='actions'),
         'url_messages': url_for('mentorship.workspace', eid=e.id, tab='messages'),
         'url_calendar': url_for('mentorship.workspace', eid=e.id, tab='calendar'),
         'url_reports': url_for('mentorship.workspace', eid=e.id, tab='reports')}
    if role == 'mentor':
        level, reasons = ms.attention(e)
        c['attention'], c['reasons'] = level, reasons
    return c


def _msg_role(user, role):
    return 'admin' if (role == 'mentor' and user.is_admin) else role


# --------------------------------------------------------------------------- #
# Bulk loading for list views. A mentor (or an admin) may follow dozens of students; reading each one separately costs
# about ten database round trips per student, which is slow on a remote database. prime() reads the same rows for every
# enrolment in a few queries and puts them in the per-request cache that the mentorship service already reads from.
# --------------------------------------------------------------------------- #
def _by_eid(rows, attr='enrolment_id'):
    out = {}
    for r in rows:
        out.setdefault(getattr(r, attr), []).append(r)
    return out


def prime(enrolments, user, role):
    if not enrolments:
        return
    from flask import g
    store = g.__dict__.setdefault('_ms_memo', {})
    ids = [e.id for e in enrolments]
    sessions = _by_eid(MsSession.query.filter(MsSession.enrolment_id.in_(ids)).order_by(MsSession.position).all())
    actions = _by_eid(MsAction.query.filter(MsAction.enrolment_id.in_(ids)).all())
    focus = {}
    for eid, xid in db.session.query(MsExamFocus.enrolment_id, MsExamFocus.exam_id).filter(MsExamFocus.enrolment_id.in_(ids)):
        focus.setdefault(eid, set()).add(xid)
    last = {}
    for c in (MsCheckin.query.filter(MsCheckin.enrolment_id.in_(ids), MsCheckin.status.in_(['Submitted', 'Reviewed']))
              .order_by(MsCheckin.week_start.desc()).all()):
        last.setdefault(c.enrolment_id, c)
    window = ms.today() + timedelta(days=ms.rule('exam_window_days'))
    pids = {e.programme_id for e in enrolments}
    soon = (MsEvent.query.filter(db.or_(MsEvent.enrolment_id.in_(ids), MsEvent.programme_id.in_(pids)),
                                 MsEvent.category.in_(ms.ATTENTION_EXAM_CATS), MsEvent.starts_on >= ms.today(),
                                 MsEvent.starts_on <= window).all())
    read = db.session.query(MsMessageRead.message_id).filter(MsMessageRead.user_id == user.id)
    unread = dict(db.session.query(MsMessage.enrolment_id, db.func.count(MsMessage.id))
                  .filter(MsMessage.enrolment_id.in_(ids), MsMessage.sender_id != user.id,
                          MsMessage.audience.in_(ms.visible_audiences(_msg_role(user, role))), ~MsMessage.id.in_(read))
                  .group_by(MsMessage.enrolment_id).all())
    for e in enrolments:
        store[('sessions', e.id)] = sessions.get(e.id, [])
        store[('actions', e.id)] = actions.get(e.id, [])
        store[('focus', e.id)] = focus.get(e.id, set())
        store[('last_checkin', e.id)] = last.get(e.id)
        store[('exam_soon', e.id)] = next((x for x in soon if x.enrolment_id == e.id or x.programme_id == e.programme_id), None)
        store[('ep_unread', e.id)] = unread.get(e.id, 0)


def mentor_agenda(enrolments, days):
    """Plan screen for a mentor: the same kinds of dates as each student's calendar (sessions, student and programme events,
    followed exams, review dates, college-list deadlines), read for every student in a few queries."""
    if not enrolments:
        return []
    start, end = ms.today(), ms.today() + timedelta(days=days)
    ids = [e.id for e in enrolments]
    by_id = {e.id: e for e in enrolments}
    by_prog = {}
    for e in enrolments:
        by_prog.setdefault(e.programme_id, []).append(e)
    items = []

    def add(e, d, title, cat):
        if d and start <= d <= end:
            items.append({'date': d, 'title': title, 'category': cat, 'days': (d - start).days, 'who': _first(_name(e))})

    for s in (MsSession.query.filter(MsSession.enrolment_id.in_(ids), MsSession.status.in_(['Planned', 'Rescheduled']),
                                     MsSession.planned_at != None).all()):  # noqa: E711
        e = by_id[s.enrolment_id]
        add(e, ms.to_local(s.planned_at, e.timezone).date(), s.title, 'Mentorship session')
    for x in (MsEvent.query.filter(db.or_(MsEvent.enrolment_id.in_(ids), MsEvent.programme_id.in_(list(by_prog))),
                                   MsEvent.done == False, MsEvent.starts_on >= start, MsEvent.starts_on <= end).all()):  # noqa: E712
        for e in ([by_id[x.enrolment_id]] if x.enrolment_id in by_id else by_prog.get(x.programme_id, [])):
            add(e, x.starts_on, x.title, x.category or 'Event')
    pairs = db.session.query(MsExamFocus.enrolment_id, MsExamFocus.exam_id).filter(MsExamFocus.enrolment_id.in_(ids)).all()
    exams = {x.id: x for x in MsExam.query.filter(MsExam.id.in_({p[1] for p in pairs}), MsExam.active == True).all()} if pairs else {}  # noqa: E712
    for eid, xid in pairs:
        x = exams.get(xid)
        if x:
            add(by_id[eid], x.starts_on, x.name, x.category or 'Exam')
    for r in MsReview.query.filter(MsReview.enrolment_id.in_(ids), MsReview.next_review_date != None).all():  # noqa: E711
        add(by_id[r.enrolment_id], r.next_review_date, 'Next review after ' + r.label, 'Quarterly review')
    for d, x, lst in (db.session.query(MsPrefDates, MsPrefEntry, MsPrefList).join(MsPrefEntry, MsPrefEntry.id == MsPrefDates.entry_id)
                      .join(MsPrefList, MsPrefList.id == MsPrefEntry.list_id).filter(MsPrefList.enrolment_id.in_(ids)).all()):
        e = by_id[lst.enrolment_id]
        add(e, d.app_open, 'Applications open: ' + x.college, 'Admission deadline')
        add(e, d.app_deadline, 'Application deadline: ' + x.college, 'Admission deadline')
    return items


def mentor_overview(cards):
    return {'students': len(cards),
            'attention': sum(1 for c in cards if c.get('attention') == 'attention'),
            'watch': sum(1 for c in cards if c.get('attention') == 'watch'),
            'overdue': sum(c['actions']['overdue'] for c in cards),
            'unread': sum(c['unread'] for c in cards),
            'sessions_week': sum(1 for c in cards if c['next'] and 0 <= c['next']['days'] <= 7)}


def sort_for_mentor(cards):
    order = {'attention': 0, 'watch': 1, 'ok': 2}
    return sorted(cards, key=lambda c: (order.get(c.get('attention'), 3), -(c['actions']['overdue']), c['name'].lower()))


# --------------------------------------------------------------------------- #
# Notices, calendar, practice and tools
# --------------------------------------------------------------------------- #
def announcements(role, limit=4):
    aud = {'student': ('all', 'students'), 'parent': ('all', 'parents')}.get(role, ('all', 'students', 'parents'))
    return (Announcement.query.filter(Announcement.active == True, Announcement.audience.in_(aud))  # noqa: E712
            .order_by(Announcement.pinned.desc(), Announcement.created_at.desc()).limit(limit).all())


def schedule(days=UPCOMING_DAYS):
    now = ms.utcnow()
    rows = (ScheduleEvent.query.filter(ScheduleEvent.starts_at >= now - timedelta(days=1),
                                       ScheduleEvent.starts_at <= now + timedelta(days=days))
            .order_by(ScheduleEvent.starts_at).limit(30).all())
    return [{'date': ms.to_local(r.starts_at, 'Asia/Kolkata').date(), 'title': r.name, 'category': r.event_type or 'Event',
             'days': (ms.to_local(r.starts_at, 'Asia/Kolkata').date() - ms.today()).days, 'who': 'Everyone',
             'important': r.important} for r in rows]


def calendar(cards_and_enrolments, days=UPCOMING_DAYS, bulk=False):
    """Merged, date-ordered agenda for the Plan screen: every followed student's dates plus the portal schedule.
    bulk=True (mentor view) reads all students' dates in a few queries instead of one calendar per student."""
    items = []
    if bulk:
        items.extend(mentor_agenda(cards_and_enrolments, days))
    else:
        for e in cards_and_enrolments:
            items.extend(_upcoming(e, days=days, limit=60))
    items.extend(schedule(days))
    seen, out = set(), []
    for i in sorted(items, key=lambda i: (i['date'], i['title'])):
        k = (i['date'], i['title'], i['who'])
        if k not in seen:
            seen.add(k)
            out.append(i)
    return out


def tool_categories(user):
    """Member Home categories resolved for this person (URLs, locks), reused as the app's Explore screen."""
    return member_hub.build(user)


PRACTICE_KEYS = ('edupulse', 'school')


def practice_tiles(user, role):
    """EduPulse practice centres, open ones first. Mentor view keeps the mentor dashboards; others never see staff tiles."""
    tiles = []
    for cat in tool_categories(user):
        for t in cat['tiles']:
            in_scope = cat['key'] in PRACTICE_KEYS and ('EduPulse' in t['title'] or 'Planner' in t['title'] or 'Mock' in t['title'])
            if role == 'mentor' and cat['key'] == 'staff':
                in_scope = True
            elif t.get('staff') and role != 'mentor':
                in_scope = False
            if in_scope and t.get('url'):
                tiles.append(t)
    return sorted(tiles, key=lambda t: (t['locked'], not t.get('staff'), t['title']))


def short_title(title):
    for cut in (' Mock Test Centre', ' Practice Centre'):
        title = title.replace(cut, '')
    return title.replace('EduPulse-', '').replace('EduPulse – ', '')


def greeting(hour):
    return 'Good morning' if hour < 12 else ('Good afternoon' if hour < 17 else 'Good evening')


def week_sessions_done(enrolments):
    """Sessions completed in the last 7 days across these enrolments (a small activity signal for the hero)."""
    if not enrolments:
        return 0
    since = ms.utcnow() - timedelta(days=7)
    return (db.session.query(MsSession.id).filter(MsSession.enrolment_id.in_([e.id for e in enrolments]),
                                                  MsSession.status == 'Completed', MsSession.actual_at >= since).count())
