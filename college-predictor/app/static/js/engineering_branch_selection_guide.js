/* ============ DATA ============ */
// ratings: 1=Low 2=Medium 3=High 4=Very High
// radar axes: coding, maths, physics, electronics, handsOn, communication (0-100)
// heat skill clusters: AI/Data, Software/Cloud, Hardware/Embedded, Design/Mechanical, Construction/Infra (1-9)
const BRANCHES = [
 {key:'cse',name:'Computer Science',abbr:'CSE',icon:'code',
  short:'Programming, data structures, algorithms, databases, networks, cloud and the foundations of software & AI.',
  who:'Students who enjoy logic puzzles, coding and continuous self-learning.',
  subjects:['Programming','Data structures','Algorithms','Databases','Operating systems','Computer networks','Cloud computing','AI foundations','Software engineering'],
  skills:['DSA','Full-stack dev','Cloud','DevOps','System design','Cyber basics','AI integration'],
  roles:['Software Developer','Full-stack Developer','Cloud Engineer','DevOps Engineer','Data Engineer','AI Engineer','Security Analyst'],
  fit:'Strong logic, coding stamina, patience for debugging, self-driven learner.',
  risk:'Saturated at the bottom — without projects and DSA depth, placements are average.',
  ai:80,demand:95,
  rate:{coding:4,math:3,physics:2,core:3,ai:4,place:4,sal:4,startup:4,higher:4,govt:2,gulf:3,nri:4},
  radar:{coding:95,math:78,physics:45,electronics:30,handsOn:35,communication:60},
  heat:[8,9,4,3,2],
  roadmap:[
   ['Programming fundamentals','C/Python + Git','Maths for CS','First mini-projects'],
   ['DSA seriously','One web/app stack','SQL & databases','Open-source contributions'],
   ['System design basics','Cloud + DevOps','A solid internship','Domain depth (AI / security)'],
   ['DSA interview prep','Capstone project','Communication & resume','Targeted applications']]},
 {key:'aids',name:'AI & Data Science',abbr:'AI&DS',icon:'cpu',
  short:'Machine learning, statistics, Python, analytics, neural networks and applied generative AI.',
  who:'Maths-comfortable students who like patterns, data and real experimentation.',
  subjects:['Statistics & probability','Python','Machine learning','Deep learning','Data visualisation','Data engineering','Generative AI applications'],
  skills:['Python','Statistics','ML','Deep learning','Data viz','MLOps','GenAI apps'],
  roles:['Data Scientist','ML Engineer','AI Product Analyst','Data Engineer','BI Analyst','Computer Vision Engineer'],
  fit:'Strong maths/statistics, curiosity for data, willingness to build real projects.',
  risk:'Crowded by buzzword-chasers — without maths and real projects, AI stays a label.',
  ai:90,demand:92,
  rate:{coding:4,math:4,physics:2,core:2,ai:4,place:3,sal:4,startup:4,higher:4,govt:2,gulf:3,nri:4},
  radar:{coding:85,math:95,physics:40,electronics:25,handsOn:35,communication:62},
  heat:[9,7,3,2,2],
  roadmap:[
   ['Python + maths foundation','Statistics basics','Excel & data handling','Curiosity projects'],
   ['Core ML algorithms','SQL & data wrangling','Visualisation','Kaggle / real datasets'],
   ['Deep learning','MLOps basics','A data internship','A published project'],
   ['GenAI / specialisation','Portfolio of 2–3 projects','Communicating results','Targeted applications']]},
 {key:'it',name:'Information Technology',abbr:'IT',icon:'server',
  short:'Software systems, web & enterprise applications, IT infrastructure, cloud and databases.',
  who:'Students who like building and running real software systems end to end.',
  subjects:['Software systems','Web applications','IT infrastructure','Cloud platforms','Databases','Enterprise applications'],
  skills:['Web dev','Cloud','Databases','DevOps','Scripting','Cyber basics'],
  roles:['Software Engineer','Web/App Developer','Cloud Engineer','Systems Analyst','Support / SRE','QA Engineer'],
  fit:'Practical builders who like systems, integration and getting things shipped.',
  risk:'Overlaps with CSE — differentiate with strong projects and a clear specialisation.',
  ai:78,demand:88,
  rate:{coding:4,math:3,physics:2,core:2,ai:3,place:3,sal:3,startup:3,higher:3,govt:2,gulf:3,nri:4},
  radar:{coding:88,math:65,physics:40,electronics:30,handsOn:45,communication:62},
  heat:[7,9,4,2,2],
  roadmap:[
   ['Programming + Git','Web basics (HTML/CSS/JS)','Databases intro','Mini web apps'],
   ['One full stack','SQL depth','Cloud fundamentals','Team project'],
   ['DevOps / CI-CD','Security basics','A real internship','Specialise (cloud / data)'],
   ['System design lite','Capstone + portfolio','Resume & communication','Applications']]},
 {key:'cyber',name:'Cyber Security',abbr:'CYBER',icon:'shield',
  short:'Ethical hacking, network security, cryptography, forensics, cloud security and risk.',
  who:'Detail-driven students who like breaking, securing and investigating systems.',
  subjects:['Network security','Cryptography','Ethical hacking','Digital forensics','Cloud security','Risk management'],
  skills:['Networking','Linux','Scripting','Pen-testing','SIEM','Cloud security'],
  roles:['Security Analyst','Penetration Tester','SOC Analyst','Security Engineer','GRC Analyst','Forensics Analyst'],
  fit:'Curious, methodical, comfortable with networks and constant learning.',
  risk:'Needs hands-on labs & certifications — theory alone does not land roles.',
  ai:72,demand:90,
  rate:{coding:3,math:3,physics:2,core:2,ai:3,place:3,sal:4,startup:3,higher:3,govt:3,gulf:3,nri:3},
  radar:{coding:78,math:62,physics:42,electronics:45,handsOn:55,communication:58},
  heat:[6,8,5,2,2],
  roadmap:[
   ['Networking + Linux','Programming basics','How attacks work','Home lab setup'],
   ['Security fundamentals','Scripting (Python/Bash)','First certification path','CTF practice'],
   ['Pen-testing / blue team','Cloud security','Security internship','Specialise'],
   ['Advanced certs','Capstone / lab portfolio','Communication & reporting','Applications']]},
 {key:'ece',name:'Electronics & Communication',abbr:'ECE',icon:'chip',
  short:'Circuits, signals, communication, embedded systems, VLSI, semiconductors, IoT and robotics.',
  who:'Students who like both hardware and code, and want broad options.',
  subjects:['Electronic circuits','Signals & systems','Communication systems','Microprocessors','Embedded systems','VLSI','Semiconductor devices','IoT'],
  skills:['Embedded C','VLSI','FPGA','IoT','PCB design','Signal processing'],
  roles:['Embedded Engineer','VLSI Engineer','Semiconductor Designer','IoT Engineer','Network Engineer','Robotics Engineer'],
  fit:'Comfortable with maths & physics, enjoys both circuits and programming.',
  risk:'Core electronics roles cluster in fewer cities — embedded/VLSI skill is key.',
  ai:65,demand:80,
  rate:{coding:2,math:3,physics:3,core:3,ai:3,place:3,sal:3,startup:3,higher:3,govt:3,gulf:3,nri:3},
  radar:{coding:62,math:80,physics:82,electronics:92,handsOn:65,communication:55},
  heat:[5,5,9,4,2],
  roadmap:[
   ['Circuits & devices','C programming','Maths/physics base','Tinkering projects'],
   ['Embedded systems','Microcontrollers','Signals basics','Hardware project'],
   ['VLSI or IoT track','PCB / FPGA','Core internship','Domain depth'],
   ['Specialised tools','Capstone + portfolio','Software cross-skill','Applications']]},
 {key:'eee',name:'Electrical & Electronics',abbr:'EEE',icon:'bolt',
  short:'Power systems, electrical machines, control systems, renewable energy, EV systems and automation.',
  who:'Students drawn to power, energy, control and the EV / renewables wave.',
  subjects:['Power systems','Electrical machines','Control systems','Renewable energy','EV systems','Industrial automation'],
  skills:['MATLAB/Simulink','Power systems','PLC & SCADA','EV systems','Renewables','Automation'],
  roles:['Power Systems Engineer','EV Engineer','Renewable Energy Engineer','Automation Engineer','Control Engineer','Design Engineer'],
  fit:'Strong physics & maths, interest in energy, machines and control.',
  risk:'Early pay tracks skill & sector — EV / renewables / automation lift prospects.',
  ai:62,demand:78,
  rate:{coding:2,math:3,physics:4,core:4,ai:3,place:3,sal:3,startup:2,higher:3,govt:4,gulf:3,nri:3},
  radar:{coding:48,math:80,physics:88,electronics:78,handsOn:70,communication:55},
  heat:[5,4,7,5,3],
  roadmap:[
   ['Circuits & machines','Maths/physics base','MATLAB intro','Basic projects'],
   ['Power & control systems','PLC basics','EV / renewables intro','Lab project'],
   ['Automation / EV depth','SCADA','Core internship','Specialise'],
   ['Energy tools','Capstone + portfolio','Cross-skill (data)','Applications']]},
 {key:'mech',name:'Mechanical',abbr:'MECH',icon:'gear',
  short:'Design, manufacturing, thermodynamics, robotics, CAD/CAM, automotive, aerospace and automation.',
  who:'Students who like machines, design, physics and building physical things.',
  subjects:['Engineering mechanics','Thermodynamics','Fluid mechanics','Manufacturing','Machine design','CAD/CAM','Robotics','Industrial automation'],
  skills:['CAD','CAE','Robotics','PLC','Industrial automation','EV tech','Additive mfg'],
  roles:['Design Engineer','Manufacturing Engineer','Automation Engineer','Robotics Engineer','EV Systems Engineer','Plant Engineer'],
  fit:'Strong physics, spatial thinking, enjoys design and hands-on work.',
  risk:'Premium roles need a multi-skill stack (CAD + automation + a digital skill).',
  ai:60,demand:72,
  rate:{coding:2,math:3,physics:4,core:4,ai:3,place:2,sal:3,startup:2,higher:3,govt:3,gulf:3,nri:3},
  radar:{coding:38,math:78,physics:88,electronics:45,handsOn:90,communication:55},
  heat:[4,3,5,9,4],
  roadmap:[
   ['Mechanics & drawing','CAD basics','Maths/physics base','Workshop projects'],
   ['Thermo & design','CAD/CAM depth','Robotics / automation intro','Build project'],
   ['Automation / EV / robotics','Simulation (CAE)','Industry internship','Specialise'],
   ['Digital cross-skill','Capstone + portfolio','Communication','Applications']]},
 {key:'civil',name:'Civil',abbr:'CIVIL',icon:'building',
  short:'Structures, construction, geotechnical, transportation, urban planning and smart infrastructure.',
  who:'Students who like construction, design and large-scale infrastructure — strong in the Gulf.',
  subjects:['Structural engineering','Construction tech','Geotechnical engineering','Transportation','Urban planning','Sustainability'],
  skills:['AutoCAD','Revit / BIM','STAAD Pro','Primavera','Quantity surveying','Sustainability'],
  roles:['Structural Engineer','Site Engineer','BIM Engineer','Project Engineer','Quantity Surveyor','Construction Manager'],
  fit:'Enjoys design + field work, planning, and large physical projects.',
  risk:'Early pay depends heavily on skills & location — BIM and Gulf demand help.',
  ai:50,demand:68,
  rate:{coding:1,math:2,physics:3,core:4,ai:2,place:2,sal:2,startup:2,higher:2,govt:4,gulf:4,nri:4},
  radar:{coding:25,math:62,physics:72,electronics:20,handsOn:85,communication:60},
  heat:[3,2,2,5,9],
  roadmap:[
   ['Mechanics & materials','AutoCAD','Maths/physics base','Site visits'],
   ['Structures & design','Revit / BIM intro','STAAD Pro','Project work'],
   ['BIM + project mgmt','Quantity surveying','Site / consulting internship','Specialise'],
   ['Sustainability / smart-infra','Capstone + portfolio','Communication','Gulf-aware applications']]},
 {key:'chem',name:'Chemical',abbr:'CHEM',icon:'flask',
  short:'Process engineering, petroleum, pharma, materials, energy and industrial chemistry.',
  who:'Students strong in chemistry & maths who like processes and industry.',
  subjects:['Process engineering','Thermodynamics','Petroleum / energy','Pharma & materials','Industrial chemistry','Environmental systems'],
  skills:['Process simulation','Plant operations','Safety / HAZOP','Data analysis','Materials','Energy systems'],
  roles:['Process Engineer','Plant Engineer','Quality Engineer','R&D Associate','Safety Engineer','Energy Analyst'],
  fit:'Strong chemistry & maths, systems thinking, comfort with industry settings.',
  risk:'Roles cluster around specific industries & locations — plan geography early.',
  ai:48,demand:62,
  rate:{coding:1,math:3,physics:3,core:4,ai:2,place:2,sal:2,startup:2,higher:3,govt:3,gulf:3,nri:2},
  radar:{coding:25,math:75,physics:70,electronics:25,handsOn:72,communication:52},
  heat:[3,2,3,4,5],
  roadmap:[
   ['Chemistry & maths base','Process basics','Lab skills','Industry awareness'],
   ['Thermo & transport','Simulation tools','Safety basics','Plant project'],
   ['Specialise (energy/pharma)','Data analysis','Plant internship','Domain depth'],
   ['Process / energy tools','Capstone + portfolio','Communication','Applications']]},
 {key:'biotech',name:'Biotechnology',abbr:'BIOTECH',icon:'dna',
  short:'Biology, genetics, bioinformatics, pharma, medical research, food and healthcare innovation.',
  who:'Biology-loving students drawn to research, healthcare and life sciences.',
  subjects:['Cell & molecular biology','Genetics','Bioinformatics','Pharma & medical research','Food technology','Bioprocess engineering'],
  skills:['Lab techniques','Bioinformatics','Data analysis','Research methods','Quality / regulatory','Python basics'],
  roles:['Research Associate','Bioinformatics Analyst','Quality / Regulatory','Lab Scientist','Process Associate','Higher-studies track'],
  fit:'Strong biology, patience for research, often a higher-studies path.',
  risk:'Industry roles in India are limited at UG level — many pursue higher studies.',
  ai:52,demand:58,
  rate:{coding:2,math:2,physics:2,core:3,ai:2,place:2,sal:2,startup:2,higher:4,govt:3,gulf:2,nri:3},
  radar:{coding:35,math:55,physics:42,electronics:20,handsOn:78,communication:55},
  heat:[4,3,2,3,3],
  roadmap:[
   ['Biology & chemistry base','Lab fundamentals','Intro bioinformatics','Curiosity reading'],
   ['Core biotech subjects','Data / Python basics','Research methods','Lab project'],
   ['Specialise (bioinfo/pharma)','Quality / regulatory','Research internship','Plan higher studies'],
   ['Research depth','Capstone / paper','Communication','Higher-studies / job apps']]},
 {key:'robo',name:'Robotics & Automation',abbr:'ROBO',icon:'robot',
  short:'Mechanical design, electronics, sensors, programming, control and AI-driven robotics.',
  who:'Students who like the intersection of mechanics, electronics and code.',
  subjects:['Mechanical design','Electronics & sensors','Control systems','Programming','AI for robotics','Industrial automation'],
  skills:['CAD','Embedded C','ROS','Control systems','Sensors','PLC / automation'],
  roles:['Robotics Engineer','Automation Engineer','Controls Engineer','Embedded Engineer','R&D Engineer','Mechatronics Engineer'],
  fit:'Multi-disciplinary, enjoys building integrated systems end to end.',
  risk:'Broad by design — needs a deliberate depth area to avoid being a generalist.',
  ai:68,demand:74,
  rate:{coding:3,math:3,physics:4,core:4,ai:4,place:3,sal:3,startup:3,higher:3,govt:2,gulf:3,nri:3},
  radar:{coding:65,math:75,physics:80,electronics:80,handsOn:88,communication:55},
  heat:[6,5,7,8,3],
  roadmap:[
   ['Mechanics + electronics','C / Python','Maths/physics base','Build a simple bot'],
   ['Control systems','Embedded + sensors','ROS basics','Robotics project'],
   ['AI for robotics','Automation / PLC','Industry internship','Specialise'],
   ['Depth area + tools','Capstone + portfolio','Communication','Applications']]},
 {key:'mechatronics',name:'Mechatronics',abbr:'MECHTR',icon:'cog',
  short:'Mechanical + electronics + computer control: smart machines, automation and robotics.',
  who:'Students who want a deliberately blended mechanical-electronics-software path.',
  subjects:['Mechanical systems','Electronics','Control systems','Microcontrollers','Automation','Smart manufacturing'],
  skills:['CAD','Embedded systems','PLC / SCADA','Control','Sensors','Automation'],
  roles:['Mechatronics Engineer','Automation Engineer','Controls Engineer','Maintenance Engineer','Design Engineer','Robotics Engineer'],
  fit:'Comfortable across disciplines, enjoys integrated smart-machine work.',
  risk:'Like robotics — pick a depth area; "knows a bit of everything" undersells you.',
  ai:64,demand:70,
  rate:{coding:3,math:3,physics:4,core:4,ai:3,place:3,sal:3,startup:2,higher:3,govt:3,gulf:3,nri:3},
  radar:{coding:58,math:72,physics:80,electronics:78,handsOn:85,communication:55},
  heat:[5,4,7,8,4],
  roadmap:[
   ['Mechanics + circuits','C programming','Maths/physics base','Hands-on kits'],
   ['Control + microcontrollers','CAD','Automation intro','Integrated project'],
   ['PLC / SCADA depth','Sensors & actuators','Industry internship','Specialise'],
   ['Depth area + tools','Capstone + portfolio','Communication','Applications']]}
];

