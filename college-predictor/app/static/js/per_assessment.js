
/* ============================================
   CONFIGURATION — connect to Google Sheets
   ============================================ */
// Paste your Google Apps Script Web App URL here after deployment
// (See setup-guide.md for instructions)
const APPS_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbyGKI5EK4pO5f0BpsbjOz_bb61ji6N9jbmXt4n_xwu_xCRdOIbovDA8pZFwdk_6oIxO1w/exec"; // e.g. "https://script.google.com/macros/s/XXXX/exec"
const EXPERT_ACCESS_CODE = "Edu@Palani"; // Change this in production

// WhatsApp community channels — update these URLs with your actual links from www.eduaakashaa.in
// These appear in every report sent to students (in-app + PDF + email).
const WHATSAPP_CHANNELS = [
  { name: "JEE Aspirants 2027",        desc: "One physics question + solution every weekday.", url: "https://whatsapp.com/channel/0029VbCqalB3QxSAakeOeL42" },
  { name: "NRI College Admission",       desc: "Get expert guidance for NRI engineering admissions via DASA & CIWG.", url: "https://whatsapp.com/channel/0029Vb7risZ9RZAVrAFgLo3m" },
  { name: "Career Counselling Updates", desc: "College alerts, scholarship news, and career path guidance.", url: "https://www.eduaakashaa.in" },
  { name: "Parent Community",           desc: "A dedicated channel for Grades 10–12 students. Get expert guidance on choosing the right stream—Science, Commerce or Arts—along with subject insights,", url: "https://whatsapp.com/channel/0029VbCdfmZIt5rp574qxr2y" }
];

/* ============================================
   PHYSICS QUESTIONS BANK (PER-based)
   These mirror what's in the Google Sheet template.
   When APPS_SCRIPT_URL is set, questions are pulled live.
   ============================================ */
const FALLBACK_QUESTIONS = [
  {
    id: "PER-002", topic: "Kinematics", subtopic: "Velocity\u2013Time Graph",
    type: "graph/diagram-based", skill: "B", level: "medium",
    question: "A velocity\u2013time graph shows a straight line with negative slope starting from a positive velocity. What does this represent?",
    options: ["Object moving with increasing speed in negative direction", "Object decelerating while moving in positive direction, eventually stopping", "Object at rest throughout", "Object moving with constant velocity"],
    correct: 1,
    misconception: "Students think 'negative slope' means the object moves backward immediately.",
    explanation: "A straight line with negative slope on a v-t graph means constant deceleration. Starting from positive v and decreasing to zero means the object slows down and stops.",
    wrongAnalysis: "Choosing A: student conflates slope sign with direction of motion. Choosing D: ignores the slope altogether.",
    perSource: "McDermott et al. (1987) \u2013 Graphs and Tracks; Phys. Teach. 25, 502"
  },
  {
    id: "PER-013", topic: "Newton's Laws of Motion", subtopic: "Newton's Third Law",
    type: "conceptual", skill: "E", level: "medium",
    question: "A truck collides with a small car. Which statement about the forces during collision is correct?",
    options: ["The truck exerts a larger force on the car than the car exerts on the truck", "The car exerts a larger force on the truck than the truck exerts on the car", "Both exert equal and opposite forces on each other", "No force acts because the collision is brief"],
    correct: 2,
    misconception: "Students believe the more massive/faster object always exerts a greater force.",
    explanation: "Newton's Third Law: forces in an interaction pair are always equal in magnitude and opposite in direction, regardless of mass or size.",
    wrongAnalysis: "Choosing A: student confuses Newton's 3rd law with the effect of forces (bigger truck causes more damage, but forces are equal).",
    perSource: "FCI Q15 variant; Minstrell (1982) Facets of Student Knowledge"
  },
  {
    id: "PER-022", topic: "Work, Energy & Power", subtopic: "Work by Perpendicular Force",
    type: "conceptual", skill: "A", level: "medium",
    question: "A satellite revolves around Earth in a perfectly circular orbit. How much work does gravity do on the satellite in one complete revolution?",
    options: ["Positive work equal to the gravitational potential energy", "Negative work because gravity pulls inward", "Zero, because the force is always perpendicular to displacement", "Work equal to kinetic energy of the satellite"],
    correct: 2,
    misconception: "Students believe any force acting over a distance must do work.",
    explanation: "In circular orbit, gravity (centripetal) is always perpendicular to the velocity (tangential displacement). W = F\u00b7d\u00b7cos90\u00b0 = 0.",
    wrongAnalysis: "Choosing A or B: student ignores the angle between force and displacement.",
    perSource: "Lawson & McDermott (1987); Energy & Work survey (Lindsey et al. 2012)"
  },
  {
    id: "PER-032", topic: "Electricity & Current", subtopic: "Series vs Parallel Circuits",
    type: "graph/diagram-based", skill: "B", level: "medium",
    question: "Two identical bulbs are connected in parallel across a battery. Compared to a single bulb, each bulb in parallel will:",
    options: ["Be dimmer because current is shared", "Be brighter because voltage is shared", "Have the same brightness as a single bulb", "Not glow at all"],
    correct: 2,
    misconception: "Students think current (not voltage) determines brightness in parallel \u2013 believing shared current means dimmer bulbs.",
    explanation: "In parallel, each bulb receives the full battery voltage. Since V and R are the same as a single bulb, each glows with the same brightness.",
    wrongAnalysis: "Choosing A: classic misconception about parallel circuits. Students apply series-circuit logic to parallel circuits.",
    perSource: "CSEM; Shipstone (1984) \u2013 A study of children's understanding of electricity in simple DC circuits"
  },
  {
    id: "PER-042", topic: "Waves & Optics", subtopic: "Speed of Sound",
    type: "conceptual", skill: "E", level: "medium",
    question: "Sound travels faster in which medium?",
    options: ["Air, because it is less dense and offers less resistance", "Water, because it is denser", "Steel, because it has high elasticity (bulk modulus) relative to density", "Vacuum, because there is no medium to slow it down"],
    correct: 2,
    misconception: "Students think less dense medium = faster sound. They ignore the elastic modulus factor.",
    explanation: "Speed of sound = \u221a(E/\u03c1) where E is elastic modulus. Steel has very high elastic modulus; although denser, the modulus effect dominates, making v_steel >> v_water >> v_air. Sound cannot travel in vacuum.",
    wrongAnalysis: "Choosing A: student confuses low density with high speed, ignoring the E/\u03c1 ratio.",
    perSource: "CBSE Class 11 Ch 15; Wave speed misconceptions (Wittmann 2003)"
  },
  {
    id: "PER-053", topic: "Thermodynamics", subtopic: "First Law of Thermodynamics",
    type: "numerical", skill: "C", level: "medium",
    question: "A gas absorbs 500 J of heat and does 200 J of work on its surroundings. What is the change in internal energy?",
    options: ["700 J", "300 J", "-300 J", "200 J"],
    correct: 1,
    misconception: "Students add Q and W instead of subtracting: \u0394U = Q + W.",
    explanation: "First Law: \u0394U = Q \u2212 W = 500 \u2212 200 = 300 J. Heat absorbed increases internal energy; work done BY gas decreases it.",
    wrongAnalysis: "Choosing A: student added Q and W. Shows confusion about the sign convention in the First Law.",
    perSource: "CBSE Class 11 Ch 12; First Law sign convention PER"
  },
  {
    id: "PER-062", topic: "Rotational Motion", subtopic: "Moment of Inertia",
    type: "conceptual", skill: "E", level: "medium",
    question: "Two cylinders of equal mass, one solid and one hollow, roll down an incline simultaneously. Which reaches the bottom first?",
    options: ["The hollow cylinder, because it is lighter inside", "The solid cylinder, because it has lower moment of inertia and rolls faster", "They reach at the same time because they have equal mass", "The hollow cylinder, because it has more surface area"],
    correct: 1,
    misconception: "Students apply the free-fall principle (equal mass \u2192 same time) ignoring rotational inertia.",
    explanation: "For rolling without slipping, a = gsin\u03b8/(1 + I/MR\u00b2). Solid cylinder: I = \u00bdMR\u00b2 \u2192 a = (2/3)gsin\u03b8. Hollow cylinder: I = MR\u00b2 \u2192 a = (1/2)gsin\u03b8. Solid has greater acceleration \u2192 reaches first.",
    wrongAnalysis: "Choosing C: student applies Galileo's free-fall result to rolling, ignoring that rotational kinetic energy distribution affects the translational acceleration.",
    perSource: "Rimoldini & Singh (2005); Rolling motion PER; CBSE Class 11 Ch 7"
  },
  {
    id: "PER-072", topic: "Gravitation", subtopic: "Variation of g with Altitude",
    type: "numerical", skill: "C", level: "medium",
    question: "If the radius of Earth is R, what is the acceleration due to gravity at a height R above Earth's surface?",
    options: ["g/2", "g/4", "g/√2", "2g"],
    correct: 1,
    misconception: "Students use g' = g(1 \u2212 2h/R) approximation without checking if it applies (it's valid only for h << R).",
    explanation: "g' = GM/(R+h)\u00b2. At h = R: g' = GM/(2R)\u00b2 = GM/4R\u00b2 = g/4. (g = GM/R\u00b2 at surface). The distance from Earth's centre doubles, so g decreases by 1/4 (inverse square law).",
    wrongAnalysis: "Choosing A: student halved g linearly, ignoring the inverse-square nature. Shows linear thinking applied to inverse-square law.",
    perSource: "CBSE Class 11 Ch 8; JEE Main gravitation; Inverse square law PER"
  },
  {
    id: "PER-081", topic: "Modern Physics & Atomic Structure", subtopic: "Bohr's Model",
    type: "conceptual", skill: "A", level: "medium",
    question: "According to Bohr's model, an electron can only exist in certain specific orbits because:",
    options: ["The nucleus pushes the electron into fixed paths", "Only orbits where the electron's angular momentum is an integral multiple of h/2π are allowed", "Electrons lose energy continuously and spiral inward to fixed positions", "The orbit radius must equal the electron's wavelength"],
    correct: 1,
    misconception: "Students confuse Bohr's angular momentum quantization with de Broglie's standing wave condition (both are related but the direct Bohr condition is angular momentum).",
    explanation: "Bohr's quantization condition: mvr = nh/2\u03c0 (n = 1,2,3...). Only orbits satisfying this angular momentum condition are stable. Electrons in these orbits do not radiate.",
    wrongAnalysis: "Choosing D: student conflates Bohr model with de Broglie's later explanation (circular orbit = whole number of wavelengths). Both are correct but answer D is incomplete as stated.",
    perSource: "CBSE Class 12 Ch 12; Atomic structure PER (McKagan et al. 2009)"
  },
  {
    id: "PER-092", topic: "Fluid Mechanics & Properties of Matter", subtopic: "Archimedes' Principle",
    type: "conceptual", skill: "E", level: "medium",
    question: "A steel ship floats while a steel ball sinks. Both are made of steel. Why?",
    options: ["The ship is lighter than the ball", "The ship displaces more water (due to its hollow shape), creating a buoyant force equal to or greater than its weight", "The ship's hull repels water", "Steel floats in salt water but not fresh water"],
    correct: 1,
    misconception: "Students think floating depends only on material, not shape/average density.",
    explanation: "By Archimedes' Principle, buoyant force = weight of fluid displaced. The ship's hull traps air, increasing the volume of water displaced. When buoyant force \u2265 total weight (ship + contents + air), it floats. Average density of ship (including air inside) < density of water.",
    wrongAnalysis: "Choosing A: student assumes the ship must be lighter. The ship is heavier in total mass than the ball \u2013 it floats due to geometry, not mass.",
    perSource: "Archimedes' Principle PER \u2013 Loverude et al. (2003); CBSE Class 11 Ch 10"
  },
];

