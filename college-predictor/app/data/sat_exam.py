"""Content for the public page /sat-exam-guidelines: the Digital SAT in one place (dates, fees, registration, ID, test day, format, content, scoring, preparation).

Every fact below was read from a College Board page on the date in CHECKED; the page for each group is listed in SOURCES. Where College Board's pages do not settle something (for example
how many practice tests Bluebook holds today, or which Indian cities have a centre for a given date) the page says so and points the reader to the account or app where the answer is live.
Dates and fees change: the page tells readers to confirm on the College Board website before paying.
"""
import sys
from datetime import date

from app.services import sat, sat_gen

CHECKED = '5 November 2026'
UPDATED = CHECKED

# test_date, regular deadline, late deadline, score release (student), all from satsuite.collegeboard.org/sat/dates-deadlines and /scores/score-release-dates
DATES = [
    (date(2026, 11, 7), date(2026, 10, 23), date(2026, 10, 27), date(2026, 11, 20)),
    (date(2026, 12, 5), date(2026, 11, 20), date(2026, 11, 24), date(2026, 12, 18)),
    (date(2027, 3, 6), date(2027, 2, 19), date(2027, 2, 23), date(2027, 3, 19)),
    (date(2027, 5, 1), date(2027, 4, 16), date(2027, 4, 20), date(2027, 5, 14)),
    (date(2027, 6, 5), date(2027, 5, 21), date(2027, 5, 25), date(2027, 6, 21)),
]

SECTIONS = [
    ('Reading and Writing', 'Module 1 and Module 2', '27 each (54)', '32 each (64)', 'Four-option multiple choice. One short passage (25 to 150 words) for each question.'),
    ('Break', '', '', '10', 'Between Reading and Writing and Math.'),
    ('Math', 'Module 1 and Module 2', '22 each (44)', '35 each (70)', 'About 75% four-option multiple choice, the rest student-produced response (you type the answer). Calculator allowed throughout.'),
]

RW_DOMAINS = [
    ('Information and Ideas', '26%', '12 to 14', 'Central ideas and details; command of evidence (textual and quantitative); inferences.'),
    ('Craft and Structure', '28%', '13 to 15', 'Words in context; text structure and purpose; cross-text connections.'),
    ('Expression of Ideas', '20%', '8 to 12', 'Rhetorical synthesis; transitions.'),
    ('Standard English Conventions', '26%', '11 to 15', 'Boundaries; form, structure and sense.'),
]
MATH_DOMAINS = [
    ('Algebra', '35%', '13 to 15', 'Linear equations in one and two variables, linear functions, systems of two linear equations, linear inequalities.'),
    ('Advanced Math', '35%', '13 to 15', 'Equivalent expressions; nonlinear equations and systems; nonlinear functions.'),
    ('Problem-Solving and Data Analysis', '15%', '5 to 7', 'Ratios, rates and units; percentages; one- and two-variable data; probability; inference and margin of error; evaluating statistical claims.'),
    ('Geometry and Trigonometry', '15%', '5 to 7', 'Area and volume; lines, angles and triangles; right triangles and trigonometry; circles.'),
]

HOW_IT_WORKS = [
    ('Digital, in Bluebook', 'You take the SAT on a laptop or tablet in College Board\'s Bluebook app, at a test centre. You cannot test on a phone.'),
    ('Two adaptive stages per section', 'Each section has two modules. How you do on the first decides whether the second is easier or harder. Within a module you may move between questions; you cannot go back to an earlier module, or back to Reading and Writing from Math.'),
    ('Some questions are unscored', 'Each module has 2 pretest questions that do not count. You cannot tell which they are, so treat every question as scored.'),
    ('No penalty for wrong answers', 'College Board advises answering every question: for most students it is better to guess than to leave a question blank.'),
    ('Built-in tools', 'Mark for review, a countdown timer you can hide until five minutes remain, an option eliminator, a line reader, highlights and notes (Reading and Writing only) and a built-in Desmos calculator in Math. A formula reference sheet is available in Math.'),
    ('Calculator', 'Allowed for all of Math. Bluebook has a calculator built in, so bringing your own is optional (it cannot be shared, and saved formulas must be cleared).'),
]

