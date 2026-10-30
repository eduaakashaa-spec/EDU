"""NUS, NTU and HKU undergraduate engineering admission, 2027 intake, for an Indian-board (CBSE) applicant.

Source: the EduAakashaA report "Admission Matrix 2027: NUS, NTU, HKU" prepared 30 Oct 2026 (AI-assisted research from each university's own pages and counsellor sites).
Every date below carries its tag from the report: OFFICIAL (the university's own page) or REPORTED (counsellor sites, to be confirmed with the university). Only OFFICIAL
dates get a "verified" stamp. Dates, fees and rules change every cycle, so re-check each item before relying on it; nothing here is a guarantee of admission.

Applied to one student's mentorship record by services/intl_pack.py (Admin -> Mentorship -> the student's row -> "Add NUS, NTU and HKU admission pack").
"""
from datetime import date

PACK_KEY = 'sg-hk-2027'
PACK_TITLE = 'NUS, NTU and HKU admission pack (2027 intake)'
CHECKED_ON = date(2026, 10, 30)
REPORT = 'EduAakashaA Admission Matrix 2027 report, 30 Oct 2026'

NUS_SRC = 'NUS: nus.edu.sg/oam/admissions (international qualifications, Indian Standard 12)'
NTU_SRC = 'NTU: ntu.edu.sg/admissions (India Standard 12 page)'
HKU_SRC = 'HKU: admissions.hku.hk/India; first-round date reported by counsellor sites (upGrad, AECC Pinnacle, Nbyula), not yet confirmed by HKU'

# ---- the exam / admission catalogue entries the student follows (shared catalogue; one per university) ----------------------------------------------------------------
EXAMS = [
    {'key': 'hku', 'name': 'HKU undergraduate admission, first round (2027 entry)', 'category': 'Admission deadline', 'stream': 'B.Tech/B.E.',
     'starts_on': date(2026, 9, 23), 'ends_on': date(2026, 11, 25), 'status': 'Expected', 'verified_on': None,
     'window_note': 'Opened 23 Sep 2026. First round closes noon Hong Kong time, 25 Nov 2026 (REPORTED: confirm with HKU in writing). Later applications are reviewed on a rolling basis.',
     'source': HKU_SRC,
     'notes': ('International / Non-JUPAS Admissions Scheme. Application fee HK$780 (about US$100), non-refundable (OFFICIAL). Offers from December 2026; accept within 3 to 4 weeks and pay a non-refundable deposit (OFFICIAL). '
               'Interview, personal statement and references count; interviews ran Nov to Jan last cycle (OFFICIAL). Reported lower boundary 90% in the best five subjects, IELTS 6.5 / TOEFL iBT 93 or 90% in Class 12 English (REPORTED). '
               'The HKU cut-off runs on Hong Kong time: submit days earlier, not on the day. HKU\'s own India page still showed last cycle\'s dates on 30 Oct 2026.')},
    {'key': 'nus', 'name': 'NUS undergraduate admission, international qualifications (2027 intake)', 'category': 'Admission deadline', 'stream': 'B.Tech/B.E.',
     'starts_on': date(2026, 12, 16), 'ends_on': date(2027, 2, 17), 'status': 'Confirmed', 'verified_on': CHECKED_ON,
     'window_note': 'Window 16 Dec 2026 to 17 Feb 2027 (OFFICIAL). Outcome online by July 2027 for most international applicants.',
     'source': NUS_SRC,
     'notes': ('Route: Qualifications route for Indian Standard 12 (CBSE, ISC) via the NUS applicant portal (OFFICIAL). No published minimum percentage; counsellors cite 93% or more for engineering (REPORTED). '
               'SAT/ACT and JEE not required; English proof not required for CBSE (OFFICIAL). Engineering needs Mathematics; Computer Engineering also needs Physics or Chemistry (prerequisites PDF dated April 2024, OFFICIAL). '
               'Update final CBSE results in the portal within 3 days of release; this applies even to Middle East applicants whose exams were cancelled (OFFICIAL). Application fee about S$25 (REPORTED). '
               'Fees AY2026/27: S$21,400 a year with the MOE Tuition Grant and a 3-year Singapore work bond, S$39,700 without (REPORTED); 2027/28 fees not found.')},
    {'key': 'ntu', 'name': 'NTU undergraduate admission, India Standard 12 (2027 intake)', 'category': 'Admission deadline', 'stream': 'B.Tech/B.E.',
     'starts_on': date(2026, 10, 15), 'ends_on': date(2027, 3, 19), 'status': 'Confirmed', 'verified_on': CHECKED_ON,
     'window_note': 'Window 15 Oct 2026 to 19 Mar 2027 depending on the qualification (OFFICIAL). Confirm the exact close for the applicant\'s qualification on the India Standard 12 page.',
     'source': NTU_SRC,
     'notes': ('Dedicated India Standard 12 form, completed in one session (no save and return); the wrong form can void the application (OFFICIAL). Minimum: average of 93% across all Standard 12 subjects including English (OFFICIAL). '
               'Offers from March on actual results only; no provisional offers (OFFICIAL). Upload the result slip within 3 days of release, otherwise the application is incomplete and not processed (OFFICIAL). '
               'JEE Main not required; a strong JEE Advanced rank is viewed favourably (OFFICIAL). Results released after 1 April rule out the Renaissance Engineering Programme and LKCMedicine (OFFICIAL). '
               'Subject rules are programme by programme in NTU\'s minimum subject requirements; Physics matters. Fees AY2026/27: about S$21,400 with grant and a 3-year work bond, S$36,350 to S$40,600 without (REPORTED).')},
]

