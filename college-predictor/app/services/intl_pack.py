"""Add the NUS, NTU and HKU admission pack (2027 intake) to one student's mentorship record.

What it creates (nothing existing is changed or removed; running it twice adds nothing twice):
  * the three admission windows in the exam catalogue, followed by this student, so they appear on the Calendar tab with their document checklists;
  * dated calendar events for the targets and hard stops;
  * KPIs on the KPI tab;
  * actions for the student, the parents and the mentor, with due dates;
  * a college list (Preferences tab) with the application dates for each university.
The content lives in app/data/intl_admissions_2027.py with the OFFICIAL / REPORTED tag of every date. No alert e-mail is sent to other members.
"""
from app.extensions import db
from app.data import intl_admissions_2027 as P
from app.models_mentorship import (MsAction, MsEvent, MsExam, MsExamFocus, MsKpi, MsPrefDates, MsPrefEntry, MsPrefList)
from app.services import exam_docs
from app.services import mentorship as svc


def _exam(spec, user_id):
    x = MsExam.query.filter_by(name=spec['name']).first()
    made = x is None
    if made:
        x = MsExam(name=spec['name'], category=spec['category'], stream=spec['stream'], starts_on=spec['starts_on'], ends_on=spec['ends_on'], status=spec['status'],
                   window_note=spec['window_note'], source=spec['source'], verified_on=spec['verified_on'], notes=spec['notes'], active=True)
        db.session.add(x)
        db.session.flush()
    return x, made


def apply(e, user_id=None):
    """Returns a dict of how many rows were added: exams, followed, events, kpis, actions, entries.
    The pack text was written for Darsh; the student's own first name is put in its place."""
    first = (e.preferred_name or (e.student.name or '').split(' ')[0] or 'the student').strip()
    T = lambda x: x.replace('Darsh', first) if isinstance(x, str) else x
    n = {'exams': 0, 'followed': 0, 'events': 0, 'kpis': 0, 'actions': 0, 'entries': 0}
    exams = {}
    for spec in P.EXAMS:
        x, made = _exam(spec, user_id)
        exams[spec['key']] = x
        n['exams'] += made
        if not MsExamFocus.query.filter_by(enrolment_id=e.id, exam_id=x.id).first():
            db.session.add(MsExamFocus(enrolment_id=e.id, exam_id=x.id, created_by=user_id))
            n['followed'] += 1

    for title, category, start, end, notes, source, verified in P.EVENTS:
        title, notes = T(title), T(notes)
        if not MsEvent.query.filter_by(enrolment_id=e.id, title=title).first():
            db.session.add(MsEvent(enrolment_id=e.id, title=title, category=category, starts_on=start, ends_on=end, notes=notes, source=source, verified_on=verified, created_by=user_id))
            n['events'] += 1

    required = sum(1 for x in exams.values() for it in exam_docs.items_for(x) if it[3])
    for cat, name, definition, method, unit, direction, baseline, target, current, freq, owner, outcome, notes in P.KPIS:
        name, definition, notes = T(name), T(definition), T(notes)
        if MsKpi.query.filter_by(enrolment_id=e.id, name=name).first():
            continue
        db.session.add(MsKpi(enrolment_id=e.id, category=cat, name=name, definition=definition, method=method, unit=unit, direction=direction, baseline=baseline,
                             target=required if unit == 'items' else target, current=current, frequency=freq, owner=owner, notes=notes, outcome_metric=outcome))
        n['kpis'] += 1

    for title, instruction, owner, due, priority in P.ACTIONS:
        if not MsAction.query.filter_by(enrolment_id=e.id, title=title).first():
            db.session.add(MsAction(enrolment_id=e.id, title=title, instruction=instruction, owner=owner, due_date=due, priority=priority, purpose='NUS, NTU and HKU 2027 intake',
                                    parent_visible=True))
            n['actions'] += 1

    plist = MsPrefList.query.filter_by(enrolment_id=e.id, name=P.LIST_NAME).first()
    if plist is None:
        plist = MsPrefList(enrolment_id=e.id, name=P.LIST_NAME, status='Research pending', notes=P.LIST_NOTES)
        db.session.add(plist)
        db.session.flush()
    have = {x.college for x in plist.entries.all()}
    for pos, c in enumerate(P.LIST, 1):
        if c['college'] in have:
            continue
        ent = MsPrefEntry(list_id=plist.id, position=pos, college=c['college'], branch=c['branch'], route=c['route'], location=c['location'], data_year=c['data_year'],
                          data_source=c['data_source'], data_note=c['data_note'], fee_note=c['fee_note'], eligibility='Not checked')
        db.session.add(ent)
        db.session.flush()
        db.session.add(MsPrefDates(entry_id=ent.id, exam_id=exams[c['key']].id, exam_label=exams[c['key']].name, app_open=c['open'], app_deadline=c['deadline'], source=c['source']))
        n['entries'] += 1

    svc.audit(e, 'intl_pack.applied', P.PACK_KEY + ' ' + ', '.join('%s=%s' % kv for kv in n.items()), role='admin')
    db.session.commit()
    return n
