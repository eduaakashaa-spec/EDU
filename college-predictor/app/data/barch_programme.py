"""Content for the members' B.Arch and B.Planning mentorship programme page.
The sessions themselves live in app/data/mentorship_addons.py (keys 'barch' and 'bplan') so enrolment, tracking and reports work as for every add-on.
Dates for JEE Main come from NTA's 2027 Information Bulletin (see app/data/jee_paper2.py). NATA 2027 is not announced yet, so its dates are shown only
as the 2026 cycle, labelled as a reference. Nothing here promises a rank, a seat or an admission."""

UPDATED = '1 November 2026'

TRACKS = [
    dict(key='barch', title='B.Arch track', weeks=16, tag='Architecture',
         exams='JEE Main Paper 2A and NATA, with the Architecture Aptitude Test route for IITs explained',
         who='Students who sketch, think in 3D and want to become architects.',
         focus=['Mathematics for Paper 2A', 'Aptitude: visual reasoning, scale, plans and elevations', 'Drawing for the Paper 2A drawing test and NATA', 'One application calendar for every exam you sit', 'Portfolio and first-year studio readiness']),
    dict(key='bplan', title='B.Planning track', weeks=10, tag='Planning',
         exams='JEE Main Paper 2B',
         who='Students drawn to cities, transport, housing, policy and data.',
         focus=['Mathematics for Paper 2B', 'Aptitude: reasoning and awareness of the built environment', 'Planning-based part: social sciences and thinking skills', 'News, maps and data habits', 'Counselling for the institutes that use a Paper 2B rank']),
]
BOTH_NOTE = ('Not sure yet? Start with the B.Arch track. Mathematics and aptitude are shared with Paper 2B, so the first sessions count for both. '
             'Your mentor then helps you choose one paper or both at the application stage.')

# exam map: name, run by, used for, format and what it tests, verify at
EXAMS = [
    ('JEE Main Paper 2A', 'NTA', 'B.Arch seats filled through JoSAA, including the Schools of Planning and Architecture and several NITs',
     'Mathematics (100) and aptitude (200) on the computer; drawing test (100) on paper. 400 marks, 3 hours.', 'jeemain.nta.nic.in'),
    ('JEE Main Paper 2B', 'NTA', 'B.Planning seats at the SPAs and MANIT Bhopal in 2025, through JoSAA',
     'Mathematics (100), aptitude (200) and planning-based questions (100), all on the computer. 400 marks, 3 hours.', 'jeemain.nta.nic.in'),
    ('NATA', 'Council of Architecture', 'B.Arch admission at recognised institutions that accept NATA, directly or through state counselling',
     '2026 pattern: drawing and composition on paper (80 marks), then multiple-choice questions on the computer (120 marks). Up to three attempts. Confirm the 2027 brochure.', 'nata.in'),
    ('JEE Advanced and the Architecture Aptitude Test', 'IIT organising institute', 'B.Arch at IIT Kharagpur, IIT Roorkee and IIT (BHU) Varanasi',
     'Only for students who qualify through JEE Advanced. Not covered by Paper 2.', 'jeeadv.ac.in'),
    ('College and state routes', 'Each college or state authority', 'B.Arch at institutes and states that use their own test, portfolio or counselling rules',
     'Rules differ. Your mentor maps your state and shortlisted colleges, and confirms each rule from the official notice.', 'The college or state notice'),
]
EXAMS_NOTE = 'Design entrances such as UCEED, NID and NIFT are for design degrees, not architecture. They appear as backup options in the Add-on programmes.'

# phases: label, months, what happens, B.Arch session numbers, B.Planning session numbers
PHASES = [
    ('Foundation', 'Weeks 1 to 2', 'Route map, eligibility, baseline in drawing, aptitude and mathematics, and a plan for your week.', (1, 2), (1, 2)),
    ('Build the skills', 'Weeks 3 to 8', 'Mathematics units, aptitude practice, the drawing habit, and the third part of your paper.', (3, 4, 5, 6, 7), (3, 4, 5, 6)),
    ('Test and apply', 'Weeks 9 to 12', 'Application calendar, full mocks, and the debrief after your first attempt.', (8, 9, 10), (7, 8)),
    ('Decide', 'Weeks 13 to 16', 'Results, college list, counselling steps, portfolio and the family decision.', (11, 12, 13, 14), (9, 10)),
]

