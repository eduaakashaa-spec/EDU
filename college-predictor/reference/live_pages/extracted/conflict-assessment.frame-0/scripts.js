
var D = {}; // master data store

/* ── SCREEN NAV ── */
function showScreen(id) {
  ['heroSection','methodology','assessment','results'].forEach(function(s) {
    var el = document.getElementById(s);
    if (el) el.classList.toggle('hidden', s !== id);
  });
  window.scrollTo({top: 0, behavior: 'smooth'});
}

/* ── TAB SWITCHING ── */
function switchTab(tab) {
  document.getElementById('panelStudent').classList.toggle('active', tab === 'student');
  document.getElementById('panelParent').classList.toggle('active', tab === 'parent');
  document.getElementById('tabStudent').classList.toggle('active', tab === 'student');
  document.getElementById('tabParent').classList.toggle('active', tab === 'parent');
  if (tab === 'parent') document.getElementById('tabParent').classList.add('or-active');
  else document.getElementById('tabParent').classList.remove('or-active');
}

/* ── STEP NAV ── */
function nextStep(who, step) {
  var prefix = who === 's' ? 's' : 'p';
  var total = who === 's' ? 7 : 6;
  var prev = step - 1;
  document.getElementById(prefix + 'Step' + prev).classList.add('hidden');
  document.getElementById(prefix + 'Step' + step).classList.remove('hidden');
  var pct = Math.round((step / total) * 100);
  document.getElementById(prefix + 'Progress').style.width = pct + '%';
  var labels = who === 's'
    ? ['Profile & Identity','Dreams & Interests','The Conflict','Future Vision','Deeper Insights','Practical Factors','Expectations']
    : ['Profile','Your Vision','Concerns','Future Goals','Deeper Understanding','Final Details'];
  document.getElementById(prefix + 'StepLabel').textContent = 'Step ' + step + ' of ' + total + ' — ' + labels[step - 1];
  window.scrollTo({top: document.getElementById('assessment').offsetTop - 80, behavior: 'smooth'});
}
function prevStep(who, step) { nextStep(who, step); }

/* ── FORM HELPERS ── */
function toggleOpt(el, key) {
  el.parentNode.querySelectorAll('.option-card').forEach(function(c) { c.classList.remove('selected'); });
  el.classList.add('selected');
  D[key] = el.textContent.trim();
}
function toggleMulti(el) { el.classList.toggle('selected'); }
function selectLikert(el, lvl) {
  el.parentNode.querySelectorAll('label').forEach(function(l) {
    l.classList.remove('checked','l1','l2','l3','l4','l5');
  });
  el.classList.add('checked', lvl);
}
function getMulti(containerId) {
  var sel = [];
  document.querySelectorAll('#' + containerId + ' .option-card.selected').forEach(function(c) { sel.push(c.textContent.trim()); });
  return sel;
}

