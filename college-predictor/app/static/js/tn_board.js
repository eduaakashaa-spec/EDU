(function () {
  'use strict';
  var D = window.EA_TNB || {};
  var JEE = D.jee || [], NEET = D.neet || [], COV = D.cov || {}, AREAS = D.areas || {}, CAL = D.cal || [];
  var NAVY = '#0E3A8A', OR = '#FF6B0A', GR = '#1F8B5C', RED = '#C23A3A', GREY = '#8C93A6';
  var ST_COL = { '12': GR, '11': NAVY, 'P': OR, 'N': RED };
  var ST_LBL = { '12': 'TN 12', '11': 'TN 11', 'P': 'Partly', 'N': 'Not in TN' };
  var ST_LONG = { '12': 'In TN Class 12 (board)', '11': 'In TN Class 11 only', 'P': 'Partly in TN', 'N': 'Not in TN' };
  var TIER_W = { 1: 4, 2: 3, 3: 2, 4: 1 };
  var $ = function (id) { return document.getElementById(id); };
  var esc = function (s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); };
  var sum = function (a, f) { return a.reduce(function (x, r) { return x + f(r); }, 0); };
  var store = {
    get: function (k) { try { return JSON.parse(localStorage.getItem(k)); } catch (e) { return null; } },
    set: function (k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) { /* private mode */ } }
  };
  var charts = {};
  if (window.Chart) { Chart.defaults.font.family = "'Plus Jakarta Sans',sans-serif"; Chart.defaults.font.size = 11; }
  function mk(id, cfg) { if (!window.Chart || !$(id)) return; if (charts[id]) charts[id].destroy(); charts[id] = new Chart($(id), cfg); }
  function stBadge(s) { return '<span class="tb-st s' + s + '">' + ST_LBL[s] + '</span>'; }
  function tierBadge(t) { return '<span class="tb-tier t' + t + '">T' + t + '</span>'; }
  function qtxt(exam, q) { return exam === 'jee' ? q + ' in 19 shifts' : q + ' a paper'; }
  function rowsFor(exam) { return exam === 'jee' ? JEE : NEET; }
  function subsFor(exam) { return exam === 'jee' ? ['Physics', 'Chemistry', 'Mathematics'] : ['Physics', 'Chemistry', 'Biology']; }
  function seg(id, cb) {
    var el = $(id); if (!el) return;
    el.addEventListener('click', function (e) {
      var b = e.target.closest('button'); if (!b) return;
      el.querySelectorAll('button').forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
      cb(b.dataset.v);
    });
  }
  function segVal(id) { var b = $(id).querySelector('[aria-pressed=true]'); return b ? b.dataset.v : null; }
  function fmt(d) { return d.toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' }); }
  function fmtS(d) { return d.toLocaleDateString('en-IN', { day: 'numeric', month: 'short' }); }
  function iso(d) { return d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0'); }
  function pd(s) { var p = s.split('-'); return new Date(+p[0], +p[1] - 1, +p[2]); }
  function addDays(d, n) { var x = new Date(d); x.setDate(x.getDate() + n); return x; }
  var TODAY = new Date(); TODAY.setHours(0, 0, 0, 0);

  /* ---------- tabs ---------- */
  var built = {};
  function show(tab) {
    document.querySelectorAll('#tabs button').forEach(function (b) { b.setAttribute('aria-selected', b.dataset.tab === tab ? 'true' : 'false'); });
    document.querySelectorAll('.tb-panel').forEach(function (p) { p.hidden = p.id !== 'p-' + tab; });
    if (!built[tab] && BUILD[tab]) { BUILD[tab](); built[tab] = true; }
    if (tab === 'plan') renderPlan();
    if (tab === 'cal') renderCal();
    try { history.replaceState(null, '', '#' + tab); } catch (e) { /* ignore */ }
  }
  $('tabs').addEventListener('click', function (e) { var b = e.target.closest('button'); if (b) show(b.dataset.tab); });
  document.addEventListener('click', function (e) {
    var g = e.target.closest('[data-goto]'); if (!g) return;
    e.preventDefault(); show(g.dataset.goto); window.scrollTo({ top: $('tabs').getBoundingClientRect().top + window.scrollY - 10, behavior: 'smooth' });
  });

  /* ---------- KPIs ---------- */
  (function () {
    var j = COV.jee.all, n = COV.neet.all;
    var k = [
      [Math.round(j.tn11_12) + '%', 'JEE Main in TN 11 + 12', 'of 2026 questions are from topics in the TN books'],
      [Math.round(j.board12) + '%', 'JEE Main in the +2 board', 'only Class 12 chapters are examined in March'],
      [Math.round(n.tn11_12) + '%', 'NEET in TN 11 + 12', 'of a NEET paper is from topics in the TN books'],
      [Math.round(n.board12) + '%', 'NEET in the +2 board', 'the other half is Class 11 or partly taught']
    ];
    $('kpis').innerHTML = k.map(function (x) { return '<div class="tb-kpi"><b>' + x[0] + '</b><span>' + x[1] + '</span><small>' + x[2] + '</small></div>'; }).join('');
  })();

  /* ---------- overview ---------- */
  function donut(id, rows) {
    var keys = ['12', '11', 'P', 'N'];
    var vals = keys.map(function (s) { return sum(rows.filter(function (r) { return r.st === s; }), function (r) { return r.q; }); });
    var tot = sum(vals, function (v) { return v; }) || 1;
    mk(id, { type: 'doughnut', data: { labels: keys.map(function (s) { return ST_LONG[s]; }), datasets: [{ data: vals, backgroundColor: keys.map(function (s) { return ST_COL[s]; }), borderWidth: 2 }] },
      options: { maintainAspectRatio: false, cutout: '58%', plugins: { legend: { position: 'right' }, tooltip: { callbacks: { label: function (c) { return c.label + ': ' + (100 * c.raw / tot).toFixed(1) + '%'; } } } } } });
  }
  function tierBars(id, rows, unit) {
    var keys = ['12', '11', 'P', 'N'];
    mk(id, { type: 'bar', data: { labels: ['Tier 1', 'Tier 2', 'Tier 3', 'Tier 4'], datasets: keys.map(function (s) {
      return { label: ST_LONG[s], backgroundColor: ST_COL[s], data: [1, 2, 3, 4].map(function (t) { return +sum(rows.filter(function (r) { return r.tier === t && r.st === s; }), function (r) { return r.q; }).toFixed(1); }) };
    }) }, options: { maintainAspectRatio: false, scales: { x: { stacked: true }, y: { stacked: true, title: { display: true, text: unit } } }, plugins: { legend: { position: 'bottom' } } } });
  }
  var BUILD = {};
  BUILD.overview = function () {
    donut('cJee', JEE); donut('cNeet', NEET);
    tierBars('cJeeTier', JEE, 'Questions in 19 shifts'); tierBars('cNeetTier', NEET, 'Questions a paper');
    var j = COV.jee, n = COV.neet;
    var topJee11 = JEE.filter(function (r) { return r.st === '11' && r.tier === 1; }).map(function (r) { return r.ch; });
    var miss = JEE.filter(function (r) { return (r.st === 'N' || r.st === 'P') && r.q > 0; }).sort(function (a, b) { return b.q - a.q; }).slice(0, 4).map(function (r) { return r.ch + ' (' + r.q + ' Qs)'; });
    var ins = [
      'Topic coverage is high: ' + j.all.tn11_12 + '% of JEE Main 2026 questions and ' + n.all.tn11_12 + '% of a NEET paper come from chapters that are in the TN Class 11 or 12 books. The gap is mostly <b>depth</b>, not missing chapters: TN board questions are direct, JEE and NEET questions combine ideas and test speed.',
      'The +2 board exam itself examines only Class 12 chapters: <b>' + j.all.board12 + '%</b> of JEE Main questions and <b>' + n.all.board12 + '%</b> of NEET. Students who study only for the board leave the other half (Class 11) unrevised for a year.',
      'Tier 1 JEE chapters taught in TN Class 11: ' + topJee11.join(', ') + '. Put them in the weekly plan from now, alongside the board syllabus.',
      'JEE topics missing or only partly in TN: ' + miss.join(', ') + '. Statistics alone is about one question every shift and is not in the TN Class 11 or 12 book.',
      'Subject view for JEE: Physics ' + j.Physics.tn11_12 + '% in TN (' + j.Physics.board12 + '% in the board), Chemistry ' + j.Chemistry.tn11_12 + '% (' + j.Chemistry.board12 + '%), Mathematics ' + j.Mathematics.tn11_12 + '% (' + j.Mathematics.board12 + '%).',
      'NEET Biology is fully in the TN Botany and Zoology books (' + n.Biology.tn11_12 + '%), but NEET questions are worded from NCERT lines and diagrams. Read the NCERT Biology text for every chapter after the TN chapter.',
      'TN teaches Solutions and Haloalkanes in Class 11 (NCERT puts them in Class 12), and splits equilibrium between Class 11 and Class 12 Ionic Equilibrium. Revise them as one unit for NEET and JEE.',
      'Several TN Class 12 chapters carry board marks but no JEE or NEET 2026 questions (Communication Systems, Solid State, Surface Chemistry, Chemistry in Everyday Life, Discrete Mathematics): study them for the board, not for the entrance exam.'
    ];
    $('insights').innerHTML = ins.map(function (x) { return '<li>' + x + '</li>'; }).join('');
  };

  /* ---------- chapter mapping ---------- */
  BUILD.map = function () {
    var fill = function () {
      var ex = segVal('mExam');
      $('mSub').innerHTML = '<option value="">All subjects</option>' + subsFor(ex).map(function (s) { return '<option>' + s + '</option>'; }).join('');
      $('mQh').textContent = ex === 'jee' ? 'Qs 2026' : 'Qs/paper';
      draw();
    };
    var draw = function () {
      var ex = segVal('mExam'), s = $('mSub').value, st = $('mSt').value, t = $('mTier').value, q = $('mQ').value.trim().toLowerCase();
      var rows = rowsFor(ex).filter(function (r) {
        return (!s || r.sub === s) && (!st || r.st === st) && (!t || r.tier === +t) && (!q || (r.ch + ' ' + r.tn).toLowerCase().indexOf(q) >= 0);
      }).slice().sort(function (a, b) { return a.tier - b.tier || b.q - a.q; });
      $('mCount').textContent = rows.length + ' chapters';
      $('mTbl').querySelector('tbody').innerHTML = rows.map(function (r) {
        return '<tr><td>' + tierBadge(r.tier) + '</td><td><b>' + esc(r.ch) + '</b><div class="tb-ct">Class ' + r.cls + ' (NCERT)</div></td><td>' + r.sub + '</td><td class="n">' + r.q + '</td><td>' + stBadge(r.st) + '</td><td class="tn">' + esc(r.tn) + '</td><td class="note">' + esc(r.note) + '</td></tr>';
      }).join('') || '<tr><td colspan="7">No chapters match.</td></tr>';
    };
    seg('mExam', fill);
    ['mSub', 'mSt', 'mTier'].forEach(function (id) { $(id).addEventListener('change', draw); });
    $('mQ').addEventListener('input', draw);
    fill();
  };

  /* ---------- gaps ---------- */
  BUILD.gaps = function () {
    var draw = function (ex) {
      var rows = rowsFor(ex), item = function (r, cls) {
        return '<div class="tb-gap ' + cls + '"><span class="m">' + r.sub + ' · ' + qtxt(ex, r.q) + ' · Tier ' + r.tier + '</span><br><b>' + esc(r.ch) + '</b> ' + stBadge(r.st) + '<br><span>' + esc(r.tn) + '.</span> ' + esc(r.note) + '</div>';
      };
      var miss = rows.filter(function (r) { return r.st === 'N' || r.st === 'P'; }).sort(function (a, b) { return b.q - a.q; });
      $('gMissing').innerHTML = miss.map(function (r) { return item(r, r.st === 'N' ? '' : 'p'); }).join('') || '<p class="tb-sub">None.</p>';
      $('gEleven').innerHTML = rows.filter(function (r) { return r.st === '11' && r.tier <= 2; }).sort(function (a, b) { return b.q - a.q; }).map(function (r) { return item(r, 'd'); }).join('');
      $('gDepth').innerHTML = rows.filter(function (r) { return r.st === '12' && r.tier <= 2; }).sort(function (a, b) { return b.q - a.q; }).map(function (r) { return item(r, 'd'); }).join('');
      $('gBoard').innerHTML = (D.boardOnly || []).map(function (b) { return '<div class="tb-gap b"><span class="m">' + b[0] + ' · TN Class ' + b[1] + '</span><br><b>' + esc(b[2]) + '</b><br>' + esc(b[3]) + '</div>'; }).join('');
      $('gNcert').innerHTML = ex === 'jee'
        ? '<strong>How to close the JEE gap while preparing for the +2 board.</strong> Study each TN Class 12 chapter for the board, then the same chapter from NCERT and solve the last 5 years of JEE Main questions on it (about 2 hours a chapter). Class 11 Tier 1 chapters (Sequences and Series, Permutations, Quadratics, Units and Errors, Rotational Motion, Hydrocarbons, Atomic Structure, Thermodynamics, GOC) need their own slots every week. JEE Main uses a numerical (integer answer) section: practise questions without options.'
        : '<strong>How to close the NEET gap while preparing for the +2 board.</strong> NEET questions are drawn from the NCERT textbook lines, tables and diagrams. After each TN chapter, read the NCERT chapter line by line and solve 40 to 60 NEET past questions on it. TN Class 11 Biology (Animal Kingdom, Morphology, Anatomy, Cell, Photosynthesis, Human Physiology) is about half of NEET Biology, and the +2 year does not revisit it. Structural Organisation in Animals uses the frog in NCERT and the earthworm and cockroach in the TN book.';
    };
    seg('gExam', draw); draw('jee');
  };

  /* ---------- tiers ---------- */
  BUILD.tiers = function () {
    var fill = function () {
      var ex = segVal('tExam');
      $('tSub').innerHTML = '<option value="">All subjects</option>' + subsFor(ex).map(function (s) { return '<option>' + s + '</option>'; }).join('');
      draw();
    };
    var draw = function () {
      var ex = segVal('tExam'), s = $('tSub').value, rows = rowsFor(ex).filter(function (r) { return !s || r.sub === s; });
      var name = ['', 'Tier 1 · must master', 'Tier 2 · high return', 'Tier 3 · steady marks', 'Tier 4 · low yield'];
      var desc = ['', 'Most-asked chapters: finish first and revise every fortnight.', 'Regular every paper: solve past questions chapter by chapter.', 'Asked now and then: learn formulas and standard questions.', 'Rare or not tested in 2026: board-level study is enough.'];
      $('tGrid').innerHTML = [1, 2, 3, 4].map(function (t) {
        var rs = rows.filter(function (r) { return r.tier === t; }).sort(function (a, b) { return b.q - a.q; });
        var tot = sum(rs, function (r) { return r.q; });
        return '<div class="tb-tcol t' + t + '"><h3>' + name[t] + '</h3><p>' + desc[t] + ' ' + rs.length + ' chapters, ' + (ex === 'jee' ? tot + ' questions in 2026' : tot.toFixed(1) + ' questions a paper') + '.</p>' +
          rs.map(function (r) { return '<div class="tb-chip" title="' + esc(r.tn) + '"><span>' + esc(r.ch) + (s ? '' : ' <em>' + r.sub.slice(0, 4) + '</em>') + '</span><span>' + stBadge(r.st) + ' <em>' + r.q + '</em></span></div>'; }).join('') + '</div>';
      }).join('');
      $('tRule').textContent = ex === 'jee'
        ? 'JEE Main Tiers from the questions in all 19 shifts of 2026: Tier 1 at least 22, Tier 2 13 to 21, Tier 3 8 to 12, Tier 4 7 or fewer (including chapters not tested). The number on each chip is the 2026 question count.'
        : 'NEET Tiers from the average questions a paper: Tier 1 at least 3.5, Tier 2 2.5 to 3, Tier 3 1.5 to 2, Tier 4 1 or fewer. The number on each chip is questions a paper (of 180).';
    };
    seg('tExam', fill); $('tSub').addEventListener('change', draw); fill();
  };

  /* ---------- assessment ---------- */
  var LV = ['', 'Very weak', 'Weak', 'Average', 'Good', 'Strong'];
  var A = store.get('tnb_assess') || { target: 'jee', hours: 18, start: iso(TODAY), r: {} };
  function subjectsOf(target) { return target === 'jee' ? ['Physics', 'Chemistry', 'Mathematics'] : target === 'neet' ? ['Physics', 'Chemistry', 'Biology'] : ['Physics', 'Chemistry', 'Mathematics', 'Biology']; }
  function dots(key, val) {
    return '<span class="tb-dots" data-k="' + esc(key) + '">' + [1, 2, 3, 4, 5].map(function (v) { return '<button type="button" data-v="' + v + '" aria-pressed="' + (val === v) + '" title="' + LV[v] + '">' + v + '</button>'; }).join('') + '</span>';
  }
  function drawRates() {
    var html = '';
    subjectsOf(A.target).forEach(function (s) {
      html += '<div class="tb-rate head"><span>' + s + '</span>' + dots(s, A.r[s]) + '</div>';
      (AREAS[s] || []).forEach(function (a) { var k = s + '|' + a[0]; html += '<div class="tb-rate sub"><span>' + a[0] + '</span>' + dots(k, A.r[k]) + '</div>'; });
    });
    $('aRates').innerHTML = html;
  }
  $('aRates').addEventListener('click', function (e) {
    var b = e.target.closest('button'); if (!b) return;
    var k = b.parentNode.dataset.k, v = +b.dataset.v;
    A.r[k] = A.r[k] === v ? undefined : v;
    b.parentNode.querySelectorAll('button').forEach(function (x) { x.setAttribute('aria-pressed', String(+x.dataset.v === A.r[k])); });
    store.set('tnb_assess', A);
  });
  $('aTarget').value = A.target; $('aHours').value = A.hours; $('aStart').value = A.start || iso(TODAY);
  $('aTarget').addEventListener('change', function () { A.target = this.value; store.set('tnb_assess', A); drawRates(); });
  $('aHours').addEventListener('change', function () { A.hours = Math.max(4, Math.min(60, +this.value || 18)); this.value = A.hours; store.set('tnb_assess', A); });
  $('aStart').addEventListener('change', function () { A.start = this.value; store.set('tnb_assess', A); });
  $('aReset').addEventListener('click', function () { A.r = {}; A.done = false; store.set('tnb_assess', A); drawRates(); $('aOut').hidden = true; });
  drawRates();

  // chapters the student is preparing, with their level and priority
  function studyRows() {
    var t = A.target, out = [];
    var add = function (exam, r) {
      var area = (AREAS[r.sub] || []).filter(function (a) { return (exam === 'jee' ? a[1] : a[2]).indexOf(r.ch) >= 0; })[0];
      var lvl = (area && A.r[r.sub + '|' + area[0]]) || A.r[r.sub] || 3;
      var share = exam === 'jee' ? r.q / 1424 * 75 : r.q;   // questions in one paper (JEE: 75, NEET: 180)
      var stF = { 'N': 1.4, 'P': 1.2, '11': 1.1, '12': 1 }[r.st];
      out.push({ exam: exam, r: r, area: area ? area[0] : r.sub, lvl: lvl, share: share, pri: TIER_W[r.tier] * ((5 - lvl) + 0.6) * stF,
        hrs: Math.max(1, Math.round(({ 1: 6, 2: 4.5, 3: 3, 4: 2 })[r.tier] * ({ 1: 1.6, 2: 1.3, 3: 1, 4: 0.6, 5: 0.3 })[lvl] * (r.st === 'N' ? 1.4 : r.st === '11' ? 1.15 : 1))) });
    };
    if (t === 'jee' || t === 'both') JEE.forEach(function (r) { if (r.q > 0) add('jee', r); });
    if (t === 'neet') NEET.forEach(function (r) { add('neet', r); });
    if (t === 'both') NEET.forEach(function (r) { if (r.sub === 'Biology') add('neet', r); });
    return out;
  }
  function focusText(x) {
    if (x.r.st === 'N') return 'Not in TN: learn from NCERT / exam book';
    if (x.r.st === 'P') return 'Partly in TN: add the missing sub-topics';
    if (x.lvl <= 2) return (x.r.st === '11' ? 'Class 11 basics again, ' : 'Board concepts first, ') + 'then past questions';
    if (x.lvl === 3) return 'Exam-level problems and past questions';
    return 'Timed practice and revision';
  }
  $('aGo').addEventListener('click', function () {
    var missing = subjectsOf(A.target).filter(function (s) { return !A.r[s]; });
    if (missing.length) { alert('Rate each subject first: ' + missing.join(', ') + '.'); return; }
    A.done = true; store.set('tnb_assess', A); renderAssess();
    $('aOut').scrollIntoView({ behavior: 'smooth' });
  });
  function renderAssess() {
    if (!A.done) return;
    $('aOut').hidden = false;
    var rows = studyRows(), bars = [], read = [];
    subjectsOf(A.target).forEach(function (s) {
      var rs = rows.filter(function (x) { return x.r.sub === s; });
      var w = sum(rs, function (x) { return x.share; }) || 1;
      var sc = Math.round(100 * sum(rs, function (x) { return x.share * x.lvl / 5; }) / w);
      read.push([s, sc]);
      (AREAS[s] || []).forEach(function (a) {
        var ar = rs.filter(function (x) { return x.area === a[0]; }); if (!ar.length) return;
        var aw = sum(ar, function (x) { return x.share; });
        var gap = Math.round(100 * sum(ar, function (x) { return x.share * (5 - x.lvl) / 4; }) / aw);
        bars.push([s + ' · ' + a[0], gap, aw]);
      });
    });
    bars.sort(function (a, b) { return b[1] * b[2] - a[1] * a[2]; });
    $('aBars').innerHTML = bars.map(function (b) {
      var c = b[1] >= 60 ? RED : b[1] >= 35 ? OR : GR;
      return '<div class="tb-barrow"><span>' + esc(b[0]) + '</span><i><b style="width:' + b[1] + '%;background:' + c + '"></b></i><span>' + b[1] + '% gap</span></div>';
    }).join('') + '<p class="tb-sub" style="margin-top:6px">Sorted by gap × exam weight, so the top rows cost you the most marks.</p>';
    mk('cRadar', { type: 'bar', data: { labels: read.map(function (r) { return r[0]; }), datasets: [{ data: read.map(function (r) { return r[1]; }), backgroundColor: read.map(function (r) { return r[1] >= 70 ? GR : r[1] >= 50 ? OR : RED; }), borderRadius: 6 }] },
      options: { indexAxis: 'y', maintainAspectRatio: false, scales: { x: { min: 0, max: 100 } }, plugins: { legend: { display: false } } } });
    var overall = Math.round(sum(read, function (r) { return r[1]; }) / read.length);
    var weak = read.slice().sort(function (a, b) { return a[1] - b[1]; })[0];
    $('aRead').innerHTML = '<li>Overall readiness <b>' + overall + '/100</b>. ' + (overall >= 75 ? 'Shift time to timed mocks and the Tier 1 depth gaps.' : overall >= 55 ? 'Board-ready in most areas; build exam depth in your weakest areas first.' : 'Start with concepts: one chapter at a time, board level first, then exam level.') + '</li>' +
      '<li>Weakest subject: <b>' + weak[0] + '</b> (' + weak[1] + '/100). Give it the first slot of each study day.</li>';
    var pri = rows.slice().sort(function (a, b) { return b.pri - a.pri; }).slice(0, 15);
    $('aPri').querySelector('tbody').innerHTML = pri.map(function (x, i) {
      return '<tr><td>' + (i + 1) + '</td><td>' + tierBadge(x.r.tier) + '</td><td><b>' + esc(x.r.ch) + '</b><div class="tb-ct">' + x.r.sub + ' · ' + esc(x.area) + '</div></td><td>' + (x.exam === 'jee' ? 'JEE' : 'NEET') + '</td><td>' + stBadge(x.r.st) + '</td><td class="n">' + x.lvl + '/5</td><td class="note">' + focusText(x) + '</td></tr>';
    }).join('');
  }
  BUILD.assess = function () { renderAssess(); };

  /* ---------- study plan ---------- */
  var M = { s1: pd('2027-01-20'), prac: pd('2027-02-08'), board: pd('2027-03-03'), boardEnd: pd('2027-03-29'), s2: pd('2027-04-02'), neet: pd('2027-05-02'), adv: pd('2027-05-16') };
  function renderPlan() {
    if (!A.done) { $('planEmpty').hidden = false; $('planOut').hidden = true; return; }
    $('planEmpty').hidden = true; $('planOut').hidden = false;
    var t = A.target, hrs = A.hours;
    var start = A.start ? pd(A.start) : TODAY;
    start = addDays(start, -((start.getDay() + 6) % 7));            // Monday of that week
    var end = t === 'jee' ? M.adv : M.neet;
    if (start >= end) { $('planSum').textContent = 'Your start date is after the exams in this plan. Choose an earlier start date.'; $('planWeeks').innerHTML = ''; return; }
    var rows = studyRows();
    // queue: before the board, Class 12 (board) chapters get a boost so board and entrance prep run together
    var q1 = rows.slice().sort(function (a, b) { return b.pri * (b.r.st === '12' ? 1.4 : 1) - a.pri * (a.r.st === '12' ? 1.4 : 1); });
    var left = q1.map(function (x) { return { x: x, h: x.hrs }; });
    var weeks = [], wk = start, phaseOf = function (d) {
      if (d < (t === 'neet' ? M.prac : M.s1) && addDays(d, 7) <= (t === 'neet' ? M.prac : M.s1)) return 1;
      if (d < M.prac) return t === 'neet' ? 1 : 2;
      if (d <= M.boardEnd) return 3;
      return 4;
    };
    var PH = {
      1: ['Board syllabus with exam depth', 'Class 12 chapters for the board, each followed by its JEE/NEET extra topics, plus your Class 11 Tier 1 gaps.'],
      2: ['JEE Main Session 1 sprint', 'Mocks every other day, revise Tier 1 formulas, keep one board chapter a day.'],
      3: ['+2 practicals and public exams', 'Board first: TN past papers and model papers. Keep 1 hour a day of entrance questions so nothing is forgotten.'],
      4: ['Entrance exam run-in', 'Full-time preparation after the board: JEE Main Session 2 or NEET first, then the remaining gaps, Class 11 revision and a full mock every 2 to 3 days.']
    };
    var evIds = ['tn-12-practical', 'tn-12-theory'].concat(t !== 'neet' ? ['jee-main-s1', 'jee-main-s2', 'jee-adv', 'bitsat', 'viteee', 'srmjeee'] : []).concat(t !== 'jee' ? ['neet-ug'] : []);
    var events = CAL.filter(function (e) { return evIds.indexOf(e.id) >= 0; });
    while (wk < end) {
      var we = addDays(wk, 6), ph = phaseOf(wk);
      var cap = ph === 1 ? hrs * 0.8 : ph === 2 ? hrs * 0.4 : ph === 3 ? Math.min(7, hrs * 0.3) : Math.max(hrs * 2, 36) * 0.7;
      var lastWeek = addDays(wk, 7) >= end;
      var tasks = [], used = 0;
      while (!lastWeek && left.length && used < cap - 1) {
        var it = left[0], take = Math.min(it.h, Math.max(2, cap - used));
        // in the board phase only Class 12 chapters (board revision doubles as exam prep) unless none left
        if (ph === 3 && it.x.r.st !== '12') { var j = left.findIndex(function (z) { return z.x.r.st === '12'; }); if (j > 0) { it = left[j]; take = Math.min(it.h, Math.max(2, cap - used)); } }
        tasks.push('<b>' + esc(it.x.r.ch) + '</b> <span class="tb-ct">(' + it.x.r.sub + ', ' + (it.x.exam === 'jee' ? 'JEE' : 'NEET') + ' Tier ' + it.x.r.tier + ', ' + Math.round(take) + ' h)</span> ' + stBadge(it.x.r.st) + ' – ' + focusText(it.x));
        it.h -= take; used += take;
        if (it.h <= 0.5) left.splice(left.indexOf(it), 1);
      }
      var extra = [];
      if (ph === 1) extra.push('One chapter test each weekend (30 questions, timed) on the chapters of this week.');
      if (ph === 2) extra.push('Mocks: 3 full JEE Main papers this week, analyse each the next day.');
      if (ph === 3) extra.push('Board: one TN past or model paper a day in the subject coming next; practical record and viva in the practical weeks.');
      if (ph === 4) extra.push((t === 'jee' ? 'Two full JEE Main mocks' : 'Three full NEET mocks (180 questions, 3 h 20 min)') + ' and error-log revision.');
      if (lastWeek) extra = ['Final week: no new chapters. Formula sheets, NCERT highlights, two light mocks, sleep on time.'];
      var evs = events.filter(function (e) { var a = pd(e.start), b = pd(e.end); return a <= we && b >= wk; }).map(function (e) { return e.name; });
      weeks.push({ wk: wk, we: we, ph: ph, tasks: tasks, extra: extra, evs: evs, used: Math.round(used) });
      wk = addDays(wk, 7);
    }
    var html = '', lastPh = 0, phN = 0;
    weeks.forEach(function (w, i) {
      if (w.ph !== lastPh) { phN++; html += '<div class="tb-phase"><b>Phase ' + phN + ' · ' + PH[w.ph][0] + '</b><span>' + PH[w.ph][1] + '</span></div>'; lastPh = w.ph; }
      html += '<div class="tb-week"><h4><span>Week ' + (i + 1) + ' · ' + fmtS(w.wk) + ' – ' + fmtS(w.we) + (w.used ? ' · ~' + w.used + ' h of chapters' : '') + '</span>' + (w.evs.length ? '<em>' + esc(w.evs.join(' · ')) + '</em>' : '') + '</h4><ul>' +
        w.tasks.map(function (x) { return '<li>' + x + '</li>'; }).join('') + w.extra.map(function (x) { return '<li>' + x + '</li>'; }).join('') + '</ul></div>';
    });
    if (left.length) {
      var need = Math.round(sum(left, function (z) { return z.h; })), wks = weeks.filter(function (w) { return w.ph === 1; }).length || weeks.length;
      html += '<div class="tb-gap p"><b>Not yet scheduled: ' + left.length + ' lower-priority chapters, about ' + need + ' hours.</b> ' + left.map(function (z) { return esc(z.x.r.ch); }).join(', ') +
        '. To fit them, add about ' + Math.ceil(need / wks) + ' hours a week before the board, or revise them in the weeks after your first exam.</div>';
    }
    $('planWeeks').innerHTML = html;
    var tgt = { jee: 'JEE Main (Session 1 from 20 Jan, Session 2 from 2 Apr 2027), the April–May institute exams and JEE Advanced (expected mid-May)', neet: 'NEET UG (expected early May 2027)', both: 'JEE Main and NEET' }[t];
    $('planSum').innerHTML = weeks.length + ' weeks from ' + fmt(start) + ' for <b>' + tgt + '</b> with the TN +2 public exams (3 to 29 Mar 2027), at ' + hrs + ' hours a week outside school (full-time after the board). ' +
      (rows.length - left.length) + ' of ' + rows.length + ' chapters scheduled, in priority order from your assessment.' + (t === 'both' ? ' JEE Main Session 2 falls inside the run-in phase: keep JEE mocks in that week.' : '');
  }

  /* ---------- calendar ---------- */
  var defaultSel = function (t) {
    var base = ['tn-12-practical', 'tn-12-theory', 'tn-12-result'];
    if (t !== 'neet') base = base.concat(['jee-main-s1', 'jee-main-s2', 'jee-adv', 'tnea', 'josaa']);
    if (t !== 'jee') base = base.concat(['neet-ug', 'mcc-aiq', 'tn-med-counselling']);
    return base;
  };
  var SEL = store.get('tnb_cal') || defaultSel(A.target);
  function drawList() {
    var g = segVal('cGrp');
    $('cList').innerHTML = CAL.filter(function (e) { return g === 'all' || e.group === g || e.group === 'both' || e.group === 'board'; }).map(function (e) {
      var a = pd(e.start), b = pd(e.end);
      return '<label class="tb-ev"><input type="checkbox" data-id="' + e.id + '"' + (SEL.indexOf(e.id) >= 0 ? ' checked' : '') + '><span><b>' + esc(e.name) + '</b><span class="tag ' + e.status + '">' + e.status.toUpperCase() + '</span><small>' +
        (e.when ? esc(e.when) : fmt(a) + (e.end !== e.start ? ' – ' + fmt(b) : '')) + '</small></span></label>';
    }).join('');
  }
  function renderCal() {
    if (!$('cList').innerHTML) drawList();
    var ev = CAL.filter(function (e) { return SEL.indexOf(e.id) >= 0; });
    var up = ev.filter(function (e) { return pd(e.end) >= TODAY; });
    $('cSum').textContent = ev.length + ' dates chosen, ' + up.length + ' still ahead. Days are counted from today, ' + fmt(TODAY) + '.';
    $('cAgenda').innerHTML = ev.map(function (e) {
      var a = pd(e.start), b = pd(e.end), dd = Math.round((a - TODAY) / 864e5);
      var cd = pd(e.end) < TODAY ? 'done' : dd <= 0 ? 'on now' : 'in ' + dd + ' days';
      return '<div class="tb-gap ' + (e.group === 'board' ? 'd' : e.status === 'Expected' ? 'b' : 'p') + '"><span class="m">' + fmt(a) + (e.end !== e.start ? ' – ' + fmt(b) : '') + ' · ' + cd + ' · ' + e.status + '</span><br><b>' + esc(e.name) + '</b><br><span class="tb-ct">' + esc(e.note) + '</span></div>';
    }).join('') || '<p class="tb-sub">Tick exams on the left to build your calendar.</p>';
    // month grids for months with chosen events
    var months = {};
    ev.forEach(function (e) { for (var d = pd(e.start); d <= pd(e.end); d = addDays(d, 1)) { var k = d.getFullYear() + '-' + d.getMonth(); (months[k] = months[k] || {})[d.getDate()] = (months[k][d.getDate()] || []).concat([e]); } });
    var keys = Object.keys(months).sort(function (a, b) { var x = a.split('-'), y = b.split('-'); return (x[0] - y[0]) * 12 + (x[1] - y[1]); });
    $('cMonths').innerHTML = keys.map(function (k) {
      var p = k.split('-'), y = +p[0], m = +p[1], first = new Date(y, m, 1), days = new Date(y, m + 1, 0).getDate(), off = (first.getDay() + 6) % 7, cells = '';
      ['M', 'T', 'W', 'T', 'F', 'S', 'S'].forEach(function (h) { cells += '<div class="h">' + h + '</div>'; });
      for (var i = 0; i < off; i++) cells += '<div></div>';
      for (var d = 1; d <= days; d++) {
        var es = months[k][d], cls = 'd';
        if (es) cls += ' ev' + (es.some(function (e) { return e.group === 'board'; }) ? ' board' : es.every(function (e) { return e.status === 'Expected'; }) ? ' exp' : '');
        if (y === TODAY.getFullYear() && m === TODAY.getMonth() && d === TODAY.getDate()) cls += ' today';
        cells += '<div class="' + cls + '"' + (es ? ' title="' + esc(es.map(function (e) { return e.name; }).join(', ')) + '"' : '') + '>' + d + '</div>';
      }
      var names = {}; Object.keys(months[k]).forEach(function (d) { months[k][d].forEach(function (e) { names[e.name] = 1; }); });
      return '<div class="tb-month"><h4>' + first.toLocaleDateString('en-IN', { month: 'long', year: 'numeric' }) + '</h4><div class="tb-cal">' + cells + '</div><ul class="tb-mlist">' + Object.keys(names).map(function (n) { return '<li>' + esc(n) + '</li>'; }).join('') + '</ul></div>';
    }).join('');
  }
  $('cList').addEventListener('change', function (e) {
    var id = e.target.dataset.id; if (!id) return;
    SEL = SEL.filter(function (x) { return x !== id; }); if (e.target.checked) SEL.push(id);
    store.set('tnb_cal', SEL); renderCal();
  });
  seg('cGrp', function () { drawList(); });
  $('cPresetJ').addEventListener('click', function () { SEL = defaultSel('jee').concat(['bitsat', 'viteee', 'srmjeee']); store.set('tnb_cal', SEL); drawList(); renderCal(); });
  $('cPresetN').addEventListener('click', function () { SEL = defaultSel('neet'); store.set('tnb_cal', SEL); drawList(); renderCal(); });
  $('cIcs').addEventListener('click', function () {
    var ev = CAL.filter(function (e) { return SEL.indexOf(e.id) >= 0; });
    if (!ev.length) { alert('Tick at least one exam first.'); return; }
    var d8 = function (s) { return s.replace(/-/g, ''); };
    var clean = function (s) { return String(s).replace(/[\\;,]/g, function (c) { return '\\' + c; }).replace(/\n/g, ' '); };
    var stamp = new Date().toISOString().replace(/[-:]/g, '').replace(/\.\d+/, '');
    var L = ['BEGIN:VCALENDAR', 'VERSION:2.0', 'PRODID:-//EduAakashaA//TN Board Exam Calendar//EN', 'CALSCALE:GREGORIAN', 'X-WR-CALNAME:My TN +2 and entrance exams'];
    ev.forEach(function (e) {
      L.push('BEGIN:VEVENT', 'UID:' + e.id + '-tnb@eduaakashaa.com', 'DTSTAMP:' + stamp, 'DTSTART;VALUE=DATE:' + d8(e.start), 'DTEND;VALUE=DATE:' + d8(iso(addDays(pd(e.end), 1))),
        'SUMMARY:' + clean(e.name + (e.status === 'Expected' ? ' (expected window)' : '')), 'DESCRIPTION:' + clean(e.status + '. ' + (e.when ? e.when + '. ' : '') + e.note + ' Confirm on the official website.'), 'TRANSP:TRANSPARENT', 'END:VEVENT');
    });
    L.push('END:VCALENDAR');
    var blob = new Blob([L.join('\r\n')], { type: 'text/calendar' }), a = document.createElement('a');
    a.href = URL.createObjectURL(blob); a.download = 'my-tn-board-and-entrance-exams.ics'; document.body.appendChild(a); a.click();
    setTimeout(function () { URL.revokeObjectURL(a.href); a.remove(); }, 500);
  });

  var start = (location.hash || '').slice(1);
  show(BUILD[start] || start === 'plan' || start === 'cal' ? start : 'overview');
})();
