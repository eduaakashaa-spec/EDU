"""
Mentorship Portal models (Grade 12 engineering mentorship).

One student record (`MsEnrolment`) is the single source of truth read by the
student, mentor and parent dashboards. Everything hangs off the enrolment, so
adding another grade / programme later is a new `MsProgramme` row — no code
change.  New tables only (db.create_all adds them; nothing existing is altered).
"""
from datetime import datetime, timezone

from app.extensions import db


def _utcnow():
    # naive UTC, consistent with models_membership
    return datetime.now(timezone.utc).replace(tzinfo=None)


# --------------------------------------------------------------------------- #
# Programme definition (admin-configurable, no code change)
# --------------------------------------------------------------------------- #
class MsProgramme(db.Model):
    __tablename__ = 'ms_programmes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(160), nullable=False)
    description = db.Column(db.Text)
    tier = db.Column(db.String(60))              # membership path this programme belongs to (informational entitlement label)
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=_utcnow)

    templates = db.relationship('MsSessionTemplate', backref='programme', lazy='dynamic',
                                order_by='MsSessionTemplate.position')


class MsSessionTemplate(db.Model):
    """One core session of a programme. The count of active rows IS the number of
    included core sessions — admins add/remove/reorder rows, nothing is hard-coded."""
    __tablename__ = 'ms_session_templates'
    id = db.Column(db.Integer, primary_key=True)
    programme_id = db.Column(db.Integer, db.ForeignKey('ms_programmes.id', ondelete='CASCADE'), index=True, nullable=False)
    position = db.Column(db.Integer, default=0)
    title = db.Column(db.String(200), nullable=False)
    topics = db.Column(db.Text)                  # one topic per line
    deliverable = db.Column(db.String(300))
    duration_min = db.Column(db.Integer, default=60)
    active = db.Column(db.Boolean, default=True)


class MsEnrolment(db.Model):
    __tablename__ = 'ms_enrolments'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), index=True, nullable=False)
    mentor_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), index=True)
    programme_id = db.Column(db.Integer, db.ForeignKey('ms_programmes.id'), nullable=False)
    preferred_name = db.Column(db.String(100))
    grade = db.Column(db.String(40), default='Grade 12')
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    status = db.Column(db.String(20), default='Active')       # Active | Paused | Completed
    timezone = db.Column(db.String(60), default='Asia/Kolkata')
    extra_quota = db.Column(db.Integer, default=0)            # paid/approved extra sessions the package allows
    goals = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=_utcnow)

    student = db.relationship('User', foreign_keys=[student_id],
                              backref=db.backref('ms_enrolments', lazy='dynamic'))
    mentor = db.relationship('User', foreign_keys=[mentor_id])
    programme = db.relationship('MsProgramme')

    # query helpers (tables defined further down this module)
    def kpis_q(self):
        return MsKpi.query.filter_by(enrolment_id=self.id)

    def branchfit(self):
        return MsBranchFit.query.filter_by(enrolment_id=self.id).first()

    @property
    def reviews(self):
        return MsReview.query.filter_by(enrolment_id=self.id)


class MsParentLink(db.Model):
    __tablename__ = 'ms_parent_links'
    id = db.Column(db.Integer, primary_key=True)
    enrolment_id = db.Column(db.Integer, db.ForeignKey('ms_enrolments.id', ondelete='CASCADE'), index=True, nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), index=True, nullable=False)
    relation = db.Column(db.String(40), default='Parent')
    __table_args__ = (db.UniqueConstraint('enrolment_id', 'parent_id'),)
    parent = db.relationship('User')


# --------------------------------------------------------------------------- #
# Execution
# --------------------------------------------------------------------------- #
SESSION_STATUSES = ('Planned', 'Completed', 'Partially completed', 'Rescheduled', 'Cancelled', 'Missed')
SESSION_KINDS = ('core', 'extra', 'intervention', 'follow-up')


