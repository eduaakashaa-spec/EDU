"""Monthly and whole-plan PDF reports for the Smart Study Planner: the plan as a calendar coloured by what was done, with infographics drawn natively
(no chart library, so they render on the web server): subject and kind-of-work bars, hours per week, topic table and key dates.
month_pdf(plan, name, year, month) and plan_report_pdf(plan, name). Uses the EduAakashaA report template in services/ea_pdf.py."""
import calendar as _cal
from collections import defaultdict
from datetime import date, timedelta

from reportlab.lib import colors as _c
from reportlab.lib.units import mm
from reportlab.platypus import Flowable, PageBreak, Spacer

from app.models_planner import SpTask
from app.services import ea_pdf as E
from app.services import planner as P

W = E.W - 2 * E.MX
SUBJ_COL = {'Physics': E.NAVY, 'Chemistry': E.ORANGE, 'Mathematics': E.GREEN, 'Biology': _c.HexColor('#7A3E9D'), 'Mock / general': E.MUTED}
OK_FILL, PART_FILL, MISS_FILL, TODO_FILL, REST_FILL = _c.HexColor('#D7EFE3'), _c.HexColor('#FCE8C2'), _c.HexColor('#F6D3D3'), E.PAPER, _c.HexColor('#E4E6EE')
STATE_LEGEND = [(OK_FILL, 'All done'), (PART_FILL, 'Part done'), (MISS_FILL, 'Missed'), (TODO_FILL, 'Coming up'), (REST_FILL, 'Rest day')]
SUBJ_LEGEND = [(E.NAVY, 'Physics'), (E.ORANGE, 'Chemistry'), (E.GREEN, 'Mathematics'), (E.ORANGE, 'MOCK tag: a mock test day')]


def _subj_col(s):
    return SUBJ_COL.get(s or 'Mock / general', E.MUTED)


def _work(tasks):
    return [t for t in tasks if t.task_type != 'rest']


def _mins(t):
    return t.minutes_done or t.minutes or 0


def _day_state(day, ts, today):
    """('none'|'rest'|'ok'|'part'|'miss'|'todo', done, total) for one day's tasks."""
    if not ts:
        return 'none', 0, 0
    w = _work(ts)
    if not w:
        return 'rest', 0, 0
    done = sum(1 for t in w if t.status == 'done')
    if done == len(w):
        return 'ok', done, len(w)
    if day >= today and not done:
        return 'todo', done, len(w)       # today is not missed until it is over
    return ('part' if done else 'miss'), done, len(w)


def _pct(a, b):
    return round(100 * a / b) if b else 0


def _tot(ts):
    w = _work(ts)
    return {'tasks': len(w), 'done': sum(1 for t in w if t.status == 'done'), 'plan_min': sum(t.minutes or 0 for t in w), 'done_min': sum(_mins(t) for t in w if t.status == 'done')}


