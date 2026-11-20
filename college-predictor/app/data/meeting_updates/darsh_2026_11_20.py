"""Meeting update for Darsh: the school and coaching schedules he sent on 19 Nov 2026, the mentors' 20 Nov reply and the 18 Nov 2026 call.

One pack, applied from Admin, Mentorship, on Darsh's Elite Mentorship enrolment (nothing is sent to anyone; running it twice adds nothing twice):
  * calendar: school model exams, pre-boards, practicals, the ALLEN SCORE-I test series, the CBSE Class 12 board exams, JEE Main Session 2 and the next mentor meeting,
  * KPIs for the JEE Main plan and the board exams, actions, one planned weekly check-in,
  * his Smart Study Planner plan (21 Nov 2026 to 9 Apr 2027, built in app/data/darsh_jee_plan.py) and the profile (goals) text.
Sources: Preboard I and Model Exam Schedule 2026-2027 (Delhi Private School Dubai), the ALLEN Overseas SCORE-I schedule image, the family messages up to 20 Nov 2026 and the 18 Nov call.
Dates not confirmed by the school or the board are said so in the calendar notes. Passwords, fees and chat links are not copied here.
"""
from datetime import date, datetime

from app.data import darsh_jee_plan as plan
from app.services import jee_gap

GAP = jee_gap.analyse(plan.RATINGS)
TOP_GAPS = ', '.join('%s (Tier %d, %.1f marks)' % (x['name'].split(' (')[0], x['tier'], x['risk']) for x in GAP['rows'][:5])

SRC_SCHOOL = 'Delhi Private School Dubai: Model Examination XII 2026-27 and Preboard Examination I 2026-27 schedules (sent by the family on 19 Nov 2026)'
SRC_ALLEN = 'ALLEN Overseas IIT-JEE SCORE Test Series, Enthusiast Course 2026-27, SCORE-I (UAE schedule, sent by the family on 19 Nov 2026)'
SRC_CBSE = 'CBSE Class 12 date sheet 2027 as reported by Careers360 on 6 Nov 2026; confirm on cbse.gov.in (Gulf timing and any revision are not confirmed)'

EVENTS = []
for _d, _sub in sorted(plan.SCHOOL_EXAMS.items()):
    _model = _d < date(2026, 12, 20)
    EVENTS.append((f'School {"model exam" if _model else "pre-board"}: {_sub} ({_d.strftime("%d %b %Y")})', 'School exam', _d, None,
                   'Marks matter little to the family ("40% and above is enough"); use the day for the school paper and keep JEE revision light.' + ('' if _model else ' Dates may be changed by the school if a JEE Main slot clashes: ask the school early.'), SRC_SCHOOL))
EVENTS += [
    ('School: Physics pre-board practical', 'School exam', date(2026, 12, 8), None, 'Chemistry and Computer Science pre-board practicals are written as 9/10/26 and 11/10/26 in the family message: ask the school for the exact dates (they look like December dates).', 'Family message, 19 Nov 2026'),
    ('CBSE practical examinations (school window)', 'School exam', date(2027, 1, 11), date(2027, 1, 20), 'External examiner; the school gives each subject its day. Darsh attends only on his practical days.', SRC_SCHOOL),
]
for _i, (_d, (_name, _)) in enumerate(sorted(plan.PART_TESTS.items()), 1):
    EVENTS.append((f'ALLEN {_name}', 'Mock test', _d, None, 'JEE Main part-syllabus test, 5:30 to 8:30 PM GST. Review the paper the next day.', SRC_ALLEN))
for _i, _d in enumerate(plan.FULL_TESTS, 7):
    EVENTS.append((f'ALLEN SCORE full test {_i:02d}', 'Mock test', _d, None, 'Full-syllabus JEE Main pattern test (timing on the schedule: 6:30 PM, 7:30 AM or 1:30 PM GST).', SRC_ALLEN))
