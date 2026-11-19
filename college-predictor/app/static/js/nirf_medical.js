(function () {
  'use strict';
  var RAW = window.EA_NIRF_MED || [];
  var D = RAW.map(function (r) { return { rank: r[0], id: r[1], name: r[2], city: r[3], state: r[4], score: r[5], p: [r[6], r[7], r[8], r[9], r[10]] }; });
  var PK = ['tlr', 'rpc', 'go', 'oi', 'per'];
  var PN = ['Teaching & Learning', 'Research', 'Graduation Outcomes', 'Outreach & Inclusivity', 'Perception'];
  var PS = ['TLR', 'RPC', 'GO', 'OI', 'PER'];
  var NAVY = '#0E3A8A', OR = '#FF6B0A', GR = '#1F8B5C', HL = '#E8DFC8';
  var COLS = [NAVY, OR, GR, '#7A4FD6', '#C23A3A', '#0A8FA8', '#B8860B', '#556', '#2E7D32', '#AD1457'];
  var $ = function (id) { return document.getElementById(id); };
  var esc = function (s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); };
  var avg = function (a) { return a.reduce(function (x, y) { return x + y; }, 0) / (a.length || 1); };
  var short = function (n) { return n.replace(/All India Institute of Medical Sciences/, 'AIIMS').replace(/ Institute of Medical Sciences?/, ' IMS').replace(/Post Graduate Institute of Medical Education and Research/, 'PGIMER').replace(/, .*$/, '').slice(0, 34); };
  var charts = {}, built = {};
  if (window.Chart) { Chart.defaults.font.family = "'Plus Jakarta Sans',sans-serif"; Chart.defaults.font.size = 11; }
  function mk(id, cfg) { if (!window.Chart) return; if (charts[id]) charts[id].destroy(); charts[id] = new Chart($(id), cfg); }

  var states = {};
  D.forEach(function (d) { (states[d.state] = states[d.state] || []).push(d); });
  var stNames = Object.keys(states).sort(function (a, b) { return states[b].length - states[a].length || a.localeCompare(b); });

  // KPIs + insights
  var top10 = D.slice(0, 10), pAvg = PK.map(function (_, i) { return avg(D.map(function (d) { return d.p[i]; })); });
  $('kpis').innerHTML = [
    [D.length, 'Institutes ranked'], [D[0].score.toFixed(1), 'Top score (' + short(D[0].name) + ')'],
    [stNames.length, 'States and UTs'], [D[D.length - 1].score.toFixed(1), 'Score at rank 50']
  ].map(function (k) { return '<div class="nm-kpi"><b>' + k[0] + '</b><span>' + esc(k[1]) + '</span></div>'; }).join('');
  var lowest = pAvg.indexOf(Math.min.apply(null, pAvg)), aiims = D.filter(function (d) { return /^All India Institute/.test(d.name); });
  var tn = states['Tamil Nadu'] || [];
  $('insights').innerHTML = [
    'AIIMS Delhi leads with ' + D[0].score.toFixed(2) + ', <strong>' + (D[0].score - D[1].score).toFixed(1) + ' points</strong> clear of PGIMER Chandigarh at rank 2. The next nine institutes sit within ' + (D[1].score - D[9].score).toFixed(1) + ' points of each other.',
    PN[lowest] + ' is the weakest parameter across the list (average ' + pAvg[lowest].toFixed(1) + ' out of 100) against ' + pAvg[2].toFixed(1) + ' for Graduation Outcomes.',
    stNames[0] + ' has the most ranked institutes (' + states[stNames[0]].length + '), then ' + stNames[1] + ' (' + states[stNames[1]].length + ') and ' + stNames[2] + ' (' + states[stNames[2]].length + ').',
    aiims.length + ' AIIMS campuses are in the top 50. Tamil Nadu has ' + tn.length + ' institutes, ' + tn.filter(function (d) { return d.rank <= 10; }).length + ' of them in the top 10.',
    'Government institutes lead on Graduation Outcomes and Teaching; private and deemed universities score higher on Outreach and often on Research. Check fees on the seat pages before you rely on rank alone.'
  ].map(function (t) { return '<li>' + t + '</li>'; }).join('');

  // ---------- tabs ----------
  var builders = {
    overview: function () {
      mk('cScores', { type: 'bar', data: { labels: D.map(function (d) { return d.rank; }), datasets: [{ data: D.map(function (d) { return d.score; }), backgroundColor: D.map(function (d) { return d.rank <= 10 ? NAVY : '#8FA8D6'; }), borderRadius: 3 }] },
        options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false }, tooltip: { callbacks: { title: function (i) { return D[i[0].dataIndex].name; }, label: function (c) { return 'Rank ' + D[c.dataIndex].rank + ' · score ' + c.raw.toFixed(2); } } } }, scales: { x: { grid: { display: false }, ticks: { maxTicksLimit: 10 } }, y: { min: 40, grid: { color: HL } } } } });
      mk('cStateCount', { type: 'bar', data: { labels: stNames, datasets: [{ data: stNames.map(function (s) { return states[s].length; }), backgroundColor: OR, borderRadius: 3 }] },
        options: { indexAxis: 'y', responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { x: { grid: { color: HL }, ticks: { stepSize: 1 } }, y: { grid: { display: false }, ticks: { font: { size: 10 } } } } } });
    },
    rankings: function () {
      var fs = $('fState'); stNames.slice().sort().forEach(function (s) { fs.insertAdjacentHTML('beforeend', '<option>' + esc(s) + '</option>'); });
      ['q', 'fState', 'fSort'].forEach(function (id) { $(id).addEventListener('input', renderTable); });
      renderTable();
    },
    top10: function () {
      $('podium').innerHTML = D.slice(0, 3).map(function (d) {
        return '<div class="nm-pod"><div class="r">RANK ' + d.rank + '</div><h3>' + esc(d.name) + '</h3><div class="nm-ct">' + esc(d.city) + ', ' + esc(d.state) + '</div><div class="s">' + d.score.toFixed(2) + '</div>' +
          d.p.map(function (v, i) { return '<div class="nm-mini"><span>' + PS[i] + '</span><i><b style="width:' + v + '%"></b></i><span>' + Math.round(v) + '</span></div>'; }).join('') + '</div>';
      }).join('');
      mk('cTop10', { type: 'bar', data: { labels: PS, datasets: top10.map(function (d, i) { return { label: d.rank + '. ' + short(d.name), data: d.p, backgroundColor: COLS[i], borderRadius: 2 }; }) },
        options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'bottom', labels: { boxWidth: 10, font: { size: 10 } } } }, scales: { x: { grid: { display: false } }, y: { max: 100, grid: { color: HL } } } } });
    },
    states: function () {
      var avgs = stNames.map(function (s) { return avg(states[s].map(function (d) { return d.score; })); });
      var ord = stNames.map(function (_, i) { return i; }).sort(function (a, b) { return avgs[b] - avgs[a]; });
      mk('cStateAvg', { type: 'bar', data: { labels: ord.map(function (i) { return stNames[i]; }), datasets: [{ data: ord.map(function (i) { return +avgs[i].toFixed(2); }), backgroundColor: NAVY, borderRadius: 3 }] },
        options: { indexAxis: 'y', responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { x: { min: 40, grid: { color: HL } }, y: { grid: { display: false }, ticks: { font: { size: 10 } } } } } });
      var sel = $('stSel'); sel.innerHTML = stNames.slice().sort().map(function (s) { return '<option>' + esc(s) + '</option>'; }).join('');
      function show() { $('stList').innerHTML = states[sel.value].map(function (d) { return '<div><span><b>#' + d.rank + '</b> ' + esc(d.name) + ' <span class="nm-ct">' + esc(d.city) + '</span></span><b>' + d.score.toFixed(1) + '</b></div>'; }).join(''); }
      sel.addEventListener('change', show); show();
    },
    params: function () {
      var t10 = PK.map(function (_, i) { return avg(top10.map(function (d) { return d.p[i]; })); });
      mk('cParamAvg', { type: 'bar', data: { labels: PS, datasets: [{ label: 'Top 10 average', data: t10.map(function (v) { return +v.toFixed(1); }), backgroundColor: NAVY, borderRadius: 3 }, { label: 'Top 50 average', data: pAvg.map(function (v) { return +v.toFixed(1); }), backgroundColor: OR, borderRadius: 3 }] },
        options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'bottom', labels: { boxWidth: 10 } } }, scales: { x: { grid: { display: false } }, y: { max: 100, grid: { color: HL } } } } });
      $('leaders').innerHTML = PK.map(function (_, i) {
        var b = D.slice().sort(function (a, c) { return c.p[i] - a.p[i]; })[0];
        return '<div class="nm-lead1"><div><em>' + PN[i] + '</em><br><b>' + esc(b.name) + '</b></div><b>' + b.p[i].toFixed(1) + '</b></div>';
      }).join('');
      mk('cScatter', { type: 'scatter', data: { datasets: [{ label: 'Institutes', data: D.map(function (d) { return { x: d.p[1], y: d.p[2], n: d.name, r: d.rank }; }), backgroundColor: D.map(function (d) { return d.rank <= 10 ? OR : 'rgba(14,58,138,.6)'; }), pointRadius: 6 }] },
        options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false }, tooltip: { callbacks: { label: function (c) { return '#' + c.raw.r + ' ' + c.raw.n + ' · RPC ' + c.raw.x + ' · GO ' + c.raw.y; } } } }, scales: { x: { title: { display: true, text: 'Research & Professional Practice' }, grid: { color: HL }, min: 0, max: 100 }, y: { title: { display: true, text: 'Graduation Outcomes' }, grid: { color: HL }, min: 40, max: 100 } } } });
    },
    compare: function () {
      var opts = D.map(function (d, i) { return '<option value="' + i + '">#' + d.rank + ' ' + esc(d.name) + '</option>'; }).join('');
      ['c1', 'c2', 'c3'].forEach(function (id, k) { var s = $(id); s.innerHTML = (k === 2 ? '<option value="">(none)</option>' : '') + opts; s.value = k === 2 ? '' : String(k * 2); s.addEventListener('change', drawCmp); });
      drawCmp();
    }
  };
  function drawCmp() {
    var sel = ['c1', 'c2', 'c3'].map(function (id) { return $(id).value; }).filter(function (v) { return v !== ''; }).map(function (v) { return D[+v]; });
    mk('cCompare', { type: 'radar', data: { labels: PN, datasets: sel.map(function (d, i) { return { label: short(d.name), data: d.p, borderColor: COLS[i], backgroundColor: COLS[i] + '26', borderWidth: 2, pointBackgroundColor: COLS[i] }; }) },
      options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'bottom' } }, scales: { r: { min: 0, max: 100, ticks: { display: false }, grid: { color: HL }, angleLines: { color: HL }, pointLabels: { font: { size: 11 } } } } } });
    $('cmpTbl').innerHTML = '<thead><tr><th>Measure</th>' + sel.map(function (d) { return '<th class="n">' + esc(short(d.name)) + '</th>'; }).join('') + '</tr></thead><tbody>' +
      '<tr><td>NIRF rank</td>' + sel.map(function (d) { return '<td class="n">' + d.rank + '</td>'; }).join('') + '</tr>' +
      '<tr><td>Overall score</td>' + sel.map(function (d) { return '<td class="n">' + d.score.toFixed(2) + '</td>'; }).join('') + '</tr>' +
      PN.map(function (n, i) { var mx = Math.max.apply(null, sel.map(function (d) { return d.p[i]; })); return '<tr><td>' + n + '</td>' + sel.map(function (d) { return '<td class="n"' + (d.p[i] === mx && sel.length > 1 ? ' style="font-weight:700;color:#1F8B5C"' : '') + '>' + d.p[i].toFixed(1) + '</td>'; }).join('') + '</tr>'; }).join('') + '</tbody>';
  }
  function renderTable() {
    var q = $('q').value.trim().toLowerCase(), st = $('fState').value, so = $('fSort').value;
    var rows = D.filter(function (d) { return (!st || d.state === st) && (!q || (d.name + ' ' + d.city).toLowerCase().indexOf(q) > -1); });
    if (so !== 'rank') { var i = PK.indexOf(so); rows = rows.slice().sort(function (a, b) { return b.p[i] - a.p[i]; }); }
    $('count').textContent = rows.length + ' of ' + D.length;
    $('tbl').querySelector('tbody').innerHTML = rows.map(function (d) {
      return '<tr data-r="' + d.rank + '"><td><span class="nm-rk' + (d.rank <= 3 ? ' t3' : '') + '">' + d.rank + '</span></td><td><div class="nm-nm">' + esc(d.name) + '</div><div class="nm-ct">' + esc(d.city) + '</div></td><td>' + esc(d.state) + '</td><td class="n"><b>' + d.score.toFixed(2) + '</b><span class="nm-bar2" style="width:' + Math.round(d.score / 2) + 'px"></span></td>' +
        d.p.map(function (v) { return '<td class="n">' + v.toFixed(1) + '</td>'; }).join('') + '</tr>';
    }).join('') || '<tr><td colspan="9" style="text-align:center;padding:24px;color:#5A6278">No institute matches.</td></tr>';
  }
  $('tbl').addEventListener('click', function (e) {
    var tr = e.target.closest('tr[data-r]'); if (!tr) return;
    show('compare'); var i = +tr.dataset.r - 1; $('c1').value = String(i); drawCmp();
  });

  function show(name) {
    document.querySelectorAll('#tabs button').forEach(function (b) { b.setAttribute('aria-selected', b.dataset.tab === name ? 'true' : 'false'); });
    document.querySelectorAll('.nm-panel').forEach(function (p) { p.hidden = p.id !== 'p-' + name; });
    if (!built[name]) { built[name] = true; builders[name](); } else { Object.keys(charts).forEach(function (k) { charts[k].resize(); }); }
    try { history.replaceState(null, '', '#' + name); } catch (e) { }
  }
  $('tabs').addEventListener('click', function (e) { var b = e.target.closest('button[data-tab]'); if (b) show(b.dataset.tab); });
  var h = (location.hash || '').slice(1);
  show(builders[h] ? h : 'overview');
})();
