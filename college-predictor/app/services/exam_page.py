"""Data behind the public /exam-schedule page (validated against official sources on 28 Nov 2026, cycle 2026-27 / admissions 2027).

Statuses — how firm the date is:
  Confirmed  announced by the conducting body (source named)
  Tentative  provisional / published as subject to change (e.g. NTA's calendar of 16 Sep 2026)
  Expected   not announced; the window is inferred from earlier cycles

`start`/`end` (ISO dates) drive the downloadable calendar (.ics). For Expected rows they are the
start/end of the likely window, never a promised exam day, and the .ics description says so.
Edit this file to update the page; nothing else needs to change.
"""
from datetime import date
from types import SimpleNamespace

from app.services import exam_calendar as xc

VERIFIED = date(2026, 11, 28)

# (id, name, badge, when, status, description, start, end, note)
_E = 'Expected'
_T = 'Tentative'
_C = 'Confirmed'

CATEGORIES = [
    {'key': 'eng', 'title': 'National Engineering', 'col': 'left', 'grad': '#0E3A8A,#0A2560', 'dot': '#60a0ff', 'exams': [
        ('jee-main-reg', 'JEE Main 2027 — Session 1 registration', 'ENGINEERING', '24 Oct – 22 Nov 2026 (closed) · corrections till 29 Nov, 11:50 pm', _C,
         "Registration has closed: the regular window ended on 22 Nov and the late-fee window (extra ₹500) on 26 Nov; NTA did not extend either. The one-time correction window is open 27–29 Nov (till 11:50 pm on 29 Nov) at jeemain.nta.nic.in, and NTA says no correction will be entertained after that. Per NTA's 27 Nov notice you cannot change mobile number, e-mail, address, emergency contact or photograph; you can change any one of candidate, father's or mother's name; and you can change Class 10 and 12 details, state code of eligibility, exam city choices, date of birth, gender, category, sub-category/PwBD (if not verified by UDID), signature, medium and paper. Any extra fee must be paid online and no fee is refunded; once submitted, the form is frozen. Only one application per candidate is allowed (NTA's 30 Oct clarification). City slip 30 Dec; admit card 13 Jan 2027.", '2026-10-24', '2026-11-22', 'NTA public notices, 24, 28 and 30 Oct and 27 Nov 2026'),
        ('jee-main-s1', 'JEE Main 2027 — Session 1', 'ENGINEERING', '20, 21, 22, 23, 24 & 28 Jan 2027', _C,
         'Computer-based test in India and 9 cities abroad. Paper 1 (B.E./B.Tech) runs in two shifts, 9 am–12 noon and 3–6 pm. Paper 2A (B.Arch) and Paper 2B (B.Planning) are 3 hours each and listed in the first shift; candidates taking both B.Arch and B.Planning get 3½ hours. Held in 13 languages. If you sit both sessions, the better total NTA score counts.', '2027-01-20', '2027-01-28', 'NTA public notice, 24 Oct 2026'),
        ('jee-main-s2', 'JEE Main 2027 — Session 2', 'ENGINEERING', '2–7 Apr 2027 (registration 5 Jan – 3 Feb)', _T,
         "Proposed in NTA's revised calendar of 26 Oct 2026 and subject to change; NTA will confirm them by a separate notice. The registration, city slip and admit card dates below are indicative until then. Registration 5 Jan – 3 Feb 2027 (late fee window 4–7 Feb, corrections 8–10 Feb), city slip 12 Mar, admit card 25 Mar. The better of your two sessions is used for ranking and JEE Advanced eligibility.", '2027-04-02', '2027-04-07', 'NTA calendar of 26 Oct 2026 (proposed dates)'),
        ('jee-adv', 'JEE Advanced 2027', 'IIT GATEWAY', 'Sunday 23 May 2027', _C,
         'Gateway to the IITs, organised by IIT Delhi for 2027 (jeeadv.ac.in). Registration, admit card and result dates are not yet announced. Only the top 2,50,000 in JEE Main Paper 1 (by category) can apply; at most two attempts in consecutive years.', '2027-05-23', '2027-05-23', 'IIT Delhi notice, 13 Nov 2026'),
        ('josaa', 'JoSAA 2027 Counselling', 'COUNSELLING', 'Jun–Aug 2027 (expected)', _E,
         'Multi-round counselling for IITs, NITs, IIITs and GFTIs. Choice-filling is high-stakes — prepare your list before the window opens.', '2027-06-15', '2027-08-15', 'Prepare choices early'),
        ('gate', 'GATE 2027', 'PG ENGINEERING', '6, 7, 13, 14, 20 & 21 Feb 2027', _C,
         'Conducted by IIT Madras (gate2027.iitm.ac.in); results 19 Mar 2027; city allotment 4 Jan 2027; admit card date to be announced. The organisers note all dates are subject to change.', '2027-02-06', '2027-02-21', 'Registration has closed'),
        ('cuet-ug', 'CUET UG 2027', 'CENTRAL UNIVERSITIES', 'May 2027 (2026: 11–31 May)', _E,
         'NTA test for central and participating universities. Notification expected around January 2027 — not yet announced.', '2027-05-10', '2027-05-31', None),
        ('nata', 'NATA 2027 (Architecture)', 'ARCHITECTURE', 'Mar–Aug 2027 (brochure awaited)', _E,
         'Mandatory for B.Arch at Council of Architecture colleges. The 2026 cycle ran multi-session from March to August; the 2027 brochure is not yet published.', '2027-03-01', '2027-08-31', 'CoA brochure awaited'),
    ]},
    {'key': 'med', 'title': 'Medicine / NEET', 'col': 'left', 'grad': '#1F8B5C,#156644', 'dot': '#5ddba0', 'exams': [
        ('neet-ug', 'NEET UG 2027', 'MEDICINE', 'Expected May 2027 (not announced)', _E,
         "The sole UG medical admission test (MBBS/BDS/AYUSH). The Education Minister said in May 2026 that NEET would move to computer-based testing from 2027, but the Centre has since told the Supreme Court that the shift is under active consideration and the final call will follow the Nilekani-led task force, whose term now runs to January 2027 (reported) — so the mode for 2027 is not settled. NTA's revised exam calendar (26 Oct 2026) runs only to April 2027 and does not list NEET UG; dates and format are not yet official — watch neet.nta.nic.in. Reports suggest about 2 May 2027 with registration in Feb–Mar 2027 (unofficial).", '2027-05-01', '2027-05-31', 'CBT for 2027 not yet final (reported)'),
        ('mcc-aiq', 'MCC AIQ Counselling', 'COUNSELLING', 'Jul–Aug 2027 (expected)', _E,
         'MCC runs the 15% All-India Quota seats; state counselling for state-quota seats runs in parallel.', '2027-07-15', '2027-08-31', None),
        ('neet-pg', 'NEET PG 2027', 'MEDICINE PG', 'Expected mid-2027 (not announced)', _E,
         'Conducted by NBEMS for MD / MS / diploma / DNB. No 2027 date yet; recent cycles ran in the middle of the year. Check nbe.edu.in.', '2027-06-01', '2027-08-31', None),
        ('ini-cet', 'INI-CET January 2027 session', 'PG AIIMS', 'Jan 2027 session held 1 Nov 2026 (CBT); result declared 6 Nov', _T,
         "Institute of National Importance PG test — AIIMS, JIPMER, PGIMER, NIMHANS. The January 2027 session was held on 1 Nov 2026 and the result was published on 6–7 Nov 2026 (Result Notification No. 304/2026 dated 6 Nov, as reported; AIIMS's calendar lists 7 Nov). Counselling and seat-allocation dates were still awaited on 28 Nov 2026. AIIMS's tentative 2027 calendar lists the July 2027 session for 22 May 2027, with the result on 29 May 2027. Confirm on aiimsexams.ac.in.", '2026-11-01', '2026-11-01', 'Result out; counselling awaited'),
        ('neet-mds', 'NEET MDS 2027', 'DENTAL PG', 'Expected about May 2027 (2026: about 2 May)', _E,
         'NBE test for MDS admissions at dental colleges. NBEMS has not announced the 2027 dates.', '2027-05-01', '2027-05-31', None),
        ('fmge', 'FMGE', 'FOREIGN MED', 'Next session: Jan–Feb 2027 (date awaited; 9 Jan 2027 reported deferred)', _T,
         "Screening test for Indian citizens with foreign medical degrees who wish to practise in India. NBEMS's tentative schedule listed the next sitting for 9 Jan 2027, but news reports citing an NBEMS notice on the additional FMGE of 31 Oct 2026 say that sitting is deferred to a later date in January or February 2027; the new date and the application window are not yet announced. Confirm on natboard.edu.in.", None, None, '9 Jan deferred (reported); new date awaited'),
        ('aiapget', 'AIAPGET 2027', 'AYUSH PG', 'Jul–Aug 2027 (expected; 2026: 22 Aug)', _E,
         'All India AYUSH Post Graduate Entrance Test.', '2027-07-01', '2027-08-31', None),
    ]},
    {'key': 'law', 'title': 'Law Entrance Exams', 'col': 'left', 'grad': '#6B3FA0,#4E2C80', 'dot': '#c09af0', 'exams': [
        ('clat', 'CLAT 2027 (NLUs)', 'LAW', 'Sunday 6 Dec 2026, 2–4 pm', _C,
         "Announced by the Consortium of NLUs (consortiumofnlus.ac.in) in its press release of 22 Jul 2026. Offline mode; syllabus and pattern unchanged. Registration closed on 7 Nov 2026, 11:59 pm (extended from 31 Oct by the Consortium's notice of 31 Oct); fee payment for started applications and corrections ran to 10 Nov. Admit card available since 21 Nov 2026, 10 am, and downloadable until 6 Dec, 1:30 pm, from your login at consortiumofnlus.ac.in (Consortium notice of 21 Nov); no physical copy is sent.", '2026-12-06', '2026-12-06', 'Admit card out since 21 Nov'),
        ('ailet', 'AILET 2027 (NLU Delhi)', 'LAW', 'Sunday 13 Dec 2026, 2–4 pm', _C,
         "NLU Delhi's own entrance test, separate from CLAT. Applications ran from 7 Aug 2026 and closed on 13 Nov 2026 (extended from 10 Nov by NLU Delhi's notice of 11 Nov). Admit card available since 24 Nov 2026, 11 am, from your AILET login at nationallawuniversitydelhi.in (NLU Delhi notice of 23 Nov); the notice gives 6 Dec 2026, 1:30 pm, as the last time to download, so download it early. Members: see the Law 2027 roadmap.", '2026-12-13', '2026-12-13', 'Admit card out since 24 Nov'),
        ('slat', 'SLAT 2027 (Symbiosis)', 'LAW', '19 & 26 Dec 2026 (best of two)', _C,
         'Tests on 19 and 26 Dec 2026 per slat-test.org (best score counts). Registration and payment close on 4 Dec 2026; admit cards on 11 Dec (Test 1) and 18 Dec (Test 2); result on 12 Jan 2027. Symbiosis notes the schedule may change.', '2026-12-19', '2026-12-26', 'Official: slat-test.org'),
        ('lsat', 'LSAT India', 'LAW', 'Discontinued (LSAC, from 2025)', _T,
         'LSAC has reportedly discontinued LSAT India from 2025 with no replacement; Indian private law schools now use CLAT, SLAT, MH CET Law or their own tests. Confirm with each college.', None, None, 'Reported discontinued'),
        ('mh-law', 'MH CET Law 2027', 'STATE LAW', '5-yr LLB: 28–29 Mar & 24 May 2027; 3-yr LLB: 4–5 May 2027 (tentative)', _T,
         'Maharashtra state law entrance for 3-year and 5-year LLB programmes. The CET Cell tentative AY 2027-28 schedule (16 Nov 2026) gives the 5-year LLB two attempts (higher score counts); registration expected Dec 2026 – Jan 2027.', '2027-03-28', '2027-05-24', 'CET Cell tentative schedule, 16 Nov 2026'),
        ('lawcet', 'AP / TS LAWCET 2027', 'STATE LAW', 'Expected May 2027', _E,
         'Law entrance for Andhra Pradesh and Telangana state law colleges.', '2027-05-01', '2027-05-31', None),
        ('cuet-pg', 'CUET PG 2027 (incl. LLM)', 'PG', '2–31 Mar 2027 (provisional)', _T,
         "Per NTA's revised exam calendar (public notice of 26 Oct 2026): 2–5, 8–9, 12, 15–19, 24–25 and 29–31 Mar 2027, 17 days in all; NTA marks the dates tentative. Registration had not opened by 28 Nov 2026 and is expected Dec 2026 – Jan 2027; subject-wise dates follow in the bulletin.", '2027-03-02', '2027-03-31', 'NTA calendar · provisional'),
    ]},
    {'key': 'comm', 'title': 'Commerce / Management', 'col': 'right', 'grad': '#C47A00,#9B5E00', 'dot': '#ffd070', 'exams': [
        ('cat', 'CAT 2026 (IIMs & MBA)', 'MBA', 'Sunday 29 Nov 2026 · 3 sessions', _C,
         'Convened by IIM Indore. Registration has closed. Admit card available since 6 Nov 2026 (moved from 4 Nov); a CAT score is valid until 31 Dec 2027. See our CAT page for details.', '2026-11-29', '2026-11-29', 'Official: iimcat.ac.in'),
        ('xat', 'XAT 2027 (XLRI)', 'MBA', 'Sunday 3 Jan 2027, 2–5 pm', _C,
         'Announced by XLRI (xatonline.in). Computer-based, single session. Registration until 6 Dec 2026; admit card from 20 Dec (tentative).', '2027-01-03', '2027-01-03', 'Register by 6 Dec'),
        ('snap', 'SNAP 2026 (Symbiosis)', 'MBA', '13, 19 & 26 Dec 2026 (3 tests)', _C,
         'Test dates per snaptest.org. Up to three attempts; best score counts. Registration and payment closed on 25 Nov 2026; admit cards on 7, 11 and 18 Dec for the three tests; result 12 Jan 2027. Apply separately to each Symbiosis institute.', '2026-12-13', '2026-12-26', 'Official: snaptest.org'),
        ('nmat', 'NMAT by GMAC 2026–27', 'MBA', '2 Nov – 20 Dec 2026 window', _T,
         'Multiple attempts within the testing window; you choose the score to send. Window and deadlines as reported: registration closed on 25 Oct 2026 (extended from 10 Oct); sources differ on the last test day (17–20 Dec). Confirm on mba.com.', '2026-11-02', '2026-12-20', 'Reported — verify'),
        ('iift', 'IIFT MBA (IB) 2027–29', 'MBA', 'Via CAT 2026 · apply by 8 Dec 2026 (extended)', _T,
         "IIFT uses CAT 2026 scores to shortlist the 2027–29 MBA (IB) and MBA (BA) intake rather than a separate NTA test (stated on iift.ac.in). Applications opened 12 Oct 2026. The deadline was 25 Nov and has been extended: the iift.ac.in banner now reads 'Last date to apply is 8 Dec 2026' (11:59 pm, as reported), though the dates table on the same page still shows 25 Nov. The shortlist is reported for the last week of January 2027. Confirm on iift.ac.in.", '2026-11-29', '2026-11-29', 'Uses CAT 2026 score · deadline extended to 8 Dec'),
        ('cmat', 'CMAT 2027 (NTA)', 'MBA', 'Thursday 11 Feb 2027', _C,
         "NTA's public notice of 23 Nov 2026 sets CMAT 2027 for 11 Feb 2027 (the September exam calendar had said 7 Feb). Computer-based, 3 hours; timing to be announced. Apply on cmat.nta.nic.in from 23 Nov to 20 Dec 2026, 11:50 pm (fee by 21 Dec); with a late fee of Rs 500, 22–25 Dec; corrections 26–28 Dec. City slip 21 Jan 2027; admit card 4 Feb; result 25 Feb 2027.", '2027-02-11', '2027-02-11', 'Apply by 20 Dec · NTA notice, 23 Nov 2026'),
        ('tissnet', 'TISS admissions 2027', 'SOCIAL SCIENCE', 'No TISSNET — CAT-based programmes: apply by 4 Dec 2026, 5 pm; others via CUET PG', _T,
         'TISS no longer holds TISSNET. Its admissions site shows CAT-PG Programme 2027–28 admissions open (HRM and labour relations, organisation development, hospital administration and analytics) on CAT 2026 scores. The TISS admission calendar gives applications from 9 Nov to 4 Dec 2026, 5 pm (all dates marked tentative); the correction window, shortlist and interview dates are still to be announced. Other MA programmes use CUET PG. Confirm on admissions.tiss.ac.in.', None, None, 'CAT-PG 2027–28 applications open'),
        ('ca', 'CA exams (ICAI Jan 2027) / CS / CMA', 'PROFESSIONAL', 'ICAI Jan 2027: Foundation 3, 5, 7, 9 Jan; Inter 2–12 Jan', _C,
         'ICAI exams in January 2027 (announcement of 23 Sep 2026): Intermediate Group I on 2, 4, 6 Jan and Group II on 8, 10, 12 Jan; Foundation on 3, 5, 7, 9 Jan; exam forms closed in November. ICSI CS Executive/Professional: 21–28 Dec 2026 (no exam 25 Dec). ICMAI CMA: Inter/Final 10–17 Dec, Foundation 13 Dec 2026 (ICMAI timetable). ICAI May 2027 dates not yet announced.', '2027-01-02', '2027-01-12', 'ICAI announcement, 23 Sep 2026'),
        ('nimcet', 'NIMCET 2027 (MCA at NITs)', 'MCA', 'Expected early Jun 2027 (2026: 6 Jun)', _E,
         'Common entrance for MCA at the NITs; mathematics-heavy.', '2027-06-01', '2027-06-10', None),
    ]},
    {'key': 'sci', 'title': 'Science / Research', 'col': 'right', 'grad': '#0E7C8B,#085F6B', 'dot': '#7de8f0', 'exams': [
        ('jam', 'JAM 2027 (IIT M.Sc)', 'IIT MSC', 'Sunday 14 Feb 2027', _C,
         'Joint Admission Test for M.Sc programmes at IITs and IISc, organised by IIT Kharagpur (jam.iitkgp.ac.in). Registration (extended) closed on 24 Oct 2026; the paid data correction window on the JOAPS portal is open now, 25 Nov – 1 Dec 2026; results 18 Mar 2027.', '2027-02-14', '2027-02-14', 'Data correction open until 1 Dec'),
        ('jest', 'JEST 2027', 'RESEARCH', 'Expected Apr 2027', _E,
         'Screening test for PhD programmes in physics and theoretical computer science at leading research institutes. Applications expected around February 2027 on jest.org.in.', '2027-04-01', '2027-04-30', None),
        ('tifr', 'TIFR GS 2027', 'RESEARCH', 'Sunday 13 Dec 2026', _C,
         'Tata Institute of Fundamental Research Graduate School test. Per the TIFR GS-2027 advertisement, applications closed on 25 Oct 2026, 11 pm. Morning session 9 am (Science Education; Mathematics PhD at CAM), afternoon session 2–5 pm (other subjects). Hall tickets, due in mid-November, are now available for download from the TIFR Graduate Studies site (tifr.res.in/academics); the test venue is shown on the hall ticket.', '2026-12-13', '2026-12-13', 'Hall tickets available — download now'),
        ('nest', 'NEST 2027', 'NISER / CEBS', 'First week of Jun 2027 (expected; 2026: 6 Jun)', _E,
         'Entrance for NISER and UM-DAE CEBS integrated M.Sc programmes. The 2027 details are not yet published on nestexam.in.', '2027-06-01', '2027-06-07', None),
        ('iat', 'IISER IAT 2027', 'IISER', 'Early Jun 2027 (expected)', _E,
         'Aptitude test for the IISERs; the notification is expected around February 2027.', '2027-06-01', '2027-06-10', None),
        ('isi', 'ISI Admission 2027', 'ISI', 'Notice ~Feb 2027 · test ~May 2027', _E,
         'Indian Statistical Institute entrance (2026 test: 10 May); official notice not yet out.', '2027-05-01', '2027-05-31', None),
        ('ugee', 'UGEE 2027 (IIIT Hyderabad)', 'RESEARCH', 'Expected May 2027', _E,
         'IIIT Hyderabad undergraduate entrance (2026: 2 May).', '2027-05-01', '2027-05-31', None),
        ('csir-net', 'CSIR-UGC NET', 'JRF / LECTURESHIP', '19, 22 & 27 Dec 2026', _C,
         "Joint CSIR-UGC NET December 2026; science subjects, computer-based. NTA's public notice of 27 Nov 2026 gives the schedule: Life Sciences and Biotechnology on 19 Dec (3–6 pm); Chemical Sciences and Earth, Atmospheric, Ocean and Planetary Sciences on 22 Dec (9 am–12 noon); Mathematical Sciences and Physical Sciences on 27 Dec (3–6 pm). Applications closed on 9 Nov 2026 (extended). The exam city intimation slip is out on csirnet.nta.nic.in since 27 Nov; it is not the admit card, which NTA will issue separately (date not announced).", '2026-12-19', '2026-12-27', 'City slip out (27 Nov) · admit card awaited'),
    ]},
    {'key': 'design', 'title': 'Design / Architecture', 'col': 'right', 'grad': '#1A6B3A,#104D28', 'dot': '#60d090', 'exams': [
        ('uceed', 'UCEED 2027 (IIT B.Des)', 'DESIGN', 'Sunday 17 Jan 2027, 9 am–12 noon', _C,
         'IIT Bombay (uceed.iitb.ac.in). Registration (regular fee) closed on 5 Nov 2026 after an extension; late fee until 10 Nov, 5 pm, with no further extension. Results 6 Mar 2027; separate B.Des application 15 Mar; admission rounds from 21 Apr. Draft Part-A key 19 Jan; shortlisting 4 Feb. Members: see the UCEED 2027 roadmap.', '2027-01-17', '2027-01-17', 'Admit card 1 Jan 2027'),
        ('ceed', 'CEED 2027 (IIT M.Des)', 'DESIGN PG', 'Sunday 17 Jan 2027, 9 am–12 noon', _C,
         'IIT Bombay (ceed.iitb.ac.in), same day as UCEED. Registration (regular fee) closed on 5 Nov 2026 after an extension; late fee 6–10 Nov, 5 pm. Admit card from 1 Jan 2027; result 3 Mar 2027.', '2027-01-17', '2027-01-17', 'Admit card 1 Jan 2027'),
        ('nid-prelims', 'NID DAT 2027 — Prelims', 'DESIGN', 'Sunday 20 Dec 2026', _C,
         'Per the NID Admissions Handbook 2027–28: one application (until 30 Nov 2026, 11:59 pm) covers Prelims and Mains. Form edit window 1 Dec (4 pm) – 3 Dec (11:59 pm); admit card from 10 Dec, 4 pm; Prelims on Sunday 20 Dec 2026. Prelims result on 16 Mar 2027, 4 pm for B.Des and the integrated M.Des (16 Feb 2027 for the M.Des). See our NID page.', '2026-12-20', '2026-12-20', 'Apply by 30 Nov, 11:59 pm — dates per the NID handbook'),
        ('nid-mains', 'NID DAT 2027 — Mains', 'DESIGN', 'After 16 Mar 2027 (date awaited)', _E,
         'Studio Sensitivity Test plus In-Person Sensitivity Test for shortlisted candidates; dates not yet announced.', None, None, None),
        ('nift', 'NIFT 2027', 'FASHION / DESIGN', 'Sunday 10 Jan 2027 (UG & PG)', _T,
         "NTA opened NIFT 2027 registration on 16 Oct 2026 (exams.nta.nic.in/niftee); one application covers all campuses. Per NTA's notice of 14 Nov, regular registration closed on 24 Nov; applications with a late fee (Rs 5,000, as reported) are accepted until 29 Nov; corrections 30 Nov – 2 Dec, with no further correction window. Exam on 10 Jan 2027 and admit card about 4 Jan 2027 as reported. Confirm on nift.ac.in.", '2027-01-10', '2027-01-10', 'Late fee until 29 Nov · corrections 30 Nov – 2 Dec'),
    ]},
    {'key': 'state', 'title': 'State-Level Exams', 'col': 'right', 'grad': '#B05A00,#883F00', 'dot': '#ffad60', 'exams': [
        ('tnea', 'TNEA 2027 (Tamil Nadu)', 'STATE · TN', 'Registration ~May 2027 (expected; 2026: 3 May–5 Jun)', _E,
         'No entrance exam — your Class 12 marks decide the rank. In 2026 counselling ran 20 Jul–30 Aug (DoTE schedule, subject to AICTE approval). See our TNEA pages.', '2027-05-01', '2027-06-05', 'No exam — Class 12 marks'),
        ('mht-cet', 'MHT CET 2027 (Maharashtra)', 'STATE · MH', 'PCM 16–26 Apr & 10–15 May 2027; PCB 8–13 Apr & 6–8 May 2027 (tentative, CET Cell)', _T,
         'CET Cell press release of 16 Nov 2026 (tentative schedule): two attempts for PCM and PCB. The first attempt is compulsory and the second optional; if you sit both, the better percentile counts. The CET Cell published the MHT CET 2027 syllabus and marking scheme on 18 Nov 2026 (about 20% weightage for Std XI and 80% for Std XII, no negative marking). Application dates not yet announced. Confirm on cetcell.mahacet.org.', '2027-04-08', '2027-05-15', '2 attempts · Apr & May'),
        ('wbjee', 'WBJEE 2027 (West Bengal)', 'STATE · WB', 'May 2027 (expected; 2026: exam 24 May)', _E,
         'Offline format. In 2026 applications ran 10 Mar–8 Apr. Check wbjeeb.nic.in; no 2027 notice yet.', '2027-05-01', '2027-05-31', None),
        ('keam', 'KEAM 2027 (Kerala)', 'STATE · KL', '21–26 Apr 2027 (reported; 2026: Engineering 17–22 Apr)', _T,
         'Conducted by CEE Kerala for engineering and other professional courses. News reports of 11 Nov 2026 give 21–26 Apr 2027 for the engineering and pharmacy tests (computer-based); CEE Kerala has not yet published the KEAM 2027 notification, and registration is expected around January 2027. Confirm on cee.kerala.gov.in.', '2027-04-21', '2027-04-26', 'Reported (unofficial)'),
        ('kcet', 'KCET 2027 (Karnataka)', 'STATE · KA', 'April 2027 (expected; 2026: 23–24 Apr)', _E,
         'Karnataka CET for government and aided engineering seats; KEA publishes the schedule.', '2027-04-01', '2027-04-30', None),
        ('comedk', 'COMEDK UGET 2027', 'STATE · KA', 'Apr–May 2027 (expected)', _E,
         'Private colleges in Karnataka; separate from KCET (2026: 9 May).', '2027-04-15', '2027-05-31', None),
        ('eapcet', 'TG-EAPCET / AP-EAPCET 2027', 'STATE · TG/AP', 'May 2027 (expected; 2026: TG 9–11 May, AP 12–18 May)', _E,
         'Telangana and Andhra Pradesh engineering entrance tests (2026: 9–18 May).', '2027-05-01', '2027-05-31', None),
        ('gujcet', 'GUJCET 2027 (Gujarat)', 'STATE · GJ', 'Mar 2027 (expected)', _E,
         'GSEB test for Gujarat engineering colleges (2026: 29 Mar).', '2027-03-01', '2027-03-31', None),
        ('uptac', 'UPTAC / AKTU 2027 (UP)', 'STATE · UP', 'Registration from late May, counselling Jun–Jul 2027 (expected)', _E,
         'Uttar Pradesh engineering admissions use your JEE Main score; there is no separate UPSEE.', '2027-05-25', '2027-07-15', 'Via JEE Main score'),
        ('ojee', 'OJEE 2027 (Odisha)', 'STATE · OD', 'May 2027 (expected; 2026: 4–9 May)', _E,
         'Odisha Joint Entrance Examination (2026: 4–9 May).', '2027-05-01', '2027-05-31', None),
        ('bcece', 'BCECE / UGEAC 2027 (Bihar)', 'STATE · BR', 'May–Jun 2027 (expected; 2026: 30–31 May)', _E,
         'Bihar engineering admissions; confirm the current route on the Bihar board website.', '2027-05-01', '2027-06-30', None),
    ]},
    {'key': 'nri', 'title': 'NRI Routes & Private Institutes', 'col': 'right', 'grad': '#4A5060,#32383F', 'dot': '#aab0c0', 'exams': [
        ('dasa', 'DASA / CIWG 2027', 'NRI ROUTE', 'Jun–Aug 2027 (expected)', _E,
         'Direct Admission of Students Abroad / CIWG for NITs, IIITs and GFTIs (via SAT or JEE Main). The 2027 schedule is not yet announced. EduAakashaA specialises in this route.', '2027-06-01', '2027-08-15', 'Our specialty'),
        ('nri-quota', 'Private & state NRI quota seats', 'NRI QUOTA', 'Jun–Sep 2027 (varies by college)', _E,
         'Many private colleges reserve NRI seats with separate fees and rules; each college publishes its own window.', '2027-06-01', '2027-09-30', 'Varies by college'),
        ('aeee', 'AEEE 2027 (Amrita)', 'INSTITUTE', '15 Apr – 7 May 2027 (tentative)', _T,
         'Amrita Vishwa Vidyapeetham opened AEEE 2027 B.Tech applications on 7 Nov 2026 (aeee.amrita.edu); fee ₹1,300. Exam window 15 Apr – 7 May 2027 with slot booking on the portal (Amrita calls the dates tentative); the last date to apply is not yet announced. See our AEEE page.', '2027-04-15', '2027-05-07', 'Applications open'),
        ('bitsat', 'BITSAT 2027', 'INSTITUTE', 'Registration from Dec 2026 · sessions Apr–Jun 2027', _E,
         'BITS Pilani has not yet published the 2027 notice; registration is expected from around December 2026 and session dates are awaited.', '2027-04-01', '2027-06-15', 'Dates awaited'),
        ('viteee', 'VITEEE 2027', 'INSTITUTE', '27 Apr – 2 May 2027 (tentative)', _T,
         'Per viteee.vit.ac.in: applications 20 Oct 2026 – 31 Mar 2027; admit card 25–30 Apr; the number of exam days varies by city; results and counselling from the second week of May. VIT marks these dates tentative. See our VITEEE page for NRI details.', '2027-04-27', '2027-05-02', 'Apply by 31 Mar 2027'),
        ('srmjeee', 'SRMJEEE 2027', 'INSTITUTE', '17–18 Apr & 19–20 Jun 2027 (tentative)', _T,
         "Per SRM's application portal (applications.srmist.edu.in/btech): two phases, Phase 1 on 17–18 Apr 2027 (apply by 2 Apr) and Phase 2 on 19–20 Jun 2027 (apply by 4 Jun). It is a centre-based computer test (CBT) at centres across India; fee ₹1,400 per phase, non-refundable, paid separately for each phase. SRM marks the exam dates tentative. The registration start date is not shown on the portal; it is reported as 30 Oct or 4 Nov 2026.", '2027-04-17', '2027-06-20', 'Tentative per SRM'),
        ('met', 'MET — Manipal 2027', 'INSTITUTE', 'Apr & May 2027 phases (reported)', _T,
         'Manipal Institute of Technology entrance. Reported: applications opened about 19 Oct 2026; Phase 1 applications close 15 Mar 2027; Phase 1 in April and Phase 2 in May 2027 (exact dates awaited); the better score counts. Confirm on manipal.edu.', '2027-04-01', '2027-05-31', 'Phase 1: apply by 15 Mar'),
        ('kiitee', 'KIITEE 2027', 'INSTITUTE', '16–20 Apr & 4–6 Jun 2027 (reported)', _T,
         'KIIT Bhubaneswar entrance. Reported: applications opened 10 Nov 2026 (kiitee.kiit.ac.in); Phase 1 on 16–20 Apr (apply by 8 Apr), Phase 2 on 4–6 Jun 2027 (apply by 30 May); slot booking needed for the admit card. Dates tentative; confirm on kiitee.kiit.ac.in.', '2027-04-16', '2027-06-06', 'Reported (unofficial)'),
    ]},
]

