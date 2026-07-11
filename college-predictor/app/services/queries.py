"""Conditional-aggregate helpers for admin stat queries.

The admin DB is remote Postgres (Neon), so each query is a full network round
trip — the latency of N separate COUNT queries dwarfs their execution time.
These helpers build `COUNT(CASE WHEN … THEN 1 END)` / `SUM(CASE WHEN …)`
expressions so a whole KPI block collapses into one SELECT.

Usage:
    total, active = db.session.query(
        db.func.count(Model.id), count_if(Model.status == 'Active')).one()
"""
from app.extensions import db


def count_if(cond):
    """COUNT(CASE WHEN cond THEN 1 END) — rows matching cond."""
    return db.func.count(db.case((cond, 1)))


def sum_if(col, cond):
    """COALESCE(SUM(CASE WHEN cond THEN col ELSE 0 END), 0)."""
    return db.func.coalesce(db.func.sum(db.case((cond, col), else_=0)), 0)
