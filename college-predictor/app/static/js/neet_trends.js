(function () {
  'use strict';
  var D = window.EA_NT; if (!D) return;
  var Y = D.years.map(String);
  var NAVY = '#0E3A8A', OR = '#FF6B0A', GR = '#1F8B5C', PU = '#7A4FD6', HL = '#E8DFC8', YC = { '2023': '#8FA8D6', '2024': NAVY, '2025': OR };
  var $ = function (id) { return document.getElementById(id); };
  var esc = function (s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); };
  var fmt = function (n) { return n == null ? '–' : Number(n).toLocaleString('en-IN'); };
  var lakh = function (n) { return (n / 100000).toFixed(2); };
  var pct = function (a, b) { return (b - a) * 100 / a; };
  var sgn = function (v) { return (v >= 0 ? '+' : '') + v.toFixed(1) + '%'; };
  var charts = {}, built = {};
  if (window.Chart) { Chart.defaults.font.family = "'Plus Jakarta Sans',sans-serif"; Chart.defaults.font.size = 11; }
  function mk(id, cfg) { if (!window.Chart || !$(id)) return; if (charts[id]) charts[id].destroy(); cfg.options = cfg.options || {}; cfg.options.responsive = true; cfg.options.maintainAspectRatio = false; charts[id] = new Chart($(id), cfg); }
  var legend = { position: 'bottom', labels: { boxWidth: 10, font: { size: 10 } } };
  var grid = { grid: { color: HL } }, nogrid = { grid: { display: false } };
  var H = D.headline, ST = D.seatTotal;
  var yrs = function (f) { return Y.map(f); };
  var ratio = function (y) { return H[y].qualified / ST[y].seats; };

  // KPIs
  function kpi(label, vals, f, inv) {
    var ch = pct(vals[0], vals[2]), good = inv ? ch < 0 : ch > 0;
    return '<div class="nt-kpi"><span>' + label + '</span><b>' + f(vals[2]) + '</b><em class="' + (good ? 'up' : 'dn') + '">' + sgn(ch) + ' vs 2023</em></div>';
  }
  $('kpis').innerHTML = [
    kpi('Qualified 2025', yrs(function (y) { return H[y].qualified; }), function (v) { return lakh(v) + ' L'; }),
    kpi('General cut-off 2025', yrs(function (y) { return D.cutoff['UR / EWS'].years[y].cutoff; }), function (v) { return v + '/720'; }, true),
    kpi('MBBS seats 2025-26', yrs(function (y) { return ST[y].seats; }), fmt),
    kpi('Medical colleges', yrs(function (y) { return ST[y].colleges; }), fmt),
    kpi('Last govt general AIR', yrs(function (y) { return D.lastGovtGeneral[y]; }), fmt)
  ].join('');

  // insights
  (function () {
    var q = yrs(function (y) { return H[y].qualified; }), s = yrs(function (y) { return ST[y].seats; }), r = Y.map(ratio);
    var cut = yrs(function (y) { return D.cutoff['UR / EWS'].years[y].cutoff; }), lg = yrs(function (y) { return D.lastGovtGeneral[y]; });
    var fem = yrs(function (y) { return D.gender[y].Female.qualified * 100 / H[y].qualified; });
    var pv = yrs(function (y) { return ST[y].pvt_seats * 100 / (ST[y].pvt_seats + ST[y].govt_seats); });
    var li = [
      'Registrations peaked at <strong>' + lakh(H['2024'].registered) + ' lakh in 2024</strong> and fell to ' + lakh(H['2025'].registered) + ' lakh in 2025. Qualifiers went ' + lakh(q[0]) + ', ' + lakh(q[1]) + ', ' + lakh(q[2]) + ' lakh.',
      'MBBS seats grew <strong>' + fmt(s[0]) + ' to ' + fmt(s[2]) + ' (' + sgn(pct(s[0], s[2])) + ')</strong>, so qualified candidates per seat eased from ' + r[0].toFixed(1) + ' to ' + r[2].toFixed(1) + ' (' + r[1].toFixed(1) + ' in 2024).',
      'The general qualifying score was ' + cut[0] + ' in 2023, ' + cut[1] + ' in 2024 and ' + cut[2] + ' in 2025. The 2025 paper was harder: the top score fell from 720 to ' + D.exam['2025'].top + '.',
      'The last general-category rank to get a government MBBS seat through MCC moved from <strong>' + fmt(lg[0]) + ' to ' + fmt(lg[1]) + ' to ' + fmt(lg[2]) + '</strong>: more seats pushed the line further down the list each year.',
      'Private seats are now ' + pv[2].toFixed(1) + '% of all MBBS seats, up from ' + pv[0].toFixed(1) + '% in 2023-24. Women are ' + fem[2].toFixed(1) + '% of qualifiers.',
      'The biggest seat gains 2023-24 to 2025-26 were in ' + gainers().slice(0, 3).map(function (g) { return esc(g.n) + ' (+' + fmt(g.gain) + ')'; }).join(', ') + '.'
    ];
    $('insights').innerHTML = li.map(function (t) { return '<li>' + t + '</li>'; }).join('');
  })();
  function gainers() {
    return Object.keys(D.stateSeats).map(function (n) { var s = D.stateSeats[n]; return { n: n, s23: s.s23, s25: s.s25, gain: s.s25 - s.s23, pct: pct(s.s23, s.s25), c23: s.c23, c25: s.c25 }; }).sort(function (a, b) { return b.gain - a.gain; });
  }
  function yrBtns(id, cb, init) {
    var el = $(id); el.innerHTML = Y.map(function (y) { return '<button type="button" data-y="' + y + '" aria-pressed="' + (y === init) + '">' + y + '</button>'; }).join('');
    el.addEventListener('click', function (e) { var b = e.target.closest('button'); if (!b) return; el.querySelectorAll('button').forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); }); cb(b.dataset.y); });
  }

  var B = {
    story: function () {
      mk('cFunnel', { type: 'bar', data: { labels: Y, datasets: [
        { label: 'Registered', data: yrs(function (y) { return H[y].registered / 1e5; }), backgroundColor: '#C9D5EE', borderRadius: 3 },
        { label: 'Appeared', data: yrs(function (y) { return H[y].appeared / 1e5; }), backgroundColor: '#8FA8D6', borderRadius: 3 },
        { label: 'Qualified', data: yrs(function (y) { return H[y].qualified / 1e5; }), backgroundColor: NAVY, borderRadius: 3 }] },
        options: { plugins: { legend: legend }, scales: { x: nogrid, y: { grid: grid.grid, title: { display: true, text: 'lakh' } } } } });
      mk('cRatio', { type: 'bar', data: { labels: Y, datasets: [{ data: Y.map(function (y) { return +ratio(y).toFixed(2); }), backgroundColor: Y.map(function (y) { return YC[y]; }), borderRadius: 4 }] },
        options: { plugins: { legend: { display: false }, tooltip: { callbacks: { label: function (c) { return c.raw + ' qualified candidates per MBBS seat'; } } } }, scales: { x: nogrid, y: { grid: grid.grid, beginAtZero: true } } } });
    },
    score: function () {
      var cl = ['UR / EWS', 'OBC', 'SC', 'ST'];
      mk('cCut', { type: 'bar', data: { labels: cl, datasets: Y.map(function (y) { return { label: y, data: cl.map(function (c) { return D.cutoff[c].years[y].cutoff; }), backgroundColor: YC[y], borderRadius: 3 }; }) },
        options: { plugins: { legend: legend }, scales: { x: nogrid, y: { grid: grid.grid, beginAtZero: true, max: 180 } } } });
      var cats = ['UR', 'EWS', 'OBC', 'SC', 'ST'];
      mk('cCat', { type: 'bar', data: { labels: cats, datasets: Y.map(function (y) { return { label: y, data: cats.map(function (c) { return Math.round(D.category[y][c].qualified / 1000); }), backgroundColor: YC[y], borderRadius: 3 }; }) },
        options: { plugins: { legend: legend }, scales: { x: nogrid, y: grid } } });
      mk('cGender', { type: 'bar', data: { labels: Y, datasets: [
        { label: 'Women', data: yrs(function (y) { return Math.round(D.gender[y].Female.qualified / 1000); }), backgroundColor: OR, borderRadius: 3 },
        { label: 'Men', data: yrs(function (y) { return Math.round(D.gender[y].Male.qualified / 1000); }), backgroundColor: NAVY, borderRadius: 3 }] },
        options: { plugins: { legend: legend }, scales: { x: nogrid, y: grid } } });
      function st(y) {
        var o = D.states[y], ks = Object.keys(o);
        mk('cState', { type: 'bar', data: { labels: ks, datasets: [{ label: 'Qualified', data: ks.map(function (k) { return o[k].qualified; }), backgroundColor: YC[y], borderRadius: 3 }] },
          options: { indexAxis: 'y', plugins: { legend: { display: false }, tooltip: { callbacks: { afterLabel: function (c) { var s = o[ks[c.dataIndex]]; return fmt(s.appeared) + ' appeared, ' + (s.qualified * 100 / s.appeared).toFixed(0) + '% qualified'; } } } }, scales: { x: grid, y: nogrid } } });
      }
      yrBtns('stYr', st, '2025'); st('2025');
      var ms = Object.keys(D.marksRank).sort(function (a, b) { return b - a; });
      $('tMarks').innerHTML = '<thead><tr><th>Score</th>' + Y.map(function (y) { return '<th class="n">AIR ' + y + '</th>'; }).join('') + '</tr></thead><tbody>' +
        ms.map(function (m) { return '<tr><td><b>' + m + '</b> / 720</td>' + Y.map(function (y) { var v = D.marksRank[m][y]; return '<td class="n">' + (v == null ? '–' : '~' + fmt(v)) + '</td>'; }).join('') + '</tr>'; }).join('') + '</tbody>';
    },
    seats: function () {
      var hy = Object.keys(D.seatHistory);
      mk('cSeatTrend', { type: 'bar', data: { labels: hy.map(function (y) { return y + '-' + String(+y + 1).slice(2); }), datasets: [{ data: hy.map(function (y) { return D.seatHistory[y]; }), backgroundColor: hy.map(function (y) { return +y >= 2023 ? NAVY : '#8FA8D6'; }), borderRadius: 3 }] },
        options: { plugins: { legend: { display: false } }, scales: { x: nogrid, y: { grid: grid.grid, min: 80000 } } } });
      mk('cGP', { type: 'bar', data: { labels: Y.map(function (y) { return y + '-' + String(+y + 1).slice(2); }), datasets: [
        { label: 'Government', data: yrs(function (y) { return ST[y].govt_seats; }), backgroundColor: NAVY, borderRadius: 3 },
        { label: 'Private', data: yrs(function (y) { return ST[y].pvt_seats; }), backgroundColor: OR, borderRadius: 3 }] },
        options: { plugins: { legend: legend }, scales: { x: { stacked: true, grid: nogrid.grid }, y: { stacked: true, grid: grid.grid } } } });
      var rows = gainers();
      function draw() {
        var q = $('stQ').value.trim().toLowerCase(), so = $('stSort').value;
        var r = rows.filter(function (x) { return !q || x.n.toLowerCase().indexOf(q) > -1; }).sort(function (a, b) { return b[so === 'gain' ? 'gain' : so === 'pct' ? 'pct' : 's25'] - a[so === 'gain' ? 'gain' : so === 'pct' ? 'pct' : 's25']; });
        var mx = Math.max.apply(null, rows.map(function (x) { return x.s25; }));
        $('tSeats').innerHTML = '<thead><tr><th>State / UT</th><th class="n">2023-24</th><th class="n">2025-26</th><th class="n">Added</th><th class="n">Growth</th><th class="n">Colleges 23→25</th></tr></thead><tbody>' +
          r.map(function (x) { return '<tr><td><b>' + esc(x.n) + '</b></td><td class="n">' + fmt(x.s23) + '</td><td class="n">' + fmt(x.s25) + '<span class="nt-bar2" style="width:' + Math.round(x.s25 * 60 / mx) + 'px"></span></td><td class="n ' + (x.gain >= 0 ? 'nt-pos' : 'nt-neg') + '">' + (x.gain >= 0 ? '+' : '') + fmt(x.gain) + '</td><td class="n">' + sgn(x.pct) + '</td><td class="n">' + x.c23 + ' → ' + x.c25 + '</td></tr>'; }).join('') + '</tbody>';
      }
      $('stQ').addEventListener('input', draw); $('stSort').addEventListener('input', draw); draw();
      var ks = Object.keys(D.stateSplit).sort(function (a, b) { var x = D.stateSplit[a], y = D.stateSplit[b]; return (y.g25 + y.p25) - (x.g25 + x.p25); });
      var shr = function (g, p) { return +(p * 100 / (g + p)).toFixed(1); };
      mk('cSplit', { type: 'bar', data: { labels: ks, datasets: [
        { label: 'Private share 2023-24 (%)', data: ks.map(function (k) { var s = D.stateSplit[k]; return shr(s.g23, s.p23); }), backgroundColor: '#8FA8D6', borderRadius: 3 },
        { label: 'Private share 2025-26 (%)', data: ks.map(function (k) { var s = D.stateSplit[k]; return shr(s.g25, s.p25); }), backgroundColor: OR, borderRadius: 3 }] },
        options: { indexAxis: 'y', plugins: { legend: legend }, scales: { x: { grid: grid.grid, max: 100 }, y: nogrid } } });
    },
    allot: function () {
      var R = D.rounds;
      mk('cRounds', { type: 'bar', data: { labels: R, datasets: Y.map(function (y) { return { label: y, data: D.allotted[y].map(function (r) { return r.allotted; }), backgroundColor: YC[y], borderRadius: 3 }; }) },
        options: { plugins: { legend: legend }, scales: { x: nogrid, y: grid } } });
      function q(y) {
        var m = D.quotaMix[y];
        mk('cQuota', { type: 'bar', data: { labels: ['Round 1', 'Round 2', 'Round 3'], datasets: [
          { label: 'AIQ 15% / open seat', data: m.map(function (r) { return r.aiq; }), backgroundColor: NAVY }, { label: 'Deemed / paid', data: m.map(function (r) { return r.deemed; }), backgroundColor: OR }, { label: 'NRI', data: m.map(function (r) { return r.nri; }), backgroundColor: GR }] },
          options: { plugins: { legend: legend }, scales: { x: { stacked: true, grid: nogrid.grid }, y: { stacked: true, grid: grid.grid } } } });
      }
      yrBtns('qYr', q, '2025'); q('2025');
      mk('cUp', { type: 'bar', data: { labels: ['Round 2', 'Round 3'], datasets: Y.map(function (y) { return { label: y, data: [D.allotted[y][1].upgraded, D.allotted[y][2].upgraded], backgroundColor: YC[y], borderRadius: 3 }; }) },
        options: { plugins: { legend: legend }, scales: { x: nogrid, y: grid } } });
      mk('cLast', { type: 'line', data: { labels: R, datasets: Y.map(function (y) { return { label: y, data: D.lastGovtByRound[y], borderColor: YC[y], backgroundColor: YC[y], tension: .25, pointRadius: 4 }; }) },
        options: { plugins: { legend: legend }, scales: { x: nogrid, y: { grid: grid.grid, min: 18000 } } } });
    },
    ranks: function () {
      var ks = Object.keys(D.closing).filter(function (k) { return !/deemed/.test(k); });
      mk('cClose', { type: 'bar', data: { labels: ks, datasets: Y.map(function (y) { return { label: y, data: ks.map(function (k) { return D.closing[k][y]; }), backgroundColor: YC[y], borderRadius: 2 }; }) },
        options: { indexAxis: 'y', plugins: { legend: legend }, scales: { x: { type: 'logarithmic', grid: grid.grid, title: { display: true, text: 'last AIR (log scale)' } }, y: nogrid } } });
      var all = Object.keys(D.closing);
      $('tClose').innerHTML = '<thead><tr><th>Institute</th>' + Y.map(function (y) { return '<th class="n">' + y + '</th>'; }).join('') + '<th class="n">2023→2025</th></tr></thead><tbody>' +
        all.map(function (k) { var c = D.closing[k], d = c['2025'] - c['2023']; return '<tr><td><b>' + esc(k) + '</b></td>' + Y.map(function (y) { return '<td class="n">' + fmt(c[y]) + '</td>'; }).join('') + '<td class="n ' + (d >= 0 ? 'nt-pos' : 'nt-neg') + '">' + (d >= 0 ? '+' : '') + fmt(d) + '</td></tr>'; }).join('') + '</tbody>';
    },
    data: function () {
      $('notes').innerHTML = D.notes.map(function (n) { return '<li>' + esc(n) + '</li>'; }).join('');
      $('sources').innerHTML = D.sources.map(function (s) { return '<li><a href="' + esc(s[1]) + '" target="_blank" rel="noopener">' + esc(s[0]) + '</a></li>'; }).join('') +
        '<li><a href="https://mcc.nic.in/archive-ug/" target="_blank" rel="noopener">MCC UG counselling archive: result and vacancy files, counted by EduAakashaA</a></li>';
    }
  };

  function show(name) {
    document.querySelectorAll('#tabs button').forEach(function (b) { b.setAttribute('aria-selected', b.dataset.tab === name ? 'true' : 'false'); });
    document.querySelectorAll('.nt-panel').forEach(function (p) { p.hidden = p.id !== 'p-' + name; });
    if (!built[name]) { built[name] = true; B[name](); } else { Object.keys(charts).forEach(function (k) { charts[k].resize(); }); }
    try { history.replaceState(null, '', '#' + name); } catch (e) { }
  }
  $('tabs').addEventListener('click', function (e) { var b = e.target.closest('button[data-tab]'); if (b) show(b.dataset.tab); });
  var h = (location.hash || '').slice(1);
  show(B[h] ? h : 'story');
})();