/* ── COLLECT DATA ── */
function collectStudent() {
  D.student = {
    name: document.getElementById('sName').value,
    age: document.getElementById('sAge').value,
    class: document.getElementById('sClass').value,
    board: document.getElementById('sBoard').value,
    location: document.getElementById('sLocation').value,
    dream: document.getElementById('sDream').value,
    course: D.sCourse || '',
    interests: getMulti('sInterestGrid'),
    parentWants: D.sParentWants || '',
    conflictLevel: document.getElementById('sConflictLevel').value,
    parentReason: (document.querySelector('input[name=sParentReason]:checked') || {}).value || '',
    frustration: document.getElementById('sFrustration').value,
    goal3: document.getElementById('sGoal3').value,
    goal5: document.getElementById('sGoal5').value,
    goal10: document.getElementById('sGoal10').value,
    values: getMulti('sValueGrid'),
    emotion: D.sEmotion || '',
    indirect1: document.getElementById('sIndirect1').value,
    stressors: getMulti('sStressGrid'),
    ifOnly: document.getElementById('sIfOnly').value,
    openness: document.getElementById('sOpenness').value,
    exams: getMulti('sExamGrid'),
    score: document.getElementById('sScore').value,
    budget: document.getElementById('sBudget').value,
    gapYear: (document.querySelector('input[name=sGap]:checked') || {}).value || '',
    flexibility: document.getElementById('sFlexibility').value,
    outcome: D.sOutcome || '',
    anything: document.getElementById('sAnything').value,
    email: document.getElementById('sEmail').value,
  };
}
function collectParent() {
  D.parent = {
    name: document.getElementById('pName').value,
    relation: document.getElementById('pRelation').value,
    profession: document.getElementById('pProfession').value,
    education: document.getElementById('pEducation').value,
    course: D.pCourse || '',
    why: D.pWhy || '',
    worries: getMulti('pWorryGrid'),
    confidence: document.getElementById('pConfidence').value,
    research: (document.querySelector('input[name=pResearch]:checked') || {}).value || '',
    goal3: document.getElementById('pGoal3').value,
    goal5: document.getElementById('pGoal5').value,
    goal10: document.getElementById('pGoal10').value,
    values: getMulti('pValueGrid'),
    relativeTest: (document.querySelector('input[name=pRelativeTest]:checked') || {}).value || '',
    influences: getMulti('pInfluenceGrid'),
    ifSupport: document.getElementById('pIfSupport').value,
    openness: document.getElementById('pOpenness').value,
    outcome: D.pOutcome || '',
    anything: document.getElementById('pAnything').value,
    email: document.getElementById('pEmail').value,
  };
}
function completeStudent() {
  collectStudent();
  D.studentDone = true;
  alert('Student assessment saved! Now please switch to the Parent tab to complete their assessment.');
  switchTab('parent');
}
function completeParent() {
  collectParent();
  D.parentDone = true;
  if (!D.studentDone) {
    alert('Please complete the Student assessment first.');
    switchTab('student');
    return;
  }
  generateResults();
}

/* ══════════════════════════════════════════
   ANALYSIS ENGINE
   ══════════════════════════════════════════ */
