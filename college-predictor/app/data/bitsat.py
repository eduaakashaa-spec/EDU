"""Content for the BITSAT page (/bitsat).
Official facts come from the BITS Pilani admissions pages read on 11 November 2026: the BITSAT landing page and timeline, the First Degree brochure page, the BITSAT FAQs and the
schedule of fees for 2026-27 (admissions.bits-pilani.ac.in). The BITSAT-2026 brochure PDF was not available (HTTP 404) when we checked, so the exam pattern is the one in earlier
brochures and in secondary sources, and is tagged 'reported'. The BITSAT 2027 cycle was not announced on those pages; the 2026 cycle is shown as the reference.
Advice is labelled as EduAakashaA advice."""

UPDATED = '11 November 2026'
SITE = 'admissions.bits-pilani.ac.in'
SITE_URL = 'https://admissions.bits-pilani.ac.in/'
CONTACT = 'bitsat@pilani.bits-pilani.ac.in'

FACTS = [
    ('130', 'multiple-choice questions in the current pattern'),
    ('390', 'marks: +3 for a right answer, −1 for a wrong one'),
    ('3 hours', 'computer-based test, two sittings allowed'),
    ('75%', 'minimum aggregate in Class 12 PCM (and 60% in each subject)'),
    ('3 campuses', 'Pilani, K K Birla Goa and Hyderabad'),
    ('No JEE', 'the BITSAT score alone decides admission'),
]

PATTERN = [
    ('Mode and duration', 'Computer-based online test of 3 hours (180 minutes).', 'reported'),
    ('Questions', '130 multiple-choice questions with four options each. Papers up to 2021 had 150.', 'reported'),
    ('Physics', '30 questions.', 'reported'),
    ('Chemistry', '30 questions.', 'reported'),
    ('English Proficiency', '10 questions: grammar, vocabulary, reading comprehension and composition.', 'reported'),
    ('Logical Reasoning', '20 questions: verbal and non-verbal reasoning.', 'reported'),
    ('Mathematics', '40 questions. B.Pharm candidates (PCB) take Biology in this part instead.', 'reported'),
    ('Marking', '+3 for a right answer, −1 for a wrong answer, 0 for a blank. Maximum 390.', 'reported'),
    ('Extra questions', 'A candidate who finishes all 130 questions early can opt for up to 12 extra questions (4 each of Physics, Chemistry and Mathematics); once opted, there is no going back to the main paper.', 'reported'),
    ('Sessions', 'Two sessions are held; you can sit one or both, and the higher score counts for admission.', 'official'),
    ('Model papers', 'BITS Pilani does not provide any model question paper. The papers in circulation are memory-based.', 'official'),
]
PATTERN_NOTE = ('Guessing pays only when you are right more than 1 time in 4, because a wrong answer costs 1 mark and a right one earns 3. The marking above is as widely reported for 2022 onwards; '
                'confirm it in the current brochure on the BITS site, which we could not open when this page was prepared.')

DATES = [
    ('Applications open', '15 December 2025', 'official'),
    ('Session 1: last date to apply', '19 March 2026 (5:00 PM); edit window 21 to 22 March 2026', 'official'),
    ('Session 1: exam', '15 to 16 April 2026', 'official'),
    ('Session 2: registration', '20 April to 05 May 2026', 'official'),
    ('Session 2: exam', '24 to 26 May 2026', 'official'),
    ('Course preference (FD Preference Form)', 'Deadline 01 June 2026; candidates whose Class 12 results are pending can submit it between 21 April and 01 June', 'official'),
    ('Class 12 marks upload', 'On or before 10 July 2026', 'official'),
]
DATES_NOTE = ('This is the 2026 cycle. The BITSAT 2027 dates were not announced on the BITS admissions site on 11 November 2026. Several education sites expect applications to open in December 2026 and '
              'the tests in April and May 2027, but those are estimates. Confirm every date on the official site.')

