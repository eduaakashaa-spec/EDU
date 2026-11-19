"""Promotional campaigns with a complimentary membership (first one: Neikkarapatti & Palani, Class of 2027, code NKP).

Flow: the public landing page posts a registration -> it is stored as `New` (no access yet) -> an admin checks the details (the page tells
families they may be checked with the school) and activates it, which creates the portal login (or upgrades an existing account) with
Premium access for a set number of days and emails the login details. Nothing here charges money or issues an invoice.
"""
import re
import secrets
import string
import threading
import time
from datetime import datetime, timedelta, timezone

from app.extensions import bcrypt, db
from app.models import User
from app.models_membership import CampaignRegistration

NKP = dict(slug='neikkarapatti-palani', code='NKP', campaign='NKP-Neikkarapatti-Palani-2027', label='Neikkarapatti & Palani · Class of 2027',
           prefix='EA-NKP-', access_days=365)
STREAMS = ('PCM', 'PCB', 'PCMB', 'Other')
ADMISSIONS = ('NEET UG', 'JEE Main / Advanced', 'TNEA')
LANGS = ('Tamil', 'English')

# ---- a light per-IP throttle (single Render worker; a multi-instance setup would use a shared store) ---------------------------------
_LOCK = threading.Lock()
_HITS = {}
RATE_WINDOW, RATE_MAX = 3600, 8


def rate_ok(ip):
    now = time.time()
    with _LOCK:
        hits = [t for t in _HITS.get(ip, []) if now - t < RATE_WINDOW]
        if len(hits) >= RATE_MAX:
            _HITS[ip] = hits
            return False
        hits.append(now)
        _HITS[ip] = hits
        if len(_HITS) > 5000:
            for k in list(_HITS):
                _HITS[k] = [t for t in _HITS[k] if now - t < RATE_WINDOW]
                if not _HITS[k]:
                    del _HITS[k]
    return True


def digits(v):
    d = re.sub(r'\D', '', str(v or ''))
    if len(d) == 12 and d.startswith('91'):
        d = d[2:]
    if len(d) == 11 and d.startswith('0'):
        d = d[1:]
    return d


def _s(v, n):
    return re.sub(r'\s+', ' ', str(v or '')).strip()[:n]


def validate(d, cfg=NKP):
    """(clean, error_en, error_ta). The error is for the first problem found."""
    name, school = _s(d.get('studentName'), 160), _s(d.get('school'), 200)
    stream = _s(d.get('stream'), 20)
    adm = [a for a in (d.get('admissions') or []) if a in ADMISSIONS] if isinstance(d.get('admissions'), list) else []
    mobile, pm = digits(d.get('mobile')), digits(d.get('parentMobile'))
    email, parent = _s(d.get('email'), 200).lower(), _s(d.get('parentName'), 160)
    code = _s(d.get('code'), 20).upper()
    lang = d.get('guidanceLanguage') if d.get('guidanceLanguage') in LANGS else 'Tamil'

    def bad(en, ta):
        return None, en, ta
    if len(name) < 2:
        return bad('Please enter the student\'s full name.', 'மாணவரின் முழுப் பெயரை உள்ளிடவும்.')
    if len(school) < 3:
        return bad('Please enter the school name.', 'பள்ளியின் பெயரை உள்ளிடவும்.')
    if stream not in STREAMS:
        return bad('Please choose the stream or group.', 'பிரிவை தேர்ந்தெடுக்கவும்.')
    if not re.fullmatch(r'[6-9]\d{9}', mobile):
        return bad('Enter a valid 10-digit mobile number.', 'சரியான 10 இலக்க மொபைல் எண்ணை உள்ளிடவும்.')
    if not adm:
        return bad('Choose at least one admission you are preparing for.', 'குறைந்தது ஒரு சேர்க்கையைத் தேர்ந்தெடுக்கவும்.')
    if not re.fullmatch(r'[^\s@]+@[^\s@]+\.[^\s@]{2,}', email):
        return bad('Enter a valid email address.', 'சரியான மின்னஞ்சல் முகவரியை உள்ளிடவும்.')
    if len(parent) < 2:
        return bad('Please enter the parent or guardian name.', 'பெற்றோர் / பாதுகாவலர் பெயரை உள்ளிடவும்.')
    if pm and not re.fullmatch(r'[6-9]\d{9}', pm):
        return bad('Enter a valid 10-digit parent mobile number, or leave it empty.', 'சரியான பெற்றோர் மொபைல் எண்ணை உள்ளிடவும் அல்லது காலியாக விடவும்.')
    if code != cfg['code']:
        return bad(f'Please enter the code {cfg["code"]}.', f'குறியீடு {cfg["code"]} ஐ உள்ளிடவும்.')
    if d.get('consent') is not True:
        return bad('Please tick the box to continue.', 'தொடர பெட்டியைத் தேர்ந்தெடுக்கவும்.')
    return dict(name=name, school=school, stream=stream, admissions=', '.join(adm), mobile='+91' + mobile, email=email, parent_name=parent,
                parent_mobile=('+91' + pm) if pm else '', language=lang, code=code,
                page_language='ta' if d.get('pageLanguage') == 'ta' else 'en'), '', ''


def _reference(cfg):
    from app.routes.membership import _allocate     # the shared, transaction-safe numbering used by membership applications
    return _allocate('ref_' + cfg['slug'][:20], cfg['prefix'])