class CalendarMonth(Flowable):
    """One month as a calendar. Each day is coloured by how much of it was done and shows tasks done/planned, subject dots, a minutes bar and a MOCK tag."""

    def __init__(self, by_day, year, month, today, width=W, cell_h=22 * mm, compact=False):
        super().__init__()
        self.by_day, self.year, self.month, self.today, self.width, self.cell_h, self.compact = by_day, year, month, today, width, cell_h, compact
        self.weeks = _cal.Calendar(0).monthdatescalendar(year, month)
        self.head_h = 6 * mm
        self.height = self.head_h + self.cell_h * len(self.weeks)

    def wrap(self, aw, ah):
        return self.width, self.height

    def draw(self):
        c, cp = self.canv, self.compact
        cw = self.width / 7.0
        for i, name in enumerate(('MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN')):
            c.setFillColor(E.NAVY_INK if i < 5 else E.NAVY)
            c.roundRect(i * cw + 0.4 * mm, self.height - self.head_h + 0.6 * mm, cw - 0.8 * mm, self.head_h - 1.2 * mm, 1.2 * mm, stroke=0, fill=1)
            c.setFillColor(_c.white)
            c.setFont(E.MONO, 6.6 if cp else 7.2)
            c.drawCentredString(i * cw + cw / 2, self.height - self.head_h + 2.2 * mm, name)
        for r, week in enumerate(self.weeks):
            for i, d in enumerate(week):
                if d.month != self.month:
                    continue
                x, y = i * cw + 0.4 * mm, self.height - self.head_h - (r + 1) * self.cell_h + 0.4 * mm
                w, h = cw - 0.8 * mm, self.cell_h - 0.8 * mm
                ts = self.by_day.get(d, [])
                st, done, total = _day_state(d, ts, self.today)
                c.setFillColor({'ok': OK_FILL, 'part': PART_FILL, 'miss': MISS_FILL, 'todo': TODO_FILL, 'rest': REST_FILL, 'none': E.CREAM2}[st])
                c.setStrokeColor(E.ORANGE if d == self.today else E.HAIR)
                c.setLineWidth(1.4 if d == self.today else 0.4)
                c.roundRect(x, y, w, h, 1.6 * mm, stroke=1, fill=1)
                c.setFillColor(E.MUTED if st == 'none' else E.INK)
                c.setFont(E.SANS_B, 8 if cp else 9.5)
                c.drawString(x + 1.6 * mm, y + h - (3.6 if cp else 4.4) * mm, str(d.day))
                if st == 'rest':
                    c.setFillColor(E.MUTED)
                    c.setFont(E.MONO, 5.6 if cp else 6.2)
                    c.drawRightString(x + w - 1.4 * mm, y + h - (3.4 if cp else 4.2) * mm, 'REST')
                    continue
                if not total:
                    continue
                if any(t.task_type == 'mock' for t in ts):
                    c.setFillColor(E.ORANGE)
                    c.setFont(E.MONO, 5)
                    c.drawRightString(x + w - 1.4 * mm, y + h - (3.4 if cp else 4.2) * mm, 'MOCK')
                elif st == 'ok':
                    c.setFillColor(E.GREEN)
                    c.circle(x + w - 2.6 * mm, y + h - (2.8 if cp else 3.4) * mm, 1.3 * mm, stroke=0, fill=1)
                c.setFillColor(E.INK)
                if not cp:
                    c.setFont(E.SANS_B, 7)
                    c.drawString(x + 1.6 * mm, y + 7.4 * mm, '%d/%d tasks' % (done, total))
                    subs = []
                    for t in _work(ts):
                        s = t.subject or 'Mock / general'
                        if s not in subs:
                            subs.append(s)
                    for k, s in enumerate(subs[:4]):
                        c.setFillColor(_subj_col(s))
                        c.circle(x + 2.4 * mm + k * 3.4 * mm, y + 5.2 * mm, 1.1 * mm, stroke=0, fill=1)
                else:
                    c.setFont(E.SANS, 5.8)
                    c.drawString(x + 1.6 * mm, y + 3.9 * mm, '%d/%d' % (done, total))
                plan_min, done_min = sum(t.minutes or 0 for t in _work(ts)), sum(_mins(t) for t in _work(ts) if t.status == 'done')
                bw = w - 3.2 * mm
                c.setFillColor(_c.HexColor('#D9D2BE'))
                c.roundRect(x + 1.6 * mm, y + 1.3 * mm, bw, 1.3 * mm, 0.6 * mm, stroke=0, fill=1)
                if plan_min and done_min:
                    c.setFillColor(E.GREEN)
                    c.roundRect(x + 1.6 * mm, y + 1.3 * mm, max(1.3 * mm, bw * min(1.0, float(done_min) / plan_min)), 1.3 * mm, 0.6 * mm, stroke=0, fill=1)


class WeekChart(Flowable):
    """Hours per week as vertical bars: planned (light) with done (solid) over it. weeks: [(label, planned_min, done_min)]."""

    def __init__(self, weeks, width=W, height=46 * mm):
        super().__init__()
        self.weeks, self.width, self.height = weeks, width, height

    def wrap(self, aw, ah):
        return self.width, self.height

    def draw(self):
        c = self.canv
        n = max(1, len(self.weeks))
        top = max([w[1] for w in self.weeks] + [60]) / 60.0
        base, plot_h = 9 * mm, self.height - 16 * mm
        slot = self.width / n
        bw = min(9 * mm, slot * 0.68)
        c.setStrokeColor(E.HAIR)
        c.setLineWidth(0.4)
        c.line(0, base, self.width, base)
        for i, (label, plan_m, done_m) in enumerate(self.weeks):
            x = i * slot + (slot - bw) / 2
            ph, dh = plot_h * (plan_m / 60.0) / top, plot_h * (done_m / 60.0) / top
            c.setFillColor(_c.HexColor('#C9D4EC'))
            c.roundRect(x, base, bw, max(ph, 0.6 * mm), 1 * mm, stroke=0, fill=1)
            if dh > 0:
                c.setFillColor(E.NAVY)
                c.roundRect(x, base, bw, max(dh, 0.8 * mm), 1 * mm, stroke=0, fill=1)
            c.setFillColor(E.INK)
            c.setFont(E.MONO, 5.6)
            c.drawCentredString(x + bw / 2, base + max(ph, 0.6 * mm) + 1.2 * mm, '%.0f' % (plan_m / 60.0))
            c.setFillColor(E.MUTED)
            c.drawCentredString(x + bw / 2, base - 3.6 * mm, label)


