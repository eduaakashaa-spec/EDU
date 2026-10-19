"""Mentorship Portal — business rules shared by the student, mentor and parent views.

Everything here reads the same tables (app/models_mentorship.py); the dashboards never
keep their own copy of a number.  Rules that a non-developer may want to tune
(`RULES`) can be overridden from Admin → Mentorship → Rules (stored in `Setting`).
"""
import io
import json
from datetime import date, datetime, timedelta, timezone

from flask_login import current_user

from app.extensions import db
from app.models_membership import Setting
from app.models_mentorship import (
    MsAction, MsAudit, MsBranch, MsBranchRating, MsCheckin, MsEnrolment, MsEvent, MsKpi, MsMessage,
    MsMessageRead, MsParentLink, MsPrefEntry, MsPrefList, MsProgramme, MsReport, MsReview, MsSession,
    MsSessionTemplate,
)

# --------------------------------------------------------------------------- #
# Configurable rules
# --------------------------------------------------------------------------- #
RULES = {
    'due_soon_days': 3,          # an open action due within N days is "Due soon"
    'overdue_attention': 3,      # N or more overdue actions → needs mentor attention
    'checkin_gap_days': 10,      # no submitted weekly check-in for N days → needs attention
    'low_confidence': 2,         # latest confidence at/below this → mentor should look
    'exam_window_days': 21,      # an exam within N days with open prep actions → attention
}
RULE_HELP = {
    'due_soon_days': 'Open action is shown as "Due soon" when due within this many days.',
    'overdue_attention': 'This many overdue actions flags the student for mentor attention.',
    'checkin_gap_days': 'Days without a submitted weekly check-in before the student is flagged.',
    'low_confidence': 'A latest confidence rating at or below this (1–5) is flagged for a check-in conversation.',
    'exam_window_days': 'An exam this close with unfinished preparation actions is flagged.',
}


def rule(name):
    row = db.session.get(Setting, 'ms_rule_' + name)
    try:
        return int(row.value) if row and row.value not in (None, '') else RULES[name]
    except (TypeError, ValueError):
        return RULES[name]


# --------------------------------------------------------------------------- #
# Time zone helpers (times are stored UTC-naive, shown in the enrolment's zone)
# --------------------------------------------------------------------------- #
_IST = timezone(timedelta(hours=5, minutes=30))


def _zone(name):
    try:
        from zoneinfo import ZoneInfo
        return ZoneInfo(name or 'Asia/Kolkata')
    except Exception:           # tz database unavailable (e.g. Windows without tzdata)
        return _IST


def utcnow():
    return datetime.now(timezone.utc).replace(tzinfo=None)


def today():
    return utcnow().date()


def to_local(dt, tzname):
    if not dt:
        return None
    return dt.replace(tzinfo=timezone.utc).astimezone(_zone(tzname))


def fmt_dt(dt, tzname='Asia/Kolkata'):
    loc = to_local(dt, tzname)
    return loc.strftime('%a %d %b %Y, %I:%M %p ') + (loc.tzname() or '') if loc else '—'


def from_local(text, tzname):
    """'2026-11-03T17:30' (local to the enrolment) → UTC-naive datetime, or None."""
    if not text:
        return None
    try:
        dt = datetime.fromisoformat(text)
    except ValueError:
        return None
    return dt.replace(tzinfo=_zone(tzname)).astimezone(timezone.utc).replace(tzinfo=None)


def to_input(dt, tzname):
    loc = to_local(dt, tzname)
    return loc.strftime('%Y-%m-%dT%H:%M') if loc else ''


def parse_date(text):
    try:
        return date.fromisoformat(text) if text else None
    except ValueError:
        return None


def week_start(d=None):
    d = d or today()
    return d - timedelta(days=d.weekday())


# --------------------------------------------------------------------------- #
# Access control — every route calls this; the server decides, not the template
# --------------------------------------------------------------------------- #
def role_for(e, user):
    """'admin' | 'mentor' | 'student' | 'parent' | None for this user on this enrolment."""
    if not user or not user.is_authenticated:
        return None
    if user.is_admin:
        return 'admin'
    if e.mentor_id == user.id and user.is_ea_mentor:
        return 'mentor'
    if e.student_id == user.id:
        return 'student'
    if MsParentLink.query.filter_by(enrolment_id=e.id, parent_id=user.id).first():
        return 'parent'
    return None


def is_staff_role(role):
    return role in ('admin', 'mentor')


TABS = [  # key, label, icon, roles allowed
    ('home', 'Home', '🏠', ('student', 'parent', 'mentor', 'admin')),
    ('sessions', 'Sessions', '🗓️', ('student', 'parent', 'mentor', 'admin')),
    ('weekly', 'Weekly Plan', '✅', ('student', 'mentor', 'admin')),
    ('kpis', 'KPIs & Progress', '📈', ('student', 'parent', 'mentor', 'admin')),
    ('reviews', 'Quarterly Reviews', '🧾', ('student', 'parent', 'mentor', 'admin')),
    ('branch', 'Branch Fit', '🧭', ('student', 'parent', 'mentor', 'admin')),
    ('prefs', 'College Preferences', '🎓', ('student', 'parent', 'mentor', 'admin')),
    ('calendar', 'Exam Calendar', '📅', ('student', 'parent', 'mentor', 'admin')),
    ('messages', 'Messages', '💬', ('student', 'parent', 'mentor', 'admin')),
    ('reports', 'Reports', '📄', ('student', 'parent', 'mentor', 'admin')),
    ('history', 'Activity History', '🕘', ('mentor', 'admin')),
]


