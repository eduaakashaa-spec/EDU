"""Registration document checklists for followed exams (member portal, Calendar tab).

Every exam gets the common list; some exams add their own items, matched on the exam name. Keys are stored in
`MsDocCheck`, so never rename a key once students have ticked it — add a new one instead. Items marked
required=False are "if applicable": they are shown and can be ticked, but confirmation does not wait for them.
The lists are a preparation aid, not the official requirement: the information bulletin of each exam decides.
"""
import re

from app.extensions import db
from app.models_mentorship import MsDocCheck, MsDocConfirm

# (key, label, hint, required)
COMMON = [
    ('photo', 'Recent passport-size photograph (scanned)', 'Light background, face clearly visible; size and format as the bulletin specifies.', True),
    ('signature', 'Scanned signature', 'Signed in black ink on white paper; scan to the size the bulletin specifies.', True),
    ('class10', 'Class 10 certificate / marksheet', 'Your date-of-birth proof — the name must match every other document exactly.', True),
    ('class12', 'Class 12 marksheet, or school details if appearing', 'Board, roll number and year of passing ready to enter.', True),
    ('id_proof', 'Photo ID (Aadhaar, passport or another ID the exam accepts)', 'Name and date of birth must match your Class 10 record.', True),
    ('contact', 'Your own email address and mobile number', 'All OTPs and admit-card notices go here; use contacts you will keep through admissions.', True),
    ('payment', 'Payment method for the application fee', 'Net banking, UPI or card — save the payment receipt.', True),
    ('category', 'Category certificate — SC / ST / OBC-NCL / EWS (if applicable)', 'Must be current and in the format the exam asks for.', False),
    ('pwd', 'Disability (PwD) certificate (if applicable)', 'Issued by a competent authority.', False),
    ('nri', 'Passport and OCI / PIO card or visa (NRI / foreign candidates)', 'Needed for overseas test centres and NRI-quota eligibility.', False),
]

STATE_DOMICILE = ('domicile', 'Domicile / nativity or residence certificate', 'State-quota seats need proof that you meet the state rules.', True)

# (name fragments, extra items) — the first matching rule wins
EXTRAS = [
    (('jee advanced',), [('jee_main', 'JEE Main application number and scorecard', 'You register for JEE Advanced only after qualifying in JEE Main.', True)]),
    (('jee main',), [('aadhaar_mobile', 'Aadhaar details updated with your current mobile (Indian residents)', 'NTA verifies identity through Aadhaar where available.', False)]),
    (('ceed',), [('degree', 'Degree certificate, or proof you are in the final year', 'CEED needs a qualifying degree or final-year status.', True)]),
    (('cuet',), [('subjects', 'List of test subjects and the universities you will apply to', 'Subject choices cannot be changed after the correction window.', True)]),
    (('kcet', 'mht cet', 'wbjee', 'keam', 'eapcet', 'tnea', 'gujcet', 'ojee'), [STATE_DOMICILE]),
]