# ---- single-day dates on the student's calendar (targets are EduAakashaA's own, set earlier than the official close) ----------------------------------------------------------
EVENTS = [
    ('Shortlist programmes, scan passport and marksheets, check prerequisites (NUS, NTU, HKU)', 'Documents', date(2026, 11, 15), None, 'Phase 1, Prepare: now to 15 Nov.', REPORT, None),
    ('HKU: target submission for the first round (3 days before the cut-off)', 'Admission deadline', date(2026, 11, 22), None, 'Our own target, set earlier than the close because the cut-off runs on Hong Kong time.', REPORT, None),
    ('HKU: first-round cut-off, noon Hong Kong time (reported, confirm with HKU)', 'Admission deadline', date(2026, 11, 25), None, 'REPORTED by counsellor sites; HKU\'s India page still showed last cycle\'s dates on 30 Oct 2026. Get the 2027 date confirmed in writing.', HKU_SRC, None),
    ('HKU: interviews if invited; offers from December (accept within 3 to 4 weeks)', 'Admission deadline', date(2026, 11, 1), date(2027, 1, 31), 'Interviews ran Nov to Jan last cycle; offers from December 2026 on a rolling basis (OFFICIAL).', 'HKU: admissions.hku.hk/India', CHECKED_ON),
    ('NUS: application window opens', 'Admission deadline', date(2026, 12, 16), None, 'Window 16 Dec 2026 to 17 Feb 2027 (OFFICIAL).', NUS_SRC, CHECKED_ON),
    ('NUS and NTU: target to submit both forms (before the board exams)', 'Admission deadline', date(2027, 1, 31), None, 'Our own target. The windows overlap the CBSE Class 12 exams, so the forms should be finished in January and applications parked in Feb to Mar.', REPORT, None),
    ('NUS: application window closes', 'Admission deadline', date(2027, 2, 17), None, 'OFFICIAL close of the 2027 intake window.', NUS_SRC, CHECKED_ON),
    ('NTU: application window closes (confirm Darsh\'s date)', 'Admission deadline', date(2027, 3, 19), None, 'The close varies by qualification. Confirm the exact date for Darsh\'s qualification on NTU\'s India Standard 12 page.', NTU_SRC, CHECKED_ON),
    ('Offers and decisions: NTU from March, NUS outcome by July, HKU compare offers; start the student visa (8 to 10 weeks)', 'Admission deadline', date(2027, 3, 1), date(2027, 7, 31),
     'NTU offers from March on actual results (OFFICIAL); NUS outcome online by July (OFFICIAL); HKU visa assessment allow 4 to 6 weeks, student visa 8 to 10 weeks per last published guidance (OFFICIAL).', REPORT, None),
]

