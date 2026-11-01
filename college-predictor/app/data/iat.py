"""Content for the IISER Aptitude Test (IAT) page.
Official facts come from the IAT 2026 Information Brochure (March 2026) and the pages of https://www.iiseradmission.in/ read on 1 November 2026
(Important Dates, Eligibility, Fees, Seat Matrix, IAT for Other Institutes, Previous years' question papers, Mock Test).
The IAT 2027 cycle was not announced on that site on that date; the 2026 cycle is shown as the reference. Advice is labelled as EduAakashaA advice."""

UPDATED = '1 November 2026'
SITE = 'iiseradmission.in'
SITE_URL = 'https://www.iiseradmission.in/'
MOCK_URL = 'https://g06.tcsion.com//OnlineAssessment/index.html?2245@@M215'
BROCHURE_URL = 'https://www.iiseradmission.in/assets/pdfs/IB_IAT_2026_ENG.pdf'
PAPERS_URL = 'https://www.iiseradmission.in/#forms_and_certificate/pqpr'
CONTACT = 'askjac2026@iiserbpr.ac.in'

FACTS = [
    ('240', 'marks: 60 questions at 4 marks each'),
    ('180 min', 'computer-based test, 15 questions in each subject'),
    ('−1', 'for a wrong answer; blank answers score 0'),
    ('7 IISERs', 'plus 5 other institutions use the IAT rank'),
]

PATTERN = [
    ('Mode', 'Computer-based test (CBT) at centres across India'),
    ('Questions', '60 multiple-choice questions, only one correct answer: 15 each from Biology, Chemistry, Mathematics and Physics'),
    ('Duration', '180 minutes (one extra hour compensatory time for eligible PwD candidates)'),
    ('Marking', '+4 for a correct answer, −1 for a wrong answer, 0 if unanswered'),
    ('Maximum marks', '240. The total out of 240 is used for the rank list'),
    ('Language', 'English and Hindi'),
    ('Ranks', 'Not every candidate gets a rank. A rank does not guarantee an offer of admission to an IISER'),
]
PATTERN_NOTE = 'A wrong answer costs 1 mark and a right one earns 4, so guessing pays off on average only if you are right more than 1 time in 5 (20%).'

# 2026 cycle, the latest published on the IISER admission site
DATES = [
    ('Application portal opens', 'Thursday, 5 March 2026'),
    ('Application portal closes', 'Monday, 13 April 2026, 11:55 pm IST'),
    ('Corrections in application form', '16 April 2026, 11:00 am IST to 18 April 2026, 11:55 pm IST'),
    ('Hall tickets released', 'Sunday, 24 May 2026'),
    ('IAT 2026', 'Sunday, 7 June 2026, 9:00 am to 12:00 noon IST'),
    ('Answer key displayed', '7 June 2026'),
    ('Candidate response upload and objections open', '9 June 2026, closing 13 June 2026'),
    ('Selective information and document upload', '13 June to 21 June 2026'),
    ('Final answer key and IAT result', '29 June 2026'),
    ('Preference form for counselling', '2 July 2026, 5:00 pm IST to 9 July 2026, 5:00 pm IST'),
]
ROUNDS = [
    ('Round 1', '24 to 28 July 2026'), ('Round 2', '1 to 5 August'), ('Round 3', '10 to 13 August'), ('Round 4', '18 to 20 August'), ('Round 5', '24 to 26 August'),
    ('Round 6', '28 to 30 August'), ('Round 7', '1 to 3 September'), ('Round 8', '5 to 7 September'), ('Round 9', '9 to 11 September'),
]
ROUNDS_NOTE = 'Tentative schedule of counselling and admission offers (offer window, 5:00 pm IST end). Final withdrawal closed on 14 September 2026, 5:00 pm IST.'
DATES_NOTE = ('This is the 2026 cycle. IAT 2027 dates were not published on the IISER admission site on 1 November 2026. If the pattern repeats, expect applications to open around March and the test in early June, '
              'then confirm on the official site before planning.')

