"""Standalone GST invoices.

Admin (admin tier):
    GET  /admin/invoices                 — list + search + totals
    GET  /admin/invoices/new             — create form (dynamic line items)
    POST /admin/invoices/new             — create + allocate a transaction-safe number
    GET  /admin/invoices/<id>            — admin view (printable) + actions
    POST /admin/invoices/<id>/email      — email the invoice to the customer
    POST /admin/invoices/<id>/payment    — record / update payment
    POST /admin/invoices/<id>/delete     — void (delete) an invoice
    GET/POST /admin/invoice-settings     — seller profile (GSTIN, bank, …), editable

Public:
    GET  /invoice/<token>                — customer's printable copy (tokenised, no login)

Invoices are emailed as inline HTML + a link to the printable page. There is no
server-side PDF generation — the printable page + browser "Print → Save as PDF"
covers it without a heavyweight dependency (weasyprint/wkhtmltopdf).
ponytail: add xhtml2pdf/fpdf2 later if a PDF *attachment* is ever required.
"""
import json
import secrets
from datetime import datetime, timezone

from flask import (Blueprint, abort, current_app, flash, redirect,
                   render_template, request, url_for)

from app.decorators import admin_required
from app.extensions import db
from app.models_membership import DocSequence, Invoice
from app.services.company import (EDITABLE_KEYS, company_profile,
                                  save_company_profile)
from app.services.email_templates import SITE
from app.services.mailer import is_configured as mail_configured
from app.services.mailer import send_async
from app.services.pricing import compute_invoice_totals, to_paise

invoices_bp = Blueprint('invoices', __name__)

PAYMENT_STATUSES = ('Unpaid', 'Partially Paid', 'Paid')
PAYMENT_MODES = ('UPI', 'Bank Transfer', 'Card', 'Cash', 'Cheque', 'Other')


@invoices_bp.app_template_filter('inr')
def _inr(paise):
    """paise int → '1,234.00' (no symbol; templates prepend ₹)."""
    return f'{int(paise or 0) / 100:,.2f}'


def _now():
    return datetime.now(timezone.utc).replace(tzinfo=None)


def _next_invoice_no(width=4):
    """Allocate the next invoice number, sharing the 'invoice' sequence with
    membership invoices so the business keeps one gap-free series. Row-locked."""
    seq = (db.session.query(DocSequence).filter_by(name='invoice')
           .with_for_update().first())
    if seq is None:
        seq = DocSequence(name='invoice', prefix='EA/', value=0)
        db.session.add(seq)
        db.session.flush()
    seq.value += 1
    return f'{seq.prefix}{str(seq.value).zfill(width)}'


def _parse_items(form):
    """Build the line-item list from the repeated form fields; drop blank rows."""
    items = []
    descs = form.getlist('item_desc')
    qtys = form.getlist('item_qty')
    rates = form.getlist('item_rate')
    for i, desc in enumerate(descs):
        desc = (desc or '').strip()[:200]
        if not desc:
            continue
        try:
            qty = int(float(qtys[i])) if i < len(qtys) and qtys[i] else 1
        except (ValueError, TypeError):
            qty = 1
        qty = max(qty, 1)
        rate = to_paise(rates[i]) if i < len(rates) else 0
        items.append({'desc': desc, 'qty': qty, 'rate': max(rate, 0)})
    return items


def _apply_totals(inv, items, gst_rate, home_state):
    t = compute_invoice_totals(items, discount=inv.discount,
                               additional_fee=inv.additional_fee,
                               customer_state=inv.customer_state or '',
                               home_state=home_state, gst_rate=gst_rate)
    inv.subtotal, inv.taxable_value = t.subtotal, t.taxable_value
    inv.cgst, inv.sgst, inv.igst = t.cgst, t.sgst, t.igst
    inv.total_gst, inv.total = t.total_gst, t.total
    return t


# --------------------------------------------------------------------------- #
# Admin — list / create
# --------------------------------------------------------------------------- #
@invoices_bp.route('/admin/invoices')
@admin_required
def admin_list():
    q = (request.args.get('q') or '').strip()
    status = (request.args.get('status') or '').strip()
    page = request.args.get('page', 1, type=int)

    query = Invoice.query
    if q:
        like = f'%{q}%'
        query = query.filter(db.or_(Invoice.customer_name.ilike(like),
                                    Invoice.customer_email.ilike(like),
                                    Invoice.invoice_no.ilike(like)))
    if status in PAYMENT_STATUSES:
        query = query.filter(Invoice.payment_status == status)

    pagination = (query.order_by(Invoice.created_at.desc())
                  .paginate(page=page, per_page=25, error_out=False))
    count, billed, collected = db.session.query(
        db.func.count(Invoice.id),
        db.func.coalesce(db.func.sum(Invoice.total), 0),
        db.func.coalesce(db.func.sum(Invoice.amount_paid), 0)).one()
    stats = {'count': count, 'billed': billed, 'collected': collected,
             'due': (billed or 0) - (collected or 0)}
    return render_template('admin/invoices_list.html', admin_tab='invoices',
                           pagination=pagination, rows=pagination.items,
                           stats=stats, q=q, status=status, statuses=PAYMENT_STATUSES)