# ---- KPIs for the student's record: (category, name, definition, method, unit, direction, baseline, target, current, frequency, owner, outcome_metric, notes) ----------------------------
KPIS = [
    ('Readiness', 'University applications submitted (of 3: HKU, NUS, NTU)', 'Each of the three applications submitted and confirmed by the university.', 'Count the applications with a confirmation email or portal status.',
     'of 3', 'higher', 0, 3, 0, 'Monthly', 'Student', False, 'HKU target 22 Nov, NUS and NTU target 31 Jan.'),
    ('Readiness', 'HKU first-round application submitted by 22 Nov', '1 when the HKU application is submitted by the target date (cut-off 25 Nov noon HKT, reported).', 'Portal confirmation.',
     'done', 'higher', 0, 1, 0, 'Weekly', 'Student', False, 'Confirm the 2027 first-round date with HKU in writing first.'),
    ('Readiness', 'NUS and NTU forms submitted by 31 Jan (of 2)', 'Both forms finished before the board exams. NUS closes 17 Feb, NTU on 19 Mar (confirm).', 'Portal confirmation for each.',
     'of 2', 'higher', 0, 2, 0, 'Monthly', 'Student', False, 'NUS opens 16 Dec; NTU has been open since 15 Oct.'),
    ('Preparation', 'Programme prerequisites checked (of 3 universities)', 'The chosen engineering programme at each university read against Darsh\'s actual Class 11 and 12 subjects.', 'Mentor review of the shortlist against subjects.',
     'of 3', 'higher', 0, 3, 0, 'Weekly', 'Mentor', False, 'NUS: Maths; Physics or Chemistry for Computer Engineering. NTU: programme by programme. HKU: Maths plus one of Biology, Chemistry or Physics.'),
    ('Preparation', 'Documents and checklist items ready', 'Required items ticked across the NUS, NTU and HKU checklists (Calendar tab).', 'Counted from the checklists.',
     'items', 'higher', 0, 24, 0, 'Weekly', 'Student and parents', False, 'Passport and marksheets by 8 Nov; budget and work-bond decision by 15 Nov.'),
    ('Preparation', 'HKU personal statement and referee ready', '1 when the personal statement is final and a referee or nominee is chosen.', 'Draft reviewed by the mentor.',
     'done', 'higher', 0, 1, 0, 'Weekly', 'Student', False, 'Final by 18 Nov, mentor review by 20 Nov.'),
    ('Readiness', 'Budget ceiling and Tuition Grant / work-bond decision made', '1 when the family has agreed a budget and decided on the Singapore grant with its 3-year work bond.', 'Recorded in the parent briefing.',
     'done', 'higher', 0, 1, 0, 'Monthly', 'Parents', False, 'By 15 Nov. Grant saves about S$18,300 a year at NUS and S$14,950 to S$19,200 at NTU (AY2026/27, reported); HKU has no bond found.'),
    ('Performance', 'Class 12 average including English (NTU minimum 93%)', 'Latest Class 12 average across all subjects including English. NTU states 93% as the minimum; HKU reported 90% in the best five; NUS publishes none (93%+ is a counsellor estimate).',
     'Enter the latest school or mock result.', '%', 'higher', None, 93, None, 'Monthly', 'Student', True,
     'Darsh\'s marks were not available when this was set up: enter the latest value. Meeting a minimum does not guarantee a place.'),
    ('Readiness', 'Results uploaded or keyed in within 3 days of release (of 3)', 'On results day the 3-day clock starts: NUS portal update, NTU result slip upload, HKU results keyed into the system.', 'Confirm each upload was accepted.',
     'of 3', 'higher', 0, 3, 0, 'On results', 'Student', False, 'Phone and email on in results week; share results with parents and mentor within the hour.'),
]

