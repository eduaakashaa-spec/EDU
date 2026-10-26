"""UCEED Mock Test Centre: saving finished attempts and the confidence (calibration) analysis used by the student, mentor and PDF reports.

Confidence codes sent by the page: G = guess, L = low, M = medium, H = high. Question status: right | part | wrong | blank | bonus.
Reading the numbers: 'sure but wrong' (H and wrong/part) is the risk flag: a confident misconception, or a careless slip. 'Unsure but right'
(G/L and right) means knowledge the student is not yet trusting. Calibration compares how often each confidence level was right.
"""
import json
import re
from datetime import datetime
from io import BytesIO

from app.extensions import db
from app.models_pulse import PulseMockResult

PAPERS = tuple(str(y) for y in range(2018, 2027)) + tuple('M%d' % i for i in range(1, 6))
CONF = (('H', 'High'), ('M', 'Medium'), ('L', 'Low'), ('G', 'Guess'))
CONF_LABEL = dict(CONF)
TOPICS = {'OBS': 'Observation', 'NUM': 'Numbers & logic', 'SPA': '3D & spatial', 'PAT': 'Patterns', 'SCI': 'Everyday science', 'VIS': 'Visual design', 'CUL': 'Art & culture'}
MAX_BODY = 400_000
MIN_RATED = 8           # fewer rated answers than this: show the numbers, but do not draw a calibration conclusion


def _num(v, default=0.0, lo=-1e6, hi=1e6):
    try:
        return max(lo, min(hi, float(v)))
    except (TypeError, ValueError):
        return default


def _dt(s):
    try:
        return datetime.fromisoformat(str(s).replace('Z', '+00:00')).replace(tzinfo=None)
    except ValueError:
        return None


def clean_payload(d):
    """Validate the posted JSON and keep only the fields we use. Returns (payload, error)."""
    if not isinstance(d, dict):
        return None, 'bad payload'
    paper = str(d.get('paper') or '')
    if paper not in PAPERS:
        return None, 'unknown paper'
    qs = d.get('questions') or {}
    if not isinstance(qs, dict) or len(qs) > 200:
        return None, 'bad questions'
    out_q = {}
    for k, q in qs.items():
        if not isinstance(q, dict) or not re.fullmatch(r'\d{1,3}', str(k)):
            continue
        st = q.get('status') if q.get('status') in ('right', 'part', 'wrong', 'blank', 'bonus') else 'blank'
        cf = q.get('confidence') if q.get('confidence') in ('G', 'L', 'M', 'H') else None
        out_q[str(k)] = {'type': str(q.get('type') or '')[:4], 'topic': (q.get('topic') if q.get('topic') in TOPICS else None), 'answer': (None if q.get('answer') is None else str(q.get('answer'))[:20]),
                         'official': str(q.get('official') or '')[:30], 'status': st, 'marks': round(_num(q.get('marks'), 0, -50, 50), 2), 'confidence': cf}
    secs = []
    for s in (d.get('sections') or [])[:6]:
        if isinstance(s, dict):
            secs.append({'type': str(s.get('type') or '')[:4], 'score': round(_num(s.get('score')), 2), 'max': round(_num(s.get('max')), 2), 'right': int(_num(s.get('right'))),
                         'partial': int(_num(s.get('partial'))), 'wrong': int(_num(s.get('wrong'))), 'blank': int(_num(s.get('blank')))})
    return {'paper': paper, 'paperTitle': str(d.get('paperTitle') or ('UCEED ' + paper))[:80], 'mode': 'mock' if d.get('mode') == 'mock' else 'practice',
            'score': round(_num(d.get('score')), 2), 'max': round(_num(d.get('max'), 200, 1, 1000), 2), 'sections': secs, 'questions': out_q,
            'startedAt': d.get('startedAt'), 'finishedAt': d.get('finishedAt'), 'autoSubmitted': bool(d.get('autoSubmitted'))}, None


