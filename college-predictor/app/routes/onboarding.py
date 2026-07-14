"""Membership onboarding assessment — public form + admin dossier tooling.

Public:
    GET  /onboarding-assessment            — landing: intro + choose student/parent
    GET  /onboarding-assessment/<role>     — the mobile stepper form
    POST /onboarding-assessment/<role>     — save one half (student or parent)

Admin (admin tier):
    GET  /admin/onboarding                 — submissions grouped into families
    GET  /admin/onboarding/<id>            — one submission + paired half + copy-for-AI

Answers are stored keyed by item id (S1…/P1…) so the AI rubric in
ONBOARDING_ASSESSMENT.md runs verbatim on a stored pair.
"""
import json
import os
import re
import threading
import time

from flask import (Blueprint, Response, abort, current_app, flash, redirect,
                   render_template, request, url_for)
from flask_login import current_user, login_required

from app.decorators import admin_required
from app.extensions import db
from app.models import OnboardingResponse
from app.services.mailer import send_async
from app.services.onboarding_assessment import (ANSWER_KEY, ROLES, intro_for,
                                                items_for, modules_for)

onboarding_bp = Blueprint('onboarding', __name__)

# simple in-memory rate limit (mirrors survey.py): 5 submissions / 10 min / IP
_RATE_LOCK = threading.Lock()
_RATE_HITS = {}
RATE_WINDOW = 600
RATE_MAX = 5


def _client_ip():
    fwd = request.headers.get('X-Forwarded-For', '')
    return (fwd.split(',')[0].strip() if fwd else request.remote_addr) or '?'


def _rate_ok(ip):
    now = time.time()
    with _RATE_LOCK:
        hits = [t for t in _RATE_HITS.get(ip, []) if now - t < RATE_WINDOW]
        if len(hits) >= RATE_MAX:
            _RATE_HITS[ip] = hits
            return False
        hits.append(now)
        _RATE_HITS[ip] = hits
        return True


def _family_key(student_name, phone, email):
    """Pair a student and parent submission. Both halves are filled from the same
    logged-in family account, so the account id IS the link — no name/phone
    guessing. The old name+contact key stays as the fallback for the handful of
    rows written before the login gate (and for any future public route)."""
    if current_user.is_authenticated:
        return 'user:%d' % current_user.id
    name = ''.join((student_name or '').lower().split())
    digits = ''.join(c for c in (phone or '') if c.isdigit())[-10:]
    tail = digits or (email or '').strip().lower()
    return (name + '|' + tail)[:240]


# --------------------------------------------------------------------------- #
# public
# --------------------------------------------------------------------------- #
@onboarding_bp.route('/onboarding-assessment')
def landing():
    return render_template('onboarding_landing.html')


@onboarding_bp.route('/onboarding-assessment/<role>', methods=['GET', 'POST'])
@login_required
def assessment(role):
    """Login-gated on purpose: the student's and the parent's halves are paired on
    the account they both sign in with, so one family = one account."""
    if role not in ROLES:
        abort(404)

    if request.method == 'POST':
        return _save(role)

    return render_template('onboarding_assessment.html', role=role,
                           modules=modules_for(role), intro=intro_for(role),
                           total=len(items_for(role)))


def _save(role):
    f = request.form
    student_name = (f.get('student_name') or '').strip()
    respondent_name = (f.get('respondent_name') or '').strip()
    email = current_user.email          # the account is the family; don't re-ask
    phone = (f.get('phone') or '').strip()

    def reshow(msg):
        flash(msg, 'error')
        return render_template('onboarding_assessment.html', role=role,
                               modules=modules_for(role), intro=intro_for(role),
                               total=len(items_for(role)), form=f), 400

    if not student_name:
        return reshow("Please enter the student's name.")
    if not _rate_ok(_client_ip()):
        flash('Too many submissions from your network. Please try again later.', 'error')
        return render_template('onboarding_assessment.html', role=role,
                               modules=modules_for(role), intro=intro_for(role),
                               total=len(items_for(role)), form=f), 429

    # Collect every item's answer, keyed by item id, straight from the form.
    # Items run in bank order, so a `when` gate always sees the answer it depends
    # on; anything the student couldn't have been shown is dropped, not stored.
    responses = {}
    for it in items_for(role):
        if not _when_met(it, responses):
            continue
        val = _read_answer(it, f)
        if val not in (None, '', {}, []):
            responses[it['id']] = val

    sub = OnboardingResponse(
        role=role,
        family_key=_family_key(student_name, phone, email),
        student_name=student_name[:150],
        respondent_name=respondent_name[:150] or (student_name[:150] if role == 'student' else ''),
        email=email.lower()[:200],
        phone=phone[:40],
        responses_json=json.dumps(responses, ensure_ascii=False) if responses else None)
    db.session.add(sub)
    db.session.commit()

    _send_confirmation(sub)  # best-effort; no-op if SMTP isn't configured
    return redirect(url_for('onboarding.assessment', role=role, done=1) + '#top')


