"""Entrance-exam qualification and subject equivalency checker (public): /entrance-equivalency/.
The profile is read from the query string so a result can be shared or bookmarked."""
from flask import Blueprint, abort, render_template, request

from app.data import equivalency as D
from app.services import equivalency as eq

equivalency_bp = Blueprint('equivalency', __name__, url_prefix='/entrance-equivalency')


@equivalency_bp.route('/', endpoint='hub')
def hub():
    qual = request.args.get('qual', '')
    subjects = [s for s in request.args.getlist('sub') if s in D.SUBJECTS]
    group = request.args.get('group', '')
    if group and group not in dict(D.GROUPS):
        group = ''
    results = eq.check(qual, subjects, group or None) if qual in dict(D.QUALS) else None
    return render_template('equivalency.html', results=results, sel_qual=qual, sel_sub=subjects, sel_group=group, **eq.context())


@equivalency_bp.route('/<exam_id>', endpoint='exam')
def exam(exam_id):
    e = eq.exam(exam_id)
    if e is None:
        abort(404)
    return render_template('equivalency_exam.html', e=e, **eq.context())
