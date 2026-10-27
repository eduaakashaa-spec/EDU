"""Smart Study Planner tables (new tables only; created by db.create_all)."""
from datetime import datetime, timezone

from app.extensions import db


def _now():
    return datetime.now(timezone.utc).replace(tzinfo=None)


class SpPlan(db.Model):
    """One study plan for one student. `level` is beginner | average | top; `exam` is JEE | UCEED | NEET."""
    __tablename__ = 'sp_plans'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), index=True, nullable=False)
    mentor_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), index=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'))
    title = db.Column(db.String(160), nullable=False)
    exam = db.Column(db.String(12), nullable=False)
    level = db.Column(db.String(10), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    weeks = db.Column(db.Integer, default=8)
    exam_date = db.Column(db.Date)
    hours_per_day = db.Column(db.Float, default=3)
    focus_json = db.Column(db.Text)                               # optional: chapters the student wants to stress
    status = db.Column(db.String(10), default='active', index=True)   # active | archived
    created_at = db.Column(db.DateTime, default=_now)
    user = db.relationship('User', foreign_keys=[user_id])
    mentor = db.relationship('User', foreign_keys=[mentor_id])
    tasks = db.relationship('SpTask', backref='plan', lazy='dynamic', cascade='all, delete-orphan')


class SpTask(db.Model):
    """One planned item on one day. status: todo | done | skipped. link_kind: reinforce | pulse | jee_mock | uceed_mock | None."""
    __tablename__ = 'sp_tasks'
    id = db.Column(db.Integer, primary_key=True)
    plan_id = db.Column(db.Integer, db.ForeignKey('sp_plans.id', ondelete='CASCADE'), index=True, nullable=False)
    day = db.Column(db.Date, index=True, nullable=False)
    subject = db.Column(db.String(40))
    chapter = db.Column(db.String(120))
    task_type = db.Column(db.String(10), nullable=False)          # learn | practice | revise | mock | error | rest
    title = db.Column(db.String(200), nullable=False)
    minutes = db.Column(db.Integer, default=30)
    minutes_done = db.Column(db.Integer, default=0)
    status = db.Column(db.String(8), default='todo', index=True)
    link_kind = db.Column(db.String(12))
    note = db.Column(db.String(300))
    done_at = db.Column(db.DateTime)
    added_by = db.Column(db.String(10), default='plan')           # plan | student | mentor | suggestion
