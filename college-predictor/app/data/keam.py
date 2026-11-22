"""KEAM (Kerala engineering) and CEE Kerala allotment: facts behind /keam-analytics, checked 22 Nov 2026.

Each fact says whether it is official (CEE Kerala, DHSE) or reported (news and coaching sites). Last ranks are in app/data/keam/lastranks.json,
built by tools/keam/build_lastranks.py from the official CEE last-rank PDFs (2025 and 2026, Phase 1 and Phase 2). CEE's 2024 pages were not reachable.
Update this file when CEE publishes the KEAM 2027 prospectus, the exam dates or new last ranks.
"""

VERIFIED = '22 Nov 2026'
O, R, E = 'Official', 'Reported', 'Expected'

SRC = {
    'cee': 'https://cee.kerala.gov.in/',
    'lr2026': 'https://cee.kerala.gov.in/keam2026/last_rank',
    'lr2025': 'https://cee.kerala.gov.in/keam2025/last_rank',
    'dates2027': 'https://www.shiksha.com/news/engineering-keam-2027-exam-date-announced-reports-claim-exam-to-be-held-from-april-21-to-26-blogId-246392',
    'plus2': 'https://news.careers360.com/kerala-board-exams-2027-timetable-out-sslc-datesheet-plus-1-plus-2-10th-12th-subject-wise-schedule',
    'hc': 'https://www.barandbench.com/news/kerala-high-court-upholds-new-keam-2026-rank-list-formula-for-equalising-cbse-icse-and-state-board-marks',
    'pattern': 'https://engineering.careers360.com/articles/keam-exam-pattern',
}

# (id, title, start, end, status, detail)
DATES = [
    ('plus2-prac', 'Kerala Plus Two practical exams', '2027-01-25', '2027-02-20', R, 'From 25 Jan 2027 as reported with the DHSE timetable of 12 Nov 2026; schools fix the days.'),
    ('keam-apply', 'KEAM 2027 online application', '2027-01-05', '2027-02-06', E, 'Expected in January; in 2026 applications ran 5 Jan – 6 Feb. Apply only on cee.kerala.gov.in.'),
    ('plus2-theory', 'Kerala Plus Two (Higher Secondary) theory exams', '2027-03-02', '2027-03-30', R, 'DHSE timetable released 12 Nov 2026 (reported). Other boards follow their own dates.'),
    ('keam-exam', 'KEAM 2027 engineering exam (CBT)', '2027-04-21', '2027-04-26', R, 'Reported, not yet confirmed by CEE Kerala. In 2026 the engineering CBT ran 17–22 Apr.'),
    ('keam-score', 'KEAM score and Plus Two marks upload', '2027-05-15', '2027-06-10', E, 'Candidates upload their Class 12 marks on the CEE portal before the rank list (2026 pattern).'),
    ('keam-rank', 'KEAM engineering rank list', '2027-06-20', '2027-06-30', E, 'In 2026 the rank list came on 26–27 Jun with about 67,500 candidates (reported).'),
    ('allot-1', 'Allotment Phase 1', '2027-07-01', '2027-07-12', E, 'In 2026 the Phase 1 last ranks were published on 8 Jul.'),
    ('allot-2', 'Allotment Phase 2', '2027-07-15', '2027-07-25', E, 'In 2026 the Phase 2 last ranks were published on 20 Jul.'),
    ('allot-3', 'Allotment Phase 3 and later rounds', '2027-07-28', '2027-08-15', E, 'In 2026 Phase 3 results came on 4 Aug (reported); stray and spot rounds follow.'),
]

PATTERN = [
    ('Questions', '150 multiple-choice questions with five options: Mathematics 75, Physics 45, Chemistry 30'),
    ('Marks', '+4 for a right answer, −1 for a wrong one: Mathematics 300, Physics 180, Chemistry 120; 600 in all'),
    ('Mode and time', 'Computer-based test, 3 hours, in several sessions; scores are normalised across sessions'),
    ('Qualifying', 'At least 10 normalised marks in the entrance exam to enter the rank list (reported)'),
    ('Engineering rank', '50% normalised KEAM score (out of 300) + 50% normalised Class 12 Physics, Chemistry and Mathematics marks (out of 300) = 600'),
    ('Board normalisation (2026)', 'The highest mark in each board is taken as 100% and others are scaled to it; the Kerala High Court upheld this formula in 2026'),
]