# ---- actions: (title, instruction, owner, due date, priority) ---------------------------------------------------------------------------------------------------------------
ACTIONS = [
    ('Mentor: get HKU 2027 dates and Darsh\'s NTU window confirmed in writing', 'Write to HKU for the 2027 first-round date and to NTU for the close date for Darsh\'s qualification. File the replies.', 'mentor', date(2026, 11, 2), 'High'),
    ('Pick the engineering programme at each university and read its prerequisites', 'One programme each at NUS, NTU and HKU. Read the subject prerequisites against Darsh\'s Class 11 and 12 subjects.', 'student', date(2026, 11, 6), 'High'),
    ('Gather passport and marksheets; make names and dates match across all documents', 'Passport valid and scanned; Class 10 and 11 marksheets scanned; CBSE admit card details; a folder and the portal logins for each university.', 'parent', date(2026, 11, 8), 'High'),
    ('Mentor: check the shortlist against actual subjects and predicted marks', 'Compare each chosen programme with Darsh\'s real subjects and predicted marks. Darsh\'s marks and branch interest were not known when the report was written.', 'mentor', date(2026, 11, 12), 'High'),
    ('Agree the budget ceiling and the Tuition Grant / work-bond decision', 'Tuition only is in the report; living costs, housing, visa and flights are extra. The grant carries a 3-year Singapore work bond.', 'parent', date(2026, 11, 15), 'High'),
    ('HKU personal statement final: draft to mentor', 'Final personal statement, referee ready, and a nominee chosen if a teacher or counsellor will enter results.', 'student', date(2026, 11, 18), 'High'),
    ('Mentor: review the HKU application before submission', 'Check programme choice, results keyed in, statement and referee.', 'mentor', date(2026, 11, 20), 'High'),
    ('Have the HK$780 application fee and card ready', 'HK$780 (about US$100), non-refundable. Keep the card ready for the NUS and NTU fees as well.', 'parent', date(2026, 11, 22), 'Medium'),
    ('Submit the HKU first-round application (target 22 Nov; cut-off noon HKT 25 Nov, reported)', 'Submit days before the cut-off; it runs on Hong Kong time. Keep the confirmation.', 'student', date(2026, 11, 22), 'High'),
    ('Fill the NUS and NTU forms yourself; parents review', 'NTU: one uninterrupted sitting for the India Standard 12 form (no save and return). NUS opens 16 Dec and closes 17 Feb. Finish in January, before the board exams.', 'student', date(2027, 1, 31), 'High'),
    ('Mentor: sign off the NUS and NTU forms; interview practice if HKU invites', 'Review each form before it goes in. HKU interviews ran Nov to Jan last cycle.', 'mentor', date(2027, 1, 25), 'High'),
    ('Results week: share results with parents and mentor within the hour', 'The 3-day clock starts at release: NUS portal update, NTU result slip, HKU results keyed in. Phone and email on.', 'student', None, 'High'),
    ('Mentor: confirm each results upload was accepted', 'Check NUS, NTU and HKU after the results hand-off; review the checklists monthly.', 'mentor', None, 'Medium'),
    ('On an offer: read the terms and deposit dates together; answer inside the window', 'HKU: accept within 3 to 4 weeks and pay the non-refundable deposit. Start the student visa (8 to 10 weeks).', 'parent', None, 'High'),
]

# ---- the college list (Preferences tab) -----------------------------------------------------------------------------------------------------------------------------------------
LIST_NAME = 'International: NUS, NTU, HKU (2027 intake)'
LIST_NOTES = ('Engineering at three universities for an Indian-board applicant. Programme at each still to be chosen with Darsh. Dates are read from the report of 30 Oct 2026; REPORTED items need confirming. '
              'No rank, mark or place is guaranteed.')
LIST = [
    {'key': 'nus', 'college': 'National University of Singapore (NUS)', 'branch': 'Engineering: programme to be chosen (12 programmes offered)', 'route': 'International',
     'location': 'Singapore', 'data_year': '2026-27', 'data_source': 'nus.edu.sg/oam; cde.nus.edu.sg (30 Oct 2026)',
     'data_note': 'No published minimum percentage; counsellors cite 93%+ for engineering (REPORTED). Holistic review of academic and non-academic achievements (OFFICIAL).',
     'fee_note': 'S$21,400 a year with MOE grant and 3-year bond; S$39,700 without (AY2026/27, REPORTED). About US$66,900 over four years with grant.',
     'open': date(2026, 12, 16), 'deadline': date(2027, 2, 17), 'source': NUS_SRC},
    {'key': 'ntu', 'college': 'Nanyang Technological University (NTU)', 'branch': 'Engineering: programme to be chosen (10 BEng programmes offered)', 'route': 'International',
     'location': 'Singapore', 'data_year': '2026-27', 'data_source': 'ntu.edu.sg/admissions (30 Oct 2026)',
     'data_note': 'Minimum average 93% across Standard 12 subjects including English (OFFICIAL). Offers on actual results only. Check each programme\'s minimum subject requirements; Physics matters.',
     'fee_note': 'About S$21,400 a year with grant and 3-year bond; S$36,350 to S$40,600 without (AY2026/27, REPORTED). About US$66,900 over four years with grant.',
     'open': date(2026, 10, 15), 'deadline': date(2027, 3, 19), 'source': NTU_SRC},
    {'key': 'hku', 'college': 'The University of Hong Kong (HKU)', 'branch': 'Engineering: programme to be chosen (departmental BEngs and faculty BEng(Elite))', 'route': 'International',
     'location': 'Hong Kong', 'data_year': '2026-27', 'data_source': 'admissions.hku.hk/India; ugadmissions.engg.hku.hk (30 Oct 2026)',
     'data_note': '90% in the best five subjects reported as the lower boundary in the 2026 cycle (REPORTED). Interview, personal statement and references count (OFFICIAL).',
     'fee_note': 'HK$280,000 a year for 2027-28 (about US$35,900), no bond found. About US$143,600 over four years (OFFICIAL).',
     'open': date(2026, 9, 23), 'deadline': date(2026, 11, 25), 'source': HKU_SRC},
]
