
// ════════════════════════════════════════════════════════════════
// DATA — Tamil Nadu district-wise TNEA college counts
// ════════════════════════════════════════════════════════════════
// Approximations from AICTE / TNEA 2024 participating-institutions list.
// Numbers split across categories (Govt / Aided / SF / Top-tier).
const DISTRICT_DATA = {
  "Chennai":          { all: 105, govt: 3, aided: 2, sf: 100, top: 5 },
  "Coimbatore":       { all: 80,  govt: 1, aided: 1, sf: 78,  top: 4 },
  "Kanchipuram":      { all: 38,  govt: 0, aided: 0, sf: 38,  top: 1 },
  "Chengalpattu":     { all: 32,  govt: 0, aided: 0, sf: 32,  top: 1 },
  "Tiruchirappalli":  { all: 30,  govt: 1, aided: 1, sf: 28,  top: 1 },
  "Madurai":          { all: 28,  govt: 1, aided: 0, sf: 27,  top: 0 },
  "Tiruvallur":       { all: 22,  govt: 0, aided: 0, sf: 22,  top: 0 },
  "Salem":            { all: 25,  govt: 1, aided: 0, sf: 24,  top: 0 },
  "Erode":            { all: 24,  govt: 1, aided: 0, sf: 23,  top: 1 },
  "Tirunelveli":      { all: 22,  govt: 1, aided: 0, sf: 21,  top: 0 },
  "Vellore":          { all: 20,  govt: 0, aided: 0, sf: 20,  top: 0 },
  "Tiruvannamalai":   { all: 16,  govt: 1, aided: 0, sf: 15,  top: 0 },
  "Namakkal":         { all: 16,  govt: 0, aided: 0, sf: 16,  top: 0 },
  "Krishnagiri":      { all: 14,  govt: 0, aided: 0, sf: 14,  top: 0 },
  "Dindigul":         { all: 11,  govt: 1, aided: 0, sf: 10,  top: 0 },
  "Virudhunagar":     { all: 11,  govt: 1, aided: 1, sf: 9,   top: 0 },
  "Thanjavur":        { all: 11,  govt: 1, aided: 0, sf: 10,  top: 1 },
  "Tiruppur":         { all: 10,  govt: 0, aided: 0, sf: 10,  top: 0 },
  "Cuddalore":        { all: 9,   govt: 1, aided: 0, sf: 8,   top: 0 },
  "Villupuram":       { all: 9,   govt: 0, aided: 0, sf: 9,   top: 0 },
  "Thoothukudi":      { all: 9,   govt: 1, aided: 0, sf: 8,   top: 0 },
  "Karur":            { all: 7,   govt: 0, aided: 0, sf: 7,   top: 0 },
  "Kanyakumari":      { all: 7,   govt: 1, aided: 0, sf: 6,   top: 0 },
  "Theni":            { all: 6,   govt: 0, aided: 0, sf: 6,   top: 0 },
  "Sivaganga":        { all: 5,   govt: 1, aided: 0, sf: 4,   top: 0 },
  "Pudukkottai":      { all: 5,   govt: 1, aided: 0, sf: 4,   top: 0 },
  "Ranipet":          { all: 5,   govt: 0, aided: 0, sf: 5,   top: 0 },
  "Ramanathapuram":   { all: 4,   govt: 1, aided: 0, sf: 3,   top: 0 },
  "Dharmapuri":       { all: 4,   govt: 1, aided: 0, sf: 3,   top: 0 },
  "Tirupathur":       { all: 4,   govt: 0, aided: 0, sf: 4,   top: 0 },
  "Nagapattinam":     { all: 4,   govt: 0, aided: 0, sf: 4,   top: 0 },
  "Mayiladuthurai":   { all: 3,   govt: 0, aided: 0, sf: 3,   top: 0 },
  "Tenkasi":          { all: 3,   govt: 0, aided: 0, sf: 3,   top: 0 },
  "Kallakurichi":     { all: 3,   govt: 0, aided: 0, sf: 3,   top: 0 },
  "Tiruvarur":        { all: 3,   govt: 0, aided: 0, sf: 3,   top: 0 },
  "Perambalur":       { all: 3,   govt: 0, aided: 0, sf: 3,   top: 0 },
  "The Nilgiris":     { all: 2,   govt: 0, aided: 0, sf: 2,   top: 0 },
  "Ariyalur":         { all: 2,   govt: 0, aided: 0, sf: 2,   top: 0 }
};

// District name aliases — GeoJSON may use slightly different spellings
const DISTRICT_ALIASES = {
  "Tiruchirapalli": "Tiruchirappalli", "Trichy": "Tiruchirappalli",
  "Thiruvallur": "Tiruvallur",
  "Thoothukkudi": "Thoothukudi", "Tuticorin": "Thoothukudi",
  "Nilgiris": "The Nilgiris",
  "Kanniyakumari": "Kanyakumari",
  "Viluppuram": "Villupuram",
  "Sivagangai": "Sivaganga",
  "Thirupathur": "Tirupathur",
  "Tirupattur": "Tirupathur",
  "Mayiladuthurai (Mayuram)": "Mayiladuthurai",
  "Tiruppattur": "Tirupathur",
  "Pudukottai": "Pudukkottai"
};
function normaliseDistrict(raw) {
  if (!raw) return raw;
  const t = raw.trim();
  return DISTRICT_ALIASES[t] || t;
}

