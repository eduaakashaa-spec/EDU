"""Mentorship-programme email templates for /admin/templates.

Content source: the Elite Mentorship brochure (Grade 12 NRI, Class of 2027) and the
2027 Student Success / Mentorship guides (October 2026 editions). Rules quoted here
are the DASA 2026 rules — re-check them against the 2027 brochure when it is
published, and never promise a rank or a seat.

Each template is defined once as a list of small blocks and rendered to BOTH the
plain-text and the HTML body the registry needs, so the two can never drift:

    ('p',  'text with **bold** and {placeholders}')
    ('h',  'SECTION HEADING')
    ('ul', ['bullet', ...])
    ('ol', ['step', ...])
    ('kv', [('Label', 'value'), ...])      -> small key/value card
    ('btn', '{link}', 'Button label')       -> call-to-action button
    ('note', 'small print')                 -> muted fine print

`build_mentorship_templates(site, whatsapp, btn)` is called from email_templates.py
(passing its constants in avoids a circular import).
"""
import html as _html
import re


def _f(key, label, default=''):
    return {'key': key, 'label': label, 'default': default}


_BOLD = re.compile(r'\*\*(.+?)\*\*')


def _h(s):                                   # literal text -> safe html, **bold** kept
    return _BOLD.sub(r'<strong>\1</strong>', _html.escape(s, quote=False))


def _t(s):                                   # literal text -> plain text
    return _BOLD.sub(r'\1', s)


def _render(blocks, btn):
    text, out = [], []
    for b in blocks:
        kind = b[0]
        if kind == 'p':
            text.append(_t(b[1])); out.append('<p>' + _h(b[1]) + '</p>')
        elif kind == 'h':
            text.append(b[1].upper())
            out.append('<p style="margin:20px 0 6px;font-size:12px;letter-spacing:.08em;'
                       'color:#0E3A8A;font-weight:700">' + _html.escape(b[1].upper()) + '</p>')
        elif kind == 'ul':
            text.append('\n'.join('• ' + _t(i) for i in b[1]))
            out.append('<ul style="margin:6px 0 14px;padding-left:20px">'
                       + ''.join('<li style="margin:4px 0">' + _h(i) + '</li>' for i in b[1]) + '</ul>')
        elif kind == 'ol':
            text.append('\n'.join('%d. %s' % (n, _t(i)) for n, i in enumerate(b[1], 1)))
            out.append('<ol style="margin:6px 0 14px;padding-left:22px">'
                       + ''.join('<li style="margin:4px 0">' + _h(i) + '</li>' for i in b[1]) + '</ol>')
        elif kind == 'kv':
            text.append('\n'.join('%s: %s' % (k, _t(v)) for k, v in b[1]))
            rows = ''.join(
                "<tr><td style='padding:9px 14px;border-bottom:1px solid #EFE7D4;color:#5A6278;"
                "white-space:nowrap'>%s</td><td style='padding:9px 14px;border-bottom:1px solid "
                "#EFE7D4'><strong>%s</strong></td></tr>" % (_html.escape(k), _h(v)) for k, v in b[1])
            out.append('<table role="presentation" cellpadding="0" cellspacing="0" style="width:100%;'
                       'border:1px solid #E8DFC8;border-radius:10px;border-collapse:separate;'
                       'margin:10px 0 16px;background:#FBF7EE">' + rows + '</table>')
        elif kind == 'btn':
            text.append(b[2] + ': ' + b[1]); out.append(btn(b[1], _html.escape(b[2])))
        elif kind == 'note':
            text.append(_t(b[1]))
            out.append('<p style="color:#5A6278;font-size:12.5px;line-height:1.6">' + _h(b[1]) + '</p>')
    return '\n\n'.join(text), ''.join(out)


NO_GUARANTEE = ('EduAakashaa guides the process. No rank, score or seat is guaranteed — admission '
                'is decided by the authorities on rank and eligibility.')