const ICONS={
 code:'<polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/>',
 cpu:'<rect x="4" y="4" width="16" height="16" rx="2"/><rect x="9" y="9" width="6" height="6"/><path d="M9 2v2M15 2v2M9 20v2M15 20v2M2 9h2M2 15h2M20 9h2M20 15h2"/>',
 server:'<rect x="3" y="4" width="18" height="7" rx="1.5"/><rect x="3" y="13" width="18" height="7" rx="1.5"/><path d="M7 7.5h.01M7 16.5h.01"/>',
 shield:'<path d="M12 2 4 6v6c0 5 3.5 8 8 10 4.5-2 8-5 8-10V6l-8-4z"/><path d="m9 12 2 2 4-4"/>',
 chip:'<rect x="5" y="5" width="14" height="14" rx="2"/><path d="M9 1v3M15 1v3M9 20v3M15 20v3M1 9h3M1 15h3M20 9h3M20 15h3"/>',
 bolt:'<path d="M13 2 4 14h7l-1 8 9-12h-7l1-8z"/>',
 gear:'<circle cx="12" cy="12" r="3.2"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M5 5l2 2M17 17l2 2M19 5l-2 2M7 17l-2 2"/>',
 building:'<rect x="5" y="3" width="14" height="18" rx="1"/><path d="M9 7h2M13 7h2M9 11h2M13 11h2M9 15h2M13 15h2M10 21v-3h4v3"/>',
 flask:'<path d="M9 2h6M10 2v6l-5 9a2 2 0 0 0 1.8 3h10.4a2 2 0 0 0 1.8-3l-5-9V2"/><path d="M7.5 14h9"/>',
 dna:'<path d="M4 3c0 6 16 6 16 12M20 3c0 6-16 6-16 12M5 7h14M5 17h14"/>',
 robot:'<rect x="5" y="8" width="14" height="11" rx="2"/><path d="M12 3v5M9 13h.01M15 13h.01M9 16h6M2 12h3M19 12h3"/>',
 cog:'<circle cx="12" cy="12" r="3"/><path d="M12 1v4M12 19v4M4.2 4.2l2.8 2.8M17 17l2.8 2.8M1 12h4M19 12h4M4.2 19.8 7 17M17 7l2.8-2.8"/>'
};
const RATE_WORDS=['','Low','Medium','High','Very High'];
const COLS=[
 {k:'name',t:'Branch'},{k:'coding',t:'Coding'},{k:'math',t:'Maths'},{k:'physics',t:'Physics'},
 {k:'core',t:'Core depth'},{k:'ai',t:'AI impact'},{k:'place',t:'Placement'},{k:'sal',t:'Salary'},
 {k:'startup',t:'Startup'},{k:'higher',t:'Higher ed'},{k:'govt',t:'Govt scope'},{k:'gulf',t:'Gulf'},{k:'nri',t:'NRI fit'}
];
const FILTERS=[
 {id:'all',t:'All branches',test:()=>true},
 {id:'hicode',t:'High coding',test:b=>b.rate.coding>=4},
 {id:'locode',t:'Low coding',test:b=>b.rate.coding<=2},
 {id:'hisal',t:'High salary potential',test:b=>b.rate.sal>=4},
 {id:'ai',t:'High AI impact',test:b=>b.ai>=70},
 {id:'gulf',t:'Gulf relevance',test:b=>b.rate.gulf>=3 && b.rate.core>=3},
 {id:'higher',t:'Higher studies',test:b=>b.rate.higher>=4},
 {id:'govt',t:'Govt job scope',test:b=>b.rate.govt>=4},
 {id:'core',t:'Core engineering',test:b=>b.rate.core>=4 && b.rate.coding<=2}
];

