"""Content for the JEE Main 2027 Paper 2A (B.Arch) and Paper 2B (B.Planning) guide.
Official facts come from NTA's Information Bulletin for JEE (Main) 2027 and the 2027 syllabus PDF (Paper 2A / 2B pages).
Anything that is EduAakashaA advice, not NTA's rule, is labelled as such on the page. The practice questions are original,
written for this page: they are not NTA questions."""

UPDATED = '1 November 2026'
NTA = 'jeemain.nta.nic.in'
NTA_PRACTICE = 'https://nta.ac.in/Quiz'

FACTS = [
    ('400', 'marks in each paper, 3 hours'),
    ('22 Nov', 'Session 1 applications close, 11:50 pm IST'),
    ('20 to 28 Jan', 'Session 1 exam days (Paper 2 dates are on the admit card)'),
    ('1 form', 'one application covers 2A, 2B or both'),
]

# (name, rows)
SESSIONS = [
    ('Session 1 (January 2027)', [
        ('Application form', '24 October to 22 November 2026, up to 11:50 pm'),
        ('Fee payment', 'Last day 22 November 2026, up to 11:50 pm'),
        ('With late fee of ₹500', '23 to 26 November 2026, up to 11:50 pm'),
        ('Corrections', '27 to 29 November 2026, up to 11:50 pm'),
        ('City intimation slip', '30 December 2026'),
        ('Admit card', '13 January 2027'),
        ('Exam days', '20, 21, 22, 23, 24 and 28 January 2027'),
    ]),
    ('Session 2 (April 2027)', [
        ('Application form', '5 January to 3 February 2027, up to 11:50 pm'),
        ('Fee payment', 'Last day 3 February 2027, up to 11:50 pm'),
        ('With late fee of ₹500', '4 to 7 February 2027, up to 11:50 pm'),
        ('Corrections', '8 to 10 February 2027, up to 11:50 pm'),
        ('City intimation slip', '12 March 2027'),
        ('Admit card', '25 March 2027'),
        ('Exam days', '2, 3, 4, 5, 6 and 7 April 2027'),
    ]),
]
DATES_NOTE = ('The bulletin gives these dates for the whole of JEE (Main). The exact day, shift and city for Paper 2A and Paper 2B are printed '
              'on your admit card. NTA publishes the answer key and your recorded response for challenges on its website after each session.')

# countdown targets used by the page script: (label, ISO date, time note)
DEADLINES = [
    ('Session 1: apply', '2026-11-22', 'closes 11:50 pm IST'),
    ('Session 1: with late fee', '2026-11-26', 'last day, ₹500 extra'),
    ('Session 1: corrections', '2026-11-29', 'window ends 11:50 pm IST'),
    ('Session 1: admit card', '2027-01-13', 'download from NTA'),
    ('Session 2: apply', '2027-02-03', 'closes 11:50 pm IST'),
    ('Session 2: exam starts', '2027-04-02', 'Paper 2 day is on your admit card'),
]

WHICH = [
    ('Paper 2A: B.Arch', 'Bachelor of Architecture', 'Mathematics (CBT), Aptitude (CBT) and a Drawing Test on paper', 'Students who like to sketch and design, think in 3D and want to become architects.', '77 questions, 400 marks'),
    ('Paper 2B: B.Planning', 'Bachelor of Planning', 'Mathematics, Aptitude and Planning-based questions, all on the computer', 'Students who care about cities, transport, land use and policy, and prefer reading and reasoning to drawing.', '100 questions, 400 marks'),
    ('Both papers', 'B.Arch and B.Planning', 'One sitting of 3 hours 30 minutes', 'Students who are open to either course and can manage the extra hour.', 'One form, higher fee'),
]

