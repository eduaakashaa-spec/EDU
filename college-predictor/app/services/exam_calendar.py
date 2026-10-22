"""Exam catalogue, focus lists, calendar invitations (.ics) and schedule-change alerts.

Admins maintain the catalogue (`MsExam`). Every add / change / removal creates an in-portal alert for everyone
with a mentorship role (students, parents, mentors) and — only when a mail transport is configured — an email
from info@. Students and mentors choose which exams to focus on (`MsExamFocus`, per student record).
"""
from datetime import date, datetime, timedelta, timezone
from urllib.parse import quote

from app.extensions import db
from app.models import User
from app.models_mentorship import (MsAlert, MsAlertRead, MsEnrolment, MsExam, MsExamFocus, MsParentLink)
from app.services import mailer
from app.services.email_templates import SITE, branded_shell

CATEGORIES_BY_NAME = {'JEE Main': 'JEE Main', 'JEE Advanced': 'JEE Advanced'}

# Dates below mirror the public /exam-schedule page (checked October 2026). Status says how firm each is;
# 'Expected' rows show only the likely window. Admin can edit any row — edits trigger alerts to members.
D = date
DEFAULT_EXAMS = [
    # (name, category, stream, starts_on, ends_on, status, window_note, source)
    ('JEE Main 2027 — Session 1', 'JEE Main', 'B.Tech/B.E.', D(2027, 1, 22), D(2027, 1, 30), 'Tentative',
     '22–24 & 28–30 Jan (buffer 31 Jan); provisional NTA calendar', 'NTA exam calendar, published 16 Sep 2026 (nta.ac.in)'),
    ('JEE Main 2027 — Session 2', 'JEE Main', 'B.Tech/B.E.', D(2027, 4, 1), D(2027, 4, 30), 'Expected',
     'Window only — April 2027, dates awaited', 'Not announced; inferred from earlier cycles'),
    ('JEE Advanced 2027', 'JEE Advanced', 'B.Tech/B.E.', D(2027, 5, 10), D(2027, 5, 24), 'Expected',
     'Window only — mid-May 2027, JAB notice awaited', 'Not announced; see jeeadv.ac.in'),
    ('UCEED 2027', 'Admission deadline', 'B.Des', D(2027, 1, 17), None, 'Confirmed',
     'Registration till 31 Oct 2026 (late fee till 6 Nov)', 'IIT Bombay — uceed.iitb.ac.in'),
    ('CEED 2027', 'Admission deadline', 'B.Des', D(2027, 1, 17), None, 'Confirmed',
     'Registration till 31 Oct 2026 (late fee till 6 Nov)', 'IIT Bombay — ceed.iitb.ac.in'),
    ('NID DAT 2027 — Prelims', 'Admission deadline', 'B.Des', D(2026, 12, 20), None, 'Confirmed',
     'Registration till 30 Nov 2026', 'NID Admissions Handbook 2027–28 — admissions.nid.edu'),
    ('NIFT 2027', 'Admission deadline', 'B.Des', D(2027, 1, 10), None, 'Tentative',
     'Registration 16 Oct – 16 Nov 2026 (late fee till 21 Nov)', 'NTA NIFT 2027 notification, 16 Oct 2026; confirm on nift.ac.in'),
    ('AEEE 2027 (Amrita)', 'Admission deadline', 'B.Tech/B.E.', D(2027, 4, 15), D(2027, 5, 7), 'Confirmed',
     'Registration opens Nov 2026', 'Amrita Vishwa Vidyapeetham — amrita.edu'),
    ('BITSAT 2027', 'Admission deadline', 'B.Tech/B.E.', D(2027, 4, 1), D(2027, 6, 15), 'Expected',
     'Registration from Dec 2026; session dates awaited', 'BITS Pilani admission portal'),
    ('VITEEE 2027', 'Admission deadline', 'B.Tech/B.E.', D(2027, 4, 27), D(2027, 5, 2), 'Tentative',
     'Applications 20 Oct 2026 – 31 Mar 2027; exam 27 Apr – 2 May (tentative per VIT)', 'VIT — viteee.vit.ac.in'),
    ('SRMJEEE 2027', 'Admission deadline', 'B.Tech/B.E.', D(2027, 4, 1), D(2027, 7, 15), 'Expected',
     'Three phases (Apr / Jun / Jul); registration from Nov 2026', 'SRMIST — srmist.edu.in'),
    ('KCET 2027', 'Admission deadline', 'B.Tech/B.E.', D(2027, 4, 1), D(2027, 4, 30), 'Expected',
     'Window only — April 2027', 'KEA Karnataka'),
    ('MHT CET 2027', 'Admission deadline', 'B.Tech/B.E.', D(2027, 4, 1), D(2027, 5, 31), 'Expected',
     'Window only — Apr–May 2027', 'CET Cell Maharashtra'),
    ('WBJEE 2027', 'Admission deadline', 'B.Tech/B.E.', D(2027, 4, 20), D(2027, 5, 10), 'Expected',
     'Window only — late Apr / early May 2027', 'WBJEEB'),
    ('KEAM 2027', 'Admission deadline', 'B.Tech/B.E.', D(2027, 4, 1), D(2027, 5, 31), 'Expected',
     'Window only — Apr–May 2027', 'CEE Kerala'),
    ('TG-EAPCET / AP-EAPCET 2027', 'Admission deadline', 'B.Tech/B.E.', D(2027, 5, 1), D(2027, 5, 31), 'Expected',
     'Window only — May 2027 (2026: 9–18 May)', 'TSCHE / APSCHE'),
    ('CUET UG 2027', 'Admission deadline', 'B.Tech/B.E.', D(2027, 5, 10), D(2027, 5, 31), 'Expected',
     'Window only — May 2027 (2026: 11–31 May)', 'NTA — cuet.nta.nic.in'),
    ('IISER IAT 2027', 'Admission deadline', 'Research/Science', D(2027, 6, 1), D(2027, 6, 10), 'Expected',
     'Window only — early June 2027', 'IISER admissions'),
    ('NEST 2027', 'Admission deadline', 'Research/Science', D(2027, 6, 1), D(2027, 6, 7), 'Tentative',
     'First week of June 2027', 'NISER / UM-DAE CEBS'),
    ('NATA 2027', 'Admission deadline', 'B.Arch', D(2027, 3, 1), D(2027, 8, 31), 'Expected',
     'Multi-session; Council of Architecture brochure awaited (2026: Mar–Aug)', 'Council of Architecture'),
]

