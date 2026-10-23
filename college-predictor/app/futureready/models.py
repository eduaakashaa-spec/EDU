"""FutureReady Mentorship Portal (Grades 8-9): data model. New tables only (db.create_all adds them; nothing existing is altered).

Everything hangs off `FrProfile` (one student). Access is decided server-side in `access.py`: admin | assigned mentor | the student | a linked parent.
Question banks, branches and admission routes live in the database so administrators can edit and version them without a rebuild.
"""
import json
from datetime import datetime, timezone

from app.extensions import db


def _now():
    return datetime.now(timezone.utc).replace(tzinfo=None)


def jl(text, default=None):
    try:
        return json.loads(text) if text else (default if default is not None else {})
    except (ValueError, TypeError):
        return default if default is not None else {}


class FrProfile(db.Model):
    __tablename__ = 'fr_profiles'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), unique=True, index=True, nullable=False)
    mentor_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), index=True)
    grade = db.Column(db.Integer, default=8)                       # 8 | 9
    curriculum = db.Column(db.String(40))                          # CBSE | ICSE | State | IB | Other
    school = db.Column(db.String(160))
    interests_text = db.Column(db.Text)                            # student's own words, onboarding step
    learning_prefs = db.Column(db.String(300))
    student_goals = db.Column(db.Text)
    parent_goals = db.Column(db.Text)
    tier = db.Column(db.String(30), default='Standard')            # programme tier: configures live-meeting frequency
    meetings_per_month = db.Column(db.Integer, default=1)
    onboarding_step = db.Column(db.Integer, default=1)             # 1..10
    onboarding_done_at = db.Column(db.DateTime)
    consent_at = db.Column(db.DateTime)                            # parent/guardian consent recorded
    consent_by = db.Column(db.String(160))
    status = db.Column(db.String(16), default='Active')            # Active | Paused | Completed
    demo = db.Column(db.Boolean, default=False)                    # clearly-labelled sample student; never mixed with real exports
    created_at = db.Column(db.DateTime, default=_now)

    student = db.relationship('User', foreign_keys=[user_id], backref=db.backref('fr_profile', uselist=False))
    mentor = db.relationship('User', foreign_keys=[mentor_id])


class FrParentLink(db.Model):
    __tablename__ = 'fr_parent_links'
    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('fr_profiles.id', ondelete='CASCADE'), index=True, nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), index=True, nullable=False)
    relation = db.Column(db.String(40), default='Parent')
    __table_args__ = (db.UniqueConstraint('profile_id', 'parent_id'),)
    parent = db.relationship('User')


# ---- content (editable, versioned) --------------------------------------------------------------------------------------
class FrAssessment(db.Model):
    __tablename__ = 'fr_assessments'
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(40), unique=True, nullable=False, index=True)
    number = db.Column(db.Integer)                                 # 1-12 as in the programme design; None for centres (quizzes)
    group = db.Column(db.String(20), default='core')               # core | engineering | entrance | sampler | foundation
    title = db.Column(db.String(160), nullable=False)
    purpose = db.Column(db.Text)
    instructions = db.Column(db.Text)
    grades = db.Column(db.String(20), default='8,9')
    minutes = db.Column(db.Integer, default=15)
    kind = db.Column(db.String(16), default='mixed')               # objective | self | rubric | mixed
    interpretation = db.Column(db.Text)                            # plain-language "what this means / does not mean"
    accessibility = db.Column(db.String(300))
    version = db.Column(db.Integer, default=1)
    review_date = db.Column(db.Date)
    active = db.Column(db.Boolean, default=True)
    position = db.Column(db.Integer, default=0)
    questions = db.relationship('FrQuestion', backref='assessment', lazy='dynamic', order_by='FrQuestion.position')


