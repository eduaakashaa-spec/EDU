
// ════════════════════════════════════════
//  CONFIG
// ════════════════════════════════════════
const APPS_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbzBM-WYfXNFgwiGMe1-lVXbLMy61dZSi9ESVvEFzkfNRII-cGFmjmeOlUD2fpfSvR6z/exec";
 
// ════════════════════════════════════════
//  DATA
// ════════════════════════════════════════
const psychometricQs=[
  {id:"psy1",q:"When faced with a complex challenge, my natural response is to:",opts:["Break it into smaller parts and analyze logically","Think about who is affected and consider feelings","Look for innovative or unconventional approaches","Evaluate costs, benefits and practical outcomes"],w:[[3,0,0],[0,0,3],[1,1,2],[0,3,0]]},
  {id:"psy2",q:"In a group discussion, I naturally tend to:",opts:["Present data-backed arguments","Mediate between different viewpoints","Propose creative new angles","Focus on actionable decisions and timelines"],w:[[3,0,0],[0,0,3],[1,0,2],[0,3,0]]},
  {id:"psy3",q:"I feel most fulfilled when I:",opts:["Solve a puzzle or figure out how something works","Help someone overcome a personal challenge","Create something beautiful or meaningful","Successfully negotiate or close a deal"],w:[[3,0,0],[0,0,3],[0,0,3],[0,3,0]]},
  {id:"psy4",q:"My ideal weekend involves:",opts:["Visiting a science museum or tinkering with gadgets","Volunteering, attending a talk, or visiting a library","Making art, playing music, or watching a documentary","Planning a small business idea or managing finances"],w:[[3,0,0],[0,0,3],[0,0,3],[0,3,0]]},
  {id:"psy5",q:"When I read news, I'm drawn to stories about:",opts:["Scientific discoveries and technology breakthroughs","Social issues, politics, and human-interest stories","Culture, philosophy, arts, and travel","Markets, startups, and business innovations"],w:[[3,0,0],[0,0,3],[0,0,3],[0,3,0]]},
  {id:"psy6",q:"Under pressure, I:",opts:["Stay calm and think systematically","Seek advice and talk through the problem","Channel stress into creative outlets","Make quick pragmatic decisions to move forward"],w:[[3,0,0],[0,1,2],[0,0,3],[0,3,0]]},
  {id:"psy7",q:"I'd describe my thinking style as:",opts:["Logical and evidence-based","Empathetic and people-oriented","Imaginative and abstract","Strategic and results-driven"],w:[[3,0,0],[0,0,3],[1,0,2],[0,3,0]]},
  {id:"psy8",q:"My ideal workspace has:",opts:["Lab equipment, whiteboards, and computers","Books, discussion spaces, and quiet corners","Open creative areas with art and inspiration boards","Meeting rooms, charts, and professional tools"],w:[[3,0,0],[0,0,3],[0,0,3],[0,3,0]]},
  {id:"psy9",q:"When making decisions, I rely most on:",opts:["Facts, data, and logical reasoning","Intuition, values, and how others feel","Imagination and exploring possibilities","Practical experience and past outcomes"],w:[[3,0,0],[0,0,3],[0,0,3],[0,3,0]]},
  {id:"psy10",q:"If I could master any skill instantly:",opts:["Advanced programming or a scientific discipline","Public speaking, writing, or counseling","Painting, filmmaking, or musical composition","Investing, business management, or negotiation"],w:[[3,0,0],[0,0,3],[0,0,3],[0,3,0]]},
  {id:"psy11",q:"The school subject that holds my attention longest:",opts:["Math or Science — I love problem sets","Languages or Social Studies — stories fascinate me","Art, Music, or Literature — I lose myself in creation","Economics or Business — real-world relevance excites me"],w:[[3,0,0],[0,0,3],[0,0,3],[0,3,0]]},
  {id:"psy12",q:"When I disagree with someone, I:",opts:["Present evidence to prove my point","Try to understand their perspective first","Reframe the issue from a different angle","Focus on finding a workable compromise"],w:[[3,0,0],[0,0,3],[0,0,3],[0,3,0]]},
  {id:"psy13",q:"I'm most proud when I:",opts:["Ace a tough exam through deep understanding","Make a difference in someone's life","Express an idea that moves people","Earn money or build something from scratch"],w:[[3,0,0],[0,0,3],[0,0,3],[0,3,0]]},
  {id:"psy14",q:"My friends come to me for:",opts:["Help with homework or explaining concepts","Emotional support and life advice","Creative ideas for projects and events","Practical tips on money, planning, or organizing"],w:[[3,0,0],[0,0,3],[0,0,3],[0,3,0]]},
  {id:"psy15",q:"I daydream about:",opts:["Inventing something or making a discovery","Understanding human behavior or changing society","Creating a masterpiece — film, book, or art","Building a company or becoming financially independent"],w:[[3,0,0],[0,0,3],[0,0,3],[0,3,0]]}
];
 
const aptitudeQs=[
  {id:"apt1",q:"If 5x - 3 = 2x + 12, then x = ?",opts:["3","5","7","15"],correct:1},
  {id:"apt2",q:"Next: 3, 9, 27, 81, ?",opts:["162","243","216","189"],correct:1},
  {id:"apt3",q:"A car travels 180 km in 2.5 hrs. Speed in m/s?",opts:["20","25","72","50"],correct:0},
  {id:"apt4",q:"Odd one out: Photosynthesis, Respiration, Osmosis, Democracy",opts:["Photosynthesis","Respiration","Osmosis","Democracy"],correct:3},
  {id:"apt5",q:"Complete: 2, 3, 5, 8, 13, ?",opts:["18","20","21","19"],correct:2},
  {id:"apt6",q:"Doctor : Hospital :: Teacher : ?",opts:["School","Student","Books","Education"],correct:0},
  {id:"apt7",q:"15% of 360 = ?",opts:["45","54","48","52"],correct:1},
  {id:"apt8",q:"All roses are flowers; some flowers fade quickly. True?",opts:["All roses fade quickly","Some roses may fade quickly","No roses fade","Roses are not flowers"],correct:1},
  {id:"apt9",q:"Rectangle 12×8 cm. Diagonal ≈ ?",opts:["14.4 cm","10 cm","20 cm","16 cm"],correct:0},
  {id:"apt10",q:"Chemical symbol 'Au' = ?",opts:["Silver","Aluminum","Gold","Argon"],correct:2},
  {id:"apt11",q:"Rearrange 'CIFAIPC' to get a:",opts:["Country","Ocean","Science term","Animal"],correct:0},
  {id:"apt12",q:"Buy ₹400, sell ₹500. Profit %?",opts:["20%","25%","15%","10%"],correct:1},
  {id:"apt13",q:"Planet closest to the Sun?",opts:["Venus","Mars","Mercury","Earth"],correct:2},
  {id:"apt14",q:"Face North, turn 90° left twice. You face:",opts:["South","East","West","North"],correct:0},
  {id:"apt15",q:"Binary 1010 = decimal?",opts:["8","10","12","14"],correct:1}
];
 
const applicationQs=[
  {id:"app1",q:"Week-long school project — you choose:",opts:["Build a working water purifier model","Create a business plan for a student café","Make a documentary about local heritage","Organize a mental health awareness campaign"]},
  {id:"app2",q:"Career fair — first booth you visit:",opts:["ISRO / IIT Research Labs","Startup Incubator / Stock Exchange","Publishing House / Film Studio","NGO / United Nations booth"]},
  {id:"app3",q:"₹500 extra — you:",opts:["Buy a science kit or electronics part","Deposit and track interest earned","Buy a book, art supply, or movie ticket","Donate it to a cause you care about"]},
  {id:"app4",q:"Help a friend's YouTube channel — you'd:",opts:["Set up analytics and optimize algorithm","Create monetization & sponsorship strategy","Write scripts, edit videos, design thumbnails","Create content about social causes"]},
  {id:"app5",q:"Innovation day — you'd:",opts:["Present an AI attendance system","Pitch a school merchandise business","Stage a play about a historical event","Lead a debate on education reform"]},
  {id:"app6",q:"Neighborhood problem — you:",opts:["Analyze data, propose technical solution","Calculate costs, propose budget-friendly fix","Write an article or create awareness posters","Organize a community meeting"]},
  {id:"app7",q:"Ideal summer internship at:",opts:["Tech company or research institute","Bank, consulting firm, or startup","Media house, museum, or art gallery","Law firm, think tank, or NGO"]},
  {id:"app8",q:"In a strategy board game, you:",opts:["Calculate probabilities, optimize moves","Negotiate alliances, manage resources","Focus on creative unexpected strategies","Observe psychology, adapt accordingly"]},
  {id:"app9",q:"Tutoring younger students — you'd teach:",opts:["Math or Science — concepts excite me","Business basics or financial literacy","Creative writing, art, or public speaking","History, civics, or social awareness"]},
  {id:"app10",q:"One world problem to solve:",opts:["Climate change through technology","Poverty through economic innovation","Cultural misunderstanding through education","Mental health through better support"]},
  {id:"app11",q:"Blank notebook — you fill it with:",opts:["Diagrams, formulas, experiment notes","Business ideas, budgets, market research","Stories, poems, sketches, travel journals","Quotes, reflections, social observations"]},
  {id:"app12",q:"New app idea — first thought:",opts:["Technology stack and how to build it","Business model and revenue potential","User experience and visual design","Social impact and accessibility"]},
  {id:"app13",q:"Dream TED Talk topic:",opts:["'How quantum computing changes everything'","'Zero to startup: lessons from failure'","'Power of storytelling in the digital age'","'Why empathy is the most underrated skill'"]},
  {id:"app14",q:"During a disaster, your instinct:",opts:["Analyze situation, devise rescue plan","Coordinate logistics, supplies, communication","Document and report to raise awareness","Provide emotional support to affected people"]},
  {id:"app15",q:"National competition — you'd choose:",opts:["Science/Math Olympiad","Stock market simulation / business quiz","Creative writing, debate, or Model UN","Essay competition on social issues"]}
];
 
