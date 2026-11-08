"""HR section (HR Admin and Admin): issue offer, experience and relieving letters, keep the register, edit the letter templates.

  /hr/                          dashboard: issue a letter, recent letters, retention reminder
  /hr/new/<kind>                fill in and issue (offer | experience | relieving); ?copy=<id> starts from an earlier letter
  /hr/letters                   register with filters; /hr/letters.csv exports it
  /hr/letters/<id>              the letter on screen; /hr/letters/<id>.pdf the A4 PDF; POST .../void cancels it (the number is never reused)
  /hr/templates/<kind>          edit the template text, preview with sample data, reset to the default
Letters hold personal and salary data, so every route needs HR Admin or Admin."""
import csv
from datetime import date, datetime
from io import StringIO

from urllib.parse import quote

from flask import Blueprint, Response, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user

from app.decorators import hr_required
from app.extensions import db
from app.models import User
from app.models_hr import HrLetter, HrLetterEmail
from app.services import hr_letters as hl
from app.services import mailer
from app.services import hr_pdf

hr_bp = Blueprint('hr', __name__, url_prefix='/hr')


@hr_bp.context_processor
def _ctx():
    return dict(hr_kinds=list(hl.KINDS.items()))


def _kind(kind):
    if kind not in hl.KINDS:
        abort(404)
    return kind


@hr_bp.route('/', endpoint='home')
@hr_required
def home():
    recent = HrLetter.query.order_by(HrLetter.id.desc()).limit(8).all()
    counts = {k: HrLetter.query.filter_by(kind=k, status='issued').count() for k in hl.KINDS}
    return render_template('hr/home.html', kinds=hl.KINDS, recent=recent, counts=counts, fy=hl.fy_of(date.today()))


@hr_bp.route('/new/<kind>', methods=['GET', 'POST'], endpoint='new')
@hr_required
def new(kind):
    _kind(kind)
    fields = hl.FIELDS[kind]
    form, errors = {f['key']: f['default'] for f in fields}, {}
    form['issue_date'] = date.today().isoformat()
    src = db.session.get(HrLetter, request.args.get('copy', type=int)) if request.args.get('copy') else None
    if src is not None and src.kind == kind:                         # start from an earlier letter (new date, new reference number)
        for f in fields:
            raw = src.values.get(f['key'] + '__d') or src.values.get(f['key'])
            if f['kind'] == 'date':
                raw = src.values.get(f['key'] + '__d')
            elif f['kind'] == 'money':
                n = src.values.get(f['key'] + '__n')
                raw = str(n) if n is not None else ''
            if raw and f['key'] != 'issue_date':
                form[f['key']] = raw
    if request.method == 'POST':
        form = {f['key']: (request.form.get(f['key']) or '').strip() for f in fields}
        vals, errors = hl.clean(kind, request.form)
        if not errors:
            try:
                row = hl.issue(kind, vals, current_user)
            except RuntimeError as ex:
                flash(str(ex), 'danger')
            else:
                flash('%s %s issued.' % (hl.KINDS[kind]['title'], row.ref_no), 'success')
                return redirect(url_for('hr.letter', letter_id=row.id))
        else:
            flash('Please fix the highlighted fields.', 'danger')
    return render_template('hr/form.html', kind=kind, info=hl.KINDS[kind], fields=fields, form=form, errors=errors, next_ref=hl.make_ref(kind, hl.fy_of(date.today()), hl.next_serial(kind, hl.fy_of(date.today()))))


def _filtered():
    q = HrLetter.query
    kind = request.args.get('kind', '')
    if kind in hl.KINDS:
        q = q.filter_by(kind=kind)
    fy = request.args.get('fy', type=int)
    if fy:
        q = q.filter_by(fy=fy)
    status = request.args.get('status', '')
    if status in ('issued', 'void'):
        q = q.filter_by(status=status)
    text = (request.args.get('q') or '').strip()
    if text:
        like = '%' + text.replace('%', '').replace('_', '') + '%'
        q = q.filter(db.or_(HrLetter.person_name.ilike(like), HrLetter.ref_no.ilike(like), HrLetter.designation.ilike(like)))
    return q.order_by(HrLetter.id.desc())


@hr_bp.route('/letters', endpoint='register')
@hr_required
def register():
    rows = _filtered().limit(500).all()
    fys = [r[0] for r in db.session.query(HrLetter.fy).distinct().order_by(HrLetter.fy.desc()).all()]
    return render_template('hr/register.html', rows=rows, kinds=hl.KINDS, fys=fys, sel=dict(kind=request.args.get('kind', ''), fy=request.args.get('fy', ''), status=request.args.get('status', ''), q=request.args.get('q', '')))


@hr_bp.route('/letters.csv', endpoint='register_csv')
@hr_required
def register_csv():
    out = StringIO()
    w = csv.writer(out)
    w.writerow(['Reference', 'Type', 'Name', 'Designation', 'Issue date', 'Status', 'Void reason', 'Issued by', 'Created'])
    names = {}
    for r in _filtered().all():
        uid = r.created_by
        if uid not in names:
            u = db.session.get(User, uid) if uid else None
            names[uid] = u.name if u else ''
        w.writerow([r.ref_no, hl.KINDS[r.kind]['title'], r.person_name, r.designation or '', r.issue_date.isoformat(), r.status, r.void_reason or '', names[uid], r.created_at.strftime('%Y-%m-%d %H:%M')])
    return Response('﻿' + out.getvalue(), mimetype='text/csv', headers={'Content-Disposition': 'attachment; filename="hr-letter-register.csv"'})