class FrQuestion(db.Model):
    __tablename__ = 'fr_questions'
    id = db.Column(db.Integer, primary_key=True)
    assessment_id = db.Column(db.Integer, db.ForeignKey('fr_assessments.id', ondelete='CASCADE'), index=True, nullable=False)
    code = db.Column(db.String(40), index=True, nullable=False)    # stable across versions, e.g. AF-M-03
    version = db.Column(db.Integer, default=1)
    active = db.Column(db.Boolean, default=True)                   # an edit adds version+1 and retires the old row (attempt history stays accurate)
    position = db.Column(db.Integer, default=0)
    qtype = db.Column(db.String(12), default='mcq')                # mcq | multi | likert | choice | text
    prompt = db.Column(db.Text, nullable=False)
    options_json = db.Column(db.Text)                              # list of strings; for 'choice' list of {t, tags}
    answer_json = db.Column(db.Text)                               # mcq: index; multi: [indexes]; others: null
    explanation = db.Column(db.Text)
    distractor_json = db.Column(db.Text)                           # {"0": "why students pick this", ...}
    skill = db.Column(db.String(40), index=True)                   # skill / dimension this item reports under
    reverse = db.Column(db.Boolean, default=False)                 # likert: reverse-scored
    level = db.Column(db.Integer)                                  # sampler difficulty 1-3
    grade_min = db.Column(db.Integer, default=8)
    grade_max = db.Column(db.Integer, default=9)
    meta_json = db.Column(db.Text)                                 # free extras: audience (student|parent), set id, rubric hints

    @property
    def options(self):
        return jl(self.options_json, [])

    @property
    def answer(self):
        return jl(self.answer_json, None)

    @property
    def distractors(self):
        return jl(self.distractor_json, {})

    @property
    def meta(self):
        return jl(self.meta_json, {})


class FrBranch(db.Model):
    __tablename__ = 'fr_branches'
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(40), unique=True, nullable=False)
    family = db.Column(db.String(60), index=True)
    name = db.Column(db.String(120), nullable=False)
    studies = db.Column(db.Text)
    problems = db.Column(db.Text)
    projects = db.Column(db.Text)
    foundations = db.Column(db.Text)
    skills = db.Column(db.Text)
    activities = db.Column(db.Text)
    related = db.Column(db.String(300))                            # comma-separated keys
    environment = db.Column(db.Text)                               # work styles and environments
    tags_json = db.Column(db.Text)                                 # interest-tag affinities used by the interest map
    active = db.Column(db.Boolean, default=True)
    position = db.Column(db.Integer, default=0)
    last_reviewed = db.Column(db.Date)


class FrAdmission(db.Model):
    """One admission route / exam / counselling process. Year-specific facts must carry a source and a verification date,
    otherwise they are shown as 'requires verification' — never as confirmed."""
    __tablename__ = 'fr_admissions'
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(40), unique=True, nullable=False)
    name = db.Column(db.String(160), nullable=False)
    classification = db.Column(db.String(40))                      # Entrance examination | Counselling process | Merit-based admission process | Institution exam
    summary = db.Column(db.Text)                                   # stable, general role in plain language
    how_it_works = db.Column(db.Text)
    eligibility = db.Column(db.Text)                               # only if verified for `admission_year`
    admission_year = db.Column(db.String(12))
    official_url = db.Column(db.String(300))
    last_verified = db.Column(db.Date)                             # None => requires verification
    reviewer = db.Column(db.String(120))
    status = db.Column(db.String(24), default='needs_verification')  # verified | needs_verification
    position = db.Column(db.Integer, default=0)
    active = db.Column(db.Boolean, default=True)


class FrResource(db.Model):
    __tablename__ = 'fr_resources'
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(60), unique=True, nullable=False)
    title = db.Column(db.String(160), nullable=False)
    kind = db.Column(db.String(20), default='activity')            # activity | project | explainer | exercise
    body = db.Column(db.Text)
    minutes = db.Column(db.Integer, default=30)
    materials = db.Column(db.String(300))
    skills = db.Column(db.String(200))                             # comma-separated skill keys it supports
    grades = db.Column(db.String(10), default='8,9')
    assessed_by = db.Column(db.String(200))                        # how completion is checked
    active = db.Column(db.Boolean, default=True)


