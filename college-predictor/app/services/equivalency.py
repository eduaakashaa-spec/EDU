"""Entrance-exam qualification and subject equivalency: the checker behind /entrance-equivalency.

The rules live in app/data/equivalency.py (each one with its official source). This module only judges a profile against them:
  verdict(exam, qual, subjects)  ->  {'status': 'yes'|'equiv'|'check'|'subjects'|'no', 'missing': [...], 'note': str}
Status meaning: yes = the qualification is accepted; equiv = accepted once an equivalence certificate is obtained; check = depends on the institute or
needs the exam notice read; subjects = the qualification is accepted but a required subject is missing; no = not accepted.
"""
from app.data import equivalency as D

STATUS_ORDER = {'yes': 0, 'equiv': 1, 'check': 2, 'subjects': 3, 'no': 4}
STATUS_LABEL = {'yes': 'Accepted', 'equiv': 'Accepted with equivalence certificate', 'check': 'Check the notice', 'subjects': 'Subject requirement not met', 'no': 'Not accepted'}


def exams():
    return D.EXAMS


def exam(exam_id):
    return next((e for e in D.EXAMS if e['id'] == exam_id), None)


def verdict(e, qual, subjects):
    """Judge one exam for a qualification key and a set of subject names the student studied."""
    have = {s for s in subjects if s in D.SUBJECTS}
    q = e['quals'].get(qual)
    if q is None:
        return {'status': 'check', 'missing': [], 'note': 'This exam notice does not name this qualification. Ask the exam body in writing before you apply.'}
    status, note = q[0], q[1]
    needs = q[2] if len(q) > 2 and q[2] is not None else e.get('needs', [])
    missing = [n['label'] for n in needs if not (have & set(n['any']))]
    if status == 'no':
        return {'status': 'no', 'missing': [], 'note': note}
    if missing:
        return {'status': 'subjects', 'missing': missing, 'note': note}
    return {'status': status, 'missing': [], 'note': note}


def check(qual, subjects, group=None):
    """Verdicts for every exam (or one group), best first."""
    rows = []
    for e in D.EXAMS:
        if e.get('level') != 'ug' or (group and e['group'] != group):
            continue
        v = verdict(e, qual, subjects)
        rows.append({'exam': e, **v, 'label': STATUS_LABEL[v['status']]})
    rows.sort(key=lambda r: (STATUS_ORDER[r['status']], r['exam']['name']))
    return rows


def context():
    return dict(exams=D.EXAMS, quals=D.QUALS, subjects=D.SUBJECTS, groups=D.GROUPS, cycle_note=D.CYCLE_NOTE, frameworks=D.FRAMEWORKS, checked=D.CHECKED, status_label=STATUS_LABEL)
