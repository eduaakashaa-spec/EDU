/* Modern page navigation: a top reading-progress bar everywhere, plus a numbered section rail (01, 02 …) that tracks the section in view
   and scrolls to it on click — the same pattern as the homepage. Sections are discovered automatically, so any page gets it. */
(function () {
  'use strict';
  if (document.querySelector('.aw-rail') || document.querySelector('[data-no-rail]')) return;     // the homepage has its own rail
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;

  // reading progress (all widths)
  var top = document.createElement('div');
  top.className = 'pr-top'; top.setAttribute('aria-hidden', 'true'); top.innerHTML = '<i></i>';
  document.body.appendChild(top);
  var topBar = top.firstChild;

  function visible(el) { var r = el.getBoundingClientRect(); return r.height > 160 && r.width > 240; }
  function label(el) {
    var h = /^H[1-6]$/.test(el.tagName) ? el : el.querySelector('h1,h2,h3,.eyebrow,[class*=eyebrow]');
    var t = (el.getAttribute('aria-label') || (h && h.textContent) || el.id || '').replace(/\s+/g, ' ').trim();
    return t.length > 60 ? t.slice(0, 57) + '…' : t;
  }
  function collect() {
    var marked = Array.prototype.slice.call(document.querySelectorAll('[data-rail]')).filter(function (s) { return s.offsetHeight > 0; });
    if (marked.length >= 3) return marked.slice(0, 9);                       // a page that marks its own sections decides the rail
    var all = Array.prototype.slice.call(document.querySelectorAll('section')).filter(function (s) {
      return !s.closest('header, nav, footer, dialog, [role=dialog], .modal, .pr-rail') && visible(s) && label(s);
    });
    // keep outermost sections only (a section inside another one is part of it)
    all = all.filter(function (s) { return !all.some(function (o) { return o !== s && o.contains(s); }); });
    if (all.length < 3) {                                            // pages built from divs: use their visible h2 headings as the topics
      var hs = Array.prototype.slice.call(document.querySelectorAll('h2')).filter(function (h) {
        var r = h.getBoundingClientRect();
        return !h.closest('header, nav, footer, dialog, [role=dialog], .modal, .pr-drawer, .pr-rail, [hidden]') && r.width > 120 && h.textContent.replace(/\s+/g, ' ').trim().length > 2;
      });
      if (hs.length >= 3) all = hs;
    }
    if (all.length > 9) {                                            // too many: keep nine evenly spaced
      var step = (all.length - 1) / 8;
      all = Array.apply(null, Array(9)).map(function (_, i) { return all[Math.round(i * step)]; });
    }
    return all;
  }

  function build() {
    var secs = collect();
    var rail = null, links = [], barFill = null, dlinks = [], toTop = null;
    var own = document.querySelector('.tn-side, .md-side, nav.sidebar');          // pages with their own topics panel keep it
    if (secs.length >= 3) {
      rail = document.createElement('nav');
      rail.className = 'pr-rail'; rail.setAttribute('aria-label', 'Page sections');
      secs.forEach(function (s, i) {
        if (!s.id) s.id = 'pr-sec-' + (i + 1);
        var a = document.createElement('a');
        a.href = '#' + s.id; a.textContent = (i < 9 ? '0' : '') + (i + 1); a.setAttribute('data-label', label(s)); a.setAttribute('aria-label', 'Section ' + (i + 1) + ': ' + label(s));
        a.addEventListener('click', function (e) {
          e.preventDefault();
          s.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'start' });
          if (history.replaceState) history.replaceState(null, '', '#' + s.id);
        });
        links.push(a); rail.appendChild(a);
        if (i === 0) { var bar = document.createElement('div'); bar.className = 'pr-bar'; bar.innerHTML = '<i></i>'; barFill = bar.firstChild; rail.appendChild(bar); }
      });
      document.body.appendChild(rail);
      if (!own) {                                                   // labelled "Topics" drawer: works at every width, no layout shift
        var btn = document.createElement('button');
        btn.type = 'button'; btn.className = 'pr-topics'; btn.setAttribute('aria-haspopup', 'dialog'); btn.setAttribute('aria-expanded', 'false');
        btn.innerHTML = '<span aria-hidden="true">&#9776;</span> Topics';
        var scrim = document.createElement('div'); scrim.className = 'pr-scrim';
        var dr = document.createElement('aside'); dr.className = 'pr-drawer'; dr.setAttribute('role', 'dialog'); dr.setAttribute('aria-label', 'On this page');
        dr.innerHTML = '<div class="pr-dh"><b>On this page</b><button type="button" class="pr-x" aria-label="Close topics">&times;</button></div><div class="pr-dl"></div>';
        var list = dr.querySelector('.pr-dl');
        secs.forEach(function (s, i) {
          var a = document.createElement('a');
          a.href = '#' + s.id; a.innerHTML = '<b>' + (i + 1) + '</b><span></span>'; a.lastChild.textContent = label(s);
          a.addEventListener('click', function (e) { e.preventDefault(); close(); s.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'start' }); if (history.replaceState) history.replaceState(null, '', '#' + s.id); });
          dlinks.push(a); list.appendChild(a);
        });
        function open() { dr.classList.add('open'); scrim.classList.add('show'); btn.setAttribute('aria-expanded', 'true'); dr.querySelector('.pr-x').focus(); }
        function close() { dr.classList.remove('open'); scrim.classList.remove('show'); btn.setAttribute('aria-expanded', 'false'); }
        btn.addEventListener('click', open); scrim.addEventListener('click', close); dr.querySelector('.pr-x').addEventListener('click', function () { close(); btn.focus(); });
        addEventListener('keydown', function (e) { if (e.key === 'Escape' && dr.classList.contains('open')) { close(); btn.focus(); } });
        document.body.appendChild(btn); document.body.appendChild(scrim); document.body.appendChild(dr);
      }
    }
    if (!own) {
      toTop = document.createElement('button'); toTop.type = 'button'; toTop.className = 'pr-totop'; toTop.setAttribute('aria-label', 'Back to top'); toTop.innerHTML = '&#8593;';
      toTop.addEventListener('click', function () { scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' }); });
      document.body.appendChild(toTop);
    }
    var ticking = false;
    function tick() {
      ticking = false;
      var d = document.documentElement, max = d.scrollHeight - innerHeight, p = max > 0 ? Math.min(1, Math.max(0, d.scrollTop / max)) : 0;
      topBar.style.transform = 'scaleX(' + p + ')';
      if (toTop) toTop.classList.toggle('show', d.scrollTop > 700);
      if (barFill) barFill.style.transform = 'scaleY(' + p + ')';
      if (links.length) {
        var mid = innerHeight * 0.4, act = 0;
        secs.forEach(function (s, i) { if (s.getBoundingClientRect().top <= mid) act = i; });
        links.forEach(function (a, i) { a.classList.toggle('on', i === act); if (i === act) a.setAttribute('aria-current', 'true'); else a.removeAttribute('aria-current'); });
        dlinks.forEach(function (a, i) { a.classList.toggle('on', i === act); });
      }
    }
    function onScroll() { if (!ticking) { ticking = true; requestAnimationFrame(tick); } }
    addEventListener('scroll', onScroll, { passive: true }); addEventListener('resize', onScroll); tick();
  }

  if (document.readyState === 'complete') build(); else addEventListener('load', build);
})();
