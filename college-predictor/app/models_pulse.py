"""
EduPulse-UCEED — chapter-wise MCQ question bank, practice attempts and progress.

New tables only (db.create_all adds them). The bank is data, not code: admins add / import questions and publish them;
students practise chapter by chapter; every answer is stored so the dashboard, mentor view and e-mail digests all read
the same rows.
"""
from datetime import datetime, timezone

from app.extensions import db


def _utcnow():
    return datetime.now(timezone.utc).replace(tzinfo=None)


class PulseChapter(db.Model):
    __tablename__ = 'pulse_chapters'
    id = db.Column(db.Integer, primary_key=True)
    exam = db.Column(db.String(20), default='uceed', index=True)
    key = db.Column(db.String(40), unique=True, nullable=False)
    title = db.Column(db.String(160), nullable=False)
    description = db.Column(db.String(400))
    position = db.Column(db.Integer, default=0)
    active = db.Column(db.Boolean, default=True)
    questions = db.relationship('PulseQuestion', backref='chapter', lazy='dynamic')


class PulseQuestion(db.Model):
    __tablename__ = 'pulse_questions'
    id = db.Column(db.Integer, primary_key=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey('pulse_chapters.id'), index=True, nullable=False)
    stem = db.Column(db.Text, nullable=False)
    option_a = db.Column(db.String(400), nullable=False)
    option_b = db.Column(db.String(400), nullable=False)
    option_c = db.Column(db.String(400), nullable=False)
    option_d = db.Column(db.String(400), nullable=False)
    correct = db.Column(db.String(1), nullable=False)            # 'A'..'D' — never sent to the browser before submission
    explanation = db.Column(db.Text)
    difficulty = db.Column(db.String(8), default='Medium')      # Easy | Medium | Hard
    source = db.Column(db.String(160), default='EduAakashaA original practice question')
    year = db.Column(db.String(8))                               # only for genuine previous-year items, if you hold the rights
    image_mime = db.Column(db.String(60))
    image_data = db.deferred(db.Column(db.LargeBinary))
    status = db.Column(db.String(10), default='draft', index=True)   # draft | published
    created_at = db.Column(db.DateTime, default=_utcnow)

    @property
    def has_image(self):
        return bool(self.image_mime)

    def options(self):
        return [('A', self.option_a), ('B', self.option_b), ('C', self.option_c), ('D', self.option_d)]


class PulseProfile(db.Model):
    """A student's EduPulse registration: who gets progress e-mails and how often."""
    __tablename__ = 'pulse_profiles'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
    exam = db.Column(db.String(20), default='uceed')
    student_class = db.Column(db.String(30))
    parent_email = db.Column(db.String(200))
    parent_consent = db.Column(db.Boolean, default=False)       # parent e-mails only with consent
    mentor_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'))
    frequency = db.Column(db.String(10), default='weekly')       # weekly | monthly | off
    email_results = db.Column(db.Boolean, default=True)          # e-mail the student after every practice set
    last_report_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=_utcnow)
    user = db.relationship('User', foreign_keys=[user_id], backref=db.backref(
        'pulse_profile', uselist=False, cascade='all, delete-orphan', passive_deletes=True))
    mentor = db.relationship('User', foreign_keys=[mentor_id])


class PulseAttempt(db.Model):
    __tablename__ = 'pulse_attempts'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), index=True, nullable=False)
    chapter_id = db.Column(db.Integer, db.ForeignKey('pulse_chapters.id'))          # null = mixed set
    mode = db.Column(db.String(10), default='practice')                              # practice | timed
    limit_sec = db.Column(db.Integer)
    started_at = db.Column(db.DateTime, default=_utcnow)
    submitted_at = db.Column(db.DateTime, index=True)
    total = db.Column(db.Integer, default=0)
    correct = db.Column(db.Integer, default=0)
    wrong = db.Column(db.Integer, default=0)
    skipped = db.Column(db.Integer, default=0)
    duration_sec = db.Column(db.Integer)
    chapter = db.relationship('PulseChapter')
    answers = db.relationship('PulseAnswer', backref='attempt', lazy='dynamic', cascade='all, delete-orphan')

    @property
    def answered(self):
        return (self.correct or 0) + (self.wrong or 0)

    @property
    def accuracy(self):
        return round(100 * self.correct / self.answered) if self.answered else None


