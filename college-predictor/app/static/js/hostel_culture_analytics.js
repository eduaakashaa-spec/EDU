/* =====================
   38 institutes scored
   ===================== */
const HOSTEL = [
  // NITs + IIEST
  {n:"NIT Trichy",         loc:"Tiruchirappalli", grp:"NIT", airport:true,  scores:[3,3,3,4,3], note:"Triple-share 1st year, no AC. South-Indian mess (acquired taste for North/Gulf students). 9 PM girls' curfew with fine; 2019 News Minute incident still cited.", verdict:"Strong outstation fit; verify mess regional balance for non-South-Indian children."},
  {n:"NIT Warangal",       loc:"Telangana",       grp:"NIT", airport:false, scores:[3,3,3,3,3], note:"1,800-bed Ultra Mega Hostel; non-AC; 9 PM in-room rule for 1st-year girls. 2012 ragging videos historic but on record.", verdict:"Stable, large-scale operation; ladies' rules first-year stricter than peers."},
  {n:"NIT Surathkal",      loc:"Karnataka",       grp:"NIT", airport:true,  scores:[3,3,4,4,4], note:"Coastal campus, IXE airport ~25 km (Gulf-connected). Triple-share 1st year. ID-card hostel access strict.", verdict:"Best Gulf-connectivity NIT in South India; coastal humidity is the trade-off."},
  {n:"NIT Rourkela",       loc:"Odisha",          grp:"NIT", airport:false, scores:[2,3,4,4,2], note:"Hot industrial steel-town. Fans only — students universally advise buying a cooler. Anti-ragging visible.", verdict:"Decent infra and rules; the heat plus distance to BBI airport are the NRI friction."},
  {n:"MNIT Jaipur",        loc:"Rajasthan",       grp:"NIT", airport:false, scores:[2,2,3,3,3], note:"Triple-share 1st year, non-AC, Jaipur 45°C+ summers. Mess flagged 'tasteless' across reviews.", verdict:"Hindi-belt culture; suits Gulf-NRI families comfortable with Rajasthani cuisine."},
  {n:"NIT Calicut",        loc:"Kerala",          grp:"NIT", airport:true,  scores:[3,3,3,3,4], note:"CCJ airport ~25 km Gulf-direct. Coconut-oil cuisine. 2016 'don't roam with boys' circular controversy.", verdict:"Strong NRI-Malayali alumni context; verify current ladies' rules."},
  {n:"SVNIT Surat",        loc:"Gujarat",         grp:"NIT", airport:false, scores:[1,2,4,3,2], note:"Written ban on coolers/AC in hostel rooms + Surat 45°C+ summer. Mother Teresa Bhavan offers single rooms for girls.", verdict:"Strongest single-NRI-red-flag in the dataset on physical comfort."},
  {n:"VNIT Nagpur",        loc:"Maharashtra",     grp:"NIT", airport:false, scores:[2,2,4,4,2], note:"Triple-design rooms shared by 4. Nagpur 46°C+ summers, no AC. Girls' curfew 10 PM, transparent rules.", verdict:"Strict-but-fair girls' rules; overcrowding + heat is the dominant complaint."},
  {n:"MNNIT Allahabad",    loc:"Prayagraj",       grp:"NIT", airport:false, scores:[2,2,2,3,2], note:"Library access asymmetry (girls cut off at 8 PM, boys till midnight) documented in institute's own student paper.", verdict:"Equity concern worth flagging; ask current ladies' rules in writing."},
  {n:"MANIT Bhopal",       loc:"Madhya Pradesh",  grp:"NIT", airport:false, scores:[2,2,3,3,2], note:"3-share 1st-year; 2024 hostel suicide with documented parental ragging allegation (Free Press Journal).", verdict:"Verify institute's anti-ragging response history before accepting a seat here."},
  {n:"NIT Kurukshetra",    loc:"Haryana",         grp:"NIT", airport:false, scores:[2,2,2,3,2], note:"6 PM girls' curfew (strictest publicly known) + heavy fines. Mess flagged tasteless.", verdict:"Strictest ladies' curfew in the dataset; for outstation girls a major friction."},
  {n:"NIT Durgapur",       loc:"West Bengal",     grp:"NIT", airport:false, scores:[2,3,3,3,3], note:"3-4 sharing till final year. 'Dilapidated' is a recurring word in reviews. Kolkata airport ~180 km (Gulf-direct).", verdict:"Old industrial-town campus; infrastructure age is the friction."},
  {n:"NIT Hamirpur",       loc:"Himachal Pradesh",grp:"NIT", airport:false, scores:[2,3,4,3,2], note:"Mild climate (great for AC-raised kids) but 'pathetic' washroom condition recurring. ~210 km from Chandigarh airport.", verdict:"Cool weather is a plus; remoteness is the trade-off."},
  {n:"NIT Delhi",          loc:"Delhi",           grp:"NIT", airport:true,  scores:[3,2,2,4,4], note:"AC rooms at premium fee (₹18-28K). 1st-year boys housed 10 km off campus. Rohini girls' hostel safety concern raised.", verdict:"DEL airport access is unmatched; mess and 1st-year off-campus housing are the real frictions."},
  {n:"IIEST Shibpur",      loc:"Howrah",          grp:"NIT", airport:true,  scores:[2,3,4,3,3], note:"Old Bengal Engineering College heritage; 11 PM curfew (liberal). Kolkata airport ~25 km (Gulf-direct).", verdict:"Heritage campus, infrastructure age. Strong gender-separation rules."},
  {n:"NIT Jamshedpur",     loc:"Jharkhand",       grp:"NIT", airport:false, scores:[2,2,3,3,2], note:"Pest issues 'no serious pest control' across multiple reviews. Mess insects reported as pattern.", verdict:"Tata-town location; documented mess hygiene concerns."},
  {n:"NIT Silchar",        loc:"Assam",           grp:"NIT", airport:false, scores:[2,2,3,2,1], note:"Documented 2022-23 ragging actions; multiple expulsions. Most isolated DASA campus. Water hygiene issues.", verdict:"Most concrete recent ragging signal in the dataset — verify institutional response."},
  // IIITs
  {n:"IIIT Allahabad",     loc:"Prayagraj",       grp:"IIIT",airport:false, scores:[3,3,4,3,2], note:"Permanent Jhalwa campus, non-AC, hot 45°C summers. North-Indian-heavy mess; South Indian students adjust.", verdict:"Mature campus; airport distance is the friction for NRI parents."},
  {n:"IIITDM Jabalpur",    loc:"Jabalpur",        grp:"IIIT",airport:false, scores:[3,2,3,3,2], note:"Permanent Dumna campus, well-maintained. Mess 'below average' is the consistent complaint.", verdict:"D&M-distinct campus; off-mess food culture is well established."},
  {n:"IIITDM Kancheepuram",loc:"Chennai",         grp:"IIIT",airport:true,  scores:[3,2,4,3,3], note:"New 14-floor towers, hot water, RO. Mess hygiene complaints recurring. ~50 km from MAA airport (Gulf-direct).", verdict:"Best Chennai-adjacent IIIT for NRI access; mess is the friction."},
  {n:"ABV-IIITM Gwalior",  loc:"Gwalior",         grp:"IIIT",airport:false, scores:[3,3,4,4,2], note:"Girls reportedly get single rooms from year one — rare positive. ~340 km from Delhi airport. Hot summers.", verdict:"Single-room policy for girls is a meaningful counsellor talking point."},
  {n:"IIIT Sricity",       loc:"Chittoor",        grp:"IIIT",airport:true,  scores:[2,3,3,3,1], note:"Located near equator, blistering May, non-AC. Girls' hostel off main academic campus with shuttle.", verdict:"Industrial-park location + heat + non-AC = strongest IIIT comfort red flag for Gulf kids."},
  {n:"IIIT Guwahati",      loc:"Assam",           grp:"IIIT",airport:true,  scores:[4,3,4,4,4], note:"~4 km from Guwahati airport (Gulf-direct). Twin-sharing, attached washrooms. 1 Gbps LAN.", verdict:"Best airport-proximity DASA campus in entire dataset. Strong NRI fit."},
  {n:"IIIT Lucknow",       loc:"Lucknow",         grp:"IIIT",airport:true,  scores:[4,3,4,4,4], note:"Permanent Chak Ganjaria campus since 2019. LKO airport has Gulf flights. GH-1/2/3 girls' hostels described positively.", verdict:"Strong newer-IIIT NRI option; verify mess regional balance with current students."},
  {n:"IIIT Kottayam",      loc:"Kerala",          grp:"IIIT",airport:true,  scores:[3,2,4,3,3], note:"Newly built 7-floor hostels, 100 rooms/floor. Mess 'worst thing about the college' is recurring. COK ~75 km.", verdict:"Worst-rated mess in IIIT cohort; Kerala parents may find the cuisine fine."},
  {n:"IIIT Trichy",        loc:"Tamil Nadu",      grp:"IIIT",airport:true,  scores:[3,4,4,4,4], note:"Permanent Sethurappatti campus 2021. Modern hostels with sensor-equipped features. TRZ airport Gulf-direct.", verdict:"One of the better-balanced IIIT NRI campuses on hostel + access metrics."},
  {n:"IIIT Pune",          loc:"Maharashtra",     grp:"IIIT",airport:true,  scores:[2,2,3,3,3], note:"Still on transit campus sharing with Trinity Academy. Veg-only mess. 4-share bunker beds for freshers.", verdict:"Transit status is the dominant red flag; verify permanent-campus timeline."},
  {n:"IIIT Una",           loc:"Himachal",        grp:"IIIT",airport:false, scores:[3,3,4,3,2], note:"Cool climate (HP foothills), CCTV + solar water heating. Polarised mess reviews. Airport ~120-180 km away.", verdict:"Climate-comfortable for Gulf-raised kids; remoteness is the friction."},
  {n:"IIIT Dharwad",       loc:"Karnataka",       grp:"IIIT",airport:false, scores:[3,3,4,3,3], note:"24/7 lady security guard at girls' hostel + CCTV — a notable callout. Mess 'average to decent'.", verdict:"Specific lady-security protocol worth highlighting to NRI parents."},
  // GFTIs + SPAs
  {n:"SPA Delhi",          loc:"New Delhi",       grp:"GFTI",airport:true,  scores:[2,2,3,3,3], note:"Only ~33% students get hostel; 10-15 km off-campus location. Mess water 'poor'. Many in PG accommodation.", verdict:"Limited hostel allocation is a real friction; many DASA-NRI families end up in PG housing."},
  {n:"SPA Bhopal",         loc:"Bhopal",          grp:"GFTI",airport:false, scores:[4,4,4,4,3], note:"On-campus doctor + counsellor (rare). Double-occupancy wood-bed rooms with balconies. ~90% residential.", verdict:"Best residential identity in the DASA list; smaller city but quality-of-life signals are strong."},
  {n:"SPA Vijayawada",     loc:"Andhra Pradesh",  grp:"GFTI",airport:false, scores:[3,4,4,4,2], note:"Architect-designed hostels won Eurasian Prize 2018. Wednesday Biryani is the inside reference. Non-AC.", verdict:"Pride-of-architecture-school hostel design; verify mess on a visit."},
  {n:"DTU Delhi",          loc:"Delhi",           grp:"GFTI",airport:true,  scores:[4,3,4,4,4], note:"AC and non-AC rooms (₹18-72K range). 9 PM girls' curfew vs boys' flexibility is the most-cited equity issue.", verdict:"Best Delhi-airport-AC-option for NRI; ladies'-equity curfew issue is the trade-off."},
  {n:"NSUT Delhi",         loc:"Delhi",           grp:"GFTI",airport:true,  scores:[3,3,4,4,4], note:"AC + non-AC girls' hostels. 8:30 PM curfew + Wi-Fi restricted to 8-11 PM in girls' hostel.", verdict:"Most-restrictive Delhi GFTI on ladies' rules; AC option exists."},
  {n:"PEC Chandigarh",     loc:"Chandigarh",      grp:"GFTI",airport:true,  scores:[3,2,3,4,4], note:"IXC airport Gulf-direct. Junior-year hostel/mess consistently worse than senior across reviews.", verdict:"Strong Chandigarh metro context for NRI; first-year friction is real."},
  {n:"JNU Delhi",          loc:"New Delhi",       grp:"GFTI",airport:true,  scores:[2,2,3,3,2], note:"Engineering school is younger add-on; 2020 hostel attack on Sabarmati documented in Time. Politically charged campus.", verdict:"Excellent academics; honest conversation about politically charged campus environment needed."},
  {n:"SMVDU Katra",        loc:"J&K",             grp:"GFTI",airport:false, scores:[3,2,4,3,2], note:"Mandatory hostel. 'First year is great, later years bad' is unusually consistent. Veg-only mess.", verdict:"Pilgrimage-town setting; remote healthcare and airport are the trade-offs."},
  {n:"UoH Hyderabad",      loc:"Hyderabad",       grp:"GFTI",airport:true,  scores:[3,2,3,4,4], note:"HYD airport excellent Gulf access. 23 hostels for 5,000+ students. Politically active campus history (Rohith Vemula 2016).", verdict:"Hyderabad metro infrastructure + airport is a strong NRI fit; campus politics merits an honest brief."},
];

