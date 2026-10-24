"""Save a member's WhatsApp group details (staff only; mentors only for their own members)."""
from flask import Blueprint, abort, flash, redirect, request
from flask_login import current_user, login_required

from app.decorators import safe_next
from app.services import wagroup as wg

wagroup_bp = Blueprint('wagroup', __name__, url_prefix='/wagroup')


@wagroup_bp.route('/<int:user_id>', methods=['POST'])
@login_required
def save(user_id):
    if not wg.can_manage(user_id):
        abort(403)
    link, err = wg.clean_link(request.form.get('invite_link'))
    if err:
        flash(err, 'danger')
    else:
        wg.save(user_id, request.form.get('group_name'), link, request.form.get('note'), current_user.id)
        flash('WhatsApp group details saved.', 'success')
    return redirect(safe_next(request.form.get('next')) or '/')
