/* /exam-schedule — one dataset, four views (Cards · Timeline/Gantt · By month · Calendar) sharing the same filters.
   All text is written with textContent. Dates are ISO strings; rows with no date are listed under "dates awaited". */
(function () {
  'use strict';
  var DATA = JSON.parse(document.getElementById('xs-data').textContent);
  var RANGE_START = new Date(2026, 9, 1), RANGE_END = new Date(2027, 8, 30);   // Oct 2026 – Sep 2027
  var MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
  var S = { view: 'cards', cat: 'all', status: 'all', q: '', gmode: 'detail', cal: null };

  function $(s, r) { return (r || document).querySelector(s); }
  function $$(s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); }
  function el(t, c, x) { var n = document.createElement(t); if (c) n.className = c; if (x != null) n.textContent = x; return n; }
  function pd(s) { var p = s.split('-'); return new Date(+p[0], +p[1] - 1, +p[2]); }
  function iso(d) { return d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0'); }
  function dayDiff(a, b) { return Math.round((b - a) / 86400000); }
  function fmtD(d) { return d.getDate() + ' ' + MONTHS[d.getMonth()].slice(0, 3) + ' ' + d.getFullYear(); }
  function today() { var d = new Date(); d.setHours(0, 0, 0, 0); return d; }

  function visible() {
    var q = S.q.trim().toLowerCase();
    return DATA.filter(function (x) {
      return (S.cat === 'all' || x.cat === S.cat) && (S.status === 'all' || x.status === S.status) &&
        (!q || (x.name + ' ' + x.badge + ' ' + x.catTitle + ' ' + x.desc).toLowerCase().indexOf(q) > -1);
    });
  }
  function rangeText(x) { return x.start === x.end ? fmtD(pd(x.start)) : fmtD(pd(x.start)) + ' – ' + fmtD(pd(x.end)); }
  function gcal(x) {
    var e = new Date(pd(x.end).getTime() + 86400000), z = function (d) { return iso(d).replace(/-/g, ''); };
    return 'https://calendar.google.com/calendar/render?action=TEMPLATE&text=' + encodeURIComponent(x.name) + '&dates=' + z(pd(x.start)) + '/' + z(e) + '&details=' + encodeURIComponent(x.when + ' (' + x.status + '). Confirm on the official website.');
  }

  // ---- detail panel -------------------------------------------------------------------------------------
  function showDetail(x) {
    var p = $('#xs-detail'); p.textContent = ''; p.hidden = false;
    var h = el('h3', null, x.name); p.appendChild(h);
    var meta = el('p', null, x.catTitle + ' · ' + x.when + (x.start ? ' · ' + rangeText(x) : '') + ' · '); meta.appendChild(el('span', 'xs-st ' + x.status, x.status)); p.appendChild(meta);
    p.appendChild(el('p', null, x.desc));
    if (x.note) p.appendChild(el('span', 'xs-note', x.note));
    var a = el('div'); a.style.cssText = 'display:flex;gap:8px;flex-wrap:wrap;margin-top:10px;';
    if (x.start) {
      var l1 = el('a', 'xs-btn n', '📅 Add to calendar (.ics)'); l1.href = '/exam-schedule/' + x.id + '.ics'; a.appendChild(l1);
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

  function renderGantt(list) {
    var host = $('#xg'); host.textContent = ''; host.className = S.gmode === 'cons' ? 'xg-cons' : '';
    var total = dayDiff(RANGE_START, RANGE_END) + 1, dated = list.filter(function (x) { return x.start; });
    var labels = el('div', 'xg-labels'), tracks = el('div', 'xg-tracks');
    labels.appendChild(el('div', 'xg-head', 'Exam / category'));
    var head = el('div', 'xg-head'); tracks.appendChild(head);
    var grid = el('div', 'xg-grid'); tracks.appendChild(grid);
    for (var m = 0; m < 12; m++) {
      var ms = new Date(2026, 9 + m, 1), me = new Date(2026, 10 + m, 0), w = (dayDiff(ms, me) + 1) / total * 100, cell = el('div', 'm', MONTHS[ms.getMonth()].slice(0, 3) + ' ' + String(ms.getFullYear()).slice(2));
      cell.style.width = w + '%'; head.appendChild(cell);
      var line = el('i'); line.style.left = (dayDiff(RANGE_START, ms) / total * 100) + '%'; grid.appendChild(line);
    }
    var t = today();
    if (t >= RANGE_START && t <= RANGE_END) { var tl = el('div', 'xg-today'); tl.style.left = ((dayDiff(RANGE_START, t) + 0.5) / total * 100) + '%'; grid.appendChild(tl); }
    function bar(x, row) {
      var a = pd(x.start), b = pd(x.end); if (b < RANGE_START || a > RANGE_END) return;
      if (a < RANGE_START) a = RANGE_START; if (b > RANGE_END) b = RANGE_END;
      var btn = el('button', 'xg-bar ' + x.status + (x.start === x.end ? ' point' : '')); btn.type = 'button'; btn.style.setProperty('--c', x.color);
      var left = dayDiff(RANGE_START, a) / total * 100, width = (dayDiff(a, b) + 1) / total * 100;
      btn.style.left = left + '%'; if (x.start === x.end) btn.style.marginLeft = '-1px'; else btn.style.width = width + '%';
      btn.title = x.name + ' — ' + x.when + ' (' + x.status + ')'; btn.setAttribute('aria-label', x.name + ', ' + x.when + ', ' + x.status);
      btn.addEventListener('click', function () { showDetail(x); }); row.appendChild(btn);
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

  function renderMonths(list) {
    var host = $('#v-months'); host.textContent = '';
    var groups = {}; list.filter(function (x) { return x.start; }).forEach(function (x) { var k = x.start.slice(0, 7); (groups[k] = groups[k] || []).push(x); });
    Object.keys(groups).sort().forEach(function (k) {
      var items = groups[k].sort(function (a, b) { return a.start < b.start ? -1 : (a.start > b.start ? 1 : 0); }), y = +k.slice(0, 4), mo = +k.slice(5) - 1;
      var sec = el('section', 'xm-month'), h = el('h3', null, MONTHS[mo] + ' ' + y); h.appendChild(el('small', null, items.length + (items.length === 1 ? ' exam' : ' exams') + ' starting')); sec.appendChild(h);
      var g = el('div', 'xm-grid');
      items.forEach(function (x) {
        var b = el('button', 'xm-item'); b.type = 'button'; b.style.setProperty('--c', x.color);
        var d = el('div', 'd', String(pd(x.start).getDate())); d.appendChild(el('small', null, MONTHS[pd(x.start).getMonth()].slice(0, 3)));
        var r = el('div'); r.appendChild(el('b', null, x.name)); r.appendChild(el('span', null, x.start === x.end ? x.when : rangeText(x)));
        var st = el('div'); st.appendChild(el('span', 'xs-st ' + x.status, x.status)); r.appendChild(st);
        b.appendChild(d); b.appendChild(r); b.addEventListener('click', function () { showDetail(x); }); g.appendChild(b);
      });
      sec.appendChild(g); host.appendChild(sec);
    });
    if (!host.firstChild) host.appendChild(el('div', 'xs-empty', 'No dated exams match these filters.'));
  }

  function renderCalendar(list) {
    if (!S.cal) { var t = today(); S.cal = (t >= RANGE_START && t <= RANGE_END) ? new Date(t.getFullYear(), t.getMonth(), 1) : new Date(2026, 9, 1); }
    var first = S.cal, y = first.getFullYear(), m = first.getMonth(), host = $('#xc'); host.textContent = '';
    $('#cal-title').textContent = MONTHS[m] + ' ' + y;
    ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'].forEach(function (d) { host.appendChild(el('div', 'xc-dow', d)); });
    var offset = (first.getDay() + 6) % 7, start = new Date(y, m, 1 - offset), dated = list.filter(function (x) { return x.start; }), td = iso(today());
    for (var i = 0; i < 42; i++) {
      var d = new Date(start.getFullYear(), start.getMonth(), start.getDate() + i), key = iso(d);
      if (i >= 35 && d.getMonth() !== m) break;
      var cell = el('button', 'xc-day' + (d.getMonth() !== m ? ' out' : '') + (key === td ? ' today' : '')); cell.type = 'button';
      cell.setAttribute('aria-label', d.getDate() + ' ' + MONTHS[d.getMonth()] + ', ' + dated.filter(function (x) { return x.start <= key && key <= x.end; }).length + ' exams');
      cell.appendChild(el('span', 'n', String(d.getDate())));
      var starting = dated.filter(function (x) { return x.start === key; }), ongoing = dated.filter(function (x) { return x.start < key && key <= x.end; });
      starting.slice(0, 3).forEach(function (x) { var c = el('span', 'xc-chip ' + x.status, x.name); c.style.setProperty('--c', x.color); c.title = x.name + ' — ' + x.when; cell.appendChild(c); });
      if (starting.length > 3) cell.appendChild(el('span', 'xc-more', '+' + (starting.length - 3) + ' more'));
      if (ongoing.length) { var dots = el('span', 'xc-dots'); ongoing.slice(0, 8).forEach(function (x) { var i2 = el('i'); i2.style.setProperty('--c', x.color); i2.title = x.name + ' (ongoing window)'; dots.appendChild(i2); }); cell.appendChild(dots); }
      (function (key2) { cell.addEventListener('click', function () { dayPanel(key2, dated); }); })(key);
      host.appendChild(cell);
    }
  }
  function dayPanel(key, dated) {
    var p = $('#xc-day'); p.textContent = ''; p.hidden = false;
    var items = dated.filter(function (x) { return x.start <= key && key <= x.end; });
    p.appendChild(el('h3', null, fmtD(pd(key)) + ' — ' + (items.length ? items.length + ' exam' + (items.length > 1 ? 's' : '') + ' on or around this day' : 'nothing scheduled')));
    items.forEach(function (x) {
      var b = el('button', 'xm-item'); b.type = 'button'; b.style.setProperty('--c', x.color); b.style.marginBottom = '6px'; b.style.width = '100%';
      var d = el('div', 'd', x.start === key ? 'Start' : 'On'); d.style.fontSize = '12px';
      var r = el('div'); r.appendChild(el('b', null, x.name)); r.appendChild(el('span', null, rangeText(x) + ' · ' + x.status)); b.appendChild(d); b.appendChild(r);
      b.addEventListener('click', function () { showDetail(x); }); p.appendChild(b);
    });
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
    $('#xs-count').textContent = list.length + ' of ' + DATA.length + ' exams' + (S.view === 'cards' ? '' : ' · ' + dated + ' with dates shown');
    $('#xs-empty').hidden = list.length > 0;
    renderCards(list);
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
  $$('.xs-sb[data-gmode]').forEach(function (b) { b.addEventListener('click', function () { $$('.xs-sb[data-gmode]').forEach(function (x) { x.classList.remove('on'); }); b.classList.add('on'); S.gmode = b.getAttribute('data-gmode'); update(); }); });
  $('#xs-q').addEventListener('input', function () { S.q = this.value; update(); });
  $('#xs-clear').addEventListener('click', function () { S.cat = 'all'; S.status = 'all'; S.q = ''; $('#xs-q').value = ''; $$('.xs-fb').forEach(function (x) { x.classList.toggle('on', x.getAttribute('data-f') === 'all'); }); $$('.xs-sb[data-s]').forEach(function (x) { x.classList.toggle('on', x.getAttribute('data-s') === 'all'); }); update(); });
  $('#cal-prev').addEventListener('click', function () { S.cal = new Date(S.cal.getFullYear(), S.cal.getMonth() - 1, 1); $('#xc-day').hidden = true; renderCalendar(visible()); });
  $('#cal-next').addEventListener('click', function () { S.cal = new Date(S.cal.getFullYear(), S.cal.getMonth() + 1, 1); $('#xc-day').hidden = true; renderCalendar(visible()); });
  $('#cal-today').addEventListener('click', function () { var t = today(); S.cal = new Date(t.getFullYear(), t.getMonth(), 1); $('#xc-day').hidden = true; renderCalendar(visible()); });

  var saved = null; try { saved = localStorage.getItem('ea-exam-view'); } catch (e) { }
  var hash = (location.hash.match(/view=(cards|gantt|months|calendar)/) || [])[1];
  setView(hash || (['cards', 'gantt', 'months', 'calendar'].indexOf(saved) > -1 ? saved : 'cards'));
})();
