
/* ── Smooth scroll — works inside iframes ── */
function scrollTo(id) {
  var el = document.getElementById(id);
  if (el) { el.scrollIntoView({ behavior: 'smooth', block: 'start' }); }
}

/* ── Quiz ── */
var Qs = [
  { q: "Where do you want to build your career?",
    o: [{t:"🌍 Internationally — anywhere",s:{acca:2}},{t:"💹 Finance hubs (NYC, London, HK)",s:{cfa:2}},{t:"🏙️ Primarily in my home country",s:{ca:2}},{t:"🤷 Not decided yet",s:{acca:1}}]
  },
  { q: "What kind of work excites you most?",
    o: [{t:"📊 Auditing & financial reporting",s:{acca:2,ca:1}},{t:"📈 Stock analysis & portfolio management",s:{cfa:3}},{t:"🧾 Tax, compliance & advisory",s:{ca:2}},{t:"🔀 A mix of all finance areas",s:{acca:2}}]
  },
  { q: "How can you dedicate time to studying?",
    o: [{t:"⏱️ Part-time alongside my job",s:{acca:2}},{t:"📚 Intense focused study windows",s:{cfa:2}},{t:"🎓 Full-time with practical training",s:{ca:2}},{t:"🔄 Flexible — whatever it takes",s:{acca:1,cfa:1,ca:1}}]
  },
  { q: "What matters most in a qualification?",
    o: [{t:"🌐 Global recognition / working abroad",s:{acca:3}},{t:"💰 Highest salary in investment finance",s:{cfa:3}},{t:"🏆 Prestigious local qualification",s:{ca:3}},{t:"⚡ Fastest route to a finance career",s:{acca:2}}]
  }
];

var cur = 0, sc = {acca:0,cfa:0,ca:0}, pend = null;

function pick(btn, idx) {
  var all = document.querySelectorAll('.qopt');
  for (var i = 0; i < all.length; i++) all[i].classList.remove('sel');
  btn.classList.add('sel');
  pend = Qs[cur].o[idx].s;
  document.getElementById('qNext').style.display = 'inline-block';
}

function nextQ() {
  if (!pend) return;
  for (var k in pend) sc[k] = (sc[k] || 0) + pend[k];
  pend = null; cur++;
  if (cur >= Qs.length) { showRes(); return; }
  document.getElementById('qProg').textContent = 'Question ' + (cur+1) + ' of ' + Qs.length;
  document.getElementById('qText').textContent = Qs[cur].q;
  var h = '';
  for (var i = 0; i < Qs[cur].o.length; i++)
    h += '<button class="qopt" onclick="pick(this,' + i + ')">' + Qs[cur].o[i].t + '</button>';
  document.getElementById('qOpts').innerHTML = h;
  document.getElementById('qNext').style.display = 'none';
}

function showRes() {
  var keys = Object.keys(sc).sort(function(a,b){ return sc[b]-sc[a]; });
  var w = keys[0];
  var info = {
    acca:{n:'ACCA',cls:'rb-a', ti:'ACCA is your ideal match!', tx:'Your goals align with ACCA — global flexibility, modular study structure, and recognition in 180+ countries.'},
    cfa: {n:'CFA', cls:'rb-c', ti:'CFA is your ideal match!',  tx:'Your passion for investment and markets points to the CFA Charter — the gold standard for finance professionals worldwide.'},
    ca:  {n:'CA',  cls:'rb-ca',ti:'CA is your ideal match!',   tx:'Your preference for domestic prestige, taxation, and comprehensive accounting makes CA the perfect qualification.'}
  }[w];
  document.getElementById('qMain').style.display = 'none';
  document.getElementById('qResult').style.display = 'block';
  var b = document.getElementById('rBadge');
  b.textContent = info.n;
  b.className = 'rbadge ' + info.cls;
  document.getElementById('rTitle').textContent = info.ti;
  document.getElementById('rText').textContent  = info.tx;
}

function resetQ() {
  cur = 0; sc = {acca:0,cfa:0,ca:0}; pend = null;
  document.getElementById('qResult').style.display = 'none';
  document.getElementById('qMain').style.display = 'block';
  document.getElementById('qProg').textContent = 'Question 1 of ' + Qs.length;
  document.getElementById('qText').textContent = Qs[0].q;
  var h = '';
  for (var i = 0; i < Qs[0].o.length; i++)
    h += '<button class="qopt" onclick="pick(this,' + i + ')">' + Qs[0].o[i].t + '</button>';
  document.getElementById('qOpts').innerHTML = h;
  document.getElementById('qNext').style.display = 'none';
}


// ---- next <script> block ----


	const heightObserver = new ResizeObserver(([{ contentRect }]) => {
		window.parent.postMessage({ action: 'iframeHeightUpdated', height: contentRect.height, id: 'z9l41_' }, '*');
	});

	heightObserver.observe(document.documentElement);