class Legend(Flowable):
    def __init__(self, items, width=W):
        super().__init__()
        self.items, self.width, self.height = items, width, 6 * mm

    def wrap(self, aw, ah):
        return self.width, self.height

    def draw(self):
        c, x = self.canv, 0
        for col, text in self.items:
            c.setFillColor(col)
            c.setStrokeColor(E.HAIR)
            c.roundRect(x, 1.2 * mm, 3.6 * mm, 3.6 * mm, 0.9 * mm, stroke=1, fill=1)
            c.setFillColor(E.MUTED)
            c.setFont(E.SANS, 7)
            c.drawString(x + 5 * mm, 2.2 * mm, text)
            x += 5 * mm + c.stringWidth(text, E.SANS, 7) + 5 * mm


def _by_day(plan):
    out = defaultdict(list)
    for t in plan.tasks.order_by(SpTask.day, SpTask.id).all():
        out[t.day].append(t)
    return out


def plan_months(plan):
    """[(year, month)] from the plan's first to its last task day."""
    days = [t.day for t in plan.tasks.all()]
    if not days:
        return []
    a, b, out = min(days), max(days), []
    y, m = a.year, a.month
    while (y, m) <= (b.year, b.month):
        out.append((y, m))
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)
    return out


def _bars(ts, key):
    by = defaultdict(lambda: [0, 0])
    for t in _work(ts):
        k = key(t)
        by[k][0] += t.minutes or 0
        if t.status == 'done':
            by[k][1] += _mins(t)
    return by


def _subject_bars(ts):
    return [(k, _pct(v[1], v[0]), '%.1fh of %.1fh' % (v[1] / 60.0, v[0] / 60.0), _subj_col(k)) for k, v in sorted(_bars(ts, lambda t: t.subject or 'Mock / general').items(), key=lambda kv: -kv[1][0])]


def _type_bars(ts):
    return [(P.TASK_TYPES[k]['label'], _pct(v[1], v[0]), '%.1fh of %.1fh' % (v[1] / 60.0, v[0] / 60.0), E.NAVY) for k, v in sorted(_bars(ts, lambda t: t.task_type).items(), key=lambda kv: -kv[1][0])]


def _weeks(by_day, lo, hi):
    out, d = [], P.week_start(lo)
    while d <= hi:
        s = _tot([t for k in range(7) for t in by_day.get(d + timedelta(days=k), [])])
        out.append((d.strftime('%d/%m'), s['plan_min'], s['done_min']))
        d += timedelta(days=7)
    return out


def _topic_rows(ts, limit):
    by = {}
    for t in _work(ts):
        if not t.chapter or t.task_type == 'mock':
            continue
        r = by.setdefault((t.subject or '', t.chapter), {'first': t.day, 'min': 0, 'n': 0, 'nd': 0})
        r['first'] = min(r['first'], t.day)
        r['min'] += t.minutes or 0
        r['n'] += 1
        r['nd'] += 1 if t.status == 'done' else 0
    rows = sorted(by.items(), key=lambda kv: -kv[1]['min'])[:limit]
    return [[s, ch[:48], r['first'].strftime('%d %b'), '%.1f h' % (r['min'] / 60.0), '%d%%' % _pct(r['nd'], r['n'])] for (s, ch), r in rows]


TOPIC_W = [31 * mm, W - 31 * mm - 22 * mm - 18 * mm - 16 * mm, 22 * mm, 18 * mm, 16 * mm]