TRACKED = ('name', 'starts_on', 'ends_on', 'status', 'window_note', 'source', 'active')


def ensure_default_exams():
    """Idempotent by name; returns how many were added. Does NOT raise alerts (it is a seed, not news)."""
    have = {x.name for x in MsExam.query.all()}
    added = 0
    for name, cat, stream, a, b, status, note, src in DEFAULT_EXAMS:
        if name in have:
            continue
        db.session.add(MsExam(name=name, category=cat, stream=stream, starts_on=a, ends_on=b, status=status,
                              window_note=note, source=src, verified_on=date(2026, 10, 16)))
        added += 1
    db.session.commit()
    return added


def fmt_range(x):
    a, b = x.starts_on, x.ends_on
    if not b or b == a:
        return a.strftime('%d %b %Y')
    if a.year == b.year and a.month == b.month:
        return f"{a.strftime('%d')}–{b.strftime('%d %b %Y')}"
    return f"{a.strftime('%d %b %Y')} – {b.strftime('%d %b %Y')}"


def _snap(x):
    return {k: getattr(x, k) for k in TRACKED}


def snapshot(x):
    return _snap(x)


def _diff_text(before, after):
    parts = []
    if before['starts_on'] != after['starts_on'] or before['ends_on'] != after['ends_on']:
        class _R:  # tiny adapter so fmt_range works on dicts
            def __init__(s, d):
                s.starts_on, s.ends_on = d['starts_on'], d['ends_on']
        parts.append(f"Dates: {fmt_range(_R(before))} → {fmt_range(_R(after))}")
    if before['status'] != after['status']:
        parts.append(f"Status: {before['status']} → {after['status']}")
    if before['name'] != after['name']:
        parts.append(f"Name: {before['name']} → {after['name']}")
    if before['window_note'] != after['window_note'] and after['window_note']:
        parts.append(f"Note: {after['window_note']}")
    if before['source'] != after['source'] and after['source']:
        parts.append(f"Source: {after['source']}")
    if before['active'] and not after['active']:
        parts.append('Removed from the schedule')
    return '; '.join(parts)