@invoices_bp.route('/admin/invoices/new', methods=['GET', 'POST'])
@admin_required
def admin_new():
    profile = company_profile()
    if request.method == 'GET':
        return render_template('admin/invoice_form.html', admin_tab='invoices',
                               profile=profile, modes=PAYMENT_MODES)

    f = request.form
    name = (f.get('customer_name') or '').strip()[:160]
    if not name:
        flash('Customer name is required.', 'danger')
        return render_template('admin/invoice_form.html', admin_tab='invoices',
                               profile=profile, modes=PAYMENT_MODES, form=f)

    items = _parse_items(f)
    if not items:
        flash('Add at least one line item with a description.', 'danger')
        return render_template('admin/invoice_form.html', admin_tab='invoices',
                               profile=profile, modes=PAYMENT_MODES, form=f)

    try:
        gst_pct = float(f.get('gst_pct') or (profile['gst_rate_f'] * 100))
    except ValueError:
        gst_pct = profile['gst_rate_f'] * 100
    gst_rate = max(gst_pct, 0) / 100.0

    inv = Invoice(
        invoice_no=_next_invoice_no(),
        customer_name=name,
        customer_email=(f.get('customer_email') or '').strip()[:200],
        customer_gstin=(f.get('customer_gstin') or '').strip()[:20],
        customer_address=(f.get('customer_address') or '').strip()[:1000],
        customer_state=(f.get('customer_state') or '').strip()[:120],
        items_json=json.dumps(items),
        discount=to_paise(f.get('discount')),
        additional_fee=to_paise(f.get('additional_fee')),
        additional_fee_label=(f.get('additional_fee_label') or '').strip()[:120],
        gst_rate=gst_rate,
        payment_status=(f.get('payment_status') if f.get('payment_status') in PAYMENT_STATUSES else 'Unpaid'),
        payment_mode=(f.get('payment_mode') or '').strip()[:60],
        payment_ref=(f.get('payment_ref') or '').strip()[:120],
        notes=(f.get('notes') or '').strip()[:4000],
        seller_json=json.dumps(profile),
        public_token=secrets.token_urlsafe(24),
    )
    _apply_totals(inv, items, gst_rate, profile['home_state'])
    if inv.payment_status == 'Paid':
        inv.amount_paid = inv.total
    db.session.add(inv)
    db.session.commit()
    flash(f'Invoice {inv.invoice_no} created.', 'success')
    return redirect(url_for('invoices.admin_detail', inv_id=inv.id))


# --------------------------------------------------------------------------- #
# Admin — one invoice
# --------------------------------------------------------------------------- #
@invoices_bp.route('/admin/invoices/<int:inv_id>')
@admin_required
def admin_detail(inv_id):
    inv = db.session.get(Invoice, inv_id) or abort(404)
    return render_template('invoice_view.html', inv=inv, seller=inv.seller,
                           show_actions=True, modes=PAYMENT_MODES,
                           statuses=PAYMENT_STATUSES, admin_tab='invoices',
                           public_url=SITE + url_for('invoices.public_view', token=inv.public_token))


