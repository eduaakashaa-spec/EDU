(function () {
  'use strict';
  var D = window.EA_MHT || {};
  var YEARS = D.years || [2023, 2024, 2025], LAST = YEARS[YEARS.length - 1];
  var NAVY = '#0E3A8A', OR = '#FF6B0A', GR = '#1F8B5C', RED = '#C23A3A', GREY = '#8C93A6';
  var YCOL = { 2023: '#C9D6F0', 2024: '#8FA8D6', 2025: OR, 2026: NAVY };
  var FAM_ORDER = ['CSE', 'AI', 'IT', 'ENTC', 'ELEC', 'MECH', 'CIVIL', 'CHEM'];
  var FN = D.famNames || {};
  var $ = function (id) { return document.getElementById(id); };
  var esc = function (s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); };
  var fmt = function (v, d) { return v == null ? '–' : (+v).toFixed(d == null ? 2 : d); };
  var nf = function (n) { return n == null ? '–' : Math.round(n).toLocaleString('en-IN'); };
  var store = { get: function (k) { try { return JSON.parse(localStorage.getItem(k)); } catch (e) { return null; } }, set: function (k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) { /* ignore */ } } };
  var charts = {};
  if (window.Chart) { Chart.defaults.font.family = "'Plus Jakarta Sans',sans-serif"; Chart.defaults.font.size = 11; }
  function mk(id, cfg) { if (!window.Chart || !$(id)) return; if (charts[id]) charts[id].destroy(); charts[id] = new Chart($(id), cfg); }
  function pd(s) { var p = s.split('-'); return new Date(+p[0], +p[1] - 1, +p[2]); }
  function fd(s) { return pd(s).toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' }); }
  function seg(id, cb) {
    var el = $(id); if (!el) return;
    el.addEventListener('click', function (e) { var b = e.target.closest('button'); if (!b) return; el.querySelectorAll('button').forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); }); cb(b.dataset.v); });
  }
  function segVal(id) { var b = $(id).querySelector('[aria-pressed=true]'); return b ? b.dataset.v : null; }
  function heat(v) { // percentile -> background colour
    if (v == null) return '#F4F1E8';
    var t = Math.max(0, Math.min(1, (v - 85) / 15));
    var a = [232, 223, 200], b = [14, 58, 138];
    return 'rgb(' + a.map(function (x, i) { return Math.round(x + (b[i] - x) * t); }).join(',') + ')';
  }

  /* ---------- full official cut-off file (lazy) ---------- */
  var FULL = null, loading = null;
  function full() {
    if (FULL) return Promise.resolve(FULL);
    if (!loading) loading = fetch(window.EA_MHT_URL).then(function (r) { return r.json(); }).then(function (d) {
      d.ci = {}; d.cats.forEach(function (c, i) { d.ci[c] = i; });
      d.inst.forEach(function (i) { i.region = regionOf(i.city); i.short = shortName(i); });
      FULL = d; return d;
    }).catch(function (e) { loading = null; netErr(); throw e; });
    return loading;
  }
  var SITES = D.sites || {};
  function web(code) { var u = SITES[code]; return u ? ' <a class="mc-web" href="' + esc(u) + '" target="_blank" rel="noopener nofollow" title="Official website (opens in a new tab)" onclick="event.stopPropagation()">Website ↗</a>' : ''; }
  function netErr() {
    var p = document.querySelector('.mc-panel:not([hidden])'); if (!p || p.querySelector('.mc-neterr')) return;
    var n = document.createElement('div'); n.className = 'mc-card mc-note mc-neterr';
    n.innerHTML = '<strong>The cut-off data did not load.</strong> Check your internet connection, then <button class="mc-btn" type="button">Try again</button>';
    n.querySelector('button').onclick = function () { var tab = p.id.replace('p-', ''); n.remove(); built[tab] = false; show(tab); if (tab === 'predict' && P.done) run(); };
    p.insertBefore(n, p.firstChild);
  }
  var R2C = {};
  Object.keys(D.regionMap || {}).forEach(function (r) { D.regionMap[r].forEach(function (c) { R2C[c] = r; }); });
  function regionOf(c) { return R2C[c] || 'Other'; }
  var SHORT = {}; (D.top || []).concat(D.nirf_cap || []).forEach(function (t) { SHORT[t.c] = t.n; });
  function shortName(i) { return SHORT[i.c] || i.n; }
  function val(b, y, lv, cat) {
    var row = ((b.y[String(y)] || {})[lv]) || [], ix = FULL.ci[cat];
    for (var k = 0; k < row.length; k++) if (row[k][0] === ix) return row[k][1] / 1e4;
    return null;
  }
  function openCut(b, y) {
    var v = val(b, y, 'S', 'GOPEN'); if (v != null) return [v, 'State'];
    v = val(b, y, 'H', 'GOPEN'); if (v != null) return [v, 'Home Univ'];
    v = val(b, y, 'S', 'LOPEN'); if (v != null) return [v, 'Women, State'];
    v = val(b, y, 'H', 'LOPEN'); if (v != null) return [v, 'Women, Home Univ'];
    return [null, null];
  }
  function catCut(b, y, cat) {
    var v = val(b, y, 'S', cat); if (v != null) return [v, 'State'];
    v = val(b, y, 'H', cat); if (v != null) return [v, 'Home Univ'];
    return [null, null];
  }
  // percentile -> state merit rank (interpolated on the official curve)
  function rankOf(p, y) {
    var c = (D.curve || {})[String(y)] || []; if (!c.length || p == null) return null;
    if (p >= c[0][0]) return c[0][1];
    for (var i = 1; i < c.length; i++) {
      if (p >= c[i][0]) { var a = c[i - 1], b = c[i], t = (a[0] - p) / (a[0] - b[0]); return a[1] + (b[1] - a[1]) * t; }
    }
    return c[c.length - 1][1];
  }

  /* ---------- tabs ---------- */
  var built = {}, BUILD = {};
  function show(tab) {
    document.querySelectorAll('#tabs button').forEach(function (b) { b.setAttribute('aria-selected', b.dataset.tab === tab ? 'true' : 'false'); });
    document.querySelectorAll('.mc-panel').forEach(function (p) { p.hidden = p.id !== 'p-' + tab; });
    if (!built[tab] && BUILD[tab]) { BUILD[tab](); built[tab] = true; }
    try { history.replaceState(null, '', '#' + tab); } catch (e) { /* ignore */ }
  }
  $('tabs').addEventListener('click', function (e) { var b = e.target.closest('button'); if (b) show(b.dataset.tab); });
  document.addEventListener('click', function (e) { var g = e.target.closest('[data-goto-tab]'); if (!g) return; e.preventDefault(); show(g.dataset.gotoTab); $('tabs').scrollIntoView({ behavior: 'smooth' }); });

  /* ---------- KPIs ---------- */
  (function () {
    var c26 = (D.candidates || []).slice(-1)[0] || [];
    var t1 = (D.top || [])[0];
    var k = [
      ['16–26 Apr', 'MHT CET 2027 PCM', 'attempt 1; attempt 2 on 10–15 May (tentative)'],
      [(c26[2] / 1e5).toFixed(2) + ' lakh', 'appeared in 2026', 'PCM attempt 1'],
      [D.n_inst, 'colleges with official cut-offs', D.n_br + ' courses, CAP Round I ' + YEARS[0] + '–' + LAST],
      [t1 ? fmt(t1.best.cut[LAST], 2) : '–', 'top cut-off ' + LAST, t1 ? t1.n + ', ' + t1.best.n : '']
    ];
    $('kpis').innerHTML = k.map(function (x) { return '<div class="mc-kpi"><b>' + esc(x[0]) + '</b><span>' + esc(x[1]) + '</span><small>' + esc(x[2]) + '</small></div>'; }).join('');
  })();

  /* ---------- overview ---------- */
  BUILD.overview = function () {
    $('dates').innerHTML = (D.dates || []).map(function (d) {
      var cls = d[4] === 'Official' ? 'd' : d[4] === 'Reported' ? 'p' : 'b';
      return '<div class="mc-gap ' + cls + '"><span class="m">' + fd(d[2]) + (d[3] !== d[2] ? ' – ' + fd(d[3]) : '') + ' · ' + d[4] + '</span><br><b>' + esc(d[1]) + '</b><br><span class="mc-ct">' + esc(d[5]) + '</span></div>';
    }).join('');
    $('pattern').innerHTML = (D.pattern || []).map(function (p) { return '<div class="mc-rate"><b>' + esc(p[0]) + '</b><span style="font-size:13px">' + esc(p[1]) + '</span></div>'; }).join('');
    var cd = D.candidates || [];
    mk('cCand', { type: 'bar', data: { labels: cd.map(function (c) { return c[0]; }), datasets: [{ label: 'Registered', data: cd.map(function (c) { return c[1]; }), backgroundColor: '#C9D6F0' }, { label: 'Appeared', data: cd.map(function (c) { return c[2]; }), backgroundColor: NAVY }] },
      options: { maintainAspectRatio: false, plugins: { legend: { position: 'bottom' } }, scales: { y: { ticks: { callback: function (v) { return (v / 1e5) + 'L'; } } } } } });
    var f = D.fam || {}, y0 = String(YEARS[0]), y1 = String(LAST);
    var g = function (k, y) { return f[k] && f[k][y] ? f[k][y].med : null; };
    var top = D.top || [];
    var ins = [
      'Core branches got much harder to enter: the median Round I open cut-off for Mechanical rose from ' + fmt(g('MECH', y0), 1) + ' to ' + fmt(g('MECH', y1), 1) + ' and for Civil from ' + fmt(g('CIVIL', y0), 1) + ' to ' + fmt(g('CIVIL', y1), 1) + ' between ' + y0 + ' and ' + y1 + '.',
      'Computer/CSE stayed the most wanted branch at the top colleges, but its median across all colleges eased from ' + fmt(g('CSE', y0), 1) + ' to ' + fmt(g('CSE', y1), 1) + ' as seats grew (' + (f.CSE && f.CSE[y0] ? f.CSE[y0].n : '–') + ' to ' + (f.CSE && f.CSE[y1] ? f.CSE[y1].n : '–') + ' courses). AI and Data Science courses grew even faster.',
      'The top ' + top.length + ' colleges by demand all closed above ' + fmt(top.length ? top[top.length - 1].best.cut[y1] : null, 1) + ' percentile for their best course in ' + y1 + '. VJTI, COEP, SPIT, ICT and PICT need about 99.7 or more for their best course.',
      'More students every year: ' + cd.map(function (c) { return c[0] + ': ' + (c[2] / 1e5).toFixed(2) + ' lakh'; }).join(', ') + ' appeared. A 99 percentile was about state merit rank ' + nf(rankOf(99, LAST)) + ' in ' + LAST + '.',
      'From 2027 there are two attempts (April and May); only the better total percentile counts. Plan the first attempt seriously: it is compulsory.',
      'The HSC theory exams end in early March and MHT CET starts in mid-April: about five weeks to switch from board answers to fast multiple-choice practice.'
    ];
    $('insights').innerHTML = ins.map(function (x) { return '<li>' + x + '</li>'; }).join('');
  };
  $('ics').addEventListener('click', function () {
    var d8 = function (s) { return s.replace(/-/g, ''); }, nx = function (s) { var x = pd(s); x.setDate(x.getDate() + 1); return x.getFullYear() + String(x.getMonth() + 1).padStart(2, '0') + String(x.getDate()).padStart(2, '0'); };
    var clean = function (s) { return String(s).replace(/[\\;,]/g, function (c) { return '\\' + c; }); };
    var stamp = new Date().toISOString().replace(/[-:]/g, '').replace(/\.\d+/, '');
    var L = ['BEGIN:VCALENDAR', 'VERSION:2.0', 'PRODID:-//EduAakashaA//MHT CET 2027//EN', 'X-WR-CALNAME:MHT CET 2027 and CAP'];
    (D.dates || []).forEach(function (d) {
      L.push('BEGIN:VEVENT', 'UID:' + d[0] + '-mhtcet2027@eduaakashaa.com', 'DTSTAMP:' + stamp, 'DTSTART;VALUE=DATE:' + d8(d[2]), 'DTEND;VALUE=DATE:' + nx(d[3]),
        'SUMMARY:' + clean(d[1] + (d[4] === 'Expected' ? ' (expected)' : '')), 'DESCRIPTION:' + clean(d[4] + '. ' + d[5] + ' Confirm on cetcell.mahacet.org.'), 'TRANSP:TRANSPARENT', 'END:VEVENT');
    });
    L.push('END:VCALENDAR');
    var a = document.createElement('a'); a.href = URL.createObjectURL(new Blob([L.join('\r\n')], { type: 'text/calendar' })); a.download = 'mht-cet-2027-and-cap.ics';
    document.body.appendChild(a); a.click(); setTimeout(function () { URL.revokeObjectURL(a.href); a.remove(); }, 500);
  });

  /* ---------- colleges map ---------- */
  var KIND = { govt: 'Government', aided: 'Government-aided', univ: 'University / deemed', pvt: 'Private unaided' };
  var MAPROWS = (D.map || []).map(function (r) { return { c: r[0], n: r[1], d: r[2], k: r[3], auto: r[4], nirf: r[5], best: r[6], bestN: r[7], courses: r[8], cs: r[9], top: r[10] }; });
  var RAMP = ['#FBF7EE', '#E8DFC8', '#B7C2DC', '#7B91C2', '#3D5DA3', '#0E3A8A'];
  var mapState = { metric: 'n', filter: 'all', sel: null };
  function mapFilter(r) {
    var f = mapState.filter;
    return f === 'all' || f === 'top' ? true : f === 'gov' ? (r.k === 'govt' || r.k === 'aided' || r.k === 'univ') : f === 'auto' ? r.auto : f === 'nirf' ? !!r.nirf : true;
  }
  function distAgg() {
    var A = {};
    MAPROWS.filter(mapFilter).forEach(function (r) {
      if (!r.d) return;
      var a = A[r.d] = A[r.d] || { n: 0, courses: 0, gov: 0, auto: 0, cs: null, rows: [] };
      a.n++; a.courses += r.courses; if (r.k !== 'pvt') a.gov++; if (r.auto) a.auto++; if (r.cs != null && (a.cs == null || r.cs > a.cs)) a.cs = r.cs; a.rows.push(r);
    });
    return A;
  }
  var METRIC_LABEL = { n: 'colleges', courses: 'courses', gov: 'government & aided colleges', cs: 'best Computer cut-off' };
  function colorFor(v, max, metric) {
    if (v == null || !v) return RAMP[0];
    var r = metric === 'cs' ? Math.max(0, (v - 85) / 15) : v / max;
    return r < .04 ? RAMP[1] : r < .12 ? RAMP[2] : r < .28 ? RAMP[3] : r < .6 ? RAMP[4] : RAMP[5];
  }
  var MAPGEO = null, mapPath = null;
  BUILD.map = function () {
    seg('mMetric', function (v) { mapState.metric = v; drawMap(); });
    seg('mFilter', function (v) { mapState.filter = v; drawMap(); });
    var miss = MAPROWS.filter(function (r) { return !r.d; }).length;
    $('mapNote').textContent = 'District from the college\'s town in the official CAP list; ' + miss + ' colleges whose name gives no town are counted in the charts but not on the map. Mumbai City and Mumbai Suburban are shown as one district. Pins for the top 20 sit on their district, not their exact address.';
    if (!window.d3) { $('mapSide').innerHTML = '<p class="mc-sub">The map could not load (no connection to the chart library). The tables below still work.</p>'; }
    else d3.json(window.EA_MH_GEO).then(function (geo) {
      MAPGEO = geo;
      var svg = d3.select('#mhMap');
      var proj = d3.geoMercator().fitSize([720, 560], geo);
      mapPath = d3.geoPath().projection(proj);
      svg.append('g').attr('class', 'districts');
      svg.append('g').attr('class', 'labels');
      svg.append('g').attr('class', 'pins');
      svg.select('.districts').selectAll('path').data(geo.features).enter().append('path')
        .attr('class', 'district').attr('d', mapPath)
        .on('mousemove', function (ev, f) { tip(ev, f.properties.district); })
        .on('mouseleave', function () { $('mapTip').hidden = true; })
        .on('click', function (ev, f) { mapState.sel = f.properties.district; drawMap(); });
      svg.select('.labels').selectAll('text').data(geo.features).enter().append('text')
        .attr('class', 'dlabel').attr('x', function (f) { return mapPath.centroid(f)[0]; }).attr('y', function (f) { return mapPath.centroid(f)[1]; })
        .text(function (f) { return f.properties.district; });
      drawMap();
    }).catch(function () { $('mapSide').innerHTML = '<p class="mc-sub">The map file could not load. Try again later; the tables below still work.</p>'; });
    drawSideCharts();
  };
  function tip(ev, name) {
    var a = distAgg()[name], box = $('mhMap').getBoundingClientRect(), t = $('mapTip');
    t.innerHTML = '<b>' + esc(name) + '</b><br>' + (a ? a.n + ' colleges · ' + a.courses + ' courses<br>' + a.gov + ' government or aided · ' + a.auto + ' autonomous' + (a.cs ? '<br>Best Computer cut-off ' + fmt(a.cs, 2) : '') : 'No CAP college in this view') + '<br><span>Click for the list</span>';
    t.hidden = false;
    var x = ev.clientX - box.left + 14, y = ev.clientY - box.top + 14;
    t.style.left = Math.min(x, box.width - 220) + 'px'; t.style.top = Math.min(y, box.height - 90) + 'px';
  }
  function drawMap() {
    var A = distAgg(), m = mapState.metric;
    var vals = Object.keys(A).map(function (k) { return A[k][m] || 0; }), max = Math.max.apply(null, vals.concat([1]));
    if (MAPGEO) {
      d3.select('#mhMap .districts').selectAll('path')
        .attr('fill', function (f) { var a = A[f.properties.district]; return colorFor(a ? a[m] : 0, max, m); })
        .classed('selected', function (f) { return f.properties.district === mapState.sel; });
      d3.select('#mhMap .labels').selectAll('text').attr('fill', function (f) { var a = A[f.properties.district]; var v = a ? a[m] : 0; return (m === 'cs' ? v > 95 : v / max > .28) ? '#fff' : '#3A4259'; });
      // top 20 pins on their district (spread in a small circle when a district has several)
      var pins = mapState.filter === 'top' ? MAPROWS.filter(function (r) { return r.top && r.d; }) : [];
      var byD = {}; pins.forEach(function (r) { (byD[r.d] = byD[r.d] || []).push(r); });
      var cent = {}; MAPGEO.features.forEach(function (f) { cent[f.properties.district] = mapPath.centroid(f); });
      var pts = []; Object.keys(byD).forEach(function (dn) { var list = byD[dn]; list.forEach(function (r, k) { var ang = 2 * Math.PI * k / list.length, rad = list.length > 1 ? 9 + list.length * 1.6 : 0; pts.push({ r: r, x: cent[dn][0] + rad * Math.cos(ang), y: cent[dn][1] + rad * Math.sin(ang) }); }); });
      var sel = d3.select('#mhMap .pins').selectAll('g.pin').data(pts, function (p) { return p.r.c; });
      sel.exit().remove();
      var g = sel.enter().append('g').attr('class', 'pin').attr('transform', function (p) { return 'translate(' + p.x + ',' + p.y + ')'; })
        .on('mousemove', function (ev, p) { var box = $('mhMap').getBoundingClientRect(), t = $('mapTip'); t.innerHTML = '<b>#' + p.r.top + ' ' + esc(p.r.n) + '</b><br>' + esc(p.r.bestN) + ': ' + fmt(p.r.best, 2) + (p.r.nirf ? '<br>NIRF 2025: ' + esc(p.r.nirf) : ''); t.hidden = false; t.style.left = Math.min(ev.clientX - box.left + 14, box.width - 220) + 'px'; t.style.top = (ev.clientY - box.top + 14) + 'px'; })
        .on('mouseleave', function () { $('mapTip').hidden = true; })
        .on('click', function (ev, p) { mapState.sel = p.r.d; drawMap(); });
      g.append('circle').attr('r', 0).transition().duration(350).delay(function (p, i) { return i * 20; }).attr('r', 8);
      g.append('text').attr('class', 'pinlabel').attr('dy', '0.35em').text(function (p) { return p.r.top; });
    }
    // legend
    var lab = m === 'cs' ? ['no data', '85+', '86+', '87+', '89+', '94+'] : ['0', '1+', Math.ceil(max * .04) + '+', Math.ceil(max * .12) + '+', Math.ceil(max * .28) + '+', Math.ceil(max * .6) + '+'];
    $('mapLegend').innerHTML = '<span>' + esc(METRIC_LABEL[m]) + '</span>' + RAMP.map(function (c, k) { return '<i style="background:' + c + '"></i><em>' + lab[k] + '</em>'; }).join('');
    if (mapState.sel) drillDown(mapState.sel, A); else topDistricts(A);
  }
  function topDistricts(A) {
    var m = mapState.metric, list = Object.keys(A).map(function (k) { return [k, A[k]]; }).filter(function (x) { return x[1][m] != null; })
      .sort(function (a, b) { return (b[1][m] || 0) - (a[1][m] || 0); }).slice(0, 12);
    var max = list.length ? list[0][1][m] || 1 : 1;
    $('mapSide').innerHTML = '<h3>Top districts by ' + esc(METRIC_LABEL[m]) + '</h3><p class="mc-sub">Click a district on the map or here.</p><ol class="mc-rank">' +
      list.map(function (x) { var v = x[1][m]; var w = m === 'cs' ? Math.max(4, (v - 80) / 20 * 100) : v / max * 100; return '<li data-d="' + esc(x[0]) + '"><span>' + esc(x[0]) + '</span><i><b style="width:' + w + '%"></b></i><em>' + (m === 'cs' ? fmt(v, 2) : v) + '</em></li>'; }).join('') + '</ol>';
  }
  function drillDown(name, A) {
    var a = A[name];
    var rows = a ? a.rows.slice().sort(function (x, y) { return (y.best || 0) - (x.best || 0); }) : [];
    $('mapSide').innerHTML = '<div class="mc-drillhead"><div><small>District</small><h3>' + esc(name) + '</h3></div><button class="mc-back" id="mapBack">All districts</button></div>' +
      (a ? '<div class="mc-tiles"><div><b>' + a.n + '</b>colleges</div><div><b>' + a.courses + '</b>courses</div><div><b>' + a.gov + '</b>govt / aided</div><div><b>' + (a.cs ? fmt(a.cs, 2) : '–') + '</b>best Computer</div></div>' +
        '<ul class="mc-clist">' + rows.map(function (r) {
          return '<li><b>' + esc(r.n) + '</b>' + web(r.c) + '<div class="mc-chips">' + (r.top ? '<span class="mc-pill o">Top 20 #' + r.top + '</span>' : '') + (r.nirf ? '<span class="mc-pill n">NIRF ' + esc(r.nirf) + '</span>' : '') + '<span class="mc-pill">' + esc(KIND[r.k]) + '</span>' + (r.auto ? '<span class="mc-pill">Autonomous</span>' : '') + '</div>' +
            '<span class="mc-ct">' + (r.best != null ? 'Best course ' + LAST + ': ' + esc(r.bestN) + ' · ' + fmt(r.best, 2) : 'No open-category cut-off in ' + LAST) + '</span></li>';
        }).join('') + '</ul>' : '<p class="mc-sub">No CAP college in this district for the current filter.</p>');
    $('mapBack').onclick = function () { mapState.sel = null; drawMap(); };
  }
  $('mapSide').addEventListener('click', function (e) { var li = e.target.closest('li[data-d]'); if (li) { mapState.sel = li.dataset.d; drawMap(); } });
  function drawSideCharts() {
    var R = {}; MAPROWS.forEach(function (r) { var k = r.d ? (R2C[r.d] || 'Other') : 'District not identified'; R[k] = (R[k] || 0) + 1; });
    var rk = Object.keys(R).sort(function (a, b) { return R[b] - R[a]; });
    var cols = [NAVY, OR, GR, '#7A4FD6', '#0A8FA8', RED, '#B8860B', GREY];
    mk('cRegion', { type: 'doughnut', data: { labels: rk, datasets: [{ data: rk.map(function (k) { return R[k]; }), backgroundColor: cols, borderWidth: 2 }] }, options: { maintainAspectRatio: false, cutout: '55%', plugins: { legend: { position: 'right', labels: { boxWidth: 12 } } } } });
    var kinds = ['pvt', 'govt', 'aided', 'univ'];
    mk('cKind', { type: 'bar', data: { labels: kinds.map(function (k) { return KIND[k]; }), datasets: [
      { label: 'Autonomous', backgroundColor: NAVY, data: kinds.map(function (k) { return MAPROWS.filter(function (r) { return r.k === k && r.auto; }).length; }) },
      { label: 'Affiliated', backgroundColor: '#B7C2DC', data: kinds.map(function (k) { return MAPROWS.filter(function (r) { return r.k === k && !r.auto; }).length; }) }] },
      options: { indexAxis: 'y', maintainAspectRatio: false, plugins: { legend: { position: 'bottom' } }, scales: { x: { stacked: true }, y: { stacked: true } } } });
    var h = D.hist || [];
    mk('cHist', { type: 'bar', data: { labels: h.map(function (x) { return x[0]; }), datasets: [{ data: h.map(function (x) { return x[1]; }), backgroundColor: h.map(function (x, i) { return i < 3 ? RED : i < 5 ? OR : NAVY; }), borderRadius: 5 }] },
      options: { maintainAspectRatio: false, plugins: { legend: { display: false }, tooltip: { callbacks: { label: function (c) { return c.raw + ' courses'; } } } }, scales: { x: { title: { display: true, text: 'Open cut-off (percentile)' } } } } });
    var all = {}; MAPROWS.forEach(function (r) { if (!r.d) return; var a = all[r.d] = all[r.d] || { n: 0, c: 0, g: 0, au: 0, cs: null, csN: '' }; a.n++; a.c += r.courses; if (r.k !== 'pvt') a.g++; if (r.auto) a.au++; if (r.cs != null && (a.cs == null || r.cs > a.cs)) { a.cs = r.cs; a.csN = r.n; } });
    $('distTbl').querySelector('tbody').innerHTML = Object.keys(all).sort(function (a, b) { return all[b].n - all[a].n; }).slice(0, 10).map(function (k) { var a = all[k]; return '<tr><td><b>' + esc(k) + '</b><div class="mc-ct">' + esc(R2C[k] || '') + '</div></td><td class="n">' + a.n + '</td><td class="n">' + a.c + '</td><td class="n">' + a.g + '</td><td class="n">' + a.au + '</td><td>' + (a.cs ? fmt(a.cs, 2) + ' <span class="mc-ct">' + esc(a.csN) + '</span>' : '–') + '</td></tr>'; }).join('');
  }

  /* ---------- eligibility ---------- */
  BUILD.elig = function () {
    $('elig').innerHTML = (D.elig || []).map(function (e) { return '<div class="mc-gap d"><b>' + esc(e[0]) + '</b><br>' + esc(e[1]) + '</div>'; }).join('');
    $('cand').innerHTML = (D.cand || []).map(function (e) { return '<div class="mc-gap b"><b>' + esc(e[0]) + '</b> · ' + esc(e[1]) + '</div>'; }).join('');
    $('seats').innerHTML = (D.seats || []).map(function (e) { return '<div class="mc-gap d"><b>' + esc(e[0]) + '</b><br>' + esc(e[1]) + '</div>'; }).join('');
    var cols = ['#C23A3A', '#B8860B', '#7A4FD6', '#0A8FA8', '#2E7D32', '#AD1457', '#FF6B0A', '#556', '#0E3A8A'];
    $('resv').innerHTML = (D.resv || []).map(function (r, i) { return '<span style="width:' + r[1] + '%;background:' + cols[i % cols.length] + '" title="' + esc(r[0]) + ' ' + r[1] + '%">' + (r[1] >= 7 ? esc(r[0]) + ' ' + r[1] + '%' : '') + '</span>'; }).join('');
    $('resvNote').textContent = (D.resv || []).map(function (r) { return r[0] + ' ' + r[1] + '%'; }).join(' · ') + '. ' + D.resvNote;
    $('stats26').innerHTML = (D.stats26 || []).map(function (s) { return '<div class="mc-gap b"><b>' + esc(s[0]) + '</b><br>' + esc(s[1]) + '</div>'; }).join('');
    var chk = function () {
      var p = +$('eP').value, c = $('eC').value, t = $('eT').value;
      var need = (t === 'mh' && c !== 'open') ? 40 : 45, ok = Math.round(p) >= need;
      $('eOut').innerHTML = '<div class="mc-gap ' + (ok ? 'd' : '') + '"><b>' + (ok ? 'Eligible on marks' : 'Not eligible on marks') + '</b><br>You need at least ' + need + '% in Physics, Chemistry and Mathematics together' + (t === 'ai' && c !== 'open' ? ' (the 40% concession is for Maharashtra candidates only)' : '') + '; you entered ' + p + '% (rounded: ' + Math.round(p) + '%). You also need a non-zero MHT CET PCM score' + (t === 'ai' ? ' or a JEE Main score (preferred for All India seats)' : '') + '.</div>';
    };
    ['eP', 'eC', 'eT'].forEach(function (id) { $(id).addEventListener('input', chk); $(id).addEventListener('change', chk); });
    chk();
  };

  /* ---------- top 20 ---------- */
  BUILD.top = function () {
    var top = D.top || [];
    $('topTbl').querySelector('tbody').innerHTML = top.map(function (t, i) {
      var b = t.best;
      return '<tr data-i="' + i + '"><td><span class="mc-rk">' + (i + 1) + '</span></td><td><b>' + esc(t.n) + '</b>' + web(t.c) + '<div class="mc-ct">' + esc(t.city || t.region) + '</div></td><td>' + (t.nirf ? '<span class="mc-pill">' + esc(t.nirf) + '</span>' : '<span class="mc-ct">not in top 300</span>') + '</td><td class="mc-ct">' + esc(t.kind) + '</td><td>' + esc(b.n) + (b.seat && b.seat.indexOf('Women') === 0 ? ' <span class="mc-pill">women</span>' : '') + '</td>' +
        YEARS.map(function (y) { return '<td class="n">' + fmt(b.cut[y], 2) + '</td>'; }).join('') + '</tr>';
    }).join('');
    $('topTbl').addEventListener('click', function (e) {
      var tr = e.target.closest('tr[data-i]'); if (!tr) return;
      var t = top[+tr.dataset.i], el = $('topDetail');
      var rows = t.rows.slice().sort(function (a, b) { return (b.cut[LAST] || 0) - (a.cut[LAST] || 0); });
      el.hidden = false;
      el.innerHTML = '<h2>' + esc(t.n) + '</h2><p class="mc-sub">' + (SITES[t.c] ? '<a href="' + esc(SITES[t.c]) + '" target="_blank" rel="noopener nofollow">Official website ↗</a> · ' : '') + esc(t.full) + ' · institute code ' + t.c + ' · ' + esc(t.kind) + (t.hu ? ' · ' + esc(t.hu) : '') + (t.nirf ? ' · NIRF 2025: ' + esc(t.nirf) : '') + '</p>' +
        '<div class="mc-tablewrap"><table class="mc-table"><thead><tr><th>Course</th><th>Branch group</th><th>Seat</th>' + YEARS.map(function (y) { return '<th class="n">' + y + '</th>'; }).join('') + '</tr></thead><tbody>' +
        rows.map(function (r) { return '<tr><td>' + esc(r.n) + '</td><td class="mc-ct">' + esc(FN[r.f] || r.f) + '</td><td class="mc-ct">' + esc(r.seat || '–') + '</td>' + YEARS.map(function (y) { return '<td class="n">' + fmt(r.cut[y], 2) + '</td>'; }).join('') + '</tr>'; }).join('') +
        '</tbody></table></div><p class="mc-sub" style="margin-top:6px">Round I closing percentile, open category. A blank means the course was not in that year\'s Round I list.</p>';
      el.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
    $('nirfCap').innerHTML = (D.nirf_cap || []).map(function (t) { return '<div class="mc-gap d"><span class="m">NIRF 2025: ' + esc(t.nirf) + ' · ' + esc(t.city) + '</span><br><b>' + esc(t.n) + '</b>' + web(t.c) + '<br><span class="mc-ct">Best 2025 course: ' + esc(t.best.n) + ' at ' + fmt(t.best.cut[LAST], 2) + '</span></div>'; }).join('') +
      '<div class="mc-gap b"><b>Shri Ramdeobaba College of Engineering, Nagpur</b> (NIRF 151–200) became Ramdeobaba University and is not in the CAP lists after 2023.</div>';
    $('nirfNot').innerHTML = (D.nirfNotCap || []).map(function (n) { return '<div class="mc-gap b">' + esc(n) + '</div>'; }).join('');
  };

  /* ---------- branch selection ---------- */
  BUILD.branch = function () {
    var f = D.fam || {};
    var ds = function (key) { return YEARS.map(function (y) { return { label: String(y), backgroundColor: YCOL[y], data: FAM_ORDER.map(function (k) { return f[k] && f[k][y] ? f[k][y][key] : null; }) }; }); };
    var opts = { maintainAspectRatio: false, plugins: { legend: { position: 'bottom' } }, scales: { y: { min: 0, max: 100, title: { display: true, text: 'Percentile' } } } };
    mk('cFam', { type: 'bar', data: { labels: FAM_ORDER.map(function (k) { return FN[k]; }), datasets: ds('med') }, options: opts });
    var o2 = JSON.parse(JSON.stringify(opts)); o2.scales.y.min = 80;
    mk('cFam90', { type: 'bar', data: { labels: FAM_ORDER.map(function (k) { return FN[k]; }), datasets: ds('p90') }, options: o2 });
    $('guide').innerHTML = (D.guide || []).map(function (g) { return '<div class="mc-gap d"><b>' + esc(FN[g[0]] || g[0]) + '</b><br>' + esc(g[1]) + '</div>'; }).join('');
    var draw = function () {
      var p = +$('bP').value;
      full().then(function (d) {
        $('bTbl').querySelector('tbody').innerHTML = FAM_ORDER.map(function (fk) {
          var best = null, n = 0;
          d.inst.forEach(function (i) { i.br.forEach(function (b) {
            if (b.f !== fk) return; var c = openCut(b, LAST); if (c[0] == null || c[1].indexOf('Women') === 0) return;
            if (c[0] <= p) { n++; if (!best || c[0] > best.c) best = { i: i, b: b, c: c[0] }; }
          }); });
          return '<tr><td><b>' + esc(FN[fk]) + '</b></td><td>' + (best ? esc(best.i.short) + web(best.i.c) + '<div class="mc-ct">' + esc(best.i.city) + '</div>' : '<span class="mc-ct">none at this percentile</span>') + '</td><td>' + (best ? esc(best.b.n) : '') + '</td><td class="n">' + (best ? fmt(best.c, 2) : '–') + '</td><td class="n">' + n + '</td></tr>';
        }).join('');
      });
    };
    $('bP').addEventListener('input', draw); draw();
  };

  /* ---------- calculator ---------- */
  BUILD.calc = function () {
    var M = D.marks || [];
    var m2p = function (m) {
      for (var i = 1; i < M.length; i++) if (m >= M[i][0]) { var a = M[i - 1], b = M[i], t = (m - b[0]) / (a[0] - b[0]); return b[1] + (a[1] - b[1]) * t; }
      return 0;
    };
    var drawM = function () {
      var m = Math.max(0, Math.min(200, +$('cM').value || 0)), p = m2p(m);
      $('cMP').textContent = '≈ ' + p.toFixed(2) + ' percentile';
      $('cMPn').innerHTML = 'About state merit rank ' + nf(rankOf(p, LAST)) + ' on the ' + LAST + ' data. Use it as a rough guide: the real percentile depends on your session. <button class="mc-btn ghost" id="cUse" style="padding:5px 10px;margin-top:6px">Use this percentile</button>';
      $('cUse').onclick = function () { $('cP').value = p.toFixed(4); drawP(); };
    };
    var drawP = function () {
      var p = +$('cP').value;
      $('cPR').innerHTML = YEARS.slice().reverse().map(function (y) { return '<div class="mc-rate"><span>State merit rank, ' + y + '</span><b>' + nf(rankOf(p, y)) + '</b></div>'; }).join('') +
        '<p class="mc-sub" style="margin-top:8px">The rank is the Maharashtra State General Merit number printed beside each cut-off in the official lists.</p>';
    };
    $('cM').addEventListener('input', drawM); $('cP').addEventListener('input', drawP); drawM(); drawP();
    var pts = (D.curve[String(LAST)] || []).filter(function (r) { return r[0] >= 80; });
    mk('cCurve', { type: 'line', data: { labels: pts.map(function (r) { return r[0]; }), datasets: YEARS.map(function (y) {
      var c = {}; (D.curve[String(y)] || []).forEach(function (r) { c[r[0]] = r[1]; });
      return { label: String(y), data: pts.map(function (r) { return c[r[0]]; }), borderColor: YCOL[y], backgroundColor: YCOL[y], pointRadius: 0, borderWidth: 2, tension: .2 };
    }) }, options: { maintainAspectRatio: false, plugins: { legend: { position: 'bottom' } }, scales: { x: { reverse: true, title: { display: true, text: 'Percentile' }, ticks: { maxTicksLimit: 12 } }, y: { title: { display: true, text: 'State merit rank' } } } } });
    full().then(function (d) {
      var list = d.inst.slice().sort(function (a, b) { return a.short.localeCompare(b.short); });
      $('cI').innerHTML = list.map(function (i) { return '<option value="' + i.c + '">' + esc(i.short) + '</option>'; }).join('');
      var vj = list.filter(function (i) { return i.c === '03012'; })[0]; if (vj) $('cI').value = vj.c;
      var fillB = function () { var i = d.inst.filter(function (x) { return x.c === $('cI').value; })[0]; $('cB').innerHTML = i.br.map(function (b, k) { return '<option value="' + k + '">' + esc(b.n) + '</option>'; }).join(''); need(); };
      var need = function () {
        var i = d.inst.filter(function (x) { return x.c === $('cI').value; })[0], b = i.br[+$('cB').value];
        $('cNeed').innerHTML = YEARS.slice().reverse().map(function (y) { var c = openCut(b, y); return '<div class="mc-rate"><span>' + y + (c[1] ? ' · ' + c[1] : '') + '</span><b>' + (c[0] == null ? '–' : fmt(c[0], 4) + ' · rank ' + nf(rankOf(c[0], y))) + '</b></div>'; }).join('') +
          '<p class="mc-sub" style="margin-top:8px">Open category, CAP Round I. Reserved-category cut-offs are in Cut-off analytics.</p>';
      };
      $('cI').addEventListener('change', fillB); $('cB').addEventListener('change', need); fillB();
    });
  };

  /* ---------- analytics ---------- */
  var CAT_LABEL = { GOPEN: 'Open', GOBC: 'OBC', GSC: 'SC', GST: 'ST', GVJ: 'VJ/DT', GNT1: 'NT-B', GNT2: 'NT-C', GNT3: 'NT-D', GSEBC: 'SEBC', LOPEN: 'Ladies Open', LOBC: 'Ladies OBC', LSC: 'Ladies SC', LST: 'Ladies ST', EWS: 'EWS', TFWS: 'TFWS', MI: 'Minority' };
  BUILD.trend = function () {
    var top = D.top || [];
    var fams = FAM_ORDER;
    $('heat').innerHTML = '<thead><tr><th>College</th>' + fams.map(function (f) { return '<th>' + esc((FN[f] || f).split(' ')[0].replace(',', '')) + '</th>'; }).join('') + '</tr></thead><tbody>' +
      top.map(function (t) {
        return '<tr><td class="nm" title="' + esc(t.n) + '">' + esc(t.n) + '</td>' + fams.map(function (f) {
          var v = null; t.rows.forEach(function (r) { if (r.f === f && r.cut[LAST] != null && (v == null || r.cut[LAST] > v)) v = r.cut[LAST]; });
          return '<td style="background:' + heat(v) + ';color:' + (v != null && v > 93 ? '#fff' : '#3A4259') + '">' + (v == null ? '' : v.toFixed(2)) + '</td>';
        }).join('') + '</tr>';
      }).join('') + '</tbody>';
    $('tR').innerHTML += (D.regions || []).map(function (r) { return '<option>' + esc(r) + '</option>'; }).join('');
    $('tF').innerHTML += FAM_ORDER.concat(['OTHER']).map(function (f) { return '<option value="' + f + '">' + esc(FN[f] || f) + '</option>'; }).join('');
    $('tCat').innerHTML = Object.keys(CAT_LABEL).map(function (c) { return '<option value="' + c + '">' + esc(CAT_LABEL[c]) + '</option>'; }).join('');
    full().then(function (d) {
      var rows = [];
      d.inst.forEach(function (i) { i.br.forEach(function (b) { rows.push({ i: i, b: b }); }); });
      var draw = function () {
        var q = $('tQ').value.trim().toLowerCase(), r = $('tR').value, f = $('tF').value, cat = $('tCat').value, s = $('tS').value;
        var out = rows.filter(function (x) { return (!q || (x.i.n + ' ' + x.i.city).toLowerCase().indexOf(q) >= 0) && (!r || x.i.region === r) && (!f || x.b.f === f); }).map(function (x) {
          var cs = YEARS.map(function (y) { return cat === 'GOPEN' ? openCut(x.b, y) : catCut(x.b, y, cat); });
          var a = cs[0][0], z = cs[cs.length - 1][0];
          return { x: x, cs: cs, ch: (a != null && z != null) ? z - a : null, last: z };
        }).filter(function (o) { return o.cs.some(function (c) { return c[0] != null; }); });
        out.sort(function (a, b) {
          if (s === 'name') return a.x.i.short.localeCompare(b.x.i.short);
          if (s === 'rise') return (b.ch == null ? -999 : b.ch) - (a.ch == null ? -999 : a.ch);
          if (s === 'fall') return (a.ch == null ? 999 : a.ch) - (b.ch == null ? 999 : b.ch);
          return (b.last == null ? -1 : b.last) - (a.last == null ? -1 : a.last);
        });
        $('tCount').textContent = out.length + ' courses';
        $('tTbl').querySelector('tbody').innerHTML = out.slice(0, 150).map(function (o) {
          var seat = (o.cs[o.cs.length - 1][1] || o.cs[1][1] || o.cs[0][1] || '');
          return '<tr><td><b>' + esc(o.x.i.short) + '</b>' + web(o.x.i.c) + '<div class="mc-ct">' + esc(o.x.i.city || o.x.i.region) + '</div></td><td>' + esc(o.x.b.n) + '</td><td class="mc-ct">' + esc(seat) + '</td>' +
            o.cs.map(function (c) { return '<td class="n">' + fmt(c[0], 2) + '</td>'; }).join('') + '<td class="n" style="color:' + (o.ch == null ? GREY : o.ch >= 0 ? GR : RED) + '">' + (o.ch == null ? '–' : (o.ch >= 0 ? '+' : '') + o.ch.toFixed(2)) + '</td></tr>';
        }).join('') || '<tr><td colspan="7">No courses match.</td></tr>';
      };
      ['tR', 'tF', 'tCat', 'tS'].forEach(function (id) { $(id).addEventListener('change', draw); });
      $('tQ').addEventListener('input', draw); draw();
      var list = d.inst.slice().sort(function (a, b) { return a.short.localeCompare(b.short); });
      $('gI').innerHTML = list.map(function (i) { return '<option value="' + i.c + '">' + esc(i.short) + '</option>'; }).join('');
      $('gI').value = '16006';
      var fillB = function () { var i = d.inst.filter(function (x) { return x.c === $('gI').value; })[0]; $('gB').innerHTML = i.br.map(function (b, k) { return '<option value="' + k + '">' + esc(b.n) + '</option>'; }).join(''); plot(); };
      var plot = function () {
        var i = d.inst.filter(function (x) { return x.c === $('gI').value; })[0], b = i.br[+$('gB').value];
        var series = [['GOPEN', 'Open', NAVY], ['GOBC', 'OBC', OR], ['GSC', 'SC', GR], ['GST', 'ST', RED], ['EWS', 'EWS', '#7A4FD6'], ['TFWS', 'TFWS', '#0A8FA8']];
        mk('cTrend', { type: 'line', data: { labels: YEARS.map(String), datasets: series.map(function (s) { return { label: s[1], data: YEARS.map(function (y) { return (s[0] === 'GOPEN' ? openCut(b, y) : catCut(b, y, s[0]))[0]; }), borderColor: s[2], backgroundColor: s[2], spanGaps: true, tension: .2 }; }) },
          options: { maintainAspectRatio: false, plugins: { legend: { position: 'bottom' } }, scales: { y: { title: { display: true, text: 'Closing percentile (Round I)' } } } } });
      };
      $('gI').addEventListener('change', fillB); $('gB').addEventListener('change', plot); fillB();
    });
  };

  /* ---------- predictor ---------- */
  var P = store.get('mhtcet_pred') || {};
  BUILD.predict = function () {
    $('pU').innerHTML = '<option value="">Not from a Maharashtra home university / not sure</option>' + (D.unis || []).map(function (u) { return '<option>' + esc(u) + '</option>'; }).join('');
    $('pR').innerHTML += (D.regions || []).map(function (r) { return '<option>' + esc(r) + '</option>'; }).join('');
    $('pF').innerHTML += FAM_ORDER.concat(['OTHER']).map(function (f) { return '<option value="' + f + '">' + esc(FN[f] || f) + '</option>'; }).join('');
    $('pY').innerHTML = YEARS.slice().reverse().map(function (y) { return '<option value="' + y + '">' + y + ' Round I cut-offs</option>'; }).join('');
    ['pP', 'pC', 'pG', 'pU', 'pR', 'pF', 'pY'].forEach(function (id) { if (P[id] != null) $(id).value = P[id]; });
    if (P.pT) $('pT').checked = true;
    seg('pShow', function () { render(); });
    if (P.done) run();
  };
  var RES = [];
  function run() {
    ['pP', 'pC', 'pG', 'pU', 'pR', 'pF', 'pY'].forEach(function (id) { P[id] = $(id).value; });
    P.pT = $('pT').checked; P.done = true; store.set('mhtcet_pred', P);
    $('pSum').textContent = 'Loading the official lists…'; $('pOut').hidden = false;
    full().then(function (d) {
      var p = +P.pP, cat = P.pC, fem = P.pG === 'f', hu = P.pU, y = +P.pY;
      var cats = ['GOPEN'];
      if (fem) cats.push('LOPEN');
      if (cat !== 'OPEN' && cat !== 'EWS') { cats.push('G' + cat); if (fem) cats.push('L' + cat); }
      if (cat === 'EWS') cats.push('EWS');
      if (P.pT) cats.push('TFWS');
      var ur = rankOf(p, y);
      RES = [];
      d.inst.forEach(function (i) {
        if (P.pR && i.region !== P.pR) return;
        var lvls = ['S'];
        if (hu && i.hu === hu) lvls.push('H');
        else if (i.hu && i.hu !== 'Autonomous Institute' && i.hu !== 'Deemed to be University') lvls.push('O');
        i.br.forEach(function (b) {
          if (P.pF && b.f !== P.pF) return;
          var best = null;
          lvls.forEach(function (lv) { cats.forEach(function (c) { var v = val(b, y, lv, c); if (v != null && (!best || v < best.v)) best = { v: v, c: c, lv: lv }; }); });
          if (!best) return;
          var cr = rankOf(best.v, y), chance = null;
          if (ur <= cr * 0.8) chance = 'Safe'; else if (ur <= cr) chance = 'Likely'; else if (ur <= cr * 1.3) chance = 'Reach';
          if (!chance) return;
          var prev = null;
          if (YEARS.indexOf(y - 1) >= 0) lvls.forEach(function (lv) { cats.forEach(function (c) { var v = val(b, y - 1, lv, c); if (v != null && (prev == null || v < prev)) prev = v; }); });
          RES.push({ i: i, b: b, v: best.v, c: best.c, lv: best.lv, prev: prev, chance: chance });
        });
      });
      RES.sort(function (a, b) { return b.v - a.v; });
      var n = { Safe: 0, Likely: 0, Reach: 0 }; RES.forEach(function (r) { n[r.chance]++; });
      $('nS').textContent = n.Safe; $('nL').textContent = n.Likely; $('nR').textContent = n.Reach;
      $('pSum').textContent = 'Percentile ' + p + ' is about state merit rank ' + nf(ur) + ' on the ' + y + ' data. Categories used: ' + cats.map(function (c) { return CAT_LABEL[c] || c; }).join(', ') +
        (hu ? '; home university: ' + hu : '; no home-university seats') + '. Sorted from the most sought-after course down.';
      render();
    });
  }
  function render() {
    var show = segVal('pShow') || 'all';
    var rows = RES.filter(function (r) { return show === 'all' || r.chance === show; });
    $('pCount').textContent = rows.length + ' courses' + (rows.length > 250 ? ' (first 250 shown)' : '');
    var LV = { S: 'State', H: 'Home Univ', O: 'Other than HU' };
    $('pTbl').querySelector('tbody').innerHTML = rows.slice(0, 250).map(function (r) {
      return '<tr><td><span class="mc-chance ' + r.chance + '">' + r.chance + '</span></td><td><b>' + esc(r.i.short) + '</b>' + web(r.i.c) + '<div class="mc-ct">' + esc(r.i.city) + '</div></td><td>' + esc(r.b.n) + '</td><td class="mc-ct">' + esc(CAT_LABEL[r.c] || r.c) + ' · ' + LV[r.lv] + '</td><td class="n">' + fmt(r.v, 2) + '</td><td class="n">' + fmt(r.prev, 2) + '</td><td class="mc-ct">' + esc(r.i.region) + '</td></tr>';
    }).join('') || '<tr><td colspan="7">No courses within reach with these filters. Try All branches or All of Maharashtra.</td></tr>';
  }
  $('pGo').addEventListener('click', run);

  // previous / next buttons at the foot of every tab, in tab order
  var ORDER = [].map.call(document.querySelectorAll('#tabs button'), function (b) { return [b.dataset.tab, b.textContent.trim()]; });
  ORDER.forEach(function (t, k) {
    var p = $('p-' + t[0]); if (!p) return;
    var nav = document.createElement('div'); nav.className = 'mc-pn';
    nav.innerHTML = (k > 0 ? '<button data-goto-tab="' + ORDER[k - 1][0] + '" class="prev">← ' + esc(ORDER[k - 1][1]) + '</button>' : '<span></span>') +
      (k < ORDER.length - 1 ? '<button data-goto-tab="' + ORDER[k + 1][0] + '" class="next">' + esc(ORDER[k + 1][1]) + ' →</button>' : '');
    p.appendChild(nav);
  });
  var _show = show;
  show = function (tab) { _show(tab); var b = document.querySelector('#tabs button[data-tab="' + tab + '"]'); if (b && b.scrollIntoView) b.scrollIntoView({ block: 'nearest', inline: 'center' }); };

  var start = (location.hash || '').slice(1);
  show(BUILD[start] ? start : 'overview');
})();
