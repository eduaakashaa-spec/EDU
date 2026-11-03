"""EduPulse free sample mock tests (public): phone and email once, then one 10-question sample for each exam.

    GET  /edupulse-free-mock-tests/           the form (first visit) or the six samples
    POST /edupulse-free-mock-tests/start      phone + email (+ name) -> unlocks the samples for this browser
    GET  /edupulse-free-mock-tests/<exam>     the sample test
    POST /edupulse-free-mock-tests/<exam>     finish: score and review
Each unlock and each finished sample is saved as a lead (source 'edupulse-free-mock'), so the team can follow up.
"""
import json
import re

from flask import Blueprint, abort, flash, redirect, render_template, request, session, url_for

from app.extensions import db
from app.models import PageLead
from app.services import free_mock as fm

free_mock_bp = Blueprint('free_mock', __name__, url_prefix='/edupulse-free-mock-tests')
_EMAIL = re.compile(r'^[^@\s]+@[^@\s]+\.[^@\s]+$')
SRC = 'edupulse-free-mock'


def _unlocked():
    return bool(session.get('fm_email'))


@free_mock_bp.route('/')
def home():
    return render_template('free_mock.html', exams=fm.EXAMS, unlocked=_unlocked(), done=session.get('fm_done') or {}, name=session.get('fm_name', ''),
                           form={}, SIZE=fm.SIZE)


@free_mock_bp.route('/start', methods=['POST'])
def start():
    if (request.form.get('website') or '').strip():                       # honeypot: bots fill every field
        return redirect(url_for('free_mock.home'))
    name = (request.form.get('name') or '').strip()[:150]
    email = (request.form.get('email') or '').strip().lower()[:200]
    phone = re.sub(r'[\s\-().]', '', (request.form.get('phone') or '').strip())[:40]
    err = None
    if not _EMAIL.match(email):
        err = 'Please enter a valid email address.'
    elif not re.fullmatch(r'\+?\d{8,15}', phone):
        err = 'Please enter a valid phone number (8 to 15 digits, with country code if outside India).'
    if err:
        return render_template('free_mock.html', exams=fm.EXAMS, unlocked=False, done={}, name='', form={'name': name, 'email': email, 'phone': phone}, error=err,
                               SIZE=fm.SIZE), 400
    db.session.add(PageLead(source=SRC, name=name, email=email, phone=phone, payload_json=json.dumps({'event': 'unlock'})))
    db.session.commit()
    session['fm_email'], session['fm_name'], session['fm_done'] = email, name, session.get('fm_done') or {}
    return redirect(url_for('free_mock.home') + '#samples')


def _exam(key):
    ex = fm.BY_KEY.get(key)
    if ex is None:
        abort(404)
    return ex


@free_mock_bp.route('/<key>', methods=['GET', 'POST'])
def take(key):
    ex = _exam(key)
    if not _unlocked():
        flash('Enter your phone and email to try the free sample tests.', 'info')
        return redirect(url_for('free_mock.home'))
    if request.method == 'GET':
        return render_template('free_mock_take.html', ex=ex, qs=fm.public_view(key))
    answers = {k[2:]: v for k, v in request.form.items() if k.startswith('a_')}
    res = fm.grade(key, answers)
    done = dict(session.get('fm_done') or {})
    done[key] = '%d/%d' % (res['right'], res['total'])
    session['fm_done'] = done
    db.session.add(PageLead(source=SRC, name=session.get('fm_name'), email=session.get('fm_email'), phone=None,
                            payload_json=json.dumps({'event': 'finished', 'exam': ex['name'], 'right': res['right'], 'wrong': res['wrong'], 'blank': res['blank']})))
    db.session.commit()
    nxt = [e for e in fm.EXAMS if e['key'] not in done]
    return render_template('free_mock_result.html', ex=ex, res=res, nxt=nxt)