# dated milestones. Official = from NTA's 2027 bulletin; reference = 2026 cycle of another body, not a promise for 2027
MILESTONES = [
    ('Official', '22 Nov 2026', 'JEE Main Session 1: last day to apply (11:50 pm IST)'),
    ('Official', '20 to 28 Jan 2027', 'JEE Main Session 1 exam days. Your Paper 2 day and shift are on the admit card.'),
    ('Official', '5 Jan to 3 Feb 2027', 'JEE Main Session 2: application window'),
    ('Official', '2 to 7 Apr 2027', 'JEE Main Session 2 exam days'),
    ('Reference', 'Mar to Jun 2026 cycle', 'NATA 2026: registration opened 9 March, Phase 1 on Fridays and Saturdays from 4 April to 13 June, Phase 2 on 7 and 8 August. The 2027 brochure was not out on 14 October 2026.'),
    ('Check', 'Per college', 'Direct college applications and state counselling dates are set by each authority. Your mentor adds them to your calendar.'),
]

RHYTHM = [
    ('Every week', 'One 60-minute mentor session with a deliverable, plus a short check-in on your actions.'),
    ('Every day', 'A 20-minute sketch (B.Arch) or news-and-map reading (B.Planning), and a small set of aptitude questions.'),
    ('Every month', 'A timed mock, an error review, and a progress report your parent can read in the portal.'),
    ('At each exam', 'A debrief within a week: what cost marks, and what to change before the next attempt.'),
]
TRACKED = [
    ('Practice', 'Sketches per week, aptitude sets done, mathematics problems done'),
    ('Accuracy', 'Aptitude accuracy, mathematics mock percentage, silly-mistake rate'),
    ('Drawing', 'Mentor review of one sketch a week against a simple five-point scale'),
    ('Readiness', 'Documents ready, applications submitted, college list complete'),
]
DELIVERABLES = ['A sketchbook with weekly reviewed pages', 'An error log that shows your repeat mistakes', 'A dated application calendar for every exam', 'A mock-test trend across the programme', 'A reach, match and safe college matrix', 'A portfolio ready for college interviews and studio admission']
KIT = ['Geometry box, pencils, erasers, and colour pencils or crayons (water colours are not allowed on the Paper 2A drawing sheet)', 'A4 drawing sheets and a sketchbook', 'A device with a stable connection for the mock tests']

PARENT_ROLE = [
    'Protect a daily 20-minute practice slot.',
    'Read the monthly report and ask your child what they learned, not only what they scored.',
    'Keep the documents ready: school certificates, ID, photo and signature files.',
    'Join the family briefing sessions at the start and before the final decision.',
]
NOT_PROMISED = ['A rank, a score, a seat or an admission', 'That an exam pattern, fee or date will stay unchanged: each session sends you to the official notice for the current year', 'A replacement for school or board preparation']

FAQ = [
    ('Is this the same as buying coaching?', 'No. It is mentoring: a weekly session with a mentor, a plan, deliverables, reviews and reports. Your child still practises daily. We help you choose what to practise and read the results honestly.'),
    ('Do we need NATA if we take JEE Paper 2A?', 'It depends on the colleges you shortlist. Some admit on a Paper 2 rank, some on NATA, some accept either, and rules differ by state. The B.Arch track maps this for your list, then confirms it from each official notice.'),
    ('Can my child take both papers?', 'Yes. The JEE Main form allows Paper 2A, Paper 2B or both, with a longer sitting and a higher fee. The programme helps you decide at the application stage.'),
    ('Who can enrol?', 'Class 11 and 12 students and drop-year students who are EduAakashaA members. The mentorship portal that carries sessions and reports is part of Elite membership; send a request and our team will confirm the plan for you.'),
    ('How is progress shown to parents?', 'In the Mentorship Portal: sessions, actions, the tracked measures above, and a monthly report.'),
    ('What if we are late for the first JEE session?', 'Session 2 applications open on 5 January 2027. The plan then moves the mock and debrief steps to fit a single attempt.'),
]