# part, 2A, 2B
PATTERN = [
    ('Part I: Mathematics', '20 MCQs (Section A) + 5 numerical-value questions (Section B), 100 marks', 'Same: 20 MCQs + 5 numerical-value questions, 100 marks'),
    ('Part II: Aptitude Test', '50 MCQs, 200 marks', 'Same: 50 MCQs, 200 marks'),
    ('Part III', 'Drawing Test: 2 questions on an A4 drawing sheet, 100 marks, pen and paper', 'Planning-based questions: 25 MCQs, 100 marks, on the computer'),
    ('Total', '77 questions, 400 marks', '100 questions, 400 marks'),
    ('Mode', 'Parts I and II on the computer; Part III offline on paper', 'All three parts on the computer'),
]
MARKING = [
    ('Correct MCQ or numerical answer', '+4'),
    ('Wrong answer', '−1 (both MCQs and numerical-value questions)'),
    ('Unanswered or marked for review without an answer', '0'),
    ('Drawing Test (2A only)', 'Two questions evaluated out of 100 marks. The bulletin does not list a negative mark for it.'),
]
PATTERN_NOTES = [
    'Section B (numerical): you type an integer using the on-screen keypad. The answer is rounded off to the nearest integer.',
    'Aptitude is half the paper (200 of 400). Mathematics is a quarter. Many students over-invest in mathematics.',
    'If a question has more than one correct option, only those who marked a correct option get +4. If a question is dropped, every candidate in that shift gets full marks for it.',
    'Overall merit joins the NTA scores of every shift of both sessions. If you sit both sessions, the better score counts.',
    'Ties are broken in this order: Mathematics score, then Aptitude score, then Drawing score (2A) or Planning score (2B), then the proportion of wrong to right answers.',
]
TIME = [
    ('Paper 2A or 2B alone', '3 hours', '4 hours for candidates entitled to a scribe'),
    ('2A and 2B together', '3 hours 30 minutes', '4 hours 40 minutes for candidates entitled to a scribe'),
    ('Shift times (3 hours)', '9:00 am to 12:00 noon, or 3:00 pm to 6:00 pm IST', ''),
    ('Shift times (3.5 hours)', '9:00 am to 12:30 pm, or 3:00 pm to 6:30 pm IST', ''),
]

FEES_HEAD = ('Centre in India', 'Centre outside India')
FEES = [
    ('One paper (2A or 2B): General male', '₹1,000', '₹5,000'),
    ('One paper: General female', '₹800', '₹4,000'),
    ('One paper: Gen-EWS or OBC-NCL male', '₹900', '₹4,500'),
    ('One paper: Gen-EWS or OBC-NCL female', '₹800', '₹4,000'),
    ('One paper: SC, ST, PwD or PwBD (all)', '₹500', '₹2,500'),
    ('2A and 2B together: General, EWS, OBC-NCL male', '₹2,000', '₹10,000'),
    ('2A and 2B together: General, EWS, OBC-NCL female', '₹1,600', '₹8,000'),
    ('2A and 2B together: SC, ST, PwD or PwBD', '₹1,000', '₹5,000'),
]
FEES_NOTE = ('Per session. Processing charges and GST are extra. A late fee of ₹500 applies to every category. '
             'Adding Paper 1 (B.E. or B.Tech) to a Paper 2 uses the same combined rows. Third-gender candidates pay the SC/ST rate.')

# who can apply
ELIGIBILITY = [
    ('Class 12 year', 'Passed Class 12 or equivalent in 2025 or 2026, or appearing in 2027. Candidates who passed in 2024 or earlier are not eligible for JEE (Main) 2027.'),
    ('Age', 'NTA sets no age limit. Individual institutes may.'),
    ('Qualifying boards', 'CBSE, CISCE, state boards, intermediate or pre-university, NIOS with five subjects, IB, Cambridge A level, and other boards NTA lists in Chapter 3 of the bulletin.'),
    ('Admission rules are separate', 'NTA runs the test only. Each institute and the Council of Architecture set subject and mark conditions for B.Arch, and each planning school sets its own. Check the institute before you pay for anything.'),
]