class MsSession(db.Model):
    __tablename__ = 'ms_sessions'
    id = db.Column(db.Integer, primary_key=True)
    enrolment_id = db.Column(db.Integer, db.ForeignKey('ms_enrolments.id', ondelete='CASCADE'), index=True, nullable=False)
    template_id = db.Column(db.Integer, db.ForeignKey('ms_session_templates.id', ondelete='SET NULL'))
    kind = db.Column(db.String(20), default='core')
    position = db.Column(db.Integer, default=0)
    title = db.Column(db.String(200), nullable=False)
    agenda = db.Column(db.Text)
    deliverable = db.Column(db.String(300))
    status = db.Column(db.String(24), default='Planned')
    planned_at = db.Column(db.DateTime)            # UTC-naive; shown in the enrolment's time zone
    actual_at = db.Column(db.DateTime)             # set only when it really happened (separate from planned)
    duration_min = db.Column(db.Integer)
    participants = db.Column(db.String(300))
    shared_summary = db.Column(db.Text)            # student-visible recap
    mentor_notes = db.Column(db.Text)              # PRIVATE to mentor/admin
    next_review_date = db.Column(db.Date)
    deliverable_url = db.Column(db.String(500))
    parent_visible = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=_utcnow)
    updated_at = db.Column(db.DateTime, default=_utcnow, onupdate=_utcnow)

    enrolment = db.relationship('MsEnrolment', backref=db.backref('sessions', lazy='dynamic',
                                order_by='MsSession.position'))


# 'Completed' = the owner says it is done; 'Closed' = the mentor has reviewed and signed it off (counts as done, cannot be reopened by the owner)
ACTION_STATUSES = ('Not Started', 'In Progress', 'Completed', 'Closed', 'Needs Help', 'Blocked', 'Cancelled')
ACTION_FINISHED = ('Completed', 'Closed')


class MsAction(db.Model):
    __tablename__ = 'ms_actions'
    id = db.Column(db.Integer, primary_key=True)
    enrolment_id = db.Column(db.Integer, db.ForeignKey('ms_enrolments.id', ondelete='CASCADE'), index=True, nullable=False)
    session_id = db.Column(db.Integer, db.ForeignKey('ms_sessions.id', ondelete='SET NULL'))
    title = db.Column(db.String(240), nullable=False)
    instruction = db.Column(db.Text)
    purpose = db.Column(db.String(300))
    priority = db.Column(db.String(10), default='Medium')      # High | Medium | Low
    owner = db.Column(db.String(10), default='student')        # student | mentor | parent
    est_minutes = db.Column(db.Integer)
    start_date = db.Column(db.Date)
    due_date = db.Column(db.Date)
    completed_at = db.Column(db.DateTime)
    status = db.Column(db.String(16), default='Not Started')
    recurrence = db.Column(db.String(20))                      # '' | weekly
    student_comment = db.Column(db.Text)
    mentor_feedback = db.Column(db.Text)
    evidence_url = db.Column(db.String(500))
    parent_visible = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=_utcnow)
    updated_at = db.Column(db.DateTime, default=_utcnow, onupdate=_utcnow)

    enrolment = db.relationship('MsEnrolment', backref=db.backref('actions', lazy='dynamic'))


