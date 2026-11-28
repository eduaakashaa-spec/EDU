/* Elite Mentorship (Grade 11 and 12) page: grade switch, self-check, time-back calculator, 5A stepper, roadmap, myth check, brochure viewer. */
(function () {
  var root = document.getElementById('em');
  if (!root) return;
  var $ = function (s) { return root.querySelector(s); };
  var $$ = function (s) { return Array.prototype.slice.call(root.querySelectorAll(s)); };
  var esc = function (s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); };

  /* ---------- grade switch ---------- */
  var grade = '11';
  try { grade = localStorage.getItem('em-grade') === '12' ? '12' : '11'; } catch (e) {}
  function setGrade(g) {
    grade = g;
    root.setAttribute('data-grade', g);
    $$('[data-g]').forEach(function (el) { el.hidden = el.getAttribute('data-g') !== g; });
    $$('[data-set-grade]').forEach(function (b) { b.setAttribute('aria-pressed', b.getAttribute('data-set-grade') === g); });
    $$('.em-track').forEach(function (t) { t.classList.toggle('is-mine', t.getAttribute('data-track') === g); });
    try { localStorage.setItem('em-grade', g); } catch (e) {}
    road(0);
  }
  root.addEventListener('click', function (e) {
    var b = e.target.closest('[data-set-grade]');
    if (b) setGrade(b.getAttribute('data-set-grade'));
  });

  /* ---------- self-check ---------- */
  var QUIZ = [
    'Someone has asked me which branch I actually want, and why.',
    'I know every entrance exam and admission route I am eligible for.',
    'I know the rules that can cost a seat, such as the Class 12 marks rule and the document list.',
    'I have one calendar with every registration window and deadline.',
    'I review each mock test with an error log, not just the score.',
    'My parents and I agree on one plan for branch and college.',
    'I check admission news on official sites before I believe a forward.',
    'I have a first list of colleges sorted into reach, match and safe.'
  ];
  var quiz = $('#em-quiz');
  quiz.innerHTML = QUIZ.map(function (q, i) { return '<label><input type="checkbox" data-q="' + i + '"><span>' + esc(q) + '</span></label>'; }).join('');
  function quizOut() {
    var n = $$('#em-quiz input:checked').length, open = QUIZ.length - n, msg;
    if (n === 0) msg = 'Tick what is true for you. Most students in coaching tick two or three.';
    else if (open === 0) msg = 'All eight are owned. You are already working the way a mentor would ask you to. A mentor can still stress-test the plan.';
    else if (open <= 2) msg = 'A strong base. A mentor would close the last ' + open + ' and stress-test the rest.';
    else if (open <= 5) msg = 'Your study has an owner: your coaching. These ' + open + ' decisions do not have one yet. That is the gap mentoring fills.';
    else msg = 'Right now ' + open + ' of 8 decisions have no owner. That is normal when coaching is the only support, and it is exactly where seats are lost.';
    $('#em-quiz-out').innerHTML = '<div class="em-meter"><i style="width:' + (n / QUIZ.length * 100) + '%"></i></div><p><b>' + n + ' of ' + QUIZ.length + '</b> decisions have an owner today.</p><p>' + msg + '</p>';
  }
  quiz.addEventListener('change', quizOut);

  /* ---------- time-back calculator ---------- */
  function calc() {
    var s = +$('#em-c1').value, p = +$('#em-c2').value, k = +$('#em-c3').value / 100, w = +$('#em-c4').value;
    var sh = Math.round(s * w * k), ph = Math.round(p * w * k);
    $('#em-c1v').textContent = s + ' h'; $('#em-c2v').textContent = p + ' h'; $('#em-c3v').textContent = Math.round(k * 100) + '%'; $('#em-c4v').textContent = w;
    $('#em-calc-out').innerHTML = '<div class="em-back"><div><b>' + sh + ' h</b><span>back for the student: about ' + Math.round(sh / 4.6) + ' full mocks with analysis, or ' + Math.round(sh / 6) + ' six-hour revision Sundays</span></div>' +
      '<div><b>' + ph + ' h</b><span>back for parents: about ' + (ph / w).toFixed(1) + ' hours a week for work, family and planning</span></div></div>';
  }
  ['#em-c1', '#em-c2', '#em-c3', '#em-c4'].forEach(function (i) { $(i).addEventListener('input', calc); });

  /* ---------- 5A method ---------- */
  var FIVE = [
    ['A1', 'Assess', '11', 'Aptitude, interests, marks and eligibility on every route. The onboarding assessment and the eligibility audit happen here.', 'Eligibility report'],
    ['A2', 'Analyze', '11', 'Rank potential is read against cut-off and seat data from three to four years, not one forwarded PDF.', 'Admissions roadmap'],
    ['A3', 'Advise', '11', 'A personal college and branch list with the trade-offs explained, built on the Branch Fit Assessment.', 'Reach, match and safe list (first draft)'],
    ['A4', 'Apply', '12', 'Forms and choices are prepared and verified with you, and the choice order is tested in the simulator. You submit.', 'Choice-filling pack'],
    ['A5', 'Achieve', '12', 'The seat decision, accept or upgrade, made with the full picture: fees, branch, campus and the ten-year view.', 'Final decision brief']
  ];
  var five = $('#em-5a');
  five.innerHTML = FIVE.map(function (a, i) { return '<button type="button" role="tab" data-a="' + i + '" aria-selected="false"><b>' + a[0] + '</b><span>' + a[1] + '</span><small>Grade ' + a[2] + '</small></button>'; }).join('');
  function showA(i) {
    var a = FIVE[i];
    $$('#em-5a button').forEach(function (b, n) { b.setAttribute('aria-selected', n === i); });
    $('#em-5a-panel').innerHTML = '<h3>' + a[0] + ' · ' + a[1] + ' <span class="em-pill">Grade ' + a[2] + ' track</span></h3><p>' + esc(a[3]) + '</p><p class="em-hold">You hold: <b>' + esc(a[4]) + '</b></p>';
  }
  five.addEventListener('click', function (e) { var b = e.target.closest('button'); if (b) showA(+b.getAttribute('data-a')); });

  /* ---------- roadmap ---------- */
  var ROAD = {
    '11': [
      ['Months 1–2', 'Onboard', 'Know where you stand', ['Onboarding assessment for student and parents', 'Eligibility audit: residency, passport, CIWG status', 'Your worry map', 'Grade 11 baseline'], 'Baseline and eligibility report'],
      ['Months 3–5', 'Discover', 'Find the fit', ['Branch Fit Assessment: 30 questions, 7 branch families', 'Industry 4.0 and AI briefing on how each branch is changing'], 'Branch Fit report'],
      ['Months 6–9', 'Build', 'Protect the base', ['Boards and JEE balance', 'Mock-test baseline and error log', 'One calendar for every entrance exam: JEE, NATA, NID, UCEED, NIFT, IAT', 'Document file started'], 'Document and deadline calendar'],
      ['Months 10–12', 'Plan', 'Hand over to Grade 12', ['First target list from 3 to 4 years of trends', 'Grade 12 roadmap and calendar', 'Parent briefing', 'Handover to the Grade 12 track'], 'First target list and Grade 12 roadmap']
    ],
    '12': [
      ['Oct–Nov', 'Onboard', 'Lock the basics', ['Onboarding assessment and eligibility audit across DASA, CIWG, JoSAA and state routes', 'Branch Fit Assessment', 'JEE Main Session 1 registration'], 'Baseline and eligibility report'],
      ['Dec–Jan', 'Target', 'Aim with data', ['Industry 4.0 and AI briefing', 'JEE strategy, mocks and error logs', 'Target list drafted from trends', 'JEE Main Session 1'], 'Target list draft: reach, match, safe'],
      ['Feb–Mar', 'Protect', 'Boards first', ['Boards and JEE balance, with the 75% rule protected', 'Document file completed while school is open'], 'Complete document file'],
      ['Apr–May', 'Map', 'Read the rank right', ['JEE Main Session 2 and the final rank', 'Rank-to-seat map from 3 to 4 years of trends', 'Quota decision: CIWG or Non-CIWG', 'Choice-filling simulator runs'], 'Rank-to-seat map'],
      ['Jun–Jul', 'Counsel', 'Apply on every route', ['Applications: JoSAA, state and private NRI', 'JoSAA and state rounds', 'DASA choice order stress-tested and locked'], 'Choice-filling pack'],
      ['Late Jul–Aug', 'Seat day', 'Decide and get ready', ['DASA and CIWG rounds: register, verify, pay', 'Seat decisions: accept or upgrade', 'College readiness: hostel, travel and year-1 preparation'], 'Final seat decision brief']
    ]
  };
  function road(sel) {
    var g = ROAD[grade];
    $('#em-road').innerHTML = g.map(function (r, i) { return '<button type="button" data-r="' + i + '" aria-pressed="' + (i === sel) + '"><i>' + (i + 1) + '</i><small>' + r[0] + '</small><b>' + r[1] + '</b></button>'; }).join('');
    var r = g[sel];
    $('#em-road-detail').innerHTML = '<h3>Gate ' + (sel + 1) + ' · ' + r[1] + ': ' + r[2] + '</h3><ul>' + r[3].map(function (x) { return '<li>' + esc(x) + '</li>'; }).join('') + '</ul><p class="em-hold">You hold at this gate: <b>' + esc(r[4]) + '</b></p>';
  }
  $('#em-road').addEventListener('click', function (e) { var b = e.target.closest('button'); if (b) road(+b.getAttribute('data-r')); });

  /* ---------- myth check ---------- */
  var CHAT = [
    ['Forwarded many times', 'URGENT!! DASA cut-offs will double. Only 99+ percentile will get any NIT.', 'Myth', 'Cut-offs move both ways: in 2026, 65% of Non-CIWG programmes eased while 54% of CIWG ones tightened. Plan on multi-year trends.'],
    ['Unknown number', 'I can arrange an NIT seat through management quota. ₹20 lakh, only 3 slots left.', 'Scam risk', 'NITs have no management quota. DASA seats are allotted by rank on the official portal only. Never pay an agent.'],
    ['Coaching group', 'Grade 11 is only for the syllabus. Think about colleges after the boards.', 'Late start', 'Eligibility, the document trail and the exam calendar all begin in Grade 11. Families who wait plan inside a one-week DASA window.'],
    ['A relative', 'Only CSE has jobs now. AI has finished Mechanical and Civil.', 'Myth', 'AI is reshaping every branch, not ending them. Fit matters more than the trend, and trends flip from year to year.'],
    ['Coaching group', 'Fill only the top 10 NITs. Everything else is a waste of a choice.', 'Risky', 'A list with no safe options can leave you without a seat in a round. Balance safe, reach, stretch and dream.'],
    ['A parent', 'My friend’s son already has a seven-college list. What is yours doing?', 'Comparison', 'Another child’s list says nothing about your fit. Build yours on aptitude first, then on data.']
  ];
  var chat = $('#em-chat');
  chat.innerHTML = CHAT.map(function (c, i) { return '<button type="button" class="em-msg" data-m="' + i + '" aria-expanded="false"><small>' + esc(c[0]) + '</small><span>' + esc(c[1]) + '</span><span class="em-msg__a" hidden><b>' + esc(c[2]) + '</b> ' + esc(c[3]) + '</span><em>Tap to fact-check</em></button>'; }).join('');
  chat.addEventListener('click', function (e) {
    var b = e.target.closest('.em-msg'); if (!b) return;
    var a = b.querySelector('.em-msg__a'), open = a.hidden;
    a.hidden = !open; b.setAttribute('aria-expanded', open); b.querySelector('em').textContent = open ? 'Tap to hide' : 'Tap to fact-check';
  });

  /* ---------- benefit tabs ---------- */
  $$('.em-tabs [data-tab]').forEach(function (t) {
    t.addEventListener('click', function () {
      $$('.em-tabs [data-tab]').forEach(function (x) { x.setAttribute('aria-selected', x === t); });
      $$('.em-tabp').forEach(function (p) { p.hidden = p.getAttribute('data-panel') !== t.getAttribute('data-tab'); });
    });
  });

  /* ---------- brochure viewer ---------- */
  var viewer = $('#em-viewer'), page = 1, pages = +viewer.getAttribute('data-pages'), first = viewer.getAttribute('data-first');
  function turn(d) {
    page = Math.min(pages, Math.max(1, page + d));
    var img = $('#em-page');
    img.src = first.replace(/brochure-\d+/, 'brochure-' + page);
    img.alt = 'Elite Mentorship brochure, page ' + page + ' of ' + pages;
    $('#em-pageno').textContent = 'Page ' + page + ' of ' + pages;
    $('#em-prev').disabled = page === 1; $('#em-next').disabled = page === pages;
  }
  $('#em-prev').addEventListener('click', function () { turn(-1); });
  $('#em-next').addEventListener('click', function () { turn(1); });
  viewer.addEventListener('keydown', function (e) { if (e.key === 'ArrowLeft') turn(-1); if (e.key === 'ArrowRight') turn(1); });

  quizOut(); calc(); showA(0); turn(0); setGrade(grade);
})();