SYLLABUS_MATHS_NOTE = ('Mathematics is the same 14 units for 2A and 2B. The only difference in the syllabus text is that Paper 2A lists areas under '
                       '"simple curves in standard forms" and Paper 2B says "simple curves".')

# (unit, title, topics, plain-words tip)
MATHS = [
    (1, 'Sets, relations and functions', 'Sets, union, intersection, complement, power set; types of relations, equivalence relations; one-one, into and onto functions; composition of functions.', 'Short, scoring. Practise definitions and counting functions.'),
    (2, 'Complex numbers and quadratic equations', 'Complex numbers as a + ib, Argand diagram, modulus and argument; quadratic equations, relations between roots and coefficients, nature of roots.', 'Roots and discriminant questions are quick marks.'),
    (3, 'Matrices and determinants', 'Types of matrices, determinants of order 2 and 3, area of triangle, adjoint and inverse, consistency of linear equations.', 'Learn the formulas; calculations are short.'),
    (4, 'Permutations and combinations', 'Counting principle, P(n, r), C(n, r), simple applications.', 'Practise word problems; they test reading more than formulas.'),
    (5, 'Binomial theorem', 'Positive integral index, general term, middle term.', 'Learn the general-term formula and use it.'),
    (6, 'Sequence and series', 'AP and GP, inserting means, relation between AM and GM.', 'Formula recall.'),
    (7, 'Limit, continuity and differentiability', 'Functions and graphs, limits, continuity, derivatives of standard functions, derivatives up to order two, rate of change, increasing and decreasing functions, maxima and minima.', 'The largest block of calculus. Spend time here.'),
    (8, 'Integral calculus', 'Anti-derivatives, substitution, parts, partial fractions, definite integrals, fundamental theorem, area under simple curves.', 'Standard integrals first, then substitution.'),
    (9, 'Differential equations', 'Order and degree, variables separable, homogeneous and linear equations of the first order.', 'Pattern questions; learn the three types.'),
    (10, 'Co-ordinate geometry', 'Straight lines, distance and section formulas, centroid, orthocentre, circumcentre; circle; parabola, ellipse, hyperbola in standard form.', 'Draw every problem. Architects will find this natural.'),
    (11, 'Three-dimensional geometry', 'Points in space, distance, section formula, direction ratios and cosines, lines, skew lines, shortest distance.', 'Good link with spatial thinking.'),
    (12, 'Vector algebra', 'Vectors and scalars, addition, components in 2D and 3D, scalar and vector products.', 'Short and formula based.'),
    (13, 'Statistics and probability', 'Mean, median, mode, variance, standard deviation, mean deviation; probability, addition and multiplication theorems, Bayes theorem, distributions.', 'Careful reading; avoid sign slips.'),
    (14, 'Trigonometry', 'Identities, trigonometric and inverse trigonometric functions and their properties.', 'Revise identities weekly; they feed other units.'),
]

