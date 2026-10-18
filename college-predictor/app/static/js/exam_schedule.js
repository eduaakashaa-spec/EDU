/* /exam-schedule — one dataset, four views (Cards · Timeline/Gantt · By month · Calendar) sharing the same filters,
   plus application-status filtering (open now / closing / late-fee / opening soon / closed) and deadline milestones.
   All text is written with textContent. Dates are ISO strings; rows with no date are listed under "dates awaited".
   Application state is computed in the browser from today's date and each exam's milestones; an "Expected" date never
   makes an application show as open. */
(function () {
  'use strict';
  var DATA = JSON.parse(document.getElementById('xs-data').textContent);
  var RANGE_START = new Date(2026, 9, 1), RANGE_END = new Date(2027, 8, 30);   // Oct 2026 – Sep 2027
  var MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
  var S = { view: 'cards', cat: 'all', status: 'all', app: 'all', q: '', gmode: 'detail', dl: true, cal: null };
  var APP_TEXT = { open: 'Applications open', closing: 'Closing soon', late: 'Late-fee window', soon: 'Opening soon', later: 'Applications later', closed: 'Applications closed', awaited: 'Dates awaited' };

  function $(s, r) { return (r || document).querySelector(s); }
  function $$(s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); }
  function el(t, c, x) { var n = document.createElement(t); if (c) n.className = c; if (x != null) n.textContent = x; return n; }
  function pd(s) { var p = s.split('-'); return new Date(+p[0], +p[1] - 1, +p[2]); }
  function iso(d) { return d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0'); }
  function dayDiff(a, b) { return Math.round((b - a) / 86400000); }
  function fmtD(d) { return d.getDate() + ' ' + MONTHS[d.getMonth()].slice(0, 3) + ' ' + d.getFullYear(); }
  function today() { var d = new Date(); d.setHours(0, 0, 0, 0); return d; }
  function ms(x, k) { return (x.ms || []).filter(function (m) { return m.k === k && m.d; })[0] || null; }

  // ---- application status ------------------------------------------------------------------------------
  function appInfo(x) {
    if (!x.ms || !x.ms.length) return null;
    var t = today(), o = ms(x, 'open'), c = ms(x, 'close'), l = ms(x, 'late');
    var od = o && pd(o.d), cd = c && pd(c.d), ld = l && pd(l.d), exp = function (m) { return m && m.s === 'Expected'; };
    if (!o && !c) return { state: 'awaited', text: 'Application dates awaited' };
    if (cd && t > (ld || cd)) return { state: 'closed', text: 'Applications closed ' + fmtD(ld || cd) };
    if (cd && ld && t > cd && t <= ld) return { state: 'late', text: 'Late-fee window until ' + fmtD(ld), days: dayDiff(t, ld) };
    if (od && t < od) { var d = dayDiff(t, od); return { state: d <= 45 ? 'soon' : 'later', text: 'Opens ' + (exp(o) ? '(expected) ' : '') + fmtD(od), days: d }; }
    if (od && !exp(o) && (!cd || t <= cd)) {
      var dc = cd ? dayDiff(t, cd) : null, closing = dc !== null && dc <= 14 && !exp(c);
      return { state: closing ? 'closing' : 'open', text: cd ? 'Open — closes ' + (exp(c) ? '(expected) ' : '') + fmtD(cd) + (dc !== null && dc <= 30 && !exp(c) ? ' (' + dc + ' day' + (dc === 1 ? '' : 's') + ')' : '') : 'Open — closing date awaited', days: dc };
    }
    return { state: 'awaited', text: 'Application dates awaited' };
  }
  function appMatches(x) {
    if (S.app === 'all') return true;
    var i = appInfo(x); if (!i) return false;
    if (S.app === 'open') return i.state === 'open' || i.state === 'closing';
    return i.state === S.app;
  }

  function visible(skipApp) {
    var q = S.q.trim().toLowerCase();
    return DATA.filter(function (x) {
      return (S.cat === 'all' || x.cat === S.cat) && (S.status === 'all' || x.status === S.status) && (skipApp || appMatches(x)) &&
        (!q || (x.name + ' ' + x.badge + ' ' + x.catTitle + ' ' + x.desc).toLowerCase().indexOf(q) > -1);
    });
  }
  function rangeText(x) { return x.start === x.end ? fmtD(pd(x.start)) : fmtD(pd(x.start)) + ' – ' + fmtD(pd(x.end)); }
  function gcal(x, from, to, text) {
    var e = new Date(pd(to || x.end).getTime() + 86400000), z = function (d) { return iso(d).replace(/-/g, ''); };
    return 'https://calendar.google.com/calendar/render?action=TEMPLATE&text=' + encodeURIComponent(text || x.name) + '&dates=' + z(pd(from || x.start)) + '/' + z(e) + '&details=' + encodeURIComponent((text ? '' : x.when + ' (' + x.status + '). ') + 'Confirm on the official website.');
  }

  // ---- detail panel -------------------------------------------------------------------------------------
  function showDetail(x) {
    var p = $('#xs-detail'); p.textContent = ''; p.hidden = false;
    p.appendChild(el('h3', null, x.name));
    var meta = el('p', null, x.catTitle + ' · ' + x.when + (x.start ? ' · ' + rangeText(x) : '') + ' · '); meta.appendChild(el('span', 'xs-st ' + x.status, x.status)); p.appendChild(meta);
    p.appendChild(el('p', null, x.desc));
    var ai = appInfo(x); if (ai) { var b0 = el('span', 'xs-appbadge ' + ai.state, ai.text); p.appendChild(b0); }
    if (x.ms && x.ms.length) {
      var ul = el('ul', 'xs-dl');
      x.ms.forEach(function (m) { var li = el('li'); li.appendChild(el('span', 'xs-dl-k', m.icon + ' ' + m.label)); li.appendChild(el('span', 'xs-dl-d', m.d ? fmtD(pd(m.d)) : 'awaited')); li.appendChild(el('span', 'xs-st ' + m.s, m.s)); if (m.n) li.appendChild(el('em', null, m.n)); ul.appendChild(li); });
      p.appendChild(ul);
    }
    if (x.note) p.appendChild(el('span', 'xs-note', x.note));
    var a = el('div'); a.style.cssText = 'display:flex;gap:8px;flex-wrap:wrap;margin-top:10px;';
    if (x.start) {
      var l1 = el('a', 'xs-btn n', '📅 Add to calendar (.ics, with deadlines)'); l1.href = '/exam-schedule/' + x.id + '.ics'; a.appendChild(l1);
      var l2 = el('a', 'xs-btn g', 'Google Calendar'); l2.href = gcal(x); l2.target = '_blank'; l2.rel = 'noopener'; a.appendChild(l2);
    }
    var b = el('button', 'xs-sb', 'Show card'); b.type = 'button'; b.addEventListener('click', function () { setView('cards'); var c = $('#card-' + x.id); if (c) { c.scrollIntoView({ behavior: 'smooth', block: 'center' }); c.classList.add('hl'); setTimeout(function () { c.classList.remove('hl'); }, 1800); } });
    a.appendChild(b);
    var cl = el('button', 'xs-sb', 'Close'); cl.type = 'button'; cl.addEventListener('click', function () { p.hidden = true; }); a.appendChild(cl);
    p.appendChild(a); p.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }

  // ---- views ----------------------------------------------------------------------------------------------
  function renderCards(list) {
    var ids = {}; list.forEach(function (x) { ids[x.id] = 1; });
    $$('.xs-card').forEach(function (c) { c.hidden = !ids[c.getAttribute('data-id')]; });
    $$('.xs-cat').forEach(function (sec) {
      var n = $$('.xs-card', sec).filter(function (c) { return !c.hidden; }).length;
      sec.hidden = n === 0; $('.xs-cnt', sec).textContent = n + (n === 1 ? ' exam' : ' exams');
    });
  }
  function badges() {
    DATA.forEach(function (x) {
      var b = $('.xs-appbadge[data-app="' + x.id + '"]'); if (!b) return;
      var i = appInfo(x); b.className = 'xs-appbadge ' + (i ? i.state : ''); b.textContent = i ? (APP_TEXT[i.state] + ' · ' + i.text) : '';
    });
    var all = visible(true), cnt = { open: 0, closing: 0, late: 0, soon: 0, closed: 0 };
    all.forEach(function (x) { var i = appInfo(x); if (!i) return; if (i.state === 'open' || i.state === 'closing') cnt.open++; if (cnt[i.state] != null && i.state !== 'open') cnt[i.state]++; });
    $$('.xs-ct').forEach(function (n) { n.textContent = String(cnt[n.getAttribute('data-ct')] || 0); });
  }

  function renderGantt(list) {
    var host = $('#xg'); host.textContent = ''; host.className = S.gmode === 'cons' ? 'xg-cons' : '';
    var total = dayDiff(RANGE_START, RANGE_END) + 1, dated = list.filter(function (x) { return x.start; });
    var labels = el('div', 'xg-labels'), tracks = el('div', 'xg-tracks');
    labels.appendChild(el('div', 'xg-head', 'Exam / category'));
    var head = el('div', 'xg-head'); tracks.appendChild(head);
    var grid = el('div', 'xg-grid'); tracks.appendChild(grid);
    for (var m = 0; m < 12; m++) {
      var mst = new Date(2026, 9 + m, 1), me = new Date(2026, 10 + m, 0), w = (dayDiff(mst, me) + 1) / total * 100, cell = el('div', 'm', MONTHS[mst.getMonth()].slice(0, 3) + ' ' + String(mst.getFullYear()).slice(2));
      cell.style.width = w + '%'; head.appendChild(cell);
      var line = el('i'); line.style.left = (dayDiff(RANGE_START, mst) / total * 100) + '%'; grid.appendChild(line);
    }
    var t = today();
    if (t >= RANGE_START && t <= RANGE_END) { var tl = el('div', 'xg-today'); tl.style.left = ((dayDiff(RANGE_START, t) + 0.5) / total * 100) + '%'; grid.appendChild(tl); }
    function place(btn, x, aIso, bIso, cls, title, point) {
      var a = pd(aIso), b = pd(bIso); if (b < RANGE_START || a > RANGE_END) return false;
      if (a < RANGE_START) a = RANGE_START; if (b > RANGE_END) b = RANGE_END;
      btn.style.left = (dayDiff(RANGE_START, a) / total * 100) + '%';
      if (point) btn.style.marginLeft = '-1px'; else btn.style.width = ((dayDiff(a, b) + 1) / total * 100) + '%';
      btn.title = title; btn.setAttribute('aria-label', title); btn.addEventListener('click', function () { showDetail(x); }); return true;
    }
    function bar(x, row) {
      if (S.dl && S.gmode === 'detail' && x.ms) {                                   // application window, late-fee period, results
        var o = ms(x, 'open'), c = ms(x, 'close'), l = ms(x, 'late'), r = ms(x, 'result');
        if (o && c) { var ab = el('button', 'xg-bar appw ' + (o.s === 'Expected' || c.s === 'Expected' ? 'Expected' : 'Confirmed')); ab.type = 'button'; ab.style.setProperty('--c', '#1F8B5C'); if (place(ab, x, o.d, c.d, '', 'Applications: ' + fmtD(pd(o.d)) + ' – ' + fmtD(pd(c.d)) + ' (' + c.s + ')')) row.appendChild(ab); }
        if (c && l) { var lb = el('button', 'xg-bar late'); lb.type = 'button'; if (place(lb, x, c.d, l.d, '', 'Late-fee period until ' + fmtD(pd(l.d)))) row.appendChild(lb); }
        if (r) { var rb = el('button', 'xg-bar res ' + r.s); rb.type = 'button'; if (place(rb, x, r.d, r.d, '', 'Result: ' + fmtD(pd(r.d)) + ' (' + r.s + ')', true)) row.appendChild(rb); }
      }
      var btn = el('button', 'xg-bar ' + x.status + (x.start === x.end ? ' point' : '')); btn.type = 'button'; btn.style.setProperty('--c', x.color);
      var ok = place(btn, x, x.start, x.end, '', x.name + ' — ' + x.when + ' (' + x.status + ')', x.start === x.end);
      if (ok) row.appendChild(btn);
    }
    var cats = []; dated.forEach(function (x) { if (cats.indexOf(x.cat) < 0) cats.push(x.cat); });
    cats.forEach(function (c) {
      var items = dated.filter(function (x) { return x.cat === c; });
      if (S.gmode === 'cons') {
        labels.appendChild(el('div', 'xg-row', items[0].catTitle + ' (' + items.length + ')'));
        var r = el('div', 'xg-row'); items.forEach(function (x) { bar(x, r); }); tracks.appendChild(r);
      } else {
        labels.appendChild(el('div', 'xg-row cat', items[0].catTitle)); tracks.appendChild(el('div', 'xg-row cat'));
        items.forEach(function (x) { labels.appendChild(el('div', 'xg-row', x.name)); var r = el('div', 'xg-row'); bar(x, r); tracks.appendChild(r); });
      }
    });
    host.appendChild(labels); host.appendChild(tracks);
  }

  // events for list/calendar views: exam start days + (optionally) deadline milestones
  function events(list) {
    var out = [];
    list.forEach(function (x) {
      if (x.start) out.push({ date: x.start, end: x.end, x: x, m: null });
      if (S.dl) (x.ms || []).forEach(function (m) { if (m.d) out.push({ date: m.d, end: m.d, x: x, m: m }); });
    });
    return out;
  }

  function renderMonths(list) {
    var host = $('#v-months'); host.textContent = '';
    var groups = {}; events(list).forEach(function (e) { var k = e.date.slice(0, 7); (groups[k] = groups[k] || []).push(e); });
    Object.keys(groups).sort().forEach(function (k) {
      var items = groups[k].sort(function (a, b) { return a.date < b.date ? -1 : (a.date > b.date ? 1 : 0); }), y = +k.slice(0, 4), mo = +k.slice(5) - 1;
      var sec = el('section', 'xm-month'), h = el('h3', null, MONTHS[mo] + ' ' + y); h.appendChild(el('small', null, items.length + (items.length === 1 ? ' item' : ' items'))); sec.appendChild(h);
      var g = el('div', 'xm-grid');
      items.forEach(function (e) {
        var x = e.x, b = el('button', 'xm-item' + (e.m ? ' ms' : '')); b.type = 'button'; b.style.setProperty('--c', x.color);
        var d = el('div', 'd', String(pd(e.date).getDate())); d.appendChild(el('small', null, MONTHS[pd(e.date).getMonth()].slice(0, 3)));
        var r = el('div');
        r.appendChild(el('b', null, e.m ? e.m.icon + ' ' + e.m.label + ' — ' + x.name : x.name));
        r.appendChild(el('span', null, e.m ? (e.m.n || x.catTitle) : (x.start === x.end ? x.when : rangeText(x))));
        var st = el('div'); st.appendChild(el('span', 'xs-st ' + (e.m ? e.m.s : x.status), e.m ? e.m.s : x.status)); r.appendChild(st);
        b.appendChild(d); b.appendChild(r); b.addEventListener('click', function () { showDetail(x); }); g.appendChild(b);
      });
      sec.appendChild(g); host.appendChild(sec);
    });
    if (!host.firstChild) host.appendChild(el('div', 'xs-empty', 'No dated items match these filters.'));
  }

  function renderCalendar(list) {
    if (!S.cal) { var t = today(); S.cal = (t >= RANGE_START && t <= RANGE_END) ? new Date(t.getFullYear(), t.getMonth(), 1) : new Date(2026, 9, 1); }
    var first = S.cal, y = first.getFullYear(), m = first.getMonth(), host = $('#xc'); host.textContent = '';
    $('#cal-title').textContent = MONTHS[m] + ' ' + y;
    ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'].forEach(function (d) { host.appendChild(el('div', 'xc-dow', d)); });
    var offset = (first.getDay() + 6) % 7, start = new Date(y, m, 1 - offset), evs = events(list), td = iso(today());
    for (var i = 0; i < 42; i++) {
      var d = new Date(start.getFullYear(), start.getMonth(), start.getDate() + i), key = iso(d);
      if (i >= 35 && d.getMonth() !== m) break;
      var cell = el('button', 'xc-day' + (d.getMonth() !== m ? ' out' : '') + (key === td ? ' today' : '')); cell.type = 'button';
      var todays = evs.filter(function (e) { return e.date <= key && key <= e.end; });
      cell.setAttribute('aria-label', d.getDate() + ' ' + MONTHS[d.getMonth()] + ', ' + todays.length + ' items');
      cell.appendChild(el('span', 'n', String(d.getDate())));
      var starting = evs.filter(function (e) { return e.date === key; }), ongoing = evs.filter(function (e) { return !e.m && e.date < key && key <= e.end; });
      starting.slice(0, 3).forEach(function (e) {
        var c = el('span', 'xc-chip ' + (e.m ? 'ms ' + e.m.s : e.x.status), e.m ? e.m.icon + ' ' + e.m.label.replace('Applications ', 'App. ') + ' · ' + e.x.name : e.x.name);
        c.style.setProperty('--c', e.x.color); c.title = e.m ? e.x.name + ' — ' + e.m.label + ' (' + e.m.s + ')' : e.x.name + ' — ' + e.x.when; cell.appendChild(c);
      });
      if (starting.length > 3) cell.appendChild(el('span', 'xc-more', '+' + (starting.length - 3) + ' more'));
      if (ongoing.length) { var dots = el('span', 'xc-dots'); ongoing.slice(0, 8).forEach(function (e) { var i2 = el('i'); i2.style.setProperty('--c', e.x.color); i2.title = e.x.name + ' (ongoing window)'; dots.appendChild(i2); }); cell.appendChild(dots); }
      (function (key2) { cell.addEventListener('click', function () { dayPanel(key2, evs); }); })(key);
      host.appendChild(cell);
    }
  }
  function dayPanel(key, evs) {
    var p = $('#xc-day'); p.textContent = ''; p.hidden = false;
    var items = evs.filter(function (e) { return e.date <= key && key <= e.end; });
    p.appendChild(el('h3', null, fmtD(pd(key)) + ' — ' + (items.length ? items.length + ' item' + (items.length > 1 ? 's' : '') + ' on or around this day' : 'nothing scheduled')));
    items.forEach(function (e) {
      var x = e.x, b = el('button', 'xm-item' + (e.m ? ' ms' : '')); b.type = 'button'; b.style.setProperty('--c', x.color); b.style.marginBottom = '6px'; b.style.width = '100%';
      var d = el('div', 'd', e.m ? e.m.icon : (e.date === key ? 'Start' : 'On')); d.style.fontSize = '12px';
      var r = el('div'); r.appendChild(el('b', null, e.m ? e.m.label + ' — ' + x.name : x.name)); r.appendChild(el('span', null, (e.m ? (e.m.n || '') + ' · ' + e.m.s : rangeText(x) + ' · ' + x.status))); b.appendChild(d); b.appendChild(r);
      b.addEventListener('click', function () { showDetail(x); }); p.appendChild(b);
    });
  }

  // ---- next deadlines (sidebar) ---------------------------------------------------------------------------
  function renderNext() {
    var host = $('#xs-next'); if (!host) return; host.textContent = '';
    var t = iso(today()), items = [];
    DATA.forEach(function (x) { (x.ms || []).forEach(function (m) { if (m.d && m.d >= t && m.k !== 'other' && m.k !== 'admit') items.push({ x: x, m: m }); }); });
    items.sort(function (a, b) { return a.m.d < b.m.d ? -1 : (a.m.d > b.m.d ? 1 : 0); });
    items.slice(0, 8).forEach(function (e) {
      var d = pd(e.m.d), b = el('button', 'xs-nx'); b.type = 'button';
      var left = el('b', null, String(d.getDate())); left.appendChild(el('small', null, MONTHS[d.getMonth()].slice(0, 3)));
      var r = el('span', null, e.m.icon + ' ' + e.m.label + ' — ' + e.x.name); r.appendChild(el('em', null, dayDiff(today(), d) + ' days · ' + e.m.s + (e.m.n ? ' · ' + e.m.n : '')));
      b.appendChild(left); b.appendChild(r); b.addEventListener('click', function () { showDetail(e.x); }); host.appendChild(b);
    });
    if (!items.length) host.appendChild(el('p', null, 'No upcoming deadlines recorded.'));
  }

  // ---- orchestration ----------------------------------------------------------------------------------------
  function awaited(list) {
    var box = $('#xs-awaited'), miss = list.filter(function (x) { return !x.start; });
    box.textContent = ''; box.hidden = !(miss.length && S.view !== 'cards'); if (box.hidden) return;
    box.appendChild(el('h3', null, 'Dates awaited (not placed on the calendar)'));
    miss.forEach(function (x) { box.appendChild(el('p', null, x.name + ' — ' + x.when)); });
  }
  function update() {
    var list = visible(), dated = list.filter(function (x) { return x.start; }).length;
    $('#xs-count').textContent = list.length + ' of ' + DATA.length + ' exams' + (S.app !== 'all' ? ' · ' + S.app.replace('open', 'applications open now').replace('soon', 'opening soon').replace('late', 'in the late-fee window').replace('closing', 'closing within 14 days').replace('closed', 'applications closed') : '') + (S.view === 'cards' ? '' : ' · ' + dated + ' with dates shown');
    $('#xs-empty').hidden = list.length > 0;
    badges(); renderCards(list);
    if (S.view === 'gantt') renderGantt(list);
    if (S.view === 'months') renderMonths(list);
    if (S.view === 'calendar') renderCalendar(list);
    awaited(list);
    $('#xs-detail').hidden = true;
  }
  function setView(v) {
    S.view = v; try { localStorage.setItem('ea-exam-view', v); } catch (e) { }
    $$('.xs-view').forEach(function (b) { var on = b.getAttribute('data-view') === v; b.classList.toggle('on', on); b.setAttribute('aria-selected', on ? 'true' : 'false'); });
    ['cards', 'gantt', 'months', 'calendar'].forEach(function (k) { $('#v-' + k).hidden = k !== v; });
    update();
  }

  $$('.xs-view').forEach(function (b) { b.addEventListener('click', function () { setView(b.getAttribute('data-view')); }); });
  $$('.xs-fb').forEach(function (b) { b.addEventListener('click', function () { $$('.xs-fb').forEach(function (x) { x.classList.remove('on'); }); b.classList.add('on'); S.cat = b.getAttribute('data-f'); update(); }); });
  $$('.xs-sb[data-s]').forEach(function (b) { b.addEventListener('click', function () { $$('.xs-sb[data-s]').forEach(function (x) { x.classList.remove('on'); }); b.classList.add('on'); S.status = b.getAttribute('data-s'); update(); }); });
  $$('.xs-ab').forEach(function (b) { b.addEventListener('click', function () { $$('.xs-ab').forEach(function (x) { x.classList.remove('on'); }); b.classList.add('on'); S.app = b.getAttribute('data-a'); update(); }); });
  $$('.xs-sb[data-gmode]').forEach(function (b) { b.addEventListener('click', function () { $$('.xs-sb[data-gmode]').forEach(function (x) { x.classList.remove('on'); }); b.classList.add('on'); S.gmode = b.getAttribute('data-gmode'); update(); }); });
  $('#xs-deadlines').addEventListener('change', function () { S.dl = this.checked; update(); });
  $('#xs-q').addEventListener('input', function () { S.q = this.value; update(); });
  $('#xs-clear').addEventListener('click', function () {
    S.cat = 'all'; S.status = 'all'; S.app = 'all'; S.q = ''; $('#xs-q').value = '';
    $$('.xs-fb').forEach(function (x) { x.classList.toggle('on', x.getAttribute('data-f') === 'all'); });
    $$('.xs-sb[data-s]').forEach(function (x) { x.classList.toggle('on', x.getAttribute('data-s') === 'all'); });
    $$('.xs-ab').forEach(function (x) { x.classList.toggle('on', x.getAttribute('data-a') === 'all'); }); update();
  });
  $('#cal-prev').addEventListener('click', function () { S.cal = new Date(S.cal.getFullYear(), S.cal.getMonth() - 1, 1); $('#xc-day').hidden = true; renderCalendar(visible()); });
  $('#cal-next').addEventListener('click', function () { S.cal = new Date(S.cal.getFullYear(), S.cal.getMonth() + 1, 1); $('#xc-day').hidden = true; renderCalendar(visible()); });
  $('#cal-today').addEventListener('click', function () { var t = today(); S.cal = new Date(t.getFullYear(), t.getMonth(), 1); $('#xc-day').hidden = true; renderCalendar(visible()); });

  var saved = null; try { saved = localStorage.getItem('ea-exam-view'); } catch (e) { }
  var hash = (location.hash.match(/view=(cards|gantt|months|calendar)/) || [])[1];
  var appHash = (location.hash.match(/app=(open|closing|late|soon|closed)/) || [])[1];
  if (appHash) { S.app = appHash; $$('.xs-ab').forEach(function (x) { x.classList.toggle('on', x.getAttribute('data-a') === appHash); }); }
  renderNext();
  setView(hash || (['cards', 'gantt', 'months', 'calendar'].indexOf(saved) > -1 ? saved : 'cards'));
})();
