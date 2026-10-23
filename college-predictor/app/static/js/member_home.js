/* Member dashboard: live search, category + type filters, collapsible sidebar, "recently opened" (this browser only).
   Everything is progressive: without JavaScript all resources stay visible. */
(function () {
  'use strict';
  var root = document.querySelector('.md');
  if (!root) return;
  var errBox = document.getElementById('md-error');

  function store(get, key, val) {
    try { if (get) return window.localStorage.getItem(key); window.localStorage.setItem(key, val); } catch (e) { /* private mode */ }
    return null;
  }

  try {
    var q = document.getElementById('md-q');
    var cards = Array.prototype.slice.call(document.querySelectorAll('#md-results ~ .md-cat .md-card'));
    var sections = Array.prototype.slice.call(document.querySelectorAll('.md-cat'));
    var count = document.getElementById('md-count');
    var empty = document.getElementById('md-empty');
    var state = { text: '', cat: 'all', type: 'all' };
    var total = cards.length;

    function match(c) {
      if (state.cat !== 'all' && c.dataset.cat !== state.cat) return false;
      var locked = c.dataset.locked === '1';
      if (state.type === 'roadmap' && c.dataset.tag !== 'roadmap') return false;
      if (state.type === 'report' && c.dataset.tag !== 'report') return false;
      if (state.type === 'open' && (locked || c.classList.contains('is-soon'))) return false;
      if (state.type === 'locked' && !locked) return false;
      if (state.text) {
        var words = state.text.split(/\s+/).filter(Boolean), hay = c.dataset.text || '';
        for (var i = 0; i < words.length; i++) if (hay.indexOf(words[i]) < 0) return false;
      }
      return true;
    }

    function apply() {
      var shown = 0;
      cards.forEach(function (c) { var ok = match(c); c.hidden = !ok; if (ok) shown++; });
      sections.forEach(function (s) {
        var any = s.querySelector('.md-card:not([hidden])');
        s.hidden = !any;
      });
      count.textContent = shown === total && !state.text && state.cat === 'all' && state.type === 'all'
        ? 'Showing ' + total + ' resources' : 'Showing ' + shown + ' of ' + total + ' resources';
      empty.hidden = shown !== 0;
      var rec = document.getElementById('md-recent');
      if (rec) rec.hidden = rec.dataset.has !== '1' || state.text !== '' || state.cat !== 'all' || state.type !== 'all';
    }

    function setCat(cat, scroll) {
      state.cat = cat;
      document.querySelectorAll('.md-fchip').forEach(function (b) { var on = b.dataset.cat === cat; b.classList.toggle('on', on); b.setAttribute('aria-pressed', on ? 'true' : 'false'); });
      document.querySelectorAll('.md-nav[data-cat]').forEach(function (a) { var on = a.dataset.cat === cat; a.classList.toggle('on', on); if (on) a.setAttribute('aria-current', 'page'); else a.removeAttribute('aria-current'); });
      apply();
      if (scroll) { var t = document.getElementById('md-results'); if (t) t.scrollIntoView({ behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth', block: 'start' }); }
    }
    function setType(type) {
      state.type = type;
      document.querySelectorAll('.md-tchip').forEach(function (b) { var on = b.dataset.type === type; b.classList.toggle('on', on); b.setAttribute('aria-pressed', on ? 'true' : 'false'); });
      apply();
    }

    q.addEventListener('input', function () { state.text = q.value.trim().toLowerCase(); apply(); });
    document.querySelectorAll('.md-fchip').forEach(function (b) { b.addEventListener('click', function () { setCat(b.dataset.cat, false); }); });
    document.querySelectorAll('.md-tchip').forEach(function (b) { b.addEventListener('click', function () { setType(b.dataset.type); }); });
    document.querySelectorAll('.md-nav[data-cat]').forEach(function (a) {
      a.addEventListener('click', function (e) { e.preventDefault(); setCat(a.dataset.cat, true); });
    });
    document.getElementById('md-clear').addEventListener('click', function () { q.value = ''; state.text = ''; setType('all'); setCat('all', false); q.focus(); });
    document.addEventListener('keydown', function (e) {
      var tag = (e.target.tagName || '').toLowerCase();
      if (e.key === '/' && tag !== 'input' && tag !== 'textarea' && tag !== 'select') { e.preventDefault(); q.focus(); }
      if (e.key === 'Escape' && document.activeElement === q && q.value) { q.value = ''; state.text = ''; apply(); }
    });

    // student details: open the form from the sidebar / account menu / welcome card
    document.querySelectorAll('[data-open-details]').forEach(function (a) {
      a.addEventListener('click', function () {
        var d = document.getElementById('details'); if (d) d.open = true;
        var m = document.querySelector('.md-menu'); if (m) m.open = false;
      });
    });
    document.addEventListener('click', function (e) { var m = document.querySelector('.md-menu'); if (m && m.open && !m.contains(e.target)) m.open = false; });

    // collapsible sidebar (remembered)
    var btn = document.getElementById('md-collapse');
    function collapsed(on) { root.dataset.collapsed = on ? '1' : '0'; btn.setAttribute('aria-expanded', on ? 'false' : 'true'); btn.setAttribute('aria-label', on ? 'Expand navigation' : 'Collapse navigation'); store(false, 'md_collapsed', on ? '1' : '0'); }
    if (store(true, 'md_collapsed') === '1') collapsed(true);
    btn.addEventListener('click', function () { collapsed(root.dataset.collapsed !== '1'); });

    // recently opened: ids of the last cards you opened in this browser, shown only if they are still available to you
    var KEY = 'md_recent';
    function recent() { try { return JSON.parse(store(true, KEY) || '[]'); } catch (e) { return []; } }
    cards.forEach(function (c) {
      if (c.tagName !== 'A' || c.dataset.locked === '1') return;
      c.addEventListener('click', function () {
        var ids = recent().filter(function (x) { return x !== c.dataset.id; }); ids.unshift(c.dataset.id);
        store(false, KEY, JSON.stringify(ids.slice(0, 4)));
      });
    });
    var grid = document.getElementById('md-recent-grid'), recBox = document.getElementById('md-recent');
    var ids = recent(), n = 0;
    ids.forEach(function (id) {
      var src = document.querySelector('.md-card[data-id="' + id + '"]');
      if (!src || src.tagName !== 'A' || src.dataset.locked === '1') return;
      var clone = src.cloneNode(true); clone.removeAttribute('data-id'); clone.removeAttribute('data-text'); clone.removeAttribute('data-cat');
      grid.appendChild(clone); n++;
    });
    if (n) { recBox.dataset.has = '1'; recBox.hidden = false; }
    apply();
  } catch (err) {
    if (errBox) errBox.hidden = false;             // the page stays fully usable: every card is a normal link
    if (window.console) console.error(err);
  }
})();