/* ============================================
   STATE
   ============================================ */
let state = {
  mode: 'student',
  step: 1,
  questions: FALLBACK_QUESTIONS,
  currentQ: 0,
  studentInfo: {},
  answers: {}, // { Q01: { selected: 1, confidence: 4 }, ... }
  expertSignedIn: false,
  submissions: [], // pulled from Sheets or localStorage
  currentReport: null
};

/* ============================================
   INIT
   ============================================ */
document.addEventListener('DOMContentLoaded', () => {
  setupRevealAnimations();
  setupForms();
  loadQuestionsFromBackend();
  loadSubmissionsFromStorage();
});

function setupRevealAnimations() {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(e => { if (e.isIntersecting) e.target.classList.add('visible'); });
  }, { threshold: 0.1 });
  document.querySelectorAll('.reveal').forEach(el => observer.observe(el));
}

function setupForms() {
  document.getElementById('registrationForm').addEventListener('submit', startAssessment);
  document.getElementById('expertLoginForm').addEventListener('submit', signInExpert);
}

/* ============================================
   MODE SWITCHING
   ============================================ */
function switchMode(mode) {
  state.mode = mode;
  document.querySelectorAll('.mode-tab').forEach(t => {
    t.classList.toggle('active', t.dataset.mode === mode);
    t.setAttribute('aria-selected', t.dataset.mode === mode);
  });
  document.getElementById('studentView').classList.toggle('hidden', mode !== 'student');
  document.getElementById('expertView').classList.toggle('hidden', mode !== 'expert');
  // close mobile menu if open
  document.getElementById('navLinks').classList.remove('open');
  // scroll to assessment area
  setTimeout(() => {
    document.getElementById('assessment').scrollIntoView({ behavior: 'smooth', block: 'start' });
  }, 50);
}

function toggleMenu() {
  document.getElementById('navLinks').classList.toggle('open');
}

/* ============================================
   STUDENT FLOW
   ============================================ */
function startAssessment(e) {
  e.preventDefault();
  state.studentInfo = {
    name: document.getElementById('fullName').value.trim(),
    email: document.getElementById('email').value.trim(),
    phone: document.getElementById('phone').value.trim(),
    grade: document.getElementById('grade').value,
    school: document.getElementById('school').value.trim(),
    topic: document.getElementById('topic').value,
    goal: document.getElementById('goal').value.trim()
  };

  // Build the question set: filter by selected topic, or pick a random mix across all topics
  const allQs = state.questions.length ? state.questions : FALLBACK_QUESTIONS;
  let selected;
  if (state.studentInfo.topic === 'Mixed (all topics)' || !state.studentInfo.topic) {
    // Sample one from each topic to maximize coverage; cap at 10
    const byTopic = {};
    allQs.forEach(q => { (byTopic[q.topic] = byTopic[q.topic] || []).push(q); });
    selected = [];
    Object.keys(byTopic).forEach(t => {
      const pool = byTopic[t];
      selected.push(pool[Math.floor(Math.random() * pool.length)]);
    });
    // If <10, top up with random; if >10, trim to 10
    while (selected.length < 10 && allQs.length > selected.length) {
      const cand = allQs[Math.floor(Math.random() * allQs.length)];
      if (!selected.find(s => s.id === cand.id)) selected.push(cand);
    }
    selected = selected.slice(0, 10);
  } else {
    // Filter to chosen topic
    const filtered = allQs.filter(q => q.topic === state.studentInfo.topic);
    if (filtered.length === 0) {
      // Fallback: use everything if no match
      selected = allQs.slice(0, 10);
    } else {
      // Shuffle and take up to 10
      const shuffled = [...filtered].sort(() => Math.random() - 0.5);
      selected = shuffled.slice(0, Math.min(10, shuffled.length));
    }
  }
  state.questions = selected;

  state.currentQ = 0;
  state.answers = {};
  document.getElementById('studentStep1').classList.add('hidden');
  document.getElementById('studentStep2').classList.remove('hidden');
  document.getElementById('qTotal').textContent = state.questions.length;
  document.getElementById('qTopicName').textContent = state.studentInfo.topic;
  renderQuestion();
}

function renderQuestion() {
  const q = state.questions[state.currentQ];
  const ans = state.answers[q.id] || {};
  document.getElementById('qCurrent').textContent = state.currentQ + 1;
  document.getElementById('progressFill').style.width = ((state.currentQ + 1) / state.questions.length * 100) + '%';

  const skillNames = { A: 'Conceptual', B: 'Visualization', C: 'Mathematical', D: 'Multi-step', E: 'Misconception trap', F: 'Application' };

  let html = `
    <div class="question-meta">
      <span class="tag navy">${q.id}</span>
      <span class="tag">${(q.type || '').replace(/\b\w/g, c => c.toUpperCase()).replace(/-/g, ' / ')}</span>
      <span class="tag orange">Skill · ${skillNames[q.skill] || q.skill}</span>
      ${q.misconception ? `<span class="tag" style="background:rgba(194,58,58,.08);color:var(--red);border-color:rgba(194,58,58,.2);">⚠ Trap</span>` : ''}
    </div>
    <p class="question-text">${q.question || q.text}</p>
    <div class="options">
  `;
  q.options.forEach((opt, i) => {
    const letter = String.fromCharCode(65 + i);
    const sel = ans.selected === i ? 'selected' : '';
    html += `<div class="option ${sel}" onclick="selectOption(${i})"><span class="option-letter">${letter}</span><span>${opt}</span></div>`;
  });
  html += `</div>
    <div class="confidence-block">
      <div class="confidence-label">How confident are you in your answer?</div>
      <div class="confidence-scale">
  `;
  const labels = ['Guess', 'Unsure', 'Maybe', 'Pretty sure', 'Very sure'];
  for (let c = 1; c <= 5; c++) {
    const sel = ans.confidence === c ? 'selected' : '';
    html += `<div class="confidence-btn ${sel}" onclick="selectConfidence(${c})"><span class="num">${c}</span><span class="lbl">${labels[c-1]}</span></div>`;
  }
  html += `</div></div>`;

  document.getElementById('questionContent').innerHTML = html;
  document.getElementById('prevBtn').style.visibility = state.currentQ === 0 ? 'hidden' : 'visible';
  document.getElementById('nextBtn').innerHTML = (state.currentQ === state.questions.length - 1) ?
    'Submit assessment <span class="arrow">→</span>' : 'Next <span class="arrow">→</span>';
}

function selectOption(i) {
  const q = state.questions[state.currentQ];
  if (!state.answers[q.id]) state.answers[q.id] = {};
  state.answers[q.id].selected = i;
  renderQuestion();
}

function selectConfidence(c) {
  const q = state.questions[state.currentQ];
  if (!state.answers[q.id]) state.answers[q.id] = {};
  state.answers[q.id].confidence = c;
  renderQuestion();
}

function prevQuestion() {
  if (state.currentQ > 0) { state.currentQ--; renderQuestion(); }
}

function nextQuestion() {
  const q = state.questions[state.currentQ];
  const ans = state.answers[q.id];
  if (!ans || ans.selected === undefined || !ans.confidence) {
    showModal('Hold on', 'Please select an answer AND a confidence rating before continuing.');
    return;
  }
  if (state.currentQ < state.questions.length - 1) {
    state.currentQ++;
    renderQuestion();
    document.getElementById('studentStep2').scrollIntoView({ behavior: 'smooth', block: 'start' });
  } else {
    submitAssessment();
  }
}

