/* ════════ CONFIG ════════ */
/* This file is public — Flask serves /static to anyone. So it holds no Apps
   Script URL and no access key: both live in the server's env and are used by
   the admin-only proxy routes below (see routes/__init__.py). */
const DATA_URL = "/counsellor-dashboard/data";
const STATUS_URL = "/counsellor-dashboard/status";

/* rank-fit model — MUST match the Choice Builder */
const CLOSE_BASE={T10:60000,B25:95000,B50:140000,B100:210000,NR:340000};
const BR_MULT={"CSE":.45,"IT":.55,"AI & Data Science":.5,"ECE":.7,"EEE / Electrical":.9,"Mechanical":1.1,"Civil":1.3,"Chemical":1.2,"Metallurgy & Materials":1.45,"Production / Industrial":1.3,"Biotechnology":1.2,"Maths & Computing":.6,"Instrumentation":1.2,"Mining":1.5,"Engg Physics":.95,"VLSI Design":.7,"Smart Manufacturing":.9,"Aerospace / Aviation":.9,"Food Technology":1.45,"Marine Engineering":1.35,"Naval Architecture":1.35,"Architecture (B.Arch)":1.0,"Planning (B.Plan)":1.2};
/* institute → NIRF band (same source as Choice Builder) */
const NMAP={"Dr B R Ambedkar NIT Jalandhar":"B100","MNIT Jaipur":"B50","MANIT Bhopal":"B100","MNNIT Allahabad":"B50","NIT Agartala":"NR","NIT Calicut":"B25","NIT Delhi":"B100","NIT Durgapur":"B50","NIT Goa":"B100","NIT Hamirpur":"B100","NIT Karnataka, Surathkal":"B25","NIT Meghalaya":"B100","NIT Nagaland":"NR","NIT Patna":"B100","NIT Puducherry":"NR","NIT Raipur":"B100","NIT Sikkim":"NR","NIT Arunachal Pradesh":"NR","NIT Jamshedpur":"B100","NIT Kurukshetra":"B100","NIT Mizoram":"NR","NIT Rourkela":"B25","NIT Silchar":"B50","NIT Srinagar":"B100","NIT Tiruchirappalli (Trichy)":"T10","NIT Uttarakhand":"NR","NIT Warangal":"B25","SVNIT Surat":"B100","VNIT Nagpur":"B50","NIT Andhra Pradesh":"NR","IIEST Shibpur":"B100","ABV-IIITM Gwalior":"B100","IIIT Kota":"NR","IIIT Guwahati":"NR","IIIT Sonepat":"NR","IIIT Una":"NR","IIIT Sri City, Chittoor":"NR","IIIT Vadodara":"NR","IIIT Allahabad":"B100","IIITDM Kancheepuram":"NR","PDPM IIITDM Jabalpur":"NR","IIIT Tiruchirappalli":"NR","IIIT Dharwad":"NR","IIIT Kottayam":"NR","IIIT Pune":"NR","IIIT Bhagalpur":"NR","IIIT Bhopal":"NR","IIIT Raichur":"NR","IIITV-ICD Diu":"NR","Assam University, Silchar":"NR","GGV Bilaspur (Central University)":"NR","JK Institute, University of Allahabad":"NR","NIAMT Ranchi":"NR","SLIET Longowal":"NR","Tezpur University":"B100","SPA Bhopal":"NR","SPA New Delhi":"NR","SPA Vijayawada":"NR","Shri Mata Vaishno Devi University":"NR","University of Hyderabad":"NR","Punjab Engineering College, Chandigarh":"NR","JNU School of Engineering, New Delhi":"NR","NIFTEM Kundli":"NR","Central University of Jammu":"NR","IET, Dr Harisingh Gour University, Sagar":"NR","Rajiv Gandhi National Aviation University":"NR","IUST Kashmir":"NR","SGSITS Indore":"NR","NITTTR Bhopal":"NR","Central University of Karnataka":"NR","Delhi Technological University (DTU)":"B50","Dr SSB UICET, Panjab University":"NR","Gautam Buddha University, Greater Noida":"NR","IMU Chennai Campus":"NR","IMU Kochi Campus":"NR","IMU Kolkata Campus":"NR","IMU Mumbai Port Campus":"NR","IMU Navi Mumbai Campus":"NR","IMU Visakhapatnam Campus":"NR","MMMUT Gorakhpur":"NR","NSUT Delhi":"B100","UIET PUSSRC Hoshiarpur":"NR","UIET Panjab University, Chandigarh":"NR","HBTU Kanpur":"NR"};

