(function () {
  // tick a task: save, then update the row without reloading
  document.addEventListener('click', function (e) {
    var b = e.target.closest('.sp-check');
    if (!b) return;
    var row = b.closest('.sp-task'), done = b.getAttribute('aria-pressed') !== 'true';
    b.disabled = true;
    fetch(b.dataset.toggle, { method: 'POST', credentials: 'same-origin', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ status: done ? 'done' : 'todo' }) })
      .then(function (r) { return r.json(); }).then(function (j) {
        b.disabled = false;
        if (!j.ok) return;
        b.setAttribute('aria-pressed', j.status === 'done' ? 'true' : 'false');
        row.classList.toggle('done', j.status === 'done');
        var k = document.querySelectorAll('.sp-kpi b');
        if (k.length >= 3 && document.querySelector('.sp-hero')) { if (j.pct != null) k[0].textContent = j.pct + '%'; if (j.week_pct != null) k[1].textContent = j.week_pct + '%'; k[2].textContent = j.streak; }
      }).catch(function () { b.disabled = false; });
  });
  // "Which level am I?" check
  var go = document.getElementById('quiz-go');
  if (go) go.addEventListener('click', function () {
    var s = 0, n = 0;
    for (var i = 0; i < 5; i++) { var c = document.querySelector('input[name="q' + i + '"]:checked'); if (c) { s += parseInt(c.value, 10); n++; } }
    var out = document.getElementById('quiz-out');
    if (n < 5) { out.textContent = 'Please answer all five questions.'; return; }
    var lv = s <= 3 ? ['beginner', 'Beginner'] : s <= 7 ? ['average', 'Average'] : ['top', 'Top scorer'];
    out.innerHTML = 'Suggested level: <b>' + lv[1] + '</b>. <a href="' + location.pathname.replace('how-it-works', 'new') + '?level=' + lv[0] + '">Build a ' + lv[1] + ' plan</a>';
  });
})();
