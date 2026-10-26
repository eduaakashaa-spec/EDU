"""EduPulse - Reinforcement: daily targeted practice with confidence capture, chapter analytics and mentor intelligence.

New tables only (db.create_all adds them). Design rules:
  * `RfAttempt` rows are immutable history: a repeated question creates a new row, nothing is overwritten.
  * Confidence (G/L/M/H) is stored beside, never inside, correctness.
  * A question edit creates version n+1 with the same `qid`; attempts keep pointing at the version that was answered.
  * Answer keys are never sent to students before the assignment's release rule says so (enforced in routes).
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


class RfTaxonomy(db.Model):
    """Exam -> subject -> chapter -> topic, plus the chapter's prerequisite (a single chapter code, optional)."""
    __tablename__ = 'rf_taxonomy'
    id = db.Column(db.Integer, primary_key=True)
    exam = db.Column(db.String(8), nullable=False, index=True)       # UCEED | JEE
    subject = db.Column(db.String(40), nullable=False)
    chapter = db.Column(db.String(80), nullable=False)
    code = db.Column(db.String(12), index=True)                      # chapter code used by the mock centres (CNQ, KIN, OBS ...)
    prereq = db.Column(db.String(12))                                 # code of a prerequisite chapter
    position = db.Column(db.Integer, default=0)
    __table_args__ = (db.UniqueConstraint('exam', 'subject', 'chapter'),)


class RfQuestionImage(db.Model):
    """Image parts of a question, keyed by the stable qid so every version keeps working: kind 'q' = the question (stem and options as printed), 's' = the worked solution.
    A separate table so existing databases need no migration."""
    __tablename__ = 'rf_question_images'
    id = db.Column(db.Integer, primary_key=True)
    qid = db.Column(db.String(40), nullable=False, index=True)
    kind = db.Column(db.String(1), nullable=False)
    mime = db.Column(db.String(30), default='image/webp')
    data = db.Column(db.LargeBinary, nullable=False)
    __table_args__ = (db.UniqueConstraint('qid', 'kind', name='uq_rf_qimg'),)


class RfQuestion(db.Model):
    __tablename__ = 'rf_questions'
    id = db.Column(db.Integer, primary_key=True)
    qid = db.Column(db.String(40), nullable=False, index=True)       # stable across versions, unique among active rows
    version = db.Column(db.Integer, default=1)
    active = db.Column(db.Boolean, default=True)                      # the current version of this qid
    exam = db.Column(db.String(8), nullable=False, index=True)
    subject = db.Column(db.String(40), index=True)
    chapter = db.Column(db.String(80), index=True)
    topic = db.Column(db.String(120))
    concept = db.Column(db.String(200))
    difficulty = db.Column(db.Integer, default=2)                    # 1 easy, 2 medium, 3 challenging
    qtype = db.Column(db.String(4), default='mcq')                    # mcq | msq | nat
    stem = db.Column(db.Text, nullable=False)                         # sanitised html
    options_json = db.Column(db.Text)
    answer_json = db.Column(db.Text)                                  # mcq: "B"; msq: ["A","C"]; nat: [[lo, hi], ...]
    explanation = db.Column(db.Text)
    misconception = db.Column(db.Text)                                # the likely error this question exposes
    marks = db.Column(db.Float, default=4)
    neg_marks = db.Column(db.Float, default=1)
    est_sec = db.Column(db.Integer, default=90)
    source = db.Column(db.String(200))
    author_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'))
    reviewer_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'))
    status = db.Column(db.String(10), default='draft', index=True)    # draft | in_review | approved | retired
    created_at = db.Column(db.DateTime, default=_now)

    @property
    def options(self):
        return jl(self.options_json, [])

    @property
    def answer(self):
        return jl(self.answer_json, None)


class RfStudent(db.Model):
    """The reinforcement roster: who a mentor assigns work to."""
    __tablename__ = 'rf_students'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), unique=True, nullable=False, index=True)
    mentor_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), index=True)
    exam = db.Column(db.String(8), default='JEE')
    grade = db.Column(db.String(20))
    group_name = db.Column(db.String(60))
    parent_report = db.Column(db.Boolean, default=False)              # parents may read the weekly report only when this is switched on
    demo = db.Column(db.Boolean, default=False)
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=_now)
    user = db.relationship('User', foreign_keys=[user_id])
    mentor = db.relationship('User', foreign_keys=[mentor_id])


class RfAssignment(db.Model):
    __tablename__ = 'rf_assignments'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(160), nullable=False)
    exam = db.Column(db.String(8), nullable=False)
    subject = db.Column(db.String(40))
    chapter = db.Column(db.String(80))
    topic = db.Column(db.String(120))
    objective = db.Column(db.String(300))
    instructions = db.Column(db.Text)
    n_questions = db.Column(db.Integer, default=8)
    mix_json = db.Column(db.Text)                                     # {"1": easy, "2": medium, "3": hard} counts
    selection = db.Column(db.String(12), default='filter')            # manual | filter | recommended
    distinct_per_student = db.Column(db.Boolean, default=False)
    start_at = db.Column(db.DateTime, default=_now)
    due_at = db.Column(db.DateTime)
    release = db.Column(db.String(12), default='after_submit')        # immediate | after_submit | scheduled | manual
    release_at = db.Column(db.DateTime)
    popup = db.Column(db.String(12), default='dismissible')           # mandatory | dismissible | time_limited
    popup_hours = db.Column(db.Integer, default=24)                   # time_limited: popup stops this many hours after start
    allow_remind = db.Column(db.Boolean, default=True)
    allow_back = db.Column(db.Boolean, default=True)
    remind_hours = db.Column(db.Integer, default=6)                   # "due soon" notice this many hours before the deadline
    timed = db.Column(db.Boolean, default=True)                       # record seconds per question
    source_id = db.Column(db.Integer)                                 # duplicated from
    recommendation_id = db.Column(db.Integer)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'))
    status = db.Column(db.String(10), default='active', index=True)   # active | closed | cancelled
    created_at = db.Column(db.DateTime, default=_now)

    @property
    def mix(self):
        return jl(self.mix_json, {})