function fitOf(name,brLabel,rank){
  if(!rank||rank<1)return "na";
  const nirf=NMAP[name];if(!nirf)return "na";
  const C=Math.round((CLOSE_BASE[nirf]||300000)*(BR_MULT[brLabel]||1));
  if(rank<=C*0.6)return "safe";
  if(rank<=C)return "target";
  return "dream";
}

/* ════════ DEMO DATA (preview only; replaced by live Sheet when hosted) ════════ */
const DEMO=[
{_row:2,Timestamp:"2026-06-12T09:14:00",Name:"Aarav Menon",Email:"aarav.menon@example.com",WhatsApp:"+971501234567","JEE Main CRL":48000,Category:"NRI",CIWG:"Yes",Country:"United Arab Emirates","Confidence (1-10)":4,"Top Choices":"1. NIT Tiruchirappalli (Trichy) — CSE | 2. NIT Warangal — CSE | 3. NIT Karnataka, Surathkal — CSE | 4. NIT Calicut — CSE | 5. MNNIT Allahabad — CSE","Self-Check Answers":"Q1: Not yet | Q2: Mostly by name | Q3: No — those are fillers | Q4: Somewhat | Q5: Need guidance | Q6: Not discussed","Fallback Strategy (ordered)":"1. CSE / IT / AI at any available institute (branch-first) | 2. Same branch at a lower-NIRF NIT / IIIT / GFTI",Comments:"Father in Dubai 12 yrs. Want only CSE.",Status:"New",Paper:"B.E. / B.Tech (Paper 1)"},
{_row:3,Timestamp:"2026-06-12T15:40:00",Name:"Diya Nair",Email:"diya.nair@example.com",WhatsApp:"+97455512345","JEE Main CRL":132000,Category:"NRI",CIWG:"Yes",Country:"Qatar","Confidence (1-10)":7,"Top Choices":"1. NIT Calicut — ECE | 2. NIT Rourkela — Mechanical | 3. SVNIT Surat — Civil | 4. NIT Raipur — Metallurgy & Materials | 5. NSUT Delhi — IT","Self-Check Answers":"Q1: Some of them | Q2: A mix of both | Q3: Yes | Q4: Yes, clearly | Q5: Yes, decided | Q6: Yes, aligned","Fallback Strategy (ordered)":"1. Same branch at a lower-NIRF NIT / IIIT / GFTI | 2. Prefer location (metro / near family) over ranking | 3. Core branch (Mech / Civil / Chemical) at a top institute",Comments:"",Status:"Contacted",Paper:"B.E. / B.Tech (Paper 1)"},
{_row:4,Timestamp:"2026-06-13T07:05:00",Name:"Rohan Pillai",Email:"rohan.pillai@example.com",WhatsApp:"+966512345678","JEE Main CRL":210000,Category:"NRI",CIWG:"No",Country:"Saudi Arabia","Confidence (1-10)":3,"Top Choices":"1. NIT Tiruchirappalli (Trichy) — CSE | 2. NIT Karnataka, Surathkal — CSE | 3. MNIT Jaipur — CSE","Self-Check Answers":"Q1: Not yet | Q2: Mostly by name | Q3: Not sure | Q4: Not really | Q5: Not CIWG eligible | Q6: Not discussed","Fallback Strategy (ordered)":"1. A different branch at a Top-50 NIRF college",Comments:"Only 3 choices, all top NITs CSE.",Status:"New",Paper:"B.E. / B.Tech (Paper 1)"},
{_row:5,Timestamp:"2026-06-13T11:22:00",Name:"Ishaan Varma",Email:"ishaan.varma@example.com",WhatsApp:"+96599887766","JEE Main CRL":95000,Category:"OCI",CIWG:"No",Country:"Kuwait","Confidence (1-10)":9,"Top Choices":"1. NIT Calicut — Mechanical | 2. VNIT Nagpur — Mechanical | 3. SVNIT Surat — Mechanical | 4. NIT Durgapur — Metallurgy & Materials | 5. MANIT Bhopal — Civil | 6. NIT Raipur — Mining","Self-Check Answers":"Q1: Yes, all 5 | Q2: Data-driven | Q3: Yes | Q4: Yes, clearly | Q5: Not CIWG eligible | Q6: Yes, aligned","Fallback Strategy (ordered)":"1. Core branch (Mech / Civil / Chemical) at a top institute | 2. Same branch at a lower-NIRF NIT / IIIT / GFTI",Comments:"Set on core mechanical. Flexible on college.",Status:"In Progress",Paper:"B.E. / B.Tech (Paper 1)"}
];

