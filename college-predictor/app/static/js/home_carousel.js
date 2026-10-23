/* Homepage banner carousel: autoplay, pause on hover / focus / hidden tab, arrows, dots, swipe, keyboard, play-pause button. */
(function () {
  'use strict';
  var root = document.querySelector('.hc');
  if (!root) return;
  var view = root.querySelector('.hc-view'), track = root.querySelector('.hc-track');
  var slides = Array.prototype.slice.call(root.querySelectorAll('.hc-slide'));
  var n = slides.length;
  if (n < 2) return;
  var MS = 5500, idx = 0, timer = null, userPaused = false, hovering = false, focusIn = false;
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduce) userPaused = true;                                     // no autoplay for people who ask for less motion
  root.style.setProperty('--hc-ms', MS + 'ms');

  var dotsBox = root.querySelector('.hc-bar'), dots = [];
  slides.forEach(function (s, i) {
    var b = document.createElement('button');
    b.type = 'button'; b.className = 'hc-dot'; b.setAttribute('aria-label', 'Go to slide ' + (i + 1) + ' of ' + n);
    b.addEventListener('click', function () { go(i, true); });
    dots.push(b); dotsBox.insertBefore(b, dotsBox.querySelector('.hc-pp'));
  });
  var pp = root.querySelector('.hc-pp'), count = root.querySelector('.hc-count'), live = root.querySelector('.hc-live');

  function render() {
    track.style.transform = 'translateX(' + (-100 * idx) + '%)';
    slides.forEach(function (s, i) { s.setAttribute('aria-hidden', i === idx ? 'false' : 'true'); s.tabIndex = i === idx ? 0 : -1; });
    dots.forEach(function (d, i) { d.classList.toggle('on', i === idx); if (i === idx) d.setAttribute('aria-current', 'true'); else d.removeAttribute('aria-current'); });
    if (count) count.textContent = (idx + 1) + ' / ' + n;
    var img = slides[(idx + 1) % n].querySelector('img'); if (img && img.loading === 'lazy') img.loading = 'eager';   // warm the next slide
  }
  function playing() { return !userPaused && !hovering && !focusIn && !document.hidden; }
  function schedule() {
    clearTimeout(timer);
    root.classList.toggle('playing', playing());
    if (pp) { pp.textContent = userPaused ? '▶' : '❚❚'; pp.setAttribute('aria-label', userPaused ? 'Play slideshow' : 'Pause slideshow'); }
    if (playing()) timer = setTimeout(function () { go(idx + 1, false); }, MS);
  }
  function go(i, manual) {
    idx = (i + n) % n; render();
    root.classList.remove('playing'); void root.offsetWidth;        // restart the progress fill
    if (live) live.textContent = manual || userPaused ? 'Slide ' + (idx + 1) + ' of ' + n : '';
    schedule();
  }
  root.querySelector('.hc-prev').addEventListener('click', function () { go(idx - 1, true); });
  root.querySelector('.hc-next').addEventListener('click', function () { go(idx + 1, true); });
  if (pp) pp.addEventListener('click', function () { userPaused = !userPaused; schedule(); });
  view.addEventListener('mouseenter', function () { hovering = true; schedule(); });
  view.addEventListener('mouseleave', function () { hovering = false; schedule(); });
  root.addEventListener('focusin', function () { focusIn = true; schedule(); });
  root.addEventListener('focusout', function () { focusIn = false; schedule(); });
  document.addEventListener('visibilitychange', schedule);
  root.addEventListener('keydown', function (e) {
    if (e.key === 'ArrowLeft') { go(idx - 1, true); e.preventDefault(); } else if (e.key === 'ArrowRight') { go(idx + 1, true); e.preventDefault(); }
  });
  // swipe
  var x0 = null, y0 = 0, moved = false;
  view.addEventListener('pointerdown', function (e) { if (e.pointerType === 'mouse') return; x0 = e.clientX; y0 = e.clientY; moved = false; });
  view.addEventListener('pointerup', function (e) {
    if (x0 === null) return;
    var dx = e.clientX - x0, dy = e.clientY - y0; x0 = null;
    if (Math.abs(dx) > 40 && Math.abs(dx) > Math.abs(dy)) { moved = true; go(idx + (dx < 0 ? 1 : -1), true); }
  });
  view.addEventListener('click', function (e) { if (moved) { e.preventDefault(); moved = false; } }, true);
  render(); schedule();
})();