def build_mentorship_templates(SITE, WHATSAPP, btn):
    T = []

    def add(key, icon, label, category, desc, versions):
        vs = []
        for v in versions:
            text, html = _render(v['blocks'], btn)
            vs.append({'key': v.get('key', 'default'), 'label': v.get('label', ''),
                       'fields': v['fields'], 'subject': v['subject'],
                       'text': text + '\n\n— Team EduAakashaa', 'html': html,
                       'wa': v.get('wa', '')})
        T.append({'key': key, 'icon': icon, 'label': label, 'category': category,
                  'desc': desc, 'versions': vs})

    PARENT = _f('name', 'Parent name', 'there')
    STUDENT = _f('student', 'Student name', 'your child')
    MENTOR = _f('mentor', 'Mentor name', 'your mentor')
    BOOK = _f('link', 'Booking / meeting link', SITE)

    # ============================ Marketing ============================ #
    C = 'Mentorship · Marketing'
    add('mp_profile_guide', '🧭', 'Profile + NRI Admission Guide — Mentorship 2027', C,
        'Introduce EduAakashaA, share the NRI Admission Guide and promote the 2027 mentorship. Sends from info@eduaakashaa.com.', [
        {'fields': [PARENT, STUDENT,
                    _f('guide', 'NRI Admission Guide link', SITE + '/nri-admission'),
                    _f('link', 'Mentorship / membership link', SITE + '/members-registration'),
                    _f('sender', 'Signed by', 'Admissions Team')],
         'subject': 'EduAakashaA — your NRI Admission Guide 2027 and mentorship for {student}',
         'blocks': [
            ('p', 'Dear {name},'),
            ('p', 'Thank you for your interest in engineering admissions in India for {student}. We are **EduAakashaA** — an '
                  'evidence-based admissions counselling practice based in Coimbatore, Tamil Nadu, guiding students and parents '
                  'in India and the Gulf through DASA, CIWG, JoSAA, TNEA and state and private NRI routes.'),
            ('h', 'Who we are'),
            ('ul', ['**Data-first guidance** — official cut-off and seat data, analysed and explained in plain language',
                    '**NRI specialists** — DASA and CIWG eligibility, documents, fees and choice-filling for Gulf families',
                    '**Mentors, not a one-time consultancy** — one senior mentor from enrolment to the seat decision',
                    '**Honest by design** — we show risks and trade-offs; we never promise a rank or a seat']),
            ('h', 'Your free NRI Admission Guide'),
            ('p', 'Our guide is updated for the 2026–27 cycle using the official DASA 2026 brochure: who is eligible for DASA and '
                  'CIWG, the two-year-abroad rule, fees, documents, the 87 participating institutes, the two-round process and what '
                  'the closing ranks did in 2026.'),
            ('btn', '{guide}', 'Read the NRI Admission Guide'),
            ('h', 'Elite Mentorship — Class of 2027'),
            ('ul', ['A dedicated 1:1 senior mentor, supported by a domain mentor and an admissions specialist',
                    'Minimum 10 virtual 1:1 sessions, time-zone friendly for Gulf families',
                    'A live admissions roadmap, reach / match / safe college list, choice-filling strategy and a final seat decision brief',
                    'Premium portal with the DASA analytics report, choice-filling simulator and personalised reports for one year']),
            ('p', 'Want portal access only? **Premium Portal Access** gives the latest DASA insights, the 2026–27 analytics report, '
                  'the Choice Builder simulator and a personalised choice-filling report.'),
            ('btn', '{link}', 'Explore mentorship paths & book a free conversation'),
            ('h', 'Contact us'),
            ('kv', [('Phone / WhatsApp', WHATSAPP), ('Email', 'info@eduaakashaa.com'),
                    ('Website', 'www.eduaakashaa.com'), ('Office', 'Coimbatore, Tamil Nadu, India')]),
            ('p', 'Reply to this email or message us on WhatsApp and a mentor will respond within one working day.'),
            ('p', 'Warm regards, **{sender}**, EduAakashaA'),
            ('note', NO_GUARANTEE + ' Rules, fees and dates are re-verified against each official notification.')],
         'wa': ('Hello {name} 👋 This is *EduAakashaA* (Coimbatore) — evidence-based admissions guidance for NRI and Indian families.\n\n'
                '📘 *NRI Admission Guide 2026–27* (DASA · CIWG · JoSAA): {guide}\n\n'
                '🎓 *Elite Mentorship — Class of 2027*: dedicated 1:1 senior mentor, 10+ sessions, live roadmap, '
                'choice-filling strategy and final seat-decision brief. Portal-only access also available.\n'
                'Free 20-min conversation: {link}\n\n'
                '📞 ' + WHATSAPP + ' · ✉️ info@eduaakashaa.com · 🌐 www.eduaakashaa.com\n'
                'No rank or seat is guaranteed — we guide the process. — {sender}')}])

    add('mp_promo_launch', '📣', 'Promotional — programme launch', C,
        'Campaign email introducing Elite Mentorship to Grade 11–12 NRI families.', [
        {'fields': [PARENT, BOOK],
         'subject': 'Grade 12 in the Gulf? One mentor, one plan, one seat decision — Class of 2027',
         'blocks': [
            ('p', 'Dear {name},'),
            ('p', 'A Grade 12 student in the Gulf prepares for boards and JEE Main while five or more Indian '
                  'admission systems run on separate calendars — DASA, CIWG, JoSAA, state and private NRI '
                  'routes. Most families do not lose seats to marks. They lose them to a **missed rule or a late start**.'),
            ('p', '**EduAakashaa Elite Mentorship** puts one senior mentor beside your family from enrolment to the seat decision:'),
            ('ul', ['A dedicated 1:1 senior mentor, supported by a domain mentor and an admissions specialist',
                    'Minimum 10 virtual 1:1 sessions per student — time-zone friendly for Gulf families',
                    'Nine strategy deliverables: baseline assessment, live roadmap, reach / match / safe college list, '
                    'DASA-CIWG and JoSAA choice-filling pack, final seat decision brief and more',
                    'Premium portal, choice-filling simulator and DASA analytics for one year']),
            ('p', 'Did you know? DASA went from three rounds to two in 2026, and closing ranks moved in opposite '
                  'directions by quota. Families planning from last year\'s PDF are planning for a process that no longer exists.'),
            ('btn', '{link}', 'Book a free 20-minute conversation'),
            ('note', NO_GUARANTEE)],
         'wa': ('Hello {name} 👋 Is your child in Grade 12 in the Gulf aiming for an NIT/IIIT/IIT seat in 2027? '
                'Most NRI families don\'t lose seats to marks — they lose them to a missed rule or a late start. '
                'EduAakashaa Elite Mentorship: one dedicated senior mentor, 10+ 1:1 sessions, a live roadmap for '
                'DASA/CIWG/JoSAA and a final seat-decision brief. Free 20-min conversation: {link}')}])

    add('mp_promo_data', '📊', 'Promotional — DASA 2026 data hook', C,
        'Second touch: the CIWG-tightened / Non-CIWG-eased closing-rank story.', [
        {'fields': [PARENT, BOOK],
         'subject': 'CIWG cut-offs tightened ~8%. Non-CIWG eased ~18%. What it means for 2027',
         'blocks': [
            ('p', 'Dear {name},'),
            ('p', 'We compared every DASA programme\'s final closing rank, 2026 against 2025, across 378 programmes:'),
            ('ul', ['**CIWG:** median closing rank fell about 8% — a tougher cut-off',
                    '**Non-CIWG:** median closing rank rose about 18% — an easier cut-off',
                    'Computer / IT / AI eased, while Civil, Bio/Food and Chemical/Materials tightened the most — '
                    'core branches are no longer a safe fallback']),
            ('p', 'A CIWG-eligible student should plan for a **better rank than last year\'s cut-off**, and build the '
                  'shortlist on three to four years of trends — never one closing rank.'),
            ('btn', '{link}', 'Talk to a mentor'),
            ('note', 'Planning estimates from DASA 2025 (after Round 3) and DASA 2026 (after Round 2), OPEN '
                     'gender-neutral seats. Not guarantees of admission.')],
         'wa': ('📊 DASA 2026 vs 2025: CIWG closing ranks got tougher (~8%), Non-CIWG easier (~18%), core branches '
                'tightened most. Plan 2027 on 3–4 years of trends, not last year\'s cut-off. Talk to a mentor: {link}')}])

    add('mp_webinar', '🎥', 'Parent briefing / webinar', C,
        'Invitation and 1-hour reminder for a live parent briefing.', [
        {'key': 'invite', 'label': 'Invitation',
         'fields': [PARENT, _f('date', 'Date', '[Date]'), _f('time', 'Time', '[Time] IST / [Time] Gulf'),
                    BOOK],
         'subject': 'Free parent briefing: JEE 2027 → JoSAA → DASA explained in 45 minutes',
         'blocks': [
            ('p', 'Dear {name},'),
            ('p', 'You are invited to a free live briefing for Grade 11–12 NRI families.'),
            ('kv', [('Date', '{date}'), ('Time', '{time}')]),
            ('h', 'What we will cover'),
            ('ol', ['The 2027 calendar — JEE Main, JEE Advanced, JoSAA, DASA/CSAB',
                    'Who qualifies for DASA and CIWG (residency and 75% rules)',
                    'What the 2026 closing-rank data says about 2027',
                    'The documents to prepare now', 'Open Q&A with a senior mentor']),
            ('btn', '{link}', 'Reserve my seat')],
         'wa': 'Hello {name} 👋 Free parent briefing — JEE 2027 → JoSAA → DASA/CIWG in 45 min. {date}, {time}. Register: {link}'},
        {'key': 'reminder', 'label': '1-hour reminder',
         'fields': [PARENT, _f('time', 'Time', '[Time] IST / [Time] Gulf'), BOOK],
         'subject': 'Starting in 1 hour: your parent briefing',
         'blocks': [
            ('p', 'Dear {name},'),
            ('p', 'A quick reminder — our parent briefing starts in one hour, at **{time}**.'),
            ('btn', '{link}', 'Join the briefing')],
         'wa': '⏰ Reminder: our parent briefing starts in 1 hour — {time}. Join: {link}'}])

    add('mp_reengage', '🔁', 'Re-engagement — quiet leads', C,
        'For enquiries with no response in 30+ days, or after JEE Main Session 1.', [
        {'fields': [PARENT, STUDENT, BOOK],
         'subject': 'Where does {student}\'s plan stand for 2027?',
         'blocks': [
            ('p', 'Dear {name},'),
            ('p', 'The next 90 days decide a lot for the Class of 2027: Session 2 strategy, the Class 12 result against '
                  'the **75% rule**, and the document file for DASA/CIWG.'),
            ('p', 'If you would like a second pair of eyes on where {student} stands, a 20-minute conversation with a '
                  'senior mentor is free, with no obligation.'),
            ('btn', '{link}', 'Book a free conversation')],
         'wa': 'Hi {name}, just checking in — the next 90 days decide a lot for {student}. Would a free 20-min conversation help? {link}'}])

    # ============================ Enquiry & enrolment ============================ #
    C = 'Mentorship · Enquiry & enrolment'
    add('mp_enquiry_reply', '📮', 'Response to enquiry — mentorship', C,
        'First reply to a mentorship enquiry: orientation and what to bring to the call.', [
        {'fields': [PARENT, STUDENT, _f('grade', 'Grade / board', 'Grade 12 · CBSE'),
                    _f('routes', 'Routes of interest', 'DASA / CIWG / JoSAA'),
                    _f('mentor', 'Your name', 'Counsellor'),
                    _f('slots', 'Call options', 'Tue 6 pm, Wed 7 pm (IST)')],
         'subject': 'Thank you for your enquiry — EduAakashaa Mentorship',
         'blocks': [
            ('p', 'Dear {name},'),
            ('p', 'Thank you for reaching out about {student}\'s admission journey. I\'m {mentor}, and I\'ll be your first '
                  'point of contact.'),
            ('p', 'From what you shared ({grade}), the routes most relevant look like: **{routes}**. Our one-to-one tier, '
                  '**Elite Mentorship**, covers every eligible route in parallel with a dedicated senior mentor.'),
            ('p', 'The first step is a free initial discussion (20–30 minutes). Could you suggest a time? I can offer: {slots}.'),
            ('h', 'Please keep ready'),
            ('ol', ['Current grade, board and latest marks',
                    'Country of schooling for Classes 11 and 12',
                    'Nationality / passport status (Indian, OCI/PIO, other) and the parent\'s work country',
                    'Any colleges, branches or routes already on your mind'])],
         'wa': ('Hello {name}, thank you for contacting EduAakashaa 🙏 I\'m {mentor}. To help best for {student}, '
                'please share: latest marks/board · country of schooling for Classes 11–12 · passport status & parent\'s '
                'work country · routes you\'re considering. Good time for a 20-min call? {slots}')}])

    add('mp_scope', '📋', 'Scope of the mentorship', C,
        'Sent after the discovery call: what is in scope, out of scope, fee and next steps.', [
        {'fields': [PARENT, STUDENT, _f('fee', 'Programme fee', '₹74,999 incl. GST'),
                    _f('schedule', 'Payment schedule', '50% on enrolment · 25% at Month 4 · 25% at Month 8 or at counselling')],
         'subject': 'Scope of Elite Mentorship for {student} — what is included (and what is not)',
         'blocks': [
            ('p', 'Dear {name},'),
            ('p', 'It was a pleasure speaking with you and {student}. Here is what Elite Mentorship includes, so you can '
                  'decide with the full picture.'),
            ('h', 'The programme'),
            ('p', 'Grade 12 track · 10–12 months · three phases (Foundation + Build, Target, Execute) delivered through '
                  'our **5A method**: Assess → Analyze → Advise → Apply → Achieve.'),
            ('h', 'In scope'),
            ('ul', ['Admissions strategy across all eligible routes (DASA, CIWG, JEE Main, JoSAA/CSAB, TNEA and state routes) '
                    'with a live deadline and document calendar',
                    'A living roadmap, revised each term',
                    'Minimum 10 virtual 1:1 sessions with a lead counsellor, a domain mentor and an admissions specialist',
                    'Form preparation, verification and deadline tracking — the family authorises and submits',
                    'Parent briefings with written summaries',
                    'Premium portal for one year, choice-filling simulator and analytics reports']),
            ('h', 'Nine strategy deliverables'),
            ('ol', ['Onboard Assessment', 'Baseline Assessment and Eligibility Report', 'Admissions Roadmap (live)',
                    'Document and Deadline Calendar', 'Termly Progress and Course-Correction Notes',
                    'Target College and Branch List — reach, match, safe',
                    'DASA/CIWG and JoSAA Choice-Filling Strategy Pack', 'Final Seat Decision Brief',
                    'Parent Guidance Report and briefing summaries']),
            ('h', 'Out of scope'),
            ('ul', ['Subject tuition and JEE coaching — this is mentorship, not coaching',
                    'Guaranteed ranks, scores or seats',
                    'Submitting forms without family sign-off',
                    'Visa, passport and immigration processing',
                    'Financial, loan or forex advice']),
            ('h', 'Fee'),
            ('kv', [('Programme fee', '{fee}'), ('Payment schedule', '{schedule}')]),
            ('p', 'Anything beyond this scope (for example, support for named institutions) is agreed per family and written '
                  'into the engagement document with its price. If you would like to proceed, reply **"Proceed"** and we will '
                  'send the engagement agreement.'),
            ('note', NO_GUARANTEE)],
         'wa': ('Hi {name}, summary of *Elite Mentorship* for {student}: ✔ dedicated senior mentor ✔ 10+ 1:1 sessions '
                '✔ 9 strategy deliverables ✔ portal + simulator + analytics (1 yr) ✔ parent briefings. '
                '✘ Not included: tuition/coaching, guaranteed rank/seat, visa/loans. Fee: {fee} — {schedule}. '
                'Full details by email. Shall I send the agreement?')}])

    add('mp_meeting_confirm', '📅', 'Initial discussion — confirmation', C,
        'Confirm the first mentorship conversation (video / phone / in person).', [
        {'fields': [PARENT, STUDENT, _f('date', 'Date', '[Day, Date]'), _f('time', 'Time', '[Time] IST / [Time] Gulf'),
                    _f('where', 'Link / phone / venue', '[Video link]'), MENTOR],
         'subject': 'Confirmed: your EduAakashaa mentorship conversation on {date}',
         'blocks': [
            ('p', 'Dear {name},'),
            ('p', 'Your initial discussion is confirmed.'),
            ('kv', [('Date', '{date}'), ('Time', '{time}'), ('Where', '{where}'), ('With', '{mentor}')]),
            ('p', 'Please keep ready {student}\'s latest mark sheet, passport details, the parent\'s work-country details and '
                  'any college or route ideas. Please invite {student} to join — their voice matters.'),
            ('p', 'Need to reschedule? Just reply to this email or WhatsApp us on ' + WHATSAPP + '.')],
         'wa': '⏰ {name}, your EduAakashaa mentorship conversation is confirmed: {date}, {time}. {where}. Please keep {student}\'s marks & passport details ready.'}])

    add('mp_enrol_confirm', '✅', 'Enrolment & payment confirmation', C,
        'On receipt of the front payment and signed engagement document.', [
        {'fields': [PARENT, STUDENT, MENTOR, _f('amount', 'Amount received', '₹37,500'),
                    _f('date', 'Date', '[Date]'), _f('receipt', 'Receipt no.', '[____]'),
                    _f('next2', 'Next instalment', '25% at Month 4 (~[Month Year])')],
         'subject': 'Enrolment confirmed — {student}, Elite Mentorship (Class of 2027)',
         'blocks': [
            ('p', 'Dear {name},'),
            ('p', 'Welcome to EduAakashaa. We confirm the enrolment of **{student}** in Elite Mentorship — Grade 12 Track, Class of 2027.'),
            ('kv', [('Lead mentor', '{mentor}'), ('Payment received', '{amount} on {date}'),
                    ('Receipt no.', '{receipt}'), ('Next instalment', '{next2}')]),
            ('h', 'What happens next'),
            ('ol', ['Within 24 hours: your welcome message and portal login',
                    'Within 3 working days: the onboarding assessment link for {student} and for you',
                    'Within 7 days: the first mentor session']),
            ('p', 'Please keep this email. Your engagement document sets out scope, schedule, and our exit, cancellation and '
                  'confidentiality terms. Early exit within 30 days is refundable pro rata; cancellations are made in writing '
                  'from the registered parent email.')],
         'wa': 'Dear {name}, payment of {amount} received 🙏 ✅ {student} is enrolled in Elite Mentorship (Class of 2027). Mentor: {mentor}. Onboarding assessment link in 3 working days; first session within 7 days.'}])

    add('mp_instalment', '⏳', 'Instalment reminder — mentorship', C,
        'Seven days before the Month-4 and Month-8 instalments.', [
        {'fields': [PARENT, STUDENT, _f('which', 'Which instalment', 'second'),
                    _f('amount', 'Amount', '₹18,750'), _f('date', 'Due date', '[Date]'),
                    _f('pay', 'Payment link / details', SITE)],
         'subject': 'Gentle reminder: instalment due {date} — {student}\'s mentorship',
         'blocks': [
            ('p', 'Dear {name},'),
            ('p', 'A gentle reminder that the **{which} instalment of {amount}** for {student}\'s Elite Mentorship falls due '
                  'on **{date}**, as per the schedule in your engagement document.'),
            ('btn', '{pay}', 'Payment details'),
            ('p', 'Please share the reference once paid and we will send the receipt. If any change is needed, write to us in advance.')],
         'wa': 'Hi {name}, gentle reminder — {which} instalment of {amount} for {student}\'s mentorship is due on {date}. Details: {pay}. Thank you!'}])

    # ============================ Onboarding ============================ #
    C = 'Mentorship · Onboarding & assessment'
    add('mp_welcome', '👋', 'Welcome — new mentorship student / parent', C,
        'Welcome note within 24 hours of enrolment (student or parent).', [
        {'key': 'student', 'label': 'To the student',
         'fields': [_f('name', 'Student first name', 'there'), MENTOR,
                    _f('date', 'First session', '[Date, Time]'), _f('link', 'Portal link', SITE + '/login')],
         'subject': 'Welcome to EduAakashaa, {name} — here is how your journey begins',
         'blocks': [
            ('p', 'Dear {name},'),
            ('p', 'Welcome! Your parents have trusted us with something important, and we take it seriously. I\'m {mentor}, '
                  'your lead mentor.'),
            ('h', 'The next 10–12 months'),
            ('ul', ['**Phase 1 · Foundation + Build** — baseline assessment, eligibility locked, roadmap and documents drafted',
                    '**Phase 2 · Target** — JEE strategy, DASA/CIWG windows prepared, choice lists stress-tested',
                    '**Phase 3 · Execute** — forms, choice filling, seat decision and confirmation']),
            ('h', 'Your first week'),
            ('ol', ['Complete the onboarding questionnaire (about 10 minutes, nothing is graded)',
                    'Log in to your portal', 'First session: {date}']),
            ('p', 'One thing to remember: we are your guide, not your teacher. You do the studying; we help you decide what to '
                  'solve and which seat to choose.'),
            ('btn', '{link}', 'Open my portal'),
            ('note', 'Small steps. Consistent progress. Better decisions.')],
         'wa': ('Hi {name} 👋 Welcome to EduAakashaa! I\'m {mentor}, your lead mentor. First: a 10-min assessment '
                '(nothing graded), then our first session on {date}. We\'re your guide, not your teacher — you do the '
                'studying, we help you decide. Small steps. Consistent progress. 🚀')},
        {'key': 'parent', 'label': 'To the parent',
         'fields': [PARENT, STUDENT, MENTOR, _f('link', 'Portal link', SITE + '/login')],
         'subject': 'Welcome to EduAakashaa — {student}\'s mentorship begins',
         'blocks': [
            ('p', 'Dear {name},'),
            ('p', 'Thank you for trusting us with {student}\'s admission journey. {mentor} will be the lead mentor, supported '
                  'by a domain mentor and an admissions specialist.'),
            ('h', 'What you will receive'),
            ('ul', ['A parent assessment link and, soon after, {student}\'s Baseline Assessment and Eligibility Report',
                    'A parent briefing at each key gate, with a written summary',
                    'A monthly progress review (30 minutes) and quarterly course-correction notes']),
            ('p', 'Your role is the most under-appreciated one: dates and documents, the money conversation, and a calm '
                  'household in the exam months. We will guide you on each.'),
            ('btn', '{link}', 'Open the member portal')],
         'wa': 'Dear {name}, welcome to EduAakashaa 🙏 {mentor} is {student}\'s lead mentor. You\'ll get a parent assessment link shortly, then the baseline report and a briefing at each key gate.'}])

    add('mp_assess_invite', '🧭', 'Onboarding assessment — mentorship invite', C,
        'Invite students and parents to the onboarding assessment (separate forms).', [
        {'key': 'student', 'label': 'Student',
         'fields': [_f('name', 'Student first name', 'there'), _f('link', 'Assessment link', SITE + '/onboarding-assessment/student'),
                    _f('days', 'Complete by', '[Date]')],
         'subject': 'Your onboarding assessment — 10 minutes, nothing graded',
         'blocks': [
            ('p', 'Dear {name},'),
            ('p', 'Before our first session I would like to understand you — not just your marks. The assessment covers your '
                  'school day and study habits, the subjects you feel most and least confident in, what usually stops you '
                  'studying, the routes your family is considering, and what you want most from a mentor.'),
            ('kv', [('Time', 'About 10 minutes'), ('Marking', 'Nothing is graded'), ('Privacy', 'Only you, your parents and your mentor'),
                    ('Complete by', '{days}')]),
            ('btn', '{link}', 'Start my assessment')],
         'wa': 'Hi {name}, time for your onboarding assessment 📝 ~10 min, nothing graded: {link} — please complete by {days}.'},
        {'key': 'parent', 'label': 'Parent',
         'fields': [PARENT, STUDENT, _f('link', 'Assessment link', SITE + '/onboarding-assessment/parent'),
                    _f('days', 'Complete by', '[Date]')],
         'subject': 'Parent onboarding assessment for {student} — 8 minutes',
         'blocks': [
            ('p', 'Dear {name},'),
            ('p', 'Parents see what we cannot: the household routine, finances, travel plans and the pressures around the '
                  'student. A short parent assessment helps us build a plan the whole family can sustain.'),
            ('ul', ['Your goals and expectations for {student}', 'Routes and countries under consideration',
                    'Budget comfort zones for tuition, hostel and travel',
                    'Documents already available (passport, visa, employer certificate, mark sheets)',
                    'Practical constraints — relocation, siblings, work schedules']),
            ('p', 'About **8 minutes**. Please complete it by **{days}**, and let {student} complete their own assessment '
                  'independently — their honest answers are the foundation of the plan.'),
            ('btn', '{link}', 'Start the parent assessment')],
         'wa': 'Hello {name} 🙏 Please complete the parent assessment for {student} (8 min): {link} — by {days}. Please let {student} fill theirs separately.'}])

    add('mp_assess_report', '📄', 'Assessment report sharing', C,
        'Share the Baseline Assessment & Eligibility Report and book the walkthrough.', [
        {'fields': [PARENT, STUDENT, _f('date', 'Walkthrough', '[Date, Time]'), BOOK],
         'subject': '{student}\'s Baseline Assessment & Eligibility Report is ready',
         'blocks': [
            ('p', 'Dear {name} and {student},'),
            ('p', 'The **Baseline Assessment and Eligibility Report** is attached. It is the first stage (Assess) of our 5A '
                  'method and the foundation for your Admissions Roadmap.'),
            ('h', 'What is in the report'),
            ('ol', ['Profile — interests, strengths, study habits and constraints',
                    'Eligibility check — residency (two years of Classes 11–12 abroad), CIWG status, the 75% / 7.5 CGPA rule '
                    'and the subject combination, route by route',
                    'Document gaps — what is ready and what must be collected, with dates',
                    'Early observations — strengths and areas to work on',
                    'Proposed priorities for the next 30 days']),
            ('p', 'Please read it as a starting point, not a verdict. Eligibility is stated against the **2026 rules** and will '
                  'be re-verified against the official 2027 brochure when published.'),
            ('kv', [('Walkthrough', '{date}')]),
            ('btn', '{link}', 'Join the walkthrough'),
            ('note', 'The report is confidential — for the enrolled student and family only. ' + NO_GUARANTEE)],
         'wa': 'Hi {name}, {student}\'s Baseline Assessment & Eligibility Report is ready 📄 (sent by email). Walkthrough: {date} — {link}. It\'s a starting point, not a verdict.'}])

    # ============================ Programme ============================ #
    C = 'Mentorship · Programme communication'
    add('mp_exam_schedule', '🗓️', 'Exam schedule information — Class of 2027', C,
        'Key exam and counselling dates, split into confirmed and expected. Update the "as of" date each send.', [
        {'fields': [PARENT, STUDENT, _f('asof', 'As of', '[Date]'),
                    _f('todo', 'This month\'s action', 'Confirm exam city choices and keep documents scanned to NTA size limits')],
         'subject': 'Class of 2027 calendar — key exam and counselling dates (as of {asof})',
         'blocks': [
            ('p', 'Dear {name},'),
            ('p', 'Here is the current admissions calendar for {student}\'s Class of 2027, as of **{asof}**. We have marked what '
                  'is listed as confirmed and what is expected from past cycles.'),
            ('h', '✅ Confirmed / listed'),
            ('ul', ['**JEE Main Session 1** — 22–24 and 28–30 January 2027 (buffer day 31 Jan), computer-based test; '
                    'subject to the NTA notification']),
            ('h', '🟠 Expected — to be confirmed'),
            ('ul', ['JEE Main Session 1 registration — late October to late November 2026',
                    'Session 1 result — February 2027',
                    'Session 2 — registration February, exam early April 2027',
                    'Final NTA score and All India Rank — late April 2027',
                    'JEE Advanced (IIT route) — registration late April–early May, exam mid-May, result early June 2027',
                    'JoSAA counselling — June–July 2027',
                    'DASA / CSAB-Special — late July–August 2027 (the 2027 brochure is not yet published; 2026 ran '
                    '28 July–18 August in two rounds)',
                    'Private NRI applications (Amrita, VIT etc.) — from November 2026',
                    'NATA — expected April–June 2027 · NID DAT prelims — tentatively late December 2026']),
            ('h', 'This month\'s action'),
            ('p', '{todo}'),
            ('note', 'Please verify each date on the official sites before acting: nta.ac.in, jeeadv.ac.in, josaa.nic.in, '
                     'csab.nic.in. We re-check every date for you and will alert you the day a notification is published.')],
         'wa': ('📅 Class of 2027 key dates (as of {asof}): ✅ JEE Main S1: 22–30 Jan 2027 (subject to NTA notice) · '
                '🟠 Registration: late Oct–Nov 2026 · 🟠 S2: April · 🟠 Advanced: mid-May · 🟠 JoSAA: Jun–Jul · '
                '🟠 DASA/CSAB: late Jul–Aug (2027 brochure awaited). Always verify on official sites.')}])

    add('mp_newsletter', '🌟', 'Motivational newsletter — students', C,
        'Monthly note to students: one thought, one habit, one reflection. Praise only what is true.', [
        {'fields': [_f('name', 'Student first name', 'there'), _f('month', 'Month', '[Month]'),
                    _f('thought', 'This month\'s thought',
                       'Nothing dramatic this week, and that is the point. Four steady weeks are worth more than one brilliant day.'),
                    _f('habit', 'This month\'s one habit',
                       'Write the reason for every mistake in your error log — five minutes, every evening.'),
                    _f('coming', 'Coming up', '[Upcoming exam / registration / session]')],
         'subject': 'Small steps, steady weeks — your {month} note from EduAakashaa',
         'blocks': [
            ('p', 'Dear {name},'),
            ('p', '**This month\'s thought**'),
            ('p', '“{thought}”'),
            ('h', 'The comparison trap'),
            ('p', 'It is easy to measure yourself against a friend\'s mock score or a topper in the coaching class. You are not '
                  'running their race. Look at your own line on your dashboard — is it going the right way?'),
            ('h', 'This month\'s one habit'),
            ('p', '{habit}'),
            ('h', 'A two-minute reflection'),
            ('ul', ['What was my hardest moment this month, and how did I handle it?',
                    'What did I do that I am proud of?', 'Which one study block will I protect next week?']),
            ('h', 'Coming up'),
            ('p', '{coming}'),
            ('note', 'Small steps. Consistent progress. Better decisions. A mock is a measurement, not a verdict — ask for '
                     'help early; that is what we are here for.')],
         'wa': 'Hi {name} 🌟 “{thought}” You are not running anyone else\'s race — look at your own line. This month\'s habit: {habit} 💪'}])

    add('mp_monthly_report', '📈', 'Monthly progress report', C,
        'One-page summary after the 30-minute monthly review. Private to student, parents and mentor.', [
        {'fields': [PARENT, STUDENT, _f('month', 'Month', '[Month Year]'), MENTOR,
                    _f('blocks', 'Study blocks completed', '[x]/[y] ([%])'),
                    _f('mock', 'Latest mock', 'score [__] · accuracy [__]%'),
                    _f('conf', 'Confidence · Consistency (1–5)', '[x] · [y]'),
                    _f('keep', 'One habit to keep', '[habit]'), _f('change', 'One habit to change', '[habit]'),
                    _f('support', 'Support needed from home', '[request]'),
                    _f('p1', 'Priority 1', '[priority + measure]'), _f('p2', 'Priority 2', '[priority + measure]'),
                    _f('p3', 'Priority 3', '[priority + measure]'), _f('next', 'Next review', '[Date]')],
         'subject': '{student} — progress review, {month}',
         'blocks': [
            ('p', 'Dear {name},'),
            ('p', 'Thank you for joining {student}\'s monthly review with {mentor}. Here is the one-page summary.'),
            ('kv', [('Study blocks completed', '{blocks}'), ('Latest mock', '{mock}'),
                    ('Confidence · Consistency', '{conf}')]),
            ('h', 'What helped · What did not'),
            ('ul', ['**Keep:** {keep}', '**Change:** {change}']),
            ('h', 'Support needed from home'),
            ('p', '{support}'),
            ('h', 'Agreed priorities for next month'),
            ('ol', ['{p1}', '{p2}', '{p3}']),
            ('kv', [('Next review', '{next}')]),
            ('note', 'We look at habits before results, and compare {student} only with {student}. Please avoid comparisons '
                     'with other children. This report is private to student, parents and mentor.')],
         'wa': '📊 {student} — {month} review: study blocks {blocks} · mock {mock} · confidence/consistency {conf}. Keep: {keep}. Change: {change}. Next review: {next}.'}])

    add('mp_quarterly_review', '🧮', 'Quarterly review & course-correction notes', C,
        'Termly review against the Admissions Roadmap, with written course-corrections.', [
        {'fields': [PARENT, STUDENT, _f('quarter', 'Quarter', '[Quarter, Year]'),
                    _f('planned', 'Milestones planned', '[x]'), _f('done', 'Milestones achieved', '[y]'),
                    _f('well', 'What went well', '[2–3 specific observations]'),
                    _f('attention', 'What needs attention', '[2–3 items with evidence]'),
                    _f('fix1', 'Course-correction 1', '[change — owner — by when]'),
                    _f('fix2', 'Course-correction 2', '[change — owner — by when]'),
                    _f('sessions', 'Sessions used', '[x] of 10+'), _f('call', 'Parent review call', '[Date, Time]'),
                    BOOK],
         'subject': '{student} — quarterly review & course-correction notes, {quarter}',
         'blocks': [
            ('p', 'Dear {name} and {student},'),
            ('p', 'Please find the quarterly review for **{quarter}**, measured against the Admissions Roadmap.'),
            ('kv', [('Roadmap milestones', '{done} of {planned} achieved'), ('Sessions used', '{sessions}')]),
            ('h', 'What went well'), ('p', '{well}'),
            ('h', 'What needs attention'), ('p', '{attention}'),
            ('h', 'Course-corrections'),
            ('ol', ['{fix1}', '{fix2}']),
            ('kv', [('Parent review call', '{call}')]),
            ('btn', '{link}', 'Join the review call'),
            ('note', 'Rules, fees and dates for the 2027 cycle are re-verified against official notifications as they are '
                     'published. ' + NO_GUARANTEE)],
         'wa': '{student} — quarterly review for {quarter} is in your inbox 📋 {done} of {planned} milestones achieved. Parent review call: {call} — {link}'}])

    add('mp_parent_briefing', '🧑‍🤝‍🧑', 'Parent briefing — at each gate', C,
        'Before JEE Main registration, Session 2, JoSAA and DASA registration.', [
        {'fields': [PARENT, _f('gate', 'Gate', 'DASA/CIWG registration'), _f('date', 'Date', '[Date]'),
                    _f('time', 'Time', '[Time] IST / [Time] Gulf'), BOOK],
         'subject': 'Parent briefing before {gate} — {date}',
         'blocks': [
            ('p', 'Dear {name},'),
            ('p', 'As part of the programme we hold a parent briefing at each key gate. The next one is ahead of **{gate}**.'),
            ('kv', [('Date', '{date}'), ('Time', '{time}'), ('Duration', '30–40 minutes')]),
            ('h', 'Agenda'),
            ('ol', ['What changes now, and what the official notification says', 'Your documents checklist',
                    'The cost worksheet and the decisions the family must make', 'Q&A']),
            ('btn', '{link}', 'Join the briefing'),
            ('note', 'A written summary will follow in your inbox.')],
         'wa': 'Hello {name}, your parent briefing before *{gate}* is on {date}, {time}. Join: {link}. Written summary to follow.'}])

    add('mp_docs_checklist', '📂', 'Document checklist status — DASA / CIWG', C,
        'Weekly nudge from three months before the window. A missing paper can cost the round.', [
        {'fields': [PARENT, STUDENT, _f('asof', 'As of', '[Date]'), _f('ready', 'Ready', '[list]'),
                    _f('pending', 'Pending (owner · due date)', '[list]')],
         'subject': 'Document checklist for {student} — status as of {asof}',
         'blocks': [
            ('p', 'Dear {name},'),
            ('p', 'In DASA a missing paper can cost the round, so we build the file early. Status as of **{asof}**:'),
            ('kv', [('Ready ✅', '{ready}'), ('Pending ⏳', '{pending}')]),
            ('h', 'The checklist (2026 rules — re-checked against the 2027 brochure)'),
            ('ul', ['Student passport and proof of date of birth',
                    'Mark sheets for Classes 10, 11 and 12',
                    'School certificate confirming Classes 11 and 12 abroad',
                    'Percentage / CGPA equivalence where the board grades differently',
                    'Medical certificate in the prescribed format',
                    'OCI or PIO card, where applicable',
                    'CIWG: parent\'s passport, visa and work permit valid in the admission year',
                    'CIWG: employer certificate in the prescribed format']),
            ('p', 'Please keep one folder (digital and paper) and one calendar, and reply with any item you need help obtaining.')],
         'wa': 'Hi {name}, document file for {student} as of {asof}: ✅ {ready} · ⏳ pending: {pending}. Need help? Reply here.'}])

    add('mp_rule_alert', '🔔', 'Official notification alert', C,
        'Send the day an official brochure, schedule or notice is published (e.g. DASA 2027).', [
        {'fields': [PARENT, STUDENT, _f('doc', 'Document', 'DASA 2027 Information Brochure'),
                    _f('date', 'Published on', '[Date]'), _f('source', 'Official source', 'https://csab.nic.in'),
                    _f('c1', 'Change 1', '[change vs 2026]'), _f('c2', 'Change 2', '[change vs 2026]'),
                    _f('impact', 'What it means for the student', '[specific impact]'),
                    _f('call', 'Call', '[Date, Time]')],
         'subject': 'Important: {doc} has been published',
         'blocks': [
            ('p', 'Dear {name},'),
            ('p', 'The **{doc}** was published on {date}.'),
            ('h', 'What changed (vs 2026)'),
            ('ul', ['{c1}', '{c2}']),
            ('h', 'What it means for {student}'),
            ('p', '{impact}'),
            ('p', 'We will update the Admissions Roadmap and document calendar and hold a short call on **{call}**.'),
            ('btn', '{source}', 'View the official notice'),
            ('note', 'Please do not act on forwarded summaries without checking the official notice.')],
         'wa': '🔔 Official update: {doc} published on {date} ({source}). Changes: {c1}; {c2}. Impact on {student}: {impact}. Call: {call}.'}])

    add('mp_seat_decision', '🎯', 'Final seat decision brief', C,
        'Delivered at allotment, before the family freezes, floats, slides or exits.', [
        {'fields': [PARENT, STUDENT, _f('seat', 'Allotted seat', '[Institute · Branch]'),
                    _f('deadline', 'Decision deadline', '[Date, Time]'), _f('call', 'Decision call', '[Date, Time]'), BOOK],
         'subject': '{student} — Final Seat Decision Brief (decision due {deadline})',
         'blocks': [
            ('p', 'Dear {name} and {student},'),
            ('p', 'The allotment result is out. Attached is the **Final Seat Decision Brief**.'),
            ('kv', [('Allotted seat', '{seat}'), ('Decision deadline', '{deadline}'), ('Decision call', '{call}')]),
            ('h', 'In the brief'),
            ('ul', ['The allotted seat — institute, branch, category and fee tier',
                    'Your options — Freeze, Slide, Float, Surrender, Withdraw, Exit — and what each costs',
                    'Comparison with your target list: branch, placements, fees, location, hostel',
                    'Total cost worksheet and documents for physical reporting',
                    'Our recommendation, and the honest risks']),
            ('p', 'The decision is yours — we prepare the picture, you make the choice.'),
            ('btn', '{link}', 'Join the decision call')],
         'wa': '🎯 {student}: Final Seat Decision Brief for {seat} is in your inbox. Decision due {deadline}. Call: {call} — {link}'}])

    # ============================ Team ============================ #
    C = 'Mentorship · Team'
    add('mp_mentor_assign', '🧑‍🏫', 'Mentor — new student assignment brief', C,
        'Internal email to a lead / domain mentor / admissions specialist.', [
        {'fields': [_f('name', 'Mentor first name', 'there'), STUDENT,
                    _f('role', 'Role', 'Lead mentor'), _f('grade', 'Grade · board · country', 'Grade 12 · CBSE · UAE'),
                    _f('parent', 'Parent contact', '[name · phone · email]'), _f('routes', 'Routes of interest', 'DASA / CIWG / JoSAA'),
                    _f('flags', 'Eligibility flags', '[e.g., OCI holder — no CIWG]'), _f('start', 'Programme start', '[Date]'),
                    _f('first', 'First session by', '[Date]'), _f('link', 'Assessments link', SITE + '/admin')],
         'subject': 'New assignment: {student} · {grade} · Class of 2027',
         'blocks': [
            ('p', 'Hi {name},'),
            ('p', 'You have been assigned as **{role}** for the student below.'),
            ('kv', [('Student', '{student}'), ('Grade · board · country', '{grade}'), ('Parent contact', '{parent}'),
                    ('Routes of interest', '{routes}'), ('Eligibility flags', '{flags}'),
                    ('Programme start', '{start}')]),
            ('h', 'First 7 days'),
            ('ol', ['Review the onboarding assessments (student and parent)',
                    'Hold session 1 by {first}, using the session-notes format',
                    'Draft the Baseline Assessment and Eligibility Report within 5–7 working days',
                    'Set up the document and deadline calendar']),
            ('h', 'Working principles'),
            ('ul', ['We are a guide, not a teacher — no subject tuition and no guaranteed outcomes',
                    'The family authorises and submits every application; we prepare and verify',
                    'Student data and reports are confidential and never posted in groups or compared',
                    'Praise only what is true; record concerns for parent or professional follow-up',
                    'Re-verify every rule and date against the official notification before advising']),
            ('btn', '{link}', 'Open the assessments'),
            ('note', 'Please acknowledge today and flag any conflict or capacity issue.')]}])

    add('mp_mentor_monthly', '🗂️', 'Mentor — monthly review & notes reminder', C,
        'Last week of every month.', [
        {'fields': [_f('name', 'Team / first name', 'team'), _f('month', 'Month', '[Month Year]'),
                    _f('due', 'Due by', '[Date]'), _f('focus', 'This month\'s focus', '[e.g., JEE Main registration check]')],
         'subject': 'Monthly review & session-notes check — {month}',
         'blocks': [
            ('p', 'Hi {name},'),
            ('p', 'Monthly check-in. Please complete by **{due}**:'),
            ('ol', ['Session notes uploaded for every session held this month',
                    'Monthly progress review held and the one-page report sent to each parent',
                    'Document and deadline calendars updated',
                    'Any student with a missed session or falling confidence flagged to me']),
            ('h', 'This month\'s focus'),
            ('p', '{focus}'),
            ('h', 'Reminders'),
            ('ul', ['Minimum 10 virtual 1:1 sessions per student across the programme — check each student\'s usage',
                    'Quarterly course-correction notes are due for the students on your list']),
            ('p', 'Please reply with a short status for your students by {due}.')]}])

    # ============================ Closing ============================ #
    C = 'Mentorship · Closing'
    add('mp_congrats', '🎉', 'Congratulations & thank-you', C,
        'After seat confirmation / reporting.', [
        {'fields': [PARENT, STUDENT, _f('institute', 'Institute / programme', '[Institute · Branch]'),
                    _f('link', 'Feedback link', SITE)],
         'subject': 'Congratulations, {student} — and thank you',
         'blocks': [
            ('p', 'Dear {name} and {student},'),
            ('p', 'Congratulations on {student}\'s admission to **{institute}**. It has been a privilege to walk this road '
                  'with your family.'),
            ('p', 'What made the difference was the steady work — the planner, the tracker, the conversations at home, and '
                  'decisions made with good information.'),
            ('p', 'Would you share a few lines about your experience? If another family could benefit, we would be glad to be '
                  'introduced.'),
            ('btn', '{link}', 'Share your feedback'),
            ('p', 'We wish {student} a wonderful journey ahead.')],
         'wa': '🎉 Congratulations, {student}! Your seat at {institute} is confirmed. So proud of the effort and the choices along the way. We\'re here for questions till you settle in.'}])

    add('mp_feedback', '💬', 'Feedback & testimonial request — mentorship', C,
        'At the programme midpoint (Month 4) or 30 days after seat confirmation.', [
        {'fields': [PARENT, _f('link', 'Feedback form link', SITE)],
         'subject': 'Two minutes of your time: how are we doing, {name}?',
         'blocks': [
            ('p', 'Dear {name},'),
            ('p', 'We would value your honest feedback on the mentorship so far.'),
            ('ul', ['What has helped most?', 'What could be better?',
                    'May we quote a line from you (first name only, with your permission)?']),
            ('btn', '{link}', 'Share feedback (2 minutes)')],
         'wa': 'Hi {name}, would you share 2 minutes of feedback on the mentorship? 🙏 {link}'}])

    add('mp_exit_ack', '📨', 'Cancellation / early-exit acknowledgement', C,
        'On a written request from the registered parent email. Confirm within 3 working days; settle within 14.', [
        {'fields': [PARENT, STUDENT, _f('date', 'Request dated', '[Date]'),
                    _f('outcome', 'Applicable clause & refund', '[clause and calculation]')],
         'subject': 'Acknowledgement of your request — {student}\'s mentorship',
         'blocks': [
            ('p', 'Dear {name},'),
            ('p', 'We acknowledge your written request dated **{date}** regarding {student}\'s Elite Mentorship.'),
            ('p', 'As per the engagement document:'),
            ('ul', ['Within 30 days of enrolment, the fee paid is refundable pro rata for sessions and deliverables not yet '
                    'used, less a one-time administration charge; portal access and materials already issued are revoked',
                    'After 30 days the fee is non-refundable, because mentor and specialist time has been committed']),
            ('kv', [('Your case', '{outcome}')]),
            ('p', 'Any refund is settled within 14 working days. We are sorry to see you go, and the door remains open. '
                  'Please keep programme materials confidential, as set out in the engagement document.')]}])

    return T
