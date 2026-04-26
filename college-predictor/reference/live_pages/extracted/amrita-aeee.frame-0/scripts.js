
// ═══ CAMPUS DATA ═══
const campuses = [
  { name:"Coimbatore", state:"Tamil Nadu", pref:95, area:"400 acres", highlight:"Flagship campus, most branches, Olympic pool, 81,000 sq.ft library", branches:"CSE, ECE, ME, CE, AE, EEE, Chemical, Cyber Security", tip:"Best for: students wanting maximum branch options & research" },
  { name:"Bengaluru", state:"Karnataka", pref:88, area:"Urban campus", highlight:"Tech hub proximity, strong CSE & IT placements, metro city access", branches:"CSE, ECE, EEE, ME, Civil", tip:"Best for: students wanting city life & tech industry exposure" },
  { name:"Amritapuri", state:"Kerala", pref:78, area:"Serene campus", highlight:"Strong research, amFOSS coding club, peaceful learning environment", branches:"CSE, ECE, EEE, ME", tip:"Best for: students focused on research & deep learning" },
  { name:"Chennai", state:"Tamil Nadu", pref:72, area:"Vengal, rural-suburban", highlight:"Growing campus, industrial exposure, Tamil Nadu state quota benefits", branches:"CSE, ECE, EEE, ME", tip:"Best for: TN students wanting proximity to industrial zones" },
  { name:"Amaravati", state:"Andhra Pradesh", pref:65, area:"Newest campus", highlight:"Modern infrastructure, rapidly growing, competitive entry ranks", branches:"CSE, AI&DS, ECE, EEE", tip:"Best for: students wanting newer campus with modern facilities" },
  { name:"Faridabad", state:"Haryana (NCR)", pref:60, area:"130-acre health city", highlight:"Attached 2000-bed Amrita Hospital, NCR Delhi region access", branches:"CSE, ECE, EEE", tip:"Best for: students in North India wanting NCR location" },
  { name:"Nagercoil", state:"Tamil Nadu", pref:55, area:"Southern tip campus", highlight:"Peaceful, strong community, value engineering education", branches:"CSE, ECE, ME, EEE", tip:"Best for: focused learning in a quiet setting" },
  { name:"Haridwar", state:"Uttarakhand", pref:50, area:"Spiritual & scenic", highlight:"Unique location, same centralized placements, growing programs", branches:"CSE, ECE, EEE", tip:"Best for: students wanting North India + spiritual campus" }
];
const cg = document.getElementById('campus-grid');
campuses.forEach(c => {
  cg.innerHTML += `<div class="card">
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px">
      <h4 style="margin:0">${c.name}</h4>
      <span class="badge badge-blue">${c.state}</span>
    </div>
    <div class="progress-ring">
      <span style="font-size:12px;font-weight:700;color:var(--gray);min-width:90px">Preference: ${c.pref}%</span>
      <div class="bar-bg"><div class="bar-fill" style="width:${c.pref}%"></div></div>
    </div>
    <p style="font-size:13px;margin-bottom:6px"><strong>Area:</strong> ${c.area}</p>
    <p style="font-size:13px;margin-bottom:6px"><strong>Highlight:</strong> ${c.highlight}</p>
    <p style="font-size:12px;margin-bottom:6px;color:var(--gray)"><strong>Branches:</strong> ${c.branches}</p>
    <p style="font-size:12px;background:var(--orange-light);padding:6px 10px;border-radius:8px;color:var(--orange);font-weight:600;margin-top:8px">💡 ${c.tip}</p>
  </div>`;
});

