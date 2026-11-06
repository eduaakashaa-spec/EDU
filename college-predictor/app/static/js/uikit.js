/* EduAakashaA UI kit behaviour (see css/uikit.css).
   1. [data-how] panels remember whether the reader closed them.
   2. .fwrap: instant filtering of a long list. Inside it: buttons .fchip[data-key][data-val], selects [data-key], a search input [data-search], items .fi with data-<key>="a b c" and data-text.
   3. select[data-jump]: scrolls to the element whose id is the chosen value.
   4. The active .ms-tab is scrolled into view in the swipeable tab bar. */
(function () {
  'use strict';
  function store(k, v) { try { if (v === undefined) return localStorage.getItem(k); localStorage.setItem(k, v); } catch (e) { return null; } }

  // 1. how panels
  [].forEach.call(document.querySelectorAll('details[data-how]'), function (d) {
    var key = 'how:' + d.getAttribute('data-how'), seen = store(key);
    if (seen === 'closed') d.open = false;
    d.addEventListener('toggle', function () { store(key, d.open ? 'open' : 'closed'); });
  });

  // 1b. on a phone the role cards become tabs (one role at a time), starting with the reader's own role
  (function () {
    var mq = window.matchMedia ? window.matchMedia('(max-width: 640px)') : null;
    [].forEach.call(document.querySelectorAll('details.how'), function (d) {
      var g = d.querySelector('.how-g'), cards = g ? [].slice.call(g.querySelectorAll('.how-r')) : [];
      if (cards.length < 2) return;
      var bar = document.createElement('div'); bar.className = 'how-tabs'; bar.setAttribute('role', 'tablist');
      var first = d.getAttribute('data-focus');
      var start = cards.filter(function (c) { return c.getAttribute('data-role') === first; })[0] || cards[0];
      function show(c) {
        cards.forEach(function (x) { x.classList.toggle('on', x === c); });
        [].forEach.call(bar.children, function (b, i) { b.setAttribute('aria-pressed', String(cards[i] === c)); });
      }
      cards.forEach(function (c) {
        var b = document.createElement('button'); b.type = 'button'; b.textContent = c.querySelector('b').textContent;
        b.addEventListener('click', function () { show(c); }); bar.appendChild(b);
      });
      g.parentNode.insertBefore(bar, g); show(start);
      d.classList.add('how-tabbed');
    });
  })();

  // 1c. long forms start folded on a phone; a link to #id inside them opens them
  [].forEach.call(document.querySelectorAll('details[data-phone-closed]'), function (d) {
    if (window.matchMedia && window.matchMedia('(max-width: 640px)').matches) d.open = false;
  });
  window.addEventListener('hashchange', function () {
    var t = document.getElementById(location.hash.slice(1)), d = t && t.querySelector('details[data-phone-closed]');
    if (d) d.open = true;
  });

  // 2. filterable lists
  [].forEach.call(document.querySelectorAll('.fwrap'), function (w) {
    var items = [].slice.call(w.querySelectorAll('.fi')), state = {}, q = '';
    var chips = [].slice.call(w.querySelectorAll('.fchip[data-key]')), selects = [].slice.call(w.querySelectorAll('select[data-key]')), search = w.querySelector('input[data-search]');
    var none = w.querySelector('.fnone'), count = w.querySelector('.fcount');
    function has(it, key, val) { if (!val) return true; var v = (it.getAttribute('data-' + key) || '').split(/\s+/); return v.indexOf(val) >= 0; }
    function ok(it, skip) {
      for (var k in state) { if (k !== skip && !has(it, k, state[k])) return false; }
      if (q && (it.getAttribute('data-text') || it.textContent).toLowerCase().indexOf(q) < 0) return false;
      return true;
    }
    function apply() {
      var shown = 0;
      items.forEach(function (it) { var s = ok(it); it.hidden = !s; if (s) shown++; });
      chips.forEach(function (c) {
        var key = c.getAttribute('data-key'), val = c.getAttribute('data-val');
        c.setAttribute('aria-pressed', String((state[key] || '') === val));
        var n = c.querySelector('.n'); if (n) n.textContent = items.filter(function (it) { return ok(it, key) && has(it, key, val); }).length;
      });
      if (none) none.classList.toggle('on', shown === 0);
      if (count) count.textContent = shown + ' of ' + items.length;
    }
    chips.forEach(function (c) { c.addEventListener('click', function () { var k = c.getAttribute('data-key'), v = c.getAttribute('data-val'); state[k] = (state[k] === v && v) ? '' : v; apply(); }); });
    selects.forEach(function (s) { s.addEventListener('change', function () { state[s.getAttribute('data-key')] = s.value; apply(); }); });
    if (search) search.addEventListener('input', function () { q = search.value.trim().toLowerCase(); apply(); });
    var phone = window.matchMedia && window.matchMedia('(max-width: 640px)').matches;
    chips.forEach(function (c) { if (c.getAttribute('data-default') === '1' || (phone && c.getAttribute('data-default-phone') === '1')) state[c.getAttribute('data-key')] = c.getAttribute('data-val'); });
    apply();
  });

  // 3. jump menus
  [].forEach.call(document.querySelectorAll('select[data-jump]'), function (s) {
    s.addEventListener('change', function () {
      var t = document.getElementById(s.value); if (!t) return;
      if (t.tagName === 'DETAILS') t.open = true;
      t.scrollIntoView({behavior: 'smooth', block: 'start'});
    });
  });

  // 4. tab bar
  var on = document.querySelector('.ms-tabs .ms-tab.on');
  if (on && on.scrollIntoView) { try { on.scrollIntoView({inline: 'center', block: 'nearest'}); } catch (e) { /* older browsers */ } }
})();
