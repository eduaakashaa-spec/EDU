"""Content for the member page /computer-science-stream: the computer stream (CSE, IT, AI and Data Science, Cyber Security, CS and Business Systems, Mathematics and Computing, hybrids) compared.

What is data: the college lists (app/data/cs_stream_josaa.json, cs_stream_tnea.json, cs_stream_private.json) are built from the JoSAA 2026 and TNEA 2026 files and, for private universities, the
universities' own pages. What is editorial: everything in this file. It describes typical syllabi, typical roles and typical routes, not any one college's official curriculum or placement record,
and it gives no salary or placement-percentage figures because none is verified for a branch label. Syllabi, intakes and recruiter rules change: confirm with each college.
"""

UPDATED = "23 November 2026"

# Levels used in the subject matrix: 0 not taught, 1 light or elective, 2 substantial, 3 core and deep.
BRANCHES = [
    {"key": "core", "family": "core", "name": "Computer Science and Engineering (CSE)", "short": "CSE", "also": "Computer Engineering, Computer Science",
     "tagline": "The base branch. Every other computer branch is a variation of it.",
     "what": "How software, computers and networks are built and why they work: algorithms, systems, databases, networks, software engineering, and electives that reach into AI, security and graphics.",
     "suits": ["You like building things and are happy to be stuck on a problem for hours", "You want the widest choice of roles and of higher-study options", "You are not yet sure which corner of computing you will like"],
     "consider": ["You can get it in a college whose CSE department is strong: it is the safest label with recruiters and with universities abroad", "You want to keep AI, security or systems open and decide through electives in year 3"],
     "caution": "A weak college with CSE on the certificate is worth less than a strong college with a newer label. Check the department, not the name.",
     "roles": ["Software engineer (backend, frontend, mobile)", "Systems and cloud engineer", "Database and data engineer", "Security engineer", "Product engineer", "Research and graduate study"],
     "projects": ["A full web app with login, a database and deployment", "A small database or shell written from scratch", "A compiler or interpreter for a tiny language", "An open-source contribution or a competitive-programming profile"],
     "intern": "Summer after year 2 and year 3. Strongest demand of all branches; open-source programmes, startup internships and campus-drive internships all take CSE.",
     "higher": "M.Tech or MS in CS; MBA; PhD. GATE has a Computer Science paper. Admission committees abroad know the label best.",
     "overlap": 5},
    {"key": "it", "family": "it", "name": "Information Technology (IT)", "short": "IT", "also": "Information Science and Engineering (ISE) at some colleges",
     "tagline": "Almost the same syllabus as CSE, tilted toward applications, data and networks.",
     "what": "Programming, databases, web and mobile, networks, information systems and software projects. Less theory of computation and compilers, more application building.",
     "suits": ["You prefer building applications and business systems over studying machines and compilers", "You want a CSE-like degree and the college offers IT with a strong department"],
     "consider": ["Your target college has IT but a weaker or costlier CSE, and the IT department shares labs and faculty with CSE", "You aim for service, product or consulting roles in software"],
     "caution": "Most of the first four semesters are the same as CSE. Do not pay a premium for the label alone. A few recruiters still list CSE first: read the placement brochure.",
     "roles": ["Software developer", "Web and mobile developer", "Business or systems analyst", "IT consultant", "Quality engineer", "Database administrator"],
     "projects": ["A hospital, library or school management system", "A mobile app with a real backend", "A network monitoring dashboard", "An e-commerce site with payments in test mode"],
     "intern": "Same pool as CSE. Service companies and consulting firms take many IT interns; product companies usually ask for the same data-structures strength as for CSE.",
     "higher": "MS in CS or IT, M.Tech, MBA. Most universities abroad treat IT as a computer-science degree; check the prerequisite list.",
     "overlap": 4},
    {"key": "aids", "family": "aids", "name": "Artificial Intelligence and Data Science (AI and DS), AI and Machine Learning (AI and ML)", "short": "AI and DS",
     "also": "AI, AI and ML, Data Science, Data Science and Engineering, Computational and Data Science, Intelligent Systems",
     "tagline": "CSE's core, then maths, statistics and machine learning earlier and deeper.",
     "what": "Programming and data structures as in CSE, plus linear algebra, probability, statistics, machine learning, deep learning, data engineering and applied projects with real datasets.",
     "suits": ["You are comfortable with maths and enjoy finding patterns in data", "You want ML projects from year 2, not an elective in year 4", "You are happy to study more statistics and less low-level systems"],
     "consider": ["The department has its own faculty with research or industry work in ML, not borrowed from CSE for two courses", "The college runs its own GPU or cloud lab and expects a project each semester", "You still keep the core: the syllabus has operating systems, databases and networks"],
     "caution": "Newer label (most colleges added it from about 2019 to 2021). Some recruiters, universities and exams list CSE and IT but not AI and DS: check eligibility in the placement brochure and the exam notice before you choose.",
     "roles": ["ML or AI engineer", "Data analyst and data scientist", "Data engineer", "Applied scientist (often after a master's)", "Software engineer in AI products", "Research roles"],
     "projects": ["A model trained on a public dataset, with an honest evaluation", "A recommendation or forecasting system with a simple app on top", "A computer-vision or language project with a deployed demo", "A data pipeline that cleans, stores and serves data"],
     "intern": "Data and ML internships exist from year 3 and are competitive. Many students also take plain software internships; a strong data-structures base keeps both doors open.",
     "higher": "MS in CS, Data Science or AI; M.Tech; PhD. GATE has a Data Science and Artificial Intelligence paper (introduced for GATE 2024) as well as Computer Science.",
     "overlap": 3},
    {"key": "cyber", "family": "cyber", "name": "Cyber Security (or CSE with specialisation in Cyber Security)", "short": "Cyber",
     "also": "CSE (Cyber Security), CSE (IoT and Cyber Security including Block Chain Technology)",
     "tagline": "CSE's base, with security, cryptography and digital forensics in the second half.",
     "what": "The CSE core, then cryptography, network and application security, secure software, ethical hacking, digital forensics, risk and compliance.",
     "suits": ["You like taking systems apart and asking how they could be broken", "You like puzzles and capture-the-flag contests", "You are patient with detail and with rules"],
     "consider": ["The college has a security lab, a faculty member who publishes or practises in security, and a CTF or bug-bounty culture", "You will build a strong CSE base first and treat security as depth"],
     "caution": "Entry-level security roles are fewer than general software roles, and employers often prefer a software or networking base first. A full Cyber Security degree is narrower than a CSE degree with a security specialisation.",
     "roles": ["Security analyst (SOC)", "Penetration tester", "Application security engineer", "Cloud security engineer", "Governance, risk and compliance", "Digital forensics"],
     "projects": ["A vulnerable web app you attack and then fix", "A network intrusion detector", "A password manager using real cryptography libraries", "Write-ups of capture-the-flag challenges"],
     "intern": "Fewer slots than for CSE, concentrated in security firms, large IT services and banks. Certificates and contest rankings help more here than in other branches.",
     "higher": "MS in cyber security or CS; M.Tech; PhD in security. Check that your degree meets the prerequisites for general CS programmes.",
     "overlap": 4},
    {"key": "biz", "family": "biz", "name": "Computer Science and Business Systems (CSBS)", "short": "CSBS", "also": "Computer Science and Business, IT-Business Informatics",
     "tagline": "A computing degree with management, economics and finance courses built in.",
     "what": "About half of the course is the CSE core. The rest adds business and management subjects, communication, economics, financial and accounting basics and enterprise systems. Introduced in 2020 with an industry partner in the syllabus design.",
     "suits": ["You see yourself in product, consulting or business-analysis roles, and enjoy both code and case studies", "You may want an MBA or a management role later"],
     "consider": ["You want software skills and business understanding together", "The college gives the same coding depth as its CSE department (same labs, same data-structures course)"],
     "caution": "Less depth in systems and in advanced electives than CSE. Compare the credit table, not the brochure. Pure coding roles at product companies will still test data structures at the same level.",
     "roles": ["Software engineer", "Business or technology analyst", "Consultant", "Product associate", "Enterprise systems (ERP, CRM) consultant", "Fintech roles"],
     "projects": ["A small business app with a real workflow (inventory, billing, bookings)", "A dashboard of company data with a written business recommendation", "A pricing or demand model for a case study", "An enterprise-systems capstone"],
     "intern": "Technology consulting, analytics and product internships fit well; software internships are open if your coding is as strong as a CSE student's.",
     "higher": "MBA (with CAT or GMAT), MS in CS, business analytics or information systems.",
     "overlap": 3},
    {"key": "mnc", "family": "mnc", "name": "Mathematics and Computing (M and C)", "short": "M and C", "also": "Mathematics and Scientific Computing, Computational Mathematics, Statistics and Data Science",
     "tagline": "More mathematics than any other computer branch, with computing as the application.",
     "what": "Real analysis, linear algebra, probability, statistics, optimisation and numerical methods alongside programming, algorithms and databases. Often offered at the IITs and NITs, and by 4-year B.Tech or 5-year dual degree.",
     "suits": ["Mathematics is your strongest subject and you enjoy proofs and modelling", "You may want research, quantitative finance, cryptography or machine-learning theory"],
     "consider": ["You are comfortable with the theory and want options in quant, data science and research", "You can get it at an institute where it sits next to a strong CSE department"],
     "caution": "Fewer software-only courses than CSE; you fill the gap through electives and projects. Some campus recruiters list only CSE and IT in their first rounds; check.",
     "roles": ["Quantitative analyst", "Data scientist", "Software engineer", "Risk and actuarial roles", "Cryptography and optimisation engineer", "Research"],
     "projects": ["An optimisation or scheduling solver for a real problem", "A pricing model for options with a simulation", "A numerical-methods library", "A cryptography implementation"],
     "intern": "Quant, analytics and research internships, plus all software internships if the coding base is strong.",
     "higher": "MS in CS, statistics, operations research or financial engineering; PhD; CAT for management.",
     "overlap": 3},
    {"key": "hybrid", "family": "hybrid", "name": "Computing hybrids: Electronics and Computer Engineering, IoT, Robotics and AI, Computational Engineering", "short": "Hybrids",
     "also": "CSE (IoT), Computer and Communication Engineering, Electrical and Computer Engineering, Robotics and Artificial Intelligence, Computer Science and Design, AR/VR",
     "tagline": "Computing joined to hardware, devices or design.",
     "what": "Programming and algorithms plus electronics, embedded systems, sensors, communication, control or design. The mix depends heavily on the college.",
     "suits": ["You like devices, circuits, robots or games as much as software", "You want embedded, IoT, robotics or XR roles"],
     "consider": ["The college has the matching labs and a strong parent department (electronics, mechanical or design)", "You are clear about the niche"],
     "caution": "Narrower roles and a less recognised label. Software-only recruiters may not shortlist these degrees automatically.",
     "roles": ["Embedded software engineer", "IoT engineer", "Robotics software engineer", "Hardware-software integration", "AR/VR developer", "Product design technologist"],
     "projects": ["A sensor network with a cloud dashboard", "A line-following or pick-and-place robot with computer vision", "A real-time embedded system", "An AR/VR prototype"],
     "intern": "Electronics, automotive, robotics and hardware-startup internships; fewer pure software internships than CSE.",
     "higher": "M.Tech in embedded, VLSI, robotics or CS; MS abroad in electrical and computer engineering or robotics.",
     "overlap": 2},
]