class MsCheckin(db.Model):
    __tablename__ = 'ms_checkins'
    id = db.Column(db.Integer, primary_key=True)
    enrolment_id = db.Column(db.Integer, db.ForeignKey('ms_enrolments.id', ondelete='CASCADE'), index=True, nullable=False)
    week_start = db.Column(db.Date, nullable=False)            # Monday of the week
    status = db.Column(db.String(12), default='Draft')         # Draft | Submitted | Reviewed
    confidence = db.Column(db.Integer)                         # 1-5
    went_well = db.Column(db.Text)
    difficult = db.Column(db.Text)
    barriers = db.Column(db.Text)
    help_needed = db.Column(db.Text)
    next_priority = db.Column(db.String(300))
    urgent_help = db.Column(db.Boolean, default=False)
    outcomes_json = db.Column(db.Text)                         # {action_id: completed|partial|not|blocked}
    outcome_notes_json = db.Column(db.Text)
    mentor_comment = db.Column(db.Text)
    share_parent = db.Column(db.Boolean, default=False)        # reflections stay private unless the mentor shares a summary
    parent_summary = db.Column(db.Text)
    submitted_at = db.Column(db.DateTime)
    reviewed_at = db.Column(db.DateTime)
    __table_args__ = (db.UniqueConstraint('enrolment_id', 'week_start'),)


# --------------------------------------------------------------------------- #
# KPIs
# --------------------------------------------------------------------------- #
KPI_DIRECTIONS = ('higher', 'lower', 'range', 'milestone', 'qualitative')


class MsKpi(db.Model):
    __tablename__ = 'ms_kpis'
    id = db.Column(db.Integer, primary_key=True)
    enrolment_id = db.Column(db.Integer, db.ForeignKey('ms_enrolments.id', ondelete='CASCADE'), index=True, nullable=False)
    category = db.Column(db.String(24), default='Preparation')   # Preparation | Performance | Mentorship | Readiness
    name = db.Column(db.String(200), nullable=False)
    definition = db.Column(db.Text)
    method = db.Column(db.String(300))
    unit = db.Column(db.String(30))
    direction = db.Column(db.String(12), default='higher')
    baseline = db.Column(db.Float)
    target = db.Column(db.Float)
    target_high = db.Column(db.Float)                            # upper bound for 'range'
    current = db.Column(db.Float)
    qualitative = db.Column(db.String(300))
    frequency = db.Column(db.String(30), default='Weekly')
    owner = db.Column(db.String(60))
    notes = db.Column(db.Text)
    status = db.Column(db.String(10), default='Active')          # Active | Paused | Archived
    outcome_metric = db.Column(db.Boolean, default=False)        # marks/rank style: shown as outcome, not controllable effort
    updated_at = db.Column(db.DateTime, default=_utcnow, onupdate=_utcnow)

    observations = db.relationship('MsKpiObs', backref='kpi', lazy='dynamic',
                                   order_by='MsKpiObs.observed_on', cascade='all, delete-orphan')


class MsKpiObs(db.Model):
    __tablename__ = 'ms_kpi_obs'
    id = db.Column(db.Integer, primary_key=True)
    kpi_id = db.Column(db.Integer, db.ForeignKey('ms_kpis.id', ondelete='CASCADE'), index=True, nullable=False)
    observed_on = db.Column(db.Date, default=lambda: _utcnow().date())
    value = db.Column(db.Float)
    text = db.Column(db.String(300))
    note = db.Column(db.String(300))
    by_user = db.Column(db.Integer, db.ForeignKey('users.id'))


# --------------------------------------------------------------------------- #
# Reviews, branch fit, preferences
# --------------------------------------------------------------------------- #
REVIEW_STATUSES = ('Draft', 'Awaiting input', 'Ready for review', 'Finalised', 'Shared')


class MsReview(db.Model):
    __tablename__ = 'ms_reviews'
    id = db.Column(db.Integer, primary_key=True)
    enrolment_id = db.Column(db.Integer, db.ForeignKey('ms_enrolments.id', ondelete='CASCADE'), index=True, nullable=False)
    label = db.Column(db.String(60), nullable=False)             # e.g. "Quarter 1"
    status = db.Column(db.String(20), default='Draft')
    snapshot_json = db.Column(db.Text)                           # pre-populated, mentor-verified data
    mentor_observations = db.Column(db.Text)
    strengths = db.Column(db.Text)
    challenges = db.Column(db.Text)
    goal_changes = db.Column(db.Text)
    interventions = db.Column(db.Text)
    next_targets = db.Column(db.Text)
    student_reflection = db.Column(db.Text)
    parent_feedback = db.Column(db.Text)
    parent_requested = db.Column(db.Boolean, default=False)
    next_review_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=_utcnow)
    finalised_at = db.Column(db.DateTime)
    shared_at = db.Column(db.DateTime)