const subjectGroups={Science:["Mathematics","Physics","Chemistry","Biology","Computer Science"],Commerce:["Accountancy","Business Studies","Economics","Statistics","Information Practices"],Humanities:["History","Political Science","Geography","Psychology","Sociology"]};
const confLevels=["Very Low","Low","Moderate","High","Very High"];
 
const topCareers={
  Science:[
    {title:"Software / AI Engineer",desc:"Build intelligent apps & AI systems",courses:["B.Tech CS/IT","B.Tech AI/ML","BCA+MCA"],jobs:["Software Dev","ML Engineer","Full-Stack Dev","DevOps"],ai:"Medium",aiNote:"AI assists but demand stays high",sal:"₹8-30L"},
    {title:"Doctor / Physician",desc:"Diagnose, treat, specialize",courses:["MBBS","MBBS+MD/MS","BDS"],jobs:["Physician","Surgeon","Specialist","Radiologist"],ai:"Low",aiNote:"Human expertise irreplaceable",sal:"₹10-40L"},
    {title:"Data Scientist",desc:"Extract insights via statistics & ML",courses:["B.Tech+MS Data Sci","BSc Stats+PG","Certs"],jobs:["Data Analyst","Data Scientist","BI Analyst","ML Researcher"],ai:"Medium",aiNote:"Strategic thinking needed",sal:"₹8-25L"},
    {title:"Aerospace Engineer",desc:"Aircraft, spacecraft & defense",courses:["B.Tech Aero","B.Tech Mech","IIST"],jobs:["Design Eng","ISRO Scientist","Avionics","Flight Test"],ai:"Low",aiNote:"Complex systems need humans",sal:"₹7-20L"},
    {title:"Pharmacist",desc:"Drug research & pharma ops",courses:["B.Pharm","M.Pharm","Pharm.D"],jobs:["Clinical Pharmacist","Drug Safety","R&D","Regulatory"],ai:"Medium",aiNote:"AI accelerates discovery",sal:"₹4-15L"},
    {title:"Architect",desc:"Design buildings & spaces",courses:["B.Arch","B.Plan","M.Arch"],jobs:["Architect","Urban Planner","Interior","Landscape"],ai:"Medium",aiNote:"Creative vision essential",sal:"₹5-18L"},
    {title:"Biotechnologist",desc:"Biology+tech for health & agri",courses:["B.Tech Biotech","BSc+MSc","Integrated MSc"],jobs:["Research Scientist","Analyst","Genetic Counselor","QC"],ai:"Low",aiNote:"Lab work needs judgment",sal:"₹5-15L"},
    {title:"Environmental Scientist",desc:"Solve environmental challenges",courses:["BSc Env Sci","B.Tech Env Eng","MSc Ecology"],jobs:["Consultant","Climate Analyst","Conservation","ESG"],ai:"Low",aiNote:"Fieldwork is human-intensive",sal:"₹4-12L"},
    {title:"Robotics Engineer",desc:"Design robots & automation",courses:["B.Tech Robotics","Mechatronics","EEE"],jobs:["Robotics Eng","Automation","IoT Dev","Controls"],ai:"Low",aiNote:"Building AI robots IS future",sal:"₹6-22L"},
    {title:"Research Scientist",desc:"Push boundaries through research",courses:["BSc+MSc+PhD","Integrated PhD","B.Tech+MS"],jobs:["Fellow","Lab Director","Professor","R&D Head"],ai:"Low",aiNote:"Hypothesis building is human",sal:"₹6-25L"}
  ],
  Commerce:[
    {title:"Chartered Accountant",desc:"Audit, tax & financial consulting",courses:["CA Foundation→Final","BCom+CA","BCom Hons+CA"],jobs:["Audit Manager","Tax Consultant","CFO","Controller"],ai:"Medium",aiNote:"Advisory value grows",sal:"₹8-30L"},
    {title:"Investment Banker",desc:"Large-scale financial deals & M&A",courses:["BCom/BBA+MBA Fin","CFA","BCom+MS Fin"],jobs:["Analyst","M&A Associate","Portfolio Mgr","Equity Research"],ai:"Medium",aiNote:"Deal-making needs relationships",sal:"₹12-50L"},
    {title:"Digital Marketing Mgr",desc:"Drive growth through online channels",courses:["BBA+DM Cert","BCom+MBA Mktg","Google/Meta Certs"],jobs:["SEO Specialist","Social Media Mgr","Growth Hacker","Content Lead"],ai:"High",aiNote:"Strategy differentiates from AI",sal:"₹5-20L"},
    {title:"Entrepreneur",desc:"Build & scale own ventures",courses:["BBA Entrepreneurship","MBA","BCom+Incubators"],jobs:["Founder/CEO","Product Mgr","Biz Dev","Consultant"],ai:"Low",aiNote:"Vision & risk-taking are human",sal:"Variable"},
    {title:"Company Secretary",desc:"Corporate governance & compliance",courses:["CS Foundation→Prof","BCom+CS","LLB+CS"],jobs:["Company Secretary","Compliance","Gov Head","Legal"],ai:"Medium",aiNote:"Judgment still human",sal:"₹6-20L"},
    {title:"Actuary",desc:"Assess financial risk via math",courses:["BSc Actuarial","BCom+IFOA/IAI","BSc Maths"],jobs:["Actuarial Analyst","Risk Mgr","Underwriter","Pension"],ai:"Medium",aiNote:"Complex modeling evolving",sal:"₹8-35L"},
    {title:"Financial Planner",desc:"Manage personal & corporate wealth",courses:["CFP Cert","BCom+MBA","NISM Certs"],jobs:["Wealth Mgr","Advisor","MF Analyst","Retirement"],ai:"Medium",aiNote:"Trust-based advice is human",sal:"₹5-18L"},
    {title:"Supply Chain Mgr",desc:"Optimize logistics & operations",courses:["BBA+MBA Ops","BCom+PGDM SCM","APICS"],jobs:["SC Analyst","Logistics Mgr","Procurement","Ops Director"],ai:"High",aiNote:"AI optimizing rapidly",sal:"₹6-22L"},
    {title:"HR Manager",desc:"Talent, culture & development",courses:["BBA+MBA HR","BA Psych+PGDM","SHRM"],jobs:["HR Partner","Talent Lead","L&D Mgr","CHRO"],ai:"Medium",aiNote:"Culture & empathy need humans",sal:"₹5-20L"},
    {title:"E-Commerce Manager",desc:"Build & manage online platforms",courses:["BBA+Ecom Spec","BCom+MBA","Seller Certs"],jobs:["E-Com Mgr","Marketplace Analyst","D2C Brand","CRO"],ai:"Medium",aiNote:"Strategy remains human-led",sal:"₹5-18L"}
  ],
  Humanities:[
    {title:"Civil Services (IAS/IPS)",desc:"Governance & administration",courses:["Any Grad+UPSC","BA Pol Sci","BA Sociology"],jobs:["IAS","IPS","IFS","IRS"],ai:"Low",aiNote:"Policy-making is human",sal:"₹8-25L+"},
    {title:"Lawyer",desc:"Practice law & advocate justice",courses:["BA LLB (5yr)","LLB (3yr)","LLM"],jobs:["Corporate Lawyer","Litigation","Legal Counsel","Judge"],ai:"Medium",aiNote:"Courtroom advocacy is human",sal:"₹5-30L"},
    {title:"Journalist",desc:"Investigate, report & present news",courses:["BA Journalism","BJMC","PG Diploma"],jobs:["Reporter","Editor","Anchor","Investigative"],ai:"High",aiNote:"Deep investigation stays human",sal:"₹4-15L"},
    {title:"Psychologist",desc:"Mental health & behavioral support",courses:["BA/BSc Psych","MA Psych","M.Phil Clinical"],jobs:["Clinical","Counselor","Org Psych","Therapist"],ai:"Low",aiNote:"Empathy irreplaceable",sal:"₹4-18L"},
    {title:"UX/UI Designer",desc:"User-friendly digital experiences",courses:["BDes CommDes","BA Fine Arts+UX","NID/NIFT"],jobs:["UX Designer","UI Designer","Product Design","UX Research"],ai:"Medium",aiNote:"User empathy needs humans",sal:"₹6-25L"},
    {title:"Filmmaker",desc:"Films, videos & digital content",courses:["BA Film","FTII","Mass Comm"],jobs:["Director","Cinematographer","Editor","Creator"],ai:"Medium",aiNote:"Storytelling is human art",sal:"₹3-25L"},
    {title:"Social Worker",desc:"Drive social change",courses:["BSW","MSW","BA Soc+PG"],jobs:["Program Mgr","Community Dev","Policy Research","CSR"],ai:"Low",aiNote:"Grassroots is human",sal:"₹3-12L"},
    {title:"Professor",desc:"Teach, research & mentor",courses:["MA/MSc+NET","PhD","B.Ed"],jobs:["Professor","Teacher","Ed Consultant","Curriculum"],ai:"Medium",aiNote:"Mentoring stays human",sal:"₹5-18L"},
    {title:"Foreign Language Expert",desc:"Bridge cultures via language",courses:["BA Foreign Lang","Diploma JNU","MA Linguistics"],jobs:["Translator","Interpreter","Localization","Embassy"],ai:"High",aiNote:"Cultural nuance needed",sal:"₹4-15L"},
    {title:"Public Policy Analyst",desc:"Research & advise on policy",courses:["BA PolSci+MPP","BA Econ+PG","NLSIU/TISS"],jobs:["Policy Analyst","Think Tank","Gov Advisor","Legislative"],ai:"Low",aiNote:"Judgment & stakeholders human",sal:"₹5-20L"}
  ]
};
 