async function submitAssessment() {
  const submission = buildSubmission();
  state.submissions.push(submission);
  saveSubmissionsToStorage();

  // Try to send to backend
  if (APPS_SCRIPT_URL) {
    try {
      await fetch(APPS_SCRIPT_URL, {
        method: 'POST',
        mode: 'no-cors',
        headers: { 'Content-Type': 'text/plain;charset=utf-8' },
        body: JSON.stringify({ action: 'submit', payload: submission })
      });
    } catch (err) { console.warn('Backend submission failed (saved locally):', err); }
  }

  document.getElementById('refId').textContent = submission.refId;
  document.getElementById('confirmName').textContent = submission.student.name;
  document.getElementById('confirmEmail').textContent = submission.student.email;
  document.getElementById('studentStep2').classList.add('hidden');
  document.getElementById('studentStep3').classList.remove('hidden');
  window.scrollTo({ top: document.getElementById('assessment').offsetTop - 80, behavior: 'smooth' });
}

function buildSubmission() {
  // Compute analytics
  const refId = 'PER-' + Date.now().toString(36).toUpperCase().slice(-6);
  let correct = 0, totalConfidence = 0;
  const details = state.questions.map(q => {
    const a = state.answers[q.id] || {};
    const isCorrect = a.selected === q.correct;
    if (isCorrect) correct++;
    totalConfidence += (a.confidence || 0);
    return {
      qid: q.id, type: q.type, skill: q.skill, misconception: q.misconception,
      selected: a.selected, correct: q.correct, isCorrect,
      confidence: a.confidence || 0
    };
  });
  const accuracy = Math.round((correct / state.questions.length) * 100);
  const avgConfidence = (totalConfidence / state.questions.length).toFixed(2);

  // Confidence × correctness matrix
  let mastery = 0, weakConfidence = 0, strongMisconception = 0, missingFoundation = 0;
  details.forEach(d => {
    const high = d.confidence >= 4;
    if (d.isCorrect && high) mastery++;
    else if (d.isCorrect && !high) weakConfidence++;
    else if (!d.isCorrect && high) strongMisconception++;
    else missingFoundation++;
  });

  // Skill scoring
  const skills = { A: [0,0], B: [0,0], C: [0,0], D: [0,0], E: [0,0], F: [0,0] };
  details.forEach(d => {
    if (skills[d.skill]) {
      skills[d.skill][1]++;
      if (d.isCorrect) skills[d.skill][0]++;
    }
  });

  // Classification
  const concept = (skills.A[0] + skills.E[0]) / Math.max(1, skills.A[1] + skills.E[1]);
  const math = (skills.C[0] + skills.D[0]) / Math.max(1, skills.C[1] + skills.D[1]);
  let learnerType = 'D';
  if (concept >= 0.6 && math >= 0.6) learnerType = 'A';
  else if (concept >= 0.6 && math < 0.6) learnerType = 'B';
  else if (concept < 0.6 && math >= 0.6) learnerType = 'C';
  else learnerType = 'D';

  // Misconceptions detected (wrong answers on misconception-flagged Qs)
  // Pull rich data from the question itself so the report can show research-grade explanations
  const misconceptionsRich = details
    .filter(d => d.misconception && !d.isCorrect)
    .map(d => {
      const q = state.questions.find(qq => qq.id === d.qid);
      return {
        tag: q.misconception,
        explanation: q.explanation || '',
        wrongAnalysis: q.wrongAnalysis || '',
        perSource: q.perSource || '',
        topic: q.topic || ''
      };
    });
  // Also keep simple string list for backwards compat
  const misconceptions = misconceptionsRich.map(m => m.tag);

  return {
    refId,
    submittedAt: new Date().toISOString(),
    student: state.studentInfo,
    answers: details,
    analytics: {
      accuracy, correct, total: state.questions.length, avgConfidence,
      mastery, weakConfidence, strongMisconception, missingFoundation,
      skills, learnerType, misconceptions, misconceptionsRich
    },
    status: 'pending', // 'pending' | 'sent'
    expertNotes: ''
  };
}

function resetStudent() {
  document.getElementById('registrationForm').reset();
  document.getElementById('studentStep1').classList.remove('hidden');
  document.getElementById('studentStep2').classList.add('hidden');
  document.getElementById('studentStep3').classList.add('hidden');
  state.currentQ = 0;
  state.answers = {};
  window.scrollTo({ top: document.getElementById('assessment').offsetTop - 80, behavior: 'smooth' });
}

/* ============================================
   EXPERT FLOW
   ============================================ */
function signInExpert(e) {
  e.preventDefault();
  const code = document.getElementById('expertCode').value.trim();
  if (code !== EXPERT_ACCESS_CODE) {
    showModal('Access denied', 'The access code is incorrect. Please contact your EduAakashaa administrator.');
    return;
  }
  state.expertSignedIn = true;
  document.getElementById('expertLogin').classList.add('hidden');
  document.getElementById('expertDashboard').classList.remove('hidden');
  refreshSubmissions();
}

function logoutExpert() {
  state.expertSignedIn = false;
  document.getElementById('expertCode').value = '';
  document.getElementById('expertLogin').classList.remove('hidden');
  document.getElementById('expertDashboard').classList.add('hidden');
  document.getElementById('expertReport').classList.add('hidden');
  document.getElementById('expertReport').innerHTML = '';
}

async function refreshSubmissions() {
  if (APPS_SCRIPT_URL) {
    try {
      const res = await fetch(APPS_SCRIPT_URL + '?action=list');
      const data = await res.json();
      if (data && Array.isArray(data.submissions)) {
        state.submissions = data.submissions;
        saveSubmissionsToStorage();
      }
    } catch (err) { console.warn('Could not pull from backend, using local data:', err); }
  }
  renderSubmissions();
}

function renderSubmissions() {
  const tbody = document.getElementById('submissionTbody');
  const subs = [...state.submissions].reverse();

  // Stats
  document.getElementById('statPending').textContent = subs.filter(s => s.status === 'pending').length;
  document.getElementById('statReviewed').textContent = subs.filter(s => s.status === 'reviewed').length;
  document.getElementById('statGenerated').textContent = subs.filter(s => s.status === 'generated').length;
  document.getElementById('statSent').textContent = subs.filter(s => s.status === 'sent').length;

  if (!subs.length) {
    tbody.innerHTML = `<tr><td colspan="8" style="text-align:center;padding:40px;color:var(--muted);">No submissions yet. Students who complete the diagnostic will appear here.</td></tr>`;
    return;
  }

  const statusLabels = {
    pending:   { cls: 'pending',   text: '01 · Pending'   },
    reviewed:  { cls: 'reviewed',  text: '02 · Reviewed'  },
    generated: { cls: 'generated', text: '03 · PDF Ready' },
    sent:      { cls: 'sent',      text: '04 · Sent'      }
  };

  tbody.innerHTML = subs.map(s => {
    const date = new Date(s.submittedAt);
    const dateStr = date.toLocaleDateString('en-IN', { day: '2-digit', month: 'short', year: 'numeric' });
    const timeStr = date.toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit' });
    const typeLabel = { A: 'Type A · Strong', B: 'Type B · Concept+', C: 'Type C · Math+', D: 'Type D · Building' };
    const sl = statusLabels[s.status] || statusLabels.pending;
    return `
      <tr>
        <td><div class="student-cell"><span class="name">${escapeHtml(s.student.name)}</span><span class="email">${escapeHtml(s.student.email)}</span></div></td>
        <td>${escapeHtml(s.student.grade || '—')}</td>
        <td>${escapeHtml(s.student.topic || '—')}</td>
        <td><span style="font-family:'JetBrains Mono';font-size:12px;">${dateStr}<br><span style="color:var(--muted);">${timeStr}</span></span></td>
        <td><strong>${s.analytics.accuracy}%</strong></td>
        <td><span class="type-badge ${s.analytics.learnerType}">${typeLabel[s.analytics.learnerType]}</span></td>
        <td><span class="type-badge ${sl.cls}">${sl.text}</span></td>
        <td><button class="btn-primary btn-sm" onclick="openReport('${s.refId}')">Open →</button></td>
      </tr>
    `;
  }).join('');
}

function openReport(refId) {
  const sub = state.submissions.find(s => s.refId === refId);
  if (!sub) return;
  state.currentReport = sub;
  document.getElementById('expertDashboard').classList.add('hidden');
  document.getElementById('expertReport').classList.remove('hidden');
  renderReport(sub);
}

function backToDashboard() {
  document.getElementById('expertReport').classList.add('hidden');
  document.getElementById('expertDashboard').classList.remove('hidden');
  document.getElementById('expertReport').innerHTML = '';
}

/* ============================================
   REPORT RENDERING (full marketing version)
   ============================================ */
