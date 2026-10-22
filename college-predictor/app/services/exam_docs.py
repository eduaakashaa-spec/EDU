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


def items_for(exam):
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