const streamSubjects={
  Science:{"State Board":["Physics","Chemistry","Maths/Bio","CS","English","Language"],CBSE:["Physics","Chemistry","Maths/Bio","CS/IP","English Core","PE"],ICSE:["Physics","Chemistry","Maths/Bio","CS","English","Env Sci"]},
  Commerce:{"State Board":["Accountancy","Biz Studies","Economics","Maths/Stats","English","Language"],CBSE:["Accountancy","Biz Studies","Economics","Maths/IP","English Core","PE"],ICSE:["Accountancy","Biz Studies","Economics","Maths","English","Commerce"]},
  Humanities:{"State Board":["History","Pol Sci","Geo/Psych","Soc/Econ","English","Language"],CBSE:["History","Pol Sci","Geo/Psych","Soc/Econ","English Core","PE"],ICSE:["History","Pol Sci","Geo/Psych","Sociology","English","Env Sci"]}
};
const streamSkills={Science:["Analytical Thinking","Mathematical Reasoning","Scientific Temperament","Problem Solving","Lab Skills","Logical Reasoning","Technical Aptitude"],Commerce:["Numerical Ability","Business Acumen","Financial Literacy","Communication","Analytical Skills","Decision Making","Strategic Thinking"],Humanities:["Critical Thinking","Communication","Empathy","Research Skills","Writing","Public Speaking","Cultural Awareness"]};
 
// ════════════════════════════════════════
//  STATE
// ════════════════════════════════════════
let currentStep = 0;
let studentPref = "";
let psyAns = {}, aptAns = {}, appAns = {};
let confData = { Science:{}, Commerce:{}, Humanities:{} };
let parentPref = "";
let results = null, skillGap = null;
let reportLang = "en"; // "en" or "ta"
 
function setLang(lang) {
  reportLang = lang;
  document.getElementById('langEn').classList.toggle('selected', lang==='en');
  document.getElementById('langTa').classList.toggle('selected', lang==='ta');
}
 
const waLinks = {
  Science: {name:"Eduaakashaa | Science Pathway (10–12)", url:"https://whatsapp.com/channel/0029Vb7qPWaJP21BPNOFTV2D"},
  Commerce: {name:"Eduaakashaa | Commerce Pathway (10–12)", url:"https://whatsapp.com/channel/0029VbCYiWV2v1Itz7YE8H2Q"},
  Humanities: {name:"Eduaakashaa | Arts & Humanities Pathway (10–12)", url:"https://whatsapp.com/channel/0029VbCWuRPDp2Q7jIMiEr2w"},
  Emerging: {name:"Eduaakashaa | Future & Emerging Pathways", url:"https://whatsapp.com/channel/0029Vb8Gshf6GcGJkjJBEj3F"}
};
 
// Tamil translation labels
const T = {
  reportTitle: "தொழில் வழி மதிப்பீட்டு அறிக்கை",
  studentDetails: "மாணவர் விவரங்கள்",
  name: "பெயர்", age: "வயது", school: "பள்ளி", city: "நகரம்", board: "வாரியம்", class_: "வகுப்பு",
  studentPref: "மாணவர் விருப்பம்", parentPref: "பெற்றோர் விருப்பம்",
  recommended: "பரிந்துரைக்கப்பட்ட பாதை",
  basedOn: "60+ கேள்விகள் அடிப்படையிலான மனநிலை, திறன் மற்றும் பயன்பாட்டு பகுப்பாய்வு",
  riskFlags: "அபாய குறிகள் & முடிவு மேட்ரிக்ஸ்",
  scores: "மதிப்பெண் விவரம்",
  stream: "பாதை", score: "மதிப்பெண்", status: "நிலை", aptitude: "திறன்",
  profileStrength: "சுயவிவர வலிமை பகுப்பாய்வு",
  dimension: "பரிமாணம்",
  prefGap: "விருப்பம் எதிர் மதிப்பீடு இடைவெளி",
  gapDetected: "⚠️ இடைவெளி கண்டறியப்பட்டது",
  aligned: "✅ ஒத்துப்போகிறது!",
  whyRec: "ஏன் இந்த பரிந்துரை?",
  dearStudent: "அன்புள்ள",
  topCareers: "முதல் 10 தொழில்கள்",
  career: "தொழில்", courses: "படிப்புகள்", jobs: "வேலை வாய்ப்புகள்", aiImpact: "AI தாக்கம்", salary: "சம்பளம்",
  skillGap: "திறன் இடைவெளி & செயல் திட்டம்",
  skill: "திறன்", current: "தற்போது", required: "தேவை", gap: "இடைவெளி", action: "செயல்",
  actionPlan: "பரிந்துரைக்கப்பட்ட செயல் திட்டம்",
  subjects: "பாடங்கள்",
  parentNote: "பெற்றோருக்கு குறிப்பு",
  dearParent: "அன்புள்ள",
  breakBarrier: "🔥 தடைகளை உடைத்தல் — வசதி மண்டலத்திலிருந்து வெளியேறுவது",
  breakIntro: "உங்கள் விருப்பமான பாதைக்கும் மதிப்பீட்டு முடிவுக்கும் இடையே இடைவெளி உள்ளது. இது சரி — வளர்ச்சி அசௌகரியத்தில் நிகழ்கிறது.",
  whatsapp: "எங்களுடன் இணையுங்கள்",
  counselling: "தனிப்பயனாக்கப்பட்ட ஆலோசனைக்கு",
  rec: "✅ பரிந்துரை",
};
 
// ════════════════════════════════════════
//  NAV
// ════════════════════════════════════════
function goStep(n) {
  document.querySelectorAll('.step').forEach(s => s.classList.remove('active'));
  document.getElementById('step'+n).classList.add('active');
  currentStep = n;
  const pw = document.getElementById('progressWrap');
  if (n > 0 && n < 8) {
    pw.style.display = 'block';
    document.getElementById('progLabel').textContent = `Step ${n}/8`;
    const pct = Math.round(n/8*100);
    document.getElementById('progPct').textContent = pct+'%';
    document.getElementById('progFill').style.width = pct+'%';
  } else { pw.style.display = 'none'; }
  window.scrollTo(0,0);
}
 
function validateInfo() {
  if (!document.getElementById('stuName').value || !document.getElementById('stuSchool').value) {
    alert('Please fill in Name and School'); return;
  }
  goStep(2);
}
 
// ════════════════════════════════════════
//  RENDER QUESTIONS
// ════════════════════════════════════════
function renderQuestions(container, qs, ansObj, countEl, nextBtn) {
  const el = document.getElementById(container);
  el.innerHTML = '';
  qs.forEach((q, idx) => {
    const card = document.createElement('div');
    card.className = 'qcard';
    card.innerHTML = `<div class="qcard-header"><span class="qcard-num">Q${idx+1}</span><span class="qcard-text">${q.q}</span></div><div class="qcard-opts" id="opts_${q.id}"></div>`;
    el.appendChild(card);
    const optsDiv = card.querySelector('.qcard-opts');
    q.opts.forEach((o, i) => {
      const btn = document.createElement('button');
      btn.className = 'qcard-opt' + (ansObj[q.id]===i?' selected':'');
      btn.textContent = o;
      btn.onclick = () => {
        ansObj[q.id] = i;
        optsDiv.querySelectorAll('.qcard-opt').forEach(b=>b.classList.remove('selected'));
        btn.classList.add('selected');
        updateCount(qs, ansObj, countEl, nextBtn);
      };
      optsDiv.appendChild(btn);
    });
  });
  updateCount(qs, ansObj, countEl, nextBtn);
}
 
function updateCount(qs, ans, countEl, nextBtn) {
  const c = qs.filter(q=>ans[q.id]!==undefined).length;
  document.getElementById(countEl).textContent = `${c}/${qs.length} answered`;
  document.getElementById(nextBtn).disabled = c < qs.length;
}
 
