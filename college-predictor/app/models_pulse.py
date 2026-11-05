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


class PulseTn10Result(db.Model):
    """One finished Tamil Nadu Class 10 mock or unit test (EduPulse-TN Class 10 Mock Test Centre). Auto-graded objective questions, 1 mark each, no negative marking.
    `payload_json` keeps one row per question: the chosen option, whether it was right, the confidence rating (G/L/M/H) and the seconds spent."""
    __tablename__ = 'pulse_tn10_results'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), index=True, nullable=False)
    mock = db.Column(db.String(12), index=True)                  # M-F1, S-F2, M-U3 ...
    title = db.Column(db.String(120))
    subject = db.Column(db.String(20))                           # Mathematics | Science
    score = db.Column(db.Integer, default=0)
    total = db.Column(db.Integer, default=0)
    attempted = db.Column(db.Integer, default=0)
    rated = db.Column(db.Integer, default=0)
    sure_wrong = db.Column(db.Integer, default=0)                # wrong answers rated High
    lucky = db.Column(db.Integer, default=0)                     # right answers rated Guess or Low
    duration_sec = db.Column(db.Integer)
    timed = db.Column(db.Boolean, default=True)
    finished_at = db.Column(db.DateTime, default=_utcnow, index=True)
    payload_json = db.Column(db.Text)
    user = db.relationship('User', foreign_keys=[user_id])


class PulseIatResult(db.Model):
    """One finished IISER Aptitude Test (IAT) mock or practice test. +4 for a right answer, -1 for a wrong one, 0 for blank (as in the real IAT).
    `payload_json` keeps one row per question: the chosen option (position shown), right or wrong, the confidence rating (G/L/M/H) and the seconds spent."""
    __tablename__ = 'pulse_iat_results'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), index=True, nullable=False)
    mock = db.Column(db.String(16), index=True)                  # F1, Y2026, S-BIO1 ...
    title = db.Column(db.String(120))
    score = db.Column(db.Integer, default=0)                     # marks: +4 / -1
    max_score = db.Column(db.Integer, default=0)
    right = db.Column(db.Integer, default=0)
    wrong = db.Column(db.Integer, default=0)
    blank = db.Column(db.Integer, default=0)
    rated = db.Column(db.Integer, default=0)
    sure_wrong = db.Column(db.Integer, default=0)                # wrong answers rated High
    lucky = db.Column(db.Integer, default=0)                     # right answers rated Guess or Low
    duration_sec = db.Column(db.Integer)
    timed = db.Column(db.Boolean, default=True)
    finished_at = db.Column(db.DateTime, default=_utcnow, index=True)
    payload_json = db.Column(db.Text)
    user = db.relationship('User', foreign_keys=[user_id])



class PulseNidResult(db.Model):
    """One finished NID DAT mock or practice test (B.Des Prelims or M.Des CDAT Paper 1 format). Marks as printed on the question (1 or 2), no negative marking.
    `payload_json` keeps one row per question: the chosen option, right or wrong, the marks, the confidence rating (G/L/M/H) and the seconds spent."""
    __tablename__ = 'pulse_nid_results'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), index=True, nullable=False)
    mock = db.Column(db.String(16), index=True)                  # B1, M2, O-BDES25, S-SPA1 ...
    title = db.Column(db.String(120))
    score = db.Column(db.Integer, default=0)
    max_score = db.Column(db.Integer, default=0)
    right = db.Column(db.Integer, default=0)
    wrong = db.Column(db.Integer, default=0)
    blank = db.Column(db.Integer, default=0)
    rated = db.Column(db.Integer, default=0)
    sure_wrong = db.Column(db.Integer, default=0)
    lucky = db.Column(db.Integer, default=0)
    duration_sec = db.Column(db.Integer)
    timed = db.Column(db.Boolean, default=True)
    finished_at = db.Column(db.DateTime, default=_utcnow, index=True)
    payload_json = db.Column(db.Text)
    user = db.relationship('User', foreign_keys=[user_id])


class PulseExpResult(db.Model):
    """One finished EduPulse-Explorer test (Grades 7 to 10): discovery test, exam taster, skill set or Daily 10. One point per question, nothing deducted.
    `payload_json` keeps one row per question: id, skill, topic, exam families, difficulty, chosen option, right or wrong, confidence (G/L/M/H) and seconds."""
    __tablename__ = 'pulse_exp_results'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), index=True, nullable=False)
    mock = db.Column(db.String(24), index=True)                  # D78, D910, X-JEE, K-MAT, DAILY ...
    title = db.Column(db.String(120))
    grade = db.Column(db.Integer)
    score = db.Column(db.Integer, default=0)
    max_score = db.Column(db.Integer, default=0)
    right = db.Column(db.Integer, default=0)
    wrong = db.Column(db.Integer, default=0)
    blank = db.Column(db.Integer, default=0)
    rated = db.Column(db.Integer, default=0)
    sure_wrong = db.Column(db.Integer, default=0)
    lucky = db.Column(db.Integer, default=0)
    duration_sec = db.Column(db.Integer)
    timed = db.Column(db.Boolean, default=True)
    finished_at = db.Column(db.DateTime, default=_utcnow, index=True)
    payload_json = db.Column(db.Text)
    user = db.relationship('User', foreign_keys=[user_id])