ELIGIBILITY = [
    ('Class 12 marks', 'At least 75% in aggregate in Physics, Chemistry and Mathematics (PCM) and at least 60% in each subject. A 74.90% aggregate is not eligible even though it rounds to 75%.', 'official'),
    ('PCB students', 'Candidates with Physics, Chemistry and Biology are eligible only for B.Pharm. and the Environmental and Sustainability Engineering programme.', 'official'),
    ('Year of passing', 'For 2026-27: Class 12 passed in 2025, or appearing in 2026 with the result before June. Passing in 2024 is not eligible.', 'official'),
    ('JEE Main', 'BITS does not consider the JEE Main score. Admission is on the BITSAT score alone.', 'official'),
    ('If eligibility fails later', 'Candidature is cancelled at any stage if the eligibility rules are not met.', 'official'),
]

CAMPUSES = [
    ('BITS Pilani, Pilani campus (Rajasthan)', 'B.E. in ten branches, B.Pharm., six M.Sc. programmes (Biological Sciences, Chemistry, Economics, Mathematics, Physics, Semiconductor and Nanoscience) and M.Sc. General Studies.'),
    ('BITS Pilani, K K Birla Goa campus', 'B.E. in nine branches and the six M.Sc. programmes.'),
    ('BITS Pilani, Hyderabad campus', 'B.E. in ten branches, B.Pharm. and the six M.Sc. programmes.'),
    ('BITS Pilani, Dubai campus', 'Admission is handled separately: see bits-dubai.ac.ae.'),
]
CAMPUS_NOTE = 'Branch lists change from year to year: use the current brochure for the exact branches and seats. Exam centres are in India and abroad, including Dubai and Kathmandu.'

FEES = [
    ('Admission fee (one time)', 'Pilani, Goa and Hyderabad', '₹64,100'),
    ('Semester fee 2026-27', 'Pilani, Goa and Hyderabad', '₹2,91,500 per semester'),
    ('Semester fee later years', 'Printed for AY 2027-28 to 2030-31', '₹3,06,000 rising to ₹3,54,500'),
    ('Hostel (on-campus)', 'Per semester', '₹36,000, plus mess and electricity advance ₹10,000 and other advances ₹12,000'),
    ('Student Union and Aid Fund', 'Per year', '₹450 and ₹225'),
    ('Institute caution deposit', 'One time, refundable', '₹3,000'),
]
FEES_NOTE = ('Fees are from the BITS schedule for the academic year 2026-27 and change every year. The BITSAT application fee was not on the pages we read: check it on the application portal. '
             'Only the caution deposit and mess advance are refundable. Merit scholarships exist: BITS states that the top 2% receive a 100% tuition waiver and the top 5% up to a 100% waiver on merit-cum-need.')

SYLLABUS = [
    ('Physics', [
        ('Mechanics', 'Units and measurement, kinematics, laws of motion, work, energy and power, rotational motion, gravitation, properties of solids and fluids, oscillations.'),
        ('Waves and heat', 'Wave motion, sound, thermal properties, kinetic theory, thermodynamics.'),
        ('Electricity and magnetism', 'Electrostatics, current electricity, magnetic effects of current, electromagnetic induction, alternating current, electromagnetic waves.'),
        ('Optics and modern physics', 'Ray and wave optics, dual nature of matter, atoms and nuclei, electronic devices.')]),
    ('Chemistry', [
        ('Physical', 'States of matter, atomic structure, chemical bonding, thermodynamics, chemical and ionic equilibria, electrochemistry, chemical kinetics, solutions.'),
        ('Inorganic', 'Periodic table, hydrogen, s-block, p-block, d- and f-block elements, coordination compounds, environmental chemistry.'),
        ('Organic', 'IUPAC naming and isomerism, hydrocarbons, haloalkanes, alcohols, phenols and ethers, carbonyl compounds, carboxylic acids, amines, biomolecules, polymers, chemistry in everyday life.')]),
    ('English and reasoning', [
        ('English Proficiency', 'Grammar (agreement, tenses, parallel construction, relative pronouns), vocabulary (synonyms, antonyms, analogies), reading comprehension, composition (rearranging sentences, paragraph unity, linking).'),
        ('Verbal reasoning', 'Analogy, classification, series, coding and decoding, direction sense, blood relations, syllogisms.'),
        ('Non-verbal reasoning', 'Pattern perception, figure formation and analysis, paper folding and cutting, counting figures, completing a series of figures.')]),
    ('Mathematics', [
        ('Algebra', 'Sets, relations and functions, complex numbers, quadratic equations, sequences and series, permutations and combinations, binomial theorem, matrices and determinants.'),
        ('Trigonometry and geometry', 'Trigonometric functions and equations, inverse functions, heights and distances, straight lines, circles, conic sections, three-dimensional geometry, vectors.'),
        ('Calculus and data', 'Limits, continuity, differentiation, applications of derivatives, integration, differential equations, statistics, probability, mathematical reasoning.')]),
]
SYLLABUS_NOTE = 'Topics are grouped from the BITSAT syllabus as commonly published (Class 11 and 12 level). Read the official syllabus document on the BITS site for the exact list.'