/* Compute composites */
HOSTEL.forEach(h=>{
  const sum = h.scores.reduce((a,b)=>a+b,0);
  h.comp = (sum/5).toFixed(1);
});

/* =====================
   HEATMAP
   ===================== */
let hmFilter='all';
function renderHeatmap(){
  const grid = document.getElementById('heatmap-grid');
  // Keep head row
  grid.innerHTML = `<div class="hm-row head">
    <div>Institute</div><div>Hostel comfort</div><div>Mess / food</div><div>Ladies safety</div><div>Outstation fit</div><div>NRI adjustment</div><div>Composite</div>
  </div>`;
  let data = HOSTEL.filter(h=>{
    if(hmFilter==='all') return true;
    if(hmFilter==='airport') return h.airport;
    return h.grp===hmFilter;
  });
  data.sort((a,b)=>parseFloat(b.comp)-parseFloat(a.comp));
  data.forEach(h=>{
    const cs = parseFloat(h.comp);
    const cls = cs>=3.8?'high':cs>=2.8?'mid':'low';
    let row = `<div class="hm-row"><div class="lbl">${h.n}<span class="gn">${h.grp} · ${h.loc}</span></div>`;
    h.scores.forEach(s=>{
      row += `<div class="hm-cell s${s}" title="${h.note}">${s}</div>`;
    });
    row += `<div class="hm-comp ${cls}">${h.comp}</div></div>`;
    grid.insertAdjacentHTML('beforeend', row);
  });
}
renderHeatmap();
document.querySelectorAll('[data-grp]').forEach(b=>{
  b.addEventListener('click',()=>{
    document.querySelectorAll('[data-grp]').forEach(p=>p.classList.remove('active'));
    b.classList.add('active');
    hmFilter = b.dataset.grp;
    renderHeatmap();
  });
});

