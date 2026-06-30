
/* ============================================================
   ASSESSMENT LOGIC
   ============================================================ */
const RIASEC_QUESTIONS = [
  { dim: 'R', text: 'I enjoy building or repairing physical things — circuits, engines, prototypes.' },
  { dim: 'R', text: 'Working with tools, hardware or machines gives me satisfaction.' },
  { dim: 'I', text: 'I get absorbed in investigating how a system actually works under the hood.' },
  { dim: 'I', text: 'I prefer problems where I have to think deeply and analyse data.' },
  { dim: 'A', text: 'I enjoy designing things where form and aesthetics matter, not just function.' },
  { dim: 'A', text: 'I often think about how an interface or product could be more elegant.' },
  { dim: 'S', text: 'I feel energised when I help a teammate get unblocked.' },
  { dim: 'S', text: 'I enjoy teaching or explaining technical concepts to someone newer.' },
  { dim: 'E', text: 'I like taking initiative, pitching ideas, and convincing others to back them.' },
  { dim: 'E', text: 'Leading a small team on a deadline sounds exciting, not stressful.' },
  { dim: 'C', text: 'I prefer structured tasks with clear rules and predictable outcomes.' },
  { dim: 'C', text: 'Organising data, documentation and records carefully matters to me.' }
];

const CAAS_QUESTIONS = [
  { dim: 'Concern',    text: 'I think about what my career will look like in five years.' },
  { dim: 'Concern',    text: 'I plan how to reach my academic and career goals.' },
  { dim: 'Control',    text: 'I take responsibility for my own decisions and actions.' },
  { dim: 'Control',    text: 'I rely on myself, not only luck, for how things turn out.' },
  { dim: 'Curiosity',  text: 'I actively explore new fields, tools and ideas outside my syllabus.' },
  { dim: 'Curiosity',  text: 'I investigate options before I commit to a path.' },
  { dim: 'Confidence', text: 'I believe I can overcome obstacles when learning something new.' },
  { dim: 'Confidence', text: 'I can deliver what I promise in a team project.' }
];

const SKILLS = [
  { cat: 'TECHNICAL', name: 'Mathematics & problem solving' },
  { cat: 'TECHNICAL', name: 'Core engineering fundamentals (your branch)' },
  { cat: 'TECHNICAL', name: 'Circuits, signals or mechanics (hands-on theory)' },
  { cat: 'DIGITAL',   name: 'Programming (any language)' },
  { cat: 'DIGITAL',   name: 'Data analysis (Excel / Pandas / SQL)' },
  { cat: 'DIGITAL',   name: 'Version control & collaboration (Git, GitHub)' },
  { cat: 'DIGITAL',   name: 'Cloud / DevOps basics (Docker, CI/CD)' },
  { cat: 'DIGITAL',   name: 'Applied AI / ML (any tool)' },
  { cat: 'SOFT',      name: 'Technical communication (writing, slides)' },
  { cat: 'SOFT',      name: 'Teamwork on real projects' },
  { cat: 'SOFT',      name: 'Time management & self-direction' },
  { cat: 'SOFT',      name: 'Ethics & professional judgement' },
  { cat: 'GREEN',     name: 'Sustainability & environmental design' },
  { cat: 'GREEN',     name: 'Energy-efficiency thinking in projects' },
  { cat: 'DOMAIN',    name: 'Industry awareness (who builds what)' },
  { cat: 'DOMAIN',    name: 'Regulatory / safety / standards literacy' }
];

// Render RIASEC questions
const riasecList = document.getElementById('riasecList');
RIASEC_QUESTIONS.forEach((q, i) => {
  const row = document.createElement('div');
  row.className = 'likert-row';
  row.innerHTML = `
    <p><span class="q-num">Q${String(i+1).padStart(2,'0')}</span>${q.text}</p>
    <div class="likert-opts" data-q="r${i}" data-dim="${q.dim}">
      ${[1,2,3,4,5].map(n => `<button type="button" class="likert-opt" data-v="${n}">${n}</button>`).join('')}
    </div>`;
  riasecList.appendChild(row);
});

// Render CAAS questions
const adaptList = document.getElementById('adaptList');
CAAS_QUESTIONS.forEach((q, i) => {
  const row = document.createElement('div');
  row.className = 'likert-row';
  row.innerHTML = `
    <p><span class="q-num">Q${String(i+1).padStart(2,'0')}</span>${q.text}</p>
    <div class="likert-opts" data-q="c${i}" data-dim="${q.dim}">
      ${[1,2,3,4,5].map(n => `<button type="button" class="likert-opt" data-v="${n}">${n}</button>`).join('')}
    </div>`;
  adaptList.appendChild(row);
});

// Render skills
const skillList = document.getElementById('skillList');
SKILLS.forEach((s, i) => {
  const row = document.createElement('div');
  row.className = 'skill-rate-row';
  row.innerHTML = `
    <div><span class="skill-cat">${s.cat}</span><span class="skill-name">${s.name}</span></div>
    <div class="likert-opts" data-q="s${i}" data-cat="${s.cat}">
      ${[0,1,2,3,4,5].map(n => `<button type="button" class="likert-opt" data-v="${n}">${n}</button>`).join('')}
    </div>`;
  skillList.appendChild(row);
});

