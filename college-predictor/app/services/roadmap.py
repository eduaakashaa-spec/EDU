"""Admission roadmap of one student (e.g. "Darsh Roadmap"): milestones per university and their dates in the student's calendar.

A roadmap belongs to one mentorship enrolment, so the people who can open it are exactly the people who can open that enrolment
(the student, parents an admin linked, the assigned mentor, admins). Everyone else gets a 404 from `mentorship.role_for`.

The built-in template is the NUS · NTU · HKU engineering 2027 route for a CBSE Class 12 student, built from the EduAakashaa
admission matrix (30 Oct 2026) and the parents' guide (17 Nov 2026). Dates are what those pages said on those days: each one
carries its source and, where the university's own page was read, the date it was verified. Admin and mentors can add milestones.
"""
from datetime import date

from app.extensions import db
from app.models_mentorship import MsEvent, MsMilestone, MsRoadmap
from app.services import mentorship as svc

TEMPLATE_ID = 'sg-hk-2027'

# group code -> (heading, one line, colour)
GROUPS = {
    'PREP': ('Prepare · all three', 'Shortlist, documents and the family decisions that come first.', '#0E3A8A'),
    'HKU': ('HKU · Hong Kong', 'Earliest deadline and earliest offers. Round 1 closes 25 Nov 2026.', '#1B7A4E'),
    'NUS': ('NUS · Singapore', 'Window 16 Dec 2026 to 17 Feb 2027. Outcome by July 2027.', '#E4572E'),
    'NTU': ('NTU · Singapore', 'Window 15 Oct 2026 to 19 Mar 2027. Outcome around end July 2027.', '#C1272D'),
}
UNIVERSITIES = ('HKU', 'NUS', 'NTU')
OWNERS = {'student': '{name}', 'parent': 'Parents', 'mentor': 'Mentor', 'family': 'Family'}

SRC_MATRIX = 'EduAakashaa admission matrix, prepared 30 Oct 2026'
SRC_DECK = "EduAakashaa parents' guide (NTU, NUS, HKU), checked 17 Nov 2026"
SRC_HKU = "HKU International / Non-JUPAS page, as read in the parents' guide on 17 Nov 2026"
SRC_NUS = "NUS Important Dates AY2027/28, as read in the parents' guide on 17 Nov 2026"
SRC_NTU = "NTU India Standard 12 page, as read in the parents' guide on 17 Nov 2026"
V17 = date(2026, 11, 17)

# (group, title, detail, owner, due_on, due_label, calendar category or None, source, verified_on, final)
M = []


def _m(grp, title, detail='', owner='student', due=None, label='', cat=None, src=SRC_MATRIX, ver=None, final=False):
    M.append(dict(grp=grp, title=title, detail=detail, owner=owner, due_on=due, due_label=label, cat=cat, source=src, verified_on=ver, final=final))


# ---- prepare ---------------------------------------------------------------------------------------------------------------------
_m('PREP', 'Confirm the programme at each university and its subject prerequisites',
   'Check each programme against {name}\'s Class 11 and 12 subjects. Engineering needs Mathematics; Computer Engineering at NUS also needs Physics or Chemistry.',
   'student', date(2026, 11, 6))
_m('PREP', 'Scan passport, Class 10 and Class 11 marksheets and CBSE admit card details',
   'Check that every name and date matches across the documents. Never send passport details over WhatsApp.', 'parent', date(2026, 11, 8))
_m('PREP', 'Write to HKU to confirm the 2027 first-round date for Indian-board applicants',
   "HKU's India page still showed the previous cycle's dates in October.", 'mentor', date(2026, 11, 10))
_m('PREP', "Mentor reviews the shortlist against {name}'s actual subjects and predicted marks", '', 'mentor', date(2026, 11, 12))
_m('PREP', 'Decide the budget ceiling and the Tuition Grant work-bond question',
   'The grant takes Singapore tuition to about S$21,400 a year but carries a 3-year work bond in Singapore. Decide before accepting any offer.',
   'parent', date(2026, 11, 15))
_m('PREP', 'Final shortlist, passports valid, budget fixed', 'Everything the three forms need is ready before the Singapore windows open.',
   'family', date(2026, 12, 15), cat='Other', src=SRC_DECK, ver=V17)

# ---- HKU -------------------------------------------------------------------------------------------------------------------------
_m('HKU', 'Personal statement final; referee or nominated teacher briefed', 'Send the draft to the mentor first.', 'student',
   date(2026, 11, 18), cat='Documents')
_m('HKU', 'Mentor reviews the statement and the full application before submission', '', 'mentor', date(2026, 11, 20), cat='Documents')
_m('HKU', 'Application complete: results keyed in and the HK$780 fee paid',
   'Our target, two days ahead of the cut-off. Predicted and Class 11 results are keyed into the HKU system, not only uploaded.',
   'parent', date(2026, 11, 22), cat='Other')