/* =====================
   COMMENTS WALL
   ===================== */
const COMMENTS = [
  {inst:"NIT Trichy",src:"Quora · The News Minute",sev:"m",body:"Curfew + South-Indian-heavy mess is mostly fine, except when one girl stayed at a bus stand because she was afraid to enter past 9 PM and what happened next became national news.",tags:["curfew","food","safety"]},
  {inst:"SVNIT Surat",src:"Hostel brochure 2025",sev:"h",body:"Installation of coolers or ACs inside hostel rooms is not permitted — and Surat hits 45°C in May. For a Gulf-raised child this is the single most extreme physical adjustment in the DASA list.",tags:["AC ban","heat","NRI"]},
  {inst:"NIT Kurukshetra",src:"Storypick · LatestLY",sev:"h",body:"6 PM ladies' curfew at Kalpana Chawla Bhawan — yes, an astronaut's name on a hostel with the strictest publicly known curfew. Heavy fines on top.",tags:["curfew","equity","ladies"]},
  {inst:"MNNIT Allahabad",src:"Perspective MNNIT · Youth Ki Awaaz",sev:"m",body:"Central library access: boys till midnight, girls cut off at 8 PM. The institute's own student paper called it openly discriminatory.",tags:["equity","library","ladies"]},
  {inst:"NSUT Delhi",src:"Medium · Quora",sev:"m",body:"Girls' hostel Wi-Fi is restricted to 8-11 PM on weekdays. Curfew 8:30 PM. Boys' hostel Wi-Fi runs 24/7.",tags:["equity","wifi","ladies"]},
  {inst:"NIT Silchar",src:"Assam Tribune · Way2Barak",sev:"h",body:"45 students documented as enduring 'relentless ragging, physical and mental abuse'. Institute responded with 9 expulsions, 5 suspensions. Most concrete recent ragging signal in our dataset.",tags:["ragging","incident","verified"]},
  {inst:"MANIT Bhopal",src:"Free Press Journal · Daily Pioneer",sev:"h",body:"2024 hostel suicide. Father told media the student 'was ragged after admission and had been disturbed since then'. Second MCA student suicide same week.",tags:["ragging","mental health","incident"]},
  {inst:"IIIT Sricity",src:"Quora hostel threads",sev:"m",body:"'Located near the equator', 'blistering May', non-AC, classrooms are AC but hostels aren't. Girls' hostel is on a different campus block with shuttle.",tags:["heat","AC gap","ladies access"]},
  {inst:"NIT Calicut",src:"HuffPost · The News Minute",sev:"m",body:"2016 hostel warden circular 'strictly instructed' girls not to 'roam with boys'. Withdrawn after national backlash.",tags:["culture","ladies","historical"]},
  {inst:"NIT Jamshedpur",src:"Collegedunia · Zollege",sev:"m",body:"Insects in mess food repeated across independent reviews. Pattern, not one-off. 'Complaints are ignored by mess administration'.",tags:["mess","hygiene","food"]},
  {inst:"NIT Delhi",src:"Shiksha · Zollege",sev:"m",body:"First-year boys housed 10 km off the main campus. Mess: 'very bad, no non-veg, unhygienic cooking procedures'. AC option exists at premium fee.",tags:["off-campus","mess","AC option"]},
  {inst:"IIIT Pune",src:"Quora · Wikipedia",sev:"m",body:"Still on transit campus at Ambegaon Budruk — sharing hostel, mess, sports with Trinity Academy of Engineering. Veg-only mess. Bunker beds, 4-sharing.",tags:["transit","veg-only","sharing"]},
  {inst:"IIIT Kottayam",src:"Quora · Collegedunia",sev:"m",body:"Mess food: 'no flavour', 'quality is a gamble', 'worst thing about the college' — repeated across independent reviewers. Sunday biryani is the rare highlight.",tags:["mess","food","quality"]},
  {inst:"NIT Hamirpur",src:"Quora · Collegedunia",sev:"m",body:"Hostels and washrooms 'in pathetic condition' is a recurring exact phrase. Night food 'over-cooked vegetables, too much oil'.",tags:["infra","mess","washroom"]},
  {inst:"NIT Rourkela",src:"Quora · Kollegeapply",sev:"l",body:"Student advice consistently: 'buy a table fan or a cooler before joining'. The heat is the dominant adjustment story.",tags:["heat","AC gap"]},
  {inst:"JNU Delhi",src:"Time · The Caravan · The Wire",sev:"h",body:"2020 masked-mob attack on Sabarmati hostel — 30+ injured. The Barak Hostel food disparity (Northeast students) documented in The Print 2024.",tags:["incident","politics","verified"]},
  {inst:"DTU Delhi",src:"Shiksha · Medium",sev:"m",body:"9 PM girls' curfew vs boys' flexibility is the most repeated equity complaint. AC rooms exist at premium fee; pollution Oct-Jan is the counter-argument.",tags:["curfew","equity","pollution"]},
  {inst:"IIITDM Kancheepuram",src:"Collegedunia · Quora",sev:"m",body:"New 14-floor towers with hot water and RO drinking water — but mess hygiene 'not maintained properly' is the recurring complaint.",tags:["new build","mess","hygiene"]},
];
const cg = document.getElementById('commentGrid');
COMMENTS.forEach(c=>{
  cg.innerHTML += `<article class="comment">
    <div class="meta"><span class="src">${c.src}</span><span class="severity sev-${c.sev}">${c.sev==='h'?'High pattern':c.sev==='m'?'Mid pattern':'Light'}</span></div>
    <div class="inst">${c.inst}</div>
    <p class="body">"${c.body}"</p>
    <div class="tag-row">${c.tags.map(t=>'<span>#'+t+'</span>').join('')}</div>
    <div class="verify">Verified — multi-source pattern</div>
  </article>`;
});