def month_pdf(plan, student_name, year, month, today=None):
    """Monthly report: the month as a calendar coloured by what was done, then subject, kind-of-work, weekly and topic infographics."""
    today = today or P.today()
    by_day = _by_day(plan)
    in_month = {d: l for d, l in by_day.items() if d.year == year and d.month == month}
    ts = [t for l in in_month.values() for t in l]
    s = _tot(ts)
    name = '%s %d' % (_cal.month_name[month], year)
    full = sum(1 for d, l in in_month.items() if _day_state(d, l, today)[0] == 'ok')
    days_work = sum(1 for l in in_month.values() if _work(l))
    meta = {'eyebrow': 'Smart Study Planner', 'title_lines': [('Monthly study', False), ('report', True)], 'title': 'Monthly study report',
            'subtitle': [plan.title, '%s · %s' % (student_name, name)],
            'cover_stats': [('Month', '%s %d' % (_cal.month_abbr[month], year)), ('Tasks done', '%d of %d' % (s['done'], s['tasks'])), ('Hours done', '%.1f' % (s['done_min'] / 60.0)), ('Full days', '%d of %d' % (full, days_work))],
            'footer_left': 'Smart Study Planner', 'running_head': 'Monthly report · ' + student_name}
    el = E.heading(name, 'Your month, <i>day by day</i>')
    el += [E.kpis([('Tasks done', '%d%%' % _pct(s['done'], s['tasks']), 'orange'), ('Tasks', '%d of %d' % (s['done'], s['tasks']), 'navy'), ('Hours done', '%.1f of %.1f' % (s['done_min'] / 60.0, s['plan_min'] / 60.0), 'green'),
                   ('Full days', '%d of %d' % (full, days_work), 'navy')]), Spacer(1, 6),
           CalendarMonth(by_day, year, month, today, cell_h=24 * mm), Spacer(1, 2), Legend(STATE_LEGEND), Legend(SUBJ_LEGEND), Spacer(1, 4),
           E.callout('<b>How to read this.</b> Each box is one day. The small bar at the foot of a box is the share of that day\'s minutes you finished; the dots show which subjects it held. Green days are fully done, '
                     'amber days are part done and red days were missed. A missed day is not a failure: move the work to a day with room, or ask your mentor to rebalance the plan.', 'orange'), PageBreak()]

    el += E.heading(name, 'Where the <i>time went</i>')
    sb = _subject_bars(ts)
    if sb:
        el += [E.P('By subject (hours done against hours planned)', 'h2'), E.Bars(sb, label_w=40 * mm, row_h=7.4 * mm)]
    tb = _type_bars(ts)
    if tb:
        el += [E.P('By kind of work', 'h2'), E.Bars(tb, label_w=40 * mm, row_h=7.4 * mm)]
    if in_month:
        wk = _weeks(by_day, min(in_month), max(in_month))
        el += [E.P('Hours per week (light bar planned, dark bar done)', 'h2'), WeekChart(wk, height=32 * mm)]
    topics = _topic_rows(ts, 5)
    if topics:
        el += [E.P('Topics worked on this month', 'h2'), E.data_table(['Subject', 'Topic', 'First', 'Planned', 'Done'], topics, TOPIC_W)]
    late = [t for t in _work(ts) if t.status == 'todo' and t.day < today]
    if late:
        names = '; '.join('%s (%s)' % (E.esc(t.title[:55]), t.day.strftime('%d %b')) for t in late[:3])
        el += [Spacer(1, 6), E.callout('<b>Still to catch up: %d task%s.</b> Oldest first: %s%s' % (len(late), '' if len(late) == 1 else 's', names, ' and more.' if len(late) > 3 else '.'), 'navy')]
    el += [Spacer(1, 4), E.P('Please note: this report counts what was recorded in the planner. It is a study aid, not a prediction of marks or ranks.', 'small')]
    return E.build_report(meta, el)