/* ============ HERO GAUGES ============ */
function gauge(value,label,color){
  const r=42,c=2*Math.PI*r;
  return `<div class="gauge-item"><svg width="104" height="104" viewBox="0 0 120 120">
    <circle cx="60" cy="60" r="${r}" fill="none" stroke="var(--cream-2)" stroke-width="12"/>
    <circle class="ring" data-val="${value}" data-max="100" cx="60" cy="60" r="${r}" fill="none"
      stroke="${color}" stroke-width="12" stroke-linecap="round"
      stroke-dasharray="${c}" stroke-dashoffset="${c}" transform="rotate(-90 60 60)"
      style="transition:stroke-dashoffset 1.1s ease"/>
    <text x="60" y="58" text-anchor="middle" font-family="Fraunces,serif" font-size="26" font-weight="600" fill="var(--navy-ink)">${value}</text>
    <text x="60" y="76" text-anchor="middle" font-family="JetBrains Mono,monospace" font-size="9" fill="var(--muted)">/ 100</text>
  </svg><div class="lbl">${label}</div></div>`;
}
document.getElementById('heroGauges').innerHTML=
  gauge(95,'CSE','var(--orange)')+gauge(92,'AI & DS','var(--navy)')+gauge(80,'ECE','var(--green)')+gauge(68,'Civil','var(--navy)');