def tabs_for(role):
    return [t for t in TABS if role in t[3]]


def audit(e, action, detail='', role=None):
    try:                                    # also callable from scripts / shells with no request
        uid = current_user.id if current_user.is_authenticated else None
    except AttributeError:
        uid = None
    db.session.add(MsAudit(enrolment_id=e.id if e else None, user_id=uid,
                           role=role, action=action, detail=(detail or '')[:500]))


# --------------------------------------------------------------------------- #
# Programme defaults (admin can edit everything afterwards)
# --------------------------------------------------------------------------- #
DEFAULT_SESSIONS = [
    ('Onboarding and Baseline Assessment',
     'Student goals and expectations\nCurrent preparation status\nAcademic strengths and challenges\nParent and student concerns\nInitial KPI baseline\nPersonal mentorship goals',
     'Baseline profile and initial action plan'),
    ('Personal Study Strategy',
     'Review current timetable\nAssess available study time\nIdentify ineffective routines\nPrioritise study and revision',
     'Personalised weekly study plan'),
    ('Syllabus and Revision Planning',
     'Review subject and chapter status\nIdentify weak areas\nBuild a realistic revision schedule',
     'Syllabus and revision tracker'),
    ('Mock-Test and Performance Review',
     'Record or review available mock-test results\nCategorise mistakes\nReview time allocation and accuracy\nIdentify the highest-priority improvement',
     'Mock-test action plan'),
    ('Board and Entrance Exam Balance',
     'Review Board deadlines and entrance preparation\nCoordinate revision priorities\nIdentify workload conflicts',
     'Integrated examination preparation calendar'),
    ('Mid-Journey Review',
     'Review goals and KPIs\nCompare current performance with baseline\nDiscuss obstacles and confidence\nUpdate action priorities',
     'Midpoint review report'),
    ('Exam Readiness and Execution',
     'Practice exam routines\nReview question-selection and time-management approaches\nDiscuss preparation for setbacks',
     'Personal exam execution plan'),
    ('Career and Engineering Branch Fit',
     'Review student interests\nComplete relevant aptitude or interest assessments if included\nExplore engineering disciplines\nDiscuss skills, curriculum and career possibilities',
     'Preliminary branch-fit report'),
    ('College Options and Admission Strategy',
     "Review the student's available academic and examination information\nIdentify suitable admission pathways\nBuild aspirational, target and backup options where evidence permits\nConsider branch, location, fees and family preferences",
     'Preliminary college preference matrix'),
    ('Final Journey Review and Next Steps',
     'Review progress against baseline\nEvaluate completion of action plans\nSummarise student strengths and development areas\nReview examination and admission readiness\nIdentify remaining actions',
     'Consolidated mentorship progress report and next-stage plan'),
]

DEFAULT_BRANCHES = [
    ('Computer Science and Engineering', 'Programming, algorithms, systems, software engineering.', 'Data structures, operating systems, databases, networks.',
     'Logical reasoning, problem solving, persistence in debugging.', 'Build a web app; solve algorithmic problems; contribute to open source.', 'Software, data, product, cybersecurity roles.',
     'Do I enjoy long stretches of coding and debugging?'),
    ('Artificial Intelligence and Data Science', 'Machine learning, statistics and data engineering on top of programming.', 'Probability & statistics, linear algebra, ML, data systems.',
     'Maths comfort, curiosity about data, programming.', 'Predict outcomes from a public dataset; build a simple classifier.', 'Data science, ML engineering, analytics.',
     'Am I comfortable with maths-heavy coursework?'),
    ('Information Technology', 'Applied computing, information systems and web/cloud technologies.', 'Programming, databases, networking, web and cloud.',
     'Practical programming, systems thinking.', 'Build a database-backed website; set up a small network lab.', 'IT services, development, cloud, support engineering.',
     'How does this differ from CSE in the colleges I am considering?'),
    ('Electronics and Communication Engineering', 'Circuits, signals, communication systems and embedded devices.', 'Analog & digital electronics, signals, communication, VLSI.',
     'Physics & maths aptitude, hands-on tinkering.', 'Build an Arduino/embedded project; simulate a simple circuit.', 'Electronics, telecom, embedded, VLSI and semiconductor roles.',
     'Am I interested in hardware as well as software?'),
    ('Electrical and Electronics Engineering', 'Power systems, machines, control and electronics.', 'Circuits, machines, power systems, control systems.',
     'Physics & maths aptitude, systems thinking.', 'Study a home energy audit; model a small control loop.', 'Power, energy, automation and EV-related roles.',
     'How interested am I in power and energy systems?'),
    ('Mechanical Engineering', 'Design, thermal and manufacturing systems.', 'Mechanics, thermodynamics, materials, manufacturing, CAD.',
     'Spatial visualisation, physics, hands-on building.', 'Design a part in CAD; build a simple mechanism.', 'Design, manufacturing, automotive, energy and robotics roles.',
     'Do I enjoy physical systems and workshop-style learning?'),
    ('Civil Engineering', 'Structures, infrastructure, geotechnics and construction.', 'Structural analysis, fluid mechanics, surveying, construction management.',
     'Physics, practical planning, outdoor/site comfort.', 'Study a local infrastructure project; model a small structure.', 'Construction, infrastructure, urban planning, consulting.',
     'Am I comfortable with site-based work?'),
    ('Chemical Engineering', 'Process design, reaction engineering and materials at industrial scale.', 'Chemistry, thermodynamics, transport phenomena, process control.',
     'Chemistry & maths aptitude, process thinking.', 'Map the process of a familiar product; study a basic mass balance.', 'Process industries, energy, materials and sustainability roles.',
     'Which parts of chemistry do I enjoy most?'),
]