class MsBranch(db.Model):
    """Administrator-maintained branch catalogue (defaults are loaded on first use)."""
    __tablename__ = 'ms_branches'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
    studies = db.Column(db.Text)
    subjects = db.Column(db.Text)
    skills = db.Column(db.Text)
    projects = db.Column(db.Text)
    careers = db.Column(db.Text)
    questions = db.Column(db.Text)
    active = db.Column(db.Boolean, default=True)
    position = db.Column(db.Integer, default=0)


class MsBranchFit(db.Model):
    __tablename__ = 'ms_branchfit'
    id = db.Column(db.Integer, primary_key=True)
    enrolment_id = db.Column(db.Integer, db.ForeignKey('ms_enrolments.id', ondelete='CASCADE'), unique=True, nullable=False)
    interests = db.Column(db.Text)
    activities = db.Column(db.Text)
    strengths = db.Column(db.Text)
    environments = db.Column(db.Text)
    career_areas = db.Column(db.Text)
    family_constraints = db.Column(db.Text)
    openness = db.Column(db.Integer)                             # 1-5 willingness to explore alternatives
    assessment_notes = db.Column(db.Text)                        # results of any aptitude/interest assessment, if used
    weights_json = db.Column(db.Text)                            # student-adjustable weights for the transparent matrix
    mentor_summary = db.Column(db.Text)
    status = db.Column(db.String(12), default='Draft')           # Draft | Submitted | Reviewed
    updated_at = db.Column(db.DateTime, default=_utcnow, onupdate=_utcnow)


class MsBranchRating(db.Model):
    __tablename__ = 'ms_branch_ratings'
    id = db.Column(db.Integer, primary_key=True)
    enrolment_id = db.Column(db.Integer, db.ForeignKey('ms_enrolments.id', ondelete='CASCADE'), index=True, nullable=False)
    branch = db.Column(db.String(120), nullable=False)
    interest = db.Column(db.Integer)          # student interest 1-5
    readiness = db.Column(db.Integer)         # academic readiness 1-5 (mentor-assessed)
    feasibility = db.Column(db.Integer)       # admission feasibility 1-5 (mentor-assessed, evidence based)
    family = db.Column(db.Integer)            # family / practical fit 1-5
    student_note = db.Column(db.Text)
    mentor_note = db.Column(db.Text)
    family_concern = db.Column(db.Text)
    __table_args__ = (db.UniqueConstraint('enrolment_id', 'branch'),)


PREF_LIST_STATUSES = ('Research pending', 'Draft created', 'Eligibility review pending', 'Mentor review pending',
                      'Parent discussion pending', 'Approved by family', 'Ready for official portal entry',
                      'Entered in official portal', 'Submitted and verified')
ADMISSION_ROUTES = ('JoSAA', 'CSAB', 'TNEA', 'DASA', 'CIWG', 'State counselling', 'Direct / management', 'Other')
ELIGIBILITY = ('Not checked', 'Eligible', 'Not eligible', 'Needs verification')


class MsPrefList(db.Model):
    __tablename__ = 'ms_pref_lists'
    id = db.Column(db.Integer, primary_key=True)
    enrolment_id = db.Column(db.Integer, db.ForeignKey('ms_enrolments.id', ondelete='CASCADE'), index=True, nullable=False)
    name = db.Column(db.String(160), nullable=False)
    status = db.Column(db.String(32), default='Research pending')
    is_final = db.Column(db.Boolean, default=False)
    notes = db.Column(db.Text)
    evidence = db.Column(db.String(300))        # e.g. confirmation reference once entered on the official portal
    created_at = db.Column(db.DateTime, default=_utcnow)
    updated_at = db.Column(db.DateTime, default=_utcnow, onupdate=_utcnow)
    entries = db.relationship('MsPrefEntry', backref='plist', lazy='dynamic',
                              order_by='MsPrefEntry.position', cascade='all, delete-orphan')