SCORING = [
    ('Total 400 to 1600', 'The sum of two section scores, Reading and Writing and Math, each 200 to 800, reported in 10-point steps.'),
    ('Not a simple count of right answers', 'Scores reflect which questions you got right, how hard they were and the likelihood that a right answer was a guess, so two students with the same number right can score differently.'),
    ('Percentiles', 'The score report shows an All Tester Percentile (the past three cohorts who took the SAT in 12th grade anywhere in the world) and a score range that shows how much your score might vary on another day.'),
    ('Benchmarks', 'College Board\'s College and Career Readiness Benchmarks for the SAT are 480 for Reading and Writing and 530 for Math.'),
    ('Domain detail', 'The report also shows the approximate number of questions and the share of each section for the eight content domains.'),
    ('When scores arrive', 'Most weekend scores are released two to four weeks after test day, through your College Board student account.'),
]

# (item, amount, note), amounts as printed on the College Board fee pages, which show the $ symbol.
FEES = [
    ('Registration fee', '$68', 'Every test taker.'),
    ('International registration fee', '$43', 'Added to the $68 when you test outside the U.S. and U.S. territories, which includes India.'),
    ('Late registration', '$38', 'Registering after the regular deadline and before the late deadline.'),
    ('Change test centre', '$34', 'Changes the centre only. To change the date you cancel and register again.'),
    ('Cancel registration', '$34', 'By the change deadline. A late cancellation, up to Thursday 11:59 p.m. ET before test day, is $44.'),
    ('Test centre fee', '$24', 'Charged only at a few listed locations (Hong Kong SAR, Macau SAR, Singapore, South Korea and Taiwan on the current page). India is not on that list.'),
    ('Waitlist', '$0', 'You are placed into an open seat within your chosen radius if one opens.'),
    ('Additional score reports', '$15 each', 'The first four are free if ordered within nine days after test day.'),
    ('Rush, archived scores, scores by phone', '$31, $35, $15', 'Rush reports are $31 and archived scores $35, each plus report fees; scores by phone are $15 a call.'),
    ('Score verification', '$55', 'Customer Service handles it.'),
]

REGISTER_STEPS = [
    ('Create or sign in to your College Board student account', 'Registration is on the My SAT dashboard. Have a photo and a payment method ready.'),
    ('Choose the date and the test centre', 'You search for a centre and pick one when you register. Dates and seats are shown in your account for your country.'),
    ('Upload an acceptable photo', 'You can update the photo until 5 days before your test.'),
    ('Pay and, if you wish, choose free score recipients', 'You can send scores to up to four organisations free of charge, chosen when you register or before the test, and changed up to nine days after.'),
    ('Set up Bluebook and print your admission ticket', 'After exam setup the ticket is available in Bluebook, starting 5 days before the test. A printed ticket is preferred.'),
]

ID_RULES = [
    'The ID must be an original, physical, unexpired photo ID. Photocopies, screenshots and digital IDs are not accepted.',
    'The full legal name on it must match your admission ticket exactly (middle names and initials are optional). If they differ you may be turned away. For a name change contact College Board Customer Service at least 30 days before the test.',
    'Testing outside your home country: a valid passport is generally required.',
    'India: a passport or a valid Aadhaar PVC card showing your name and photo. An Aadhaar letter is accepted only as the hard copy issued by the Government of India in its original form.',
    'Not accepted: birth certificates, credit or debit cards, employee IDs and temporary IDs. Students 21 or over may use only government-issued photo ID.',
]