/* ════════ STATE ════════ */
let DATA=[];
let live=false;
const F={status:new Set(),risk:new Set(),cat:new Set()};
let dark=window.matchMedia&&window.matchMedia('(prefers-color-scheme: dark)').matches;
let openRows=new Set();

/* ════════ derive ════════ */
function num(x){const n=parseInt((x+"").replace(/[^\d]/g,''),10);return isNaN(n)?0:n;}
function parseChoices(str){
  return (str||"").split(" | ").map(c=>{
    const m=c.replace(/^\s*\d+\.\s*/,'').split(" — ");
    return {name:(m[0]||"").trim(),br:(m[1]||"").trim()};
  }).filter(c=>c.name);
}
function riskOf(r){
  const conf=num(r["Confidence (1-10)"]), rank=num(r["JEE Main CRL"]);
  const ch=parseChoices(r["Top Choices"]);
  let dream=0,safe=0;
  ch.forEach(c=>{const f=fitOf(c.name,c.br,rank);if(f==="dream")dream++;if(f==="safe")safe++;});
  const dreamPct=ch.length?dream/ch.length:0;
  let score=0;
  if(conf<=4)score+=2; else if(conf<=6)score+=1;
  if(ch.length<5)score+=1;
  if(dreamPct>=0.6)score+=2; else if(dreamPct>=0.35)score+=1;
  if(safe===0&&ch.length)score+=1;
  return score>=4?"High":score>=2?"Medium":"Low";
}

/* ════════ render ════════ */
function chipset(el,items,set){
  document.getElementById(el).innerHTML=items.map(i=>`<button class="fchip ${set.has(i)?'on':''}" onclick="toggleF('${el}','${i}')">${i}</button>`).join("");
}
function toggleF(el,v){const set=el==="fStatus"?F.status:el==="fRisk"?F.risk:F.cat;set.has(v)?set.delete(v):set.add(v);chipset(el,el==="fStatus"?["New","Contacted","In Progress","Closed"]:el==="fRisk"?["High","Medium","Low"]:CATS,set);render();}
let CATS=[];

function stats(){
  const t=DATA.length;
  const nw=DATA.filter(r=>(r.Status||"New")==="New").length;
  const hi=DATA.filter(r=>riskOf(r)==="High").length;
  const ciwg=DATA.filter(r=>(r.CIWG||"")==="Yes").length;
  const avg=t?(DATA.reduce((s,r)=>s+num(r["Confidence (1-10)"]),0)/t).toFixed(1):"–";
  document.getElementById("stats").innerHTML=
    `<div class="stat"><b>${t}</b><span>Total submissions</span></div>
     <div class="stat"><b>${nw}</b><span>New / untouched</span></div>
     <div class="stat risk"><b>${hi}</b><span>High-risk lists</span></div>
     <div class="stat"><b>${ciwg}</b><span>CIWG eligible</span></div>
     <div class="stat"><b>${avg}</b><span>Avg confidence</span></div>`;
}

