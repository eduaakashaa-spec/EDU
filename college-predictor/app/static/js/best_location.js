/* ---------------- INTERSECTION OBSERVER REVEAL ---------------- */
const io = new IntersectionObserver((entries)=>{
  entries.forEach(e=>{ if(e.isIntersecting){ e.target.classList.add('visible'); io.unobserve(e.target); }});
}, {threshold:.12});
document.querySelectorAll('.reveal').forEach(el=>io.observe(el));

/* ---------------- DATA: STATES & HUBS ---------------- */
const STATE_DATA = {
  "Tamil Nadu":      { education:9.2, safety:8.6, hostel:8.4, climate:7.4, cost:7.8, airport:9.0, internship:8.6, language:8.2, nri:9.0, diversity:8.4 },
  "Karnataka":       { education:9.4, safety:7.8, hostel:8.0, climate:9.0, cost:6.5, airport:9.2, internship:9.4, language:8.6, nri:8.6, diversity:9.0 },
  "Maharashtra":     { education:9.0, safety:7.6, hostel:7.8, climate:7.8, cost:6.2, airport:9.0, internship:9.0, language:7.8, nri:8.2, diversity:8.8 },
  "Telangana":       { education:8.8, safety:8.0, hostel:8.0, climate:7.0, cost:7.2, airport:8.8, internship:8.6, language:8.4, nri:8.4, diversity:8.4 },
  "Delhi":           { education:8.6, safety:6.6, hostel:7.2, climate:6.0, cost:6.0, airport:9.4, internship:8.6, language:8.0, nri:8.2, diversity:8.6 },
  "Gujarat":         { education:8.0, safety:8.8, hostel:7.6, climate:6.8, cost:7.4, airport:8.0, internship:7.4, language:7.0, nri:8.6, diversity:7.4 },
  "Andhra Pradesh":  { education:8.2, safety:7.8, hostel:7.6, climate:7.0, cost:7.8, airport:7.6, internship:7.6, language:7.6, nri:7.6, diversity:7.4 },
  "Kerala":          { education:8.4, safety:8.6, hostel:8.0, climate:8.6, cost:7.4, airport:8.4, internship:7.2, language:7.6, nri:8.8, diversity:7.8 },
  "Uttar Pradesh":   { education:7.8, safety:6.0, hostel:7.0, climate:6.4, cost:8.0, airport:7.4, internship:7.0, language:7.6, nri:6.8, diversity:7.6 },
  "West Bengal":     { education:8.2, safety:7.2, hostel:7.4, climate:7.0, cost:7.6, airport:7.8, internship:7.2, language:7.2, nri:7.0, diversity:7.8 },
  "Rajasthan":       { education:7.6, safety:7.6, hostel:7.4, climate:6.2, cost:7.6, airport:7.2, internship:6.8, language:7.4, nri:7.4, diversity:7.2 },
  "Madhya Pradesh":  { education:7.4, safety:7.0, hostel:7.0, climate:7.0, cost:8.0, airport:6.8, internship:6.6, language:7.4, nri:6.6, diversity:7.0 },
  "Haryana":         { education:7.8, safety:6.4, hostel:7.0, climate:6.4, cost:7.0, airport:8.8, internship:7.8, language:7.6, nri:7.2, diversity:7.8 },
  "Punjab":          { education:7.6, safety:7.8, hostel:7.4, climate:7.0, cost:7.4, airport:7.6, internship:7.0, language:7.2, nri:7.6, diversity:7.4 },
  "Odisha":          { education:7.4, safety:7.6, hostel:7.2, climate:7.0, cost:7.8, airport:6.8, internship:6.4, language:7.0, nri:6.6, diversity:6.8 },
  "Goa":             { education:7.2, safety:8.0, hostel:7.6, climate:8.4, cost:6.0, airport:8.0, internship:6.2, language:7.6, nri:8.4, diversity:8.0 }
};