/* ============ BRANCH EXPLORER ============ */
const grid=document.getElementById('branchGrid');
function renderGrid(){
  grid.innerHTML=BRANCHES.map((b,i)=>{
    const top=Object.entries(b.rate).filter(([k,v])=>v===4).slice(0,2).map(([k])=>({coding:'High coding',math:'Maths-heavy',ai:'AI-shaped',place:'Strong placements',sal:'High pay potential',startup:'Startup-friendly',higher:'Higher studies',gulf:'Gulf demand',nri:'NRI-friendly',govt:'Govt scope',core:'Core depth',physics:'Physics-heavy'}[k])).filter(Boolean);
    return `<article class="bcard" data-key="${b.key}" tabindex="0" role="button" aria-label="Open ${b.name} details">
      <span class="stamp">${String(i+1).padStart(2,'0')}</span>
      <div class="ico"><svg viewBox="0 0 24 24">${ICONS[b.icon]}</svg></div>
      <span class="abbr">${b.abbr}</span>
      <h3>${b.name}</h3>
      <p>${b.short}</p>
      <div class="tags">${top.map(t=>`<span class="tag vh">${t}</span>`).join('')}</div>
      <span class="more">View detail →</span>
    </article>`;
  }).join('');
  grid.querySelectorAll('.bcard').forEach(c=>{
    c.addEventListener('click',()=>openModal(c.dataset.key));
    c.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();openModal(c.dataset.key);}});
  });
}
renderGrid();