def _letter(letter_id):
    row = db.session.get(HrLetter, letter_id)
    if row is None:
        abort(404)
    return row


@hr_bp.route('/letters/<int:letter_id>', endpoint='letter')
@hr_required
def letter(letter_id):
    row = _letter(letter_id)
    to, subject, body = hl.default_email(row)
    f = request.args if request.args.get('compose') else {}
    mail = dict(to=f.get('to', to), cc=f.get('cc', ''), subject=f.get('subject', subject), body=f.get('body', body))
    sent = HrLetterEmail.query.filter_by(letter_id=row.id).order_by(HrLetterEmail.id.desc()).all()
    senders = mailer.allowed_senders()
    mailto = 'mailto:%s?subject=%s&body=%s' % (quote(to), quote(subject), quote(body))
    return render_template('hr/letter.html', row=row, info=hl.KINDS[row.kind], html=hl.to_html(hl.render(row)), mail=mail, sent=sent, senders=senders, mail_ok=mailer.is_configured(), mailto=mailto)


@hr_bp.route('/letters/<int:letter_id>.pdf', endpoint='letter_pdf')
@hr_required
def letter_pdf(letter_id):
    row = _letter(letter_id)
    data = hr_pdf.build(hl.render(row), title='%s - %s' % (hl.KINDS[row.kind]['title'], row.ref_no), void=row.status == 'void')
    name = row.ref_no.replace('/', '-') + '.pdf'
    return Response(data, mimetype='application/pdf', headers={'Content-Disposition': 'inline; filename="%s"' % name})


@hr_bp.route('/letters/<int:letter_id>/void', methods=['POST'], endpoint='void')
@hr_required
def void(letter_id):
    row = _letter(letter_id)
    reason = (request.form.get('reason') or '').strip()[:300]
    if row.status == 'void':
        flash('That letter is already void.', 'info')
    elif not reason:
        flash('Give a reason for voiding the letter.', 'danger')
    else:
        row.status, row.void_reason, row.voided_by, row.voided_at = 'void', reason, current_user.id, datetime.utcnow()
        db.session.commit()
        flash('%s marked void. The number stays in the register and is not reused.' % row.ref_no, 'success')
    return redirect(url_for('hr.letter', letter_id=row.id))


@hr_bp.route('/letters/<int:letter_id>/email', methods=['POST'], endpoint='email')
@hr_required
def email(letter_id):
    row = _letter(letter_id)
    if row.status == 'void':
        flash('A void letter cannot be emailed.', 'danger')
        return redirect(url_for('hr.letter', letter_id=row.id))
    to, e1 = hl.parse_emails(request.form.get('to'))
    cc, e2 = hl.parse_emails(request.form.get('cc'))
    if request.form.get('copy_me') and current_user.email and current_user.email.lower() not in [x.lower() for x in cc + to]:
        cc = cc + [current_user.email]
    subject = (request.form.get('subject') or '').strip()[:200]
    body = (request.form.get('body') or '').replace('\r\n', '\n').strip()[:4000]
    senders = mailer.allowed_senders()
    from_addr = request.form.get('from') or (senders[0] if senders else None)
    err = e1 or e2 or (None if to else 'Enter the email address to send to.') or (None if subject else 'Enter a subject.') or (None if body else 'Write a short message.') or \
        (None if from_addr in senders else 'Choose one of the allowed sender addresses.')
    if err:
        flash(err, 'danger')
        return redirect(url_for('hr.letter', letter_id=row.id, compose=1, to=', '.join(to), cc=request.form.get('cc', ''), subject=subject, body=body) + '#email')
    ok, msg = hl.send_letter(row, to, cc, subject, body, from_addr, current_user)
    flash(msg, 'success' if ok else 'danger')
    return redirect(url_for('hr.letter', letter_id=row.id) + '#email')


@hr_bp.route('/templates', endpoint='templates')
@hr_required
def templates():
    rows = [(k, hl.KINDS[k], hl.template(k)) for k in hl.KINDS]
    return render_template('hr/templates.html', rows=rows)


@hr_bp.route('/templates/<kind>', methods=['GET', 'POST'], endpoint='template_edit')
@hr_required
def template_edit(kind):
    _kind(kind)
    tpl = hl.template(kind)
    body, errors = tpl.body, []
    if request.method == 'POST':
        if request.form.get('action') == 'reset':
            tpl.body, tpl.version, tpl.updated_by, tpl.updated_at = hl.DEFAULTS[kind], tpl.version + 1, current_user.id, datetime.utcnow()
            db.session.commit()
            flash('Template reset to the default text.', 'success')
            return redirect(url_for('hr.template_edit', kind=kind))
        body = (request.form.get('body') or '').replace('\r\n', '\n').strip()
        errors = hl.validate_body(body)
        if not errors and body:
            if body != tpl.body:
                tpl.body, tpl.version, tpl.updated_by, tpl.updated_at = body, tpl.version + 1, current_user.id, datetime.utcnow()
                db.session.commit()
                flash('Template saved. Letters already issued keep the text they were issued with.', 'success')
            return redirect(url_for('hr.template_edit', kind=kind))
        if not body:
            errors.append('The template cannot be empty.')
    preview = hl.to_html(hl.blocks(body, hl.sample_values(kind)))
    keys = [f['key'] for f in hl.FIELDS[kind]] + [c for c in hl.COMPUTED if kind == 'offer' or c in ('ref_no', 'year', 'serial')]
    return render_template('hr/template_edit.html', kind=kind, info=hl.KINDS[kind], tpl=tpl, body=body, errors=errors, preview=preview, keys=keys, default_differs=tpl.body != hl.DEFAULTS[kind])
