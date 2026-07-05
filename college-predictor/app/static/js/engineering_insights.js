/*
============================================================
  GOOGLE SHEETS INTEGRATION — ONE-TIME SETUP
============================================================
  1. Create a new Google Sheet. First row headers (left-to-right):
     Timestamp | Name | Email | Phone | Parent Name | Class | Board |
     JEE Rank | Target Exam | City | Parent Phone | Notes |
     Electronics | Electrical | Mechanical | CSE | Civil | Chemical | AI/DS |
     Top Branch | Top Score

  2. In the sheet: Extensions > Apps Script. Paste this script:

       function doPost(e){
         try{
           var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
           var d = JSON.parse(e.postData.contents);
           sheet.appendRow([
             new Date(), d.name, d.email, d.phone, d.parent_name,
             d.class, d.board, d.jee_rank, d.target_exam, d.city,
             d.parent_phone, d.notes,
             d.scores ? d.scores.electronics : "",
             d.scores ? d.scores.electrical  : "",
             d.scores ? d.scores.mechanical  : "",
             d.scores ? d.scores.cse         : "",
             d.scores ? d.scores.civil       : "",
             d.scores ? d.scores.chemical    : "",
             d.scores ? d.scores.ai_ds       : "",
             d.top_branch || "", d.top_score || ""
           ]);
           return ContentService.createTextOutput(JSON.stringify({ok:true}))
                                .setMimeType(ContentService.MimeType.JSON);
         }catch(err){
           return ContentService.createTextOutput(JSON.stringify({ok:false,error:err.message}))
                                .setMimeType(ContentService.MimeType.JSON);
         }
       }

  3. Deploy > New Deployment > Type: Web App. Execute as: Me.
     Who has access: Anyone. Copy the Web App URL.

  4. Paste your URL inside the quotes below in place of "REPLACE_ME".
     The form will then POST securely to your sheet on every submit.
============================================================
*/
const GOOGLE_SHEETS_WEBHOOK_URL = "REPLACE_ME";

/* SCROLL REVEAL */
const io = new IntersectionObserver((entries)=>{
  entries.forEach(e=>{ if(e.isIntersecting){ e.target.classList.add('visible'); io.unobserve(e.target);} });
},{threshold:.12,rootMargin:'0px 0px -40px 0px'});
document.querySelectorAll('.reveal').forEach(el=>io.observe(el));

/* HAMBURGER */
const ham = document.getElementById('hamburger');
const nlinks = document.getElementById('navLinks');
ham.addEventListener('click',()=>nlinks.classList.toggle('open'));
nlinks.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>nlinks.classList.remove('open')));

/* STORAGE FOR STUDENT DATA */
let studentData = null;

/* FORM SUBMIT */
const form = document.getElementById('studentForm');
const formStatus = document.getElementById('formStatus');
const assessLock = document.getElementById('assessLock');
const assessWrap = document.getElementById('assessWrap');

form.addEventListener('submit', async (e)=>{
  e.preventDefault();
  formStatus.className = 'form-status';
  formStatus.textContent = '';

  const fd = new FormData(form);
  const data = Object.fromEntries(fd.entries());
  studentData = data;

  // POST to Google Sheet (if configured) — non-blocking; assessment unlocks regardless
  if (GOOGLE_SHEETS_WEBHOOK_URL && GOOGLE_SHEETS_WEBHOOK_URL !== "REPLACE_ME"){
    try{
      await fetch(GOOGLE_SHEETS_WEBHOOK_URL, {
        method:'POST',
        mode:'no-cors',
        headers:{'Content-Type':'text/plain'},
        body: JSON.stringify(data)
      });
      formStatus.className = 'form-status success';
      formStatus.textContent = '✓ Saved. Your assessment is unlocked below.';
    }catch(err){
      formStatus.className = 'form-status error';
      formStatus.textContent = 'Saved locally — Google Sheet sync failed. Assessment is still unlocked.';
    }
  } else {
    formStatus.className = 'form-status success';
    formStatus.textContent = '✓ Saved locally. Configure Google Sheets URL for cloud sync. Assessment is unlocked below.';
  }

  // Unlock assessment
  assessLock.style.display = 'none';
  assessWrap.classList.add('unlocked');
  setTimeout(()=>{
    document.getElementById('assessment').scrollIntoView({behavior:'smooth',block:'start'});
  }, 400);
});

document.getElementById('formReset').addEventListener('click',()=>{
  form.reset();
  formStatus.className = 'form-status';
  formStatus.textContent = '';
});

/* ============================================================
   ASSESSMENT WEIGHTS · 15 questions × 7 branches
   Each row = one question's weight per branch (0.0 to 1.0)
   ============================================================ */
const branchKeys = ['electronics','electrical','mechanical','cse','civil','chemical','ai_ds'];
const branchLabels = {
  electronics:'Electronics (ECE / EI / Mechatronics)',
  electrical:'Electrical (EEE / EE / Energy / EV)',
  mechanical:'Mechanical (ME / Aero / Auto / Production)',
  cse:'Computer Science (CSE / IT / Cyber / M&C)',
  civil:'Civil (CE / Structural / Construction)',
  chemical:'Chemical (ChE / Pharma / Petroleum)',
  ai_ds:'AI & Data Science (AI / ML / DS)'
};

// Q1=Math, Q2=Chem, Q3=Physics, Q4=Code, Q5=Devices, Q6=Infra, Q7=Energy,
// Q8=Pharma/FMCG, Q9=AI/ML, Q10=Hands-on, Q11=3D-viz, Q12=Field, Q13=PSU,
// Q14=Reading, Q15=Re-learning
const W = {
  electronics: [0.75, 0.30, 0.90, 0.55, 0.95, 0.35, 0.45, 0.30, 0.60, 0.85, 0.55, 0.40, 0.55, 0.55, 0.65],
  electrical:  [0.85, 0.30, 0.90, 0.60, 0.80, 0.50, 1.00, 0.40, 0.45, 0.75, 0.45, 0.70, 0.95, 0.40, 0.50],
  mechanical:  [0.75, 0.30, 0.95, 0.45, 1.00, 0.55, 0.65, 0.40, 0.35, 0.95, 1.00, 0.85, 0.80, 0.30, 0.45],
  cse:         [0.70, 0.20, 0.30, 1.00, 0.40, 0.30, 0.35, 0.25, 0.75, 0.40, 0.40, 0.10, 0.20, 0.75, 0.95],
  civil:       [0.60, 0.20, 0.85, 0.30, 0.70, 1.00, 0.45, 0.30, 0.20, 0.65, 0.95, 1.00, 1.00, 0.25, 0.35],
  chemical:    [0.85, 1.00, 0.75, 0.40, 0.50, 0.35, 0.70, 1.00, 0.30, 0.85, 0.40, 0.90, 0.70, 0.55, 0.45],
  ai_ds:       [1.00, 0.30, 0.40, 1.00, 0.40, 0.30, 0.40, 0.30, 1.00, 0.40, 0.40, 0.10, 0.20, 1.00, 1.00]
};

const sliders = () => document.querySelectorAll('input[type="range"][data-q]');
let currentScores = null;

function updateSliderFill(s){
  const v = parseInt(s.value);
  const p = ((v-1)/9)*100;
  s.style.setProperty('--p', p+'%');
  document.getElementById('v'+s.dataset.q).textContent = v;
}

function computeScores(){
  const answers = Array.from(sliders()).sort((a,b)=>+a.dataset.q-+b.dataset.q).map(s=>parseInt(s.value));
  const scores = {};
  branchKeys.forEach(br=>{
    const w = W[br];
    let weighted = 0, max = 0;
    for(let i=0;i<15;i++){
      weighted += answers[i] * w[i];
      max += 10 * w[i];
    }
    scores[br] = Math.round((weighted/max)*100);
  });
  return scores;
}

function renderResults(){
  const scores = computeScores();
  currentScores = scores;
  // Sort branches by score desc
  const sorted = branchKeys.map(k=>({k,v:scores[k]})).sort((a,b)=>b.v-a.v);
  const top = sorted[0];
  document.getElementById('topPct').textContent = top.v + '%';
  document.getElementById('topBranch').textContent = branchLabels[top.k];
  document.getElementById('resultTitle').textContent = 'Your top fit: ' + branchLabels[top.k].split('(')[0].trim();
  const second = sorted[1], third = sorted[2];
  document.getElementById('resultBody').textContent =
    'Your strongest branch alignment is '+branchLabels[top.k].split('(')[0].trim()+
    '. Strong alternatives: '+branchLabels[second.k].split('(')[0].trim()+
    ' ('+second.v+'%) and '+branchLabels[third.k].split('(')[0].trim()+' ('+third.v+'%). '+
    'A counsellor session helps translate this into specific colleges + branches based on your JOSAA rank.';

  // Ranking list
  const list = document.getElementById('rankList');
  list.innerHTML = '';
  sorted.forEach((row,i)=>{
    const div = document.createElement('div');
    div.className = 'rank-row';
    div.innerHTML = `
      <div class="rank-no">${i+1}</div>
      <div class="rank-name">${branchLabels[row.k]}</div>
      <div class="rank-bar"><div class="fill" style="width:${row.v}%"></div></div>
      <div class="rank-pct">${row.v}%</div>
    `;
    list.appendChild(div);
  });

  // Radar chart
  updateRadar(scores);
}