function render(){
  CATS=[...new Set(DATA.map(r=>r.Category).filter(Boolean))];
  if(!document.querySelector("#fStatus .fchip")){chipset("fStatus",["New","Contacted","In Progress","Closed"],F.status);chipset("fRisk",["High","Medium","Low"],F.risk);}
  chipset("fCat",CATS,F.cat);
  stats();
  const q=document.getElementById("q").value.toLowerCase().trim();
  let rows=DATA.filter(r=>{
    const st=r.Status||"New", rk=riskOf(r);
    return (!F.status.size||F.status.has(st))&&(!F.risk.size||F.risk.has(rk))&&(!F.cat.size||F.cat.has(r.Category))&&
      (!q||((r.Name||"")+(r.Email||"")+(r.Country||"")).toLowerCase().includes(q));
  });
  const s=document.getElementById("sortSel").value;
  if(s==="confLow")rows.sort((a,b)=>num(a["Confidence (1-10)"])-num(b["Confidence (1-10)"]));
  else if(s==="confHigh")rows.sort((a,b)=>num(b["Confidence (1-10)"])-num(a["Confidence (1-10)"]));
  else if(s==="rankBest")rows.sort((a,b)=>num(a["JEE Main CRL"])-num(b["JEE Main CRL"]));
  else if(s==="risk"){const o={High:0,Medium:1,Low:2};rows.sort((a,b)=>o[riskOf(a)]-o[riskOf(b)]);}
  else rows.sort((a,b)=>new Date(b.Timestamp)-new Date(a.Timestamp));

  const L=document.getElementById("list");
  if(!rows.length){L.innerHTML='<div class="empty">No submissions match these filters.</div>';return;}
  L.innerHTML=rows.map(r=>{
    const conf=num(r["Confidence (1-10)"]), rk=riskOf(r), st=r.Status||"New", open=openRows.has(r._row);
    const confColor=conf<=4?"var(--warn)":conf<=6?"var(--amber)":"var(--good)";
    const ch=parseChoices(r["Top Choices"]), rank=num(r["JEE Main CRL"]);
    const plist=ch.map((c,i)=>{const f=fitOf(c.name,c.br,rank);return `<div class="prow"><div class="pn">${i+1}</div><div class="nm">${c.name} — <b>${c.br}</b></div><span class="fit ${f}">${f==="na"?"—":f}</span></div>`;}).join("");
    const qa=(r["Self-Check Answers"]||"").split(" | ").map(x=>`<div>${x}</div>`).join("");
    const fbl=(r["Fallback Strategy (ordered)"]||"").split(" | ").map(x=>`<div>${x}</div>`).join("");
    const waMsg=encodeURIComponent("Hi "+(r.Name||"")+", this is EduAakashaa regarding your DASA 2026 preference list. ");
    return `<div class="sub">
      <div class="shead" onclick="tog(${r._row})">
        <div class="who"><h3>${r.Name||"(no name)"}</h3><div class="sm">${r.Country||""} · ${(r.Timestamp?new Date(r.Timestamp).toLocaleString('en-GB',{day:'2-digit',month:'short',hour:'2-digit',minute:'2-digit'}):"")}</div></div>
        <span class="pill crl">CRL ${num(r["JEE Main CRL"]).toLocaleString()}</span>
        ${r.CIWG==="Yes"?'<span class="pill ciwg">CIWG</span>':''}
        <div class="conf"><b style="color:${confColor}">${conf||"–"}</b><span>conf</span></div>
        <span class="risk-b ${rk}">${rk} risk</span>
        <select class="statSel" data-s="${st}" onclick="event.stopPropagation()" onchange="setStatus(${r._row},this.value)">
          ${["New","Contacted","In Progress","Closed"].map(o=>`<option ${o===st?'selected':''}>${o}</option>`).join("")}
        </select>
      </div>
      <div class="detail ${open?'open':''}" id="d${r._row}">
        <div class="dgrid">
          <div><b>Email:</b> ${r.Email||"—"}</div><div><b>WhatsApp:</b> ${r.WhatsApp||"—"}</div>
          <div><b>Category:</b> ${r.Category||"—"}</div><div><b>Paper:</b> ${r.Paper||"—"}</div>
        </div>
        <div class="dh">Preference list · rank-fit (${ch.length})</div>
        <div class="plist">${plist||'<div class="prow">—</div>'}</div>
        <div class="dh">Self-check responses</div><div class="qa">${qa||"—"}</div>
        <div class="dh">Fallback strategy (ordered)</div><div class="fbl">${fbl||"—"}</div>
        ${r.Comments?`<div class="dh">Comments</div><div class="qa">${r.Comments}</div>`:""}
        <div class="cbtns">
          <a class="cbtn wa" target="_blank" href="https://wa.me/${(r.WhatsApp||'').replace(/[^\d]/g,'')}?text=${waMsg}">💬 WhatsApp</a>
          <a class="cbtn em" href="mailto:${r.Email}?subject=${encodeURIComponent('EduAakashaa — Your DASA 2026 choice list')}">✉ Email</a>
        </div>
      </div>
    </div>`;
  }).join("");
}
function tog(row){openRows.has(row)?openRows.delete(row):openRows.add(row);const d=document.getElementById("d"+row);if(d)d.classList.toggle("open");}