const HUB_PINS = [
  { name:"Chennai",    state:"Tamil Nadu",  city:"Chennai",     lat:13.08, lng:80.27, type:"engineering" },
  { name:"Coimbatore", state:"Tamil Nadu",  city:"Coimbatore",  lat:11.02, lng:76.96, type:"engineering" },
  { name:"Trichy",     state:"Tamil Nadu",  city:"Trichy",      lat:10.79, lng:78.70, type:"engineering" },
  { name:"Bengaluru",  state:"Karnataka",   city:"Bengaluru",   lat:12.97, lng:77.59, type:"ai" },
  { name:"Manipal",    state:"Karnataka",   city:"Manipal",     lat:13.35, lng:74.79, type:"medical" },
  { name:"Hyderabad",  state:"Telangana",   city:"Hyderabad",   lat:17.39, lng:78.49, type:"semi" },
  { name:"Pune",       state:"Maharashtra", city:"Pune",        lat:18.52, lng:73.86, type:"engineering" },
  { name:"Mumbai",     state:"Maharashtra", city:"Mumbai",      lat:19.08, lng:72.88, type:"bschool" },
  { name:"Ahmedabad",  state:"Gujarat",     city:"Ahmedabad",   lat:23.03, lng:72.59, type:"bschool" },
  { name:"Delhi NCR",  state:"Delhi",       city:"Delhi NCR",   lat:28.61, lng:77.21, type:"all" }
];

function normaliseName(raw){
  const map = {
    "Orissa":"Odisha","Pondicherry":"Puducherry","Uttaranchal":"Uttarakhand","Telengana":"Telangana",
    "NCT of Delhi":"Delhi","Delhi (NCT)":"Delhi",
    "Jammu & Kashmir":"Jammu and Kashmir","Jammu And Kashmir":"Jammu and Kashmir",
    "Andaman & Nicobar Islands":"Andaman and Nicobar Islands",
    "Dadra and Nagar Haveli":"Dadra and Nagar Haveli and Daman and Diu",
    "Daman and Diu":"Dadra and Nagar Haveli and Daman and Diu"
  };
  return map[(raw||"").trim()] || (raw||"").trim();
}

/* ---------------- HERO MINI MAP ---------------- */
function compositeScore(s){ if(!s) return 0; return (s.education*.35 + s.safety*.2 + s.internship*.2 + s.nri*.15 + s.airport*.1); }
const RAMP = ["rgba(255,255,255,.04)","rgba(255,255,255,.10)","rgba(255,107,10,.18)","rgba(255,107,10,.30)","rgba(255,107,10,.45)","rgba(255,107,10,.60)"];
function colorFor(value, max){
  if(!value || max===0) return RAMP[0];
  const r = value/max;
  if(r<.5) return RAMP[1];
  if(r<.7) return RAMP[2];
  if(r<.82) return RAMP[3];
  if(r<.93) return RAMP[4];
  return RAMP[5];
}

const GEO_SOURCES = [
  "https://cdn.jsdelivr.net/gh/udit-001/india-maps-data@ef25ebc/geojson/india.geojson",
  "https://cdn.jsdelivr.net/gh/udit-001/india-maps-data@main/geojson/india.geojson"
];
const loadGeo = ()=> GEO_SOURCES.reduce((p,url)=> p.catch(()=> d3.json(url)), Promise.reject());

let cachedGeo = null;

loadGeo().then(geo=>{
  cachedGeo = geo;
  renderHeroMap(geo);
  renderMainMap(geo);
  renderTopStates();
});

function renderHeroMap(geo){
  const svg = d3.select("#hero-india-svg");
  const projection = d3.geoMercator().fitSize([600,600], geo);
  const path = d3.geoPath().projection(projection);
  const maxScore = Math.max(...Object.values(STATE_DATA).map(compositeScore));

  svg.selectAll("path.state").data(geo.features).enter().append("path")
    .attr("class","state").attr("d", path)
    .attr("fill", d=>{
      const name = normaliseName(d.properties.st_nm);
      const s = STATE_DATA[name];
      return s ? colorFor(compositeScore(s), maxScore) : "rgba(255,255,255,.04)";
    });

  // Pins
  const pinsLayer = svg.append("g").attr("class","pins-layer");
  pinsLayer.selectAll("circle.pin").data(HUB_PINS).enter().append("circle")
    .attr("class","pin")
    .attr("cx", d=> projection([d.lng, d.lat])[0])
    .attr("cy", d=> projection([d.lng, d.lat])[1])
    .attr("r", 0)
    .transition().duration(500).delay((d,i)=>i*120).attr("r", 4.5);

  // Pulsing ring on the brightest hub (Bengaluru)
  pinsLayer.selectAll("circle.pin-pulse").data([HUB_PINS[3]]).enter().append("circle")
    .attr("class","pin-pulse")
    .attr("cx", d=> projection([d.lng, d.lat])[0])
    .attr("cy", d=> projection([d.lng, d.lat])[1])
    .attr("r", 4.5);
}