# --------------------------------------------------------------------------- #
# confirmation email (fired on submit; needs SMTP configured — see mailer.py)
# --------------------------------------------------------------------------- #
def _brand_shell(body_html):
    """Kept as a thin alias so this module's callers don't change — every email
    now renders through the single shared shell (see email_templates)."""
    from app.services.email_templates import branded_shell
    return branded_shell(body_html)


def _send_confirmation(sub):
    first = (sub.respondent_name or sub.student_name or 'there').split(' ')[0]
    if sub.role == 'student':
        subject = "We've got your answers, %s — thank you!" % first
        text = ("Hi %s,\n\nThanks for completing your EduAakashaa onboarding assessment. "
                "Your counsellor now has your answers and will use them to prepare for your "
                "first 1-on-1 — so the session is about you, not generic advice.\n\n"
                "If your parent hasn't filled their short version yet, please share the link "
                "with them.\n\n— Team EduAakashaa") % first
        extra = ("<p>If your parent hasn't filled their short version yet, please share the "
                 "link with them.</p>")
    else:
        subject = "Thank you — your parent questionnaire is in"
        text = ("Dear %s,\n\nThank you for completing the parent questionnaire for %s. "
                "Your counsellor will combine your answers with the student's to make the first "
                "session genuinely useful.\n\nWe'll be in touch shortly to schedule your "
                "1-on-1.\n\n— Team EduAakashaa") % (first, sub.student_name or 'your child')
        extra = ("<p>We'll be in touch shortly to schedule your 1-on-1.</p>")
    html = _brand_shell(
        "<p>Hi %s,</p><p>Thanks for completing your EduAakashaa onboarding assessment. "
        "Your counsellor now has your answers and will use them to prepare for your first "
        "1-on-1.</p>%s" % (first, extra))
    send_async(sub.email, subject, text, html)


def _read_answer(it, f):
    """Pull one item's answer out of the submitted form into a JSON-able value.
    Field naming: base id for simple types, id + '__' + suffix for compound ones."""
    t = it['type']
    iid = it['id']
    g = lambda k='': (f.get(iid + (('__' + k) if k else '')) or '').strip()

    if t in ('choice', 'sjt', 'open'):
        if t == 'open':
            return g() or None
        if t == 'choice':
            base = g()
            if it.get('other') and base == 'Something else':
                extra = g('other')
                return ('Something else: ' + extra) if extra else base
            return base or None
        # sjt: choice + why
        choice, why = g('choice'), g('why')
        if not choice and not why:
            return None
        return {'choice': choice, 'why': why}

    if t == 'likert':
        v = g()
        return int(v) if v.isdigit() else None

    if t == 'num':
        out = {}
        for lab in it['fields']:
            v = g(_slug(lab))
            out[lab] = v
        return out if any(v for v in out.values()) else None

    if t == 'choice_multi':
        out = {}
        for row in it['rows']:
            v = g(_slug(row))
            if v:
                out[row] = v
        return out or None

    if t == 'likert_multi':
        out = {}
        for row in it['rows']:
            v = g(_slug(row))
            if v.isdigit():
                out[row] = int(v)
        return out or None

    if t == 'mostleast':
        most, least = g('most'), g('least')
        if not most and not least:
            return None
        return {'most': most, 'least': least}

    if t == 'pick':
        picked = [o for o in it['options'] if f.get(iid + '__' + _slug(o))]
        return picked or None

    if t == 'rank':
        # each option carries a 1..N rank select; return options ordered best-first
        ranked = []
        for o in it['options']:
            v = g(_slug(o))
            if v.isdigit():
                ranked.append((int(v), o))
        if not ranked:
            return None
        ordered = [o for _, o in sorted(ranked)]
        if it.get('other'):
            extra = g('other')
            if extra:
                ordered = [(x + ' (' + extra + ')') if x == 'Something else' else x
                           for x in ordered]
        return ordered

    if t == 'choice_pair':
        out = {}
        for grp in it['groups']:
            v = g(grp['key'])
            if v:
                out[grp['key']] = v
        return out or None

    return None


def _when_met(it, answers):
    """True when a conditional item's gate is satisfied by the given answers.
    `when` is {earlier_item_id: required_answer} — see _mcq in the question bank."""
    return all(answers.get(k) == v for k, v in (it.get('when') or {}).items())


def _slug(label):
    """Stable, form-safe suffix for a row/option label."""
    return ''.join(c if c.isalnum() else '_' for c in label)[:60]


@onboarding_bp.app_template_filter('oa_slug')
def _oa_slug(label):
    """Template-side twin of _slug so form field names match the reader exactly."""
    return _slug(label or '')


