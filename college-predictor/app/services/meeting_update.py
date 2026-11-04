"""Apply a meeting update (app/data/meeting_updates) to one student's mentorship enrolment.

A pack can: log the meeting as a completed session, add KPIs, archive KPIs, add actions, cancel actions the meeting dropped, add a note to an action, add planned sessions, add calendar
events, append the meeting decisions to the details of existing sessions (matched by programme and session title) and cancel the planned sessions of an add-on that was dropped.
Nothing existing is deleted; running a pack twice adds nothing twice. No e-mail or alert is sent to anyone.
"""
from app.extensions import db
from app.models_mentorship import ACTION_FINISHED, MsAction, MsEvent, MsKpi, MsSession
from app.services import mentorship as svc


def _first(e):
    return (e.preferred_name or (e.student.name or '').split(' ')[0] or 'the student').strip()


def apply(e, pack, user_id=None):
    """Returns a dict of how many rows changed: meeting, kpis, kpis_archived, actions, actions_cancelled, actions_noted, sessions, events, session_notes, sessions_cancelled."""
    n = {'meeting': 0, 'kpis': 0, 'kpis_archived': 0, 'actions': 0, 'actions_cancelled': 0, 'actions_noted': 0, 'sessions': 0, 'events': 0, 'session_notes': 0, 'sessions_cancelled': 0}
    now = svc.utcnow()
    tag = pack.get('note_tag', 'Update 2 Nov 2026: ')

    m = pack.get('meeting')
    if m and not e.sessions.filter(MsSession.title == m['title']).first():
        db.session.add(MsSession(enrolment_id=e.id, kind='follow-up', position=svc.next_position(e), title=m['title'], agenda=m.get('agenda'), status='Completed', planned_at=m['at'],
                                 actual_at=m['at'], duration_min=m.get('duration_min'), participants=m.get('participants'), shared_summary=m.get('summary'),
                                 mentor_notes=m.get('notes'), parent_visible=True))
        n['meeting'] += 1

    for cat, name, definition, method, unit, direction, baseline, target, current, freq, owner, outcome, notes in pack.get('kpis', []):
        if MsKpi.query.filter_by(enrolment_id=e.id, name=name).first():
            continue
        db.session.add(MsKpi(enrolment_id=e.id, category=cat, name=name, definition=definition, method=method, unit=unit, direction=direction, baseline=baseline, target=target,
                             current=current, frequency=freq, owner=owner, notes=notes, outcome_metric=outcome))
        n['kpis'] += 1
    for needle, reason in pack.get('kpis_archive', []):
        for k in MsKpi.query.filter(MsKpi.enrolment_id == e.id, MsKpi.status != 'Archived', MsKpi.name.ilike('%' + needle + '%')).all():
            k.status = 'Archived'
            k.notes = ((k.notes + '\n') if k.notes else '') + reason
            n['kpis_archived'] += 1

    for title, instruction, owner, due, priority, recurrence in pack.get('actions', []):
        if not MsAction.query.filter_by(enrolment_id=e.id, title=title).first():
            db.session.add(MsAction(enrolment_id=e.id, title=title, instruction=instruction, owner=owner, due_date=due, priority=priority, recurrence=recurrence or None,
                                    purpose='Meeting of 2 Nov 2026', parent_visible=True))
            n['actions'] += 1
    for needle, reason in pack.get('actions_cancel', []):
        for a in MsAction.query.filter(MsAction.enrolment_id == e.id, MsAction.title.ilike('%' + needle + '%')).all():
            if a.status not in ACTION_FINISHED and a.status != 'Cancelled':
                a.status = 'Cancelled'
                a.mentor_feedback = ((a.mentor_feedback + '\n') if a.mentor_feedback else '') + reason
                n['actions_cancelled'] += 1
    for needle, note in pack.get('actions_note', []):
        for a in MsAction.query.filter(MsAction.enrolment_id == e.id, MsAction.title.ilike('%' + needle + '%')).all():
            if note not in (a.mentor_feedback or ''):
                a.mentor_feedback = ((a.mentor_feedback + '\n') if a.mentor_feedback else '') + note
                n['actions_noted'] += 1

    for title, agenda, deliverable, minutes, kind in pack.get('sessions', []):
        if not e.sessions.filter(MsSession.title == title).first():
            db.session.add(MsSession(enrolment_id=e.id, kind=kind, position=svc.next_position(e), title=title, agenda=agenda, deliverable=deliverable, duration_min=minutes,
                                     status='Planned', parent_visible=True))
            db.session.flush()
            n['sessions'] += 1

    for title, category, start, end, notes, source in pack.get('events', []):
        if not MsEvent.query.filter_by(enrolment_id=e.id, title=title).first():
            db.session.add(MsEvent(enrolment_id=e.id, title=title, category=category, starts_on=start, ends_on=end, notes=notes, source=source, created_by=user_id))
            n['events'] += 1

    prog = (e.programme.name or '').lower()
    for prog_needle, title_needle, text in pack.get('session_notes', []):
        if prog_needle.lower() not in prog:
            continue
        for s in e.sessions.filter(MsSession.title.ilike('%' + title_needle + '%')).all():
            if s.status in ('Cancelled',) or (tag + text) in (s.agenda or ''):
                continue
            s.agenda = ((s.agenda + '\n\n') if s.agenda else '') + tag + text
            n['session_notes'] += 1
    for prog_needle, reason in pack.get('cancel_programmes', []):
        if prog_needle.lower() in prog:
            for s in e.sessions.filter(MsSession.status.in_(['Planned', 'Rescheduled'])).all():
                s.status = 'Cancelled'
                s.mentor_notes = ((s.mentor_notes + '\n') if s.mentor_notes else '') + reason
                n['sessions_cancelled'] += 1

    svc.audit(e, 'meeting_update.applied', pack['key'] + ' ' + ', '.join('%s=%s' % kv for kv in n.items() if kv[1]), role='admin')
    db.session.commit()
    return n


def summary(n):
    """A one-line description of what apply() changed, for the admin message."""
    names = {'meeting': 'meeting logged', 'kpis': 'KPIs added', 'kpis_archived': 'KPIs archived', 'actions': 'actions added', 'actions_cancelled': 'actions cancelled',
             'actions_noted': 'actions noted', 'sessions': 'sessions planned', 'events': 'calendar dates added', 'session_notes': 'session details updated',
             'sessions_cancelled': 'sessions cancelled'}
    parts = ['%d %s' % (v, names[k]) for k, v in n.items() if v]
    return ', '.join(parts) if parts else 'nothing new to add (already applied)'