/* ---------------- MAIN MAP ---------------- */
let currentFilter = "all";
let selectedState = null;

function renderMainMap(geo){
  const svg = d3.select("#india-svg");
  svg.selectAll("*").remove();
  const projection = d3.geoMercator().fitSize([720,720], geo);
  const path = d3.geoPath().projection(projection);

  const statesLayer = svg.append("g").attr("class","states-layer");
  const pinsLayer = svg.append("g").attr("class","pins-layer");

  const maxScore = Math.max(...Object.values(STATE_DATA).map(compositeScore));
  const lightRamp = ["#FBF7EE","#F0E5D0","#E5C9A4","#C99860","#FF8A3D","#FF6B0A"];
  function lightColor(v,mx){
    if(!v||mx===0) return lightRamp[0];
    const r=v/mx; if(r<.5)return lightRamp[1]; if(r<.7)return lightRamp[2]; if(r<.82)return lightRamp[3]; if(r<.93)return lightRamp[4]; return lightRamp[5];
  }

  statesLayer.selectAll("path.state").data(geo.features).enter().append("path")
    .attr("class","state").attr("d", path)
    .attr("fill", d=>{
      const name = normaliseName(d.properties.st_nm);
      const s = STATE_DATA[name];
      return s ? lightColor(compositeScore(s), maxScore) : "#F0EBDC";
    })
    .on("mousemove", function(event, d){
      const name = normaliseName(d.properties.st_nm);
      const s = STATE_DATA[name];
      if(!s) return;
      const tip = document.getElementById('mapTooltip');
      tip.classList.add('visible');
      tip.style.left = (event.clientX+14)+'px';
      tip.style.top  = (event.clientY+14)+'px';
      tip.innerHTML = `
        <div class="tt-title">${name}</div>
        <div class="tt-row"><span>Education</span><b>${s.education.toFixed(1)}</b></div>
        <div class="tt-row"><span>Safety</span><b>${s.safety.toFixed(1)}</b></div>
        <div class="tt-row"><span>NRI comfort</span><b>${s.nri.toFixed(1)}</b></div>
        <div class="tt-row"><span>Internships</span><b>${s.internship.toFixed(1)}</b></div>
      `;
    })
    .on("mouseleave", ()=> document.getElementById('mapTooltip').classList.remove('visible'))
    .on("click", function(event, d){
      const name = normaliseName(d.properties.st_nm);
      if(!STATE_DATA[name]) return;
      selectedState = name;
      d3.selectAll("#india-svg path.state").classed("selected", false);
      d3.select(this).classed("selected", true);
      renderStateDetail(name);
    });

  // Pins
  pinsLayer.selectAll("circle.pin").data(HUB_PINS).enter().append("circle")
    .attr("class","pin")
    .attr("cx", d=> projection([d.lng, d.lat])[0])
    .attr("cy", d=> projection([d.lng, d.lat])[1])
    .attr("r", 0)
    .style("display", d=> (currentFilter==="all" || d.type===currentFilter) ? null : "none")
    .on("mousemove", function(event, d){
      const tip = document.getElementById('mapTooltip');
      tip.classList.add('visible');
      tip.style.left = (event.clientX+14)+'px';
      tip.style.top  = (event.clientY+14)+'px';
      const s = STATE_DATA[d.state];
      tip.innerHTML = `
        <div class="tt-title">${d.name} · ${d.state}</div>
        <div class="tt-row"><span>Hub type</span><b>${d.type.toUpperCase()}</b></div>
        <div class="tt-row"><span>Edu score</span><b>${s?s.education.toFixed(1):"—"}</b></div>
        <div class="tt-row"><span>Internships</span><b>${s?s.internship.toFixed(1):"—"}</b></div>
      `;
      d3.select(this).attr("r", 8);
    })
    .on("mouseleave", function(){
      document.getElementById('mapTooltip').classList.remove('visible');
      d3.select(this).attr("r", 5.5);
    })
    .on("click", function(event, d){
      selectedState = d.state;
      d3.selectAll("#india-svg path.state").classed("selected", false);
      d3.selectAll("#india-svg path.state").each(function(p){
        if(normaliseName(p.properties.st_nm) === d.state) d3.select(this).classed("selected", true);
      });
      renderStateDetail(d.state);
    })
    .transition().duration(500).delay((d,i)=>i*60).attr("r", 5.5);
}