_m('HKU', 'HKU first round closes (noon Hong Kong time)',
   '9:30 am India time, 8:00 am UAE time. Submit well before. The matrix of 30 Oct called this date counsellor-reported; the parents\' guide of 17 Nov '
   "cites HKU's page. Confirm on your HKU portal.",
   'student', date(2026, 11, 25), cat='Admission deadline', src=SRC_HKU, ver=V17)
_m('HKU', 'Counsellor or teacher reference submitted', 'Due 1 Dec according to the parents\' guide.', 'mentor', date(2026, 12, 1), cat='Documents', src=SRC_DECK)
_m('HKU', 'Interview, if invited', 'Interviews ran from November to January last cycle. Practise with the mentor.', 'student', label='Nov 2026 to Jan 2027')
_m('HKU', 'First-round offers can arrive', 'Accept within three to four weeks of an offer and pay the non-refundable deposit.', 'student',
   date(2026, 12, 1), cat='Admission deadline', src="HKU general information 2027 admission, as read in the admission matrix", ver=None)
_m('HKU', 'Offer accepted and deposit paid', 'Read the offer terms together, including deposit dates.', 'parent', label='Within 3 to 4 weeks of the offer')
_m('HKU', 'Actual Class 12 results keyed into the HKU system', 'Results day starts the clock. Keep the phone and email on.', 'student', label='Results day + 3 days')
_m('HKU', 'Student visa, housing and budget started', "HKU's guidance: 4 to 6 weeks for assessment and 8 to 10 weeks for the visa.", 'parent', label='After accepting')
_m('HKU', 'HKU admission complete', 'Offer accepted, deposit paid, visa and housing under way.', 'family', label='Entry September 2027', final=True)

# ---- NUS -------------------------------------------------------------------------------------------------------------------------
_m('NUS', 'NUS window opens: start the form', 'International Qualifications route, including CBSE. Use the Applicant Portal.', 'student',
   date(2026, 12, 16), cat='Admission deadline', src=SRC_NUS, ver=V17)
_m('NUS', 'Submit the NUS application (our target)', 'Two weeks before the close, so a technical fault or a missing document leaves room.', 'student',
   date(2027, 1, 31), cat='Other')
_m('NUS', 'Pay the S$20 application fee by card', 'Check junk mail for emails from the Office of Admissions.', 'parent', label='With the form')
_m('NUS', 'Apply for the scholarships {name} is eligible for', 'NUS International Undergraduate Scholarship and the Science & Technology scholarship were reported as open to Indian applicants.',
   'student', label='When applying')
_m('NUS', 'Confirm the submission shows as complete in the portal', '', 'mentor', date(2027, 2, 10), cat='Other')
_m('NUS', 'NUS window closes (11:59 pm Singapore time)',
   "The page read gave no closing time; last year's pattern was 11:59 pm. That is 7:59 pm in the UAE and 9:29 pm in India. Confirm on the portal.",
   'student', date(2027, 2, 17), cat='Admission deadline', src=SRC_NUS, ver=V17)
_m('NUS', 'Upload the final CBSE results in the Applicant Portal', 'Miss this and the application is incomplete. Agree beforehand who uploads.',
   'student', label='Results day + 3 days')
_m('NUS', 'NUS outcome released', 'Most international applicants hear online by July 2027.', 'student', date(2027, 7, 31), cat='Admission deadline',
   src=SRC_NUS, ver=V17)
_m('NUS', 'Offer accepted; Tuition Grant and bond decided', 'Compare scholarship, bond and total cost, then respond inside the stated window.', 'family',
   label='On the offer')
_m('NUS', "Student's Pass, housing and budget started", '', 'parent', label='After accepting')
_m('NUS', 'NUS admission complete', 'Offer accepted, Student\'s Pass and housing under way.', 'family', label='Entry August 2027', final=True)

# ---- NTU -------------------------------------------------------------------------------------------------------------------------
_m('NTU', 'Submit the NTU India Standard 12 form (our target)',
   'The form cannot be saved: block one uninterrupted sitting of about 20 minutes. The window opened on 15 Oct 2026. Minimum 93% average, English included.',
   'student', date(2027, 1, 31), cat='Other')
_m('NTU', 'Pay the S$25 application fee on the status page', 'PayNow, Visa or MasterCard. Non-refundable. Keep every receipt.', 'parent', label='With the form')
_m('NTU', 'NTU window closes: form, fee, declarations and programme choices',
   'NTU gives no closing time, so treat 18 March as the last safe day (UAE time).', 'student', date(2027, 3, 19), cat='Admission deadline', src=SRC_NTU, ver=V17)
_m('NTU', 'Supporting documents uploaded', "Taken from NTU's timetable for other international qualifications: confirm on your Check Status page.",
   'student', date(2027, 3, 22), cat='Documents', src=SRC_NTU)
_m('NTU', 'Upload the Class 12 result slip and CBSE admit card', 'Within 3 days of release. Late means an incomplete application and NTU decides on actual results only.',
   'student', label='Results day + 3 days')
_m('NTU', 'NTU outcome (estimated)', 'NTU estimates the end of July 2027 for India Standard 12; some offers may start from March.', 'student',
   date(2027, 7, 31), cat='Admission deadline', src=SRC_NTU, ver=V17)