# Subject matrix: typical syllabi (our reading). Order: CSE, IT, AI and DS, Cyber, CSBS, M and C, Hybrids.
SUBJECT_COLS = ["CSE", "IT", "AI and DS", "Cyber", "CSBS", "M and C", "Hybrids"]
SUBJECTS = [
    ("Programming (C, C++, Java, Python)", [3, 3, 3, 3, 3, 3, 3], "common"),
    ("Data structures", [3, 3, 3, 3, 3, 3, 2], "common"),
    ("Discrete mathematics", [3, 3, 3, 3, 2, 3, 2], "common"),
    ("Database systems", [3, 3, 3, 2, 3, 2, 2], "common"),
    ("Operating systems", [3, 3, 2, 3, 2, 2, 2], "common"),
    ("Computer networks", [3, 3, 2, 3, 2, 1, 3], "common"),
    ("Software engineering", [3, 3, 2, 2, 3, 1, 2], "common"),
    ("Algorithms design and analysis", [3, 3, 3, 2, 2, 3, 2], "common"),
    ("Computer organisation and architecture", [3, 2, 2, 2, 1, 1, 3], "common"),
    ("Theory of computation and compilers", [3, 1, 1, 1, 1, 3, 1], "differs"),
    ("Linear algebra, probability and statistics", [2, 2, 3, 2, 2, 3, 2], "differs"),
    ("Machine learning and deep learning", [1, 1, 3, 1, 1, 2, 1], "differs"),
    ("Data engineering and big data", [1, 2, 3, 1, 2, 1, 1], "differs"),
    ("Cryptography, network and application security", [1, 1, 1, 3, 1, 2, 1], "differs"),
    ("Cloud, DevOps and web engineering", [2, 3, 2, 2, 2, 1, 2], "differs"),
    ("Management, economics, finance and enterprise systems", [0, 1, 0, 0, 3, 0, 0], "differs"),
    ("Real analysis, optimisation and numerical methods", [0, 0, 1, 0, 0, 3, 0], "differs"),
    ("Digital electronics, embedded systems and sensors", [1, 0, 0, 0, 0, 0, 3], "differs"),
]