function generateResults() {
  var s = D.student, p = D.parent;
  showScreen('results');
  document.getElementById('resDate').textContent = new Date().toLocaleDateString('en-IN', {day:'numeric',month:'long',year:'numeric'});

  // ── CONFLICT DIMENSIONS ──
  var courseConflict = (s.course !== p.course && p.course !== 'Same as my child\'s choice' && p.course !== 'Open — whatever is best') ? 85 : 15;
  var valueConflict = calcValueOverlap(s.values, p.values);
  var commConflict = Math.max(10, 100 - ((parseInt(s.openness) + parseInt(p.openness)) / 2) * 10);
  var trustGap = p.relativeTest === 'no_obj' ? 80 : p.relativeTest === 'maybe' ? 55 : 25;
  var hiddenIssues = calcHiddenScore(s, p);
  var overallConflict = Math.round((courseConflict * 0.25 + valueConflict * 0.2 + commConflict * 0.2 + trustGap * 0.15 + hiddenIssues * 0.2));

  // Conflict Meter
  var meterHTML = '<div style="font-size:48px;font-weight:900;margin-bottom:8px;font-family:Playfair Display,serif">' + overallConflict + '<span style="font-size:20px;opacity:.6">/100</span></div>';
  meterHTML += '<div style="font-size:14px;opacity:.8;margin-bottom:24px">Overall Conflict Score — ' + getConflictLabel(overallConflict) + '</div>';
  var dims = [
    {label:'Course Mismatch',val:courseConflict,color:'#DC2626'},
    {label:'Value Misalignment',val:valueConflict,color:'#D97706'},
    {label:'Communication Gap',val:commConflict,color:'#2563EB'},
    {label:'Trust Deficit',val:trustGap,color:'#7C3AED'},
    {label:'Hidden Issues',val:hiddenIssues,color:'#F58220'},
  ];
  dims.forEach(function(d) {
    meterHTML += '<div class="conflict-level"><span class="conflict-label">' + d.label + '</span><div class="conflict-bar-bg"><div class="conflict-bar-fill" style="width:' + d.val + '%;background:' + d.color + '"></div></div><span class="conflict-pct">' + d.val + '%</span></div>';
  });
  document.getElementById('conflictMeter').innerHTML = meterHTML;

  // ── CHARTS ──
  buildRadarChart(s);
  buildConflictChart(dims);
  buildValuesChart(s, p);

  // ── INSIGHTS ──
  var insights = [];
  if (courseConflict > 50) insights.push({icon:'⚡',title:'Course Conflict Detected',text:'Student wants <strong>' + s.course + '</strong> while parent prefers <strong>' + p.course + '</strong>. This is the primary visible conflict but often not the root cause.'});
  if (trustGap > 50) insights.push({icon:'🔍',title:'Trust Factor Identified',text:'The "relative test" reveals this conflict may be more about trust in the student\'s judgment than the field itself. Parent indicated they would be less concerned if a trusted person made the same choice.'});
  if (s.emotion && s.emotion.includes('Anxiety')) insights.push({icon:'😰',title:'Emotional Distress Alert',text:'Student reports anxiety when imagining the parent-preferred path. Forcing this path risks academic underperformance, dropout, and long-term resentment. Studies show students in misaligned courses are 2.7x more likely to drop out.'});
  if (hiddenIssues > 60) insights.push({icon:'🧠',title:'Hidden Influences Active',text:'Both parties show signs of being influenced by external factors (social comparison, financial fear, peer pressure) rather than pure rational analysis. This is extremely common and addressable.'});

  var valueOverlap = getSharedValues(s.values, p.values);
  if (valueOverlap.length > 0) insights.push({icon:'✅',title:'Shared Values Found!',text:'Both student and parent value: <strong>' + valueOverlap.join(', ') + '</strong>. This is your common ground — the resolution should demonstrate how BOTH paths can satisfy these shared values.'});

  if (commConflict > 60) insights.push({icon:'🗣️',title:'Communication Breakdown',text:'Both parties show low openness to the other\'s perspective (Student: ' + s.openness + '/10, Parent: ' + p.openness + '/10). The first step should be a structured conversation — not about the decision, but about understanding each other\'s fears and hopes.'});

  if (p.research === 'no' || p.research === 'surface' || p.research === 'no_need') insights.push({icon:'📚',title:'Information Gap',text:'Parent has not deeply researched the student\'s preferred field. Many parental objections dissolve with proper information. We recommend researching placement data, salary ranges, and growth prospects for <strong>' + s.course + '</strong>.'});

  var ig = document.getElementById('insightsGrid');
  ig.innerHTML = '';
  insights.forEach(function(ins) {
    ig.innerHTML += '<div class="insight-card"><h4>' + ins.icon + ' ' + ins.title + '</h4><p>' + ins.text + '</p></div>';
  });

  // ── RECOMMENDATIONS ──
  var recs = generateRecommendations(s, p, overallConflict, courseConflict, trustGap, hiddenIssues, commConflict);
  var rc = document.getElementById('recsContainer');
  rc.innerHTML = '';
  recs.forEach(function(r) {
    rc.innerHTML += '<div class="rec-card ' + r.type + '"><h4>' + r.icon + ' ' + r.title + '</h4><p>' + r.text + '</p></div>';
  });

  // ── TIMELINE ──
  var tc = document.getElementById('timelineContainer');
  tc.innerHTML = '';
  var timeline = [
    {yr:'Now',title:'Structured Family Dialogue',text:'Hold a 60-min family conversation using the IBR model: each person shares their FEARS first, then HOPES. No interrupting. No solutions yet — just understanding.'},
    {yr:'Week 1-2',title:'Research Sprint',text:'Both parent and student independently research the OTHER person\'s preferred field. Parent explores ' + (s.course||'student\'s choice') + '; student explores ' + (p.course||'parent\'s choice') + '. Share findings.'},
    {yr:'Month 1',title:'Expert Consultation',text:'Book an EduAakashaA counselling session to review entrance exam scores, budget, and real placement data. Get objective information from someone both parties trust.'},
    {yr:'3 Years',title:'Student Vision: ' + (s.goal3 || 'In college, building skills'),text:'Parent Vision: ' + (p.goal3 || 'In a good institution, focused')},
    {yr:'5 Years',title:'Student Vision: ' + (s.goal5 || 'Graduated, working in chosen field'),text:'Parent Vision: ' + (p.goal5 || 'Employed, independent')},
    {yr:'10 Years',title:'Student Vision: ' + (s.goal10 || 'Established career, giving back'),text:'Parent Vision: ' + (p.goal10 || 'Settled, financially stable')},
  ];
  timeline.forEach(function(t) {
    tc.innerHTML += '<div class="timeline-item"><h5>' + t.yr + ' — ' + t.title + '</h5><p>' + t.text + '</p></div>';
  });
}

