/* FutureReady: autosave for assessment pages. Progressive enhancement: the form works with a normal POST if this script fails. */
(function () {
  var f = document.getElementById('fr-form');
  if (!f) return;
  var url = f.getAttribute('data-save'), st = document.getElementById('fr-saved'), timer = null;
  function collect() {
    var d = {};
    Array.prototype.forEach.call(f.elements, function (e) {
      if (!e.name || e.name === 'action' || e.name === 'csrf_token') return;
      if (e.type === 'radio') { if (e.checked) d[e.name] = parseInt(e.value, 10); else if (!(e.name in d)) d[e.name] = d[e.name]; }
      else if (e.type === 'checkbox') { d[e.name] = d[e.name] || []; if (e.checked) d[e.name].push(parseInt(e.value, 10)); }
      else if (e.value !== '') d[e.name] = e.value;
    });
    Object.keys(d).forEach(function (k) { if (d[k] === undefined) delete d[k]; });
    return d;
  }
  function save() {
    if (!url) return;
    fetch(url, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(collect()), credentials: 'same-origin' })
      .then(function (r) { return r.json(); })
      .then(function (j) { if (st) st.textContent = j.ok ? 'Saved (' + j.n + ' answered)' : 'Could not save'; })
      .catch(function () { if (st) st.textContent = 'Offline: your answers will be saved when you press Save'; });
  }
  f.addEventListener('change', function () { clearTimeout(timer); timer = setTimeout(save, 700); });
  var answered = function () { return f.querySelectorAll('.fr-q').length; };
  var bar = document.getElementById('fr-progress');
  function prog() {
    if (!bar) return;
    var names = {}, done = {};
    Array.prototype.forEach.call(f.elements, function (e) {
      if (!e.name || e.name === 'action') return;
      names[e.name] = 1;
      if ((e.type === 'radio' || e.type === 'checkbox') ? e.checked : e.value !== '') done[e.name] = 1;
    });
    var n = Object.keys(names).length, d = Object.keys(done).length;
    bar.style.width = (n ? Math.round(100 * d / n) : 0) + '%';
    bar.setAttribute('aria-valuenow', n ? Math.round(100 * d / n) : 0);
  }
  f.addEventListener('change', prog); f.addEventListener('input', prog); prog();
})();