# aptitude units, shared by 2A and 2B
APTITUDE = [
    ('Unit 1: awareness and visualising', [
        'Awareness of persons, buildings, materials, objects and textures related to architecture and the built environment',
        'Visualising three-dimensional objects from two-dimensional drawings',
        'Visualising different sides of three-dimensional objects',
        'Analytical reasoning and mental ability: visual, numerical and verbal',
    ], 'Read about famous buildings and architects, notice materials around you, and practise reasoning puzzles daily.'),
    ('Unit 2: three-dimensional perception', [
        'Scale and proportion of objects, building forms and elements',
        'Colour, texture, harmony and contrast',
        'Designing and drawing geometrical or abstract shapes and patterns in pencil',
        'Transforming forms in 2D and 3D: union, subtraction, rotation, development of surfaces and volumes',
        'Plans, elevations and 3D views of objects; making 2D and 3D compositions from given shapes',
    ], 'Build small models from paper, draw top, front and side views of everyday objects, and rotate shapes in your head.'),
]
DRAWING = {
    'title': 'Part III for Paper 2A: Drawing Test',
    'topics': [
        'Sketching scenes and activities from memory: urban life (public spaces, markets, festivals, street scenes, monuments, recreation spaces)',
        'Landscape: riverfronts, jungle, gardens, trees, plants',
        'Rural life',
    ],
    'rules': [
        'Done offline on an A4 drawing sheet.',
        'Bring your own geometry box, pencils, erasers, and colour pencils or crayons.',
        'Water colours are not allowed on the sheet.',
        'Two questions are evaluated out of 100 marks. NTA adds the digitally evaluated marks to your total.',
    ],
    'tip': 'Practise one 20-minute sketch a day from memory: a market, a street, a garden. Show people, scale and depth, not only the building.',
}
PLANNING = {
    'title': 'Part III for Paper 2B: Planning',
    'units': [
        ('Unit 1: general awareness', 'General knowledge about prominent cities, development issues, government programmes.'),
        ('Unit 2: social sciences', 'Nationalism and nationalism in India, the pre-modern world, the 19th-century global economy, colonialism and colonial cities, industrialisation, resources and development (agriculture, water, minerals, industries, national economy), human settlements; power-sharing, federalism, political parties, democracy, the Constitution of India; economic sectors, globalisation, the idea of development, poverty; population structure, social exclusion and inequality, urbanisation, rural development.'),
        ('Unit 3: thinking skills', 'Comprehension of an unseen passage; map-reading (scale, distance, direction, area); critical reasoning; reading charts, graphs and tables; basic statistics and quantitative reasoning.'),
    ],
    'tip': 'The social-science list reads like Class 9 and 10 NCERT geography, history, civics and economics. Revise those, then add a newspaper habit about cities and government schemes.',
}

CHOOSE = [
    ('Choose 2A (B.Arch) if', ['you sketch, doodle or build things without being asked', 'you can imagine a shape from another side', 'you enjoy buildings, spaces and how they feel', 'you can commit to daily drawing practice']),
    ('Choose 2B (B.Planning) if', ['you notice traffic, water, housing and how cities grow', 'you like maps, data, reading and debate', 'you prefer reasoning to drawing', 'you are curious about policy and public systems']),
    ('Take both if', ['you honestly like both sets of ideas', 'you can handle 3 hours 30 minutes', 'you will give the Drawing Test real practice', 'your family accepts the higher fee']),
]

# month, what, who (EduAakashaA suggestion, not an NTA rule)
PLAN = [
    ('Now to 22 Nov', 'Decide 2A, 2B or both. Collect documents. Submit the form. Do not wait for the last day.'),
    ('Dec', 'Finish the syllabus read-through. Start a daily 20-minute sketch (2A) or newspaper habit (2B). Take the NTA practice test once to learn the screen.'),
    ('Early Jan', 'Mixed practice: 25 maths questions, 25 aptitude questions, one sketch or one planning set, per day. Download the admit card on 13 Jan.'),
    ('20 to 28 Jan', 'Session 1. Afterwards, review the answer key and your response sheet. Note which units cost you marks.'),
    ('Feb', 'Apply for Session 2 (5 Jan to 3 Feb). Fix the weakest units. Do three full timed papers.'),
    ('March to April', 'Admit card on 25 March. Two sketching sessions a week at exam length. Session 2 runs 2 to 7 April.'),
]

PARENTS = [
    ('Time and cost', 'One form covers both papers. Fees are per session and rise sharply for a centre outside India. Add GST and processing charges to the budget.'),
    ('The drawing kit', 'Buy the geometry box, pencils, erasers and colour pencils early so your child practises with the same tools. No water colours.'),
    ('Two chances', 'Session 1 is a rehearsal, Session 2 is the improvement. NTA uses the better score.'),
    ('What to ask schools', 'Whether the institute needs another test or portfolio, which conditions the Council of Architecture sets, and when counselling opens. NTA does not run counselling.'),
    ('How to help', 'Protect sleep, ask to see this week\'s sketches, and read the answer key together after each mock.'),
    ('Do not panic', 'Aptitude is half the marks. A student weaker in mathematics can still score well by being strong in aptitude and drawing or planning.'),
]