_m('NTU', 'Offer accepted; Tuition Grant and bond decided', 'The same 3-year work bond applies to the grant.', 'family', label='On the offer')
_m('NTU', "Student's Pass, housing and budget started", '', 'parent', label='After accepting')
_m('NTU', 'NTU admission complete', 'Offer accepted, Student\'s Pass and housing under way.', 'family', label='Entry August 2027', final=True)

# an exam, not a milestone: shown in the calendar so the family can see it next to the deadlines
EXTRA_EVENTS = [
    dict(title='CBSE Class 12 board exams (window; date sheet to be confirmed)', category='Board exam', starts_on=date(2027, 2, 15), ends_on=date(2027, 3, 31),
         notes='A placeholder window for February to March 2027. Replace it with the dates from the CBSE date sheet for your centre as soon as it is published.',
         source='EduAakashaa admission matrix: Feb to Mar 2027, follow the CBSE date sheet', verified_on=None),
]


def first_name(e):
    return (e.preferred_name or (e.student.name or '').split(' ')[0] or 'Student').strip()


def owner_label(code, e):
    return OWNERS.get(code, code or '').format(name=first_name(e))


def get(e):
    return MsRoadmap.query.filter_by(enrolment_id=e.id).first()


def create(e, title=None, user_id=None):
    """Create the roadmap from the template, with calendar events for the dated milestones. Returns the roadmap, or None if one exists."""
    if get(e):
        return None
    name = first_name(e)
    rm = MsRoadmap(enrolment_id=e.id, title=(title or f'{name} Roadmap')[:120], subtitle='Engineering 2027 entry · NUS · NTU · HKU',
                   template=TEMPLATE_ID, created_by=user_id,
                   note=("Prepared from the EduAakashaa admission matrix (30 Oct 2026) and the parents' guide (17 Nov 2026). Dates and fees change every cycle: "
                         "confirm each one on the university's own portal before acting."))
    db.session.add(rm)
    db.session.flush()
    for pos, t in enumerate(M):
        ev = None
        d = t['due_on']
        if d and t['cat']:
            ev = MsEvent(enrolment_id=e.id, title=f"{t['grp']}: {t['title'].format(name=name)}"[:240], category=t['cat'], starts_on=d,
                         notes=(t['detail'] or '').format(name=name), source=t['source'], verified_on=t['verified_on'], created_by=user_id)
            db.session.add(ev)
            db.session.flush()
        db.session.add(MsMilestone(roadmap_id=rm.id, grp=t['grp'], title=t['title'].format(name=name), detail=(t['detail'] or '').format(name=name),
                                   owner=t['owner'], due_on=d, due_label=t['due_label'], position=pos, final=t['final'],
                                   event_id=ev.id if ev else None, source=t['source'], verified_on=t['verified_on']))
    for x in EXTRA_EVENTS:
        db.session.add(MsEvent(enrolment_id=e.id, created_by=user_id, **x))
    svc.audit(e, 'roadmap.created', rm.title)
    db.session.commit()
    return rm


def status(m, today):
    """('done' | 'overdue' | 'soon' | 'open' | 'later', short text) for the chip next to a milestone."""
    if m.done:
        return 'done', 'Done' + (f' {m.done_on.strftime("%d %b")}' if m.done_on else '')
    if m.due_on:
        n = (m.due_on - today).days
        if n < 0:
            return 'overdue', f'Overdue by {-n} day' + ('' if n == -1 else 's')
        if n == 0:
            return 'soon', 'Due today'
        if n <= 7:
            return 'soon', f'Due in {n} day' + ('' if n == 1 else 's')
        return 'open', m.due_on.strftime('%d %b %Y')
    return 'later', m.due_label or 'No date yet'


def summary(rm, today):
    """Per group: counts, percentage, the next open milestone and whether the final milestone is done."""
    out = {}
    for code in GROUPS:
        ms = [m for m in rm.milestones if m.grp == code]
        if not ms:
            continue
        done = sum(1 for m in ms if m.done)
        nxt = next((m for m in sorted((m for m in ms if not m.done), key=lambda m: (m.due_on is None, m.due_on or date.max, m.position))), None)
        fin = next((m for m in ms if m.final), None)
        out[code] = dict(code=code, ms=ms, total=len(ms), done=done, pct=round(100 * done / len(ms)), next=nxt,
                         complete=bool(fin and fin.done), heading=GROUPS[code][0], line=GROUPS[code][1], colour=GROUPS[code][2])
    return out


def next_dates(rm, today, n=5):
    rows = [m for m in rm.milestones if m.due_on and not m.done and m.due_on >= today]
    rows.sort(key=lambda m: (m.due_on, m.position))
    return rows[:n]


def toggle(m, user):
    """Tick or untick a milestone and keep its calendar event in step."""
    m.done = not m.done
    m.done_on = svc.today() if m.done else None
    m.done_by = user.id if m.done else None
    if m.event_id:
        ev = db.session.get(MsEvent, m.event_id)
        if ev:
            ev.done = m.done
    return m.done