ELIGIBILITY = [
    ('Who can apply', 'Indian nationals, OCI/PIO card holders and foreign nationals'),
    ('Class 12 year (2026 cycle)', 'Passed Class XII or equivalent in 2024 or 2025, or appearing in 2026, from a board recognised by COBSE. A diploma of at least 3 years is also accepted. Passing in 2023 or earlier is not eligible.'),
    ('Subjects', 'At least three of Biology, Chemistry, Mathematics and Physics in Class XII, for the 5-year BS-MS at all IISERs'),
    ('Mathematics needed', 'BS-MS in Computational and Data Sciences (IISER Kolkata), B.Tech (IISER Bhopal), BS in Economic Sciences (IISER Bhopal), BS in Economic and Statistical Sciences (IISER Tirupati)'),
    ('Marks in Class XII', '60% aggregate, or 55% for SC, ST and PwD candidates, counting all subjects taken. Candidates waiting for results can apply, but admission depends on meeting the minimum.'),
    ('Reservation', 'SC 15%, ST 7.5%, OBC-NCL 27%, EWS up to 10%, PwD 5% (horizontal), Kashmiri Migrants 3 supernumerary seats per IISER. EWS and OBC-NCL certificates must be issued on or after 1 April 2026.'),
]

FEES = [
    ('Application fee', 'General, EWS, OBC, OBC-NCL', '₹2,000'),
    ('Application fee', 'SC, ST, PwD, Kashmiri Migrant and Kashmiri Pandit/Hindu families', '₹1,000'),
    ('Application fee', 'Foreign nationals', '₹12,000'),
    ('Seat acceptance fee', 'General, EWS, OBC-NCL, PwD and Kashmiri categories', '₹35,000 (₹25,000 plus ₹10,000 non-refundable)'),
    ('Seat acceptance fee', 'SC and ST', '₹17,500 (₹12,500 plus ₹5,000 non-refundable)'),
]
FEES_NOTE = 'The application fee is non-refundable. The seat acceptance fee is paid only after an offer and is adjusted against the first-semester fee; the fee structure differs between IISERs.'

# the seven IISERs with their 2026 BS-MS seats (tentative, including supernumerary) and the other programmes at each campus
IISERS = [
    ('IISER Berhampur', 'Odisha', 'iiserbpr.ac.in', 300, []),
    ('IISER Bhopal', 'Madhya Pradesh', 'iiserb.ac.in', 300, ['B.Tech in Chemical Engineering (40)', 'B.Tech in Electrical Engineering and Computer Science (75)', 'B.Tech in Data Science and Engineering (80)', 'BS in Economic Sciences (55)']),
    ('IISER Kolkata', 'West Bengal', 'iiserkol.ac.in', 280, ['BS-MS in Computational and Data Sciences (30)']),
    ('IISER Mohali', 'Punjab', 'iisermohali.ac.in', 275, ['Majors in Geology and Environmental Sciences are new in the regular BS-MS']),
    ('IISER Pune', 'Maharashtra', 'iiserpune.ac.in', 288, []),
    ('IISER Thiruvananthapuram', 'Kerala', 'iisertvm.ac.in', 320, []),
    ('IISER Tirupati', 'Andhra Pradesh', 'iisertirupati.ac.in', 250, ['BS in Economic and Statistical Sciences (50)']),
]
SEATS_TOTAL = 2343
SEATS_NOTE = 'Tentative total of 2,343 seats across BS-MS, BS and B.Tech, including supernumerary seats. The numbers in brackets are seats for that programme.'

OTHERS = [
    ('Indian Institute of Science (IISc), Bengaluru', '4-year Bachelor of Science (BS) (Research) programme'),
    ('Indian Institute of Technology Madras', '4-year Bachelor of Science (BS) programme'),
    ('Indian Institute of Technology Guwahati', '4-year BS programme in Biomedical Science and Engineering'),
    ('Indian Association for the Cultivation of Science (IACS), Kolkata', 'Integrated Bachelor’s–Master’s in Science (BS-MS) programme'),
    ('Indian Institute of Engineering Science and Technology (IIEST), Shibpur', '5-year BS-MS in Chemistry, Physics and Applied Geology'),
]
OTHERS_NOTE = ('To apply to any of these you must complete both steps: apply to the IAT on the IISER portal, then apply to the programme separately on that institute’s website. '
               'Their eligibility and admission rules can differ from the IISERs’.')

PROGRAMMES = ['5-year BS-MS (dual degree) at all seven IISERs', '5-year BS-MS in Computational and Data Sciences (IISER Kolkata)', '4-year BS in Economic Sciences (IISER Bhopal)',
              '4-year BS in Economic and Statistical Sciences (IISER Tirupati)', '4-year B.Tech in Chemical Engineering, Data Science and Engineering, and Electrical Engineering and Computer Science (IISER Bhopal)']