// ════════════════════════════════════════════════════════════════
// Top-tier TN colleges — pins overlay (NIRF ranked / NAAC A++)
// ════════════════════════════════════════════════════════════════
const TOP_PINS = [
  { name: "Anna University CEG", city: "Chennai", district: "Chennai", lat: 13.01, lng: 80.24, note: "NIRF #15 · NAAC A++" },
  { name: "NIT Trichy", city: "Tiruchirappalli", district: "Tiruchirappalli", lat: 10.76, lng: 78.81, note: "NIRF #9 (not in TNEA)" },
  { name: "PSG College of Tech", city: "Coimbatore", district: "Coimbatore", lat: 11.02, lng: 76.96, note: "NAAC A++" },
  { name: "SSN College of Engg", city: "Kalavakkam", district: "Kanchipuram", lat: 12.75, lng: 80.20, note: "Top-tier SF" },
  { name: "SASTRA University", city: "Thanjavur", district: "Thanjavur", lat: 10.73, lng: 79.02, note: "Deemed · NAAC A++" },
  { name: "VIT Vellore", city: "Vellore", district: "Vellore", lat: 12.97, lng: 79.16, note: "NIRF #11 · Deemed" },
  { name: "Amrita Coimbatore", city: "Coimbatore", district: "Coimbatore", lat: 10.90, lng: 76.90, note: "NIRF #25 · Deemed" },
  { name: "Thiagarajar College of Engg", city: "Madurai", district: "Madurai", lat: 9.88, lng: 78.08, note: "Autonomous · NIRF Top 100" },
  { name: "CIT Coimbatore", city: "Coimbatore", district: "Coimbatore", lat: 11.03, lng: 77.00, note: "Autonomous SF" },
  { name: "Bannari Amman Inst of Tech", city: "Sathyamangalam", district: "Erode", lat: 11.51, lng: 77.24, note: "Autonomous SF" }
];

// ════════════════════════════════════════════════════════════════
// Notable colleges per district — for drill-down
// ════════════════════════════════════════════════════════════════
const NOTABLE_BY_DISTRICT = {
  "Chennai": [
    { name: "Anna University CEG", tag: "Constituent", co: 199 },
    { name: "MIT Chrompet", tag: "Constituent", co: 199 },
    { name: "AC Tech Anna Univ", tag: "Constituent", co: 197 },
    { name: "SRM Valliammai Engg College", tag: "SF", co: 168 },
    { name: "Velammal Engg College", tag: "SF", co: 187 },
    { name: "Easwari Engg College", tag: "SF", co: 184 },
    { name: "Sri Sairam Engg College", tag: "SF", co: 185 },
    { name: "Jeppiaar Engg College", tag: "SF", co: 162 },
    { name: "Panimalar Inst of Tech", tag: "SF", co: 165 },
    { name: "Misrimal Navajee Munoth Jain", tag: "SF", co: 158 }
  ],
  "Coimbatore": [
    { name: "PSG College of Technology", tag: "SF", co: 198.5 },
    { name: "Coimbatore Inst of Technology", tag: "SF", co: 197.5 },
    { name: "Kumaraguru College of Tech", tag: "SF", co: 191 },
    { name: "Government CT Coimbatore", tag: "Govt", co: 197 },
    { name: "Karunya Inst of Tech", tag: "SF", co: 178 },
    { name: "Amrita Coimbatore (separate from TNEA)", tag: "SF", co: 0 },
    { name: "Sri Krishna College of Engg", tag: "SF", co: 174 },
    { name: "SNS College of Technology", tag: "SF", co: 168 },
    { name: "Hindusthan College of Engg", tag: "SF", co: 164 }
  ],
  "Kanchipuram": [
    { name: "SSN College of Engineering", tag: "SF", co: 198 },
    { name: "SRM IST (Kattankulathur)", tag: "SF", co: 172 },
    { name: "Sri Sivasubramaniya Nadar", tag: "SF", co: 196 },
    { name: "Sri Sai Ram Engg College", tag: "SF", co: 185 }
  ],
  "Chengalpattu": [
    { name: "Saveetha Engg College (Thandalam)", tag: "SF", co: 182 },
    { name: "Hindustan Inst of Tech & Sci", tag: "SF", co: 178 },
    { name: "Sri Sairam Engg College (Tambaram)", tag: "SF", co: 185 },
    { name: "Rajalakshmi Engg College", tag: "SF", co: 192 }
  ],
  "Tiruchirappalli": [
    { name: "NIT Trichy (not TNEA, JoSAA)", tag: "Constituent", co: 0 },
    { name: "Bharathidasan Inst of Tech", tag: "Constituent", co: 191 },
    { name: "Saranathan College of Engg", tag: "SF", co: 174 },
    { name: "K Ramakrishnan College of Engg", tag: "SF", co: 168 },
    { name: "M.A.M. College of Engineering", tag: "SF", co: 162 },
    { name: "Government CT Tiruchirappalli", tag: "Govt", co: 188 }
  ],
  "Madurai": [
    { name: "Thiagarajar College of Engg", tag: "SF", co: 192 },
    { name: "Velammal College of Engg & Tech", tag: "SF", co: 175 },
    { name: "Anna University Madurai Regional", tag: "Constituent", co: 184 },
    { name: "Government CT Madurai", tag: "Govt", co: 178 }
  ],
  "Salem": [
    { name: "Sona College of Technology", tag: "SF", co: 178 },
    { name: "Government CT Salem", tag: "Govt", co: 172 },
    { name: "Knowledge Inst of Tech", tag: "SF", co: 168 },
    { name: "Vinayaka Mission's CT", tag: "SF", co: 160 }
  ],
  "Erode": [
    { name: "Bannari Amman Inst of Tech", tag: "SF", co: 190 },
    { name: "Kongu Engineering College", tag: "SF", co: 187 },
    { name: "Government CT Erode", tag: "Govt", co: 174 },
    { name: "Velalar College of Engg & Tech", tag: "SF", co: 162 }
  ],
  "Tirunelveli": [
    { name: "National Engineering College", tag: "SF", co: 184 },
    { name: "Government CT Tirunelveli", tag: "Govt", co: 172 },
    { name: "Francis Xavier Engg College", tag: "SF", co: 162 }
  ],
  "Vellore": [
    { name: "VIT Vellore (Deemed, not TNEA)", tag: "SF", co: 0 },
    { name: "CC Tech (CSEIT Anna Univ)", tag: "SF", co: 168 },
    { name: "GRT Inst of Engg & Tech", tag: "SF", co: 158 }
  ],
  "Tiruvallur": [
    { name: "Vel Tech Engineering College", tag: "SF", co: 174 },
    { name: "RM Engineering College", tag: "SF", co: 162 },
    { name: "Velammal Inst of Tech", tag: "SF", co: 178 }
  ],
  "Tiruvannamalai": [
    { name: "Arunai Engineering College", tag: "SF", co: 158 },
    { name: "Government CT Tiruvannamalai", tag: "Govt", co: 165 },
    { name: "ARM College of Engg & Tech", tag: "SF", co: 152 }
  ],
  "Thanjavur": [
    { name: "SASTRA University (Deemed)", tag: "SF", co: 0 },
    { name: "PRIST University", tag: "SF", co: 0 },
    { name: "Government CT Thanjavur", tag: "Govt", co: 168 }
  ],
  "Namakkal": [
    { name: "K.S. Rangasamy CT (Tiruchengode)", tag: "SF", co: 178 },
    { name: "Selvam College of Tech", tag: "SF", co: 158 }
  ],
  "Karur": [
    { name: "M. Kumarasamy College of Engg", tag: "SF", co: 168 }
  ],
  "Krishnagiri": [
    { name: "Adhiyamaan College of Engg (Hosur)", tag: "SF", co: 172 },
    { name: "K.S.R.M. College of Engg", tag: "SF", co: 158 }
  ],
  "Dindigul": [
    { name: "PSNA College of Engg & Tech", tag: "SF", co: 174 },
    { name: "Government CT Dindigul", tag: "Govt", co: 168 }
  ],
  "Cuddalore": [
    { name: "Sri Manakula Vinayagar Engg College", tag: "SF", co: 158 },
    { name: "Government CT Cuddalore", tag: "Govt", co: 168 }
  ],
  "Tiruppur": [
    { name: "PA College of Engg & Tech", tag: "SF", co: 158 },
    { name: "Akshaya College of Engg", tag: "SF", co: 148 }
  ],
  "Virudhunagar": [
    { name: "Mepco Schlenk Engg College", tag: "Aided", co: 182 },
    { name: "Government CT Virudhunagar", tag: "Govt", co: 168 }
  ]
};