// Handle likert clicks (event delegation)
document.addEventListener('click', (e) => {
  if (e.target.matches('.likert-opt')) {
    const parent = e.target.parentElement;
    parent.querySelectorAll('.likert-opt').forEach(b => b.classList.remove('selected'));
    e.target.classList.add('selected');
  }
});

// Chip selection logic
document.querySelectorAll('.chip-group').forEach(group => {
  group.addEventListener('click', e => {
    if (!e.target.matches('.chip')) return;
    const chip = e.target;
    if (group.dataset.single) {
      group.querySelectorAll('.chip').forEach(c => c.classList.remove('selected'));
      chip.classList.add('selected');
    } else if (group.dataset.multi) {
      const max = parseInt(group.dataset.max, 10);
      const selected = group.querySelectorAll('.chip.selected').length;
      if (chip.classList.contains('selected')) {
        chip.classList.remove('selected');
      } else if (selected < max) {
        chip.classList.add('selected');
      }
    }
  });
});

// Parental consent conditional
document.getElementById('f-minor').addEventListener('change', e => {
  document.getElementById('parentConsent').style.display = e.target.value === 'yes' ? 'block' : 'none';
});

// Step navigation
let currentStep = 1;
const TOTAL_STEPS = 6;

function updateStep() {
  document.querySelectorAll('.step').forEach(s => s.classList.remove('active'));
  document.querySelector(`.step[data-step="${currentStep}"]`).classList.add('active');
  document.getElementById('stepNum').textContent = currentStep;
  document.getElementById('progressFill').style.width = `${(currentStep / TOTAL_STEPS) * 100}%`;
  document.getElementById('btnPrev').style.visibility = currentStep > 1 ? 'visible' : 'hidden';
  const nextBtn = document.getElementById('btnNext');
  nextBtn.innerHTML = currentStep === TOTAL_STEPS
    ? 'Submit & generate preview <span class="arrow">→</span>'
    : 'Continue <span class="arrow">→</span>';
  document.getElementById('assessmentWrap').scrollIntoView({ behavior: 'smooth', block: 'start' });
}
function nextStep() {
  if (currentStep < TOTAL_STEPS) {
    currentStep++; updateStep();
  } else {
    submitAssessment();
  }
}
function prevStep() { if (currentStep > 1) { currentStep--; updateStep(); } }

function submitAssessment() {
  const consent = document.getElementById('f-consent').checked;
  if (!consent) { alert('Please tick the data consent box to continue. Your data is never stored without consent.'); return; }
  const minor = document.getElementById('f-minor').value === 'yes';
  if (minor && !document.getElementById('f-parent-consent').checked) {
    alert('Since the student is under 18, parental consent is required.'); return;
  }
  // Quick validation
  const name = document.getElementById('f-name').value.trim();
  if (!name) { alert('Please provide a name on step 1.'); currentStep = 1; updateStep(); return; }

  // Simulate submission success
  const id = 'EA-2026-' + Date.now().toString().slice(-6);
  alert(`✓ Assessment submitted successfully!\n\nYour Assessment ID: ${id}\n\nYour report is queued for expert review. You'll receive the full 12-page PDF within 2 working days.\n\nScroll down to view the sample report layout.`);
  document.getElementById('report').scrollIntoView({ behavior: 'smooth' });
}

/* ============================================================
   FAQ behaviour
   ============================================================ */
function toggleFAQ(header) {
  const item = header.closest('.faq-item');
  const isOpen = item.classList.contains('open');
  document.querySelectorAll('.faq-item.open').forEach(i => i.classList.remove('open'));
  if (!isOpen) item.classList.add('open');
}
document.querySelectorAll('.faq-cat-tab').forEach(tab => {
  tab.addEventListener('click', () => {
    document.querySelectorAll('.faq-cat-tab').forEach(t => t.classList.remove('active'));
    tab.classList.add('active');
    const cat = tab.dataset.cat;
    document.querySelectorAll('.faq-item').forEach(item => {
      item.style.display = (cat === 'all' || item.dataset.cat === cat) ? '' : 'none';
    });
  });
});

/* ============================================================
   REPORT CHARTS (using Chart.js)
   ============================================================ */