/* state filter pills */
document.querySelectorAll('#map .filter-pill').forEach(btn=>{
  btn.addEventListener('click', ()=>{
    currentFilter = btn.dataset.filter;
    document.querySelectorAll('#map .filter-pill').forEach(b=>{
      b.setAttribute('aria-pressed', b.dataset.filter===currentFilter ? 'true':'false');
    });
    d3.selectAll("#india-svg .pin").style("display", d=> (currentFilter==="all" || d.type===currentFilter) ? null : "none");
  });
});

/* ---------------- DETAIL PANEL ---------------- */
function renderTopStates(){
  document.getElementById('dpEyebrow').textContent = "Top study destinations";
  document.getElementById('dpTitle').textContent   = "Ranked by composite score";
  document.getElementById('dpBack').classList.remove('visible');

  const ranked = Object.entries(STATE_DATA).map(([n,s])=>({ name:n, score:compositeScore(s) }))
    .sort((a,b)=> b.score-a.score).slice(0,10);
  const max = ranked[0].score;
  const html = `
    <div class="dp-section-title">Composite score · top 10</div>
    <ol class="ranked-list">
      ${ranked.map((r,i)=>`
        <li>
          <span class="rank-num">${String(i+1).padStart(2,'0')}</span>
          <span class="rank-name">${r.name}</span>
          <span class="rank-val">${r.score.toFixed(1)}</span>
          <div class="rank-bar"><i style="width:${(r.score/max*100).toFixed(0)}%"></i></div>
        </li>`).join('')}
    </ol>
    <div class="dp-section-title">Click any state on the map for the full breakdown</div>
  `;
  document.getElementById('dpBody').innerHTML = html;
}

function renderStateDetail(name){
  const s = STATE_DATA[name];
  if(!s) return;
  document.getElementById('dpEyebrow').textContent = "State drill-down";
  document.getElementById('dpTitle').textContent   = name;
  document.getElementById('dpBack').classList.add('visible');

  const hubs = HUB_PINS.filter(p=> p.state===name);
  const composite = compositeScore(s).toFixed(1);
  const html = `
    <div class="dp-stats">
      <div class="dp-stat"><div class="dp-stat-label">Education</div><div class="dp-stat-val">${s.education.toFixed(1)}<span> /10</span></div></div>
      <div class="dp-stat"><div class="dp-stat-label">Safety</div><div class="dp-stat-val">${s.safety.toFixed(1)}<span> /10</span></div></div>
      <div class="dp-stat"><div class="dp-stat-label">NRI comfort</div><div class="dp-stat-val">${s.nri.toFixed(1)}<span> /10</span></div></div>
      <div class="dp-stat"><div class="dp-stat-label">Composite</div><div class="dp-stat-val">${composite}<span> /10</span></div></div>
    </div>
    <div class="dp-section-title">All metrics</div>
    <ol class="ranked-list">
      ${[
        ["Education quality", s.education],
        ["Student safety", s.safety],
        ["Hostel quality", s.hostel],
        ["Climate score", s.climate],
        ["Cost of living", s.cost],
        ["Airport connectivity", s.airport],
        ["Internships", s.internship],
        ["Language friendliness", s.language],
        ["NRI comfort", s.nri],
        ["Student diversity", s.diversity]
      ].map(([k,v])=>`
        <li>
          <span class="rank-num">·</span>
          <span class="rank-name">${k}</span>
          <span class="rank-val">${v.toFixed(1)}</span>
          <div class="rank-bar"><i style="width:${(v/10*100).toFixed(0)}%"></i></div>
        </li>`).join('')}
    </ol>
    ${hubs.length ? `
      <div class="dp-section-title">Notable hubs in ${name}</div>
      <ol class="ranked-list">
        ${hubs.map((h,i)=>`
          <li>
            <span class="rank-num">${String(i+1).padStart(2,'0')}</span>
            <span class="rank-name">${h.city} <small style="color:var(--muted);font-family:'JetBrains Mono',monospace;font-size:10px;text-transform:uppercase;letter-spacing:.1em">· ${h.type}</small></span>
          </li>`).join('')}
      </ol>` : ''}
  `;
  document.getElementById('dpBody').innerHTML = html;
}