const fbar=document.getElementById('filters');
fbar.innerHTML=FILTERS.map((f,i)=>`<button class="pill${i===0?' active':''}" data-f="${f.id}">${f.t}</button>`).join('');
fbar.querySelectorAll('.pill').forEach(p=>p.addEventListener('click',()=>{
  fbar.querySelectorAll('.pill').forEach(x=>x.classList.remove('active'));
  p.classList.add('active');
  const f=FILTERS.find(x=>x.id===p.dataset.f);
  grid.querySelectorAll('.bcard').forEach(c=>{
    const b=BRANCHES.find(x=>x.key===c.dataset.key);
    c.classList.toggle('hide',!f.test(b));
  });
}));

/* ============ MODAL ============ */
function openModal(key){
  const b=BRANCHES.find(x=>x.key===key); if(!b)return;
  document.getElementById('mTitle').textContent=b.name;
  document.getElementById('mAbbr').textContent=b.abbr+' · Branch detail';
  document.getElementById('mBody').innerHTML=`
   <div class="mblock"><div class="mt">In one line</div><p>${b.short}</p></div>
   <div class="mgrid">
     <div class="mblock"><div class="mt">Who it suits</div><p>${b.who}</p></div>
     <div class="mblock"><div class="mt">Best-fit profile</div><p>${b.fit}</p></div>
   </div>
   <div class="mblock"><div class="mt">What you'll study</div><div class="chips">${b.subjects.map(s=>`<span class="chip">${s}</span>`).join('')}</div></div>
   <div class="mblock"><div class="mt">Skills to build</div><div class="chips">${b.skills.map(s=>`<span class="chip">${s}</span>`).join('')}</div></div>
   <div class="mblock"><div class="mt">Common roles</div><div class="chips">${b.roles.map(s=>`<span class="chip">${s}</span>`).join('')}</div></div>
   <div class="mgrid">
     <div class="mblock"><div class="mt">AI impact on the role</div>
       <div class="meter"><div class="ml"><span>How much the role is changing</span><span>${b.ai}/100</span></div><div class="mtrack"><div class="mfill" data-w="${b.ai}"></div></div></div></div>
     <div class="mblock"><div class="mt">Future demand signal</div>
       <div class="meter"><div class="ml"><span>Direction of travel</span><span>${b.demand}/100</span></div><div class="mtrack"><div class="mfill" data-w="${b.demand}"></div></div></div></div>
   </div>
   <div class="mblock"><div class="mt">Honest risk flag</div><p>${b.risk}</p></div>`;
  document.getElementById('modalBg').classList.add('open');
  document.body.style.overflow='hidden';
  setTimeout(()=>document.querySelectorAll('#mBody .mfill').forEach(f=>f.style.width=f.dataset.w+'%'),120);
}
function closeModal(){document.getElementById('modalBg').classList.remove('open');document.body.style.overflow='';}
document.getElementById('modalClose').addEventListener('click',closeModal);
document.getElementById('modalBg').addEventListener('click',e=>{if(e.target.id==='modalBg')closeModal();});
document.addEventListener('keydown',e=>{if(e.key==='Escape')closeModal();});