class MsPrefEntry(db.Model):
    __tablename__ = 'ms_pref_entries'
    id = db.Column(db.Integer, primary_key=True)
    list_id = db.Column(db.Integer, db.ForeignKey('ms_pref_lists.id', ondelete='CASCADE'), index=True, nullable=False)
    position = db.Column(db.Integer, default=0)
    college = db.Column(db.String(200), nullable=False)
    branch = db.Column(db.String(160))
    route = db.Column(db.String(30))
    tier = db.Column(db.String(12))              # Aspirational | Target | Backup
    interest = db.Column(db.Integer)
    eligibility = db.Column(db.String(20), default='Not checked')
    data_note = db.Column(db.Text)               # historical cutoff etc. — must carry year + source
    data_source = db.Column(db.String(200))
    data_year = db.Column(db.String(20))
    fee_note = db.Column(db.String(300))
    location = db.Column(db.String(160))
    reason = db.Column(db.Text)
    mentor_reco = db.Column(db.Text)
    parent_comment = db.Column(db.Text)
    review_status = db.Column(db.String(20), default='Not reviewed')


# --------------------------------------------------------------------------- #
# Calendar, messages, reports, audit
# --------------------------------------------------------------------------- #
EVENT_CATEGORIES = ('School exam', 'Board exam', 'JEE Main', 'JEE Advanced', 'Mock test', 'Revision',
                    'Admission deadline', 'Counselling', 'Choice filling', 'Documents', 'Other')


class MsEvent(db.Model):
    __tablename__ = 'ms_events'
    id = db.Column(db.Integer, primary_key=True)
    programme_id = db.Column(db.Integer, db.ForeignKey('ms_programmes.id', ondelete='CASCADE'), index=True)   # programme template
    enrolment_id = db.Column(db.Integer, db.ForeignKey('ms_enrolments.id', ondelete='CASCADE'), index=True)   # or one student
    title = db.Column(db.String(240), nullable=False)
    category = db.Column(db.String(24), default='Other')
    starts_on = db.Column(db.Date, nullable=False)
    ends_on = db.Column(db.Date)
    notes = db.Column(db.Text)
    source = db.Column(db.String(300))           # where the date comes from (official notice URL / body)
    verified_on = db.Column(db.Date)             # last verified date; empty = unverified
    done = db.Column(db.Boolean, default=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))


class MsMessage(db.Model):
    __tablename__ = 'ms_messages'
    id = db.Column(db.Integer, primary_key=True)
    enrolment_id = db.Column(db.Integer, db.ForeignKey('ms_enrolments.id', ondelete='CASCADE'), index=True, nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    audience = db.Column(db.String(10), default='student')       # student | parent | all | internal
    kind = db.Column(db.String(14), default='message')           # message | announcement | note
    body = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=_utcnow)
    sender = db.relationship('User')


class MsMessageRead(db.Model):
    __tablename__ = 'ms_message_reads'
    message_id = db.Column(db.Integer, db.ForeignKey('ms_messages.id', ondelete='CASCADE'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)


class MsReport(db.Model):
    __tablename__ = 'ms_reports'
    id = db.Column(db.Integer, primary_key=True)
    enrolment_id = db.Column(db.Integer, db.ForeignKey('ms_enrolments.id', ondelete='CASCADE'), index=True, nullable=False)
    status = db.Column(db.String(10), default='Draft')           # Draft | Approved | Shared
    data_json = db.Column(db.Text)                               # frozen snapshot — what was reviewed is what is shared
    data_through = db.Column(db.Date)
    generated_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    approved_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=_utcnow)
    approved_at = db.Column(db.DateTime)
    shared_at = db.Column(db.DateTime)


