"""Meeting update for Yusra Kazi: the 2 Nov 2026 follow-up call with Navid (father), Dr. Saravanan and Kalil.

Two packs, applied from Admin, Mentorship, on the enrolment they belong to (nothing is sent to anyone; running a pack twice adds nothing twice):
  * ELITE   for the Elite Mentorship enrolment: logs the meeting, retires what the meeting dropped, adds KPIs, actions and the next planned sessions.
  * ADDONS  for each add-on enrolment (B.Arch, NID, UCEED if she has them): adds the meeting decisions to the matching session details; a UCEED add-on's planned sessions are cancelled.
Source: the meeting transcript of 2 Nov 2026 and the Discovery Report. Dates not stated in the meeting are suggestions, marked in the notes. Text shown to the family follows the portal rules
(for example "EduAakashaA Members Group", never a chat-group wording). Fees and the payment are kept in the private mentor notes only.
"""
from datetime import date, datetime

MEETING_DAY = date(2026, 11, 2)
NOTE_TAG = 'Update 2 Nov 2026: '

ELITE = {
    'key': 'yusra-2026-11-02-elite',
    'label': 'Yusra Kazi, 2 Nov 2026 meeting: log the meeting, KPIs, actions and next sessions (Elite Mentorship enrolment)',
    'for': 'Apply to the Elite Mentorship enrolment.',
    'meeting': {
        'title': 'Follow-up call with Navid: exam plan, branch options and EduPulse',
        'at': datetime(2026, 11, 2, 12, 0), 'duration_min': 48, 'participants': 'Navid (father), Dr. Saravanan, Kalil',
        'agenda': 'Pre-boards and JEE timing; JEE Main Paper 2 as the main aim; plan B and C; EduPulse practice and mock tests; Architecture and Planning college analytics; NID and chemical routes; scheduling.',
        'summary': ('Now: finish the school pre-boards (they end on 18 November) with no JEE study load. From 19 November the main aim is JEE Main Paper 2 (B.Arch), with Paper 1 as the lighter back-up; the January and April sessions both stay open. '
                    'UCEED is dropped: Yusra is not interested in UI/UX, product or transport design, and it would pull her away from the CBSE syllabus. '
                    'Plan B and C will be explored one short session at a time: NID, JEE Paper 2 and chemical engineering first, then a branch presentation (chemical, metallurgy and materials, biotechnology, B.Planning, and the outlook to 2031). '
                    'Practice: EduPulse daily practice and weekly reinforcement, and Paper 2 mock tests, from 19 November. '
                    'Answers to write down for the family: whether DASA, CIWG, JoSAA and Study in India apply to the colleges they like, B.Planning at COEP Pune, and the cost gap between CIWG and open quota. '
                    'Deadlines and messages will go through one group, the EduAakashaA Members Group, and one mentor number.'),
        'notes': ('PRIVATE. Navid pays the first instalment on 3 Nov 2026 (mark it received only after checking). He asked for one WhatsApp group and one number because he mutes groups and missed deadlines. '
                  'His worry: a second stream if architecture does not work, judged from a 2031 view and AI change. Yusra is not interested in programming or civil; chemistry interests her. '
                  'Pre-boards run to 18 Nov (chemistry paper the day after the call), case-study exams in January after the Christmas break, board exams about February to March. '
                  'Tutors (maths, physics, chemistry) are hired by the family; no coaching class and no architecture coaching. '
                  'Claims made in the call and not yet verified: COEP B.Planning CIWG fee about 6 lakh a year and board-mark based entry; Study in India mark slabs lower than the JEE route; NID closing date (father said mid to end November, Kalil read 30 November). '
                  'The transcript is automatic: UC = UCEED, BR = B.Arch, NAT = NATA, JE = JEE, NRI of = NIRF.'),
    },
    # KPIs: (category, name, definition, method, unit, direction, baseline, target, current, frequency, owner, outcome_metric, notes)
    'kpis': [
        ('Preparation', 'EduPulse practice time', 'Minutes of EduPulse practice a week once the pre-boards are over (30 minutes a day, or about two hours a week at least).',
         'EduPulse progress page', 'min per week', 'higher', None, 120, None, 'Weekly', 'Student', False, 'Starts 19 Nov 2026. Set the baseline at the first reading.'),
        ('Preparation', 'Confidence-rated mocks completed (JEE Paper 1 and Paper 2)', 'Full or section mocks finished with a confidence rating on every answer.',
         'EduPulse reports', 'mocks', 'higher', None, 4, None, 'Fortnightly', 'Student', False, 'Suggested pace: one every two weeks from December. Mentors to confirm. Paper 2 first, Paper 1 lighter.'),
        ('Preparation', 'Weekly reinforcement sets completed', 'Share of the reinforcement sets Dr. Saravanan assigns that are finished.',
         'Reinforcement tool', '%', 'higher', None, 100, None, 'Weekly', 'Student', False, ''),
        ('Preparation', 'Topic comfort map posted', 'Physics, chemistry and maths topics listed as easy, medium or hard, posted in the EduAakashaA Members Group.',
         'Posted in the group', 'done', 'milestone', 0, 1, None, 'Once', 'Student', False, 'Due 17 Nov 2026. The study schedule from 19 Nov is built from it.'),
        ('Readiness', 'Plan A / B / C decided', 'Plan A (B.Arch through JEE Paper 2) and two or three back-up disciplines chosen after the branch presentation and the fit check.',
         'Mentor review', 'done', 'milestone', 0, 1, None, 'Review', 'Dr. Saravanan', False, 'Review again after the January JEE result.'),
        ('Readiness', 'Branch exposure sessions done', 'Short sessions on the options: NID, JEE Paper 2, chemical and metallurgy, B.Planning, biotechnology.',
         'Session log', 'sessions', 'higher', 0, 5, None, 'Per session', 'Mentor', False, 'Order agreed: NID first, then JEE Paper 2, then chemical.'),
        ('Readiness', 'Eligibility checklist written (DASA, CIWG, JoSAA, Study in India)', 'A written answer for each college the family likes: which route applies and what it costs.',
         'Mentor document', 'done', 'milestone', 0, 1, None, 'Once', 'Mentor', False, "The parents' open question from the discovery call."),
        ('Readiness', 'Application deadlines verified (NID, NIFT, NATA)', 'Every closing date and correction window checked on the official site and entered in the calendar.',
         'Official sites', 'done', 'milestone', 0, 1, None, 'Weekly', 'Mentor', False, 'NID and NIFT first: the dates heard in the call differ.'),
        ('Mentorship', 'Single messaging channel agreed', 'One group and one mentor number for messages and deadlines.',
         'Parent confirmation', 'done', 'milestone', 0, 1, None, 'Once', 'Mentor', False, ''),
        ('Performance', 'Pre-board marks (Physics, Chemistry, Maths)', 'Average of the three school pre-board papers.',
         'Marksheets', '%', 'higher', 56.8, None, None, 'Per exam', 'Student', True,
         'Baseline is the average of the school test in the onboarding assessment (Physics 61, Chemistry 56.5, Maths 53). Record the pre-board marks after 18 Nov and set a target with the family.'),
        ('Performance', 'JEE Main January score (Paper 2 and Paper 1)', 'Score and percentile in the January session.',
         'NTA score card', 'marks', 'higher', None, None, None, 'Per attempt', 'Student', True, 'Decides the plan for the April session and the second attempt.'),
    ],
    'kpis_archive': [('UCEED', 'Archived after the 2 Nov 2026 meeting: UCEED is dropped.')],
    # actions: (title, instruction, owner, due, priority, recurrence)
    'actions': [
        ('Finish the school pre-boards; no JEE study load until 18 Nov', 'Pre-boards run to 18 November. Keep JEE practice off until then.', 'student', date(2026, 11, 18), 'High', ''),
        ('Post your physics, chemistry and maths topics as easy, medium or hard', 'List the topics you are comfortable with, moderate with, and weak in, and post them in the EduAakashaA Members Group. The schedule from 19 Nov is built from it.',
         'student', date(2026, 11, 17), 'High', ''),
        ('Share the study-holiday dates', 'Tell the mentors which days before 18 Nov Yusra is free, for one short check-in.', 'parent', date(2026, 11, 10), 'Medium', ''),
        ('Prepare the study schedule from 19 Nov to the JEE date', 'Chapters, important JEE topics, Paper 2 drawing and aptitude time, EduPulse practice slots.', 'mentor', date(2026, 11, 19), 'High', ''),
        ('Add JEE Paper 2 (B.Arch) mock tests and the Paper 2 approach guide to EduPulse', 'Mocks with a confidence rating, and a short guide on how to approach each part.', 'mentor', date(2026, 11, 19), 'High', ''),
        ('Start EduPulse daily practice and weekly reinforcement', 'About 30 minutes a day, or about two hours a week. Rate every answer: Guess, Low, Medium or High.', 'student', date(2026, 11, 19), 'High', 'weekly'),
        ('Keep weekly sketching practice for JEE Paper 2 drawing', 'Weekend practice within the time limits from the call. This replaces the earlier UCEED sketch practice.', 'student', None, 'Medium', 'weekly'),
        ('Verify the NID and NIFT closing dates and correction windows on the official sites', 'The father heard mid to end November; the call screen showed 30 November. Confirm and add to the calendar.', 'mentor', date(2026, 11, 6), 'High', ''),
        ('Prepare a short NID session: course list and a sample paper', 'Add NID practice papers to EduPulse. Register only if Yusra is comfortable after the session.', 'mentor', date(2026, 11, 12), 'Medium', ''),
        ('Prepare the branch presentation', 'Chemical, metallurgy and materials, biotechnology, B.Planning, semiconductors, and the outlook to 2031 including AI change.', 'mentor', date(2026, 11, 21), 'Medium', ''),
        ('Run the branch fit tool and choose two or three disciplines', 'After the presentation, use the branch fit tool in the portal.', 'student', date(2026, 11, 30), 'Medium', ''),
        ('Write the B.Planning versus B.Arch comparison', 'Curriculum, entry route, jobs and Maharashtra colleges. The COEP B.Planning syllabus is already with Yusra.', 'mentor', date(2026, 11, 28), 'Medium', ''),
        ('Write the chemical and metallurgy route note', 'UDCT Mumbai, NIT branches, and the Study in India route, with the marks and fees each college asks.', 'mentor', date(2026, 11, 28), 'Medium', ''),
        ('Check the COEP B.Planning CIWG fee and entry criteria', 'Confirm the fee and whether entry is by board marks, from the college and the counselling notices.', 'mentor', date(2026, 11, 28), 'Medium', ''),
        ('Read the Study in India scheme and keep the portal login ready', 'Read the scheme and keep the username and password ready before the admission window.', 'parent', date(2026, 12, 1), 'Medium', ''),
        ('Use one messaging group and one mentor number', 'Move deadlines and updates to the EduAakashaA Members Group and one mentor number, as the father asked.', 'mentor', date(2026, 11, 9), 'High', ''),
        ('Fix the next session (Tuesday evening or a weekend after 18 Nov)', 'Also a quick session in a study holiday if dates allow. Evenings and weekends only.', 'parent', date(2026, 11, 14), 'Medium', ''),
    ],
    # (title substring, reason): matching actions that are not finished are cancelled
    'actions_cancel': [
        ('UCEED', 'Dropped at the 2 Nov 2026 meeting: Yusra is not interested in UI/UX, product or transport design.'),
        ('fixed weekly study slots', 'Replaced by the study schedule that Dr. Saravanan prepares from 19 Nov 2026.'),
    ],
    # (title substring, note added to the mentor feedback)
    'actions_note': [
        ('unit-test marks', 'Add the pre-board marks after 18 Nov so the recovery plan uses both.'),
    ],
    # planned sessions: (title, agenda, deliverable, duration, kind)
    'sessions': [
        ('Pre-board check-in and topic comfort map', 'Hear which physics, chemistry and maths topics feel easy, medium and hard. Keep it short: one study holiday before 18 Nov.\nNo JEE study load until the pre-boards end.', 'Topic comfort list', 30, 'extra'),
        ('Branch options I: NID, JEE Paper 2 and chemical engineering', 'NID course list and a sample paper; how JEE Paper 2 (B.Arch) is built; chemical, metallurgy and the UDCT route.\nAfter the pre-boards. Evening or weekend only.', 'One-page notes on each option', 60, 'extra'),
        ('Branch presentation: scope, jobs and the 2031 view', 'Chemical, metallurgy and materials, biotechnology, B.Planning (COEP), semiconductors (heavy on programming), and the effect of AI.\nThen the portal branch fit tool.', 'Draft Plan A / B / C', 60, 'extra'),
        ('JEE schedule kick-off (from 19 Nov)', 'Walk through the schedule to the JEE date: chapters, important topics, Paper 2 drawing and aptitude, EduPulse daily and weekly reinforcement, confidence rating.', 'Agreed weekly timetable', 45, 'extra'),
        ('Eligibility and payments walk-through: DASA, CIWG, Study in India, COEP and Anna University', "Written answers to the parents' questions: which routes apply to the colleges they like, the cost gap between CIWG and open quota, and what happens after the first year if the branch does not fit.", 'Written eligibility and cost note', 45, 'extra'),
        ('January JEE review and Plan A / B / C check', 'After the January JEE Main score: what to change for April, and whether Plan B or C moves up. Also the board-exam plan.', 'Updated plan', 45, 'extra'),
    ],
    'events': [
        ('School pre-boards end (as reported by the family)', 'Other', date(2026, 11, 18), None, 'The family said the pre-boards end on 18 Nov 2026. Confirm with the school.', 'Family, 2 Nov 2026 call'),
    ],
}

