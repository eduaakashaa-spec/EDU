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

  nirfStack(); nirfRadar(); closing(); fillM(); fillL(); dasa(); seats(); find();
})();
