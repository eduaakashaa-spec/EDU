/* Architecture and Planning analytics: NIRF 2025 scores, JoSAA 2026 rounds 1 to 5, DASA 2025 vs 2026, NIT+ seat matrix.
   Data arrives in window.ARCH (see architecture_analytics.html). Nothing leaves the browser. */
(function () {
  'use strict';
  var A = window.ARCH; if (!A || !window.Chart) return;
  var NAVY = '#0E3A8A', OR = '#FF6B0A', GREEN = '#1F8B5C', GOLD = '#E0A100', RED = '#C23A3A', GREY = '#8A92A6';
  var dark = document.documentElement.getAttribute('data-theme') === 'dark' || (window.matchMedia && matchMedia('(prefers-color-scheme: dark)').matches && document.documentElement.getAttribute('data-theme') !== 'light');
  var TXT = dark ? '#d7dbe6' : '#33405c', GRID = dark ? 'rgba(255,255,255,.12)' : 'rgba(14,58,138,.10)';
  Chart.defaults.color = TXT; Chart.defaults.font.family = "'Plus Jakarta Sans',system-ui,sans-serif"; Chart.defaults.borderColor = GRID;
  var QN = { AI: 'All India', HS: 'Home State', OS: 'Other State' }, PN = { A: 'B.Arch', P: 'B.Planning' };
  var CATS = ['OPEN', 'EWS', 'OBC-NCL', 'SC', 'ST', 'OPEN (PwD)', 'OBC-NCL (PwD)'];
  var $ = function (id) { return document.getElementById(id); };
  var fmt = function (n) { return n == null ? '' : n.toLocaleString('en-IN'); };
  var charts = {};
  function mk(id, cfg) { if (charts[id]) charts[id].destroy(); charts[id] = new Chart($(id), cfg); return charts[id]; }
  function short(i) { return A.meta[A.inst[i]] ? A.meta[A.inst[i]][0] : A.inst[i]; }
  function isIIT(i) { return A.meta[A.inst[i]] && A.meta[A.inst[i]][3] === 'IIT'; }
  function last(arr) { for (var k = arr.length - 1; k >= 0; k--) if (arr[k] != null) return arr[k]; return null; }
  function first(arr) { for (var k = 0; k < arr.length; k++) if (arr[k] != null) return arr[k]; return null; }
  function opt(sel, items, val) { sel.innerHTML = items.map(function (x) { return '<option value="' + x[0] + '"' + (x[0] === val ? ' selected' : '') + '>' + x[1] + '</option>'; }).join(''); }
  function barOpts(horizontal, extra) {
    var o = { indexAxis: horizontal ? 'y' : 'x', responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: {} };
    if (extra) for (var k in extra) o[k] = extra[k];
    return o;
  }

  /* ---- NIRF ---- */
  var W = A.weights;
  function nirfStack() {
    var n = +$('nirfN').value, rows = A.nirf.slice(0, n);
    var sets = A.params.map(function (p, k) {
      return { label: p[1] + ' (x' + p[2] + ')', data: rows.map(function (r) { return +(r[5][k] * p[2]).toFixed(2); }), backgroundColor: [NAVY, OR, GREEN, GOLD, GREY][k] };
    });
    $('nirfWrap').style.height = Math.max(300, rows.length * 24 + 90) + 'px';
    mk('nirfBars', { type: 'bar', data: { labels: rows.map(function (r) { return r[0] + '. ' + r[1].replace('Indian Institute of Technology', 'IIT').replace('National Institute of Technology', 'NIT').replace('School of Planning and Architecture', 'SPA').replace('School of Planning & Architecture', 'SPA').replace(/,.*$/, ''); }), datasets: sets },
      options: barOpts(true, { plugins: { legend: { position: 'bottom', labels: { boxWidth: 12 } }, tooltip: { callbacks: { footer: function (it) { return 'Total ' + rows[it[0].dataIndex][4].toFixed(2); } } } }, scales: { x: { stacked: true, max: 90, title: { display: true, text: 'Weighted points (adds up to the NIRF score)' } }, y: { stacked: true } } }) });
  }
  function nirfRadar() {
    var a = A.nirf[+$('rdA').value], b = A.nirf[+$('rdB').value];
    mk('nirfRadar', { type: 'radar', data: { labels: A.params.map(function (p) { return p[0]; }), datasets: [
      { label: a[1], data: a[5], borderColor: NAVY, backgroundColor: 'rgba(14,58,138,.18)' }, { label: b[1], data: b[5], borderColor: OR, backgroundColor: 'rgba(255,107,10,.18)' }] },
      options: { responsive: true, maintainAspectRatio: false, scales: { r: { min: 0, max: 100, grid: { color: GRID }, angleLines: { color: GRID }, pointLabels: { color: TXT }, ticks: { backdropColor: 'transparent', color: TXT } } }, plugins: { legend: { position: 'bottom' } } } });
    $('rdTxt').textContent = 'Overall: ' + a[1] + ' ' + a[4].toFixed(2) + ' (rank ' + a[0] + ') and ' + b[1] + ' ' + b[4].toFixed(2) + ' (rank ' + b[0] + '). Scores are out of 100 for each parameter.';
  }
  var nsel = A.nirf.map(function (r, k) { return [k, r[0] + '. ' + r[1]]; });
  opt($('rdA'), nsel, 0); opt($('rdB'), nsel, 7);
  ['nirfN'].forEach(function (id) { $(id).addEventListener('change', nirfStack); });
  ['rdA', 'rdB'].forEach(function (id) { $(id).addEventListener('change', nirfRadar); });

  /* ---- JoSAA final-round closing ---- */
  var fProg = $('fProg'), fQ = $('fQ'), fCat = $('fCat'), fG = $('fG'), fList = $('fList');
  function filtered() {
    var iit = fList.value === 'iit';
    return A.rows.filter(function (r) {
      return r.p === fProg.value && r.q === fQ.value && r.s === fCat.value && r.g === fG.value && isIIT(r.i) === iit;
    });
  }
  function closing() {
    var rs = filtered().filter(function (r) { return last(r.c) != null; }).sort(function (a, b) { return last(a.c) - last(b.c); });
    $('clNone').hidden = rs.length > 0;
    $('clWrap').style.height = Math.max(160, rs.length * 30 + 80) + 'px';
    mk('clBars', { type: 'bar', data: { labels: rs.map(function (r) { return short(r.i); }), datasets: [
      { label: 'Round 1 closing', data: rs.map(function (r) { return first(r.c); }), backgroundColor: 'rgba(14,58,138,.35)' },
      { label: 'Round 5 closing', data: rs.map(function (r) { return last(r.c); }), backgroundColor: OR }] },
      options: barOpts(true, { plugins: { legend: { position: 'bottom' } }, scales: { x: { title: { display: true, text: 'Closing rank (smaller = harder to get)' }, ticks: { callback: function (v) { return fmt(v); } } } } }) });
  }
  [fProg, fQ, fCat, fG, fList].forEach(function (s) { s.addEventListener('change', closing); });

  /* ---- movement across rounds ---- */
  var mI = $('mI'), mQ = $('mQ'), mC = $('mC');
  function seatsFor() { return A.rows.filter(function (r) { return r.i === +mI.value; }); }
  function fillM() {
    var rs = seatsFor(), progs = {}, qs = {};
    rs.forEach(function (r) { progs[r.p] = 1; qs[r.q] = 1; });
    var keep = mQ.value;
    opt(mQ, Object.keys(qs).map(function (q) { return [q, QN[q]]; }), keep in qs ? keep : Object.keys(qs)[0]);
    var pk = $('mP').value;
    opt($('mP'), Object.keys(progs).map(function (p) { return [p, PN[p]]; }), pk in progs ? pk : Object.keys(progs)[0]);
    move();
  }
  function move() {
    var rs = seatsFor().filter(function (r) { return r.p === $('mP').value && r.q === mQ.value && r.g === 'N' && r.s === mC.value; });
    var r = rs[0];
    if (!r) { $('mTxt').textContent = 'This category had no seats in this pool.'; if (charts.mv) charts.mv.destroy(); return; }
    $('mTxt').textContent = short(r.i) + ' ' + PN[r.p] + ', ' + QN[r.q] + ', ' + r.s + ': the closing rank moved from ' + fmt(first(r.c)) + ' in Round 1 to ' + fmt(last(r.c)) + ' in the last round (' + (last(r.c) > first(r.c) ? 'later rounds reached higher ranks: seats were released by candidates who left' : 'it did not move') + ').';
    mk('mv', { type: 'line', data: { labels: ['Round 1', 'Round 2', 'Round 3', 'Round 4', 'Round 5'], datasets: [
      { label: 'Closing rank', data: r.c, borderColor: OR, backgroundColor: OR, tension: .25, spanGaps: true },
      { label: 'Opening rank', data: r.o, borderColor: NAVY, backgroundColor: NAVY, tension: .25, spanGaps: true }] },
      options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'bottom' } }, scales: { y: { reverse: false, title: { display: true, text: 'Rank' }, ticks: { callback: function (v) { return fmt(v); } } } } } });
  }
  var ids = Object.keys(A.byInst).map(Number);
  opt(mI, ids.map(function (i) { return [i, short(i)]; }), ids[0]);
  opt(mC, CATS.map(function (c) { return [c, c]; }), 'OPEN');
  mI.addEventListener('change', fillM); mQ.addEventListener('change', move); $('mP').addEventListener('change', move); mC.addEventListener('change', move);

  /* ---- category ladder for one institute ---- */
  var lI = $('lI');
  function ladder() {
    var rs = A.rows.filter(function (r) { return r.i === +lI.value && r.p === $('lP').value && r.q === $('lQ').value && r.g === 'N'; });
    var by = {}; rs.forEach(function (r) { by[r.s] = last(r.c); });
    var labs = CATS.filter(function (c) { return by[c] != null; });
    mk('lad', { type: 'bar', data: { labels: labs, datasets: [{ label: 'Final-round closing rank', data: labs.map(function (c) { return by[c]; }), backgroundColor: labs.map(function (c) { return c === 'OPEN' ? NAVY : OR; }) }] },
      options: barOpts(false, { scales: { y: { ticks: { callback: function (v) { return fmt(v); } }, title: { display: true, text: 'Closing rank' } } } }) });
    $('lNone').hidden = labs.length > 0;
  }
  function fillL() {
    var rs = A.rows.filter(function (r) { return r.i === +lI.value; }), pr = {}, q = {};
    rs.forEach(function (r) { pr[r.p] = 1; q[r.q] = 1; });
    var pk = $('lP').value, qk = $('lQ').value;
    opt($('lP'), Object.keys(pr).map(function (p) { return [p, PN[p]]; }), pk in pr ? pk : Object.keys(pr)[0]);
    opt($('lQ'), Object.keys(q).map(function (x) { return [x, QN[x]]; }), qk in q ? qk : Object.keys(q)[0]);
    ladder();
  }
  opt(lI, ids.map(function (i) { return [i, short(i)]; }), ids[0]);
  lI.addEventListener('change', fillL); $('lP').addEventListener('change', ladder); $('lQ').addEventListener('change', ladder);

  /* ---- rank finder ---- */
  function find() {
    var rank = parseInt($('rkN').value, 10), body = $('rkBody'); body.innerHTML = '';
    if (!(rank > 0)) { $('rkTxt').textContent = 'Type your rank to see the list.'; return; }
    var iit = $('rkList').value === 'iit', p = $('rkP').value, cat = $('rkC').value, g = $('rkG').value, out = [];
    A.rows.forEach(function (r) {
      if (r.p !== p || r.s !== cat || isIIT(r.i) !== iit) return;
      if (g !== 'B' && r.g !== g) return;
      var c5 = last(r.c), c1 = first(r.c); if (c5 == null) return;
      var st = rank <= c1 ? 0 : rank <= c5 ? 1 : rank <= c5 * 1.15 ? 2 : 3;
      out.push({ r: r, c1: c1, c5: c5, st: st });
    });
    out.sort(function (a, b) { return a.st - b.st || b.c5 - a.c5; });
    var lab = ['Open at your rank in Round 1', 'Open at your rank only by the last round', 'Just beyond: within 15% of the last closing rank', 'Closed before your rank'], cls = ['ok', 'ok2', 'near', 'no'];
    var counts = [0, 0, 0, 0];
    out.forEach(function (o) {
      counts[o.st]++;
      if (o.st === 3 && $('rkHide').checked) return;
      var tr = document.createElement('tr');
      tr.innerHTML = '<td>' + short(o.r.i) + '</td><td>' + QN[o.r.q] + (o.r.g === 'F' ? ' &middot; female-only pool' : '') + '</td><td class="n">' + fmt(o.c1) + '</td><td class="n">' + fmt(o.c5) + '</td><td><span class="rk-' + cls[o.st] + '">' + lab[o.st] + '</span></td>';
      body.appendChild(tr);
    });
    $('rkTxt').textContent = 'For rank ' + fmt(rank) + ', ' + PN[p] + ', ' + cat + ': ' + counts[0] + ' seat pools were still open in Round 1, ' + counts[1] + ' only by the last round, ' + counts[2] + ' just beyond. HS pools apply only to students of that institute’s state. This is 2026 history, not a prediction.';
  }
  ['rkN', 'rkP', 'rkC', 'rkG', 'rkList', 'rkHide'].forEach(function (id) { $(id).addEventListener(id === 'rkN' ? 'input' : 'change', find); });
  opt($('rkC'), CATS.map(function (c) { return [c, c]; }), 'OPEN');

  /* ---- DASA ---- */
  function dasa() {
    var rows = A.dasa.filter(function (d) { return d.f25 != null && d.f26 != null; });
    rows.sort(function (a, b) { return a.f26 - b.f26; });
    var nm = function (d) { return d.inst.replace('National Institute of Technology', 'NIT').replace('School of Planning & Architecture', 'SPA').replace('Visvesvaraya', 'V').replace(/,? ?(Bhopal|Nagpur)?$/, '$1').replace(/^SPA[:,]? /, 'SPA ') + ' · ' + (d.prog.indexOf('Planning (4') === 0 ? 'B.Plan' : 'B.Arch') + ' · ' + d.quota.replace('DASA-', ''); };
    $('dsWrap').style.height = Math.max(240, rows.length * 34 + 80) + 'px';
    mk('dsBars', { type: 'bar', data: { labels: rows.map(nm), datasets: [{ label: '2025 final (Round 3)', data: rows.map(function (d) { return d.f25; }), backgroundColor: 'rgba(14,58,138,.45)' }, { label: '2026 final (Round 2)', data: rows.map(function (d) { return d.f26; }), backgroundColor: OR }] },
      options: barOpts(true, { plugins: { legend: { position: 'bottom' } }, scales: { x: { type: 'logarithmic', title: { display: true, text: 'Final closing rank (log scale)' }, ticks: { callback: function (v) { return [1, 10, 100, 1000, 10000, 100000].indexOf(v) > -1 ? fmt(v) : ''; } } } } }) });
  }

  /* ---- seats ---- */
  function seats() {
    var s = A.seats.filter(function (x) { return x.seats > 0; }).sort(function (a, b) { return b.seats - a.seats; });
    $('stWrap').style.height = Math.max(240, s.length * 30 + 80) + 'px';
    mk('stBars', { type: 'bar', data: { labels: s.map(function (x) { return x.name + ' · ' + (x.prog === 'A' ? 'B.Arch' : 'B.Plan'); }), datasets: [
      { label: 'Home State seats', data: s.map(function (x) { return x.hs; }), backgroundColor: NAVY }, { label: 'Other State seats', data: s.map(function (x) { return x.os; }), backgroundColor: OR }] },
      options: barOpts(true, { plugins: { legend: { position: 'bottom' } }, scales: { x: { stacked: true, title: { display: true, text: 'Seats' } }, y: { stacked: true } } }) });
  }


  /* ---- NIRF compare, factor explorer: every value comes from the NIRF 2025 data sheets ---- */
  var X = A.nirfx;
  var nm = function (x) { return x.rank + '. ' + x.name; };
  var DASH = '–';
  var money = function (v) { return v == null ? DASH : '₹' + v.toLocaleString('en-IN'); };
  var num = function (v) { return v == null ? DASH : v.toLocaleString('en-IN'); };
  var pc = function (v) { return v == null ? DASH : v + '%'; };
  var lakh = function (v) { return v == null ? DASH : '₹' + v + ' lakh'; };
  var d1 = function (v) { return v.toFixed(1); };
  // [label, getter, formatter, best: 'hi' | 'lo' | null]; a row with no getter is a heading
  var M = [
    ['NIRF 2025', null],
    ['Rank', function (x) { return x.rank; }, num, 'lo'], ['Overall score', function (x) { return x.score; }, function (v) { return v.toFixed(2); }, 'hi'],
    ['Teaching, learning and resources (TLR)', function (x) { return x.scores[0]; }, d1, 'hi'],
    ['Research and professional practice (RPC)', function (x) { return x.scores[1]; }, d1, 'hi'],
    ['Graduation outcomes (GO)', function (x) { return x.scores[2]; }, d1, 'hi'],
    ['Outreach and inclusivity (OI)', function (x) { return x.scores[3]; }, d1, 'hi'],
    ['Perception (PR)', function (x) { return x.scores[4]; }, d1, 'hi'],
    ['Intake and students', null],
    ['B.Arch intake (2023-24)', function (x) { return x.intake_ug5; }, num, null], ['B.Planning intake (2023-24)', function (x) { return x.intake_ug4; }, num, null],
    ['All students on roll', function (x) { return x.students; }, num, null], ['Women', function (x) { return x.women_pct; }, pc, null],
    ['From other states', function (x) { return x.outside_state_pct; }, pc, 'hi'], ['From abroad (students)', function (x) { return x.abroad; }, num, 'hi'],
    ['Socially challenged (SC, ST, OBC)', function (x) { return x.social_pct; }, pc, null], ['Economically backward', function (x) { return x.ebc_pct; }, pc, null],
    ['Full tuition reimbursed', function (x) { return x.reimb_pct; }, pc, null],
    ['Teaching and resources', null],
    ['Faculty', function (x) { return x.faculty; }, num, null], ['Students per faculty member', function (x) { return x.spf; }, d1, 'lo'],
    ['Library, labs and studio spend per student (2023-24)', function (x) { return x.acad_per_student; }, money, 'hi'],
    ['Accessibility facilities (of 3)', function (x) { return x.pcs; }, num, 'hi'],
    ['Research income (sponsored and consultancy)', null],
    ['Income, last 3 years', function (x) { return +(x.research_lakh + x.consult_lakh).toFixed(1); }, lakh, 'hi'], ['Income per faculty member, last 3 years', function (x) { return x.research_per_fac; }, lakh, 'hi'],
    ['Graduate outcomes (5-year B.Arch)', null],
    ['Graduating batch', function (x) { return x.year; }, function (v) { return v; }, null], ['Graduated', function (x) { return x.grads; }, num, null], ['Placed', function (x) { return x.placed; }, num, null],
    ['Placed (latest batch)', function (x) { return x.placed_pct; }, pc, 'hi'], ['Placed (average of 3 batches)', function (x) { return x.avg_placed_pct; }, pc, 'hi'],
    ['Median salary a year', function (x) { return x.median; }, money, 'hi'], ['Went to higher studies (latest batch)', function (x) { return x.higher_pct; }, pc, null],
    ['NIRF rating chart: sub-scores (marks, where NIRF\u2019s chart is held)', null]
  ];
  A.subp.forEach(function (sp, j) { M.push([sp[1] + ' (' + sp[0] + ', of ' + sp[2] + ')', function (x) { return x.sub ? x.sub[j] : null; }, function (v) { return v.toFixed(2); }, sp[0] === 'PR' || sp[2] ? 'hi' : null]); });
  var cm = ['cmA', 'cmB', 'cmC', 'cmD'];
  function compare() {
    var picks = cm.map(function (id) { return $(id).value === '' ? null : X[+$(id).value]; }).filter(Boolean);
    var h = '<thead><tr><th></th>' + picks.map(function (x) { return '<th class="h">' + x.name + '<br><small>' + x.city + ', ' + x.state + '</small></th>'; }).join('') + '</tr></thead><tbody>';
    M.forEach(function (m) {
      if (!m[1]) { h += '<tr class="sec"><td colspan="' + (picks.length + 1) + '">' + m[0] + '</td></tr>'; return; }
      var vals = picks.map(function (x) { return m[1](x); }), best = null;
      if (m[3] && picks.length > 1) {
        var ok = vals.filter(function (v) { return v != null; });
        if (ok.length) best = m[3] === 'hi' ? Math.max.apply(null, ok) : Math.min.apply(null, ok);
      }
      h += '<tr><td class="k">' + m[0] + '</td>' + vals.map(function (v) { return '<td class="n' + (best != null && v === best ? ' best' : '') + '">' + (v == null ? DASH : m[2](v)) + '</td>'; }).join('') + '</tr>';
    });
    $('cmT').innerHTML = h + '</tbody>';
    var cols = [NAVY, OR, GREEN, GOLD];
    mk('cmRadar', { type: 'radar', data: { labels: A.params.map(function (p) { return p[0]; }), datasets: picks.map(function (x, k) { return { label: x.name, data: x.scores, borderColor: cols[k], backgroundColor: cols[k] + '22' }; }) },
      options: { responsive: true, maintainAspectRatio: false, scales: { r: { min: 0, max: 100, grid: { color: GRID }, angleLines: { color: GRID }, pointLabels: { color: TXT }, ticks: { backdropColor: 'transparent', color: TXT } } }, plugins: { legend: { position: 'bottom' } } } });
  }
  var xs = X.map(function (x, k) { return [k, nm(x)]; });
  var want = (new URLSearchParams(location.search).get('c') || '').split(',').map(function (v) { return parseInt(v, 10) - 1; }).filter(function (v) { return v >= 0 && v < X.length; });
  var dflt = [0, 7, 18, 1];
  cm.forEach(function (id, k) {
    var el = $(id), items = (k >= 2 ? [['', 'None']] : []).concat(xs);
    var v = want[k] != null ? want[k] : (want.length && k >= 2 ? '' : dflt[k]);
    opt(el, items, v);
    el.addEventListener('change', compare);
  });
  compare();
  if (want.length && location.hash === '#compare' && $('compare').scrollIntoView) $('compare').scrollIntoView();

  var EM = M.filter(function (m) { return m[1]; });
  var exItems = EM.map(function (m, k) { return [k, m[0]]; }).filter(function (o) { return o[1] !== 'Rank' && o[1] !== 'Graduating batch'; });
  opt($('exM'), exItems, EM.map(function (m) { return m[0]; }).indexOf('Median salary a year'));
  function explore() {
    var m = EM[+$('exM').value], rows = X.map(function (x) { return [x, m[1](x)]; }).filter(function (r) { return r[1] != null; });
    rows.sort(function (a, b) { return b[1] - a[1]; });
    $('exWrap').style.height = Math.max(300, rows.length * 22 + 80) + 'px';
    mk('exBars', { type: 'bar', data: { labels: rows.map(function (r) { return r[0].rank + '. ' + r[0].name.replace('Indian Institute of Technology', 'IIT').replace('National Institute of Technology', 'NIT').replace('School of Planning and Architecture', 'SPA').replace('School of Planning & Architecture', 'SPA').replace(/,.*$/, ''); }), datasets: [{ label: m[0], data: rows.map(function (r) { return r[1]; }), backgroundColor: OR }] },
      options: barOpts(true, { plugins: { legend: { display: false }, tooltip: { callbacks: { label: function (c) { return m[2](c.raw); } } } } }) });
  }
  $('exM').addEventListener('change', explore);
  explore();
  var pts = X.filter(function (x) { return x.median && x.placed_pct != null; });
  mk('exScatter', { type: 'bubble', data: { datasets: [{ label: 'Institutes', data: pts.map(function (x) { return { x: x.placed_pct, y: x.median, r: Math.max(4, Math.sqrt(x.intake_ug5 || 20) * 1.4), n: nm(x) + ' (intake ' + x.intake_ug5 + ')' }; }), backgroundColor: 'rgba(255,107,10,.55)', borderColor: OR }] },
    options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false }, tooltip: { callbacks: { label: function (c) { return c.raw.n + ': ' + c.raw.x + '% placed, median ₹' + c.raw.y.toLocaleString('en-IN'); } } } },
      scales: { x: { title: { display: true, text: 'Placed, latest graduating batch (%)' }, min: 0, max: 100 }, y: { title: { display: true, text: 'Median salary a year (₹)' }, ticks: { callback: function (v) { return fmt(v); } } } } } });


  /* ---- NIRF rating chart (15 sub-scores) ---- */
  var RT = X.filter(function (x) { return x.sub; });
  if (RT.length && $('rtI')) {
    var SP = A.subp, avgPct = SP.map(function (sp, j) { return RT.reduce(function (a, x) { return a + 100 * x.sub[j] / sp[2]; }, 0) / RT.length; });
    opt($('rtI'), RT.map(function (x, k) { return [k, nm(x)]; }), 0);
    var ratingChart = function () {
      var x = RT[+$('rtI').value];
      mk('rtBars', { type: 'bar', data: { labels: SP.map(function (sp) { return sp[0]; }), datasets: [
        { label: 'Marks available', data: SP.map(function (sp) { return sp[2]; }), backgroundColor: dark ? 'rgba(255,255,255,.14)' : 'rgba(14,58,138,.12)' },
        { label: 'Marks scored', data: x.sub, backgroundColor: SP.map(function (sp) { return { TLR: '#9B3326', RPC: '#2FA655', GO: '#5F7FB5', OI: '#4F2A76', PR: OR }[sp[3]]; }) }] },
        options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'bottom' }, tooltip: { callbacks: { title: function (it) { return SP[it[0].dataIndex][1]; } } } }, scales: { x: { stacked: false }, y: { max: 100, title: { display: true, text: 'Marks' } } }, datasets: { bar: { grouped: false } } } });
      var dz = SP.map(function (sp, j) { return [100 * x.sub[j] / sp[2] - avgPct[j], j]; }).sort(function (a, b) { return b[0] - a[0]; });
      var up = dz.filter(function (d) { return d[0] > 8; }).slice(0, 3).map(function (d) { return SP[d[1]][1].toLowerCase(); });
      var dn = dz.slice().reverse().filter(function (d) { return d[0] < -8; }).slice(0, 3).map(function (d) { return SP[d[1]][1].toLowerCase(); });
      $('rtTxt').textContent = x.name + ': ' + (up.length ? 'stronger than most of the ' + RT.length + ' on ' + up.join(', ') : 'close to the group average everywhere') + (dn.length ? '; weaker than most on ' + dn.join(', ') : '') + '. Overall NIRF score ' + x.score.toFixed(2) + ', rank ' + x.rank + '.';
    };
    $('rtI').addEventListener('change', ratingChart); ratingChart();
    var order = SP.map(function (sp, j) { return j; }).sort(function (a, b) { return avgPct[b] - avgPct[a]; });
    $('rtAvg').parentNode.style.height = (SP.length * 26 + 80) + 'px';
    mk('rtAvg', { type: 'bar', data: { labels: order.map(function (j) { return SP[j][1] + ' (' + SP[j][0] + ')'; }), datasets: [{ label: 'Average share of marks earned (%)', data: order.map(function (j) { return +avgPct[j].toFixed(0); }), backgroundColor: order.map(function (j) { return avgPct[j] >= 75 ? GREEN : avgPct[j] >= 40 ? GOLD : RED; }) }] },
      options: barOpts(true, { plugins: { legend: { display: false } }, scales: { x: { max: 100, title: { display: true, text: '% of the marks available' } } } }) });
  }
  nirfStack(); nirfRadar(); closing(); fillM(); fillL(); dasa(); seats(); find();
})();