function renderReport(sub) {
  const a = sub.analytics;
  const date = new Date(sub.submittedAt).toLocaleString('en-IN', { dateStyle: 'medium', timeStyle: 'short' });
  const typeName = {
    A: 'Conceptual + Analytical',
    B: 'Conceptual Strong, Math Developing',
    C: 'Math Strong, Conceptual Developing',
    D: 'Foundation Builder'
  };
  const typeDesc = {
    A: 'Excellent grasp of physics concepts AND mathematical execution. Ready to push into challenging JEE-Adv / Olympiad-level problems.',
    B: 'Strong intuition for physics, but mathematical execution needs sharpening. Focus on disciplined formula derivation and step-wise solving.',
    C: 'Crunches numbers cleanly, but conceptual reasoning is fragile. Prioritise mental-model building, diagrams, and "explain in your own words".',
    D: 'Building foundations. Most growth will come from clearing common misconceptions before drilling problems. We have a clear plan for you.'
  };

  const skillNames = { A: 'Conceptual', B: 'Visual', C: 'Math', D: 'Multi-step', E: 'Misconception', F: 'Application' };
  const skillScores = Object.keys(a.skills).map(k => {
    const [c, t] = a.skills[k];
    return t > 0 ? Math.round((c / t) * 100) : 0;
  });
  const uniqueMisconceptions = [...new Set(a.misconceptions)];
  const plan = generate7DayPlan(a);
  const gaps = generateGapList(a, skillScores);

  // Workflow stepper
  const stages = ['pending', 'reviewed', 'generated', 'sent'];
  const stageIdx = stages.indexOf(sub.status || 'pending');
  const stageLabels = ['01 Submitted', '02 Reviewed', '03 PDF Generated', '04 Sent'];
  const stepperHtml = stages.map((st, i) => {
    let cls = '';
    if (i < stageIdx) cls = 'done';
    else if (i === stageIdx) cls = 'active';
    return `<div class="workflow-step ${cls}"><span class="dot">${i < stageIdx ? '✓' : (i+1).toString().padStart(2,'0')}</span><span class="label">${stageLabels[i].split(' ').slice(1).join(' ')}</span></div>${i < stages.length - 1 ? '<span class="workflow-arrow">→</span>' : ''}`;
  }).join('');

  // Action buttons depending on status
  let actionButtonsHtml = '';
  const status = sub.status || 'pending';
  if (status === 'pending') {
    actionButtonsHtml = `<button class="btn-primary btn-sm" onclick="markReviewed('${sub.refId}')">Mark as Reviewed <span class="arrow">→</span></button>`;
  } else if (status === 'reviewed') {
    actionButtonsHtml = `<button class="btn-primary btn-sm" id="genPdfBtn_${sub.refId}" onclick="generatePdf('${sub.refId}')">Generate PDF Report <span class="arrow">→</span></button>`;
  } else if (status === 'generated') {
    actionButtonsHtml = `<button class="btn-primary btn-sm" id="sendBtn_${sub.refId}" onclick="sendReport('${sub.refId}')">Send to Student <span class="arrow">→</span></button>`;
  } else if (status === 'sent') {
    actionButtonsHtml = `<button class="btn-ghost btn-sm" onclick="generatePdf('${sub.refId}', true)">Re-generate PDF</button> <button class="btn-ghost btn-sm" onclick="sendReport('${sub.refId}', true)">Re-send Email</button>`;
  }

  // PDF link card if generated
  const pdfCardHtml = sub.pdfUrl ? `
    <div class="pdf-result-card">
      <div class="ico"><svg viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg></div>
      <div class="info">
        <h5>PDF report saved to Google Drive</h5>
        <p>Filename: <strong>EduAakashaa-Report-${sub.refId}.pdf</strong></p>
      </div>
      <a href="${sub.pdfUrl}" target="_blank" rel="noopener">Open in Drive →</a>
    </div>` : '';

  const sentInfoHtml = (status === 'sent' && sub.sentAt) ? `
    <div class="pdf-result-card" style="background:rgba(31,139,92,.06);border-color:rgba(31,139,92,.25);">
      <div class="ico"><svg viewBox="0 0 24 24"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg></div>
      <div class="info">
        <h5>Report sent to ${escapeHtml(sub.student.name)}</h5>
        <p>Email delivered to <strong>${escapeHtml(sub.student.email)}</strong> on ${new Date(sub.sentAt).toLocaleString('en-IN', { dateStyle: 'medium', timeStyle: 'short' })}</p>
      </div>
    </div>` : '';

  const html = `
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:20px;flex-wrap:wrap;gap:12px;">
      <button class="btn-ghost btn-sm" onclick="backToDashboard()">← Back to dashboard</button>
      <div style="display:flex;gap:10px;flex-wrap:wrap;">
        ${actionButtonsHtml}
        <button class="btn-ghost btn-sm" onclick="window.print()">Print</button>
      </div>
    </div>

    <!-- Workflow stepper -->
    <div class="workflow-stepper">${stepperHtml}</div>

    ${pdfCardHtml}
    ${sentInfoHtml}

    <!-- The actual report - this whole element is what gets converted to PDF -->
    <div class="report-section" id="printableReport">
      <div class="report-header">
        <span class="eyebrow" style="background:rgba(255,255,255,0.08);color:#fff;border-color:rgba(255,255,255,0.18);">PER Diagnostic Report · ${sub.refId}</span>
        <h2 style="color:#fff;margin-top:14px;font-size:42px;">Personal report for <em style="color:var(--orange);">${escapeHtml(sub.student.name)}</em></h2>
        <p style="color:rgba(255,255,255,0.85);margin-top:8px;">${escapeHtml(sub.student.topic)} · ${escapeHtml(sub.student.grade)}</p>
        <div class="report-meta-grid">
          <div class="report-meta-item"><div class="lbl">Submitted</div><div class="val">${date}</div></div>
          <div class="report-meta-item"><div class="lbl">Accuracy</div><div class="val">${a.accuracy}% · ${a.correct}/${a.total}</div></div>
          <div class="report-meta-item"><div class="lbl">Avg confidence</div><div class="val">${a.avgConfidence} / 5</div></div>
          <div class="report-meta-item"><div class="lbl">Learner type</div><div class="val">Type ${a.learnerType}</div></div>
        </div>
      </div>

      <div class="report-body">

        <!-- Promo banner #1 -->
        <div class="report-promo-banner">
          <div>
            <h4>Want to walk through this report with an expert?</h4>
            <p>Book a FREE 30-minute counselling session — no commitment, no upsell.</p>
          </div>
          <a href="https://www.eduaakashaa.in/contact-us" target="_blank" rel="noopener">Expert Guidance →</a>
        </div>

        <!-- Classification -->
        <h3 class="report-section-title">Your learner profile</h3>
        <div class="classification-banner">
          <div class="class-icon ${a.learnerType}">${a.learnerType}</div>
          <div>
            <span class="eyebrow" style="margin-bottom:8px;background:rgba(14,58,138,.06);border-color:rgba(14,58,138,.18);color:var(--navy);">Validated by FCI · CSEM · FMCE Frameworks</span>
            <h4 style="font-size:24px;margin-top:10px;">${typeName[a.learnerType]}</h4>
            <p style="color:var(--ink);margin-top:8px;font-size:15px;line-height:1.55;">${typeDesc[a.learnerType]}</p>
          </div>
        </div>

        <!-- Charts -->
        <h3 class="report-section-title">Performance breakdown</h3>
        <div class="chart-grid">
          <div class="chart-card">
            <h4>Skill profile</h4>
            <p class="note">% accuracy across the six skill dimensions</p>
            <div class="chart-canvas-wrap"><canvas id="skillChart_${sub.refId}"></canvas></div>
          </div>
          <div class="chart-card">
            <h4>Question-type accuracy</h4>
            <p class="note">Where strengths and gaps cluster</p>
            <div class="chart-canvas-wrap"><canvas id="typeChart_${sub.refId}"></canvas></div>
          </div>
        </div>

        <!-- Confidence × Correctness matrix -->
        <h3 class="report-section-title">Confidence × Correctness matrix</h3>
        <p style="margin-bottom:16px;">Based on the <strong>Mazur Peer Instruction Model</strong>. This is the most diagnostic view of your responses — it tells us not just <em>what</em> you got wrong, but <em>how dangerously</em> you got it wrong.</p>
        <div class="matrix-grid">
          <div class="matrix-card green">
            <div class="mlbl">✓ Correct + High confidence</div>
            <div class="mval">${a.mastery}</div>
            <div class="mdesc"><strong>Mastery zone.</strong> You know it and you know that you know it.</div>
          </div>
          <div class="matrix-card blue">
            <div class="mlbl">✓ Correct + Low confidence</div>
            <div class="mval">${a.weakConfidence}</div>
            <div class="mdesc"><strong>Underconfidence.</strong> You got it right but doubted yourself — practice will fix this.</div>
          </div>
          <div class="matrix-card red">
            <div class="mlbl">✗ Wrong + High confidence</div>
            <div class="mval">${a.strongMisconception}</div>
            <div class="mdesc"><strong>Strong misconception.</strong> Highest priority — you confidently believed something incorrect.</div>
          </div>
          <div class="matrix-card amber">
            <div class="mlbl">✗ Wrong + Low confidence</div>
            <div class="mval">${a.missingFoundation}</div>
            <div class="mdesc"><strong>Missing foundation.</strong> Concept never landed — needs a teaching reset.</div>
          </div>
        </div>

        <!-- Skill gaps -->
        <h3 class="report-section-title">Strengths &amp; gap areas</h3>
        <div class="gap-list">
          ${gaps.map(g => `
            <div class="gap-item">
              <div class="gap-icon"><svg viewBox="0 0 24 24"><path d="${g.icon}"/></svg></div>
              <div>
                <div class="gtitle">${g.title}</div>
                <div class="gdesc">${g.desc}</div>
              </div>
              <div class="gscore ${g.tier}">${g.score}%</div>
            </div>
          `).join('')}
        </div>

        <!-- Inline CTA #1 -->
        <div class="report-inline-ad">
          <div class="text"><strong>Need targeted practice?</strong> Our JEE Main / NEET physics drill series turns these skill gaps into mastery — visit <a href="https://www.eduaakashaa.in" target="_blank" rel="noopener" style="color:var(--orange);">www.eduaakashaa.in</a></div>
          <a href="https://www.eduaakashaa.in/contact-us" target="_blank" rel="noopener">Talk to Expert →</a>
        </div>

        <!-- Misconceptions -->
        ${(a.misconceptionsRich || []).length > 0 ? `
          <h3 class="report-section-title">Misconceptions detected</h3>
          <p style="margin-bottom:12px;font-size:13px;">Each misconception below was flagged by a research-validated PER trap question. The "What happened" describes the conceptual error; the "Truth" is what the physics actually says.</p>
          ${(a.misconceptionsRich || []).map(m => `
            <div class="misconception-card">
              <h5>⚠ ${escapeHtml(m.tag)} <span style="font-family:'JetBrains Mono';font-size:9.5px;font-weight:500;color:var(--muted);text-transform:uppercase;letter-spacing:0.15em;margin-left:6px;">· ${escapeHtml(m.topic)}</span></h5>
              ${m.wrongAnalysis ? `<p style="margin-top:6px;"><strong style="color:var(--red);">What happened:</strong> ${escapeHtml(m.wrongAnalysis)}</p>` : ''}
              ${m.explanation ? `<p style="margin-top:6px;"><strong style="color:var(--green);">The truth:</strong> ${escapeHtml(m.explanation)}</p>` : ''}
              ${m.perSource ? `<p style="margin-top:8px;font-family:'JetBrains Mono';font-size:9px;color:var(--muted);text-transform:uppercase;letter-spacing:0.15em;">Source · ${escapeHtml(m.perSource)}</p>` : ''}
            </div>
          `).join('')}
        ` : (uniqueMisconceptions.length > 0 ? `
          <h3 class="report-section-title">Misconceptions detected</h3>
          ${uniqueMisconceptions.map(m => `
            <div class="misconception-card">
              <h5>⚠ ${escapeHtml(m)}</h5>
              <p>${escapeHtml(getMisconceptionExplanation(m))}</p>
            </div>
          `).join('')}
        ` : `
          <h3 class="report-section-title">Misconceptions detected</h3>
          <div style="padding:20px;background:rgba(31,139,92,.06);border:1px solid rgba(31,139,92,.2);border-radius:var(--radius-sm);"><strong style="color:var(--green);">✓ Clean run.</strong> No major research-flagged misconceptions triggered. Excellent.</div>
        `)}

        <!-- Counsellor's notes (editable) -->
        <h3 class="report-section-title">Counsellor's note</h3>
        <p style="margin-bottom:14px;">Personal observations from your EduAakashaa counsellor — these will appear in the final PDF and email.</p>
        <textarea id="expertNotesField" placeholder="e.g. Aarav, you're a sharp problem-solver but force diagrams trip you up. Let's focus this week on free body diagrams and Newton's 3rd law pairs. Book a free 30-min slot to walk through.">${escapeHtml(sub.expertNotes || '')}</textarea>
        <div style="margin-top:14px;display:flex;gap:10px;">
          <button class="btn-ghost btn-sm" onclick="saveExpertNotes('${sub.refId}')">Save notes</button>
        </div>

        <!-- 7-day plan -->
        <h3 class="report-section-title">Your 7-day action plan</h3>
        <p style="margin-bottom:18px;">Built from your specific gap pattern. Spend ~60 minutes per day on the listed activity — consistency beats intensity.</p>
        <div class="plan-grid">
          ${plan.map((d, i) => `
            <div class="plan-day">
              <div class="day-num">Day ${i+1}</div>
              <div class="day-title">${d.title}</div>
              <div class="day-desc">${d.desc}</div>
            </div>
          `).join('')}
        </div>

        <!-- WhatsApp community section -->
        <div class="report-whatsapp">
          <div style="position:relative;z-index:1;">
            <span class="eyebrow">Free · Daily · Curated</span>
            <h4 style="margin-top:10px;">Join our <em>WhatsApp community</em>.</h4>
            <p class="lead">Daily physics drills, JEE/NEET strategy, parent guides, and weekly Q&amp;A — all free, all on WhatsApp. Pick the channels that match your goals.</p>
            <div class="wa-grid">
              ${WHATSAPP_CHANNELS.map(ch => `
                <div class="wa-card">
                  <div class="wa-icon"><svg viewBox="0 0 24 24"><path d="M20.52 3.48A11.94 11.94 0 0 0 12 0C5.37 0 0 5.37 0 12c0 2.12.55 4.18 1.6 6L0 24l6.18-1.62A11.94 11.94 0 0 0 12 24c6.63 0 12-5.37 12-12a11.94 11.94 0 0 0-3.48-8.52zM12 22a9.94 9.94 0 0 1-5.1-1.4l-.36-.21-3.66.96.98-3.57-.24-.37A9.94 9.94 0 1 1 22 12 9.94 9.94 0 0 1 12 22zm5.46-7.46c-.3-.15-1.78-.88-2.06-.98-.27-.1-.47-.15-.67.15-.2.3-.78.98-.96 1.18-.18.2-.36.22-.66.07-.3-.15-1.27-.47-2.42-1.5a9.16 9.16 0 0 1-1.7-2.1c-.18-.3-.02-.46.13-.6.13-.13.3-.36.45-.54.15-.18.2-.3.3-.5.1-.2.05-.38-.02-.53-.07-.15-.67-1.6-.92-2.2-.24-.58-.5-.5-.67-.5h-.57c-.2 0-.5.07-.77.38-.27.3-1.02 1-1.02 2.43 0 1.43 1.04 2.81 1.18 3 .15.2 2.05 3.13 4.96 4.4.7.3 1.24.48 1.66.62.7.22 1.33.18 1.84.12.56-.08 1.78-.73 2.03-1.43.25-.7.25-1.3.18-1.43-.07-.13-.27-.2-.57-.36z"/></svg></div>
                  <div class="wa-name">${escapeHtml(ch.name)}</div>
                  <div class="wa-desc">${escapeHtml(ch.desc)}</div>
                  <a class="wa-join" href="${escapeHtml(ch.url)}" target="_blank" rel="noopener">Join Channel →</a>
                </div>
              `).join('')}
            </div>
            <p style="margin-top:14px;font-size:12px;color:rgba(255,255,255,0.7);">Find all channel links and the latest community list at <a href="https://www.eduaakashaa.in" target="_blank" rel="noopener" style="color:#fff;border-bottom:1px solid rgba(255,255,255,0.4);">www.eduaakashaa.in</a></p>
          </div>
        </div>

        <!-- Why us -->
        <h3 class="report-section-title">Why students choose EduAakashaa</h3>
        <div class="report-why-grid">
          <div class="report-why-card">
            <div class="icon"><svg viewBox="0 0 24 24"><path d="M9 12l2 2 4-4M3 12a9 9 0 1 0 18 0 9 9 0 0 0-18 0z"/></svg></div>
            <h5>Evidence-based, not hype</h5>
            <p>Diagnostics built on Physics Education Research (PER) frameworks from Harvard, MIT, and Carnegie Mellon — not generic mock tests.</p>
          </div>
          <div class="report-why-card">
            <div class="icon"><svg viewBox="0 0 24 24"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg></div>
            <h5>1-on-1 PER counsellors</h5>
            <p>Every counsellor is trained in cognitive science, mental model analysis, and confidence calibration — not just exam coaching.</p>
          </div>
          <div class="report-why-card">
            <div class="icon"><svg viewBox="0 0 24 24"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 1 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg></div>
            <h5>India + UAE presence</h5>
            <p>Coimbatore HQ &amp; Dubai office means we understand both Indian boards / JEE / NEET and UAE / international applications.</p>
          </div>
          <div class="report-why-card">
            <div class="icon"><svg viewBox="0 0 24 24"><path d="M12 2l3 7h7l-5.5 4 2 7L12 16l-6.5 4 2-7L2 9h7z"/></svg></div>
            <h5>Free first session</h5>
            <p>30 minutes with a senior counsellor on us. We earn your trust before we earn your fee — that's our principle.</p>
          </div>
        </div>

        <!-- Services -->
        <h3 class="report-section-title">Where students like you go next</h3>
        <div class="report-services-list">
          <div class="report-service-item"><div class="num">01 · DIAGNOSTIC</div><div class="title">PER-based assessments</div><div class="desc">Topic-by-topic for Physics, Chemistry, Math &amp; Biology — JEE, NEET, CBSE, IB.</div></div>
          <div class="report-service-item"><div class="num">02 · COACHING</div><div class="title">JEE / NEET strategy mentorship</div><div class="desc">Personalised 90-day plans. Fortnightly mentor reviews. Test analytics.</div></div>
          <div class="report-service-item"><div class="num">03 · CAREER</div><div class="title">Career &amp; college counselling</div><div class="desc">Stream selection, college shortlisting, JoSAA / NEET counselling support.</div></div>
          <div class="report-service-item"><div class="num">04 · ABROAD</div><div class="title">UAE &amp; overseas applications</div><div class="desc">SAT prep, university applications, visa &amp; documentation guidance.</div></div>
          <div class="report-service-item"><div class="num">05 · PARENTS</div><div class="title">Parent counselling sessions</div><div class="desc">For parents navigating board pressure, career conversations, and exam anxiety.</div></div>
          <div class="report-service-item"><div class="num">06 · COMMUNITY</div><div class="title">Free WhatsApp daily drills</div><div class="desc">15K+ aspirants. One question, one solution, every weekday.</div></div>
        </div>

        <!-- Inline CTA #2 -->
        <div class="report-inline-ad">
          <div class="text"><strong>Stuck on Day 4?</strong> Our mentors are 1-tap away. Free first 30 minutes — no card, no commitment.</div>
          <a href="https://www.eduaakashaa.in/contact-us" target="_blank" rel="noopener">Expert Guidance →</a>
        </div>

        <!-- Testimonial -->
        <div class="report-testimonial">
          <div class="quote">"The PER diagnostic was the first time someone told me <em>why</em> I was getting questions wrong, not just that I was. The 7-day plan looked simple but it changed my entire approach to physics."</div>
          <div class="author">— <strong>Saanvi R.</strong> · JEE Main 2025 · Now at IIT Madras</div>
        </div>

        <!-- Final CTA -->
        <div class="report-final-cta">
          <div class="report-final-cta-inner">
            <span class="eyebrow">FREE · NO CARD · NO COMMITMENT</span>
            <h3>Talk to <em>a real expert</em>.</h3>
            <p>Your first counselling session is on us — 30 minutes, 1-on-1, with a PER-trained counsellor. We'll walk through this exact report and build your next 30 days together.</p>
            <div class="cta-row">
              <a href="https://www.eduaakashaa.in/contact-us" target="_blank" rel="noopener" class="solid">Expert Guidance →</a>
              <a href="https://www.eduaakashaa.in" target="_blank" rel="noopener" class="outline">Visit eduaakashaa.in</a>
            </div>
          </div>
        </div>

        <!-- Signature -->
        <div style="margin-top:36px;padding-top:24px;border-top:1px solid var(--hairline);display:flex;justify-content:space-between;flex-wrap:wrap;gap:12px;">
          <div>
            <div style="font-family:'JetBrains Mono';font-size:11px;text-transform:uppercase;letter-spacing:0.2em;color:var(--muted);">Prepared by</div>
            <div style="font-family:'Fraunces';font-size:18px;font-weight:600;color:var(--navy-ink);margin-top:4px;">EduAakashaa Counselling Team</div>
            <div style="font-size:13px;color:var(--muted);">PER Diagnostic v1.0 · ${date}</div>
          </div>
          <div style="text-align:right;">
            <div style="font-family:'JetBrains Mono';font-size:11px;text-transform:uppercase;letter-spacing:0.2em;color:var(--muted);">Get in touch</div>
            <div style="font-size:14px;color:var(--navy-ink);margin-top:4px;">info@eduaakashaa.com</div>
            <div style="font-size:13px;color:var(--muted);">+91-80157 22706 · +971 50 516 8081</div>
          </div>
        </div>
      </div>
    </div>
  `;

  document.getElementById('expertReport').innerHTML = html;
  window.scrollTo({ top: 0, behavior: 'smooth' });
  setTimeout(() => renderReportCharts(sub, skillScores), 100);
}