// ════════════════════════════════════════════════════════════════
// FILTER CONFIG
// ════════════════════════════════════════════════════════════════
const FILTERS = {
  all: { title: "All TNEA colleges", sub: "Choropleth by participating-college count per district",
         mode: "choropleth",
         panelMeta: "All 571 TNEA colleges · 38 districts",
         panelTitle: "All TNEA colleges",
         panelBody: "All 571 colleges admit through TNEA — the Anna University-run counselling that uses Class 12 PCM marks (out of 200) as the cut-off. Chennai, Coimbatore, Kanchipuram, Chengalpattu and Tiruchirappalli together host nearly half of all colleges." },
  govt: { title: "Government engineering colleges", sub: "21 colleges run directly by the Tamil Nadu government",
          mode: "choropleth",
          panelMeta: "Govt fee · TNEA quota only",
          panelTitle: "Government colleges in TN",
          panelBody: "Tamil Nadu has 21 government engineering colleges run by the State Directorate of Technical Education. Tuition is among the lowest in India (₹15,000–25,000/year), seats are 100% government-quota via TNEA, and infrastructure varies — strong in Coimbatore, Tirunelveli, Madurai; weaker in newer districts." },
  aided: { title: "Government-aided colleges", sub: "6 colleges receiving partial state grants",
           mode: "choropleth",
           panelMeta: "Aided fee structure · 65% govt quota",
           panelTitle: "Aided colleges in TN",
           panelBody: "Six private institutions that receive partial salary support from the state government. Fee structures are mid-tier (₹40,000–80,000/year), 65% of seats are filled through TNEA, the remaining 35% through management quota. Includes Mepco Schlenk Virudhunagar and Coimbatore Inst of Tech (in part)." },
  sf: { title: "Self-financing colleges", sub: "544 private colleges admitting via TNEA + management quota",
        mode: "choropleth",
        panelMeta: "SF fee · 65% TNEA · 35% management",
        panelTitle: "Self-financing colleges",
        panelBody: "The bulk of TN's engineering ecosystem — 544 private self-financed colleges affiliated to Anna University. 65% of seats are filled through TNEA counselling using cut-offs, and 35% through management quota (institute-set fees, donation, NRI). Fees range from ₹65,000 to ₹2.5 lakh/year depending on tier." },
  top: { title: "Top-tier TN colleges (NIRF / NAAC A++)", sub: "10 colleges with NIRF Engineering Top 100 or NAAC A++ grade",
         mode: "pins",
         panelMeta: "NIRF Top 100 · or NAAC A++ grade",
         panelTitle: "Top-tier colleges in Tamil Nadu",
         panelBody: "The elite tier of TN engineering — most ranked in NIRF Engineering Top 100 or accredited NAAC A++. Some (IIT Madras, NIT Trichy) admit via JoSAA, not TNEA; others (VIT, SASTRA, SRM, Amrita) are Deemed Universities with their own entrance exams; the TNEA-eligible top-tier includes Anna University CEG/MIT/AC Tech, PSG Tech, CIT Coimbatore, Thiagarajar College, Bannari Amman and Kongu." }
};