// ════════════════════════════════════════
//  RENDER PREFERENCE CARDS
// ════════════════════════════════════════
function renderPrefCards() {
  const prefs = [
    {v:"Science",emoji:"🔬",desc:"Physics, Chemistry, Maths/Bio, Engineering, Medicine, Technology"},
    {v:"Commerce",emoji:"💼",desc:"Accountancy, Business, Economics, Finance, Entrepreneurship"},
    {v:"Humanities",emoji:"📚",desc:"History, Political Science, Psychology, Law, Arts, Media"},
    {v:"Not Sure",emoji:"🤔",desc:"I want the assessment to help me decide — open to any stream"}
  ];
  const el = document.getElementById('prefCards');
  el.innerHTML = '';
  prefs.forEach(p => {
    const card = document.createElement('div');
    card.className = 'pref-card' + (studentPref===p.v?' selected':'');
    card.innerHTML = `<div class="pref-row"><span class="pref-emoji">${p.emoji}</span><div><div class="pref-title">${p.v}</div><div class="pref-desc">${p.desc}</div></div></div>`;
    card.onclick = () => { studentPref=p.v; renderPrefCards(); document.getElementById('prefNext').disabled=false; };
    el.appendChild(card);
  });
}
 
// ════════════════════════════════════════
//  RENDER CONFIDENCE
// ════════════════════════════════════════
function renderConfidence() {
  const el = document.getElementById('confSection');
  el.innerHTML = '';
  Object.entries(subjectGroups).forEach(([stream, subjects]) => {
    const div = document.createElement('div');
    div.className = 'conf-group';
    div.innerHTML = `<h3>${stream} Subjects</h3>`;
    subjects.forEach(sub => {
      const row = document.createElement('div');
      row.className = 'conf-row';
      row.innerHTML = `<span class="conf-label">${sub}</span><div class="conf-btns" id="conf_${stream}_${sub.replace(/\s/g,'_')}"></div>`;
      div.appendChild(row);
      const btnsDiv = row.querySelector('.conf-btns');
      confLevels.forEach((lv, i) => {
        const btn = document.createElement('button');
        btn.className = 'conf-btn' + (confData[stream][sub]===i?' selected':'');
        btn.textContent = lv;
        btn.onclick = () => { confData[stream][sub]=i; renderConfidence(); };
        btnsDiv.appendChild(btn);
      });
    });
    el.appendChild(div);
  });
}
 
// ════════════════════════════════════════
//  RENDER PARENT STREAM BTNS
// ════════════════════════════════════════
function renderParentBtns() {
  const el = document.getElementById('parStreamBtns');
  el.innerHTML = '';
  ["Science","Commerce","Humanities","Not Sure"].forEach(s => {
    const btn = document.createElement('button');
    btn.className = 'par-stream-btn' + (parentPref===s?' selected':'');
    btn.textContent = s;
    btn.onclick = () => { parentPref=s; renderParentBtns(); };
    el.appendChild(btn);
  });
}
 
// ════════════════════════════════════════
//  ANALYSIS
// ════════════════════════════════════════
function analyze() {
  let sc = {Science:0,Commerce:0,Humanities:0};
  psychometricQs.forEach(q => { const a=psyAns[q.id]; if(a!==undefined&&q.w[a]){sc.Science+=q.w[a][0];sc.Commerce+=q.w[a][1];sc.Humanities+=q.w[a][2];} });
  let aptScore=0; aptitudeQs.forEach(q=>{if(aptAns[q.id]===q.correct)aptScore++;});
  sc.Science+=aptScore*1.5; sc.Commerce+=aptScore; sc.Humanities+=aptScore*0.5;
  Object.values(appAns).forEach(v=>{if(v===0)sc.Science+=3;if(v===1)sc.Commerce+=3;if(v===2)sc.Humanities+=3;if(v===3)sc.Humanities+=2;});
  Object.entries(confData).forEach(([stream,subjects])=>{const vals=Object.values(subjects);if(vals.length){const avg=vals.reduce((a,b)=>a+b,0)/vals.length;if(sc[stream]!==undefined)sc[stream]+=avg*2;}});
  const tot=sc.Science+sc.Commerce+sc.Humanities||1;
  const pct={Science:Math.round(sc.Science/tot*100),Commerce:Math.round(sc.Commerce/tot*100),Humanities:Math.round(sc.Humanities/tot*100)};
  const sorted=Object.entries(sc).sort((a,b)=>b[1]-a[1]);
  const recommended=sorted[0][0];
  const dims={Analytical:0,Creative:0,Social:0,Practical:0,Leadership:0,Research:0};
  psychometricQs.forEach(q=>{const a=psyAns[q.id];if(a===0){dims.Analytical+=2;dims.Research+=1;}if(a===1){dims.Social+=2;dims.Creative+=1;}if(a===2){dims.Creative+=2;dims.Social+=1;}if(a===3){dims.Practical+=2;dims.Leadership+=1;}});
  const maxD=Math.max(...Object.values(dims))||1;
  const radar={}; Object.entries(dims).forEach(([k,v])=>{radar[k]=Math.round(v/maxD*100);});
  const risks=[];
  if(studentPref&&studentPref!=="Not Sure"&&studentPref!==recommended) risks.push({flag:"⚠️ Stream Preference Mismatch",detail:`You prefer ${studentPref} but assessment suggests ${recommended}. Gap: ${pct[recommended]-(pct[studentPref]||0)}%`,severity:"warning"});
  if(aptScore<7) risks.push({flag:"📉 Aptitude Below Average",detail:`Scored ${aptScore}/15. Targeted practice recommended.`,severity:"warning"});
  if(aptScore<4) risks.push({flag:"🚨 Critical Aptitude Gap",detail:`Scored ${aptScore}/15. Intensive coaching needed.`,severity:"critical"});
  const lowConf=[];
  if(confData[recommended]) Object.entries(confData[recommended]).forEach(([sub,lv])=>{if(lv<=1)lowConf.push(sub);});
  if(lowConf.length) risks.push({flag:"📚 Low Subject Confidence",detail:`Low confidence in: ${lowConf.join(", ")}. Bridge courses recommended.`,severity:"warning"});
 
  const gap = streamSkills[recommended].map(sk=>({skill:sk,current:Math.floor(Math.random()*40)+30,required:Math.floor(Math.random()*20)+75}));
 
  return { scores:sc, percentages:pct, recommended, aptitudeScore:aptScore, aptitudeTotal:15, radarData:radar, risks, sorted, skillGap:gap };
}
 
// ════════════════════════════════════════
//  SVG RADAR CHART
// ════════════════════════════════════════
function radarSVG(data, size) {
  size = size || 260;
  const keys=Object.keys(data), n=keys.length, cx=size/2, cy=size/2, r=size*.38;
  const step=2*Math.PI/n;
  const pt=(i,val)=>({x:cx+r*(val/100)*Math.cos(i*step-Math.PI/2),y:cy+r*(val/100)*Math.sin(i*step-Math.PI/2)});
  let svg=`<svg width="${size}" height="${size}" viewBox="0 0 ${size} ${size}" xmlns="http://www.w3.org/2000/svg">`;
  [25,50,75,100].forEach(lv=>{const pts=keys.map((_,i)=>pt(i,lv)).map(p=>`${p.x},${p.y}`).join(' ');svg+=`<polygon points="${pts}" fill="none" stroke="#e5e7eb" stroke-width="${lv===100?1.5:.5}"/>`;});
  keys.forEach((_,i)=>{const p=pt(i,100);svg+=`<line x1="${cx}" y1="${cy}" x2="${p.x}" y2="${p.y}" stroke="#e5e7eb" stroke-width=".5"/>`;});
  const polyPts=keys.map((_,i)=>{const p=pt(i,data[keys[i]]);return`${p.x},${p.y}`;}).join(' ');
  svg+=`<polygon points="${polyPts}" fill="rgba(36,84,164,.2)" stroke="#2454A4" stroke-width="2"/>`;
  keys.forEach((k,i)=>{const p=pt(i,data[k]),lp=pt(i,118);
    svg+=`<circle cx="${p.x}" cy="${p.y}" r="4" fill="#2454A4"/>`;
    svg+=`<text x="${lp.x}" y="${lp.y}" text-anchor="middle" dominant-baseline="middle" font-size="10" font-weight="600" fill="#1a1a2e">${k}</text>`;
    svg+=`<text x="${lp.x}" y="${lp.y+12}" text-anchor="middle" font-size="9" fill="#6b7280">${data[k]}%</text>`;
  });
  svg+=`</svg>`;
  return svg;
}
 
// ════════════════════════════════════════
//  RENDER RESULTS
// ════════════════════════════════════════
function submitAndShowResults() {
  if(!document.getElementById('parName').value){alert('Parent name required');return;}
  results = analyze();
  skillGap = results.skillGap;
  goStep(8);
  renderResults();
  setTimeout(submitToGoogle, 500);
}
 
