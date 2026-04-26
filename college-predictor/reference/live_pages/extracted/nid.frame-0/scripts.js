
// Smooth scroll
document.querySelectorAll('nav a').forEach(a => {
  a.addEventListener('click', e => {
    e.preventDefault();
    const id = a.getAttribute('href');
    document.querySelector(id)?.scrollIntoView({ behavior: 'smooth', block: 'start' });
    document.querySelectorAll('nav a').forEach(n => n.classList.remove('active'));
    a.classList.add('active');
  });
});

// Fade-in on scroll
const obs = new IntersectionObserver(entries => {
  entries.forEach(e => { if(e.isIntersecting) e.target.classList.add('visible'); });
}, { threshold: 0.1 });
document.querySelectorAll('.fade-in').forEach(el => obs.observe(el));

// Tab switching
function showTab(id) {
  document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  document.getElementById(id).classList.add('active');
  event.target.classList.add('active');
}

// Accordion
function toggleAcc(el) {
  el.parentElement.classList.toggle('open');
}

// Quiz calculation
function calculateResult() {
  let d = 0, e = 0, b = 0;
  for (let i = 1; i <= 10; i++) {
    const sel = document.querySelector(`input[name="q${i}"]:checked`);
    if (!sel) { alert('Please answer all 10 questions.'); return; }
    if (sel.value === 'D') d++;
    else if (sel.value === 'E') e++;
    else b++;
  }
  // Distribute balanced scores
  d += b * 0.4;
  e += b * 0.6;
  const total = d + e;
  const dPct = Math.round((d/total)*100);
  const ePct = 100 - dPct;

  document.getElementById('designMeter').style.width = dPct + '%';
  document.getElementById('engMeter').style.width = ePct + '%';
  document.getElementById('designPct').textContent = dPct + '%';
  document.getElementById('engPct').textContent = ePct + '%';

  let title, advice;
  if (dPct >= 70) {
    title = '🎨 Strong Design Inclination — NID Could Be Your Ideal Path!';
    advice = 'Your responses indicate a strong creative and visual thinking orientation. You naturally gravitate toward design problems, aesthetics, and user experiences. NID\'s B.Des program would be an excellent fit. Start preparing for NID DAT with focus on sketching, visual reasoning, and design awareness. Consider specializations like Communication Design, Industrial Design, or UX/UI Design.';
  } else if (dPct >= 50) {
    title = '🔀 Balanced Profile — Consider Design-Tech Intersection!';
    advice = 'You show appreciation for both technical and creative thinking. This makes you ideal for emerging fields at the intersection of design and technology — UX/UI Design, Interaction Design, or Design Engineering. Consider NID for a design foundation, or explore programs like B.Des at IIT (IDC), MIT Institute of Design, or Srishti that blend both worlds.';
  } else {
    title = '⚙️ Strong Engineering Inclination — Technical Path Recommended!';
    advice = 'Your responses suggest a strong analytical and logical thinking pattern. Engineering (B.Tech/B.E.) through JEE or state exams would align well with your strengths. However, if you have even a small creative spark, consider Computer Science with a focus on UX Engineering, Game Development, or Human-Computer Interaction — fields that value both technical skills and some design sensibility.';
  }

  document.getElementById('resultTitle').textContent = title;
  document.getElementById('resultAdvice').textContent = advice;
  document.getElementById('resultBox').classList.add('show');
  document.getElementById('resultBox').scrollIntoView({ behavior: 'smooth' });
}


// ---- next <script> block ----


	const heightObserver = new ResizeObserver(([{ contentRect }]) => {
		window.parent.postMessage({ action: 'iframeHeightUpdated', height: contentRect.height, id: 'zKf-Z-' }, '*');
	});

	heightObserver.observe(document.documentElement);