let currentFilter = "all";
let selectedDistrict = null;

// ════════════════════════════════════════════════════════════════
// MAP setup
// ════════════════════════════════════════════════════════════════
const svg = d3.select("#tn-map");
const tooltip = d3.select("#mapTooltip");
const mapLoading = document.getElementById('mapLoading');
let mapPaths = null;
let projection = null;
let districtKey = "district"; // detected from GeoJSON

const GEO_SOURCES = [
  "https://cdn.jsdelivr.net/gh/udit-001/india-maps-data@ef25ebc/geojson/states/tamil-nadu.geojson",
  "https://cdn.jsdelivr.net/gh/udit-001/india-maps-data@main/geojson/states/tamil-nadu.geojson"
];
const loadGeo = () => GEO_SOURCES.reduce((p, url) => p.catch(() => d3.json(url)), Promise.reject());

loadGeo().then(geo => {
  mapLoading.style.display = "none";
  // Auto-detect the district name property
  const sample = (geo.features[0] || {}).properties || {};
  const candidates = ["district", "dist_name", "NAME_2", "DISTRICT", "Dist_Name", "name"];
  districtKey = candidates.find(k => k in sample) || "district";
  renderMap(geo);
  render(currentFilter);
}).catch(err => {
  console.warn("TN map load failed:", err);
  mapLoading.innerHTML = "<strong style='color:var(--navy-ink);font-family:Fraunces,serif;font-size:16px;'>Map couldn't load</strong><br>The ranked list and stats below still work. Refresh to retry.";
  render(currentFilter);
});

function renderMap(geo) {
  // Auto-fit to viewBox — works regardless of TN's exact bbox
  projection = d3.geoMercator().fitSize([540, 720], geo);
  const pathGen = d3.geoPath().projection(projection);

  svg.append("g").attr("class", "districts-layer");
  svg.append("g").attr("class", "pins-layer");

  mapPaths = svg.select(".districts-layer").selectAll("path.district")
    .data(geo.features).enter().append("path")
    .attr("class", "district").attr("d", pathGen).attr("fill", "var(--cream-2)")
    .on("mousemove", function(event, d) {
      const name = normaliseDistrict(d.properties[districtKey] || "");
      const data = DISTRICT_DATA[name];
      const val = data ? (data[currentFilter] || 0) : 0;
      const cfg = FILTERS[currentFilter];
      const wrap = svg.node().getBoundingClientRect();
      const x = event.clientX - wrap.left + 14;
      const y = event.clientY - wrap.top + 14;
      tooltip.html(
        "<strong>" + (name || "Unknown") + "</strong>" +
        "<div class='tip-num'>" + val + "</div>" +
        "<div class='tip-label'>" + (currentFilter === 'all' ? 'TNEA colleges' : cfg.title) + "</div>" +
        (data ? "<div class='tip-sub'>Click for college list →</div>" : "")
      ).style("left", x + "px").style("top", y + "px").style("opacity", 1);
    })
    .on("mouseleave", () => tooltip.style("opacity", 0))
    .on("click", function(event, d) {
      const name = normaliseDistrict(d.properties[districtKey] || "");
      if (DISTRICT_DATA[name]) {
        selectedDistrict = name;
        d3.selectAll("#tn-map path.district").classed("selected", false);
        d3.select(this).classed("selected", true);
        renderDistrictDetail(name);
      }
    });
}

function renderPins(show) {
  const pinsLayer = svg.select(".pins-layer");
  pinsLayer.selectAll("*").remove();
  if (!show || !projection) return;

  pinsLayer.selectAll("circle.pin")
    .data(TOP_PINS).enter().append("circle")
    .attr("class", "pin")
    .attr("cx", d => projection([d.lng, d.lat])[0])
    .attr("cy", d => projection([d.lng, d.lat])[1])
    .attr("r", 0)
    .on("mousemove", function(event, d) {
      const wrap = svg.node().getBoundingClientRect();
      const x = event.clientX - wrap.left + 14;
      const y = event.clientY - wrap.top + 14;
      tooltip.html(
        "<strong>" + d.name + "</strong>" +
        "<div class='tip-label' style='margin-top:6px;'>" + d.city + ", " + d.district + "</div>" +
        "<div class='tip-sub'>" + d.note + "</div>"
      ).style("left", x + "px").style("top", y + "px").style("opacity", 1);
      d3.select(this).attr("r", 10);
    })
    .on("mouseleave", function() { tooltip.style("opacity", 0); d3.select(this).attr("r", 6); })
    .transition().duration(450).delay((d, i) => i * 40).attr("r", 6);
}

// ════════════════════════════════════════════════════════════════
// Color ramp + legend
// ════════════════════════════════════════════════════════════════
const RAMP = ["#FBF7EE", "#E8DFC8", "#B7C2DC", "#7B91C2", "#3D5DA3", "#0E3A8A"];
(function buildLegend() {
  const c = document.getElementById('legendScale');
  RAMP.forEach(col => { const d = document.createElement('div'); d.style.background = col; c.appendChild(d); });
})();
function colorFor(value, max) {
  if (!value || max === 0) return RAMP[0];
  const r = value / max;
  if (r < 0.04) return RAMP[1];
  if (r < 0.12) return RAMP[2];
  if (r < 0.28) return RAMP[3];
  if (r < 0.60) return RAMP[4];
  return RAMP[5];
}