let radarChart = null;
function updateRadar(scores){
  const ctx = document.getElementById('branchRadar').getContext('2d');
  const labels = ['Electronics','Electrical','Mechanical','CSE','Civil','Chemical','AI/DS'];
  const data = branchKeys.map(k=>scores[k]);
  if(radarChart){
    radarChart.data.datasets[0].data = data;
    radarChart.update();
    return;
  }
  Chart.defaults.font.family = "'Plus Jakarta Sans', sans-serif";
  radarChart = new Chart(ctx, {
    type:'radar',
    data:{
      labels:labels,
      datasets:[{
        label:'Branch Fit (%)',
        data:data,
        backgroundColor:'rgba(255,107,10,.18)',
        borderColor:'#FF6B0A',
        borderWidth:2,
        pointBackgroundColor:'#FF6B0A',
        pointRadius:4
      }]
    },
    options:{
      responsive:true,maintainAspectRatio:false,
      plugins:{legend:{display:false},tooltip:{callbacks:{label:c=>` ${c.label}: ${c.raw}%`}}},
      scales:{
        r:{
          beginAtZero:true,max:100,
          grid:{color:'#E8DFC8'},
          angleLines:{color:'#E8DFC8'},
          pointLabels:{font:{size:11,weight:'500'},color:'#0E1B3D'},
          ticks:{display:false,stepSize:25}
        }
      }
    }
  });
}

// Bind sliders
sliders().forEach(s=>{
  updateSliderFill(s);
  s.addEventListener('input',()=>{ updateSliderFill(s); renderResults(); pushUpdatedScores(); });
});
renderResults();

// Push updated scores to Google Sheet (debounced)
let pushTimer = null;
function pushUpdatedScores(){
  if (!studentData) return;
  if (!GOOGLE_SHEETS_WEBHOOK_URL || GOOGLE_SHEETS_WEBHOOK_URL === "REPLACE_ME") return;
  clearTimeout(pushTimer);
  pushTimer = setTimeout(()=>{
    const sorted = branchKeys.map(k=>({k,v:currentScores[k]})).sort((a,b)=>b.v-a.v);
    const payload = Object.assign({}, studentData, {
      scores: currentScores,
      top_branch: branchLabels[sorted[0].k],
      top_score: sorted[0].v
    });
    fetch(GOOGLE_SHEETS_WEBHOOK_URL,{
      method:'POST', mode:'no-cors',
      headers:{'Content-Type':'text/plain'},
      body: JSON.stringify(payload)
    }).catch(()=>{});
  }, 1500);
}

/* PDF REPORT GENERATION */
document.getElementById('downloadPdf').addEventListener('click', generatePDF);

async function generatePDF(){
  if (!currentScores){
    alert('Please move at least one slider in the assessment first.');
    return;
  }
  if (!studentData){
    alert('Please fill in the student information form first.');
    document.getElementById('student-info').scrollIntoView({behavior:'smooth'});
    return;
  }

  const { jsPDF } = window.jspdf;
  const doc = new jsPDF({unit:'mm',format:'a4'});
  const pageW = 210, pageH = 297;
  const NAVY = [14,58,138], NAVY_INK = [7,26,68], ORANGE = [255,107,10],
        CREAM = [251,247,238], MUTED = [90,98,120], INK = [14,27,61];

  // --- HEADER BAR ---
  doc.setFillColor(...NAVY_INK);
  doc.rect(0, 0, pageW, 38, 'F');

  // Brand mark (simple cube placeholder, since image may not be loadable in jsPDF without conversion)
  doc.setFillColor(...ORANGE);
  doc.rect(15, 11, 16, 16, 'F');
  doc.setFillColor(...NAVY);
  doc.rect(19, 7, 16, 16, 'F');

  // Brand text
  doc.setFont('helvetica','bold');
  doc.setFontSize(20);
  doc.setTextColor(255,255,255);
  doc.text('Edu', 42, 18);
  doc.setTextColor(...ORANGE);
  doc.text('Aakashaa', 56, 18);
  doc.setFont('helvetica','normal');
  doc.setFontSize(8.5);
  doc.setTextColor(255,255,255);
  doc.text('LEARN  ·  GROW  ·  SUCCEED', 42, 24);
  doc.setFontSize(10);
  doc.setTextColor(255,255,255);
  doc.text('Branch-Fit Assessment Report', pageW-15, 18, {align:'right'});
  doc.setFontSize(8.5);
  doc.setTextColor(200,200,200);
  const today = new Date().toLocaleDateString('en-IN', {year:'numeric',month:'long',day:'numeric'});
  doc.text(today, pageW-15, 24, {align:'right'});

  // --- TITLE ---
  doc.setTextColor(...NAVY_INK);
  doc.setFont('helvetica','bold');
  doc.setFontSize(22);
  doc.text('Personalised Branch-Fit Report', 15, 55);
  doc.setFont('helvetica','normal');
  doc.setFontSize(11);
  doc.setTextColor(...MUTED);
  doc.text('Based on the EduAakashaa 15-question cross-branch assessment.', 15, 62);

  // Orange accent line
  doc.setDrawColor(...ORANGE);
  doc.setLineWidth(0.8);
  doc.line(15, 66, 35, 66);

  // --- STUDENT INFO ---
  let y = 78;
  doc.setFont('helvetica','bold');
  doc.setFontSize(11);
  doc.setTextColor(...NAVY);
  doc.text('STUDENT INFORMATION', 15, y);
  y += 5;
  doc.setDrawColor(232,223,200);
  doc.line(15, y, pageW-15, y);
  y += 6;

  const infoPairs = [
    ['Name', studentData.name || '—'],
    ['Email', studentData.email || '—'],
    ['Mobile', studentData.phone || '—'],
    ['Class', studentData.class || '—'],
    ['Board', studentData.board || '—'],
    ['Target Exam', studentData.target_exam || '—'],
    ['Expected Rank', studentData.jee_rank || '—'],
    ['City', studentData.city || '—'],
    ['Parent Name', studentData.parent_name || '—'],
    ['Parent Mobile', studentData.parent_phone || '—']
  ];

  doc.setFont('helvetica','normal');
  doc.setFontSize(10);
  for (let i=0; i<infoPairs.length; i+=2){
    const left = infoPairs[i], right = infoPairs[i+1];
    doc.setTextColor(...MUTED);
    doc.setFontSize(8.5);
    doc.text(left[0].toUpperCase(), 15, y);
    if (right) doc.text(right[0].toUpperCase(), 110, y);
    doc.setTextColor(...INK);
    doc.setFontSize(10.5);
    doc.text(String(left[1]).substring(0,45), 15, y+5);
    if (right) doc.text(String(right[1]).substring(0,45), 110, y+5);
    y += 11;
  }

  if (studentData.notes){
    y += 2;
    doc.setTextColor(...MUTED);
    doc.setFontSize(8.5);
    doc.text('NOTES', 15, y);
    y += 5;
    doc.setTextColor(...INK);
    doc.setFontSize(10.5);
    const noteLines = doc.splitTextToSize(studentData.notes, pageW-30);
    doc.text(noteLines, 15, y);
    y += noteLines.length * 5 + 4;
  }

  // --- ASSESSMENT RESULTS ---
  y += 4;
  doc.setFont('helvetica','bold');
  doc.setFontSize(11);
  doc.setTextColor(...NAVY);
  doc.text('BRANCH-FIT RANKING', 15, y);
  y += 5;
  doc.setDrawColor(232,223,200);
  doc.line(15, y, pageW-15, y);
  y += 8;

  const sorted = branchKeys.map(k=>({k,v:currentScores[k]})).sort((a,b)=>b.v-a.v);

  // Top recommendation box
  doc.setFillColor(255,247,238);
  doc.setDrawColor(...ORANGE);
  doc.setLineWidth(0.5);
  doc.roundedRect(15, y, pageW-30, 24, 3, 3, 'FD');
  doc.setTextColor(...MUTED);
  doc.setFontSize(8);
  doc.text('TOP RECOMMENDATION', 22, y+7);
  doc.setTextColor(...NAVY_INK);
  doc.setFont('helvetica','bold');
  doc.setFontSize(14);
  doc.text(branchLabels[sorted[0].k], 22, y+15);
  doc.setTextColor(...ORANGE);
  doc.setFontSize(22);
  doc.text(sorted[0].v + '%', pageW-22, y+17, {align:'right'});
  y += 30;

  // Full ranking table
  doc.autoTable({
    startY: y,
    head: [['Rank', 'Branch Family', 'Fit %', 'Read More']],
    body: sorted.map((row,i)=>[
      String(i+1),
      branchLabels[row.k],
      row.v + '%',
      'eduaakashaa.in'
    ]),
    theme:'grid',
    headStyles:{fillColor:NAVY_INK, textColor:[255,255,255], font:'helvetica', fontStyle:'bold', fontSize:9.5},
    bodyStyles:{font:'helvetica', fontSize:10, textColor:INK},
    alternateRowStyles:{fillColor:CREAM},
    margin:{left:15, right:15},
    columnStyles:{
      0:{cellWidth:18, halign:'center', fontStyle:'bold'},
      1:{cellWidth:95},
      2:{cellWidth:25, halign:'right', fontStyle:'bold', textColor:ORANGE},
      3:{cellWidth:42, fontSize:8.5, textColor:MUTED}
    }
  });

  y = doc.lastAutoTable.finalY + 12;

  // New page if needed
  if (y > 245){
    doc.addPage();
    y = 25;
  }

  // --- RECOMMENDATION TEXT ---
  doc.setFont('helvetica','bold');
  doc.setFontSize(11);
  doc.setTextColor(...NAVY);
  doc.text('WHAT THIS MEANS', 15, y);
  y += 5;
  doc.setDrawColor(232,223,200);
  doc.line(15, y, pageW-15, y);
  y += 7;

  doc.setFont('helvetica','normal');
  doc.setFontSize(10);
  doc.setTextColor(...INK);
  const reco =
    'Your strongest branch alignment is ' + branchLabels[sorted[0].k] + ' at ' + sorted[0].v + '% fit. ' +
    'Strong alternatives are ' + branchLabels[sorted[1].k] + ' (' + sorted[1].v + '%) and ' +
    branchLabels[sorted[2].k] + ' (' + sorted[2].v + '%). ' +
    'These rankings combine your responses on math, physics, chemistry, coding, hands-on aptitude, 3D visualisation, ' +
    'field-readiness, PSU preference, AI/research curiosity and adaptability. ' +
    '\n\nNext step: book a 45-minute counselling session with EduAakashaa to translate this into specific ' +
    'colleges + branches based on your actual JOSAA / TNEA / DASA rank. We will produce a written branch plan ' +
    'with rank ladder, internship strategy and a 4-year roadmap.';
  const recoLines = doc.splitTextToSize(reco, pageW-30);
  doc.text(recoLines, 15, y);
  y += recoLines.length * 5 + 6;

  // --- NEXT STEPS BOX ---
  if (y > 240){ doc.addPage(); y = 25; }
  doc.setFillColor(...NAVY_INK);
  doc.roundedRect(15, y, pageW-30, 36, 3, 3, 'F');
  doc.setTextColor(...ORANGE);
  doc.setFont('helvetica','bold');
  doc.setFontSize(9);
  doc.text('NEXT STEP · BOOK YOUR COUNSELLING SESSION', 22, y+8);
  doc.setTextColor(255,255,255);
  doc.setFont('helvetica','bold');
  doc.setFontSize(14);
  doc.text('Right college. Right branch. Right future.', 22, y+18);
  doc.setFont('helvetica','normal');
  doc.setFontSize(10);
  doc.setTextColor(220,220,220);
  doc.text('45 mins · 1-on-1 · written branch plan + rank ladder', 22, y+26);
  doc.setTextColor(...ORANGE);
  doc.setFontSize(10);
  doc.setFont('helvetica','bold');
  doc.text('+91 80157 22706  ·  +971 50 516 8081', 22, y+33);

  // --- FOOTER ---
  const totalPages = doc.internal.getNumberOfPages();
  for (let p=1; p<=totalPages; p++){
    doc.setPage(p);
    doc.setFillColor(...CREAM);
    doc.rect(0, pageH-16, pageW, 16, 'F');
    doc.setDrawColor(232,223,200);
    doc.line(0, pageH-16, pageW, pageH-16);
    doc.setFont('helvetica','normal');
    doc.setFontSize(7.5);
    doc.setTextColor(...MUTED);
    doc.text('EduAakashaa  ·  www.eduaakashaa.in  ·  info@eduaakashaa.com', 15, pageH-9);
    doc.text('Coimbatore, Tamil Nadu  ·  Dubai, UAE', 15, pageH-5);
    doc.setTextColor(...NAVY);
    doc.setFont('helvetica','bold');
    doc.text('Page '+p+' of '+totalPages, pageW-15, pageH-7, {align:'right'});
  }

  const safeName = (studentData.name || 'student').replace(/[^a-z0-9]/gi,'_').toLowerCase();
  doc.save('eduaakashaa_branch_fit_' + safeName + '.pdf');
}

