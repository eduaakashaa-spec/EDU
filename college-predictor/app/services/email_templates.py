"""Email template registry for /admin/templates.

Each template card has one or more "versions" (a version selector shows when
there is more than one). `subject` / `text` / `html` carry {placeholders}
filled client-side from that version's fields. The `html` is the email body
only — it is wrapped in the branded shell (logo header + footer) client-side,
so every email looks identical without repeating the chrome here.

Nothing is auto-sent: the admin opens a ready draft (Gmail compose / mailto)
or copies the formatted email and pastes it into Gmail.
"""

import html
import re

SENDER_EMAIL = 'eduaakashaa@gmail.com'      # Gmail drafts / reply-to identity
FOOTER_EMAIL = 'info@eduaakashaa.com'       # shown in every email footer
WHATSAPP_NUMBER = '+91-80157 22706'
# EduAakashaa is registered and operates in India only — no UAE/Dubai
# establishment or contact number anywhere in customer-facing copy.
SITE = 'https://www.eduaakashaa.com'
LOGO_URL = SITE + '/static/images/logo.png'


def _f(key, label, default=''):
    return {'key': key, 'label': label, 'default': default}


# --------------------------------------------------------------------------- #
# Announcement starters (admin → Broadcast → Announcements).
# Simpler than the email registry on purpose: an announcement is just a title +
# message, and the admin edits it inline right after picking, so these only need
# to prefill the form — no {placeholders} or versions to resolve.
# --------------------------------------------------------------------------- #
ANNOUNCEMENT_TEMPLATES = [
    {'key': 'jee_main_reg', 'icon': '📝', 'label': 'JEE Main 2027 Session 1: next steps',
     'title': 'JEE Main 2027 Session 1: registration has closed. What happens next',
     'body': ('JEE Main 2027 Session 1 registration closed on 22 November 2026 (late-fee window 23 to 26 November). '
              'NTA has opened a one-time correction window from 27 to 29 November, until 11:50 pm, at '
              'jeemain.nta.nic.in: check your form now, because some fields cannot be changed. '
              'The exam city slip is due on 30 December and the admit card on 13 January 2027. '
              'Session 1 exams are on 20, 21, 22, 23, 24 and 28 January 2027. '
              'Session 2 is proposed for 2 to 7 April 2027, with registration from 5 January to 3 February; '
              'NTA will confirm these by a separate notice. JEE Advanced is on Sunday 23 May 2027. '
              'Please confirm all dates on jeemain.nta.nic.in.')},
    {'key': 'deadlines_fortnight', 'icon': '⏳', 'label': 'Deadlines in the next two weeks',
     'title': 'Admission deadlines in the next two weeks (checked 28 November 2026)',
     'body': ('Dates to act on now: NID DAT registration closes on 30 November at 11:59 pm. '
              'TISS programmes that use CAT close on 4 December, 5 pm. CLAT 2027 is on Sunday 6 December, 2 to 4 pm; '
              'download the admit card before 1:30 pm that day. IIFT MBA (IB) applications are shown as extended to '
              '8 December: confirm on iift.ac.in. AILET 2027 is on Sunday 13 December; the admit card has been out since '
              '24 November. CMAT 2027 registration is open until 20 December, and the exam has moved to 11 February 2027. '
              'Please confirm each date on the official site before acting. The full list is on our Exam Schedule page.')},
    {'key': 'results', 'icon': '📢', 'label': 'Results / list out',
     'title': 'DASA Round-1 results are out',
     'body': ('Round-1 seat allotment results have been published. Log in to the official '
              'portal to check your allotment, then accept or float before the deadline. '
              'Message us if you want help reading your result.')},
    {'key': 'deadline', 'icon': '⏰', 'label': 'Deadline reminder',
     'title': 'Choice locking closes this Friday',
     'body': ('A reminder that choice locking closes this Friday at 5 PM. Choices not locked '
              'are auto-locked as they stand — please review your order before then.')},
    {'key': 'schedule', 'icon': '🗓️', 'label': 'Schedule change',
     'title': 'Counselling schedule updated',
     'body': ('The counselling schedule has been revised. The updated dates are on your '
              'dashboard under upcoming events. No action is needed from you right now.')},
    {'key': 'webinar', 'icon': '🎥', 'label': 'Webinar / live session',
     'title': 'Live session this Sunday, 6 PM',
     'body': ('We are running a live Q&A this Sunday at 6 PM covering choice filling and '
              'branch selection. Bring your questions — the joining link will be shared here '
              'a day before.')},
    {'key': 'docs', 'icon': '📄', 'label': 'Documents reminder',
     'title': 'Keep your documents ready',
     'body': ('Please keep your marksheets, ID proof and category certificates scanned and '
              'ready. Having them on hand saves time when the verification window opens.')},
    {'key': 'maintenance', 'icon': '🛠️', 'label': 'Maintenance notice',
     'title': 'Brief maintenance on Saturday night',
     'body': ('The site will be briefly unavailable on Saturday between 11 PM and midnight '
              'while we ship an update. Nothing you have saved will be affected.')},
]


# --------------------------------------------------------------------------- #
# Server-side rendering — lets routes auto-send these same templates instead of
# duplicating the copy. The admin composer still renders client-side for live
# preview; `branded_shell` below is the twin of wrapHtml() in
# templates/admin/templates.html — change both together.
# --------------------------------------------------------------------------- #
def branded_shell(body_html, signature=True):
    """Wrap an email body in the standard chrome (logo header, accent bar,
    signature, footer). Inline styles only — email clients strip <style>."""
    return (
        '<div style="background:#F1EADB;padding:26px 12px;font-family:Arial,Helvetica,sans-serif">'
        '<div style="max-width:560px;margin:0 auto;background:#ffffff;border:1px solid #E8DFC8;'
        'border-radius:16px;overflow:hidden">'
        '<div style="background:#0E3A8A;padding:20px 28px">'
        '<table role="presentation" cellpadding="0" cellspacing="0" style="border-collapse:collapse"><tr>'
        f'<td style="vertical-align:middle;padding-right:12px"><img src="{LOGO_URL}" width="40" '
        'height="40" alt="EduAakashaa" style="display:block;background:#ffffff;border-radius:10px;padding:3px"></td>'
        '<td style="vertical-align:middle">'
        '<div style="font-size:19px;font-weight:700;line-height:1.2">'
        '<span style="color:#ffffff">Edu</span><span style="color:#FF9350">Aakashaa</span></div>'
        '<div style="color:#B9C6E8;font-size:11px;letter-spacing:.04em">Choose right. '
        'Engineering admissions, guided honestly.</div></td></tr></table></div>'
        '<div style="height:4px;background:linear-gradient(90deg,#FF6B0A,#FFB25A)"></div>'
        f'<div style="padding:28px;color:#0E1B3D;font-size:15px;line-height:1.65">{body_html}'
        + ('<p style="margin:26px 0 0">Warm regards,<br><strong>Team EduAakashaa</strong><br>'
           '<span style="color:#5A6278;font-size:13px">Coimbatore, India</span></p>' if signature else '') + '</div>'
        '<div style="padding:18px 28px;background:#FBF7EE;border-top:1px solid #E8DFC8;'
        'color:#5A6278;font-size:12px;line-height:1.7">'
        '<strong style="color:#0E1B3D">EduAakashaa</strong> &middot; Evidence-based college guidance<br>'
        f'WhatsApp: {WHATSAPP_NUMBER}<br>'
        f'<a href="mailto:{FOOTER_EMAIL}" style="color:#0E3A8A">{FOOTER_EMAIL}</a>'
        '</div></div></div>')


def _fill(text, values, escape=False):
    """Replace {placeholders}; an unknown/blank value leaves the token as-is
    (same rule the composer uses, so previews and auto-sends agree)."""
    def sub(m):
        val = values.get(m.group(1))
        if val in (None, ''):
            return m.group(0)
        return html.escape(str(val)) if escape else str(val)
    return re.sub(r'\{(\w+)\}', sub, text)


def render_email(key, values, version='default'):
    """→ (subject, text, html) for a registry template, ready to hand to the
    mailer. Raises KeyError if the template key is unknown."""
    tpl = next((t for t in EMAIL_TEMPLATES if t['key'] == key), None)
    if tpl is None:
        raise KeyError(f'unknown email template: {key}')
    ver = next((v for v in tpl['versions'] if v['key'] == version), tpl['versions'][0])
    return (_fill(ver['subject'], values),
            _fill(ver['text'], values),
            branded_shell(_fill(ver['html'], values, escape=True), signature=not ver.get('nosig')))


def _btn(url, label):
    """Inline-styled CTA button that survives Gmail's CSS sanitiser."""
    return ('<p style="margin:24px 0 8px"><a href="' + url + '" '
            'style="background:#0E3A8A;color:#ffffff;text-decoration:none;'
            'padding:12px 28px;border-radius:999px;font-weight:700;font-size:14px;'
            'display:inline-block">' + label + '</a></p>')

JOIN_LINK = SITE + '/join-our-team?ref=email#register'


def _banner(filename, alt):
    """Full-width banner image linking to the register-interest page. JPG (not WebP) so Outlook and older clients show it; absolute URL, as email needs."""
    return ('<p style="margin:0 0 18px"><a href="{link}"><img src="' + SITE + '/static/img/email/' + filename + '" width="504" alt="' + alt + '" '
            'style="display:block;width:100%;max-width:504px;height:auto;border:0;border-radius:12px"></a></p>')