TEST_DAY = [
    ('Bring', 'A fully charged laptop or tablet with Bluebook installed and exam setup done; your admission ticket; your physical photo ID; pencils or pens; your College Board username and password. Scratch paper is provided.'),
    ('Arrive', 'Centres open at 7:45 a.m. and doors close at 8 a.m. unless your ticket says otherwise; aim for 15 minutes before the start for check-in. Nobody is admitted after testing has started.'),
    ('Device', 'Windows or Mac laptops, iPads and school-managed Chromebooks, with a battery of at least 3 hours; laptop screens of at least 10 inches and tablets of at least 8. External keyboards are allowed with tablets only. If you need to borrow a device, ask at least 30 days before the test and arrive 30 minutes early.'),
    ('Not allowed', 'Phones, smartwatches, smart glasses, fitness trackers and headphones or earbuds (even switched off), other apps on the testing device, screenshots, copying or recording questions, and AI tools during the test or breaks.'),
    ('If your connection drops', 'Your answers are saved on the device. If you are offline when time ends you must reconnect and submit by 11:59 p.m. local time the next day.'),
    ('Sundays', 'Sunday testing is only for students who cannot test on Saturdays for religious reasons, and it is not offered in India.'),
]

ACCOMMODATIONS = [
    'Approval from College Board\'s Services for Students with Disabilities (SSD) is needed before you register with accommodations. It can take up to seven weeks, and a resubmission can add another seven.',
    'Request deadlines on the current page: 16 October 2026 for the 5 December test, 15 January 2027 for 6 March, 12 March 2027 for 1 May and 16 April 2027 for 5 June.',
    'Apply through your school\'s SSD coordinator (with a parent or guardian\'s consent form) or on your own with the Student Eligibility Form and documentation. An IEP or 504 plan does not by itself give accommodations.',
    'Approved students receive an eligibility letter with a code to enter when registering. Accommodations cannot be added or waived on test day.',
]

PREPARE = [
    ('Take the official practice tests in Bluebook', 'Bluebook offers free full-length practice tests and a short Digital Test Preview. Practice-test scores are saved only if you are signed in to your College Board account. College Board\'s BigFuture page says there are 7 free full-length practice tests; open the Bluebook app to see what is available today.'),
    ('Use Official SAT Prep on Khan Academy', 'Free lessons and quizzes, and the Student Question Bank of real SAT and PSAT questions, are linked from College Board\'s practice page.'),
    ('Learn the eight domains, not tricks', 'Questions are built from the published content domains above. Find your weakest domain from a practice test and drill it, then return to a full test.'),
    ('Practise the Math tools', 'Learn the Desmos calculator in Bluebook before test day and practise typing student-produced responses (a number, decimal or fraction).'),
    ('Train timing', 'On average there are about 1.19 minutes per Reading and Writing question and 1.59 minutes per Math question. Use mark for review and return before the module ends.'),
    ('Review every miss', 'Write down why you missed each question: content gap, misread, or timing. EduPulse-SAT turns misses into review cards that return on a schedule.'),
]

FAQ = [
    ('Is the SAT adaptive?', 'Yes. Each section has two modules; your performance on the first decides whether the second is easier or harder. EduAakashaA\'s own practice papers are not adaptive, so use the official Bluebook practice tests to feel the real thing.'),
    ('Is there negative marking?', 'No. College Board says to answer every question; it states that the way a score is worked out is not a guessing penalty.'),
    ('How long is the SAT?', '2 hours 14 minutes of testing: Reading and Writing 64 minutes (54 questions), a 10-minute break, then Math 70 minutes (44 questions). 98 questions in all.'),
    ('Can I use a calculator?', 'Yes, on the whole Math section. A Desmos calculator is built into Bluebook; you may also bring an approved calculator.'),
    ('What is the total score?', '400 to 1600, the sum of two section scores of 200 to 800 each.'),
    ('How many times can I take it?', 'This page does not give a limit because the College Board pages we checked do not state one. Each sitting needs its own registration and fees. Check the College Board website for current policy, and the requirements of each university you apply to.'),
    ('Which scores do universities see?', 'Score Choice lets you pick which test dates to send, but some colleges require all scores, and it does not apply to the free score sends you choose at registration. Check each university\'s policy.'),
    ('Is the SAT offered in India?', 'Yes. The College Board dates page applies to both US and international students and does not list India separately. Which centres have seats on a date is shown in your account when you search; we cannot list them here.'),
    ('When is the next test I can register for?', 'The 5 December 2026 test: regular registration closes 20 November and late registration 24 November (11:59 p.m. U.S. Eastern time). The 7 November 2026 test has closed.'),
    ('Do these EduAakashaA tests give an official SAT score?', 'No. They are original practice questions without adaptive modules; we show questions right and percent right per section and domain, not a College Board scaled score.'),
]