def record_change(exam, before=None):
    """Create the alert for an add (before=None) or a change; bump the version. Returns the alert or None."""
    if before is None:
        alert = MsAlert(exam_id=exam.id, kind='new', title=f'New exam added: {exam.name}',
                        detail=f"{fmt_range(exam)} · {exam.status}" + (f" · {exam.window_note}" if exam.window_note else ''))
    else:
        after = _snap(exam)
        text = _diff_text(before, after)
        if not text:
            return None                                  # nothing the reader cares about changed
        exam.version = (exam.version or 1) + 1
        removed = before['active'] and not after['active']
        alert = MsAlert(exam_id=exam.id, kind='removed' if removed else 'changed',
                        title=('Exam removed: ' if removed else 'Schedule change: ') + exam.name, detail=text)
    db.session.add(alert)
    db.session.flush()
    return alert


# --------------------------------------------------------------------------- #
# who gets told
# --------------------------------------------------------------------------- #
def audience_emails():
    """Distinct emails of every student, linked parent and mentor on an Active enrolment."""
    ids = set()
    for e in MsEnrolment.query.filter_by(status='Active').all():
        ids.add(e.student_id)
        if e.mentor_id:
            ids.add(e.mentor_id)
        ids.update(l.parent_id for l in MsParentLink.query.filter_by(enrolment_id=e.id).all())
    if not ids:
        return []
    return sorted({u.email for u in User.query.filter(User.id.in_(ids)).all() if u.email})


def email_alert(alert):
    """Best-effort email (from info@) — only when a mail transport is configured. Returns the count queued."""
    if not mailer.is_configured():
        return 0
    subject = '[EduAakashaA] ' + alert.title
    link = SITE + '/mentorship/'
    text = f"{alert.title}\n{alert.detail or ''}\n\nOpen your mentorship calendar to add or review it: {link}\n" \
           "Dates marked tentative or expected can still change — always confirm on the official notice.\n"
    body = (f'<h2 style="margin:0 0 8px;color:#0E3A8A;font-family:Georgia,serif">{_esc(alert.title)}</h2>'
            f'<p style="font-size:15px;line-height:1.55">{_esc(alert.detail or "")}</p>'
            f'<p><a href="{link}" style="background:#FF6B0A;color:#fff;text-decoration:none;padding:10px 18px;border-radius:999px;'
            'font-weight:700">Open my calendar</a></p>'
            '<p style="font-size:12px;color:#5A6278">Tentative or expected dates can change — confirm on the official notice.</p>')
    return mailer.send_bulk(audience_emails(), subject, text, branded_shell(body),
                            from_addr=mailer.INFO_FROM, reply_to=mailer.INFO_FROM)


def _esc(s):
    from markupsafe import escape
    return str(escape(s))


# --------------------------------------------------------------------------- #
# alerts per user
# --------------------------------------------------------------------------- #
def unread_alerts(user, days=45, limit=12):
    since = datetime.now(timezone.utc).replace(tzinfo=None) - timedelta(days=days)
    read = db.session.query(MsAlertRead.alert_id).filter(MsAlertRead.user_id == user.id)
    return (MsAlert.query.filter(MsAlert.created_at >= since, ~MsAlert.id.in_(read))
            .order_by(MsAlert.id.desc()).limit(limit).all())


