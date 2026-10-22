"""Data behind the public /exam-schedule page (October 2026 research, cycle 2026-27 / admissions 2027).

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

VERIFIED = date(2026, 10, 22)

# (id, name, badge, when, status, description, start, end, note)
_E = 'Expected'
_T = 'Tentative'
_C = 'Confirmed'

CATEGORIES = [
    {'key': 'eng', 'title': 'National Engineering', 'col': 'left', 'grad': '#0E3A8A,#0A2560', 'dot': '#60a0ff', 'exams': [
        ('jee-main-reg', 'JEE Main 2027 — Registration', 'ENGINEERING', 'Expected late Oct 2026', _E,
         'NTA has not yet opened registration or published the Information Bulletin. Apply only at jeemain.nta.nic.in; a correction window follows.', '2026-10-25', '2026-11-25', 'Bulletin awaited'),
        ('jee-main-s1', 'JEE Main 2027 — Session 1', 'ENGINEERING', '22–24 & 28–30 Jan 2027 (buffer 31 Jan)', _T,
         'From NTA\'s exam calendar published 16 Sep 2026, which NTA describes as provisional. B.Tech / B.Arch / B.Planning for NITs, IIITs and GFTIs. Your better session counts.', '2027-01-22', '2027-01-30', 'NTA calendar · provisional'),
        ('jee-main-s2', 'JEE Main 2027 — Session 2', 'ENGINEERING', 'April 2027 (dates awaited)', _E,
         'Final session. Registration is expected around early February. The better of your two sessions is used for ranking and JEE Advanced eligibility.', '2027-04-01', '2027-04-30', None),
        ('jee-adv', 'JEE Advanced 2027', 'IIT GATEWAY', 'Mid-May 2027 (JAB notice awaited)', _E,
         'Gateway to the IITs. The organising IIT and exact dates are not yet announced by the Joint Admission Board (jeeadv.ac.in). Must qualify JEE Main first.', '2027-05-10', '2027-05-24', 'Must qualify JEE Main first'),
        ('josaa', 'JoSAA 2027 Counselling', 'COUNSELLING', 'Jun–Aug 2027 (expected)', _E,
         'Multi-round counselling for IITs, NITs, IIITs and GFTIs. Choice-filling is high-stakes — prepare your list before the window opens.', '2027-06-15', '2027-08-15', 'Prepare choices early'),
        ('gate', 'GATE 2027', 'PG ENGINEERING', '6, 7, 13, 14, 20 & 21 Feb 2027', _C,
         'Conducted by IIT Madras (gate2027.iitm.ac.in); includes a new Robotics & Automation paper. Results expected 19 Mar 2027. The organisers note all dates are subject to change.', '2027-02-06', '2027-02-21', 'Registration has closed'),
        ('cuet-ug', 'CUET UG 2027', 'CENTRAL UNIVERSITIES', 'May 2027 (2026: 11–31 May)', _E,
         'NTA test for central and participating universities. Notification expected around January 2027 — not yet announced.', '2027-05-10', '2027-05-31', None),
        ('nata', 'NATA 2027 (Architecture)', 'ARCHITECTURE', 'Mar–Aug 2027 (brochure awaited)', _E,
         'Mandatory for B.Arch at Council of Architecture colleges. The 2026 cycle ran multi-session from March to August; the 2027 brochure is not yet published.', '2027-03-01', '2027-08-31', 'CoA brochure awaited'),
    ]},
    {'key': 'med', 'title': 'Medicine / NEET', 'col': 'left', 'grad': '#1F8B5C,#156644', 'dot': '#5ddba0', 'exams': [
        ('neet-ug', 'NEET UG 2027', 'MEDICINE', 'Expected May 2027 (not announced)', _E,
         'The sole UG medical admission test (MBBS/BDS/AYUSH). The Government has said NEET moves to computer-based testing from 2027, reportedly over several days; dates and format are not yet official — watch neet.nta.nic.in.', '2027-05-01', '2027-05-31', 'CBT shift announced'),
        ('mcc-aiq', 'MCC AIQ Counselling', 'COUNSELLING', 'Jul–Aug 2027 (expected)', _E,
         'MCC runs the 15% All-India Quota seats; state counselling for state-quota seats runs in parallel.', '2027-07-15', '2027-08-31', None),
        ('neet-pg', 'NEET PG 2027', 'MEDICINE PG', 'Expected mid-2027 (not announced)', _E,
         'Conducted by NBEMS for MD / MS / diploma / DNB. No 2027 date yet; recent cycles ran in the middle of the year. Check nbe.edu.in.', '2027-06-01', '2027-08-31', None),
        ('ini-cet', 'INI-CET January 2027 session', 'PG AIIMS', 'Sunday 1 Nov 2026, 9 am–12 noon', _T,
         'Institute of National Importance PG test — AIIMS, JIPMER, PGIMER, NIMHANS. From the AIIMS tentative 2027 calendar: registration closed 13 Oct; admit card 26 Oct; result expected ~7 Nov. The July 2027 session follows. Confirm on aiimsexams.ac.in.', '2026-11-01', '2026-11-01', 'Registration closed'),
        ('neet-mds', 'NEET MDS 2027', 'DENTAL PG', 'Expected early 2027', _E,
         'NBE test for MDS admissions at dental colleges.', '2027-02-01', '2027-02-28', None),
        ('fmge', 'FMGE', 'FOREIGN MED', 'Jun & Dec sessions (expected)', _E,
         'Screening test for Indian citizens with foreign medical degrees who wish to practise in India.', '2027-06-01', '2027-06-30', None),
        ('aiapget', 'AIAPGET 2027', 'AYUSH PG', 'Jul 2027 (expected)', _E,
         'All India AYUSH Post Graduate Entrance Test.', '2027-07-01', '2027-07-31', None),
    ]},
    {'key': 'law', 'title': 'Law Entrance Exams', 'col': 'left', 'grad': '#6B3FA0,#4E2C80', 'dot': '#c09af0', 'exams': [
        ('clat', 'CLAT 2027 (NLUs)', 'LAW', 'Sunday 6 Dec 2026, 2–4 pm', _C,
         'Announced by the Consortium of NLUs (consortiumofnlus.ac.in). Offline mode; syllabus and pattern unchanged. Registration ran until 31 Oct 2026.', '2026-12-06', '2026-12-06', 'Registration closes 31 Oct'),
        ('ailet', 'AILET 2027 (NLU Delhi)', 'LAW', 'Sunday 13 Dec 2026, 2–4 pm', _C,
         'NLU Delhi\'s own entrance test, separate from CLAT; applications from 7 Aug 2026 (closing date reported ~10 Nov). Confirm on nationallawuniversitydelhi.in. Members: see the Law 2027 roadmap.', '2026-12-13', '2026-12-13', 'Separate application'),
        ('slat', 'SLAT 2027 (Symbiosis)', 'LAW', '19 & 26 Dec 2026 (reported)', _T,
         'Computer-based tests reported for 19 and 26 Dec 2026; registration reported to close ~4 Dec; results ~12 Jan 2027. Confirm on slat-test.org.', '2026-12-19', '2026-12-26', 'Reported — verify'),
        ('lsat', 'LSAT India 2027', 'LAW', 'Expected Jan & May 2027', _E,
         'Accepted by many private law schools; check lsatindia.in.', '2027-01-01', '2027-01-31', None),
        ('mh-law', 'MH CET Law 2027', 'STATE LAW', 'Expected Apr 2027', _E,
         'Maharashtra state law entrance for 3-year and 5-year LLB programmes.', '2027-04-01', '2027-04-30', None),
        ('lawcet', 'AP / TS LAWCET 2027', 'STATE LAW', 'Expected May 2027', _E,
         'Law entrance for Andhra Pradesh and Telangana state law colleges.', '2027-05-01', '2027-05-31', None),
        ('cuet-pg', 'CUET PG 2027 (incl. LLM)', 'PG', 'March 2027', _T,
         'Listed in NTA\'s exam calendar across several March 2027 clusters; subject-wise dates follow in the bulletin.', '2027-03-01', '2027-03-31', 'NTA calendar · provisional'),
    ]},
    {'key': 'comm', 'title': 'Commerce / Management', 'col': 'right', 'grad': '#C47A00,#9B5E00', 'dot': '#ffd070', 'exams': [
        ('cat', 'CAT 2026 (IIMs & MBA)', 'MBA', 'Sunday 29 Nov 2026 · 3 sessions', _C,
         'Convened by IIM Indore. Registration has closed. Admit card from about 4 Nov 2026; a CAT score is valid until 31 Dec 2027. See our CAT page for details.', '2026-11-29', '2026-11-29', 'Official: iimcat.ac.in'),
        ('xat', 'XAT 2027 (XLRI)', 'MBA', 'Sunday 3 Jan 2027, 2–5 pm', _C,
         'Announced by XLRI (xatonline.in). Computer-based, single session. Registration until 6 Dec 2026; admit card from 20 Dec (tentative).', '2027-01-03', '2027-01-03', 'Register by 6 Dec'),
        ('snap', 'SNAP 2026 (Symbiosis)', 'MBA', '13, 19 & 26 Dec 2026 (3 tests)', _C,
         'Test dates per snaptest.org. Up to three attempts; best score counts. Registration reported to close 25 Nov; result reported for 12 Jan 2027. Apply separately to each Symbiosis institute.', '2026-12-13', '2026-12-26', 'Official: snaptest.org'),
        ('nmat', 'NMAT by GMAC 2026–27', 'MBA', '2 Nov – 20 Dec 2026 window', _T,
         'Multiple attempts within the testing window; you choose the score to send. Window and deadlines as reported — one report says registration was extended to 25 Oct; confirm on mba.com.', '2026-11-02', '2026-12-20', 'Reported — verify'),
        ('iift', 'IIFT MBA (IB) 2027–29', 'MBA', 'Via CAT 2026 · apply by 25 Nov 2026', _T,
         'IIFT is reported to shortlist the 2027–29 MBA (IB) and MBA (BA) intake on CAT 2026 scores rather than a separate NTA test. Applications opened 12 Oct and close 25 Nov 2026; confirm on iift.ac.in.', '2026-11-29', '2026-11-29', 'Uses CAT 2026 score'),
        ('cmat', 'CMAT 2027 (NTA)', 'MBA', '7 Feb 2027', _T,
         'From NTA\'s exam calendar of 16 Sep 2026 (provisional).', '2027-02-07', '2027-02-07', 'NTA calendar · provisional'),
        ('tissnet', 'TISSNET 2027', 'SOCIAL SCIENCE', 'Expected Jan 2027', _E,
         'Tata Institute of Social Sciences entrance for MA / MBA-type programmes.', '2027-01-01', '2027-01-31', None),
        ('ca', 'CA / CS / CMA Foundation', 'PROFESSIONAL', 'Jun & Dec sessions (expected)', _E,
         'Foundation levels of ICAI, ICSI and ICMAI; check each institute for its exact dates and registration windows.', '2027-06-01', '2027-06-30', None),
        ('nimcet', 'NIMCET 2027 (MCA at NITs)', 'MCA', 'Expected May 2027', _E,
         'Common entrance for MCA at the NITs; mathematics-heavy.', '2027-05-01', '2027-05-31', None),
    ]},
    {'key': 'sci', 'title': 'Science / Research', 'col': 'right', 'grad': '#0E7C8B,#085F6B', 'dot': '#7de8f0', 'exams': [
        ('jam', 'JAM 2027 (IIT M.Sc)', 'IIT MSC', 'Sunday 14 Feb 2027', _C,
         'Joint Admission Test for M.Sc programmes at IITs and IISc, organised by IIT Kharagpur (jam.iitkgp.ac.in). Registration (extended) closes 22 Oct 2026; results 18 Mar 2027.', '2027-02-14', '2027-02-14', 'Registration closes 22 Oct'),
        ('jest', 'JEST 2027', 'RESEARCH', 'Expected Apr 2027', _E,
         'Screening test for PhD programmes in physics and theoretical computer science at leading research institutes. Applications expected around February 2027 on jest.org.in.', '2027-04-01', '2027-04-30', None),
        ('tifr', 'TIFR GS 2027', 'RESEARCH', 'Sunday 13 Dec 2026', _C,
         'Tata Institute of Fundamental Research Graduate School test. Per the TIFR GS-2027 advertisement, applications close 25 Oct 2026, 11 pm; hall tickets around mid-November.', '2026-12-13', '2026-12-13', 'Apply by 25 Oct'),
        ('nest', 'NEST 2027', 'NISER / CEBS', 'First week of Jun 2027', _T,
         'Entrance for NISER and UM-DAE CEBS integrated M.Sc programmes. Tentative calendar; confirm on the official site.', '2027-06-01', '2027-06-07', None),
        ('iat', 'IISER IAT 2027', 'IISER', 'Early Jun 2027 (expected)', _E,
         'Aptitude test for the IISERs; the notification is expected around February 2027.', '2027-06-01', '2027-06-10', None),
        ('isi', 'ISI Admission 2027', 'ISI', 'Notice ~Feb 2027 · test ~May 2027', _E,
         'Indian Statistical Institute entrance (2026 test: 10 May); official notice not yet out.', '2027-05-01', '2027-05-31', None),
        ('ugee', 'UGEE 2027 (IIIT Hyderabad)', 'RESEARCH', 'Expected May 2027', _E,
         'IIIT Hyderabad undergraduate entrance (2026: 2 May).', '2027-05-01', '2027-05-31', None),
        ('csir-net', 'CSIR-UGC NET', 'JRF / LECTURESHIP', '19, 22 & 27 Dec 2026 (reported)', _T,
         'Joint CSIR-UGC NET; science subjects. NTA\'s notification of 7 Oct 2026 is reported to set the test for 19, 22 and 27 Dec (the earlier calendar said 20–21 Dec). Apply by 5 Nov (late fee 6–9 Nov); corrections 10–12 Nov. Confirm on csirnet.nta.nic.in.', '2026-12-19', '2026-12-27', 'Reported — verify'),
    ]},
    {'key': 'design', 'title': 'Design / Architecture', 'col': 'right', 'grad': '#1A6B3A,#104D28', 'dot': '#60d090', 'exams': [
        ('uceed', 'UCEED 2027 (IIT B.Des)', 'DESIGN', 'Sunday 17 Jan 2027, 9 am–12 noon', _C,
         'IIT Bombay (uceed.iitb.ac.in). Registration until 31 Oct 2026 (late fee until 6 Nov, 5 pm). Results 6 Mar 2027; separate B.Des application 15 Mar; admission rounds from 21 Apr. Members: see the UCEED 2027 roadmap.', '2027-01-17', '2027-01-17', 'Register by 31 Oct'),
        ('ceed', 'CEED 2027 (IIT M.Des)', 'DESIGN PG', 'Sunday 17 Jan 2027, 9 am–12 noon', _C,
         'IIT Bombay (ceed.iitb.ac.in), same day as UCEED. Registration until 31 Oct 2026 (late fee until 6 Nov).', '2027-01-17', '2027-01-17', 'Register by 31 Oct'),
        ('nid-prelims', 'NID DAT 2027 — Prelims', 'DESIGN', '20 Dec 2026', _C,
         'Per the NID Admissions Handbook 2027–28: one application (till 30 Nov 2026) covers Prelims and Mains; Prelims result on 16 Mar 2027. See our NID page.', '2026-12-20', '2026-12-20', 'Apply by 30 Nov'),
        ('nid-mains', 'NID DAT 2027 — Mains', 'DESIGN', 'After 16 Mar 2027 (date awaited)', _E,
         'Studio Sensitivity Test plus In-Person Sensitivity Test for shortlisted candidates; dates not yet announced.', None, None, None),
        ('nift', 'NIFT 2027', 'FASHION / DESIGN', 'Sunday 10 Jan 2027 (UG & PG)', _T,
         'NTA opened NIFT 2027 registration on 16 Oct 2026 (exams.nta.nic.in/niftee); one application covers all campuses. Apply by 16 Nov (late fee until 21 Nov); corrections 22–25 Nov; admit card about 4 Jan 2027. Confirm on nift.ac.in.', '2027-01-10', '2027-01-10', 'Apply by 16 Nov'),
    ]},
    {'key': 'state', 'title': 'State-Level Exams', 'col': 'right', 'grad': '#B05A00,#883F00', 'dot': '#ffad60', 'exams': [
        ('tnea', 'TNEA 2027 (Tamil Nadu)', 'STATE · TN', 'Registration ~May 2027 (expected)', _E,
         'No entrance exam — your Class 12 marks decide the rank. Counselling follows in July–August. See our TNEA pages.', '2027-05-01', '2027-05-31', 'No exam — Class 12 marks'),
        ('mht-cet', 'MHT CET 2027 (Maharashtra)', 'STATE · MH', 'Apr–May 2027 (expected)', _E,
         'PCM / PCB groups. Dates come from the CET Cell, Maharashtra.', '2027-04-01', '2027-05-31', None),
        ('wbjee', 'WBJEE 2027 (West Bengal)', 'STATE · WB', 'Late Apr – early May 2027 (expected)', _E,
         'Offline format. Check wbjeeb.nic.in.', '2027-04-20', '2027-05-10', None),
        ('keam', 'KEAM 2027 (Kerala)', 'STATE · KL', 'Apr–May 2027 (expected)', _E,
         'Conducted by CEE Kerala for engineering and other professional courses.', '2027-04-01', '2027-05-31', None),
        ('kcet', 'KCET 2027 (Karnataka)', 'STATE · KA', 'April 2027 (expected)', _E,
         'Karnataka CET for government and aided engineering seats; KEA publishes the schedule.', '2027-04-01', '2027-04-30', None),
        ('comedk', 'COMEDK UGET 2027', 'STATE · KA', 'Apr–May 2027 (expected)', _E,
         'Private colleges in Karnataka; separate from KCET (2026: 9 May).', '2027-04-15', '2027-05-31', None),
        ('eapcet', 'TG-EAPCET / AP-EAPCET 2027', 'STATE · TG/AP', 'May 2027 (expected)', _E,
         'Telangana and Andhra Pradesh engineering entrance tests (2026: 9–18 May).', '2027-05-01', '2027-05-31', None),
        ('gujcet', 'GUJCET 2027 (Gujarat)', 'STATE · GJ', 'Mar 2027 (expected)', _E,
         'GSEB test for Gujarat engineering colleges (2026: 29 Mar).', '2027-03-01', '2027-03-31', None),
        ('uptac', 'UPTAC / AKTU 2027 (UP)', 'STATE · UP', 'Counselling ~Jun 2027 (expected)', _E,
         'Uttar Pradesh engineering admissions use your JEE Main score; there is no separate UPSEE.', '2027-06-01', '2027-06-30', 'Via JEE Main score'),
        ('ojee', 'OJEE 2027 (Odisha)', 'STATE · OD', 'May 2027 (expected)', _E,
         'Odisha Joint Entrance Examination (2026: 4–9 May).', '2027-05-01', '2027-05-31', None),
        ('bcece', 'BCECE / UGEAC 2027 (Bihar)', 'STATE · BR', 'Apr–Jun 2027 (expected)', _E,
         'Bihar engineering admissions; confirm the current route on the Bihar board website.', '2027-04-01', '2027-06-30', None),
    ]},
    {'key': 'nri', 'title': 'NRI Routes & Private Institutes', 'col': 'right', 'grad': '#4A5060,#32383F', 'dot': '#aab0c0', 'exams': [
        ('dasa', 'DASA / CIWG 2027', 'NRI ROUTE', 'Jun–Aug 2027 (expected)', _E,
         'Direct Admission of Students Abroad / CIWG for NITs, IIITs and GFTIs (via SAT or JEE Main). The 2027 schedule is not yet announced. EduAakashaA specialises in this route.', '2027-06-01', '2027-08-15', 'Our specialty'),
        ('nri-quota', 'Private & state NRI quota seats', 'NRI QUOTA', 'Jun–Sep 2027 (varies by college)', _E,
         'Many private colleges reserve NRI seats with separate fees and rules; each college publishes its own window.', '2027-06-01', '2027-09-30', 'Varies by college'),
        ('aeee', 'AEEE 2027 (Amrita)', 'INSTITUTE', '15 Apr – 7 May 2027', _C,
         'Announced by Amrita Vishwa Vidyapeetham; registration opens in November 2026. See our AEEE page.', '2027-04-15', '2027-05-07', 'Registration from Nov 2026'),
        ('bitsat', 'BITSAT 2027', 'INSTITUTE', 'Registration from Dec 2026 · sessions Apr–Jun 2027', _E,
         'BITS Pilani has announced a December registration start; session dates are awaited.', '2027-04-01', '2027-06-15', 'Dates awaited'),
        ('viteee', 'VITEEE 2027', 'INSTITUTE', '27 Apr – 2 May 2027 (tentative)', _T,
         'Per viteee.vit.ac.in: applications 20 Oct 2026 – 31 Mar 2027; admit card 25–30 Apr; the number of exam days varies by city; results and counselling from the second week of May. VIT marks these dates tentative. See our VITEEE page for NRI details.', '2027-04-27', '2027-05-02', 'Apply by 31 Mar 2027'),
        ('srmjeee', 'SRMJEEE 2027', 'INSTITUTE', 'Apr / Jun / Jul 2027 phases (expected)', _E,
         'Registration expected from November 2026.', '2027-04-01', '2027-07-15', None),
        ('met', 'MET — Manipal 2027', 'INSTITUTE', 'Not announced (2026: Apr & May)', _E,
         'Manipal Institute of Technology entrance; dates not yet released.', None, None, None),
        ('kiitee', 'KIITEE 2027', 'INSTITUTE', 'Not announced (2026: Apr & Jun)', _E,
         'KIIT Bhubaneswar entrance; dates not yet released.', None, None, None),
    ]},
]

MILESTONES = [
    ('OCT 2026', 'JEE Main registration expected · TIFR GS closes 25 Oct · UCEED / CEED registration closes 31 Oct'),
    ('NOV 2026', 'INI-CET (1 Nov) · NIFT closes 16 Nov · CAT (29 Nov) · NID registration closes 30 Nov · AEEE & SRMJEEE registration expected'),
    ('DEC 2026', 'CLAT (6 Dec) · TIFR GS & AILET (13 Dec) · SNAP (13, 19, 26 Dec) · NID DAT Prelims (20 Dec) · BITSAT registration expected'),
    ('JAN 2027', 'XAT (3 Jan) · NIFT (10 Jan) · UCEED & CEED (17 Jan) · JEE Main Session 1 (22–30 Jan, provisional)'),
    ('FEB 2027', 'GATE (6, 7, 13, 14, 20, 21 Feb) · CMAT (7 Feb, provisional) · JAM (14 Feb)'),
    ('MAR 2027', 'CUET PG (provisional) · NID Prelims result (16 Mar)'),
    ('APR 2027', 'JEE Main Session 2 · AEEE (from 15 Apr) · state CETs begin'),
    ('MAY 2027', 'JEE Advanced · NEET UG · CUET UG · COMEDK / EAPCET (all expected)'),
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
# Application / deadline milestones (checked 22 Oct 2026). kind: open | close | late | admit | result | other
# status as above. A date of None means "announced as pending". Expected dates never make an application show as "open now".
# --------------------------------------------------------------------------- #
KIND_LABEL = {'open': 'Applications open', 'close': 'Applications close', 'late': 'Last date with late fee', 'admit': 'Admit card',
              'result': 'Result', 'other': 'Next step'}
KIND_ICON = {'open': '▶', 'close': '⏰', 'late': '⏳', 'admit': '🎫', 'result': '✅', 'other': '📌'}
DEADLINES = {
    'uceed': [('open', '2026-10-01', _C, 'Registration (regular fee) — official'), ('close', '2026-10-31', _C, None),
              ('late', '2026-11-06', _T, 'Until 5 pm — reported; confirm on the site'), ('admit', '2027-01-01', _T, 'From this date — reported'),
              ('result', '2027-03-06', _C, None), ('other', '2027-03-15', _C, 'Separate B.Des application (official)'), ('other', '2027-04-21', _C, 'Admission rounds begin (official)')],
    'ceed': [('open', '2026-10-01', _T, 'Reported with UCEED'), ('close', '2026-10-31', _T, None), ('late', '2026-11-06', _T, 'Reported')],
    'clat': [('open', '2026-08-03', _T, 'Announced by the Consortium (reported)'), ('close', '2026-10-31', _T, 'No extension confirmed'), ('result', None, _E, 'Date awaited')],
    'ailet': [('open', '2026-08-07', _T, 'Announced by NLU Delhi (reported)'), ('close', '2026-11-10', _T, 'Reported by several sources — confirm'),
              ('admit', '2026-11-30', _E, 'About this date'), ('result', '2026-12-22', _E, 'Fourth week of December')],
    'slat': [('open', '2026-08-01', _T, 'Opened in August (exact day not stated)'), ('close', '2026-12-04', _T, 'Reported'),
             ('admit', '2026-12-11', _T, 'Test 1 (Test 2: 18 Dec)'), ('result', '2027-01-12', _T, 'Reported')],
    'nid-prelims': [('open', '2026-09-10', _C, 'NID Handbook 2027–28'), ('close', '2026-11-30', _C, None), ('admit', '2026-12-10', _C, 'From 4 pm'),
                    ('result', '2027-03-16', _C, 'Re-totalling 16–17 Mar')],
    'cat': [('open', '2026-08-03', _C, None), ('close', '2026-09-22', _C, 'Extended from 15 Sep'), ('admit', '2026-11-04', _C, 'Until the exam'),
            ('result', None, _E, 'Date awaited — reports differ (late Dec to Jan)')],
    'gate': [('open', '2026-09-02', _T, 'Reported'), ('close', '2026-09-27', _T, 'Regular deadline'), ('late', '2026-10-05', _T, 'Reported'),
             ('result', '2027-03-19', _T, 'Reported by IIT Madras coverage')],
    'jee-main-s1': [('open', '2026-10-25', _E, 'Expected late October'), ('close', '2026-11-25', _E, 'About a month later'), ('result', '2027-02-12', _E, 'About 12 Feb')],
    'cuet-ug': [('open', '2027-01-15', _E, 'Notification expected ~January')],
    'aeee': [('open', '2026-11-01', _E, 'Registration opens in November')],
    'bitsat': [('open', '2026-12-01', _T, 'BITS announced December (tentative)')],
    'srmjeee': [('open', '2026-11-01', _E, 'Expected from November')],
    'nift': [('open', '2026-10-16', _T, 'NTA notification (reported)'), ('close', '2026-11-16', _T, None), ('late', '2026-11-21', _T, 'Late fee'),
             ('admit', '2027-01-04', _T, 'Reported')],
    'xat': [('close', '2026-12-06', _C, 'xatonline.in'), ('admit', '2026-12-20', _T, 'Tentative per XLRI')],
    'snap': [('close', '2026-11-25', _T, 'Reported'), ('result', '2027-01-12', _T, 'Reported')],
    'nmat': [('other', '2026-11-02', _T, 'Testing window opens (reported)')],
    'iift': [('open', '2026-10-12', _T, 'Reported'), ('close', '2026-11-25', _T, 'Reported — confirm on iift.ac.in')],
    'ini-cet': [('admit', '2026-10-26', _T, 'AIIMS tentative calendar'), ('result', '2026-11-07', _T, 'Expected')],
    'jam': [('close', '2026-10-22', _C, 'Extended deadline — jam.iitkgp.ac.in'), ('result', '2027-03-18', _C, None)],
    'tifr': [('close', '2026-10-25', _C, 'Until 11 pm — TIFR advertisement')],
    'viteee': [('open', '2026-10-20', _C, 'viteee.vit.ac.in'), ('close', '2027-03-31', _T, 'Tentative per VIT'),
               ('admit', '2027-04-25', _T, '25–30 Apr, tentative per VIT')],
    'csir-net': [('open', '2026-10-07', _T, 'Reported'), ('close', '2026-11-05', _T, 'Reported'), ('late', '2026-11-09', _T, 'Reported')],
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