function renderResults() {
  const r = results, gap = skillGap;
  const stu = { name:document.getElementById('stuName').value, age:document.getElementById('stuAge').value, school:document.getElementById('stuSchool').value, city:document.getElementById('stuCity').value, board:document.getElementById('stuBoard').value, currentClass:document.getElementById('stuClass').value };
  const par = { name:document.getElementById('parName').value, phone:document.getElementById('parPhone').value, email:document.getElementById('parEmail').value, preferredStream:parentPref, reason:document.getElementById('parReason').value, expectations:document.getElementById('parExpect').value };
  const board = stu.board==="ICSE"?"ICSE":stu.board==="State Board"?"State Board":"CBSE";
  const subjects = (streamSubjects[r.recommended]||{})[board]||[];
  const parentMatch = par.preferredStream===r.recommended||par.preferredStream==="Not Sure";
  const careers = topCareers[r.recommended];
  const prefGap = studentPref&&studentPref!=="Not Sure"&&studentPref!==r.recommended;
  const topTraits = Object.entries(r.radarData).sort((a,b)=>b[1]-a[1]).slice(0,2).map(e=>e[0]);
 
  // Heatmap data
  const heatDims=["Personality","Aptitude","Application","Confidence","Overall"];
  const heatData={};
  ["Science","Commerce","Humanities"].forEach(s=>{
    const base=r.percentages[s];
    heatData[s]={Personality:Math.min(100,base+Math.floor(Math.random()*20-10)),Aptitude:Math.min(100,base+Math.floor(Math.random()*20-10)),Application:Math.min(100,base+Math.floor(Math.random()*20-10)),Confidence:Math.min(100,base+Math.floor(Math.random()*20-10)),Overall:base};
  });
  const heatColor=v=>v>=70?"#16a34a":v>=50?"#d97706":v>=30?"#ea580c":"#dc2626";
  const heatBg=v=>v>=70?"#f0fdf4":v>=50?"#fffbeb":v>=30?"#fff7ed":"#fef2f2";
 
  let html = '';
  html += `<div id="bannerArea"></div>`;
  const isTa_ = reportLang==='ta';
  html += `<div style="text-align:center;margin-bottom:22px"><h2 style="font-family:'Playfair Display',serif;font-size:26px;color:var(--dark)">🎓 ${isTa_?'விரிவான மதிப்பீட்டு அறிக்கை':'Comprehensive Assessment Report'}</h2><p style="color:var(--gray);font-size:13px">${isTa_?'மாணவர்':'for'} <strong>${stu.name}</strong> · ${stu.school} · ${isTa_?'வகுப்பு':'Class'} ${stu.currentClass} (${stu.board})</p></div>`;
 
  // Recommended box
  html += `<div class="rec-box"><div class="rec-label">${isTa_?T.recommended:'Recommended Stream'}</div><div class="rec-stream">${r.recommended}</div><div class="rec-sub">${isTa_?T.basedOn:'Based on 60+ question psychometric, aptitude & application analysis'}</div></div>`;
 
  // Risk flags
  if(r.risks.length) {
    html += `<div class="card"><div class="card-title">🚦 Decision Matrix & Risk Flags</div>`;
    r.risks.forEach(rk => { html += `<div class="risk-flag ${rk.severity==='critical'?'risk-crit':'risk-warn'}"><div class="risk-title" style="color:${rk.severity==='critical'?'var(--red)':'#92400e'}">${rk.flag}</div><div class="risk-detail">${rk.detail}</div></div>`; });
    html += `</div>`;
  }
 
  // Two col: radar + scores
  html += `<div class="two-col">`;
  html += `<div class="card"><div class="card-title">🕸️ Profile Strength Radar</div><div class="radar-wrap">${radarSVG(r.radarData)}</div><p style="font-size:11px;color:var(--gray);text-align:center;margin-top:8px">Higher = stronger trait</p></div>`;
  html += `<div class="card"><div class="card-title">📊 Stream Suitability</div>`;
  ["Science","Commerce","Humanities"].forEach(s=>{
    const isRec=s===r.recommended, isPref=s===studentPref;
    html+=`<div class="score-bar"><div class="score-info"><span>${s} ${isRec?"⭐":""}</span><span>${r.percentages[s]}%</span></div><div class="score-track"><div class="score-fill" style="width:${r.percentages[s]}%;background:${isRec?'linear-gradient(90deg,var(--primary),var(--accent))':isPref?'var(--yellow)':'#d1d5db'}"></div></div></div>`;
  });
  html+=`<div style="margin-top:10px;padding:8px 12px;background:#f0f9ff;border-radius:8px;font-size:12px"><strong>Aptitude:</strong> ${r.aptitudeScore}/${r.aptitudeTotal} (${Math.round(r.aptitudeScore/r.aptitudeTotal*100)}%)</div></div>`;
  html += `</div>`;
 
  // Heatmap
  html += `<div class="card"><div class="card-title">🗺️ Stream Suitability Heatmap</div><table class="heatmap"><thead><tr><th style="text-align:left">Stream</th>`;
  heatDims.forEach(d=>{html+=`<th>${d}</th>`;});
  html+=`</tr></thead><tbody>`;
  ["Science","Commerce","Humanities"].forEach(s=>{
    html+=`<tr><td>${s}</td>`;
    heatDims.forEach(d=>{const v=heatData[s][d];html+=`<td style="background:${heatBg(v)};color:${heatColor(v)}">${v}%</td>`;});
    html+=`</tr>`;
  });
  html+=`</tbody></table><p style="font-size:10px;color:var(--gray);margin-top:8px">🟢 70%+ Strong · 🟡 50-69% Moderate · 🟠 30-49% Developing · 🔴 Below 30%</p></div>`;
 
  // Preference gap
  html+=`<div class="card"><div class="card-title">🔍 Preference vs Assessment Gap</div>`;
  html+=`<div class="three-col"><div class="col-box" style="background:#f0f9ff"><div class="col-label">Student Preference</div><div class="col-value" style="color:var(--primary)">${studentPref||"N/A"}</div></div><div class="col-box" style="background:rgba(244,123,32,.08)"><div class="col-label">Assessment Result</div><div class="col-value" style="color:var(--accent)">${r.recommended}</div></div><div class="col-box" style="background:${parentMatch?'#f0fdf4':'#fef3c7'}"><div class="col-label">Parent Preference</div><div class="col-value" style="color:${parentMatch?'var(--green)':'var(--yellow)'}">${par.preferredStream||"N/A"}</div></div></div>`;
  if(prefGap){
    html+=`<div class="gap-box gap-warning"><div style="font-weight:700;font-size:13px;color:#92400e">⚠️ Gap Detected Between Preference & Assessment</div><div style="font-size:12px;margin-top:4px">You preferred <strong>${studentPref}</strong> (${r.percentages[studentPref]||0}%) but assessment suggests <strong>${r.recommended}</strong> (${r.percentages[r.recommended]}%). This ${(r.percentages[r.recommended])-(r.percentages[studentPref]||0)}% gap suggests your natural abilities may align differently. This is valuable information for an informed decision.</div></div>`;
  } else {
    html+=`<div class="gap-box gap-ok"><div style="font-weight:700;font-size:13px;color:var(--green)">✅ Preference & Assessment Aligned!</div><div style="font-size:12px;margin-top:4px">Your natural aptitude matches your preferred stream — a strong positive indicator.</div></div>`;
  }
  html+=`</div>`;
 
  // Why this recommendation
  html+=`<div class="card" style="background:rgba(36,84,164,.03);border:1.5px solid rgba(36,84,164,.15)"><div class="card-title">💡 ${isTa_?T.whyRec:'Why This Recommendation?'}</div><div style="font-size:13px;line-height:1.7"><p style="margin-bottom:10px">${isTa_?T.dearStudent:'Dear'} <strong>${stu.name}</strong>,</p><p style="margin-bottom:10px">${isTa_?`60+ கேள்விகளின் பகுப்பாய்வுக்குப் பிறகு — <strong>${r.recommended}</strong> உங்களுக்கு மிகவும் பொருத்தமானது.`:`After analyzing 60+ responses spanning personality, aptitude, application, and confidence — <strong>${r.recommended}</strong> is your strongest fit.`}</p><p style="margin-bottom:10px">${isTa_?`உங்கள் மனநிலை சோதனை வலுவான <strong>${topTraits.join(', ')}</strong> போக்குகளைக் காட்டுகிறது — ${r.recommended} க்கான முக்கிய பலங்கள். உங்கள் திறன் மதிப்பெண் <strong>${r.aptitudeScore}/15</strong>.`:`Your psychometric profile shows strong <strong>${topTraits.join(' and ')}</strong> tendencies — core strengths for ${r.recommended}. Your aptitude score of <strong>${r.aptitudeScore}/15</strong> and application responses consistently point toward ${r.recommended}-oriented thinking.`}</p>`;
  if(prefGap) html+=`<p style="padding:8px 12px;background:#fef3c7;border-radius:8px;margin-bottom:10px">📌 <strong>${reportLang==='ta'?`${studentPref} பற்றிய உங்கள் விருப்பம்:`:`About your preference for ${studentPref}:`}</strong> ${reportLang==='ta'?`விருப்பங்களும் திறனும் வேறுபடுவது இயல்பானது. திறந்த மனதுடன் ${r.recommended} தொழில்களை ஆராயுங்கள்.`:`It's normal for preferences and aptitude to differ. Explore the Top 10 ${r.recommended} careers below with an open mind.`}</p>`;
  html+=`<p>${reportLang==='ta'?'இது விவாதத்தின் தொடக்கப் புள்ளி, இறுதி தீர்ப்பு அல்ல. ஆராயுங்கள், கேள்விகள் கேளுங்கள், உங்களுக்கு சரியான தேர்வை செய்யுங்கள்.':'This is a starting point for discussion, not a final verdict. Explore, ask questions, and make the choice that feels right for YOU.'}</p></div></div>`;
 
  // ★ BREAKING BARRIERS — when gap exists
  if(prefGap){
    const isTa = reportLang==='ta';
    html+=`<div class="card" style="background:linear-gradient(135deg,rgba(244,123,32,.06),rgba(231,76,60,.06));border:2px solid rgba(244,123,32,.3)">
      <div class="card-title" style="color:var(--accent);font-size:18px">🔥 ${isTa?T.breakBarrier:'Breaking Barriers — Stepping Out of Your Comfort Zone'}</div>
      <p style="font-size:13px;margin-bottom:14px;line-height:1.6">${isTa?T.breakIntro:`Your preferred stream (${studentPref}) and the assessment result (${r.recommended}) don't match. <strong>This is not a failure — it's an opportunity.</strong> Growth happens when we challenge our assumptions. Here's how to take the risk and break through:`}</p>
      
      <div style="display:grid;gap:10px;margin-bottom:16px">
        <div style="padding:14px 18px;background:#fff;border-radius:10px;border-left:4px solid var(--accent)">
          <div style="font-weight:700;font-size:13px;color:var(--accent);margin-bottom:4px">🪞 ${isTa?'படி 1: ஏன் என்று உங்களையே கேளுங்கள்':'Step 1: Ask Yourself WHY'}</div>
          <div style="font-size:12px;line-height:1.6">${isTa?`"நான் ஏன் ${studentPref} விரும்புகிறேன்?" - பெற்றோர் விருப்பம், நண்பர்கள் அழுத்தம், அல்லது உண்மையான ஆர்வம்? உங்கள் பதிலை எழுதுங்கள்.`:`"Why do I prefer ${studentPref}?" — Is it family expectation, peer pressure, limited exposure, or genuine passion? Write your honest answer down. If it's external pressure, you owe it to yourself to explore ${r.recommended} fairly.`}</div>
        </div>
        <div style="padding:14px 18px;background:#fff;border-radius:10px;border-left:4px solid var(--primary)">
          <div style="font-weight:700;font-size:13px;color:var(--primary);margin-bottom:4px">🧪 ${isTa?'படி 2: 30-நாள் சவால்':'Step 2: The 30-Day Exploration Challenge'}</div>
          <div style="font-size:12px;line-height:1.6">${isTa?`அடுத்த 30 நாட்களுக்கு, ${r.recommended} தொடர்பான ஒரு செயலை தினமும் செய்யுங்கள்: YouTube வீடியோ பாருங்கள், புத்தகம் படியுங்கள், அந்த துறையில் வேலை செய்பவர்களிடம் பேசுங்கள்.`:`Commit to one ${r.recommended}-related activity daily for 30 days: watch a career documentary, read a chapter, solve a puzzle, or talk to someone in that field. Track how you feel — curiosity? excitement? boredom? Your emotional response is data.`}</div>
        </div>
        <div style="padding:14px 18px;background:#fff;border-radius:10px;border-left:4px solid var(--green)">
          <div style="font-weight:700;font-size:13px;color:var(--green);margin-bottom:4px">🤝 ${isTa?'படி 3: வழிகாட்டி கண்டுபிடியுங்கள்':'Step 3: Find a Mentor or Role Model'}</div>
          <div style="font-size:12px;line-height:1.6">${isTa?`${r.recommended} துறையில் வெற்றிகரமாக இருக்கும் ஒருவரை கண்டுபிடியுங்கள். அவர்களின் பயணத்தை கேளுங்கள். LinkedIn, YouTube, அல்லது குடும்ப நண்பர்கள் மூலம் தொடர்பு கொள்ளுங்கள்.`:`Find someone thriving in a ${r.recommended} career. Hear their journey. Many successful people ended up in fields they never initially considered. Reach out via LinkedIn, YouTube comments, or family networks.`}</div>
        </div>
        <div style="padding:14px 18px;background:#fff;border-radius:10px;border-left:4px solid var(--red)">
          <div style="font-weight:700;font-size:13px;color:var(--red);margin-bottom:4px">🎯 ${isTa?'படி 4: முடிவெடுக்கும் காலக்கெடு':'Step 4: Set a Decision Deadline'}</div>
          <div style="font-size:12px;line-height:1.6">${isTa?`இன்றிலிருந்து 3 மாதம் கழித்து இறுதி முடிவு எடுங்கள். அதுவரை இரண்டு பாதைகளையும் ஆராயுங்கள். பின்னர் தன்னம்பிக்கையுடன் தேர்வு செய்யுங்கள்.`:`Give yourself 3 months from today. During this period, explore BOTH ${studentPref} and ${r.recommended} actively. Keep a journal. At the deadline, make your decision with confidence — not confusion.`}</div>
        </div>
        <div style="padding:14px 18px;background:#fff;border-radius:10px;border-left:4px solid #7c3aed">
          <div style="font-weight:700;font-size:13px;color:#7c3aed;margin-bottom:4px">💪 ${isTa?'படி 5: உறுதிமொழி':'Step 5: Make a Commitment Statement'}</div>
          <div style="font-size:12px;line-height:1.6">${isTa?`"நான் ${r.recommended} ஐ உண்மையாக ஆராய்வேன், எனது வசதி மண்டலத்தை விட்டு வெளியே வருவேன்" என்று உங்களுக்கும் உங்கள் பெற்றோருக்கும் சொல்லுங்கள்.`:`Say this out loud: "I will genuinely explore ${r.recommended} for the next 90 days with an open mind. I will not let fear of the unknown stop me from discovering where I truly belong." Share this commitment with your parents.`}</div>
        </div>
      </div>
      <div style="padding:12px 16px;background:rgba(244,123,32,.08);border-radius:10px;font-size:12px;text-align:center;font-weight:600;color:var(--accent)">${isTa?`"வசதி மண்டலத்தின் முடிவில்தான் உண்மையான வாழ்க்கை தொடங்குகிறது" — நீல் டொனால்ட் வால்ஷ்`:`"Life begins at the end of your comfort zone." — Neale Donald Walsch`}</div>
    </div>`;
  }
 
  // Top 10 careers
  html+=`<div class="card"><div class="card-title">🏆 Top 10 Careers — ${r.recommended}</div><div style="overflow-x:auto"><table class="career-table"><thead><tr><th style="width:28px;text-align:center">#</th><th>Career</th><th>Courses</th><th>Job Roles</th><th style="text-align:center">AI</th><th style="text-align:center">Salary</th></tr></thead><tbody>`;
  careers.forEach((c,i)=>{
    const aiCls=c.ai==="High"?"ai-high":c.ai==="Medium"?"ai-med":"ai-low";
    html+=`<tr><td style="text-align:center;font-weight:700;color:var(--primary)">${i+1}</td><td><strong>${c.title}</strong><br><span style="font-size:10px;color:var(--gray)">${c.desc}</span></td><td style="font-size:10.5px">${c.courses.join(", ")}</td><td style="font-size:10.5px">${c.jobs.join(", ")}</td><td style="text-align:center"><span class="ai-tag ${aiCls}">${c.ai}</span><div style="font-size:9px;color:var(--gray);margin-top:2px">${c.aiNote}</div></td><td style="text-align:center;font-weight:600;font-size:10.5px">${c.sal}</td></tr>`;
  });
  html+=`</tbody></table></div></div>`;
 
  // Skill gap + action plan
  html+=`<div class="card"><div class="card-title">📈 Skill Gap & Action Plan</div><table class="skill-table"><thead><tr><th>Skill</th><th style="text-align:center">Current</th><th style="text-align:center">Required</th><th style="text-align:center">Gap</th><th>Action</th></tr></thead><tbody>`;
  gap.forEach(g=>{
    const gv=g.required-g.current;
    const act=gv>40?"Intensive coaching + daily practice":gv>25?"Regular practice + online courses":"Self-study + periodic review";
    const col=gv>40?"var(--red)":gv>25?"var(--yellow)":"var(--green)";
    html+=`<tr><td style="font-weight:600">${g.skill}</td><td style="text-align:center">${g.current}%</td><td style="text-align:center">${g.required}%</td><td style="text-align:center;font-weight:700;color:${col}">${gv}%</td><td style="font-size:11px;color:var(--gray)">${act}</td></tr>`;
  });
  html+=`</tbody></table>`;
  html+=`<div class="action-box"><div style="font-weight:700;font-size:13px;color:var(--primary);margin-bottom:6px">📋 Recommended Action Plan</div><strong>0-3 months:</strong> Bridge critical gaps (red). Explore ${r.recommended} careers. Enroll in foundation courses.<br><strong>3-6 months:</strong> Build practice routines. Join clubs/communities. Take mock tests.<br><strong>6-12 months:</strong> Pursue certifications/workshops. Attend career fairs. Finalize choice.<br><strong>1-2 years:</strong> Entrance exam prep. Build portfolio. Seek professional mentorship.</div></div>`;
 
  // Subjects
  html+=`<div class="card"><div class="card-title">📚 Subjects — ${r.recommended} (${board})</div><div>${subjects.map(s=>`<span class="tag">${s}</span>`).join(' ')}</div></div>`;
 
  // Note to parents
  html+=`<div class="card note-box"><div class="card-title">💬 ${isTa_?T.parentNote:'A Note for Parents'}</div><p style="margin-bottom:8px">${isTa_?T.dearParent:'Dear'} <strong>${par.name||'Parent'}</strong>,</p><p style="margin-bottom:8px">${isTa_?'இந்த மதிப்பீடு ஒரு <strong>உரையாடலின் தொடக்கம்</strong>, இறுதி முடிவு அல்ல.':'This assessment is a <strong>conversation starter</strong>, not a final decision.'}</p><p style="font-weight:700;color:var(--primary);margin-bottom:6px">${isTa_?`${stu.name} உடன் எப்படி விவாதிப்பது:`:`How to discuss with ${stu.name}:`}</p>`;
  html+=`<div class="note-item"><strong>${isTa_?'1. ஆர்வத்துடன் தொடங்குங்கள்:':'1. Start with curiosity:'}</strong> ${isTa_?`"எந்த கேள்விகள் சுவாரஸ்யமாக இருந்தன?" என்று கேளுங்கள், "${r.recommended} எடு" என்று சொல்ல வேண்டாம்.`:`Ask "What questions were interesting?" not "See, you should take ${r.recommended}."`}</div>`;
  html+=`<div class="note-item"><strong>${isTa_?'2. இடைவெளியை ஆராயுங்கள்:':'2. Explore the gap:'}</strong> ${prefGap?(isTa_?`உங்கள் குழந்தை ${studentPref} விரும்புகிறது, மதிப்பீடு ${r.recommended} பரிந்துரைக்கிறது. என்ன கவர்கிறது என்று கேளுங்கள்.`:`Your child preferred ${studentPref} while assessment suggests ${r.recommended}. Ask what attracts them — it reveals values.`):(isTa_?'மதிப்பீடு விருப்பத்துடன் ஒத்துப்போகிறது — இன்னும் ஏன் என்று ஆராயுங்கள்.':'Assessment aligns with preference — still explore WHY to ensure it\'s informed.')}</div>`;
  html+=`<div class="note-item"><strong>${isTa_?'3. தொழில்களில் கவனம் செலுத்துங்கள்:':'3. Focus on careers, not just streams:'}</strong> ${isTa_?'முதல் 10 தொழில்களை ஒன்றாக பாருங்கள். 10 விருப்பங்களைக் காட்டுவது கண்ணைத் திறக்கும்.':'Review Top 10 careers together. Showing 10 options can be eye-opening.'}</div>`;
  html+=`<div class="note-item"><strong>${isTa_?'4. உணர்வுகளை ஏற்றுக்கொள்ளுங்கள்:':'4. Acknowledge feelings:'}</strong> ${isTa_?'"நான் உங்களைப் புரிந்துகொள்ள விரும்புகிறேன், உங்களை என்ன உற்சாகப்படுத்துகிறது என்று சொல்லுங்கள்."':'If there\'s a mismatch, say "I hear you, help me understand what excites you."'}</div>`;
  html+=`<div class="note-item"><strong>${isTa_?'5. அடுத்த படிகளை ஒன்றாக திட்டமிடுங்கள்:':'5. Plan next steps together:'}</strong> ${isTa_?'செயல் திட்டத்தைப் பயன்படுத்துங்கள். சிறிய இலக்குகளை அமைக்கவும். 3-6 மாதங்களுக்குப் பிறகு மறுபரிசீலனை செய்யுங்கள்.':'Use the Action Plan. Set small goals. Revisit after 3-6 months.'}</div>`;
  if(!parentMatch) html+=`<p style="margin-top:10px;padding:10px 14px;background:#fef2f2;border-radius:8px;border-left:3px solid var(--red);font-size:12px"><strong>⚠️</strong> ${isTa_?`உங்கள் விருப்பம் (${par.preferredStream}) மதிப்பீட்டிலிருந்து (${r.recommended}) வேறுபடுகிறது. உள்ளார்ந்த ஊக்கம் திறனுடன் ஒத்துப்போகும்போது மாணவர்கள் சிறப்பாக செயல்படுவார்கள்.`:`Your preference (${par.preferredStream}) differs from assessment (${r.recommended}). Students perform best when intrinsic motivation aligns with ability.`}</p>`;
  html+=`</div>`;
 
  // Actions
  html+=`<div style="display:flex;gap:10px;justify-content:center;flex-wrap:wrap;margin-bottom:16px">`;
  html+=`<button class="btn btn-primary" onclick="printReport()" id="printBtn">🖨️ Print Full Report</button>`;
  html+=`<button class="btn btn-secondary" onclick="retake()">🔄 Retake Assessment</button>`;
  html+=`</div>`;
  html+=`<div id="pdfBtnArea"></div>`;
 
  // WhatsApp Community Links
  const wa = waLinks[r.recommended];
  const isTa = reportLang==='ta';
  html+=`<div class="card" style="background:linear-gradient(135deg,#dcfce7,#d1fae5);border:1.5px solid #86efac">
    <div class="card-title" style="color:#16a34a">📱 ${isTa?'எங்கள் WhatsApp சமூகத்தில் இணையுங்கள்':'Join Our WhatsApp Communities'}</div>
    <p style="font-size:12px;color:var(--dark);margin-bottom:12px">${isTa?'வழிகாட்டுதல், புதுப்பிப்புகள் மற்றும் சக மாணவர்களுடன் இணையுங்கள்:':'Stay connected for guidance, updates, and connect with fellow students:'}</p>
    <div style="display:grid;gap:8px">
      <a href="${wa.url}" target="_blank" style="display:flex;align-items:center;gap:10px;padding:12px 16px;background:#fff;border-radius:10px;text-decoration:none;border:1px solid #86efac;transition:all .2s">
        <span style="font-size:24px">💚</span>
        <div><div style="font-weight:700;font-size:13px;color:#16a34a">${wa.name}</div><div style="font-size:11px;color:var(--gray)">⭐ ${isTa?'உங்கள் பரிந்துரைக்கப்பட்ட பாதை — முதலில் இணையுங்கள்!':'Your recommended pathway — join this first!'}</div></div>
      </a>
      <a href="${waLinks.Emerging.url}" target="_blank" style="display:flex;align-items:center;gap:10px;padding:12px 16px;background:#fff;border-radius:10px;text-decoration:none;border:1px solid #86efac;transition:all .2s">
        <span style="font-size:24px">🚀</span>
        <div><div style="font-weight:700;font-size:13px;color:#16a34a">${waLinks.Emerging.name}</div><div style="font-size:11px;color:var(--gray)">${isTa?'AI, தொழில்நுட்பம் & எதிர்கால தொழில்கள்':'AI, tech & future career trends'}</div></div>
      </a>
      ${prefGap?`<a href="${waLinks[studentPref]?waLinks[studentPref].url:'#'}" target="_blank" style="display:flex;align-items:center;gap:10px;padding:12px 16px;background:#fff;border-radius:10px;text-decoration:none;border:1px solid #fbbf24;transition:all .2s">
        <span style="font-size:24px">🔍</span>
        <div><div style="font-weight:700;font-size:13px;color:#d97706">${waLinks[studentPref]?waLinks[studentPref].name:'Explore More'}</div><div style="font-size:11px;color:var(--gray)">${isTa?'உங்கள் விருப்பமான பாதை — ஒப்பிட்டு பாருங்கள்':'Your preferred pathway — explore & compare'}</div></div>
      </a>`:''}
    </div>
  </div>`;
 
  html+=`<div class="footer-box"><p style="font-size:12px;margin-bottom:2px">${isTa?T.counselling:'For personalized 1-on-1 counselling'}</p><a href="https://www.eduaakashaa.in" target="_blank">www.eduaakashaa.in</a><p style="font-size:10px;color:var(--gray);margin-top:4px">contact@eduaakashaa.in</p></div>`;
 
  document.getElementById('resultsContent').innerHTML = html;
 
  // Build print content
  buildPrintContent(r, gap, stu, par, careers, subjects, board, parentMatch, prefGap, topTraits, heatData, heatDims);
}
 
// ════════════════════════════════════════
//  PRINT
// ════════════════════════════════════════
function buildPrintContent(r,gap,stu,par,careers,subjects,board,parentMatch,prefGap,topTraits,heatData,heatDims) {
  let h = `<div style="text-align:center;border-bottom:3px solid #2454A4;padding-bottom:14px;margin-bottom:18px"><h1 style="color:#2454A4;font-size:24px">EduAakashaa</h1><p style="color:#F47B20;font-size:11px;letter-spacing:3px">PSYCHOMETRIC CAREER STREAM ASSESSMENT REPORT</p><p style="font-size:10px;color:#888;margin-top:3px">www.eduaakashaa.in | contact@eduaakashaa.in</p></div>`;
  h+=`<h2>Student Details</h2><table><tr><td><b>Name</b></td><td>${stu.name}</td><td><b>Age</b></td><td>${stu.age}</td></tr><tr><td><b>School</b></td><td>${stu.school}</td><td><b>City</b></td><td>${stu.city}</td></tr><tr><td><b>Board</b></td><td>${stu.board}</td><td><b>Class</b></td><td>${stu.currentClass}</td></tr><tr><td><b>Student Pref</b></td><td>${studentPref}</td><td><b>Parent Pref</b></td><td>${par.preferredStream||'N/A'}</td></tr></table>`;
  h+=`<div style="background:#2454A4;color:#fff;text-align:center;padding:18px;border-radius:8px;margin:16px 0"><div style="font-size:10px;letter-spacing:3px">RECOMMENDED STREAM</div><div style="font-size:26px;font-weight:800">${r.recommended}</div></div>`;
  if(r.risks.length){h+=`<h2>Risk Flags</h2>`;r.risks.forEach(rk=>{h+=`<div class="${rk.severity==='critical'?'risk-crit':'risk-warn'}"><b>${rk.flag}</b> — ${rk.detail}</div>`;});}
  h+=`<h2>Scores</h2><table><tr><th>Stream</th><th>Score</th><th>Student</th><th>Parent</th><th>Status</th></tr>`;
  ["Science","Commerce","Humanities"].forEach(s=>{h+=`<tr${s===r.recommended?' style="background:#f0f9ff"':''}><td><b>${s}</b></td><td>${r.percentages[s]}%</td><td>${s===studentPref?'✓':''}</td><td>${s===par.preferredStream?'✓':''}</td><td>${s===r.recommended?'✅ REC':'—'}</td></tr>`;});
  h+=`</table><p><b>Aptitude:</b> ${r.aptitudeScore}/${r.aptitudeTotal}</p>`;
  h+=`<h2>Profile Strength</h2><table><tr><th>Dimension</th><th>Score</th></tr>`;
  Object.entries(r.radarData).sort((a,b)=>b[1]-a[1]).forEach(([k,v])=>{h+=`<tr><td>${k}</td><td>${v}%</td></tr>`;});
  h+=`</table>`;
  h+=`<h2>Why ${r.recommended}?</h2><p>Your profile shows strong ${topTraits.join(' and ')} traits. Combined with aptitude and application responses, ${r.recommended} is the strongest fit.${prefGap?` Your preference for ${studentPref} is noted — explore ${r.recommended} careers with an open mind.`:''}</p>`;
  h+=`<div class="pagebreak"></div><h2>Top 10 Careers — ${r.recommended}</h2><table><tr><th>#</th><th>Career</th><th>Courses</th><th>Jobs</th><th>AI</th><th>Salary</th></tr>`;
  careers.forEach((c,i)=>{h+=`<tr><td>${i+1}</td><td><b>${c.title}</b><br><span style="font-size:9px">${c.desc}</span></td><td style="font-size:10px">${c.courses.join(', ')}</td><td style="font-size:10px">${c.jobs.join(', ')}</td><td style="text-align:center"><b style="color:${c.ai==='High'?'#dc2626':c.ai==='Medium'?'#d97706':'#16a34a'}">${c.ai}</b></td><td style="font-size:10px">${c.sal}</td></tr>`;});
  h+=`</table>`;
  h+=`<h2>Skill Gap & Action Plan</h2><table><tr><th>Skill</th><th>Current</th><th>Required</th><th>Gap</th><th>Action</th></tr>`;
  gap.forEach(g=>{const gv=g.required-g.current;h+=`<tr><td>${g.skill}</td><td>${g.current}%</td><td>${g.required}%</td><td style="color:#dc2626;font-weight:700">${gv}%</td><td style="font-size:10px">${gv>40?'Intensive coaching':'Regular practice'}</td></tr>`;});
  h+=`</table><h3>Timeline</h3><p><b>0-3 mo:</b> Bridge gaps. Explore careers.<br><b>3-6 mo:</b> Build routines. Join communities.<br><b>6-12 mo:</b> Certifications. Career fairs.<br><b>1-2 yr:</b> Exam prep. Portfolio. Mentorship.</p>`;
  h+=`<h2>Subjects (${board})</h2><p>${subjects.join(', ')}</p>`;
  h+=`<h2>Parent Input</h2><table><tr><td><b>Parent</b></td><td>${par.name}</td><td><b>Contact</b></td><td>${par.phone} | ${par.email}</td></tr><tr><td><b>Pref</b></td><td>${par.preferredStream||'N/A'}</td><td><b>Aligned</b></td><td>${parentMatch?'✅ Yes':'⚠️ No'}</td></tr></table>`;
  h+=`<h2>Note to Parents</h2><p>This is a conversation starter. Discuss openly with ${stu.name}. Explore careers together. If mismatch exists, approach with curiosity. Consider counselling at www.eduaakashaa.in.</p>`;
  // Breaking barriers in print
  if(prefGap){
    h+=`<h2>🔥 Breaking Barriers — Stepping Out of Comfort Zone</h2>`;
    h+=`<p>Your preferred stream (${studentPref}) and assessment result (${r.recommended}) don't match. This is an opportunity for growth.</p>`;
    h+=`<p><b>Step 1 — Ask Yourself WHY:</b> Is your preference based on genuine passion or external pressure?</p>`;
    h+=`<p><b>Step 2 — 30-Day Challenge:</b> Explore one ${r.recommended}-related activity daily for 30 days.</p>`;
    h+=`<p><b>Step 3 — Find a Mentor:</b> Connect with someone thriving in a ${r.recommended} career.</p>`;
    h+=`<p><b>Step 4 — Decision Deadline:</b> Give yourself 3 months. Explore both paths, then decide with confidence.</p>`;
    h+=`<p><b>Step 5 — Commitment:</b> "I will genuinely explore ${r.recommended} for 90 days with an open mind."</p>`;
  }
  // WhatsApp links in print
  const waRec = waLinks[r.recommended];
  h+=`<h2>📱 Join Our WhatsApp Communities</h2>`;
  h+=`<p><b>${waRec.name}</b><br/>${waRec.url}</p>`;
  h+=`<p><b>${waLinks.Emerging.name}</b><br/>${waLinks.Emerging.url}</p>`;
  if(prefGap && waLinks[studentPref]){h+=`<p><b>${waLinks[studentPref].name}</b> (Your preferred pathway)<br/>${waLinks[studentPref].url}</p>`;}
  h+=`<div class="footer"><b style="color:#2454A4">EduAakashaa</b> — www.eduaakashaa.in | contact@eduaakashaa.in<br><em>Generated ${new Date().toLocaleDateString('en-IN')}. For personalized counselling, visit our website.</em></div>`;
  document.getElementById('printContent').innerHTML = h;
}
 
function printReport() {
  const content = document.getElementById('printContent').innerHTML;
  const w = window.open('','_blank');
  w.document.write(`<!DOCTYPE html><html><head><title>EduAakashaa Report</title></head><body>${content}</body></html>`);
  w.document.close();
  setTimeout(()=>w.print(),400);
}
 
function retake() {
  psyAns={}; aptAns={}; appAns={}; confData={Science:{},Commerce:{},Humanities:{}}; studentPref=''; parentPref=''; results=null; skillGap=null; reportLang='en';
  document.getElementById('langEn').classList.add('selected');
  document.getElementById('langTa').classList.remove('selected');
  goStep(0);
}
 
// ════════════════════════════════════════
//  GOOGLE SUBMIT
// ════════════════════════════════════════
async function submitToGoogle() {
  if(APPS_SCRIPT_URL.includes('YOUR_APPS')){showBanner('error','Apps Script URL not configured. Deploy the script first.');return;}
  showBanner('saving','Saving to Google Sheets & generating PDF on Drive...');
  const stu={name:document.getElementById('stuName').value,age:document.getElementById('stuAge').value,school:document.getElementById('stuSchool').value,city:document.getElementById('stuCity').value,board:document.getElementById('stuBoard').value,currentClass:document.getElementById('stuClass').value};
  const par={name:document.getElementById('parName').value,phone:document.getElementById('parPhone').value,email:document.getElementById('parEmail').value,preferredStream:parentPref,reason:document.getElementById('parReason').value,expectations:document.getElementById('parExpect').value};
  const board=stu.board==='ICSE'?'ICSE':stu.board==='State Board'?'State Board':'CBSE';
  const r=results;
  try{
    const resp=await fetch(APPS_SCRIPT_URL,{method:'POST',headers:{'Content-Type':'text/plain'},
      body:JSON.stringify({action:'saveAssessment',studentInfo:stu,studentPreference:studentPref,personalityAns:psyAns,aptitudeAns:aptAns,applicationAns:appAns,confidenceData:confData,parentInfo:par,results:r,skillGap,reportLang,topCareers:topCareers[r.recommended],streamInfo:{subjects:(streamSubjects[r.recommended]||{})[board]||[],careers:topCareers[r.recommended].map(c=>c.title)}})});
    const data=await resp.json();
    if(data.success){
      showBanner('success','✅ Saved to Sheets & PDF uploaded to Drive!');
      if(data.pdfUrl){document.getElementById('pdfBtnArea').innerHTML=`<div style="text-align:center;margin-bottom:16px"><button class="btn btn-primary" onclick="window.open('${data.pdfUrl}','_blank')">📄 Open PDF from Google Drive</button></div>`;}
    } else { showBanner('error','Error: '+(data.error||'Unknown')); }
  }catch(e){showBanner('error','Network error: '+e.message);}
}
 
function showBanner(type,text) {
  const area = document.getElementById('bannerArea');
  if(!area) return;
  const cls = type==='saving'?'banner-saving':type==='success'?'banner-success':'banner-error';
  const icon = type==='saving'?'⏳':type==='success'?'✅':'❌';
  area.innerHTML = `<div class="banner ${cls}"><span style="font-size:16px">${icon}</span>${text}</div>`;
}
 
// ════════════════════════════════════════
//  INIT
// ════════════════════════════════════════
document.addEventListener('DOMContentLoaded', () => {
  renderPrefCards();
  renderQuestions('psyQuestions', psychometricQs, psyAns, 'psyCount', 'psyNext');
  renderQuestions('aptQuestions', aptitudeQs, aptAns, 'aptCount', 'aptNext');
  renderQuestions('appQuestions', applicationQs, appAns, 'appCount', 'appNext');
  renderConfidence();
  renderParentBtns();
});


// ---- next <script> block ----


	const heightObserver = new ResizeObserver(([{ contentRect }]) => {
		window.parent.postMessage({ action: 'iframeHeightUpdated', height: contentRect.height, id: 'z04zhT' }, '*');
	});

	heightObserver.observe(document.documentElement);