PRESET_KPIS = [
    ('Preparation', 'Planned study sessions completed', '%', 'higher', 100),
    ('Preparation', 'Weekly revision target completion', '%', 'higher', 90),
    ('Preparation', 'Syllabus milestones completed', 'count', 'higher', None),
    ('Preparation', 'Practice targets completed', '%', 'higher', 90),
    ('Preparation', 'Mock tests completed', 'count', 'higher', None),
    ('Preparation', 'Mock-test analyses completed', '%', 'higher', 100),
    ('Performance', 'Mock-test percentage (outcome)', '%', 'higher', None),
    ('Performance', 'Accuracy in mock tests (outcome)', '%', 'higher', None),
    ('Performance', 'Silly-mistake rate (outcome)', '%', 'lower', None),
    ('Mentorship', 'Weekly check-ins submitted', '%', 'higher', 90),
    ('Mentorship', 'Action items completed on time', '%', 'higher', 85),
    ('Readiness', 'Branch-fit assessment completed', 'milestone', 'milestone', 1),
    ('Readiness', 'Eligibility checks completed', '%', 'higher', 100),
    ('Readiness', 'Required documents tracked', '%', 'higher', 100),
    ('Readiness', 'Choice-filling preparation completed', 'milestone', 'milestone', 1),
]
OUTCOME_HINT = '(outcome)'


def ensure_default_programme():
    """Create the standard 10-session programme if none exists. Returns the first programme."""
    prog = MsProgramme.query.filter(db.or_(MsProgramme.tier == None, MsProgramme.tier != 'Add-on')).first()  # noqa: E711
    if prog:
        return prog
    prog = MsProgramme(name='Grade 12 Engineering Mentorship',
                       description='Board + JEE preparation, weekly accountability, branch fit, college strategy and choice-filling readiness.',
                       tier='Elite Mentorship')
    db.session.add(prog)
    db.session.flush()
    for i, (title, topics, deliverable) in enumerate(DEFAULT_SESSIONS, 1):
        db.session.add(MsSessionTemplate(programme_id=prog.id, position=i, title=title, topics=topics,
                                         deliverable=deliverable, duration_min=60))
    db.session.commit()
    return prog


def ensure_addon_programmes():
    """Create the ready-made add-on programmes (UCEED, NID, NIFT, IIT Delhi–Abu Dhabi, TNEA, state-specific, SRM, Amrita, VIT)
    that do not exist yet. Idempotent: existing programmes (and any admin edits to them) are left alone. Returns how many were created."""
    from app.data.mentorship_addons import ADDONS, TIER
    made = 0
    for a in ADDONS:
        if MsProgramme.query.filter_by(name=a['title']).first():
            continue
        prog = MsProgramme(name=a['title'], tier=TIER, active=True,
                           description=f"{a['blurb']} For: {a['audience']} About {a['weeks']} weeks. Verify: {a['verify']}")
        db.session.add(prog)
        db.session.flush()
        for i, (title, topics, deliverable) in enumerate(a['sessions'], 1):
            db.session.add(MsSessionTemplate(programme_id=prog.id, position=i, title=title, topics=topics,
                                             deliverable=deliverable, duration_min=60))
        made += 1
    db.session.commit()
    return made