document.getElementById('dpBack').addEventListener('click', ()=>{
  selectedState = null;
  d3.selectAll("#india-svg path.state").classed("selected", false);
  renderTopStates();
});

/* ---------------- SUITABILITY INDEX ---------------- */
const PRESETS = {
  balanced:  { academic:30, safety:20, culture:15, career:15, lifestyle:10, parent:10 },
  safety:    { academic:20, safety:35, culture:15, career:10, lifestyle:10, parent:10 },
  placement: { academic:25, safety:10, culture:10, career:35, lifestyle:10, parent:10 },
  nri:       { academic:20, safety:25, culture:15, career:10, lifestyle:10, parent:20 },
  budget:    { academic:25, safety:15, culture:10, career:15, lifestyle:20, parent:15 }
};

const SLIDER_KEYS = ["academic","safety","culture","career","lifestyle","parent"];

// Map each preset weight key to underlying state data dimensions
function scoreState(stateName, w){
  const s = STATE_DATA[stateName];
  if(!s) return 0;
  const academic = s.education;
  const safety = s.safety;
  const culture = (s.language + s.hostel)/2;
  const career = s.internship;
  const lifestyle = (s.climate + s.cost)/2;
  const parent = (s.nri + s.airport)/2;
  const total = w.academic + w.safety + w.culture + w.career + w.lifestyle + w.parent;
  if(total===0) return 0;
  return (
    academic*w.academic + safety*w.safety + culture*w.culture +
    career*w.career + lifestyle*w.lifestyle + parent*w.parent
  ) / total;
}

let radarChart = null;
function recompute(){
  const w = {};
  SLIDER_KEYS.forEach(k=>{
    const inp = document.querySelector(`input[data-key="${k}"]`);
    w[k] = +inp.value;
    inp.parentElement.querySelector('.slider-val').textContent = w[k]+"%";
  });
  const total = Object.values(w).reduce((a,b)=>a+b,0);
  document.getElementById('weightTotal').innerHTML = `${total}<span>%</span>`;

  const ranked = Object.keys(STATE_DATA).map(name=>({ name, score: scoreState(name, w) }))
    .sort((a,b)=> b.score-a.score).slice(0,5);

  const max = ranked[0].score;
  document.getElementById('matchGrid').innerHTML = ranked.map((r,i)=>`
    <div class="match-row">
      <div class="match-rank">0${i+1}</div>
      <div>
        <div class="match-name">${r.name}<small>${(r.score/10*100).toFixed(0)}% match · score ${r.score.toFixed(2)}</small></div>
      </div>
      <div class="match-score">${(r.score/10*100).toFixed(0)}</div>
    </div>`).join('');

  // radar
  const top3 = ranked.slice(0,3);
  const labels = ["Academics","Safety","Culture","Career","Lifestyle","NRI/Parent"];
  const palette = ["#FF6B0A","#FFFFFF","#FF8A3D"];
  const datasets = top3.map((r,i)=>{
    const s = STATE_DATA[r.name];
    return {
      label: r.name,
      data: [s.education, s.safety, (s.language+s.hostel)/2, s.internship, (s.climate+s.cost)/2, (s.nri+s.airport)/2],
      borderColor: palette[i],
      backgroundColor: i===0 ? "rgba(255,107,10,.18)" : (i===1 ? "rgba(255,255,255,.10)":"rgba(255,138,61,.10)"),
      borderWidth: 2,
      pointBackgroundColor: palette[i],
      pointRadius: 3
    };
  });

  if(radarChart) radarChart.destroy();
  const ctx = document.getElementById('radarChart');
  radarChart = new Chart(ctx, {
    type:'radar',
    data:{ labels, datasets },
    options:{
      responsive:true,
      maintainAspectRatio:false,
      plugins:{
        legend:{
          labels:{ color:"rgba(255,255,255,.85)", font:{ family:"JetBrains Mono", size:10 }, usePointStyle:true, padding:14 }
        }
      },
      scales:{
        r:{
          angleLines:{ color:"rgba(255,255,255,.12)" },
          grid:{ color:"rgba(255,255,255,.12)" },
          pointLabels:{ color:"rgba(255,255,255,.7)", font:{ family:"JetBrains Mono", size:10 } },
          ticks:{ display:false, beginAtZero:true, max:10 },
          min:0, max:10
        }
      }
    }
  });
}