# --------------------------------------------------------------------------- #
# admin
# --------------------------------------------------------------------------- #
@onboarding_bp.route('/admin/onboarding')
@admin_required
def admin_list():
    q = (request.args.get('q') or '').strip()
    query = OnboardingResponse.query
    if q:
        like = f'%{q}%'
        query = query.filter(db.or_(
            OnboardingResponse.student_name.ilike(like),
            OnboardingResponse.respondent_name.ilike(like),
            OnboardingResponse.email.ilike(like)))
    rows = query.order_by(OnboardingResponse.created_at.desc()).all()

    # group into families by family_key; newest activity first
    fams = {}
    for r in rows:
        fam = fams.setdefault(r.family_key or ('id-%d' % r.id),
                              {'student': None, 'parent': None,
                               'name': r.student_name or '—', 'last': r.created_at})
        if fam[r.role] is None:          # keep the newest of each role
            fam[r.role] = r
        if r.created_at and (fam['last'] is None or r.created_at > fam['last']):
            fam['last'] = r.created_at
    families = sorted(fams.values(),
                      key=lambda x: x['last'] or 0, reverse=True)

    total, students, parents = 0, 0, 0
    for f in families:
        if f['student']:
            students += 1
        if f['parent']:
            parents += 1
    total = len(families)
    stats = {'families': total, 'students': students, 'parents': parents,
             'complete': sum(1 for f in families if f['student'] and f['parent'])}
    return render_template('admin/onboarding_list.html', admin_tab='onboarding',
                           families=families, stats=stats, q=q)


def _student_parent(sub):
    """Return (student, parent) records for sub's family (the newest opposite half)."""
    other = 'parent' if sub.role == 'student' else 'student'
    pair = (OnboardingResponse.query
            .filter_by(family_key=sub.family_key, role=other)
            .order_by(OnboardingResponse.created_at.desc()).first()
            if sub.family_key else None)
    return (sub if sub.role == 'student' else pair,
            sub if sub.role == 'parent' else pair)


@onboarding_bp.route('/admin/onboarding/<int:sub_id>')
@admin_required
def admin_detail(sub_id):
    sub = db.session.get(OnboardingResponse, sub_id) or abort(404)
    student, parent = _student_parent(sub)
    return render_template('admin/onboarding_detail.html', admin_tab='onboarding',
                           sub=sub, student=student, parent=parent,
                           modules_for=modules_for, ai_bundle=_ai_bundle(student, parent))


def _rubric_text():
    """The AI Analysis Rubric + Insight Dossier template (Deliverables 2 & 3),
    read from the design doc so the downloaded file is self-contained for the AI."""
    path = os.path.join(current_app.root_path, os.pardir, 'ONBOARDING_ASSESSMENT.md')
    try:
        md = open(path, encoding='utf-8').read()
    except OSError:
        return ''
    i = md.find('# DELIVERABLE 2')
    return md[i:].strip() if i >= 0 else ''


@onboarding_bp.route('/admin/onboarding/<int:sub_id>/download')
@admin_required
def admin_download(sub_id):
    sub = db.session.get(OnboardingResponse, sub_id) or abort(404)
    student, parent = _student_parent(sub)
    rubric = _rubric_text()
    parts = [_ai_bundle(student, parent)]
    if rubric:
        parts += ['\n\n' + '=' * 70,
                  'RUBRIC & DOSSIER TEMPLATE (apply these to the answers above)',
                  '=' * 70 + '\n', rubric]
    body = '\n'.join(parts)
    slug = re.sub(r'[^A-Za-z0-9]+', '_', (sub.student_name or 'family')).strip('_') or 'family'
    return Response(body, mimetype='text/markdown',
                    headers={'Content-Disposition':
                             'attachment; filename=onboarding_%s.md' % slug})


def _ai_bundle(student, parent):
    """The exact text the consultant pastes into an AI: a pointer to the rubric,
    plus both halves rendered as `item_id [tag] question → answer`. Confidential
    items (S50/P34) are included ONLY for the counsellor — the rubric keeps them
    out of the family-facing dossier."""
    def render(sub, role):
        if sub is None:
            return '(%s assessment not submitted)' % role
        lines = ['STUDENT:' if role == 'student' else 'PARENT:',
                 'Student name: %s' % (sub.student_name or ''),
                 'Filled by: %s' % (sub.respondent_name or '')]
        resp = sub.responses
        for it in items_for(role):
            ans = resp.get(it['id'])
            if it.get('when') and not _when_met(it, resp):
                continue          # e.g. the class-12 quiz for a class-11 student
            line = '%s [%s] %s -> %s' % (it['id'], it['tag'], it['text'], _flat(ans))
            key = ANSWER_KEY.get(it['id'])
            if key:               # scored item: the AI can't mark it without the key
                line += '   [correct: %s | %s]' % (
                    key, 'RIGHT' if ans == key else 'wrong' if ans else 'not answered')
            lines.append(line)
        return '\n'.join(lines)

    header = ("Run the EduAakashaa onboarding analysis. Use the AI Analysis Rubric "
              "(Deliverable 2) and Insight Dossier template (Deliverable 3) from "
              "ONBOARDING_ASSESSMENT.md. Below are this family's answers, keyed by "
              "item id.\n")
    return header + '\n\n' + render(student, 'student') + '\n\n' + render(parent, 'parent')


def _flat(ans):
    if ans is None:
        return '(not answered)'
    if isinstance(ans, list):
        return '; '.join(str(a) for a in ans)
    if isinstance(ans, dict):
        return '; '.join('%s: %s' % (k, v) for k, v in ans.items() if v not in (None, ''))
    return str(ans)