MILESTONES = [
    ('OCT 2026', 'JEE Main Session 1 registration opened 24 Oct (closed 22 Nov) · TIFR GS closed 25 Oct · UCEED / CEED registration closed 5 Nov (late fee to 10 Nov)'),
    ('NOV 2026', 'INI-CET result (6 Nov) · AEEE registration opened 7 Nov · CLAT admit card (21 Nov) · JEE Main Session 1 closed 22 Nov (late fee 23–26 Nov; corrections 27–29 Nov) · CMAT registration opened 23 Nov · AILET admit card (24 Nov) · NIFT closed 24 Nov (late fee to 29 Nov) · CAT (29 Nov) · NID registration closes 30 Nov'),
    ('DEC 2026', 'TISS CAT-based programmes close 4 Dec · CLAT (6 Dec) · IIFT applications close 8 Dec · CMAT registration closes 20 Dec · CSIR NET (19, 22, 27 Dec) · TIFR GS & AILET (13 Dec) · SNAP (13, 19, 26 Dec) · SLAT (19, 26 Dec) · NID DAT Prelims (20 Dec) · BITSAT registration expected'),
    ('JAN 2027', 'ICAI exams (2–12 Jan) · XAT (3 Jan) · NIFT (10 Jan) · UCEED & CEED (17 Jan) · JEE Main Session 1 (20–24 & 28 Jan)'),
    ('FEB 2027', 'GATE (6, 7, 13, 14, 20, 21 Feb) · CMAT (11 Feb) · JAM (14 Feb)'),
    ('MAR 2027', 'CUET PG (2–31 Mar, provisional) · TN +2 board exams (3–29 Mar) · NID Prelims result (16 Mar) · MH CET Law 5-yr (28–29 Mar, tentative)'),
    ('APR 2027', 'JEE Main Session 2 (2–7 Apr) · MHT CET PCB (8–13 Apr) & PCM (16–26 Apr), tentative · AEEE (from 15 Apr) · KEAM (21–26 Apr, reported) · SRMJEEE & KIITEE Phase 1 (reported)'),
    ('MAY 2027', 'JEE Advanced (Sun 23 May) · MHT CET 2nd attempt (PCB 6–8, PCM 10–15 May) · NEET UG · CUET UG · COMEDK / EAPCET (expected)'),
    ('JUN–AUG', 'JoSAA · MCC · TNEA · DASA / CIWG counselling (expected)'),
]