def _invoice_email(inv):
    """(subject, text, html) for the customer — inline HTML + a link to the
    printable copy. Uses the seller snapshot stored on the invoice."""
    s = inv.seller
    view = SITE + url_for('invoices.public_view', token=inv.public_token)
    money = lambda p: f'₹{int(p or 0) / 100:,.2f}'
    rows = ''.join(
        f"<tr><td style='padding:6px 8px;border-bottom:1px solid #eee'>{it['desc']}</td>"
        f"<td style='padding:6px 8px;border-bottom:1px solid #eee;text-align:center'>{it['qty']}</td>"
        f"<td style='padding:6px 8px;border-bottom:1px solid #eee;text-align:right'>{money(it['rate'])}</td>"
        f"<td style='padding:6px 8px;border-bottom:1px solid #eee;text-align:right'>{money(it['qty'] * it['rate'])}</td></tr>"
        for it in inv.items)
    subject = f"Invoice {inv.invoice_no} from {s.get('brand_name', 'EduAakashaa')}"
    text = (f"Hi {inv.customer_name},\n\nPlease find your invoice {inv.invoice_no} "
            f"for {money(inv.total)}.\n\nView / download: {view}\n\n"
            f"— {s.get('legal_name', 'EduAakashaa')}")
    html = (
        f"<p>Hi {inv.customer_name},</p><p>Please find your invoice "
        f"<strong>{inv.invoice_no}</strong> below.</p>"
        "<table style='border-collapse:collapse;width:100%;font-size:14px;max-width:560px'>"
        "<thead><tr>"
        "<th style='text-align:left;padding:6px 8px;border-bottom:2px solid #0E3A8A'>Item</th>"
        "<th style='padding:6px 8px;border-bottom:2px solid #0E3A8A'>Qty</th>"
        "<th style='text-align:right;padding:6px 8px;border-bottom:2px solid #0E3A8A'>Rate</th>"
        "<th style='text-align:right;padding:6px 8px;border-bottom:2px solid #0E3A8A'>Amount</th>"
        f"</tr></thead><tbody>{rows}</tbody></table>"
        f"<p style='font-size:14px'>Taxable: {money(inv.taxable_value)}"
        + (f" &middot; Discount: −{money(inv.discount)}" if inv.discount else "")
        + f" &middot; GST: {money(inv.total_gst)}<br>"
        f"<strong style='font-size:16px'>Total: {money(inv.total)}</strong></p>"
        f"<p style='margin:22px 0'><a href='{view}' style='background:#0E3A8A;color:#fff;"
        "text-decoration:none;padding:12px 26px;border-radius:8px;font-weight:700'>"
        "View / download invoice →</a></p>"
        f"<p style='color:#666;font-size:13px'>{s.get('legal_name', 'EduAakashaa')}"
        + (f" &middot; GSTIN {s.get('gstin')}" if s.get('gstin') else "") + "</p>")
    return subject, text, html


@invoices_bp.route('/admin/invoices/<int:inv_id>/email', methods=['POST'])
@admin_required
def admin_email(inv_id):
    inv = db.session.get(Invoice, inv_id) or abort(404)
    if not inv.customer_email:
        flash('Add a customer email to this invoice before sending.', 'danger')
        return redirect(url_for('invoices.admin_detail', inv_id=inv.id))
    subject, text, html = _invoice_email(inv)
    send_async(inv.customer_email, subject, text, html)
    inv.emailed_at = _now()
    db.session.commit()
    if mail_configured():
        flash(f'Invoice emailed to {inv.customer_email}.', 'success')
    else:
        flash('Email is not configured (SMTP_* env vars) — invoice marked sent but no email left the server.', 'info')
    return redirect(url_for('invoices.admin_detail', inv_id=inv.id))


@invoices_bp.route('/admin/invoices/<int:inv_id>/payment', methods=['POST'])
@admin_required
def admin_payment(inv_id):
    inv = db.session.get(Invoice, inv_id) or abort(404)
    status = request.form.get('payment_status')
    if status in PAYMENT_STATUSES:
        inv.payment_status = status
    inv.payment_mode = (request.form.get('payment_mode') or '').strip()[:60]
    inv.payment_ref = (request.form.get('payment_ref') or '').strip()[:120]
    if inv.payment_status == 'Paid':
        inv.amount_paid = inv.total
    else:
        inv.amount_paid = to_paise(request.form.get('amount_paid'))
    db.session.commit()
    flash('Payment updated.', 'success')
    return redirect(url_for('invoices.admin_detail', inv_id=inv.id))


@invoices_bp.route('/admin/invoices/<int:inv_id>/delete', methods=['POST'])
@admin_required
def admin_delete(inv_id):
    inv = db.session.get(Invoice, inv_id) or abort(404)
    no = inv.invoice_no
    db.session.delete(inv)
    db.session.commit()
    flash(f'Invoice {no} deleted.', 'info')
    return redirect(url_for('invoices.admin_list'))


# --------------------------------------------------------------------------- #
# Public — customer's printable copy
# --------------------------------------------------------------------------- #
@invoices_bp.route('/invoice/<token>')
def public_view(token):
    inv = Invoice.query.filter_by(public_token=token).first() or abort(404)
    return render_template('invoice_view.html', inv=inv, seller=inv.seller,
                           show_actions=False)


# --------------------------------------------------------------------------- #
# Admin — seller / invoice settings
# --------------------------------------------------------------------------- #
@invoices_bp.route('/admin/invoice-settings', methods=['GET', 'POST'])
@admin_required
def admin_settings():
    if request.method == 'POST':
        # gst rate is entered as a percentage; store it as a fraction
        data = {k: request.form.get(k, '') for k in EDITABLE_KEYS if k != 'gst_rate'}
        try:
            pct = float(request.form.get('gst_pct') or 18)
        except ValueError:
            pct = 18
        data['gst_rate'] = str(max(pct, 0) / 100.0)
        save_company_profile(data)
        flash('Invoice settings saved.', 'success')
        return redirect(url_for('invoices.admin_settings'))
    return render_template('admin/invoice_settings.html', admin_tab='invoices',
                           profile=company_profile())