document.querySelectorAll('input[type="range"][data-key]').forEach(inp=>{
  inp.addEventListener('input', recompute);
});
document.querySelectorAll('.preset-pill').forEach(btn=>{
  btn.addEventListener('click', ()=>{
    document.querySelectorAll('.preset-pill').forEach(b=> b.classList.remove('active'));
    btn.classList.add('active');
    const p = PRESETS[btn.dataset.preset];
    SLIDER_KEYS.forEach(k=>{
      document.querySelector(`input[data-key="${k}"]`).value = p[k];
    });
    recompute();
  });
});
recompute();

/* ---------------- DECISION TOOL ---------------- */
const TOOL_QUESTIONS_COUNT = 10;
let toolStep = 1;
const toolAnswers = {};

// Scoring biases: how each answer nudges destination rankings
const TOOL_DESTINATIONS = ["Chennai","Coimbatore","Bengaluru","Hyderabad","Pune","Manipal","Mumbai","Delhi NCR","Ahmedabad"];
const TOOL_BASE = { Chennai:78, Coimbatore:72, Bengaluru:80, Hyderabad:76, Pune:74, Manipal:70, Mumbai:72, "Delhi NCR":68, Ahmedabad:66 };

const TOOL_BIAS = {
  1:{ // climate
    warm:      { Chennai:+8, Mumbai:+6, Coimbatore:+2 },
    moderate:  { Bengaluru:+10, Pune:+8, Coimbatore:+8, Hyderabad:+4 },
    cool:      { Manipal:+10, Bengaluru:+4 },
    any:       {}
  },
  2:{
    veg:    { Coimbatore:+6, Ahmedabad:+10, Pune:+6, Chennai:+4 },
    jain:   { Ahmedabad:+12, Mumbai:+6 },
    mixed:  { Bengaluru:+6, Hyderabad:+4, "Delhi NCR":+4 },
    halal:  { Hyderabad:+8, Mumbai:+6, "Delhi NCR":+4 }
  },
  3:{
    under3:  { Coimbatore:+10, Chennai:+4 },
    "3to6":  { Coimbatore:+8, Chennai:+6, Pune:+4 },
    "6to12": { Bengaluru:+6, Pune:+6, Manipal:+4 },
    above12: { Bengaluru:+8, Manipal:+8, Mumbai:+6 }
  },
  4:{
    english: { Bengaluru:+8, Hyderabad:+6, Mumbai:+4 },
    hindi:   { "Delhi NCR":+10, Pune:+6, Ahmedabad:+4 },
    tamil:   { Chennai:+10, Coimbatore:+10 },
    any:     {}
  },
  5:{
    within30:      { Chennai:+8, Bengaluru:+8, Hyderabad:+8, Mumbai:+8 },
    within2h:      { Coimbatore:+6, Pune:+4 },
    anywhere:      { Manipal:+6 },
    international: { Chennai:+10, Bengaluru:+10, Hyderabad:+8, Coimbatore:+6, Mumbai:+8 }
  },
  6:{
    top:       { Chennai:+8, Coimbatore:+10, Pune:+4, Ahmedabad:+8 },
    important: { Chennai:+6, Coimbatore:+6 },
    balanced:  {},
    open:      {}
  },
  7:{
    critical:  { Bengaluru:+10, Pune:+8, Hyderabad:+8 },
    important: { Chennai:+6, Coimbatore:+4, Mumbai:+4 },
    moderate:  {},
    abroad:    { Manipal:+6, Bengaluru:+4 }
  },
  8:{
    oncampus:  { Manipal:+8, Coimbatore:+4 },
    approved:  { Bengaluru:+4, Pune:+4 },
    day:       { Chennai:+4, Coimbatore:+4 },
    open:      {}
  },
  9:{
    yes:      { Coimbatore:+8, Chennai:+6, Manipal:+4 },
    strict:   { Manipal:+6, Coimbatore:+6, Chennai:+4 },
    standard: {},
    na:       {}
  },
  10:{
    critical:  { Mumbai:+8, "Delhi NCR":+6, Bengaluru:+6 },
    nice:      {},
    lessimp:   {},
    any:       {}
  }
};