ADDONS = {
    'key': 'yusra-2026-11-02-addons',
    'label': 'Yusra Kazi, 2 Nov 2026 meeting: update session details in an add-on enrolment (B.Arch, NID, UCEED)',
    'for': 'Apply to each add-on enrolment: B.Arch, NID or UCEED.',
    # (programme name contains, session title contains, text appended to the session agenda); sessions that do not exist are skipped
    'session_notes': [
        ('B.Arch', 'Baseline: drawing', "JEE Main Paper 2 (B.Arch) is the main aim; Paper 1 is the lighter back-up. The earlier UCEED sketching is replaced by weekly drawing practice for Paper 2. Do this after the pre-boards (they end on 18 Nov 2026)."),
        ('B.Arch', 'Paper 2A mathematics', "Start from the topic comfort map Yusra posts by 17 Nov 2026; the schedule from 19 Nov follows it. Yusra feels comfortable with the Paper 2 aptitude and maths part, so spend more time on drawing and on keeping Paper 1 ticking over."),
        ('B.Arch', 'Drawing: the Paper 2A', "Weekend sketching practice within the time limits agreed on the call. No weekday load on top of school and tuition. UCEED is dropped, so Part B practice here is for Paper 2 drawing and NATA."),
        ('B.Arch', 'NATA multiple-choice', "NATA and JEE Paper 2 overlap a lot (the father's own view). Confirm NATA dates on the official site; the April session was mentioned."),
        ('B.Arch', 'Application calendar', "Remove UCEED. Add the January and April JEE Main sessions, and verify NATA, NID and NIFT dates on the official sites. The NID closing date was reported as mid to end November."),
        ('B.Arch', 'Mock tests', "From 19 Nov use the EduPulse Paper 2 mocks and rate every answer. Paper 1 mocks stay lighter. Review confidence mistakes with Dr. Saravanan."),
        ('B.Arch', 'Results, ranks and the college list', "Keep Plan B and C open: chemical engineering (UDCT Mumbai), metallurgy and materials, B.Planning (COEP Pune), and NID. Mark every college with the route that applies (DASA, CIWG, JoSAA, Study in India)."),
        ('B.Arch', 'Counselling and admission steps', "Write down for the family which routes apply to the colleges they like, and the cost gap between CIWG and open quota. The Study in India route lets some colleges take lower board marks than the JEE route (check each college)."),
        ('B.Arch', 'Parent briefing', "The family looks ahead to 2031 and the effect of AI on jobs, and wants one or two realistic alternatives to architecture. Bring the branch comparison and the Plan A / B / C draft."),
        ('NID', 'Application, documents and deadlines', "Verify the NID closing date and correction window on the official site first: the family heard mid to end November. Decide whether to register only after the NID session."),
        ('NID', 'Studio test practice', "Add NID practice papers to EduPulse. Yusra enjoys designing presentations and sketching diagrams, but has not tested architecture or design interest in depth."),
        ('NID', 'Orientation', "NID is the first option to look at after the pre-boards, ahead of JEE Paper 2 and chemical engineering. Keep it short and see how she reacts before registering."),
    ],
    # (programme name contains, reason): planned sessions of that add-on are cancelled
    'cancel_programmes': [
        ('UCEED', 'UCEED is dropped (2 Nov 2026 meeting): Yusra is not interested in UI/UX, product or transport design.'),
    ],
}

PACKS = [ELITE, ADDONS]