/* ============================================================
   SKILLS, SUBJECTS, JOBS, INDIA MAP, COMPANIES
   ============================================================ */
const branchLabelsShort={electronics:'ECE',electrical:'EEE',mechanical:'MECH',cse:'CSE',civil:'CIVIL',chemical:'CHEM',ai_ds:'AI/DS'};
const branchLabelsFull={electronics:'Electronics',electrical:'Electrical',mechanical:'Mechanical',cse:'Computer Sci.',civil:'Civil',chemical:'Chemical',ai_ds:'AI & Data Science'};
const skillsByBranch={
  electronics:['Math & Physics foundation','Digital + analog circuits','Programming (C / Py / Verilog)','Hands-on prototyping','Systems thinking','Signal & wave intuition'],
  electrical:['Strong Math','Electromagnetism','Circuit + system thinking','MATLAB / PLC programming','Lab discipline','Field readiness'],
  mechanical:['3D visualisation','Math + Physics','CAD / CAE software','Hands-on workshop','Project coordination','Field readiness'],
  cse:['Algorithmic thinking','Math + Probability','Self-directed coding','Continuous learning','Communication','Project portfolio'],
  civil:['Spatial reasoning','Math + Physics','CAD / BIM / GIS','Site readiness','Coordination skills','Sustainability literacy'],
  chemical:['Chemistry (all branches)','Mass & energy balance','Math comfort','Lab discipline','ASPEN / MATLAB sim','Safety mindset'],
  ai_ds:['Heavy math + stats','Python + PyTorch','Research paper reading','Project portfolio','Communication','Adapt to fast change']
};
function renderSkillsRow(){
  const row=document.getElementById('skillsRow');if(!row)return;
  let h='';['electronics','electrical','mechanical','cse','civil','chemical','ai_ds'].forEach(br=>{
    h+=`<div class="skill-card"><div class="sc-branch">${branchLabelsFull[br]}</div><h4>Skills you'll build</h4><ul class="sk-list">${skillsByBranch[br].map(s=>`<li>${s}</li>`).join('')}</ul></div>`;
  });row.innerHTML=h;
}