// ═══ SKILLS QUIZ ═══
const quizData = [
  { q:"How interested are you in programming & coding?", b:["CSE","AI & Data Science","CSE (AI)"] },
  { q:"How comfortable are you with advanced mathematics?", b:["CSE","ECE","EEE","Aerospace"] },
  { q:"Do you enjoy working with electronic circuits & hardware?", b:["ECE","EEE"] },
  { q:"Are you interested in designing machines or structures?", b:["Mechanical","Civil","Aerospace"] },
  { q:"Do you like data analysis and finding patterns?", b:["AI & Data Science","CSE (AI)"] },
  { q:"Are you fascinated by aircraft, space & aerodynamics?", b:["Aerospace"] },
  { q:"Do you enjoy chemistry and chemical processes?", b:["Chemical Engineering"] },
  { q:"How interested are you in AI, ML & automation?", b:["AI & Data Science","CSE (AI)","CSE"] },
];
let quizAnswers = {};
const qc = document.getElementById('quiz-container');
function renderQuiz() {
  let h = '';
  quizData.forEach((q,i) => {
    h += `<div class="card quiz-q" style="margin-bottom:14px">
      <div class="q-text">${i+1}. ${q.q}</div>
      <div class="quiz-btns">
        ${[1,2,3,4,5].map(v => `<button onclick="selectQ(${i},${v},this)" ${quizAnswers[i]===v?'class="selected"':''}>${v}</button>`).join('')}
        <span class="quiz-hint">1=Low, 5=High</span>
      </div>
    </div>`;
  });
  const allDone = Object.keys(quizAnswers).length === quizData.length;
  h += `<div style="text-align:center;margin-top:20px"><button class="btn-primary" onclick="showResults()" ${allDone?'':'disabled'}>🎯 Get My Branch Recommendation</button></div>`;
  qc.innerHTML = h;
}
function selectQ(idx, val, el) {
  quizAnswers[idx] = val;
  renderQuiz();
}
function showResults() {
  const scores = {};
  Object.entries(quizAnswers).forEach(([idx,val]) => {
    quizData[idx].b.forEach(b => { scores[b] = (scores[b]||0) + val; });
  });
  const sorted = Object.entries(scores).sort((a,b) => b[1]-a[1]).slice(0,3);
  let h = '<div class="card" style="border:2px solid var(--orange);padding:28px"><h4 style="text-align:center;font-size:20px;margin-bottom:20px">🎯 Your Recommended Branches</h4>';
  const medals = ['🥇','🥈','🥉'];
  sorted.forEach(([name,score],i) => {
    const max = quizData.reduce((s,q) => s + (q.b.includes(name)?5:0), 0);
    const pct = Math.round((score/max)*100);
    const grad = i===0 ? 'var(--orange),#FF6B2B' : 'var(--blue),#2563EB';
    h += `<div style="margin-bottom:14px"><div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px"><span style="font-weight:800;color:${i===0?'var(--orange)':'var(--blue)'};font-size:16px">${medals[i]} ${name}</span><span style="font-weight:700;color:var(--gray);font-size:13px">${pct}% match</span></div><div class="result-bar"><div class="result-fill" style="width:${pct}%;background:linear-gradient(90deg,${grad})"></div></div></div>`;
  });
  h += `<div style="text-align:center;margin-top:20px;padding:14px;background:var(--off-white);border-radius:10px"><p style="font-size:14px;color:var(--gray);margin-bottom:6px">Want detailed, personalized counselling?</p><a href="mailto:contact@eduaakashaa.com" style="font-weight:800;font-size:15px">✉ contact@eduaakashaa.com</a></div></div>`;
  h += `<div style="text-align:center;margin-top:16px"><button onclick="quizAnswers={};renderQuiz()" style="font-family:'Outfit',sans-serif;font-size:14px;font-weight:700;padding:10px 28px;border-radius:24px;border:2px solid var(--blue);background:var(--white);color:var(--blue);cursor:pointer">↻ Retake Assessment</button></div>`;
  qc.innerHTML = h;
}
renderQuiz();