# Where the real difference sits, semester by semester.
JOURNEY = [
    {"when": "Semesters 1 and 2", "title": "Almost identical", "text": "Maths, physics or basic engineering, programming and communication. Many colleges teach all computer branches together in year 1, and some allot the branch only after year 1."},
    {"when": "Semesters 3 and 4", "title": "Mostly the same core", "text": "Data structures, discrete maths, databases, operating systems, computer organisation, algorithms. This is the CSE core, and AI and DS, IT and CSBS keep most of it."},
    {"when": "Semesters 5 and 6", "title": "The labels start to matter", "text": "Electives and project subjects pull the branches apart: machine learning for AI and DS, security for Cyber, management and enterprise systems for CSBS, embedded systems for hybrids."},
    {"when": "Semesters 7 and 8", "title": "Where you actually specialise", "text": "Capstone project, internship, and the final electives. A CSE student who picks AI electives and a project in machine learning ends up close to an AI and DS student, which is the point most families miss."},
]

PLACEMENT_NOTES = [
    ("Skills decide the role more than the label", "Recruiters test data structures, problem solving, projects and communication. A CSE, IT or AI and DS student who passes those tests gets the same software interview."),
    ("Eligibility lists matter", "Some recruiters list the branches they accept. Core CSE and IT are almost always on the list. AI and DS, CSBS and Cyber are usually on recent lists, but not always: ask the placement office for the last three years of eligibility lists and the number of offers by branch."),
    ("The college decides the doors", "Which companies visit, how many offers and which roles depend on the college's tier, its alumni network and its placement cell, far more than on the branch name. Compare placement reports, not brochures."),
    ("Ask for branch-wise data", "Ask for offers by branch, the median offer and the share of students placed in the last three batches, with the number of students who sat. Treat any single headline figure as a highlight, not a typical outcome."),
]

