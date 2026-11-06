"""Entrance-exam equivalency rules (generated from official notices; every rule carries its source link).
Cycle and verification dates are in CYCLE_NOTE and CHECKED. Re-check each notice when a new cycle is announced."""
QUALS = [('cbse', 'Class 12 of CBSE, CISCE or a state board'),
 ('preuniv', 'Intermediate or two-year pre-university course'),
 ('nios', 'NIOS Senior Secondary (open school)'),
 ('diploma', '3-year diploma after Class 10 (AICTE or state board)'),
 ('voc', 'Class 12 vocational (HSC Vocational)'),
 ('ib', 'IB Diploma'),
 ('cambridge', 'Cambridge A level or High School Certificate'),
 ('foreign', 'Other foreign board or US high school diploma')]
SUBJECTS = ['Physics',
 'Chemistry',
 'Mathematics',
 'Biology',
 'Biotechnology',
 'English',
 'Computer Science']
GROUPS = [('eng', 'Engineering and architecture'),
 ('med', 'Medical'),
 ('design', 'Design'),
 ('univ', 'University and law')]
CYCLE_NOTE = "Rules are read from the latest published notice of each exam (cycle shown on every exam page)."
CHECKED = {'date': '2026-11-06',
 'notes': ['A verdict of Check the notice means the official notice does not name your qualification or leaves the decision to '
           'the institute. Ask in writing and keep the reply.',
           'Equivalence certificates for foreign or unlisted boards come from the Association of Indian Universities (AIU) or '
           'the UGC. Apply early; processing can take weeks.',
           'Minimum marks differ by exam, university and category. Where a notice sets no common minimum, this page says so '
           'rather than quoting coaching-site figures.',
           'Qualifying in Class 12 in the same year is allowed by most exams, but admission needs proof of passing by the date '
           'in the brochure.']}
FRAMEWORKS = [{'source': 'https://aiu.ac.in/frontpage/equivalence-of-degree/',
  'text': 'AIU issues an Equivalence Certificate for school-level exams of foreign boards; applications are accepted online only '
          'via evaluation.aiu.ac.in. AIU has also equated some school board qualifications to Grade 10 and 12 for '
          'higher-education admission and government jobs (details are in a linked notification, not on the page). Vocational '
          'stream exams of Indian boards have an AIU equivalence list (linked PDF).',
  'title': 'Equivalence note'},
 {'source': 'https://aiu.ac.in/frontpage/equivalence-of-degree/',
  'text': 'Students who passed below Grade 10 get a Letter of Equivalence: documents are a request/application letter, '
          'transcript of last class passed, Transfer Certificate or Principal letter confirming last exam passed, and payment '
          'proof; fee Rs 1,180 online; queries to evaluation@aiu.ac.in.',
  'title': 'Equivalence note'},
 {'source': 'https://nios.ac.in/govtcircular.aspx',
  'text': 'NIOS: AIU letter EV/11(354)/91 dated 25 July 1991 granted equivalence of NOS (now NIOS) courses with those of '
          'recognised boards for admission to higher studies. CUET 2026 accepts NIOS Senior Secondary with a minimum of five '
          'subjects.',
  'title': 'Equivalence note'},
 {'source': 'https://cdnbbsr.s3waas.gov.in/s3d1a21da7bca4abff8b0b61b87597de73/uploads/2026/01/202601031633478370.pdf',
  'text': 'Diploma and others: CUET 2026 accepts an AICTE/state-technical-board diploma of at least 3 years as a qualifying '
          'exam; HSC Vocational, GCE A level, Cambridge High School Certificate, IB Diploma and NDA Joint Services Wing exam are '
          'also accepted. Foreign/unlisted boards need a UGC equivalence certificate.',
  'title': 'Equivalence note'},
 {'source': 'https://news.careers360.com/ncert-grant-equivalence-class-10-12-certificates-all-central-state-private-school-boards-through-parakh-nep-centre-replaces-aiu',
  'text': 'Press report, not confirmed on an official page: A Sept 2025 news report says the Centre assigned equivalence of '
          'Class 10/12 certificates across school boards to NCERT (via PARAKH), replacing AIU for that role. Not verified on an '
          'official page.',
  'title': 'Equivalence note'},
 {'source': 'https://www.pw.live/iit-jee/exams/jee-main-eligibility-for-foreign-boards',
  'text': 'Press report, not confirmed on an official page: Older press-reported guidance: foreign-board Class 12 needs 12 years '
          'of schooling and a pass in at least four subjects, from a board recognised by the Ministry of Education. Not verified '
          'on an official page.',
  'title': 'Other note'}]