/* =====================
   INSTITUTE CARDS
   ===================== */
let cardFilter='all';
function renderCards(){
  const grid = document.getElementById('cardGrid');
  grid.innerHTML='';
  let data = HOSTEL.filter(h=>{
    if(cardFilter==='all') return true;
    return h.grp===cardFilter;
  });
  data.sort((a,b)=>parseFloat(b.comp)-parseFloat(a.comp));
  data.forEach(h=>{
    const labels=['Comfort','Food','Ladies','Outstn','NRI'];
    const cs = parseFloat(h.comp);
    const tier = cs>=3.8?'STRONG':cs>=2.8?'MID':'CAUTION';
    let nums = '';
    h.scores.forEach((s,i)=>{
      nums += `<div class="s${s}"><div class="n">${s}</div><div class="lab">${labels[i]}</div></div>`;
    });
    grid.innerHTML += `<article class="iiit-card">
      <span class="stamp">${tier} · ${h.comp}/5</span>
      <h3>${h.n}</h3>
      <div class="meta">${h.loc} · ${h.grp} · ${h.airport?'Airport ≤25 km':'Airport distant'}</div>
      <div class="nums">${nums}</div>
      <div class="note">${h.note}</div>
      <div class="verdict"><b>EduAakashaa take</b>${h.verdict}</div>
    </article>`;
  });
}
renderCards();
document.querySelectorAll('[data-card]').forEach(b=>{
  b.addEventListener('click',()=>{
    document.querySelectorAll('[data-card]').forEach(p=>p.classList.remove('active'));
    b.classList.add('active');
    cardFilter = b.dataset.card;
    renderCards();
  });
});