/* ============ COMPARISON MATRIX ============ */
let sortKey=null,sortAsc=false;
const mHead=document.getElementById('matrixHead'),mBody=document.getElementById('matrixBody');
mHead.innerHTML=COLS.map(c=>`<th data-k="${c.k}">${c.t}</th>`).join('');
function rateCell(v){
  const dots=[1,2,3,4].map(n=>`<i class="${n<=v?'on':''}"></i>`).join('');
  return `<span class="rate ${v===4?'vh':''}">${dots}<span class="rl">${RATE_WORDS[v]}</span></span>`;
}
function renderMatrix(){
  let rows=[...BRANCHES];
  const q=document.getElementById('matrixSearch').value.trim().toLowerCase();
  if(q)rows=rows.filter(b=>(b.name+' '+b.abbr).toLowerCase().includes(q));
  if(sortKey)rows.sort((a,b)=>{const av=sortKey==='name'?a.name:a.rate[sortKey],bv=sortKey==='name'?b.name:b.rate[sortKey];const r=sortKey==='name'?String(av).localeCompare(bv):av-bv;return sortAsc?r:-r;});
  mBody.innerHTML=rows.map(b=>`<tr data-key="${b.key}" style="cursor:pointer">
    <td><span class="bname">${b.name}<small>${b.abbr}</small></span></td>
    ${COLS.slice(1).map(c=>`<td>${rateCell(b.rate[c.k])}</td>`).join('')}
  </tr>`).join('');
  mBody.querySelectorAll('tr').forEach(tr=>tr.addEventListener('click',()=>openModal(tr.dataset.key)));
}
mHead.querySelectorAll('th').forEach(th=>th.addEventListener('click',()=>{
  const k=th.dataset.k; if(sortKey===k)sortAsc=!sortAsc; else{sortKey=k;sortAsc=(k==='name');}
  renderMatrix();
}));
document.getElementById('matrixSearch').addEventListener('input',renderMatrix);
renderMatrix();

/* ============ RADAR ============ */
Chart.defaults.font.family="'Plus Jakarta Sans', sans-serif";
let radarSel=['cse','mech'];
const radarCtx=document.getElementById('radarChart');
const RADAR_AXES=[['coding','Coding'],['math','Maths'],['physics','Physics'],['electronics','Electronics'],['handsOn','Hands-on'],['communication','Communication']];
let radarChart;
function buildRadar(){
  const cols=['#0E3A8A','#FF6B0A'];
  const ds=radarSel.map((k,i)=>{const b=BRANCHES.find(x=>x.key===k);return{label:b.abbr,data:RADAR_AXES.map(a=>b.radar[a[0]]),borderColor:cols[i],backgroundColor:i?'rgba(255,107,10,.15)':'rgba(14,58,138,.15)',borderWidth:2,pointBackgroundColor:cols[i],pointRadius:3};});
  if(radarChart)radarChart.destroy();
  radarChart=new Chart(radarCtx,{type:'radar',data:{labels:RADAR_AXES.map(a=>a[1]),datasets:ds},
    options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{position:'bottom',labels:{boxWidth:12,font:{size:11}}}},
    scales:{r:{suggestedMin:0,suggestedMax:100,grid:{color:'#E8DFC8'},angleLines:{color:'#E8DFC8'},pointLabels:{font:{size:11},color:'#0E1B3D'},ticks:{display:false}}}}});
}
const rp=document.getElementById('radarPicker');
rp.innerHTML=BRANCHES.map(b=>`<button class="rm-pill${radarSel.includes(b.key)?' active':''}" data-k="${b.key}">${b.abbr}</button>`).join('');
rp.querySelectorAll('.rm-pill').forEach(p=>p.addEventListener('click',()=>{
  const k=p.dataset.k;
  if(radarSel.includes(k)){if(radarSel.length>1)radarSel=radarSel.filter(x=>x!==k);}
  else{radarSel.push(k);if(radarSel.length>2)radarSel.shift();}
  rp.querySelectorAll('.rm-pill').forEach(x=>x.classList.toggle('active',radarSel.includes(x.dataset.k)));
  buildRadar();
}));
buildRadar();