// ════════════════════════════════════════════════════════════════
// RENDER
// ════════════════════════════════════════════════════════════════
function render(filterKey) {
  currentFilter = filterKey;
  const cfg = FILTERS[filterKey];

  document.getElementById('mapTitle').textContent = cfg.title;
  document.getElementById('mapSub').textContent = cfg.sub;
  document.getElementById('panelMeta').textContent = cfg.panelMeta;
  document.getElementById('panelTitle').textContent = cfg.panelTitle;
  document.getElementById('panelBody').textContent = cfg.panelBody;

  document.querySelectorAll('.filter-pill').forEach(b => {
    b.setAttribute('aria-pressed', b.dataset.filter === filterKey ? 'true' : 'false');
  });
  document.getElementById('pinNote').classList.toggle('visible', cfg.mode === 'pins');

  const values = Object.values(DISTRICT_DATA).map(r => r[filterKey] || 0);
  const max = Math.max(...values, 1);

  if (mapPaths) {
    mapPaths.transition().duration(450).attr("fill", function(d) {
      const name = normaliseDistrict(d.properties[districtKey] || "");
      const data = DISTRICT_DATA[name];
      const val = data ? (data[filterKey] || 0) : 0;
      if (cfg.mode === 'pins') return val > 0 ? "#F0E5D0" : RAMP[0];
      return colorFor(val, max);
    });
  }
  renderPins(cfg.mode === 'pins');

  if (selectedDistrict) renderDistrictDetail(selectedDistrict); else renderTopDistricts();

  // Stats strip
  const total = values.reduce((a, b) => a + b, 0);
  document.getElementById('statTotal').textContent = total;
  document.getElementById('statDistricts').textContent = values.filter(v => v > 0).length;
  const sorted = Object.entries(DISTRICT_DATA)
    .filter(([, v]) => (v[filterKey] || 0) > 0)
    .sort((a, b) => b[1][filterKey] - a[1][filterKey]);
  const topD = sorted[0];
  document.getElementById('statTop').textContent = topD ? topD[0] : "—";
  if (topD && topD[0].length > 10) document.getElementById('statTop').style.fontSize = "clamp(18px, 2.2vw, 26px)";
  else document.getElementById('statTop').style.fontSize = "";
  const top2Sum = sorted.slice(0, 2).reduce((s, [, v]) => s + v[filterKey], 0);
  const sharePct = total ? Math.round(top2Sum / total * 100) : 0;
  document.getElementById('statShare').innerHTML = sharePct + "<span>%</span>";
}

function renderTopDistricts() {
  const filterKey = currentFilter;
  const cfg = FILTERS[filterKey];
  const ranked = Object.entries(DISTRICT_DATA)
    .map(([d, r]) => ({ d, val: r[filterKey] || 0 }))
    .filter(r => r.val > 0).sort((a, b) => b.val - a.val);
  const top = ranked.slice(0, 12);
  const topMax = top.length ? top[0].val : 1;
  const titleLabel = filterKey === "all" ? "all TNEA" : cfg.title.split(" ")[0];

  let html = "<h3>Top districts · " + titleLabel + "</h3>"
           + "<div class='sub'>Click any district for the named college list</div>"
           + "<ol class='ranked-list'>";
  if (top.length === 0) {
    html += "<li style='padding:24px 0;color:var(--muted);font-size:14px;list-style:none;'>No data for this filter.</li>";
  } else {
    top.forEach((r, i) => {
      const pct = Math.max(2, Math.round(r.val / topMax * 100));
      html += "<li class='ranked-item' data-district='" + r.d + "'>"
            + "<div class='ranked-num'>" + String(i + 1).padStart(2, '0') + "</div>"
            + "<div class='ranked-bar-wrap'>"
              + "<div class='ranked-bar-name'>" + r.d + "</div>"
              + "<div class='ranked-bar-track'><div class='ranked-bar-fill' style='width:" + pct + "%'></div></div>"
            + "</div>"
            + "<div class='ranked-val'>" + r.val + "</div>"
          + "</li>";
    });
  }
  html += "</ol>";
  document.getElementById('rightPanel').innerHTML = html;

  document.querySelectorAll('.ranked-item').forEach(li => {
    li.addEventListener('click', () => {
      const d = li.dataset.district;
      if (d && DISTRICT_DATA[d]) {
        selectedDistrict = d;
        d3.selectAll("#tn-map path.district").classed("selected", function(feat) {
          const name = normaliseDistrict((feat && feat.properties && feat.properties[districtKey]) || "");
          return name === d;
        });
        renderDistrictDetail(d);
      }
    });
  });
}