function recomputeTool(){
  const scores = {...TOOL_BASE};
  Object.entries(toolAnswers).forEach(([q, val])=>{
    const bias = (TOOL_BIAS[q] || {})[val] || {};
    Object.entries(bias).forEach(([city, delta])=>{
      scores[city] = (scores[city]||0) + delta;
    });
  });

  const ranked = Object.entries(scores).map(([name,score])=>({ name, score }))
    .sort((a,b)=> b.score-a.score).slice(0,4);

  const maxS = Math.max(...ranked.map(r=>r.score));
  document.getElementById('recList').innerHTML = ranked.map((r,i)=>`
    <div class="rec-card">
      <div>
        <div class="rec-name">${r.name}</div>
        <div class="rec-tag">Rank · ${String(i+1).padStart(2,'0')} · Composite ${r.score}</div>
      </div>
      <div class="rec-match">${Math.min(99, Math.round(r.score/maxS*98))}<small>%</small></div>
    </div>`).join('');

  const answered = Object.keys(toolAnswers).length;
  document.getElementById('trTitle').textContent = answered >= 5
    ? "Your shortlist · matches refining"
    : (answered >=1 ? "Your draft shortlist" : "Your shortlist will appear here");
  document.getElementById('trSub').textContent = answered >=10
    ? "Final 4 destinations matched to all 10 answers."
    : `Answered ${answered}/10. Keep going — the model recalibrates with every answer.`;
}

function showStep(n){
  toolStep = Math.max(1, Math.min(TOOL_QUESTIONS_COUNT, n));
  document.querySelectorAll('.tool-step').forEach(s=>{
    s.classList.toggle('active', +s.dataset.step === toolStep);
  });
  const pct = (toolStep/TOOL_QUESTIONS_COUNT)*100;
  document.getElementById('tpBar').style.width = pct+"%";
  document.getElementById('tpNum').textContent = String(toolStep).padStart(2,'0')+" / "+TOOL_QUESTIONS_COUNT;
  document.getElementById('toolBack').disabled = (toolStep===1);
  document.getElementById('toolHelper').textContent = toolStep === TOOL_QUESTIONS_COUNT
    ? "Last question — pick to finalise"
    : "Pick an option to continue";
}

document.querySelectorAll('.tool-step').forEach(step=>{
  const q = +step.dataset.step;
  step.querySelectorAll('.opt-tile').forEach(tile=>{
    tile.addEventListener('click', ()=>{
      step.querySelectorAll('.opt-tile').forEach(t=> t.classList.remove('selected'));
      tile.classList.add('selected');
      toolAnswers[q] = tile.dataset.val;
      recomputeTool();
      setTimeout(()=>{
        if(q < TOOL_QUESTIONS_COUNT) showStep(q+1);
      }, 320);
    });
  });
});

document.getElementById('toolBack').addEventListener('click', ()=> showStep(toolStep-1));
recomputeTool();