class MsAudit(db.Model):
    __tablename__ = 'ms_audit'
    id = db.Column(db.Integer, primary_key=True)
    enrolment_id = db.Column(db.Integer, index=True)
    user_id = db.Column(db.Integer)
    role = db.Column(db.String(10))
    action = db.Column(db.String(60), nullable=False)
    detail = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=_utcnow)


# --------------------------------------------------------------------------- #
# Exam catalogue, focus selection and schedule alerts
# --------------------------------------------------------------------------- #
EXAM_STATUSES = ('Confirmed', 'Tentative', 'Expected', 'Cancelled')


class MsExam(db.Model):
    """One entrance exam / admission milestone in the shared catalogue that students and mentors can follow.
    `version` goes up on every schedule change so calendar clients (ICS SEQUENCE) pick up the update."""
    __tablename__ = 'ms_exams'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(24), default='Other')
    stream = db.Column(db.String(40))                 # B.Tech/B.E. | B.Des | B.Arch | Research/Science | …
    starts_on = db.Column(db.Date, nullable=False)    # first day (or first day of the expected window)
    ends_on = db.Column(db.Date)
    status = db.Column(db.String(12), default='Expected')
    window_note = db.Column(db.String(200))           # e.g. "Window only — exact date not announced"
    source = db.Column(db.String(300))
    verified_on = db.Column(db.Date)
    notes = db.Column(db.Text)
    active = db.Column(db.Boolean, default=True)
    version = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=_utcnow)
    updated_at = db.Column(db.DateTime, default=_utcnow, onupdate=_utcnow)


class MsExamFocus(db.Model):
    __tablename__ = 'ms_exam_focus'
    id = db.Column(db.Integer, primary_key=True)
    enrolment_id = db.Column(db.Integer, db.ForeignKey('ms_enrolments.id', ondelete='CASCADE'), index=True, nullable=False)
    exam_id = db.Column(db.Integer, db.ForeignKey('ms_exams.id', ondelete='CASCADE'), index=True, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=_utcnow)
    __table_args__ = (db.UniqueConstraint('enrolment_id', 'exam_id'),)
    exam = db.relationship('MsExam')


class MsAlert(db.Model):
    __tablename__ = 'ms_alerts'
    id = db.Column(db.Integer, primary_key=True)
    exam_id = db.Column(db.Integer, db.ForeignKey('ms_exams.id', ondelete='SET NULL'), index=True)
    kind = db.Column(db.String(10), nullable=False)   # new | changed | removed
    title = db.Column(db.String(300), nullable=False)
    detail = db.Column(db.String(600))
    created_at = db.Column(db.DateTime, default=_utcnow, index=True)
    exam = db.relationship('MsExam')


class MsAlertRead(db.Model):
    __tablename__ = 'ms_alert_reads'
    alert_id = db.Column(db.Integer, db.ForeignKey('ms_alerts.id', ondelete='CASCADE'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)


# --------------------------------------------------------------------------- #
# Parent onboarding assessment (one per linked parent per student record)
# --------------------------------------------------------------------------- #
class MsParentAssessment(db.Model):
    __tablename__ = 'ms_parent_assessments'
    id = db.Column(db.Integer, primary_key=True)
    enrolment_id = db.Column(db.Integer, db.ForeignKey('ms_enrolments.id', ondelete='CASCADE'), index=True, nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), index=True, nullable=False)
    answers = db.Column(db.Text, default='{}')               # JSON of the form answers
    invited_at = db.Column(db.DateTime)                      # last time the invitation email was queued
    submitted_at = db.Column(db.DateTime)
    __table_args__ = (db.UniqueConstraint('enrolment_id', 'parent_id'),)
    parent = db.relationship('User')