ELIGIBILITY = [
    ('Subjects', 'Pass Class 12 with Physics and Mathematics compulsory, plus Chemistry (or Computer Science, Biotechnology or Biology where the prospectus allows).'),
    ('Minimum marks', 'At least 45% in Physics, Chemistry and Mathematics together; 40% for SEBC candidates (per the prospectus) and a pass for SC and ST candidates. Check the 2027 prospectus.'),
    ('Entrance', 'Write KEAM engineering and get at least 10 normalised marks to enter the rank list.'),
    ('Nativity', 'Keralites compete for State Merit and community seats; Non-Keralite Category I and II candidates are eligible for State Merit seats only (no reservation).'),
    ('Class 12 marks', 'Upload your board marks on the CEE portal when asked: without them you are not ranked, because half of the rank comes from them.'),
    ('NRI quota', 'Self-financing colleges fill NRI seats themselves, outside the CEE rank list.'),
]

# community codes printed in the last-rank tables
CATS = [
    ('SM', 'State Merit', 'Open merit seats for everyone in the rank list'),
    ('EZ', 'Ezhava', 'SEBC: Ezhava, Thiyya, Billava'),
    ('MU', 'Muslim', 'SEBC'),
    ('BH', 'Other Backward Hindu', 'SEBC'),
    ('LA', 'Latin Catholic and Anglo-Indian', 'SEBC'),
    ('DV', 'Dheevara', 'SEBC: Dheevara and related communities'),
    ('VK', 'Viswakarma', 'SEBC: Viswakarma and related communities'),
    ('BX', 'Other Backward Christian', 'SEBC'),
    ('KN', 'Kusavan', 'SEBC: Kusavan, Kulalan and related communities'),
    ('KU', 'Kudumbi', 'SEBC'),
    ('SC', 'Scheduled Caste', ''),
    ('ST', 'Scheduled Tribe', ''),
    ('EW', 'EWS', 'Economically Weaker Sections (general category)'),
]
OTHER_CATS = 'The last column lists smaller quotas as code:rank, for example FW (fee waiver) and PD (persons with disability), as printed by CEE.'
RESERVATION_NOTE = ('Government and aided seats are split between State Merit and reservation for SEBC communities (EZ, MU, BH, LA, DV, VK, BX, KN, KU), '
                    'SC, ST and EWS, as set out in the KEAM prospectus. Self-financing colleges have their own seat shares. A reserved candidate is considered '
                    'for State Merit first, then for the community seat.')

TYPES = {
    'G': ('Government and aided', 'Government colleges and aided colleges such as TKM Kollam and NSS Palakkad: the lowest fees'),
    'N': ('Government-controlled self-financing', 'CAPE, IHRD, LBS and university colleges: higher fees than government, lower than private'),
    'S': ('Private self-financing', 'Private colleges: the highest fees; some seats are management or NRI quota outside CEE'),
}

STATS = [
    ('Engineering rank list 2026', 'About 67,500 candidates (reported, 26–27 Jun 2026)'),
    ('Seats allotted in Phase 2, 2026', '28,104 engineering seats (reported)'),
    ('Seats allotted in Phase 3, 2026', '27,544 engineering seats (reported)'),
]
RANKLIST_2026 = 67505   # reported size of the 2026 engineering rank list, used to turn a rank into a position

# NIRF India Rankings 2025, Engineering: KEAM colleges in the list (app/data/files/nirf_full.json)
NIRF = {'TVE': '101–150'}
NIRF_NOT_KEAM = ['NIT Calicut (21, JEE Main via JoSAA)', 'IIST Thiruvananthapuram (61, JEE Advanced)', 'IIT Palakkad (64, JEE Advanced)']

FAMILY_NAMES = {'CSE': 'Computer / CSE', 'AI': 'AI, ML & Data Science', 'IT': 'Information Technology', 'ENTC': 'Electronics & Communication', 'ELEC': 'Electrical',
                'MECH': 'Mechanical & allied', 'CIVIL': 'Civil', 'CHEM': 'Chemical, bio & food', 'OTHER': 'Other'}