function renderReportCharts(sub, skillScores) {
  const skillLabels = ['Conceptual', 'Visual', 'Math', 'Multi-step', 'Misconception\nresistance', 'Application'];
  const skillCanvas = document.getElementById('skillChart_' + sub.refId);
  if (skillCanvas) {
    new Chart(skillCanvas, {
      type: 'radar',
      data: {
        labels: skillLabels,
        datasets: [{
          label: 'Accuracy %',
          data: skillScores,
          backgroundColor: 'rgba(255,107,10,0.18)',
          borderColor: '#FF6B0A',
          borderWidth: 2,
          pointBackgroundColor: '#0E3A8A',
          pointBorderColor: '#fff',
          pointRadius: 5
        }]
      },
      options: {
        responsive: true, maintainAspectRatio: false,
        scales: {
          r: {
            min: 0, max: 100,
            ticks: { stepSize: 25, color: '#5A6278', font: { size: 10 }, backdropColor: 'transparent' },
            grid: { color: '#E8DFC8' },
            angleLines: { color: '#E8DFC8' },
            pointLabels: { color: '#0E1B3D', font: { size: 11, family: 'Plus Jakarta Sans' } }
          }
        },
        plugins: { legend: { display: false } }
      }
    });
  }

  // Question type chart
  const typeMap = {};
  sub.answers.forEach(d => {
    if (!typeMap[d.type]) typeMap[d.type] = [0, 0];
    typeMap[d.type][1]++;
    if (d.isCorrect) typeMap[d.type][0]++;
  });
  const typeLabels = Object.keys(typeMap);
  const typeData = typeLabels.map(t => Math.round((typeMap[t][0] / typeMap[t][1]) * 100));

  const typeCanvas = document.getElementById('typeChart_' + sub.refId);
  if (typeCanvas) {
    new Chart(typeCanvas, {
      type: 'bar',
      data: {
        labels: typeLabels,
        datasets: [{
          label: 'Accuracy %',
          data: typeData,
          backgroundColor: ['#0E3A8A', '#FF6B0A', '#1F8B5C', '#E89A1C', '#0A2560'],
          borderRadius: 8,
          maxBarThickness: 50
        }]
      },
      options: {
        responsive: true, maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: {
          x: { grid: { display: false }, ticks: { color: '#0E1B3D', font: { family: 'Plus Jakarta Sans' } } },
          y: { min: 0, max: 100, ticks: { color: '#5A6278', stepSize: 25 }, grid: { color: '#E8DFC8' } }
        }
      }
    });
  }
}