class PulseExpCard(db.Model):
    """Spaced reinforcement: one card per question idea a student got wrong or was unsure of. `qkey` is a bank id, or g:<generator> for a generated idea that returns with new numbers.
    Leitner boxes 0 to 5; a right answer moves the card up and pushes its next review out, a wrong answer sends it back to box 0."""
    __tablename__ = 'pulse_exp_cards'
    __table_args__ = (db.UniqueConstraint('user_id', 'qkey', name='uq_exp_card'),)
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), index=True, nullable=False)
    qkey = db.Column(db.String(48), nullable=False)
    skill = db.Column(db.String(4))
    topic = db.Column(db.String(120))
    box = db.Column(db.Integer, default=0)
    due = db.Column(db.Date, index=True)
    seen = db.Column(db.Integer, default=0)
    right_run = db.Column(db.Integer, default=0)
    last_right = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime, default=_utcnow)
    updated_at = db.Column(db.DateTime, default=_utcnow)


class PulseExpProfile(db.Model):
    """A student's Explorer settings: grade, the interest check answers and the weekly goal."""
    __tablename__ = 'pulse_exp_profiles'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
    grade = db.Column(db.Integer, default=8)
    interests_json = db.Column(db.Text)
    weekly_goal = db.Column(db.Integer, default=3)
    updated_at = db.Column(db.DateTime, default=_utcnow)


class PulseExpCreative(db.Model):
    """A creative challenge a student did at home and marked against the rubric (not marked by the computer)."""
    __tablename__ = 'pulse_exp_creative'
    __table_args__ = (db.UniqueConstraint('user_id', 'cid', name='uq_exp_creative'),)
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), index=True, nullable=False)
    cid = db.Column(db.String(8), nullable=False)
    scores_json = db.Column(db.Text)
    total = db.Column(db.Integer, default=0)
    note = db.Column(db.String(400))
    done_at = db.Column(db.DateTime, default=_utcnow)


class PulseNiftResult(db.Model):
    """One finished EduPulse-NIFT test: a GAT mock, a previous-year paper, a section set or a Daily Review. +1 for a right answer, -0.25 for a wrong one (as in the NIFT papers).
    `payload_json` keeps one row per question: id, section, topic, chosen option, right or wrong, confidence (G/L/M/H) and seconds."""
    __tablename__ = 'pulse_nift_results'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), index=True, nullable=False)
    mock = db.Column(db.String(24), index=True)                  # M-BDES-1, Y-2022-BDES, S-QA, DAILY ...
    title = db.Column(db.String(140))
    prog = db.Column(db.String(8))                               # BDES, BFTECH, MDES, MFM, MFTECH
    score = db.Column(db.Float, default=0)
    max_score = db.Column(db.Float, default=0)
    right = db.Column(db.Integer, default=0)
    wrong = db.Column(db.Integer, default=0)
    blank = db.Column(db.Integer, default=0)
    rated = db.Column(db.Integer, default=0)
    sure_wrong = db.Column(db.Integer, default=0)
    lucky = db.Column(db.Integer, default=0)
    duration_sec = db.Column(db.Integer)
    timed = db.Column(db.Boolean, default=True)
    finished_at = db.Column(db.DateTime, default=_utcnow, index=True)
    payload_json = db.Column(db.Text)
    user = db.relationship('User', foreign_keys=[user_id])


class PulseNiftCard(db.Model):
    """Spaced reinforcement for NIFT: one card per question idea missed or unsure. `qkey` is a bank id, or g:<generator> for a generated idea that returns with new numbers.
    Leitner boxes 0 to 5."""
    __tablename__ = 'pulse_nift_cards'
    __table_args__ = (db.UniqueConstraint('user_id', 'qkey', name='uq_nift_card'),)
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), index=True, nullable=False)
    qkey = db.Column(db.String(48), nullable=False)
    sec = db.Column(db.String(4))
    topic = db.Column(db.String(120))
    box = db.Column(db.Integer, default=0)
    due = db.Column(db.Date, index=True)
    seen = db.Column(db.Integer, default=0)
    right_run = db.Column(db.Integer, default=0)
    last_right = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime, default=_utcnow)
    updated_at = db.Column(db.DateTime, default=_utcnow)