for _i, _d in enumerate(plan.PYP_DAYS, 1):
    EVENTS.append((f'ALLEN previous-year paper {_i:02d}', 'Mock test', _d, None, 'Slot 1 (1:30 to 4:30 PM GST) or Slot 2 (9:30 PM to 12:30 AM). Full syllabus.', SRC_ALLEN))
EVENTS += [
    ('CBSE Class 12 board exams 2027 (theory)', 'Board exam', date(2027, 2, 16), date(2027, 4, 9), 'Theory papers 10:30 AM to 1:30 PM for most subjects. Darsh\'s papers are listed below.', SRC_CBSE),
    ('CBSE board: Physics', 'Board exam', date(2027, 2, 16), None, 'First paper of the session, 16 days after the end of JEE Main Session 1 and the day before the NUS application deadline (17 Feb 2027).', SRC_CBSE),
    ('CBSE board: Chemistry', 'Board exam', date(2027, 2, 27), None, '', SRC_CBSE),
    ('CBSE board: English Core', 'Board exam', date(2027, 3, 5), None, 'NTU asks for a minimum of 93% average including English.', SRC_CBSE),
    ('CBSE board: Mathematics', 'Board exam', date(2027, 3, 9), None, '', SRC_CBSE),
    ('CBSE board: Computer Science', 'Board exam', date(2027, 3, 31), None, 'Falls in the expected JEE Main Session 2 week (early April). Check the NTA dates before choosing the Session 2 city and slot.', SRC_CBSE),
    ('JEE Main 2027 Session 2 (expected, NTA to notify)', 'JEE Main', date(2027, 4, 2), None, 'Sources report early April; the exact days are not announced. It overlaps the end of the CBSE window (to 9 Apr).', 'NTA calendar as reported by Vedantu and Careers360, Nov 2026'),
    ('Weekly check-in with mentors (30 to 40 minutes)', 'Other', date(2026, 11, 23), None, 'Monday 23 Nov 2026, 8:00 PM UAE time: JEE plan walk-through, the 11 colleges Darsh shortlisted, boards against JEE.', 'Family message, 19 Nov 2026'),
]

