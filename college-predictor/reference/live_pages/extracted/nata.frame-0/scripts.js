
// ===== TAB NAVIGATION =====
function showTab(id) {
  document.querySelectorAll('.section').forEach(function(s) { s.classList.remove('active'); });
  document.getElementById('sec-' + id).classList.add('active');
  document.querySelectorAll('.tab-btn').forEach(function(b) { b.classList.remove('active'); });
  event.target.classList.add('active');
}

// ===== QUIZ =====
var questions = [
  { q: "When you see a beautiful building, what is your first thought?", a: ["I want to design something like this!", "I wonder how it was built structurally."] },
  { q: "Which activity do you enjoy more?", a: ["Sketching, drawing, or painting", "Solving math puzzles or coding"] },
  { q: "Your ideal weekend project would be:", a: ["Designing a dream house layout on paper", "Building a robot or writing a program"] },
  { q: "In a group project, you naturally take charge of:", a: ["The visual design, layout, and presentation look", "The data analysis, logic, and technical parts"] },
  { q: "Which subject excites you the most?", a: ["Art, History, Geography, Environmental Studies", "Physics, Mathematics, Computer Science"] },
  { q: "How do you prefer to solve problems?", a: ["Visually \u2014 diagrams, models, spatial thinking", "Analytically \u2014 formulas, data, step-by-step logic"] },
  { q: "Your dream workspace looks like:", a: ["A creative studio with models, sketches, mood boards", "A tech lab with computers, circuits, whiteboards"] },
  { q: "Which career sounds more exciting?", a: ["Designing sustainable cities and green buildings", "Developing AI systems or launching a tech startup"] },
  { q: "When you travel to a new place, you notice:", a: ["The architecture, colors, spaces, landscape design", "The transportation systems, technology, infrastructure"] },
  { q: "What motivates you more?", a: ["Creating something visually beautiful that people experience", "Building efficient systems that solve real-world problems"] }
];

var currentQ = 0;
var ans = [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1];

function renderQuiz() {
  var area = document.getElementById('quizArea');
  var html = '';
  html += '<div class="qprog"><div class="qprog-bar" style="width:' + ((currentQ + 1) * 10) + '%"></div></div>';
  html += '<div class="qnum">Question ' + (currentQ + 1) + ' of 10</div>';
  html += '<h3>' + questions[currentQ].q + '</h3>';
  html += '<div class="qopts">';
  for (var j = 0; j < 2; j++) {
    var sel = ans[currentQ] === j ? ' sel' : '';
    html += '<button class="qopt' + sel + '" onclick="pickAnswer(' + currentQ + ',' + j + ')">' + questions[currentQ].a[j] + '</button>';
  }
  html += '</div>';
  html += '<div class="qnav">';
  html += '<button class="qbtn qbtn-prev" onclick="prevQ()"' + (currentQ === 0 ? ' disabled' : '') + '>\u2190 Previous</button>';
  html += '<button class="qbtn qbtn-next" onclick="nextQ()"' + (ans[currentQ] === -1 ? ' style="opacity:.4;cursor:not-allowed"' : '') + '>' + (currentQ === 9 ? 'See Results' : 'Next \u2192') + '</button>';
  html += '</div>';
  area.innerHTML = html;
}

function pickAnswer(qi, ai) {
  ans[qi] = ai;
  renderQuiz();
}

function nextQ() {
  if (ans[currentQ] === -1) return;
  if (currentQ < 9) { currentQ++; renderQuiz(); }
  else { showResults(); }
}

function prevQ() {
  if (currentQ > 0) { currentQ--; renderQuiz(); }
}

function showResults() {
  var archS = 0, engS = 0;
  for (var i = 0; i < 10; i++) { if (ans[i] === 0) archS += 10; else engS += 10; }

  var icon, title, desc, advice, iconBg;
  if (archS >= 70) {
    icon = '\u{1F3DB}\uFE0F'; iconBg = 'rgba(8,145,178,.2)';
    title = 'You\'re a Natural <span style="color:#22D3EE">Architect!</span>';
    desc = 'Your creative instincts, spatial thinking, and design sensibility point strongly toward Architecture.';
    advice = '<strong>Recommended Path:</strong> Prepare for NATA 2026. Start daily sketching practice. Explore design thinking workshops. Target top NIRF-ranked architecture colleges like IIT Roorkee, NIT Calicut, or CEPT University.';
  } else if (engS >= 70) {
    icon = '\u2699\uFE0F'; iconBg = 'rgba(245,158,11,.2)';
    title = 'You\'re a Born <span style="color:#F59E0B">Engineer!</span>';
    desc = 'Your analytical mind, logical thinking, and technical curiosity align perfectly with Engineering.';
    advice = '<strong>Recommended Path:</strong> Focus on JEE Main/Advanced or state CET preparation. Explore CS, Mechanical, or ECE based on interests. Target IITs and NITs. Build projects to strengthen your portfolio.';
  } else {
    icon = '\u{1F4A1}'; iconBg = 'rgba(139,92,246,.2)';
    title = 'You Have a <span style="color:#8B5CF6">Dual Aptitude!</span>';
    desc = 'You show strengths in both creative and analytical thinking. Exciting crossover opportunities await.';
    advice = '<strong>Recommended Path:</strong> Explore hybrid fields like Computational Design, Smart Cities, BIM, or Industrial Design. Consider preparing for both NATA and JEE simultaneously.';
  }

  var area = document.getElementById('quizArea');
  var html = '<div class="result-box">';
  html += '<div class="result-icon" style="background:' + iconBg + '">' + icon + '</div>';
  html += '<h2 style="font-size:24px;font-weight:800;margin-bottom:8px">' + title + '</h2>';
  html += '<div class="result-scores">';
  html += '<div><div style="font-size:28px;font-weight:800;color:#22D3EE">' + archS + '%</div><div style="font-size:11px;opacity:.5">Architecture</div></div>';
  html += '<div><div style="font-size:28px;font-weight:800;color:#F59E0B">' + engS + '%</div><div style="font-size:11px;opacity:.5">Engineering</div></div>';
  html += '</div>';
  html += '<p style="color:rgba(255,255,255,.7);max-width:450px;margin:0 auto;font-size:14px">' + desc + '</p>';
  html += '<div class="result-advice">' + advice + '</div>';
  html += '<button class="qbtn qbtn-next" onclick="resetQuiz()" style="margin-top:20px">Retake Test</button>';
  html += '</div>';
  area.innerHTML = html;
}

function resetQuiz() {
  currentQ = 0;
  ans = [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1];
  renderQuiz();
}

// Initial render
renderQuiz();


// ---- next <script> block ----


	const heightObserver = new ResizeObserver(([{ contentRect }]) => {
		window.parent.postMessage({ action: 'iframeHeightUpdated', height: contentRect.height, id: 'zSoeKF' }, '*');
	});

	heightObserver.observe(document.documentElement);