def _perks(items):
    """A simple inline-styled bullet list that survives Gmail's CSS sanitiser."""
    return ('<ul style="margin:8px 0 4px;padding-left:20px;color:#0E1B3D">'
            + ''.join('<li style="margin:4px 0">' + i + '</li>' for i in items) + '</ul>')

NOTE_HTML = '<p style="color:#5A6278;font-size:13px">It takes about two minutes and only registers your interest. Our team will contact you to talk about the next steps.</p>'



# ---- School counsellor outreach -------------------------------------------------------------------------------------------------------
_SCHOOL_LINKS = [
    (SITE + '/free-guides', 'Free Student Guides'),
    (SITE + '/edupulse-free-mock-tests/', 'Free Sample Mock Tests (9 samples, sign-up needed)'),
    (SITE + '/josaa', 'JoSAA Predictor'),
    (SITE + '/dasa-admissions-guide', 'DASA / CIWG Admissions Guide'),
    (SITE + '/nirf-ranking', 'NIRF Explorer (college rankings)'),
    (SITE + '/class12-pcm/', 'Class 12 PCM Analytics'),
    (SITE + '/class12-pcb/', 'Class 12 PCB Analytics'),
    (SITE + '/tneamatrix', 'TNEA Seat Matrix'),
    (SITE + '/free-report', 'Free TNEA Report: 3,448 college \u00d7 branch cut-off rows, no sign-up'),
]


def _school_panel(n):
    """The "free on the portal" box of the outreach emails (first n links)."""
    li = ''.join('<li style="margin:3px 0"><a href="%s" style="color:#0E3A8A">%s</a></li>' % (u, t) for u, t in _SCHOOL_LINKS[:n])
    return ('<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#FBF7EE;border-left:4px solid #FF6B0A;margin:8px 0 16px">'
            '<tr><td style="padding:12px 16px;font-size:14px;line-height:1.6"><strong style="color:#0E3A8A">Free on the EduAakashaA portal for students and parents</strong>'
            '<ul style="padding-left:18px;margin:6px 0 0">' + li + '</ul></td></tr></table>')


def _school_panel_text(n):
    return 'Free on the EduAakashaA portal for students and parents:\n' + ''.join('- %s: %s\n' % (t, u) for u, t in _SCHOOL_LINKS[:n])


_SIGN_HTML = ('<p style="margin:22px 0 0">Warm regards,<br><strong style="color:#0E3A8A">{sender}</strong><br>{role}<br>'
              'WhatsApp ' + WHATSAPP_NUMBER + ' | ' + FOOTER_EMAIL + '<br><a href="' + SITE + '" style="color:#FF6B0A">www.EduAakashaA.com</a></p>'
              '<p style="font-style:italic;color:#5A6278;font-size:13px;margin:14px 0 0">Guiding students towards the right future.</p>')
_SIGN_TEXT = ('Warm regards,\n{sender}\n{role}\nWhatsApp ' + WHATSAPP_NUMBER + ' | ' + FOOTER_EMAIL + '\nwww.EduAakashaA.com')
_SCHOOL_FIELDS = [_f('counsellor', 'Counsellor name', 'Career Counsellor'), _f('school', 'School name', '[School name]'),
                  _f('sender', 'Your name', 'Sabira Banu'), _f('role', 'Your title', 'Founder, EduAakashaA')]
_UNSUB_TEXT = 'You are receiving this because your role is listed publicly on your school\u2019s website. Reply \u201cunsubscribe\u201d and we will not contact you again.'

SCHOOL_OUTREACH = {
    'key': 'school-outreach', 'icon': '\U0001F3EB', 'label': 'School counsellor outreach', 'category': 'School outreach',
    # list sending from a CSV file: column -> the field it fills (email is the recipient); the sample rows make the downloadable template
    'csv': {'columns': [['email', 'Email (required)'], ['school', 'School name (required)'], ['counsellor', 'Counsellor name (optional)']],
            'sample': [['counsellor@exampleschool.ae', 'Example Indian High School', 'Ms Anita Rao'], ['info@anotherschool.qa', 'Another Indian School', '']],
            'filename': 'school-outreach-list.csv'},
    'desc': 'Offer a school counsellor a free session for Grade 11 and 12 families: first email, follow-up and a short version for a general school inbox, each with a WhatsApp message.',
    'versions': [
        {'key': 'initial', 'label': 'Initial outreach', 'nosig': True, 'fields': _SCHOOL_FIELDS,
         'subject': 'Free college-selection session for your Grade 11 & 12 families \u2013 {school}',
         'html': ('<p>Dear {counsellor},</p>'
                  '<p>I am {sender}, {role}, an education consultancy that guides Indian families abroad through engineering admissions in India, including <strong>DASA, CIWG, JoSAA</strong> and state pathways to NITs, IIITs and GFTIs.</p>'
                  '<p>As you support Grade 11 and 12 students at {school}, I would like to offer your school a <strong style="color:#FF6B0A">complimentary 45-minute session</strong> for students and parents:</p>'
                  + _perks(['How NRI / Gulf-based students can use the DASA and CIWG routes', 'Choosing branch and college using cut-offs, placements and ROI',
                            'Timeline: exams, registration and counselling rounds for the coming cycle', 'Live Q&amp;A, plus a free printable admissions checklist for each family'])
                  + _school_panel(9)
                  + '<p>The session can be online or at your campus, at a time that suits your calendar. There is no cost or obligation, and we will not contact families directly. Any follow-up happens only if a parent chooses to reach out to us.</p>'
                  '<p>May I send a short outline, or would a 10-minute call this week work for you?</p>' + _SIGN_HTML
                  + '<p style="font-size:12px;color:#5A6278;margin:16px 0 0">' + _UNSUB_TEXT + '</p>'),
         'text': ('Dear {counsellor},\n\nI am {sender}, {role}, an education consultancy that guides Indian families abroad through engineering admissions in India, including DASA, CIWG, JoSAA and state pathways to NITs, IIITs and GFTIs.\n\n'
                  'As you support Grade 11 and 12 students at {school}, I would like to offer your school a complimentary 45-minute session for students and parents:\n'
                  '- How NRI / Gulf-based students can use the DASA and CIWG routes\n- Choosing branch and college using cut-offs, placements and ROI\n- Timeline: exams, registration and counselling rounds for the coming cycle\n'
                  '- Live Q&A, plus a free printable admissions checklist for each family\n\n' + _school_panel_text(9)
                  + '\nThe session can be online or at your campus, at a time that suits your calendar. There is no cost or obligation, and we will not contact families directly. Any follow-up happens only if a parent chooses to reach out to us.\n\n'
                  'May I send a short outline, or would a 10-minute call this week work for you?\n\n' + _SIGN_TEXT + '\n\n' + _UNSUB_TEXT),
         'wa': ('Dear {counsellor}, I am {sender} from EduAakashaA. We guide Indian families abroad through engineering admissions in India (DASA, CIWG, JoSAA, state routes). '
                'May we offer {school} a free 45-minute session for Grade 11 and 12 students and parents, online or on campus? No cost or obligation, and we will not contact families directly. '
                'Free guides: ' + SITE + '/free-guides  Reply STOP and we will not message again.')},
        {'key': 'followup', 'label': 'Follow-up (after 5 to 7 days)', 'nosig': True, 'fields': _SCHOOL_FIELDS,
         'subject': 'Re: Free college-selection session for {school}',
         'html': ('<p>Dear {counsellor},</p><p>Just a gentle follow-up on my note about a free admissions guidance session for your Grade 11 and 12 families.</p>' + _school_panel(5)
                  + '<p>If a full session is not possible right now, I can instead share a <strong style="color:#FF6B0A">one-page DASA/CIWG guide</strong> that you may circulate to parents in whichever way you prefer. It is yours to use with no strings attached.</p>'
                  '<p>Would you like me to send it across?</p>' + _SIGN_HTML),
         'text': ('Dear {counsellor},\n\nJust a gentle follow-up on my note about a free admissions guidance session for your Grade 11 and 12 families.\n\n' + _school_panel_text(5)
                  + '\nIf a full session is not possible right now, I can instead share a one-page DASA/CIWG guide that you may circulate to parents in whichever way you prefer. It is yours to use with no strings attached.\n\n'
                  'Would you like me to send it across?\n\n' + _SIGN_TEXT),
         'wa': ('Dear {counsellor}, a gentle follow-up on our free admissions session for {school} Grade 11 and 12 families. If a session is not possible now, may I send a one-page DASA/CIWG guide you can share with parents? {sender}, EduAakashaA')},
        {'key': 'general', 'label': 'General school inbox', 'nosig': True, 'fields': _SCHOOL_FIELDS,
         'subject': 'For the Career Counsellor \u2013 free admissions session for Grade 11 & 12',
         'html': ('<p>Dear Sir/Madam,</p><p>Could you please forward this note to your Career Counsellor or Grade 11\u201312 coordinator?</p>'
                  '<p>EduAakashaA offers {school} a <strong style="color:#FF6B0A">free session</strong> on DASA, CIWG and engineering admissions in India for Gulf-based students and parents. It can be held online or on campus, with no cost or obligation.</p>'
                  + _school_panel(5) + '<p>If suitable, please share the counsellor\u2019s contact or reply here and I will send the outline.</p>' + _SIGN_HTML),
         'text': ('Dear Sir/Madam,\n\nCould you please forward this note to your Career Counsellor or Grade 11-12 coordinator?\n\nEduAakashaA offers {school} a free session on DASA, CIWG and engineering admissions in India for Gulf-based students and parents. It can be held online or on campus, with no cost or obligation.\n\n'
                  + _school_panel_text(5) + '\nIf suitable, please share the counsellor\u2019s contact or reply here and I will send the outline.\n\n' + _SIGN_TEXT),
         'wa': ('Dear Sir/Madam, please forward to your Career Counsellor: EduAakashaA offers {school} a free session on DASA, CIWG and engineering admissions in India for Grade 11 and 12 students and parents (online or on campus, no cost). {sender}, WhatsApp ' + WHATSAPP_NUMBER)},
    ],
}