# Architecture, NID and NIFT programmes (name, studies, subjects, skills, projects, careers, reflection question).
# Programme and discipline lists differ by campus and year — students must confirm them in the current NID / NIFT / university notice.
DESIGN_BRANCHES = [
    ('Architecture (B.Arch)', 'Five-year professional degree in designing buildings and spaces: design studio, structures, materials, history and sustainability.',
     'Architectural design studio, building construction, structures, building services, history of architecture, environment and sustainability.',
     'Freehand drawing, spatial visualisation, maths and physics basics, patience for long design projects, presentation skills.',
     'Measure and sketch a room or street corner; build a scale model; keep a sketchbook of buildings you observe.',
     'Architect (registration with the Council of Architecture), urban designer, conservation, interior and landscape design, research. Entrance route (for example NATA / JEE Main Paper 2) is stated in the current notice.',
     'Do I enjoy drawing and model-making for hours, and presenting my ideas to critics?'),
    ('Urban and Regional Planning (B.Plan)', 'Planning cities, transport, housing and land use with a mix of design, policy and data.',
     'Planning studio, urban design, transport, housing, GIS, environment, planning law and economics.',
     'Spatial thinking, data comfort, communication, interest in how cities work.',
     'Map a neighbourhood\'s amenities; study one local planning problem such as traffic or waste.',
     'Urban planner, transport and housing consultant, GIS analyst, government and development agencies.',
     'Am I interested in cities and policy as much as in drawing?'),
    ('Interior Architecture and Interior Design', 'Designing interior spaces: layout, materials, lighting, furniture and how people use rooms.',
     'Design studio, materials and construction, lighting, furniture design, colour, drawing and visualisation software.',
     'Drawing and colour sense, spatial planning, client communication, detail orientation.',
     'Redesign one room on paper with a plan, mood board and materials list.',
     'Interior designer, space planner, furniture and exhibition design, design-build firms.',
     'Do I notice how spaces feel and function, and can I turn that into drawings?'),
    ('NID B.Des: Industrial, Product and Transportation Design', 'Designing products and systems — usability, form, materials and manufacturing.',
     'Design fundamentals, ergonomics, materials and processes, model-making, sketching and CAD, design research.',
     'Sketching, observation, problem finding, hands-on prototyping.',
     'Redesign an everyday object; document the problems users face and build a cardboard prototype.',
     'Product, industrial and automotive designer, design researcher, design consultancies and in-house design teams.',
     'Do I like making things and improving how people use them?'),
    ('NID B.Des: Communication Design (Graphic, Film, Animation, Photography, Exhibition)', 'Visual communication across print, screen, motion and exhibition.',
     'Typography and layout, visual storytelling, photography, film and video, animation, exhibition design.',
     'Drawing, storytelling, visual taste, software comfort.',
     'Make a short visual story, poster series or 30-second animation; keep a visual journal.',
     'Graphic and brand designer, filmmaker, animator, motion and exhibition designer, art director.',
     'Do I express ideas best through images, motion or stories?'),
    ('NID B.Des: Textile, Apparel and Lifestyle Accessory Design', 'Designing fabrics, garments and accessories, from material to finished product.',
     'Textile fundamentals, weaving/printing/dyeing, pattern and construction, accessory design, craft traditions.',
     'Colour and pattern sense, hand skills, material curiosity.',
     'Create a small print or weave sample; sketch a garment or accessory series.',
     'Textile, apparel and accessory designer, craft and sustainability work, design studios and brands.',
     'Do I enjoy working with materials, colour and craft?'),
    ('NID B.Des: Ceramic and Glass, Furniture and Interior, Toy and Game Design', 'Material-led and experience-led design disciplines (availability varies by campus and year).',
     'Material studies (clay, glass, wood, metal), making and prototyping, play and interaction design, spatial design.',
     'Hands-on making, playfulness, spatial and material sense.',
     'Make one object in clay or wood; prototype a simple board game and test it with friends.',
     'Studio craftsperson, furniture and lifestyle designer, toy and game designer, design researcher.',
     'Do I learn best by making and testing physical things?'),
    ('NID B.Des: Interaction, New Media and Universal Design', 'Designing digital experiences and inclusive products and services.',
     'Interaction design, UX research, new-media tools, accessibility and inclusive design.',
     'Empathy, logical thinking, sketching, comfort with digital tools.',
     'Redesign one app screen flow; test it with two people and note what confused them.',
     'UX/UI designer, interaction designer, accessibility specialist, service designer.',
     'Am I curious about how people use technology and what makes it easy or hard?'),
    ('NIFT B.Des: Fashion Design', 'Designing garments and collections — trends, fabrics, pattern-making and styling.',
     'Fashion illustration, textile knowledge, pattern-making, garment construction, trend and colour forecasting.',
     'Sketching, colour and style sense, creativity, perseverance with construction detail.',
     'Sketch a mini collection from a theme; sew or drape one simple garment.',
     'Fashion designer, stylist, costume designer, buying and merchandising, fashion brands and export houses.',
     'Do I enjoy sketching clothes and following trends, and finishing detailed work?'),
    ('NIFT B.Des: Accessory, Leather and Knitwear Design', 'Designing bags, footwear, jewellery, leather goods and knitted products.',
     'Material study (leather, metal, yarns), product drawing, construction and finishing, knit technology, accessory trends.',
     'Product sketching, hands-on craftsmanship, material curiosity.',
     'Design and prototype a bag or small accessory; try basic knitting or leather work.',
     'Accessory, footwear and leather designer, knitwear designer, brand design teams, export houses.',
     'Do I prefer designing objects and materials to designing full garments?'),
    ('NIFT B.Des: Textile Design and Fashion Communication', 'Fabric surface design on one side, fashion media, styling and visual communication on the other.',
     'Textile design (weaving, printing), fashion illustration, photography, styling, visual merchandising, communication design.',
     'Visual taste, storytelling, drawing, software and camera comfort.',
     'Make a print repeat or a small styled photo story; build a fashion mood board.',
     'Textile designer, fashion stylist, visual merchandiser, fashion journalist or communicator, brand creative teams.',
     'Am I drawn more to fabric design or to telling fashion stories visually?'),
    ('NIFT B.FTech: Apparel Production', 'Technology side of fashion: garment manufacturing, quality, production planning and industry engineering.',
     'Garment construction technology, fabric science, production planning, quality, industrial engineering, apparel CAD.',
     'Maths and logic, process thinking, interest in manufacturing, teamwork.',
     'Study how one garment is made step by step; time a simple sewing operation and list improvements.',
     'Production manager, quality and merchandising roles, apparel technologists, export and manufacturing companies.',
     'Do I enjoy how things are made and improved in factories more than designing them?'),
]


def ensure_branches():
    """Load the branch catalogue; adds any default branch that is missing by name (so new defaults reach existing sites).
    Existing rows, including admin edits and deactivations, are never changed."""
    have = {b.name for b in MsBranch.query.all()}
    pos = MsBranch.query.count()
    for name, studies, subjects, skills, projects, careers, q in DEFAULT_BRANCHES + DESIGN_BRANCHES:
        if name in have:
            continue
        pos += 1
        db.session.add(MsBranch(name=name, studies=studies, subjects=subjects, skills=skills, projects=projects,
                                careers=careers, questions=q, position=pos))
    db.session.commit()