function renderDistrictDetail(district) {
  const data = DISTRICT_DATA[district];
  if (!data) return;
  const colleges = NOTABLE_BY_DISTRICT[district] || [];

  let html = "<div class='drill-header'>"
           + "<div class='drill-title'><small>District drill-down</small>" + district + "</div>"
           + "<button class='drill-back' onclick='clearSelection()'>TN view</button>"
           + "</div>";
  html += "<div class='drill-stats'>"
        + "<div class='drill-stat'><div class='num'>" + data.all + "</div><div class='lab'>Total TNEA colleges</div></div>"
        + "<div class='drill-stat'><div class='num'>" + (data.govt + data.aided) + "<span>•</span></div><div class='lab'>Govt + Aided</div></div>"
        + "<div class='drill-stat'><div class='num'>" + data.sf + "</div><div class='lab'>Self-financing</div></div>"
        + "<div class='drill-stat'><div class='num'>" + data.top + "<span>•</span></div><div class='lab'>NIRF / A++ tier</div></div>"
        + "</div>";

  if (colleges.length > 0) {
    html += "<div class='drill-section-title'>Notable colleges · with CSE cut-off (OC 2024 approx)</div><ul class='college-list'>";
    colleges.forEach(c => {
      const tagClass = (c.tag || "").toLowerCase();
      const cutoffStr = c.co > 0 ? c.co.toString() : "—";
      html += "<li class='college-item'>"
            + "<div><div class='name'>" + c.name + "</div><div class='meta'>CSE cut-off · " + cutoffStr + "</div></div>"
            + "<span class='tag " + tagClass + "'>" + c.tag + "</span>"
          + "</li>";
    });
    html += "</ul>";
  } else {
    html += "<div class='drill-section-title'>Notable colleges</div>"
          + "<div style='font-size:13px;color:var(--muted);padding:8px 0;'>Detailed college list for " + district + " not curated yet. Visit tneaonline.org for the full list of TNEA-participating colleges in this district.</div>";
  }
  document.getElementById('rightPanel').innerHTML = html;
}

window.clearSelection = function() {
  selectedDistrict = null;
  d3.selectAll("#tn-map path.district").classed("selected", false);
  renderTopDistricts();
};

document.querySelectorAll('.filter-pill').forEach(btn => {
  btn.addEventListener('click', () => render(btn.dataset.filter));
});

document.getElementById('hamburger').addEventListener('click', () => {
  document.getElementById('navLinks').classList.toggle('open');
});

const io = new IntersectionObserver((entries) => {
  entries.forEach(e => { if (e.isIntersecting) e.target.classList.add('visible'); });
}, { threshold: 0.1 });
document.querySelectorAll('.reveal').forEach(el => io.observe(el));

renderTopDistricts();

// ════════════════════════════════════════════════════════════════
// COLLEGES BROWSER — TN-specific subset
// ════════════════════════════════════════════════════════════════
const BRANCH_LABELS = {
  CSE: "Computer Science", IT: "Information Tech", AIML: "AI & ML", AIDS: "AI & Data Science",
  ECE: "Electronics & Comm", EEE: "Electrical & Electronics", Mech: "Mechanical", Civil: "Civil",
  Chem: "Chemical", Bio: "Biotechnology", Auto: "Automobile", Aero: "Aerospace",
  Mechatronics: "Mechatronics", Robot: "Robotics", Food: "Food Tech", Marine: "Marine"
};

