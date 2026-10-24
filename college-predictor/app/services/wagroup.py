"""WhatsApp group details per member and the permission rule for editing them."""
import re

from flask_login import current_user

from app.extensions import db
from app.models_mentorship import MemberWaGroup, MsEnrolment

_LINK = re.compile(r'^https://chat\.whatsapp\.com/[A-Za-z0-9_-]{8,40}/?$')


def get(user_id):
    return MemberWaGroup.query.filter_by(user_id=user_id).first()


def clean_link(raw):
    """Return (link, error). Only official invite links are stored, so a mistyped or malicious URL never becomes a button."""
    raw = (raw or '').strip()
    if not raw:
        return '', None
    if raw.startswith('chat.whatsapp.com/'):
        raw = 'https://' + raw
    if raw.startswith('http://chat.whatsapp.com/'):
        raw = 'https://' + raw[7:]
    return (raw, None) if _LINK.match(raw) else ('', 'Use the group invite link, which looks like https://chat.whatsapp.com/XXXXXXXX')


def can_manage(user_id, user=None):
    """Admin: any member. Staff mentor: only members they mentor (mentorship portal or FutureReady)."""
    user = user or current_user
    if not user or not user.is_authenticated:
        return False
    if user.is_admin:
        return True
    if not user.is_ea_mentor:
        return False
    if MsEnrolment.query.filter_by(student_id=user_id, mentor_id=user.id).first():
        return True
    try:
        from app.futureready.models import FrProfile
        return bool(FrProfile.query.filter_by(user_id=user_id, mentor_id=user.id).first())
    except Exception:
        return False


def save(user_id, name, link, note, by):
    g = get(user_id) or MemberWaGroup(user_id=user_id)
    g.group_name = (name or '').strip()[:120]
    g.invite_link = link
    g.note = (note or '').strip()[:300]
    g.updated_by = by
    db.session.add(g)
    db.session.commit()
    return g
