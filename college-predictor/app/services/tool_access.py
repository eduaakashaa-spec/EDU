"""Per-member and per-mentor tool access, set by an admin (Admin -> Users -> Tool access).

The tier rules stay the default: Premium opens the premium tools, Elite adds the mentorship portal, staff open their own tools. An admin can then make an
exception for one person and one tool:
  allow : open a premium tool for someone without it, or the mentorship portal for a member who is not Elite
  deny  : switch a tool off for someone who would normally have it
Tools are the Member Home tiles (the key is the tile slug). The decorators in app/decorators.py and the mentorship portal ask this module; admins are never restricted.
Allow exceptions only widen the premium tools and the mentorship portal; they never open staff-only screens to someone outside the team.
"""
from flask import g, request

from app.extensions import db
from app.models_membership import UserToolAccess
from app.services import member_hub as mh

MENTORSHIP_KEY = 'my-mentorship'


def tools():
    """Tools an admin can control: every Member Home tile gated by a membership or by staff access."""
    out, seen = [], set()
    for cat in mh.CATEGORIES:
        for t in cat['tiles']:
            if t.get('access') not in ('premium', 'elite'):
                continue
            key = mh.slugify(t['title'])
            if key in seen:
                continue
            seen.add(key)
            out.append({'key': key, 'title': t['title'], 'category': cat['title'], 'endpoint': t.get('endpoint', ''), 'staff': bool(t.get('staff')),
                        'access': t['access'], 'desc': t.get('desc', '')})
    return out


def keys():
    return {t['key'] for t in tools()}


def _overrides(user):
    """{tool_key: mode} for this user, read once per request."""
    if not getattr(user, 'id', None):
        return {}
    cache = g.__dict__.setdefault('_tool_access', {})
    if user.id not in cache:
        cache[user.id] = {r.tool_key: r.mode for r in UserToolAccess.query.filter_by(user_id=user.id).all()}
    return cache[user.id]


def mode_for(user, key):
    """'allow', 'deny' or None (follow the tier). Admins are never restricted."""
    if getattr(user, 'is_admin', False):
        return None
    return _overrides(user).get(key)


def _tile_for_endpoint(endpoint, staff_gate):
    """The tool a page belongs to: the tile with that exact endpoint, else the first tile of the same blueprint with the same member/staff side."""
    if not endpoint:
        return None
    blueprint = endpoint.split('.')[0]
    exact = fallback = None
    for cat in mh.CATEGORIES:
        for t in cat['tiles']:
            ep = t.get('endpoint') or ''
            if ep == endpoint and exact is None:
                exact = t
            if ep.split('.')[0] == blueprint and bool(t.get('staff')) == staff_gate and fallback is None and t.get('access') in ('premium', 'elite'):
                fallback = t
    t = exact or fallback
    return mh.slugify(t['title']) if t else None


def request_mode(user, staff_gate=False):
    """The exception that applies to the page being served, or None."""
    try:
        key = _tile_for_endpoint(request.endpoint, staff_gate)
    except RuntimeError:                       # no request context
        return None
    return mode_for(user, key) if key else None


def can_open(user, tile):
    """Member Home: is this tile open for this user (tier rule first, then the admin's exception)?"""
    key = mh.slugify(tile['title'])
    mode = mode_for(user, key)
    if mode == 'deny':
        return False
    if tile.get('access') == 'elite':
        return bool(user.is_elite) or mode == 'allow'
    if tile.get('access') == 'premium':
        return bool(user.is_premium) or (mode == 'allow' and not tile.get('staff'))
    return True


def has_mentorship(user):
    """The mentorship portal (workspace, weekly plan, KPIs, reviews): Elite members and staff; a premium member only with an admin 'allow'."""
    mode = mode_for(user, MENTORSHIP_KEY)
    if mode == 'deny':
        return False
    return bool(user.is_elite) or mode == 'allow'


def save(user, modes, admin_email=''):
    """Replace this user's exceptions with {tool_key: 'allow'|'deny'} (anything else = default). Returns the number of exceptions kept."""
    team = {t['key'] for t in tools() if t['staff']}
    clean = {k: v for k, v in modes.items() if k in keys() and v in ('allow', 'deny') and not (v == 'allow' and k in team)}   # allow never opens a team-only tool
    UserToolAccess.query.filter_by(user_id=user.id).delete()
    for k, v in clean.items():
        db.session.add(UserToolAccess(user_id=user.id, tool_key=k, mode=v, updated_by=admin_email[:200]))
    db.session.commit()
    g.__dict__.get('_tool_access', {}).pop(user.id, None)
    return len(clean)


def explain(user, tile):
    """(open?, plain-language reason) for one Member Home tile and one person: the tier rule first, then any admin exception. Used by Admin -> Members -> Diagnose."""
    key = mh.slugify(tile['title'])
    mode = mode_for(user, key)
    access = tile.get('access')
    if access == 'soon':
        return False, 'Coming soon'
    if tile.get('staff') and not user.is_staff:
        return False, 'Team tool: hidden for this account (needs the EA mentor or admin plan)'
    if mode == 'deny':
        return False, 'Blocked by an admin exception (Tool access)'
    if access == 'elite':
        if user.is_elite:
            return True, 'Open: Elite plan' if user.tier == 'elite' else 'Open: team account'
        if mode == 'allow':
            return True, 'Open: admin exception (allow)'
        return False, 'Locked: needs Elite Mentorship (plan is %s)' % _plan(user)
    if access == 'premium':
        if user.is_premium:
            return True, 'Open: %s' % ('Premium or Elite plan' if user.tier in ('premium', 'elite') else 'team account')
        if mode == 'allow' and not tile.get('staff'):
            return True, 'Open: admin exception (allow)'
        return False, 'Locked: needs Premium (plan is %s)' % _plan(user)
    return True, 'Open: any signed-in member'


def _plan(user):
    if user.tier in ('premium', 'elite') and user.tier_expires_at:
        return '%s, expired on %s' % (user.tier, user.tier_expires_at.strftime('%d %b %Y'))
    return user.tier