function generate7DayPlan(a) {
  const t = a.learnerType;
  const plans = {
    A: [
      { title: 'Stretch problems', desc: 'Pick 5 hard JEE-Adv questions on Newton\'s laws. Set 90-min timer.' },
      { title: 'Olympiad sampler', desc: 'Try 2 INPhO mechanics problems. Discuss approach with mentor.' },
      { title: 'Teach back', desc: 'Explain Newton 3 to a junior or sibling in your own words. Record yourself.' },
      { title: 'Mixed practice', desc: 'Do a 30-Q timed mock mixing kinematics + dynamics + work-energy.' },
      { title: 'Error log', desc: 'Re-attempt every question you got wrong. Write WHY you missed it.' },
      { title: 'Multi-rep day', desc: 'For 3 problems, draw FBD + write equations + solve numerically + explain in words.' },
      { title: 'Reflect & plan', desc: 'Identify your weakest skill from the radar chart. Set Week 2 goals.' }
    ],
    B: [
      { title: 'Formula derivations', desc: 'Derive 5 key formulas (a = F/m, v² = u² + 2as, etc.) from scratch.' },
      { title: 'Step-wise solving', desc: 'Pick 5 numerical problems. Write EVERY step — no skipping.' },
      { title: 'Unit dimension drill', desc: 'Practice 20 dimensional analysis problems. Builds calculation discipline.' },
      { title: 'Numerical sprint', desc: 'Time yourself on 10 medium numericals. Aim for under 90 seconds each.' },
      { title: 'Concept-to-math bridge', desc: 'Take 5 conceptual scenarios. Write the equation that models each.' },
      { title: 'Re-attempt errors', desc: 'Go back to questions you got wrong. Solve cleanly with all steps shown.' },
      { title: 'Mixed mock', desc: 'Take a 25-Q timed test. Track time per question.' }
    ],
    C: [
      { title: 'Mental models', desc: 'Watch 2 PhET simulations on Newton\'s laws. Predict THEN observe.' },
      { title: 'FBD drill', desc: 'Draw free-body diagrams for 10 different scenarios — no equations, just diagrams.' },
      { title: 'Explain it back', desc: 'Pick 5 wrong-answer questions. Write a paragraph explaining the physics in plain English.' },
      { title: 'Misconception hunt', desc: 'Read 1 PER paper summary on motion misconceptions. Identify which you held.' },
      { title: 'Conceptual MCQs', desc: 'Do 20 conceptual-only MCQs (no calculation). Focus on reasoning.' },
      { title: 'Real-world transfer', desc: 'Find 3 real-life examples of Newton\'s laws. Explain to a parent.' },
      { title: 'Mixed practice', desc: 'Take a balanced mock and watch if conceptual accuracy improved.' }
    ],
    D: [
      { title: 'Reset & basics', desc: 'Re-read NCERT Chapter 5 (Class 11). Highlight 5 things you didn\'t fully understand.' },
      { title: 'Watch & take notes', desc: 'Watch a high-quality YouTube series on Newton\'s laws (e.g. Khan Academy). Take written notes.' },
      { title: 'Solve along', desc: 'Pick 5 NCERT solved examples. Cover the solution and try first. Compare.' },
      { title: 'Misconception clearing', desc: 'Address each misconception flagged in your report — one at a time.' },
      { title: 'Easy MCQs', desc: 'Attempt 15 easy-level conceptual MCQs. Build confidence.' },
      { title: 'Diagram practice', desc: 'Draw FBDs for 8 scenarios with help from textbook examples.' },
      { title: 'Counsellor session', desc: 'Book your free 30-min EduAakashaa session. We\'ll co-build your Week 2 plan.' }
    ]
  };
  return plans[t];
}

function generateGapList(a, skillScores) {
  const skills = ['A', 'B', 'C', 'D', 'E', 'F'];
  const titles = {
    A: 'Conceptual clarity',
    B: 'Visualization & graph reading',
    C: 'Mathematical execution',
    D: 'Multi-step reasoning',
    E: 'Misconception resistance',
    F: 'Real-world application'
  };
  const descs = {
    A: 'Your grasp of physics ideas in plain language.',
    B: 'Reading and interpreting graphs, diagrams, and FBDs.',
    C: 'Algebra, formula manipulation, calculation accuracy.',
    D: 'Holding multiple steps in working memory.',
    E: 'Resisting research-flagged trap questions.',
    F: 'Connecting physics to everyday scenarios.'
  };
  const icons = {
    A: 'M12 2v20M2 12h20',
    B: 'M3 3v18h18M7 14l4-4 4 4 5-5',
    C: 'M4 4h16v16H4z M9 9h6v6H9z',
    D: 'M3 6h18M3 12h18M3 18h12',
    E: 'M12 9v2m0 4h.01M9 4h6l5 5v6l-5 5H9l-5-5V9z',
    F: 'M3 21l8-8 4 4 6-6'
  };
  return skills.map((k, i) => {
    const score = skillScores[i];
    let tier = 'low';
    if (score >= 75) tier = 'high';
    else if (score >= 50) tier = 'mid';
    return { title: titles[k], desc: descs[k], score, tier, icon: icons[k] };
  });
}

function getMisconceptionExplanation(m) {
  const explanations = {
    "Force-of-motion fallacy": "Many students believe motion REQUIRES a continuous force. In reality, an object in motion stays in motion (Newton 1) — force is needed only to CHANGE velocity, not maintain it.",
    "Position vs velocity confusion": "A horizontal line on a v-t graph shows constant velocity, NOT constant position. Constant position would be a horizontal line on a position-time graph.",
    "Constant velocity requires net force": "At constant velocity, net force = ZERO. The forward push from the engine balances friction & drag exactly. Newton's first law in action.",
    "Heavier objects fall faster": "Galileo's classic — in vacuum, all objects fall with the same acceleration g, regardless of mass. The misconception comes from observing air resistance.",
    "Action-reaction cancellation": "Action-reaction pairs act on DIFFERENT objects, so they never cancel out on the same object. The cart moves because the ground pushes the horse, not the cart.",
    "Slope vs area confusion": "On a force-time graph: AREA under the curve = impulse (change in momentum). SLOPE doesn't have a standard physical meaning here.",
    "Friction always opposes motion": "Friction opposes RELATIVE motion between surfaces. When you walk, your foot pushes back on the ground, so friction on your foot points FORWARD — that's what propels you."
  };
  return explanations[m] || "This misconception was flagged by a research-validated trap. Discuss with your counsellor for a deeper conceptual reset.";
}

