/* Top engineering colleges by city region and state. Data: window.ENG (NIRF Engineering list, DASA 2025 seat matrix, researched fee / entrance / NRI text). */
(function () {
  'use strict';
  var E = window.ENG; if (!E) return;
  var $ = function (id) { return document.getElementById(id); };
  var esc = function (s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); };
  var inr = function (n) { return '₹' + n.toLocaleString('en-IN'); };
  var dark = document.documentElement.getAttribute('data-theme') === 'dark';
  var view = 'city', cur = null, flt = '', sortBy = 'rank', chart = null, q = '';
  var C = E.colleges;

  function regions() { return view === 'city' ? E.cities : E.states; }
  function groupIds(g) { return g.ids; }
  function rail() {
    var rs = regions(), t = q.trim().toLowerCase();
    $('ecRail').innerHTML = rs.map(function (g) { return '<button type="button" role="tab" data-k="' + g.key + '"' + (t && g.label.toLowerCase().indexOf(t) < 0 && (g.state || '').toLowerCase().indexOf(t) < 0 ? ' hidden' : '') + '>' + (g.capital ? '★ ' : '') + esc(g.label) + '<small>' + g.n + '</small></button>'; }).join('');
    [].slice.call($('ecRail').querySelectorAll('button')).forEach(function (b) { b.addEventListener('click', function () { select(b.dataset.k); }); });
  }
  function mark() {
    [].slice.call($('ecRail').querySelectorAll('button')).forEach(function (b) { b.classList.toggle('on', b.dataset.k === cur); });
    var on = $('ecRail').querySelector('button.on'); if (on && on.scrollIntoView) { try { on.scrollIntoView({ block: 'nearest', inline: 'center' }); } catch (e) {} }
  }
  function find(k) { return regions().filter(function (g) { return g.key === k; })[0]; }
  function search(t) {
    var out = [];
    Object.keys(C).forEach(function (k) { var c = C[k]; if ((c.name + ' ' + c.city + ' ' + c.state).toLowerCase().indexOf(t) > -1) out.push(c); });
    out.sort(function (a, b) { return (a.rank || 999) - (b.rank || 999); });
    return out.slice(0, 24);
  }
  function select(k) {
    cur = k; mark(); draw();
    try { history.replaceState(null, '', '#' + k); } catch (e) {}
  }
  function nriInfo(c) {
    var parts = [];
    if (c.dasa) parts.push('<span class="ec-tag">DASA</span>' + c.dasa.seats + ' supernumerary seats in ' + c.dasa.programmes + ' programmes <small>(DASA 2025 matrix)</small>');
    if (c.nri) parts.push(esc(c.nri));
    if (!parts.length) {
      if (c.type === 'IIT') return '<span class="ec-na">No DASA seats: IITs are outside DASA</span>';
      return '<span class="ec-na">Not published: ask the college</span>';
    }
    return parts.join('<br>');
  }
  function hasNri(c) { return !!(c.dasa || c.nri); }
  function card(c, i) {
    var elig = c.eligibility ? esc(c.eligibility) : null, short = elig && elig.length > 150 ? elig.slice(0, 150).replace(/\s+\S*$/, '') + '…' : elig;
    return '<article class="ec-c"><div class="ec-img"><img src="' + E.tile + c.key + '.svg" alt="" loading="lazy" width="400" height="220"><span class="ec-rk">' + esc(c.label) + '</span><span class="ec-ty">' + esc(E.types[c.type] || c.type) + '</span></div>' +
      '<div class="ec-b"><h4>' + esc(c.name) + '</h4><small>' + esc(c.city) + ', ' + esc(c.state) + '</small>' +
      (c.score ? '<div class="ec-sc"><span>NIRF score</span><div><i style="width:' + Math.min(100, c.score) + '%"></i></div><b>' + c.score.toFixed(1) + '</b></div>' : '<div class="ec-sc"><span>NIRF band</span><b>' + esc((c.band || '').replace('Rank ', '')) + '</b></div>') +
      '<dl class="ec-dl"><dt>Entrance</dt><dd>' + (c.exams ? esc(c.exams.join(', ')) : (c.type === 'IIT' ? 'JEE Advanced via JoSAA' : c.type === 'NIT' || c.dasa ? 'JEE Main via JoSAA / CSAB' : '<span class="ec-na">Ask the college</span>')) + '</dd>' +
      '<dt>Eligible</dt><dd>' + (short ? short + (elig.length > 150 ? '<details class="ec-more"><summary>Full rule</summary>' + elig + '<br><small>As stated by ' + esc(c.elig_src || 'the college') + '</small></details>' : '<br><small class="ec-more">As stated by ' + esc(c.elig_src || 'the college') + '</small>') : '<span class="ec-na">Not published: ask the college</span>') + '</dd>' +
      '<dt>Fee</dt><dd>' + (c.fee ? '<b>' + inr(c.fee) + '</b> a year' + (c.fee_year ? ' <small>(tuition, ' + esc(c.fee_year) + ')</small>' : ' <small>(tuition)</small>') + (c.fee_note ? '<br><small class="ec-more">' + esc(c.fee_note) + '</small>' : '') : '<span class="ec-na">Not published: ask the college</span>') + '</dd>' +
      '<dt>NRI quota</dt><dd>' + nriInfo(c) + '</dd></dl>' +
      '<div class="ec-ft">' + (c.website ? '<a href="' + esc(c.website) + '" target="_blank" rel="noopener nofollow">College website</a>' : '<span></span>') + '<span class="ec-more">' + esc(c.state) + '</span></div></div></article>';
  }
  function draw() {
    var g, ids, title, sub, list;
    var t = q.trim().toLowerCase();
    if (cur === '_search') {
      list = search(t); title = 'Colleges matching “' + esc(q.trim()) + '”'; sub = list.length + ' found in the NIRF Engineering list';
    } else {
      g = find(cur) || regions()[0]; cur = g.key; ids = groupIds(g); list = ids.map(function (k) { return C[k]; });
      title = 'Top ' + list.length + ' engineering colleges in ' + esc(g.label); sub = (view === 'city' ? g.state + ' · ' : '') + list.length + ' of ' + g.n + ' NIRF-listed institutions in this ' + (view === 'city' ? 'region' : 'state') + ', best NIRF position first';
    }
    $('ecTitle').innerHTML = title; $('ecSub').textContent = sub;
    var shown = list.filter(function (c) { return flt === 'nri' ? hasNri(c) : flt === 'govt' ? c.govt : flt === 'pri' ? !c.govt : true; });
    if (sortBy === 'fee') shown = shown.slice().sort(function (a, b) { return (a.fee || 1e12) - (b.fee || 1e12); });
    // stats
    var ranked = list.filter(function (c) { return c.rank; }), sc = list.filter(function (c) { return c.score; });
    var best = ranked.length ? Math.min.apply(null, ranked.map(function (c) { return c.rank; })) : null;
    var avg = sc.length ? sc.reduce(function (a, c) { return a + c.score; }, 0) / sc.length : null;
    var feeKnown = list.filter(function (c) { return c.fee; });
    $('ecStats').innerHTML = [
      [best ? '#' + best : '–', 'best NIRF rank'], [avg ? avg.toFixed(1) : '–', 'average NIRF score'], [list.filter(function (c) { return c.govt; }).length + ' / ' + list.filter(function (c) { return !c.govt; }).length, 'central / private or deemed'],
      [list.filter(hasNri).length, 'with an NRI route'], [feeKnown.length ? inr(Math.min.apply(null, feeKnown.map(function (c) { return c.fee; }))) : '–', 'lowest published fee']
    ].map(function (s) { return '<div><b>' + s[0] + '</b><span>' + s[1] + '</span></div>'; }).join('');
    $('ecGrid').innerHTML = shown.map(card).join('');
    $('ecNone').hidden = shown.length > 0;
    // chart
    var cs = list.filter(function (c) { return c.score; });
    $('ecCvW').style.height = Math.max(200, cs.length * 28 + 60) + 'px';
    if (chart) chart.destroy();
    if (window.Chart && cs.length) {
      chart = new Chart($('ecChart'), { type: 'bar', data: { labels: cs.map(function (c) { return c.label.replace('NIRF ', '') + ' ' + c.name.replace('Indian Institute of Technology', 'IIT').replace('National Institute of Technology', 'NIT').replace(/,.*$/, '').slice(0, 30); }), datasets: [{ data: cs.map(function (c) { return c.score; }), backgroundColor: cs.map(function (c) { return c.govt ? '#0E3A8A' : '#FF6B0A'; }), borderRadius: 4 }] },
        options: { indexAxis: 'y', responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false }, tooltip: { callbacks: { label: function (x) { return 'NIRF score ' + x.raw.toFixed(2); } } } }, scales: { x: { min: 0, title: { display: true, text: 'NIRF score (blue: IIT, NIT, IIIT, centrally funded; orange: others)' } } } } });
    } else if (window.Chart) { chart = null; }
  }
  function cmp() {
    var rs = regions().slice().sort(function (a, b) { return (a.best || 999) - (b.best || 999); });
    $('ecCmp').querySelector('tbody').innerHTML = rs.map(function (g) { return '<tr class="cl" data-k="' + g.key + '"><td>' + esc(g.label) + '</td><td class="n">' + (g.best ? '#' + g.best : '–') + '</td><td class="n">' + (g.top100 != null ? g.top100 : '') + '</td><td class="n">' + (g.avg || '') + '</td></tr>'; }).join('');
    [].slice.call($('ecCmp').querySelectorAll('tr.cl')).forEach(function (r) { r.addEventListener('click', function () { select(r.dataset.k); window.scrollTo({ top: $('ecPanel').offsetTop - 10, behavior: 'smooth' }); }); });
  }
  // view toggle, filters, search
  [].slice.call($('ecView').querySelectorAll('button')).forEach(function (b) { b.addEventListener('click', function () {
    [].slice.call($('ecView').querySelectorAll('button')).forEach(function (x) { x.classList.remove('on'); }); b.classList.add('on'); view = b.dataset.v;
    cur = view === 'city' ? 'chennai' : 'tamil-nadu'; rail(); cmp(); select(cur); }); });
  [].slice.call($('ecFl').querySelectorAll('button')).forEach(function (b) { b.addEventListener('click', function () {
    [].slice.call($('ecFl').querySelectorAll('button')).forEach(function (x) { x.classList.remove('on'); }); b.classList.add('on'); flt = b.dataset.f; draw(); }); });
  $('ecSort').addEventListener('change', function () { sortBy = this.value; draw(); });
  $('ecQ').addEventListener('input', function () {
    q = this.value; rail();
    var t = q.trim().toLowerCase();
    if (t.length >= 3 && !regions().some(function (g) { return g.label.toLowerCase().indexOf(t) > -1; }) && search(t).length) { cur = '_search'; draw(); mark(); }
    else if (cur === '_search') { cur = view === 'city' ? 'chennai' : 'tamil-nadu'; draw(); mark(); }
    else mark();
  });
  function setView(v) { view = v; [].slice.call($('ecView').querySelectorAll('button')).forEach(function (b) { b.classList.toggle('on', b.dataset.v === v); }); }
  function applyHash(first) {
    var h = (location.hash || '').slice(1) || new URLSearchParams(location.search).get('city') || '';
    var isCity = E.cities.some(function (c) { return c.key === h; }), isState = E.states.some(function (c) { return c.key === h; });
    if (h && (isCity || isState)) { var v = isCity ? 'city' : 'state'; if (v !== view) { setView(v); rail(); cmp(); } cur = h; mark(); draw(); return; }
    if (first) { cur = view === 'city' ? 'chennai' : 'tamil-nadu'; rail(); cmp(); mark(); draw(); }
  }
  rail(); cmp(); applyHash(true);
  window.addEventListener('hashchange', function () { applyHash(false); });
})();