// SUBJECTS DATA — map = 7 chars [ECE,EEE,MECH,CSE,CIVIL,CHEM,AI/DS], C=Core E=Elective -=N/A
const subjectsData=[
  {cat:'F',name:'Engineering Mathematics I (Calc, LA)',map:'CCCCCCC',fut:false},
  {cat:'F',name:'Engineering Mathematics II (DE, Prob, Stats)',map:'CCCCCCC',fut:false},
  {cat:'F',name:'Engineering Physics',map:'CCCCCCC',fut:false},
  {cat:'F',name:'Engineering Chemistry',map:'CCCCCCE',fut:false},
  {cat:'F',name:'Programming Fundamentals (C / Python)',map:'CCCCCCC',fut:false},
  {cat:'F',name:'Engineering Graphics / CAD',map:'CCCCCE-',fut:false},
  {cat:'F',name:'Communication / Technical Writing',map:'CCCCCCC',fut:false},
  {cat:'X',name:'Engineering Mechanics',map:'ECC-CE-',fut:false},
  {cat:'X',name:'Digital Logic & Electronics',map:'CCEC--E',fut:false},
  {cat:'X',name:'Probability, Statistics & Data',map:'EEECECC',fut:false},
  {cat:'X',name:'Numerical Methods & Computing',map:'CCCEECC',fut:false},
  {cat:'X',name:'Material Science / Engg Materials',map:'EEC-CC-',fut:false},
  {cat:'X',name:'Linear Algebra (Advanced)',map:'EEEC-EC',fut:false},
  {cat:'B',name:'Electric Circuits & Networks',map:'CC-E---',fut:false},
  {cat:'B',name:'Signals & Systems',map:'CC----E',fut:false},
  {cat:'B',name:'Communication Systems',map:'CE-E---',fut:false},
  {cat:'B',name:'Microprocessors & Embedded Systems',map:'CCEC--E',fut:false},
  {cat:'B',name:'VLSI Design & Verification',map:'CE-E--E',fut:false},
  {cat:'B',name:'Power Systems',map:'-C-----',fut:false},
  {cat:'B',name:'Power Electronics',map:'EC-----',fut:false},
  {cat:'B',name:'Electrical Machines',map:'ECE----',fut:false},
  {cat:'B',name:'Control Systems',map:'CCC--CE',fut:false},
  {cat:'B',name:'Thermodynamics',map:'--C-EC-',fut:false},
  {cat:'B',name:'Fluid Mechanics',map:'--C-CC-',fut:false},
  {cat:'B',name:'Heat & Mass Transfer',map:'--C-EC-',fut:false},
  {cat:'B',name:'Strength of Materials',map:'--C-CE-',fut:false},
  {cat:'B',name:'Manufacturing Processes',map:'EEC--E-',fut:false},
  {cat:'B',name:'Machine Design',map:'--C----',fut:false},
  {cat:'B',name:'Structural Analysis',map:'--E-C--',fut:false},
  {cat:'B',name:'Surveying & GIS',map:'----C--',fut:false},
  {cat:'B',name:'Geotechnical Engineering',map:'----C--',fut:false},
  {cat:'B',name:'Transportation Engineering',map:'----C--',fut:false},
  {cat:'B',name:'Hydraulics & Water Resources',map:'--E-CE-',fut:false},
  {cat:'B',name:'Concrete Technology',map:'----CE-',fut:false},
  {cat:'B',name:'Chemical Reaction Engineering',map:'-----C-',fut:false},
  {cat:'B',name:'Mass Transfer Operations',map:'-----C-',fut:false},
  {cat:'B',name:'Process Control & Instrumentation',map:'ECE--C-',fut:false},
  {cat:'B',name:'Plant Design & Economics',map:'--E--C-',fut:false},
  {cat:'B',name:'Polymer & Materials Chemistry',map:'--E--C-',fut:false},
  {cat:'B',name:'Data Structures & Algorithms',map:'CEEC--C',fut:false},
  {cat:'B',name:'Operating Systems',map:'EE-C--C',fut:false},
  {cat:'B',name:'Database Systems',map:'EEECEEC',fut:false},
  {cat:'B',name:'Computer Networks',map:'CE-C--E',fut:false},
  {cat:'B',name:'Theory of Computation',map:'---C--E',fut:false},
  {cat:'B',name:'Software Engineering',map:'EEECEEE',fut:false},
  {cat:'B',name:'Machine Learning Fundamentals',map:'EEEC-EC',fut:false},
  {cat:'B',name:'Deep Learning & Neural Networks',map:'EEEE-EC',fut:false},
  {cat:'B',name:'Computer Vision',map:'EE-E--C',fut:false},
  {cat:'B',name:'Natural Language Processing',map:'---E--C',fut:false},
  {cat:'B',name:'Reinforcement Learning',map:'---E--C',fut:false},
  {cat:'B',name:'Quantum Computing & Q-Algorithms',map:'EEEE-EE',fut:true},
  {cat:'B',name:'Robotics & Autonomous Systems',map:'EECE-EE',fut:true},
  {cat:'B',name:'IoT & Embedded AI',map:'CEEEEEE',fut:true},
  {cat:'B',name:'Renewable Energy & Green Hydrogen',map:'-CE-EC-',fut:true},
  {cat:'B',name:'Smart Materials / Nanotech',map:'E-C-EC-',fut:true},
  {cat:'B',name:'Cybersecurity & Cryptography',map:'E--C--C',fut:true},
  {cat:'B',name:'Sustainability & Net-Zero Engg',map:'EEEECCE',fut:true},
  {cat:'B',name:'Bioinformatics & Bio-AI',map:'---E-CC',fut:true},
  {cat:'B',name:'AR / VR / Spatial Computing',map:'E-EEE-E',fut:true},
  {cat:'B',name:'Blockchain & Web3 Engineering',map:'---E--E',fut:true},
  {cat:'B',name:'Drone / UAV Engineering',map:'EECEE-E',fut:true},
  {cat:'B',name:'Edge AI / Embedded ML',map:'CE-E--C',fut:true},
  {cat:'B',name:'5G / 6G & Next-Gen Comms',map:'CE-E---',fut:true},
  {cat:'B',name:'Carbon Capture & Climate Tech',map:'-EE-EC-',fut:true},
  {cat:'B',name:'EV Powertrains & Battery Tech',map:'ECC--E-',fut:true}
];
function renderSubjectsMatrix(filter){
  const tbody=document.getElementById('subjectsBody');if(!tbody)return;
  filter=filter||'all';
  const groups={F:'Foundation — Core for almost every branch',X:'Cross-Core — Shared across multiple branches',B:'Branch-Specific Core',FUT:'★ Futuristic / In-demand Electives for 2030'};
  const buckets=[
    {key:'F',items:subjectsData.filter(s=>s.cat==='F'&&!s.fut)},
    {key:'X',items:subjectsData.filter(s=>s.cat==='X'&&!s.fut)},
    {key:'B',items:subjectsData.filter(s=>s.cat==='B'&&!s.fut)},
    {key:'FUT',items:subjectsData.filter(s=>s.fut)}
  ];
  let html='';
  buckets.forEach(g=>{
    let visible=g.items;
    if(filter==='F'&&g.key!=='F')return;
    if(filter==='X'&&g.key!=='X')return;
    if(filter==='B'&&g.key!=='B')return;
    if(filter==='FUT'&&g.key!=='FUT')return;
    if(filter==='COMMON'){visible=g.items.filter(s=>(s.map.match(/C/g)||[]).length>=4);if(visible.length===0)return;}
    if(visible.length===0)return;
    html+=`<tr class="cat-row"><td colspan="8">${groups[g.key]} · ${visible.length} subject${visible.length>1?'s':''}</td></tr>`;
    visible.forEach(s=>{
      const isCommon=(s.map.match(/C/g)||[]).length>=4;
      const cells=s.map.split('').map(c=>{
        if(c==='C')return `<td><span class="cell-core${isCommon?' cell-common':''}">C</span></td>`;
        if(c==='E')return `<td><span class="cell-elec">E</span></td>`;
        return `<td><span class="cell-na">—</span></td>`;
      }).join('');
      const futBadge=s.fut?`<span class="fut">FUT</span>`:'';
      html+=`<tr><td>${s.name}${futBadge}</td>${cells}</tr>`;
    });
  });
  if(!html)html='<tr><td colspan="8" style="text-align:center;padding:30px;color:var(--muted)">No subjects match this filter. Try another.</td></tr>';
  tbody.innerHTML=html;
}
document.querySelectorAll('[data-subj-filter]').forEach(btn=>{
  btn.addEventListener('click',()=>{
    document.querySelectorAll('[data-subj-filter]').forEach(b=>b.classList.remove('active'));
    btn.classList.add('active');
    renderSubjectsMatrix(btn.dataset.subjFilter);
  });
});