# interest check: (statement, axis) axis A architecture/drawing, S spatial, M maths, P planning/people, G reading/GK
INTEREST = [
    ('I like sketching or doodling even when no one asks me to.', 'A'),
    ('I notice how buildings, bridges and streets look and feel.', 'A'),
    ('I enjoy building models, Lego, paper craft or craft work.', 'S'),
    ('I can imagine how an object looks from the back or the top.', 'S'),
    ('I enjoy solving maths puzzles and getting an exact answer.', 'M'),
    ('I like finding patterns in numbers, shapes or tables.', 'M'),
    ('I wonder why some neighbourhoods are crowded or have poor roads.', 'P'),
    ('I like reading maps, charts or data about cities and people.', 'P'),
    ('I follow news about cities, housing, water, transport or government schemes.', 'G'),
    ('I enjoy reading a passage and answering questions on it.', 'G'),
    ('I would rather finish a drawing than write an essay.', 'A'),
    ('I like debating how public money should be spent.', 'P'),
]
AXES = {'A': 'Design and drawing', 'S': 'Spatial thinking', 'M': 'Mathematics and reasoning', 'P': 'Cities and people', 'G': 'Reading and awareness'}

# mini aptitude: (area, question, options, answer index, explanation)
QUIZ = [
    ('Spatial', 'A solid cube is painted red on all faces and cut into 27 equal small cubes (3 × 3 × 3). How many small cubes have exactly two red faces?',
     ['8', '12', '6', '1'], 1, 'Edge cubes that are not corners: 12 edges × 1 middle cube each = 12. Corners (8) have three faces, face centres (6) have one, the core (1) has none.'),
    ('Spatial', 'A triangular prism has how many faces in all?',
     ['4', '5', '6', '9'], 1, 'Two triangular ends plus three rectangular sides = 5.'),
    ('Views', 'A cylinder standing on its circular base is seen from directly above. The view is:',
     ['A rectangle', 'A triangle', 'A circle', 'An ellipse'], 2, 'The top view of an upright cylinder is its circular top.'),
    ('Scale', 'A plan is drawn to a scale of 1 : 500. A wall measures 3.2 cm on the plan. Its real length is:',
     ['6.4 m', '16 m', '160 m', '1.6 m'], 1, '3.2 cm × 500 = 1,600 cm = 16 m.'),
    ('Numerical', 'Find the next number: 2, 6, 12, 20, 30, ?',
     ['40', '42', '44', '36'], 1, 'The differences grow by 2 each time (4, 6, 8, 10, then 12): 30 + 12 = 42.'),
    ('Verbal', 'Blueprint is to building as score is to:',
     ['Orchestra', 'Music', 'Singer', 'Theatre'], 1, 'A blueprint is the plan for a building; a musical score is the written plan for music.'),
    ('Awareness', 'Which material, made by heating limestone with clay and grinding the result, is the binder in concrete?',
     ['Gypsum plaster', 'Lime paint', 'Cement', 'Bitumen'], 2, 'Cement is made from heated limestone and clay (clinker), and binds sand and aggregate in concrete.'),
    ('Colour', 'In the standard colour wheel, the complement of blue is:',
     ['Green', 'Orange', 'Violet', 'Red'], 1, 'Blue sits opposite orange; complementary colours create strong contrast.'),
    ('Map reading', 'On a map 1 cm stands for 2 km. A rectangular park measures 3 cm × 2 cm on the map. Its real area is:',
     ['6 km²', '12 km²', '24 km²', '48 km²'], 2, 'Real sides are 6 km and 4 km, so the area is 24 km².'),
    ('Charts', 'A city grew from 40 lakh to 46 lakh people in ten years. The growth was:',
     ['6%', '12%', '15%', '18%'], 2, '6 ÷ 40 = 0.15, so 15%.'),
    ('Planning', 'Why do planners encourage mixed land use (homes, shops and offices close together)?',
     ['To raise land prices only', 'To shorten daily travel and keep streets active', 'To stop all vehicles', 'To reduce green space'], 1, 'Mixed use puts daily needs within a short distance, which cuts travel time and keeps streets in use.'),
    ('Mathematics', 'The slope of the line 2x + 3y = 6 is:',
     ['2/3', '−2/3', '3/2', '−3/2'], 1, 'Write y = −(2/3)x + 2; the slope is −2/3.'),
]
QUIZ_NOTE = ('These twelve items were written by EduAakashaA for this page, in the style of the syllabus units. They are not NTA questions. '
             'For NTA\'s own computer-based practice, use the Test Practice Centre at nta.ac.in/Quiz and check which exam and paper it offers.')

