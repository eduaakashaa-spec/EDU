/* EduPulse - Reinforcement question flow. One question at a time; every answer needs a confidence level before moving on.
   Progress is saved to the server after each step (autosave), so a closed tab resumes at the last unanswered question. */
(function () {
  var root = document.getElementById('rf-app');
  if (!root) return;
  var API = root.getAttribute('data-api'), SAVE = API + '/save', SUBMIT = API + '/submit', REVIEW = API + '/review', HOME = root.getAttribute('data-home');
  var CONF = JSON.parse(root.getAttribute('data-conf'));
  var CDESC = { G: 'I am unsure and am choosing what seems most likely.', L: 'I have some understanding but may have made a mistake.', M: 'I understand the concept reasonably well but am not completely sure.', H: 'I understand the concept and believe my answer is correct.' };
  var CTITLE = { G: 'Guess', L: 'Low', M: 'Medium', H: 'High' };
  var CICON = { G: '?', L: '◔', M: '◑', H: '✓' };
  var S = { items: [], i: 0, t0: 0, started: 0 };
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function post(url, body) { return fetch(url, { method: 'POST', headers: { 'Content-Type': 'application/json' }, credentials: 'same-origin', body: JSON.stringify(body || {}) }).then(function (r) { return r.json().then(function (j) { j._status = r.status; return j; }); }); }

  function load() {
    fetch(API, { credentials: 'same-origin' }).then(function (r) { return r.json(); }).then(function (d) {
      if (!d.ok) { root.innerHTML = '<p class="rf-note">This assignment could not be opened.</p>'; return; }
      S.d = d; S.items = d.items;
      if (d.completed) { return done({ answered: d.items.length, released: d.released, release_note: '' }, true); }
      S.i = d.resume || 0; render();
    }).catch(function () { root.innerHTML = '<p class="rf-note">Could not load the questions. Check your connection and refresh.</p>'; });
  }
  function cur() { return S.items[S.i]; }
  function complete(it) { return it.answer !== null && it.answer !== undefined && it.answer !== '' && !(Array.isArray(it.answer) && !it.answer.length) && !!it.confidence; }
  function elapsed() { var s = Math.round((Date.now() - S.t0) / 1000); S.t0 = Date.now(); return s; }

  function render() {
    var it = cur(), n = S.items.length; S.t0 = Date.now();
    var answered = S.items.filter(complete).length;
    var h = '<div class="rf-top"><span>Question ' + (S.i + 1) + ' of ' + n + '</span><span>' + esc(S.d.exam) + ' · ' + esc(it.subject) + ' · ' + esc(it.chapter) + '</span></div>' +
      '<div class="rf-bar" role="progressbar" aria-valuemin="0" aria-valuemax="' + n + '" aria-valuenow="' + answered + '"><i style="width:' + Math.round(100 * answered / n) + '%"></i></div>';
    if (S.i === 0 && S.d.instructions) h += '<div class="rf-note">' + esc(S.d.instructions) + '</div>';
    h += '<div class="rf-q"><div class="meta"><span class="rf-pill">' + esc(it.topic || it.chapter) + '</span><span class="rf-pill">' + esc(it.difficulty) + '</span><span class="rf-pill">' + (it.qtype === 'nat' ? 'Numerical answer' : it.qtype === 'msq' ? 'Select all that apply' : 'Single answer') + '</span></div>';
    h += '<div class="stem">' + it.stem + '</div>';
    if (it.qtype === 'nat') {
      h += '<div class="rf-nat" style="margin-top:12px"><label class="rf-muted" for="rf-nat">Your answer (a number)</label><input id="rf-nat" inputmode="decimal" autocomplete="off" value="' + esc(it.answer == null ? '' : it.answer) + '"></div>';
    } else {
      h += '<div class="rf-opts" role="' + (it.qtype === 'msq' ? 'group' : 'radiogroup') + '">';
      it.options.forEach(function (o, k) {
        var L = 'ABCD'[k]; if (!o) return;
        var on = it.qtype === 'msq' ? (it.answer || []).indexOf(L) > -1 : it.answer === L;
        h += '<label class="rf-opt' + (on ? ' on' : '') + '"><input type="' + (it.qtype === 'msq' ? 'checkbox' : 'radio') + '" name="o" value="' + L + '"' + (on ? ' checked' : '') + '><b>' + L + '</b><span>' + o + '</span></label>';
      });
      h += '</div>';
    }
    var has = it.answer !== null && it.answer !== undefined && it.answer !== '' && !(Array.isArray(it.answer) && !it.answer.length);
    h += '<div class="rf-conf"><h3>How confident are you in your answer?</h3><div class="grid" role="group" aria-label="Confidence">';
    CONF.forEach(function (c) {
      var k = c[0];
      h += '<button type="button" class="rf-cf ' + k + '" data-c="' + k + '" aria-pressed="' + (it.confidence === k) + '"' + (has ? '' : ' disabled') + '><span class="ic">' + CICON[k] + '<br>' + CTITLE[k] + '</span><span><b>' + (k === 'G' ? 'Guessing' : k === 'L' ? 'Low confidence' : k === 'M' ? 'Medium confidence' : 'High confidence') + '</b><small>' + CDESC[k] + '</small></span></button>';
    });
    h += '</div><p class="rf-muted" id="rf-hint" style="margin:8px 0 0">' + (has ? (it.confidence ? 'You can change this before you move on.' : 'Pick one to continue.') : 'Answer first, then rate your confidence.') + '</p></div></div>';
    var last = S.i === n - 1;
    h += '<div class="rf-nav2"><button class="rf-btn ghost" id="rf-prev"' + (S.i && S.d.allow_back ? '' : ' disabled') + '>Previous</button><button class="rf-btn" id="rf-next"' + (complete(it) ? '' : ' disabled') + '>' + (last ? 'Submit' : 'Next') + '</button></div>';
    root.innerHTML = h; bind();
  }
  function persist(extra) { var it = cur(); var body = { item_id: it.id, answer: it.answer, confidence: it.confidence, seconds: (it.seconds || 0) + (extra || 0) }; it.seconds = body.seconds; return post(SAVE, body); }
  function refreshNext() { var b = document.getElementById('rf-next'); if (b) b.disabled = !complete(cur()); document.querySelectorAll('.rf-cf').forEach(function (x) { x.setAttribute('aria-pressed', String(cur().confidence === x.getAttribute('data-c'))); });
    var h = document.getElementById('rf-hint'); if (h) h.textContent = cur().confidence ? 'You can change this before you move on.' : 'Pick one to continue.'; }
  function bind() {
    var it = cur();
    function enableConf() { document.querySelectorAll('.rf-cf').forEach(function (b) { b.disabled = false; }); var h = document.getElementById('rf-hint'); if (h && !it.confidence) h.textContent = 'Pick one to continue.'; }
    document.querySelectorAll('.rf-opt input').forEach(function (inp) {
      inp.addEventListener('change', function () {
        if (it.qtype === 'msq') { it.answer = Array.prototype.map.call(document.querySelectorAll('.rf-opt input:checked'), function (x) { return x.value; }); }
        else { it.answer = inp.value; }
        document.querySelectorAll('.rf-opt').forEach(function (l) { l.classList.toggle('on', l.querySelector('input').checked); });
        if (!(it.answer && it.answer.length)) it.confidence = null;
        enableConf(); persist(0); refreshNext();
      });
    });
    var nat = document.getElementById('rf-nat');
    if (nat) nat.addEventListener('input', function () {
      var v = nat.value.replace(/[^0-9.\-−]/g, ''); if (v !== nat.value) nat.value = v;
      it.answer = v === '' ? null : v; if (v === '') it.confidence = null; enableConf(); refreshNext(); clearTimeout(nat._t); nat._t = setTimeout(function () { persist(0); }, 500);
    });
    document.querySelectorAll('.rf-cf').forEach(function (b) { b.addEventListener('click', function () { it.confidence = b.getAttribute('data-c'); persist(0); refreshNext(); }); });
    document.getElementById('rf-prev').addEventListener('click', function () { persist(elapsed()).then(function () { S.i--; render(); }); });
    document.getElementById('rf-next').addEventListener('click', function () {
      var btn = this; btn.disabled = true;
      persist(elapsed()).then(function () {
        if (S.i < S.items.length - 1) { S.i++; render(); window.scrollTo(0, 0); return; }
        post(SUBMIT, {}).then(function (j) {
          if (!j.ok) { alert(j.error || 'Could not submit.'); if (j.missing && j.missing.length) { S.i = j.missing[0] - 1; render(); } else btn.disabled = false; return; }
          done(j, false);
        });
      });
    });
  }
  function done(j, again) {
    var n = S.items.length;
    var h = '<div class="rf-done"><h1>' + (again ? 'Already completed' : 'Today’s reinforcement completed!') + '</h1><p class="rf-muted">' + esc(S.d.title) + '</p>';
    if (!again) h += '<div class="kp"><div><b>' + j.answered + '/' + n + '</b>Questions answered</div><div><b>' + j.correct + '/' + n + '</b>Correct answers</div><div><b>' + j.revisit + '</b>Concepts to revisit</div><div><b>' + j.streak + '</b>Day practice streak</div></div>' +
      '<p>Well done for finishing. Each answer and your confidence help your mentor choose what to reinforce next. Mistakes are information, not a verdict.</p>';
    h += '<p class="rf-note" id="rf-rel">' + esc(j.release_note || '') + '</p><div id="rf-review"></div><p><a class="rf-btn" href="' + HOME + '">Back to my reinforcement</a></p></div>';
    root.innerHTML = h;
    if (j.released) { fetch(REVIEW, { credentials: 'same-origin' }).then(function (r) { return r.json(); }).then(function (r) {
      if (!r.ok) return; var out = '<h3 style="text-align:left;font-family:Fraunces,serif">Answers and explanations</h3>';
      r.items.forEach(function (q) {
        var ans = q.answer; var show = q.qtype === 'nat' ? (ans && ans[0] ? ans[0][0] : '') : (Array.isArray(ans) ? ans.join(', ') : ans);
        var yours = q.yours == null ? 'not answered' : (Array.isArray(q.yours) ? q.yours.join(', ') : q.yours);
        out += '<div class="rf-rev ' + (q.correct ? 'ok' : 'no') + '"><div class="rf-muted">Question ' + q.pos + ' · your answer: ' + esc(yours) + (q.confidence ? ' (' + esc(CTITLE[q.confidence]) + ')' : '') + ' · correct: ' + esc(show) + '</div><div>' + q.stem + '</div>' +
          '<div style="margin-top:8px">' + (q.explanation || '') + '</div>' + (q.misconception ? '<div class="rf-note"><b>Common mistake.</b> ' + q.misconception + '</div>' : '') + '</div>';
      });
      document.getElementById('rf-review').innerHTML = out; }); }
  }
  load();
})();