// TOP 100 JOBS
const jobsData=[
  {id:1,title:'ML / AI Engineer',branches:['ai_ds','cse','electronics'],salary:'top',govt:false,status:'hot'},
  {id:2,title:'Software Engineer (Product)',branches:['cse','ai_ds','electronics'],salary:'high',govt:false,status:'stable'},
  {id:3,title:'Full-Stack Web Developer',branches:['cse','ai_ds'],salary:'mid',govt:false,status:'stable'},
  {id:4,title:'Backend Engineer',branches:['cse','ai_ds'],salary:'high',govt:false,status:'stable'},
  {id:5,title:'Frontend Engineer',branches:['cse','ai_ds'],salary:'mid',govt:false,status:'stable'},
  {id:6,title:'Mobile App Developer',branches:['cse','ai_ds'],salary:'mid',govt:false,status:'stable'},
  {id:7,title:'DevOps / SRE Engineer',branches:['cse','ai_ds','electronics'],salary:'high',govt:false,status:'hot'},
  {id:8,title:'Cloud Architect',branches:['cse','ai_ds','electronics'],salary:'top',govt:false,status:'hot'},
  {id:9,title:'Cybersecurity Analyst',branches:['cse','ai_ds','electronics'],salary:'high',govt:false,status:'hot'},
  {id:10,title:'Penetration Tester',branches:['cse','electronics'],salary:'high',govt:false,status:'hot'},
  {id:11,title:'Data Scientist',branches:['ai_ds','cse'],salary:'high',govt:false,status:'hot'},
  {id:12,title:'Data Engineer',branches:['ai_ds','cse'],salary:'high',govt:false,status:'hot'},
  {id:13,title:'BI Analyst',branches:['ai_ds','cse','chemical'],salary:'mid',govt:false,status:'stable'},
  {id:14,title:'NLP Engineer',branches:['ai_ds','cse'],salary:'top',govt:false,status:'hot'},
  {id:15,title:'Computer Vision Engineer',branches:['ai_ds','cse','electronics'],salary:'top',govt:false,status:'hot'},
  {id:16,title:'AI Research Scientist',branches:['ai_ds','cse'],salary:'top',govt:false,status:'hot'},
  {id:17,title:'Quant Developer',branches:['cse','ai_ds','electronics'],salary:'top',govt:false,status:'hot'},
  {id:18,title:'Quant Researcher',branches:['ai_ds','cse'],salary:'top',govt:false,status:'hot'},
  {id:19,title:'Blockchain Developer',branches:['cse','ai_ds'],salary:'high',govt:false,status:'stable'},
  {id:20,title:'Game Developer',branches:['cse','ai_ds'],salary:'mid',govt:false,status:'stable'},
  {id:21,title:'AR / VR Developer',branches:['cse','ai_ds','electronics'],salary:'high',govt:false,status:'hot'},
  {id:22,title:'Database Administrator',branches:['cse','ai_ds'],salary:'mid',govt:false,status:'stable'},
  {id:23,title:'QA / Test Automation',branches:['cse','electronics'],salary:'mid',govt:false,status:'stable'},
  {id:24,title:'Solutions / Enterprise Architect',branches:['cse','electronics','ai_ds'],salary:'top',govt:false,status:'stable'},
  {id:25,title:'IT Services Software Engineer',branches:['cse','ai_ds','electronics','electrical','mechanical','civil','chemical'],salary:'low',govt:false,status:'declining'},
  {id:26,title:'VLSI Design Engineer',branches:['electronics','ai_ds'],salary:'top',govt:false,status:'hot'},
  {id:27,title:'Embedded Systems Engineer',branches:['electronics','electrical','cse'],salary:'high',govt:false,status:'hot'},
  {id:28,title:'ASIC Designer',branches:['electronics'],salary:'top',govt:false,status:'hot'},
  {id:29,title:'FPGA Engineer',branches:['electronics','electrical'],salary:'high',govt:false,status:'hot'},
  {id:30,title:'RF / Microwave Engineer',branches:['electronics','electrical'],salary:'high',govt:false,status:'stable'},
  {id:31,title:'Telecom 5G / 6G Engineer',branches:['electronics','electrical'],salary:'high',govt:false,status:'hot'},
  {id:32,title:'Network Engineer',branches:['electronics','cse','electrical'],salary:'mid',govt:false,status:'stable'},
  {id:33,title:'IoT Solutions Engineer',branches:['electronics','electrical','cse'],salary:'high',govt:false,status:'hot'},
  {id:34,title:'Robotics Software Engineer',branches:['electronics','mechanical','ai_ds'],salary:'high',govt:false,status:'hot'},
  {id:35,title:'Avionics Engineer',branches:['electronics','mechanical'],salary:'high',govt:true,status:'hot'},
  {id:36,title:'Semiconductor Fab Engineer',branches:['electronics','chemical'],salary:'high',govt:false,status:'hot'},
  {id:37,title:'PCB / Hardware Designer',branches:['electronics','electrical'],salary:'mid',govt:false,status:'stable'},
  {id:38,title:'Test & Validation Engineer',branches:['electronics','electrical','mechanical'],salary:'mid',govt:false,status:'stable'},
  {id:39,title:'Biomedical Devices Engineer',branches:['electronics','mechanical','chemical'],salary:'high',govt:false,status:'hot'},
  {id:40,title:'EDA Tools Developer',branches:['electronics','cse','ai_ds'],salary:'top',govt:false,status:'hot'},
  {id:41,title:'Power Systems Engineer',branches:['electrical'],salary:'high',govt:true,status:'stable'},
  {id:42,title:'EV Powertrain Engineer',branches:['electrical','mechanical','electronics'],salary:'high',govt:false,status:'hot'},
  {id:43,title:'Renewable Energy Engineer',branches:['electrical','mechanical','chemical'],salary:'high',govt:false,status:'hot'},
  {id:44,title:'Solar PV / Plant Engineer',branches:['electrical','chemical'],salary:'mid',govt:false,status:'hot'},
  {id:45,title:'Wind Turbine Engineer',branches:['electrical','mechanical'],salary:'mid',govt:false,status:'hot'},
  {id:46,title:'Smart Grid Engineer',branches:['electrical','cse','electronics'],salary:'high',govt:false,status:'hot'},
  {id:47,title:'Battery / Energy Storage Engineer',branches:['electrical','chemical','mechanical'],salary:'high',govt:false,status:'hot'},
  {id:48,title:'Power Electronics Engineer',branches:['electrical','electronics'],salary:'high',govt:false,status:'hot'},
  {id:49,title:'Substation / Transmission Engineer',branches:['electrical'],salary:'mid',govt:true,status:'stable'},
  {id:50,title:'Hydropower Engineer',branches:['electrical','civil','mechanical'],salary:'mid',govt:true,status:'stable'},
  {id:51,title:'Design Engineer (CAD)',branches:['mechanical','civil'],salary:'mid',govt:false,status:'stable'},
  {id:52,title:'CAE / FEA Analyst',branches:['mechanical','civil','electronics'],salary:'high',govt:false,status:'stable'},
  {id:53,title:'Production / Plant Engineer',branches:['mechanical','chemical','electrical'],salary:'mid',govt:false,status:'stable'},
  {id:54,title:'Smart Manufacturing Engineer',branches:['mechanical','electrical','electronics'],salary:'high',govt:false,status:'hot'},
  {id:55,title:'Automobile R&D Engineer',branches:['mechanical','electrical'],salary:'high',govt:false,status:'hot'},
  {id:56,title:'Aerospace Engineer',branches:['mechanical','electronics'],salary:'high',govt:true,status:'hot'},
  {id:57,title:'Drone / UAV Engineer',branches:['mechanical','electronics','ai_ds'],salary:'high',govt:false,status:'hot'},
  {id:58,title:'HVAC / Refrigeration Engineer',branches:['mechanical','chemical'],salary:'mid',govt:false,status:'stable'},
  {id:59,title:'Marine / Naval Engineer',branches:['mechanical','electrical'],salary:'high',govt:true,status:'stable'},
  {id:60,title:'Propulsion / Engine Engineer',branches:['mechanical','chemical','electronics'],salary:'high',govt:true,status:'hot'},
  {id:61,title:'Structural Design Engineer',branches:['civil'],salary:'mid',govt:false,status:'stable'},
  {id:62,title:'Construction Project Manager',branches:['civil','mechanical'],salary:'high',govt:false,status:'hot'},
  {id:63,title:'Site / Field Engineer',branches:['civil','mechanical'],salary:'low',govt:false,status:'stable'},
  {id:64,title:'Transportation Planner',branches:['civil'],salary:'mid',govt:true,status:'hot'},
  {id:65,title:'Highway / Bridge Engineer',branches:['civil'],salary:'mid',govt:true,status:'hot'},
  {id:66,title:'Metro / Rail Engineer',branches:['civil','mechanical','electrical'],salary:'high',govt:true,status:'hot'},
  {id:67,title:'Environmental Engineer',branches:['civil','chemical'],salary:'mid',govt:true,status:'hot'},
  {id:68,title:'Water Resources / Hydraulics Engineer',branches:['civil','chemical'],salary:'mid',govt:true,status:'stable'},
  {id:69,title:'Urban Planner / Smart City',branches:['civil'],salary:'mid',govt:true,status:'hot'},
  {id:70,title:'BIM / GIS / Survey Engineer',branches:['civil','cse'],salary:'mid',govt:false,status:'hot'},
  {id:71,title:'Process Engineer',branches:['chemical'],salary:'high',govt:false,status:'hot'},
  {id:72,title:'Plant Operator / Operations',branches:['chemical','electrical'],salary:'mid',govt:false,status:'stable'},
  {id:73,title:'Petroleum / Drilling Engineer',branches:['chemical','mechanical'],salary:'top',govt:true,status:'stable'},
  {id:74,title:'Refinery Engineer',branches:['chemical','mechanical'],salary:'high',govt:true,status:'stable'},
  {id:75,title:'Pharma Production Engineer',branches:['chemical'],salary:'high',govt:false,status:'hot'},
  {id:76,title:'R&D Chemist / Formulation',branches:['chemical','ai_ds'],salary:'high',govt:false,status:'hot'},
  {id:77,title:'Polymer / Materials Engineer',branches:['chemical','mechanical'],salary:'mid',govt:false,status:'hot'},
  {id:78,title:'Food Process Engineer',branches:['chemical'],salary:'mid',govt:false,status:'stable'},
  {id:79,title:'Environmental Compliance Engineer',branches:['chemical','civil'],salary:'mid',govt:true,status:'hot'},
  {id:80,title:'Biotech / Bioprocess Engineer',branches:['chemical','ai_ds'],salary:'high',govt:false,status:'hot'},
  {id:81,title:'Product Manager (Tech)',branches:['cse','ai_ds','electronics','electrical','mechanical','civil','chemical'],salary:'top',govt:false,status:'hot'},
  {id:82,title:'Engineering Manager',branches:['cse','ai_ds','electronics','electrical','mechanical','civil','chemical'],salary:'top',govt:false,status:'stable'},
  {id:83,title:'Technical Program Manager',branches:['cse','ai_ds','electronics','mechanical'],salary:'top',govt:false,status:'hot'},
  {id:84,title:'UX / UI Designer',branches:['cse','ai_ds','mechanical'],salary:'mid',govt:false,status:'hot'},
  {id:85,title:'Management Consultant (Tech)',branches:['cse','ai_ds','electronics','electrical','mechanical','civil','chemical'],salary:'top',govt:false,status:'hot'},
  {id:86,title:'Investment Banking Analyst',branches:['cse','ai_ds','mechanical','electrical','chemical'],salary:'top',govt:false,status:'stable'},
  {id:87,title:'Tech Entrepreneur / Founder',branches:['cse','ai_ds','electronics','electrical','mechanical','civil','chemical'],salary:'top',govt:false,status:'hot'},
  {id:88,title:'Patent / IP Engineer',branches:['cse','electronics','chemical','mechanical'],salary:'high',govt:false,status:'stable'},
  {id:89,title:'Technical Writer / Documentation',branches:['cse','electronics','mechanical','electrical','civil','chemical','ai_ds'],salary:'mid',govt:false,status:'stable'},
  {id:90,title:'Sales / Application Engineer',branches:['mechanical','electrical','chemical','electronics'],salary:'mid',govt:false,status:'stable'},
  {id:91,title:'IES Officer (Engg Services)',branches:['civil','mechanical','electrical','electronics'],salary:'high',govt:true,status:'stable'},
  {id:92,title:'ISRO Scientist',branches:['electronics','mechanical','electrical','cse','ai_ds'],salary:'high',govt:true,status:'hot'},
  {id:93,title:'DRDO Scientist',branches:['electronics','mechanical','chemical','cse','ai_ds'],salary:'high',govt:true,status:'hot'},
  {id:94,title:'BARC / Nuclear Engineer',branches:['electrical','mechanical','chemical','electronics'],salary:'high',govt:true,status:'stable'},
  {id:95,title:'NTPC / Power PSU Engineer',branches:['electrical','mechanical'],salary:'high',govt:true,status:'stable'},
  {id:96,title:'Power Grid Corp Engineer',branches:['electrical'],salary:'high',govt:true,status:'hot'},
  {id:97,title:'ONGC / IOCL / GAIL Engineer',branches:['chemical','mechanical','electrical'],salary:'high',govt:true,status:'stable'},
  {id:98,title:'Indian Railways (IRSE / SSE)',branches:['civil','mechanical','electrical','electronics'],salary:'mid',govt:true,status:'stable'},
  {id:99,title:'Defence Tech Officer (Navy / Air Force)',branches:['mechanical','electrical','electronics','civil'],salary:'high',govt:true,status:'stable'},
  {id:100,title:'IAS / IPS via UPSC',branches:['cse','ai_ds','electronics','electrical','mechanical','civil','chemical'],salary:'top',govt:true,status:'stable'}
];
let jobFilters={branch:'all',salary:'all',type:'all',status:'all'};
function renderJobsTable(){
  const tbody=document.getElementById('jobsBody');if(!tbody)return;
  const filtered=jobsData.filter(j=>{
    if(jobFilters.branch!=='all'&&!j.branches.includes(jobFilters.branch))return false;
    if(jobFilters.salary!=='all'&&j.salary!==jobFilters.salary)return false;
    if(jobFilters.type==='govt'&&!j.govt)return false;
    if(jobFilters.type==='private'&&j.govt)return false;
    if(jobFilters.status!=='all'&&j.status!==jobFilters.status)return false;
    return true;
  });
  let html='';
  filtered.forEach(j=>{
    const multiClass=j.branches.length>=4?' multi':'';
    const branchTags=j.branches.slice(0,4).map(b=>`<span class="br-dot${multiClass}">${branchLabelsShort[b]}</span>`).join('');
    const moreTag=j.branches.length>4?`<span class="br-dot multi">+${j.branches.length-4}</span>`:'';
    const sal={top:'TOP ₹25L+',high:'HIGH ₹12-25L',mid:'MID ₹6-12L',low:'LOW ₹3-6L'}[j.salary];
    const status={hot:'🔥 HOT',stable:'STABLE',declining:'DECLINING'}[j.status];
    html+=`<tr><td>${j.id}</td><td><div class="job-title">${j.title}</div></td><td><div class="br-dots">${branchTags}${moreTag}</div></td><td><span class="salary-badge salary-${j.salary}">${sal}</span></td><td>${j.govt?'<span class="govt-flag">GOVT</span>':'<span class="priv-flag">PRIVATE</span>'}</td><td><span class="status-tag status-${j.status}">${status}</span></td></tr>`;
  });
  if(filtered.length===0)html='<tr><td colspan="6" style="text-align:center;padding:40px;color:var(--muted);font-style:italic">No jobs match the current filter combination. Try removing some filters.</td></tr>';
  tbody.innerHTML=html;
}
['data-job-branch','data-job-salary','data-job-type','data-job-status'].forEach(attr=>{
  document.querySelectorAll(`[${attr}]`).forEach(btn=>{
    btn.addEventListener('click',()=>{
      const key=attr.replace('data-job-','');
      if(btn.classList.contains('active')&&(key==='type'||key==='status')){btn.classList.remove('active');jobFilters[key]='all';}
      else{document.querySelectorAll(`[${attr}]`).forEach(b=>b.classList.remove('active'));btn.classList.add('active');jobFilters[key]=btn.getAttribute(attr);}
      renderJobsTable();
    });
  });
});