INTERNSHIP_PATH = [
    ("After year 1", "Learn one language well, build a small project, join a club. Few formal internships open yet."),
    ("Summer after year 2", "First internship, usually a startup, a research lab or an open-source programme. Competitive-programming and project portfolios decide the shortlist."),
    ("Summer after year 3", "The internship that matters most. Large companies convert many of these into pre-placement offers; take it seriously and ask for a project with real users."),
    ("Year 4", "Final-year project, placements and applications for master's. A research internship helps for higher studies."),
]

# Why the leading institutes keep to core CSE while private universities offer many variants.
WHY_LEADERS = [
    ("Depth beats labels", "A single large CSE department can offer electives, minors, specialisations and a dual degree. Splitting it into several small departments divides the same faculty and the same labs across thinner programmes."),
    ("Faculty and research drive the offer", "A new branch needs its own faculty, labs and courses. Top institutes tie intake to research and faculty strength, not to demand for a label."),
    ("Specialise later, not at admission", "At the IITs, NITs and IIITs, AI, security or systems come through electives, minors, a master's or a 5-year dual degree. The degree stays CSE, which recruiters and universities abroad recognise immediately."),
    ("Selection is by rank", "JoSAA seats are filled by rank. Every extra label means another cut-off, and a lower-ranked label is read as a weaker one. So the leading institutes add a new programme only when the faculty and research are there, and the tables on this page show which ones have."),
    ("Private universities answer the market", "Families ask for AI, data and cyber, so private universities add them. Regulators allow colleges to add emerging-area branches and seats, and a new label also helps a college attract students. The quality still depends on the department behind it."),
    ("Both models can work", "A new label in a strong college can be an excellent course; the same label in a college without the faculty and labs is a rename of CSE with a few electives. That is why the question to ask is who teaches it and what they have built."),
]