BRANCH_GUIDE = [
    ('CSE', 'The lowest last ranks at almost every college: in 2026 Phase 1, CET Trivandrum Computer Science closed at State Merit rank 388. Pick it at a lower-ranked college only if software is clearly your goal.'),
    ('AI', 'AI, ML and Data Science branches have grown fast and close a little behind Computer Science at the same college.'),
    ('ENTC', 'Electronics and Communication keeps both hardware and software doors open; at the top government colleges it closes within a few thousand ranks of CSE.'),
    ('ELEC', 'Electrical and Electronics suits power, energy and KSEB/PSU careers; it closes well after CSE and ECE.'),
    ('MECH', 'Mechanical and allied branches are core engineering; at government colleges they are within reach for ranks that miss CSE by a wide margin.'),
    ('CIVIL', 'Civil usually has the highest last ranks: a route into a top government college for public works, construction and government jobs.'),
]

# district of each college, keyed by college code, from the town in its name (14 districts as named in the map file)
TOWN_DISTRICT = [
    ('Thiruvananthapuram', 'Thiruvananthapuram'), ('Attingal', 'Thiruvananthapuram'), ('Muttathara', 'Thiruvananthapuram'), ('Kariavattom', 'Thiruvananthapuram'),
    ('Barton Hill', 'Thiruvananthapuram'), ('Parippally', 'Kollam'), ('Kollam', 'Kollam'), ('Kottarakkara', 'Kollam'), ('Karunagappally', 'Kollam'),
    ('Pathanapuram', 'Kollam'), ('Perumon', 'Kollam'), ('Adoor', 'Pathanamthitta'), ('Aranmula', 'Pathanamthitta'), ('Kallooppara', 'Pathanamthitta'),
    ('Thiruvalla', 'Pathanamthitta'), ('Pathanamthitta', 'Pathanamthitta'), ('Chengannur', 'Alappuzha'), ('Cherthala', 'Alappuzha'), ('Punnapra', 'Alappuzha'),
    ('Mavelikkara', 'Alappuzha'), ('Alappuzha', 'Alappuzha'), ('Palai', 'Kottayam'), ('Kidangoor', 'Kottayam'), ('Poonjar', 'Kottayam'), ('Kanjirampara', 'Kottayam'),
    ('Kottayam', 'Kottayam'), ('KOTTAYAM', 'Kottayam'), ('Thodupuzha', 'Idukki'), ('Munnar', 'Idukki'), ('Kolahalamedu', 'Idukki'), ('Idukki', 'Idukki'),
    ('Kothamangalam', 'Ernakulam'), ('Vengoor', 'Ernakulam'), ('Ettapilly', 'Ernakulam'), ('Kochi', 'Ernakulam'), ('Cochin', 'Ernakulam'), ('Ernakulam', 'Ernakulam'),
    ('Mannuthy', 'Thrissur'), ('Thrissur', 'Thrissur'), ('Thirissur', 'Thrissur'), ('Palakkad', 'Palakkad'), ('Valanchery', 'Malappuram'), ('Kuttipuram', 'Malappuram'),
    ('Kuttippuram', 'Malappuram'), ('Perinthalmanna', 'Malappuram'), ('Tavanur', 'Malappuram'), ('Malappuram', 'Malappuram'), ('Mukkam', 'Kozhikode'),
    ('Vadakara', 'Kozhikode'), ('Kozhikode', 'Kozhikode'), ('Kozhikkode', 'Kozhikode'), ('Pookode', 'Wayanad'), ('Wayanad', 'Wayanad'), ('Payyannur', 'Kannur'),
    ('Payyanur', 'Kannur'), ('Thalassery', 'Kannur'), ('Kannur', 'Kannur'), ('Trikaripur', 'Kasaragod'), ('Kasaragod', 'Kasaragod'), ('Kasargod', 'Kasaragod'),
]
REGIONS = {
    'South Kerala': ['Thiruvananthapuram', 'Kollam', 'Pathanamthitta', 'Alappuzha'],
    'Central Kerala': ['Kottayam', 'Idukki', 'Ernakulam', 'Thrissur'],
    'North Kerala': ['Palakkad', 'Malappuram', 'Kozhikode', 'Wayanad', 'Kannur', 'Kasaragod'],
}