FAQ = [
    ('Do I need to apply separately for 2A and 2B?', 'official', 'No. It is one application form. You choose Paper 2A, Paper 2B, or both, and the fee depends on the choice.'),
    ('Is the Drawing Test on the computer?', 'official', 'No. Parts I and II of Paper 2A are on the computer. Part III, the Drawing Test, is on paper using an A4 drawing sheet.'),
    ('What can I carry for drawing?', 'official', 'Your own geometry box set, pencils, erasers and colour pencils or crayons. Water colours are not allowed on the sheet.'),
    ('Is there negative marking?', 'official', 'Yes. +4 for a correct answer and −1 for a wrong answer, in both MCQs and numerical-value questions. The Drawing Test is marked out of 100.'),
    ('How long is the exam?', 'official', '3 hours for one paper, 3 hours 30 minutes if you take both 2A and 2B in one sitting.'),
    ('If I appear in both sessions, which score counts?', 'official', 'The better of your JEE (Main) 2027 NTA scores is used for ranking.'),
    ('Is the syllabus the same as for Paper 1?', 'official', 'No. Paper 2 has its own syllabus: 14 units of mathematics (no physics or chemistry), an aptitude test, and either a drawing test or planning-based questions.'),
    ('Is NATA needed as well?', 'check', 'NTA does not decide this. Many institutes accept either NATA or JEE Main Paper 2 for B.Arch, but rules differ by institute and by counselling. Check the institute and see our NATA page.'),
    ('Which seats does the Paper 2 rank open?', 'check', 'The bulletin says Paper 2 is for admission to B.Arch and B.Planning courses in the country. Counselling bodies publish their own rules and seat lists, so read their brochure for 2027 when it appears.'),
    ('Can I take only Paper 1 and Paper 2A?', 'official', 'Yes. The bulletin lists the combinations Paper 1 with 2A, Paper 1 with 2B, Paper 1 with both, or 2A with 2B. Each has its own fee row.'),
    ('How should a student weak at drawing prepare?', 'advice', 'Start with simple shapes, perspective and proportion, 20 minutes a day, from memory and from real scenes. Ask a mentor to review a weekly sheet. If drawing still feels like a chore after a month, consider Paper 2B.'),
    ('What if my city intimation slip shows a far city?', 'official', 'Write to NTA through the helpline listed on the bulletin. Do not change your exam plan without a reply in writing.'),
]
TAGS = {'official': 'Official source', 'check': 'Check with the institute', 'advice': 'EduAakashaA advice'}

SOURCES = [
    ('NTA Information Bulletin, JEE (Main) 2027', 'Dates, fees, pattern, marking, timing, drawing-kit rules (Chapters 1, 2 and 8)'),
    ('NTA syllabus for JEE (Main) 2027, Paper 2A and 2B pages', 'Mathematics, Aptitude, Drawing and Planning syllabus'),
    ('NTA Test Practice Centre, nta.ac.in/Quiz', 'Computer-based practice screen (the page lists no Paper 2 items)'),
]