// TOP 100 COMPANIES
const companies=[
  {n:'ISRO',init:'IS',color:'#003F87',sector:'govt',city:'Bengaluru'},
  {n:'DRDO',init:'DR',color:'#1F4E79',sector:'govt',city:'Hyderabad'},
  {n:'BARC',init:'BA',color:'#0E3A8A',sector:'govt',city:'Mumbai'},
  {n:'HAL',init:'HL',color:'#005EA8',sector:'govt',city:'Bengaluru'},
  {n:'BEL',init:'BE',color:'#0066B3',sector:'govt',city:'Bengaluru'},
  {n:'NTPC',init:'NT',color:'#002F6C',sector:'govt',city:'Delhi NCR'},
  {n:'Power Grid Corp',init:'PG',color:'#E67E22',sector:'govt',city:'Delhi NCR'},
  {n:'ONGC',init:'ON',color:'#E63946',sector:'govt',city:'Delhi NCR'},
  {n:'IOCL',init:'IO',color:'#F37021',sector:'govt',city:'Delhi NCR'},
  {n:'BPCL',init:'BP',color:'#E10000',sector:'govt',city:'Mumbai'},
  {n:'GAIL',init:'GA',color:'#005EA8',sector:'govt',city:'Delhi NCR'},
  {n:'Indian Railways',init:'IR',color:'#1B4F8E',sector:'govt',city:'Delhi NCR'},
  {n:'NHPC',init:'NH',color:'#3470B5',sector:'govt',city:'Delhi NCR'},
  {n:'SAIL',init:'SA',color:'#2E7D32',sector:'govt',city:'Delhi NCR'},
  {n:'Coal India',init:'CI',color:'#1A1A1A',sector:'govt',city:'Kolkata'},
  {n:'BHEL',init:'BH',color:'#0F2C59',sector:'govt',city:'Delhi NCR'},
  {n:'NMDC',init:'NM',color:'#0A4D8C',sector:'mining',city:'Hyderabad'},
  {n:'Bharat Dynamics',init:'BD',color:'#2C3E50',sector:'govt',city:'Hyderabad'},
  {n:'ECIL',init:'EC',color:'#125B96',sector:'govt',city:'Hyderabad'},
  {n:'NPCIL',init:'NP',color:'#1E5A8D',sector:'govt',city:'Mumbai'},
  {n:'TCS',init:'TC',color:'#1C3D6B',sector:'it',city:'Mumbai'},
  {n:'Infosys',init:'IN',color:'#007CC3',sector:'it',city:'Bengaluru'},
  {n:'Wipro',init:'WI',color:'#341B6E',sector:'it',city:'Bengaluru'},
  {n:'HCL Tech',init:'HC',color:'#021A40',sector:'it',city:'Delhi NCR'},
  {n:'Tech Mahindra',init:'TM',color:'#E2231A',sector:'it',city:'Pune'},
  {n:'Cognizant',init:'CG',color:'#1F44CB',sector:'it',city:'Chennai'},
  {n:'LTIMindtree',init:'LT',color:'#0046AD',sector:'it',city:'Mumbai'},
  {n:'Mphasis',init:'MP',color:'#7B2D8E',sector:'it',city:'Bengaluru'},
  {n:'Persistent Systems',init:'PE',color:'#00ABE0',sector:'it',city:'Pune'},
  {n:'Coforge',init:'CF',color:'#FF6900',sector:'it',city:'Delhi NCR'},
  {n:'Mindtree',init:'MT',color:'#FF6900',sector:'it',city:'Bengaluru'},
  {n:'Capgemini',init:'CP',color:'#0070AD',sector:'it',city:'Mumbai'},
  {n:'Accenture',init:'AC',color:'#A100FF',sector:'it',city:'Bengaluru'},
  {n:'Microsoft India',init:'MS',color:'#0078D4',sector:'it',city:'Hyderabad'},
  {n:'Google India',init:'GO',color:'#EA4335',sector:'it',city:'Bengaluru'},
  {n:'Amazon India',init:'AM',color:'#FF9900',sector:'it',city:'Bengaluru'},
  {n:'Meta India',init:'ME',color:'#1877F2',sector:'it',city:'Bengaluru'},
  {n:'Salesforce',init:'SF',color:'#00A1E0',sector:'it',city:'Hyderabad'},
  {n:'SAP Labs',init:'SP',color:'#0FAAFF',sector:'it',city:'Bengaluru'},
  {n:'Adobe India',init:'AD',color:'#FA0F00',sector:'it',city:'Bengaluru'},
  {n:'Flipkart',init:'FK',color:'#2874F0',sector:'startups',city:'Bengaluru'},
  {n:'Razorpay',init:'RP',color:'#0C2451',sector:'startups',city:'Bengaluru'},
  {n:'Swiggy',init:'SW',color:'#FC8019',sector:'startups',city:'Bengaluru'},
  {n:'Zomato',init:'ZO',color:'#E23744',sector:'startups',city:'Delhi NCR'},
  {n:'CRED',init:'CR',color:'#1B1B1B',sector:'startups',city:'Bengaluru'},
  {n:'Zerodha',init:'ZE',color:'#387ED1',sector:'startups',city:'Bengaluru'},
  {n:'PhonePe',init:'PP',color:'#5F259F',sector:'startups',city:'Bengaluru'},
  {n:'Paytm',init:'PT',color:'#00B9F1',sector:'startups',city:'Delhi NCR'},
  {n:'Postman',init:'PM',color:'#FF6C37',sector:'startups',city:'Bengaluru'},
  {n:'Sarvam AI',init:'SR',color:'#FF6B0A',sector:'startups',city:'Bengaluru'},
  {n:'Tata Motors',init:'TT',color:'#003366',sector:'manufacturing',city:'Pune'},
  {n:'Mahindra & Mahindra',init:'MA',color:'#C8102E',sector:'manufacturing',city:'Mumbai'},
  {n:'Maruti Suzuki',init:'MZ',color:'#005CB9',sector:'manufacturing',city:'Delhi NCR'},
  {n:'Hyundai India',init:'HY',color:'#002C5F',sector:'manufacturing',city:'Chennai'},
  {n:'Bajaj Auto',init:'BJ',color:'#0070BA',sector:'manufacturing',city:'Pune'},
  {n:'TVS Motor',init:'TV',color:'#003478',sector:'manufacturing',city:'Chennai'},
  {n:'Hero MotoCorp',init:'HE',color:'#E1261C',sector:'manufacturing',city:'Delhi NCR'},
  {n:'Bosch India',init:'BO',color:'#ED1C24',sector:'manufacturing',city:'Bengaluru'},
  {n:'Siemens India',init:'SI',color:'#009999',sector:'manufacturing',city:'Mumbai'},
  {n:'ABB India',init:'AB',color:'#FF0000',sector:'manufacturing',city:'Bengaluru'},
  {n:'L&T',init:'LN',color:'#00A19A',sector:'heavy',city:'Mumbai'},
  {n:'Reliance Industries',init:'RI',color:'#0066B3',sector:'oil',city:'Mumbai'},
  {n:'Adani Group',init:'AG',color:'#0070C0',sector:'heavy',city:'Ahmedabad'},
  {n:'Tata Steel',init:'TS',color:'#1F3864',sector:'heavy',city:'Jamshedpur'},
  {n:'JSW Steel',init:'JS',color:'#005EB8',sector:'heavy',city:'Mumbai'},
  {n:'Vedanta',init:'VD',color:'#C8102E',sector:'mining',city:'Mumbai'},
  {n:'Hindalco',init:'HI',color:'#003B71',sector:'heavy',city:'Mumbai'},
  {n:'Thermax',init:'TX',color:'#E63946',sector:'heavy',city:'Pune'},
  {n:'Cummins India',init:'CM',color:'#C8102E',sector:'manufacturing',city:'Pune'},
  {n:'Honeywell India',init:'HN',color:'#E10000',sector:'manufacturing',city:'Bengaluru'},
  {n:'Sun Pharma',init:'SU',color:'#F47B20',sector:'pharma',city:'Mumbai'},
  {n:'Cipla',init:'CL',color:'#00529E',sector:'pharma',city:'Mumbai'},
  {n:"Dr Reddy's Labs",init:'DR',color:'#00558C',sector:'pharma',city:'Hyderabad'},
  {n:'Lupin',init:'LU',color:'#A50034',sector:'pharma',city:'Mumbai'},
  {n:'Aurobindo Pharma',init:'AU',color:'#1B5E94',sector:'pharma',city:'Hyderabad'},
  {n:'Biocon',init:'BC',color:'#56A8B5',sector:'pharma',city:'Bengaluru'},
  {n:'Serum Institute',init:'SE',color:'#00529E',sector:'pharma',city:'Pune'},
  {n:'Bharat Biotech',init:'BB',color:'#0070C0',sector:'pharma',city:'Hyderabad'},
  {n:'Glenmark',init:'GL',color:'#005EB8',sector:'pharma',city:'Mumbai'},
  {n:'Aarti Industries',init:'AA',color:'#0066B3',sector:'oil',city:'Mumbai'},
  {n:'SRF',init:'SF',color:'#003366',sector:'oil',city:'Delhi NCR'},
  {n:'PI Industries',init:'PI',color:'#E63946',sector:'oil',city:'Delhi NCR'},
  {n:'Atul Ltd',init:'AT',color:'#1B4F8E',sector:'oil',city:'Ahmedabad'},
  {n:'Deepak Nitrite',init:'DN',color:'#005EB8',sector:'oil',city:'Mumbai'},
  {n:'Vinati Organics',init:'VO',color:'#0F4C81',sector:'oil',city:'Mumbai'},
  {n:'Tata Power',init:'TP',color:'#003366',sector:'energy',city:'Mumbai'},
  {n:'Adani Green',init:'AN',color:'#2E8B57',sector:'energy',city:'Ahmedabad'},
  {n:'ReNew Power',init:'RW',color:'#00A19A',sector:'energy',city:'Delhi NCR'},
  {n:'Ola Electric',init:'OL',color:'#1B1B1B',sector:'energy',city:'Bengaluru'},
  {n:'Ather Energy',init:'AE',color:'#FF6B0A',sector:'energy',city:'Bengaluru'},
  {n:'Suzlon Energy',init:'SZ',color:'#C8102E',sector:'energy',city:'Pune'},
  {n:'Reliance NewEnergy',init:'RN',color:'#0066B3',sector:'energy',city:'Mumbai'},
  {n:'Amara Raja',init:'AR',color:'#005EB8',sector:'energy',city:'Hyderabad'},
  {n:'Exide Industries',init:'EX',color:'#E63946',sector:'energy',city:'Kolkata'},
  {n:'JSW Energy',init:'JE',color:'#005EB8',sector:'energy',city:'Mumbai'},
  {n:'Tata Projects',init:'TJ',color:'#1F3864',sector:'construction',city:'Mumbai'},
  {n:'AFCONS',init:'AF',color:'#005CB9',sector:'construction',city:'Mumbai'},
  {n:'Shapoorji Pallonji',init:'SH',color:'#003B71',sector:'construction',city:'Mumbai'},
  {n:'GMR Group',init:'GM',color:'#B22222',sector:'construction',city:'Delhi NCR'},
  {n:'NCC Limited',init:'NC',color:'#0070C0',sector:'construction',city:'Hyderabad'}
];
const sectorLabels={all:'All Sectors',govt:'Government / PSU',it:'IT / Software',manufacturing:'Manufacturing / Auto',heavy:'Heavy Industry',oil:'Oil & Chemical',pharma:'Pharma & Bio',energy:'Energy / EV / Renewable',construction:'Construction / Infrastructure',mining:'Mining / Minerals',startups:'Startups / Product'};
const sectorDesc={
  all:'All major job hubs across India highlighted. Use the filter chips above to focus on a specific sector — only the cities active in that sector will glow on the map.',
  govt:'ISRO, DRDO, BARC, NTPC, Power Grid, ONGC and major PSUs — long-term stable Group-A careers concentrated in Delhi NCR, Bengaluru, Hyderabad, Mumbai.',
  it:'India\'s $245B IT industry. TCS, Infosys, Wipro and global majors. Top hubs: Bengaluru, Hyderabad, Pune, Chennai, NCR.',
  manufacturing:'India\'s auto-belt — Tata, Mahindra, Maruti, Hyundai, Bosch. Centred on Pune, Chennai, NCR, Coimbatore.',
  heavy:'Tata Steel, L&T, JSW, BHEL, Reliance, Adani. Hubs: Jamshedpur, Mumbai, Ahmedabad, Kolkata, Delhi.',
  oil:'Specialty chemicals + petroleum. Aarti, SRF, PI Industries, Reliance, Atul, Deepak Nitrite. Mumbai + Vapi-Vadodara corridor.',
  pharma:'India is "pharmacy of the world". Sun Pharma, Cipla, Dr Reddy\'s, Biocon, Serum Institute. Mumbai, Hyderabad, Bengaluru, Pune.',
  energy:'500 GW renewable target, EV push, smart grids. Tata Power, Adani Green, ReNew, Ola, Ather. Bengaluru, Mumbai, NCR, Pune.',
  construction:'₹100 lakh crore infrastructure pipeline. L&T, Tata Projects, AFCONS, Shapoorji, GMR.',
  mining:'Coal India, NMDC, Vedanta, Hindustan Zinc. Concentrated in Kolkata, Hyderabad, Mumbai.',
  startups:'Indian product unicorns — Flipkart, Razorpay, Swiggy, Zomato, CRED, Sarvam. Bengaluru-led; NCR and Mumbai growing.'
};
function renderCompanies(filter){
  const grid=document.getElementById('companiesGrid');if(!grid)return;
  filter=filter||'all';
  const visible=filter==='all'?companies:companies.filter(c=>c.sector===filter);
  let h='';
  visible.forEach((c,i)=>{
    h+=`<div class="company-card" data-sector="${c.sector}"><div class="co-logo" style="background:${c.color}">${c.init}</div><div class="co-info"><div class="co-name">${i+1}. ${c.n}</div><div class="co-sector">${sectorLabels[c.sector]} · ${c.city}</div></div></div>`;
  });
  if(!h)h='<div style="color:rgba(255,255,255,.6);font-style:italic;padding:30px">No companies match this filter.</div>';
  grid.innerHTML=h;
  const cosEl=document.getElementById('msCos');if(cosEl)cosEl.textContent=visible.length;
}
// D3 INDIA MAP — real GeoJSON
function normaliseStateName(raw){
  const m={"Orissa":"Odisha","Pondicherry":"Puducherry","Uttaranchal":"Uttarakhand","Telengana":"Telangana","NCT of Delhi":"Delhi","Delhi (NCT)":"Delhi","Jammu & Kashmir":"Jammu and Kashmir","Jammu And Kashmir":"Jammu and Kashmir","Andaman & Nicobar Islands":"Andaman and Nicobar Islands","Andaman & Nicobar Island":"Andaman and Nicobar Islands","Dadra and Nagar Haveli":"Dadra and Nagar Haveli and Daman and Diu","Daman and Diu":"Dadra and Nagar Haveli and Daman and Diu","Daman & Diu":"Dadra and Nagar Haveli and Daman and Diu"};
  return m[(raw||"").trim()]||(raw||"").trim();
}
// City → state lookup
const cityToState={'Delhi NCR':'Delhi','Mumbai':'Maharashtra','Pune':'Maharashtra','Ahmedabad':'Gujarat','Surat':'Gujarat','Bengaluru':'Karnataka','Chennai':'Tamil Nadu','Coimbatore':'Tamil Nadu','Hyderabad':'Telangana','Kolkata':'West Bengal','Visakhapatnam':'Andhra Pradesh','Trivandrum':'Kerala','Jamshedpur':'Jharkhand','Jaipur':'Rajasthan','Bhubaneswar':'Odisha','Lucknow':'Uttar Pradesh'};
// Hub city coordinates (lat/lng) for D3 projection
const cityHubs=[
  {name:'Delhi NCR',lat:28.61,lng:77.21,sectors:['govt','it','manufacturing','heavy','startups'],info:'Govt HQ · Gurgaon IT · Auto · Startups',size:14},
  {name:'Mumbai',lat:19.07,lng:72.87,sectors:['it','manufacturing','pharma','heavy','oil','startups'],info:'Finance · IT · Pharma corridor · Heavy industry',size:14},
  {name:'Pune',lat:18.52,lng:73.86,sectors:['it','manufacturing','startups'],info:'Auto manufacturing · IT · Startups',size:10},
  {name:'Ahmedabad',lat:23.02,lng:72.57,sectors:['oil','pharma','manufacturing','heavy'],info:'Petrochem · Pharma · Specialty Chem',size:10},
  {name:'Surat',lat:21.17,lng:72.83,sectors:['oil','pharma','manufacturing'],info:'ONGC · Reliance · Petrochem · Pharma',size:9},
  {name:'Bengaluru',lat:12.97,lng:77.59,sectors:['it','startups','manufacturing','govt'],info:'IT capital · ISRO · Startups · Aerospace',size:15},
  {name:'Chennai',lat:13.08,lng:80.27,sectors:['it','manufacturing','startups','construction'],info:'Auto manufacturing · IT · Hyundai · TCS',size:12},
  {name:'Coimbatore',lat:11.02,lng:76.96,sectors:['manufacturing','it'],info:'Textiles · Auto components · Manufacturing',size:9},
  {name:'Hyderabad',lat:17.38,lng:78.49,sectors:['it','pharma','govt','startups'],info:'Pharma capital · IT · DRDO · Bharat Biotech',size:13},
  {name:'Kolkata',lat:22.57,lng:88.36,sectors:['govt','heavy','manufacturing','construction'],info:'Govt · Heavy industry · Coal · Steel',size:11},
  {name:'Visakhapatnam',lat:17.69,lng:83.21,sectors:['oil','heavy','manufacturing','construction'],info:'Petroleum · Shipbuilding · Steel',size:9},
  {name:'Trivandrum',lat:8.52,lng:76.94,sectors:['govt','it'],info:'ISRO · IT · Govt sector',size:9},
  {name:'Jamshedpur',lat:22.80,lng:86.20,sectors:['heavy','manufacturing','mining'],info:'Tata Steel · Heavy manufacturing',size:9},
  {name:'Jaipur',lat:26.91,lng:75.79,sectors:['govt','manufacturing','startups'],info:'State govt · Manufacturing · Startups',size:9},
  {name:'Bhubaneswar',lat:20.30,lng:85.82,sectors:['mining','heavy','it'],info:'Mining · Steel · IT zone',size:8},
  {name:'Lucknow',lat:26.85,lng:80.95,sectors:['govt','manufacturing'],info:'UP Govt · Manufacturing · Defence',size:9}
];
let indiaProjection=null, indiaPath=null, geoLoaded=false;
const GEO_SOURCES=[
  "https://cdn.jsdelivr.net/gh/udit-001/india-maps-data@ef25ebc/geojson/india.geojson",
  "https://cdn.jsdelivr.net/gh/udit-001/india-maps-data@main/geojson/india.geojson"
];
function loadIndiaGeo(){
  return GEO_SOURCES.reduce((p,url)=>p.catch(()=>d3.json(url)),Promise.reject());
}
function renderIndiaMap(){
  if(typeof d3==='undefined'){console.error('D3 not loaded');return;}
  loadIndiaGeo().then(geo=>{
    geoLoaded=true;
    const svg=d3.select("#indiaMap");
    indiaProjection=d3.geoMercator().fitSize([720,720],geo);
    indiaPath=d3.geoPath().projection(indiaProjection);

    // States
    svg.select(".states-layer").selectAll("path.state")
      .data(geo.features).enter().append("path")
      .attr("class","state")
      .attr("d",indiaPath)
      .attr("data-name",d=>normaliseStateName(d.properties.st_nm));

    // City pins (with pulse aura)
    const pinLayer=svg.select(".pins-layer");
    cityHubs.forEach((h,i)=>{
      const xy=indiaProjection([h.lng,h.lat]);
      const g=pinLayer.append("g").attr("class","city-hub").attr("data-sectors",h.sectors.join(",")).attr("data-name",h.name);
      g.append("circle").attr("class","city-pulse").attr("cx",xy[0]).attr("cy",xy[1]).attr("r",6).style("animation-delay",(i*0.15)+"s");
      g.append("circle").attr("class","city-pin").attr("cx",xy[0]).attr("cy",xy[1]).attr("r",0).attr("data-base-r",Math.max(5,h.size*0.55))
        .on("mouseenter",function(){showTooltip(h);d3.select(this).attr("r",h.size*0.9);})
        .on("mouseleave",function(){hideTooltip();d3.select(this).attr("r",h.size*0.55);})
        .on("mousemove",moveTooltip)
        .transition().duration(500).delay(300+i*40).attr("r",h.size*0.55);
      // Label offset: right of pin, except specific cities pushed left
      const leftShift=['Ahmedabad','Surat','Mumbai','Coimbatore','Trivandrum','Jaipur'].includes(h.name);
      g.append("text").attr("class","city-label").attr("x",xy[0]+(leftShift?-10:10)).attr("y",xy[1]+4).attr("text-anchor",leftShift?'end':'start').text(h.name);
    });

    // Hide loader
    const loader=document.getElementById('mapLoading');if(loader)loader.classList.add('hide');
    applyMapFilter('all');
  }).catch(err=>{
    console.error('GeoJSON load failed:',err);
    const loader=document.getElementById('mapLoading');
    if(loader)loader.innerHTML='<div style="font-family:Fraunces,serif;font-size:16px;margin-bottom:8px">Could not load India map</div><div style="font-size:11px;font-family:JetBrains Mono,monospace;letter-spacing:.16em;text-transform:uppercase;color:rgba(255,255,255,.6)">Check your connection · reload page</div>';
  });
}

