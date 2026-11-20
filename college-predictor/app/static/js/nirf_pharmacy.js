(function () {
  'use strict';
  var RAW = window.EA_NIRF_PHARM || [];
  var D = RAW.map(function (r, i) { return { i: i, rank: r[0], id: r[1], name: r[2], city: r[3], state: r[4], score: r[5], p: [r[6], r[7], r[8], r[9], r[10]] }; });
  var PK = ['tlr', 'rpc', 'go', 'oi', 'per'];
  var PN = ['Teaching & Learning', 'Research', 'Graduation Outcomes', 'Outreach & Inclusivity', 'Perception'];
  var PS = ['TLR', 'RPC', 'GO', 'OI', 'PER'];
  var NAVY = '#0E3A8A', OR = '#FF6B0A', GR = '#1F8B5C', HL = '#E8DFC8', LB = '#8FA8D6';
  var COLS = [NAVY, OR, GR, '#7A4FD6', '#C23A3A', '#0A8FA8', '#B8860B', '#556', '#2E7D32', '#AD1457'];
  var $ = function (id) { return document.getElementById(id); };
  var esc = function (s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); };
  var avg = function (a) { return a.reduce(function (x, y) { return x + y; }, 0) / (a.length || 1); };
  var isNiper = function (d) { return /^National Institute of Pharmaceutical Education and Research/i.test(d.name); };
  var short = function (n) {
    return n.replace(/^National Institute of Pharmaceutical Education and Research,?\s*/i, 'NIPER ').replace(/^Birla Institute of Technology & Science -Pilani/, 'BITS Pilani')
      .replace(/Institute of Science and Technology/, 'IST').replace(/ Institute of Chemical Technology/, 'ICT').replace(/^SVKM`s Narsee Monjee Institute of Management Studies/, 'NMIMS Mumbai').replace(/^SVKM`s /, '').replace(/^S\.R\.M\. IST/, 'SRM IST').replace(/College of Pharmacy/, 'CoP').slice(0, 34);
  };
  var charts = {}, built = {};
  if (window.Chart) { Chart.defaults.font.family = "'Plus Jakarta Sans',sans-serif"; Chart.defaults.font.size = 11; }
  function mk(id, cfg) { if (!window.Chart) return; if (charts[id]) charts[id].destroy(); charts[id] = new Chart($(id), cfg); }

  var states = {};
  D.forEach(function (d) { (states[d.state] = states[d.state] || []).push(d); });
  var stNames = Object.keys(states).sort(function (a, b) { return states[b].length - states[a].length || a.localeCompare(b); });
  var top10 = D.slice(0, 10), pAvg = PK.map(function (_, i) { return avg(D.map(function (d) { return d.p[i]; })); });
  var nipers = D.filter(isNiper);

  // ---------- KPI strip + insights ----------
  $('kpis').innerHTML = [
    [D.length, 'Institutes ranked'], [D[0].score.toFixed(1), 'Top score (' + short(D[0].name) + ')'],
    [stNames.length, 'States and UTs'], [nipers.length + ' of 7', 'NIPERs in top 30'], [D[D.length - 1].score.toFixed(1), 'Score at rank 100']
  ].map(function (k) { return '<div class="np-kpi"><b>' + k[0] + '</b><span>' + esc(k[1]) + '</span></div>'; }).join('');

  var lowest = PK.map(function (_, i) { return i; }).sort(function (a, b) { return pAvg[a] - pAvg[b]; })[0];
  var best = PK.map(function (_, i) { return i; }).sort(function (a, b) { return pAvg[b] - pAvg[a]; })[0];
  var pun = states['Punjab'] || [], tn = states['Tamil Nadu'] || [];
  var gap = function (k) { return avg(D.slice(0, 10).map(function (d) { return d.p[k]; })) - avg(D.slice(10).map(function (d) { return d.p[k]; })); };
  $('insights').innerHTML = [
    'Jamia Hamdard leads with ' + D[0].score.toFixed(2) + ', <strong>' + (D[0].score - D[1].score).toFixed(1) + ' points</strong> ahead of BITS Pilani. Ranks 3 to 9 sit within ' + (D[2].score - D[8].score).toFixed(1) + ' points of each other.',
    'All seven NIPERs rank between ' + nipers[0].rank + ' and ' + nipers[nipers.length - 1].rank + ' (Hyderabad ' + nipers[0].rank + ', Mohali ' + nipers[1].rank + '). They score high on Teaching and Graduation Outcomes but lower on Research than Jamia Hamdard or BITS.',
    PN[best] + ' is the strongest parameter overall (average ' + pAvg[best].toFixed(1) + ' out of 100); ' + PN[lowest] + ' is the weakest (' + pAvg[lowest].toFixed(1) + '). The top 10 lead ranks 11 to 100 by ' + gap(4).toFixed(0) + ' points on Perception and ' + gap(1).toFixed(0) + ' on Research, but only ' + gap(3).toFixed(0) + ' on Outreach.',
    stNames[0] + ' has the most ranked institutes (' + states[stNames[0]].length + '), then ' + stNames[1] + ' (' + states[stNames[1]].length + ') and ' + stNames[2] + ' (' + states[stNames[2]].length + '). Punjab has ' + pun.length + '; ' + tn.filter(function (d) { return d.rank <= 10; }).length + ' of Tamil Nadu\'s ' + tn.length + ' are in the top 10.',
    'JSS College of Pharmacy, Ooty has the best Graduation Outcomes score on the list (' + D[3].p[2].toFixed(1) + '), and Delhi Pharmaceutical Sciences and Research University the highest Perception after Jamia Hamdard. Rank is a guide: also check PCI approval, fees and placement for the specific college.'
  ].map(function (t) { return '<li>' + t + '</li>'; }).join('');

  // NIPER strip
  $('niper').innerHTML = nipers.map(function (d) {
    return '<div class="np-nip" data-i="' + d.i + '"><div class="r">#' + d.rank + '</div><b>' + esc(short(d.name)) + '</b><div class="np-ct">' + esc(d.city) + '</div><div class="s">' + d.score.toFixed(1) + '</div>' +
      '<div class="np-spark">' + d.p.map(function (v, i) { return '<i title="' + PS[i] + ' ' + v.toFixed(0) + '" style="height:' + Math.max(4, v * 0.34) + 'px"></i>'; }).join('') + '</div></div>';
  }).join('');
  $('niper').addEventListener('click', function (e) { var c = e.target.closest('.np-nip'); if (c) { show('compare'); $('c1').value = c.dataset.i; drawCmp(); } });

  function heatCol(v) { // light to navy, matching the brand ramp
    var t = Math.max(0, Math.min(1, v / 100)), a = [234, 239, 247], m = [143, 168, 214], b = [14, 58, 138], f, g;
    if (t < .5) { f = a; g = m; t = t * 2; } else { f = m; g = b; t = (t - .5) * 2; }
    return 'rgb(' + [0, 1, 2].map(function (k) { return Math.round(f[k] + (g[k] - f[k]) * t); }).join(',') + ')';
  }

  // ---------- tabs ----------
  var builders = {
    overview: function () {
      mk('cScores', { type: 'bar', data: { labels: D.map(function (d) { return d.rank; }), datasets: [{ data: D.map(function (d) { return d.score; }), backgroundColor: D.map(function (d) { return d.rank <= 10 ? NAVY : d.rank <= 25 ? OR : LB; }), borderRadius: 2 }] },
        options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false }, tooltip: { callbacks: { title: function (i) { return D[i[0].dataIndex].name; }, label: function (c) { return 'Rank ' + D[c.dataIndex].rank + ' · score ' + c.raw.toFixed(2); } } } }, scales: { x: { grid: { display: false }, ticks: { maxTicksLimit: 10 } }, y: { min: 35, grid: { color: HL } } } } });
      var bands = [['70 and above', 70, 101], ['60 to 70', 60, 70], ['50 to 60', 50, 60], ['Below 50', 0, 50]];
      var counts = bands.map(function (b) { return D.filter(function (d) { return d.score >= b[1] && d.score < b[2]; }).length; });
      mk('cBands', { type: 'doughnut', data: { labels: bands.map(function (b, i) { return b[0] + ' (' + counts[i] + ')'; }), datasets: [{ data: counts, backgroundColor: [NAVY, '#4C6CB3', OR, HL], borderWidth: 2, borderColor: '#fff' }] },
        options: { responsive: true, maintainAspectRatio: false, cutout: '58%', plugins: { legend: { position: 'bottom', labels: { boxWidth: 10, font: { size: 10 } } } } } });
      var top = stNames.slice(0, 12);
      mk('cStateCount', { type: 'bar', data: { labels: top, datasets: [{ data: top.map(function (s) { return states[s].length; }), backgroundColor: OR, borderRadius: 3 }] },
        options: { indexAxis: 'y', responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { x: { grid: { color: HL }, ticks: { stepSize: 2 } }, y: { grid: { display: false }, ticks: { font: { size: 10 } } } } } });
    },
    rankings: function () {
      var fs = $('fState'); stNames.slice().sort().forEach(function (s) { fs.insertAdjacentHTML('beforeend', '<option>' + esc(s) + '</option>'); });
      ['q', 'fState', 'fBand', 'fSort'].forEach(function (id) { $(id).addEventListener('input', renderTable); });
      renderTable();
    },
    top10: function () {
      $('podium').innerHTML = D.slice(0, 3).map(function (d) {
        return '<div class="np-pod"><div class="r">RANK ' + d.rank + '</div><h3>' + esc(d.name) + '</h3><div class="np-ct">' + esc(d.city) + ', ' + esc(d.state) + '</div><div class="s">' + d.score.toFixed(2) + '</div>' +
          d.p.map(function (v, i) { return '<div class="np-mini"><span>' + PS[i] + '</span><i><b style="width:' + v + '%"></b></i><span>' + Math.round(v) + '</span></div>'; }).join('') + '</div>';
      }).join('');
      mk('cTop10', { type: 'bar', data: { labels: PS, datasets: top10.map(function (d, i) { return { label: d.rank + '. ' + short(d.name), data: d.p, backgroundColor: COLS[i], borderRadius: 2 }; }) },
        options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'bottom', labels: { boxWidth: 10, font: { size: 10 } } } }, scales: { x: { grid: { display: false } }, y: { max: 100, grid: { color: HL } } } } });
    },
    heat: function () {
      function draw() {
        var n = +$('heatN').value;
        $('heat').innerHTML = '<thead><tr><th>#</th><th>Institute</th><th class="n">Score</th>' + PS.map(function (s, i) { return '<th class="n" title="' + PN[i] + '">' + s + '</th>'; }).join('') + '</tr></thead><tbody>' +
          D.slice(0, n).map(function (d) {
            return '<tr data-i="' + d.i + '"><td>' + d.rank + '</td><td class="np-hn">' + esc(short(d.name)) + '</td><td class="n"><b>' + d.score.toFixed(1) + '</b></td>' +
              d.p.map(function (v) { return '<td class="n np-hc" style="background:' + heatCol(v) + ';color:' + (v > 55 ? '#fff' : '#071A44') + '">' + Math.round(v) + '</td>'; }).join('') + '</tr>';
          }).join('') + '</tbody>';
      }
      $('heatN').addEventListener('change', draw); draw();
      $('heat').addEventListener('click', function (e) { var tr = e.target.closest('tr[data-i]'); if (tr) { show('compare'); $('c1').value = tr.dataset.i; drawCmp(); } });
    },
    states: function () {
      var avgs = stNames.map(function (s) { return avg(states[s].map(function (d) { return d.score; })); });
      var ord = stNames.map(function (_, i) { return i; }).sort(function (a, b) { return avgs[b] - avgs[a]; });
      mk('cStateAvg', { type: 'bar', data: { labels: ord.map(function (i) { return stNames[i] + (states[stNames[i]].length === 1 ? ' *' : ''); }), datasets: [{ data: ord.map(function (i) { return +avgs[i].toFixed(2); }), backgroundColor: ord.map(function (i) { return states[stNames[i]].length === 1 ? LB : NAVY; }), borderRadius: 3 }] },
        options: { indexAxis: 'y', responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false }, tooltip: { callbacks: { label: function (c) { return 'Average ' + c.raw + ' · ' + states[stNames[ord[c.dataIndex]]].length + ' institute(s)'; } } } }, scales: { x: { min: 35, grid: { color: HL } }, y: { grid: { display: false }, ticks: { font: { size: 9 } } } } } });
      var sel = $('stSel'); sel.innerHTML = stNames.slice().sort().map(function (s) { return '<option>' + esc(s) + '</option>'; }).join('');
      function showSt() { $('stList').innerHTML = states[sel.value].map(function (d) { return '<div><span><b>#' + d.rank + '</b> ' + esc(d.name) + ' <span class="np-ct">' + esc(d.city) + '</span></span><b>' + d.score.toFixed(1) + '</b></div>'; }).join(''); }
      sel.addEventListener('change', showSt); showSt();
    },
    params: function () {
      var t10 = PK.map(function (_, i) { return avg(top10.map(function (d) { return d.p[i]; })); });
      var t50 = PK.map(function (_, i) { return avg(D.slice(0, 50).map(function (d) { return d.p[i]; })); });
      mk('cParamAvg', { type: 'bar', data: { labels: PS, datasets: [
        { label: 'Top 10', data: t10.map(function (v) { return +v.toFixed(1); }), backgroundColor: NAVY, borderRadius: 3 },
        { label: 'Top 50', data: t50.map(function (v) { return +v.toFixed(1); }), backgroundColor: OR, borderRadius: 3 },
        { label: 'All 100', data: pAvg.map(function (v) { return +v.toFixed(1); }), backgroundColor: LB, borderRadius: 3 }] },
        options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'bottom', labels: { boxWidth: 10 } } }, scales: { x: { grid: { display: false } }, y: { max: 100, grid: { color: HL } } } } });
      $('leaders').innerHTML = PK.map(function (_, i) {
        var b = D.slice().sort(function (a, c) { return c.p[i] - a.p[i]; })[0];
        return '<div class="np-lead1"><div><em>' + PN[i] + '</em><br><b>' + esc(b.name) + '</b></div><b>' + b.p[i].toFixed(1) + '</b></div>';
      }).join('');
      mk('cScatter', { type: 'scatter', data: { datasets: [{ label: 'Institutes', data: D.map(function (d) { return { x: d.p[1], y: d.p[2], n: d.name, r: d.rank }; }), backgroundColor: D.map(function (d) { return d.rank <= 10 ? OR : 'rgba(14,58,138,.55)'; }), pointRadius: 5 }] },
        options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false }, tooltip: { callbacks: { label: function (c) { return '#' + c.raw.r + ' ' + c.raw.n + ' · RPC ' + c.raw.x + ' · GO ' + c.raw.y; } } } }, scales: { x: { title: { display: true, text: 'Research & Professional Practice' }, grid: { color: HL }, min: 0, max: 100 }, y: { title: { display: true, text: 'Graduation Outcomes' }, grid: { color: HL }, min: 30, max: 100 } } } });
    },
    compare: function () {
      var opts = D.map(function (d) { return '<option value="' + d.i + '">#' + d.rank + ' ' + esc(d.name) + '</option>'; }).join('');
      ['c1', 'c2', 'c3'].forEach(function (id, k) { var s = $(id); s.innerHTML = (k === 2 ? '<option value="">(none)</option>' : '') + opts; s.value = k === 2 ? '' : String(k === 0 ? 0 : 4); s.addEventListener('change', drawCmp); });
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
    var q = $('q').value.trim().toLowerCase(), st = $('fState').value, so = $('fSort').value, bd = $('fBand').value;
    var rows = D.filter(function (d) {
      var inBand = !bd || (bd === '100' ? d.rank > 50 : d.rank <= +bd);
      return inBand && (!st || d.state === st) && (!q || (d.name + ' ' + d.city).toLowerCase().indexOf(q) > -1);
    });
    if (so !== 'rank') { var k = PK.indexOf(so); rows = rows.slice().sort(function (a, b) { return b.p[k] - a.p[k]; }); }
    $('count').textContent = rows.length + ' of ' + D.length;
    $('tbl').querySelector('tbody').innerHTML = rows.map(function (d) {
      return '<tr data-i="' + d.i + '"><td><span class="np-rk' + (d.rank <= 3 ? ' t3' : '') + '">' + d.rank + '</span></td><td><div class="np-nm">' + esc(d.name) + '</div><div class="np-ct">' + esc(d.city) + '</div></td><td>' + esc(d.state) + '</td><td class="n"><b>' + d.score.toFixed(2) + '</b><span class="np-bar2" style="width:' + Math.round(d.score / 2) + 'px"></span></td>' +
        d.p.map(function (v) { return '<td class="n">' + v.toFixed(1) + '</td>'; }).join('') + '</tr>';
    }).join('') || '<tr><td colspan="9" style="text-align:center;padding:24px;color:#5A6278">No institute matches.</td></tr>';
  }
  $('tbl').addEventListener('click', function (e) {
    var tr = e.target.closest('tr[data-i]'); if (!tr) return;
    show('compare'); $('c1').value = tr.dataset.i; drawCmp();
  });

  function show(name) {
    document.querySelectorAll('#tabs button').forEach(function (b) { b.setAttribute('aria-selected', b.dataset.tab === name ? 'true' : 'false'); });
    document.querySelectorAll('.np-panel').forEach(function (p) { p.hidden = p.id !== 'p-' + name; });
    if (!built[name]) { built[name] = true; builders[name](); } else { Object.keys(charts).forEach(function (k) { charts[k].resize(); }); }
    try { history.replaceState(null, '', '#' + name); } catch (e) { }
    window.scrollTo({ top: 0 });
  }
  $('tabs').addEventListener('click', function (e) { var b = e.target.closest('button[data-tab]'); if (b) show(b.dataset.tab); });
  var h = (location.hash || '').slice(1);
  show(builders[h] ? h : 'overview');
})();