def enrol(student, mentor, programme, start=None, end=None, extra_quota=0, preferred_name=None):
    e = MsEnrolment(student_id=student.id, mentor_id=mentor.id if mentor else None, programme_id=programme.id,
                    start_date=start or today(), end_date=end, extra_quota=extra_quota or 0,
                    preferred_name=preferred_name or (student.name or '').split(' ')[0])
    db.session.add(e)
    db.session.flush()
    for t in programme.templates.filter_by(active=True).order_by(MsSessionTemplate.position):
        db.session.add(MsSession(enrolment_id=e.id, template_id=t.id, kind='core', position=t.position, title=t.title,
                                 agenda=t.topics, deliverable=t.deliverable, duration_min=t.duration_min))
    db.session.flush()
    audit(e, 'enrolment.created', f'student={student.id} mentor={mentor.id if mentor else None}', role='admin')
    return e


def next_position(e):
    last = e.sessions.order_by(MsSession.position.desc()).first()
    return (last.position if last else 0) + 1


def extras_used(e):
    return e.sessions.filter(MsSession.kind != 'core', MsSession.status != 'Cancelled').count()


def can_add_extra(e, role):
    """Extra sessions are package-controlled: admins always, mentors only within the paid/approved quota."""
    if role == 'admin':
        return True
    return role == 'mentor' and extras_used(e) < (e.extra_quota or 0)


# --------------------------------------------------------------------------- #
# Sessions, actions, KPIs — derived status
# --------------------------------------------------------------------------- #
def session_stats(e):
    rows = e.sessions.all()
    core = [s for s in rows if s.kind == 'core' and s.status != 'Cancelled']
    done_core = [s for s in core if s.status == 'Completed']
    return {
        'core_total': len(core),
        'core_done': len(done_core),
        'partial': sum(1 for s in rows if s.status == 'Partially completed'),
        'extra_total': sum(1 for s in rows if s.kind != 'core' and s.status != 'Cancelled'),
        'extra_done': sum(1 for s in rows if s.kind != 'core' and s.status == 'Completed'),
        'cancelled': sum(1 for s in rows if s.status == 'Cancelled'),        # never counted as completed
        'missed': sum(1 for s in rows if s.status == 'Missed'),
        'pct': round(100 * len(done_core) / len(core)) if core else 0,
    }


def next_session(e):
    now = utcnow()
    upcoming = (e.sessions.filter(MsSession.status.in_(['Planned', 'Rescheduled']), MsSession.planned_at != None)  # noqa: E711
                .order_by(MsSession.planned_at).all())
    for s in upcoming:
        if s.planned_at >= now - timedelta(hours=1):
            return s
    return None


def action_state(a, ref=None):
    """Workflow label for an action (an indicator, not a judgement about the student)."""
    ref = ref or today()
    if a.status == 'Cancelled':
        return 'Cancelled'
    if a.status == 'Completed':
        if a.due_date and a.completed_at and a.completed_at.date() > a.due_date:
            return 'Completed late'
        return 'Completed on time'
    if a.status == 'Blocked':
        return 'Blocked'
    if a.status == 'Needs Help':
        return 'Requires mentor attention'
    if a.due_date:
        if a.due_date < ref:
            return 'Overdue'
        if a.due_date == ref:
            return 'Due today'
        if (a.due_date - ref).days <= rule('due_soon_days'):
            return 'Due soon'
    return 'Open'


def action_stats(e, only_visible_to_parent=False):
    q = e.actions.filter(MsAction.status != 'Cancelled')            # cancelled leave the denominator
    if only_visible_to_parent:
        q = q.filter(MsAction.parent_visible == True)  # noqa: E712
    rows = q.all()
    done = [a for a in rows if a.status == 'Completed']
    overdue = [a for a in rows if action_state(a) == 'Overdue']
    return {'total': len(rows), 'done': len(done), 'overdue': len(overdue),
            'needs_help': sum(1 for a in rows if a.status in ('Needs Help', 'Blocked')),
            'pct': round(100 * len(done) / len(rows)) if rows else 0}


def kpi_view(k):
    """Progress/trend/status for a KPI according to its target type."""
    obs = [o for o in k.observations.all() if o.value is not None]
    cur = k.current if k.current is not None else (obs[-1].value if obs else None)
    trend = None
    if len(obs) >= 2:
        diff = obs[-1].value - obs[-2].value
        trend = 'flat' if diff == 0 else ('up' if diff > 0 else 'down')
    pct, status = None, 'No data'
    d = k.direction
    if d == 'qualitative':
        status = 'Reviewed' if (k.qualitative or cur is not None) else 'No data'
    elif cur is not None:
        if d == 'higher' and k.target is not None:
            base = k.baseline if k.baseline is not None else 0
            pct = 100 if cur >= k.target else (0 if k.target == base else max(0, min(100, 100 * (cur - base) / (k.target - base))))
            status = 'Achieved' if cur >= k.target else ('On track' if pct >= 50 else 'Needs attention')
        elif d == 'lower' and k.target is not None:
            base = k.baseline if k.baseline is not None else cur
            pct = 100 if cur <= k.target else (0 if base == k.target else max(0, min(100, 100 * (base - cur) / (base - k.target))))
            status = 'Achieved' if cur <= k.target else ('On track' if pct >= 50 else 'Needs attention')
        elif d == 'range' and k.target is not None and k.target_high is not None:
            ok = k.target <= cur <= k.target_high
            pct, status = (100 if ok else 0), ('In range' if ok else 'Out of range')
        elif d == 'milestone' and k.target is not None:
            pct = 100 if cur >= k.target else max(0, min(100, 100 * cur / k.target))
            status = 'Achieved' if cur >= k.target else 'In progress'
    # for 'lower' KPIs a fall is an improvement; expose that to the template
    improving = None if trend in (None, 'flat') else ((trend == 'up') != (d == 'lower'))
    return {'current': cur, 'pct': None if pct is None else round(pct), 'status': status, 'trend': trend, 'improving': improving,
            'obs': obs}