/* ── CALCULATION HELPERS ── */
function calcValueOverlap(sv, pv) {
  if (!sv || !pv || sv.length === 0 || pv.length === 0) return 60;
  var shared = 0;
  sv.forEach(function(v) { if (pv.indexOf(v) > -1) shared++; });
  var total = Math.max(sv.length, pv.length);
  return Math.round(100 - (shared / total) * 100);
}
function getSharedValues(sv, pv) {
  if (!sv || !pv) return [];
  return sv.filter(function(v) { return pv.indexOf(v) > -1; });
}
function calcHiddenScore(s, p) {
  var score = 0;
  if (s.stressors && s.stressors.length > 2) score += 20;
  if (s.emotion && (s.emotion.includes('Anxiety') || s.emotion.includes('Anger'))) score += 15;
  if (p.influences && p.influences.length > 2) score += 20;
  if (p.relativeTest === 'no_obj') score += 15;
  if (p.research === 'no' || p.research === 'no_need') score += 15;
  if (s.parentReason === 'status' || s.parentReason === 'control') score += 15;
  return Math.min(score, 100);
}
function getConflictLabel(v) {
  if (v < 25) return 'Low — Minor differences, easily resolvable';
  if (v < 50) return 'Moderate — Significant disagreement, structured dialogue needed';
  if (v < 75) return 'High — Deep conflict, professional mediation recommended';
  return 'Critical — Urgent intervention needed to prevent lasting damage';
}

function generateRecommendations(s, p, overall, course, trust, hidden, comm) {
  var recs = [];
  if (course > 50) {
    recs.push({type:'', icon:'🎯', title:'Bridge Course Strategy',
      text:'Instead of choosing one side, explore the INTERSECTION of both preferences. If student wants ' + (s.course||'their choice') + ' and parent prefers ' + (p.course||'their choice') + ', look for interdisciplinary programs, dual degrees, or specializations that combine elements of both. For example: BioTech bridges Medicine + Engineering; FinTech bridges Finance + CS; UX Design bridges Arts + Technology.'});
  }
  if (comm > 50) {
    recs.push({type:'warn', icon:'🗣️', title:'Communication Protocol',
      text:'Schedule a "Family Council" — 45 minutes, structured: (1) Each person gets 10 uninterrupted minutes to share fears, not demands. (2) 10 minutes where each person paraphrases what the other said. (3) 15 minutes identifying shared goals. Rule: no phones, no "you always" statements.'});
  }
  if (trust > 50) {
    recs.push({type:'info', icon:'🤝', title:'"Prove It" Pilot Program',
      text:'Parent agrees to support the student\'s choice IF the student demonstrates commitment: complete a 30-day online course in the field, attend 3 webinars, interview 2 professionals, and present findings. This builds trust through action, not arguments.'});
  }
  if (hidden > 40) {
    recs.push({type:'warn', icon:'🧠', title:'Address Hidden Influences',
      text:'Both parties should explicitly list the EXTERNAL pressures affecting them (relatives, neighbours, social media, personal regrets). Separating external noise from genuine concerns often reduces conflict by 40-60%.'});
  }
  recs.push({type:'', icon:'📊', title:'Data-Based Decision',
    text:'Research together: (1) Average starting salary in both fields, (2) 5-year career growth trajectory, (3) Current job market demand, (4) Real alumni stories from both paths. EduAakashaA can provide this data for specific colleges and courses.'});
  recs.push({type:'info', icon:'📞', title:'Expert Mediation',
    text:'Book a joint counselling session at EduAakashaA where both parent and student present their views to a neutral career expert. Having an external authority often breaks deadlocks that family conversations cannot.'});
  return recs;
}