/* ---------------- CITY COMPARISON ---------------- */
const CITY_METRICS = {
  Chennai:    { placement:8.6, safety:8.4, stress:6.6, climate:6.8, cost:7.4, pollution:6.4, internet:8.8, startup:7.2, manufact:8.0, culture:8.4, transport:8.0, medical:8.6 },
  Bengaluru:  { placement:9.6, safety:7.4, stress:7.0, climate:9.0, cost:5.6, pollution:5.6, internet:9.4, startup:9.8, manufact:7.0, culture:9.0, transport:7.0, medical:8.8 },
  Pune:       { placement:8.8, safety:7.6, stress:6.6, climate:8.4, cost:6.4, pollution:6.4, internet:9.0, startup:8.8, manufact:8.6, culture:8.6, transport:7.4, medical:8.0 },
  Hyderabad:  { placement:9.0, safety:8.0, stress:6.6, climate:7.0, cost:7.0, pollution:6.6, internet:9.2, startup:8.2, manufact:8.4, culture:8.4, transport:7.6, medical:8.6 },
  Coimbatore: { placement:7.8, safety:9.0, stress:5.8, climate:7.6, cost:8.6, pollution:7.6, internet:8.4, startup:6.6, manufact:9.0, culture:8.2, transport:7.0, medical:8.0 },
  Ahmedabad:  { placement:7.6, safety:8.4, stress:5.8, climate:6.4, cost:7.6, pollution:6.8, internet:8.6, startup:7.2, manufact:8.8, culture:7.6, transport:7.4, medical:7.6 }
};
const METRIC_LIST = [
  ["placement","Placement Quality"],
  ["safety","Safety"],
  ["stress","Student Stress"],
  ["climate","Climate"],
  ["cost","Cost of Living"],
  ["pollution","Air Quality"],
  ["internet","Internet"],
  ["startup","Startup Density"],
  ["manufact","Manufacturing"],
  ["culture","Campus Culture"],
  ["transport","Public Transport"],
  ["medical","Medical Access"]
];

let activeCities = ["Chennai","Bengaluru","Pune","Hyderabad"];
let cityRadar = null;

function renderMetricTable(){
  const html = METRIC_LIST.map(([key,label])=>{
    const bars = activeCities.map(c=>{
      const v = CITY_METRICS[c][key];
      return `<div class="bar"><span class="bar-name">${c}</span><div class="bar-track"><div class="bar-fill" style="width:${v*10}%"></div></div><span class="bar-val">${v.toFixed(1)}</span></div>`;
    }).join('');
    return `<div class="metric-row"><div class="metric-label">${label}</div><div class="bars">${bars}</div></div>`;
  }).join('');
  document.getElementById('metricTable').innerHTML = html;
}

function renderCityRadar(){
  const palette = ["#0E3A8A","#FF6B0A","#1F8B5C","#E89A1C","#C23A3A","#7B91C2"];
  const labels = METRIC_LIST.map(m=>m[1]);
  const datasets = activeCities.map((c,i)=>({
    label: c,
    data: METRIC_LIST.map(m=> CITY_METRICS[c][m[0]]),
    borderColor: palette[i],
    backgroundColor: palette[i]+"22",
    borderWidth: 2,
    pointRadius: 2.5,
    pointBackgroundColor: palette[i]
  }));
  if(cityRadar) cityRadar.destroy();
  cityRadar = new Chart(document.getElementById('cityRadarChart'),{
    type:'radar',
    data:{ labels, datasets },
    options:{
      responsive:true, maintainAspectRatio:false,
      plugins:{ legend:{ position:'bottom', labels:{ font:{ family:"JetBrains Mono", size:10 }, color:"#5A6278", usePointStyle:true, padding:14 } } },
      scales:{
        r:{
          angleLines:{ color:"#E8DFC8" },
          grid:{ color:"#E8DFC8" },
          pointLabels:{ font:{ family:"JetBrains Mono", size:9 }, color:"#5A6278" },
          ticks:{ display:false, beginAtZero:true, max:10 },
          min:0, max:10
        }
      }
    }
  });
}

document.querySelectorAll('#cityChips .city-chip').forEach(chip=>{
  chip.addEventListener('click', ()=>{
    const city = chip.dataset.city;
    if(activeCities.includes(city)){
      if(activeCities.length<=1) return;
      activeCities = activeCities.filter(c=> c!==city);
      chip.classList.remove('active');
    } else {
      if(activeCities.length>=5) return;
      activeCities.push(city);
      chip.classList.add('active');
    }
    renderMetricTable();
    renderCityRadar();
  });
});

renderMetricTable();
renderCityRadar();
