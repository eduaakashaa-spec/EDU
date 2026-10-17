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

VERIFIED = date(2026, 10, 16)

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
        ('neet-pg', 'NEET PG 2027', 'MEDICINE PG', 'Expected Mar 2027', _E,
         'Conducted by NBE for MD / MS / diploma / DNB. Check nbe.edu.in.', '2027-03-01', '2027-03-31', None),
        ('ini-cet', 'INI-CET (AIIMS PG)', 'PG AIIMS', 'Jan & Jul sessions (expected)', _E,
         'Institute of National Importance PG test — AIIMS, JIPMER, PGIMER, NIMHANS.', '2027-01-15', '2027-01-31', None),
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
        ('xat', 'XAT 2027 (XLRI)', 'MBA', 'Early Jan 2027 (expected)', _E,
         'Held on a Sunday in early January; the official date comes with the XLRI notification.', '2027-01-03', '2027-01-03', None),
        ('snap', 'SNAP 2026 (Symbiosis)', 'MBA', 'Dec 2026 (3 slots, expected)', _E,
         'Up to three attempts; best score counts. Apply separately to each Symbiosis institute.', '2026-12-01', '2026-12-31', None),
        ('nmat', 'NMAT by GMAC 2026–27', 'MBA', 'Oct 2026 – Jan 2027 window', _E,
         'Multiple attempts within the testing window; you choose the score to send.', '2026-10-01', '2027-01-31', None),
        ('iift', 'IIFT 2027', 'MBA', 'Expected Nov–Dec 2026', _E,
         'Foreign-trade MBA entrance conducted by NTA.', '2026-11-25', '2026-12-31', None),
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
        ('jam', 'JAM 2027 (IIT M.Sc)', 'IIT MSC', 'Expected Feb 2027', _E,
         'Joint Admission Test for M.Sc programmes at IITs and IISc.', '2027-02-01', '2027-02-28', None),
        ('jest', 'JEST 2027', 'RESEARCH', 'Expected Feb 2027', _E,
         'Screening test for PhD programmes in physics and theoretical computer science at leading research institutes.', '2027-02-01', '2027-02-28', None),
        ('tifr', 'TIFR GS 2027', 'RESEARCH', 'Expected Dec 2026', _E,
         'Tata Institute of Fundamental Research Graduate School test.', '2026-12-01', '2026-12-31', None),
        ('nest', 'NEST 2027', 'NISER / CEBS', 'First week of Jun 2027', _T,
         'Entrance for NISER and UM-DAE CEBS integrated M.Sc programmes. Tentative calendar; confirm on the official site.', '2027-06-01', '2027-06-07', None),
        ('iat', 'IISER IAT 2027', 'IISER', 'Early Jun 2027 (expected)', _E,
         'Aptitude test for the IISERs; the notification is expected around February 2027.', '2027-06-01', '2027-06-10', None),
        ('isi', 'ISI Admission 2027', 'ISI', 'Notice ~Feb 2027 · test ~May 2027', _E,
         'Indian Statistical Institute entrance (2026 test: 10 May); official notice not yet out.', '2027-05-01', '2027-05-31', None),
        ('ugee', 'UGEE 2027 (IIIT Hyderabad)', 'RESEARCH', 'Expected May 2027', _E,
         'IIIT Hyderabad undergraduate entrance (2026: 2 May).', '2027-05-01', '2027-05-31', None),
        ('csir-net', 'CSIR-UGC NET', 'JRF / LECTURESHIP', 'Dec 2026 (20–21 Dec, NTA calendar)', _T,
         'Joint CSIR-UGC NET listed in NTA\'s calendar for 20–21 Dec 2026; science subjects.', '2026-12-20', '2026-12-21', 'NTA calendar · provisional'),
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
        ('nift', 'NIFT 2027', 'FASHION / DESIGN', 'Jan–Feb 2027 (sources differ)', _T,
         'NTA\'s calendar lists 10 Jan; other reports say the second week of February. Registration expected from December 2026. Confirm on nift.ac.in.', '2027-01-10', '2027-02-14', 'NTA calendar · provisional'),
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
        ('viteee', 'VITEEE 2027', 'INSTITUTE', 'Late Apr – early May 2027 (expected)', _E,
         'VIT notification not yet published. See our VITEEE page for NRI details.', '2027-04-20', '2027-05-10', None),
        ('srmjeee', 'SRMJEEE 2027', 'INSTITUTE', 'Apr / Jun / Jul 2027 phases (expected)', _E,
         'Registration expected from November 2026.', '2027-04-01', '2027-07-15', None),
        ('met', 'MET — Manipal 2027', 'INSTITUTE', 'Not announced (2026: Apr & May)', _E,
         'Manipal Institute of Technology entrance; dates not yet released.', None, None, None),
        ('kiitee', 'KIITEE 2027', 'INSTITUTE', 'Not announced (2026: Apr & Jun)', _E,
         'KIIT Bhubaneswar entrance; dates not yet released.', None, None, None),
    ]},
]

MILESTONES = [
    ('OCT 2026', 'JEE Main registration expected · UCEED / CEED registration closes 31 Oct'),
    ('NOV 2026', 'CAT (29 Nov) · NID registration closes 30 Nov · AEEE & SRMJEEE registration expected'),
    ('DEC 2026', 'CLAT (6 Dec) · NID DAT Prelims (20 Dec) · BITSAT & NIFT registration expected'),
    ('JAN 2027', 'UCEED & CEED (17 Jan) · JEE Main Session 1 (22–30 Jan, provisional)'),
    ('FEB 2027', 'GATE (6, 7, 13, 14, 20, 21 Feb) · CMAT (7 Feb, provisional)'),
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


def timeline_data():
    """Flat list for the Timeline / By-month / Calendar views (rendered client-side from one JSON blob)."""
    out = []
    for cat, row in all_exams():
        id_, name, badge, when, status, desc, start, end, note = row
        out.append({'id': id_, 'name': name, 'cat': cat['key'], 'catTitle': cat['title'], 'color': cat['grad'].split(',')[0],
                    'status': status, 'start': start, 'end': end or start, 'when': when, 'badge': badge, 'desc': desc, 'note': note})
    return out
