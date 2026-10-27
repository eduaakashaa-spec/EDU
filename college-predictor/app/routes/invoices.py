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
from app.models_membership import DocSequence, Invoice, InvoiceCancel, InvoiceReceipt, MembershipInvoice
from app.services import invoice_catalog
from flask_login import current_user
from app.services.company import (EDITABLE_KEYS, company_profile,
                                  save_company_profile)
from markupsafe import escape

from app.services.email_templates import SITE, branded_shell
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


_BANK_KEYS = ('bank_ac_name', 'bank_name', 'bank_branch', 'bank_ac_no', 'bank_ifsc')


def _seller_for_display(snapshot):
    """The seller snapshot stored on a document, with today's saved bank details filled in when the snapshot has none (documents issued before the bank details
    were entered in Invoice Settings, for example)."""
    seller = dict(snapshot or {})
    if not seller.get('bank_ac_no'):
        try:
            cur = company_profile()
            for k in _BANK_KEYS:
                if cur.get(k):
                    seller[k] = cur[k]
        except Exception:
            pass
    return seller


def _bank_html(s):
    """Bank details block for e-mails ('' when none are saved)."""
    if not s.get('bank_ac_no'):
        return ''
    rows = [('Account name', s.get('bank_ac_name') or s.get('legal_name')), ('Bank', ', '.join(x for x in (s.get('bank_name'), s.get('bank_branch')) if x)),
            ('Account number', s.get('bank_ac_no')), ('IFSC', s.get('bank_ifsc'))]
    cells = ''.join(f"<tr><td style='padding:3px 10px 3px 0;color:#5A6278'>{escape(k)}</td><td style='padding:3px 0;font-weight:600'>{escape(v)}</td></tr>" for k, v in rows if v)
    return f"<p style='margin:22px 0 6px;font-weight:700'>Bank details for payment</p><table role='presentation' style='font-size:13.5px'>{cells}</table>"


def _next_receipt_no(width=4):
    """Next receipt number (RCPT/NNNN) from the same gap-free 'receipt' series membership receipts use. Row-locked."""
    seq = db.session.query(DocSequence).filter_by(name='receipt').with_for_update().first()
    if seq is None:
        seq = DocSequence(name='receipt', prefix='RCPT/', value=0)
        db.session.add(seq)
        db.session.flush()
    seq.value += 1
    return f'{seq.prefix}{str(seq.value).zfill(width)}'


def _gst_split(amount, rate, intra):
    """GST inside a GST-inclusive amount: (taxable, gst, cgst, sgst, igst). A rate of 0 means no GST."""
    if not rate or amount <= 0:
        return amount, 0, 0, 0, 0
    taxable = round(amount / (1 + rate))
    gst = amount - taxable
    if intra:
        c = gst // 2
        return taxable, gst, c, gst - c, 0
    return taxable, gst, 0, 0, gst


def _issue_receipt(inv, amount, mode='', ref='', notes=''):
    """One receipt for a payment of `amount` paise against invoice `inv` (call after inv.amount_paid is updated)."""
    taxable, gst, c, s_, i_ = _gst_split(amount, inv.gst_rate or 0, bool(inv.cgst))
    r = InvoiceReceipt(receipt_no=_next_receipt_no(), invoice_id=inv.id, invoice_no=inv.invoice_no, customer_name=inv.customer_name, customer_email=inv.customer_email,
                       customer_address=inv.customer_address, description='Payment against invoice %s' % inv.invoice_no, amount=amount, gst_rate=inv.gst_rate or 0,
                       taxable_value=taxable, total_gst=gst, cgst=c, sgst=s_, igst=i_, balance_after=max((inv.total or 0) - (inv.amount_paid or 0), 0),
                       payment_mode=(mode or inv.payment_mode or '')[:60], payment_ref=(ref or inv.payment_ref or '')[:120], notes=notes[:4000],
                       seller_json=inv.seller_json, public_token=secrets.token_urlsafe(24))
    db.session.add(r)
    return r


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
def _all_invoices():
    """Every invoice the business has issued, from both places it can come from:
    standalone invoices and membership-application invoices. They already share
    one EA/NNNN number series, so an admin should see one list.

    Merged in Python rather than a SQL UNION because the two tables keep the
    customer in different places (own columns vs the linked application).
    ponytail: fine at this volume (hundreds); if it ever reaches thousands,
    move to a UNION query with SQL-side paging."""
    rows = []
    for inv in Invoice.query.all():
        rows.append({
            'no': inv.invoice_no, 'date': inv.invoice_date or inv.created_at,
            'customer': inv.customer_name, 'email': inv.customer_email or '',
            'total': inv.total or 0, 'paid': inv.amount_paid or 0,
            'status': inv.payment_status or 'Unpaid', 'source': 'Invoice',
            'url': url_for('invoices.admin_detail', inv_id=inv.id),
        })
    for mi in MembershipInvoice.query.all():
        app_row = mi.application
        rows.append({
            'no': mi.invoice_no, 'date': mi.invoice_date or mi.created_at,
            'customer': app_row.name if app_row else '—',
            'email': (app_row.email if app_row else ''),
            'total': (app_row.final_total if app_row else 0) or 0,
            'paid': mi.amount_paid or 0,
            'status': mi.payment_status or 'Unpaid', 'source': 'Membership',
            'url': (url_for('membership.admin_detail', app_id=mi.application_id)
                    if mi.application_id else '#'),
        })
    rows.sort(key=lambda r: r['date'] or datetime.min, reverse=True)
    return rows