def save_result(user_id, d):
    p, err = clean_payload(d)
    if err:
        return None, err
    qs = p['questions'].values()
    right = sum(1 for q in qs if q['status'] in ('right', 'bonus'))
    wrong = sum(1 for q in qs if q['status'] in ('wrong', 'part'))
    rated = [q for q in qs if q['confidence']]
    sure_wrong = sum(1 for q in rated if q['confidence'] == 'H' and q['status'] in ('wrong', 'part'))
    r = PulseMockResult(user_id=user_id, paper=p['paper'], paper_title=p['paperTitle'], mode=p['mode'], score=p['score'], max_score=p['max'],
                        answered=sum(1 for q in qs if q['status'] != 'blank'), right=right, wrong=wrong, sure_wrong=sure_wrong, rated=len(rated),
                        auto_submitted=p['autoSubmitted'], started_at=_dt(p['startedAt']), finished_at=_dt(p['finishedAt']) or datetime.utcnow(),
                        payload_json=json.dumps(p, separators=(',', ':')))
    db.session.add(r)
    db.session.commit()
    return r, None


# ---- analysis -------------------------------------------------------------------------------------------------------------------
def analyse(rows):
    """Confidence, topic and section analysis over one or more attempts (each a PulseMockResult)."""
    conf = {c: {'n': 0, 'right': 0, 'wrong': 0} for c, _ in CONF}
    topics = {}
    sections = {}
    unrated = 0
    for r in rows:
        p = json.loads(r.payload_json or '{}')
        for q in (p.get('questions') or {}).values():
            if q['status'] == 'blank':
                continue
            ok = q['status'] in ('right', 'bonus')
            bad = q['status'] in ('wrong', 'part')
            if q['confidence']:
                c = conf[q['confidence']]
                c['n'] += 1
                c['right'] += 1 if ok else 0
                c['wrong'] += 1 if bad else 0
            else:
                unrated += 1
            if q['topic']:
                t = topics.setdefault(q['topic'], {'n': 0, 'right': 0, 'wrong': 0, 'sure_wrong': 0, 'unsure_right': 0})
                t['n'] += 1
                t['right'] += 1 if ok else 0
                t['wrong'] += 1 if bad else 0
                t['sure_wrong'] += 1 if (q['confidence'] == 'H' and bad) else 0
                t['unsure_right'] += 1 if (q['confidence'] in ('G', 'L') and ok) else 0
        for s in p.get('sections') or []:
            a = sections.setdefault(s['type'], {'score': 0.0, 'max': 0.0})
            a['score'] += s['score']
            a['max'] += s['max']
    for c in conf.values():
        c['pct'] = round(100 * c['right'] / c['n']) if c['n'] else None
    for t in topics.values():
        t['pct'] = round(100 * t['right'] / t['n']) if t['n'] else None
        t['label'] = None
    for k, t in topics.items():
        t['label'] = TOPICS[k]
    rated = sum(c['n'] for c in conf.values())
    sure_wrong = conf['H']['wrong']
    unsure_right = conf['G']['right'] + conf['L']['right']
    notes = []
    if rated < MIN_RATED:
        notes.append('Too few answers carry a confidence rating to judge calibration. Rate every answer in the next mock.')
    else:
        h, g = conf['H'], conf['G']
        if h['n'] >= 3 and h['pct'] is not None and h['pct'] < 70:
            notes.append('High-confidence answers were right only %d%% of the time: revisit the %d confident mistakes first; they point to a belief or method to correct, not just a slip.' % (h['pct'], h['wrong']))
        if conf['L']['n'] + g['n'] >= 3 and unsure_right >= 0.4 * (conf['L']['n'] + g['n']):
            notes.append('%d answers you were unsure about were right. You know more than you trust: write down why an answer is right before moving on.' % unsure_right)
        if g['n'] >= 3 and g['pct'] is not None and g['pct'] <= 30:
            notes.append('Guesses were right %d%% of the time. Where negative marking applies, leave real guesses blank.' % g['pct'])
        if not notes:
            notes.append('Confidence matches results well. Keep rating every answer so this stays reliable.')
    risky = sorted([(k, t) for k, t in topics.items() if t['sure_wrong']], key=lambda kv: -kv[1]['sure_wrong'])
    return {'conf': conf, 'topics': topics, 'sections': sections, 'rated': rated, 'unrated': unrated, 'sure_wrong': sure_wrong, 'unsure_right': unsure_right,
            'notes': notes, 'risky_topics': [(k, TOPICS[k], t['sure_wrong']) for k, t in risky],
            'weak_topics': [TOPICS[k] for k, t in sorted(topics.items(), key=lambda kv: (kv[1]['pct'] if kv[1]['pct'] is not None else 101)) if t['n'] >= 4 and t['pct'] is not None and t['pct'] < 50][:3],
            'enough': rated >= MIN_RATED}