KPIS = [
    ('Preparation', 'Study plan tasks completed (JEE and boards)', 'Tasks ticked done in the Study Planner divided by tasks due so far.', 'Study Planner progress report each Sunday', '%', 'higher', None, 85, None, 'Weekly', 'Student', False,
     'Suggested target. The plan has about 6 hours on a normal day and 4 on a Saturday; edit a task rather than skip it.'),
    ('Preparation', 'JEE study hours per week', 'Minutes done on tasks that are not school exams, divided by 60.', 'Study Planner weekly report', 'hours', 'higher', None, 34, None, 'Weekly', 'Student', False,
     'From the plan: 30 to 38 hours in a normal week, less in school-exam and mock-heavy weeks. Suggested.'),
    ('Preparation', 'ALLEN tests and previous-year papers attempted', 'Of 11 SCORE tests and 10 previous-year papers between 30 Nov 2026 and 17 Jan 2027.', 'Tick each test in the Study Planner', 'of 21', 'higher', 0, 21, None, 'Weekly', 'Student', False,
     'Every paper is reviewed the next day (the plan books 75 minutes for it).'),
    ('Preparation', 'Weak topics: self-rated 0 or 1 (of 69 JEE topics)', 'Topics Darsh rated 0 or 1 in the self-assessment of 20 Nov 2026: Physics 4 (elasticity and fluids, thermal properties, thermodynamics and KTG, waves and sound), Chemistry 4 (states of matter, s-block, p-block, metallurgy and qualitative analysis), Mathematics 3 (complex numbers, statistics, mathematical reasoning).',
     'Darsh re-rates the same three PDFs every month; the mentors check against the error log', 'topics', 'lower', 11, 3, 11, 'Monthly', 'Student', False,
     'The plan starts each of these from the basics, with 30 extra minutes. Target of 3 or fewer by 17 Jan is a suggestion.'),
    ('Preparation', 'JEE readiness from the gap map', 'His 69 topic ratings against what JEE Main needs, weighted by the questions each chapter had in the 19 shifts of 2026 (Tier 1 and 2 need rating 3, Tier 3 needs 2).',
     'Gap map in the Study Planner; re-run after each monthly re-rating', '%', 'higher', GAP['readiness'], 90, GAP['readiness'], 'Monthly', 'Student', False,
     'Baseline from the 20 Nov self-assessment. Target is a suggestion. Physics and Mathematics hold the most marks within reach, so the plan gives them extra time.'),
    ('Preparation', 'Marks within reach per paper from closing gaps (gap map)', 'Questions per paper x 4 x the gap that remains to the level JEE Main needs, summed over topics. A planning estimate, not a score prediction.',
     'Gap map in the Study Planner', 'marks', 'lower', round(GAP['total_risk']), 30, round(GAP['total_risk']), 'Monthly', 'Mentor', False,
     'Baseline is the 20 Nov self-assessment; about %d%% of it sits in the top 5 topics: %s.' % (round(GAP['top5_share']), TOP_GAPS)),
    ('Performance', 'JEE Main mock score (out of 300)', 'Net score in ALLEN SCORE and previous-year papers.', 'Score of each paper', 'marks', 'higher', 100, 120, None, 'Per paper', 'Mentor', True,
     'Baseline is the 80 to 120 range Darsh reported for coaching tests (class top about 200). Target 120 = about 30 correct answers with no negatives, the figure the mentors gave on 18 Nov.'),
    ('Performance', 'Negative marks per mock paper', 'Marks lost to wrong answers in each timed paper.', 'Paper analysis', 'marks', 'lower', 10, 4, None, 'Per paper', 'Student', True,
     'Darsh reported losing 10 to 11 marks in some papers. The rule is: attempt only what you are sure of. Target is a suggestion.'),
    ('Performance', 'Chemistry questions correct per paper (of 25)', 'Correct answers in the Chemistry section.', 'Paper analysis', 'questions', 'higher', None, 15, None, 'Per paper', 'Student', True,
     'Mentor target of 18 Nov: 15 Chemistry, 10 Physics, 5 Mathematics, about 30 in all.'),
    ('Performance', 'Physics questions correct per paper (of 25)', 'Correct answers in the Physics section.', 'Paper analysis', 'questions', 'higher', None, 10, None, 'Per paper', 'Student', True, 'Term 1 topics (mechanics, heat) are the weak area Darsh named.'),
    ('Performance', 'Mathematics questions correct per paper (of 25)', 'Correct answers in the Mathematics section, sure questions only.', 'Paper analysis', 'questions', 'higher', None, 5, None, 'Per paper', 'Student', True, 'Calculus is the weak area; treat Mathematics as basics plus the quick questions.'),
    ('Readiness', 'CBSE Class 12 predicted aggregate', 'Predicted marks given by the school.', 'School predicted marks sheet', '%', 'higher', None, 95, 95, 'Per exam', 'Student', True,
     'Predicted 95% (30 Oct). NTU asks for at least 93% average including English; marks on the pre-boards and boards will replace the prediction. SAT 1430 is on record.'),
    ('Readiness', 'NUS and NTU document upload complete', 'Documents on the 30 Oct list uploaded to the portal: passport, Grade 10 and 11 marksheets, predicted marks, SAT report, certificates.', 'Mentor document check', 'of 7', 'higher', None, 7, None, 'Fortnightly', 'Parent', False,
     'Complete before the NUS window opens on 16 Dec 2026 (deadline 17 Feb 2027).'),
    ('Readiness', 'Admission documents in Google Drive, shared with the mentor and verified', 'Scans of the documents on the NUS, NTU and HKU lists kept in the Drive folder Darsh University Documents (link on this tab), shared with the mentor, who opens each file and checks it.',
     'Mentor opens the folder and counts the files that are complete, legible and match the marksheets', 'of 7', 'higher', 0, 7, 1, 'Fortnightly', 'Mentor', False,
     'On 20 Nov the folder held 1 file: Darsh 11th Marks.pdf. Still to add: passport, Class 10 marksheet, predicted marks sheet, SAT report, certificates and the personal statement.'),
    ('Mentorship', 'Weekly mentor check-ins held', '30 to 40 minute call, as requested on 19 Nov.', 'Session log', 'calls', 'higher', 0, 1, None, 'Weekly', 'Mentor', False, 'One call a week until the JEE Main session, then fortnightly during the boards.'),
]