// Defer so page is responsive first
window.addEventListener('load', () => {
  const navy = '#0E3A8A';
  const orange = '#FF6B0A';
  const ink = '#0E1B3D';
  const muted = '#5A6278';

  // RIASEC radar
  new Chart(document.getElementById('riasecChart'), {
    type: 'radar',
    data: {
      labels: ['Realistic', 'Investigative', 'Artistic', 'Social', 'Enterprising', 'Conventional'],
      datasets: [{
        label: 'Aanya',
        data: [4.2, 4.6, 3.8, 2.4, 2.2, 2.0],
        backgroundColor: 'rgba(14,58,138,.18)',
        borderColor: navy,
        borderWidth: 2,
        pointBackgroundColor: orange,
        pointBorderColor: 'white',
        pointRadius: 4,
        pointHoverRadius: 6
      }]
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        r: {
          min: 0, max: 5,
          ticks: { stepSize: 1, color: muted, backdropColor: 'transparent', font: { size: 10 } },
          grid: { color: 'rgba(14,27,61,.08)' },
          angleLines: { color: 'rgba(14,27,61,.08)' },
          pointLabels: { color: ink, font: { size: 11, weight: '600', family: 'Plus Jakarta Sans' } }
        }
      }
    }
  });

  // CAAS radar
  new Chart(document.getElementById('caasChart'), {
    type: 'radar',
    data: {
      labels: ['Concern', 'Control', 'Curiosity', 'Confidence'],
      datasets: [{
        label: 'You',
        data: [3.2, 4.0, 4.2, 4.0],
        backgroundColor: 'rgba(255,107,10,.18)',
        borderColor: orange, borderWidth: 2,
        pointBackgroundColor: navy, pointBorderColor: 'white', pointRadius: 5, pointHoverRadius: 7
      }, {
        label: 'Peer avg',
        data: [3.5, 3.4, 3.3, 3.4],
        backgroundColor: 'transparent',
        borderColor: muted, borderWidth: 1.5, borderDash: [4, 4],
        pointRadius: 0
      }]
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      plugins: { legend: { position: 'bottom', labels: { color: ink, font: { size: 11 } } } },
      scales: {
        r: {
          min: 0, max: 5,
          ticks: { stepSize: 1, color: muted, backdropColor: 'transparent', font: { size: 10 } },
          grid: { color: 'rgba(14,27,61,.08)' },
          angleLines: { color: 'rgba(14,27,61,.08)' },
          pointLabels: { color: ink, font: { size: 11, weight: '600' } }
        }
      }
    }
  });

  // Skill radar (current vs target)
  new Chart(document.getElementById('skillRadar'), {
    type: 'radar',
    data: {
      labels: ['Embedded C', 'ML / Py', 'Signals / DSP', 'Git/DevOps', 'Communication', 'Teamwork', 'Green design'],
      datasets: [{
        label: 'Current',
        data: [2, 3, 3, 2, 3, 4, 2],
        backgroundColor: 'rgba(14,58,138,.18)',
        borderColor: navy, borderWidth: 2,
        pointBackgroundColor: navy, pointRadius: 4
      }, {
        label: 'Target (Embedded-AI role)',
        data: [5, 4, 4, 4, 4, 4, 3],
        backgroundColor: 'rgba(255,107,10,.15)',
        borderColor: orange, borderWidth: 2, borderDash: [5, 3],
        pointBackgroundColor: orange, pointRadius: 4
      }]
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      plugins: { legend: { position: 'bottom', labels: { color: ink, font: { size: 11 } } } },
      scales: {
        r: {
          min: 0, max: 5,
          ticks: { stepSize: 1, color: muted, backdropColor: 'transparent', font: { size: 10 } },
          grid: { color: 'rgba(14,27,61,.08)' },
          angleLines: { color: 'rgba(14,27,61,.08)' },
          pointLabels: { color: ink, font: { size: 11, weight: '600' } }
        }
      }
    }
  });

  // Heatmap: gap intensities (0-4 scale)
  const heatData = {
    'heat-tech':  [1, 2, 3, 2, 1],   // mid gaps
    'heat-digi':  [3, 3, 4, 4, 3],   // big gaps
    'heat-soft':  [2, 2, 1, 1, 1],   // smaller
    'heat-green': [3, 2, 3, 3, 2],   // moderate-high
    'heat-dom':   [2, 2, 3, 2, 2]
  };
  Object.entries(heatData).forEach(([id, values]) => {
    const el = document.getElementById(id);
    if (!el) return;
    values.forEach(v => {
      const intensity = v / 4;
      // interpolate from cream to orange/red
      const r = Math.round(251 - (251 - 194) * intensity);
      const g = Math.round(247 - (247 - 58)  * intensity);
      const b = Math.round(238 - (238 - 58)  * intensity);
      const cell = document.createElement('div');
      cell.className = 'heat-cell';
      cell.style.background = `rgb(${r},${g},${b})`;
      cell.style.color = intensity > 0.5 ? 'white' : '#6B5E3D';
      cell.textContent = v;
      el.appendChild(cell);
    });
  });
});

/* ============================================================
   Scroll reveal (light touch)
   ============================================================ */
const obs = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) e.target.classList.add('visible'); }), { threshold: .08 });
document.querySelectorAll('section > .container > *').forEach(el => { el.classList.add('reveal'); obs.observe(el); });

// Close mobile menu on nav click
document.querySelectorAll('#menu a').forEach(a => a.addEventListener('click', () => document.getElementById('menu').classList.remove('open')));

;

	const heightObserver = new ResizeObserver(([{ contentRect }]) => {
		window.parent.postMessage({ action: 'iframeHeightUpdated', height: contentRect.height, id: 'zR2i2E' }, '*');
	});

	heightObserver.observe(document.documentElement);