/* ── CHARTS ── */
function buildRadarChart(s) {
  var ctx = document.getElementById('radarChart');
  var interests = s.interests || [];
  var R=0,I=0,A=0,S=0,E=0,C=0;
  interests.forEach(function(i) {
    if (i.includes('Building') || i.includes('Fixing')) R += 3;
    if (i.includes('Research') || i.includes('Experiment')) I += 3;
    if (i.includes('art') || i.includes('Writing') || i.includes('Creating')) A += 3;
    if (i.includes('Helping') || i.includes('Teaching')) S += 3;
    if (i.includes('Leading') || i.includes('Organis')) E += 3;
    if (i.includes('data') || i.includes('Systems') || i.includes('Organising data')) C += 3;
    if (i.includes('Coding') || i.includes('Tech')) { I += 2; R += 1; }
    if (i.includes('Gaming') || i.includes('Strategy')) { E += 2; I += 1; }
  });
  new Chart(ctx, {
    type: 'radar',
    data: {
      labels: ['Realistic','Investigative','Artistic','Social','Enterprising','Conventional'],
      datasets: [{
        label: 'Student Profile',
        data: [R||1, I||1, A||1, S||1, E||1, C||1],
        backgroundColor: 'rgba(245,130,32,0.15)',
        borderColor: '#F58220',
        pointBackgroundColor: '#F58220',
        borderWidth: 2
      }]
    },
    options: {responsive:true, maintainAspectRatio:false, scales:{r:{beginAtZero:true,ticks:{display:false},grid:{color:'#EEF2F7'},pointLabels:{font:{size:12,family:'DM Sans',weight:600},color:'#1B3764'}}}, plugins:{legend:{display:false}}}
  });
}

function buildConflictChart(dims) {
  var ctx = document.getElementById('conflictChart');
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: dims.map(function(d){return d.label}),
      datasets: [{
        data: dims.map(function(d){return d.val}),
        backgroundColor: dims.map(function(d){return d.color + '33'}),
        borderColor: dims.map(function(d){return d.color}),
        borderWidth: 2, borderRadius: 8, barThickness: 36
      }]
    },
    options: {responsive:true,maintainAspectRatio:false,indexAxis:'y',
      scales:{x:{max:100,grid:{color:'#EEF2F7'},ticks:{callback:function(v){return v+'%'},font:{size:11}}},y:{grid:{display:false},ticks:{font:{size:12,family:'DM Sans',weight:600}}}},
      plugins:{legend:{display:false}}}
  });
}