// ═══ FAQ ═══
const faqs = [
  { cat:'nri', q:'Can NRI students get direct admission without AEEE?', a:'Yes. OCI/PIO students and Indian students who completed Class 12 abroad with NRI-status parents are exempt from AEEE and can apply directly through the NRI quota at any of the 8 engineering campuses.' },
  { cat:'nri', q:'What is the NRI fee structure for B.Tech?', a:'NRI tuition fee is approximately USD 7,000 per year. Hostel and mess charges are additional. Payment can be made via international wire transfer or demand draft.' },
  { cat:'nri', q:'Do NRI students need SAT scores?', a:'SAT scores can be used as an alternative admission route. However, NRI/OCI/PIO status itself qualifies for direct admission without any entrance exam.' },
  { cat:'nri', q:'What documents are needed for NRI quota?', a:'Valid passport, OCI/PIO card, Class 12 mark sheets, parent\'s NRI status proof, passport-size photos, and address proof. All documents must be attested.' },
  { cat:'nri', q:'Are NRI students eligible for scholarships?', a:'NRI scholarship programs are separate from AEEE-based scholarships. Contact the Directorate of Admissions at Amrita or email contact@eduaakashaa.com for guidance.' },
  { cat:'nri', q:'Can NRI students choose any campus?', a:'Yes, NRI students can opt for any of the 8 campuses — Coimbatore, Bengaluru, Chennai, Amritapuri, Amaravati, Faridabad, Nagercoil, and Haridwar.' },
  { cat:'gen', q:'What is CSAP counselling?', a:'CSAP (Centralized Seat Allotment Process) is held online after results. Register with ₹5,000, fill campus and branch preferences, seats allocated based on rank across multiple rounds.' },
  { cat:'gen', q:'Is it mandatory to attend both Phase 1 and Phase 2?', a:'No. You can attend either or both. Your best score across phases is considered for ranking. Phase 2 costs an additional ₹600.' },
  { cat:'exam', q:'Can I apply through both AEEE and JEE Main?', a:'Yes. Register for both during the AEEE application — no additional fee. 70% seats via AEEE, 30% via JEE Main. Separate merit lists are prepared.' },
  { cat:'fee', q:'How are scholarships maintained after admission?', a:'Slab 1 requires ≥8.0 CGPA; Slab 2 requires ≥7.5 CGPA. If CGPA drops, you move to a higher fee slab. No disciplinary issues should be on record.' },
  { cat:'gen', q:'What happens if I don\'t get a seat in CSAP?', a:'If you don\'t receive any preference in the last CSAP round, your ₹5,000 registration fee is refunded. You may also contact admissions for non-scholarship/institutional seats.' },
  { cat:'gen', q:'Is Amrita recognized and accredited?', a:'Yes. NAAC A++ (highest grade), UGC recognized, Institute of Eminence by Govt. of India, NIRF #8 University, QS World 1001-1200, AACSB accredited (Business School).' },
  { cat:'exam', q:'What is the new exam pattern change for 2026?', a:'A new Quantitative Aptitude section (10 questions, 30 marks) has been added. Physics reduced from 30 to 25 questions, Chemistry from 25 to 20. Total remains 100 questions, 300 marks.' },
  { cat:'fee', q:'What is the non-scholarship fee for B.Tech?', a:'Non-scholarship (institutional quota) fee is approximately ₹6,00,000 per year. These seats are based on Class 12 PCM marks without entrance exam. Not donation-based.' },
  { cat:'exam', q:'What are the AEEL exam details?', a:'AEEL is a 2-hour CBT with 80 questions covering Physics, Chemistry, Biology and English. For admission to Nursing, Pharmacy, Agriculture and Allied Health programs.' },
  { cat:'fee', q:'Are education loans available for Amrita?', a:'Yes. Amrita has partnerships with banks like Bank of Baroda and Dhanalakshmi Bank for education loans. Installment payment options are available through the university portal.' },
];
function renderFaqs(filter) {
  const fl = document.getElementById('faq-list');
  const filtered = filter==='all' ? faqs : faqs.filter(f=>f.cat===filter);
  fl.innerHTML = filtered.map((f,i) => {
    const catLabel = {nri:'🌍 NRI',gen:'📋 General',fee:'💰 Fees',exam:'📝 Exam'}[f.cat];
    const catClass = {nri:'badge-purple',gen:'badge-blue',fee:'badge-orange',exam:'badge-green'}[f.cat];
    return `<div class="faq-item" onclick="toggleFaq(this)">
      <div class="faq-q"><div style="display:flex;align-items:center;gap:10px"><span class="badge ${catClass}">${catLabel}</span><span>${f.q}</span></div><span class="toggle">+</span></div>
      <div class="faq-a">${f.a}</div>
    </div>`;
  }).join('');
}
function toggleFaq(el) { el.classList.toggle('open'); }
function filterFaq(cat, btn) {
  document.querySelectorAll('.faq-filters button').forEach(b=>b.classList.remove('active'));
  btn.classList.add('active');
  renderFaqs(cat);
}
renderFaqs('all');


// ---- next <script> block ----


	const heightObserver = new ResizeObserver(([{ contentRect }]) => {
		window.parent.postMessage({ action: 'iframeHeightUpdated', height: contentRect.height, id: 'zIZdjU' }, '*');
	});

	heightObserver.observe(document.documentElement);
