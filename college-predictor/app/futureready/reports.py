"""Reports A-F. A report is a frozen JSON snapshot (what a mentor reviewed is exactly what the family sees) rendered as HTML or PDF.

Every report states its evidence basis (self-report / parent observation / assessment / mentor judgement), carries the limits of the data,
and never contains private mentor notes, ranks, cut-offs or admission predictions."""
import json
from datetime import date, datetime
from io import BytesIO

from app.extensions import db
from app.futureready import engine
from app.futureready.models import (FrAction, FrAdmission, FrAssessment, FrAttempt, FrBadge, FrGoal, FrNote, FrProject, FrReport, FrSession,
                                    FrShortlist, FrSkillScore, _now, jl)

KINDS = {
    'starting_point': 'Starting-Point Report', 'skill_gap': 'Skill-Gap Report', 'engineering': 'Engineering Pathway Report',
    'monthly': 'Monthly Progress Report', 'quarterly': 'Quarterly Review Report', 'growth': 'Growth Report',
}
LIMITS = ['This report describes where your child is today. It is not a prediction of marks, rank, branch or admission.',
          'Self-report answers show how a student sees themselves; they are shown separately from tested results.',
          'Small sets of questions give a snapshot, not a measure of ability. Results change with practice, mood and time of day.',
          'Admission rules and dates change every year; always confirm on the official website.']


def alignment(profile):
    """Compare the student's and parent's answers to Assessment 10: shared interests, differing confidence, topics to talk about."""
    st = engine.latest_attempt(profile.id, 'alignment', 'student')
    pa = engine.latest_attempt(profile.id, 'alignment', 'parent')
    if not (st and pa):
        return None
    s, p = st.responses, pa.responses
    gaps, shared = [], []
    for code, name in (('PS-01', 'enjoys most'), ('PS-02', 'is best at')):
        a, b = set(s.get(code, [])), set(p.get(code, []))
        if a and b:
            common = a & b
            if common:
                shared.append(f'Both chose {len(common)} of 3 for “{name}”')
            if len(common) <= 1:
                gaps.append(f'what the student {name}: choices barely overlap')
    labels = {'PS-03': 'confidence about subject choices', 'PS-04': 'ease of talking about the future', 'PS-05': 'support for studying', 'PS-06': 'understanding of admissions'}
    for c, lb in labels.items():
        if c in s and c in p and abs(int(s[c]) - int(p[c])) >= 2:
            gaps.append(f'{lb} (student {s[c]}/5, parent {p[c]}/5)')
    return dict(gaps=gaps, shared=shared, student_text={k: v for k, v in s.items() if k.startswith('PS-T')}, parent_text={k: v for k, v in p.items() if k.startswith('PS-T')})


def _assessment_status(profile):
    rows = []
    for a in FrAssessment.query.filter(FrAssessment.group.in_(['core', 'engineering', 'entrance']), FrAssessment.active == True).order_by(FrAssessment.position).all():  # noqa: E712
        at = engine.latest_attempt(profile.id, a.key)
        rows.append(dict(number=a.number, title=a.title, done=bool(at), when=at.submitted_at.strftime('%d %b %Y') if at and at.submitted_at else '', key=a.key))
    return rows


def _skill_rows(profile, kinds=('objective',)):
    from app.futureready.reco import latest_skills
    out = []
    for (akey, sk), v in latest_skills(profile.id).items():
        if v.kind in kinds:
            if v.kind == 'objective':
                out.append(dict(assessment=akey, skill=sk, label=engine.label(sk), kind=v.kind, value=v.value, n=v.n, band=engine.band(v.value, v.n)))
            else:
                out.append(dict(assessment=akey, skill=sk, label=engine.label(sk), kind=v.kind, value=v.value, n=v.n,
                                band='Strong tendency' if v.value >= 4 else 'Mixed' if v.value >= 3 else 'Less like me'))
    return sorted(out, key=lambda r: (r['kind'], r['value']))


def _mentor_summary(profile):
    return [dict(body=n.body, when=n.created_at.strftime('%d %b %Y'), basis=n.basis) for n in
            FrNote.query.filter_by(profile_id=profile.id, visibility='shared').order_by(FrNote.id.desc()).limit(5).all()]