def mark_read(user, alert_ids):
    have = {r.alert_id for r in MsAlertRead.query.filter(MsAlertRead.user_id == user.id, MsAlertRead.alert_id.in_(alert_ids))}
    for aid in set(alert_ids) - have:
        db.session.add(MsAlertRead(alert_id=aid, user_id=user.id))


# --------------------------------------------------------------------------- #
# calendar invitations
# --------------------------------------------------------------------------- #
def _ics_escape(s):
    return (s or '').replace('\\', '\\\\').replace(';', '\\;').replace(',', '\\,').replace('\r', '').replace('\n', '\\n')


def _fold(line):
    out = []
    while len(line.encode('utf-8')) > 74:
        cut = 74
        while len(line[:cut].encode('utf-8')) > 74:
            cut -= 1
        out.append(line[:cut])
        line = ' ' + line[cut:]
    out.append(line)
    return '\r\n'.join(out)


def description(x):
    custom = getattr(x, 'ics_description', None)      # public exam-schedule page supplies its own text
    if custom:
        return custom
    bits = [f'Status: {x.status}.']
    if x.window_note:
        bits.append(x.window_note + '.')
    if x.source:
        bits.append(f'Source: {x.source}.')
    bits.append('Verified ' + x.verified_on.strftime('%d %b %Y') + '.' if x.verified_on else 'Not yet verified.')
    if x.status != 'Confirmed':
        bits.append('This date is not final — confirm on the official notice. You will be alerted in the portal if it changes.')
    return ' '.join(bits)


def make_ics(exams, name='EduAakashaA exams'):
    now = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    lines = ['BEGIN:VCALENDAR', 'VERSION:2.0', 'PRODID:-//EduAakashaA//Mentorship Portal//EN', 'CALSCALE:GREGORIAN',
             'METHOD:PUBLISH', 'X-WR-CALNAME:' + _ics_escape(name)]
    for x in exams:
        end = (x.ends_on or x.starts_on) + timedelta(days=1)         # DTEND is exclusive for all-day events
        lines += ['BEGIN:VEVENT', f'UID:exam-{x.id}@eduaakashaa.com', f'DTSTAMP:{now}', f'SEQUENCE:{max((x.version or 1) - 1, 0)}',
                  f'DTSTART;VALUE=DATE:{x.starts_on.strftime("%Y%m%d")}', f'DTEND;VALUE=DATE:{end.strftime("%Y%m%d")}',
                  'SUMMARY:' + _ics_escape(x.name + ('' if x.status == 'Confirmed' else f' ({x.status.lower()})')),
                  'DESCRIPTION:' + _ics_escape(description(x)),
                  'STATUS:' + ('CONFIRMED' if x.status == 'Confirmed' else ('CANCELLED' if x.status == 'Cancelled' else 'TENTATIVE')),
                  'TRANSP:TRANSPARENT', 'URL:' + SITE + '/exam-schedule',
                  'BEGIN:VALARM', 'ACTION:DISPLAY', 'DESCRIPTION:Tomorrow: ' + _ics_escape(x.name), 'TRIGGER:-P1D', 'END:VALARM',
                  'END:VEVENT']
    lines.append('END:VCALENDAR')
    return ('\r\n'.join(_fold(l) for l in lines) + '\r\n').encode('utf-8')


def gcal_link(x):
    end = (x.ends_on or x.starts_on) + timedelta(days=1)
    return ('https://calendar.google.com/calendar/render?action=TEMPLATE&text=' + quote(x.name) +
            f'&dates={x.starts_on.strftime("%Y%m%d")}/{end.strftime("%Y%m%d")}&details=' + quote(description(x)))