function buildValuesChart(s, p) {
  var ctx = document.getElementById('valuesChart');
  var allVals = ['High Income','Passion / Fulfillment','Work-Life Balance','Global Opportunities','Job Security','Innovation / Impact','Family Approval','Prestige / Status','Financial security','Social prestige','Happiness / Satisfaction','Stability / Close to family','Global mobility','Continue family legacy'];
  var shortVals = [];
  var sScores = [], pScores = [];
  allVals.forEach(function(v) {
    var sHas = (s.values||[]).some(function(sv){return sv.includes(v.split(' ')[0])});
    var pHas = (p.values||[]).some(function(pv){return pv.includes(v.split(' ')[0])});
    if (sHas || pHas) {
      shortVals.push(v.length > 18 ? v.substring(0,18)+'…' : v);
      sScores.push(sHas ? 1 : 0);
      pScores.push(pHas ? 1 : 0);
    }
  });
  if (shortVals.length === 0) { shortVals = ['No data']; sScores = [0]; pScores = [0]; }
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: shortVals,
      datasets: [
        {label:'Student',data:sScores,backgroundColor:'#F5822055',borderColor:'#F58220',borderWidth:2,borderRadius:6,barPercentage:0.6},
        {label:'Parent',data:pScores,backgroundColor:'#1B376455',borderColor:'#1B3764',borderWidth:2,borderRadius:6,barPercentage:0.6}
      ]
    },
    options: {responsive:true,maintainAspectRatio:false,
      scales:{y:{max:1.2,ticks:{display:false},grid:{color:'#EEF2F7'}},x:{grid:{display:false},ticks:{font:{size:10},maxRotation:45}}},
      plugins:{legend:{position:'top',labels:{font:{size:12,family:'DM Sans',weight:600},usePointStyle:true,pointStyle:'rectRounded'}}}}
  });
}

/* ── GOOGLE SHEETS INTEGRATION ── */
function saveToSheets() {
  /*
    To connect Google Sheets:
    1. Create a Google Sheet
    2. Go to Extensions → Apps Script
    3. Paste this code:

    function doPost(e) {
      var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
      var data = JSON.parse(e.postData.contents);
      sheet.appendRow([
        new Date(),
        data.studentName, data.studentCourse, data.parentName, data.parentCourse,
        data.conflictLevel, data.overallScore, data.studentGoal3, data.parentGoal3,
        JSON.stringify(data.studentValues), JSON.stringify(data.parentValues),
        data.studentEmail, data.parentEmail
      ]);
      return ContentService.createTextOutput(JSON.stringify({status:'ok'}));
    }

    4. Deploy as Web App → Anyone can access
    5. Copy the URL and replace SHEET_WEBHOOK_URL below
  */
  var SHEET_WEBHOOK_URL = ''; // Replace with your Apps Script URL

  if (!SHEET_WEBHOOK_URL) {
    alert('Google Sheets not configured yet.\n\nClick the ⚙ setup guide on the homepage for instructions, or check the code comments in saveToSheets() function.');
    return;
  }
  var payload = {
    studentName: D.student.name,
    studentCourse: D.student.course,
    parentName: D.parent.name,
    parentCourse: D.parent.course,
    conflictLevel: D.student.conflictLevel,
    overallScore: '',
    studentGoal3: D.student.goal3,
    parentGoal3: D.parent.goal3,
    studentValues: D.student.values,
    parentValues: D.parent.values,
    studentEmail: D.student.email,
    parentEmail: D.parent.email
  };
  fetch(SHEET_WEBHOOK_URL, {
    method: 'POST', mode: 'no-cors',
    headers: {'Content-Type':'application/json'},
    body: JSON.stringify(payload)
  }).then(function() { alert('Data saved to Google Sheets!'); })
    .catch(function() { alert('Error saving. Check the webhook URL.'); });
}

function generateReport() {
  alert('PDF report generation requires a backend service.\n\nFor now, use Ctrl+P (Cmd+P on Mac) to print this page as PDF.\n\nOr contact EduAakashaA to receive a detailed professionally formatted report.');
  window.print();
}


// ---- next <script> block ----


	const heightObserver = new ResizeObserver(([{ contentRect }]) => {
		window.parent.postMessage({ action: 'iframeHeightUpdated', height: contentRect.height, id: 'zdOcXL' }, '*');
	});

	heightObserver.observe(document.documentElement);