# ---- student records ---------------------------------------------------------------------------------------------------
class FrAttempt(db.Model):
    __tablename__ = 'fr_attempts'
    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('fr_profiles.id', ondelete='CASCADE'), index=True, nullable=False)
    assessment_id = db.Column(db.Integer, db.ForeignKey('fr_assessments.id'), index=True, nullable=False)
    audience = db.Column(db.String(10), default='student')         # student | parent (alignment assessment)
    set_key = db.Column(db.String(40))                             # sampler: "<skill>:<level>"
    attempt_no = db.Column(db.Integer, default=1)
    version = db.Column(db.Integer, default=1)                     # assessment version at the time
    status = db.Column(db.String(14), default='in_progress')       # in_progress | submitted
    responses_json = db.Column(db.Text)                            # {code: value}
    result_json = db.Column(db.Text)                               # computed by engine.score_attempt
    rubric_json = db.Column(db.Text)                               # mentor rubric ratings for practical tasks
    started_at = db.Column(db.DateTime, default=_now)
    submitted_at = db.Column(db.DateTime)
    assessment = db.relationship('FrAssessment')
    profile = db.relationship('FrProfile', backref=db.backref('attempts', lazy='dynamic'))

    @property
    def responses(self):
        return jl(self.responses_json, {})

    @property
    def result(self):
        return jl(self.result_json, {})

    @property
    def rubric(self):
        return jl(self.rubric_json, {})


class FrSkillScore(db.Model):
    """Flat rows written when an attempt is scored: lets growth reports compare a student with their own history."""
    __tablename__ = 'fr_skill_scores'
    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('fr_profiles.id', ondelete='CASCADE'), index=True, nullable=False)
    attempt_id = db.Column(db.Integer, db.ForeignKey('fr_attempts.id', ondelete='CASCADE'), index=True, nullable=False)
    assessment_key = db.Column(db.String(40), index=True)
    skill = db.Column(db.String(40), index=True)
    kind = db.Column(db.String(12))                                # objective | self | rubric
    value = db.Column(db.Float)                                    # objective/rubric: percent 0-100; self: mean 1-5
    n = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=_now)


class FrShortlist(db.Model):
    __tablename__ = 'fr_shortlist'
    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('fr_profiles.id', ondelete='CASCADE'), index=True, nullable=False)
    branch_id = db.Column(db.Integer, db.ForeignKey('fr_branches.id', ondelete='CASCADE'), nullable=False)
    note = db.Column(db.Text)                                      # what attracted the student
    created_at = db.Column(db.DateTime, default=_now)
    __table_args__ = (db.UniqueConstraint('profile_id', 'branch_id'),)
    branch = db.relationship('FrBranch')


class FrGoal(db.Model):
    __tablename__ = 'fr_goals'
    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('fr_profiles.id', ondelete='CASCADE'), index=True, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    metric = db.Column(db.String(120))                             # how we will know
    baseline = db.Column(db.Float)
    target = db.Column(db.Float)
    current = db.Column(db.Float)
    unit = db.Column(db.String(30))
    due_date = db.Column(db.Date)
    status = db.Column(db.String(14), default='Active')            # Active | Achieved | Revised | Dropped
    set_by = db.Column(db.String(10), default='mentor')            # mentor | student | parent
    created_at = db.Column(db.DateTime, default=_now)


class FrAction(db.Model):
    __tablename__ = 'fr_actions'
    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('fr_profiles.id', ondelete='CASCADE'), index=True, nullable=False)
    goal_id = db.Column(db.Integer, db.ForeignKey('fr_goals.id', ondelete='SET NULL'))
    title = db.Column(db.String(240), nullable=False)
    detail = db.Column(db.Text)
    why = db.Column(db.String(300))
    owner = db.Column(db.String(10), default='student')            # student | parent | mentor
    source = db.Column(db.String(14), default='mentor')            # mentor | recommendation | student | onboarding
    resource_key = db.Column(db.String(60))
    due_date = db.Column(db.Date)
    status = db.Column(db.String(14), default='Not started')       # Not started | In progress | Done | Skipped
    evidence = db.Column(db.Text)                                  # what the student did / learned
    reflection = db.Column(db.Text)
    mentor_feedback = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=_now)
    completed_at = db.Column(db.DateTime)


class FrNote(db.Model):
    """Mentor notes. visibility 'mentor' is never shown to student or parent. `basis` keeps self-reports, parent observations,
    assessment results and mentor judgement visibly separate."""
    __tablename__ = 'fr_notes'
    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('fr_profiles.id', ondelete='CASCADE'), index=True, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'))
    kind = db.Column(db.String(14), default='observation')         # session | observation | parent | escalation | message
    basis = db.Column(db.String(16), default='mentor')             # self_report | parent | assessment | mentor
    visibility = db.Column(db.String(10), default='mentor')       # mentor (private) | shared (student+parent)
    body = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=_now)
    author = db.relationship('User')