WHEN_TO_CHOOSE = [
    ("You are undecided between several computing fields", "Core CSE. It keeps every door open, and electives let you move later."),
    ("You enjoy statistics and data more than systems", "AI and DS, if the department is real: ask about faculty, labs and the first-year syllabus. Otherwise CSE with AI electives."),
    ("You like breaking and defending systems", "CSE first; Cyber Security if the college has a proper security lab and the CSE base is also in the syllabus."),
    ("You are drawn to products, consulting or an MBA later", "CSBS, or CSE with a management minor, if the coding depth is the same as CSE."),
    ("Mathematics is your real strength", "Mathematics and Computing at an institute that also has a strong CSE department."),
    ("You like devices, robots or games", "A hybrid (Electronics and Computer, IoT, Robotics and AI) only if the college has the labs and a strong parent department."),
    ("You cannot get core CSE at your target college", "Compare the college and the department first. A strong institute with AI and DS or IT usually beats a weak institute with CSE."),
]

HIGHER_STUDIES = [
    ("MS abroad (USA, Canada, Germany, UK, Singapore)", "Admission looks at your marks, projects, research or internship experience and, for many programmes, GRE and English scores. Most universities accept any computer-stream degree; check the prerequisite course list. CSE gives the clearest match."),
    ("M.Tech in India (IITs, NITs, IIITs)", "Through GATE. GATE has a Computer Science paper and, from 2024, a Data Science and Artificial Intelligence paper. Check each institute's list of eligible bachelor's degrees."),
    ("MBA", "Through CAT, GMAT or XAT. Every computer branch qualifies; CSBS students may find the management courses already familiar."),
    ("PhD and research", "Mathematics, algorithms and theory matter most. CSE, Mathematics and Computing and AI and DS all lead here; research internships in year 3 matter more than the label."),
    ("Specialised master's (quant finance, robotics, cyber security, bioinformatics)", "Your branch shows commitment to the field, but the prerequisites decide admission. Plan the electives you need."),
]

