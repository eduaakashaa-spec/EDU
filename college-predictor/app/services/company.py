"""Editable seller/company profile used on invoices.

Values are read from the `settings` table (admin-editable, so the GSTIN etc. can
be set once and changed later without a redeploy), falling back to config.COMPANY
defaults for any key not overridden. Everything is plain strings except gst_rate.
"""
from flask import current_app

from app.extensions import db
from app.models_membership import Setting

# setting key -> function producing the default from app config
_DEFAULTS = {
    'legal_name':   lambda c: c['COMPANY'].get('LEGAL_NAME', ''),
    'brand_name':   lambda c: c['COMPANY'].get('BRAND_NAME', 'EduAakashaa'),
    'gstin':        lambda c: c['COMPANY'].get('GSTIN', ''),
    'pan':          lambda c: c['COMPANY'].get('PAN', ''),
    'address':      lambda c: c['COMPANY'].get('ADDRESS', ''),
    'phone':        lambda c: c['COMPANY'].get('PHONE_IN', ''),
    'email':        lambda c: c['COMPANY'].get('EMAIL', c.get('ADMIN_EMAIL', '')),
    'website':      lambda c: c['COMPANY'].get('WEBSITE', ''),
    'logo_url':     lambda c: c['COMPANY'].get('LOGO_URL', ''),
    'bank_name':    lambda c: c['COMPANY'].get('BANK_NAME', ''),
    'bank_ac_name': lambda c: c['COMPANY'].get('BANK_AC_NAME', ''),
    'bank_ac_no':   lambda c: c['COMPANY'].get('BANK_AC_NO', ''),
    'bank_ifsc':    lambda c: c['COMPANY'].get('BANK_IFSC', ''),
    'bank_branch':  lambda c: c['COMPANY'].get('BANK_BRANCH', ''),
    'home_state':   lambda c: c.get('HOME_STATE', 'Tamil Nadu'),
    'gst_rate':     lambda c: str(c.get('GST_RATE', 0.18)),
    'invoice_terms': lambda c: 'Payment due on receipt. This is a computer-generated invoice.',
}

# keys the settings form is allowed to write (same set)
EDITABLE_KEYS = tuple(_DEFAULTS.keys())


def company_profile():
    """Merge DB overrides over config defaults → dict of string values.
    gst_rate is additionally exposed as a float under 'gst_rate_f'."""
    cfg = current_app.config
    overrides = {s.key: s.value for s in Setting.query.all()}
    profile = {}
    for key, default_fn in _DEFAULTS.items():
        val = overrides.get(key)
        profile[key] = val if val not in (None, '') else default_fn(cfg)
    try:
        profile['gst_rate_f'] = float(profile['gst_rate'])
    except (ValueError, TypeError):
        profile['gst_rate_f'] = float(cfg.get('GST_RATE', 0.18))
    return profile


def save_company_profile(form):
    """Upsert the editable keys from a form-like mapping (blank clears an
    override, so it falls back to the config default)."""
    for key in EDITABLE_KEYS:
        if key not in form:
            continue
        value = (form.get(key) or '').strip()
        row = db.session.get(Setting, key)
        if row is None:
            db.session.add(Setting(key=key, value=value))
        else:
            row.value = value
    db.session.commit()
