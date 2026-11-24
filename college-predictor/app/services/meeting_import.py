"""Apply a meeting update to a student's mentorship record in one step.

A mentor (or an admin) pastes a small JSON document that describes what came out of a meeting: the meeting itself, the actions, the
calendar dates and the changes to the student's roadmap (a university put on hold, a new milestone, a step ticked). Nothing is guessed:
only what is in the document is written, every item that already exists is skipped (so pasting it twice changes nothing), and a dry run
shows what would happen before anything is saved.

    {
      "version": 1,
      "session": {"title": "...", "held_at": "2026-11-18T16:01:00Z", "duration_min": 51, "participants": "...", "agenda": "...",
                  "shared_summary": "visible to student and parents", "mentor_notes": "private to mentors and admins",
                  "parent_visible": true},
      "actions": [{"title": "...", "instruction": "...", "purpose": "...", "owner": "student|parent|mentor", "priority": "High|Medium|Low",
                   "due_date": "2026-11-20", "status": "Not Started|Completed", "recurrence": "weekly", "parent_visible": true}],
      "events":  [{"title": "...", "category": "School exam", "starts_on": "2026-11-25", "ends_on": "2026-12-16", "notes": "...",
                   "source": "...", "verified_on": "2026-11-18"}],
      "kpis":    [{"category": "Preparation", "name": "...", "definition": "...", "method": "...", "unit": "questions a day", "direction": "higher|lower|range|milestone|qualitative",
                   "baseline": 0, "target": 8, "frequency": "Weekly", "owner": "Student", "notes": "..."}],
      "kpi_updates": [{"name_contains": "check-ins held", "value": 1, "text": "", "note": "23 Nov call", "observed_on": "2026-11-23"}],
      "roadmap": {"groups": {"HKU": {"status": "On hold", "note": "..."}},
                  "milestones": [{"group": "JEE", "title": "...", "detail": "...", "owner": "student", "due_on": "2026-11-24",
                                  "due_label": "", "calendar": true, "category": "Other", "source": "...", "done": false}],
                  "tick": [{"group": "JEE", "title_contains": "...", "done": true}]}
    }
"""
import json
from datetime import date, datetime, timedelta, timezone

from app.extensions import db
from app.models_mentorship import (ACTION_STATUSES, EVENT_CATEGORIES, KPI_DIRECTIONS, ROADMAP_GROUP_STATUSES, SESSION_STATUSES, MsAction, MsEvent, MsKpi, MsKpiObs,
                                   MsMilestone, MsSession)
from app.services import mentorship as svc
from app.services import roadmap as rmap

PRIORITIES = ('High', 'Medium', 'Low')
KPI_CATEGORIES = ('Preparation', 'Performance', 'Mentorship', 'Readiness')
OWNER_CODES = ('student', 'parent', 'mentor')
MAX_ITEMS = 80
MAX_TEXT = 12000


def _s(v, n=500):
    return (str(v).strip() if v is not None else '')[:n]


def _date(v, where, errs, required=False):
    if v in (None, ''):
        if required:
            errs.append(f'{where}: a date is required (YYYY-MM-DD)')
        return None
    try:
        return date.fromisoformat(str(v).strip()[:10])
    except ValueError:
        errs.append(f'{where}: "{v}" is not a date (use YYYY-MM-DD)')
        return None


def _datetime(v, where, errs):
    """An ISO date-time with a time zone ("2026-11-18T16:01:00Z" or "+04:00"); stored as UTC without a zone, as the portal does."""
    if not v:
        return None
    try:
        dt = datetime.fromisoformat(str(v).strip().replace('Z', '+00:00'))
    except ValueError:
        errs.append(f'{where}: "{v}" is not a date and time (for example 2026-11-18T16:01:00Z)')
        return None
    if dt.tzinfo is not None:
        dt = dt.astimezone(timezone.utc).replace(tzinfo=None)
    return dt