# What AI changes, in plain terms. Qualitative: no job-count or salary claims.
AI_TASKS = [
    {"label": "Being automated or compressed", "tone": "bad",
     "items": ["Boilerplate code, simple scripts, routine tests and documentation", "Basic data cleaning and standard reports", "First-line support and simple query answering", "Translating a clear specification into routine code"]},
    {"label": "Being changed: AI is your assistant", "tone": "mid",
     "items": ["Everyday software development: faster with AI tools, but the engineer owns the design, the review and the bugs", "Data analysis: AI drafts, a person checks and decides", "Testing and quality engineering", "Security operations: AI triages alerts, analysts investigate"]},
    {"label": "Growing", "tone": "good",
     "items": ["System design and architecture, reliability and performance", "Building, evaluating and running AI systems in products", "Data engineering and data quality", "Security for AI systems and AI-assisted attacks", "Domain experts who can use computing: health, finance, climate, manufacturing"]},
]

FUTURE_JOBS = [
    {"role": "AI and ML engineer", "what": "Builds, trains, evaluates and deploys models inside products.", "best": ["AI and DS", "CSE", "M and C"], "skills": "Python, maths, ML frameworks, evaluation, deployment"},
    {"role": "Data engineer", "what": "Builds the pipelines and platforms that keep data clean, fast and trustworthy.", "best": ["CSE", "IT", "AI and DS"], "skills": "SQL, distributed systems, cloud, orchestration"},
    {"role": "MLOps and AI platform engineer", "what": "Runs models in production: monitoring, cost, safety, updates.", "best": ["CSE", "IT", "AI and DS"], "skills": "Cloud, containers, observability, ML basics"},
    {"role": "Cloud, DevOps and reliability engineer", "what": "Keeps large systems secure, available and affordable.", "best": ["CSE", "IT", "Cyber"], "skills": "Linux, networking, cloud, automation"},
    {"role": "Security engineer and AI security specialist", "what": "Protects systems and AI models, and defends against AI-assisted attacks.", "best": ["Cyber", "CSE", "M and C"], "skills": "Systems, networks, cryptography, threat modelling"},
    {"role": "Applied scientist and researcher", "what": "Creates new methods; usually needs a master's or a PhD.", "best": ["M and C", "AI and DS", "CSE"], "skills": "Mathematics, algorithms, research writing"},
    {"role": "Product engineer and AI product manager", "what": "Decides what to build with AI and why, and works with engineers and customers.", "best": ["CSBS", "CSE", "IT"], "skills": "Software basics, user research, communication, metrics"},
    {"role": "Embedded, IoT and robotics software engineer", "what": "Puts intelligence into devices, vehicles and machines.", "best": ["Hybrids", "CSE"], "skills": "C and C++, embedded systems, sensors, control"},
    {"role": "AI governance, risk and compliance", "what": "Makes AI use safe, legal and auditable inside organisations.", "best": ["Cyber", "CSBS", "CSE"], "skills": "Risk, law and policy basics, security, communication"},
    {"role": "Computing in other fields", "what": "Computational biology, health technology, climate and finance modelling.", "best": ["M and C", "AI and DS", "CSE"], "skills": "Domain knowledge plus statistics and programming"},
]