# --------------------------------------------------------------------------- #
# Calendar, attention, journey
# --------------------------------------------------------------------------- #
def events_for(e, include_all=True):
    """Programme template events + this student's events (+ sessions, action due dates, review dates)."""
    items = []
    ev = MsEvent.query.filter(db.or_(MsEvent.enrolment_id == e.id, MsEvent.programme_id == e.programme_id)).all()
    for x in ev:
        items.append({'date': x.starts_on, 'end': x.ends_on, 'title': x.title, 'category': x.category, 'source': x.source,
                      'verified': x.verified_on, 'notes': x.notes, 'done': x.done, 'kind': 'event', 'id': x.id,
                      'scope': 'Programme' if x.programme_id else 'Student'})
    from app.models_mentorship import MsExam, MsExamFocus
    for f in MsExamFocus.query.filter_by(enrolment_id=e.id).all():
        x = db.session.get(MsExam, f.exam_id)
        if x and x.active:
            items.append({'date': x.starts_on, 'end': x.ends_on, 'title': x.name, 'category': x.category, 'source': x.source,
                          'verified': x.verified_on, 'notes': ((x.window_note + ' · ') if x.window_note else '') + x.status,
                          'done': False, 'kind': 'event', 'id': None, 'scope': 'Following', 'status': x.status})
    for s in e.sessions.filter(MsSession.planned_at != None, MsSession.status.in_(['Planned', 'Rescheduled', 'Completed'])).all():  # noqa: E711
        items.append({'date': to_local(s.planned_at, e.timezone).date(), 'title': s.title, 'category': 'Mentorship session',
                      'notes': fmt_dt(s.planned_at, e.timezone), 'done': s.status == 'Completed', 'kind': 'session', 'id': s.id})
    for a in e.actions.filter(MsAction.due_date != None, MsAction.status != 'Cancelled').all():  # noqa: E711
        items.append({'date': a.due_date, 'title': 'Due: ' + a.title, 'category': 'Action due', 'done': a.status == 'Completed',
                      'notes': action_state(a), 'kind': 'action', 'id': a.id})
    for r in e.reviews.filter(MsReview.next_review_date != None).all() if hasattr(e, 'reviews') else []:  # noqa: E711
        items.append({'date': r.next_review_date, 'title': 'Next review after ' + r.label, 'category': 'Quarterly review',
                      'kind': 'review', 'id': r.id})
    items.sort(key=lambda i: (i['date'], i['title']))
    return items


def attention(e):
    """-> (level, [reasons]).  level: ok | watch | attention.  Workflow indicators only."""
    reasons = []
    ast = action_stats(e)
    if ast['overdue'] >= rule('overdue_attention'):
        reasons.append(f"{ast['overdue']} overdue actions")
    elif ast['overdue']:
        reasons.append(f"{ast['overdue']} overdue action" + ('s' if ast['overdue'] > 1 else ''))
    if ast['needs_help']:
        reasons.append(f"{ast['needs_help']} action(s) marked Needs Help / Blocked")
    started = e.start_date or today()
    last = (MsCheckin.query.filter(MsCheckin.enrolment_id == e.id, MsCheckin.status.in_(['Submitted', 'Reviewed']))
            .order_by(MsCheckin.week_start.desc()).first())
    if e.status == 'Active':
        ref = last.week_start if last else started
        if (today() - ref).days > rule('checkin_gap_days') + (0 if last else 7):
            reasons.append('No weekly check-in submitted recently')
    if last and last.urgent_help:
        reasons.append('Student asked for urgent help')
    if last and last.confidence is not None and last.confidence <= rule('low_confidence'):
        reasons.append('Low confidence reported — worth a conversation')
    if e.sessions.filter(MsSession.status == 'Missed').count():
        reasons.append('A session was missed')
    window = today() + timedelta(days=rule('exam_window_days'))
    exam_cats = ('Board exam', 'JEE Main', 'JEE Advanced', 'School exam')
    soon = MsEvent.query.filter(db.or_(MsEvent.enrolment_id == e.id, MsEvent.programme_id == e.programme_id),
                                MsEvent.category.in_(exam_cats), MsEvent.starts_on >= today(), MsEvent.starts_on <= window).first()
    if soon and ast['total'] - ast['done'] > 0:
        reasons.append(f'Exam within {rule("exam_window_days")} days with open actions')
    level = 'ok'
    if reasons:
        level = 'attention' if (ast['overdue'] >= rule('overdue_attention') or (last and last.urgent_help)
                                or ast['needs_help'] or len(reasons) >= 3) else 'watch'
    return level, reasons


def journey(e):
    """Timeline of every session (core + extra) with a derived current stage."""
    rows = e.sessions.order_by(MsSession.position).all()
    current = None
    for s in rows:
        if s.kind == 'core' and s.status not in ('Completed', 'Cancelled'):
            current = s
            break
    return rows, current


def unread_count(e, user, role):
    q = MsMessage.query.filter(MsMessage.enrolment_id == e.id, MsMessage.sender_id != user.id)
    q = q.filter(MsMessage.audience.in_(visible_audiences(role)))
    ids = [m.id for m in q.all()]
    if not ids:
        return 0
    read = {r.message_id for r in MsMessageRead.query.filter(MsMessageRead.user_id == user.id, MsMessageRead.message_id.in_(ids))}
    return len(ids) - len(read)