ACTIONS = [
    ('Add the remaining documents to the Google Drive folder Darsh University Documents',
     'The folder holds the Class 11 marks sheet. Add scans of the passport, Class 10 marksheet, predicted marks sheet, SAT report, certificates and the personal statement, named clearly (for example Passport.pdf). Then share the folder with Dr. Saravanan as Viewer and tick the box on the Readiness KPIs tab.',
     'student', date(2026, 11, 25), 'High', None),
    ('Mentor: open the Google Drive folder, verify each file and record the result',
     'Readiness KPIs tab, Mentor verification. Check that every file opens, is legible and that names and dates match the marksheets. Record Verified or Needs changes with what is missing, before HKU first-round submission (cut-off 25 Nov, noon Hong Kong time).',
     'mentor', date(2026, 11, 26), 'High', None),
    ('Re-rate the weak topics every month on the same three self-assessment PDFs',
     'Take the 11 topics rated 0 or 1 (and any that slipped) and re-rate them honestly after each block of work: 21 Dec, 18 Jan. Send the updated PDFs to Dr. Saravanan privately. A topic only moves up when you can solve JEE Main level questions on it without help.',
     'student', date(2026, 12, 21), 'Medium', None),
    ('Open the new Study Planner plan every morning and tick each task',
     'Today\'s tasks are listed in Member Home, Study Planner. Do the Chemistry block first, then Physics, then Mathematics (only the sure questions). Write each mistake in the error log. If a day is lost, edit the task, do not skip silently.',
     'student', date(2026, 11, 22), 'High', 'weekly'),
    ('Attempt only questions you are sure of in every ALLEN test and previous-year paper',
     'Order: Chemistry, Physics, Mathematics. No guessing (each wrong answer costs 1 mark and about 200 to 300 ranks near the cut-off). After every paper, mark each question: sure and right, sure and wrong, guessed.',
     'student', date(2026, 11, 30), 'High', None),
    ('Mentors: walk Darsh through the plan, now built on his own topic ratings',
     'Meeting on Monday 23 Nov, 8:00 PM UAE time. Check the daily hours, the Saturday and Sunday load and the days that clash with ALLEN tests and school exams. His ratings put 11 of 69 topics at 0 or 1: confirm those come first. Then publish the 30 to 40 day topic schedule.',
     'mentor', date(2026, 11, 23), 'High', None),
    ('Mentors: review the 11 colleges Darsh shortlisted from Study in India and answer his question',
     'List: NIT Warangal, NIT Tiruchirappalli, NIT Surathkal, NIT Calicut, NIT Rourkela, MNIT Jaipur, DTU, IIIT Delhi, VIT Vellore, Manipal, BITS Pilani. Dr. Saravanan\'s advice (20 Nov): Study in India is the last option; do not spend time on it now, revisit in March and April, and concentrate on JEE Main.',
     'mentor', date(2026, 11, 23), 'Medium', None),
    ('Ask the school for the exact dates of the Chemistry and Computer Science pre-board practicals',
     'The family message gives 9/10/26 and 11/10/26, which cannot be future dates. Confirm with the school and send the dates so they can be added to the calendar and the plan.',
     'parent', date(2026, 11, 23), 'Medium', None),
    ('Check each pre-board against the JEE Main admit card as soon as it is out',
     'The Chemistry pre-board (22 Jan) and the Mathematics pre-board (25 Jan) fall inside the JEE Main Session 1 window (20 to 31 Jan, exact days differ between sources). Ask the school for another date for any paper that clashes.',
     'parent', date(2027, 1, 13), 'High', None),
    ('Plan the Physics board paper (16 Feb) against JEE Main Session 1 and the NUS deadline (17 Feb)',
     'Physics is the first board paper, 16 days after JEE Main Session 1 ends and one day before the NUS application deadline. Decide before 20 Jan whether NUS stays on the list, so its application is not pushed into board week.',
     'parent', date(2027, 1, 15), 'High', None),
    ('Upload the NUS and NTU documents to the portal before the NUS window opens',
     'Passport, Grade 10 and 11 marksheets, predicted marks, SAT 1430 report, subject-wise predicted marks and certificates. The mentors will check eligibility and gaps.',
     'parent', date(2026, 12, 15), 'Medium', None),
]