FILTERS = [('all', 'All Exams'), ('eng', 'Engineering'), ('med', 'Medicine'), ('law', 'Law'), ('comm', 'Commerce / MBA'),
           ('sci', 'Science / Research'), ('design', 'Design / Arch'), ('state', 'State-Level'), ('nri', 'NRI & Private')]

CONTACT_LINE = 'Free counselling: www.eduaakashaa.com | +91-80157 22706 | info@eduaakashaa.com'


def all_exams():
    for cat in CATEGORIES:
        for row in cat['exams']:
            yield cat, row


def counts():
    total = sum(len(c['exams']) for c in CATEGORIES)
    by = {}
    for _c, row in all_exams():
        by[row[4]] = by.get(row[4], 0) + 1
    return {'total': total, 'categories': len(CATEGORIES), **by}


def as_event(row):
    """Adapter so services.exam_calendar.make_ics can export a row; None when the row has no date."""
    id_, name, _badge, when, status, desc, start, end, note = row
    if not start:
        return None
    a = date.fromisoformat(start)
    b = date.fromisoformat(end) if end else a
    tail = {'Confirmed': 'Announced by the conducting body.',
            'Tentative': 'Provisional date — it may change.',
            'Expected': 'EXPECTED WINDOW ONLY — the exam date is not announced yet.'}[status]
    text = f'{when}. {desc} {tail} Always confirm on the official website. {CONTACT_LINE}'
    return SimpleNamespace(id=id_, name=name, starts_on=a, ends_on=b, status=status, version=1, window_note=None, source=None,
                           verified_on=VERIFIED, ics_description=text)