# ---- Elite Mentorship (Grade 11 and Grade 12): students and parents -----------------------------------------------------------------
_EM_PAGE = SITE + '/elite-mentorship'
_EM_BROCHURE = SITE + '/static/docs/EduAakashaA-Elite-Mentorship-Brochure.pdf'
_EM_POSTER = SITE + '/static/img/elite/poster.jpg'
_EM_HERO = SITE + '/static/img/elite/hero.jpg'
_EM_WA = 'https://wa.me/918015722706?text=Hello%20EduAakashaA%2C%20I%20would%20like%20to%20book%20an%20initial%20discussion%20about%20Elite%20Mentorship.'
_EM_CHANNEL = 'https://whatsapp.com/channel/0029VbBxOWUKwqSYpWBgge1x'
_EM_FIELDS = [_f('name', 'Recipient first name', 'there'), _f('student', 'Student first name', 'your child'),
              _f('sender', 'Your name', 'Sabira Banu'), _f('role', 'Your title', 'Founder, EduAakashaA')]
_EM_NOTE = 'This is mentorship, not coaching. EduAakashaA cannot and does not guarantee a rank or a seat.'


def _em_hero(line1, line2):
    """Photo banner with the headline underneath, linking to the programme page."""
    return ('<a href="' + _EM_PAGE + '" style="text-decoration:none"><img src="' + _EM_HERO + '" width="504" alt="A mentor and a student working through a plan on a laptop" '
            'style="display:block;width:100%;max-width:504px;height:auto;border:0;border-radius:12px 12px 0 0"></a>'
            '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#071A44;border-radius:0 0 12px 12px;margin:0 0 18px"><tr>'
            '<td style="padding:16px 18px"><div style="font-family:Georgia,serif;font-size:21px;line-height:1.25;font-weight:700;color:#ffffff">' + line1 + '</div>'
            '<div style="font-family:Georgia,serif;font-size:21px;line-height:1.25;font-weight:700;font-style:italic;color:#FFB27A">' + line2 + '</div></td></tr></table>')