def register(clean, ip='', cfg=NKP):
    """Store a registration. A second registration with the same email or mobile for the same campaign returns the first one."""
    dup = CampaignRegistration.query.filter(CampaignRegistration.campaign == cfg['campaign'],
                                            db.or_(db.func.lower(CampaignRegistration.email) == clean['email'], CampaignRegistration.mobile == clean['mobile'])
                                            ).order_by(CampaignRegistration.id).first()
    if dup:
        return dup, False
    r = CampaignRegistration(campaign=cfg['campaign'], code=clean['code'], name=clean['name'], school=clean['school'], stream=clean['stream'],
                             admissions=clean['admissions'], mobile=clean['mobile'], email=clean['email'], parent_name=clean['parent_name'],
                             parent_mobile=clean['parent_mobile'] or None, language=clean['language'], page_language=clean['page_language'],
                             consent=True, consent_at=datetime.now(timezone.utc).replace(tzinfo=None), ip=(ip or '')[:64], status='New')
    r.reference = _reference(cfg)
    db.session.add(r)
    db.session.commit()
    return r, True


def _password():
    alphabet = string.ascii_letters.replace('l', '').replace('I', '').replace('O', '') + string.digits.replace('0', '').replace('1', '')
    return ''.join(secrets.choice(alphabet) for _ in range(10))


def activate(r, admin_id, days=None, notify=True, cfg=NKP):
    """Verify -> complimentary Premium access. Returns (message, temp_password or None). Creates the login, or upgrades an existing account;
    never lowers an Elite or staff account. The temporary password is returned once so the admin can pass it on if email is not configured."""
    days = max(1, min(int(days or cfg['access_days']), 1100))
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    user = User.query.filter(db.func.lower(User.email) == r.email.lower()).first()
    pw = None
    if user is None:
        pw = _password()
        user = User(name=r.name, email=r.email, tier='premium', tier_expires_at=now + timedelta(days=days),
                    password_hash=bcrypt.generate_password_hash(pw).decode())
        db.session.add(user)
        db.session.flush()
        msg = f'Account created for {r.email}.'
    else:
        if user.tier in ('admin', 'ea_mentor', 'mentor'):
            msg = f'{r.email} is a staff account: its access was not changed.'
        else:
            live = user.tier in ('premium', 'elite') and (user.tier_expires_at is None or user.tier_expires_at > now)
            if not live:
                user.tier = 'premium'                                   # free or lapsed: switch the complimentary access on
            if user.tier_expires_at is not None or not live:             # an open-ended paid membership is left as it is
                user.tier_expires_at = max(user.tier_expires_at or now, now + timedelta(days=days))
            msg = f'Existing account {r.email} upgraded (an existing membership is never shortened).'
    r.user_id, r.status, r.handled_by, r.handled_at = user.id, 'Activated', admin_id, now
    r.access_until = user.tier_expires_at
    db.session.commit()
    sent = False
    if notify:
        sent = send_welcome(r, user, pw)
    return msg + (f' Complimentary access until {user.tier_expires_at.strftime("%d %b %Y")}.' if user.tier_expires_at else '') + \
        (' Login details emailed.' if sent else (' Email is not configured: share the login yourself.' if notify else '')), pw


def send_welcome(r, user, password=None):
    """Email the welcome (with the login for a new account). Returns True if an email transport is configured."""
    from flask import url_for
    from app.services import mailer
    if not mailer.is_configured():
        return False
    first = (r.name or 'there').split(' ')[0]
    login = url_for('auth.login', _external=True)
    until = user.tier_expires_at.strftime('%d %b %Y') if user.tier_expires_at else 'open-ended'
    ta = r.language == 'Tamil'
    if password:
        creds = f'\n  Login page : {login}\n  Email      : {user.email}\n  Password   : {password}\n'
    else:
        creds = f'\n  Login page : {login}\n  Use your existing EduAakashaa password (or "Forgot password" on the login page).\n'
    text = (f'Hi {first},\n\nYour complimentary EduAakashaa membership is active (Neikkarapatti & Palani, Class of 2027). It covers NEET, JEE and TNEA '
            f'guidance until {until}.\n{creds}\nPlease change the password after your first login. Questions? WhatsApp +91 80157 22706.\n\n— Team EduAakashaa')
    if ta:
        text += (f'\n\nவணக்கம் {first}, உங்கள் இலவச EduAakashaa உறுப்பினர் கணக்கு செயல்பட்டுள்ளது ({until} வரை). மேலே உள்ள விவரங்களுடன் உள்நுழையவும்.')
    mailer.send_async(user.email, 'Your complimentary EduAakashaa membership is active', text)
    return True


def notify_team(r):
    """Heads-up to the team inbox; best effort."""
    from app.services import mailer
    mailer.notify_admin(f'New {NKP["code"]} registration: {r.name} ({r.reference})',
                        f'{r.name}\nSchool: {r.school}\nStream: {r.stream}\nAdmissions: {r.admissions}\nMobile: {r.mobile}\nEmail: {r.email}\n'
                        f'Parent: {r.parent_name} {r.parent_mobile or ""}\nGuidance language: {r.language}\n\nVerify and activate in Admin > Campaign registrations.')


def send_received(r):
    from app.services import mailer
    if not mailer.is_configured():
        return
    first = (r.name or '').split(' ')[0]
    mailer.send_async(r.email, 'We received your EduAakashaa registration',
                      f'Hi {first},\n\nThank you for registering for the complimentary membership for Grade 12 students of Neikkarapatti & Palani '
                      f'(reference {r.reference}). Our team will confirm your details and send your portal login on WhatsApp or email.\n\n— Team EduAakashaa')