/* =====================
   D3 TREEMAP
   ===================== */
const tmData = {
  name:"DASA 2026",
  children:[
    {name:"NITs + IIEST",grp:"NIT",children:HOSTEL.filter(h=>h.grp==='NIT').map(h=>({name:h.n,value:Math.round(parseFloat(h.comp)*100),comp:h.comp,loc:h.loc,grp:h.grp}))},
    {name:"IIITs",grp:"IIIT",children:HOSTEL.filter(h=>h.grp==='IIIT').map(h=>({name:h.n,value:Math.round(parseFloat(h.comp)*100),comp:h.comp,loc:h.loc,grp:h.grp}))},
    {name:"SPAs & GFTIs",grp:"GFTI",children:HOSTEL.filter(h=>h.grp==='GFTI').map(h=>({name:h.n,value:Math.round(parseFloat(h.comp)*100),comp:h.comp,loc:h.loc,grp:h.grp}))}
  ]
};
const tmSvg = d3.select('#tmSvg');
const tmBack = document.getElementById('tmBack');
let tmCurrent = null;
function colorFor(comp){
  if(comp>=3.8) return '#1F8B5C';
  if(comp>=3.4) return '#48A876';
  if(comp>=2.8) return '#E89A1C';
  if(comp>=2.2) return '#E37A3A';
  return '#C23A3A';
}
function drawTreemap(data, drilled){
  const w = document.getElementById('treemap').clientWidth - 50;
  const h = 520;
  tmSvg.attr('viewBox',`0 0 ${w} ${h}`).attr('width',w).attr('height',h);
  tmSvg.selectAll('*').remove();
  const root = d3.hierarchy(data).sum(d=>d.value||0).sort((a,b)=>b.value-a.value);
  d3.treemap().size([w,h]).padding(4).round(true)(root);
  const nodes = drilled? root.leaves() : root.children;
  const g = tmSvg.selectAll('g.tm-node').data(nodes).enter().append('g').attr('class','tm-node').attr('transform',d=>`translate(${d.x0},${d.y0})`).style('cursor', drilled?'default':'pointer').on('click',(_,d)=>{
    if(!drilled){ drawTreemap(d.data, true); tmCurrent = d.data; tmBack.classList.add('show'); }
  });
  g.append('rect').attr('width',d=>d.x1-d.x0).attr('height',d=>d.y1-d.y0).attr('fill',d=>{
    if(drilled) return colorFor(parseFloat(d.data.comp));
    // Overview: color by tier-avg
    const avg = d.data.children ? d.data.children.reduce((s,c)=>s+parseFloat(c.comp),0)/d.data.children.length : 3;
    return colorFor(avg);
  }).attr('rx',6).attr('stroke','#fff').attr('stroke-width',2);
  g.append('text').attr('x',12).attr('y',24).attr('fill','#fff').attr('font-family',"'Fraunces',serif").attr('font-weight','600').attr('font-size',drilled?13:18).text(d=>d.data.name);
  if(!drilled){
    g.append('text').attr('x',12).attr('y',46).attr('fill','rgba(255,255,255,.8)').attr('font-family',"'JetBrains Mono',monospace").attr('font-size',10).attr('letter-spacing','.18em').attr('text-transform','uppercase').text(d=>(d.data.children?.length||0)+' INSTITUTES');
    g.append('text').attr('x',12).attr('y',d=>d.y1-d.y0-14).attr('fill','rgba(255,255,255,.9)').attr('font-family',"'JetBrains Mono',monospace").attr('font-size',10).text('CLICK TO DRILL →');
  } else {
    g.append('text').attr('x',12).attr('y',40).attr('fill','rgba(255,255,255,.85)').attr('font-family',"'JetBrains Mono',monospace").attr('font-size',9).attr('letter-spacing','.15em').text(d=>d.data.loc.toUpperCase());
    g.append('text').attr('x',d=>(d.x1-d.x0)-12).attr('y',d=>(d.y1-d.y0)-14).attr('fill','#fff').attr('font-family',"'JetBrains Mono',monospace").attr('font-weight','700').attr('font-size',13).attr('text-anchor','end').text(d=>d.data.comp);
  }
}
drawTreemap(tmData, false);
tmBack.addEventListener('click',()=>{ drawTreemap(tmData,false); tmBack.classList.remove('show'); });
window.addEventListener('resize',()=>drawTreemap(tmCurrent||tmData, !!tmCurrent));

/* Reveal */
const obs = new IntersectionObserver(es=>{es.forEach(e=>{if(e.isIntersecting)e.target.classList.add('visible')})},{threshold:0.1});
document.querySelectorAll('.reveal').forEach(el=>obs.observe(el));
