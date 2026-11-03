"""EduPulse-NIFT: GAT mocks, previous-year practice and spaced reinforcement for NIFT, plus CAT / studio practice.

Student (Premium member):  /nift-mock/                 centre: GAT mocks per programme, previous-year papers, section sets, Daily Review, progress, studio
                           /nift-mock/test/<id>        the test page (questions without answers); id is M-<prog>, S-<section> or Y-<year>-<prog>
                           /nift-mock/daily            Daily Review: due review cards plus new questions from the weakest sections
                           /nift-mock/submit/<id>      POST: a finished attempt, marked on the server (+1 right, -0.25 wrong)
                           /nift-mock/result/<id>      report with the key and explanations: the student, their mentor, or an admin
                           /nift-mock/progress         tracker: section levels, mock trend, review boxes, streak and badges
                           /nift-mock/student/<uid>    the same tracker for a mentor or admin
                           /nift-mock/studio           CAT / studio tasks from the previous papers, self-marked against a rubric
"""
import json

from flask import Blueprint, abort, flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.decorators import premium_required
from app.extensions import db
from app.models_pulse import PulseNiftResult, PulseNiftStudio, PulseProfile
from app.routes.pulse import _ensure_profile
from app.services import nift

nift_bp = Blueprint('nift_mock', __name__, url_prefix='/nift-mock')


def _can_see(r):
    if r.user_id == current_user.id or current_user.is_admin:
        return True
    prof = db.session.get(PulseProfile, r.user_id)
    return bool(current_user.is_staff and prof and prof.mentor_id == current_user.id)


@nift_bp.route('/')
@premium_required
def home():
    done = {}
    for r in nift.for_user(current_user.id):
        done.setdefault(r.mock, r)
    cat = nift.catalogue()
    return render_template('pulse/nift.html', mocks=[t for t in cat if t['kind'] == 'mock'], sets=[t for t in cat if t['kind'] == 'set'], years=[t for t in cat if t['kind'] == 'year'], done=done,
                           tr=nift.tracker(current_user.id), SEC=nift.SEC, PROGS=nift.PROGS, studio=nift.studio(), ana=nift.analysis())


def _take(t, timed):
    return render_template('pulse/nift_take.html', t=t, paper=nift.paper_for_browser(t['qids']), CONF=nift.CONF, timed=timed)


@nift_bp.route('/test/<tid>')
@premium_required
def take(tid):
    n = PulseNiftResult.query.filter_by(user_id=current_user.id, mock=tid).count()
    t = nift.compose(tid, current_user.id, n) or abort(404)
    return _take(t, request.args.get('mode') != 'practice')


@nift_bp.route('/daily')
@premium_required
def daily():
    return _take(nift.daily(current_user.id), False)


@nift_bp.route('/submit/<tid>', methods=['POST'])
@premium_required
def submit(tid):
    if (request.content_length or 0) > nift.MAX_BODY:
        return jsonify(ok=False, error='too large'), 413
    known = {x['id']: x for x in nift.catalogue()}
    if tid == 'DAILY':
        t = {'id': 'DAILY', 'title': 'Daily Review'}
    elif tid in known:
        t = known[tid]
    else:
        abort(404)
    _ensure_profile()
    r, err = nift.save_result(current_user.id, t, request.get_json(silent=True))
    if err:
        return jsonify(ok=False, error=err), 400
    return jsonify(ok=True, id=r.id, url=url_for('nift_mock.report', rid=r.id))


@nift_bp.route('/result/<int:rid>')
@login_required
def report(rid):
    r = db.session.get(PulseNiftResult, rid) or abort(404)
    if not _can_see(r):
        abort(404)
    own = r.user_id == current_user.id
    return render_template('pulse/nift_report.html', r=r, an=nift.analyse([r]), review=nift.review(r), CONF_LABEL=nift.CONF_LABEL, LETTERS=nift.LETTERS, own=own,
                           due=nift.tracker(current_user.id)['due'] if own else 0, WRONG=nift.WRONG)


@nift_bp.route('/progress')
@premium_required
def progress():
    return render_template('pulse/nift_progress.html', tr=nift.tracker(current_user.id), SEC=nift.SEC, student=current_user, own=True)


@nift_bp.route('/student/<int:uid>')
@login_required
def student_progress(uid):
    from app.models import User
    prof = db.session.get(PulseProfile, uid)
    if not (current_user.is_admin or (current_user.is_staff and prof and prof.mentor_id == current_user.id)):
        abort(404)
    u = db.session.get(User, uid) or abort(404)
    return render_template('pulse/nift_progress.html', tr=nift.tracker(uid), SEC=nift.SEC, student=u, own=False)


@nift_bp.route('/studio')
@premium_required
def studio():
    done = {c.tid: c for c in PulseNiftStudio.query.filter_by(user_id=current_user.id).all()}
    return render_template('pulse/nift_studio.html', items=nift.studio(), done=done)


@nift_bp.route('/studio/<tid>', methods=['GET', 'POST'])
@premium_required
def studio_task(tid):
    c = next((x for x in nift.studio() if x['id'] == tid), None) or abort(404)
    if request.method == 'POST':
        try:
            scores = [int(request.form.get('s%d' % i, '')) for i in range(len(c['rubric']))]
        except ValueError:
            scores = None
        if scores is None or not nift.save_studio(current_user.id, tid, scores, request.form.get('note', '')):
            flash('Please mark every line within its marks.', 'error')
        else:
            flash('Saved. Show your work to your mentor.', 'ok')
        return redirect(url_for('nift_mock.studio_task', tid=tid))
    row = PulseNiftStudio.query.filter_by(user_id=current_user.id, tid=tid).first()
    return render_template('pulse/nift_task.html', c=c, row=row, vals=json.loads(row.scores_json) if row else None, items=nift.studio())