def for_user(user_id, limit=None):
    q = PulseMockResult.query.filter_by(user_id=user_id).order_by(PulseMockResult.finished_at.desc())
    return q.limit(limit).all() if limit else q.all()


def summary(user_id):
    rows = for_user(user_id)
    if not rows:
        return {'attempts': 0, 'rows': [], 'best': None, 'avg_pct': None, 'trend': [], 'an': analyse([]), 'sure_wrong_rate': None}
    pct = [round(100 * r.score / r.max_score) for r in reversed(rows) if r.max_score]
    rated = sum(r.rated or 0 for r in rows)
    return {'attempts': len(rows), 'rows': rows, 'best': max(rows, key=lambda r: (r.score or 0) / (r.max_score or 1)), 'avg_pct': round(sum(pct) / len(pct)) if pct else None,
            'trend': pct[-10:], 'an': analyse(rows), 'sure_wrong_rate': round(100 * sum(r.sure_wrong or 0 for r in rows) / rated) if rated else None}


# ---- PDF (EduAakashaA report template, see app/services/ea_pdf.py) --------------------------------------------------------------------
def pdf(result, student_name):
    from reportlab.lib.units import mm
    from reportlab.platypus import PageBreak, Spacer

    from app.services import ea_pdf as E

    an = analyse([result])
    p = json.loads(result.payload_json or '{}')
    pct = round(100 * result.score / result.max_score) if result.max_score else 0
    when = (result.finished_at or datetime.utcnow()).strftime('%d %b %Y')
    meta = {'eyebrow': 'UCEED Mock Test Centre', 'title_lines': [('Mock test', False), ('report', True)], 'title': 'UCEED mock report',
            'subtitle': [result.paper_title or 'UCEED mock', '%s  ·  %s  ·  %s' % (student_name, 'timed mock' if result.mode == 'mock' else 'practice', when)],
            'cover_stats': [('Score', '%g / %g' % (result.score, result.max_score)), ('Accuracy', '%d%%' % pct), ('Right', result.right), ('Confident mistakes', result.sure_wrong)],
            'footer_left': 'UCEED Mock Test Centre', 'running_head': 'UCEED mock report · ' + (result.paper_title or '')}
    el = E.heading('Your result', 'How this <i>mock</i> went')
    el += [E.P('%s took <b>%s</b> as a %s on %s. The score is out of %g. Sections below show where the marks came from; the next page shows how well the confidence ratings matched the results.' %
               (E.esc(student_name), E.esc(result.paper_title or 'the paper'), 'timed mock' if result.mode == 'mock' else 'practice set', when, result.max_score)), Spacer(1, 4),
           E.kpis([('Score', '%g' % result.score, 'navy'), ('Accuracy', '%d%%' % pct, 'orange'), ('Right', result.right, 'green'), ('Wrong or partly wrong', result.wrong, 'red'),
                   ('High confidence, wrong', result.sure_wrong, 'red')])]
    if p.get('sections'):
        el += [E.P('By section', 'h2'), E.data_table(['Section', 'Score', 'Right', 'Partial', 'Wrong', 'Blank'],
                                                   [[s['type'], '%s / %s' % (s['score'], s['max']), s['right'], s['partial'], s['wrong'], s['blank']] for s in p['sections']],
                                                   [38 * mm, 40 * mm, 24 * mm, 24 * mm, 24 * mm, 24 * mm]), Spacer(1, 6),
               E.Bars([(s['type'], round(100 * s['score'] / s['max']) if s['max'] else 0, '%g / %g' % (s['score'], s['max']), E.NAVY) for s in p['sections']])]
    el += [Spacer(1, 8), E.callout('<b>Read this score as practice guidance.</b> A mock score does not predict the UCEED score, rank or admission. Use it to see which sections and topics to work on next.', 'navy'),
           PageBreak()]

    el += E.heading('Confidence check', 'Did your confidence <i>match</i> your results?')
    el += [E.P('Every answer was rated Guess, Low, Medium or High. A well-calibrated student is right more often when more confident. Gaps between the two are where the useful learning is.'), Spacer(1, 4)]
    tone = {'H': E.NAVY, 'M': E.NAVY, 'L': E.ORANGE, 'G': E.ORANGE}
    el.append(E.Bars([(CONF_LABEL[c], an['conf'][c]['pct'], ('%d%%  (%d of %d)' % (an['conf'][c]['pct'], an['conf'][c]['right'], an['conf'][c]['n'])) if an['conf'][c]['pct'] is not None else 'no answers', tone[c])
                      for c, _ in CONF], row_h=9 * mm))
    el += [Spacer(1, 4), E.P('Bars show the share of answers that were right at each confidence level.', 'small'), Spacer(1, 4)]
    for n in an['notes']:
        el.append(E.callout(E.esc(n)))
        el.append(Spacer(1, 4))
    if an['topics']:
        rows = sorted(an['topics'].values(), key=lambda t: t['pct'] if t['pct'] is not None else 101)
        el += [E.P('By topic', 'h2'),
               E.Bars([(t['label'], t['pct'], '%d%%  (%d)' % (t['pct'], t['n']), E.GREEN if t['pct'] >= 70 else (E.ORANGE if t['pct'] >= 50 else E.RED)) for t in rows], label_w=44 * mm),
               Spacer(1, 6), E.data_table(['Topic', 'Answered', 'Right %', 'Sure but wrong', 'Unsure but right'], [[t['label'], t['n'], '%d%%' % t['pct'], t['sure_wrong'], t['unsure_right']] for t in rows],
                                           [52 * mm, 26 * mm, 26 * mm, 36 * mm, 34 * mm])]
    el.append(PageBreak())

    el += E.heading('Next steps', 'What to do <i>this week</i>')
    nxt = []
    if an['risky_topics']:
        nxt.append(('Re-solve the confident mistakes first', 'Start with %s. Wrong answers given with High confidence usually point to a method or belief to correct, not a slip.' % ', '.join(t[1] for t in an['risky_topics'][:3])))
    if an['weak_topics']:
        nxt.append(('Give short, regular sessions to weaker topics', '%s scored under 50%%. Two or three 25-minute sessions through the week work better than one long one.' % ', '.join(an['weak_topics'])))
    if an['unsure_right']:
        nxt.append(('Trust what you know', '%d answers were right but rated Guess or Low. Write one line on why each is right before moving on.' % an['unsure_right']))
    nxt += [('Rate every answer in the next mock', 'Confidence ratings are what make this report useful. Answers without a rating are left out of the calibration.'),
            ('Repeat after 7 to 10 days', 'Take another paper, or retry the same topics through EduPulse Reinforcement daily practice, and compare the two reports.'),
            ('Share this report with your mentor', 'Your EduAakashaa mentor can turn these patterns into a plan for the weeks ahead.')]
    el += [E.steps(nxt), Spacer(1, 10),
           E.callout('<b>Please note.</b> This report is generated automatically from your recorded mock attempt. Scores and topic percentages are practice guidance and depend on how many questions were answered; '
                     'they are not a prediction of the UCEED score, rank or admission, and are not a guarantee of any outcome. Official papers are IIT Bombay material used for practice; explanations are written by EduAakashaA.', 'orange')]
    return E.build_report(meta, el)