# syllabus, as listed in the 2026 brochure
SYLLABUS = [
    ('Biology', [
        ('Diversity in the living world', 'Biological classification and the five kingdoms, viruses, viroids and lichens; plant kingdom; animal kingdom'),
        ('Structural organisation in plants and animals', 'Morphology and anatomy of flowering plants; organ systems; frog'),
        ('Cell: structure and functions', 'Cell theory, prokaryotic and eukaryotic cells; biomolecules and enzymes; cell cycle, mitosis and meiosis'),
        ('Plant physiology', 'Photosynthesis (light reaction, C4 pathway, photorespiration); respiration; plant growth and growth regulators'),
        ('Human physiology', 'Breathing and gas exchange; body fluids and circulation; excretion; locomotion; neural control; chemical coordination'),
        ('Reproduction', 'Sexual reproduction in flowering plants; human reproduction; reproductive health'),
        ('Genetics and evolution', 'Inheritance and variation; molecular basis of inheritance; evolution, Hardy–Weinberg principle'),
        ('Biology in human welfare', 'Human health and disease, immunity, cancer; microbes in human welfare'),
        ('Biotechnology', 'Principles, processes and applications of recombinant DNA technology'),
        ('Ecology', 'Organisms and populations, logistic growth; ecosystem and energy flow; biodiversity and conservation'),
    ]),
    ('Chemistry', [
        ('Basic concepts and atomic structure', 'Mole concept, stoichiometry; Bohr model, quantum mechanical model'),
        ('Periodicity and chemical bonding', 'Periodic trends; VSEPR, valence bond theory, hybridisation, molecular orbital theory, hydrogen bonding'),
        ('d- and f-block elements and coordination compounds', 'Properties of transition elements; Werner’s theory, nomenclature, isomerism, bonding, metal carbonyls'),
        ('Thermodynamics, equilibrium and redox', 'Enthalpy, Gibbs energy; chemical and ionic equilibria, buffers, solubility; oxidation number and electrode processes'),
        ('Solutions, electrochemistry and kinetics', 'Colligative properties; Nernst equation, conductance, batteries; rate laws and temperature dependence'),
        ('Organic chemistry: principles and hydrocarbons', 'Isomerism, reaction mechanism, purification and analysis; alkanes, alkenes, alkynes, aromatic hydrocarbons'),
        ('Organic chemistry: functional groups', 'Haloalkanes and haloarenes; alcohols, phenols and ethers; aldehydes, ketones and carboxylic acids; amines and diazonium salts'),
        ('Biomolecules', 'Carbohydrates, proteins, enzymes, vitamins, nucleic acids, hormones'),
    ]),
    ('Mathematics', [
        ('Sets, relations and functions', 'Sets, Venn diagrams, relations, types of functions, composition, inverse'),
        ('Counting and binomial theorem', 'Permutations and combinations; binomial theorem, Pascal’s triangle'),
        ('Complex numbers and equations', 'Argand plane, modulus and conjugate; quadratic equations; linear inequalities'),
        ('Trigonometry', 'Identities, equations, inverse trigonometric functions and graphs'),
        ('Vectors and matrices', 'Dot and cross products, projection; matrices, determinants, adjoint and inverse'),
        ('Coordinate and 3D geometry', 'Lines, circle, parabola, ellipse, hyperbola; lines and planes in space, shortest distance'),
        ('Sequences and series', 'AP and GP, AM–GM, special sums'),
        ('Limits, differentiation and applications', 'Limits, continuity; derivatives, chain rule, implicit and parametric; rate of change, maxima and minima, tangents and normals'),
        ('Integration and differential equations', 'Substitution, parts, partial fractions, definite integrals, area; separation of variables, homogeneous and linear equations'),
        ('Statistics and probability', 'Mean deviation, variance, standard deviation; conditional probability, total probability, Bayes’ theorem'),
    ]),
    ('Physics', [
        ('Mechanics 1', 'Units and dimensions; motion in a straight line and in a plane; laws of motion'),
        ('Mechanics 2', 'Work, energy and power; collisions; system of particles and rotational motion'),
        ('Gravitation and properties of matter', 'Kepler’s laws, escape speed, satellites; elasticity; fluids, Bernoulli’s principle, viscosity, surface tension'),
        ('Heat and thermodynamics', 'Calorimetry, heat transfer; laws of thermodynamics, Carnot engine; kinetic theory of gases'),
        ('Oscillations and waves', 'Simple harmonic motion, pendulum; progressive waves, superposition, beats'),
        ('Electrostatics and current electricity', 'Coulomb’s law, Gauss’s law; potential, capacitors; Ohm’s law, Kirchhoff’s rules'),
        ('Magnetism and electromagnetic induction', 'Biot–Savart and Ampere’s laws; magnetism and matter; Faraday’s and Lenz’s laws; AC circuits'),
        ('Optics and electromagnetic waves', 'Electromagnetic spectrum; ray optics and instruments; wave optics, interference, diffraction, polarisation'),
        ('Modern physics', 'Photoelectric effect and matter waves; atoms and Bohr model; nuclei; semiconductor devices'),
    ]),
]
SYLLABUS_NOTE = 'Topics are grouped from the 2026 brochure (pages 23 to 32). The brochure lists every sub-topic; read it before you plan your revision.'