# (group, page) used as the "where this came from" list. Every page was read on CHECKED.
SOURCES = [
    ('Test structure, timing and scoring', 'https://satsuite.collegeboard.org/sat/whats-on-the-test/structure'),
    ('Assessment Framework for the Digital SAT Suite', 'https://satsuite.collegeboard.org/media/pdf/assessment-framework-for-digital-sat-suite.pdf'),
    ('Understanding SAT scores', 'https://satsuite.collegeboard.org/media/pdf/sat-sd-understanding-scores.pdf'),
    ('Content domains', 'https://satsuite.collegeboard.org/practice/content-domains'),
    ('Dates and deadlines', 'https://satsuite.collegeboard.org/sat/dates-deadlines'),
    ('Score release dates', 'https://satsuite.collegeboard.org/scores/score-release-dates'),
    ('Test fees', 'https://satsuite.collegeboard.org/sat/registration/fees-refunds/test-fees'),
    ('International testing fees', 'https://satsuite.collegeboard.org/sat/registration/international-testing/fees'),
    ('Registration', 'https://satsuite.collegeboard.org/sat/registration'),
    ('ID requirements', 'https://satsuite.collegeboard.org/sat/what-to-bring-do/id-requirements'),
    ('What to bring and what to expect', 'https://satsuite.collegeboard.org/sat/what-to-bring-do/what-to-bring'),
    ('Testing rules', 'https://satsuite.collegeboard.org/sat/testing-rules'),
    ('Bluebook device requirements', 'https://bluebook.collegeboard.org/technology/devices/requirements/overview'),
    ('Accommodations (SSD)', 'https://accommodations.collegeboard.org/request-accommodations/dates-deadlines'),
    ('Practice', 'https://bluebook.collegeboard.org/students/practice'),
]


def _status(row, today):
    d, reg, late, _ = row
    if today > d:
        return 'Test day passed', 'past'
    if today <= reg:
        return 'Registration open', 'open'
    if today <= late:
        return 'Late registration only', 'late'
    return 'Registration closed', 'closed'


def dates(today=None):
    today = today or date.today()
    out = []
    for row in DATES:
        s, k = _status(row, today)
        out.append({'test': row[0], 'regular': row[1], 'late': row[2], 'scores': row[3], 'status': s, 'kind': k})
    return out


def samples():
    """Eight free sample questions: four Reading and Writing from the bank (one per domain) and four Math from the generator (fixed seeds so the page is stable)."""
    out = []
    bank = sat.bank()
    for dom in sat.RW_DOMAINS:
        q = next(x for x in bank if x['domain'] == dom)
        out.append(q)
    for fam, seed in (('lin1', 11), ('pct', 3), ('pyth', 5), ('quad', 8)):
        q = sat_gen.build(fam, seed)
        while q['kind'] != 'mcq':
            seed += 1
            q = sat_gen.build(fam, seed)
        out.append(q)
    return [{'sec': 'Reading and Writing' if q['sec'] == 'RW' else 'Math', 'domain': q['domain'], 'passage': q.get('passage', ''), 'q': q['stem'], 'opts': q['opts'], 'ans': q['ans'], 'why': q['why']}
            for q in out if q.get('opts')]


def context():
    return {'d': sys.modules[__name__], 'dates': dates(), 'samples': samples(), 'st': sat.stats()}