@invoices_bp.route('/admin/invoices')
@admin_required
def admin_list():
    q = (request.args.get('q') or '').strip().lower()
    status = (request.args.get('status') or '').strip()
    source = (request.args.get('source') or '').strip()
    page = max(request.args.get('page', 1, type=int), 1)

    everything = _all_invoices()
    # stats always describe the whole book, not the current filter
    live = [r for r in everything if r['status'] != 'Cancelled']
    billed = sum(r['total'] for r in live)
    collected = sum(r['paid'] for r in live)
    stats = {'count': len(live), 'billed': billed, 'collected': collected,
             'due': billed - collected, 'cancelled': len(everything) - len(live)}

    rows = everything
    if q:
        rows = [r for r in rows if q in (r['no'] or '').lower()
                or q in (r['customer'] or '').lower() or q in (r['email'] or '').lower()]
    if status in PAYMENT_STATUSES + ('Cancelled',):
        rows = [r for r in rows if r['status'] == status]
    if source in ('Invoice', 'Membership'):
        rows = [r for r in rows if r['source'] == source]

    per_page, total = 25, len(rows)
    pages = max((total + per_page - 1) // per_page, 1)
    page = min(page, pages)
    window = rows[(page - 1) * per_page: page * per_page]
    pager = {'page': page, 'pages': pages, 'total': total,
             'has_prev': page > 1, 'has_next': page < pages,
             'prev_num': page - 1, 'next_num': page + 1}

    return render_template('admin/invoices_list.html', admin_tab='invoices',
                           rows=window, pager=pager, stats=stats, q=q,
                           status=status, source=source, statuses=PAYMENT_STATUSES + ('Cancelled',))


@invoices_bp.route('/admin/invoices/new', methods=['GET', 'POST'])
@admin_required
def admin_new():
    profile = company_profile()
    if request.method == 'GET':
        return render_template('admin/invoice_form.html', admin_tab='invoices',
                               profile=profile, modes=PAYMENT_MODES, catalog=invoice_catalog.load())

    f = request.form
    name = (f.get('customer_name') or '').strip()[:160]
    if not name:
        flash('Customer name is required.', 'danger')
        return render_template('admin/invoice_form.html', admin_tab='invoices',
                               profile=profile, modes=PAYMENT_MODES, form=f, catalog=invoice_catalog.load())

    items = _parse_items(f)
    if not items:
        flash('Add at least one line item with a description.', 'danger')
        return render_template('admin/invoice_form.html', admin_tab='invoices',
                               profile=profile, modes=PAYMENT_MODES, form=f, catalog=invoice_catalog.load())

    try:
        gst_pct = float(f.get('gst_pct') or (profile['gst_rate_f'] * 100))
    except ValueError:
        gst_pct = profile['gst_rate_f'] * 100
    gst_rate = max(gst_pct, 0) / 100.0
    no_gst = f.get('gst_mode') == 'none'                                  # an invoice without GST: rate 0, no tax lines, no GSTIN
    if no_gst:
        gst_rate = 0.0

    inv = Invoice(
        invoice_no=_next_invoice_no(),
        customer_name=name,
        customer_email=(f.get('customer_email') or '').strip()[:200],
        customer_gstin='' if no_gst else (f.get('customer_gstin') or '').strip()[:20],
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
    db.session.flush()
    if inv.amount_paid:                                                      # created already paid: issue its receipt now
        _issue_receipt(inv, inv.amount_paid)
    db.session.commit()
    flash(f'Invoice {inv.invoice_no} created{" without GST" if no_gst else ""}.' + (' Payment receipt issued.' if inv.amount_paid else ''), 'success')
    return redirect(url_for('invoices.admin_detail', inv_id=inv.id))


# --------------------------------------------------------------------------- #
# Admin — one invoice
# --------------------------------------------------------------------------- #
@invoices_bp.route('/admin/invoices/<int:inv_id>')
@admin_required
def admin_detail(inv_id):
    inv = db.session.get(Invoice, inv_id) or abort(404)
    return render_template('invoice_view.html', inv=inv, seller=_seller_for_display(inv.seller),
                           show_actions=True, modes=PAYMENT_MODES,
                           statuses=PAYMENT_STATUSES, admin_tab='invoices',
                           public_url=SITE + url_for('invoices.public_view', token=inv.public_token))


def _invoice_email(inv):
    """(subject, text, html) for the customer — inline HTML + a link to the
    printable copy. Uses the seller snapshot stored on the invoice."""
    s = _seller_for_display(inv.seller)
    view = SITE + url_for('invoices.public_view', token=inv.public_token)
    money = lambda p: f'₹{int(p or 0) / 100:,.2f}'
    first = (inv.customer_name or '').strip().split(' ')[0] or 'there'
    cell = 'padding:9px 10px;border-bottom:1px solid #EFE7D4'

    rows = ''.join(
        f"<tr><td style='{cell}'>{escape(it['desc'])}</td>"
        f"<td style='{cell};text-align:center;color:#5A6278'>{it['qty']}</td>"
        f"<td style='{cell};text-align:right;color:#5A6278'>{money(it['rate'])}</td>"
        f"<td style='{cell};text-align:right;font-weight:600'>{money(it['qty'] * it['rate'])}</td></tr>"
        for it in inv.items)

    def total_row(label, value, strong=False, accent=False):
        weight = 'font-weight:700;' if strong else ''
        colour = 'color:#0E3A8A;' if accent else 'color:#0E1B3D;'
        size = 'font-size:16px;' if strong else 'font-size:13.5px;'
        return (f"<tr><td colspan='3' style='padding:4px 10px;text-align:right;"
                f"color:#5A6278;{size}'>{label}</td>"
                f"<td style='padding:4px 10px;text-align:right;{weight}{colour}{size}'>{value}</td></tr>")

    totals = total_row('Subtotal' if inv.no_gst else 'Taxable value', money(inv.taxable_value))
    if inv.discount:
        totals += total_row('Discount', '−' + money(inv.discount))
    if inv.additional_fee:
        totals += total_row(escape(inv.additional_fee_label or 'Additional fee'),
                            money(inv.additional_fee))
    if not inv.no_gst:
        totals += total_row(f'GST ({round(inv.gst_rate * 100, 2)}%)', money(inv.total_gst))
    totals += ("<tr><td colspan='4' style='padding:0 10px'>"
               "<div style='border-top:2px solid #0E3A8A;margin-top:6px'></div></td></tr>")
    totals += total_row('Total', money(inv.total), strong=True, accent=True)

    subject = f"Invoice {inv.invoice_no} from {s.get('brand_name', 'EduAakashaa')}"
    text = (f"Hi {first},\n\nPlease find your invoice {inv.invoice_no} "
            f"for {money(inv.total)}.\n\nView / download: {view}\n\n"
            f"— Team EduAakashaa")

    status = ('Paid' if inv.payment_status == 'Paid' else inv.payment_status)
    chip_bg = 'rgba(31,139,92,.14);color:#1F8B5C' if inv.payment_status == 'Paid' \
        else 'rgba(194,58,58,.10);color:#C23A3A'

    body = (
        f"<p style='margin:0 0 6px'>Hi {escape(first)},</p>"
        f"<p style='margin:0 0 18px'>Here is your invoice <strong>{inv.invoice_no}</strong>"
        f"{' dated ' + inv.invoice_date.strftime('%d %b %Y') if inv.invoice_date else ''}."
        f" <span style='display:inline-block;font-size:11px;font-weight:700;padding:2px 9px;"
        f"border-radius:99px;background:{chip_bg}'>{status}</span></p>"

        "<table role='presentation' cellpadding='0' cellspacing='0' "
        "style='border-collapse:collapse;width:100%;font-size:13.5px'>"
        "<thead><tr>"
        "<th style='text-align:left;padding:8px 10px;background:#0E3A8A;color:#fff;"
        "font-size:11px;letter-spacing:.06em;text-transform:uppercase'>Item</th>"
        "<th style='padding:8px 10px;background:#0E3A8A;color:#fff;font-size:11px;"
        "letter-spacing:.06em;text-transform:uppercase'>Qty</th>"
        "<th style='text-align:right;padding:8px 10px;background:#0E3A8A;color:#fff;"
        "font-size:11px;letter-spacing:.06em;text-transform:uppercase'>Rate</th>"
        "<th style='text-align:right;padding:8px 10px;background:#0E3A8A;color:#fff;"
        "font-size:11px;letter-spacing:.06em;text-transform:uppercase'>Amount</th>"
        f"</tr></thead><tbody>{rows}{totals}</tbody></table>"

        f"<p style='margin:24px 0 8px'><a href='{view}' style='background:#FF6B0A;color:#ffffff;"
        "text-decoration:none;padding:12px 28px;border-radius:999px;font-weight:700;"
        "font-size:14px;display:inline-block'>View / download invoice →</a></p>"
        "<p style='margin:14px 0 0;font-size:12.5px;color:#5A6278'>"
        "Open the link above to print or save this invoice as a PDF.</p>"
        + ('' if inv.payment_status == 'Paid' else _bank_html(s))
        + (f"<p style='margin:10px 0 0;font-size:12.5px;color:#5A6278'>GSTIN "
           f"{escape(s.get('gstin'))}</p>" if (s.get('gstin') and not inv.no_gst) else ''))

    return subject, text, branded_shell(body)


@invoices_bp.route('/admin/invoices/<int:inv_id>/email', methods=['POST'])
@admin_required
def admin_email(inv_id):
    inv = db.session.get(Invoice, inv_id) or abort(404)
    if inv.cancelled:
        flash('This invoice is cancelled. Reinstate it before sending.', 'danger')
        return redirect(url_for('invoices.admin_detail', inv_id=inv.id))
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
    if inv.cancelled:
        flash('This invoice is cancelled. Reinstate it before recording a payment.', 'danger')
        return redirect(url_for('invoices.admin_detail', inv_id=inv.id))
    status = request.form.get('payment_status')
    inv.payment_mode = (request.form.get('payment_mode') or '').strip()[:60]
    inv.payment_ref = (request.form.get('payment_ref') or '').strip()[:120]
    before = inv.amount_paid or 0
    received = to_paise(request.form.get('amount_received'))
    if received > 0:                                                         # an amount received now: add it
        inv.amount_paid = min(before + received, inv.total or 0) if (inv.total or 0) else before + received
    elif status == 'Paid':
        inv.amount_paid = inv.total
    elif status == 'Unpaid':
        inv.amount_paid = 0
    if received > 0 or status == 'Paid':                                     # status follows the money
        inv.payment_status = 'Paid' if inv.amount_paid >= (inv.total or 0) > 0 else ('Partially Paid' if inv.amount_paid > 0 else 'Unpaid')
    elif status in PAYMENT_STATUSES:
        inv.payment_status = status
    delta = (inv.amount_paid or 0) - before
    msg = 'Payment updated.'
    if delta > 0:                                                            # every payment received gets its own receipt
        db.session.flush()
        r = _issue_receipt(inv, delta, inv.payment_mode, inv.payment_ref)
        msg = 'Payment recorded. Receipt %s issued.' % r.receipt_no
    db.session.commit()
    flash(msg, 'success')
    return redirect(url_for('invoices.admin_detail', inv_id=inv.id))


# --------------------------------------------------------------------------- #
# Payment receipts (with or without GST)
# --------------------------------------------------------------------------- #
def _receipt_email(r):
    s = r.seller
    view = SITE + url_for('invoices.public_receipt', token=r.public_token)
    money = lambda p: f'₹{int(p or 0) / 100:,.2f}'
    first = (r.customer_name or '').strip().split(' ')[0] or 'there'
    subject = f"Payment receipt {r.receipt_no} from {s.get('brand_name', 'EduAakashaa')}"
    text = f"Hi {first},\n\nThank you. We received {money(r.amount)}. Your receipt is {r.receipt_no}.\n\nView / download: {view}\n\n— Team EduAakashaa"
    gst_line = '' if r.no_gst else f"<p style='margin:0 0 6px;color:#5A6278'>Includes GST of {money(r.total_gst)} ({round(r.gst_rate * 100, 2)}%).</p>"
    body = (f"<p style='margin:0 0 6px'>Hi {escape(first)},</p>"
            f"<p style='margin:0 0 14px'>Thank you. We have received <strong>{money(r.amount)}</strong>"
            f"{' against invoice <strong>' + escape(r.invoice_no) + '</strong>' if r.invoice_no else ''}. Your payment receipt is <strong>{r.receipt_no}</strong>.</p>"
            + gst_line + ('' if r.balance_after is None else f"<p style='margin:0 0 6px;color:#5A6278'>Balance due on the invoice: {money(r.balance_after)}.</p>")
            + f"<p style='margin:20px 0 8px'><a href='{view}' style='background:#FF6B0A;color:#ffffff;text-decoration:none;padding:12px 28px;border-radius:999px;font-weight:700;font-size:14px;display:inline-block'>View / download receipt →</a></p>")
    return subject, text, branded_shell(body)


@invoices_bp.route('/admin/receipts')
@admin_required
def admin_receipts():
    q = (request.args.get('q') or '').strip()
    query = InvoiceReceipt.query
    if q:
        like = f'%{q}%'
        query = query.filter(db.or_(InvoiceReceipt.customer_name.ilike(like), InvoiceReceipt.receipt_no.ilike(like), InvoiceReceipt.invoice_no.ilike(like), InvoiceReceipt.customer_email.ilike(like)))
    rows = query.order_by(InvoiceReceipt.id.desc()).limit(300).all()
    return render_template('admin/receipts_list.html', admin_tab='invoices', rows=rows, q=q, total=sum(r.amount or 0 for r in rows))


@invoices_bp.route('/admin/receipts/new', methods=['GET', 'POST'])
@admin_required
def admin_receipt_new():
    """A payment receipt on its own (no invoice), with or without GST."""
    profile = company_profile()
    if request.method == 'GET':
        return render_template('admin/receipt_form.html', admin_tab='invoices', profile=profile, modes=PAYMENT_MODES, form=None)
    f = request.form
    name = (f.get('customer_name') or '').strip()[:160]
    amount = to_paise(f.get('amount'))
    if not name or amount <= 0:
        flash('Enter the payer\'s name and an amount greater than zero.', 'danger')
        return render_template('admin/receipt_form.html', admin_tab='invoices', profile=profile, modes=PAYMENT_MODES, form=f)
    rate = 0.0
    if f.get('gst_mode') == 'with':
        try:
            rate = max(float(f.get('gst_pct') or profile['gst_rate_f'] * 100), 0) / 100.0
        except ValueError:
            rate = profile['gst_rate_f']
    state = (f.get('customer_state') or '').strip()
    intra = bool(state) and state.lower() == (profile['home_state'] or '').strip().lower()
    taxable, gst, c, s_, i_ = _gst_split(amount, rate, intra)
    r = InvoiceReceipt(receipt_no=_next_receipt_no(), customer_name=name, customer_email=(f.get('customer_email') or '').strip()[:200], customer_address=(f.get('customer_address') or '').strip()[:1000],
                       description=(f.get('description') or 'Payment received').strip()[:300], amount=amount, gst_rate=rate, taxable_value=taxable, total_gst=gst, cgst=c, sgst=s_, igst=i_,
                       payment_mode=(f.get('payment_mode') or '').strip()[:60], payment_ref=(f.get('payment_ref') or '').strip()[:120], notes=(f.get('notes') or '').strip()[:4000],
                       seller_json=json.dumps(profile), public_token=secrets.token_urlsafe(24))
    d = f.get('receipt_date')
    if d:
        try:
            r.receipt_date = datetime.strptime(d, '%Y-%m-%d')
        except ValueError:
            pass
    db.session.add(r)
    db.session.commit()
    flash(f'Receipt {r.receipt_no} created{" without GST" if not rate else ""}.', 'success')
    return redirect(url_for('invoices.admin_receipt', rid=r.id))


@invoices_bp.route('/admin/receipts/<int:rid>')
@admin_required
def admin_receipt(rid):
    r = db.session.get(InvoiceReceipt, rid) or abort(404)
    return render_template('receipt_view.html', r=r, seller=r.seller, show_actions=True, admin_tab='invoices', public_url=SITE + url_for('invoices.public_receipt', token=r.public_token))


@invoices_bp.route('/admin/receipts/<int:rid>/email', methods=['POST'])
@admin_required
def admin_receipt_email(rid):
    r = db.session.get(InvoiceReceipt, rid) or abort(404)
    if not r.customer_email:
        flash('Add a customer email to this receipt before sending.', 'danger')
        return redirect(url_for('invoices.admin_receipt', rid=r.id))
    subject, text, html = _receipt_email(r)
    send_async(r.customer_email, subject, text, html)
    r.emailed_at = _now()
    db.session.commit()
    flash(f'Receipt emailed to {r.customer_email}.' if mail_configured() else 'Email is not configured (SMTP_* env vars): receipt marked sent but no email left the server.', 'success' if mail_configured() else 'info')
    return redirect(url_for('invoices.admin_receipt', rid=r.id))


@invoices_bp.route('/admin/receipts/<int:rid>/delete', methods=['POST'])
@admin_required
def admin_receipt_delete(rid):
    r = db.session.get(InvoiceReceipt, rid) or abort(404)
    no = r.receipt_no
    db.session.delete(r)
    db.session.commit()
    flash(f'Receipt {no} deleted.', 'info')
    return redirect(url_for('invoices.admin_receipts'))


@invoices_bp.route('/receipt/<token>')
def public_receipt(token):
    r = InvoiceReceipt.query.filter_by(public_token=token).first() or abort(404)
    return render_template('receipt_view.html', r=r, seller=r.seller, show_actions=False)


@invoices_bp.route('/admin/invoices/<int:inv_id>/cancel', methods=['POST'])
@admin_required
def admin_cancel(inv_id):
    """Cancel (void) an invoice: it keeps its number and stays on record as Cancelled, is left out of the totals and takes no further payments."""
    inv = db.session.get(Invoice, inv_id) or abort(404)
    if inv.cancelled:
        return redirect(url_for('invoices.admin_detail', inv_id=inv.id))
    reason = (request.form.get('reason') or '').strip()[:300]
    if not reason:
        flash('Give a reason for cancelling the invoice.', 'danger')
        return redirect(url_for('invoices.admin_detail', inv_id=inv.id))
    db.session.add(InvoiceCancel(invoice_id=inv.id, reason=reason, prev_status=inv.payment_status, cancelled_by=current_user.id))
    inv.payment_status = 'Cancelled'
    db.session.commit()
    paid = inv.amount_paid or 0
    flash(f'Invoice {inv.invoice_no} cancelled.' + (f' ₹{paid / 100:,.2f} had been received against it; its receipts stay on record, so refund or adjust that amount separately.' if paid else ''), 'success')
    return redirect(url_for('invoices.admin_detail', inv_id=inv.id))


@invoices_bp.route('/admin/invoices/<int:inv_id>/reinstate', methods=['POST'])
@admin_required
def admin_reinstate(inv_id):
    inv = db.session.get(Invoice, inv_id) or abort(404)
    if inv.cancelled:
        c = inv.cancel_info
        inv.payment_status = ('Paid' if (inv.amount_paid or 0) >= (inv.total or 0) > 0 else 'Partially Paid' if (inv.amount_paid or 0) > 0 else 'Unpaid')
        if c:
            db.session.delete(c)
        db.session.commit()
        flash(f'Invoice {inv.invoice_no} reinstated.', 'success')
    return redirect(url_for('invoices.admin_detail', inv_id=inv.id))


@invoices_bp.route('/admin/invoice-settings/catalog', methods=['POST'])
@admin_required
def admin_catalog():
    """Save the item catalogue offered in the invoice form (names and prices), or reset it to the membership paths."""
    if request.form.get('reset'):
        invoice_catalog.reset()
        flash('Item catalogue reset to the EduAakashaA membership paths.', 'info')
        return redirect(url_for('invoices.admin_settings') + '#catalog')
    names, prices, groups = request.form.getlist('cat_name'), request.form.getlist('cat_price'), request.form.getlist('cat_group')
    drop = set(request.form.getlist('cat_remove'))
    items = [{'name': n, 'price': p, 'group': (groups[i] if i < len(groups) else 'Other')} for i, (n, p) in enumerate(zip(names, prices)) if str(i) not in drop]
    invoice_catalog.save(items)
    flash('Item catalogue saved.', 'success')
    return redirect(url_for('invoices.admin_settings') + '#catalog')


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
    return render_template('invoice_view.html', inv=inv, seller=_seller_for_display(inv.seller),
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
                           profile=company_profile(), catalog=invoice_catalog.load())
