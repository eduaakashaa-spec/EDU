"""Portal guide: step-by-step instructions per role (content lives in app/services/portal_guide.py)."""
from flask import Blueprint, render_template, request, url_for
from flask_login import current_user, login_required

from app.services import member_hub
from app.services import portal_guide as pg

portal_guide_bp = Blueprint('portal_guide', __name__, url_prefix='/portal-guide')


def _resolve(entries):
    """Copy each entry with its `where` endpoints turned into links; an endpoint that no longer exists is simply left out."""
    out = []
    for e in entries:
        links = []
        for label, endpoint in e.get('where', []):
            try:
                links.append((label, url_for(endpoint)))
            except Exception:
                continue
        out.append(dict(e, links=links))
    return out


@portal_guide_bp.route('/')
@login_required
def index():
    roles = pg.roles_visible(current_user)
    role = request.args.get('role')
    if role not in roles:
        role = 'admin' if 'admin' in roles else ('mentor' if 'mentor' in roles else 'student')
    return render_template('portal_guide.html', roles=roles, role=role, entries=_resolve(pg.entries_for(role)), everyone=_resolve(pg.entries_for('all')), pg=pg, is_new=pg.is_new,
                           missing=sorted({t['title'] for c in member_hub.CATEGORIES for t in c['tiles'] if t.get('endpoint')} - pg.covered_tiles()) if current_user.is_admin else [])