/* ============ HEATMAP ============ */
const HEAT_COLS=['AI / Data','Software / Cloud','Hardware / Embedded','Design / Mechanical','Construction / Infra'];
const heatRows=BRANCHES.map(b=>({label:b.abbr,vals:b.heat}));
(function heatmap(){
  const svg=d3.select('#heatmap'),W=460,H=300,pad={l:64,t:64,r:8,b:14};
  const cw=(W-pad.l-pad.r)/HEAT_COLS.length, ch=(H-pad.t-pad.b)/heatRows.length;
  const color=d3.scaleLinear().domain([1,5,9]).range(['#EAEFF7','#8FA8D6','#0E3A8A']);
  // column labels (rotated)
  HEAT_COLS.forEach((c,ci)=>{
    svg.append('text').attr('transform',`translate(${pad.l+ci*cw+cw/2},${pad.t-8}) rotate(-32)`).attr('font-size',9).attr('font-family','JetBrains Mono').attr('fill','#5A6278').text(c);
  });
  heatRows.forEach((row,bi)=>{
    svg.append('text').attr('x',pad.l-8).attr('y',pad.t+bi*ch+ch/2+3).attr('text-anchor','end').attr('font-size',9.5).attr('font-family','JetBrains Mono').attr('fill','#071A44').text(row.label);
    row.vals.forEach((v,ri)=>{
      svg.append('rect').attr('x',pad.l+ri*cw).attr('y',pad.t+bi*ch).attr('width',cw-2).attr('height',ch-2)
        .attr('fill',color(v)).attr('rx',3)
        .append('title').text(`${row.label} · ${HEAT_COLS[ri]}: ${v}/9`);
      svg.append('text').attr('x',pad.l+ri*cw+(cw-2)/2).attr('y',pad.t+bi*ch+ch/2+3).attr('text-anchor','middle')
        .attr('font-size',9.5).attr('font-weight',600).attr('fill',v>5?'#fff':'#071A44').text(v);
    });
  });
})();

/* ============ ROADMAP GENERATOR ============ */
const rmPicker=document.getElementById('rmPicker'),rmTrack=document.getElementById('rmTrack');
rmPicker.innerHTML=BRANCHES.map((b,i)=>`<button class="rm-pill${i===0?' active':''}" data-k="${b.key}">${b.abbr}</button>`).join('');
function renderRoadmap(key){
  const b=BRANCHES.find(x=>x.key===key);
  const phases=['Build foundations','Go deeper','Prove it (internship)','Convert to offers'];
  rmTrack.innerHTML=b.roadmap.map((yr,i)=>`<div class="rm-step">
    <div class="yr">Year ${i+1}</div><div class="ph">${phases[i]}</div>
    <ul>${yr.map(s=>`<li>${s}</li>`).join('')}</ul></div>`).join('');
}
rmPicker.querySelectorAll('.rm-pill').forEach(p=>p.addEventListener('click',()=>{
  rmPicker.querySelectorAll('.rm-pill').forEach(x=>x.classList.remove('active'));
  p.classList.add('active');renderRoadmap(p.dataset.k);
}));
renderRoadmap('cse');

/* ============ FITNESS QUIZ ============ */
const QUESTIONS=[
 {q:'How do you feel about coding and logic puzzles?',opts:[['Love them — I tinker for fun',{coding:3,software:2}],['Comfortable, in moderation',{coding:1,software:1}],['Not really my thing',{handsOn:2,physics:1}]]},
 {q:'How comfortable are you with advanced maths & physics?',opts:[['Very — they come naturally',{math:3,physics:2,hardware:1}],['Okay with effort',{math:1}],['I prefer to avoid heavy maths',{handsOn:1,bio:1}]]},
 {q:'What kind of work appeals more?',opts:[['Desk-based software / data',{software:3,coding:1}],['Hands-on machines & building',{handsOn:3,physics:1}],['Field, structures & projects',{infra:3,handsOn:1}],['Labs, biology & research',{bio:3}]]},
 {q:'How do you feel about electronics & circuits?',opts:[['Fascinated by hardware',{hardware:3,physics:1}],['Mildly interested',{hardware:1}],['Prefer software or other',{software:1}]]},
 {q:'What is your bigger career priority?',opts:[['High-demand, fast-moving fields',{software:2,coding:1,ai:2}],['Stable core-engineering domains',{infra:2,hardware:1,physics:1}],['Research & higher studies',{bio:2,math:1}]]},
 {q:'Are you an NRI / Gulf-based student?',opts:[['Yes — Gulf career matters',{infra:2,hardware:1}],['Yes — global flexibility matters',{software:2,ai:1}],['No / not a factor',{}]]}
];
// map score dimensions to branches
const DIM_BRANCH={software:['cse','it'],coding:['cse','aids'],ai:['aids','cse'],hardware:['ece','robo'],physics:['eee','mech'],handsOn:['mech','robo'],infra:['civil','eee'],bio:['biotech','chem'],math:['aids','ece']};
const quizEl=document.getElementById('quiz');
let qIdx=0,scores={};
function renderQ(){
  if(qIdx>=QUESTIONS.length){return renderResult();}
  const Q=QUESTIONS[qIdx];
  quizEl.innerHTML=`<div class="q-prog"><span class="qc">Question ${qIdx+1} / ${QUESTIONS.length}</span><span class="q-bar"><i style="width:${qIdx/QUESTIONS.length*100}%"></i></span></div>
    <div class="q-text">${Q.q}</div>
    <div class="q-opts">${Q.opts.map((o,i)=>`<button class="q-opt" data-i="${i}">${o[0]}</button>`).join('')}</div>`;
  quizEl.querySelectorAll('.q-opt').forEach(btn=>btn.addEventListener('click',()=>{
    const o=Q.opts[+btn.dataset.i][1];
    for(const k in o)scores[k]=(scores[k]||0)+o[k];
    qIdx++;renderQ();
  }));
}
function renderResult(){
  const tally={};
  for(const dim in scores){(DIM_BRANCH[dim]||[]).forEach((bk,rank)=>{tally[bk]=(tally[bk]||0)+scores[dim]*(rank===0?1:0.6);});}
  const ranked=Object.entries(tally).sort((a,b)=>b[1]-a[1]).map(([k])=>BRANCHES.find(x=>x.key===k));
  const primary=ranked[0]||BRANCHES[0],backup=ranked[1]||BRANCHES[2];
  const skill=primary.skills[0];
  quizEl.innerHTML=`<div class="q-result">
    <div class="q-prog"><span class="qc">Result · Indicative only</span><span class="q-bar"><i style="width:100%"></i></span></div>
    <span class="rtag">Your direction</span>
    <h3>Explore <em style="font-style:italic">${primary.name}</em> first</h3>
    <p style="color:var(--muted);font-size:15px">Based on your answers, here's a starting direction. Treat it as a conversation-opener with a mentor — not a final verdict.</p>
    <div class="q-rec">
      <div class="rc"><div class="l">Primary fit</div><div class="v">${primary.name}<small>${primary.abbr}</small></div></div>
      <div class="rc"><div class="l">Backup to consider</div><div class="v">${backup.name}<small>${backup.abbr}</small></div></div>
      <div class="rc"><div class="l">Skill to start now</div><div class="v" style="font-size:15px">${skill}</div></div>
      <div class="rc"><div class="l">Before you commit</div><div class="v" style="font-size:14px">Verify the college's median salary &amp; placement %</div></div>
    </div>
    <div style="display:flex;gap:12px;flex-wrap:wrap">
      <button class="btn-primary" id="quizDetail">See ${primary.abbr} detail <span class="arw">→</span></button>
      <button class="btn-ghost" id="quizRestart">Retake quiz</button>
    </div></div>`;
  document.getElementById('quizDetail').addEventListener('click',()=>openModal(primary.key));
  document.getElementById('quizRestart').addEventListener('click',()=>{qIdx=0;scores={};renderQ();});
}
renderQ();