def plan_report_pdf(plan, student_name, today=None):
    """Whole-plan report: overview and weekly load, every month as a calendar, then topic and key-date infographics."""
    today = today or P.today()
    by_day = _by_day(plan)
    all_t = [t for l in by_day.values() for t in l]
    months = plan_months(plan)
    s = _tot(all_t)
    first, last = (min(by_day), max(by_day)) if by_day else (today, today)
    due = [t for t in _work(all_t) if t.day <= today]
    due_done = sum(1 for t in due if t.status == 'done')
    info = P.LEVEL_INFO[plan.level]
    weeks = _weeks(by_day, first, last)
    meta = {'eyebrow': 'Smart Study Planner', 'title_lines': [('Whole plan', False), ('report', True)], 'title': 'Whole plan report',
            'subtitle': [plan.title, '%s · %s to %s' % (student_name, first.strftime('%d %b %Y'), last.strftime('%d %b %Y'))],
            'cover_stats': [('Months', str(len(months))), ('Tasks', str(s['tasks'])), ('Hours planned', '%.0f' % (s['plan_min'] / 60.0)), ('Done so far', '%d%%' % _pct(due_done, len(due)))],
            'footer_left': 'Smart Study Planner', 'running_head': 'Whole plan report · ' + student_name}
    el = E.heading('The whole plan', 'From <i>%s</i> to <i>%s</i>' % (first.strftime('%d %b'), last.strftime('%d %b %Y')))
    el += [E.kpis([('Weeks', len(weeks), 'navy'), ('Tasks', s['tasks'], 'navy'), ('Hours planned', '%.0f' % (s['plan_min'] / 60.0), 'orange'),
                   ('Hours a day', '%g' % (plan.hours_per_day or info['hours']), 'navy'), ('Done so far', '%d%%' % _pct(due_done, len(due)), 'green')]), Spacer(1, 6)]
    if plan.exam_date:
        left = (plan.exam_date - today).days
        el += [E.callout('<b>Exam: %s.</b> %s' % (plan.exam_date.strftime('%d %b %Y'), ('%d days to go from today.' % left) if left >= 0 else 'The exam date has passed.'), 'navy'), Spacer(1, 4)]
    el += [E.P('Hours each week (light bar planned, dark bar done)', 'h2'), WeekChart(weeks, height=50 * mm), Spacer(1, 2)]
    by = _bars(all_t, lambda t: t.subject or 'Mock / general')
    top = max([v[0] for v in by.values()] + [1])
    if by:
        el += [E.P('Planned time by subject', 'h2'), E.Bars([(k, _pct(v[0], top), '%.0f hours (%d%% done)' % (v[0] / 60.0, _pct(v[1], v[0])), _subj_col(k)) for k, v in sorted(by.items(), key=lambda kv: -kv[1][0])], label_w=40 * mm)]
    el += [PageBreak()]

    for i in range(0, len(months), 2):
        pair = months[i:i + 2]
        el += E.heading('Calendar', ' and '.join('<i>%s</i>' % _cal.month_name[m] for _y, m in pair))
        for y, m in pair:
            ms = _tot([t for d, l in by_day.items() if d.year == y and d.month == m for t in l])
            el += [E.P('<b>%s %d</b> &nbsp;·&nbsp; %d tasks &nbsp;·&nbsp; %.0f hours planned &nbsp;·&nbsp; %d%% done' % (_cal.month_name[m], y, ms['tasks'], ms['plan_min'] / 60.0, _pct(ms['done'], ms['tasks']))),
                   CalendarMonth(by_day, y, m, today, cell_h=11.5 * mm, compact=True), Spacer(1, 7)]
        el += [Legend(STATE_LEGEND), PageBreak()]

    el += E.heading('Topics and key dates', 'What the plan <i>covers</i>')
    topics = _topic_rows(all_t, 12)
    if topics:
        el += [E.P('Biggest topics by planned time', 'h2'), E.data_table(['Subject', 'Topic', 'First', 'Planned', 'Done'], topics, TOPIC_W)]
    mocks = [t for t in _work(all_t) if t.task_type == 'mock']
    if mocks:
        rows = [[t.day.strftime('%a %d %b %Y'), t.title[:70], 'Done' if t.status == 'done' else ('Missed' if t.day < today else 'Coming up')] for t in mocks[:8]]
        el += [E.P('Mock tests and test days', 'h2'), E.data_table(['Date', 'Task', 'Status'], rows, [32 * mm, W - 32 * mm - 24 * mm, 24 * mm])]
    el += [Spacer(1, 8), E.callout('<b>Please note.</b> This report shows the plan as built and what was recorded against it. Plans change as school dates and mock results come in: ask your mentor to rebalance when they do. '
                                   'It is a study aid, not a prediction of marks or ranks.', 'orange')]
    return E.build_report(meta, el)