// TN-specific college DB with cut-offs
const TN_COLLEGES = [
  { n: "Anna University CEG", d: "Chennai", t: "Constituent", co: 199, b: ["CSE","IT","ECE","EEE","Mech","Civil","Chem","Bio","Geo","Aero","Auto","Mining","Mfg","Mat","Print","Rubber"] },
  { n: "MIT Chrompet", d: "Chennai", t: "Constituent", co: 199, b: ["CSE","IT","ECE","EEE","Mech","Civil","Auto","Aero","Prod"] },
  { n: "AC Tech Anna Univ", d: "Chennai", t: "Constituent", co: 197, b: ["CSE","Chem","Bio","Food","Pharma","Mat"] },
  { n: "PSG College of Tech", d: "Coimbatore", t: "SF", co: 198.5, b: ["CSE","IT","ECE","EEE","Mech","Civil","Chem","Auto","Bio","Prod","Robot","Mechatronics","AIML"] },
  { n: "SSN College of Engg", d: "Kanchipuram", t: "SF", co: 198, b: ["CSE","IT","ECE","EEE","Mech","Civil","Chem","Bio"] },
  { n: "CIT Coimbatore", d: "Coimbatore", t: "SF", co: 197.5, b: ["CSE","IT","ECE","EEE","Mech","Civil","AIDS"] },
  { n: "Govt CT Coimbatore", d: "Coimbatore", t: "Govt", co: 197, b: ["CSE","ECE","EEE","Mech","Civil"] },
  { n: "Sri Sivasubramaniya Nadar", d: "Kanchipuram", t: "SF", co: 196, b: ["CSE","IT","ECE","EEE","Mech","Civil"] },
  { n: "Rajalakshmi Engg College", d: "Chengalpattu", t: "SF", co: 192, b: ["CSE","IT","ECE","EEE","Mech","Civil","AIML","AIDS"] },
  { n: "Thiagarajar College of Engg", d: "Madurai", t: "SF", co: 192, b: ["CSE","IT","ECE","EEE","Mech","Civil","Mechatronics","AIDS"] },
  { n: "Kumaraguru CoT", d: "Coimbatore", t: "SF", co: 191, b: ["CSE","IT","ECE","EEE","Mech","Civil","Auto","AIDS","Robot"] },
  { n: "Bharathidasan IoT (BIT)", d: "Tiruchirappalli", t: "Constituent", co: 191, b: ["CSE","IT","ECE","EEE","Mech","Civil"] },
  { n: "Bannari Amman IoT", d: "Erode", t: "SF", co: 190, b: ["CSE","IT","ECE","EEE","Mech","Civil","Bio","AIML","Mechatronics","Food"] },
  { n: "Kongu Engineering College", d: "Erode", t: "SF", co: 187, b: ["CSE","IT","ECE","EEE","Mech","Civil","Chem","Food","Auto"] },
  { n: "Velammal Engg College", d: "Chennai", t: "SF", co: 187, b: ["CSE","IT","ECE","EEE","Mech","Civil","Bio","AIDS","Cyber"] },
  { n: "Sri Sairam Engg College", d: "Chennai", t: "SF", co: 185, b: ["CSE","IT","ECE","EEE","Mech","Civil","AIDS"] },
  { n: "Sri Sai Ram (Tambaram)", d: "Chengalpattu", t: "SF", co: 185, b: ["CSE","IT","ECE","EEE","Mech","Civil","AIML"] },
  { n: "Easwari Engg College", d: "Chennai", t: "SF", co: 184, b: ["CSE","IT","ECE","EEE","Mech","Civil","AIML","AIDS"] },
  { n: "Anna University Madurai Regional", d: "Madurai", t: "Constituent", co: 184, b: ["CSE","IT","ECE","EEE","Mech","Civil"] },
  { n: "National Engg College", d: "Tirunelveli", t: "SF", co: 184, b: ["CSE","IT","ECE","EEE","Mech","Civil"] },
  { n: "Mepco Schlenk Engg College", d: "Virudhunagar", t: "Aided", co: 182, b: ["CSE","IT","ECE","EEE","Mech","Civil","Chem","AIDS"] },
  { n: "Saveetha Engg College", d: "Chengalpattu", t: "SF", co: 182, b: ["CSE","IT","ECE","EEE","Mech","Civil","Bio","AIML","AIDS","Cyber"] },
  { n: "Sona College of Tech", d: "Salem", t: "SF", co: 178, b: ["CSE","IT","ECE","EEE","Mech","Civil","Bio"] },
  { n: "Karunya Inst of Tech", d: "Coimbatore", t: "SF", co: 178, b: ["CSE","IT","ECE","EEE","Mech","Civil","Aero","Bio","Food","AIDS"] },
  { n: "Hindustan Inst of T&S", d: "Chengalpattu", t: "SF", co: 178, b: ["CSE","IT","ECE","EEE","Mech","Civil","Auto","Aero","AIML"] },
  { n: "Govt CT Madurai", d: "Madurai", t: "Govt", co: 178, b: ["CSE","ECE","EEE","Mech","Civil"] },
  { n: "K.S. Rangasamy CT", d: "Namakkal", t: "SF", co: 178, b: ["CSE","IT","ECE","EEE","Mech","Civil","Auto"] },
  { n: "PSNA College of Engg", d: "Dindigul", t: "SF", co: 174, b: ["CSE","IT","ECE","EEE","Mech","Civil"] },
  { n: "Sri Krishna College of Engg", d: "Coimbatore", t: "SF", co: 174, b: ["CSE","IT","ECE","EEE","Mech","AIDS"] },
  { n: "Govt CT Erode", d: "Erode", t: "Govt", co: 174, b: ["CSE","ECE","EEE","Mech","Civil"] },
  { n: "Saranathan College of Engg", d: "Tiruchirappalli", t: "SF", co: 174, b: ["CSE","IT","ECE","EEE","Mech","Civil","AIDS"] },
  { n: "Vel Tech Engg College", d: "Tiruvallur", t: "SF", co: 174, b: ["CSE","IT","ECE","EEE","Mech","Civil","Auto","Aero"] },
  { n: "Adhiyamaan College of Engg", d: "Krishnagiri", t: "SF", co: 172, b: ["CSE","IT","ECE","EEE","Mech","Civil"] },
  { n: "Govt CT Salem", d: "Salem", t: "Govt", co: 172, b: ["CSE","ECE","EEE","Mech","Civil"] },
  { n: "Govt CT Tirunelveli", d: "Tirunelveli", t: "Govt", co: 172, b: ["CSE","ECE","EEE","Mech","Civil"] },
  { n: "SRM Valliammai Engg College", d: "Chengalpattu", t: "SF", co: 168, b: ["CSE","IT","ECE","EEE","Mech","Civil","AIDS"] },
  { n: "K Ramakrishnan College of Engg", d: "Tiruchirappalli", t: "SF", co: 168, b: ["CSE","IT","ECE","EEE","Mech","Civil"] },
  { n: "Govt CT Cuddalore", d: "Cuddalore", t: "Govt", co: 168, b: ["CSE","ECE","EEE","Mech","Civil"] },
  { n: "Govt CT Tiruchirappalli", d: "Tiruchirappalli", t: "Govt", co: 188, b: ["CSE","ECE","EEE","Mech","Civil"] },
  { n: "Panimalar IoT", d: "Chennai", t: "SF", co: 165, b: ["CSE","IT","ECE","EEE","Mech","AIDS","Cyber"] },
  { n: "Jeppiaar Engg College", d: "Chennai", t: "SF", co: 162, b: ["CSE","IT","ECE","EEE","Mech","Civil","AIDS"] },
  { n: "Francis Xavier Engg College", d: "Tirunelveli", t: "SF", co: 162, b: ["CSE","IT","ECE","EEE","Mech","Civil"] },
  { n: "M.A.M. College of Engg", d: "Tiruchirappalli", t: "SF", co: 162, b: ["CSE","IT","ECE","EEE","Mech","Civil"] },
  { n: "Velammal CET", d: "Madurai", t: "SF", co: 175, b: ["CSE","IT","ECE","EEE","Mech","Civil"] }
];