def _em_stats(items):
    """A row of big-number tiles: [(value, label)]."""
    w = str(100 // len(items))
    return ('<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="margin:6px 0 16px"><tr>'
            + ''.join('<td width="' + w + '%" style="padding:0 3px;vertical-align:top"><div style="background:#FBF7EE;border:1px solid #E8DFC8;border-radius:10px;padding:10px 6px;text-align:center">'
                      '<div style="font-size:21px;font-weight:700;color:#FF6B0A;line-height:1.1">' + v + '</div>'
                      '<div style="font-size:11px;color:#5A6278;line-height:1.35;margin-top:3px">' + l + '</div></div></td>' for v, l in items)
            + '</tr></table>')


def _em_icons(rows):
    """Icon rows: [(emoji, title, text)]. Each icon sits in a tinted circle."""
    return ('<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="margin:6px 0 14px">'
            + ''.join('<tr><td width="46" style="vertical-align:top;padding:7px 0"><div style="width:38px;height:38px;border-radius:19px;background:#FFF1E4;text-align:center;font-size:19px;line-height:38px">' + i + '</div></td>'
                      '<td style="vertical-align:top;padding:7px 0 7px 6px"><strong style="color:#0E3A8A">' + t + '</strong><br><span style="color:#3C465F;font-size:14px">' + d + '</span></td></tr>' for i, t, d in rows)
            + '</table>')


def _em_steps(steps):
    """Numbered roadmap: [(when, title, text)]."""
    return ('<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="margin:6px 0 14px">'
            + ''.join('<tr><td width="34" style="vertical-align:top;padding:6px 0"><div style="width:26px;height:26px;border-radius:13px;background:#0E3A8A;color:#ffffff;text-align:center;font-weight:700;font-size:13px;line-height:26px">' + str(n + 1) + '</div></td>'
                      '<td style="vertical-align:top;padding:6px 0 6px 4px;font-size:14px"><span style="color:#C24F00;font-weight:700;font-size:12px;letter-spacing:.04em">' + w.upper() + '</span><br><strong>' + t + '</strong> ' + d + '</td></tr>'
                      for n, (w, t, d) in enumerate(steps))
            + '</table>')


def _em_vs():
    return ('<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="margin:6px 0 16px;border:1px solid #E8DFC8;border-radius:10px;font-size:13.5px">'
            '<tr><td width="50%" style="padding:10px 12px;border-right:1px solid #E8DFC8;vertical-align:top"><strong>\U0001F4DA Coaching</strong><br>'
            '<span style="color:#3C465F">&ldquo;How do I solve this problem faster?&rdquo;<br>Builds marks and percentile.</span></td>'
            '<td width="50%" style="padding:10px 12px;background:#E3F2EA;vertical-align:top"><strong style="color:#14704A">\U0001F9ED Mentoring</strong><br>'
            '<span style="color:#3C465F">&ldquo;What am I aiming for, and is this the right route for me?&rdquo;<br>Decides what the marks are for.</span></td></tr></table>')


def _em_links():
    """Buttons: page, WhatsApp, then brochure and poster."""
    b = lambda url, label, bg, fg: ('<a href="' + url + '" style="background:' + bg + ';color:' + fg + ';text-decoration:none;padding:11px 20px;border-radius:999px;'  # noqa: E731
                                    'font-weight:700;font-size:14px;display:inline-block;margin:4px 6px 4px 0">' + label + '</a>')
    o = lambda url, label: ('<a href="' + url + '" style="border:1.5px solid #0E3A8A;color:#0E3A8A;text-decoration:none;padding:9px 16px;border-radius:999px;'  # noqa: E731
                            'font-weight:700;font-size:13px;display:inline-block;margin:4px 6px 4px 0">' + label + '</a>')
    return ('<p style="margin:18px 0 4px">' + b(_EM_PAGE, '\U0001F5FA\uFE0F See the roadmap and map your worries', '#0E3A8A', '#ffffff')
            + b(_EM_WA, '\U0001F4AC Chat with us on WhatsApp', '#1FA855', '#ffffff') + '</p>'
            '<p style="margin:0 0 6px">' + o(_EM_BROCHURE, '\U0001F4D8 Brochure (PDF)') + o(_EM_POSTER, '\U0001F5BC\uFE0F Poster') + o(_EM_CHANNEL, '\U0001F4E3 WhatsApp channel') + '</p>')


def _em_links_text():
    return ('Roadmap, self-check and worry map: ' + _EM_PAGE + '\nBrochure (PDF): ' + _EM_BROCHURE + '\nPoster: ' + _EM_POSTER
            + '\nChat on WhatsApp: https://wa.me/918015722706\nWhatsApp channel: ' + _EM_CHANNEL)


_EM_G11_STEPS = [('Months 1\u20132', 'Onboard.', 'Eligibility audit and your Grade 11 baseline.'), ('Months 3\u20135', 'Discover.', 'Branch Fit Assessment and the Industry 4.0 and AI briefing.'),
                 ('Months 6\u20139', 'Build.', 'Boards and JEE balance, mock error log, one exam calendar, document file.'), ('Months 10\u201312', 'Plan.', 'First target list and a Grade 12 roadmap.')]
_EM_G12_STEPS = [('Oct\u2013Jan', 'Onboard and target.', 'Eligibility audit, Branch Fit, JEE strategy and a target list.'), ('Feb\u2013Mar', 'Protect.', 'Boards first, with the 75% rule protected and documents ready.'),
                 ('Apr\u2013May', 'Map.', 'Final rank, rank-to-seat map and the quota decision.'), ('Jun\u2013Aug', 'Counsel and decide.', 'Applications, choice filling and the final seat decision.')]


def _em_version(key, label, parent, grade):
    g11 = grade == 11
    track = 'Grade 11 track' if g11 else 'Grade 12 track'
    stats = [('1:1', 'senior mentor'), ('4' if g11 else '10+', 'online one-to-one sessions'), ('1 year' if g11 else '10\u201312', 'academic year' if g11 else 'months, to seat day'), ('9', 'routes on one calendar')]
    steps = _EM_G11_STEPS if g11 else _EM_G12_STEPS
    fee = ('Grade 11 track: \u20B925,000 for one academic year. Register during 2026\u201327 and the Grade 12 track is \u20B950,000 instead of \u20B975,000, with portal access for two years.' if g11 else
           'Grade 12 track: \u20B975,000 for 10 to 12 months, paid in three parts (50% on enrolment, 25% at month 4, 25% at counselling).')
    if parent:
        subject = ('{student}\u2019s Grade 11: the one year with no deadline on the decisions' if g11 else '{student}\u2019s Grade 12: who is carrying the admissions decisions?')
        opener = ('<p>Dear {name},</p><p>Most families do not lose seats to marks. They lose them to <strong>a missed rule or a late start</strong>. '
                  + ('Grade 11 is the one year in which eligibility, branch fit and the exam calendar can be settled calmly, before a deadline sits on top of them.' if g11 else
                     'In Grade 12 the pattern we see every year is a child in coaching and a parent carrying admissions alone, late at night, from group-chat forwards.') + '</p>')
        icons = [('\U0001F4CB', 'Briefed at every gate', 'A written summary after each key session, so both parents stay aligned.'),
                 ('\u2705', 'One verified source', 'Answers checked against official notices, not group-chat forwards.'),
                 ('\U0001F4B0', 'Fees and return, side by side', 'Tuition, hostel and travel for every shortlisted seat, before you commit.'),
                 ('\U0001F4C1', 'Documents on time', 'A checklist and a deadline calendar, with certificates collected while school is in session.')]
        ask = '<p>The page below has a two-minute <strong>worry map</strong>: tap what is on your mind and see what a mentor does about each worry. Shall we book a first discussion this week?</p>'
        hero = _em_hero('One decision, several clocks,', 'one mentor beside your family.')
        wa = ('Dear {name}, EduAakashaA Elite Mentorship gives {student} one senior mentor for ' + ('Grade 11: eligibility, branch fit, exam calendar and a first target list.' if g11 else 'Grade 12: strategy, documents, choice filling and the seat decision.')
              + ' Map your worries in two minutes: ' + _EM_PAGE + '  Brochure: ' + _EM_BROCHURE + '  Reply here to book a first discussion. {sender}, EduAakashaA')
        text_open = ('Dear {name},\n\nMost families do not lose seats to marks. They lose them to a missed rule or a late start.\n\n')
    else:
        subject = ('{name}, your coaching builds the marks. Who decides what they are for?' if g11 else '{name}, the rank is half the story. The other half is decisions')
        opener = ('<p>Hi {name},</p><p>You already give coaching hours every week. Here is a question nobody in class asks: <strong>which branch do you actually want, and why?</strong> '
                  + ('Grade 11 is the best year to find out, while there is no deadline on your shoulders.' if g11 else 'In Grade 12, a rank becomes a seat only through dozens of decisions: routes, quota, choice order, deadlines.') + '</p>')
        icons = [('\U0001F3AF', 'A goal you chose', 'A 30-question Branch Fit Assessment across seven branch families, before any college is named.'),
                 ('\u23F1\uFE0F', 'Time back for study', 'Your mentor carries the rules, research and deadlines. You keep the hours for mocks.'),
                 ('\U0001F4C8', 'Mock tests that teach', 'A baseline, an error log and a review habit, so the same mistake is not repeated.'),
                 ('\U0001F9D8', 'Less noise, less stress', 'One verified voice in place of group chats, reels and comparisons.')]
        ask = '<p>Try the one-minute <strong>self-check</strong> on the page below: eight questions on who owns your decisions today. Then show it to your parents.</p>'
        hero = _em_hero('Coaching builds the marks.', 'Mentorship decides what they are for.')
        wa = ('Hi {name}! Coaching builds the marks. Mentorship decides what they are for. Take the one-minute self-check and see your ' + ('Grade 11' if g11 else 'Grade 12')
              + ' roadmap: ' + _EM_PAGE + '  Poster: ' + _EM_POSTER + '  Questions? Reply here. {sender}, EduAakashaA')
        text_open = 'Hi {name},\n\nYou already give coaching hours every week. Here is a question nobody in class asks: which branch do you actually want, and why?\n\n'
    html_body = (hero + opener + _em_stats(stats) + _em_vs()
                 + '<p style="margin:14px 0 2px"><strong style="color:#0E3A8A">\u2728 What changes with a mentor</strong></p>' + _em_icons(icons)
                 + '<p style="margin:14px 0 2px"><strong style="color:#0E3A8A">\U0001F5FA\uFE0F Your ' + track + ' roadmap</strong></p>' + _em_steps(steps)
                 + '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#FBEFD2;border:1px dashed #C24F00;border-radius:10px;margin:6px 0 14px"><tr>'
                   '<td style="padding:10px 14px;font-size:14px">\U0001F3F7\uFE0F ' + fee + '</td></tr></table>'
                 + ask + _em_links() + _SIGN_HTML
                 + '<p style="font-size:12px;color:#5A6278;margin:16px 0 0">' + _EM_NOTE + ' Fees are as published for 2027\u201328; please confirm when you book.</p>')
    text_body = (text_open + 'Coaching builds the marks. Mentorship decides what they are for. Most students need both.\n\n'
                 + 'What changes with a mentor:\n' + ''.join('- ' + t + ': ' + d + '\n' for _i, t, d in icons)
                 + '\nYour ' + track + ' roadmap:\n' + ''.join(str(n + 1) + '. ' + w + ': ' + t + ' ' + d + '\n' for n, (w, t, d) in enumerate(steps))
                 + '\n' + fee + '\n\n' + _em_links_text() + '\n\n' + _SIGN_TEXT + '\n\n' + _EM_NOTE)
    return {'key': key, 'label': label, 'nosig': True, 'fields': _EM_FIELDS, 'subject': subject, 'html': html_body, 'text': text_body, 'wa': wa}


ELITE_MENTORSHIP = {
    'key': 'elite-mentorship', 'icon': '\U0001F9ED', 'label': 'Elite Mentorship: Grade 11 and 12', 'category': 'Mentorship programmes',
    'desc': 'Introduce Elite Mentorship to a student or to parents, for Grade 11 or Grade 12: photo banner, key numbers, coaching and mentoring side by side, '
            'the roadmap, and buttons for the programme page, brochure, poster and WhatsApp. Each version has a short WhatsApp message.',
    'versions': [_em_version('student-g11', 'To a student · Grade 11', False, 11), _em_version('student-g12', 'To a student · Grade 12', False, 12),
                 _em_version('parent-g11', 'To parents · Grade 11', True, 11), _em_version('parent-g12', 'To parents · Grade 12', True, 12)],
}


# --------------------------------------------------------------------------- #
# The registry. Grouped by `category` for the admin UI.
# --------------------------------------------------------------------------- #
EMAIL_TEMPLATES = [

    # ===================== School outreach ================================= #
    SCHOOL_OUTREACH,

    # ===================== Mentorship programmes ============================ #
    ELITE_MENTORSHIP,

    # ===================== Members & Onboarding ============================ #
    {'key': 'welcome', 'icon': '👋', 'label': 'Welcome message',
     'category': 'Members & Onboarding',
     'desc': 'Welcome a new user, a premium member who just paid, or a new College Guide.',
     'versions': [
        {'key': 'user', 'label': 'New user', 'fields': [_f('name', 'First name', 'there')],
         'subject': 'Welcome to EduAakashaa 🎓',
         'text': ("Hi {name},\n\nWelcome to EduAakashaa! You now have free access to our "
                  "college predictors (JOSAA, TNEA, DASA), NIRF rankings and career-planning "
                  "tools.\n\nWhenever you're deciding on a college, we're here to help you "
                  "choose right.\n\nStart exploring: " + SITE + "\nQuestions? WhatsApp us at "
                  + WHATSAPP_NUMBER + ".\n\n— Team EduAakashaa"),
         'html': ("<p>Hi {name},</p><p>Welcome to <strong>EduAakashaa</strong>! You now have "
                  "free access to our college predictors (JOSAA, TNEA, DASA), NIRF rankings "
                  "and career-planning tools.</p><p>Whenever you're deciding on a college, "
                  "we're here to help you choose right.</p>"
                  + _btn(SITE, 'Start exploring')
                  + "<p>Questions? WhatsApp us at <strong>" + WHATSAPP_NUMBER + "</strong>.</p>")},
        {'key': 'premium', 'label': 'Premium — just paid',
         'fields': [_f('name', 'First name', 'there'), _f('plan', 'Plan', 'Premium')],
         'subject': 'Your EduAakashaa Premium is active, {name}! 🎉',
         'text': ("Hi {name},\n\nThank you for your payment — your {plan} membership is now "
                  "active! You've unlocked every premium tool: expert predictors, member "
                  "reports and 1-on-1 counsellor support.\n\nCounselling season moves fast — "
                  "let's build your perfect choice list together. Head to your dashboard to "
                  "get started: " + SITE + "/dashboard\n\n— Team EduAakashaa"),
         'html': ("<p>Hi {name},</p><p>Thank you for your payment — your <strong>{plan}</strong> "
                  "membership is now active! 🎉 You've unlocked every premium tool: expert "
                  "predictors, member reports and 1-on-1 counsellor support.</p>"
                  "<p>Counselling season moves fast — let's build your perfect choice list "
                  "together.</p>" + _btn(SITE + '/dashboard', 'Go to your dashboard'))},
        {'key': 'guide', 'label': 'New College Guide',
         'fields': [_f('name', 'First name', 'there'), _f('college', 'College', 'your college')],
         'subject': "You're a College Guide now, {name}! 🙌",
         'text': ("Hi {name},\n\nWelcome aboard as an EduAakashaa College Guide! Whenever a "
                  "parent has questions about {college}, we'll reach out — hop on a quick call "
                  "or drop a short video, and get paid ₹500–1000 for it. No lock-in, no spam, "
                  "fully on your schedule.\n\nMeanwhile, share your invite link to earn ₹1000 "
                  "referral bonuses. We'll be in touch when a parent wants your take.\n\n— Team EduAakashaa"),
         'html': ("<p>Hi {name},</p><p>Welcome aboard as an <strong>EduAakashaa College Guide</strong>! "
                  "Whenever a parent has questions about <strong>{college}</strong>, we'll reach "
                  "out — hop on a quick call or drop a short video, and <strong>get paid ₹500–1000</strong> "
                  "for it. No lock-in, no spam, fully on your schedule.</p>"
                  "<p>Meanwhile, share your invite link to earn ₹1000 referral bonuses. We'll be "
                  "in touch when a parent wants your take.</p>")},
     ]},

    {'key': 'assessment_invite', 'icon': '🧭', 'label': 'Onboarding assessment invite',
     'category': 'Members & Onboarding',
     'desc': 'Ask the student (or parent) to complete the profiling assessment before the first 1-on-1.',
     'versions': [
        {'key': 'student', 'label': 'Student', 'fields': [
            _f('name', 'First name', 'there'),
            _f('link', 'Assessment link', SITE + '/onboarding-assessment/student'),
            _f('days', 'Complete within', '2 days')],
         'subject': 'Before your first session — a 20-minute head start, {name}',
         'text': ("Hi {name},\n\nBefore your first 1-on-1, we'd like to understand you properly "
                  "— your interests, strengths and what you actually want from engineering. "
                  "Please complete your onboarding assessment (about 20 minutes, on your "
                  "phone):\n\n{link}\n\nAnswer honestly — there are no right answers, and "
                  "nothing you say is shared without your OK. Your counsellor uses this to "
                  "make the session about YOU, not generic advice.\n\nPlease finish it within "
                  "{days} so we can prepare.\n\n— Team EduAakashaa"),
         'html': ("<p>Hi {name},</p><p>Before your first 1-on-1, we'd like to understand you "
                  "properly — your interests, strengths and what you actually want from "
                  "engineering. Please complete your onboarding assessment "
                  "(about <strong>20 minutes</strong>, on your phone).</p>"
                  + _btn('{link}', 'Start my assessment')
                  + "<p>Answer honestly — there are no right answers, and nothing you say is "
                  "shared without your OK. Your counsellor uses this to make the session about "
                  "<strong>you</strong>, not generic advice.</p>"
                  "<p>Please finish it within <strong>{days}</strong> so we can prepare.</p>")},
        {'key': 'parent', 'label': 'Parent', 'fields': [
            _f('name', 'Parent name', 'there'), _f('student', 'Student name', 'your child'),
            _f('link', 'Assessment link', SITE + '/onboarding-assessment/parent'),
            _f('days', 'Complete within', '2 days')],
         'subject': 'Your side of the picture — 10 minutes before our session',
         'text': ("Dear {name},\n\nThank you for trusting EduAakashaa with {student}'s "
                  "engineering admissions. Before the first counselling session, we ask "
                  "parents to fill a short questionnaire (about 10 minutes) — your "
                  "expectations, budget planning and questions about the admissions "
                  "process:\n\n{link}\n\nPlease fill it independently — don't compare answers "
                  "with {student}. Seeing where you both agree (and differ) is exactly what "
                  "makes the first session useful.\n\nPlease finish it within {days}.\n\n"
                  "— Team EduAakashaa"),
         'html': ("<p>Dear {name},</p><p>Thank you for trusting EduAakashaa with "
                  "<strong>{student}</strong>'s engineering admissions. Before the first "
                  "counselling session, we ask parents to fill a short questionnaire "
                  "(about <strong>10 minutes</strong>) — your expectations, budget planning "
                  "and questions about the admissions process.</p>"
                  + _btn('{link}', 'Fill the parent questionnaire')
                  + "<p>Please fill it independently — don't compare answers with {student}. "
                  "Seeing where you both agree (and differ) is exactly what makes the first "
                  "session useful.</p><p>Please finish it within <strong>{days}</strong>.</p>")},
     ]},

    {'key': 'session_booked', 'icon': '📅', 'label': 'Session confirmed',
     'category': 'Members & Onboarding',
     'desc': 'Confirm a booked 1-on-1 counselling session with date, time and how to join.',
     'versions': [
        {'key': 'default', 'label': '', 'fields': [
            _f('name', 'First name', 'there'), _f('date', 'Date', '15 Jul 2026'),
            _f('time', 'Time (IST)', '6:00 PM'), _f('mode', 'Mode', 'Google Meet'),
            _f('counsellor', 'Counsellor', 'our senior counsellor')],
         'subject': 'Confirmed: your 1-on-1 on {date} at {time} IST',
         'text': ("Hi {name},\n\nYour 1-on-1 counselling session is confirmed:\n\n"
                  "Date: {date}\nTime: {time} IST\nMode: {mode}\nWith: {counsellor}\n\n"
                  "Keep your recent marks handy, and bring every question you have — no "
                  "question is too small. If the time doesn't work anymore, reply here or "
                  "WhatsApp us at " + WHATSAPP_NUMBER + " and we'll reschedule.\n\n"
                  "— Team EduAakashaa"),
         'html': ("<p>Hi {name},</p><p>Your 1-on-1 counselling session is confirmed:</p>"
                  "<table style=\"border-collapse:collapse;margin:16px 0;font-size:15px\">"
                  "<tr><td style=\"padding:6px 18px 6px 0;color:#5A6278\">Date</td>"
                  "<td style=\"padding:6px 0;font-weight:700\">{date}</td></tr>"
                  "<tr><td style=\"padding:6px 18px 6px 0;color:#5A6278\">Time</td>"
                  "<td style=\"padding:6px 0;font-weight:700\">{time} IST</td></tr>"
                  "<tr><td style=\"padding:6px 18px 6px 0;color:#5A6278\">Mode</td>"
                  "<td style=\"padding:6px 0;font-weight:700\">{mode}</td></tr>"
                  "<tr><td style=\"padding:6px 18px 6px 0;color:#5A6278\">With</td>"
                  "<td style=\"padding:6px 0;font-weight:700\">{counsellor}</td></tr></table>"
                  "<p>Keep your recent marks handy, and bring every question you have — no "
                  "question is too small.</p><p>If the time doesn't work anymore, reply here "
                  "or WhatsApp us at <strong>" + WHATSAPP_NUMBER + "</strong> and we'll "
                  "reschedule.</p>")},
     ]},

    {'key': 'session_recap', 'icon': '🗒️', 'label': 'Session recap & next steps',
     'category': 'Members & Onboarding',
     'desc': 'After a 1-on-1: thank them and put the agreed next steps in writing.',
     'versions': [
        {'key': 'default', 'label': '', 'fields': [
            _f('name', 'First name', 'there'),
            _f('steps', 'Agreed next steps', 'finalise your college list by Friday')],
         'subject': 'Your session recap & next steps, {name}',
         'text': ("Hi {name},\n\nGreat talking with you today! Putting what we agreed in "
                  "writing so nothing slips:\n\nNext steps: {steps}\n\nYour dashboard has "
                  "every tool we used in the session: " + SITE + "/dashboard\n\nStuck on "
                  "anything before the next check-in? Reply here or WhatsApp us at "
                  + WHATSAPP_NUMBER + ".\n\n— Team EduAakashaa"),
         'html': ("<p>Hi {name},</p><p>Great talking with you today! Putting what we agreed "
                  "in writing so nothing slips:</p>"
                  "<div style=\"background:#FBF7EE;border-left:4px solid #FF6B0A;padding:14px 18px;"
                  "border-radius:0 10px 10px 0;margin:16px 0\"><strong>Next steps:</strong> "
                  "{steps}</div>"
                  + _btn(SITE + '/dashboard', 'Open your dashboard')
                  + "<p>Stuck on anything before the next check-in? Reply here or WhatsApp us "
                  "at <strong>" + WHATSAPP_NUMBER + "</strong>.</p>")},
     ]},

    {'key': 'report_ready', 'icon': '📊', 'label': 'Report delivered',
     'category': 'Members & Onboarding',
     'desc': 'Tell a member their personalised report is ready to view/download.',
     'versions': [
        {'key': 'default', 'label': '', 'fields': [
            _f('name', 'First name', 'there'),
            _f('report', 'Report name', 'College Fit Report')],
         'subject': 'Your {report} is ready, {name} 📊',
         'text': ("Hi {name},\n\nYour personalised {report} is ready! It covers our analysis "
                  "and clear recommendations for your next steps.\n\nView it on your "
                  "dashboard: " + SITE + "/dashboard\n\nRead it once, note your questions, "
                  "and bring them to your next session — that's where the report really "
                  "pays off.\n\n— Team EduAakashaa"),
         'html': ("<p>Hi {name},</p><p>Your personalised <strong>{report}</strong> is ready! "
                  "It covers our analysis and clear recommendations for your next steps.</p>"
                  + _btn(SITE + '/dashboard', 'View my report')
                  + "<p>Read it once, note your questions, and bring them to your next "
                  "session — that's where the report really pays off.</p>")},
     ]},

    {'key': 'docs', 'icon': '📄', 'label': 'Documents',
     'category': 'Members & Onboarding',
     'desc': 'Chase missing documents, or confirm everything has been received.',
     'versions': [
        {'key': 'pending', 'label': 'Missing documents', 'fields': [
            _f('name', 'First name', 'there'),
            _f('docs', 'Documents needed', 'Class 12 marksheet, JEE scorecard')],
         'subject': 'Documents pending: {docs}',
         'text': ("Hi {name},\n\nTo move ahead with your counselling file we still need:\n\n"
                  "{docs}\n\nPlease send them as photos or PDFs — reply to this email or "
                  "WhatsApp them to " + WHATSAPP_NUMBER + ". Clear photos are fine; nothing "
                  "needs to be attested at this stage.\n\n— Team EduAakashaa"),
         'html': ("<p>Hi {name},</p><p>To move ahead with your counselling file we still "
                  "need:</p><div style=\"background:#FBF7EE;border-left:4px solid #E89A1C;"
                  "padding:14px 18px;border-radius:0 10px 10px 0;margin:16px 0\">"
                  "<strong>{docs}</strong></div>"
                  "<p>Please send them as photos or PDFs — reply to this email or WhatsApp "
                  "them to <strong>" + WHATSAPP_NUMBER + "</strong>. Clear photos are fine; "
                  "nothing needs to be attested at this stage.</p>")},
        {'key': 'received', 'label': 'All received', 'fields': [_f('name', 'First name', 'there')],
         'subject': 'Got everything — your documents are in ✅',
         'text': ("Hi {name},\n\nQuick confirmation: we've received all your documents and "
                  "your counselling file is complete. Nothing more needed from you right "
                  "now.\n\nWe'll flag it immediately if anything else comes up during "
                  "registration or choice filling.\n\n— Team EduAakashaa"),
         'html': ("<p>Hi {name},</p><p>Quick confirmation: we've received all your documents "
                  "and your counselling file is <strong>complete</strong>. ✅ Nothing more "
                  "needed from you right now.</p><p>We'll flag it immediately if anything "
                  "else comes up during registration or choice filling.</p>")},
     ]},

    {'key': 'renewal', 'icon': '🔔', 'label': 'Premium renewal reminder',
     'category': 'Members & Onboarding',
     'desc': 'Remind a premium member their membership is expiring.',
     'versions': [
        {'key': 'default', 'label': '', 'fields': [
            _f('name', 'First name', 'there'), _f('plan', 'Plan', 'Premium'),
            _f('validity', 'Valid until', '31 Mar 2026')],
         'subject': 'Your EduAakashaa membership is expiring soon, {name}',
         'text': ("Hi {name},\n\nA quick heads-up — your {plan} membership is valid until "
                  "{validity}. Renew in time to keep uninterrupted access to the premium "
                  "predictors, expert reports and counsellor support during counselling "
                  "season.\n\nRenew: " + SITE + "/members-registration\n\n— Team EduAakashaa"),
         'html': ("<p>Hi {name},</p><p>A quick heads-up — your <strong>{plan}</strong> membership "
                  "is valid until <strong>{validity}</strong>. Renew in time to keep "
                  "uninterrupted access to the premium predictors, expert reports and "
                  "counsellor support during counselling season.</p>"
                  + _btn(SITE + '/members-registration', 'Renew now'))},
     ]},

    # ===================== Admissions & Payments =========================== #
    {'key': 'application', 'icon': '📥', 'label': 'Application received',
     'category': 'Admissions & Payments',
     'desc': 'Acknowledge a new membership application with its reference number.',
     'versions': [
        {'key': 'default', 'label': '', 'fields': [
            _f('name', 'First name', 'there'), _f('reference', 'Reference', 'EA-PREM-0001')],
         'subject': "We've got your application, {name} (ref {reference})",
         'text': ("Hi {name},\n\nThanks for applying for EduAakashaa membership — your reference "
                  "number is {reference}. Our team will review it and reach out within 2 working "
                  "days to confirm your plan and next steps.\n\nQuestions in the meantime? "
                  "WhatsApp us at " + WHATSAPP_NUMBER + ".\n\n— Team EduAakashaa"),
         'html': ("<p>Hi {name},</p><p>Thanks for applying for EduAakashaa membership — your "
                  "reference number is <strong>{reference}</strong>. Our team will review it and "
                  "reach out within 2 working days to confirm your plan and next steps.</p>"
                  "<p>Questions in the meantime? WhatsApp us at <strong>" + WHATSAPP_NUMBER
                  + "</strong>.</p>")},
     ]},

    {'key': 'app_approved', 'icon': '✅', 'label': 'Application approved',
     'category': 'Admissions & Payments',
     'desc': 'Confirm the plan and share the amount so the family can pay and get started.',
     'versions': [
        {'key': 'default', 'label': '', 'fields': [
            _f('name', 'First name', 'there'), _f('reference', 'Reference', 'EA-PREM-0001'),
            _f('plan', 'Plan', 'Premium'), _f('amount', 'Amount ₹', '15,000')],
         'subject': 'Approved! Your {plan} membership awaits, {name} ✅',
         'text': ("Hi {name},\n\nGood news — your application ({reference}) is approved for the "
                  "{plan} plan. The membership fee is ₹{amount} (inclusive of GST).\n\nWe'll "
                  "send the invoice and payment details separately. Once the payment is in, "
                  "your membership activates the same day and we schedule your first 1-on-1."
                  "\n\nAny questions about the plan or payment? WhatsApp us at "
                  + WHATSAPP_NUMBER + ".\n\n— Team EduAakashaa"),
         'html': ("<p>Hi {name},</p><p>Good news — your application (<strong>{reference}</strong>) "
                  "is approved for the <strong>{plan}</strong> plan. The membership fee is "
                  "<strong>₹{amount}</strong> (inclusive of GST).</p>"
                  "<p>We'll send the invoice and payment details separately. Once the payment "
                  "is in, your membership activates the same day and we schedule your first "
                  "1-on-1.</p><p>Any questions about the plan or payment? WhatsApp us at "
                  "<strong>" + WHATSAPP_NUMBER + "</strong>.</p>")},
     ]},

    {'key': 'payment_reminder', 'icon': '⏳', 'label': 'Payment reminder',
     'category': 'Admissions & Payments',
     'desc': 'Gently chase a pending invoice / balance due.',
     'versions': [
        {'key': 'default', 'label': '', 'fields': [
            _f('name', 'First name', 'there'), _f('reference', 'Invoice / reference', 'EA/0001'),
            _f('amount', 'Balance due ₹', '7,500'), _f('due', 'Due by', '20 Jul 2026')],
         'subject': 'Gentle reminder: ₹{amount} pending on {reference}',
         'text': ("Hi {name},\n\nA gentle reminder that ₹{amount} is pending on your "
                  "EduAakashaa invoice {reference}, due by {due}.\n\nOnce it's cleared, your "
                  "membership continues uninterrupted — especially important with counselling "
                  "deadlines coming up.\n\nAlready paid? Please ignore this and accept our "
                  "thanks — or reply with the reference so we can match it quickly.\n\n"
                  "— Team EduAakashaa"),
         'html': ("<p>Hi {name},</p><p>A gentle reminder that <strong>₹{amount}</strong> is "
                  "pending on your EduAakashaa invoice <strong>{reference}</strong>, due by "
                  "<strong>{due}</strong>.</p><p>Once it's cleared, your membership continues "
                  "uninterrupted — especially important with counselling deadlines coming "
                  "up.</p><p>Already paid? Please ignore this and accept our thanks — or reply "
                  "with the reference so we can match it quickly.</p>")},
     ]},

    {'key': 'payment_received', 'icon': '🧾', 'label': 'Payment received',
     'category': 'Admissions & Payments',
     'desc': 'Acknowledge a full or partial payment with the receipt details.',
     'versions': [
        {'key': 'full', 'label': 'Paid in full', 'fields': [
            _f('name', 'First name', 'there'), _f('amount', 'Amount ₹', '15,000'),
            _f('receipt', 'Receipt no', 'RCPT/0001')],
         'subject': 'Payment received — receipt {receipt} 🧾',
         'text': ("Hi {name},\n\nWe've received your payment of ₹{amount} — thank you! Your "
                  "receipt number is {receipt} and your membership is fully paid.\n\nNext: "
                  "we'll schedule your onboarding and first 1-on-1. See you inside!\n\n"
                  "— Team EduAakashaa"),
         'html': ("<p>Hi {name},</p><p>We've received your payment of <strong>₹{amount}</strong> "
                  "— thank you! Your receipt number is <strong>{receipt}</strong> and your "
                  "membership is <strong>fully paid</strong>.</p><p>Next: we'll schedule your "
                  "onboarding and first 1-on-1. See you inside!</p>")},
        {'key': 'partial', 'label': 'Partial payment', 'fields': [
            _f('name', 'First name', 'there'), _f('amount', 'Amount received ₹', '7,500'),
            _f('balance', 'Balance due ₹', '7,500'), _f('due', 'Balance due by', '31 Jul 2026')],
         'subject': 'Received ₹{amount} — ₹{balance} remaining',
         'text': ("Hi {name},\n\nThank you — we've received your payment of ₹{amount}. The "
                  "remaining balance is ₹{balance}, due by {due}.\n\nYour membership benefits "
                  "are already active, so don't wait to use the tools and book your "
                  "sessions.\n\n— Team EduAakashaa"),
         'html': ("<p>Hi {name},</p><p>Thank you — we've received your payment of "
                  "<strong>₹{amount}</strong>. The remaining balance is "
                  "<strong>₹{balance}</strong>, due by <strong>{due}</strong>.</p>"
                  "<p>Your membership benefits are already active, so don't wait to use the "
                  "tools and book your sessions.</p>")},
     ]},

    # ========================= College Guides ============================== #
    {'key': 'guide_match', 'icon': '🎯', 'label': 'Guide — matched with a parent',
     'category': 'College Guides',
     'desc': 'Ask a College Guide if they’re free to talk to a matched parent.',
     'versions': [
        {'key': 'default', 'label': '', 'fields': [
            _f('name', 'First name', 'there'), _f('parent', 'Parent / who', 'A parent'),
            _f('college', 'College', 'your college')],
         'subject': 'A parent wants to talk to you, {name} 🎓',
         'text': ("Hi {name},\n\n{parent} is looking at {college} and would love to hear from "
                  "someone who's actually been there — you! It's a short, paid session "
                  "(₹500–1000): a quick call or a short video answering their questions.\n\n"
                  "Are you free in the next few days? Reply and we'll set it up. Totally your "
                  "call — no pressure.\n\n— Team EduAakashaa"),
         'html': ("<p>Hi {name},</p><p><strong>{parent}</strong> is looking at "
                  "<strong>{college}</strong> and would love to hear from someone who's actually "
                  "been there — you! It's a short, paid session (<strong>₹500–1000</strong>): a "
                  "quick call or a short video answering their questions.</p><p>Are you free in "
                  "the next few days? Reply and we'll set it up. Totally your call — no pressure.</p>")},
     ]},

    {'key': 'ty_session', 'icon': '🙏', 'label': 'Thank you — Guide session',
     'category': 'College Guides',
     'desc': 'Thank a College Guide after they answer a parent’s questions.',
     'versions': [
        {'key': 'default', 'label': '', 'fields': [
            _f('name', 'First name', 'there'), _f('college', 'College', 'your college'),
            _f('amount', 'Payout ₹', '1000')],
         'subject': 'Thanks for guiding a parent, {name} 🙏',
         'text': ("Hi {name},\n\nThank you for taking the time to answer a parent's questions "
                  "about {college} — your honest, first-hand take genuinely helps a family "
                  "choose right.\n\nYour payout of ₹{amount} is being processed and will "
                  "reflect in your College Guide dashboard. We'll reach out again when another "
                  "parent needs your perspective.\n\n— Team EduAakashaa"),
         'html': ("<p>Hi {name},</p><p>Thank you for taking the time to answer a parent's "
                  "questions about <strong>{college}</strong> — your honest, first-hand take "
                  "genuinely helps a family choose right.</p><p>Your payout of "
                  "<strong>₹{amount}</strong> is being processed and will reflect in your "
                  "College Guide dashboard. We'll reach out again when another parent needs "
                  "your perspective.</p>")},
     ]},

    {'key': 'payment', 'icon': '💸', 'label': 'Payout credited — Guide',
     'category': 'College Guides',
     'desc': 'Tell a College Guide their payout has been credited.',
     'versions': [
        {'key': 'default', 'label': '', 'fields': [
            _f('name', 'First name', 'there'), _f('amount', 'Amount ₹', '1000')],
         'subject': '₹{amount} credited to you, {name} 💸',
         'text': ("Hi {name},\n\nGood news — your payout of ₹{amount} has been credited. Thank "
                  "you for being an EduAakashaa College Guide and helping parents with your "
                  "real college experience.\n\nKeep an eye on your dashboard for your next "
                  "session. Questions about a payout? Just reply here.\n\n— Team EduAakashaa"),
         'html': ("<p>Hi {name},</p><p>Good news — your payout of <strong>₹{amount}</strong> "
                  "has been credited. 💸 Thank you for being an EduAakashaa College Guide and "
                  "helping parents with your real college experience.</p><p>Keep an eye on your "
                  "dashboard for your next session. Questions about a payout? Just reply here.</p>")},
     ]},

    {'key': 'ty_survey', 'icon': '📝', 'label': 'Thank you — Survey',
     'category': 'College Guides',
     'desc': 'Thank someone for filling the college experience survey (and nudge them to guide).',
     'versions': [
        {'key': 'default', 'label': '', 'fields': [
            _f('name', 'First name', 'there'), _f('college', 'College', 'your college')],
         'subject': 'Thanks for the honest review, {name}! 🙌',
         'text': ("Hi {name},\n\nThank you for filling out the EduAakashaa college survey about "
                  "{college}. Your real, no-filter feedback helps NRI parents make better "
                  "decisions for their kids.\n\nWant to earn from what you know? Become a "
                  "College Guide and get paid ₹500–1000 to answer parents' questions: "
                  + SITE + "/alumni-network\n\n— Team EduAakashaa"),
         'html': ("<p>Hi {name},</p><p>Thank you for filling out the EduAakashaa college survey "
                  "about <strong>{college}</strong>. Your real, no-filter feedback helps NRI "
                  "parents make better decisions for their kids.</p><p>Want to earn from what "
                  "you know? Become a College Guide and get paid <strong>₹500–1000</strong> to "
                  "answer parents' questions.</p>"
                  + _btn(SITE + '/alumni-network', 'Become a College Guide'))},
     ]},

    # ======================= Engagement & Season =========================== #
    {'key': 'deadline_alert', 'icon': '⏰', 'label': 'Counselling deadline alert',
     'category': 'Engagement & Season',
     'desc': 'Warn a family about an approaching JoSAA / TNEA / other counselling deadline.',
     'versions': [
        {'key': 'josaa', 'label': 'JoSAA', 'fields': [
            _f('name', 'First name', 'there'), _f('round', 'Round / event', 'JoSAA Round 2 choice locking'),
            _f('date', 'Deadline', '18 Jul 2026, 5 PM')],
         'subject': '⏰ {round} closes {date}',
         'text': ("Hi {name},\n\nHeads-up: {round} closes on {date}. After that the portal "
                  "locks and choices can't be changed.\n\nIf you want a second pair of eyes on "
                  "your choice list before you lock, reply here or WhatsApp us at "
                  + WHATSAPP_NUMBER + " — we'll review it with you before the deadline.\n\n"
                  "— Team EduAakashaa"),
         'html': ("<p>Hi {name},</p><p>Heads-up: <strong>{round}</strong> closes on "
                  "<strong>{date}</strong>. After that the portal locks and choices can't be "
                  "changed.</p><p>If you want a second pair of eyes on your choice list before "
                  "you lock, reply here or WhatsApp us at <strong>" + WHATSAPP_NUMBER
                  + "</strong> — we'll review it with you before the deadline.</p>")},
        {'key': 'tnea', 'label': 'TNEA', 'fields': [
            _f('name', 'First name', 'there'), _f('round', 'Round / event', 'TNEA Round 1 choice filling'),
            _f('date', 'Deadline', '22 Jul 2026')],
         'subject': '⏰ {round} — deadline {date}',
         'text': ("Hi {name},\n\nReminder: {round} must be completed by {date}. TNEA rounds "
                  "move quickly and missed windows can't be reopened.\n\nUnsure about your "
                  "order of choices? Our TNEA tools and counsellors can pressure-test your "
                  "list before you submit: " + SITE + "\n\nWhatsApp us any time: "
                  + WHATSAPP_NUMBER + "\n\n— Team EduAakashaa"),
         'html': ("<p>Hi {name},</p><p>Reminder: <strong>{round}</strong> must be completed by "
                  "<strong>{date}</strong>. TNEA rounds move quickly and missed windows can't "
                  "be reopened.</p><p>Unsure about your order of choices? Our TNEA tools and "
                  "counsellors can pressure-test your list before you submit.</p>"
                  + _btn(SITE, 'Open the TNEA tools')
                  + "<p>WhatsApp us any time: <strong>" + WHATSAPP_NUMBER + "</strong></p>")},
        {'key': 'generic', 'label': 'Other', 'fields': [
            _f('name', 'First name', 'there'), _f('round', 'Event', 'BITSAT application window'),
            _f('date', 'Deadline', '25 Jul 2026')],
         'subject': '⏰ Don\'t miss it: {round} — {date}',
         'text': ("Hi {name},\n\nQuick reminder: {round} closes on {date}.\n\nIf this applies "
                  "to you, block 30 minutes this week to finish it — last-day server rushes "
                  "are real. Need help deciding whether it's worth applying? Reply here or "
                  "WhatsApp " + WHATSAPP_NUMBER + ".\n\n— Team EduAakashaa"),
         'html': ("<p>Hi {name},</p><p>Quick reminder: <strong>{round}</strong> closes on "
                  "<strong>{date}</strong>.</p><p>If this applies to you, block 30 minutes "
                  "this week to finish it — last-day server rushes are real. Need help "
                  "deciding whether it's worth applying? Reply here or WhatsApp <strong>"
                  + WHATSAPP_NUMBER + "</strong>.</p>")},
     ]},

    {'key': 'winback', 'icon': '🌱', 'label': 'Win-back — expired member',
     'category': 'Engagement & Season',
     'desc': 'Re-engage a member whose premium membership lapsed.',
     'versions': [
        {'key': 'default', 'label': '', 'fields': [
            _f('name', 'First name', 'there')],
         'subject': 'We kept your seat warm, {name}',
         'text': ("Hi {name},\n\nYour EduAakashaa Premium has lapsed — but your data, saved "
                  "predictions and reports are all still here.\n\nIf this admissions season "
                  "still matters for your family, rejoin and pick up exactly where you left "
                  "off — predictors, reports and 1-on-1 counselling included.\n\nRejoin: "
                  + SITE + "/members-registration\n\nNot the right time? No hard feelings — "
                  "the free tools remain yours forever.\n\n— Team EduAakashaa"),
         'html': ("<p>Hi {name},</p><p>Your EduAakashaa Premium has lapsed — but your data, "
                  "saved predictions and reports are all still here.</p><p>If this admissions "
                  "season still matters for your family, rejoin and pick up exactly where you "
                  "left off — predictors, reports and 1-on-1 counselling included.</p>"
                  + _btn(SITE + '/members-registration', 'Rejoin Premium')
                  + "<p>Not the right time? No hard feelings — the free tools remain yours "
                  "forever.</p>")},
     ]},

    {'key': 'feedback', 'icon': '💬', 'label': 'Feedback / testimonial request',
     'category': 'Engagement & Season',
     'desc': 'Ask a member how it went and (optionally) for a short testimonial.',
     'versions': [
        {'key': 'default', 'label': '', 'fields': [
            _f('name', 'First name', 'there')],
         'subject': 'How did we do, {name}?',
         'text': ("Hi {name},\n\nNow that the dust has settled, we'd love two minutes of "
                  "honest feedback: what helped, and what we should do better?\n\nJust reply "
                  "to this email — we read every response personally.\n\nAnd if EduAakashaa "
                  "made a real difference for your family, a short line we can share with "
                  "other parents would mean a lot. 🙏\n\n— Team EduAakashaa"),
         'html': ("<p>Hi {name},</p><p>Now that the dust has settled, we'd love two minutes "
                  "of honest feedback: what helped, and what we should do better?</p>"
                  "<p>Just reply to this email — we read every response personally.</p>"
                  "<p>And if EduAakashaa made a real difference for your family, a short line "
                  "we can share with other parents would mean a lot. 🙏</p>")},
     ]},

    {'key': 'inquiry_reply', 'icon': '📮', 'label': 'Inquiry response',
     'category': 'Engagement & Season',
     'desc': 'First response to a contact-form inquiry — acknowledge and offer a call.',
     'versions': [
        {'key': 'default', 'label': '', 'fields': [
            _f('name', 'First name', 'there'), _f('topic', 'They asked about', 'engineering admissions')],
         'subject': 'Re: your question about {topic}',
         'text': ("Hi {name},\n\nThanks for reaching out to EduAakashaa about {topic} — happy "
                  "to help.\n\nThe quickest way forward is a short call so we understand your "
                  "situation properly. WhatsApp us at " + WHATSAPP_NUMBER + " with a good "
                  "time, or simply reply to this email with "
                  "your questions.\n\nMeanwhile, our free predictors and guides are at "
                  + SITE + ".\n\n— Team EduAakashaa"),
         'html': ("<p>Hi {name},</p><p>Thanks for reaching out to EduAakashaa about "
                  "<strong>{topic}</strong> — happy to help.</p><p>The quickest way forward is "
                  "a short call so we understand your situation properly. WhatsApp us at "
                  "<strong>" + WHATSAPP_NUMBER + "</strong> with a good time, or simply reply "
                  "to this email with your questions.</p>"
                  + _btn(SITE, 'Explore the free tools'))},
     ]},

    # ===================== Recruitment ===================================== #
    {'key': 'recruit_invite', 'icon': '\U0001F9D1\u200d\U0001F3EB', 'label': 'Invite tutors and mentors to register',
     'category': 'Recruitment',
     'desc': 'Marketing email to potential tutors and career counsellors: logo, hiring banner and a button to register their interest on the Join our Team page.',
     'versions': [
        {'key': 'both', 'label': 'Tutors and mentors', 'fields': [
            _f('name', 'First name', 'there'), _f('link', 'Register-interest link', JOIN_LINK)],
         'subject': 'Teach, mentor and grow with EduAakashaa',
         'text': ("Hi {name},\n\nEduAakashaa is growing its network of tutors and career counsellors. We guide students across "
                  "CBSE, State Boards, JEE, NEET and more with one-to-one coaching and mentoring, all online. If teaching or "
                  "mentoring is your strength, we would like to hear from you.\n\nWhat you get:\n"
                  "- Reach students anywhere, online\n- Flexible scheduling that fits your day\n- Competitive compensation\n"
                  "- Tools and support from the team\n- A community of educators\n\nRegister your interest (about two minutes): {link}\n\n"
                  "This only registers your interest. Our team will contact you to talk about the next steps.\n\n- Team EduAakashaa"),
         'html': (_banner('hiring-both.jpg', 'We are hiring: teach, mentor and grow with EduAakashaa')
                  + "<p>Hi {name},</p><p><strong>EduAakashaa</strong> is growing its network of <strong>tutors and career "
                  "counsellors</strong>. We guide students across CBSE, State Boards, JEE, NEET and more with one-to-one coaching "
                  "and mentoring, all online. If teaching or mentoring is your strength, we would like to hear from you.</p>"
                  + _perks(['Reach students anywhere, online', 'Flexible scheduling that fits your day', 'Competitive compensation',
                            'Tools and support from the team', 'A community of educators'])
                  + _btn('{link}', 'Register your interest') + NOTE_HTML)},
        {'key': 'tutor', 'label': 'Tutors', 'fields': [
            _f('name', 'First name', 'there'), _f('subjects', 'Subjects we need', 'Maths, Physics, Chemistry and Biology'),
            _f('link', 'Register-interest link', JOIN_LINK)],
         'subject': 'Tutor opportunity with EduAakashaa: teach online, from anywhere',
         'text': ("Hi {name},\n\nWe are looking for tutors for {subjects} and more, across CBSE and State Board curricula, to teach "
                  "one-to-one with EduAakashaa.\n\nAs a tutor you would:\n- Plan lessons around each student\n"
                  "- Teach live sessions over video\n- Track progress and share regular feedback\n- Use your own notes and materials\n\n"
                  "Register your interest (about two minutes): {link}\n\nThis only registers your interest. Our team will contact "
                  "you to talk about the next steps.\n\n- Team EduAakashaa"),
         'html': (_banner('hiring-tutors.jpg', 'Now hiring tutors for Maths, Physics, Chemistry, Biology and more')
                  + "<p>Hi {name},</p><p>We are looking for <strong>tutors</strong> for <strong>{subjects}</strong> and more, across "
                  "CBSE and State Board curricula, to teach one-to-one with <strong>EduAakashaa</strong>.</p><p>As a tutor you would:</p>"
                  + _perks(['Plan lessons around each student', 'Teach live sessions over video', 'Track progress and share regular feedback',
                            'Use your own notes and materials'])
                  + _btn('{link}', 'Register your interest') + NOTE_HTML)},
        {'key': 'mentor', 'label': 'Mentors', 'fields': [
            _f('name', 'First name', 'there'), _f('link', 'Register-interest link', JOIN_LINK)],
         'subject': 'Mentor opportunity: guide students and parents with EduAakashaa',
         'text': ("Hi {name},\n\nWe are looking for career counsellors and mentors to guide students and parents with EduAakashaa.\n\n"
                  "As a mentor you would:\n- Guide students on career paths after Class 10 and Class 12\n"
                  "- Run aptitude and interest mapping\n- Help with college selection and entrance-exam strategy\n"
                  "- Hold one-to-one mentoring sessions\n\nRegister your interest (about two minutes): {link}\n\n"
                  "This only registers your interest. Our team will contact you to talk about the next steps.\n\n- Team EduAakashaa"),
         'html': (_banner('hiring-mentors.jpg', 'Now hiring mentors: career counsellors who guide students and parents')
                  + "<p>Hi {name},</p><p>We are looking for <strong>career counsellors and mentors</strong> to guide students and parents "
                  "with <strong>EduAakashaa</strong>.</p><p>As a mentor you would:</p>"
                  + _perks(['Guide students on career paths after Class 10 and Class 12', 'Run aptitude and interest mapping',
                            'Help with college selection and entrance-exam strategy', 'Hold one-to-one mentoring sessions'])
                  + _btn('{link}', 'Register your interest') + NOTE_HTML)},
     ]},
]


# Mentorship programme templates (built from the Elite Mentorship brochure and the
# 2027 student guides) — defined in their own module, appended to the registry.
from app.services.mentorship_email_templates import build_mentorship_templates  # noqa: E402

EMAIL_TEMPLATES.extend(build_mentorship_templates(SITE, WHATSAPP_NUMBER, _btn))
