(function () {
  'use strict';
  var D = window.EA_KEAM || {};
  var ROUNDS = D.rounds || [], RIDS = ROUNDS.map(function (r) { return r.id; }), REF = D.ref || '2026-1';
  var LATEST = RIDS[RIDS.length - 1];
  var NAVY = '#0E3A8A', OR = '#FF6B0A', GR = '#1F8B5C', RED = '#C23A3A', GREY = '#8C93A6';
  var RCOL = { '2025-1': '#B7C2DC', '2025-2': '#8FA8D6', '2026-1': OR, '2026-2': NAVY };
  var FAM_ORDER = ['CSE', 'AI', 'IT', 'ENTC', 'ELEC', 'MECH', 'CIVIL', 'CHEM'];
  var FN = D.famNames || {};
  var CATN = {}; (D.cats || []).forEach(function (c) { CATN[c[0]] = c[1]; });
  var TYPEN = {}; Object.keys(D.types || {}).forEach(function (k) { TYPEN[k] = D.types[k][0]; });
  var $ = function (id) { return document.getElementById(id); };
  var esc = function (s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); };
  var nf = function (n) { return n == null ? '–' : Math.round(n).toLocaleString('en-IN'); };
  var rlab = function (rid) { var r = ROUNDS.filter(function (x) { return x.id === rid; })[0]; return r ? r.year + ' Phase ' + r.phase : rid; };
  var store = { get: function (k) { try { return JSON.parse(localStorage.getItem(k)); } catch (e) { return null; } }, set: function (k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) { /* ignore */ } } };
  var charts = {};
  if (window.Chart) { Chart.defaults.font.family = "'Plus Jakarta Sans',sans-serif"; Chart.defaults.font.size = 11; }
  function mk(id, cfg) { if (!window.Chart || !$(id)) return; if (charts[id]) charts[id].destroy(); charts[id] = new Chart($(id), cfg); }
  function pd(s) { var p = s.split('-'); return new Date(+p[0], +p[1] - 1, +p[2]); }
  function fd(s) { return pd(s).toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' }); }
  function seg(id, cb) { var el = $(id); if (!el) return; el.addEventListener('click', function (e) { var b = e.target.closest('button'); if (!b) return; el.querySelectorAll('button').forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); }); cb(b.dataset.v); }); }
  function segVal(id) { var b = $(id).querySelector('[aria-pressed=true]'); return b ? b.dataset.v : null; }
  function heat(v) { // last rank -> colour (log scale; small rank = dark)
    if (v == null) return '#F4F1E8';
    var t = Math.max(0, Math.min(1, 1 - (Math.log10(v) - 2.5) / 2.3));
    var a = [232, 223, 200], b = [14, 58, 138];
    return 'rgb(' + a.map(function (x, i) { return Math.round(x + (b[i] - x) * t); }).join(',') + ')';
  }
  var SITES = D.sites || {};
  function web(code) { var u = SITES[code]; return u ? ' <a class="km-web" href="' + esc(u) + '" target="_blank" rel="noopener nofollow" title="Official website (opens in a new tab)" onclick="event.stopPropagation()">Website ↗</a>' : ''; }
  var DIST = {}; Object.keys(D.regions || {}).forEach(function (r) { D.regions[r].forEach(function (d) { DIST[d] = r; }); });

  /* ---------- full official file (lazy) ---------- */
  var FULL = null, loading = null;
  var MAPROWS = (D.map || []).map(function (r) { return { c: r[0], n: r[1], d: r[2], t: r[3], nirf: r[4], best: r[5], bestN: r[6], courses: r[7], cs: r[8], top: r[9] }; });
  var COLX = {}; MAPROWS.forEach(function (r) { COLX[r.c] = r; });
  function full() {
    if (FULL) return Promise.resolve(FULL);
    if (!loading) loading = fetch(window.EA_KEAM_URL).then(function (r) { return r.json(); }).then(function (d) {
      d.ci = {}; d.cats.forEach(function (c, i) { d.ci[c] = i; });
      d.col = {}; d.colleges.forEach(function (c) { var x = COLX[c.c] || {}; c.short = x.n || c.n; c.d = x.d; c.region = DIST[x.d] || 'Other'; d.col[c.c] = c; });
      FULL = d; return d;
    }).catch(function (e) { loading = null; netErr(); throw e; });
    return loading;
  }
  function netErr() {
    var p = document.querySelector('.km-panel:not([hidden])'); if (!p || p.querySelector('.km-neterr')) return;
    var n = document.createElement('div'); n.className = 'km-card km-note km-neterr';
    n.innerHTML = '<strong>The last-rank data did not load.</strong> Check your internet connection, then <button class="km-btn" type="button">Try again</button>';
    n.querySelector('button').onclick = function () { var tab = p.id.replace('p-', ''); n.remove(); built[tab] = false; show(tab); if (tab === 'predict' && P.done) run(); };
    p.insertBefore(n, p.firstChild);
  }
  function lr(row, rid, cat) { var v = row.r[rid]; return v ? v[FULL.ci[cat]] : null; }

  /* ---------- tabs and navigation ---------- */
  var built = {}, BUILD = {};
  function show(tab) {
    document.querySelectorAll('#tabs button').forEach(function (b) { b.setAttribute('aria-selected', b.dataset.tab === tab ? 'true' : 'false'); });
    document.querySelectorAll('.km-panel').forEach(function (p) { p.hidden = p.id !== 'p-' + tab; });
    if (!built[tab] && BUILD[tab]) { BUILD[tab](); built[tab] = true; }
    var b = document.querySelector('#tabs button[data-tab="' + tab + '"]'); if (b && b.scrollIntoView) b.scrollIntoView({ block: 'nearest', inline: 'center' });
    try { history.replaceState(null, '', '#' + tab); } catch (e) { /* ignore */ }
  }
  $('tabs').addEventListener('click', function (e) { var b = e.target.closest('button'); if (b) show(b.dataset.tab); });
  document.addEventListener('click', function (e) { var g = e.target.closest('[data-goto-tab]'); if (!g) return; e.preventDefault(); show(g.dataset.gotoTab); $('tabs').scrollIntoView({ behavior: 'smooth' }); });

  /* ---------- KPIs ---------- */
  (function () {
    var t1 = (D.top || [])[0];
    var k = [['21–26 Apr', 'KEAM 2027 (reported)', 'not yet confirmed by CEE Kerala'], [nf(D.ranklist), 'in the 2026 rank list', 'engineering, reported'],
      [D.n_col, 'colleges in the tables', D.n_courses + ' courses, 4 rounds'], [t1 ? nf(t1.best.sm[REF]) : '–', 'smallest last rank', t1 ? t1.n + ', ' + t1.best.n + ' (2026 P1)' : '']];
    $('kpis').innerHTML = k.map(function (x) { return '<div class="km-kpi"><b>' + esc(x[0]) + '</b><span>' + esc(x[1]) + '</span><small>' + esc(x[2]) + '</small></div>'; }).join('');
  })();

  /* ---------- overview ---------- */
  BUILD.overview = function () {
    $('dates').innerHTML = (D.dates || []).map(function (d) {
      var cls = d[4] === 'Official' ? 'd' : d[4] === 'Reported' ? 'p' : 'b';
      return '<div class="km-gap ' + cls + '"><span class="m">' + fd(d[2]) + (d[3] !== d[2] ? ' – ' + fd(d[3]) : '') + ' · ' + d[4] + '</span><br><b>' + esc(d[1]) + '</b><br><span class="km-ct">' + esc(d[5]) + '</span></div>';
    }).join('');
    $('pattern').innerHTML = (D.pattern || []).map(function (p) { return '<div class="km-rate"><b>' + esc(p[0]) + '</b><span style="font-size:13px">' + esc(p[1]) + '</span></div>'; }).join('');
    mk('cSplit', { type: 'doughnut', data: { labels: ['KEAM score (normalised) 300', 'Plus Two PCM (normalised) 300'], datasets: [{ data: [300, 300], backgroundColor: [NAVY, OR], borderWidth: 2 }] },
      options: { maintainAspectRatio: false, cutout: '58%', plugins: { legend: { position: 'right' } } } });
    var f = D.fam || {}, top = D.top || [];
    var m = function (k, rid) { return f[k] && f[k][rid] ? f[k][rid].med : null; };
    var tve = top[0], sel = top.filter(function (t) { return t.t === 'S'; })[0];
    var ins = [
      'Your Plus Two marks are half of your KEAM rank. A strong board result can move you thousands of places, so the board exams in March matter as much as the entrance test in April.',
      tve ? tve.n + ' is the most sought-after: its ' + tve.best.n + ' closed at State Merit rank ' + nf(tve.best.sm['2026-1']) + ' in 2026 Phase 1 and ' + nf(tve.best.sm['2026-2']) + ' in Phase 2.' : '',
      'The top ten are almost all government and aided colleges (CET, GEC Thrissur, TKM, Model Engineering College, MA College Kothamangalam); ' + (sel ? 'the best private college, ' + sel.n + ', closed at ' + nf(sel.best.sm[REF]) + ' for ' + sel.best.n + '.' : ''),
      'Phase 2 closes later than Phase 1: the median State Merit last rank for Computer/CSE moved from ' + nf(m('CSE', '2026-1')) + ' to ' + nf(m('CSE', '2026-2')) + ' in 2026. If you miss a seat in Phase 1, keep your options open.',
      'Of the ' + (D.hist || []).reduce(function (a, b) { return a + b[1]; }, 0) + ' courses with a State Merit last rank in 2026 Phase 1, only ' + ((D.hist || [])[0] || [0, 0])[1] + ' closed within rank 1,000 and ' + ((D.hist || [])[1] || [0, 0])[1] + ' between 1,000 and 5,000: most seats are open to ranks well beyond 20,000.',
      'Community quotas help: at CET, Computer Science closed at rank ' + nf(tve ? tve.best.sm['2026-1'] : null) + ' for State Merit but later for most SEBC communities. Check your category in the Rank calculator.'
    ].filter(Boolean);
    $('insights').innerHTML = ins.map(function (x) { return '<li>' + x + '</li>'; }).join('');
  };
  $('ics').addEventListener('click', function () {
    var d8 = function (s) { return s.replace(/-/g, ''); }, nx = function (s) { var x = pd(s); x.setDate(x.getDate() + 1); return x.getFullYear() + String(x.getMonth() + 1).padStart(2, '0') + String(x.getDate()).padStart(2, '0'); };
    var clean = function (s) { return String(s).replace(/[\\;,]/g, function (c) { return '\\' + c; }); };
    var stamp = new Date().toISOString().replace(/[-:]/g, '').replace(/\.\d+/, '');
    var L = ['BEGIN:VCALENDAR', 'VERSION:2.0', 'PRODID:-//EduAakashaA//KEAM 2027//EN', 'X-WR-CALNAME:KEAM 2027 and allotment'];
    (D.dates || []).forEach(function (d) { L.push('BEGIN:VEVENT', 'UID:' + d[0] + '-keam2027@eduaakashaa.com', 'DTSTAMP:' + stamp, 'DTSTART;VALUE=DATE:' + d8(d[2]), 'DTEND;VALUE=DATE:' + nx(d[3]), 'SUMMARY:' + clean(d[1] + (d[4] !== 'Official' ? ' (' + d[4].toLowerCase() + ')' : '')), 'DESCRIPTION:' + clean(d[4] + '. ' + d[5] + ' Confirm on cee.kerala.gov.in.'), 'TRANSP:TRANSPARENT', 'END:VEVENT'); });
    L.push('END:VCALENDAR');
    var a = document.createElement('a'); a.href = URL.createObjectURL(new Blob([L.join('\r\n')], { type: 'text/calendar' })); a.download = 'keam-2027-and-allotment.ics';
    document.body.appendChild(a); a.click(); setTimeout(function () { URL.revokeObjectURL(a.href); a.remove(); }, 500);
  });

  /* ---------- Kerala map ---------- */
  var RAMP = ['#FBF7EE', '#E8DFC8', '#B7C2DC', '#7B91C2', '#3D5DA3', '#0E3A8A'];
  var ms = { metric: 'n', filter: 'all', sel: null }, GEO = null, path = null;
  var METRIC = { n: 'colleges', courses: 'courses', gov: 'government & aided colleges', cs: 'best Computer last rank' };
  function mFilter(r) { return ms.filter === 'all' || ms.filter === 'top' || r.t === ms.filter; }
  function agg() {
    var A = {};
    MAPROWS.filter(mFilter).forEach(function (r) { if (!r.d) return; var a = A[r.d] = A[r.d] || { n: 0, courses: 0, gov: 0, cs: null, rows: [] }; a.n++; a.courses += r.courses; if (r.t === 'G') a.gov++; if (r.cs != null && (a.cs == null || r.cs < a.cs)) a.cs = r.cs; a.rows.push(r); });
    return A;
  }
  function colour(v, max, m) {
    if (v == null || !v) return RAMP[0];
    var r = m === 'cs' ? Math.max(0, 1 - (Math.log10(v) - 2.5) / 2.3) : v / max;
    return r < .04 ? RAMP[1] : r < .12 ? RAMP[2] : r < .28 ? RAMP[3] : r < .6 ? RAMP[4] : RAMP[5];
  }
  BUILD.map = function () {
    seg('mMetric', function (v) { ms.metric = v; drawMap(); });
    seg('mFilter', function (v) { ms.filter = v; drawMap(); });
    $('mapNote').textContent = 'District from the town in each college\'s name in the CEE tables. Pins for the top 20 sit on their district, not their exact address.';
    if (!window.d3) { $('mapSide').innerHTML = '<p class="km-sub">The map could not load. The tables below still work.</p>'; }
    else d3.json(window.EA_KL_GEO).then(function (geo) {
      GEO = geo;
      var svg = d3.select('#klMap'), proj = d3.geoMercator().fitSize([520, 640], geo);
      path = d3.geoPath().projection(proj);
      svg.append('g').attr('class', 'districts'); svg.append('g').attr('class', 'labels'); svg.append('g').attr('class', 'pins');
      svg.select('.districts').selectAll('path').data(geo.features).enter().append('path').attr('class', 'district').attr('d', path)
        .on('mousemove', function (ev, f) { tip(ev, f.properties.district); }).on('mouseleave', function () { $('mapTip').hidden = true; })
        .on('click', function (ev, f) { ms.sel = f.properties.district; drawMap(); });
      svg.select('.labels').selectAll('text').data(geo.features).enter().append('text').attr('class', 'dlabel')
        .attr('x', function (f) { return path.centroid(f)[0]; }).attr('y', function (f) { return path.centroid(f)[1]; }).text(function (f) { return f.properties.district; });
      drawMap();
    }).catch(function () { $('mapSide').innerHTML = '<p class="km-sub">The map file could not load. The tables below still work.</p>'; });
    sideCharts();
  };
  function tip(ev, name) {
    var a = agg()[name], box = $('klMap').getBoundingClientRect(), t = $('mapTip');
    t.innerHTML = '<b>' + esc(name) + '</b><br>' + (a ? a.n + ' colleges · ' + a.courses + ' courses<br>' + a.gov + ' government or aided' + (a.cs ? '<br>Best Computer last rank ' + nf(a.cs) : '') : 'No college in this view') + '<br><span>Click for the list</span>';
    t.hidden = false; t.style.left = Math.min(ev.clientX - box.left + 14, box.width - 220) + 'px'; t.style.top = Math.min(ev.clientY - box.top + 14, box.height - 90) + 'px';
  }
  function drawMap() {
    var A = agg(), m = ms.metric, max = Math.max.apply(null, Object.keys(A).map(function (k) { return A[k][m] || 0; }).concat([1]));
    if (GEO) {
      d3.select('#klMap .districts').selectAll('path').attr('fill', function (f) { var a = A[f.properties.district]; return colour(a ? a[m] : 0, max, m); }).classed('selected', function (f) { return f.properties.district === ms.sel; });
      d3.select('#klMap .labels').selectAll('text').attr('fill', function (f) { var a = A[f.properties.district], v = a ? a[m] : 0; return (m === 'cs' ? (v && v < 3000) : v / max > .28) ? '#fff' : '#3A4259'; });
      var pins = ms.filter === 'top' ? MAPROWS.filter(function (r) { return r.top && r.d; }) : [], byD = {}, cent = {};
      pins.forEach(function (r) { (byD[r.d] = byD[r.d] || []).push(r); });
      GEO.features.forEach(function (f) { cent[f.properties.district] = path.centroid(f); });
      var pts = []; Object.keys(byD).forEach(function (dn) { var list = byD[dn]; list.forEach(function (r, k) { var ang = 2 * Math.PI * k / list.length, rad = list.length > 1 ? 9 + list.length * 1.8 : 0; pts.push({ r: r, x: cent[dn][0] + rad * Math.cos(ang), y: cent[dn][1] + rad * Math.sin(ang) }); }); });
      var sel = d3.select('#klMap .pins').selectAll('g.pin').data(pts, function (p) { return p.r.c; });
      sel.exit().remove();
      var g = sel.enter().append('g').attr('class', 'pin').attr('transform', function (p) { return 'translate(' + p.x + ',' + p.y + ')'; })
        .on('mousemove', function (ev, p) { var box = $('klMap').getBoundingClientRect(), t = $('mapTip'); t.innerHTML = '<b>#' + p.r.top + ' ' + esc(p.r.n) + '</b><br>' + esc(p.r.bestN) + ': ' + nf(p.r.best) + ' (2026 P1)'; t.hidden = false; t.style.left = Math.min(ev.clientX - box.left + 14, box.width - 220) + 'px'; t.style.top = (ev.clientY - box.top + 14) + 'px'; })
        .on('mouseleave', function () { $('mapTip').hidden = true; }).on('click', function (ev, p) { ms.sel = p.r.d; drawMap(); });
      g.append('circle').attr('r', 0).transition().duration(350).delay(function (p, i) { return i * 20; }).attr('r', 8);
      g.append('text').attr('class', 'pinlabel').attr('dy', '0.35em').text(function (p) { return p.r.top; });
    }
    var lab = m === 'cs' ? ['none', '40k+', '20k', '7k', '3k', 'under 1k'] : ['0', '1+', Math.ceil(max * .04) + '+', Math.ceil(max * .12) + '+', Math.ceil(max * .28) + '+', Math.ceil(max * .6) + '+'];
    $('mapLegend').innerHTML = '<span>' + esc(METRIC[m]) + '</span>' + RAMP.map(function (c, k) { return '<i style="background:' + c + '"></i><em>' + lab[k] + '</em>'; }).join('');
    if (ms.sel) drill(ms.sel, A); else topD(A);
  }
  function topD(A) {
    var m = ms.metric, list = Object.keys(A).map(function (k) { return [k, A[k]]; }).filter(function (x) { return x[1][m] != null; })
      .sort(function (a, b) { return m === 'cs' ? a[1].cs - b[1].cs : (b[1][m] || 0) - (a[1][m] || 0); });
    var max = m === 'cs' ? 1 : (list.length ? list[0][1][m] || 1 : 1);
    $('mapSide').innerHTML = '<h3>Districts by ' + esc(METRIC[m]) + '</h3><p class="km-sub">Click a district on the map or here.</p><ol class="km-rank">' + list.map(function (x) {
      var v = x[1][m], w = m === 'cs' ? Math.max(6, 100 - Math.log10(v) * 18) : v / max * 100;
      return '<li data-d="' + esc(x[0]) + '"><span>' + esc(x[0]) + '</span><i><b style="width:' + w + '%"></b></i><em>' + nf(v) + '</em></li>';
    }).join('') + '</ol>';
  }
  function drill(name, A) {
    var a = A[name], rows = a ? a.rows.slice().sort(function (x, y) { return (x.best || 1e9) - (y.best || 1e9); }) : [];
    $('mapSide').innerHTML = '<div class="km-drillhead"><div><small>District</small><h3>' + esc(name) + '</h3></div><button class="km-back" id="mapBack">All districts</button></div>' +
      (a ? '<div class="km-tiles"><div><b>' + a.n + '</b>colleges</div><div><b>' + a.courses + '</b>courses</div><div><b>' + a.gov + '</b>govt / aided</div><div><b>' + nf(a.cs) + '</b>best Computer</div></div><ul class="km-clist">' +
        rows.map(function (r) { return '<li><b>' + esc(r.n) + '</b>' + web(r.c) + '<div class="km-chips">' + (r.top ? '<span class="km-pill o">Top 20 #' + r.top + '</span>' : '') + (r.nirf ? '<span class="km-pill n">NIRF ' + esc(r.nirf) + '</span>' : '') + '<span class="km-pill">' + esc(TYPEN[r.t]) + '</span></div><span class="km-ct">' + (r.best != null ? 'Best course 2026 P1: ' + esc(r.bestN) + ' · last rank ' + nf(r.best) : 'No State Merit last rank in 2026 Phase 1') + '</span></li>'; }).join('') + '</ul>'
        : '<p class="km-sub">No college in this district for the current filter.</p>');
    $('mapBack').onclick = function () { ms.sel = null; drawMap(); };
  }
  $('mapSide').addEventListener('click', function (e) { var li = e.target.closest('li[data-d]'); if (li) { ms.sel = li.dataset.d; drawMap(); } });
  function sideCharts() {
    var R = {}; MAPROWS.forEach(function (r) { var k = DIST[r.d] || 'Other'; R[k] = (R[k] || 0) + 1; });
    var rk = Object.keys(R);
    mk('cRegion', { type: 'doughnut', data: { labels: rk, datasets: [{ data: rk.map(function (k) { return R[k]; }), backgroundColor: [NAVY, OR, GR, GREY], borderWidth: 2 }] }, options: { maintainAspectRatio: false, cutout: '55%', plugins: { legend: { position: 'right' } } } });
    var ts = ['G', 'N', 'S'];
    mk('cKind', { type: 'bar', data: { labels: ts.map(function (t) { return TYPEN[t]; }), datasets: [{ data: ts.map(function (t) { return MAPROWS.filter(function (r) { return r.t === t; }).length; }), backgroundColor: [NAVY, '#3D5DA3', OR], borderRadius: 6 }] }, options: { indexAxis: 'y', maintainAspectRatio: false, plugins: { legend: { display: false } } } });
    var h = D.hist || [];
    mk('cHist', { type: 'bar', data: { labels: h.map(function (x) { return x[0]; }), datasets: [{ data: h.map(function (x) { return x[1]; }), backgroundColor: h.map(function (x, i) { return i < 2 ? RED : i < 4 ? OR : NAVY; }), borderRadius: 5 }] }, options: { maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { x: { title: { display: true, text: 'State Merit last rank' } } } } });
    var all = {}; MAPROWS.forEach(function (r) { if (!r.d) return; var a = all[r.d] = all[r.d] || { n: 0, c: 0, g: 0, cs: null, csN: '' }; a.n++; a.c += r.courses; if (r.t === 'G') a.g++; if (r.cs != null && (a.cs == null || r.cs < a.cs)) { a.cs = r.cs; a.csN = r.n; } });
    $('distTbl').querySelector('tbody').innerHTML = Object.keys(all).sort(function (a, b) { return all[b].n - all[a].n; }).map(function (k) { var a = all[k]; return '<tr><td><b>' + esc(k) + '</b><div class="km-ct">' + esc(DIST[k] || '') + '</div></td><td class="n">' + a.n + '</td><td class="n">' + a.c + '</td><td class="n">' + a.g + '</td><td>' + (a.cs ? nf(a.cs) + ' <span class="km-ct">' + esc(a.csN) + '</span>' : '–') + '</td></tr>'; }).join('');
  }

  /* ---------- eligibility and categories ---------- */
  BUILD.elig = function () {
    $('elig').innerHTML = (D.elig || []).map(function (e) { return '<div class="km-gap d"><b>' + esc(e[0]) + '</b><br>' + esc(e[1]) + '</div>'; }).join('');
    $('types').innerHTML = ['G', 'N', 'S'].map(function (t) { return '<div class="km-gap b"><b>' + esc(D.types[t][0]) + '</b> · ' + esc(D.types[t][1]) + '</div>'; }).join('');
    $('resvNote').textContent = D.resvNote; $('otherCats').textContent = D.otherCats;
    var tve = (D.top || [])[0];
    full().then(function (d) {
      var row = d.rows.filter(function (r) { return r.c === 'TVE' && r.n === 'Computer Science and Engineering'; })[0];
      $('catTbl').querySelector('tbody').innerHTML = (D.cats || []).map(function (c) { return '<tr><td><b>' + c[0] + '</b></td><td>' + esc(c[1]) + '</td><td class="km-ct">' + esc(c[2]) + '</td><td class="n">' + (row ? nf(lr(row, '2026-1', c[0])) : '–') + '</td></tr>'; }).join('');
    });
    var chk = function () {
      var p = +$('eP').value, c = $('eC').value, k = +$('eK').value;
      var need = c === 'gen' ? 45 : c === 'sebc' ? 40 : 0, okP = p >= need, okK = k >= 10;
      $('eOut').innerHTML = '<div class="km-gap ' + (okP && okK ? 'd' : '') + '"><b>' + (okP && okK ? 'Eligible on these figures' : 'Not eligible on these figures') + '</b><br>' +
        (c === 'scst' ? 'SC and ST candidates need a pass in the qualifying subjects. ' : 'You need at least ' + need + '% in Physics, Chemistry and Mathematics together; you entered ' + p + '%. ') +
        'You also need at least 10 normalised marks in KEAM' + (okK ? '' : ' (you entered ' + k + ')') + '. Confirm in the 2027 prospectus.</div>';
    };
    ['eP', 'eC', 'eK'].forEach(function (id) { $(id).addEventListener('input', chk); $(id).addEventListener('change', chk); }); chk();
  };

  /* ---------- top 20 ---------- */
  BUILD.top = function () {
    var top = D.top || [];
    $('topTbl').querySelector('tbody').innerHTML = top.map(function (t, i) {
      return '<tr data-i="' + i + '"><td><span class="km-rk">' + (i + 1) + '</span></td><td><b>' + esc(t.n) + '</b>' + web(t.c) + '<div class="km-ct">' + esc(t.district || '') + (t.nirf ? ' · NIRF ' + esc(t.nirf) : '') + '</div></td><td class="km-ct">' + esc(t.type) + '</td><td>' + esc(t.best.n) + '</td>' +
        RIDS.map(function (rid) { return '<td class="n">' + nf(t.best.sm[rid]) + '</td>'; }).join('') + '</tr>';
    }).join('');
    $('topTbl').addEventListener('click', function (e) {
      var tr = e.target.closest('tr[data-i]'); if (!tr) return;
      var t = top[+tr.dataset.i], el = $('topDetail'); el.hidden = false;
      el.innerHTML = '<h2>' + esc(t.n) + '</h2><p class="km-sub">' + (SITES[t.c] ? '<a href="' + esc(SITES[t.c]) + '" target="_blank" rel="noopener nofollow">Official website ↗</a> · ' : '') + 'College code ' + t.c + ' · ' + esc(t.type) + ' · ' + esc(t.district || '') + (t.nirf ? ' · NIRF 2025: ' + esc(t.nirf) : '') + '</p><div class="km-tablewrap"><table class="km-table"><thead><tr><th>Course</th><th>Branch group</th>' +
        RIDS.map(function (rid) { return '<th class="n">' + esc(rlab(rid)) + '</th>'; }).join('') + '</tr></thead><tbody>' +
        t.rows.map(function (r) { return '<tr><td>' + esc(r.n) + '</td><td class="km-ct">' + esc(FN[r.f] || r.f) + '</td>' + RIDS.map(function (rid) { return '<td class="n">' + nf(r.sm[rid]) + '</td>'; }).join('') + '</tr>'; }).join('') +
        '</tbody></table></div><p class="km-sub" style="margin-top:6px">State Merit last rank. A dash means the course had no State Merit allotment in that round.</p>';
      el.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
    $('nirf').innerHTML = '<div class="km-gap d"><span class="m">NIRF 2025: 101–150</span><br><b>College of Engineering Trivandrum (CET)</b> is the only KEAM college in the NIRF 2025 engineering top 300.</div>' +
      (D.nirfNot || []).map(function (n) { return '<div class="km-gap b">' + esc(n) + ': ranked, but not through KEAM.</div>'; }).join('');
  };

  /* ---------- branch selection ---------- */
  BUILD.branch = function () {
    var f = D.fam || {};
    mk('cFam', { type: 'bar', data: { labels: FAM_ORDER.map(function (k) { return FN[k]; }), datasets: ['2025-1', '2026-1'].map(function (rid) { return { label: rlab(rid), backgroundColor: RCOL[rid], data: FAM_ORDER.map(function (k) { return f[k] && f[k][rid] ? f[k][rid].p10 : null; }) }; }) },
      options: { maintainAspectRatio: false, plugins: { legend: { position: 'bottom' } }, scales: { y: { title: { display: true, text: 'State Merit last rank (smaller = harder)' } } } } });
    mk('cMove', { type: 'bar', data: { labels: FAM_ORDER.map(function (k) { return FN[k]; }), datasets: ['2026-1', '2026-2'].map(function (rid) { return { label: rlab(rid), backgroundColor: RCOL[rid], data: FAM_ORDER.map(function (k) { return f[k] && f[k][rid] ? f[k][rid].med : null; }) }; }) },
      options: { maintainAspectRatio: false, plugins: { legend: { position: 'bottom' } }, scales: { y: { title: { display: true, text: 'Median State Merit last rank' } } } } });
    $('guide').innerHTML = (D.guide || []).map(function (g) { return '<div class="km-gap d"><b>' + esc(FN[g[0]] || g[0]) + '</b><br>' + esc(g[1]) + '</div>'; }).join('');
    var draw = function () {
      var rank = +$('bR').value;
      full().then(function (d) {
        $('bTbl').querySelector('tbody').innerHTML = FAM_ORDER.map(function (fk) {
          var best = null, n = 0;
          d.rows.forEach(function (r) { if (r.f !== fk) return; var v = lr(r, LATEST, 'SM'); if (v == null || rank > v) return; n++; if (!best || v < best.v) best = { r: r, v: v }; });
          return '<tr><td><b>' + esc(FN[fk]) + '</b></td><td>' + (best ? esc(d.col[best.r.c].short) + web(best.r.c) + '<div class="km-ct">' + esc(d.col[best.r.c].d || '') + '</div>' : '<span class="km-ct">none at this rank</span>') + '</td><td>' + (best ? esc(best.r.n) : '') + '</td><td class="n">' + (best ? nf(best.v) : '–') + '</td><td class="n">' + n + '</td></tr>';
        }).join('');
      });
    };
    $('bR').addEventListener('input', draw); draw();
  };

  /* ---------- rank calculator ---------- */
  BUILD.calc = function () {
    var pos = function () {
      var r = Math.max(1, +$('cR').value || 1), N = D.ranklist || 67505, pct = Math.max(0, 100 * (1 - r / N));
      $('cPos').textContent = 'Top ' + (100 - pct).toFixed(2) + '%';
      $('cPosN').textContent = 'Rank ' + nf(r) + ' is ahead of about ' + nf(Math.max(0, N - r)) + ' candidates (' + pct.toFixed(2) + ' percentile of the 2026 list). Your rank comes from your KEAM score and your Plus Two marks together.';
    };
    $('cR').addEventListener('input', pos); pos();
    var f = D.fam || {};
    $('cMove2').innerHTML = FAM_ORDER.map(function (k) { var a = f[k] && f[k]['2026-1'], b = f[k] && f[k]['2026-2']; return a && b ? '<div class="km-rate"><span>' + esc(FN[k]) + '</span><b>' + nf(a.med) + ' → ' + nf(b.med) + '</b></div>' : ''; }).join('');
    $('cY').innerHTML = RIDS.slice().reverse().map(function (rid) { return '<option value="' + rid + '">' + esc(rlab(rid)) + '</option>'; }).join('');
    full().then(function (d) {
      var cols = d.colleges.slice().sort(function (a, b) { return a.short.localeCompare(b.short); });
      $('cI').innerHTML = cols.map(function (c) { return '<option value="' + c.c + '">' + esc(c.short) + '</option>'; }).join(''); $('cI').value = 'TVE';
      var rowsOf = function () { return d.rows.filter(function (r) { return r.c === $('cI').value; }); };
      var fillB = function () { $('cB').innerHTML = rowsOf().map(function (r, k) { return '<option value="' + k + '">' + esc(r.n) + '</option>'; }).join(''); need(); };
      var need = function () {
        var r = rowsOf()[+$('cB').value], rid = $('cY').value; if (!r) return;
        $('cNeed').innerHTML = '<h2>' + esc(d.col[r.c].short) + ' · ' + esc(r.n) + '</h2><p class="km-sub">' + (SITES[r.c] ? '<a href="' + esc(SITES[r.c]) + '" target="_blank" rel="noopener nofollow">Official website ↗</a> · ' : '') + 'Last rank for each category, ' + esc(rlab(rid)) + '. Your rank must be this or smaller.</p><div class="km-tablewrap"><table class="km-table"><thead><tr><th>Category</th>' +
          RIDS.map(function (x) { return '<th class="n">' + esc(rlab(x)) + '</th>'; }).join('') + '</tr></thead><tbody>' +
          d.cats.map(function (c) { return '<tr' + (c === 'SM' ? ' style="font-weight:700"' : '') + '><td>' + c + ' · ' + esc(CATN[c] || '') + '</td>' + RIDS.map(function (x) { return '<td class="n"' + (x === rid ? ' style="background:#FFF6EA"' : '') + '>' + nf(lr(r, x, c)) + '</td>'; }).join('') + '</tr>'; }).join('') +
          '</tbody></table></div>' + (r.o && r.o[rid] ? '<p class="km-sub" style="margin-top:6px">Other categories (' + esc(rlab(rid)) + '): ' + Object.keys(r.o[rid]).map(function (k) { return k + ' ' + nf(r.o[rid][k]); }).join(', ') + '</p>' : '');
      };
      $('cI').addEventListener('change', fillB); $('cB').addEventListener('change', need); $('cY').addEventListener('change', need); fillB();
    });
  };

  /* ---------- last-rank analytics ---------- */
  BUILD.trend = function () {
    var top = D.top || [];
    $('heat').innerHTML = '<thead><tr><th>College</th>' + FAM_ORDER.map(function (f) { return '<th>' + esc((FN[f] || f).split(' ')[0].replace(',', '')) + '</th>'; }).join('') + '</tr></thead><tbody>' +
      top.map(function (t) { return '<tr><td class="nm" title="' + esc(t.n) + '">' + esc(t.n) + '</td>' + FAM_ORDER.map(function (f) { var v = null; t.rows.forEach(function (r) { var x = r.sm[REF]; if (r.f === f && x != null && (v == null || x < v)) v = x; }); return '<td style="background:' + heat(v) + ';color:' + (v != null && v < 6000 ? '#fff' : '#3A4259') + '">' + (v == null ? '' : nf(v)) + '</td>'; }).join('') + '</tr>'; }).join('') + '</tbody>';
    var ds = {}; MAPROWS.forEach(function (r) { if (r.d) ds[r.d] = 1; });
    $('tD').innerHTML += Object.keys(ds).sort().map(function (k) { return '<option>' + esc(k) + '</option>'; }).join('');
    $('tF').innerHTML += FAM_ORDER.map(function (f) { return '<option value="' + f + '">' + esc(FN[f]) + '</option>'; }).join('');
    $('tCat').innerHTML = (D.cats || []).map(function (c) { return '<option value="' + c[0] + '">' + c[0] + ' · ' + esc(c[1]) + '</option>'; }).join('');
    full().then(function (d) {
      var draw = function () {
        var q = $('tQ').value.trim().toLowerCase(), dd = $('tD').value, f = $('tF').value, t = $('tT').value, cat = $('tCat').value, s = $('tS').value;
        var out = d.rows.filter(function (r) { var c = d.col[r.c]; return (!q || (c.short + ' ' + (c.d || '')).toLowerCase().indexOf(q) >= 0) && (!dd || c.d === dd) && (!f || r.f === f) && (!t || c.t === t); })
          .map(function (r) { var v = RIDS.map(function (rid) { return lr(r, rid, cat); }); var a = lr(r, '2025-1', cat), b = lr(r, '2026-1', cat); return { r: r, v: v, ch: a != null && b != null ? b - a : null, ref: b }; })
          .filter(function (o) { return o.v.some(function (x) { return x != null; }); });
        out.sort(function (a, b) {
          if (s === 'name') return d.col[a.r.c].short.localeCompare(d.col[b.r.c].short);
          if (s === 'up') return (a.ch == null ? 1e9 : a.ch) - (b.ch == null ? 1e9 : b.ch);
          if (s === 'down') return (b.ch == null ? -1e9 : b.ch) - (a.ch == null ? -1e9 : a.ch);
          return (a.ref == null ? 1e9 : a.ref) - (b.ref == null ? 1e9 : b.ref);
        });
        $('tCount').textContent = out.length + ' rows';
        $('tTbl').querySelector('tbody').innerHTML = out.slice(0, 150).map(function (o) { var c = d.col[o.r.c]; return '<tr><td><b>' + esc(c.short) + '</b>' + web(o.r.c) + '<div class="km-ct">' + esc(c.d || '') + ' · ' + esc(TYPEN[c.t]) + '</div></td><td>' + esc(o.r.n) + '</td>' + o.v.map(function (x) { return '<td class="n">' + nf(x) + '</td>'; }).join('') + '<td class="n" style="color:' + (o.ch == null ? GREY : o.ch <= 0 ? RED : GR) + '">' + (o.ch == null ? '–' : (o.ch > 0 ? '+' : '') + nf(o.ch)) + '</td></tr>'; }).join('') || '<tr><td colspan="7">No rows match.</td></tr>';
      };
      ['tD', 'tF', 'tT', 'tCat', 'tS'].forEach(function (id) { $(id).addEventListener('change', draw); }); $('tQ').addEventListener('input', draw); draw();
      var cols = d.colleges.slice().sort(function (a, b) { return a.short.localeCompare(b.short); });
      $('gI').innerHTML = cols.map(function (c) { return '<option value="' + c.c + '">' + esc(c.short) + '</option>'; }).join(''); $('gI').value = 'TCR';
      var rowsOf = function () { return d.rows.filter(function (r) { return r.c === $('gI').value; }); };
      var fillB = function () { $('gB').innerHTML = rowsOf().map(function (r, k) { return '<option value="' + k + '">' + esc(r.n) + '</option>'; }).join(''); plot(); };
      var plot = function () {
        var r = rowsOf()[+$('gB').value]; if (!r) return;
        var series = [['SM', NAVY], ['EZ', OR], ['MU', GR], ['BH', '#7A4FD6'], ['SC', RED], ['EW', '#0A8FA8']];
        mk('cTrend', { type: 'line', data: { labels: RIDS.map(rlab), datasets: series.map(function (s) { return { label: s[0] + ' · ' + (CATN[s[0]] || ''), data: RIDS.map(function (rid) { return lr(r, rid, s[0]); }), borderColor: s[1], backgroundColor: s[1], spanGaps: true, tension: .2 }; }) },
          options: { maintainAspectRatio: false, plugins: { legend: { position: 'bottom' } }, scales: { y: { reverse: true, title: { display: true, text: 'Last rank (top = harder)' } } } } });
      };
      $('gI').addEventListener('change', fillB); $('gB').addEventListener('change', plot); fillB();
    });
  };

  /* ---------- predictor ---------- */
  var P = store.get('keam_pred') || {}, RES = [];
  BUILD.predict = function () {
    $('pC').innerHTML += (D.cats || []).filter(function (c) { return c[0] !== 'SM'; }).map(function (c) { return '<option value="' + c[0] + '">' + c[0] + ' · ' + esc(c[1]) + '</option>'; }).join('');
    $('pRg').innerHTML += Object.keys(D.regions || {}).map(function (r) { return '<option>' + esc(r) + '</option>'; }).join('');
    $('pF').innerHTML += FAM_ORDER.map(function (f) { return '<option value="' + f + '">' + esc(FN[f]) + '</option>'; }).join('');
    $('pY').innerHTML = RIDS.slice().reverse().map(function (rid) { return '<option value="' + rid + '">' + esc(rlab(rid)) + ' last ranks</option>'; }).join('');
    ['pR', 'pC', 'pT', 'pRg', 'pF', 'pY'].forEach(function (id) { if (P[id] != null) $(id).value = P[id]; });
    seg('pShow', function () { render(); });
    if (P.done) run();
  };
  function run() {
    ['pR', 'pC', 'pT', 'pRg', 'pF', 'pY'].forEach(function (id) { P[id] = $(id).value; }); P.done = true; store.set('keam_pred', P);
    $('pOut').hidden = false; $('pSum').textContent = 'Loading the official tables…';
    full().then(function (d) {
      var rank = Math.max(1, +P.pR), cat = P.pC, rid = P.pY, cats = cat === 'SM' ? ['SM'] : ['SM', cat];
      var other = RIDS.filter(function (x) { return x !== rid; }).slice(-1)[0];
      RES = [];
      d.rows.forEach(function (r) {
        var c = d.col[r.c];
        if (P.pT && c.t !== P.pT) return; if (P.pRg && c.region !== P.pRg) return; if (P.pF && r.f !== P.pF) return;
        var best = null; cats.forEach(function (k) { var v = lr(r, rid, k); if (v != null && (!best || v > best.v)) best = { v: v, k: k }; });
        if (!best) return;
        var chance = rank <= best.v * 0.8 ? 'Safe' : rank <= best.v ? 'Likely' : rank <= best.v * 1.25 ? 'Reach' : null;
        if (!chance) return;
        var ov = null; cats.forEach(function (k) { var v = lr(r, other, k); if (v != null && (ov == null || v > ov)) ov = v; });
        RES.push({ r: r, c: c, v: best.v, k: best.k, ov: ov, chance: chance });
      });
      RES.sort(function (a, b) { return a.v - b.v; });
      var n = { Safe: 0, Likely: 0, Reach: 0 }; RES.forEach(function (x) { n[x.chance]++; });
      $('nS').textContent = n.Safe; $('nL').textContent = n.Likely; $('nRe').textContent = n.Reach;
      $('pSum').textContent = 'Rank ' + nf(rank) + ' against ' + rlab(rid) + ' last ranks for ' + cats.map(function (k) { return k + ' (' + (CATN[k] || '') + ')'; }).join(' and ') + '. "Other" shows ' + rlab(other) + ' for comparison. Sorted from the hardest seat down.';
      render();
    });
  }
  function render() {
    var sh = segVal('pShow') || 'all', rows = RES.filter(function (x) { return sh === 'all' || x.chance === sh; });
    $('pCount').textContent = rows.length + ' courses' + (rows.length > 250 ? ' (first 250 shown)' : '');
    $('pTbl').querySelector('tbody').innerHTML = rows.slice(0, 250).map(function (x) {
      return '<tr><td><span class="km-chance ' + x.chance + '">' + x.chance + '</span></td><td><b>' + esc(x.c.short) + '</b>' + web(x.c.c) + '<div class="km-ct">' + esc(x.c.d || '') + '</div></td><td>' + esc(x.r.n) + '</td><td class="km-ct">' + x.k + ' · ' + esc(CATN[x.k] || '') + '</td><td class="n">' + nf(x.v) + '</td><td class="n">' + nf(x.ov) + '</td><td class="km-ct">' + esc(TYPEN[x.c.t]) + '</td></tr>';
    }).join('') || '<tr><td colspan="7">No courses within reach with these filters. Try All branches, All types or a later phase.</td></tr>';
  }
  $('pGo').addEventListener('click', run);

  /* ---------- previous / next ---------- */
  var ORDER = [].map.call(document.querySelectorAll('#tabs button'), function (b) { return [b.dataset.tab, b.textContent.trim()]; });
  ORDER.forEach(function (t, k) {
    var p = $('p-' + t[0]); if (!p) return;
    var nav = document.createElement('div'); nav.className = 'km-pn';
    nav.innerHTML = (k > 0 ? '<button data-goto-tab="' + ORDER[k - 1][0] + '" class="prev">← ' + esc(ORDER[k - 1][1]) + '</button>' : '<span></span>') + (k < ORDER.length - 1 ? '<button data-goto-tab="' + ORDER[k + 1][0] + '" class="next">' + esc(ORDER[k + 1][1]) + ' →</button>' : '');
    p.appendChild(nav);
  });
  var start = (location.hash || '').slice(1);
  show(BUILD[start] ? start : 'overview');
})();