function applyMapFilter(filter){
  filter=filter||'all';
  // Companies per state for choropleth
  const filtered=filter==='all'?companies:companies.filter(c=>c.sector===filter);
  const stateCounts={};
  filtered.forEach(c=>{const st=cityToState[c.city];if(st)stateCounts[st]=(stateCounts[st]||0)+1;});
  const maxCount=Math.max(...Object.values(stateCounts),1);
  // Recolor states
  if(geoLoaded){
    d3.selectAll("#indiaMap path.state").attr("fill",function(){
      const name=this.getAttribute("data-name");
      const v=stateCounts[name]||0;
      if(v===0) return "rgba(255,255,255,0.06)";
      const r=v/maxCount;
      if(r<0.20) return "rgba(255,107,10,0.20)";
      if(r<0.40) return "rgba(255,107,10,0.38)";
      if(r<0.65) return "rgba(255,107,10,0.58)";
      if(r<0.90) return "rgba(255,107,10,0.78)";
      return "rgba(255,107,10,0.95)";
    });
  }
  // Filter city pins
  let activeCount=0;
  cityHubs.forEach(h=>{const active=(filter==='all')||h.sectors.includes(filter);if(active)activeCount++;});
  if(geoLoaded){
    d3.selectAll("#indiaMap .city-hub").each(function(){
      const g=d3.select(this);
      const sectors=(g.attr("data-sectors")||"").split(",");
      const active=(filter==='all')||sectors.includes(filter);
      g.select(".city-pin").classed("dim",!active);
      g.select(".city-pulse").classed("dim",!active);
      g.select(".city-label").classed("dim",!active);
    });
  }
  // Side panel
  const msTitle=document.getElementById('msTitle');if(msTitle)msTitle.textContent=sectorLabels[filter]||'All Sectors';
  const msDesc=document.getElementById('msDesc');if(msDesc)msDesc.textContent=sectorDesc[filter]||sectorDesc.all;
  const msHubs=document.getElementById('msHubs');if(msHubs)msHubs.textContent=activeCount;
  // Hub list
  const list=document.getElementById('mapHubList');
  if(list){
    let lh='';
    cityHubs.forEach(h=>{
      if((filter==='all')||h.sectors.includes(filter)){
        lh+=`<div class="map-hub-item"><span class="mh-dot"></span><div><div class="mh-name">${h.name}</div><div class="mh-info">${h.info}</div></div></div>`;
      }
    });
    list.innerHTML=lh||'<div style="color:rgba(255,255,255,.5);font-size:13px;padding:10px;font-style:italic">No hubs active for this sector.</div>';
  }
  renderCompanies(filter);
}

// Tooltip
function showTooltip(h){const tt=document.getElementById('mapTooltip');if(tt){tt.innerHTML=`<div class="tt-title">${h.name}</div><div class="tt-info">${h.info}</div>`;tt.classList.add('show');}}
function hideTooltip(){const tt=document.getElementById('mapTooltip');if(tt)tt.classList.remove('show');}
function moveTooltip(e){const tt=document.getElementById('mapTooltip');if(tt){const card=document.querySelector('.india-map-card');const r=card.getBoundingClientRect();tt.style.left=(e.clientX-r.left+16)+'px';tt.style.top=(e.clientY-r.top-10)+'px';}}

// Filter chip bindings (map)
document.querySelectorAll('[data-map-filter]').forEach(btn=>{
  btn.addEventListener('click',()=>{
    document.querySelectorAll('[data-map-filter]').forEach(b=>b.classList.remove('active'));
    btn.classList.add('active');
    applyMapFilter(btn.dataset.mapFilter);
  });
});

// Initialize all sections
renderSkillsRow();
renderSubjectsMatrix('all');
renderJobsTable();
renderCompanies('all');
renderIndiaMap();