class FrSession(db.Model):
    __tablename__ = 'fr_sessions'
    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('fr_profiles.id', ondelete='CASCADE'), index=True, nullable=False)
    kind = db.Column(db.String(14), default='monthly')             # initial | monthly | quarterly | adhoc | transition
    title = db.Column(db.String(200))
    planned_at = db.Column(db.DateTime)
    held_at = db.Column(db.DateTime)
    status = db.Column(db.String(12), default='Planned')           # Planned | Held | Missed | Cancelled
    agenda = db.Column(db.Text)
    summary = db.Column(db.Text)                                   # shared summary
    created_at = db.Column(db.DateTime, default=_now)


class FrRecommendation(db.Model):
    __tablename__ = 'fr_recommendations'
    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('fr_profiles.id', ondelete='CASCADE'), index=True, nullable=False)
    rule_key = db.Column(db.String(60), index=True)
    resource_key = db.Column(db.String(60))
    title = db.Column(db.String(200))
    why = db.Column(db.Text)
    learn = db.Column(db.Text)
    minutes = db.Column(db.Integer)
    materials = db.Column(db.String(300))
    assessed_by = db.Column(db.String(300))
    next_step = db.Column(db.String(300))
    evidence_json = db.Column(db.Text)
    status = db.Column(db.String(12), default='Suggested')         # Suggested | Accepted | Done | Dismissed
    approved = db.Column(db.Boolean, default=False)               # a mentor has reviewed it (shown to parent/student once approved or auto-approved low-stakes)
    created_at = db.Column(db.DateTime, default=_now)


class FrProject(db.Model):
    __tablename__ = 'fr_projects'
    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('fr_profiles.id', ondelete='CASCADE'), index=True, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(12), default='Planned')           # Planned | In progress | Completed
    evidence_url = db.Column(db.String(400))
    reflection = db.Column(db.Text)
    mentor_feedback = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=_now)


class FrBadge(db.Model):
    __tablename__ = 'fr_badges'
    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('fr_profiles.id', ondelete='CASCADE'), index=True, nullable=False)
    key = db.Column(db.String(40), nullable=False)
    earned_at = db.Column(db.DateTime, default=_now)
    __table_args__ = (db.UniqueConstraint('profile_id', 'key'),)


class FrReport(db.Model):
    __tablename__ = 'fr_reports'
    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('fr_profiles.id', ondelete='CASCADE'), index=True, nullable=False)
    kind = db.Column(db.String(20), nullable=False)                # starting_point | skill_gap | engineering | monthly | quarterly | growth
    title = db.Column(db.String(200))
    period = db.Column(db.String(40))
    data_json = db.Column(db.Text)                                 # frozen snapshot: what was reviewed is what is shared
    status = db.Column(db.String(10), default='Draft')             # Draft | Shared
    created_by = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'))
    created_at = db.Column(db.DateTime, default=_now)
    shared_at = db.Column(db.DateTime)

    @property
    def data(self):
        return jl(self.data_json, {})


class FrNotice(db.Model):
    __tablename__ = 'fr_notices'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), index=True, nullable=False)
    profile_id = db.Column(db.Integer, db.ForeignKey('fr_profiles.id', ondelete='CASCADE'), index=True)
    text = db.Column(db.String(300), nullable=False)
    url = db.Column(db.String(200))
    read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=_now)


class FrWindow(db.Model):
    """Scheduled assessment window / reporting period (administrator)."""
    __tablename__ = 'fr_windows'
    id = db.Column(db.Integer, primary_key=True)
    assessment_key = db.Column(db.String(40))                      # None = reporting period
    label = db.Column(db.String(120))
    opens_on = db.Column(db.Date)
    closes_on = db.Column(db.Date)
    grade = db.Column(db.Integer)                                  # None = all grades


class FrAudit(db.Model):
    __tablename__ = 'fr_audit'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    role = db.Column(db.String(10))
    profile_id = db.Column(db.Integer, index=True)
    action = db.Column(db.String(60), nullable=False)
    detail = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=_now)