class RfAssignmentStudent(db.Model):
    """One student's copy of an assignment (own question set, own progress). Unique per (assignment, student): never duplicated on re-login."""
    __tablename__ = 'rf_assignment_students'
    id = db.Column(db.Integer, primary_key=True)
    assignment_id = db.Column(db.Integer, db.ForeignKey('rf_assignments.id', ondelete='CASCADE'), index=True, nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('rf_students.id', ondelete='CASCADE'), index=True, nullable=False)
    status = db.Column(db.String(12), default='not_started')          # not_started | in_progress | completed
    started_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    dismissed_until = db.Column(db.DateTime)
    last_pos = db.Column(db.Integer, default=0)
    __table_args__ = (db.UniqueConstraint('assignment_id', 'student_id'),)
    assignment = db.relationship('RfAssignment', backref=db.backref('students', lazy='dynamic', cascade='all, delete-orphan'))
    student = db.relationship('RfStudent')


class RfItem(db.Model):
    """A question placed in one student's assignment."""
    __tablename__ = 'rf_items'
    id = db.Column(db.Integer, primary_key=True)
    asg_student_id = db.Column(db.Integer, db.ForeignKey('rf_assignment_students.id', ondelete='CASCADE'), index=True, nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('rf_questions.id'), nullable=False)
    position = db.Column(db.Integer, default=0)
    asg_student = db.relationship('RfAssignmentStudent', backref=db.backref('items', lazy='dynamic', order_by='RfItem.position', cascade='all, delete-orphan'))
    question = db.relationship('RfQuestion')
    __table_args__ = (db.UniqueConstraint('asg_student_id', 'question_id'),)


class RfDraft(db.Model):
    """Autosaved answer while an assignment is in progress. Becomes immutable RfAttempt rows on submit."""
    __tablename__ = 'rf_drafts'
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('rf_items.id', ondelete='CASCADE'), unique=True, nullable=False)
    answer_json = db.Column(db.Text)
    confidence = db.Column(db.String(1))
    seconds = db.Column(db.Integer, default=0)
    updated_at = db.Column(db.DateTime, default=_now, onupdate=_now)


class RfAttempt(db.Model):
    __tablename__ = 'rf_attempts'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('rf_students.id', ondelete='CASCADE'), index=True, nullable=False)
    assignment_id = db.Column(db.Integer, db.ForeignKey('rf_assignments.id', ondelete='SET NULL'), index=True)
    question_id = db.Column(db.Integer, db.ForeignKey('rf_questions.id'), index=True, nullable=False)   # the version answered
    qid = db.Column(db.String(40), index=True)                        # stable id (join across versions)
    exam = db.Column(db.String(8))
    subject = db.Column(db.String(40), index=True)
    chapter = db.Column(db.String(80), index=True)
    topic = db.Column(db.String(120))
    difficulty = db.Column(db.Integer)
    answer_json = db.Column(db.Text)
    confidence = db.Column(db.String(1))                              # G | L | M | H (null only if the student skipped, which the UI prevents)
    correct = db.Column(db.Boolean)
    marks = db.Column(db.Float)
    seconds = db.Column(db.Integer)
    answered_at = db.Column(db.DateTime, default=_now, index=True)
    question = db.relationship('RfQuestion')
    student = db.relationship('RfStudent')


class RfObservation(db.Model):
    __tablename__ = 'rf_observations'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('rf_students.id', ondelete='CASCADE'), index=True, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'))
    chapter = db.Column(db.String(80))
    body = db.Column(db.Text, nullable=False)
    follow_up_on = db.Column(db.Date)
    done = db.Column(db.Boolean, default=False)
    for_parent = db.Column(db.Boolean, default=False)                # shown in the parent report only when ticked
    created_at = db.Column(db.DateTime, default=_now)
    author = db.relationship('User')


class RfRecommendation(db.Model):
    __tablename__ = 'rf_recommendations'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('rf_students.id', ondelete='CASCADE'), index=True, nullable=False)
    rule = db.Column(db.String(30))
    chapter = db.Column(db.String(80))
    title = db.Column(db.String(200))
    why = db.Column(db.Text)
    evidence_json = db.Column(db.Text)
    question_ids = db.Column(db.Text)                                 # json list of RfQuestion ids suggested
    follow_up_days = db.Column(db.Integer, default=3)
    status = db.Column(db.String(10), default='suggested', index=True)   # suggested | approved | rejected
    assignment_id = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=_now)
    student = db.relationship('RfStudent')


class RfNotice(db.Model):
    __tablename__ = 'rf_notices'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), index=True, nullable=False)
    kind = db.Column(db.String(24))
    text = db.Column(db.String(300), nullable=False)
    url = db.Column(db.String(200))
    dedupe_key = db.Column(db.String(120))
    read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=_now)
    __table_args__ = (db.UniqueConstraint('user_id', 'dedupe_key'),)


class RfSetting(db.Model):
    __tablename__ = 'rf_settings'
    key = db.Column(db.String(40), primary_key=True)
    value = db.Column(db.String(60))


class RfAudit(db.Model):
    __tablename__ = 'rf_audit'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    action = db.Column(db.String(60), nullable=False)
    detail = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=_now, index=True)