PLAN = [
    ('Start with the NCERT base', 'Finish Class 11 and 12 Physics, Chemistry and Mathematics with NCERT-level problems first. BITSAT rewards speed on direct questions more than very hard ones.'),
    ('Train for speed', '130 questions in 180 minutes leaves about 80 seconds each. Practise English and Logical Reasoning (30 questions, the quickest marks) until each takes under a minute.'),
    ('Use past papers early', 'Sit one full year paper every week in the last two months, on a computer with the clock on. Then redo only the questions you rated Guess or got wrong while sure.'),
    ('Guess with care', 'A wrong answer costs 1 mark and a right one earns 3, so a guess pays only above 25% accuracy. Remove at least one option before you guess.'),
    ('Plan for two sittings', 'The higher of two sessions counts. Treat Session 1 as a real attempt and use the gap to fix your weakest subject, then decide whether to sit Session 2.'),
    ('Keep Class 12 on track', 'The 75% aggregate and 60% in each subject are conditions of admission, not only of applying. Do not let boards slip while you prepare.'),
]

FAQ = [
    ('Is the BITSAT paper published?', 'official', 'No. BITS Pilani states that it does not provide any model question paper. The papers you find online are memory-based reconstructions made after each sitting, so questions and answers can contain errors. Treat them as practice.'),
    ('Do I need JEE Main for BITS Pilani?', 'official', 'No. BITS does not consider the JEE Main score. Admission to the First Degree programmes is on the BITSAT score.'),
    ('Can I take BITSAT twice?', 'official', 'Yes, there are two sessions. You can appear in one or both, and the higher score is used.'),
    ('Which campuses and courses does BITSAT cover?', 'official', 'Pilani, K K Birla Goa and Hyderabad for B.E., B.Pharm. and M.Sc. programmes. Dubai admissions are separate. Mumbai is a separate campus with its own admission page.'),
    ('What marks do I need in Class 12?', 'official', '75% in PCM aggregate and at least 60% in each of Physics, Chemistry and Mathematics. PCB students can apply only for B.Pharm. and Environmental and Sustainability Engineering.'),
    ('How is the paper marked?', 'reported', '+3 for a right answer and −1 for a wrong one, 130 questions, 390 marks. Older papers (up to 2021) had 150 questions. Check the current brochure for any change.'),
    ('What can I do if I finish early?', 'reported', 'You may opt for up to 12 extra questions (4 each from Physics, Chemistry and Mathematics) after answering all 130. Once you opt in you cannot return to change the main paper.'),
    ('How should I use the EduAakashaA mock test centre?', 'advice', 'Take a full year paper under the clock, rate your confidence on every answer, then read the report: it shows how many marks negative marking cost you and which answers you were sure about but got wrong. Repeat with a different year.'),
]
TAGS = {'official': 'Official BITS Pilani page', 'reported': 'Widely reported: confirm in the brochure', 'advice': 'EduAakashaA advice'}

SOURCES = [
    ('BITSAT landing page and timeline', 'Dates, sessions, campuses and scholarships.', 'https://admissions.bits-pilani.ac.in/BITSAT_LP/index.html'),
    ('BITSAT FAQs', 'Eligibility rules, year of passing, Class 12 marks, FD preference form.', 'https://admissions.bits-pilani.ac.in/FD/BITSAT_FAQs.html'),
    ('First Degree brochure page', 'Campuses and programmes admitted through BITSAT.', 'https://admissions.bits-pilani.ac.in/FD/FD_brochure.html'),
    ('Schedule of fees 2026-27', 'Admission, semester, hostel and other fees.', 'https://admissions.bits-pilani.ac.in/FD/FD_fee.html'),
]