# University applications abroad have their own checklist (from the NUS / NTU / HKU admission report, 30 Oct 2026); it replaces the Indian-exam list for an exam named after the university.
UNIVERSITY = {
    'nus': [
        ('nus_passport', 'Passport valid and scanned', 'Name and dates must match the marksheets.', True),
        ('nus_marksheets', 'Class 10 and 11 marksheets scanned', 'Keep CBSE admit card details with them.', True),
        ('nus_prereq', 'Prerequisites confirmed: Maths; Physics or Chemistry for Computer Engineering', 'Check the NUS prerequisites PDF for the chosen programme (the copy read was dated April 2024).', True),
        ('nus_grant', 'Tuition Grant and 3-year work bond decision made', 'About S$18,300 a year saved with the grant; the grant carries a 3-year Singapore work bond.', True),
        ('nus_submitted', 'Application submitted (window 16 Dec to 17 Feb)', 'Target: submit by 31 January, before the CBSE exams.', True),
        ('nus_scholarship', 'Scholarship applications made', 'NUS International Undergraduate Scholarship and others open to Indians (reported).', False),
        ('nus_results', 'Final CBSE results updated in the portal within 3 days of release', 'The 3-day clock starts at release.', True),
        ('nus_outcome', 'Outcome read and answered (by July)', 'Read the terms and answer inside the window.', True),
        ('nus_visa', 'Student pass, housing and budget planned', 'Living costs, housing, visa and flights are extra.', True),
    ],
    'ntu': [
        ('ntu_passport', 'Passport valid and scanned', 'Name and dates must match the marksheets.', True),
        ('ntu_marksheets', 'Marksheets scanned; 93% average worked out including English', '93% across all Standard 12 subjects including English is the stated minimum.', True),
        ('ntu_subjects', 'Programme minimum-subject PDF checked', 'Subject rules are programme by programme; Physics matters.', True),
        ('ntu_window', 'Exact window confirmed on the India Standard 12 page', 'The close varies by qualification (15 Oct 2026 to 19 Mar 2027).', True),
        ('ntu_sitting', 'One uninterrupted sitting booked for the form', 'No save and return; the wrong form can void the application.', True),
        ('ntu_submitted', 'Form submitted and fee paid (about S$25, reported)', 'Target: submit by 31 January.', True),
        ('ntu_scholarship', 'Scholarship applied for on the tracking page', 'All scholarships are applied for through the application tracking page.', False),
        ('ntu_results', 'Result slip uploaded within 3 days of release', 'Otherwise the application is incomplete and not processed.', True),
        ('ntu_visa', 'Student pass, housing and budget planned', 'Offers from March on actual results only.', True),
    ],
    'hku': [
        ('hku_passport', 'Passport valid and scanned', 'Name and dates must match the marksheets.', True),
        ('hku_date', '2027 first-round date confirmed with HKU in writing', "The HKU India page still showed last cycle's dates on 30 Oct 2026; the 25 Nov cut-off is reported.", True),
        ('hku_results', 'Predicted and Class 11 results ready to key in', 'Results are keyed into the application system, not just uploaded.', True),
        ('hku_statement', 'Personal statement and referee ready; nominee chosen', 'A teacher or counsellor can be nominated to enter results and upload documents.', True),
        ('hku_fee', 'HK$780 (about US$100) fee ready', 'Non-refundable.', True),
        ('hku_submitted', 'Submitted for the first round (noon Hong Kong time, 25 Nov)', 'Target 22 Nov; the cut-off runs on Hong Kong time.', True),
        ('hku_interview', 'Interview prepared if invited', 'Interviews ran Nov to Jan last cycle.', False),
        ('hku_offer', 'Offer accepted within 3 to 4 weeks; deposit paid', 'The deposit is non-refundable.', True),
        ('hku_visa', 'Student visa started (8 to 10 weeks)', 'Allow 4 to 6 weeks for assessment per last published guidance.', True),
    ],
}


def university_key(exam):
    name = (exam.name or '').lower()
    return next((k for k in UNIVERSITY if re.search('(?<![a-z])' + k + '(?![a-z])', name)), None)


def items_for(exam):
    uni = university_key(exam)
    if uni:
        return list(UNIVERSITY[uni])
    name = (exam.name or '').lower()
    # word-start match, so 'ceed' does not catch 'UCEED' but 'eapcet' still catches 'TG-EAPCET'
    extra = next((items for keys, items in EXTRAS if any(re.search(r'\b' + re.escape(k), name) for k in keys)), [])
    return COMMON[:-1] + extra + COMMON[-1:]          # keep the NRI line last


def checklist(e, exam):
    """Items with their ticked state plus progress and confirmation for one student record and exam."""
    ticked = {c.item_key for c in MsDocCheck.query.filter_by(enrolment_id=e.id, exam_id=exam.id).all()}
    conf = MsDocConfirm.query.filter_by(enrolment_id=e.id, exam_id=exam.id).first()
    items = [{'key': k, 'label': lbl, 'hint': hint, 'required': req, 'ticked': k in ticked} for k, lbl, hint, req in items_for(exam)]
    req = [i for i in items if i['required']]
    done = sum(1 for i in req if i['ticked'])
    return {'items': items, 'done': done, 'total': len(req), 'ready': done == len(req), 'confirmed': conf}


def save(e, exam, keys, user_id, confirm=False):
    """Replace the ticked set with `keys`. Returns 'confirmed', 'incomplete' (confirm asked but not ready), or 'saved'.
    Unticking a required item withdraws an earlier confirmation."""
    valid = {k for k, *_ in items_for(exam)}
    want = set(keys) & valid
    rows = {c.item_key: c for c in MsDocCheck.query.filter_by(enrolment_id=e.id, exam_id=exam.id).all()}
    for k, row in rows.items():
        if k not in want:
            db.session.delete(row)
    for k in want - rows.keys():
        db.session.add(MsDocCheck(enrolment_id=e.id, exam_id=exam.id, item_key=k, ticked_by=user_id))
    ready = all(k in want for k, _l, _h, req in items_for(exam) if req)
    conf = MsDocConfirm.query.filter_by(enrolment_id=e.id, exam_id=exam.id).first()
    if conf and not ready:
        db.session.delete(conf)
    if confirm:
        if not ready:
            return 'incomplete'
        if not conf:
            db.session.add(MsDocConfirm(enrolment_id=e.id, exam_id=exam.id, confirmed_by=user_id))
        return 'confirmed'
    return 'saved'