/* ============================================
   4-STAGE WORKFLOW: Reviewed → Generated → Sent
   ============================================ */

// STAGE 02: Mark report as reviewed (expert has read and approved)
async function markReviewed(refId) {
  const sub = state.submissions.find(s => s.refId === refId);
  if (!sub) return;

  // Save any expert notes first
  const notesField = document.getElementById('expertNotesField');
  if (notesField) sub.expertNotes = notesField.value;

  sub.status = 'reviewed';
  sub.reviewedAt = new Date().toISOString();
  saveSubmissionsToStorage();

  // Sync to backend
  if (APPS_SCRIPT_URL) {
    try {
      await fetch(APPS_SCRIPT_URL, {
        method: 'POST',
        mode: 'no-cors',
        headers: { 'Content-Type': 'text/plain;charset=utf-8' },
        body: JSON.stringify({ action: 'markReviewed', refId, expertNotes: sub.expertNotes || '' })
      });
    } catch (err) { console.warn('Backend update failed:', err); }
  }

  showModal('✓ Report reviewed', `Report for ${sub.student.name} (${sub.refId}) has been marked as reviewed. Next step: generate the PDF report.`);
  renderReport(sub);
  renderSubmissions();
}

// STAGE 03: Generate PDF report — sends rendered HTML to Apps Script which saves PDF to Google Drive
async function generatePdf(refId, force) {
  const sub = state.submissions.find(s => s.refId === refId);
  if (!sub) return;

  // Save expert notes if textbox exists
  const notesField = document.getElementById('expertNotesField');
  if (notesField) sub.expertNotes = notesField.value;

  if (!APPS_SCRIPT_URL) {
    showModal('Backend not connected', 'PDF generation requires the Google Apps Script backend. Please paste your APPS_SCRIPT_URL into index.html and re-deploy. See setup-guide.md for instructions.');
    return;
  }

  // Visual feedback
  const btn = document.getElementById('genPdfBtn_' + refId);
  if (btn) { btn.innerHTML = '<span class="spinner"></span> Generating PDF…'; btn.disabled = true; }

  // Capture the rendered report HTML (the part that becomes the PDF)
  const reportEl = document.getElementById('printableReport');
  const reportHtml = reportEl ? reportEl.outerHTML : '';
  const fullHtml = buildPdfHtml(sub, reportHtml);

  try {
    const res = await fetch(APPS_SCRIPT_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'text/plain;charset=utf-8' },
      body: JSON.stringify({
        action: 'generatePdf',
        refId,
        html: fullHtml,
        studentName: sub.student.name,
        expertNotes: sub.expertNotes || ''
      })
    });
    const data = await res.json();
    if (data && data.ok) {
      sub.pdfUrl = data.url;
      sub.pdfFileId = data.fileId;
      sub.status = 'generated';
      sub.generatedAt = new Date().toISOString();
      saveSubmissionsToStorage();
      showModal('✓ PDF generated', `Saved to Google Drive: ${data.name}\n\nThe report is now ready to be sent to the student.`);
      renderReport(sub);
      renderSubmissions();
    } else {
      throw new Error((data && data.error) || 'Unknown error');
    }
  } catch (err) {
    if (btn) { btn.innerHTML = 'Generate PDF Report <span class="arrow">→</span>'; btn.disabled = false; }
    showModal('PDF generation failed', 'Could not generate PDF: ' + err.message + '\n\nCheck your Apps Script logs and ensure Drive API access is granted.');
  }
}

// STAGE 04: Send report to student via email from info@eduaakashaa.com
async function sendReport(refId, force) {
  const sub = state.submissions.find(s => s.refId === refId);
  if (!sub) return;

  if (!APPS_SCRIPT_URL) {
    showModal('Backend not connected', 'Email sending requires the Google Apps Script backend deployed under info@eduaakashaa.com. See setup-guide.md.');
    return;
  }

  if (!sub.pdfFileId) {
    showModal('No PDF to send', 'Please generate the PDF first before sending the email.');
    return;
  }

  const btn = document.getElementById('sendBtn_' + refId);
  if (btn) { btn.innerHTML = '<span class="spinner"></span> Sending email…'; btn.disabled = true; }

  try {
    const res = await fetch(APPS_SCRIPT_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'text/plain;charset=utf-8' },
      body: JSON.stringify({
        action: 'sendReport',
        refId,
        pdfFileId: sub.pdfFileId,
        studentEmail: sub.student.email,
        studentName: sub.student.name,
        topic: sub.student.topic,
        learnerType: sub.analytics.learnerType,
        accuracy: sub.analytics.accuracy,
        expertNotes: sub.expertNotes || ''
      })
    });
    const data = await res.json();
    if (data && data.ok) {
      sub.status = 'sent';
      sub.sentAt = new Date().toISOString();
      saveSubmissionsToStorage();
      showModal('✓ Email sent', `Report has been emailed to ${sub.student.name} at ${sub.student.email} from info@eduaakashaa.com.`);
      renderReport(sub);
      renderSubmissions();
    } else {
      throw new Error((data && data.error) || 'Unknown error');
    }
  } catch (err) {
    if (btn) { btn.innerHTML = 'Send to Student <span class="arrow">→</span>'; btn.disabled = false; }
    showModal('Email failed', 'Could not send email: ' + err.message + '\n\nCheck your Apps Script logs and ensure MailApp permissions are granted to the info@eduaakashaa.com account.');
  }
}

// Build a print-ready, self-contained HTML for the PDF
function buildPdfHtml(sub, reportHtml) {
  // Strip the chart canvases — Apps Script's HTML→PDF won't render them
  // We'll keep the data summary in the static elements
  const cleanedHtml = reportHtml
    .replace(/<canvas[^>]*><\/canvas>/g, '')
    .replace(/<div class="chart-canvas-wrap">.*?<\/div>/gs, '<div style="padding:18px;background:#FBF7EE;border-radius:8px;text-align:center;color:#5A6278;font-size:11px;">📊 See interactive charts in your online report at eduaakashaa.in</div>');

  return `<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>EduAakashaa PER Report — ${sub.refId}</title>
<style>
${getReportPrintStyles()}
</style></head>
<body>
${cleanedHtml}
</body></html>`;
}