def visible_audiences(role):
    """Message audiences each role may read. Internal mentor notes never leave staff."""
    return {'student': ('student', 'all'), 'parent': ('parent', 'all'),
            'mentor': ('student', 'parent', 'all', 'internal'), 'admin': ('student', 'parent', 'all', 'internal')}.get(role, ())


# --------------------------------------------------------------------------- #
# Snapshots — quarterly review & final report
# --------------------------------------------------------------------------- #
def _kpi_rows(e):
    out = []
    for k in e.kpis_q().filter(MsKpi.status != 'Archived').all():
        v = kpi_view(k)
        out.append({'name': k.name, 'category': k.category, 'unit': k.unit or '', 'direction': k.direction,
                    'baseline': k.baseline, 'target': k.target, 'current': v['current'], 'status': v['status'],
                    'trend': v['trend'], 'outcome': bool(k.outcome_metric), 'qualitative': k.qualitative})
    return out


def build_snapshot(e):
    ss, ast = session_stats(e), action_stats(e)
    checkins = MsCheckin.query.filter(MsCheckin.enrolment_id == e.id, MsCheckin.status.in_(['Submitted', 'Reviewed'])).all()
    return {
        'taken_on': today().isoformat(),
        'sessions': ss, 'actions': ast,
        'checkins_submitted': len(checkins),
        'confidence': [c.confidence for c in sorted(checkins, key=lambda c: c.week_start) if c.confidence is not None][-8:],
        'kpis': _kpi_rows(e),
        'open_actions': [a.title for a in e.actions.filter(MsAction.status.notin_(['Completed', 'Cancelled'])).limit(15).all()],
    }


def report_data(e):
    """Frozen, verified-records-only data for the final report. Missing data is labelled, never zero-filled."""
    snap = build_snapshot(e)
    fit = e.branchfit() if hasattr(e, 'branchfit') else None
    ratings = MsBranchRating.query.filter_by(enrolment_id=e.id).all()
    lists = MsPrefList.query.filter_by(enrolment_id=e.id).all()
    final = next((l for l in lists if l.is_final), None) or (lists[0] if lists else None)
    reviews = MsReview.query.filter(MsReview.enrolment_id == e.id, MsReview.status.in_(['Finalised', 'Shared'])).all()
    sess = [{'n': s.position, 'title': s.title, 'kind': s.kind, 'status': s.status,
             'planned': fmt_dt(s.planned_at, e.timezone) if s.planned_at else None,
             'actual': fmt_dt(s.actual_at, e.timezone) if s.actual_at else None,
             'deliverable': s.deliverable, 'summary': s.shared_summary} for s in e.sessions.order_by(MsSession.position)]
    return {
        'student': e.preferred_name or e.student.name, 'full_name': e.student.name, 'grade': e.grade,
        'programme': e.programme.name, 'mentor': e.mentor.name if e.mentor else 'Not assigned',
        'start': e.start_date.isoformat() if e.start_date else None, 'end': e.end_date.isoformat() if e.end_date else None,
        'data_through': today().isoformat(), 'goals': e.goals,
        'snapshot': snap, 'sessions': sess,
        'reviews': [{'label': r.label, 'strengths': r.strengths, 'challenges': r.challenges, 'next_targets': r.next_targets,
                     'observations': r.mentor_observations} for r in reviews],
        'branch': {'completed': bool(fit and fit.status in ('Submitted', 'Reviewed')),
                   'mentor_summary': fit.mentor_summary if fit else None,
                   'ratings': [{'branch': r.branch, 'interest': r.interest, 'readiness': r.readiness,
                                'feasibility': r.feasibility, 'family': r.family} for r in ratings]},
        'preferences': {'list': final.name if final else None, 'status': final.status if final else None,
                        'entries': [{'n': i + 1, 'college': x.college, 'branch': x.branch, 'route': x.route,
                                     'eligibility': x.eligibility} for i, x in enumerate(final.entries)] if final else []},
        'next_milestones': [{'date': i['date'].isoformat(), 'title': i['title'], 'category': i['category']}
                            for i in events_for(e) if i['date'] >= today() and i['kind'] == 'event'][:8],
    }


def na(v):
    return 'Not recorded' if v in (None, '', []) else v


