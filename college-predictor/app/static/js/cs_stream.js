/* Computer stream explainer: builds each panel from the page data (window script #cs-data). No external libraries. */
(function () {
  'use strict';
  var D = JSON.parse(document.getElementById('cs-data').textContent);
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var esc = function (s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); };
  var FAM = {}; D.families.forEach(function (f) { FAM[f[0]] = f[1]; });
  var FAMKEYS = D.families.map(function (f) { return f[0]; });
  var BR = {}; D.branches.forEach(function (b) { BR[b.key] = b; });
  var short = function (k) { return String(FAM[k] || k).split(' (')[0]; };
  var fchip = function (k, n) { return '<span class="cs-fchip cs-f-' + k + '" title="' + esc(FAM[k] || k) + '"><i></i>' + esc(short(k)) + (n ? ' <b class="cs-n">' + n + '</b>' : '') + '</span>'; };
  var rankText = function (r, b) { return r ? '<span class="cs-rank">#' + r + '</span>' : (b && !/^Rank 1 ?-100$/.test(b) ? '<span class="cs-rank"><small>' + esc(b.replace('Rank ', '')) + '</small></span>' : '<small class="cs-small">not in list</small>'); };
  var pct = function (a, b) { return b ? Math.round(100 * a / b) : 0; };

  // ---- numbers used in the page -----------------------------------------------------------------------------------------------------------------
  var inst = D.josaa;
  var byType = {};
  inst.forEach(function (i) { var t = i.t === 'Other' ? 'Other' : i.t; (byType[t] = byType[t] || []).push(i); });
  var famSet = function (i) { var s = {}; i.p.forEach(function (p) { s[p[1]] = 1; }); return s; };
  var iits = byType.IIT || [];
  var iitCoreOnly = iits.filter(function (i) { return Object.keys(famSet(i)).every(function (k) { return k === 'core' || k === 'mnc'; }); }).length;
  var iitAi = iits.filter(function (i) { return famSet(i).aids; }).length;

  // ---- tabs --------------------------------------------------------------------------------------------------------------------------------------
  function show(tab, push) {
    $$('#tabs button').forEach(function (b) { b.setAttribute('aria-selected', b.dataset.tab === tab ? 'true' : 'false'); });
    $$('.cs-panel').forEach(function (p) { p.hidden = p.dataset.panel !== tab; });
    if (push) history.replaceState(null, '', '#' + tab);
    window.scrollTo({ top: Math.max(0, $('#tabs').getBoundingClientRect().top + window.scrollY - 8), behavior: 'smooth' });
  }
  $('#tabs').addEventListener('click', function (e) { var b = e.target.closest('button'); if (b) show(b.dataset.tab, true); });
  document.addEventListener('click', function (e) { var g = e.target.closest('[data-go]'); if (g) { e.preventDefault(); show(g.dataset.go, true); } });

  // ---- KPIs --------------------------------------------------------------------------------------------------------------------------------------
  $('#kpis').innerHTML = [
    [inst.length, 'JoSAA institutes with a computer-stream branch'],
    [D.n_programmes, 'computer-stream programmes in the JoSAA 2026 list'],
    [D.families.length, 'branch families compared'],
    [D.private.length + (D.tnea ? D.tnea.listed.length : 0), 'private and state colleges with branch lists']
  ].map(function (k) { return '<div class="cs-kpi"><b>' + k[0] + '</b><span>' + k[1] + '</span></div>'; }).join('');

  // ---- START -------------------------------------------------------------------------------------------------------------------------------------
  $('#p-start').innerHTML =
    '<div class="cs-card"><h2>The short answer</h2>' +
    '<p>All computer branches share the same foundation: programming, data structures, maths for computing, databases, operating systems and networks. They differ mainly in the <b>last two years</b>: which electives you take and what your final project is about. ' +
    'A CSE student who picks machine-learning electives and builds an ML project ends up close to an AI and Data Science student. The label matters less than the <b>college, the department and what you build</b>.</p>' +
    '<p>The label does matter in three places: <b>recruiter eligibility lists</b>, <b>entrance and admission rules</b> (for example GATE papers and some master\'s programmes) and <b>how a college is organised</b>. The tabs above take these one at a time.</p></div>' +
    '<h2>The computer stream at a glance</h2><p class="cs-sub">Seven families. Tap one to read it in full.</p>' +
    '<div class="cs-bcards">' + D.branches.map(function (b) {
      return '<div class="cs-bc cs-f-' + b.family + '"><h3>' + esc(b.short) + '</h3><p>' + esc(b.tagline) + '</p>' +
        '<div class="cs-meter" title="Overlap with core CSE">' + [1, 2, 3, 4, 5].map(function (n) { return '<i class="' + (n <= b.overlap ? 'on' : '') + '"></i>'; }).join('') + '<span class="cs-small" style="margin-left:6px">overlap with CSE</span></div>' +
        '<button type="button" data-open="' + b.key + '">Read the full comparison →</button></div>';
    }).join('') + '</div>' +
    '<div class="cs-grid2" style="margin-top:14px"><div class="cs-card"><h2>Three things to check before the label</h2><ul class="cs-list">' +
    '<li><b>The department</b>: its own faculty, labs and electives, not borrowed from CSE for two courses.</li>' +
    '<li><b>Recruiter eligibility</b>: ask for the last three years\' lists and branch-wise offers.</li>' +
    '<li><b>The rank and the college</b>: a strong college with a newer label usually beats a weak college with CSE.</li></ul></div>' +
    '<div class="cs-card"><h2>Where to go next</h2><ul class="cs-list">' +
    '<li><a href="#" data-go="colleges">Which colleges offer which branch, with NIRF ranks</a></li>' +
    '<li><a href="#" data-go="why">Why leading institutes offer few computer branches and private universities many</a></li>' +
    '<li><a href="#" data-go="choose">When to consider each branch (a short guide)</a></li>' +
    '<li><a href="#" data-go="ai">What AI changes, the jobs ahead and the skills to build</a></li></ul></div></div>';
  $('#p-start').addEventListener('click', function (e) { var o = e.target.closest('[data-open]'); if (o) { show('branches', true); var d = $('#acc-' + o.dataset.open); if (d) { d.open = true; setTimeout(function () { d.scrollIntoView({ behavior: 'smooth', block: 'start' }); }, 200); } } });

  // ---- BRANCHES ----------------------------------------------------------------------------------------------------------------------------------
  function li(a) { return '<ul>' + a.map(function (x) { return '<li>' + esc(x) + '</li>'; }).join('') + '</ul>'; }
  $('#p-branches').innerHTML =
    '<h2>The branches, one by one</h2><p class="cs-sub">What it is, who it suits, when to consider it, and the honest caution. Names vary by college: the "also called" line lists the common ones.</p>' +
    D.branches.map(function (b) {
      return '<details class="cs-acc cs-f-' + b.family + '" id="acc-' + b.key + '"><summary><b>' + esc(b.name) + '</b><span>' + esc(b.tagline) + '</span></summary><div class="cs-acc-body">' +
        '<div class="cs-acc-wide"><p>' + esc(b.what) + '</p><p class="cs-small">Also called: ' + esc(b.also) + '</p></div>' +
        '<div><h4>Suits you if</h4>' + li(b.suits) + '</div><div><h4>Consider it when</h4>' + li(b.consider) + '</div>' +
        '<div class="cs-acc-wide"><h4>Watch out</h4><p>' + esc(b.caution) + '</p></div></div></details>';
    }).join('') +
    '<div class="cs-card cs-note"><b>How to read "overlap".</b> It is our reading of how much of a typical syllabus matches core CSE (5 means nearly all). It is not a college\'s official figure: compare the credit tables of the colleges you are considering.</div>';

  // ---- SUBJECTS ----------------------------------------------------------------------------------------------------------------------------------
  var cells = '';
  var last = '';
  D.subjects.forEach(function (s) {
    if (s[2] !== last) { cells += '<tr class="cs-sec"><td colspan="' + (D.subject_cols.length + 1) + '">' + (s[2] === 'common' ? 'Common to almost every computer branch' : 'Where the branches differ') + '</td></tr>'; last = s[2]; }
    cells += '<tr><td>' + esc(s[0]) + '</td>' + s[1].map(function (v) { return '<td class="l' + v + '">' + ['–', 'light', 'solid', 'core'][v] + '</td>'; }).join('') + '</tr>';
  });
  $('#p-subjects').innerHTML =
    '<h2>Subjects: what is common, and where the real difference is</h2><p class="cs-sub">Our reading of typical syllabi. Intensity of each subject by branch.</p>' +
    '<div class="cs-card"><div class="cs-matrix-wrap"><table class="cs-matrix"><thead><tr><th>Subject</th>' + D.subject_cols.map(function (c) { return '<th>' + esc(c) + '</th>'; }).join('') + '</tr></thead><tbody>' + cells + '</tbody></table></div>' +
    '<div class="cs-legend"><span style="--lc:#0E3A8A">core and deep</span><span style="--lc:#9BB6E8">solid</span><span style="--lc:#DCE6F7">light or elective</span><span style="--lc:#F4F1E6">not taught</span></div></div>' +
    '<h2>Semester by semester</h2><div class="cs-journey">' + D.journey.map(function (j) { return '<div class="cs-step"><small>' + esc(j.when) + '</small><b>' + esc(j.title) + '</b><p>' + esc(j.text) + '</p></div>'; }).join('') + '</div>' +
    '<div class="cs-card cs-note"><b>The takeaway.</b> The first two years are close to identical across the computer branches. The difference is concentrated in the electives and the project of years 3 and 4. So the question is not "which label has the right subjects" but "does this college\'s department teach the electives and run the labs I want".</div>';

  // ---- CAREERS -----------------------------------------------------------------------------------------------------------------------------------
  function careersFor(k) {
    var b = BR[k];
    return '<div class="cs-grid3"><div class="cs-card"><h3>Typical roles</h3>' + li(b.roles) + '</div><div class="cs-card"><h3>Project ideas</h3>' + li(b.projects) + '</div>' +
      '<div class="cs-card"><h3>Internships</h3><p>' + esc(b.intern) + '</p><h3>Higher studies</h3><p>' + esc(b.higher) + '</p></div></div>';
  }
  $('#p-careers').innerHTML =
    '<h2>Projects, internships and placements</h2><p class="cs-sub">Pick a branch family. No salary or placement-percentage figures are shown: none is verified for a branch label.</p>' +
    '<div id="car-chips">' + D.branches.map(function (b, i) { return '<button type="button" class="cs-fchip cs-f-' + b.family + '" data-car="' + b.key + '" aria-pressed="' + (i === 0) + '"><i></i>' + esc(b.short) + '</button>'; }).join('') + '</div>' +
    '<div id="car-body">' + careersFor(D.branches[0].key) + '</div>' +
    '<h2>Internship path</h2><div class="cs-roadmap">' + D.internship_path.map(function (s) { return '<div><b>' + esc(s[0]) + '</b>' + esc(s[1]) + '</div>'; }).join('') + '</div>' +
    '<h2 style="margin-top:18px">Placements: what to know</h2><div class="cs-grid2">' + D.placement_notes.map(function (n) { return '<div class="cs-card"><h3 style="margin-top:0">' + esc(n[0]) + '</h3><p style="margin:0">' + esc(n[1]) + '</p></div>'; }).join('') + '</div>';
  $('#car-chips').addEventListener('click', function (e) { var b = e.target.closest('[data-car]'); if (!b) return; $$('#car-chips button').forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); }); $('#car-body').innerHTML = careersFor(b.dataset.car); });

  // ---- COLLEGES ----------------------------------------------------------------------------------------------------------------------------------
  var state = { sub: 'josaa', type: '', q: '', fam: {}, nirfOnly: false, pq: '', pcity: '', pfam: {} };
  var typeOrder = ['IIT', 'NIT', 'IIIT', 'Other'];
  var typeName = { IIT: 'IITs', NIT: 'NITs', IIIT: 'IIITs', Other: 'Other JoSAA institutes' };

  function josaaRows() {
    var want = Object.keys(state.fam).filter(function (k) { return state.fam[k]; });
    var rows = inst.filter(function (i) {
      if (state.type && i.t !== state.type) return false;
      if (state.nirfOnly && !(i.r || (i.b && !/^Rank 1 ?-100$/.test(i.b)))) return false;
      if (state.q && (i.n + ' ' + (i.s || '')).toLowerCase().indexOf(state.q.toLowerCase()) < 0) return false;
      if (want.length) { var s = famSet(i); if (!want.every(function (k) { return s[k]; })) return false; }
      return true;
    });
    rows.sort(function (a, b) { var ra = a.r || 9999, rb = b.r || 9999; return ra - rb || a.n.localeCompare(b.n); });
    return rows;
  }
  function progList(i) {
    return '<ul class="cs-prog">' + i.p.map(function (p) { return '<li><b style="color:var(--fc)" class="cs-f-' + p[1] + '">●</b> ' + esc(p[0]) + (p[2] ? ' <em>(' + p[2] + '-year)</em>' : '') + (p[3] ? ' <em>· closing rank ' + p[3].toLocaleString('en-IN') + '</em>' : '') + '</li>'; }).join('') + '</ul>';
  }
  function josaaTable() {
    var rows = josaaRows();
    if (!rows.length) return '<div class="cs-empty">No institute matches these filters.</div>';
    return '<p class="cs-small">' + rows.length + ' institutes. Tap a row to see every programme with its closing rank.</p><div class="cs-tbl-wrap"><table class="cs-tbl"><thead><tr><th>NIRF</th><th>Institute</th><th>Computer-stream families</th></tr></thead><tbody>' +
      rows.map(function (i) {
        var s = famSet(i);
        return '<tr><td>' + rankText(i.r, i.b) + '</td><td><details class="cs-row"><summary><b>' + esc(i.n) + '</b><span class="cs-type">' + esc(i.t) + '</span>' + (i.s ? '<br><small class="cs-small">' + esc(i.s) + '</small>' : '') + '</summary>' + progList(i) + '</details></td>' +
          '<td>' + FAMKEYS.filter(function (k) { return s[k]; }).map(function (k) { return fchip(k, i.p.filter(function (p) { return p[1] === k; }).length); }).join('') + '</td></tr>';
      }).join('') + '</tbody></table></div>';
  }
  function privRows() {
    var want = Object.keys(state.pfam).filter(function (k) { return state.pfam[k]; });
    return D.private.filter(function (u) {
      if (state.pcity && u.city !== state.pcity) return false;
      if (state.pq && (u.n + ' ' + (u.city || '') + ' ' + (u.state || '')).toLowerCase().indexOf(state.pq.toLowerCase()) < 0) return false;
      if (want.length) { var s = {}; u.p.forEach(function (p) { if (p[1]) s[p[1]] = 1; }); if (!want.every(function (k) { return s[k]; })) return false; }
      return true;
    });
  }
  function privTable() {
    var rows = privRows();
    if (!rows.length) return '<div class="cs-empty">No university matches these filters.</div>';
    return '<p class="cs-small">' + rows.length + ' universities. Tap "programmes" to list them all.</p><div class="cs-tbl-wrap"><table class="cs-tbl"><thead><tr><th>NIRF</th><th>University</th><th>Admission route (as stated on the page)</th><th>Computer-stream programmes</th></tr></thead><tbody>' +
      rows.map(function (u) {
        var cnt = {}; u.p.forEach(function (p) { if (p[1]) cnt[p[1]] = (cnt[p[1]] || 0) + 1; });
        return '<tr><td>' + rankText(u.r, u.b) + '</td><td><b>' + esc(u.n) + '</b>' + (u.city ? '<br><small class="cs-small">' + esc(u.city) + (u.state ? ', ' + esc(u.state) : '') + (u.campus ? ' · ' + esc(u.campus) + ' campus' : '') + '</small>' : '') + (u.url ? '<br><a class="cs-small" href="' + esc(u.url) + '" target="_blank" rel="noopener">' + (u.kind && u.kind !== 'own site' ? 'Official filing (NIRF or AICTE) ↗' : 'University page ↗') + '</a>' : '') + '</td>' +
          '<td>' + (u.entrance ? esc(u.entrance) : '<span class="cs-small">Not stated on the page read: check the university</span>') + '</td>' +
          '<td><div>' + FAMKEYS.filter(function (k) { return cnt[k]; }).map(function (k) { return fchip(k, cnt[k]); }).join('') + '</div><details class="cs-row"><summary><b>' + u.p.length + ' programme' + (u.p.length === 1 ? '' : 's') + '</b> <span class="cs-small">(tap to list)</span></summary><ul class="cs-prog">' + u.p.map(function (p) { return '<li>' + esc(p[0]) + '</li>'; }).join('') + '</ul>' + (u.caveat ? '<p class="cs-small cs-cav">' + esc(u.caveat) + '</p>' : '') + '</details>' + (u.partial ? '<span class="cs-pill or" title="The page read may not show every programme">List may be incomplete</span>' : '') + '</td></tr>';
      }).join('') + '</tbody></table></div>';
  }
  function colleges() {
    var out = '<h2>Colleges and the branches they offer</h2><p class="cs-sub">Three lists from three sources. The JoSAA list is the full set of IITs, NITs, IIITs and other centrally funded institutes; private universities and Tamil Nadu counselling colleges are shown separately because they are admitted differently.</p>' +
      '<div class="cs-sub-tabs" id="sub-tabs">' + [['josaa', 'IITs, NITs, IIITs and other JoSAA institutes (' + inst.length + ')'], ['private', 'Private universities (' + D.private.length + ')'], ['tnea', 'Tamil Nadu counselling colleges']].map(function (t) { return '<button type="button" data-sub="' + t[0] + '" aria-pressed="' + (state.sub === t[0]) + '">' + t[1] + '</button>'; }).join('') + '</div>';
    if (state.sub === 'josaa') {
      out += '<div class="cs-filters"><input type="search" id="f-q" placeholder="Search institute or state" value="' + esc(state.q) + '" aria-label="Search institute or state">' +
        '<select id="f-type" aria-label="Institute type"><option value="">All types</option>' + typeOrder.map(function (t) { return '<option value="' + t + '"' + (state.type === t ? ' selected' : '') + '>' + typeName[t] + '</option>'; }).join('') + '</select>' +
        '<label class="cs-small"><input type="checkbox" id="f-nirf"' + (state.nirfOnly ? ' checked' : '') + '> NIRF-ranked only</label></div>' +
        '<div id="f-fam">' + FAMKEYS.map(function (k) { return '<button type="button" class="cs-fchip cs-f-' + k + '" data-fam="' + k + '" title="' + esc(FAM[k]) + '" aria-pressed="' + !!state.fam[k] + '"><i></i>' + esc(short(k)) + '</button>'; }).join('') + '</div>' +
        '<div class="cs-card" id="josaa-out" style="margin-top:10px">' + josaaTable() + '</div>' +
        '<p class="cs-small">' + esc(D.josaa_meta.source) + '. Closing rank: ' + esc(D.josaa_meta.rank_rule) + '. NIRF: ' + esc(D.josaa_meta.nirf_source || 'NIRF Engineering list held on the portal') + '. Institutes not found in that list show "not in list"; that is not a judgement on quality.</p>';
    } else if (state.sub === 'private') {
      var cities = {};
      D.private.forEach(function (u) { if (u.city) cities[u.city] = (cities[u.city] || 0) + 1; });
      var cityList = Object.keys(cities).sort(function (a, b) { return cities[b] - cities[a] || a.localeCompare(b); });
      out += '<div class="cs-card cs-note">Branch lists below were read from each university’s own website' + (D.private_checked ? ' on ' + esc(D.private_checked) : '') + '. ' + esc(D.private_note || '') + ' Seats, branches and entrance routes change every year: confirm on the university’s admission page.</div>' +
        '<div class="cs-filters"><input type="search" id="p-q" placeholder="Search university or city" value="' + esc(state.pq) + '" aria-label="Search university or city">' +
        '<select id="p-city" aria-label="City"><option value="">All cities (' + D.private.length + ')</option>' + cityList.map(function (c) { return '<option value="' + esc(c) + '"' + (state.pcity === c ? ' selected' : '') + '>' + esc(c) + ' (' + cities[c] + ')</option>'; }).join('') + '</select></div>' +
        '<div id="p-fam">' + FAMKEYS.map(function (k) { return '<button type="button" class="cs-fchip cs-f-' + k + '" data-pfam="' + k + '" title="' + esc(FAM[k]) + '" aria-pressed="' + !!state.pfam[k] + '"><i></i>' + esc(short(k)) + '</button>'; }).join('') + '</div>' +
        '<div class="cs-card" id="priv-out" style="margin-top:10px">' + privTable() + '</div>' +
        '<p class="cs-small">Universities whose pages could not be read, or whose list looked incomplete, are left out rather than guessed. NIRF is the NIRF Engineering position or band held on the portal.</p>';
    } else {
      var t = D.tnea;
      if (!t) { out += '<div class="cs-empty">Tamil Nadu data is not available.</div>'; }
      else {
        out += '<div class="cs-card"><h2>Colleges offering each branch family in Tamil Nadu counselling</h2><p class="cs-sub">Of the ' + t.total + ' colleges with allotments in TNEA 2026. This is how fast private colleges have added branches.</p>' +
          FAMKEYS.filter(function (k) { return t.counts[k] != null; }).map(function (k) { return '<div class="cs-hbar cs-f-' + k + '" style="margin:6px 0"><span style="min-width:230px;color:#0E1B3D">' + esc(FAM[k]) + '</span><div style="width:' + pct(t.counts[k], t.total) * 0.55 + '%"></div><span>' + t.counts[k] + ' of ' + t.total + ' (' + pct(t.counts[k], t.total) + '%)</span></div>'; }).join('') + '</div>' +
          '<div class="cs-card"><h2>NIRF-listed colleges and their computer-stream branches</h2><div class="cs-tbl-wrap"><table class="cs-tbl"><thead><tr><th>NIRF</th><th>College</th><th>Branches in TNEA 2026</th></tr></thead><tbody>' +
          t.listed.map(function (c) { return '<tr><td>' + rankText(c.nirf_rank, c.nirf_band) + '</td><td><b>' + esc(c.name) + '</b><br><small class="cs-small">' + esc(c.city || '') + '</small></td><td><ul class="cs-prog">' + c.programmes.map(function (p) { return '<li>' + esc(p) + '</li>'; }).join('') + '</ul></td></tr>'; }).join('') +
          '</tbody></table></div></div><p class="cs-small">' + esc(t.source) + '. Only colleges that appear in the NIRF Engineering list are shown. Deemed universities such as SRM, VIT and SASTRA admit through their own exams, not TNEA: see the private universities list.</p>';
      }
    }
    $('#p-colleges').innerHTML = out;
  }
  colleges();
  $('#p-colleges').addEventListener('click', function (e) {
    var s = e.target.closest('[data-sub]'); if (s) { state.sub = s.dataset.sub; colleges(); return; }
    var pf = e.target.closest('[data-pfam]'); if (pf) { state.pfam[pf.dataset.pfam] = !state.pfam[pf.dataset.pfam]; pf.setAttribute('aria-pressed', state.pfam[pf.dataset.pfam] ? 'true' : 'false'); $('#priv-out').innerHTML = privTable(); return; }
    var f = e.target.closest('[data-fam]'); if (f) { state.fam[f.dataset.fam] = !state.fam[f.dataset.fam]; f.setAttribute('aria-pressed', state.fam[f.dataset.fam] ? 'true' : 'false'); $('#josaa-out').innerHTML = josaaTable(); }
  });
  $('#p-colleges').addEventListener('input', function (e) { if (e.target.id === 'f-q') { state.q = e.target.value; $('#josaa-out').innerHTML = josaaTable(); } if (e.target.id === 'p-q') { state.pq = e.target.value; $('#priv-out').innerHTML = privTable(); } });
  $('#p-colleges').addEventListener('change', function (e) {
    if (e.target.id === 'f-type') { state.type = e.target.value; $('#josaa-out').innerHTML = josaaTable(); }
    if (e.target.id === 'p-city') { state.pcity = e.target.value; $('#priv-out').innerHTML = privTable(); }
    if (e.target.id === 'f-nirf') { state.nirfOnly = e.target.checked; $('#josaa-out').innerHTML = josaaTable(); }
  });

  // ---- WHY TOP INSTITUTES STAY CORE ----------------------------------------------------------------------------------------------------------------
  var heat = '<div class="cs-card"><h2>What each kind of institute offers</h2><p class="cs-sub">Share of institutes that list at least one programme in each family (JoSAA 2026).</p><div class="cs-tbl-wrap"><table class="cs-tbl cs-heat"><thead><tr><th>Institute type</th><th>Institutes</th>' + FAMKEYS.map(function (k) { return '<th>' + esc(FAM[k].split(' (')[0]) + '</th>'; }).join('') + '</tr></thead><tbody>' +
    typeOrder.filter(function (t) { return byType[t]; }).map(function (t) {
      var L = byType[t];
      return '<tr><td><b>' + typeName[t] + '</b></td><td>' + L.length + '</td>' + FAMKEYS.map(function (k) { var n = L.filter(function (i) { return famSet(i)[k]; }).length, p = pct(n, L.length); return '<td class="h" style="background:rgba(14,58,138,' + (p / 100 * 0.85 + 0.04) + ');color:' + (p > 45 ? '#fff' : '#0E1B3D') + '">' + p + '%</td>'; }).join('') + '</tr>';
    }).join('') + '</tbody></table></div></div>';
  var top = inst.filter(function (i) { return i.r; }).sort(function (a, b) { return a.r - b.r; }).slice(0, 12);
  var topTbl = '<div class="cs-card"><h2>The twelve best-ranked JoSAA institutes</h2><p class="cs-sub">By NIRF Engineering rank. How many computer-stream families does each one offer?</p><div class="cs-tbl-wrap"><table class="cs-tbl"><thead><tr><th>NIRF</th><th>Institute</th><th>Families offered</th></tr></thead><tbody>' +
    top.map(function (i) { var s = famSet(i); return '<tr><td>' + rankText(i.r) + '</td><td><b>' + esc(i.n.replace('Indian Institute of Technology', 'IIT').replace('National Institute of Technology', 'NIT')) + '</b></td><td>' + FAMKEYS.filter(function (k) { return s[k]; }).map(function (k) { return fchip(k); }).join('') + '</td></tr>'; }).join('') + '</tbody></table></div></div>';
  var nProg = function (i) { var u = {}; i.p.forEach(function (p) { u[p[0]] = 1; }); return Object.keys(u).length; };
  var median = function (a) { a = a.slice().sort(function (x, y) { return x - y; }); var m = a.length >> 1; return a.length ? (a.length % 2 ? a[m] : (a[m - 1] + a[m]) / 2) : 0; };
  var med = function (t) { return median((byType[t] || []).map(nProg)); };
  var privMed = median(D.private.map(function (u) { return u.p.length; }));
  var privMax = Math.max.apply(null, D.private.map(function (u) { return u.p.length; }).concat([0]));
  var oneFam = iits.filter(function (i) { return Object.keys(famSet(i)).length === 1; }).length;
  $('#p-why').innerHTML =
    '<h2>Why do the leading institutes keep the computer family small while private universities offer many variants?</h2>' +
    '<div class="cs-card"><p>The data says it is a matter of <b>how many</b>, not a strict "CSE only". In the JoSAA 2026 list the <b>median IIT offers ' + med('IIT') + ' computer-stream programmes</b>, the median NIT ' + med('NIT') + ' and the median IIIT ' + med('IIIT') + '. ' +
    'Almost every IIT offers core CSE plus one or two focused programmes (most often Mathematics and Computing, and at ' + iitAi + ' of ' + iits.length + ' IITs an AI or Data Science programme); ' + oneFam + ' IITs list a single family. ' +
    'The ' + D.private.length + ' private universities whose own pages we could read list a <b>median of ' + privMed + ' programmes, up to ' + privMax + '</b>' + (D.tnea ? ', and in Tamil Nadu counselling <b>' + D.tnea.counts.aids + ' of ' + D.tnea.total + ' colleges</b> offer an AI or Data Science programme and <b>' + D.tnea.counts.biz + '</b> offer Computer Science and Business Systems' : '') + '.</p></div>' +
    heat + topTbl +
    '<h2>The reasons</h2><div class="cs-grid2">' + D.why_leaders.map(function (w, n) { return '<div class="cs-card"><h3 style="margin-top:0"><span class="cs-pill or">' + (n + 1) + '</span> ' + esc(w[0]) + '</h3><p style="margin:0">' + esc(w[1]) + '</p></div>'; }).join('') + '</div>' +
    '<div class="cs-card cs-note"><b>What this means for you.</b> Do not read "the IITs do not offer it" as "it is not good", or "the private college offers it" as "it is better". Ask who teaches the branch, what the labs are, and what the last three batches did. Then compare it with the same college\'s CSE.</div>';

  // ---- CHOOSE AND STUDY AHEAD ----------------------------------------------------------------------------------------------------------------------
  var QZ = [
    { q: 'What do you enjoy most?', o: [['Building apps and systems that work', { core: 3, it: 2 }], ['Finding patterns in data and teaching computers to learn', { aids: 3, mnc: 1 }], ['Breaking systems to learn how to protect them', { cyber: 3, core: 1 }], ['Understanding people, money and business, with technology', { biz: 3, it: 1 }], ['Mathematics and proofs', { mnc: 3, aids: 1 }], ['Devices, robots, sensors or games', { hybrid: 3 }]] },
    { q: 'How do you feel about advanced mathematics (probability, linear algebra, proofs)?', o: [['I enjoy it', { mnc: 2, aids: 2, core: 1 }], ['I can manage it', { core: 1, it: 1, cyber: 1, biz: 1 }], ['I would prefer less of it', { it: 2, biz: 1 }]] },
    { q: 'Do you want to keep options open and decide the specialisation later?', o: [['Yes, I am not sure yet', { core: 3, it: 1 }], ['No, I know my direction', { aids: 1, cyber: 1, hybrid: 1, biz: 1 }]] },
    { q: 'Where do you see yourself in ten years?', o: [['Building software products', { core: 2, it: 2 }], ['In research, a PhD or a quant or AI lab', { mnc: 2, aids: 2, core: 1 }], ['In product, consulting or management', { biz: 3, it: 1 }], ['In security, devices or another specialist field', { cyber: 2, hybrid: 2 }]] }
  ];
  var quiz = '<div class="cs-card cs-quiz"><h2>Which branch should I look at first?</h2><p class="cs-sub">Four questions. It gives two branches to read about, not a decision: compare the college and the department before you choose.</p><form id="qz">' +
    QZ.map(function (q, n) { return '<fieldset><legend>' + (n + 1) + '. ' + esc(q.q) + '</legend>' + q.o.map(function (o, k) { return '<label><input type="radio" name="q' + n + '" value="' + k + '" required> ' + esc(o[0]) + '</label>'; }).join('') + '</fieldset>'; }).join('') +
    '<button class="cs-btn" type="submit">Show my two branches</button> <button class="cs-btn ghost" type="reset" id="qz-reset">Start again</button></form><div id="qz-out" aria-live="polite"></div></div>';
  $('#p-choose').innerHTML =
    '<h2>Choose, then plan the years after</h2>' + quiz +
    '<div class="cs-card"><h2>When to consider each branch</h2><div class="cs-tbl-wrap"><table class="cs-tbl"><thead><tr><th>If this is you</th><th>Consider</th></tr></thead><tbody>' + D.when.map(function (w) { return '<tr><td><b>' + esc(w[0]) + '</b></td><td>' + esc(w[1]) + '</td></tr>'; }).join('') + '</tbody></table></div></div>' +
    '<h2>Higher studies</h2><div class="cs-grid2">' + D.higher.map(function (h) { return '<div class="cs-card"><h3 style="margin-top:0">' + esc(h[0]) + '</h3><p style="margin:0">' + esc(h[1]) + '</p></div>'; }).join('') + '</div>' +
    '<div class="cs-card"><h2>Ask every college these eight questions (and get the answers in writing)</h2><ol class="cs-list">' + D.ask.map(function (a) { return '<li>' + esc(a) + '</li>'; }).join('') + '</ol></div>' +
    '<div class="cs-card cs-faq"><h2>Common questions</h2>' + D.faq.map(function (f) { return '<details><summary>' + esc(f[0]) + '</summary><p>' + esc(f[1]) + '</p></details>'; }).join('') + '</div>';
  $('#qz').addEventListener('submit', function (e) {
    e.preventDefault();
    var sc = {};
    QZ.forEach(function (q, n) { var v = $('input[name=q' + n + ']:checked', $('#qz')); if (v) { var w = q.o[+v.value][1]; Object.keys(w).forEach(function (k) { sc[k] = (sc[k] || 0) + w[k]; }); } });
    var ranked = Object.keys(sc).sort(function (a, b) { return sc[b] - sc[a]; }).slice(0, 2);
    $('#qz-out').innerHTML = '<div class="cs-result"><h3 style="margin-top:0">Read these two first</h3>' + ranked.map(function (k) { var b = BR[k]; return '<p><b class="cs-f-' + k + '" style="color:var(--fc)">' + esc(b.short) + ': ' + esc(b.tagline) + '</b><br>' + esc(b.caution) + '</p>'; }).join('') +
      '<p class="cs-small">Core CSE is always a safe comparison point. Next: <a href="#" data-go="colleges">see which colleges offer these branches</a>.</p></div>';
  });
  $('#qz-reset').addEventListener('click', function () { $('#qz-out').innerHTML = ''; });

  // ---- AI AND FUTURE -----------------------------------------------------------------------------------------------------------------------------
  var jobs = function (flt) {
    return D.future_jobs.filter(function (j) { return !flt || j.best.indexOf(flt) >= 0; }).map(function (j) {
      return '<div class="cs-job"><div><b>' + esc(j.role) + '</b></div><div><p>' + esc(j.what) + '</p><p class="cs-small">Skills: ' + esc(j.skills) + '</p></div><div>' + j.best.map(function (b) { return '<span class="cs-pill">' + esc(b) + '</span>'; }).join('') + '</div></div>';
    }).join('') || '<div class="cs-empty">No role listed for this branch.</div>';
  };
  $('#p-ai').innerHTML =
    '<h2>What AI changes in computing careers</h2><p class="cs-sub">A qualitative view. No job-count or salary prediction is made: nobody can verify one.</p>' +
    '<div class="cs-grid3">' + D.ai_tasks.map(function (t) { return '<div class="cs-task ' + t.tone + '"><h3>' + esc(t.label) + '</h3>' + li(t.items) + '</div>'; }).join('') + '</div>' +
    '<div class="cs-card cs-note"><b>The honest summary.</b> Routine coding is getting faster and cheaper, so the entry bar is rising. Judgement, system design, data quality, security and the ability to build with AI tools are rising in value. Choose a college where you will build real projects, not only attend lectures.</div>' +
    '<div class="cs-card"><h2>Futuristic jobs and the branches that lead to them</h2><div class="cs-filters"><label class="cs-small" for="jf">Show roles that suit</label><select id="jf"><option value="">All branches</option>' + D.branches.map(function (b) { return '<option value="' + esc(b.short) + '">' + esc(b.short) + '</option>'; }).join('') + '</select></div><div id="jobs">' + jobs('') + '</div></div>' +
    '<h2>Skills to build</h2><div class="cs-grid2"><div class="cs-card"><h3 style="margin-top:0">For every branch</h3><ul class="cs-list">' + D.skills.universal.map(function (s) { return '<li><b>' + esc(s[0]) + '.</b> ' + esc(s[1]) + '</li>'; }).join('') + '</ul></div>' +
    '<div class="cs-card"><h3 style="margin-top:0">Branch by branch</h3><ul class="cs-list">' + D.skills.by_branch.map(function (s) { return '<li><b>' + esc(s[0]) + ':</b> ' + esc(s[1]) + '</li>'; }).join('') + '</ul></div></div>' +
    '<h2>Year by year</h2><div class="cs-roadmap">' + D.skills.years.map(function (y) { return '<div><b>' + esc(y[0]) + '</b>' + esc(y[1]) + '</div>'; }).join('') + '</div>';
  $('#jf').addEventListener('change', function () { $('#jobs').innerHTML = jobs(this.value); });

  // ---- sources and start tab ---------------------------------------------------------------------------------------------------------------------
  $('#sources').innerHTML = D.sources.map(function (s) { return '<li>' + esc(s) + '</li>'; }).join('');
  var h = (location.hash || '').replace('#', '');
  if (h && $('#p-' + h)) show(h, false);
})();
