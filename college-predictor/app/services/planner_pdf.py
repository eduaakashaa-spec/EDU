"""PDF downloads for the Smart Study Planner, in the EduAakashaA report template (see services/ea_pdf.py):
template_pdf (blank planner sheets with an example for a level), week_pdf (a student's plan for one week) and progress_pdf (progress report)."""
from datetime import timedelta

from reportlab.lib.units import mm
from reportlab.platypus import PageBreak, Spacer, Table, TableStyle

from app.services import ea_pdf as E
from app.services import planner as P

W = E.W - 2 * E.MX


def _grid(head, rows, widths, row_h=None):
    t = Table([[E.Paragraph(h.upper(), E.ST['th']) for h in head]] + rows, colWidths=widths, rowHeights=([None] + [row_h] * len(rows)) if row_h else None, repeatRows=1)
    t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), E.NAVY_INK), ('GRID', (0, 0), (-1, -1), 0.4, E.HAIR), ('VALIGN', (0, 0), (-1, -1), 'TOP'), ('ROWBACKGROUNDS', (0, 1), (-1, -1), [E.PAPER, E.CREAM2]),
                           ('TOPPADDING', (0, 0), (-1, -1), 4), ('BOTTOMPADDING', (0, 0), (-1, -1), 4), ('LEFTPADDING', (0, 0), (-1, -1), 5)]))
    return t


def template_pdf(level, exam='JEE'):
    info = P.LEVEL_INFO[level]
    meta = {'eyebrow': 'Smart Study Planner', 'title_lines': [('Study planner', False), ('template', True)], 'title': 'Study planner template',
            'subtitle': ['%s · %s' % (info['label'], info['tagline']), 'For %s · print it, fill it, keep it on your desk' % P.EXAMS.get(exam, exam)],
            'cover_stats': [('Level', info['label']), ('Hours a day', '%g' % info['hours']), ('Mocks', ('1 every 2 weeks' if info['mocks_per_week'] == 0 else '%d a week' % info['mocks_per_week'])), ('Rest', 'Sunday')],
            'footer_left': 'Smart Study Planner', 'running_head': 'Study planner template · ' + info['label']}
    el = E.heading('How this level works', '%s: <i>%s</i>' % (info['label'], info['tagline'].lower()))
    el += [E.P('<b>Who it is for.</b> ' + E.esc(info['who'])), E.P('<b>How it works.</b> ' + E.esc(info['how'])), E.P('An example day', 'h2'),
           E.data_table(['Time', 'Block', 'What to do'], [[a, b, c] for a, b, c in info['example_day']], [34 * mm, 28 * mm, W - 62 * mm]), E.P('The six kinds of task, with an example', 'h2')]
    rows = [[v['label'], v['how'], v['example']] for k, v in P.TASK_TYPES.items() if k != 'rest']
    el += [E.data_table(['Task', 'How to do it', 'Example'], rows, [24 * mm, 74 * mm, W - 98 * mm]), Spacer(1, 6),
           E.callout('<b>Tip.</b> Rate your confidence (Guess, Low, Medium, High) on every practice answer. Right answers you guessed, and wrong answers you were sure about, are the ones to fix first.', 'orange'), PageBreak()]

    el += E.heading('Weekly planner', 'Plan the <i>week</i>, then keep the promise')
    el += [E.P('Week starting: ______________ &nbsp;&nbsp; Goal for the week: ____________________________________________'), Spacer(1, 4)]
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    grid_rows = [[d, '', '', '', '', ''] for d in days]
    grid_rows[5][1] = 'Mock test'
    grid_rows[6][1] = 'Rest'
    el += [_grid(['Day', 'Morning', 'Afternoon', 'Evening', 'Night', 'Done'], grid_rows, [24 * mm, 36 * mm, 36 * mm, 36 * mm, 30 * mm, W - 162 * mm], row_h=17 * mm), Spacer(1, 8),
           E.P('End-of-week reflection', 'h2'), E.P('What went well: ____________________________________________________________'), E.P('What I will change: __________________________________________________________'),
           E.P('Questions for my mentor: _________________________________________________________'), PageBreak()]

    el += E.heading('Error log', 'Every mistake is a <i>mark</i> you can win back')
    el += [E.P('For each wrong or guessed question write what you did, the reason (concept, careless or guess) and the fix. Review this page every Sunday.'), Spacer(1, 4),
           _grid(['Question / topic', 'What I did', 'Reason', 'The fix', 'Fixed?'], [['', '', '', '', ''] for _ in range(11)], [40 * mm, 42 * mm, 24 * mm, 46 * mm, W - 152 * mm], row_h=15 * mm),
           Spacer(1, 8), E.callout('<b>Please note.</b> This template is a study aid. It does not predict marks or ranks. EduAakashaA mentors can adapt the plan to your school timetable.', 'orange')]
    return E.build_report(meta, el)