SKILLS = {
    "universal": [("Problem solving and data structures", "The one skill every interview checks, in every branch."), ("Programming in at least two languages", "For example Python plus Java, C++ or JavaScript."),
                  ("Mathematics for computing", "Discrete maths, probability, linear algebra. It grows in value as AI grows."), ("Systems thinking", "How operating systems, databases, networks and the cloud fit together."),
                  ("Using AI tools well", "Prompting, reviewing, testing and correcting AI output. The engineer, not the tool, is accountable."), ("Communication and teamwork", "Clear writing, code review, presenting a project, working with non-engineers."),
                  ("Learning how to learn", "The tools will change several times in a career; the habit of building small projects keeps you current.")],
    "by_branch": [("CSE", "Algorithms, systems, one specialisation (AI, security or systems), a deployed project."), ("IT", "Web and mobile engineering, databases, cloud, testing, business analysis."),
                  ("AI and DS", "Statistics, machine learning, data pipelines, model evaluation, one end-to-end deployed project."), ("Cyber", "Networks, operating systems, cryptography, scripting, contests and a responsible-disclosure habit."),
                  ("CSBS", "Coding at CSE depth, plus finance, economics, product thinking and presentation."), ("M and C", "Proofs, optimisation, numerical methods, probability, plus real coding projects."),
                  ("Hybrids", "C and C++, electronics, embedded systems, a built prototype.")],
    "years": [("Year 1", "Basics of programming and maths. One small project. Join a club."), ("Year 2", "Data structures and algorithms. Databases and operating systems. A first internship or open-source contribution."),
              ("Year 3", "Your specialisation through electives, a serious project, a competitive internship."), ("Year 4", "Capstone, placements or applications for a master's, and a portfolio of two or three finished projects.")],
}

# Questions to put to any college (ask for answers in writing).
ASK_COLLEGES = [
    "How many full-time faculty teach this branch, and how many hold a PhD or have worked in this area?",
    "Is the first-year and second-year syllabus the same as CSE? Which subjects are different, and when does the difference begin?",
    "Show the credit table for all eight semesters and the electives offered in the last two years.",
    "Which labs does this branch have (GPU or cloud, security, IoT) and who maintains them?",
    "Placement and internship data by branch for the last three batches: students who sat, students placed, offers, and the recruiters that visited.",
    "Do the recruiters' eligibility lists include this branch? Show last year's lists.",
    "Is the programme accredited by NBA and approved by AICTE, and is the intake approved for this year?",
    "Can students change branch or take a minor or specialisation in AI, security or business?",
]

FAQ = [
    ("Is CSE always better than AI and DS or IT?", "No. CSE is the broadest and the safest label, but the college, the department and what you build matter more. A strong college with IT or AI and DS can serve you better than a weak college with CSE."),
    ("Will AI make a computer degree useless?", "No. AI tools change how software is written and raise the bar for entry-level work. People who understand systems, data and problem solving, and who use AI tools well, are still needed. The skills that age worst are routine coding with no depth."),
    ("Which branch pays the most?", "No branch label sets the salary. The college, your skills, the role and the employer do. Be careful with any single number that is quoted for a branch."),
    ("Can an AI and DS student apply to software roles?", "Yes, if your data-structures and programming skills match a CSE student's, and the recruiter's eligibility list includes your branch. Check the list."),
    ("Can a CSE student work in AI?", "Yes. Take AI and mathematics electives, build projects, and consider a master's or a specialisation. Many AI engineers hold a CSE degree."),
    ("Should I choose a hybrid branch?", "Only if you are clear about devices, robots or games and the college has the labs. Otherwise keep the broader label."),
    ("What if I miss a computer branch in counselling?", "Think about the college first, then the branch. Consider electronics and communication or electrical engineering with computing electives in a strong college, and plan a master's in computing."),
]

SOURCES = [
    "JoSAA 2026 opening and closing ranks, Rounds 1 to 5 (the portal's JoSAA file): branches offered at IITs, NITs, IIITs and other JoSAA institutes, and Open category closing ranks.",
    "NIRF Engineering list held on the portal (app/data/eng_colleges.json): ranks and bands.",
    "TNEA 2026 allotment lists (DOTE Chennai, held on the portal): branches offered in Tamil Nadu counselling colleges.",
    "Private university branch lists: each university's own website, read on the date shown on the page.",
    "Editorial content (differences, subjects, roles, AI impact): EduAakashaA reading of typical syllabi and industry practice. Not a college's official curriculum.",
]