EXAMS = [{'body': 'National Testing Agency',
  'courses': ['B.E./B.Tech'],
  'cycle': 'JEE Main 2027 bulletin (Oct 2026)',
  'group': 'eng',
  'id': 'jee-main',
  'level': 'ug',
  'name': 'JEE Main (B.E./B.Tech) 2027',
  'needs': [{'any': ['Physics'], 'label': 'Physics'},
            {'any': ['Mathematics'], 'label': 'Mathematics'},
            {'any': ['Chemistry', 'Biology', 'Biotechnology'], 'label': 'Chemistry, Biology or Biotechnology'}],
  'not_found': ['JEE Main 2026-cycle bulletin was not listed on the NTA documents page; the 2027 bulletin (Oct 2026) is used. '
                '2026-cycle year-of-appearance wording only from JoSAA 2026 (first appearance 2024/2025/2026 for NIT+).',
                'JEE Main 2027 bulletin does not state the subject combination or 50% rules for Paper 2A/2B; only JoSAA and CoA '
                'rules verified. Older JEE Main 2024 bulletin B.Arch/B.Plan 50% wording seen only via a search summary, not '
                'read.',
                'Category-wise JEE Main qualifying percentile cut-offs for JEE Advanced not extracted.',
                'State B.Arch routes (TNEA, KEAM, MHT-CET etc.) and state-specific rules not verified.',
                'JEE Advanced foreign national/OCI-PIO(F) criteria and JoSAA special institute restrictions not read.',
                "NATA brochure says only '10+2 or equivalent'; explicit acceptance of IB/Cambridge/NIOS/foreign boards for "
                'B.Arch and AIU equivalence rules not verified from AIU.',
                'NTA site returns 403 to the fetch tool; the 2027 bulletin was obtained by direct download.'],
  'quals': {'cambridge': ['yes', 'GCE A level and Cambridge High School Certificate are listed.'],
            'cbse': ['yes', 'Class 12 of any recognised central or state board is listed.'],
            'diploma': ['yes', 'An AICTE or state board diploma of at least three years is listed.'],
            'foreign': ['equiv', 'An AIU equivalence certificate is needed for any other or foreign board.'],
            'ib': ['yes', 'IB Diploma is listed.'],
            'nios': ['yes', 'NIOS Senior Secondary with at least five subjects is listed.'],
            'preuniv': ['yes', 'Intermediate or two-year pre-university is listed.'],
            'voc': ['yes', 'HSC Vocational is listed.']},
  'rules': [{'source': 'https://cdnbbsr.s3waas.gov.in/s3f8e59f4b2fe7c5705bf878bbd494ccdf/uploads/2026/10/202610241890224107.pdf',
             'text': 'Information Bulletin Ch.3 s.3.2 qualifying exams: final exam of 10+2 by any recognised Central/State Board '
                     '(CBSE, CISCE etc); Intermediate or 2-year Pre-University by recognised board or university; 2-year NDA '
                     'Joint Services Wing course; NIOS Senior Secondary with minimum 5 subjects; BOSSE Sikkim.',
             'topic': 'qualification'},
            {'source': 'https://cdnbbsr.s3waas.gov.in/s3f8e59f4b2fe7c5705bf878bbd494ccdf/uploads/2026/10/202610241890224107.pdf',
             'text': 'Also accepted: any public school/board/university exam in India or abroad recognised as 10+2 equivalent by '
                     'AIU; HSC Vocational; AICTE or State Board of Technical Education diploma of at least 3 years; GCE A level '
                     '(London/Cambridge/Sri Lanka); Cambridge High School Certificate or IB Diploma (Geneva).',
             'topic': 'qualification'},
            {'source': 'https://cdnbbsr.s3waas.gov.in/s3f8e59f4b2fe7c5705bf878bbd494ccdf/uploads/2026/10/202610241890224107.pdf',
             'text': 'Class 12 done abroad or from a board not listed needs an AIU equivalence certificate. If the Class 12 exam '
                     'is not a public exam, the candidate must have passed an earlier public (Board/Pre-University) exam.',
             'topic': 'qualification'},
            {'source': 'https://cdnbbsr.s3waas.gov.in/s3f8e59f4b2fe7c5705bf878bbd494ccdf/uploads/2026/10/202610241890224107.pdf',
             'text': 'Year of appearance (s.3.3, 2027 cycle): passed Class 12/equivalent in 2025 or 2026, or appearing in 2027. '
                     'Passed in 2024 or earlier is not eligible. Passing year = year the result was first declared pass; '
                     'improvement attempts do not change it. No age limit (s.3.1).',
             'topic': 'other'},
            {'source': 'https://cdnbbsr.s3waas.gov.in/s3f8e59f4b2fe7c5705bf878bbd494ccdf/uploads/2026/10/202610241890224107.pdf',
             'text': 'The 2027 NTA bulletin Chapter 3 states no subject combination and no minimum Class 12 percentage for '
                     "appearing; candidates must check each admitting institute's eligibility. Example in s.3.3: PCB pass in "
                     '2025 plus Maths pass in 2026 means 2025 is the passing year.',
             'topic': 'subjects'},
            {'source': 'https://cdnbbsr.s3waas.gov.in/s3f8e59f4b2fe7c5705bf878bbd494ccdf/uploads/2026/10/202610241890224107.pdf',
             'text': 'No minimum Class 12 marks to appear in JEE Main per the 2027 bulletin; marks rules apply at admission (see '
                     'JoSAA entries).',
             'topic': 'marks'},
            {'source': 'https://cdnbbsr.s3waas.gov.in/s3f8e59f4b2fe7c5705bf878bbd494ccdf/uploads/2026/10/202610241890224107.pdf',
             'text': 'JEE Advanced route: be among top 2,50,000 successful candidates in the B.E./B.Tech paper (bulletin '
                     's.11.6.2).',
             'topic': 'other'}],
  'summary': 'To sit the test no subject combination or Class 12 percentage is set. Subjects and marks are checked at admission '
             '(see JoSAA); the year of passing matters: 2025 or 2026 pass, or appearing in 2027.'},
 {'body': 'IIT Roorkee for Joint Admission Board',
  'courses': ['B.Tech/B.S./Integrated M.Sc at IITs'],
  'cycle': 'JEE Advanced 2026 brochure',
  'group': 'eng',
  'id': 'jee-advanced',
  'level': 'ug',
  'name': 'JEE Advanced 2026',
  'needs': [{'any': ['Physics'], 'label': 'Physics'},
            {'any': ['Chemistry'], 'label': 'Chemistry'},
            {'any': ['Mathematics'], 'label': 'Mathematics'}],
  'not_found': ['JEE Main 2026-cycle bulletin was not listed on the NTA documents page; the 2027 bulletin (Oct 2026) is used. '
                '2026-cycle year-of-appearance wording only from JoSAA 2026 (first appearance 2024/2025/2026 for NIT+).',
                'JEE Main 2027 bulletin does not state the subject combination or 50% rules for Paper 2A/2B; only JoSAA and CoA '
                'rules verified. Older JEE Main 2024 bulletin B.Arch/B.Plan 50% wording seen only via a search summary, not '
                'read.',
                'Category-wise JEE Main qualifying percentile cut-offs for JEE Advanced not extracted.',
                'State B.Arch routes (TNEA, KEAM, MHT-CET etc.) and state-specific rules not verified.',
                'JEE Advanced foreign national/OCI-PIO(F) criteria and JoSAA special institute restrictions not read.',
                "NATA brochure says only '10+2 or equivalent'; explicit acceptance of IB/Cambridge/NIOS/foreign boards for "
                'B.Arch and AIU equivalence rules not verified from AIU.',
                'NTA site returns 403 to the fetch tool; the 2027 bulletin was obtained by direct download.'],
  'quals': {'cambridge': ['yes', 'GCE A level and Cambridge High School Certificate are listed.'],
            'cbse': ['yes', 'Class 12 of any recognised central or state board is listed.'],
            'diploma': ['yes', 'An AICTE or state board diploma of at least three years is listed.'],
            'foreign': ['equiv', 'An AIU equivalence certificate is needed for any other or foreign board.'],
            'ib': ['yes', 'IB Diploma is listed.'],
            'nios': ['yes', 'NIOS Senior Secondary with at least five subjects is listed.'],
            'preuniv': ['yes', 'Intermediate or two-year pre-university is listed.'],
            'voc': ['yes', 'HSC Vocational is listed.']},
  'rules': [{'source': 'https://jeeadv.ac.in/eligibility.html',
             'text': 'Five criteria must all be met (Eligibility page A1-A5). A1: rank within top 2,50,000 of JEE Main 2026 '
                     'B.E./B.Tech paper (split OPEN 40.5%, GEN-EWS 10%, OBC-NCL 27%, SC 15%, ST 7.5%, 5% PwD horizontal).',
             'topic': 'other'},
            {'source': 'https://jeeadv.ac.in/eligibility.html',
             'text': 'A2 age: born on or after 1 Oct 2001; SC/ST/PwD get five years relaxation (born on or after 1 Oct 1996). '
                     'A3: maximum two attempts in two consecutive years.',
             'topic': 'other'},
            {'source': 'https://jeeadv.ac.in/eligibility.html',
             'text': 'A4: must have appeared in Class 12 (or equivalent) for the first time in 2025 or 2026 with Physics, '
                     'Chemistry and Mathematics compulsory. First appearance in 2024 or earlier is not eligible, except boards '
                     'that declared 2023-24 results on or after 18 June 2024.',
             'topic': 'qualification'},
            {'source': 'https://jeeadv.ac.in/eligibility.html',
             'text': 'A5: not previously admitted to any IIT programme listed in JoSAA 2025 business rules (exceptions: IIT prep '
                     'course only, or seat not reported/withdrawn/cancelled before last round).',
             'topic': 'other'},
            {'source': 'https://jeeadv.ac.in/documents/IBEnglish_2026.pdf',
             'text': 'Brochure clause 25 equivalents: 10+2 of Central/State board recognised by AIU; Intermediate/2-yr '
                     'Pre-University; NDA Joint Services Wing; NIOS Senior Secondary with minimum 5 subjects; any public '
                     'school/board/university exam in India or abroad recognised by AIU; HSC vocational; AICTE/State Board '
                     '3-year diploma; GCE A level; Cambridge HSC or IB Diploma; other/foreign boards need AIU equivalence '
                     'certificate.',
             'topic': 'qualification'},
            {'source': 'https://jeeadv.ac.in/documents/IBEnglish_2026.pdf',
             'text': 'Brochure clause 26, P-C-M compulsory and at least five subjects: EITHER 75% aggregate (65% for SC, ST, '
                     'PwD) OR category-wise top 20 percentile of successful candidates of that board. Marksheet must be from a '
                     'single board.',
             'topic': 'marks'},
            {'source': 'https://jeeadv.ac.in/documents/IBEnglish_2026.pdf',
             'text': 'Five subjects counted: Physics, Chemistry, Mathematics, one language (best if several), and the '
                     'best-scoring other subject; each scaled to 100 (total out of 500). Only Class 12 marks where a board '
                     'combines Class 11+12; final year only for 2-year/3-year courses; final two semesters for semester boards.',
             'topic': 'subjects'},
            {'source': 'https://jeeadv.ac.in/documents/IBEnglish_2026.pdf',
             'text': 'Improvement: the percentile route needs re-appearance in ALL subjects in the same academic year; the 75% '
                     'route allows improvement in some subjects. Board without top-20 data: candidate gets a board certificate '
                     '(Annexure II), otherwise CBSE cut-off is used. PwD top-20 cut-off = lowest of GEN/OBC-NCL/SC/ST cut-offs.',
             'topic': 'other'},
            {'source': 'https://jeeadv.ac.in/documents/IBEnglish_2026.pdf',
             'text': 'Foreign nationals and OCI/PIO(F) follow separate criteria at jeeadv.ac.in/foreign.html (not extracted).',
             'topic': 'other'},
            {'source': 'https://cdnbbsr.s3waas.gov.in/s313111c20aee51aeb480ecbd988cd8cc9/uploads/2026/06/20260601632081678.pdf',
             'text': 'JoSAA: Business Rules 2026 Annexure 2(a), IITs/IISc: P-C-M compulsory; five subjects; 75% aggregate (65% '
                     'SC/ST/PwD) or category-wise top 20 percentile; same-board marksheet; matches JEE Advanced clause 26.',
             'topic': 'marks'},
            {'source': 'https://cdnbbsr.s3waas.gov.in/s313111c20aee51aeb480ecbd988cd8cc9/uploads/2026/06/20260601632081678.pdf',
             'text': 'JoSAA: Criterion (i): qualified in JEE Advanced 2026 for IIT/IISc programmes and meets Annexure 2(a). '
                     'Preparatory courses need at least 2.5% in each subject and 8.75% aggregate in JEE Advanced 2026 (Clause '
                     '17).',
             'topic': 'other'},
            {'source': 'https://cdnbbsr.s3waas.gov.in/s313111c20aee51aeb480ecbd988cd8cc9/uploads/2026/06/20260601632081678.pdf',
             'text': 'JoSAA: Annexure 4 equivalence list is the same as JEE Main (10+2, Intermediate, NDA, NIOS with 5 subjects, '
                     'AIU-recognised foreign, HSC vocational, 3-yr AICTE/State diploma, GCE A level, Cambridge HSC/IB, AIU '
                     'certificate for others).',
             'topic': 'qualification'}],
  'summary': 'Top 2,50,000 in JEE Main, first Class 12 appearance in 2025 or 2026, Physics, Chemistry and Maths compulsory, and '
             '75 percent (65 percent for SC, ST, PwD) or the board top 20 percentile for admission.'},
 {'body': 'Joint Seat Allocation Authority',
  'courses': ['B.E./B.Tech', 'B.Arch', 'B.Planning'],
  'cycle': 'JoSAA 2026 business rules',
  'group': 'eng',
  'id': 'josaa-nit',
  'level': 'ug',
  'name': 'JoSAA: NITs, IIITs and GFTIs 2026',
  'needs': [{'any': ['Physics'], 'label': 'Physics'},
            {'any': ['Mathematics'], 'label': 'Mathematics'},
            {'any': ['Chemistry', 'Biology', 'Biotechnology'], 'label': 'Chemistry, Biology or Biotechnology'}],
  'not_found': ['JEE Main 2026-cycle bulletin was not listed on the NTA documents page; the 2027 bulletin (Oct 2026) is used. '
                '2026-cycle year-of-appearance wording only from JoSAA 2026 (first appearance 2024/2025/2026 for NIT+).',
                'JEE Main 2027 bulletin does not state the subject combination or 50% rules for Paper 2A/2B; only JoSAA and CoA '
                'rules verified. Older JEE Main 2024 bulletin B.Arch/B.Plan 50% wording seen only via a search summary, not '
                'read.',
                'Category-wise JEE Main qualifying percentile cut-offs for JEE Advanced not extracted.',
                'State B.Arch routes (TNEA, KEAM, MHT-CET etc.) and state-specific rules not verified.',
                'JEE Advanced foreign national/OCI-PIO(F) criteria and JoSAA special institute restrictions not read.',
                "NATA brochure says only '10+2 or equivalent'; explicit acceptance of IB/Cambridge/NIOS/foreign boards for "
                'B.Arch and AIU equivalence rules not verified from AIU.',
                'NTA site returns 403 to the fetch tool; the 2027 bulletin was obtained by direct download.'],
  'quals': {'cambridge': ['yes', 'GCE A level and Cambridge High School Certificate are listed.'],
            'cbse': ['yes', 'Class 12 of any recognised central or state board is listed.'],
            'diploma': ['yes', 'An AICTE or state board diploma of at least three years is listed.'],
            'foreign': ['equiv', 'An AIU equivalence certificate is needed for any other or foreign board.'],
            'ib': ['yes', 'IB Diploma is listed.'],
            'nios': ['yes', 'NIOS Senior Secondary with at least five subjects is listed.'],
            'preuniv': ['yes', 'Intermediate or two-year pre-university is listed.'],
            'voc': ['yes', 'HSC Vocational is listed.']},
  'rules': [{'source': 'https://cdnbbsr.s3waas.gov.in/s313111c20aee51aeb480ecbd988cd8cc9/uploads/2026/06/20260601632081678.pdf',
             'text': 'Annexure 2(b): must have appeared in Class 12 (or equivalent) for the first time in 2024, 2025 or 2026 '
                     '(2026 cycle).',
             'topic': 'qualification'},
            {'source': 'https://cdnbbsr.s3waas.gov.in/s313111c20aee51aeb480ecbd988cd8cc9/uploads/2026/06/20260601632081678.pdf',
             'text': '75% aggregate in five subjects (65% for SC, ST, PwD) OR category-wise top 20 percentile of successful '
                     'candidates of that board; marksheet from one board; each listed subject must also be passed.',
             'topic': 'marks'},
            {'source': 'https://cdnbbsr.s3waas.gov.in/s313111c20aee51aeb480ecbd988cd8cc9/uploads/2026/06/20260601632081678.pdf',
             'text': 'B.E./B.Tech five subjects: Physics; any ONE of Chemistry, Biology, Biotechnology, Technical Vocational '
                     'subject; Mathematics; a language; best other subject.',
             'topic': 'substitution'},
            {'source': 'https://cdnbbsr.s3waas.gov.in/s313111c20aee51aeb480ecbd988cd8cc9/uploads/2026/06/20260601632081678.pdf',
             'text': 'B.Planning: Mathematics plus best other four subjects. B.Arch: Physics, Chemistry, Mathematics plus best '
                     'other two subjects.',
             'topic': 'subjects'},
            {'source': 'https://cdnbbsr.s3waas.gov.in/s313111c20aee51aeb480ecbd988cd8cc9/uploads/2026/06/20260601632081678.pdf',
             'text': 'B.Arch via JEE Main Paper IIA and B.Plan via Paper IIB for NIT/IIEST/IIIT/GFTI seats; both must meet '
                     'Annexure 2(b) (criteria iv and v). Improvement: best of the performances if reappeared in ALL subjects.',
             'topic': 'other'},
            {'source': 'https://cdnbbsr.s3waas.gov.in/s313111c20aee51aeb480ecbd988cd8cc9/uploads/2026/06/20260601632081678.pdf',
             'text': 'Top-20 percentile cut-offs (out of 500) for 2026 are published at josaa.nic.in/top-20-percentile/; JoSAA '
                     'also lists special institute/programme restrictions (not extracted).',
             'topic': 'other'}],
  'summary': 'NITs, IIITs and other GFTIs: first Class 12 appearance in 2024, 2025 or 2026, and 75 percent (65 percent for SC, '
             'ST, PwD) or the board top 20 percentile. B.Tech counts Physics, Maths and one of Chemistry, Biology, Biotechnology '
             'or a technical vocational subject.'},
 {'body': 'Council of Architecture',
  'courses': ['B.Arch (5-year)'],
  'cycle': 'NATA 2026 brochure',
  'group': 'eng',
  'id': 'nata',
  'level': 'ug',
  'name': 'NATA (B.Arch) 2026',
  'needs': [{'any': ['Physics'], 'label': 'Physics'},
            {'any': ['Mathematics'], 'label': 'Mathematics'},
            {'any': ['Chemistry', 'Biology', 'Computer Science'],
             'label': 'Chemistry, Biology or Computer Science (or another listed subject)'}],
  'not_found': ['JEE Main 2026-cycle bulletin was not listed on the NTA documents page; the 2027 bulletin (Oct 2026) is used. '
                '2026-cycle year-of-appearance wording only from JoSAA 2026 (first appearance 2024/2025/2026 for NIT+).',
                'JEE Main 2027 bulletin does not state the subject combination or 50% rules for Paper 2A/2B; only JoSAA and CoA '
                'rules verified. Older JEE Main 2024 bulletin B.Arch/B.Plan 50% wording seen only via a search summary, not '
                'read.',
                'Category-wise JEE Main qualifying percentile cut-offs for JEE Advanced not extracted.',
                'State B.Arch routes (TNEA, KEAM, MHT-CET etc.) and state-specific rules not verified.',
                'JEE Advanced foreign national/OCI-PIO(F) criteria and JoSAA special institute restrictions not read.',
                "NATA brochure says only '10+2 or equivalent'; explicit acceptance of IB/Cambridge/NIOS/foreign boards for "
                'B.Arch and AIU equivalence rules not verified from AIU.',
                'NTA site returns 403 to the fetch tool; the 2027 bulletin was obtained by direct download.'],
  'quals': {'cambridge': ['check', 'The brochure says 10+2 or equivalent. Confirm with the counselling authority.'],
            'cbse': ['yes', 'Class 12 with Physics, Maths and one other listed subject, at least 45 percent aggregate.'],
            'diploma': ['yes', 'A 10+3 diploma with Mathematics and at least 45 percent aggregate is accepted.', []],
            'foreign': ['check', 'Get an AIU equivalence certificate and confirm with the counselling authority.'],
            'ib': ['check',
                   'The brochure says 10+2 or equivalent. Confirm with the counselling authority and get an AIU certificate if '
                   'asked.'],
            'nios': ['check',
                     'The brochure says 10+2 or equivalent and does not name NIOS. Confirm with the Council of Architecture.'],
            'preuniv': ['check', 'The brochure says 10+2 or equivalent; confirm with the counselling authority.'],
            'voc': ['check', 'Not named in the notice; confirm with the exam body in writing.']},
  'rules': [{'source': 'https://www.nata.in/assets/pdf/Final-NATA-BROCHURE-2026.pdf',
             'text': 'To APPEAR in NATA 2026: passed or appearing in 10+2 with subjects in para 5.2, or passed or appearing in '
                     '10+3 Diploma with Mathematics as a subject (brochure Eligibility Criteria, 5.0-5.1).',
             'topic': 'qualification'},
            {'source': 'https://www.nata.in/assets/pdf/Final-NATA-BROCHURE-2026.pdf',
             'text': 'For ADMISSION to B.Arch (CoA Minimum Standards of Architectural Education Regulations 2020, Reg 4(1), '
                     'quoted in brochure 5.2): 10+2 or equivalent with Physics and Mathematics compulsory plus one of Chemistry, '
                     'Biology, Technical Vocational subject, Computer Science, Information Technology, Informatics Practices, '
                     'Engineering Graphics or Business Studies.',
             'topic': 'subjects'},
            {'source': 'https://www.nata.in/assets/pdf/Final-NATA-BROCHURE-2026.pdf',
             'text': 'At least 45% aggregate in 10+2 (or equivalent); or passed 10+3 Diploma with Mathematics compulsory and at '
                     'least 45% aggregate. The older 2017 amendment (50% in PCM and 50% aggregate) is superseded by the 2020 '
                     'regulations.',
             'topic': 'marks'},
            {'source': 'https://www.nata.in/assets/pdf/Final-NATA-BROCHURE-2026.pdf',
             'text': 'Prima facie eligible applicants are provisionally allowed; originals verified at counselling; a NATA score '
                     'gives no right to admission. Reservations follow state/UT counselling rules. NATA 2025 score stays valid '
                     'for 2026-27 in stated cases.',
             'topic': 'other'},
            {'source': 'https://www.coa.gov.in/app/myauth/notification/Amendment_in_Eligibility_Regulations.pdf',
             'text': 'Historic reference only: CoA 2017 Gazette amendment of 50% in PCM and 50% aggregate, effective 2019-20.',
             'topic': 'marks'}],
  'summary': 'B.Arch needs Physics and Maths plus one of Chemistry, Biology, Computer Science and similar subjects, with at '
             'least 45 percent aggregate. A 10+3 diploma with Maths and 45 percent also qualifies.'},
 {'body': 'National Testing Agency',
  'courses': ['B.Arch', 'B.Planning'],
  'cycle': 'JEE Main 2027 bulletin (Oct 2026)',
  'group': 'eng',
  'id': 'jee-main-paper2',
  'level': 'ug',
  'name': 'JEE Main Paper 2 (B.Arch, B.Planning) 2027',
  'needs': [{'any': ['Mathematics'], 'label': 'Mathematics'}],
  'not_found': ['JEE Main 2026-cycle bulletin was not listed on the NTA documents page; the 2027 bulletin (Oct 2026) is used. '
                '2026-cycle year-of-appearance wording only from JoSAA 2026 (first appearance 2024/2025/2026 for NIT+).',
                'JEE Main 2027 bulletin does not state the subject combination or 50% rules for Paper 2A/2B; only JoSAA and CoA '
                'rules verified. Older JEE Main 2024 bulletin B.Arch/B.Plan 50% wording seen only via a search summary, not '
                'read.',
                'Category-wise JEE Main qualifying percentile cut-offs for JEE Advanced not extracted.',
                'State B.Arch routes (TNEA, KEAM, MHT-CET etc.) and state-specific rules not verified.',
                'JEE Advanced foreign national/OCI-PIO(F) criteria and JoSAA special institute restrictions not read.',
                "NATA brochure says only '10+2 or equivalent'; explicit acceptance of IB/Cambridge/NIOS/foreign boards for "
                'B.Arch and AIU equivalence rules not verified from AIU.',
                'NTA site returns 403 to the fetch tool; the 2027 bulletin was obtained by direct download.'],
  'quals': {'cambridge': ['yes', 'GCE A level and Cambridge High School Certificate are listed.'],
            'cbse': ['yes', 'Class 12 of any recognised central or state board is listed.'],
            'diploma': ['yes', 'An AICTE or state board diploma of at least three years is listed.'],
            'foreign': ['equiv', 'An AIU equivalence certificate is needed for any other or foreign board.'],
            'ib': ['yes', 'IB Diploma is listed.'],
            'nios': ['yes', 'NIOS Senior Secondary with at least five subjects is listed.'],
            'preuniv': ['yes', 'Intermediate or two-year pre-university is listed.'],
            'voc': ['yes', 'HSC Vocational is listed.']},
  'rules': [{'source': 'https://cdnbbsr.s3waas.gov.in/s3f8e59f4b2fe7c5705bf878bbd494ccdf/uploads/2026/10/202610241890224107.pdf',
             'text': 'Same qualifying-exam list and year-of-appearance rule as Paper 1 (passed 2025/2026 or appearing 2027).',
             'topic': 'qualification'},
            {'source': 'https://cdnbbsr.s3waas.gov.in/s3f8e59f4b2fe7c5705bf878bbd494ccdf/uploads/2026/10/202610241890224107.pdf',
             'text': 'Paper 2A: Mathematics, Aptitude Test, Drawing Test; Paper 2B: Mathematics, Aptitude Test, Planning-Based '
                     'Test. The NTA bulletin sets no Class 12 subject or percentage criteria; these come from JoSAA/CSAB and CoA '
                     '(see josaa-nit and nata entries).',
             'topic': 'subjects'},
            {'source': 'https://cdnbbsr.s3waas.gov.in/s313111c20aee51aeb480ecbd988cd8cc9/uploads/2026/06/20260601632081678.pdf',
             'text': 'For NIT+ seats via JoSAA 2026: B.Arch counts Physics, Chemistry, Mathematics in the five subjects; '
                     'B.Planning needs Mathematics only.',
             'topic': 'subjects'}],
  'summary': 'Paper 2A (B.Arch) and 2B (B.Planning). The NTA bulletin sets no Class 12 subject rule; JoSAA counts Physics, '
             'Chemistry and Maths for B.Arch and Maths for B.Planning.'},
 {'body': 'NTA conducting; NMC/DCI/NCISM/NCH regulate',
  'courses': ['MBBS', 'BDS', 'BAMS', 'BUMS', 'BSMS', 'BHMS', 'BVSc & AH (15% VCI quota)', 'B.Sc Nursing', 'allied'],
  'cycle': 'NEET UG 2026',
  'group': 'med',
  'id': 'neet-ug',
  'level': 'ug',
  'name': 'NEET UG 2026',
  'needs': [{'any': ['Physics'], 'label': 'Physics'},
            {'any': ['Chemistry'], 'label': 'Chemistry'},
            {'any': ['Biology', 'Biotechnology'], 'label': 'Biology or Biotechnology'},
            {'any': ['English'], 'label': 'English'}],
  'not_found': ['NIOS/open schooling is not named in the 2026 bulletin text (it relies on recognised-board wording; coaching '
                'sites say NIOS is accepted, secondary only)',
                'IB/Cambridge/American curricula and any AIU biology-or-biotechnology ruling are not named; only the generic AIU '
                'equivalence certificate and Code 07 scope-and-standard rule were found',
                'Vocational stream rules not in bulletin',
                'Class 12 compartment/supplementary rules not in bulletin beyond result-awaited and '
                'passed-by-first-round-of-counselling',
                'Practical requirement beyond bulletin text; actual GMER-2023 text and NMC public notice 22.11.2023 not fetched '
                '(nmc.org.in URLs 404)',
                'Detailed B.Sc Nursing (INC) and BVSc (VCI) eligibility not fetched',
                'NEET UG 2027 bulletin not yet available',
                'Direct neet.nta.nic.in pages returned 403; bulletin read from govt CDN copy'],
  'quals': {'cambridge': ['equiv',
                          'Needs an equivalence certificate (AIU or UGC) showing it equals Indian Class 12. The qualification '
                          'must also meet the scope-and-standard test in the bulletin.'],
            'cbse': ['yes',
                     'Class 12 after 12 years of study with Physics, Chemistry, Biology or Biotechnology and English, including '
                     'practicals.'],
            'diploma': ['check', 'Not named in the notice; confirm with the exam body in writing.'],
            'foreign': ['equiv',
                        'Needs an equivalence certificate (AIU or UGC) showing it equals Indian Class 12. The qualification must '
                        'also meet the scope-and-standard test in the bulletin.'],
            'ib': ['equiv',
                   'Needs an equivalence certificate (AIU or UGC) showing it equals Indian Class 12. The qualification must also '
                   'meet the scope-and-standard test in the bulletin.'],
            'nios': ['check',
                     'The bulletin does not name NIOS. It accepts a recognised board result with PCB and English; confirm with '
                     'NTA and your admitting authority.'],
            'preuniv': ['yes', 'Intermediate or pre-degree Science with PCB or Biotechnology and compulsory English is listed.'],
            'voc': ['check',
                    'Vocational stream rules are not in the bulletin. Not named in the notice; confirm with the exam body in '
                    'writing.']},
  'rules': [{'source': 'https://cdnbbsr.s3waas.gov.in/s37bc1ec1d9c3426357e69acd5bf320061/uploads/2026/02/202602081576322299.pdf',
             'text': 'Qualifying exam (Codes 01-07, Ch.6 s.3, bulletin pp.26-28; approved by NMC letters dated 05.12.2025, '
                     '13.01.2026, 28.01.2026): Higher/Senior Secondary or ISC, i.e. Class 12 after 12 years of study, with '
                     'Physics, Chemistry, Biology/Biotechnology and English, including practical tests in these subjects, plus '
                     'Mathematics or another elective, and English at not less than the NCERT core-course level.',
             'topic': 'qualification'},
            {'source': 'https://cdnbbsr.s3waas.gov.in/s37bc1ec1d9c3426357e69acd5bf320061/uploads/2026/02/202602081576322299.pdf',
             'text': 'Candidates whose Class 12 result is awaited may apply and appear (Code 01) but are not eligible for '
                     'admission unless they have passed by the time of the first counselling round (also Ch.8 s.1(ii)(d): not '
                     'admitted until eligibility is fulfilled).',
             'topic': 'qualification'},
            {'source': 'https://cdnbbsr.s3waas.gov.in/s37bc1ec1d9c3426357e69acd5bf320061/uploads/2026/02/202602081576322299.pdf',
             'text': 'Other accepted Indian qualifications (Codes 03-07): Intermediate/Pre-degree Science of an Indian '
                     'University/Board with PCB/Biotech incl. practicals and compulsory English; Pre-professional/Pre-medical '
                     'exam with PCB/Biotech and English after Higher Secondary/Pre-University; first year of a 3-year degree '
                     'course with PCB/Biotech incl. practicals (earlier qualifier with PCB/Biotech+English); B.Sc. with at least '
                     'two of Physics, Chemistry, Biology (Botany, Zoology)/Biotechnology and earlier qualifier with PCB and '
                     'English; any other exam equal in scope and standard (last 2 years of 10+2 study of PCB/Biotech with '
                     'practicals, plus English).',
             'topic': 'qualification'},
            {'source': 'https://cdnbbsr.s3waas.gov.in/s37bc1ec1d9c3426357e69acd5bf320061/uploads/2026/02/202602081576322299.pdf',
             'text': 'Foreign or other university/board examinations: the institute needs a certificate from the concerned '
                     'Indian University or the Association of Indian Universities (AIU) saying the exam is equivalent to Class '
                     '12 under the Intermediate Science examination (Codes 03-07). Bulletin note: candidates from '
                     'foreign/international boards must ensure their exam is equal in scope and standard as described in Code 07 '
                     '(last 2 years of PCB/Biotech study with practicals, plus English).',
             'topic': 'qualification'},
            {'source': 'https://cdnbbsr.s3waas.gov.in/s37bc1ec1d9c3426357e69acd5bf320061/uploads/2026/02/202602081576322299.pdf',
             'text': 'Subjects must be Physics, Chemistry, Biology/Biotechnology and English. Biology is written as Biology '
                     '(Botany, Zoology)/Biotechnology in the B.Sc. clause. Practical tests in these subjects are required for '
                     'the Class 12 and equivalent routes.',
             'topic': 'subjects'},
            {'source': 'https://cdnbbsr.s3waas.gov.in/s37bc1ec1d9c3426357e69acd5bf320061/uploads/2026/02/202602081576322299.pdf',
             'text': 'Candidates who passed Class 12 earlier and later studied Physics, Chemistry, Biology/Biotechnology and '
                     'English, even as additional subjects, from a board recognised by the concerned Government, may appear in '
                     'NEET-UG and get an Eligibility Certificate (NMC Public Notice 22.11.2023, para 7, quoted in Codes 01/02); '
                     'candidature is considered only with documentary proof of having passed the qualifying exam with the '
                     'required subjects. So Biology/Biotechnology as an additional subject counts.',
             'topic': 'substitution'},
            {'source': 'https://cdnbbsr.s3waas.gov.in/s37bc1ec1d9c3426357e69acd5bf320061/uploads/2026/02/202602081576322299.pdf',
             'text': 'Counselling eligibility is by NEET percentile, not a Class 12 PCB aggregate (Ch.8 s.1(ii)(a), p.39): '
                     'Unreserved and GEN-EWS 50th percentile; SC/ST/OBC 40th percentile; Benchmark-disability: 45th percentile '
                     'for Unreserved/GEN-EWS and 40th percentile for SC/ST/OBC-NCL. Percentile is computed on the highest marks '
                     'in the All India common merit list. Central Govt may lower the cut-off for an academic year if too few '
                     'qualify (s.1(ii)(b)). Same cut-offs apply to INIs and to BAMS/BSMS/BUMS/BHMS (Ch.9 s.5).',
             'topic': 'marks'},
            {'source': 'https://cdnbbsr.s3waas.gov.in/s37bc1ec1d9c3426357e69acd5bf320061/uploads/2026/02/202602081576322299.pdf',
             'text': 'The bulletin states no minimum Class 12 percentage in PCB (the 50%/45%/40% PCB-aggregate rule seen on '
                     'coaching sites is not in this bulletin); treat that as superseded/unsupported unless a state or '
                     'institution rule says otherwise.',
             'topic': 'marks'},
            {'source': 'https://cdnbbsr.s3waas.gov.in/s37bc1ec1d9c3426357e69acd5bf320061/uploads/2026/02/202602081576322299.pdf',
             'text': 'AYUSH (BAMS/BSMS/BUMS/BHMS), Ch.9 s.2: passed 10+2 or equivalent with Physics, Chemistry, Biology or '
                     'Biotechnology; age 17 on or before 31 December of admission year. BUMS: Class 10 Urdu/Arabic/Persian or '
                     'pass the Urdu test; BSMS: Tamil in Class 10/higher secondary, or study Tamil in the first professional '
                     'year (Ch.8 s.1(ii)(c)).',
             'topic': 'other'},
            {'source': 'https://cdnbbsr.s3waas.gov.in/s37bc1ec1d9c3426357e69acd5bf320061/uploads/2026/02/202602081576322299.pdf',
             'text': 'Age: minimum 17 years on or before 31 December of the exam year (GMER-2023 amendment 16.06.2023); '
                     'General/EWS must be born on or before 31.12.2009 for 2026; no upper age limit (NMC letter 13.01.2026). '
                     'Ch.6 s.1.',
             'topic': 'other'},
            {'source': 'https://cdnbbsr.s3waas.gov.in/s37bc1ec1d9c3426357e69acd5bf320061/uploads/2026/02/202602081576322299.pdf',
             'text': 'Use of NEET result (Ch.7 s.1C): B.Sc (H) Nursing per respective eligibility rules; BVSc and AH 15% VCI '
                     'quota via MCC data; Military Nursing Service B.Sc Nursing aspirants must qualify NEET. The bulletin gives '
                     'no separate qualification rules for nursing, BVSc or BDS beyond NMC/DCI regulations; BDS is covered with '
                     'MBBS in Chapter 6.',
             'topic': 'other'},
            {'source': 'https://cdnbbsr.s3waas.gov.in/s37bc1ec1d9c3426357e69acd5bf320061/uploads/2026/02/202602081576322299.pdf',
             'text': 'NRI/OCI/Foreign nationals may appear (Ch.5; Ch.6 s.2); they upload an Indian mission certificate or '
                     'citizenship proof. Admission is subject to State/institution/Govt of India rules. Indian citizens/OCI '
                     'studying medicine abroad also need NEET qualification. OCI rights follow the Supreme Court order of '
                     '03.02.2023 (WP 891 of 2021). No separate qualification equivalence is given for them.',
             'topic': 'nri'}],
  'summary': 'Class 12 with Physics, Chemistry, Biology or Biotechnology and English, with practicals. Eligibility is by NEET '
             'percentile, not a Class 12 percentage.'},
 {'body': 'IIT Bombay (UCEED Office)',
  'courses': ['B.Des at IIT Bombay, IIT Delhi, IIT Guwahati, IIT Hyderabad, IIT Indore, IIT Roorkee and IIITDM Jabalpur'],
  'cycle': 'UCEED 2027',
  'group': 'design',
  'id': 'uceed',
  'level': 'ug',
  'name': 'UCEED 2027',
  'needs': [],
  'not_found': ['UCEED brochure pages 18-19 and point 21 (p.40) not read directly; rules come from the official UCEED 2027 '
                'website eligibility pages. Any minimum-marks or institute-level extra conditions in the brochure are '
                'unverified.',
                'NIFT Admission Prospectus / Admissions Guidelines 2027 (the document the bulletin defers to) could not be '
                'opened (file over 10 MB); bulletin Chapter 2 tables were used instead. Extra notes in the prospectus are '
                'unverified.',
                'NIFT rule for candidates appearing in Class XII in 2027 and any minimum marks: not found in the bulletin text '
                'read.',
                'NID B.Des handbook year wording (2026-27 vs 2027-28 for Class XII appearers) is inconsistent in the PDF; '
                'intended year not resolved.',
                'NID detail on IB/Cambridge beyond the AIU equivalence-certificate rule and IB being named as a recognised '
                'board: nothing further found.',
                'NID separate non-integrated 4-year B.Des handbook for 2027-28 not seen; the combined Integrated Pathway and '
                'B.Des handbook was used.'],
  'quals': {'cambridge': ['yes', 'GCE A level and Cambridge High School Certificate are listed.'],
            'cbse': ['yes', 'Any stream may appear.'],
            'diploma': ['check',
                        'A 3-year AICTE or state board diploma is accepted for appearing, but institutes may not accept it for '
                        'admission.'],
            'foreign': ['equiv', 'Needs an equivalence certificate (AIU or UGC) showing it equals Indian Class 12.'],
            'ib': ['yes', 'IB Diploma is listed.'],
            'nios': ['yes', 'NIOS Senior Secondary with at least five subjects is listed.'],
            'preuniv': ['yes', 'Intermediate or two-year pre-university from an AIU-recognised board is listed.'],
            'voc': ['yes', 'HSC Vocational is listed.']},
  'rules': [{'source': 'https://www.uceed.iitb.ac.in/2027/eligibility-exam.html',
             'text': 'Qualifying exam is Class XII or equivalent, first appeared for in 2026 or 2027. Candidates who first '
                     'appeared in 2025 or earlier are not eligible. Exception: if a Board declared its 2024-25 results on or '
                     "after 30 September 2025, its 2025 appearers are eligible. 'Appearance' means the Board declared that "
                     "year's result, even if no exam was held or the result was withheld. If a Board declared results before 30 "
                     'Sept 2025, a candidate with a withheld result is not eligible.',
             'topic': 'qualification'},
            {'source': 'https://www.uceed.iitb.ac.in/2027/eligibility-exam.html',
             'text': 'All streams (Science, Commerce, Arts and Humanities) are eligible to appear in UCEED.',
             'topic': 'qualification'},
            {'source': 'https://www.uceed.iitb.ac.in/2027/eligibility-exam.html',
             'text': 'Accepted qualifying exams: 10+2 of a Central or State Board recognised by AIU; Intermediate or two-year '
                     'Pre-University exam from an AIU-recognised Board or University; final exam of the two-year Joint Services '
                     'Wing course of NDA; NIOS Senior Secondary exam with minimum five subjects; any public school, Board or '
                     'University exam in India or abroad recognised by AIU or UGC as equivalent to 10+2; H.S.C. vocational exam; '
                     'GCE Advanced (A) level (London, Cambridge, Sri Lanka); Cambridge High School Certificate; IB Diploma.',
             'topic': 'qualification'},
            {'source': 'https://www.uceed.iitb.ac.in/2027/eligibility-exam.html',
             'text': 'Diploma: a diploma of at least three years from an AICTE-recognised institution or a State Board of '
                     'Technical Education is accepted for appearing in UCEED, but participating institutes may not accept 3-year '
                     "diplomas, so candidates must check each institute's criteria.",
             'topic': 'qualification'},
            {'source': 'https://www.uceed.iitb.ac.in/2027/eligibility-exam.html',
             'text': 'Class XII completed outside India or from a Board not in the list requires an AIU certificate of '
                     'equivalence to Class XII. A non-public (private) Class XII exam is accepted only if the candidate has '
                     'already passed at least one public Board or Pre-University exam.',
             'topic': 'substitution'},
            {'source': 'https://www.uceed.iitb.ac.in/2027/eligibility-admission.html',
             'text': 'Candidates appearing in Class XII in 2027 can apply; all parts of the final exam must be completed by the '
                     'application date (exceptions via email to uceed@iitb.ac.in). Proof of passing with the required '
                     'eligibility must reach the admitting institute by 30 September 2027. Boards giving only letter grades must '
                     'issue a certificate stating the passing grade.',
             'topic': 'qualification'},
            {'source': 'https://www.uceed.iitb.ac.in/2027/eligibility-admission.html',
             'text': 'Subject requirement for B.Des admission by institute: IIT Bombay, IIT Delhi, IIT Hyderabad, IIT Indore '
                     'accept all streams; IIT Guwahati and IIT Roorkee require Physics, Chemistry, Mathematics; IIITDM Jabalpur '
                     'requires Physics, Chemistry and Mathematics or Biology. PCM Science students can apply to all seven '
                     'institutes; others (Science without one of P/C/M, Commerce, Arts) only to IIT Bombay, Delhi, Hyderabad, '
                     'Indore.',
             'topic': 'subjects'},
            {'source': 'https://www.uceed.iitb.ac.in/2027/eligibility-admission.html',
             'text': 'No minimum Class XII percentage is stated on the exam or admission eligibility pages; the rule is simply '
                     'to have passed Class XII or equivalent. Brochure point 21 (p.40) not read directly.',
             'topic': 'marks'},
            {'source': 'https://www.uceed.iitb.ac.in/2027/eligibility-exam.html',
             'text': 'Age: born on or after 1 Oct 2002 for OPEN/EWS/OBC-NCL; born on or after 1 Oct 1997 for SC/ST/PwD. Maximum '
                     'two attempts, in consecutive years. Foreign nationals meet the same criteria; seats supernumerary, capped '
                     "at 10% of a programme's seats. OCI/PIO cards issued before 4 March 2021 are considered only under OPEN.",
             'topic': 'other'}],
  'summary': 'Class 12 in any stream. Which stream the institute wants is decided at admission: IIT Guwahati and Roorkee need '
             'Physics, Chemistry and Maths.'},
 {'body': 'National Institute of Design',
  'courses': ['B.Des', 'M.Des (Integrated Pathway, 5.5 years)'],
  'cycle': 'UCEED 2027',
  'group': 'design',
  'id': 'nid_bdes',
  'level': 'ug',
  'name': 'NID DAT: B.Des and Integrated M.Des 2027',
  'needs': [],
  'not_found': ['UCEED brochure pages 18-19 and point 21 (p.40) not read directly; rules come from the official UCEED 2027 '
                'website eligibility pages. Any minimum-marks or institute-level extra conditions in the brochure are '
                'unverified.',
                'NIFT Admission Prospectus / Admissions Guidelines 2027 (the document the bulletin defers to) could not be '
                'opened (file over 10 MB); bulletin Chapter 2 tables were used instead. Extra notes in the prospectus are '
                'unverified.',
                'NIFT rule for candidates appearing in Class XII in 2027 and any minimum marks: not found in the bulletin text '
                'read.',
                'NID B.Des handbook year wording (2026-27 vs 2027-28 for Class XII appearers) is inconsistent in the PDF; '
                'intended year not resolved.',
                'NID detail on IB/Cambridge beyond the AIU equivalence-certificate rule and IB being named as a recognised '
                'board: nothing further found.',
                'NID separate non-integrated 4-year B.Des handbook for 2027-28 not seen; the combined Integrated Pathway and '
                'B.Des handbook was used.'],
  'quals': {'cambridge': ['yes', 'GCE A level is listed.'],
            'cbse': ['yes', 'Any stream.'],
            'diploma': ['yes', 'An AICTE 3-year diploma after Class 10 is listed.'],
            'foreign': ['equiv', 'Needs an equivalence certificate (AIU or UGC) showing it equals Indian Class 12.'],
            'ib': ['yes', 'IB is named as an accepted board.'],
            'nios': ['yes', 'NIOS Senior Secondary with at least five subjects is listed.'],
            'preuniv': ['yes', 'Intermediate or two-year pre-university is listed.'],
            'voc': ['check', 'Not named in the notice; confirm with the exam body in writing.']},
  'rules': [{'source': 'https://admissions.nid.edu/NIDA2027/download/BDES_IntegratedPathway_AdmissionsHandbook2027_28.pdf',
             'text': 'Open to candidates who have passed or will appear in higher secondary (10+2) in academic year 2026-27, in '
                     'any stream (Science, Arts, Commerce, Humanities etc.), from any recognised board such as CBSE, IB, ICSE or '
                     'equivalent. The handbook also mentions 2027-28 appearers in the same section; year labels are internally '
                     'inconsistent, so confirm in the PDF.',
             'topic': 'qualification'},
            {'source': 'https://admissions.nid.edu/NIDA2027/download/BDES_IntegratedPathway_AdmissionsHandbook2027_28.pdf',
             'text': 'Equivalents listed: 10+2 final exam of AIU-recognised Central or State Board; Intermediate or two-year '
                     'Pre-University exam; final exam of two-year Joint Services Wing course of NDA; NIOS Senior Secondary with '
                     'minimum five subjects; any public school, Board or University exam in India or abroad recognised by AIU as '
                     'equivalent to 10+2; H.S.C. vocational exam; GCE Advanced (A) level (London, Cambridge, Sri Lanka); '
                     'AICTE-approved three-year full-time diploma after Class X from a state Board of Technical Education.',
             'topic': 'qualification'},
            {'source': 'https://admissions.nid.edu/NIDA2027/download/BDES_IntegratedPathway_AdmissionsHandbook2027_28.pdf',
             'text': 'Class XII (or equivalent) from outside India or from a Board not listed needs an equivalence certificate '
                     'from AIU or Ministry of Education, Government of India, uploaded at document upload stage. IB is named as '
                     'an accepted board in Section 5.1.',
             'topic': 'substitution'},
            {'source': 'https://admissions.nid.edu/NIDA2027/download/BDES_IntegratedPathway_AdmissionsHandbook2027_28.pdf',
             'text': 'Candidates awaiting Class XII result get provisional admission with an undertaking; they must have '
                     'appeared before physical document verification, passed in the first attempt, and submit the marksheet on '
                     'or before 15 July 2027. Any backlog, compartment or supplementary means admission is cancelled and fees '
                     'forfeited.',
             'topic': 'other'},
            {'source': 'https://admissions.nid.edu/NIDA2027/download/BDES_IntegratedPathway_AdmissionsHandbook2027_28.pdf',
             'text': 'No minimum Class XII percentage is stated in the eligibility section.',
             'topic': 'marks'},
            {'source': 'https://admissions.nid.edu/NIDA2027/download/BDES_IntegratedPathway_AdmissionsHandbook2027_28.pdf',
             'text': 'Age: born on or after 1 July 2006 (General, EWS, foreign nationals); on or after 1 July 2003 (OBC-NCL, SC, '
                     'ST); on or after 1 July 2001 (PwD). Applying for B.Des/Integrated M.Des after 10+2 bars applying to the '
                     'standalone M.Des (same-day exams).',
             'topic': 'other'}],
  'summary': 'Class 12 in any stream from a recognised board. Class 12 marksheet is due by 15 July 2027 with a first-attempt '
             'pass.'},
 {'body': 'National Institute of Design',
  'courses': ['M.Des (all disciplines, NID Ahmedabad, Gandhinagar, Bengaluru)', 'M.Des Design Education'],
  'cycle': 'UCEED 2027',
  'group': 'design',
  'id': 'nid_mdes',
  'level': 'pg',
  'name': 'NID DAT: M.Des 2027',
  'needs': [],
  'not_found': ['UCEED brochure pages 18-19 and point 21 (p.40) not read directly; rules come from the official UCEED 2027 '
                'website eligibility pages. Any minimum-marks or institute-level extra conditions in the brochure are '
                'unverified.',
                'NIFT Admission Prospectus / Admissions Guidelines 2027 (the document the bulletin defers to) could not be '
                'opened (file over 10 MB); bulletin Chapter 2 tables were used instead. Extra notes in the prospectus are '
                'unverified.',
                'NIFT rule for candidates appearing in Class XII in 2027 and any minimum marks: not found in the bulletin text '
                'read.',
                'NID B.Des handbook year wording (2026-27 vs 2027-28 for Class XII appearers) is inconsistent in the PDF; '
                'intended year not resolved.',
                'NID detail on IB/Cambridge beyond the AIU equivalence-certificate rule and IB being named as a recognised '
                'board: nothing further found.',
                'NID separate non-integrated 4-year B.Des handbook for 2027-28 not seen; the combined Integrated Pathway and '
                'B.Des handbook was used.'],
  'quals': {},
  'rules': [{'source': 'https://admissions.nid.edu/NIDA2027/download/MDES_AdmissionsHandbook2027-28.pdf',
             'text': "M.Des (any discipline except Design Education): Bachelor's degree or equivalent in any discipline from a "
                     'UGC-recognised university or institution (Act of Parliament or State legislature, or deemed university '
                     'under Sec 3 UGC Act), or an equivalent qualification recognised by Ministry of Education.',
             'topic': 'qualification'},
            {'source': 'https://admissions.nid.edu/NIDA2027/download/MDES_AdmissionsHandbook2027-28.pdf',
             'text': "M.Des Design Education: Master's degree or equivalent in Design, OR Bachelor's degree in Design followed "
                     "by a Master's degree in any discipline.",
             'topic': 'qualification'},
            {'source': 'https://admissions.nid.edu/NIDA2027/download/MDES_AdmissionsHandbook2027-28.pdf',
             'text': 'Degree from a university or board outside India requires an AIU or Ministry of Education equivalence '
                     'certificate, submitted at the document upload stage.',
             'topic': 'substitution'},
            {'source': 'https://admissions.nid.edu/NIDA2027/download/MDES_AdmissionsHandbook2027-28.pdf',
             'text': 'Final-year candidates (2026-27) may apply: must have appeared in all subjects and cleared earlier backlogs '
                     'by 28 June 2027, passed in first attempt, and submit final marksheets by 31 July 2027, with undertakings '
                     'from self, parents and college.',
             'topic': 'other'},
            {'source': 'https://admissions.nid.edu/NIDA2027/download/MDES_AdmissionsHandbook2027-28.pdf',
             'text': 'Age: M.Des born on or after 1 July 1995 (General/EWS/foreign), 1 July 1992 (OBC-NCL/SC/ST), 1 July 1990 '
                     '(PwD). Design Education: 1 July 1992, 1 July 1989, 1 July 1987 respectively.',
             'topic': 'other'}],
  'summary': 'A bachelor degree in any discipline. M.Des Design Education needs a Master in Design, or a Bachelor in Design '
             'followed by a Master in any discipline.'},
 {'body': 'NIFT, exam conducted by NTA',
  'courses': ['B.Des (4 yr)', 'B.FTech (4 yr)', 'M.Des', 'M.F.M.', 'M.FTech', 'NLEA lateral entry (B.Des, B.FTech)'],
  'cycle': 'UCEED 2027',
  'group': 'design',
  'id': 'nift',
  'level': 'ug',
  'name': 'NIFT entrance (NIFTEE) 2027',
  'needs': [],
  'not_found': ['UCEED brochure pages 18-19 and point 21 (p.40) not read directly; rules come from the official UCEED 2027 '
                'website eligibility pages. Any minimum-marks or institute-level extra conditions in the brochure are '
                'unverified.',
                'NIFT Admission Prospectus / Admissions Guidelines 2027 (the document the bulletin defers to) could not be '
                'opened (file over 10 MB); bulletin Chapter 2 tables were used instead. Extra notes in the prospectus are '
                'unverified.',
                'NIFT rule for candidates appearing in Class XII in 2027 and any minimum marks: not found in the bulletin text '
                'read.',
                'NID B.Des handbook year wording (2026-27 vs 2027-28 for Class XII appearers) is inconsistent in the PDF; '
                'intended year not resolved.',
                'NID detail on IB/Cambridge beyond the AIU equivalence-certificate rule and IB being named as a recognised '
                'board: nothing further found.',
                'NID separate non-integrated 4-year B.Des handbook for 2027-28 not seen; the combined Integrated Pathway and '
                'B.Des handbook was used.'],
  'quals': {'cambridge': ['yes', 'GCE A level is listed.'],
            'cbse': ['yes', 'B.Des takes any stream. B.FTech needs Mathematics.'],
            'diploma': ['yes', 'A 3 or 4 year diploma after Class 10 is listed (an engineering diploma for B.FTech).'],
            'foreign': ['equiv', 'Needs an equivalence certificate (AIU or UGC) showing it equals Indian Class 12.'],
            'ib': ['yes', 'IB is listed.'],
            'nios': ['yes', 'NIOS Senior Secondary with five subjects is listed (with Mathematics for B.FTech).'],
            'preuniv': ['check', 'Not named in the notice; confirm with the exam body in writing.'],
            'voc': ['check', 'Not named in the notice; confirm with the exam body in writing.']},
  'rules': [{'source': 'https://www.nift.ac.in/sites/default/files/2026-10/Information%20Bulletin%20-NIFTEE%202027%20-16.10.2026.pdf',
             'text': 'B.Des: pass in 10+2 from any recognised Central/State Board (CBSE, CISCE etc.); OR NIOS Senior Secondary '
                     'pass with minimum five subjects; OR 3 or 4 year diploma recognised by AICTE or State Board of Technical '
                     'Education after Class X; OR any public school/Board/University exam in India or abroad recognised by AIU '
                     'as equivalent to 10+2; OR GCE A level (London/Cambridge/Sri Lanka) or International Baccalaureate (IB). No '
                     'stream restriction.',
             'topic': 'qualification'},
            {'source': 'https://www.nift.ac.in/sites/default/files/2026-10/Information%20Bulletin%20-NIFTEE%202027%20-16.10.2026.pdf',
             'text': 'B.FTech: same routes as B.Des but with Mathematics: 10+2 with Mathematics; NIOS with five subjects '
                     'including Mathematics; 3 or 4 year diploma in any branch of Engineering (AICTE/State Board) after Class X; '
                     'AIU-equivalent exam with Mathematics; GCE A level with Mathematics, or IB. The bulletin text does not '
                     'state Physics as compulsory.',
             'topic': 'subjects'},
            {'source': 'https://www.nift.ac.in/sites/default/files/2026-10/Information%20Bulletin%20-NIFTEE%202027%20-16.10.2026.pdf',
             'text': 'Candidates applying for B.FTech (with Mathematics) can also enrol for B.Des by taking CAT along with GAT '
                     '(not applicable for NLEA).',
             'topic': 'substitution'},
            {'source': 'https://www.nift.ac.in/sites/default/files/2026-10/Information%20Bulletin%20-NIFTEE%202027%20-16.10.2026.pdf',
             'text': 'M.Des and M.F.M.: undergraduate degree in any discipline from an institute/university recognised by law in '
                     'India; OR undergraduate diploma of minimum three years from NIFT/NID. FAQ confirms a non-design graduate '
                     'can apply for M.Des.',
             'topic': 'qualification'},
            {'source': 'https://www.nift.ac.in/sites/default/files/2026-10/Information%20Bulletin%20-NIFTEE%202027%20-16.10.2026.pdf',
             'text': 'M.FTech: B.FTech from NIFT; OR B.E./B.Tech from any recognised institute/university; OR B.FTech (4 yr) '
                     'from any recognised institute/university.',
             'topic': 'qualification'},
            {'source': 'https://www.nift.ac.in/sites/default/files/2026-10/Information%20Bulletin%20-NIFTEE%202027%20-16.10.2026.pdf',
             'text': 'NLEA lateral entry B.Des: Class X pass AND 3 or 4 year related diploma (AICTE/AIU/UGC/State Board); OR '
                     'minimum 2 year related diploma after Class X plus one year full-time industry experience; OR minimum 1 '
                     'year related diploma after Class XII plus one year industry experience; OR 2-year regular UG Diploma at '
                     'NIFT after Class XII. NLEA B.FTech has parallel routes with engineering/apparel-related diplomas; the '
                     '2-year or 1-year routes need Mathematics at Class X or XII, plus one year industry experience; or the '
                     '2-year NIFT UG diploma after Class XII with Mathematics.',
             'topic': 'qualification'},
            {'source': 'https://www.nift.ac.in/sites/default/files/2026-10/Information%20Bulletin%20-NIFTEE%202027%20-16.10.2026.pdf',
             'text': 'Foreign National/NRI/OCI/SAARC: degree/certificate from a non-Indian board or university needs an AIU or '
                     'UGC equivalence certificate before admission; working English required; minimum 50% in SAT/GMAT/GRE '
                     '(scores not declared before 1 Jan 2025, received by 31 March 2027).',
             'topic': 'substitution'},
            {'source': 'https://www.nift.ac.in/sites/default/files/2026-10/Information%20Bulletin%20-NIFTEE%202027%20-16.10.2026.pdf',
             'text': 'No minimum Class XII percentage is stated in the bulletin eligibility chapter.',
             'topic': 'marks'},
            {'source': 'https://www.nift.ac.in/sites/default/files/2026-10/Information%20Bulletin%20-NIFTEE%202027%20-16.10.2026.pdf',
             'text': 'Age: B.Des and B.FTech under 24 as on 1 August of the admission year, relaxed by 5 years for '
                     'SC/ST/PwD/PwBD. No age limit for M.Des, M.F.M., M.FTech.',
             'topic': 'other'}],
  'summary': 'B.Des: any stream. B.FTech needs Mathematics. M.Des and MFM take any bachelor degree; M.FTech takes B.FTech or '
             'B.E./B.Tech.'},
 {'body': 'National Testing Agency (NTA)',
  'courses': ['UG programmes at central universities and participating institutions'],
  'cycle': 'CUET',
  'group': 'univ',
  'id': 'cuet-ug',
  'level': 'ug',
  'name': 'CUET UG 2026',
  'needs': [],
  'not_found': ['Exact AIU fee, document list and processing time for a foreign-board Class 12 Equivalence Certificate '
                '(evaluation.aiu.ac.in returned HTTP 401; AIU page gives no details)',
                'AIU notification equating specific Indian/foreign school boards to Class 12 and the vocational equivalence list '
                '(linked PDFs not readable; 2022 public notice PDF could not be parsed)',
                'Official confirmation that NCERT/PARAKH has replaced AIU for school-board equivalence (only news reports)',
                'Official NIOS equivalence letter text and any UGC circular on NIOS (PDF not parseable; NIOS page lists AIU 1991 '
                'letter, MHRD 1990 resolution, AICTE 2025 circular)',
                'IB / Cambridge A level / American high school specific subject or marks conditions beyond the CUET list entry; '
                'American high school diploma is not in the CUET list',
                'Class 12 via Indian Army or other special routes (no official page found; only NDA Joint Services Wing is '
                'listed by CUET)',
                'CLAT 2027 full UG notification/brochure text (only eligibility web page, press release and some NLU brochures '
                'via search); PwD and other-category relaxations per NLU unverified',
                'Any CUET-wide minimum percentage or category relaxation (none exists in the bulletin; set by universities)'],
  'quals': {'cambridge': ['yes', 'GCE A level and Cambridge High School Certificate are listed.'],
            'cbse': ['yes', 'Class 12 of any recognised central or state board is listed.'],
            'diploma': ['yes', 'A recognised diploma of at least three years is listed.'],
            'foreign': ['equiv', 'Needs a UGC equivalence certificate.'],
            'ib': ['yes', 'IB Diploma is listed.'],
            'nios': ['yes', 'NIOS Senior Secondary with at least five subjects is listed.'],
            'preuniv': ['yes', 'Intermediate or two-year pre-university is listed.'],
            'voc': ['yes', 'HSC Vocational is listed.']},
  'rules': [{'source': 'https://cdnbbsr.s3waas.gov.in/s3d1a21da7bca4abff8b0b61b87597de73/uploads/2026/01/202601031633478370.pdf',
             'text': 'No age limit for sitting CUET (UG) 2026. Candidates who have passed Class 12/equivalent or are appearing '
                     'in 2026 can appear. Any age criterion of the admitting university still applies.',
             'topic': 'qualification'},
            {'source': 'https://cdnbbsr.s3waas.gov.in/s3d1a21da7bca4abff8b0b61b87597de73/uploads/2026/01/202601031633478370.pdf',
             'text': 'Bulletin 3.2 list of qualifying examinations: (i) 10+2 of any recognised Central/State Board incl. CBSE, '
                     'CISCE; (ii) Intermediate / two-year Pre-University; (iii) final exam of the two-year Joint Services Wing '
                     'of NDA; (iv) NIOS Senior Secondary with a minimum of five subjects; (v) any Indian or foreign public '
                     'school/board/university exam recognised as equivalent to 10+2 by AIU/UGC or an agency notified by MoE; '
                     '(vi) Higher Secondary Certificate Vocational Examination; (vii) AICTE- or state-technical-board-recognised '
                     'Diploma of at least 3 years; (viii) GCE A level (London/Cambridge/Sri Lanka); (ix) Cambridge High School '
                     'Certificate or IB Diploma (IB Office, Geneva); (x) Class 12 from outside India or a board not listed: '
                     'produce a UGC certificate of equivalence; (xi) if Class 12 is not a public exam, candidate must have '
                     'passed at least one earlier public (Board or Pre-University) exam.',
             'topic': 'equivalence'},
            {'source': 'https://cdnbbsr.s3waas.gov.in/s3d1a21da7bca4abff8b0b61b87597de73/uploads/2026/01/202601031633478370.pdf',
             'text': 'Year of appearance in Class 12/equivalent: the relevant conditions of each university/institution apply; '
                     'candidate must verify on the university website. Existing university policies on quota, category, '
                     'relaxation, reservation, qualification and subject combinations apply. Appearing in CUET does not entitle '
                     'admission unless programme-wise eligibility is met (Ch.3, 3.3 and Note).',
             'topic': 'other'},
            {'source': 'https://cdnbbsr.s3waas.gov.in/s3d1a21da7bca4abff8b0b61b87597de73/uploads/2026/01/202601031633478370.pdf',
             'text': '37 test papers (13 languages, 23 domain subjects, 1 General Aptitude Test). Candidate may choose up to a '
                     'maximum of five subjects including languages and General Aptitude Test. Candidates are told to select '
                     'subjects per the eligibility of the programme at the desired university; subject requirements are set by '
                     'each university, not NTA. Each paper 60 minutes; +5 correct, -1 wrong.',
             'topic': 'subjects'},
            {'source': 'https://cdnbbsr.s3waas.gov.in/s3d1a21da7bca4abff8b0b61b87597de73/uploads/2026/01/202601031633478370.pdf',
             'text': 'The bulletin sets no common minimum Class 12 percentage; minimum marks and category relaxations are '
                     'decided by each university per programme (Ch.3 Note: university policies on quota, category, relaxation '
                     'apply).',
             'topic': 'marks'}],
  'summary': 'One test for many central universities. Each university sets its own subject combination, minimum marks and '
             'relaxations.'},
 {'body': 'Consortium of National Law Universities',
  'courses': ['BA LLB (Hons) and other 5-year integrated LLB at participating NLUs'],
  'cycle': 'CUET',
  'group': 'univ',
  'id': 'clat-ug',
  'level': 'ug',
  'name': 'CLAT UG 2027',
  'needs': [],
  'not_found': ['Exact AIU fee, document list and processing time for a foreign-board Class 12 Equivalence Certificate '
                '(evaluation.aiu.ac.in returned HTTP 401; AIU page gives no details)',
                'AIU notification equating specific Indian/foreign school boards to Class 12 and the vocational equivalence list '
                '(linked PDFs not readable; 2022 public notice PDF could not be parsed)',
                'Official confirmation that NCERT/PARAKH has replaced AIU for school-board equivalence (only news reports)',
                'Official NIOS equivalence letter text and any UGC circular on NIOS (PDF not parseable; NIOS page lists AIU 1991 '
                'letter, MHRD 1990 resolution, AICTE 2025 circular)',
                'IB / Cambridge A level / American high school specific subject or marks conditions beyond the CUET list entry; '
                'American high school diploma is not in the CUET list',
                'Class 12 via Indian Army or other special routes (no official page found; only NDA Joint Services Wing is '
                'listed by CUET)',
                'CLAT 2027 full UG notification/brochure text (only eligibility web page, press release and some NLU brochures '
                'via search); PwD and other-category relaxations per NLU unverified',
                'Any CUET-wide minimum percentage or category relaxation (none exists in the bulletin; set by universities)'],
  'quals': {'cambridge': ['check', 'Equivalent examinations are accepted; confirm with the NLU.'],
            'cbse': ['yes', 'Class 12 with 45 percent (40 percent for SC, ST, PwD).'],
            'diploma': ['check', 'Only a press report says a diploma equal to Class 12 is accepted. Confirm with the NLU.'],
            'foreign': ['check',
                        'Equivalent examinations are accepted; get an AIU equivalence certificate and confirm with the NLU.'],
            'ib': ['check', 'Equivalent examinations are accepted; confirm with the NLU.'],
            'nios': ['check', 'The official page says 10+2 or equivalent; confirm with the NLU.'],
            'preuniv': ['check', 'The official page says 10+2 or an equivalent examination; confirm with the NLU.'],
            'voc': ['check', 'Not named in the notice; confirm with the exam body in writing.']},
  'rules': [{'source': 'https://consortiumofnlus.ac.in/clat-2027/ug-eligibility.html',
             'text': 'Passed 10+2 or an equivalent examination.',
             'topic': 'qualification'},
            {'source': 'https://consortiumofnlus.ac.in/clat-2027/ug-eligibility.html',
             'text': 'Minimum 45% marks or equivalent grade for candidates outside the reserved categories below; 40% for SC, ST '
                     'and PwD candidates (per the Consortium UG eligibility page). Individual NLU brochures may vary (search '
                     'summaries: HPNLU brochure shows 50% general / 45% SC-ST; NUALS shows 45% with state-specific relaxations), '
                     'so the target NLU brochure must be checked.',
             'topic': 'marks'},
            {'source': 'https://consortiumofnlus.ac.in/clat-2027/ug-eligibility.html',
             'text': 'Candidates appearing in the March/April 2027 qualifying exam can apply, but must produce proof of passing '
                     'the qualifying exam at admission or lose the right to be considered.',
             'topic': 'other'},
            {'source': 'https://consortiumofnlus.ac.in/clat-2027/notifications/Press_Release_CLAT_2027.pdf',
             'text': 'No upper age limit for UG. Exam Sunday 6 Dec 2026, 2:00-4:00 pm; application window 3 Aug - 31 Oct 2026 '
                     '(press release 22 Jul 2026).',
             'topic': 'other'},
            {'source': 'https://news.careers360.com/clat-2027-notification-out-live-nlu-law-registrationt-link-consortiumofnlus-ac-in-exam-date-syllabus-eligibility-fees-updates',
             'text': 'Press report, not confirmed on an official page: Careers360 report of the notification says a diploma or '
                     'other programme equivalent to Class 12 is also accepted; the official eligibility page only says 10+2 or '
                     'equivalent.',
             'topic': 'equivalence'}],
  'summary': 'Class 12 or equivalent with 45 percent (40 percent for SC, ST and PwD) on the Consortium page; individual NLU '
             'brochures may differ.'}]