# official website of each college, keyed by the CEE college code; only links that were found and checked are listed
SITES = {  # checked 22 Nov 2026; group or university pages where a college has no site of its own (KVASU dairy colleges, KUFOS, KMCT campuses)
    'AAE': 'https://engineering.alazharthodupuzha.org/', 'AAP': 'https://alameen.edu.in/', 'ADR': 'https://cea.ac.in/',
    'AEC': 'https://cearanmula.ac.in/', 'AIK': 'https://aisat.ac.in/', 'AJC': 'https://www.ajce.in/',
    'AME': 'https://www.rist.edu.in/', 'ASI': 'https://www.adishankara.ac.in/', 'ATP': 'https://ahalia.ac.in/',
    'AWH': 'https://awhengg.org/', 'BJK': 'https://www.bji.ac.in/', 'BMC': 'https://www.bmce.ac.in/',
    'CCE': 'https://cce.edu.in/', 'CCV': 'https://mgmtc.in/', 'CDI': 'https://www.kvasu.ac.in/college/more/10',
    'CDP': 'https://www.kvasu.ac.in/college/more/11', 'CDT': 'https://www.kvasu.ac.in/college/more/4', 'CDV': 'https://www.kvasu.ac.in/college/more/8',
    'CEA': 'https://ceattingal.ihrd.ac.in/', 'CEC': 'https://cectl.ac.in/', 'CEK': 'https://cekottarakkara.ihrd.ac.in/',
    'CEM': 'https://cemuttathara.org/', 'CEN': 'https://www.cetp.edu.in/', 'CHN': 'https://ceconline.edu/',
    'CIM': 'https://mentorcolleges.com/', 'CKC': 'https://christknowledgecity.com/', 'CMA': 'https://carmelcet.in/',
    'COU': 'https://kufos.ac.in/', 'DMC': 'https://mdit.ac.in/', 'ECE': 'https://iccscem.ac.in/',
    'EKC': 'https://ekctc.edu.in/', 'FIT': 'https://fisat.ac.in/', 'GIK': 'https://gitgroup.ac.in/',
    'HGW': 'https://holygraceengineering.com/', 'ICE': 'https://icet.ac.in/', 'IDK': 'https://gecidukki.ac.in/',
    'IES': 'https://iesce.info/', 'IGW': 'https://www.iiet.org.in/', 'JBT': 'https://jaibharathengg.com/',
    'JCE': 'https://jawaharlalcolleges.com/', 'JEC': 'https://www.jecc.ac.in/', 'JIT': 'https://www.jcmcsiit.ac.in/',
    'KCT': 'https://kcaet.kau.in/', 'KGR': 'https://ce-kgr.org/', 'KIT': 'https://www.kitsgroup.ac.in/',
    'KKE': 'https://geckkd.ac.in/', 'KMC': 'https://www.kmct.edu.in/campuses/engineering/', 'KME': 'https://www.kmeacollege.ac.in/',
    'KMI': 'https://www.kmctitm.org/', 'KMT': 'https://www.kmctemergingtechnology.org/', 'KMV': 'https://kmct.org/',
    'KMW': 'https://www.kmct.edu.in/campuses/womens-engineering/', 'KMY': 'https://www.kmctiem.org/', 'KMZ': 'https://kmct.org/',
    'KNP': 'https://ceknpy.ac.in/', 'KNR': 'https://gcek.ac.in/', 'KSD': 'https://lbscek.ac.in/',
    'KTE': 'https://www.rit.ac.in/', 'KVE': 'https://kvmce.in/', 'LBT': 'https://lbt.ac.in/',
    'LMC': 'https://lmcst.ac.in/', 'MAC': 'https://mace.ac.in/', 'MBC': 'https://www.mbcpeermade.com/',
    'MBI': 'https://mbits.ac.in/', 'MBT': 'https://mbcet.ac.in/', 'MCC': 'https://musaliarcollegeckl.com/',
    'MCE': 'https://www.marian.ac.in/', 'MCK': 'https://musaliarcollege.com/', 'MCT': 'https://mcet.ac.in/',
    'MDL': 'https://www.mec.ac.in/', 'MEA': 'https://www.meaec.edu.in/', 'MEC': 'https://www.malabarcet.ac.in/',
    'MEE': 'https://mescet.ac.in/', 'MEK': 'https://mesitam.ac.in/', 'MES': 'https://mesce.ac.in/',
    'MET': 'https://metsengg.ac.in/', 'MGC': 'https://www.mgcet.com/', 'MGE': 'https://www.mgmcet.ac.in/',
    'MGP': 'https://saintgits.org/', 'MHP': 'https://acetvm.com/', 'MLM': 'https://www.mangalam.ac.in/',
    'MLT': 'https://mitkannur.ac.in/', 'MNR': 'https://cemunnar.ac.in/', 'MUS': 'https://www.mace.edu.in/',
    'MUT': 'https://mgmits.ac.in/', 'MZC': 'https://www.mzce.ac.in/', 'NCE': 'https://ncerc.ac.in/',
    'NIE': 'https://nice.nirmalacollege.edu.in/', 'NSS': 'https://nssce.ac.in/', 'PAA': 'https://paacet.in/',
    'PEC': 'https://cepathanapuram.ac.in/', 'PJR': 'https://cep.ac.in/', 'PKD': 'https://gecskp.ac.in/',
    'PRC': 'https://www.providence.edu.in/', 'PRN': 'https://perumonec.ac.in/', 'PRP': 'https://cempunnapra.org/',
    'PTA': 'https://cek.ac.in/', 'RCE': 'https://royalcet.ac.in/', 'RET': 'https://www.rajagiritech.ac.in/',
    'RIE': 'https://www.riet.edu.in/', 'SBC': 'https://sbce.ac.in/', 'SCM': 'https://scmsgroup.org/sset/',
    'SCT': 'https://sctce.ac.in/', 'SHR': 'https://sahrdaya.ac.in/', 'SIT': 'https://sist.ac.in/',
    'SJC': 'https://sjcetpalai.ac.in/', 'SNG': 'https://sngce.ac.in/', 'SNM': 'https://snmimt.edu.in/',
    'SNP': 'https://www.snit.edu.in/', 'SPT': 'https://simat.ac.in/', 'STC': 'https://www.stthomascollege.ac.in/',
    'STI': 'https://www.stisttvm.edu.in/', 'STM': 'https://stthomaskannur.ac.in/', 'TCE': 'https://toms.ac.in/',
    'TCR': 'https://gectcr.ac.in/', 'TCT': 'https://thetrinitycollege.in/', 'TJE': 'https://www.thejusengg.com/',
    'TKI': 'https://tkmit.ac.in/', 'TKM': 'https://www.tkmce.ac.in/', 'TKR': 'https://www.cetkr.ac.in/',
    'TLY': 'https://cethalassery.ac.in/', 'TOC': 'https://tistcochin.edu.in/', 'TRV': 'https://www.gecbh.ac.in/',
    'TVE': 'https://www.cet.ac.in/', 'UCC': 'https://iet.uoc.ac.in/', 'UCE': 'https://ucet.ac.in/',
    'UCK': 'https://uck.ac.in/', 'UKP': 'https://ukfcet.ac.in/', 'UNT': 'https://uec.ac.in/',
    'VAK': 'https://vidyatcklmr.ac.in/', 'VAS': 'https://vidyaacademy.ac.in/', 'VDA': 'https://www.cev.ac.in/',
    'VIT': 'https://visat.in/', 'VJC': 'https://vjcet.org/', 'VKE': 'https://college.vkcet.com/',
    'VML': 'https://vjec.ac.in/', 'VPE': 'https://www.mahagurutech.ac.in/', 'VVT': 'https://vedavyasa.org/vvit/',
    'WYD': 'https://www.gecwyd.ac.in/', 'YCE': 'https://ycet.ac.in/',
}
SITES_MISSING = {'SNC': 'Sree Narayana Guru College of Engineering and Technology, Kannur: its site returned a server error on every check', 'TEC': 'Travancore Engineering College, Kollam: no working official site found'}
