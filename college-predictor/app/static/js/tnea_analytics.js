(function () {
  'use strict';
  var D = window.EA_TNEA || {};
  var NAVY = '#0E3A8A', OR = '#FF6B0A', GR = '#1F8B5C', RED = '#C23A3A', GREY = '#8C93A6';
  var FAM_ORDER = ['CSE', 'AI', 'IT', 'ENTC', 'ELEC', 'MECH', 'CIVIL', 'CHEM'];
  var FN = D.famNames || {};
  var COMMS = (D.comms || []).map(function (c) { return c[0]; });
  var CN = {}; (D.comms || []).forEach(function (c) { CN[c[0]] = c[1]; });
  var TYPEN = {}; var TKEYS = Object.keys(D.types || {}); TKEYS.forEach(function (k) { TYPEN[k] = D.types[k][0]; });
  var BASIS = { fin: '2026 final', '1': '2026 Round 1', '2': '2026 Round 2', '3': '2026 Round 3', y25: '2025 sheet' };
  var $ = function (id) { return document.getElementById(id); };
  var esc = function (s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); };
  var nf = function (n) { return n == null ? '–' : Math.round(n).toLocaleString('en-IN'); };
  var mf = function (m) { return m == null ? '–' : (Math.round(m * 1000) / 1000).toString(); };
  var store = { get: function (k) { try { return JSON.parse(localStorage.getItem(k)); } catch (e) { return null; } }, set: function (k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) { /* ignore */ } } };
  var charts = {};
  if (window.Chart) { Chart.defaults.font.family = "'Plus Jakarta Sans',sans-serif"; Chart.defaults.font.size = 11; }
  function mk(id, cfg) { if (!window.Chart || !$(id)) return; if (charts[id]) charts[id].destroy(); charts[id] = new Chart($(id), cfg); }
  function pd(s) { var p = s.split('-'); return new Date(+p[0], +p[1] - 1, +p[2]); }
  function fd(s) { return pd(s).toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' }); }
  function seg(id, cb) { var el = $(id); if (!el) return; el.addEventListener('click', function (e) { var b = e.target.closest('button'); if (!b) return; el.querySelectorAll('button').forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); }); cb(b.dataset.v); }); }
  function segVal(id) { var b = $(id).querySelector('[aria-pressed=true]'); return b ? b.dataset.v : null; }
  function heat(v) { // closing mark -> colour (high mark = dark)
    if (v == null) return '#F4F1E8';
    var t = Math.max(0, Math.min(1, (v - 110) / 90));
    var a = [232, 223, 200], b = [14, 58, 138];
    return 'rgb(' + a.map(function (x, i) { return Math.round(x + (b[i] - x) * t); }).join(',') + ')';
  }
  var SITES = D.sites || {};
  function web(code) { var u = SITES[code]; return u ? ' <a class="tq-web" href="' + esc(u) + '" target="_blank" rel="noopener nofollow" title="Official website (opens in a new tab)" onclick="event.stopPropagation()">Website ↗</a>' : ''; }
  var DIST = {}; Object.keys(D.regions || {}).forEach(function (r) { D.regions[r].forEach(function (d) { DIST[d] = r; }); });
  var CURVE = D.curve || [];
  function rankAt(m) { // typical 2026 rank for a cut-off (curve runs 200 down to 50 in half marks)
    if (!CURVE.length) return null; if (m >= CURVE[0][0]) return CURVE[0][1];
    for (var i = 1; i < CURVE.length; i++) { if (m >= CURVE[i][0]) { var a = CURVE[i - 1], b = CURVE[i], t = (a[0] - m) / (a[0] - b[0]); return Math.round(a[1] + (b[1] - a[1]) * t); } }
    return CURVE[CURVE.length - 1][1];
  }

  /* ---------- full official file (lazy) ---------- */
  var FULL = null, loading = null;
  var MAPROWS = (D.map || []).map(function (r) { return { c: r[0], n: r[1], d: r[2], t: r[3], nirf: r[4], best: r[5], bestN: r[6], courses: r[7], cs: r[8], top: r[9], seats: r[10] }; });
  var COLX = {}; MAPROWS.forEach(function (r) { COLX[r.c] = r; });
  function full() {
    if (FULL) return Promise.resolve(FULL);
    if (!loading) loading = fetch(window.EA_TNEA_URL).then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); }).then(function (d) {
      d.ci = {}; d.comms.forEach(function (c, i) { d.ci[c] = i; });
      d.col = {}; d.colleges.forEach(function (c) { var x = COLX[c.c] || {}; c.short = x.n || c.n; c.d = x.d; c.t = x.t; c.region = DIST[x.d] || 'Other'; d.col[c.c] = c; });
      d.rows.forEach(function (r) { r.n = d.branches[r.b] || r.b; r.f = famOf(r.n); });
      FULL = d; return d;
    }).catch(function (e) { loading = null; netErr(); throw e; });
    return loading;
  }
  // same branch groups as app/services/tnea_analytics.py FAMILIES
  function famOf(n) {
    n = n.toLowerCase();
    var R = [['AI', /artificial|machine learning|data scien|data visual|generative/], ['IT', /information technology/], ['ELEC', /electrical/], ['CSE', /computer|cyber|internet of things|software|block ?chain/],
      ['ENTC', /electronics|communication|instrumentation|vlsi/], ['MECH', /mechanical|automobile|production|manufactur|mechatron|robot|aeronaut|aerospace|marine|industrial engineering|mining|metallurg|material/],
      ['CIVIL', /civil|structural|environment|geo ?informatics/], ['CHEM', /chemical|petro|polymer|plastic|bio|food|textile|fashion|apparel|handloom|leather|ceramic|pharma|rubber|agricult|chemistry/]];
    for (var i = 0; i < R.length; i++) if (R[i][1].test(n)) return R[i][0];
    return 'OTHER';
  }
  function netErr() {
    var p = document.querySelector('.tq-panel:not([hidden])'); if (!p || p.querySelector('.tq-neterr')) return;
    var n = document.createElement('div'); n.className = 'tq-card tq-note tq-neterr';
    n.innerHTML = '<strong>The cut-off data did not load.</strong> Check your internet connection, then <button class="tq-btn" type="button">Try again</button>';
    n.querySelector('button').onclick = function () { var tab = p.id.replace('p-', ''); n.remove(); built[tab] = false; show(tab); if (tab === 'predict' && P.done) run(); };
    p.insertBefore(n, p.firstChild);
  }
  // closing [mark, rank, seats] in a round, the final (lowest across rounds), or the 2025 sheet mark
  function cell(row, k, comm) { var v = row.r[k]; return v ? v[FULL.ci[comm]] : null; }
  function fin(row, comm) { var best = null; ['1', '2', '3'].forEach(function (k) { var v = cell(row, k, comm); if (v && (!best || v[0] < best[0] || (v[0] === best[0] && v[1] > best[1]))) best = v; }); return best; }
  function mark(row, basis, comm) {
    if (basis === 'y25') return row.y25 ? row.y25[FULL.ci[comm]] : null;
    var v = basis === 'fin' ? fin(row, comm) : cell(row, basis, comm); return v ? v[0] : null;
  }

  /* ---------- tabs and navigation ---------- */
  var built = {}, BUILD = {};
  function show(tab) {
    document.querySelectorAll('#tabs button').forEach(function (b) { b.setAttribute('aria-selected', b.dataset.tab === tab ? 'true' : 'false'); });
    document.querySelectorAll('.tq-panel').forEach(function (p) { p.hidden = p.id !== 'p-' + tab; });
    if (!built[tab] && BUILD[tab]) { BUILD[tab](); built[tab] = true; }
    var b = document.querySelector('#tabs button[data-tab="' + tab + '"]'); if (b && b.scrollIntoView) b.scrollIntoView({ block: 'nearest', inline: 'center' });
    try { history.replaceState(null, '', '#' + tab); } catch (e) { /* ignore */ }
  }
  $('tabs').addEventListener('click', function (e) { var b = e.target.closest('button'); if (b) show(b.dataset.tab); });
  document.addEventListener('click', function (e) { var g = e.target.closest('[data-goto-tab]'); if (!g) return; e.preventDefault(); show(g.dataset.gotoTab); $('tabs').scrollIntoView({ behavior: 'smooth' }); });

  /* ---------- KPIs ---------- */
  (function () {
    var t1 = (D.top || [])[0];
    var k = [['3–29 Mar', 'TN +2 theory exams 2027', 'official DGE timetable'], [nf(D.n_seats), 'seats allotted in 2026', 'general academic, 3 rounds'],
      [D.n_col, 'colleges in counselling', D.n_courses + ' branches, ' + nf(D.n_rows) + ' courses'], [t1 ? mf(t1.best.fin[0]) : '–', 'highest closing cut-off', t1 ? t1.n + ', ' + t1.best.n + ' (OC, 2026)' : '']];
    $('kpis').innerHTML = k.map(function (x) { return '<div class="tq-kpi"><b>' + esc(x[0]) + '</b><span>' + esc(x[1]) + '</span><small>' + esc(x[2]) + '</small></div>'; }).join('');
  })();

  /* ---------- overview ---------- */
  BUILD.overview = function () {
    $('dates').innerHTML = (D.dates || []).map(function (d) {
      var cls = d[4] === 'Official' ? 'd' : d[4] === 'Reported' ? 'p' : 'b';
      return '<div class="tq-gap ' + cls + '"><span class="m">' + fd(d[2]) + (d[3] !== d[2] ? ' – ' + fd(d[3]) : '') + ' · ' + d[4] + '</span><br><b>' + esc(d[1]) + '</b><br><span class="tq-ct">' + esc(d[5]) + '</span></div>';
    }).join('');
    $('pattern').innerHTML = (D.pattern || []).map(function (p) { return '<div class="tq-rate"><b>' + esc(p[0]) + '</b><span style="font-size:13px">' + esc(p[1]) + '</span></div>'; }).join('');
    mk('cSplit', { type: 'doughnut', data: { labels: ['Mathematics 100', 'Physics ÷ 2 = 50', 'Chemistry ÷ 2 = 50'], datasets: [{ data: [100, 50, 50], backgroundColor: [NAVY, OR, GR], borderWidth: 2 }] },
      options: { maintainAspectRatio: false, cutout: '58%', plugins: { legend: { position: 'right' } } } });
    var sr = D.seatsRound || {};
    $('roundTbl').querySelector('tbody').innerHTML = (D.rounds26 || []).map(function (r) { return '<tr><td><b>Round ' + r[0] + '</b></td><td>' + mf(r[1]) + ' to ' + mf(r[2]) + '</td><td>' + nf(r[3]) + ' – ' + nf(r[4]) + '</td><td class="n">' + nf(sr[r[0]]) + '</td><td class="tq-ct">' + esc(r[5]) + '</td></tr>'; }).join('');
    var f = D.fam || {}, top = D.top || [], h = D.hist || [];
    var g = function (k, y, s) { return f[k] && f[k][y] ? f[k][y][s] : null; };
    var priv = top.filter(function (t) { return /^T/.test(t.t); })[0], tot = h.reduce(function (a, b) { return a + b[1]; }, 0);
    var r1 = D.rounds26 && D.rounds26[0];
    var ins = [
      'Mathematics is half your cut-off. One extra mark in Mathematics adds a full mark to your cut-off; one extra mark in Physics or Chemistry adds half a mark. Around a cut-off of 180, one mark was worth about ' + nf((rankAt(180) - rankAt(181))) + ' places in 2026.',
      top[0] ? top[0].n + ' is the most sought-after: its ' + top[0].best.n + ' closed at ' + mf(top[0].best.fin[0]) + ' for OC (closing rank ' + nf(top[0].best.fin[1]) + ').' : '',
      'The top of the list is Anna University (CEG, MIT), PSG Tech, Thiagarajar, CIT and GCT Coimbatore' + (priv ? '; the best self-financing college, ' + priv.n + ', closed at ' + mf(priv.best.fin[0]) + ' for ' + priv.best.n + '.' : '.'),
      r1 ? 'Round 1 took cut-offs from ' + mf(r1[1]) + ' to ' + mf(r1[2]) + ' (ranks up to ' + nf(r1[4]) + ') and filled ' + nf((D.seatsRound || {})[1]) + ' seats; most of the ' + nf(D.n_seats) + ' seats went in Rounds 2 and 3.' : '',
      'Only ' + ((h[0] || [0, 0])[1] + (h[1] || [0, 0])[1]) + ' of ' + nf(tot) + ' courses closed at 190 or more for OC, and the median Computer Science course closed at ' + mf(g('CSE', 'fin', 'med')) + '. A cut-off in the 150s still opens hundreds of courses.',
      'Community seats help: at CEG, Computer Science closed at 200 for OC but lower for BC, MBC, SC and SCA. Check your community in the Cut-off calculator.'
    ].filter(Boolean);
    $('insights').innerHTML = ins.map(function (x) { return '<li>' + esc(x) + '</li>'; }).join('');
  };
  $('ics').addEventListener('click', function () {
    var d8 = function (s) { return s.replace(/-/g, ''); }, nx = function (s) { var x = pd(s); x.setDate(x.getDate() + 1); return x.getFullYear() + String(x.getMonth() + 1).padStart(2, '0') + String(x.getDate()).padStart(2, '0'); };
    var clean = function (s) { return String(s).replace(/[\\;,]/g, function (c) { return '\\' + c; }); };
    var stamp = new Date().toISOString().replace(/[-:]/g, '').replace(/\.\d+/, '');
    var L = ['BEGIN:VCALENDAR', 'VERSION:2.0', 'PRODID:-//EduAakashaA//TNEA 2027//EN', 'X-WR-CALNAME:TN +2 and TNEA 2027'];
    (D.dates || []).forEach(function (d) { L.push('BEGIN:VEVENT', 'UID:' + d[0] + '-tnea2027@eduaakashaa.com', 'DTSTAMP:' + stamp, 'DTSTART;VALUE=DATE:' + d8(d[2]), 'DTEND;VALUE=DATE:' + nx(d[3]), 'SUMMARY:' + clean(d[1] + (d[4] !== 'Official' ? ' (' + d[4].toLowerCase() + ')' : '')), 'DESCRIPTION:' + clean(d[4] + '. ' + d[5] + ' Confirm on tneaonline.org.'), 'TRANSP:TRANSPARENT', 'END:VEVENT'); });
    L.push('END:VCALENDAR');
    var a = document.createElement('a'); a.href = URL.createObjectURL(new Blob([L.join('\r\n')], { type: 'text/calendar' })); a.download = 'tnea-2027-and-tn-plus2.ics';
    document.body.appendChild(a); a.click(); setTimeout(function () { URL.revokeObjectURL(a.href); a.remove(); }, 500);
  });

  /* ---------- Tamil Nadu map ---------- */
  var RAMP = ['#FBF7EE', '#E8DFC8', '#B7C2DC', '#7B91C2', '#3D5DA3', '#0E3A8A'];
  var ms = { metric: 'n', filter: 'all', sel: null }, GEO = null, path = null;
  var METRIC = { n: 'colleges', seats: 'seats allotted 2026', gov: 'government & university colleges', cs: 'best Computer cut-off' };
  var GOV = function (t) { return t === 'G' || t === 'U'; };
  function mFilter(r) { return ms.filter === 'all' || ms.filter === 'top' || r.t === ms.filter; }
  function agg() {
    var A = {};
    MAPROWS.filter(mFilter).forEach(function (r) { if (!r.d) return; var a = A[r.d] = A[r.d] || { n: 0, courses: 0, seats: 0, gov: 0, cs: null, rows: [] }; a.n++; a.courses += r.courses; a.seats += r.seats || 0; if (GOV(r.t)) a.gov++; if (r.cs != null && (a.cs == null || r.cs > a.cs)) a.cs = r.cs; a.rows.push(r); });
    return A;
  }
  function colour(v, max, m) {
    if (v == null || !v) return RAMP[0];
    var r = m === 'cs' ? Math.max(0, (v - 120) / 80) : v / max;
    return r < .04 ? RAMP[1] : r < .12 ? RAMP[2] : r < .28 ? RAMP[3] : r < .6 ? RAMP[4] : RAMP[5];
  }
  BUILD.map = function () {
    seg('mMetric', function (v) { ms.metric = v; drawMap(); });
    seg('mFilter', function (v) { ms.filter = v; drawMap(); });
    $('mapNote').textContent = 'District as given for each college in the TNEA cut-off data (Mayiladuthurai colleges are shown in Nagapattinam, as in the map file). Pins for the top 20 sit on their district, not their exact address.';
    if (!window.d3) { $('mapSide').innerHTML = '<p class="tq-sub">The map could not load. The tables below still work.</p>'; }
    else d3.json(window.EA_TN_GEO).then(function (geo) {
      GEO = geo;
      var svg = d3.select('#tnMap'), proj = d3.geoMercator().fitSize([520, 600], geo);
      path = d3.geoPath().projection(proj);
      svg.append('g').attr('class', 'districts'); svg.append('g').attr('class', 'labels'); svg.append('g').attr('class', 'pins');
      svg.select('.districts').selectAll('path').data(geo.features).enter().append('path').attr('class', 'district').attr('d', path)
        .on('mousemove', function (ev, f) { tip(ev, f.properties.district); }).on('mouseleave', function () { $('mapTip').hidden = true; })
        .on('click', function (ev, f) { ms.sel = f.properties.district; drawMap(); });
      svg.select('.labels').selectAll('text').data(geo.features).enter().append('text').attr('class', 'dlabel')
        .attr('x', function (f) { return path.centroid(f)[0]; }).attr('y', function (f) { return path.centroid(f)[1]; }).text(function (f) { return f.properties.district; });
      drawMap();
    }).catch(function () { $('mapSide').innerHTML = '<p class="tq-sub">The map file could not load. The tables below still work.</p>'; });
    sideCharts();
  };
  function tip(ev, name) {
    var a = agg()[name], box = $('tnMap').getBoundingClientRect(), t = $('mapTip');
    t.innerHTML = '<b>' + esc(name) + '</b><br>' + (a ? a.n + ' colleges · ' + a.courses + ' courses<br>' + nf(a.seats) + ' seats allotted · ' + a.gov + ' govt or university' + (a.cs ? '<br>Best Computer cut-off ' + mf(a.cs) : '') : 'No college in this view') + '<br><span>Click for the list</span>';
    t.hidden = false; t.style.left = Math.min(ev.clientX - box.left + 14, box.width - 220) + 'px'; t.style.top = Math.min(ev.clientY - box.top + 14, box.height - 90) + 'px';
  }
  function drawMap() {
    var A = agg(), m = ms.metric, max = Math.max.apply(null, Object.keys(A).map(function (k) { return A[k][m] || 0; }).concat([1]));
    if (GEO) {
      d3.select('#tnMap .districts').selectAll('path').attr('fill', function (f) { var a = A[f.properties.district]; return colour(a ? a[m] : 0, max, m); }).classed('selected', function (f) { return f.properties.district === ms.sel; });
      d3.select('#tnMap .labels').selectAll('text').attr('fill', function (f) { var a = A[f.properties.district], v = a ? a[m] : 0; return (m === 'cs' ? (v && v >= 178) : v / max > .28) ? '#fff' : '#3A4259'; });
      var pins = ms.filter === 'top' ? MAPROWS.filter(function (r) { return r.top && r.d; }) : [], byD = {}, cent = {};
      pins.forEach(function (r) { (byD[r.d] = byD[r.d] || []).push(r); });
      GEO.features.forEach(function (f) { cent[f.properties.district] = path.centroid(f); });
      var pts = []; Object.keys(byD).forEach(function (dn) { var list = byD[dn], c0 = cent[dn]; if (!c0) return; list.forEach(function (r, k) { var ang = 2 * Math.PI * k / list.length, rad = list.length > 1 ? 9 + list.length * 1.8 : 0; pts.push({ r: r, x: c0[0] + rad * Math.cos(ang), y: c0[1] + rad * Math.sin(ang) }); }); });
      var sel = d3.select('#tnMap .pins').selectAll('g.pin').data(pts, function (p) { return p.r.c; });
      sel.exit().remove();
      var g = sel.enter().append('g').attr('class', 'pin').attr('transform', function (p) { return 'translate(' + p.x + ',' + p.y + ')'; })
        .on('mousemove', function (ev, p) { var box = $('tnMap').getBoundingClientRect(), t = $('mapTip'); t.innerHTML = '<b>#' + p.r.top + ' ' + esc(p.r.n) + '</b><br>' + esc(p.r.bestN) + ': ' + mf(p.r.best) + ' (OC, 2026)'; t.hidden = false; t.style.left = Math.min(ev.clientX - box.left + 14, box.width - 220) + 'px'; t.style.top = (ev.clientY - box.top + 14) + 'px'; })
        .on('mouseleave', function () { $('mapTip').hidden = true; }).on('click', function (ev, p) { ms.sel = p.r.d; drawMap(); });
      g.append('circle').attr('r', 0).transition().duration(350).delay(function (p, i) { return i * 20; }).attr('r', 8);
      g.append('text').attr('class', 'pinlabel').attr('dy', '0.35em').text(function (p) { return p.r.top; });
    }
    var lab = m === 'cs' ? ['none', 'under 125', '130+', '142+', '165+', '190+'] : ['0', '1+', Math.ceil(max * .04) + '+', Math.ceil(max * .12) + '+', Math.ceil(max * .28) + '+', Math.ceil(max * .6) + '+'];
    $('mapLegend').innerHTML = '<span>' + esc(METRIC[m]) + '</span>' + RAMP.map(function (c, k) { return '<i style="background:' + c + '"></i><em>' + lab[k] + '</em>'; }).join('');
    if (ms.sel) drill(ms.sel, A); else topD(A);
  }
  function topD(A) {
    var m = ms.metric, list = Object.keys(A).map(function (k) { return [k, A[k]]; }).filter(function (x) { return x[1][m] != null; })
      .sort(function (a, b) { return (b[1][m] || 0) - (a[1][m] || 0); });
    var max = list.length ? list[0][1][m] || 1 : 1;
    $('mapSide').innerHTML = '<h3>Districts by ' + esc(METRIC[m]) + '</h3><p class="tq-sub">Click a district on the map or here.</p><ol class="tq-rank">' + list.map(function (x) {
      var v = x[1][m], w = m === 'cs' ? Math.max(6, (v - 100) / 100 * 100) : v / max * 100;
      return '<li data-d="' + esc(x[0]) + '"><span>' + esc(x[0]) + '</span><i><b style="width:' + w + '%"></b></i><em>' + (m === 'cs' ? mf(v) : nf(v)) + '</em></li>';
    }).join('') + '</ol>';
  }
  function drill(name, A) {
    var a = A[name], rows = a ? a.rows.slice().sort(function (x, y) { return (y.best || 0) - (x.best || 0); }) : [];
    $('mapSide').innerHTML = '<div class="tq-drillhead"><div><small>District</small><h3>' + esc(name) + '</h3></div><button class="tq-back" id="mapBack">All districts</button></div>' +
      (a ? '<div class="tq-tiles"><div><b>' + a.n + '</b>colleges</div><div><b>' + nf(a.seats) + '</b>seats 2026</div><div><b>' + a.gov + '</b>govt / univ</div><div><b>' + mf(a.cs) + '</b>best Computer</div></div><ul class="tq-clist">' +
        rows.map(function (r) { return '<li><b>' + esc(r.n) + '</b>' + web(r.c) + '<div class="tq-chips">' + (r.top ? '<span class="tq-pill o">Top 20 #' + r.top + '</span>' : '') + (r.nirf ? '<span class="tq-pill n">NIRF ' + esc(r.nirf) + '</span>' : '') + '<span class="tq-pill">' + esc(TYPEN[r.t]) + '</span></div><span class="tq-ct">' + (r.best != null ? 'Best course: ' + esc(r.bestN) + ' · OC closing ' + mf(r.best) : 'No OC allotment in 2026') + ' · code ' + r.c + '</span></li>'; }).join('') + '</ul>'
        : '<p class="tq-sub">No college in this district for the current filter.</p>');
    $('mapBack').onclick = function () { ms.sel = null; drawMap(); };
  }
  $('mapSide').addEventListener('click', function (e) { var li = e.target.closest('li[data-d]'); if (li) { ms.sel = li.dataset.d; drawMap(); } });
  function sideCharts() {
    var R = {}; MAPROWS.forEach(function (r) { var k = DIST[r.d] || 'Other'; R[k] = (R[k] || 0) + 1; });
    var rk = Object.keys(R);
    mk('cRegion', { type: 'doughnut', data: { labels: rk, datasets: [{ data: rk.map(function (k) { return R[k]; }), backgroundColor: [NAVY, OR, GR, '#7A4FD6', GREY], borderWidth: 2 }] }, options: { maintainAspectRatio: false, cutout: '55%', plugins: { legend: { position: 'right' } } } });
    mk('cKind', { type: 'bar', data: { labels: TKEYS.map(function (t) { return TYPEN[t]; }), datasets: [{ data: TKEYS.map(function (t) { return MAPROWS.filter(function (r) { return r.t === t; }).length; }), backgroundColor: [NAVY, '#3D5DA3', OR, '#FF8A3D', '#FFB27A', GREY], borderRadius: 6 }] }, options: { indexAxis: 'y', maintainAspectRatio: false, plugins: { legend: { display: false } } } });
    var h = D.hist || [];
    mk('cHist', { type: 'bar', data: { labels: h.map(function (x) { return x[0]; }), datasets: [{ data: h.map(function (x) { return x[1]; }), backgroundColor: h.map(function (x, i) { return i < 2 ? RED : i < 4 ? OR : NAVY; }), borderRadius: 5 }] }, options: { maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { x: { title: { display: true, text: 'OC closing cut-off (final 2026)' } } } } });
    var all = {}; MAPROWS.forEach(function (r) { if (!r.d) return; var a = all[r.d] = all[r.d] || { n: 0, c: 0, s: 0, g: 0, cs: null, csN: '' }; a.n++; a.c += r.courses; a.s += r.seats || 0; if (GOV(r.t)) a.g++; if (r.cs != null && (a.cs == null || r.cs > a.cs)) { a.cs = r.cs; a.csN = r.n; } });
    $('distTbl').querySelector('tbody').innerHTML = Object.keys(all).sort(function (a, b) { return all[b].n - all[a].n; }).map(function (k) { var a = all[k]; return '<tr><td><b>' + esc(k) + '</b><div class="tq-ct">' + esc(DIST[k] || '') + '</div></td><td class="n">' + a.n + '</td><td class="n">' + a.c + '</td><td class="n">' + nf(a.s) + '</td><td class="n">' + a.g + '</td><td>' + (a.cs ? mf(a.cs) + ' <span class="tq-ct">' + esc(a.csN) + '</span>' : '–') + '</td></tr>'; }).join('');
  }

  /* ---------- eligibility and communities ---------- */
  BUILD.elig = function () {
    $('elig').innerHTML = (D.elig || []).map(function (e) { return '<div class="tq-gap d"><b>' + esc(e[0]) + '</b><br>' + esc(e[1]) + '</div>'; }).join('');
    $('types').innerHTML = TKEYS.map(function (t) { return '<div class="tq-gap b"><b>' + esc(D.types[t][0]) + '</b> · ' + esc(D.types[t][1]) + '</div>'; }).join('');
    $('resvNote').textContent = D.resvNote;
    var rowsHtml = function (row) {
      return (D.comms || []).map(function (c) { var v = row ? fin(row, c[0]) : null; return '<tr><td><b>' + c[0] + '</b></td><td>' + esc(c[1]) + '</td><td class="n">' + esc(c[2]) + '</td><td class="tq-ct">' + esc(c[3]) + '</td><td class="n">' + (v ? mf(v[0]) + ' <span class="tq-ct">rank ' + nf(v[1]) + '</span>' : '–') + '</td></tr>'; }).join('');
    };
    $('catTbl').querySelector('tbody').innerHTML = rowsHtml(null);
    full().then(function (d) { var row = d.rows.filter(function (r) { return r.c === 1 && r.b === 'CS'; })[0]; $('catTbl').querySelector('tbody').innerHTML = rowsHtml(row); });
    var chk = function () {
      var p = +$('eP').value, c = $('eC').value, need = c === 'OC' ? 45 : 40, ok = p >= need;
      $('eOut').innerHTML = '<div class="tq-gap ' + (ok ? 'd' : '') + '"><b>' + (ok ? 'Eligible on these marks' : 'Not eligible on these marks') + '</b><br>' + c + ' candidates need at least ' + need + '% in Mathematics, Physics and Chemistry together; you entered ' + p + '%. Confirm in the TNEA 2027 information brochure.</div>';
    };
    ['eP', 'eC'].forEach(function (id) { $(id).addEventListener('input', chk); $(id).addEventListener('change', chk); }); chk();
  };

  /* ---------- top 20 ---------- */
  BUILD.top = function () {
    var top = D.top || [];
    $('topTbl').querySelector('tbody').innerHTML = top.map(function (t, i) {
      return '<tr data-i="' + i + '"><td><span class="tq-rk">' + (i + 1) + '</span></td><td><b>' + esc(t.n) + '</b>' + web(t.c) + '<div class="tq-ct">' + esc(t.district || '') + (t.nirf ? ' · NIRF ' + esc(t.nirf) : '') + '</div></td><td class="tq-ct">' + esc(t.type) + '</td><td>' + esc(t.best.n) + '</td>' +
        '<td class="n">' + mf(t.best.rd['1']) + '</td><td class="n"><b>' + mf(t.best.fin[0]) + '</b></td><td class="n">' + nf(t.best.fin[1]) + '</td><td class="n">' + mf(t.best.y25) + '</td></tr>';
    }).join('');
    $('topTbl').addEventListener('click', function (e) {
      var tr = e.target.closest('tr[data-i]'); if (!tr) return;
      var t = top[+tr.dataset.i], el = $('topDetail'); el.hidden = false;
      el.innerHTML = '<h2>' + esc(t.n) + '</h2><p class="tq-sub">' + (SITES[t.c] ? '<a href="' + esc(SITES[t.c]) + '" target="_blank" rel="noopener nofollow">Official website ↗</a> · ' : '') + 'TNEA code ' + t.c + ' · ' + esc(t.type) + ' · ' + esc(t.district || '') + (t.nirf ? ' · NIRF 2025: ' + esc(t.nirf) : '') + '</p><div class="tq-tablewrap"><table class="tq-table"><thead><tr><th>Course</th><th>Branch group</th><th class="n">Round 1</th><th class="n">Round 2</th><th class="n">Round 3</th><th class="n">Final 2026</th><th class="n">Closing rank</th><th class="n">2025 sheet</th></tr></thead><tbody>' +
        t.rows.map(function (r) { return '<tr><td>' + esc(r.n) + '</td><td class="tq-ct">' + esc(FN[r.f] || r.f) + '</td>' + ['1', '2', '3'].map(function (k) { return '<td class="n">' + mf(r.rd[k]) + '</td>'; }).join('') + '<td class="n"><b>' + mf(r.fin ? r.fin[0] : null) + '</b></td><td class="n">' + nf(r.fin ? r.fin[1] : null) + '</td><td class="n">' + mf(r.y25) + '</td></tr>'; }).join('') +
        '</tbody></table></div><p class="tq-sub" style="margin-top:6px">OC closing cut-off. A dash in a round means no OC seat was allotted in that round.</p>';
      el.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
    var order = function (s) { var m = /^(\d+)/.exec(s || ''); return m ? +m[1] : 999; };
    var nr = MAPROWS.filter(function (r) { return r.nirf; }).sort(function (a, b) { return order(a.nirf) - order(b.nirf) || (b.best || 0) - (a.best || 0); });
    $('nirfTbl').querySelector('tbody').innerHTML = nr.map(function (r) { return '<tr><td><span class="tq-pill n">' + esc(r.nirf) + '</span></td><td><b>' + esc(r.n) + '</b>' + web(r.c) + '<div class="tq-ct">' + esc(r.d || '') + '</div></td><td class="tq-ct">' + esc(TYPEN[r.t]) + '</td><td>' + esc(r.bestN || '') + '</td><td class="n">' + mf(r.best) + '</td></tr>'; }).join('');
    $('nirf').innerHTML = (D.nirfNot || []).map(function (n) { return '<div class="tq-gap b">' + esc(n) + '</div>'; }).join('');
  };

  /* ---------- branch selection ---------- */
  BUILD.branch = function () {
    var f = D.fam || {}, sf = D.seatsFam || {};
    mk('cFam', { type: 'bar', data: { labels: FAM_ORDER.map(function (k) { return FN[k]; }), datasets: [['p90', 'Top 10% of courses', NAVY], ['med', 'Median course', OR]].map(function (s) { return { label: s[1], backgroundColor: s[2], data: FAM_ORDER.map(function (k) { return f[k] && f[k].fin ? f[k].fin[s[0]] : null; }) }; }) },
      options: { maintainAspectRatio: false, plugins: { legend: { position: 'bottom' } }, scales: { y: { min: 80, max: 200, title: { display: true, text: 'OC closing cut-off (higher = harder)' } } } } });
    mk('cMove', { type: 'bar', data: { labels: FAM_ORDER.map(function (k) { return FN[k]; }), datasets: [['1', '#B7C2DC'], ['2', '#3D5DA3'], ['3', OR]].map(function (s) { return { label: 'Round ' + s[0], backgroundColor: s[1], data: FAM_ORDER.map(function (k) { return sf[k] ? sf[k][s[0]] : null; }) }; }) },
      options: { maintainAspectRatio: false, plugins: { legend: { position: 'bottom' } }, scales: { x: { stacked: true }, y: { stacked: true, title: { display: true, text: 'Seats allotted' } } } } });
    $('guide').innerHTML = (D.guide || []).map(function (g) { return '<div class="tq-gap d"><b>' + esc(FN[g[0]] || g[0]) + '</b><br>' + esc(g[1]) + '</div>'; }).join('');
    var draw = function () {
      var m = +$('bR').value;
      full().then(function (d) {
        $('bTbl').querySelector('tbody').innerHTML = FAM_ORDER.map(function (fk) {
          var best = null, n = 0;
          d.rows.forEach(function (r) { if (r.f !== fk) return; var v = mark(r, 'fin', 'OC'); if (v == null || m < v) return; n++; if (!best || v > best.v) best = { r: r, v: v }; });
          return '<tr><td><b>' + esc(FN[fk]) + '</b></td><td>' + (best ? esc(d.col[best.r.c].short) + web(best.r.c) + '<div class="tq-ct">' + esc(d.col[best.r.c].d || '') + '</div>' : '<span class="tq-ct">none at this cut-off</span>') + '</td><td>' + (best ? esc(best.r.n) : '') + '</td><td class="n">' + (best ? mf(best.v) : '–') + '</td><td class="n">' + n + '</td></tr>';
        }).join('');
      });
    };
    $('bR').addEventListener('input', draw); draw();
  };

  /* ---------- cut-off calculator ---------- */
  BUILD.calc = function () {
    var calc = function () {
      var M = Math.min(100, Math.max(0, +$('cM').value || 0)), Pp = Math.min(100, Math.max(0, +$('cP').value || 0)), C = Math.min(100, Math.max(0, +$('cC').value || 0));
      var cut = M + Pp / 2 + C / 2, rk = rankAt(cut), rd = (D.rounds26 || []).filter(function (r) { return cut <= r[1] + 1e-9 && cut >= r[2] - 1e-9; })[0];
      $('cOut').textContent = mf(cut) + ' / 200';
      $('cOutN').textContent = 'Mathematics ' + M + ' + Physics ' + Pp + ' ÷ 2 + Chemistry ' + C + ' ÷ 2. ' + (rd ? 'In 2026 this cut-off was called in Round ' + rd[0] + '.' : cut > 171.333 && cut < 171.5 ? 'In 2026 this fell between the Round 1 and Round 2 bands.' : cut < 77.5 ? 'Below the lowest cut-off called in 2026 (77.5).' : '');
      $('cRank').textContent = rk ? 'About rank ' + nf(rk) : '–';
      $('cRankN').textContent = rk ? 'Of about ' + nf(D.ranklist) + ' candidates called in 2026: roughly the top ' + Math.max(0.01, 100 * rk / D.ranklist).toFixed(1) + '%.' : '';
      var steps = [-2, -1, 1, 2].map(function (s) { return [s, rankAt(cut + s)]; });
      $('cStep').innerHTML = steps.map(function (x) { return '<div class="tq-rate"><span>' + (x[0] > 0 ? '+' : '') + x[0] + ' mark' + (Math.abs(x[0]) > 1 ? 's' : '') + ' (' + mf(cut + x[0]) + ')</span><b>rank ' + nf(x[1]) + '</b></div>'; }).join('') +
        '<p class="tq-sub" style="margin-top:6px">One more mark in Mathematics adds a full mark to the cut-off; in Physics or Chemistry, half a mark.</p>';
      mk('cCurve', { type: 'line', data: { labels: CURVE.filter(function (c, i) { return i % 4 === 0 && c[0] >= 80; }).map(function (c) { return c[0]; }), datasets: [{ label: 'Typical 2026 rank', data: CURVE.filter(function (c, i) { return i % 4 === 0 && c[0] >= 80; }).map(function (c) { return c[1]; }), borderColor: NAVY, pointRadius: 0, tension: .2 }] },
        options: { maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { x: { reverse: false, title: { display: true, text: 'Cut-off' } }, y: { title: { display: true, text: 'Rank' } } } } });
    };
    ['cM', 'cP', 'cC'].forEach(function (id) { $(id).addEventListener('input', calc); }); calc();
    full().then(function (d) {
      var cols = d.colleges.slice().sort(function (a, b) { return a.short.localeCompare(b.short); });
      $('cI').innerHTML = cols.map(function (c) { return '<option value="' + c.c + '">' + esc(c.short) + '</option>'; }).join(''); $('cI').value = '1';
      var rowsOf = function () { return d.rows.filter(function (r) { return String(r.c) === $('cI').value; }); };
      var fillB = function () { $('cB').innerHTML = rowsOf().map(function (r, k) { return '<option value="' + k + '">' + esc(r.n) + '</option>'; }).join(''); need(); };
      var need = function () {
        var r = rowsOf()[+$('cB').value]; if (!r) return;
        $('cNeed').innerHTML = '<h3 style="margin:10px 0 4px">' + esc(d.col[r.c].short) + ' · ' + esc(r.n) + '</h3><p class="tq-sub">' + (SITES[r.c] ? '<a href="' + esc(SITES[r.c]) + '" target="_blank" rel="noopener nofollow">Official website ↗</a> · ' : '') + 'Closing cut-off (and rank) for each community. Your cut-off must be this or higher.</p><div class="tq-tablewrap"><table class="tq-table"><thead><tr><th>Community</th><th class="n">Round 1</th><th class="n">Round 2</th><th class="n">Round 3</th><th class="n">Final 2026</th><th class="n">Seats 2026</th><th class="n">2025 sheet</th></tr></thead><tbody>' +
          COMMS.map(function (c) {
            var seats = 0; ['1', '2', '3'].forEach(function (k) { var v = cell(r, k, c); if (v) seats += v[2]; }); var f0 = fin(r, c);
            return '<tr' + (c === 'OC' ? ' style="font-weight:700"' : '') + '><td>' + c + ' · ' + esc(CN[c] || '') + '</td>' + ['1', '2', '3'].map(function (k) { var v = cell(r, k, c); return '<td class="n">' + (v ? mf(v[0]) + ' <span class="tq-ct">' + nf(v[1]) + '</span>' : '–') + '</td>'; }).join('') +
              '<td class="n" style="background:#FFF6EA">' + (f0 ? '<b>' + mf(f0[0]) + '</b> <span class="tq-ct">' + nf(f0[1]) + '</span>' : '–') + '</td><td class="n">' + (seats || '–') + '</td><td class="n">' + mf(r.y25 ? r.y25[d.ci[c]] : null) + '</td></tr>';
          }).join('') + '</tbody></table></div>';
      };
      $('cI').addEventListener('change', fillB); $('cB').addEventListener('change', need); fillB();
    });
  };

  /* ---------- cut-off analytics ---------- */
  BUILD.trend = function () {
    var top = D.top || [];
    $('heat').innerHTML = '<thead><tr><th>College</th>' + FAM_ORDER.map(function (f) { return '<th>' + esc((FN[f] || f).split(' ')[0].replace(',', '')) + '</th>'; }).join('') + '</tr></thead><tbody>' +
      top.map(function (t) { return '<tr><td class="nm" title="' + esc(t.n) + '">' + esc(t.n) + '</td>' + FAM_ORDER.map(function (f) { var v = null; t.rows.forEach(function (r) { var x = r.fin ? r.fin[0] : null; if (r.f === f && x != null && (v == null || x > v)) v = x; }); return '<td style="background:' + heat(v) + ';color:' + (v != null && v >= 170 ? '#fff' : '#3A4259') + '">' + (v == null ? '' : mf(v)) + '</td>'; }).join('') + '</tr>'; }).join('') + '</tbody>';
    var ds = {}; MAPROWS.forEach(function (r) { if (r.d) ds[r.d] = 1; });
    $('tD').innerHTML += Object.keys(ds).sort().map(function (k) { return '<option>' + esc(k) + '</option>'; }).join('');
    $('tF').innerHTML += FAM_ORDER.concat(['OTHER']).map(function (f) { return '<option value="' + f + '">' + esc(FN[f]) + '</option>'; }).join('');
    $('tT').innerHTML += TKEYS.map(function (t) { return '<option value="' + t + '">' + esc(TYPEN[t]) + '</option>'; }).join('');
    $('tCat').innerHTML = (D.comms || []).map(function (c) { return '<option value="' + c[0] + '">' + c[0] + ' · ' + esc(c[1]) + '</option>'; }).join('');
    full().then(function (d) {
      var draw = function () {
        var q = $('tQ').value.trim().toLowerCase(), dd = $('tD').value, f = $('tF').value, t = $('tT').value, cat = $('tCat').value, s = $('tS').value;
        var out = d.rows.filter(function (r) { var c = d.col[r.c]; return (!q || (c.short + ' ' + (c.d || '') + ' ' + c.c).toLowerCase().indexOf(q) >= 0) && (!dd || c.d === dd) && (!f || r.f === f) && (!t || c.t === t); })
          .map(function (r) { var v = ['1', '2', '3', 'fin', 'y25'].map(function (k) { return mark(r, k, cat); }); return { r: r, v: v, ch: v[3] != null && v[4] != null ? v[3] - v[4] : null, ref: v[3] }; })
          .filter(function (o) { return o.v.some(function (x) { return x != null; }); });
        out.sort(function (a, b) {
          if (s === 'name') return d.col[a.r.c].short.localeCompare(d.col[b.r.c].short);
          if (s === 'up') return (b.ch == null ? -1e9 : b.ch) - (a.ch == null ? -1e9 : a.ch);
          if (s === 'down') return (a.ch == null ? 1e9 : a.ch) - (b.ch == null ? 1e9 : b.ch);
          return (b.ref == null ? -1 : b.ref) - (a.ref == null ? -1 : a.ref);
        });
        $('tCount').textContent = out.length + ' rows';
        $('tTbl').querySelector('tbody').innerHTML = out.slice(0, 150).map(function (o) { var c = d.col[o.r.c]; return '<tr><td><b>' + esc(c.short) + '</b>' + web(o.r.c) + '<div class="tq-ct">' + esc(c.d || '') + ' · ' + esc(TYPEN[c.t] || '') + ' · code ' + c.c + '</div></td><td>' + esc(o.r.n) + '</td>' + o.v.map(function (x, i) { return '<td class="n">' + (i === 3 ? '<b>' + mf(x) + '</b>' : mf(x)) + '</td>'; }).join('') + '<td class="n" style="color:' + (o.ch == null ? GREY : o.ch >= 0 ? RED : GR) + '">' + (o.ch == null ? '–' : (o.ch > 0 ? '+' : '') + mf(o.ch)) + '</td></tr>'; }).join('') || '<tr><td colspan="8">No rows match.</td></tr>';
      };
      ['tD', 'tF', 'tT', 'tCat', 'tS'].forEach(function (id) { $(id).addEventListener('change', draw); }); $('tQ').addEventListener('input', draw); draw();
      var cols = d.colleges.slice().sort(function (a, b) { return a.short.localeCompare(b.short); });
      $('gI').innerHTML = cols.map(function (c) { return '<option value="' + c.c + '">' + esc(c.short) + '</option>'; }).join(''); $('gI').value = '2006';
      var rowsOf = function () { return d.rows.filter(function (r) { return String(r.c) === $('gI').value; }); };
      var fillB = function () { $('gB').innerHTML = rowsOf().map(function (r, k) { return '<option value="' + k + '">' + esc(r.n) + '</option>'; }).join(''); plot(); };
      var plot = function () {
        var r = rowsOf()[+$('gB').value]; if (!r) return;
        var ks = ['y25', '1', '2', '3', 'fin'], cols2 = ['#B7C2DC', '#8FA8D6', '#3D5DA3', NAVY, OR];
        mk('cTrend', { type: 'bar', data: { labels: COMMS.map(function (c) { return c; }), datasets: ks.map(function (k, i) { return { label: BASIS[k], backgroundColor: cols2[i], data: COMMS.map(function (c) { return mark(r, k, c); }) }; }) },
          options: { maintainAspectRatio: false, plugins: { legend: { position: 'bottom' } }, scales: { y: { min: 70, max: 200, title: { display: true, text: 'Closing cut-off (higher = harder)' } } } } });
      };
      $('gI').addEventListener('change', fillB); $('gB').addEventListener('change', plot); fillB();
    });
  };

  /* ---------- predictor ---------- */
  var P = store.get('tnea_pred') || {}, RES = [];
  BUILD.predict = function () {
    $('pC').innerHTML += (D.comms || []).filter(function (c) { return c[0] !== 'OC'; }).map(function (c) { return '<option value="' + c[0] + '">' + c[0] + ' · ' + esc(c[1]) + '</option>'; }).join('');
    $('pT').innerHTML += TKEYS.map(function (t) { return '<option value="' + t + '">' + esc(TYPEN[t]) + '</option>'; }).join('');
    $('pRg').innerHTML += Object.keys(D.regions || {}).map(function (r) { return '<option>' + esc(r) + '</option>'; }).join('');
    $('pF').innerHTML += FAM_ORDER.map(function (f) { return '<option value="' + f + '">' + esc(FN[f]) + '</option>'; }).join('');
    ['pR', 'pC', 'pT', 'pRg', 'pF', 'pY'].forEach(function (id) { if (P[id] != null) $(id).value = P[id]; });
    seg('pShow', function () { render(); });
    if (P.done) run();
  };
  function run() {
    ['pR', 'pC', 'pT', 'pRg', 'pF', 'pY'].forEach(function (id) { P[id] = $(id).value; }); P.done = true; store.set('tnea_pred', P);
    $('pOut').hidden = false; $('pSum').textContent = 'Loading the official tables…';
    full().then(function (d) {
      var m = Math.min(200, Math.max(0, +P.pR || 0)), cat = P.pC, basis = P.pY || 'fin', cats = cat === 'OC' ? ['OC'] : ['OC', cat];
      RES = [];
      d.rows.forEach(function (r) {
        var c = d.col[r.c];
        if (P.pT && c.t !== P.pT) return; if (P.pRg && c.region !== P.pRg) return; if (P.pF && r.f !== P.pF) return;
        var best = null; cats.forEach(function (k) { var v = mark(r, basis, k); if (v != null && (!best || v < best.v)) best = { v: v, k: k }; });
        if (!best) return;
        var chance = m >= best.v + 3 ? 'Safe' : m >= best.v ? 'Likely' : m >= best.v - 3 ? 'Reach' : null;
        if (!chance) return;
        RES.push({ r: r, c: c, v: best.v, k: best.k, r1: mark(r, '1', 'OC'), chance: chance });
      });
      RES.sort(function (a, b) { return b.v - a.v; });
      var n = { Safe: 0, Likely: 0, Reach: 0 }; RES.forEach(function (x) { n[x.chance]++; });
      $('nS').textContent = n.Safe; $('nL').textContent = n.Likely; $('nRe').textContent = n.Reach;
      $('pSum').textContent = 'Cut-off ' + mf(m) + ' (about rank ' + nf(rankAt(m)) + ' in 2026) against ' + BASIS[basis] + ' closing marks for ' + cats.map(function (k) { return k + ' (' + (CN[k] || '') + ')'; }).join(' and ') + '. Sorted from the hardest seat down.' + (basis === 'y25' ? ' The 2025 sheet is unverified.' : '');
      render();
    });
  }
  function render() {
    var sh = segVal('pShow') || 'all', rows = RES.filter(function (x) { return sh === 'all' || x.chance === sh; });
    $('pCount').textContent = rows.length + ' courses' + (rows.length > 250 ? ' (first 250 shown)' : '');
    $('pTbl').querySelector('tbody').innerHTML = rows.slice(0, 250).map(function (x) {
      return '<tr><td><span class="tq-chance ' + x.chance + '">' + x.chance + '</span></td><td><b>' + esc(x.c.short) + '</b>' + web(x.c.c) + '<div class="tq-ct">' + esc(x.c.d || '') + ' · code ' + x.c.c + '</div></td><td>' + esc(x.r.n) + '</td><td class="tq-ct">' + x.k + ' · ' + esc(CN[x.k] || '') + '</td><td class="n">' + mf(x.v) + '</td><td class="n">' + mf(x.r1) + '</td><td class="tq-ct">' + esc(TYPEN[x.c.t] || '') + '</td></tr>';
    }).join('') || '<tr><td colspan="7">No courses within reach with these filters. Try All branches, All types or the 2026 final closing marks.</td></tr>';
  }
  $('pGo').addEventListener('click', run);

  /* ---------- previous / next ---------- */
  var ORDER = [].map.call(document.querySelectorAll('#tabs button'), function (b) { return [b.dataset.tab, b.textContent.trim()]; });
  ORDER.forEach(function (t, k) {
    var p = $('p-' + t[0]); if (!p) return;
    var nav = document.createElement('div'); nav.className = 'tq-pn';
    nav.innerHTML = (k > 0 ? '<button data-goto-tab="' + ORDER[k - 1][0] + '" class="prev">← ' + esc(ORDER[k - 1][1]) + '</button>' : '<span></span>') + (k < ORDER.length - 1 ? '<button data-goto-tab="' + ORDER[k + 1][0] + '" class="next">' + esc(ORDER[k + 1][1]) + ' →</button>' : '');
    p.appendChild(nav);
  });
  var start = (location.hash || '').slice(1);
  show(BUILD[start] ? start : 'overview');
})();
