/* Exam roadmap engine — interactive roadmap, dashboard and weekly planner, driven by a JSON config (#rm-cfg).
   Used by the UCEED 2027 and Law 2027 pages. Prototype storage: this browser only (localStorage); a production version
   stores the same objects per student in the membership database behind login. User text is written with textContent. */
(function () {
  'use strict';
  var CFG = JSON.parse(document.getElementById('rm-cfg').textContent);
  var OFFICIAL = CFG.official, PHASES = CFG.phases, LEVEL_W = CFG.weights, TYPES = CFG.types;
  var TOPIC = PHASES.filter(function (p) { return p.topic; })[0] || PHASES.slice(1, 2)[0], REVP = PHASES.filter(function (p) { return p.rev; })[0] || PHASES.slice(5, 6)[0];
  var DAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];

  // ---- storage ------------------------------------------------------------------------------------
  var KEY = CFG.key, mem = null, persistOk = true;
  function blank() { return { profile: { name: '', start: '', hours: 8, level: 'intermediate', target: '' }, tasks: {}, planner: [], mocks: [], drawings: [], sample: false, notes: {} }; }
  function load() {
    try { var raw = localStorage.getItem(KEY); if (raw) return Object.assign(blank(), JSON.parse(raw)); } catch (e) { persistOk = false; }
    return mem || blank();
  }
  var S = load();
  function save() { mem = S; try { localStorage.setItem(KEY, JSON.stringify(S)); } catch (e) { persistOk = false; } }

  // ---- helpers ------------------------------------------------------------------------------------
  function $(s, r) { return (r || document).querySelector(s); }
  function $$(s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); }
  function el(tag, cls, text) { var n = document.createElement(tag); if (cls) n.className = cls; if (text != null) n.textContent = text; return n; }
  function iso(d) { return d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0'); }
  function parse(s) { var p = (s || '').split('-'); return p.length === 3 ? new Date(+p[0], +p[1] - 1, +p[2]) : null; }
  function addDays(d, n) { var x = new Date(d); x.setDate(x.getDate() + n); return x; }
  function monday(d) { var x = new Date(d); x.setHours(0, 0, 0, 0); x.setDate(x.getDate() - ((x.getDay() + 6) % 7)); return x; }
  function fmt(d) { return d.toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' }); }
  function today() { var d = new Date(); d.setHours(0, 0, 0, 0); return d; }
  function uid() { return 'x' + Date.now().toString(36) + Math.random().toString(36).slice(2, 6); }
  function toast(m) { var t = $('#uc-toast'); t.textContent = m; t.classList.add('show'); clearTimeout(t._t); t._t = setTimeout(function () { t.classList.remove('show'); }, 2600); }
  function examDate() {
    var t = (CFG.targets || []).filter(function (x) { return x.id === S.profile.target; })[0] || (CFG.targets || [])[0];
    return t ? t.date : CFG.exam;
  }
  function targetOfficial() { var t = (CFG.targets || []).filter(function (x) { return x.id === S.profile.target; })[0] || (CFG.targets || [])[0]; return t ? t.official : true; }
  function taskId(p, i) { return p.id + 't' + i; }
  function status(id) { return S.tasks[id] || 'todo'; }
  var NEXT = { todo: 'doing', doing: 'done', done: 'todo' };
  var LABEL = { todo: 'Not started', doing: 'In progress', done: 'Completed' };

  // ---- roadmap schedule (adjusts to start date and level) -------------------------------------------
  function schedule() {
    var start = parse(S.profile.start) || today(), exam = parse(examDate()), out = [];
    var days = Math.round((exam - start) / 86400000), w = LEVEL_W[S.profile.level] || LEVEL_W.intermediate;
    if (days < 14) { PHASES.forEach(function (p, i) { out.push(null); }); return { rows: out, days: days }; }
    var cur = start;
    for (var i = 0; i < 6; i++) {
      var len = Math.max(2, Math.round(days * w[i])), end = i === 5 ? exam : addDays(cur, len - 1);
      out.push([cur, end]); cur = addDays(end, 1);
    }
    out.push('after');
    return { rows: out, days: days };
  }

  function phaseProgress(p) {
    var done = 0; p.tasks.forEach(function (_, i) { if (status(taskId(p, i)) === 'done') done++; });
    return { done: done, total: p.tasks.length, pct: Math.round(100 * done / p.tasks.length) };
  }
  function overall() {
    var d = 0, t = 0; PHASES.forEach(function (p) { var q = phaseProgress(p); d += q.done; t += q.total; });
    return { done: d, total: t, pct: t ? Math.round(100 * d / t) : 0 };
  }
  function currentPhase() { for (var i = 0; i < PHASES.length; i++) if (phaseProgress(PHASES[i]).pct < 100) return i; return PHASES.length - 1; }

  // ---- render: roadmap ------------------------------------------------------------------------------
  function renderRoadmap() {
    var host = $('#uc-road'); host.textContent = '';
    var sch = schedule(), cur = currentPhase();
    $('#uc-sched-note').textContent = sch.days >= 14
      ? 'Your plan runs ' + fmt(parse(S.profile.start) || today()) + ' → ' + fmt(parse(examDate())) + ' (' + sch.days + ' days to the exam). Phase dates adjust to your start date and level.' + (targetOfficial() ? '' : ' Note: the next exam date is not announced — this is a planning assumption.')
      : 'Fewer than 14 days remain before ' + fmt(parse(examDate())) + ', so a phase-by-phase schedule is not meaningful. Use the weekly planner to prioritise mock tests, error review and the official admit-card instructions.';
    PHASES.forEach(function (p, pi) {
      var q = phaseProgress(p), d = el('details', 'uc-phase' + (pi === cur ? ' now' : '')); if (pi === cur) d.open = true;
      var sm = el('summary'), ring = el('div', 'uc-ring'); ring.style.setProperty('--p', q.pct); ring.setAttribute('data-t', q.pct + '%'); ring.setAttribute('role', 'img'); ring.setAttribute('aria-label', 'Phase ' + (pi + 1) + ' ' + q.pct + ' percent complete');
      var mid = el('div'); mid.appendChild(el('h3', null, 'Phase ' + (pi + 1) + ' · ' + p.t));
      var r = sch.rows[pi], when = p.after ? CFG.afterText : (r ? fmt(r[0]) + ' → ' + fmt(r[1]) : 'Dates not scheduled (exam is under 2 weeks away)');
      mid.appendChild(el('div', 'when', when + ' · ' + q.done + '/' + q.total + ' tasks'));
      sm.appendChild(ring); sm.appendChild(mid); sm.appendChild(el('span', 'uc-tag plan tag', pi === cur ? 'Current' : (q.pct === 100 ? 'Done' : 'Planned')));
      d.appendChild(sm);
      var body = el('div', 'body');
      p.tasks.forEach(function (txt, i) {
        var id = taskId(p, i), s = status(id), row = el('div', 'uc-task' + (s === 'done' ? ' done' : ''));
        row.appendChild(el('span', 't', txt));
        var b = el('button', 'uc-st', LABEL[s]); b.type = 'button'; b.setAttribute('data-s', s); b.setAttribute('aria-label', txt + ': ' + LABEL[s] + '. Click to change.');
        b.addEventListener('click', function () { S.tasks[id] = NEXT[status(id)]; save(); renderAll(); });
        row.appendChild(b); body.appendChild(row);
      });
      if (p.note) body.appendChild(el('div', 'uc-deliv', p.note));
      body.appendChild(el('div', 'uc-deliv', 'Deliverable: ' + p.d));
      d.appendChild(body); host.appendChild(d);
    });
  }

  // ---- render: dashboard ----------------------------------------------------------------------------
  function weekKey(d) { return iso(monday(d)); }
  function plannedThisWeek() { var wk = weekKey(today()); return S.planner.filter(function (x) { return x.week === wk; }); }
  function render() { renderDashboard(); }
  function renderDashboard() {
    var o = overall(), cur = currentPhase(), wkTasks = plannedThisWeek(), mins = 0;
    wkTasks.forEach(function (x) { if (x.done && x.type !== 'off') mins += x.min; });
    var wkStart = monday(today()), dMin = 0;
    S.drawings.forEach(function (x) { var d = parse(x.date); if (d && d >= wkStart && d < addDays(wkStart, 7)) dMin += x.min; });
    var target = Math.round((+S.profile.hours || 0) * 60), actual = mins + dMin;
    $('#d-name').textContent = S.profile.name || 'Your name';
    $('#d-start').textContent = S.profile.start ? fmt(parse(S.profile.start)) : 'Not set';
    $('#d-phase').textContent = 'Phase ' + (cur + 1) + ' · ' + PHASES[cur].t;
    $('#d-pct').textContent = o.pct + '%'; $('#d-bar').style.width = o.pct + '%';
    $('#d-done').textContent = o.done + ' of ' + o.total + ' tasks completed';
    $('#d-week').textContent = (actual / 60).toFixed(1) + ' h of ' + (target / 60).toFixed(1) + ' h';
    $('#d-weekbar').style.width = target ? Math.min(100, Math.round(100 * actual / target)) + '%' : '0%';
    $('#d-sample').hidden = !S.sample;

    // next best action
    var na = $('#d-next'); na.textContent = '';
    var found = null;
    for (var pi = cur; pi < PHASES.length && !found; pi++) PHASES[pi].tasks.forEach(function (t, i) { if (!found && status(taskId(PHASES[pi], i)) !== 'done') found = { p: pi, i: i, t: t, s: status(taskId(PHASES[pi], i)) }; });
    if (found) {
      na.appendChild(el('p', null, 'Phase ' + (found.p + 1) + ' · ' + PHASES[found.p].t)); na.appendChild(el('h3', null, found.t));
      var b = el('button', 'uc-btn o sm', found.s === 'doing' ? 'Mark completed' : 'Start this task'); b.type = 'button';
      b.addEventListener('click', function () { S.tasks[taskId(PHASES[found.p], found.i)] = found.s === 'doing' ? 'done' : 'doing'; save(); renderAll(); toast('Updated'); });
      na.appendChild(b);
    } else na.appendChild(el('h3', null, 'Every roadmap task is complete 🎉 — review your institute comparison and application tracker.'));

    // topic progress (phase 2)
    var tp = $('#d-topics'); tp.textContent = '';
    TOPIC.tasks.forEach(function (t, i) {
      var s = status(taskId(TOPIC, i)), v = s === 'done' ? 100 : s === 'doing' ? 50 : 0, row = el('div'); row.style.margin = '8px 0';
      row.appendChild(el('div', null, t + ' — ' + LABEL[s])); var bar = el('div', 'uc-bar'), fill = el('i'); fill.style.width = v + '%'; bar.appendChild(fill); row.appendChild(bar); tp.appendChild(row);
    });

    // drawing tracker
    var dl = $('#d-draw'); dl.textContent = '';
    var recent = S.drawings.slice().sort(function (a, b) { return a.date < b.date ? 1 : -1; }).slice(0, 5);
    if (!recent.length) dl.appendChild(el('div', 'uc-empty', 'No ' + CFG.log.noun + ' logged yet.'));
    recent.forEach(function (x) { dl.appendChild(el('div', 'uc-task', fmt(parse(x.date)) + ' · ' + x.min + ' min · ' + (x.subject || CFG.log.name))); });
    $('#d-draw-wk').textContent = dMin + ' min this week';

    // mocks
    var mh = $('#d-mocks'); mh.textContent = '';
    var mocks = S.mocks.slice().sort(function (a, b) { return a.date < b.date ? -1 : 1; });
    if (!mocks.length) mh.appendChild(el('div', 'uc-empty', 'No mock tests recorded yet. Add your first one below.'));
    else {
      var sp = el('div', 'uc-spark'); sp.setAttribute('role', 'img'); sp.setAttribute('aria-label', 'Score percentage across mock tests');
      mocks.slice(-10).forEach(function (m) { var i = el('i'); var pct = Math.round(100 * m.a / CFG.mock.a.max); i.style.height = Math.max(6, pct * 0.9) + 'px'; i.setAttribute('data-v', pct + '%'); i.title = m.date + ': ' + m.a + '/' + CFG.mock.a.max; sp.appendChild(i); });
      mh.appendChild(sp);
      var t = el('table', 'uc-table'), hd = el('tr'); ['Date', CFG.mock.a.label].concat(CFG.mock.b ? [CFG.mock.b.label] : [], ['Accuracy', 'Unfinished', 'Weak topic']).forEach(function (h) { hd.appendChild(el('th', null, h)); }); t.appendChild(hd);
      mocks.slice(-6).reverse().forEach(function (m) { var r = el('tr'); [fmt(parse(m.date)), m.a].concat(CFG.mock.b ? [m.b === '' || m.b == null ? '—' : m.b] : [], [m.acc === '' || m.acc == null ? '—' : m.acc + '%', m.unf === '' || m.unf == null ? '—' : m.unf, m.weak || '—']).forEach(function (c) { r.appendChild(el('td', null, String(c))); }); t.appendChild(r); });
      var w = el('div', 'uc-scroll'); w.appendChild(t); mh.appendChild(w);
    }

    // weak-topic alerts
    var al = $('#d-alerts'); al.textContent = ''; var cnt = {};
    S.mocks.forEach(function (m) { if (m.weak) cnt[m.weak.toLowerCase()] = (cnt[m.weak.toLowerCase()] || 0) + 1; });
    Object.keys(cnt).forEach(function (k) { if (cnt[k] >= 2) al.appendChild(el('div', 'uc-alert', '⚠ “' + k + '” was marked weak in ' + cnt[k] + ' mock tests — schedule focused practice.')); });
    if (cur >= 3) TOPIC.tasks.forEach(function (t, i) { if (status(taskId(TOPIC, i)) === 'todo') al.appendChild(el('div', 'uc-alert', '⚠ Core topic not started: ' + t)); });
    if (!al.firstChild) al.appendChild(el('div', 'uc-empty', 'No weak-topic alerts right now.'));

    // upcoming tasks and deadlines
    var up = $('#d-up'); up.textContent = ''; var n = 0;
    PHASES.forEach(function (p, pi) { p.tasks.forEach(function (t, i) { if (n < 4 && pi >= cur && status(taskId(p, i)) !== 'done') { up.appendChild(el('div', 'uc-task', t)); n++; } }); });
    OFFICIAL.forEach(function (o2) { var d = parse(o2[1]); if (d >= today()) { var days = Math.round((d - today()) / 86400000); up.appendChild(el('div', 'uc-task', '📌 ' + o2[0] + ' — ' + o2[2] + ' (' + days + ' days)')); } });

    // revision checklist
    var rv = $('#d-rev'); rv.textContent = '';
    REVP.tasks.forEach(function (t, i) { var id = taskId(REVP, i), s = status(id), r = el('div', 'uc-task' + (s === 'done' ? ' done' : '')); r.appendChild(el('span', 't', t)); var b = el('button', 'uc-st', LABEL[s]); b.type = 'button'; b.setAttribute('data-s', s); b.addEventListener('click', function () { S.tasks[id] = NEXT[status(id)]; save(); renderAll(); }); r.appendChild(b); rv.appendChild(r); });

    // mentor feedback
    $('#d-feedback').textContent = S.notes.feedback || 'No mentor feedback yet. In the live Mentorship Portal this card shows your mentor’s latest note and next action.';
  }

  // ---- planner -------------------------------------------------------------------------------------
  var weekOffset = 0;
  function renderPlanner() {
    var host = $('#uc-week'); host.textContent = '';
    var ws = addDays(monday(today()), weekOffset * 7), wk = iso(ws), tIso = iso(today());
    $('#pl-range').textContent = fmt(ws) + ' – ' + fmt(addDays(ws, 6));
    var items = S.planner.filter(function (x) { return x.week === wk; }), planned = 0, done = 0, cnt = 0, dn = 0;
    items.forEach(function (x) { if (x.type !== 'off') { planned += x.min; cnt++; if (x.done) { done += x.min; dn++; } } });
    $('#pl-pct').textContent = (planned ? Math.round(100 * done / planned) : 0) + '% of planned time done (' + dn + '/' + cnt + ' tasks, ' + (done / 60).toFixed(1) + ' of ' + (planned / 60).toFixed(1) + ' h)';
    DAYS.forEach(function (dn2, di) {
      var date = addDays(ws, di), col = el('div', 'uc-day' + (iso(date) === tIso ? ' today' : '')); col.appendChild(el('h4', null, dn2 + ' ' + date.getDate()));
      var list = items.filter(function (x) { return x.day === di; });
      if (!list.length) col.appendChild(el('div', 'uc-fine', 'Free'));
      list.forEach(function (x) {
        var t = el('div', 'uc-pt ' + x.type + (x.done ? ' done' : '')); t.appendChild(el('div', null, x.title + (x.type === 'off' ? '' : ' · ' + x.min + ' min')));
        t.appendChild(el('div', 'uc-fine', TYPES[x.type]));
        var a = el('div', 'acts');
        function mini(label, fn, aria) { var b = el('button', 'uc-mini', label); b.type = 'button'; b.setAttribute('aria-label', aria); b.addEventListener('click', fn); a.appendChild(b); }
        if (x.type !== 'off') mini(x.done ? 'Undo' : '✓ Done', function () { x.done = !x.done; save(); renderAll(); }, (x.done ? 'Mark not done: ' : 'Mark done: ') + x.title);
        mini('Edit', function () { var nt = prompt('Task title', x.title); if (nt === null) return; var nm = x.type === 'off' ? 0 : parseInt(prompt('Minutes', x.min), 10); x.title = (nt || x.title).slice(0, 80); if (!isNaN(nm)) x.min = Math.max(0, Math.min(600, nm)); save(); renderAll(); }, 'Edit ' + x.title);
        if (!x.done && x.type !== 'off') mini('→ Next day', function () { if (x.day < 6) x.day++; else { x.day = 0; x.week = iso(addDays(parse(x.week), 7)); } save(); renderAll(); toast('Moved'); }, 'Move to next day: ' + x.title);
        mini('✕', function () { S.planner = S.planner.filter(function (y) { return y !== x; }); save(); renderAll(); }, 'Delete ' + x.title);
        t.appendChild(a); col.appendChild(t);
      });
      host.appendChild(col);
    });
  }

  function starterWeek() {
    var ws = addDays(monday(today()), weekOffset * 7), wk = iso(ws), total = Math.max(2, +S.profile.hours || 8) * 60;
    var mixes = CFG.mixes;
    var offDays = S.planner.filter(function (x) { return x.week === wk && x.type === 'off'; }).map(function (x) { return x.day; });
    var free = [0, 1, 2, 3, 4, 5, 6].filter(function (d) { return offDays.indexOf(d) < 0; });
    if (!free.length) { toast('Every day is marked off'); return; }
    if (S.planner.some(function (x) { return x.week === wk && x.type !== 'off'; }) && !confirm('Replace the tasks in this week with a suggested starter week? (School exam / holiday markers are kept.)')) return;
    S.planner = S.planner.filter(function (x) { return x.week !== wk || x.type === 'off'; });
    (mixes[S.profile.level] || mixes.intermediate).forEach(function (m, i) {
      var min = Math.max(15, Math.round(total * m[1] / 5) * 5), day = free[(i * 2) % free.length];
      S.planner.push({ id: uid(), week: wk, day: day, type: m[0], title: TYPES[m[0]], min: min, done: false });
    });
    save(); renderAll(); toast('Starter week created from ' + (total / 60) + ' h/week — edit it to fit your school schedule');
  }

  function summary() {
    var wk = weekKey(addDays(today(), weekOffset * 7)), items = S.planner.filter(function (x) { return x.week === wk && x.type !== 'off'; });
    var done = items.filter(function (x) { return x.done; }), left = items.filter(function (x) { return !x.done; });
    var mins = done.reduce(function (a, x) { return a + x.min; }, 0), name = S.profile.name || 'Student';
    var lines = [CFG.examName + ' — weekly summary for ' + name, 'Week of ' + fmt(parse(wk)), '', 'Completed (' + done.length + ', ' + (mins / 60).toFixed(1) + ' h):'];
    done.forEach(function (x) { lines.push(' • ' + x.title + ' (' + TYPES[x.type] + ', ' + x.min + ' min)'); }); if (!done.length) lines.push(' • nothing marked complete yet');
    lines.push('', 'Still pending (' + left.length + '):'); left.forEach(function (x) { lines.push(' • ' + x.title + ' (' + TYPES[x.type] + ', ' + x.min + ' min)'); }); if (!left.length) lines.push(' • none');
    var o = overall(); lines.push('', 'Roadmap completion: ' + o.pct + '% (' + o.done + '/' + o.total + ' tasks). Current phase: ' + PHASES[currentPhase()].t + '.');
    $('#pl-summary').value = lines.join('\n'); $('#pl-summary').hidden = false; $('#pl-copy').hidden = false;
  }

  // ---- sample data / reset ---------------------------------------------------------------------------
  function loadSample() {
    var s = blank(), t = today(), wk = weekKey(t);
    s.sample = true; s.profile = { name: 'Sample Student', start: iso(addDays(t, -42)), hours: 10, level: 'intermediate', target: S.profile.target || '' };
    PHASES[0].tasks.forEach(function (_, i) { s.tasks[taskId(PHASES[0], i)] = 'done'; });
    TOPIC.tasks.forEach(function (_, i) { s.tasks[taskId(TOPIC, i)] = i < 4 ? 'done' : (i < 6 ? 'doing' : 'todo'); });
    s.tasks[taskId(PHASES[2], 0)] = 'done'; s.tasks[taskId(PHASES[2], 1)] = 'doing';
    var sm = CFG.sample;
    s.mocks = sm.mocks.map(function (m) { var o = { date: iso(addDays(t, -m.ago)), a: m.a, acc: m.acc, unf: m.unf, weak: m.weak }; if (m.b != null) o.b = m.b; return o; });
    s.drawings = sm.logs.map(function (x) { return { date: iso(addDays(t, -x.ago)), min: x.min, subject: x.subject }; });
    s.planner = sm.planner.map(function (x) { return { id: uid(), week: wk, day: x[0], type: x[1], title: x[2], min: x[3], done: x[4] }; });
    s.notes.feedback = sm.feedback;
    S = s; save(); renderAll(); toast('Sample data loaded — clearly marked as demo');
  }

  function renderAll() { renderRoadmap(); renderDashboard(); renderPlanner(); renderInstitutes(); }

  // ---- institutes: personal comparison matrix (ratings stay in this browser) ------------------------
  function renderInstitutes() {
    $$('.uc-inst').forEach(function (row) {
      var id = row.getAttribute('data-id'), v = (S.notes.inst || {})[id] || {};
      $$('input,select', row).forEach(function (f) { var k = f.name; if (document.activeElement !== f) f.value = v[k] || ''; });
    });
  }

  function updateCountdown() {
    var t = (CFG.targets || []).filter(function (x) { return x.id === S.profile.target; })[0] || (CFG.targets || [])[0];
    var d = Math.round((parse(examDate()) - today()) / 86400000), name = t ? t.label.split(' — ')[0] : CFG.examName;
    $('#cd-days').textContent = d > 0 ? String(d) : (d === 0 ? 'Today' : 'Held');
    $('#cd-label').textContent = d > 0 ? 'days to ' + name + ' (' + fmt(parse(examDate())) + ')' + (targetOfficial() ? '' : ' — assumed date') : (d === 0 ? name + ' is today' : name + ' has taken place');
    var rc = Math.round((parse(CFG.regClose) - today()) / 86400000);
    $('#cd-reg').textContent = rc >= 0 ? 'Registration closes in ' + rc + ' day' + (rc === 1 ? '' : 's') + ' — ' + CFG.regText : 'Registration closed on ' + CFG.regText + ' — ' + CFG.regNote + '.';
  }

  // ---- wire up ---------------------------------------------------------------------------------------
  function init() {
    $('#pf-name').value = S.profile.name; $('#pf-start').value = S.profile.start; $('#pf-hours').value = S.profile.hours; $('#pf-level').value = S.profile.level;
    if ($('#pf-target')) $('#pf-target').value = S.profile.target || CFG.targets[0].id;
    ['pf-name', 'pf-start', 'pf-hours', 'pf-level'].concat($('#pf-target') ? ['pf-target'] : []).forEach(function (id) {
      $('#' + id).addEventListener('change', function () {
        S.profile = { name: $('#pf-name').value.slice(0, 60), start: $('#pf-start').value, hours: Math.max(1, Math.min(60, +$('#pf-hours').value || 8)), level: $('#pf-level').value, target: $('#pf-target') ? $('#pf-target').value : '' }; save(); renderAll(); updateCountdown();
      });
    });
    $('#pf-name').addEventListener('input', function () { S.profile.name = this.value.slice(0, 60); save(); $('#d-name').textContent = S.profile.name || 'Your name'; });
    $('#btn-sample').addEventListener('click', loadSample);
    $('#btn-reset').addEventListener('click', function () { if (confirm('Clear all roadmap, planner and tracker data stored in this browser?')) { S = blank(); save(); $('#pf-name').value = ''; $('#pf-start').value = ''; $('#pf-hours').value = 8; $('#pf-level').value = 'intermediate'; if ($('#pf-target')) $('#pf-target').value = CFG.targets[0].id; renderAll(); updateCountdown(); toast('Cleared'); } });
    $('#pl-prev').addEventListener('click', function () { weekOffset--; renderPlanner(); });
    $('#pl-next').addEventListener('click', function () { weekOffset++; renderPlanner(); });
    $('#pl-this').addEventListener('click', function () { weekOffset = 0; renderPlanner(); });
    $('#pl-starter').addEventListener('click', starterWeek);
    $('#pl-summary-btn').addEventListener('click', summary);
    $('#pl-copy').addEventListener('click', function () { var t = $('#pl-summary'); t.select(); try { document.execCommand('copy'); toast('Summary copied'); } catch (e) { toast('Select the text and copy'); } });
    $('#pl-resched').addEventListener('click', function () {
      var wk = weekKey(today()), td = (today().getDay() + 6) % 7, n = 0;
      S.planner.forEach(function (x) { if (x.week === wk && !x.done && x.type !== 'off' && x.day < td) { x.day = td; n++; } });
      if (td === 6) S.planner.forEach(function (x) { if (x.week === wk && !x.done && x.type !== 'off' && x.day === 6) { x.week = iso(addDays(parse(wk), 7)); x.day = 0; n++; } });
      save(); renderAll(); toast(n ? n + ' unfinished task(s) rescheduled' : 'Nothing to reschedule');
    });
    $('#pl-form').addEventListener('submit', function (e) {
      e.preventDefault(); var f = e.target, E = f.elements, title = E.title.value.trim().slice(0, 80), type = E.type.value, min = parseInt(E.minutes.value, 10) || 0;
      if (!title) { E.title.focus(); return; }
      S.planner.push({ id: uid(), week: iso(addDays(monday(today()), weekOffset * 7)), day: +E.day.value, type: type, title: title, min: type === 'off' ? 0 : Math.max(5, Math.min(600, min || 30)), done: false });
      save(); E.title.value = ''; renderAll();
    });
    $('#mock-form').addEventListener('submit', function (e) {
      e.preventDefault(); var f = e.target, E = f.elements, a = parseFloat(E.a.value);
      if (isNaN(a) || a < -100 || a > CFG.mock.a.max) { toast('Score must be between -100 and ' + CFG.mock.a.max); return; }
      S.mocks.push({ date: E.date.value || iso(today()), a: a, b: !E.b || E.b.value === '' ? '' : Math.max(0, Math.min(CFG.mock.b.max, +E.b.value)), acc: E.acc.value === '' ? '' : Math.max(0, Math.min(100, +E.acc.value)), unf: E.unf.value === '' ? '' : Math.max(0, +E.unf.value), weak: E.weak.value.trim().slice(0, 40) });
      save(); f.reset(); renderAll(); toast('Mock test saved');
    });
    $('#draw-form').addEventListener('submit', function (e) {
      e.preventDefault(); var f = e.target, E = f.elements, m = parseInt(E.min.value, 10);
      if (!m || m < 5) { toast('Enter the minutes practised'); return; }
      S.drawings.push({ date: E.date.value || iso(today()), min: Math.min(600, m), subject: E.subject.value.trim().slice(0, 50) }); save(); f.reset(); renderAll();
    });
    $$('.uc-inst input,.uc-inst select').forEach(function (f) {
      f.addEventListener('change', function () { var id = f.closest('.uc-inst').getAttribute('data-id'); S.notes.inst = S.notes.inst || {}; S.notes.inst[id] = S.notes.inst[id] || {}; S.notes.inst[id][f.name] = f.value.slice(0, 120); save(); });
    });
    $('#lead-form').addEventListener('submit', function (e) {
      e.preventDefault(); var f = e.target, E = f.elements, msg = $('#lead-msg'); msg.className = 'uc-msg';
      if (!E.consent.checked) { msg.textContent = 'Please tick the consent box so we can contact you.'; msg.classList.add('err'); return; }
      var contact = E.contact.value.trim(), body = { name: E.name.value.trim(), contact: contact, email: /@/.test(contact) ? contact : '', phone: /@/.test(contact) ? '' : contact, class: E.cls.value, prep_status: E.prep.value, guidance: E.guidance.value, consent: true, page: CFG.page };
      if (!body.name || !contact) { msg.textContent = 'Please enter the student name and a contact.'; msg.classList.add('err'); return; }
      msg.textContent = 'Sending…';
      fetch('/api/leads?source=' + CFG.leadSource, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) })
        .then(function (r) { if (!r.ok) throw new Error(); msg.textContent = 'Thank you! Our team will contact you about your ' + CFG.examName + ' preparation plan.'; msg.classList.add('ok'); f.reset(); })
        .catch(function () { msg.textContent = 'Could not send right now — please email info@eduaakashaa.com or WhatsApp us.'; msg.classList.add('err'); });
    });
    updateCountdown();
    if (!persistOk) $('#uc-nostore').hidden = false;
    // sticky nav highlight
    var links = $$('.uc-nav a'), io = 'IntersectionObserver' in window ? new IntersectionObserver(function (es) { es.forEach(function (en) { if (en.isIntersecting) links.forEach(function (a) { a.classList.toggle('on', a.getAttribute('href') === '#' + en.target.id); }); }); }, { rootMargin: '-40% 0px -55% 0px' }) : null;
    if (io) links.forEach(function (a) { var s = $(a.getAttribute('href')); if (s) io.observe(s); });
    renderAll();
  }
  document.addEventListener('DOMContentLoaded', init);
})();