def week_pdf(plan, student_name, d=None):
    d = d or P.today()
    w0 = P.week_start(d)
    info = P.LEVEL_INFO[plan.level]
    tasks = [t for t in plan.tasks.all() if w0 <= t.day < w0 + timedelta(days=7)]
    tasks.sort(key=lambda t: (t.day, t.id))
    meta = {'eyebrow': 'Smart Study Planner', 'title_lines': [('This week\'s', False), ('study plan', True)], 'title': 'Weekly study plan',
            'subtitle': [plan.title, '%s · week of %s' % (student_name, w0.strftime('%d %b %Y'))],
            'cover_stats': [('Level', info['label']), ('Tasks', str(sum(1 for t in tasks if t.task_type != 'rest'))), ('Hours planned', '%.1f' % (sum(t.minutes or 0 for t in tasks) / 60.0)), ('Exam', plan.exam)],
            'footer_left': 'Smart Study Planner', 'running_head': 'Weekly plan · ' + student_name}
    el = E.heading('Your week', 'Week of <i>%s</i>' % w0.strftime('%d %b'))
    rows = []
    for t in tasks:
        rows.append([t.day.strftime('%a %d'), P.TASK_TYPES[t.task_type]['label'], t.title, '%d min' % (t.minutes or 0) if t.minutes else '-', 'Done' if t.status == 'done' else ''])
    el += [E.data_table(['Day', 'Type', 'Task', 'Time', 'Status'], rows, [20 * mm, 22 * mm, W - 78 * mm, 18 * mm, 18 * mm]), Spacer(1, 8),
           E.callout('<b>Today\'s thought.</b> ' + E.esc(P.quote_of_the_day(d)), 'navy'), Spacer(1, 6),
           E.callout('<b>Tip.</b> Tick a task only when it is finished. A smaller plan you complete beats a bigger plan you abandon.', 'orange')]
    return E.build_report(meta, el)


def progress_pdf(stats, student_name, activity):
    plan = stats['plan']
    info = P.LEVEL_INFO[plan.level]
    pct = stats['pct_due'] if stats['pct_due'] is not None else 0
    meta = {'eyebrow': 'Smart Study Planner', 'title_lines': [('Study progress', False), ('report', True)], 'title': 'Study progress report',
            'subtitle': [plan.title, '%s · %s' % (student_name, P.today().strftime('%d %b %Y'))],
            'cover_stats': [('Completed so far', '%d%%' % pct), ('Streak', '%d days' % stats['streak']), ('Hours done', '%.1f' % (stats['done_min'] / 60.0)), ('EduPulse questions', str(activity.get('questions', 0)))],
            'footer_left': 'Smart Study Planner', 'running_head': 'Progress report · ' + student_name}
    el = E.heading('Where you stand', 'Progress so <i>far</i>')
    el += [E.P('%s is on the <b>%s</b> plan (%s). Of the %d tasks due so far, %d are done.' % (E.esc(student_name), info['label'], P.EXAMS[plan.exam], stats['due'], len([1 for t in stats['plan'].tasks.all() if t.status == 'done' and t.day <= P.today()]))),
           Spacer(1, 4), E.kpis([('Done to date', '%d%%' % pct, 'orange'), ('This week', '%s%%' % (stats['week_pct'] if stats['week_pct'] is not None else '-'), 'navy'), ('Streak (days)', stats['streak'], 'green'),
                                 ('Overdue tasks', len(stats['overdue']), 'red'), ('Hours done', '%.1f / %.1f' % (stats['done_min'] / 60.0, stats['planned_min'] / 60.0), 'navy')])]
    subj = stats['by_subject']
    if subj:
        el += [E.P('By subject', 'h2'), E.Bars([(k, round(100 * v['done'] / v['planned']) if v['planned'] else 0, '%d of %d min' % (v['done'], v['planned']), E.NAVY) for k, v in subj.items()], label_w=44 * mm)]
    el += [E.P('By kind of work', 'h2'), E.data_table(['Type', 'Tasks done', 'Minutes done', 'Minutes planned'], [[P.TASK_TYPES[k]['label'], '%d of %d' % (v['completed'], v['tasks']), v['done'], v['planned']] for k, v in stats['by_type'].items()],
                                                       [40 * mm, 40 * mm, 40 * mm, W - 120 * mm]), PageBreak()]
    el += E.heading('EduPulse', 'Practice from the <i>question banks</i>')
    el += [E.P('Questions answered in EduPulse this week count toward your plan. Practice tasks in the planner link straight to EduPulse.'), Spacer(1, 4),
           E.kpis([('Reinforcement answers', activity.get('reinforce_answers', 0), 'navy'), ('UCEED practice answers', activity.get('pulse_answers', 0), 'navy'), ('Mock tests', activity.get('mocks', 0), 'orange')]), Spacer(1, 8)]
    steps = []
    if stats['overdue']:
        steps.append(('Clear the overdue tasks', '%d task(s) are past their date. Do the shortest first, or mark them skipped if they no longer fit.' % len(stats['overdue'])))
    if stats['streak'] < 3:
        steps.append(('Rebuild the streak', 'Finish one task today. A streak of three days is easier to keep than it sounds.'))
    steps += [('Keep the error log', 'Write every wrong or guessed answer with the reason and the fix.'), ('Share this report with your mentor', 'It shows what to adjust in next week\'s plan.')]
    el += [E.steps(steps), Spacer(1, 8), E.callout('<b>Today\'s thought.</b> ' + E.esc(P.quote_of_the_day()), 'navy'), Spacer(1, 6),
           E.callout('<b>Please note.</b> This report counts what you recorded in the planner and what EduPulse recorded. It is a study aid, not a prediction of marks or ranks.', 'orange')]
    return E.build_report(meta, el)