function getReportPrintStyles() {
  // Return a self-contained CSS bundle for the PDF
  // (Apps Script's HTML→PDF works best with inline CSS, no external fonts)
  return `
    body { font-family: Helvetica, Arial, sans-serif; background: #FBF7EE; color: #0E1B3D; line-height: 1.55; margin: 0; padding: 14mm 12mm; font-size: 12px; }
    h1, h2, h3, h4, h5 { color: #071A44; line-height: 1.2; margin: 0; }
    h2 { font-size: 26px; font-weight: 700; margin-bottom: 6px; }
    h3 { font-size: 18px; font-weight: 600; margin-top: 20px; margin-bottom: 10px; padding-left: 16px; border-left: 3px solid #FF6B0A; }
    h4 { font-size: 15px; font-weight: 600; }
    h5 { font-size: 13px; font-weight: 600; }
    p { margin: 0 0 8px 0; }
    em { color: #FF6B0A; font-style: italic; font-weight: 600; }
    strong { color: #071A44; }
    a { color: #FF6B0A; text-decoration: none; font-weight: 600; }
    .report-section { background: #FFFDF7; border-radius: 12px; overflow: hidden; }
    .report-header { background: linear-gradient(135deg, #0E3A8A 0%, #0A2560 100%); color: #fff; padding: 28px; }
    .report-header h2 { color: #fff !important; }
    .report-header em { color: #FF6B0A !important; }
    .report-header p { color: rgba(255,255,255,0.85); }
    .report-meta-grid { display: table; width: 100%; margin-top: 18px; padding-top: 14px; border-top: 1px solid rgba(255,255,255,0.15); }
    .report-meta-item { display: table-cell; padding-right: 16px; }
    .report-meta-item .lbl { font-size: 9px; color: rgba(255,255,255,0.6); letter-spacing: 0.15em; text-transform: uppercase; margin-bottom: 4px; }
    .report-meta-item .val { font-size: 14px; color: #fff; font-weight: 600; }
    .report-body { padding: 24px; }
    .eyebrow { display: inline-block; font-size: 10px; text-transform: uppercase; letter-spacing: 0.2em; padding: 4px 10px; border: 1px solid #E8DFC8; border-radius: 999px; background: #FFFDF7; color: #0E3A8A; }
    .report-promo-banner { background: #FF6B0A; color: #fff; padding: 16px 20px; border-radius: 10px; margin: 14px 0; }
    .report-promo-banner h4 { color: #fff; }
    .report-promo-banner p { color: rgba(255,255,255,0.92); font-size: 12px; }
    .classification-banner { background: #F5EFDF; border: 1px solid #E8DFC8; border-radius: 12px; padding: 18px; margin: 12px 0; }
    .classification-banner .class-icon { display: inline-block; width: 50px; height: 50px; border-radius: 12px; background: #0E3A8A; color: #fff; text-align: center; line-height: 50px; font-size: 24px; font-weight: 700; vertical-align: top; margin-right: 16px; }
    .matrix-grid { width: 100%; margin: 12px 0; }
    .matrix-card { display: inline-block; width: 47%; padding: 12px; margin: 4px 1%; vertical-align: top; border: 1px solid #E8DFC8; border-radius: 8px; box-sizing: border-box; }
    .matrix-card.green { background: rgba(31,139,92,0.06); border-color: rgba(31,139,92,0.2); }
    .matrix-card.blue { background: rgba(14,58,138,0.05); border-color: rgba(14,58,138,0.18); }
    .matrix-card.amber { background: rgba(232,154,28,0.07); border-color: rgba(232,154,28,0.2); }
    .matrix-card.red { background: rgba(194,58,58,0.06); border-color: rgba(194,58,58,0.2); }
    .matrix-card .mlbl { font-size: 9px; text-transform: uppercase; letter-spacing: 0.15em; margin-bottom: 4px; font-weight: 600; }
    .matrix-card.green .mlbl { color: #1F8B5C; }
    .matrix-card.blue .mlbl { color: #0E3A8A; }
    .matrix-card.amber .mlbl { color: #E89A1C; }
    .matrix-card.red .mlbl { color: #C23A3A; }
    .matrix-card .mval { font-size: 24px; font-weight: 700; color: #071A44; line-height: 1; margin-bottom: 4px; }
    .matrix-card .mdesc { font-size: 11px; color: #0E1B3D; }
    .gap-list { margin: 10px 0; }
    .gap-item { padding: 10px 0; border-bottom: 1px dashed #E8DFC8; }
    .gap-item .gtitle { font-weight: 600; font-size: 13px; color: #071A44; }
    .gap-item .gdesc { font-size: 11px; color: #5A6278; margin-top: 2px; }
    .gap-item .gscore { float: right; font-weight: 700; font-size: 14px; color: #071A44; }
    .gap-item .gap-icon { display: none; }
    .misconception-card { padding: 12px 16px; background: rgba(194,58,58,0.04); border: 1px solid rgba(194,58,58,0.18); border-left: 3px solid #C23A3A; border-radius: 6px; margin-bottom: 8px; }
    .misconception-card h5 { color: #071A44; font-size: 13px; margin-bottom: 4px; }
    .misconception-card p { font-size: 11px; }
    .plan-grid { width: 100%; margin: 12px 0; }
    .plan-day { display: inline-block; width: 13.5%; vertical-align: top; padding: 8px; box-sizing: border-box; border: 1px solid #E8DFC8; background: #FFFDF7; }
    .plan-day .day-num { font-size: 8px; color: #FF6B0A; text-transform: uppercase; letter-spacing: 0.15em; font-weight: 600; }
    .plan-day .day-title { font-size: 11px; font-weight: 600; color: #071A44; margin: 3px 0; }
    .plan-day .day-desc { font-size: 9px; color: #5A6278; line-height: 1.35; }
    .report-whatsapp { background: #075e54; color: #fff; padding: 22px; border-radius: 12px; margin: 14px 0; }
    .report-whatsapp h4 { color: #fff !important; font-size: 18px; }
    .report-whatsapp em { color: #25D366 !important; }
    .report-whatsapp p { color: rgba(255,255,255,0.85); font-size: 12px; }
    .report-whatsapp .eyebrow { background: rgba(255,255,255,0.1) !important; color: #fff !important; border-color: rgba(255,255,255,0.18) !important; }
    .wa-grid { width: 100%; margin-top: 10px; }
    .wa-card { display: inline-block; width: 47%; padding: 12px; margin: 4px 1%; vertical-align: top; background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15); border-radius: 8px; box-sizing: border-box; }
    .wa-card .wa-icon { display: none; }
    .wa-card .wa-name { color: #fff; font-size: 13px; font-weight: 600; margin-bottom: 3px; }
    .wa-card .wa-desc { color: rgba(255,255,255,0.78); font-size: 11px; margin-bottom: 8px; }
    .wa-card .wa-join { display: inline-block; font-size: 9px; background: #25D366; color: #fff !important; padding: 4px 10px; border-radius: 999px; font-weight: 600; text-decoration: none; }
    .report-inline-ad { background: #FFFDF7; border: 2px dashed #FF6B0A; padding: 12px 16px; border-radius: 8px; margin: 12px 0; }
    .report-inline-ad strong { font-size: 12px; }
    .report-inline-ad .text { font-size: 11px; }
    .report-inline-ad a { background: #FF6B0A; color: #fff !important; padding: 5px 10px; border-radius: 999px; font-size: 10px; font-weight: 700; text-transform: uppercase; }
    .report-why-grid { width: 100%; margin: 10px 0; }
    .report-why-card { display: inline-block; width: 47%; padding: 12px; margin: 4px 1%; vertical-align: top; box-sizing: border-box; background: #FFFDF7; border: 1px solid #E8DFC8; border-radius: 8px; }
    .report-why-card .icon { display: none; }
    .report-why-card h5 { color: #071A44; font-size: 13px; margin-bottom: 4px; }
    .report-why-card p { font-size: 11px; color: #5A6278; }
    .report-services-list { width: 100%; margin: 10px 0; }
    .report-service-item { display: inline-block; width: 47%; padding: 10px; margin: 4px 1%; vertical-align: top; box-sizing: border-box; background: #FFFDF7; border: 1px solid #E8DFC8; border-radius: 6px; }
    .report-service-item .num { font-size: 9px; color: #FF6B0A; letter-spacing: 0.15em; font-weight: 700; }
    .report-service-item .title { font-size: 13px; font-weight: 600; color: #071A44; margin: 2px 0; }
    .report-service-item .desc { font-size: 10px; color: #5A6278; }
    .report-testimonial { background: #FFFDF7; border-left: 3px solid #FF6B0A; padding: 14px 18px; border-radius: 6px; margin: 12px 0; }
    .report-testimonial .quote { font-style: italic; font-size: 13px; color: #071A44; margin-bottom: 6px; }
    .report-testimonial .author { font-size: 10px; color: #5A6278; letter-spacing: 0.15em; text-transform: uppercase; }
    .report-final-cta { background: #0A2560; color: #fff; padding: 22px; border-radius: 12px; margin: 14px 0; }
    .report-final-cta h3 { color: #fff !important; border: none !important; padding-left: 0 !important; }
    .report-final-cta em { color: #FF6B0A !important; }
    .report-final-cta p { color: rgba(255,255,255,0.85); }
    .report-final-cta .eyebrow { background: rgba(255,255,255,0.1) !important; color: #fff !important; border-color: rgba(255,255,255,0.18) !important; }
    .report-final-cta .cta-row a { padding: 8px 14px; border-radius: 999px; font-size: 11px; font-weight: 700; margin-right: 6px; }
    .report-final-cta .cta-row a.solid { background: #FF6B0A; color: #fff !important; }
    .report-final-cta .cta-row a.outline { border: 1px solid rgba(255,255,255,0.3); color: #fff !important; }
    textarea { display: none; }
    button, .btn-ghost, .btn-primary, .btn-sm { display: none; }
    .chart-grid { display: none; }
  `;
}

function saveExpertNotes(refId) {
  const sub = state.submissions.find(s => s.refId === refId);
  if (!sub) return;
  sub.expertNotes = document.getElementById('expertNotesField').value;
  saveSubmissionsToStorage();
  showModal('Saved', 'Notes saved locally. They will be included in the email when you mark this report as sent.');
}

function exportCSV() {
  if (!state.submissions.length) {
    showModal('Nothing to export', 'No submissions to export yet.');
    return;
  }
  const rows = [['RefID','Name','Email','Phone','Grade','School','Topic','Submitted','Accuracy','AvgConfidence','LearnerType','Mastery','Underconfident','StrongMisconception','MissingFoundation','Status','Misconceptions']];
  state.submissions.forEach(s => {
    const a = s.analytics;
    rows.push([
      s.refId, s.student.name, s.student.email, s.student.phone, s.student.grade,
      s.student.school, s.student.topic, s.submittedAt,
      a.accuracy, a.avgConfidence, a.learnerType,
      a.mastery, a.weakConfidence, a.strongMisconception, a.missingFoundation,
      s.status, [...new Set(a.misconceptions)].join(' | ')
    ]);
  });
  const csv = rows.map(r => r.map(c => `"${String(c||'').replace(/"/g,'""')}"`).join(',')).join('\n');
  const blob = new Blob([csv], { type: 'text/csv' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url; a.download = `eduaakashaa-submissions-${Date.now()}.csv`;
  document.body.appendChild(a); a.click(); document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

/* ============================================
   STORAGE & BACKEND
   ============================================ */
function saveSubmissionsToStorage() {
  try {
    localStorage.setItem('eduaakashaa_submissions', JSON.stringify(state.submissions));
  } catch (e) { /* localStorage unavailable */ }
}

function loadSubmissionsFromStorage() {
  try {
    const data = localStorage.getItem('eduaakashaa_submissions');
    if (data) state.submissions = JSON.parse(data);
  } catch (e) { state.submissions = []; }
}

async function loadQuestionsFromBackend() {
  if (!APPS_SCRIPT_URL) return;
  try {
    const res = await fetch(APPS_SCRIPT_URL + '?action=questions');
    const data = await res.json();
    if (data && Array.isArray(data.questions) && data.questions.length > 0) {
      state.questions = data.questions;
    }
  } catch (err) {
    console.warn('Using fallback questions (backend unavailable):', err);
  }
}

/* ============================================
   UTILITIES
   ============================================ */
function showModal(title, body) {
  document.getElementById('modalTitle').textContent = title;
  document.getElementById('modalBody').textContent = body;
  document.getElementById('modalOverlay').classList.add('active');
}
function closeModal() {
  document.getElementById('modalOverlay').classList.remove('active');
}
function escapeHtml(s) {
  if (s === null || s === undefined) return '';
  return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;').replace(/'/g,'&#39;');
}

;

	const heightObserver = new ResizeObserver(([{ contentRect }]) => {
		window.parent.postMessage({ action: 'iframeHeightUpdated', height: contentRect.height, id: 'zcMZ8b' }, '*');
	});

	heightObserver.observe(document.documentElement);