def _actions_summary(profile, since=None):
    q = FrAction.query.filter_by(profile_id=profile.id)
    items = q.all()
    if since:
        items = [a for a in items if (a.created_at and a.created_at >= since) or (a.completed_at and a.completed_at >= since)]
    done = [a for a in items if a.status == 'Done']
    return dict(total=len(items), done=len(done), titles_done=[a.title for a in done][:8], open=[dict(title=a.title, owner=a.owner, due=a.due_date.strftime('%d %b') if a.due_date else '')
                                                                  for a in items if a.status in ('Not started', 'In progress')][:8])


def build(profile, kind, reviewer=None):
    """Return the frozen report data for `kind`."""
    d = dict(kind=kind, title=KINDS[kind], student=profile.student.name or profile.student.email, grade=profile.grade, school=profile.school or '',
             generated=_now().strftime('%d %b %Y'), limits=LIMITS, demo=bool(profile.demo), mentor=profile.mentor.name if profile.mentor else '')
    obj = _skill_rows(profile)
    selfr = _skill_rows(profile, ('self',))
    interests = engine.interest_profile(profile.id)
    d['assessments'] = _assessment_status(profile)
    d['objective'] = obj
    d['self'] = [r for r in selfr if r['assessment'] in ('habits', 'per', 'communication', 'selfmgmt', 'reflection')]
    d['interests'] = [dict(label=engine.label(k), value=v) for k, v in list(interests.items())[:6]]
    if kind == 'starting_point':
        d['strengths'] = [r['label'] for r in obj if r['band'] == 'Secure'][:5]
        d['focus'] = [r['label'] for r in obj if r['band'] in ('Needs reinforcement', 'Developing')][:5]
        d['habit_strengths'] = [r['label'] for r in d['self'] if r['assessment'] == 'habits' and r['value'] >= 4][:4]
        d['habit_focus'] = [r['label'] for r in d['self'] if r['assessment'] == 'habits' and r['value'] < 3][:4]
        d['alignment'] = alignment(profile)
        d['branches'] = [dict(name=m['branch'].name, why=m['why']) for m in engine.branch_matches(profile.id, 5)]
        d['goals'] = [dict(title=g.title, due=g.due_date.strftime('%d %b %Y') if g.due_date else '') for g in FrGoal.query.filter_by(profile_id=profile.id, status='Active').all()]
        d['next'] = ['Agree 2–3 goals for the next 30 days with your mentor.', 'Start with one recommended practice task this week.', 'Plan the first monthly session.']
    elif kind == 'skill_gap':
        d['gaps'] = [r for r in obj if r['band'] in ('Needs reinforcement', 'Developing')]
        d['secure'] = [r for r in obj if r['band'] == 'Secure']
        d['too_few'] = [r for r in obj if r['band'] == 'Too few items']
        from app.futureready.reco import _resources_for
        d['plan'] = [dict(skill=g['label'], tasks=[r.title for r in _resources_for(g['skill'])[:2]]) for g in d['gaps'][:6]]
    elif kind == 'engineering':
        d['branches'] = [dict(name=m['branch'].name, why=m['why'], pct=m['pct']) for m in engine.branch_matches(profile.id, 6)]
        d['shortlist'] = [dict(name=s.branch.name, note=s.note or '') for s in FrShortlist.query.filter_by(profile_id=profile.id).all()]
        a12 = engine.latest_attempt(profile.id, 'entrance_check')
        d['awareness'] = a12.result.get('overall_pct') if a12 else None
        d['admissions'] = [dict(name=a.name, classification=a.classification, verified=a.status == 'verified', last=a.last_verified.strftime('%d %b %Y') if a.last_verified else '') for a in
                           FrAdmission.query.filter_by(active=True).order_by(FrAdmission.position).all()]
        d['skills_needed'] = 'Strong basics in mathematics and science, clear reasoning, and curiosity. Explore with projects before choosing.'
    else:
        since = None
        if kind == 'monthly':
            t = _now()
            since = datetime(t.year, t.month, 1)
            d['period'] = t.strftime('%B %Y')
        elif kind == 'quarterly':
            t = _now()
            q0 = ((t.month - 1) // 3) * 3 + 1
            since = datetime(t.year, q0, 1)
            d['period'] = f'Q{(t.month - 1) // 3 + 1} {t.year}'
        d['actions'] = _actions_summary(profile, since)
        d['sessions'] = [dict(title=s.title or s.kind.title(), when=(s.held_at or s.planned_at).strftime('%d %b') if (s.held_at or s.planned_at) else '', status=s.status, summary=s.summary or '')
                         for s in FrSession.query.filter_by(profile_id=profile.id).order_by(FrSession.id.desc()).limit(6).all()]
        d['goals'] = [dict(title=g.title, status=g.status, baseline=g.baseline, current=g.current, target=g.target, unit=g.unit or '') for g in FrGoal.query.filter_by(profile_id=profile.id).all()]
        d['projects'] = [dict(title=p.title, status=p.status) for p in FrProject.query.filter_by(profile_id=profile.id).all()]
        d['badges'] = [b.key for b in FrBadge.query.filter_by(profile_id=profile.id).all()]
        d['mentor_notes'] = _mentor_summary(profile)
        if kind in ('quarterly', 'growth'):
            d['growth'] = growth(profile)
    return d


def growth(profile):
    """First vs latest value per skill from the student's own history. A change from fewer than MIN_ITEMS items, or a single attempt, is labelled."""
    rows = (FrSkillScore.query.filter_by(profile_id=profile.id).order_by(FrSkillScore.id).all())
    by = {}
    for r in rows:
        by.setdefault((r.assessment_key, r.skill, r.kind), []).append(r)
    out = []
    for (akey, sk, kind), lst in by.items():
        if len(lst) < 2:
            continue
        a, b = lst[0], lst[-1]
        delta = round(b.value - a.value, 1)
        unit = '%' if kind in ('objective', 'rubric') else ' pts'
        out.append(dict(label=engine.label(sk), assessment=akey, kind=kind, first=a.value, last=b.value, delta=delta, unit=unit, n=len(lst), small=min(a.n or 0, b.n or 0) < engine.MIN_ITEMS,
                        trend=[x.value for x in lst]))
    return sorted(out, key=lambda r: -abs(r['delta']))


def save(profile, kind, user):
    d = build(profile, kind)
    r = FrReport(profile_id=profile.id, kind=kind, title=d['title'], period=d.get('period', ''), data_json=json.dumps(d), created_by=user.id)
    db.session.add(r)
    db.session.commit()
    return r


# ---- PDF ------------------------------------------------------------------------------------------------------------------------
NAVY, ORANGE, CREAM = '#0E3A8A', '#FF6B0A', '#FBF7EE'


def pdf(report):
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.lib.units import mm
    from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

    d = report.data
    ss = getSampleStyleSheet()
    H = ParagraphStyle('h', parent=ss['Heading1'], textColor=colors.HexColor(NAVY), fontSize=20, spaceAfter=4)
    H2 = ParagraphStyle('h2', parent=ss['Heading2'], textColor=colors.HexColor(NAVY), fontSize=13, spaceBefore=10, spaceAfter=4)
    P = ParagraphStyle('p', parent=ss['BodyText'], fontSize=9.5, leading=13, textColor=colors.HexColor('#0E1B3D'))
    SM = ParagraphStyle('sm', parent=P, fontSize=8, textColor=colors.HexColor('#5A6278'))

    def esc(t):
        return (str(t) if t is not None else '').replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

    el = [Paragraph('EduAakashaa FutureReady', SM), Paragraph(esc(d['title']), H),
          Paragraph(f"{esc(d['student'])} · Grade {d['grade']} {('· ' + esc(d['school'])) if d.get('school') else ''} · {esc(d.get('period') or d['generated'])}", P)]
    if d.get('demo'):
        el.append(Paragraph('<b>DEMONSTRATION DATA: sample student, not a real child.</b>', P))
    el.append(Spacer(1, 6))

    def table(rows, widths, head):
        t = Table([head] + rows, colWidths=widths, repeatRows=1)
        t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(NAVY)), ('TEXTCOLOR', (0, 0), (-1, 0), colors.white), ('FONTSIZE', (0, 0), (-1, -1), 8.5),
                               ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F5EFDF')]), ('GRID', (0, 0), (-1, -1), 0.25, colors.HexColor('#E8DFC8')),
                               ('VALIGN', (0, 0), (-1, -1), 'TOP')]))
        return t

    def bullets(title, items):
        if items:
            el.append(Paragraph(title, H2))
            for i in items:
                el.append(Paragraph('• ' + esc(i), P))

    if d.get('objective'):
        el.append(Paragraph('Tested skills (snapshot)', H2))
        el.append(table([[esc(r['label']), f"{int(r['value'])}% of {r['n']}", esc(r['band'])] for r in d['objective']], [80 * mm, 40 * mm, 50 * mm], ['Skill', 'Result', 'Band']))
    if d.get('self'):
        el.append(Paragraph('How the student sees themselves (self-report)', H2))
        el.append(table([[esc(r['label']), f"{r['value']:.1f} / 5", esc(r['band'])] for r in d['self']], [80 * mm, 40 * mm, 50 * mm], ['Area', 'Average', 'Reading']))
    if d.get('interests'):
        bullets('Strongest interests (to explore, not to decide)', [f"{i['label']} ({i['value']}/100)" for i in d['interests']])
    for key, title in (('strengths', 'Secure skills'), ('focus', 'Skills to strengthen first'), ('habit_strengths', 'Study habits that are working'), ('habit_focus', 'Study habits to improve')):
        bullets(title, d.get(key))
    if d.get('branches'):
        bullets('Engineering branches to explore next', [f"{b['name']}" + (f" (links to: {', '.join(b['why'])})" if b.get('why') else '') for b in d['branches']])
    bullets('Shortlist', [f"{s['name']} {('— ' + s['note']) if s['note'] else ''}" for s in d.get('shortlist', [])])
    if d.get('plan'):
        bullets('Practice plan for the gaps', [f"{p['skill']}: {', '.join(p['tasks']) or 'mentor will choose a task'}" for p in d['plan']])
    if d.get('admissions'):
        el.append(Paragraph('Admission routes: awareness', H2))
        el.append(table([[esc(a['name']), esc(a['classification']), 'Verified ' + a['last'] if a['verified'] else 'Requires verification'] for a in d['admissions']], [70 * mm, 55 * mm, 45 * mm], ['Route', 'Type', 'Status']))
    if d.get('actions'):
        a = d['actions']
        bullets('Actions', [f"{a['done']} of {a['total']} agreed actions completed"] + [f"Done: {t}" for t in a['titles_done']] + [f"Open: {o['title']} ({o['owner']})" for o in a['open']])
    if d.get('goals'):
        bullets('Goals', [f"{g['title']}" + (f" ({g.get('status')})" if g.get('status') else '') for g in d['goals']])
    bullets('Sessions', [f"{s['when']} {s['title']} ({s['status']})" + (f": {s['summary']}" if s['summary'] else '') for s in d.get('sessions', [])])
    bullets('Mentor comments', [f"{n['when']}: {n['body']}" for n in d.get('mentor_notes', [])])
    if d.get('growth'):
        el.append(Paragraph('Growth compared with the student’s own earlier results', H2))
        el.append(table([[esc(g['label']), f"{g['first']:.0f}{g['unit']}" if g['unit'] == '%' else f"{g['first']:.1f}", f"{g['last']:.0f}{g['unit']}" if g['unit'] == '%' else f"{g['last']:.1f}",
                          f"{g['delta']:+.1f}", 'few items' if g['small'] else ''] for g in d['growth']], [70 * mm, 30 * mm, 30 * mm, 20 * mm, 20 * mm], ['Skill', 'First', 'Latest', 'Change', 'Note']))
    bullets('What to do next', d.get('next'))
    el.append(Paragraph('Please note', H2))
    for l in d['limits']:
        el.append(Paragraph('• ' + esc(l), SM))
    el.append(Spacer(1, 8))
    el.append(Paragraph('EduAakashaa · info@eduaakashaa.com · +91-80157 22706 · www.eduaakashaa.com. Prepared with AI-assisted analysis and reviewed by a mentor; verify admission details on official sources.', SM))

    buf = BytesIO()
    SimpleDocTemplate(buf, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=16 * mm, bottomMargin=16 * mm, title=d['title']).build(el)
    return buf.getvalue()