def find(exam_id):
    for _c, row in all_exams():
        if row[0] == exam_id:
            return row
    return None


def all_events():
    return [e for e in (as_event(r) for _c, r in all_exams()) if e]


def all_ics():
    return xc.make_ics(all_events(), 'India Entrance Exams 2026-27 - EduAakashaA')


# --------------------------------------------------------------------------- #
# Application / deadline milestones (checked 28 Nov 2026). kind: open | close | late | admit | result | other
# status as above. A date of None means "announced as pending". Expected dates never make an application show as "open now".
# --------------------------------------------------------------------------- #
KIND_LABEL = {'open': 'Applications open', 'close': 'Applications close', 'late': 'Last date with late fee', 'admit': 'Admit card',
              'result': 'Result', 'other': 'Next step'}
KIND_ICON = {'open': '▶', 'close': '⏰', 'late': '⏳', 'admit': '🎫', 'result': '✅', 'other': '📌'}
DEADLINES = {
    'cmat': [('open', '2026-11-23', _C, 'NTA public notice, 23 Nov'), ('close', '2026-12-20', _C, 'Until 11:50 pm; fee payment until 21 Dec, 11:50 pm'), ('late', '2026-12-25', _C, 'Late fee Rs 500, 22–25 Dec, until 11:50 pm'), ('other', '2026-12-28', _C, 'Correction window 26–28 Dec, until 11:50 pm'), ('other', '2027-01-21', _C, 'Exam city announced'), ('admit', '2027-02-04', _C, 'NTA website'), ('other', '2027-02-21', _C, 'Recorded responses and provisional answer key, 19–21 Feb'), ('result', '2027-02-25', _C, None)],
    'uceed': [('open', '2026-10-01', _C, 'Registration (regular fee) — official'), ('close', '2026-11-05', _C, 'Extended from 31 Oct — official'),
              ('late', '2026-11-10', _C, 'Until 5 pm (window 6–10 Nov), no further extension — official'), ('admit', '2027-01-01', _C, 'From 1 pm — official'), ('other', '2027-01-08', _C, 'Last date to fix admit-card discrepancies, 5 pm'),
              ('result', '2027-03-06', _C, None), ('other', '2027-03-15', _C, 'Separate B.Des application (official)'), ('other', '2027-04-21', _C, 'Admission rounds begin (official)')],
    'ceed': [('open', '2026-10-01', _C, 'Registration (regular fee)'), ('close', '2026-11-05', _C, 'Extended from 31 Oct'), ('late', '2026-11-10', _C, 'Until 5 pm (window 6–10 Nov)'),
             ('admit', '2027-01-01', _C, 'From 1 pm'), ('other', '2027-01-19', _C, 'Draft Part-A answer key (comments till 21 Jan, 5 pm)'), ('other', '2027-01-26', _C, 'Final Part-A answer key, 5 pm'), ('other', '2027-02-04', _C, 'Part-A cut-off marks'), ('result', '2027-03-03', _C, None),
             ('other', '2027-03-10', _C, 'Score cards available (download until 31 Jul 2027)')],
    'clat': [('open', '2026-08-03', _C, 'Consortium press release of 22 Jul 2026'), ('close', '2026-11-07', _C, 'Extended from 31 Oct (Consortium notice of 31 Oct); closed'), ('admit', '2026-11-21', _C, 'Released 21 Nov, 10 am; download until 6 Dec, 1:30 pm (Consortium notice of 21 Nov)'), ('result', None, _E, 'Date awaited')],
    'ailet': [('open', '2026-08-07', _C, 'NLU Delhi admission notice of 7 Aug 2026'), ('close', '2026-11-13', _C, 'Extended from 10 Nov (NLU Delhi notice of 11 Nov); closed'), ('admit', '2026-11-24', _C, 'Released 24 Nov, 11 am; download until 6 Dec, 1:30 pm (NLU Delhi notice of 23 Nov)'), ('result', '2026-12-22', _E, 'Fourth week of December')],
    'slat': [('open', '2026-08-21', _T, 'Opened in August (reported)'), ('close', '2026-12-04', _C, 'Registration and payment — slat-test.org'),
             ('admit', '2026-12-11', _C, 'Test 1 (Test 2: 18 Dec) — slat-test.org'), ('result', '2027-01-12', _C, 'slat-test.org')],
    'nid-prelims': [('open', '2026-09-10', _C, 'NID Handbook 2027–28'), ('close', '2026-11-30', _C, 'Until 11:59 pm — NID admissions site and handbook'), ('other', '2026-12-03', _C, 'Form edit window 1 Dec (4 pm) – 3 Dec, 11:59 pm (NID handbook)'), ('admit', '2026-12-10', _C, 'From 4 pm (NID handbook)'), ('other', '2027-02-28', _C, 'One-time window to fix the category certificate, 16–28 Feb 2027, for B.Des / integrated M.Des (M.Des: 15–31 Jan) — NID handbook'), ('result', '2027-03-16', _C, '4 pm, B.Des / integrated M.Des; re-totalling 16–17 Mar. M.Des Prelims result is 16 Feb 2027 (NID handbooks)')],
    'cat': [('open', '2026-08-03', _C, None), ('close', '2026-09-22', _T, 'Extended from 15 Sep — verify on iimcat.ac.in'), ('admit', '2026-11-06', _T, 'Moved from 4 Nov (IIM Indore release, reported); until the exam'),
            ('result', None, _E, 'Date awaited — reports differ (late Dec to Jan)')],
    'gate': [('open', '2026-09-02', _C, 'GATE 2027 portal'), ('close', '2026-10-05', _C, 'Regular deadline'), ('late', '2026-10-12', _C, 'Late fee; special window 15–16 Oct'),
             ('other', '2026-11-30', _C, 'Rectification window for scrutiny defects (no fee) closes'), ('other', '2027-01-04', _C, 'City allotment'), ('result', '2027-03-19', _C, 'gate2027.iitm.ac.in')],
    'jee-main-s1': [('open', '2026-10-24', _C, 'NTA public notice'), ('close', '2026-11-22', _C, 'Closed; fee was also due by 22 Nov, 11:50 pm'), ('late', '2026-11-26', _C, 'Closed; late fee ₹500 extra, 23–26 Nov'), ('other', '2026-11-29', _C, 'Correction window 27–29 Nov closes at 11:50 pm (one-time)'), ('admit', '2027-01-13', _C, 'City slip 30 Dec 2026'), ('result', '2027-02-12', _E, 'About 12 Feb')],
    'jee-main-s2': [('open', '2027-01-05', _E, 'Indicative — NTA notice awaited'), ('close', '2027-02-03', _E, 'Indicative; late fee till 7 Feb'), ('admit', '2027-03-25', _E, 'Indicative; city slip 12 Mar')],
    'cuet-ug': [('open', '2027-01-15', _E, 'Notification expected ~January')],
    'aeee': [('open', '2026-11-07', _C, 'aeee.amrita.edu')],
    'bitsat': [('open', '2026-12-01', _E, 'December expected (no official 2027 notice yet)')],
    'srmjeee': [('open', '2026-10-30', _T, 'Reported; some sources say 4 Nov'), ('close', '2027-04-02', _T, 'Phase 1, per SRM portal'), ('close', '2027-06-04', _T, 'Phase 2, per SRM portal')],
    'nift': [('open', '2026-10-16', _C, 'NTA notice, 16 Oct'), ('close', '2026-11-24', _C, 'Extended from 16 Nov — NTA notice of 14 Nov'), ('late', '2026-11-29', _C, 'Late fee 25–29 Nov — NTA notice of 14 Nov'), ('other', '2026-12-02', _C, 'Correction window 30 Nov – 2 Dec; no further correction after this — NTA notice of 14 Nov'), ('admit', '2027-01-04', _T, 'Reported')],
    'xat': [('close', '2026-12-06', _C, 'xatonline.in'), ('admit', '2026-12-20', _T, 'Tentative per XLRI')],
    'snap': [('close', '2026-11-25', _C, 'snaptest.org'), ('admit', '2026-12-07', _C, 'SNAP 01 (SNAP 02: 11 Dec; SNAP 03: 18 Dec) — snaptest.org'), ('result', '2027-01-12', _C, 'snaptest.org')],
    'nmat': [('other', '2026-11-02', _T, 'Testing window opens (reported)')],
    'iift': [('open', '2026-10-12', _C, 'iift.ac.in announcement, 12 Oct'), ('close', '2026-12-08', _T, "Extended from 25 Nov — iift.ac.in banner; until 11:59 pm (reported). The page's dates table still shows 25 Nov — confirm on iift.ac.in")],
    'tissnet': [('open', '2026-11-09', _T, 'CAT-PG programmes — TISS admission calendar (dates marked tentative)'), ('close', '2026-12-04', _T, 'Until 5 pm — TISS admission calendar (marked tentative); no extension shown')],
    'ini-cet': [('admit', '2026-10-26', _T, 'AIIMS tentative calendar'), ('result', '2026-11-06', _T, 'Result notification 304/2026 (reported); AIIMS calendar lists 7 Nov; counselling dates still awaited on 28 Nov')],
    'jam': [('close', '2026-10-24', _C, 'Extended deadline — jam.iitkgp.ac.in'), ('other', '2026-12-01', _C, 'Paid data correction on the JOAPS portal, 25 Nov – 1 Dec 2026 — live now per jam.iitkgp.ac.in (update of 25 Nov)'), ('admit', '2027-01-05', _T, 'Reported; official site gives no admit card date yet'), ('result', '2027-03-18', _C, None)],
    'tifr': [('close', '2026-10-25', _C, 'Until 11 pm — TIFR advertisement'), ('admit', None, _C, 'Now available for download — tifr.res.in/academics (seen 28 Nov; release date not stated)')],
    'viteee': [('open', '2026-10-20', _C, 'viteee.vit.ac.in'), ('close', '2027-03-31', _T, 'Tentative per VIT'),
               ('admit', '2027-04-25', _T, '25–30 Apr, tentative per VIT')],
    'jee-adv': [('other', '2027-05-23', _C, 'Exam day: IIT Delhi notice, 13 Nov 2026')],
    'mht-cet': [('other', '2027-04-08', _T, 'PCB attempt 1 (8–13 Apr); attempt 2 6–8 May'), ('other', '2027-04-16', _T, 'PCM attempt 1 (16–26 Apr); attempt 2 10–15 May')],
    'mh-law': [('open', '2027-01-05', _E, 'Registration expected Dec 2026 – Jan 2027')],
    'met': [('open', '2026-10-19', _T, 'Reported'), ('close', '2027-03-15', _T, 'Phase 1, reported')],
    'kiitee': [('open', '2026-11-10', _T, 'Reported'), ('close', '2027-04-08', _T, 'Phase 1, reported'), ('close', '2027-05-30', _T, 'Phase 2, reported')],
    'fmge': [('other', None, _T, 'New exam date and application window awaited (9 Jan 2027 sitting reported deferred) — natboard.edu.in')],
    'csir-net': [('open', '2026-10-08', _T, 'NTA notification dated 7 Oct'), ('close', '2026-11-09', _C, 'Extended — NTA notice of 5 Nov; until 11:50 pm'), ('other', '2026-11-12', _T, 'Correction window 10–12 Nov (NTA notice of 10 Nov; dates as reported)'), ('other', '2026-11-20', _C, 'Subject-wise schedule — NTA notice of 20 Nov'), ('other', '2026-11-27', _C, 'Exam city intimation slip released — NTA notice of 27 Nov (not the admit card)'), ('admit', None, _E, 'To be issued separately — date not announced')],
}