const ALL_BRANCHES = Array.from(new Set(TN_COLLEGES.flatMap(c => c.b))).sort();
const ALL_TYPES = ["Govt","Aided","Constituent","SF"];
const ALL_DISTRICTS = Array.from(new Set(TN_COLLEGES.map(c => c.d))).sort();

const browseState = { search: "", types: new Set(), district: "", branches: new Set(), sort: "cutoff" };

(function buildDistrictDropdown() {
  const sel = document.getElementById('districtFilter');
  ALL_DISTRICTS.forEach(d => { const o = document.createElement('option'); o.value = d; o.textContent = d; sel.appendChild(o); });
})();

(function buildTypeChips() {
  const wrap = document.getElementById('typeChips');
  ALL_TYPES.forEach(t => {
    const btn = document.createElement('button');
    btn.className = 'chip'; btn.setAttribute('aria-pressed', 'false');
    btn.textContent = t; btn.dataset.type = t;
    btn.addEventListener('click', () => {
      if (browseState.types.has(t)) browseState.types.delete(t); else browseState.types.add(t);
      btn.setAttribute('aria-pressed', browseState.types.has(t) ? 'true' : 'false');
      renderColleges();
    });
    wrap.appendChild(btn);
  });
})();

(function buildBranchChips() {
  const wrap = document.getElementById('branchChips');
  const order = ["CSE","IT","ECE","EEE","Mech","Civil","Chem","AIML","AIDS","Bio","Auto","Aero","Mechatronics","Robot"];
  const shown = order.filter(b => ALL_BRANCHES.includes(b));
  shown.forEach(b => {
    const btn = document.createElement('button');
    btn.className = 'chip'; btn.setAttribute('aria-pressed', 'false');
    btn.textContent = b; btn.title = BRANCH_LABELS[b] || b; btn.dataset.branch = b;
    btn.addEventListener('click', () => {
      if (browseState.branches.has(b)) browseState.branches.delete(b); else browseState.branches.add(b);
      btn.setAttribute('aria-pressed', browseState.branches.has(b) ? 'true' : 'false');
      renderColleges();
    });
    wrap.appendChild(btn);
  });
})();

document.getElementById('searchInput').addEventListener('input', e => { browseState.search = e.target.value.toLowerCase().trim(); renderColleges(); });
document.getElementById('districtFilter').addEventListener('change', e => { browseState.district = e.target.value; renderColleges(); });
document.getElementById('sortBy').addEventListener('change', e => { browseState.sort = e.target.value; renderColleges(); });
document.getElementById('resetFilters').addEventListener('click', () => {
  browseState.search = ""; browseState.types.clear(); browseState.district = "";
  browseState.branches.clear(); browseState.sort = "cutoff";
  document.getElementById('searchInput').value = "";
  document.getElementById('districtFilter').value = "";
  document.getElementById('sortBy').value = "cutoff";
  document.querySelectorAll('#typeChips .chip, #branchChips .chip').forEach(c => c.setAttribute('aria-pressed', 'false'));
  renderColleges();
});

function renderColleges() {
  let list = TN_COLLEGES.slice();
  if (browseState.search) {
    const q = browseState.search;
    list = list.filter(c => c.n.toLowerCase().includes(q) || c.d.toLowerCase().includes(q));
  }
  if (browseState.types.size > 0) list = list.filter(c => browseState.types.has(c.t));
  if (browseState.district) list = list.filter(c => c.d === browseState.district);
  if (browseState.branches.size > 0) list = list.filter(c => Array.from(browseState.branches).every(b => c.b.includes(b)));

  list.sort((a, b) => {
    if (browseState.sort === "name") return a.n.localeCompare(b.n);
    if (browseState.sort === "district") return a.d.localeCompare(b.d) || a.n.localeCompare(b.n);
    if (browseState.sort === "type") { const order = ["Constituent","Govt","Aided","SF"]; return order.indexOf(a.t) - order.indexOf(b.t) || a.n.localeCompare(b.n); }
    return (b.co || 0) - (a.co || 0); // cut-off high to low
  });

  document.getElementById('resultsCount').textContent = list.length;
  const grid = document.getElementById('collegesGrid');
  if (list.length === 0) {
    grid.style.gridTemplateColumns = "1fr";
    grid.innerHTML = "<div class='no-results'><strong>No colleges match your filters</strong>Try removing a filter or different search term.</div>";
    return;
  }
  grid.style.gridTemplateColumns = "";
  grid.innerHTML = list.map(c => {
    const tagClass = c.t.toLowerCase();
    const branchHtml = c.b.map(b => "<span class='branch-chip' title='" + (BRANCH_LABELS[b] || b) + "'>" + b + "</span>").join("");
    return "<article class='college-card'>"
         + "<div class='cc-head'>"
           + "<div class='cc-name'>" + c.n + "</div>"
           + "<div class='cc-tags'>"
             + "<span class='cc-tag cutoff'>CSE " + c.co + "</span>"
             + "<span class='cc-tag " + tagClass + "'>" + c.t + "</span>"
           + "</div>"
         + "</div>"
         + "<div class='cc-loc'>" + c.d + " district</div>"
         + "<div class='cc-sep'></div>"
         + "<div class='cc-branches-label'><strong>" + c.b.length + "</strong> branches offered</div>"
         + "<div class='branch-chips'>" + branchHtml + "</div>"
         + "</article>";
  }).join("");
}

renderColleges();

;

	const heightObserver = new ResizeObserver(([{ contentRect }]) => {
		window.parent.postMessage({ action: 'iframeHeightUpdated', height: contentRect.height, id: 'z_WV04' }, '*');
	});

	heightObserver.observe(document.documentElement);