/* ============ PASSION VS REALITY ============ */
const PVR=[
 ['"I love computers, so CSE it is."','CSE rewards consistent coding practice, logical thinking and patience for debugging — the degree is the easy part; the self-learning is the job.'],
 ['"I like cars, so Mechanical."','Mechanical is physics, thermodynamics, design and manufacturing. Premium roles increasingly need CAD plus automation or a digital skill on top.'],
 ['"AI pays well, so AI & DS is safe."','AI demands real maths, statistics and shipped projects. Without strong fundamentals, "AI" becomes a line on a resume, not a capability.'],
 ['"Civil has less competition."','Civil suits students who love construction, BIM and infrastructure — strong in the Gulf — but early pay leans heavily on skills and location.']
];
document.getElementById('pvrGrid').innerHTML=PVR.map(p=>`<div class="pvr">
  <div class="side pass"><div class="h">Passion says</div><p>${p[0]}</p></div>
  <div class="side real"><div class="h">Reality check</div><p>${p[1]}</p></div></div>`).join('');

/* ============ FAQ ============ */
const FAQS=[
 ['Q·01 · For students','Is it better to pick a popular branch or the right-fit one?','A right-fit branch you stay motivated in usually beats a "popular" branch you struggle through. Popularity shifts every few years; your aptitude and interest are more durable. Use the fitness quiz as a start, then validate with a mentor.'],
 ['Q·02 · For parents','Does the branch decide the salary?','Not on its own. The branch sets a range, but the profile a student builds — projects, internships, communication, depth — decides where in that range they land. Two students in the same branch and college can see very different offers.'],
 ['Q·03 · On AI','Will AI make some branches pointless?','We have not seen evidence of that. AI is changing what each role expects rather than removing the role. The practical response is to build the AI-adjacent skills for your branch, whatever it is — not to avoid the branch.'],
 ['Q·04 · For NRI families','Should an NRI student pick the same branches as Indian peers?','Only if the same factors apply. NRI families should also weigh adjustment, hostel and food comfort, location, Gulf job relevance and the higher-studies pathway alongside the subject itself, and plan the DASA / CIWG route deliberately.'],
 ['Q·05 · On colleges','What should we check before trusting a college brochure?','Ask for branch-wise placement percentage, the median (not headline) salary, verified internship data, and whether labs and any "Centre of Excellence" are actually used by students for real projects — not just marketing.']
];
document.getElementById('faqList').innerHTML=FAQS.map(f=>`<div class="faq"><div class="faq-q"><span class="qn">${f[0]}</span><span class="qt">${f[1]}</span><span class="tog"></span></div><div class="faq-a"><p>${f[2]}</p></div></div>`).join('');
document.querySelectorAll('.faq-q').forEach(q=>q.addEventListener('click',()=>q.parentElement.classList.toggle('open')));

/* ============ NAV + REVEAL ============ */
const hamb=document.getElementById('hamb'),navLinks=document.getElementById('navLinks');
hamb.addEventListener('click',()=>navLinks.classList.toggle('show'));
navLinks.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>navLinks.classList.remove('show')));
const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('visible');io.unobserve(e.target);}}),{threshold:.12});
document.querySelectorAll('.reveal').forEach(el=>io.observe(el));
setTimeout(()=>{const c=2*Math.PI*42;document.querySelectorAll('#heroGauges .ring').forEach(el=>{el.style.strokeDashoffset=c*(1-(+el.dataset.val)/(+el.dataset.max));});},250);