/* ════════ status write-back ════════ */
function setStatus(row,status){
  const r=DATA.find(x=>x._row===row);if(r)r.Status=status;
  const sel=document.querySelector(`#d${row}`)?.closest('.sub')?.querySelector('.statSel');if(sel)sel.dataset.s=status;
  stats();
  if(live){
    fetch(STATUS_URL,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({row,status})}).catch(()=>{});
  }
}

/* ════════ live load ════════ */
/* Same-origin now that the Sheet is read through our proxy, so this is a plain
   fetch — the old JSONP callback/timeout dance only existed to reach Apps
   Script cross-origin. */
function loadLive(){
  fetch(DATA_URL,{headers:{"Accept":"application/json"}})
    .then(r=>r.json().catch(()=>({})).then(res=>({ok:r.ok,status:r.status,res})))
    .then(({ok,status,res})=>{
      if(!ok){
        if(status===503){banner("⚠️ Live data isn't configured on the server (DASA_SCRIPT_URL / DASA_SCRIPT_KEY). Showing demo data.",true);}
        else if(res&&res.error==="unauthorized"){banner("⚠️ The Sheet rejected the server's access key — check DASA_SCRIPT_KEY matches ACCESS_KEY in the Apps Script. Showing demo data.",true);}
        else{banner("⚠️ Couldn't reach the Sheet — showing demo data.",true);}
        return;
      }
      if(res&&res.rows){DATA=res.rows;live=true;banner("✅ Live data from Google Sheet — "+DATA.length+" submissions.",false);openRows.clear();render();}
    })
    .catch(()=>{banner("⚠️ Couldn't reach the server — showing demo data.",true);});
}
function banner(msg,warn){const b=document.getElementById("banner");b.textContent=msg;b.classList.add("show");b.style.background=warn?"var(--amber-soft)":"var(--good-soft)";b.style.borderColor=warn?"var(--amber)":"var(--good)";}

/* ════════ CSV ════════ */
function exportCsv(){
  const cols=["Timestamp","Name","JEE Main CRL","Category","CIWG","Country","Email","WhatsApp","Confidence (1-10)","Status","Top Choices","Fallback Strategy (ordered)","Self-Check Answers","Comments"];
  const esc=v=>'"'+String(v==null?"":v).replace(/"/g,'""')+'"';
  const lines=[cols.join(",")].concat(DATA.map(r=>cols.map(c=>esc(c==="Status"?(r.Status||"New"):r[c])).join(",")));
  const blob=new Blob([lines.join("\n")],{type:"text/csv"});
  const a=document.createElement("a");a.href=URL.createObjectURL(blob);a.download="dasa2026-submissions.csv";a.click();
}

/* ════════ theme ════════ */
function applyTheme(){document.documentElement.dataset.theme=dark?"dark":"light";document.getElementById("themeBtn").textContent=dark?"☀️":"🌙";}
function toggleTheme(){dark=!dark;applyTheme();}

/* ════════ init ════════ */
applyTheme();
DATA=DEMO.slice();render();loadLive();
