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
    n = {'meeting': 0, 'kpis': 0, 'kpis_archived': 0, 'actions': 0, 'actions_cancelled': 0, 'actions_noted': 0, 'sessions': 0, 'events': 0, 'session_notes': 0, 'sessions_cancelled': 0, 'plan_tasks': 0, 'profile': 0, 'assessment': 0, 'docs_folder': 0, 'rf_sets': 0}
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

    goals = pack.get('goals')
    if goals and goals not in (e.goals or ''):
        e.goals = ((e.goals.strip() + '\n\n') if e.goals and e.goals.strip() else '') + goals
        n['profile'] += 1
    df = pack.get('docs_folder')
    if df:                                                                     # the student's Google Drive folder of documents (Readiness KPIs tab); set once, never overwritten
        from app.models_mentorship import MsDocFolder
        if not MsDocFolder.query.filter_by(enrolment_id=e.id).first():
            db.session.add(MsDocFolder(enrolment_id=e.id, url=df['url'], note=df.get('note'), shared_with_mentor=bool(df.get('shared')), set_by=user_id))
            n['docs_folder'] += 1
    asm = pack.get('assessment')
    if asm:                                                                    # the JEE self-assessment behind the plan (Study Planner, JEE gap map); saved once
        import json
        from app.models_planner import SpAssessment
        last = SpAssessment.query.filter_by(user_id=e.student_id).order_by(SpAssessment.id.desc()).first()
        if not last or last.ratings != {k: int(v) for k, v in asm['ratings'].items()}:
            db.session.add(SpAssessment(user_id=e.student_id, entered_by=user_id, ratings_json=json.dumps(asm['ratings']), note=asm.get('note')))
            n['assessment'] += 1
    sp = pack.get('study_plan')
    if sp:
        n['plan_tasks'] += _study_plan(e, sp, user_id)
    rfp = pack.get('reinforcement')
    if rfp and (asm or pack.get('assessment') is None):                       # default EduPulse Reinforcement question sets from the student's gap map (needs a saved assessment)
        from app.services import rf_gap
        r = rf_gap.assign_defaults(e.student, e.mentor, limit=rfp.get('limit', 8), gap_days=rfp.get('gap_days', 3))
        n['rf_sets'] += len(r['made'])

    svc.audit(e, 'meeting_update.applied', pack['key'] + ' ' + ', '.join('%s=%s' % kv for kv in n.items() if kv[1]), role='admin')
    db.session.commit()
    return n


def _study_plan(e, sp, user_id):
    """Create the student's Smart Study Planner plan from a pack (once: a plan with the same title is left alone). The student's other active plan is archived. Returns the tasks added."""
    from app.models_planner import SpPlan, SpTask
    if SpPlan.query.filter_by(user_id=e.student_id, title=sp['title']).first():
        return 0
    for old in SpPlan.query.filter_by(user_id=e.student_id, status='active').all():
        old.status = 'archived'
    tasks = sp['tasks']() if callable(sp['tasks']) else sp['tasks']
    plan = SpPlan(user_id=e.student_id, mentor_id=e.mentor_id, created_by=user_id, title=sp['title'], exam=sp['exam'], level=sp['level'], start_date=sp['start'],
                  weeks=max(2, min(26, ((sp['end'] - sp['start']).days // 7) + 1)), exam_date=sp.get('exam_date'), hours_per_day=sp.get('hours') or 3, status='active')
    db.session.add(plan)
    db.session.flush()
    for t in tasks:
        db.session.add(SpTask(plan_id=plan.id, day=t['day'], subject=t.get('subject'), chapter=t.get('chapter'), task_type=t['task_type'], title=t['title'][:200], minutes=t['minutes'],
                              note=(t.get('note') or None), added_by='mentor'))
    return len(tasks)


def summary(n):
    """A one-line description of what apply() changed, for the admin message."""
    names = {'meeting': 'meeting logged', 'kpis': 'KPIs added', 'kpis_archived': 'KPIs archived', 'actions': 'actions added', 'actions_cancelled': 'actions cancelled',
             'actions_noted': 'actions noted', 'sessions': 'sessions planned', 'events': 'calendar dates added', 'session_notes': 'session details updated',
             'sessions_cancelled': 'sessions cancelled', 'plan_tasks': 'study-plan tasks added', 'profile': 'profile goals updated', 'assessment': 'JEE self-assessment saved', 'docs_folder': 'Drive documents folder linked', 'rf_sets': 'EduPulse Reinforcement question sets assigned'}
    parts = ['%d %s' % (v, names[k]) for k, v in n.items() if v]
    return ', '.join(parts) if parts else 'nothing new to add (already applied)'