# papers: year, official link text, what EduAakashaA holds
PAPERS = [
    ('2026', 'Answer key (final and provisional)', 'IAT 2026 held on 7 June 2026'),
    ('2025', 'Question paper', ''),
    ('2024', 'Question paper', ''),
    ('2023', 'Question paper', ''),
    ('2022', 'Question paper', ''),
    ('2021', 'Question paper', ''),
    ('2019', 'Question paper', ''),
    ('2018', 'Question paper (English only)', ''),
    ('2017', 'Question paper', ''),
]
PAPERS_NOTE = 'The official site lists the question papers for 2017 to 2025 (no paper for 2020). The 2025 and 2026 documents also carry the official answer key. For the earlier years the site does not publish keys.'

PLAN = [
    ('Biology (60 marks)', 'NCERT Class 11 and 12, line by line, including figures and tables. Add data-based questions: pedigrees, enzyme kinetics graphs, gene regulation, population curves.'),
    ('Chemistry (60 marks)', 'Physical chemistry numericals, bonding and coordination chemistry, and organic mechanisms. Practise reading reaction schemes and chromatograms.'),
    ('Mathematics (60 marks)', 'Class 11 and 12 depth rather than tricks: functions, calculus, complex numbers, conics and probability. Solve each question two ways when you can.'),
    ('Physics (60 marks)', 'Conceptual mechanics, thermodynamics, electrostatics, optics and modern physics, with units and dimension checks as a habit.'),
    ('Strategy', 'Each section has 15 questions for 60 marks, so protect time for the section you are weakest in. Mark guesses, then come back. Attempt a question when you can remove at least one option and are better than 20% likely to be right.'),
]

FAQ = [
    ('Is the IAT the only way into an IISER?', 'official', 'Yes for 2026. The brochure says all students admitted to IISERs in 2026–27 are admitted through the IAT 2026.'),
    ('Do I need JEE or NEET marks?', 'official', 'No. Admission uses the IAT score only, plus the Class XII eligibility conditions. The IAT is separate from JEE Main, JEE Advanced and NEET.'),
    ('Can a Biology student without Mathematics apply?', 'official', 'Yes for the 5-year BS-MS: you need at least three of Biology, Chemistry, Mathematics and Physics. Some programmes need Mathematics; see Who can apply.'),
    ('Is there negative marking?', 'official', 'Yes. 4 marks for a correct answer, minus 1 for a wrong answer and 0 for unanswered questions.'),
    ('Does a rank mean a seat?', 'official', 'No. Not every candidate is ranked and a rank does not guarantee an offer. Seats are offered through counselling rounds.'),
    ('Can I apply to IISc, IIT Madras or IACS with the same score?', 'official', 'Yes, for the programmes listed above, but you must apply separately on each institute’s website as well as for the IAT.'),
    ('Which IISER should I choose?', 'advice', 'Compare programmes, location, research areas and the closing ranks of past rounds, which the official site publishes. The mentorship programme helps you build a preference list.'),
    ('How early should preparation start?', 'advice', 'Class 11 students should build NCERT depth in all four subjects. A twelve-month plan before the June test works well for most students.'),
]
TAGS = {'official': 'Official source', 'advice': 'EduAakashaA advice'}

SOURCES = [
    ('IAT 2026 Information Brochure (March 2026)', 'Pattern, eligibility, programmes, syllabus, other institutions', BROCHURE_URL),
    ('iiseradmission.in', 'Important dates, eligibility, fees, seat matrix, IAT for other institutes, previous years’ papers, mock test', SITE_URL),
    ('Official IAT mock test', 'Practice on the official computer-based interface', MOCK_URL),
]