class PulseAnswer(db.Model):
    __tablename__ = 'pulse_answers'
    id = db.Column(db.Integer, primary_key=True)
    attempt_id = db.Column(db.Integer, db.ForeignKey('pulse_attempts.id', ondelete='CASCADE'), index=True, nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('pulse_questions.id'), index=True, nullable=False)
    position = db.Column(db.Integer, default=0)
    chosen = db.Column(db.String(1))                                                 # null = skipped
    is_correct = db.Column(db.Boolean, default=False)
    question = db.relationship('PulseQuestion')


class PulseAnswerConf(db.Model):
    """How sure the student was about one practice answer: G guess, L low, M medium, H high. A separate table so existing databases need no migration."""
    __tablename__ = 'pulse_answer_conf'
    answer_id = db.Column(db.Integer, db.ForeignKey('pulse_answers.id', ondelete='CASCADE'), primary_key=True)
    confidence = db.Column(db.String(1), nullable=False)


class PulseMockResult(db.Model):
    """One finished UCEED mock-test attempt (a previous-year paper or an EduAakashaa practice paper), posted by the Mock Test Centre.
    `payload_json` keeps the per-question rows (answer, status, marks, confidence) so reports can be rebuilt without the paper."""
    __tablename__ = 'pulse_mock_results'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), index=True, nullable=False)
    paper = db.Column(db.String(10), index=True)                  # 2018..2026 or M1..M5
    paper_title = db.Column(db.String(80))
    mode = db.Column(db.String(12))                               # mock (timed) | practice
    score = db.Column(db.Float)
    max_score = db.Column(db.Float)
    answered = db.Column(db.Integer, default=0)
    right = db.Column(db.Integer, default=0)
    wrong = db.Column(db.Integer, default=0)
    sure_wrong = db.Column(db.Integer, default=0)                 # High confidence but wrong/partly wrong
    rated = db.Column(db.Integer, default=0)                      # answers carrying a confidence rating
    auto_submitted = db.Column(db.Boolean, default=False)
    started_at = db.Column(db.DateTime)
    finished_at = db.Column(db.DateTime, default=_utcnow, index=True)
    payload_json = db.Column(db.Text)
    user = db.relationship('User', foreign_keys=[user_id])


class PulseJeeResult(db.Model):
    """One finished JEE Main mock (EduAakashaa practice paper or an NTA previous-year paper) posted by the JEE Mock Test Centre.
    Marking is +4 / -1 (MCQ and numerical). `payload_json` keeps the per-question rows (answer, status, marks, confidence, seconds)."""
    __tablename__ = 'pulse_jee_results'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), index=True, nullable=False)
    paper = db.Column(db.String(12), index=True)
    paper_title = db.Column(db.String(80))
    mode = db.Column(db.String(12))                               # mock (timed) | practice
    score = db.Column(db.Float)
    max_score = db.Column(db.Float)
    attempted = db.Column(db.Integer, default=0)
    right = db.Column(db.Integer, default=0)
    wrong = db.Column(db.Integer, default=0)
    blank = db.Column(db.Integer, default=0)
    gained = db.Column(db.Float, default=0)                       # marks from correct answers
    lost = db.Column(db.Float, default=0)                         # marks deducted for wrong answers (positive number)
    avoidable = db.Column(db.Integer, default=0)                  # wrong answers rated Guess or Low
    sure_wrong = db.Column(db.Integer, default=0)                 # wrong answers rated High
    rated = db.Column(db.Integer, default=0)
    math_score = db.Column(db.Float, default=0)
    phy_score = db.Column(db.Float, default=0)
    chem_score = db.Column(db.Float, default=0)
    duration_sec = db.Column(db.Integer)
    auto_submitted = db.Column(db.Boolean, default=False)
    started_at = db.Column(db.DateTime)
    finished_at = db.Column(db.DateTime, default=_utcnow, index=True)
    payload_json = db.Column(db.Text)
    user = db.relationship('User', foreign_keys=[user_id])


class PulseReport(db.Model):
    """Log of progress digests sent, so a period is never mailed twice."""
    __tablename__ = 'pulse_reports'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), index=True, nullable=False)
    period_start = db.Column(db.DateTime)
    period_end = db.Column(db.DateTime)
    sent_to = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=_utcnow)
