// ======== JOSAA Portal — Server-Side API Version ========

// ======== INSTITUTE TYPE (client helper) ========
function getType(name) {
  if (/Indian Institute of Technology/i.test(name) && !/Information/i.test(name)) return 'IIT';
  if (/National Institute of Technology/i.test(name)) return 'NIT';
  if (/Indian Institute of Information Technology/i.test(name) || /\bIIIT\b/i.test(name)) return 'IIIT';
  return 'GFTI';
}

// ======== PAGE NAVIGATION ========
function showPage(id, btn) {
  document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
  document.getElementById('page-' + id).classList.add('active');
  if (btn) btn.classList.add('active');
  if (id === 'analytics') initCharts();
  if (id === 'matrix') renderMatrix();
  if (id === 'nirf') initNIRF();
  if (id === 'insights') renderInsights();
}

// ======== TAB SYSTEM ========
function switchTab(page, tabId, btn) {
  const page_el = document.getElementById('page-' + page);
  page_el.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));
  page_el.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  document.getElementById(tabId).classList.add('active');
  btn.classList.add('active');
}

// ======== POPULATE SELECTS (from API) ========
function populateBranches() {
  fetch('/api/josaa/meta')
    .then(r => r.json())
    .then(data => {
      const seen = new Set();
      const opts = data.programs.map(p => {
        const s = p.replace(/\s*\(\d+ Years.*$/, '').trim();
        if (seen.has(s)) return '';
        seen.add(s);
        return `<option value="${s}">${s}</option>`;
      }).join('');
      ['branchInput', 'matBranch'].forEach(id => {
        const el = document.getElementById(id);
        if (el) el.innerHTML = '<option value="">All Branches</option>' + opts;
      });
    });
}

// ======== PREDICTOR (server-side filtering) ========
let allResults = [];
let rPage = 1;
const PER_PAGE = 25;

function runPredictor() {
  const rank = parseInt(document.getElementById('rankInput').value);
  if (!rank || rank < 1) { alert('Enter a valid JEE rank!'); return; }

  const cat = document.getElementById('catInput').value;
  const gender = document.getElementById('genderInput').value;
  const quota = document.getElementById('quotaInput').value;
  const instType = document.getElementById('typeInput').value;
  const branch = document.getElementById('branchInput').value;
  const buf = document.getElementById('showBuffer').checked ? '1' : '0';

  const params = new URLSearchParams({
    rank, cat, gender, quota, instType, branch, buffer: buf
  });

  document.getElementById('resultsArea').style.display = 'none';
  document.getElementById('emptyState').style.display = 'none';

  fetch('/api/josaa/predict?' + params)
    .then(r => r.json())
    .then(data => {
      allResults = data;
      rPage = 1;
      rerenderResults();
    });
}

function rerenderResults() {
  const sort = document.getElementById('sortSelect').value;
  const chMap = { safe: 0, moderate: 1, reach: 2, longshot: 3 };
  if (sort === 'nirf') allResults.sort((a, b) => a.nirfRank - b.nirfRank);
  else if (sort === 'open') allResults.sort((a, b) => a.open - b.open);
  else if (sort === 'close') allResults.sort((a, b) => a.close - b.close);
  else allResults.sort((a, b) => chMap[a.chance] - chMap[b.chance] || a.nirfRank - b.nirfRank);

  const total = allResults.length;
  document.getElementById('resultsArea').style.display = total ? 'block' : 'none';
  document.getElementById('emptyState').style.display = total ? 'none' : 'block';
  if (!total) return;

  document.getElementById('resultsCount').textContent = `${total} colleges found | Page ${rPage}/${Math.ceil(total / PER_PAGE)}`;

  const start = (rPage - 1) * PER_PAGE;
  const slice = allResults.slice(start, start + PER_PAGE);

  document.getElementById('resultsBody').innerHTML = slice.map((r, i) => {
    const progShort = r.prog.replace(/\s*\(\d+ Years.*$/, '').trim();
    const nirfDisp = r.nirfRank < 9999 ? `<span class="nirf-badge">#${r.nirfRank}</span>` : '<span style="color:var(--muted)">—</span>';
    return `<tr>
      <td style="color:var(--muted);font-size:11px">${start + i + 1}</td>
      <td><div style="font-weight:700;font-size:12px;color:var(--blue-dark)">${r.inst}</div></td>
      <td><div style="font-size:12px">${progShort}</div></td>
      <td><span class="tag tag-${r.instType.toLowerCase()}">${r.instType}</span></td>
      <td style="font-size:11px;color:var(--muted)">${r.q}</td>
      <td style="font-weight:700;color:var(--blue-dark)">${r.open.toLocaleString()}</td>
      <td style="font-weight:700;color:var(--orange-dark)">${r.close.toLocaleString()}</td>
      <td><span class="chance ${r.chance}">${r.chance === 'safe' ? '✅ Safe' : r.chance === 'moderate' ? '⚡ Moderate' : r.chance === 'reach' ? '🎯 Reach' : '🔴 Long Shot'}</span></td>
      <td>${nirfDisp}</td>
    </tr>`;
  }).join('');

  renderPagination(total);
}

function renderPagination(total) {
  const pages = Math.ceil(total / PER_PAGE);
  if (pages <= 1) { document.getElementById('pagination').innerHTML = ''; return; }
  let h = `<button class="pg-btn" ${rPage === 1 ? 'disabled' : ''} onclick="goPg(${rPage - 1})">‹</button>`;
  const start = Math.max(1, rPage - 3), end = Math.min(pages, rPage + 3);
  if (start > 1) h += `<button class="pg-btn" onclick="goPg(1)">1</button><span style="color:var(--muted);font-size:12px">…</span>`;
  for (let i = start; i <= end; i++) h += `<button class="pg-btn ${i === rPage ? 'active' : ''}" onclick="goPg(${i})">${i}</button>`;
  if (end < pages) h += `<span style="color:var(--muted);font-size:12px">…</span><button class="pg-btn" onclick="goPg(${pages})">${pages}</button>`;
  h += `<button class="pg-btn" ${rPage === pages ? 'disabled' : ''} onclick="goPg(${rPage + 1})">›</button>`;
  h += `<span style="font-size:11px;color:var(--muted);margin-left:4px">Total: ${total}</span>`;
  document.getElementById('pagination').innerHTML = h;
}

function goPg(p) { rPage = p; rerenderResults(); document.getElementById('resultsArea').scrollIntoView({ behavior: 'smooth', block: 'nearest' }); }

// ======== MATRIX (server-side) ========
function renderMatrix() {
  const search = (document.getElementById('matSearch').value || '');
  const type = document.getElementById('matType').value;
  const cat = document.getElementById('matCat').value;
  const branch = document.getElementById('matBranch').value;
  const quota = document.getElementById('matQuota').value;

  const params = new URLSearchParams({ cat, quota, type, branch, search });

  fetch('/api/josaa/matrix?' + params)
    .then(r => r.json())
    .then(data => {
      const { branches, rows } = data;
      if (!rows.length) {
        document.getElementById('matrixWrap').innerHTML = '<div style="padding:24px;text-align:center;color:var(--muted)">No data. Adjust filters.</div>';
        return;
      }

      const getRankBg = c => c <= 5000 ? '#D1FAE5' : c <= 20000 ? '#DBEAFE' : c <= 50000 ? '#FEF3C7' : c <= 150000 ? '#FCE7F3' : '#F9FAFB';

      let tbl = '<table style="width:100%;border-collapse:collapse;font-size:11px"><thead><tr>';
      tbl += '<th style="background:var(--blue-dark);color:#fff;padding:9px 12px;text-align:left;position:sticky;left:0;z-index:3;min-width:200px">Institute</th>';
      tbl += '<th style="background:var(--blue-dark);color:#fff;padding:9px 8px;min-width:65px">NIRF</th>';
      tbl += '<th style="background:var(--blue-dark);color:#fff;padding:9px 8px;min-width:55px">Type</th>';
      branches.forEach(b => {
        const s = b.replace(/\s*\(\d+ Years.*$/, '').trim()
          .replace('Computer Science and Engineering', 'CSE')
          .replace('Electronics and Communication Engineering', 'ECE')
          .replace('Electrical Engineering', 'EE').replace('Mechanical Engineering', 'ME')
          .replace('Civil Engineering', 'CE').replace('Chemical Engineering', 'ChE')
          .replace('Mathematics and Computing', 'M&C').replace('Information Technology', 'IT')
          .replace('Artificial Intelligence', 'AI').replace('Data Science and Artificial Intelligence', 'DS/AI');
        tbl += `<th style="background:var(--blue-dark);color:#fff;padding:9px 6px;text-align:center;min-width:80px" title="${b}">${s}</th>`;
      });
      tbl += '</tr></thead><tbody>';

      rows.forEach((row, idx) => {
        const bg = idx % 2 === 0 ? '#fff' : '#F8FAFF';
        tbl += `<tr style="background:${bg}">`;
        tbl += `<td style="padding:7px 12px;font-weight:700;font-size:11px;color:var(--blue-dark);position:sticky;left:0;background:${bg};border-right:2px solid var(--border)">${row.inst}</td>`;
        tbl += `<td style="padding:7px 6px;text-align:center">${row.nirfRank ? `<span class="nirf-badge">#${row.nirfRank}</span>` : '—'}</td>`;
        tbl += `<td style="padding:7px 6px;text-align:center"><span class="tag tag-${row.instType.toLowerCase()}">${row.instType}</span></td>`;
        branches.forEach(b => {
          const d = row.branches[b];
          if (d) {
            tbl += `<td style="padding:5px 6px;text-align:center;background:${getRankBg(d.c)};border:1px solid rgba(0,0,0,0.04)">
              <div style="font-weight:700;color:var(--blue-dark)">${d.c.toLocaleString()}</div>
              <div style="font-size:9px;color:var(--muted)">${d.o.toLocaleString()}</div>
            </td>`;
          } else tbl += `<td style="padding:5px;text-align:center;color:var(--muted)">—</td>`;
        });
        tbl += '</tr>';
      });
      tbl += '</tbody></table><div style="padding:8px 14px;font-size:10px;color:var(--muted);background:#f9fafb;border-top:1px solid var(--border)">🟢≤5K &nbsp;🔵≤20K &nbsp;🟡≤50K &nbsp;🩷≤1.5L &nbsp;⚪>1.5L | Bold = Closing Rank | Small = Opening Rank | Sorted by NIRF</div>';
      document.getElementById('matrixWrap').innerHTML = tbl;
    });
}

// ======== NIRF (server-side) ========
let nirfInited = false;
function initNIRF() {
  if (nirfInited) return;
  nirfInited = true;
  // Hide state filter since CSV has no state data
  const el = document.getElementById('nirfState');
  if (el) el.style.display = 'none';
  renderNIRF();
}

function renderNIRF() {
  const q = (document.getElementById('nirfSearch').value || '');
  const maxR = parseInt(document.getElementById('nirfRange').value) || 9999;

  const params = new URLSearchParams({ q, maxRank: maxR });

  fetch('/api/josaa/nirf?' + params)
    .then(r => r.json())
    .then(fil => {
      document.getElementById('nirfList').innerHTML = fil.map(n => {
        const rc = n.Rank === 1 ? 'r1' : n.Rank === 2 ? 'r2' : n.Rank === 3 ? 'r3' : '';
        const pct = Math.max(0, 100 - n.Rank * 0.3).toFixed(0);
        return `<div class="nirf-row">
          <div class="nirf-rank ${rc}">#${n.Rank}</div>
          <div style="flex:1"><div style="font-weight:700;font-size:12px;color:var(--blue-dark)">${n.Name}</div></div>
          <div class="nirf-bar"><div class="nirf-bar-fill" style="width:${pct}%"></div></div>
          <div class="nirf-score">#${n.Rank}</div>
        </div>`;
      }).join('') || '<div style="padding:20px;text-align:center;color:var(--muted)">No results found.</div>';
    });
}

// ======== INSIGHTS (server-side) ========
let insightsLoaded = false;
function renderInsights() {
  if (insightsLoaded) return;
  insightsLoaded = true;

  fetch('/api/josaa/insights')
    .then(r => r.json())
    .then(data => {
      const { iitBranches, nitBranches } = data;

      document.getElementById('insightsGrid').innerHTML = `
        <div class="ins-card"><div class="ins-title">🏆 IIT Branches: Easiest Entry (OPEN, Avg Closing)</div>
          ${iitBranches.map(([b, r]) => `<div class="ins-row"><span>${b.slice(0, 35)}</span><span class="ins-val">~${r.toLocaleString()}</span></div>`).join('')}</div>
        <div class="ins-card orange"><div class="ins-title">📊 NIT Branches: Avg Closing Rank (AI, OPEN)</div>
          ${nitBranches.map(([b, r]) => `<div class="ins-row"><span>${b.slice(0, 35)}</span><span class="ins-val">~${r.toLocaleString()}</span></div>`).join('')}</div>
        <div class="ins-card green"><div class="ins-title">💡 Category Advantage (CSE, Top NITs, CRL)</div>
          <div class="ins-row"><span>OPEN</span><span class="ins-val">~11,000</span></div>
          <div class="ins-row"><span>EWS</span><span class="ins-val">~15,000</span></div>
          <div class="ins-row"><span>OBC-NCL</span><span class="ins-val">~25,000</span></div>
          <div class="ins-row"><span>SC</span><span class="ins-val">~55,000</span></div>
          <div class="ins-row"><span>ST</span><span class="ins-val">~90,000</span></div>
          <div style="font-size:10px;color:var(--muted);margin-top:6px">Avg CRL closing across top-5 NITs, AI quota</div>
        </div>
        <div class="ins-card purple"><div class="ins-title">🗺️ HS Quota Advantage (NIT CSE, Your State)</div>
          <div style="font-size:11px;color:var(--text);line-height:1.9">
            <p>🔹 HS closing rank is typically <strong>15–45% lower</strong> than OS/AI</p>
            <p>🔹 Only 1 NIT per state offers HS quota</p>
            <p>🔹 Worth filling even if it's not your preferred campus</p>
            <p>🔹 Tamil Nadu: NIT Trichy & Calicut (HS)</p>
            <p>🔹 Maharashtra: VNIT Nagpur (HS)</p>
          </div>
        </div>
      `;

      // Tradeoff Chart
      const ctx1 = document.getElementById('chartTradeoff');
      if (ctx1 && !ctx1._drawn) {
        ctx1._drawn = true;
        new Chart(ctx1, {
          type: 'bar',
          data: {
            labels: ['NIT Trichy\nCSE', 'NIT Surathkal\nCSE', 'NIT Surathkal\nMech', 'NIT Warangal\nCSE', 'NIT Warangal\nMech', 'NIT Calicut\nCSE', 'NIT Calicut\nECE', 'NIT Silchar\nCSE'],
            datasets: [
              { label: 'Avg Closing Rank (OPEN,AI)', data: [11000, 18000, 42000, 14000, 35000, 20000, 28000, 44000], backgroundColor: ['#1E4DB7', '#1E4DB7', '#F97316', '#1E4DB7', '#F97316', '#1E4DB7', '#F97316', '#10B981'], borderRadius: 4 },
            ]
          },
          options: { responsive: true, plugins: { legend: { display: false }, tooltip: { callbacks: { label: ctx => ` Closing: ${ctx.raw.toLocaleString()}` } } }, scales: { y: { title: { display: true, text: 'Avg Closing Rank' }, grid: { color: 'rgba(0,0,0,0.05)' } } } }
        });
      }

      const ctx2 = document.getElementById('chartSalary');
      if (ctx2 && !ctx2._drawn) {
        ctx2._drawn = true;
        new Chart(ctx2, {
          type: 'radar',
          data: {
            labels: ['Campus Placement', 'Avg Package (LPA)', 'Top Package', 'Industry Demand', 'Research Scope', 'Entrepreneurship'],
            datasets: [
              { label: 'NIT Trichy (Any Branch)', data: [9, 8, 7, 8, 9, 8], borderColor: '#1E4DB7', backgroundColor: 'rgba(30,77,183,0.12)', pointBackgroundColor: '#1E4DB7' },
              { label: 'Lower NIT CSE', data: [6, 7, 8, 9, 5, 7], borderColor: '#F97316', backgroundColor: 'rgba(249,115,22,0.12)', pointBackgroundColor: '#F97316' }
            ]
          },
          options: { responsive: true, plugins: { legend: { position: 'bottom', labels: { font: { size: 10 } } } }, scales: { r: { ticks: { display: false }, grid: { color: 'rgba(0,0,0,0.1)' } } } }
        });
      }
    });
}

// ======== CHARTS (server-side analytics) ========
let chartsInited = false;
function initCharts() {
  if (chartsInited) return;
  chartsInited = true;

  fetch('/api/josaa/analytics')
    .then(r => r.json())
    .then(data => {
      // 1. Institute type donut
      const tc = data.typeCnt;
      new Chart(document.getElementById('chartType'), {
        type: 'doughnut',
        data: {
          labels: [`IIT (${tc.IIT})`, `NIT (${tc.NIT})`, `IIIT (${tc.IIIT})`, `GFTI (${tc.GFTI})`],
          datasets: [{ data: [tc.IIT, tc.NIT, tc.IIIT, tc.GFTI], backgroundColor: ['#163896', '#1E4DB7', '#F97316', '#10B981'], borderWidth: 0 }]
        },
        options: { responsive: true, plugins: { legend: { position: 'bottom', labels: { font: { size: 11 } } } } }
      });

      // 2. Seat type pie
      new Chart(document.getElementById('chartCat'), {
        type: 'pie',
        data: {
          labels: Object.keys(data.seatCnt),
          datasets: [{ data: Object.values(data.seatCnt), backgroundColor: ['#163896', '#1E4DB7', '#F97316', '#10B981', '#8B5CF6', '#EC4899', '#F59E0B', '#06B6D4', '#EF4444', '#84CC16'], borderWidth: 0 }]
        },
        options: { responsive: true, plugins: { legend: { position: 'right', labels: { font: { size: 10 }, padding: 6 } } } }
      });

      // 3. Top branches bar
      new Chart(document.getElementById('chartBranch'), {
        type: 'bar',
        data: {
          labels: data.topBranches.map(([p]) => p),
          datasets: [{ data: data.topBranches.map(([, c]) => c), backgroundColor: 'rgba(30,77,183,0.8)', borderRadius: 4 }]
        },
        options: { indexAxis: 'y', responsive: true, plugins: { legend: { display: false } }, scales: { x: { grid: { color: 'rgba(0,0,0,0.05)' } } } }
      });

      // 4. Avg closing by type
      const typeKeys = ['IIT', 'NIT', 'IIIT', 'GFTI'];
      new Chart(document.getElementById('chartTypeAvg'), {
        type: 'bar',
        data: {
          labels: typeKeys,
          datasets: [{ label: 'Avg Closing Rank', data: typeKeys.map(t => data.typeAvg[t]), backgroundColor: ['#163896', '#1E4DB7', '#F97316', '#10B981'], borderRadius: 6 }]
        },
        options: { responsive: true, plugins: { legend: { display: false } }, scales: { y: { title: { display: true, text: 'Avg Closing Rank' } } } }
      });

      // 5. Cutoff scatter
      const colors5 = ['#163896', '#1E4DB7', '#F97316', '#10B981', '#8B5CF6', '#EC4899'];
      const scatterLabels = Object.keys(data.scatterData);
      new Chart(document.getElementById('chartCutoff'), {
        type: 'scatter',
        data: {
          datasets: scatterLabels.map((label, i) => ({
            label,
            data: data.scatterData[label],
            backgroundColor: colors5[i],
            pointRadius: 4
          }))
        },
        options: {
          responsive: true,
          plugins: {
            legend: { position: 'bottom', labels: { font: { size: 10 }, padding: 8 }, display: true },
            tooltip: { callbacks: { label: ctx => ` ${ctx.dataset.label} — ${ctx.raw.label || ''} — Rank: ${ctx.raw.y?.toLocaleString()}` } }
          },
          scales: {
            x: { title: { display: true, text: 'NIRF Rank' }, grid: { color: 'rgba(0,0,0,0.05)' } },
            y: { title: { display: true, text: 'Closing Rank (JOSAA)' }, grid: { color: 'rgba(0,0,0,0.05)' } }
          }
        }
      });

      // 6. Top 25 institutes
      new Chart(document.getElementById('chartTopInst'), {
        type: 'bar',
        data: {
          labels: data.top25.map(d => d.inst),
          datasets: [{
            label: 'Min Opening Rank', data: data.top25.map(d => d.val),
            backgroundColor: data.top25.map(d => d.type === 'IIT' ? '#163896' : d.type === 'NIT' ? '#1E4DB7' : '#F97316'),
            borderRadius: 4
          }]
        },
        options: { responsive: true, plugins: { legend: { display: false } }, scales: { x: { ticks: { font: { size: 9 }, maxRotation: 45 } }, y: { title: { display: true, text: 'Min Opening Rank' } } } }
      });

      // 7. Hidden gem
      new Chart(document.getElementById('chartGem'), {
        type: 'bar',
        data: {
          labels: data.gemData.map(d => d.inst),
          datasets: [
            { label: 'CSE Closing Rank', data: data.gemData.map(d => d.cse), backgroundColor: 'rgba(249,115,22,0.85)', borderRadius: 4 },
            { label: 'Mechanical Closing Rank', data: data.gemData.map(d => d.mech), backgroundColor: 'rgba(30,77,183,0.7)', borderRadius: 4 },
            { label: 'ECE Closing Rank', data: data.gemData.map(d => d.ece), backgroundColor: 'rgba(16,185,129,0.7)', borderRadius: 4 }
          ]
        },
        options: { responsive: true, plugins: { legend: { position: 'bottom', labels: { font: { size: 10 } } } }, scales: { x: { ticks: { font: { size: 9 }, maxRotation: 45 } }, y: { title: { display: true, text: 'Closing Rank' } } } }
      });

      // 8. Category advantage CSE
      new Chart(document.getElementById('chartCatAdv'), {
        type: 'bar',
        data: {
          labels: data.catAdvantage.cats,
          datasets: [{ label: 'Avg CSE Closing Rank (All Institutes, AI)', data: data.catAdvantage.vals, backgroundColor: ['#163896', '#1E4DB7', '#F97316', '#10B981', '#8B5CF6'], borderRadius: 6 }]
        },
        options: { responsive: true, plugins: { legend: { display: false } }, scales: { y: { title: { display: true, text: 'Avg Closing Rank' } } } }
      });
    });
}

// ======== FAQ ========
const faqs = [
  ['What is JOSAA and who is it for?', 'JOSAA (Joint Seat Allocation Authority) manages seat allocation for 128 institutes including IITs, NITs, IIITs, and GFTIs. It\u2019s for students who have qualified JEE Main (for NIT/IIIT/GFTI) or both JEE Main + JEE Advanced (for IITs).'],
  ['Why does this tool show IIT data with JEE Main ranks?', 'JOSAA publishes all data (including IIT) using the same rank format. IIT seats shown in JOSAA data correspond to JEE Advanced CRL ranks. IITs require JEE Advanced \u2014 not JEE Main. The rank ranges shown for IITs in this tool are JEE Advanced equivalents shown in JOSAA official data.'],
  ['What is Home State (HS) quota and how does it help?', 'HS quota reserves 50% of NIT seats for students from the state where the NIT is located. HS closing ranks can be 15\u201345% lower than All India (AI) quota. For example, if you\u2019re from Tamil Nadu, NIT Trichy\u2019s HS quota will have much lower cutoffs than AI quota.'],
  ['How many choices should I fill during JOSAA?', 'Fill as many as possible \u2014 ideally 500\u20132000 choices in order of preference. JOSAA allows up to 25,000 choices. Students who fill more choices have significantly better outcomes. Never leave slots unfilled.'],
  ['What is Float, Freeze, and Slide in JOSAA?', 'Float = Automatically upgrade to any better allotment (better college + better branch). Freeze = Stay with current allotment, no upgrade. Slide = Same institute, better branch only. Always choose Float unless you\u2019re 100% satisfied with your current seat.'],
  ['What happens if I don\u2019t pay the seat acceptance fee?', 'Your allotted seat is cancelled and you exit JOSAA. No refund. You lose your chance for that round. Always pay by midnight of the deadline even if you plan to upgrade.'],
  ['Can girls get additional seats in JOSAA?', 'Yes! Supernumerary seats for female candidates add ~20% extra seats in most IIT/NIT programs. Female-only seats have higher closing ranks (worse ranks can qualify). These are over and above regular seats.'],
  ['What is the CSAB special round?', 'After 6 JOSAA rounds, CSAB (Central Seat Allocation Board) conducts 1\u20132 special rounds for remaining vacant NIT/IIIT/GFTI seats. Separate registration needed. Good for improving college/branch after JOSAA.'],
  ['Is CSE always better than other branches?', 'Not always! A better-ranked NIT with Mechanical/ECE often outperforms a lower-ranked NIT with CSE in terms of placements, peer quality, and alumni network. Data shows that NIT Trichy Mechanical (~42K closing) has better avg placement than NIT Silchar CSE (~44K closing).'],
  ['How is NIRF ranking calculated for engineering colleges?', 'NIRF evaluates on 5 parameters: Teaching, Learning & Resources (30%), Research & Professional Practice (30%), Graduation Outcomes (20%), Outreach & Inclusivity (10%), and Perception (10%). IITs dominate Research; NITs score on Graduation Outcomes.']
];

function initFAQ() {
  const container = document.getElementById('faqContainer');
  if (!container || container.children.length) return;
  container.innerHTML = faqs.map((f, i) => `
    <div class="faq-item">
      <div class="faq-q" onclick="toggleFAQ(this)" id="fq${i}">
        <span>Q${i + 1}. ${f[0]}</span>
        <span class="arrow">▼</span>
      </div>
      <div class="faq-a" id="fa${i}">${f[1]}</div>
    </div>`).join('');
}

function toggleFAQ(el) {
  const ans = el.nextElementSibling;
  el.classList.toggle('open');
  ans.classList.toggle('open');
}

// ======== INIT ========
document.addEventListener('DOMContentLoaded', () => {
  populateBranches();
  initFAQ();
  renderNIRF();
  document.getElementById('rankInput').addEventListener('keydown', e => { if (e.key === 'Enter') runPredictor(); });
});