class PulseNiftStudio(db.Model):
    """A NIFT CAT / studio task a student did on paper and marked against the rubric (not marked by the computer)."""
    __tablename__ = 'pulse_nift_studio'
    __table_args__ = (db.UniqueConstraint('user_id', 'tid', name='uq_nift_studio'),)
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), index=True, nullable=False)
    tid = db.Column(db.String(8), nullable=False)
    scores_json = db.Column(db.Text)
    total = db.Column(db.Integer, default=0)
    note = db.Column(db.String(400))
    done_at = db.Column(db.DateTime, default=_utcnow)


class PulseNeetResult(db.Model):
    """One finished EduPulse-NEET test: a full mock, a half mock, a previous-year paper, a subject set or a Daily Review. +4 for a right answer, -1 for a wrong one (as in NEET).
    `payload_json` keeps one row per question: id, subject, topic, chosen option, right or wrong, confidence (G/L/M/H) and seconds."""
    __tablename__ = 'pulse_neet_results'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), index=True, nullable=False)
    mock = db.Column(db.String(24), index=True)                  # M-FULL, M-PC, Y-2022, S-PHY, DAILY ...
    title = db.Column(db.String(140))
    score = db.Column(db.Float, default=0)
    max_score = db.Column(db.Float, default=0)
    right = db.Column(db.Integer, default=0)
    wrong = db.Column(db.Integer, default=0)
    blank = db.Column(db.Integer, default=0)
    rated = db.Column(db.Integer, default=0)
    sure_wrong = db.Column(db.Integer, default=0)
    lucky = db.Column(db.Integer, default=0)
    duration_sec = db.Column(db.Integer)
    timed = db.Column(db.Boolean, default=True)
    finished_at = db.Column(db.DateTime, default=_utcnow, index=True)
    payload_json = db.Column(db.Text)
    user = db.relationship('User', foreign_keys=[user_id])


class PulseNeetCard(db.Model):
    """Spaced reinforcement for NEET: one card per question missed or answered with low confidence. `qkey` is a bank id. Leitner boxes 0 to 5 (0, 1, 3, 7, 14, 30 days)."""
    __tablename__ = 'pulse_neet_cards'
    __table_args__ = (db.UniqueConstraint('user_id', 'qkey', name='uq_neet_card'),)
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), index=True, nullable=False)
    qkey = db.Column(db.String(48), nullable=False)
    sec = db.Column(db.String(4))
    topic = db.Column(db.String(120))
    box = db.Column(db.Integer, default=0)
    due = db.Column(db.Date, index=True)
    seen = db.Column(db.Integer, default=0)
    right_run = db.Column(db.Integer, default=0)
    last_right = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime, default=_utcnow)
    updated_at = db.Column(db.DateTime, default=_utcnow)


class PulseSatResult(db.Model):
    """One finished EduPulse-SAT test: a full practice SAT, a section half, a domain set or a Daily Review. One mark for each right answer, no negative marking.
    `payload_json` keeps one row per question: id, section, domain, skill, chosen option (or typed response), right or wrong, confidence (G/L/M/H) and seconds."""
    __tablename__ = 'pulse_sat_results'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), index=True, nullable=False)
    mock = db.Column(db.String(24), index=True)                  # M-FULL, M-RW, M-MATH, S-ALG, DAILY ...
    title = db.Column(db.String(140))
    score = db.Column(db.Float, default=0)
    max_score = db.Column(db.Float, default=0)
    right = db.Column(db.Integer, default=0)
    wrong = db.Column(db.Integer, default=0)
    blank = db.Column(db.Integer, default=0)
    rated = db.Column(db.Integer, default=0)
    sure_wrong = db.Column(db.Integer, default=0)
    lucky = db.Column(db.Integer, default=0)
    duration_sec = db.Column(db.Integer)
    timed = db.Column(db.Boolean, default=True)
    finished_at = db.Column(db.DateTime, default=_utcnow, index=True)
    payload_json = db.Column(db.Text)
    user = db.relationship('User', foreign_keys=[user_id])


class PulseSatCard(db.Model):
    """Spaced reinforcement for the SAT: one card per question missed or answered with low confidence. `qkey` is a bank id, or 'g:<family>' for a generated Math question
    (which returns with new numbers). Leitner boxes 0 to 5 (0, 1, 3, 7, 14, 30 days)."""
    __tablename__ = 'pulse_sat_cards'
    __table_args__ = (db.UniqueConstraint('user_id', 'qkey', name='uq_sat_card'),)
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), index=True, nullable=False)
    qkey = db.Column(db.String(48), nullable=False)
    sec = db.Column(db.String(6))
    topic = db.Column(db.String(120))
    box = db.Column(db.Integer, default=0)
    due = db.Column(db.Date, index=True)
    seen = db.Column(db.Integer, default=0)
    right_run = db.Column(db.Integer, default=0)
    last_right = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime, default=_utcnow)
    updated_at = db.Column(db.DateTime, default=_utcnow)