def parse(text):
    """Return (plan, errors). `plan` is only usable when `errors` is empty."""
    errs = []
    try:
        raw = json.loads(text or '')
    except ValueError as ex:
        return None, [f'This is not valid JSON ({ex}). Paste the whole update file, from the first {{ to the last }}.']
    if not isinstance(raw, dict):
        return None, ['The update must be a JSON object ({ ... }).']
    if raw.get('version', 1) != 1:
        errs.append('Unsupported version: this portal reads version 1.')
    plan = dict(session=None, actions=[], events=[], kpis=[], kpi_updates=[], groups={}, milestones=[], ticks=[])

    s = raw.get('session')
    if s:
        if not isinstance(s, dict) or not _s(s.get('title'), 200):
            errs.append('session: a title is required')
        else:
            status = _s(s.get('status'), 24) or 'Completed'
            if status not in SESSION_STATUSES:
                errs.append(f'session: status must be one of {", ".join(SESSION_STATUSES)}')
            plan['session'] = dict(title=_s(s['title'], 200), held_at=_datetime(s.get('held_at'), 'session.held_at', errs), status=status,
                                   duration_min=int(s['duration_min']) if str(s.get('duration_min') or '').isdigit() else None,
                                   participants=_s(s.get('participants'), 300), agenda=_s(s.get('agenda'), MAX_TEXT),
                                   shared_summary=_s(s.get('shared_summary'), MAX_TEXT), mentor_notes=_s(s.get('mentor_notes'), MAX_TEXT),
                                   parent_visible=bool(s.get('parent_visible', True)),
                                   next_review_date=_date(s.get('next_review_date'), 'session.next_review_date', errs))
            if plan['session']['held_at'] is None and status == 'Completed':
                errs.append('session: held_at is required for a completed meeting')

    def items(key):
        v = raw.get(key) or []
        if not isinstance(v, list) or len(v) > MAX_ITEMS:
            errs.append(f'{key}: expected a list of at most {MAX_ITEMS} items')
            return []
        return [x for x in v if isinstance(x, dict)]

    for i, a in enumerate(items('actions'), 1):
        w = f'actions[{i}]'
        if not _s(a.get('title'), 240):
            errs.append(f'{w}: a title is required')
            continue
        pr = _s(a.get('priority'), 10) or 'Medium'
        ow = _s(a.get('owner'), 10) or 'student'
        st = _s(a.get('status'), 16) or 'Not Started'
        if pr not in PRIORITIES or ow not in OWNER_CODES or st not in ('Not Started', 'In Progress', 'Completed'):
            errs.append(f'{w}: priority must be High, Medium or Low; owner student, parent or mentor; status Not Started, In Progress or Completed')
        plan['actions'].append(dict(title=_s(a['title'], 240), instruction=_s(a.get('instruction'), MAX_TEXT), purpose=_s(a.get('purpose'), 300), priority=pr, owner=ow,
                                    due_date=_date(a.get('due_date'), w + '.due_date', errs), status=st,
                                    recurrence='weekly' if _s(a.get('recurrence'), 20) == 'weekly' else '',
                                    est_minutes=int(a['est_minutes']) if str(a.get('est_minutes') or '').isdigit() else None,
                                    parent_visible=bool(a.get('parent_visible', True))))

    for i, x in enumerate(items('events'), 1):
        w = f'events[{i}]'
        if not _s(x.get('title'), 240):
            errs.append(f'{w}: a title is required')
            continue
        cat = _s(x.get('category'), 24) or 'Other'
        if cat not in EVENT_CATEGORIES:
            errs.append(f'{w}: category must be one of {", ".join(EVENT_CATEGORIES)}')
        plan['events'].append(dict(title=_s(x['title'], 240), category=cat, starts_on=_date(x.get('starts_on'), w + '.starts_on', errs, True),
                                   ends_on=_date(x.get('ends_on'), w + '.ends_on', errs), notes=_s(x.get('notes'), 2000), source=_s(x.get('source'), 300) or None,
                                   verified_on=_date(x.get('verified_on'), w + '.verified_on', errs)))

    def num(v, w):
        if v in (None, ''):
            return None
        try:
            return float(v)
        except (TypeError, ValueError):
            errs.append(f'{w}: "{v}" is not a number')
            return None

    for i, k in enumerate(items('kpis'), 1):
        w = f'kpis[{i}]'
        if not _s(k.get('name'), 200):
            errs.append(f'{w}: a name is required')
            continue
        cat, dr = _s(k.get('category'), 24) or 'Preparation', _s(k.get('direction'), 12) or 'higher'
        if cat not in KPI_CATEGORIES or dr not in KPI_DIRECTIONS:
            errs.append(f'{w}: category must be one of {", ".join(KPI_CATEGORIES)} and direction one of {", ".join(KPI_DIRECTIONS)}')
        plan['kpis'].append(dict(name=_s(k['name'], 200), category=cat, direction=dr, definition=_s(k.get('definition'), 2000), method=_s(k.get('method'), 300), unit=_s(k.get('unit'), 30),
                                 baseline=num(k.get('baseline'), w + '.baseline'), target=num(k.get('target'), w + '.target'), target_high=num(k.get('target_high'), w + '.target_high'),
                                 frequency=_s(k.get('frequency'), 30) or 'Weekly', owner=_s(k.get('owner'), 60), notes=_s(k.get('notes'), 2000), outcome=bool(k.get('outcome_metric', False))))
    for i, u in enumerate(items('kpi_updates'), 1):
        w = f'kpi_updates[{i}]'
        if not _s(u.get('name_contains'), 120):
            errs.append(f'{w}: name_contains is required (part of the KPI name)')
            continue
        val, txt = num(u.get('value'), w + '.value'), _s(u.get('text'), 300)
        if val is None and not txt:
            errs.append(f'{w}: give a value or a text')
            continue
        plan['kpi_updates'].append(dict(needle=_s(u['name_contains'], 120).lower(), value=val, text=txt, note=_s(u.get('note'), 300), on=_date(u.get('observed_on'), w + '.observed_on', errs)))

    rm = raw.get('roadmap') or {}
    if rm and not isinstance(rm, dict):
        errs.append('roadmap: expected an object')
        rm = {}
    for code, g in (rm.get('groups') or {}).items():
        g = g if isinstance(g, dict) else {}
        if code not in rmap.GROUPS or _s(g.get('status'), 12) not in ROADMAP_GROUP_STATUSES:
            errs.append(f'roadmap.groups.{code}: section must be one of {", ".join(rmap.GROUPS)} and status one of {", ".join(ROADMAP_GROUP_STATUSES)}')
            continue
        plan['groups'][code] = dict(status=_s(g['status'], 12), note=_s(g.get('note'), 500))
    ms = rm.get('milestones') or []
    for i, m in enumerate(ms if isinstance(ms, list) else [], 1):
        w = f'roadmap.milestones[{i}]'
        if not isinstance(m, dict) or m.get('group') not in rmap.GROUPS or not _s(m.get('title'), 240):
            errs.append(f'{w}: needs a title and a section ({", ".join(rmap.GROUPS)})')
            continue
        ow = _s(m.get('owner'), 12) or 'student'
        if ow not in rmap.OWNERS:
            errs.append(f'{w}: owner must be one of {", ".join(rmap.OWNERS)}')
        cat = _s(m.get('category'), 24) or 'Other'
        if cat not in EVENT_CATEGORIES:
            errs.append(f'{w}: category must be one of {", ".join(EVENT_CATEGORIES)}')
        plan['milestones'].append(dict(grp=m['group'], title=_s(m['title'], 240), detail=_s(m.get('detail'), 2000), owner=ow,
                                       due_on=_date(m.get('due_on'), w + '.due_on', errs), due_label=_s(m.get('due_label'), 60), cat=cat,
                                       calendar=bool(m.get('calendar', True)), source=_s(m.get('source'), 300) or None,
                                       verified_on=_date(m.get('verified_on'), w + '.verified_on', errs), done=bool(m.get('done', False)),
                                       done_on=_date(m.get('done_on'), w + '.done_on', errs)))
    for i, t in enumerate(rm.get('tick') or [], 1):
        if not isinstance(t, dict) or t.get('group') not in rmap.GROUPS or not _s(t.get('title_contains'), 120):
            errs.append(f'roadmap.tick[{i}]: needs a section and title_contains')
            continue
        plan['ticks'].append(dict(grp=t['group'], needle=_s(t['title_contains'], 120).lower(), done=bool(t.get('done', True))))
    if not (plan['session'] or plan['actions'] or plan['events'] or plan['kpis'] or plan['kpi_updates'] or plan['groups'] or plan['milestones'] or plan['ticks']):
        errs.append('The update is empty: it has no meeting, actions, events, KPIs or roadmap changes.')
    return plan, errs