SESSIONS = [
    ('Weekly check-in: JEE plan, boards and shortlist',
     '1. Walk through the study plan from 21 Nov (hours, test days, Saturdays)\n2. Topic ratings from the three PDFs\n3. The 11 colleges Darsh shortlisted (backup only for now)\n4. Chemistry and Computer Science practical dates\n5. Boards against JEE: the Physics paper on 16 Feb and the NUS deadline on 17 Feb',
     'A confirmed plan and the 30 to 40 day topic schedule.', 40, 'follow-up'),
]

GOALS = ('Updated 20 Nov 2026. Darsh (Grade 12 CBSE, Dubai) is preparing for JEE Main 2027 and the CBSE board exams (16 Feb to 9 Apr 2027) with Elite Mentorship. '
         'Routes: JEE Main with DASA and CIWG, IIT Delhi Abu Dhabi (CAET), NTU Singapore (application submitted), NUS Singapore (window 16 Dec 2026 to 17 Feb 2027), Study in India as a backup, HKU on hold. '
         'Profile: CBSE predicted 95%, SAT 1430, JEE coaching tests 80 to 120 out of 300 with heavy negative marking. Self-assessment of 20 Nov (69 topics): 11 rated 0 or 1, namely Physics elasticity and fluids, thermal properties, thermodynamics and KTG, waves and sound; Chemistry states of matter, s-block, p-block, metallurgy and qualitative analysis; Mathematics complex numbers, statistics, mathematical reasoning. Strongest: Chemistry (mole concept, haloalkanes, amines rated 4) and Physics EM waves and semiconductors (4). He rates Mathematics calculus and integrals at 3 but reports few attempts in tests: to be checked in the first mock. '
         'Plan: Chemistry first, then Physics, Mathematics only the sure questions; no guessing; weekly 30 to 40 minute mentor check-in.')

GOALS += (' Gap map (ratings against the JEE Main 2026 chapter Tiers): %d%% ready; biggest gaps: %s. States of matter, s-block and Mathematical reasoning are rated 0 or 1 but had no question in 2026, so they wait until the end.'
          % (GAP['readiness'], TOP_GAPS))

PACKS = [{
    'key': 'darsh-2026-11-20',
    'label': 'Darsh, 20 Nov 2026: school and ALLEN schedules, board exams, KPIs, actions, study plan and profile (Elite Mentorship enrolment)',
    'for': 'Apply to Darsh\'s Elite Mentorship enrolment.',
    'note_tag': 'Update 20 Nov 2026: ',
    'kpis': KPIS,
    'actions': ACTIONS,
    'sessions': SESSIONS,
    'actions_note': [('Tick the Physics, Chemistry', 'Done 20 Nov 2026: Darsh returned all three self-assessments (Physics 22, Chemistry 26, Mathematics 21 topics). The study plan now follows his ratings.')],
    'events': EVENTS,
    'goals': GOALS,
    'assessment': {'ratings': plan.RATINGS, 'note': 'Returned by Darsh on 20 Nov 2026 (three self-assessment PDFs, 69 topics).'},
    'study_plan': {'title': 'Darsh: JEE Main 2027 and CBSE Grade 12 plan (21 Nov 2026 to 9 Apr 2027)', 'exam': 'JEE', 'level': 'average', 'start': plan.START, 'end': plan.END,
                   'exam_date': date(2027, 1, 20), 'hours': 5.0, 'tasks': plan.build},
}]