def report_pdf(data, status='Draft'):
    """PDF bytes via ReportLab, or None when ReportLab is not installed (callers fall back to print-HTML)."""
    try:
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
        from reportlab.lib.units import mm
        from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
    except ImportError:
        return None
    navy, orange = colors.HexColor('#0E3A8A'), colors.HexColor('#FF6B0A')
    ss = getSampleStyleSheet()
    h1 = ParagraphStyle('h1', parent=ss['Title'], textColor=navy, fontSize=22, alignment=0)
    h2 = ParagraphStyle('h2', parent=ss['Heading2'], textColor=navy, fontSize=13, spaceBefore=12)
    body = ParagraphStyle('b', parent=ss['BodyText'], fontSize=9.5, leading=13)
    small = ParagraphStyle('s', parent=body, fontSize=8, textColor=colors.HexColor('#5A6278'))

    def P(t, st=body):
        from xml.sax.saxutils import escape
        return Paragraph(escape(str(t)).replace('\n', '<br/>'), st)

    def table(rows, widths=None, head=True):
        t = Table([[P(c) for c in r] for r in rows], colWidths=widths, repeatRows=1 if head else 0)
        st = [('GRID', (0, 0), (-1, -1), .4, colors.HexColor('#E8DFC8')), ('VALIGN', (0, 0), (-1, -1), 'TOP')]
        if head:
            st.append(('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E1E9F7')))
        t.setStyle(TableStyle(st))
        return t

    snap = data['snapshot']
    story = [P('EduAakashaA Mentorship Progress Report', h1),
             P(f"{data['full_name']} · {data['grade']} · {data['programme']}", body),
             P(f"Status: {status}. Data through {data['data_through']}. Mentor: {data['mentor']}.", small), Spacer(1, 6)]
    story += [P('1. Programme and mentorship period', h2),
              table([['Student', data['full_name']], ['Mentor', data['mentor']], ['Start', na(data['start'])],
                     ['End', na(data['end'])], ['Goals', na(data['goals'])]], [40 * mm, 130 * mm], head=False)]
    ss_, as_ = snap['sessions'], snap['actions']
    story += [P('2. Sessions and actions', h2),
              P(f"Core sessions completed: {ss_['core_done']} of {ss_['core_total']} ({ss_['pct']}%). Additional sessions held: "
                f"{ss_['extra_done']} of {ss_['extra_total']}. Cancelled sessions ({ss_['cancelled']}) are not counted as completed."),
              P(f"Actions completed: {as_['done']} of {as_['total']} ({as_['pct']}%) — cancelled actions are excluded from the total. "
                f"Open and overdue: {as_['overdue']}. Weekly check-ins submitted: {snap['checkins_submitted']}."),
              table([['#', 'Session', 'Type', 'Status', 'Held on']] +
                    [[s['n'], s['title'], s['kind'], s['status'], s['actual'] or 'Not recorded'] for s in data['sessions']],
                    [10 * mm, 80 * mm, 22 * mm, 30 * mm, 38 * mm])]
    story.append(P('3. KPIs (baseline → target → latest)', h2))
    if snap['kpis']:
        story.append(table([['KPI', 'Type', 'Baseline', 'Target', 'Latest', 'Status']] +
                           [[k['name'] + (' (exam outcome)' if k['outcome'] else ''), k['category'], na(k['baseline']), na(k['target']),
                             na(k['current'] if k['current'] is not None else k['qualitative']), k['status']] for k in snap['kpis']],
                           [62 * mm, 24 * mm, 20 * mm, 20 * mm, 22 * mm, 22 * mm]))
        story.append(P('Marks and ranks are shown as exam outcomes; they are not fully within a student\'s control.', small))
    else:
        story.append(P('No KPIs recorded.'))
    story.append(P('4. Quarterly reviews', h2))
    story += [P(f"{r['label']}: strengths — {na(r['strengths'])}; challenges — {na(r['challenges'])}; next targets — {na(r['next_targets'])}")
              for r in data['reviews']] or [P('No finalised quarterly review yet.')]
    br = data['branch']
    story.append(P('5. Branch fit', h2))
    story.append(P('Branch-fit assessment completed.' if br['completed'] else 'Branch-fit assessment not completed.'))
    if br['ratings']:
        story.append(table([['Branch', 'Interest', 'Readiness', 'Feasibility', 'Family fit']] +
                           [[r['branch'], na(r['interest']), na(r['readiness']), na(r['feasibility']), na(r['family'])] for r in br['ratings']],
                           [70 * mm, 24 * mm, 24 * mm, 26 * mm, 26 * mm]))
        story.append(P('Interest, readiness, feasibility and family fit are shown separately (1–5); they are discussion aids, not predictions.', small))
    if br['mentor_summary']:
        story.append(P('Mentor summary: ' + br['mentor_summary']))
    pf = data['preferences']
    story.append(P('6. College preference summary', h2))
    if pf['entries']:
        story.append(P(f"List: {pf['list']} — workflow status: {pf['status']}. A list prepared in EduAakashaA is not an official counselling submission."))
        story.append(table([['#', 'College', 'Branch', 'Route', 'Eligibility']] +
                           [[x['n'], x['college'], na(x['branch']), na(x['route']), x['eligibility']] for x in pf['entries']],
                           [10 * mm, 70 * mm, 45 * mm, 22 * mm, 28 * mm]))
    else:
        story.append(P('No preference list recorded.'))
    story.append(P('7. Outstanding tasks and next milestones', h2))
    story += [P('• ' + t) for t in snap['open_actions']] or [P('No open actions.')]
    story += [P(f"{m['date']} — {m['title']} ({m['category']})") for m in data['next_milestones']]
    story += [Spacer(1, 10), P('This report summarises recorded mentorship activity. It does not guarantee any examination rank, '
                               'seat, college or branch. Missing items are marked "Not recorded" and are not zero scores.', small)]

    buf = io.BytesIO()

    def footer(canv, doc):
        canv.saveState()
        canv.setFillColor(orange)
        canv.rect(0, 0, A4[0], 4, stroke=0, fill=1)
        canv.setFillColor(colors.HexColor('#5A6278'))
        canv.setFont('Helvetica', 7.5)
        canv.drawString(18 * mm, 8 * mm, 'EduAakashaA · www.eduaakashaa.com · info@eduaakashaa.com')
        canv.drawRightString(A4[0] - 18 * mm, 8 * mm, f'Page {doc.page}')
        canv.restoreState()

    SimpleDocTemplate(buf, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=16 * mm,
                      bottomMargin=16 * mm, title='EduAakashaA Mentorship Progress Report').build(story, onFirstPage=footer, onLaterPages=footer)
    return buf.getvalue()


def jdump(x):
    return json.dumps(x, default=str)


def jload(s, default=None):
    try:
        return json.loads(s) if s else (default if default is not None else {})
    except ValueError:
        return default if default is not None else {}