def apply(e, plan, user_id=None, dry=False):
    """Write the plan to the record. Returns (lines, counts). With dry=True nothing is saved. Items that already exist are skipped."""
    lines, n = [], dict(created=0, skipped=0)

    def made(txt):
        n['created'] += 1
        lines.append(('new', txt))

    def skip(txt):
        n['skipped'] += 1
        lines.append(('skip', txt + ' (already there)'))

    sess = None
    s = plan['session']
    if s:
        day = s['held_at'].date() if s['held_at'] else None
        sess = next((x for x in e.sessions.all() if x.title.strip().lower() == s['title'].lower()
                     and ((x.actual_at or x.planned_at) and day and (x.actual_at or x.planned_at).date() == day)), None)
        if sess:
            skip(f'Meeting: {s["title"]}')
        else:
            pos = max([x.position or 0 for x in e.sessions.all()], default=0) + 1
            sess = MsSession(enrolment_id=e.id, kind='follow-up', position=pos, title=s['title'], agenda=s['agenda'] or None, status=s['status'],
                             planned_at=s['held_at'], actual_at=s['held_at'] if s['status'] in ('Completed', 'Partially completed') else None,
                             duration_min=s['duration_min'], participants=s['participants'] or None, shared_summary=s['shared_summary'] or None,
                             mentor_notes=s['mentor_notes'] or None, parent_visible=s['parent_visible'], next_review_date=s['next_review_date'])
            db.session.add(sess)
            db.session.flush()
            made(f'Meeting: {s["title"]}' + (f' ({svc.fmt_dt(s["held_at"], e.timezone)})' if s['held_at'] else ''))

    have = {(a.title or '').strip().lower() for a in e.actions.all()}
    for a in plan['actions']:
        if a['title'].lower() in have:
            skip(f'Action: {a["title"]}')
            continue
        done = a['status'] == 'Completed'
        db.session.add(MsAction(enrolment_id=e.id, session_id=sess.id if sess else None, title=a['title'], instruction=a['instruction'] or None,
                                purpose=a['purpose'] or None, priority=a['priority'], owner=a['owner'], due_date=a['due_date'], status=a['status'],
                                recurrence=a['recurrence'] or None, est_minutes=a['est_minutes'], parent_visible=a['parent_visible'],
                                start_date=svc.today() if not done else None, completed_at=(s['held_at'] if s and s['held_at'] else svc.utcnow()) if done else None))
        have.add(a['title'].lower())
        made(f'Action ({a["owner"]}, {a["priority"]}{", due " + a["due_date"].strftime("%d %b %Y") if a["due_date"] else ""}): {a["title"]}')

    have_ev = {((x.title or '').strip().lower(), x.starts_on) for x in MsEvent.query.filter_by(enrolment_id=e.id).all()}
    for x in plan['events']:
        if (x['title'].lower(), x['starts_on']) in have_ev:
            skip(f'Calendar: {x["title"]}')
            continue
        db.session.add(MsEvent(enrolment_id=e.id, title=x['title'], category=x['category'], starts_on=x['starts_on'], ends_on=x['ends_on'],
                               notes=x['notes'] or None, source=x['source'], verified_on=x['verified_on'], created_by=user_id))
        have_ev.add((x['title'].lower(), x['starts_on']))
        made(f'Calendar: {x["title"]} ({x["starts_on"].strftime("%d %b %Y")})')

    have_k = {(k.name or '').strip().lower() for k in e.kpis_q().all()}
    for k in plan['kpis']:
        if k['name'].lower() in have_k:
            skip(f'KPI: {k["name"]}')
            continue
        kp = MsKpi(enrolment_id=e.id, category=k['category'], name=k['name'], definition=k['definition'] or None, method=k['method'] or None, unit=k['unit'] or None, direction=k['direction'],
                   baseline=k['baseline'], target=k['target'], target_high=k['target_high'], frequency=k['frequency'], owner=k['owner'] or (e.student.name if e.student else ''),
                   notes=k['notes'] or None, outcome_metric=k['outcome'] or svc.OUTCOME_HINT in k['name'].lower())
        kp.current = k['baseline']
        db.session.add(kp)
        db.session.flush()
        if k['baseline'] is not None:
            db.session.add(MsKpiObs(kpi_id=kp.id, value=k['baseline'], note='Baseline', by_user=user_id))
        have_k.add(k['name'].lower())
        made(f'KPI ({k["category"]}): {k["name"]}')
    for u in plan['kpi_updates']:
        hit = next((k for k in e.kpis_q().order_by(MsKpi.id).all() if u['needle'] in (k.name or '').lower() and k.status != 'Archived'), None)
        if hit is None:
            lines.append(('warn', f'No KPI contains "{u["needle"]}": nothing recorded.'))
            continue
        day = u['on'] or (s['held_at'].date() if s and s['held_at'] else svc.today())
        if any(o.observed_on == day and o.value == u['value'] and (o.text or '') == (u['text'] or '') for o in hit.observations.all()):
            skip(f'KPI reading: {hit.name} on {day.strftime("%d %b %Y")}')
            continue
        db.session.add(MsKpiObs(kpi_id=hit.id, value=u['value'], text=u['text'] or None, note=u['note'] or None, by_user=user_id, observed_on=day))
        if u['value'] is not None:
            hit.current = u['value']
        if u['text']:
            hit.qualitative = u['text']
        made(f'KPI reading: {hit.name} = {u["value"] if u["value"] is not None else u["text"]} ({day.strftime("%d %b %Y")})')

    if plan['groups'] or plan['milestones'] or plan['ticks']:
        rm = rmap.get(e)
        if rm is None:
            lines.append(('warn', 'The roadmap changes were not applied: this student has no roadmap yet. Create it on the Roadmap tab, then apply the update again.'))
        else:
            cur = rmap.group_state(rm)
            for code, g in plan['groups'].items():
                if cur.get(code, ('Active', '', None))[:2] == (g['status'], g['note']):
                    skip(f'Roadmap: {rmap.GROUPS[code][0]} is {g["status"]}')
                else:
                    rmap.set_group(rm, code, g['status'], g['note'], on=(s['held_at'].date() if s and s['held_at'] else None), user_id=user_id)
                    made(f'Roadmap: {rmap.GROUPS[code][0]} set to {g["status"]}')
            have_m = {(m.grp, m.title.strip().lower()) for m in rm.milestones}
            for m in plan['milestones']:
                if (m['grp'], m['title'].lower()) in have_m:
                    skip(f'Milestone: {m["title"]}')
                    continue
                rmap.add_milestone(rm, e, m['grp'], m['title'], m['detail'], m['owner'], m['due_on'], m['due_label'], m['calendar'], m['cat'], m['source'],
                                   m['verified_on'], user_id, m['done'], m['done_on'] or (svc.today() if m['done'] else None))
                have_m.add((m['grp'], m['title'].lower()))
                made(f'Milestone ({rmap.GROUPS[m["grp"]][0]}): {m["title"]}' + (' · done' if m['done'] else ''))
            for t in plan['ticks']:
                hit = next((m for m in rm.milestones if m.grp == t['grp'] and t['needle'] in m.title.lower()), None)
                if hit is None:
                    lines.append(('warn', f'No milestone in {t["grp"]} contains "{t["needle"]}": nothing ticked.'))
                elif hit.done == t['done']:
                    skip(f'Milestone: {hit.title}')
                else:
                    rmap.set_done(hit, t['done'], user_id, svc.today())
                    made(f'Milestone {"done" if t["done"] else "reopened"}: {hit.title}')
    if dry:
        db.session.rollback()
    else:
        if n['created']:
            svc.audit(e, 'meeting.imported', f'{n["created"]} new, {n["skipped"]} already there' + (f': {s["title"]}' if s else ''))
        db.session.commit()
    return lines, n