def deadlines_for(exam_id):
    out = []
    for kind, d, status, note in DEADLINES.get(exam_id, []):
        dt = date.fromisoformat(d).strftime('%d %b %Y').lstrip('0') if d else None
        out.append({'k': kind, 'd': d, 'dt': dt, 's': status, 'n': note, 'label': KIND_LABEL[kind], 'icon': KIND_ICON[kind]})
    return out


def timeline_data():
    """Flat list for the Timeline / By-month / Calendar views (rendered client-side from one JSON blob)."""
    out = []
    for cat, row in all_exams():
        id_, name, badge, when, status, desc, start, end, note = row
        out.append({'id': id_, 'name': name, 'cat': cat['key'], 'catTitle': cat['title'], 'color': cat['grad'].split(',')[0],
                    'status': status, 'start': start, 'end': end or start, 'when': when, 'badge': badge, 'desc': desc, 'note': note,
                    'ms': deadlines_for(id_)})
    return out


def milestone_events(exam_id=None):
    """Dated deadline milestones as ICS-ready events (all exams, or one)."""
    rows = [(c, r) for c, r in all_exams() if exam_id in (None, r[0])]
    out = []
    for _c, r in rows:
        for m in deadlines_for(r[0]):
            if not m['d']:
                continue
            d = date.fromisoformat(m['d'])
            tail = {'Confirmed': 'Announced by the conducting body.', 'Tentative': 'Reported date — confirm on the official site.',
                    'Expected': 'EXPECTED — not announced; the real date may differ.'}[m['s']]
            text = f"{m['label']} for {r[1]}. {m['n'] + '. ' if m['n'] else ''}{tail} {CONTACT_LINE}"
            out.append(SimpleNamespace(id=f"{r[0]}-{m['k']}-{m['d']}", name=f"{r[1]} — {m['label']}", starts_on=d, ends_on=d,
                                       status=m['s'], version=1, window_note=None, source=None, verified_on=VERIFIED, ics_description=text))
    return out


def deadlines_ics(exam_id=None):
    name = 'Entrance exam deadlines 2026-27 - EduAakashaA'
    return xc.make_ics(milestone_events(exam_id), name)
