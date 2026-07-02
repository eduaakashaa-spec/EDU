
// Data now lives in app/data/files/*.csv and is served by /api/data/*.js
const DATA = window.EA_DASA_SEAT_MATRIX || [];

// CONFIG
const CATS=['Computing & IT','Electronics & Comm','Mechanical','Civil & Infra',
  'Chemical & Process','Electrical & Power','Architecture & Planning','Materials & Metallurgy',
  'Bio & Life Sciences','Science & Mathematics','Aerospace','Mining','Maritime','Specialised Tech','Management'];
const CICONS={'Computing & IT':'💻','Electronics & Comm':'📡','Mechanical':'⚙️',
  'Civil & Infra':'🏗️','Chemical & Process':'🧪','Electrical & Power':'⚡',
  'Architecture & Planning':'📐','Materials & Metallurgy':'🪨','Bio & Life Sciences':'🧬',
  'Science & Mathematics':'🔬','Aerospace':'✈️','Mining':'⛏️','Maritime':'⚓','Specialised Tech':'🏭','Management':'📊'};
const CCOLS=['#F97316','#FB923C','#10B981','#1D4ED8','#EC4899','#3B82F6','#A78BFA',
  '#F59E0B','#84CC16','#8B5CF6','#06B6D4','#94A3B8','#14B8A6','#FDBA74','#60A5FA'];

// TOTALS
const tot=v=>DATA.reduce((a,r)=>a+r[v],0);
const totalDasa=tot('dasa_total'),totalCiwg=tot('ciwg'),totalNC=tot('nonciwg');
const nInst=new Set(DATA.map(r=>r.institute)).size;
const nStates=new Set(DATA.map(r=>r.state)).size;
const nProg=DATA.length;
const nRanked=new Set(DATA.filter(r=>r.nirf_rank&&r.nirf_rank<999).map(r=>r.institute)).size;

// KPIs
const kpis=[
  {l:'Institutes',v:nInst,c:'#F97316',s:'NITs · IIESTs · IIITs · GFTIs'},
  {l:'States / UTs',v:nStates,c:'#F0ABFC',s:'Geographic spread across India'},
  {l:'Programmes',v:nProg,c:'#94A3B8',s:'Unique degree programmes'},
  {l:'Total DASA Seats',v:totalDasa,c:'#FDBA74',s:'CIWG + Non-CIWG combined'},
  {l:'Non-CIWG Seats',v:totalNC,c:'#3B82F6',s:'~67% — NRI / OCI / Foreign'},
  {l:'CIWG Seats',v:totalCiwg,c:'#34D399',s:'~33% — Gulf NRI category'},
  {l:'NIRF Ranked',v:nRanked,c:'#F59E0B',s:'Have Engineering rank 2026'},
];
const kg=document.getElementById('kpiGrid');
kpis.forEach((k,i)=>{
  const d=document.createElement('div');d.className='kpi';d.style.animationDelay=(i*.055)+'s';
  d.innerHTML=`<div class="kpi-bar" style="background:${k.c}"></div>
    <div class="kpi-l">${k.l}</div>
    <div class="kpi-v" style="color:${k.c}" data-t="${k.v}">0</div>
    <div class="kpi-s">${k.s}</div>`;
  kg.appendChild(d);
});
function cntUp(){document.querySelectorAll('[data-t]').forEach(el=>{
  const t=+el.dataset.t,n=60;let i=0;
  const f=()=>{i++;el.textContent=Math.round(t*(i/n)).toLocaleString();if(i<n)requestAnimationFrame(f);else el.textContent=t.toLocaleString();};f();});}
setTimeout(cntUp,200);

// SHORT NAME
const shortN=n=>n.replace('National Institute of Technology','NIT').replace('Indian Institute of Engineering Science and Technology','IIEST').replace('Indian Institute of Information Technology','IIIT').replace('Delhi Technological University, Delhi','DTU').replace('Manipal Institute of Technology, Manipal','MIT Manipal').replace('Netaji Subhas University of Technology, Delhi','NSUT').replace('Maulana Azad ','').replace('Malaviya ','').replace('Motilal Nehru ','').replace('Sardar Vallabhbhai ','SV').replace('Visvesvaraya ','V').replace('Dr. B R Ambedkar ','').replace('Madan Mohan Malaviya University of Technology, Gorakhpur','MMMUT').replace('University of Hyderabad','Univ Hyderabad').replace('Sant Longowal Institute of Engineering and Technology','SLIET').replace('Pandit Deendayal Energy University, Gandhinagar','PDEU').replace(/, (Surathkal|Calicut|Warangal|Rourkela|Raipur|Patna|Durgapur|Silchar|Srinagar|Hamirpur|Kurukshetra|Jamshedpur|Meghalaya|Puducherry|Delhi|Surat|Nagpur|Allahabad|Gwalior)$/,'').replace(', Jalandhar','').replace(', Chandigarh','');

// NIRF STRIP
const instNirf={};
DATA.forEach(r=>{
  if(r.nirf_rank&&r.nirf_rank<999&&!instNirf[r.institute]){
    const s=DATA.filter(x=>x.institute===r.institute).reduce((a,x)=>a+x.dasa_total,0);
    instNirf[r.institute]={rank:r.nirf_rank,score:r.nirf_score,seats:s,city:r.city,state:r.state};
  }
});
const nirfArr=Object.entries(instNirf).sort((a,b)=>a[1].rank-b[1].rank);
const strip=document.getElementById('nirfScroller');
nirfArr.forEach(([name,info])=>{
  const c=info.rank<=10?'#F59E0B':info.rank<=50?'#10B981':'#3B82F6';
  const d=document.createElement('div');d.className='nirf-card';
  d.title=`${name}
NIRF: #${info.rank} | Score: ${info.score?.toFixed(2)||'N/A'}
City: ${info.city}, ${info.state}
DASA Seats: ${info.seats}`;
  d.innerHTML=`<div class="nc-rank" style="color:${c}">#${info.rank}</div>
    <div class="nc-score">${info.score?.toFixed(2)||'—'}</div>
    <div class="nc-name">${shortN(name)}</div>
    <div class="nc-loc">📍 ${info.city}</div>`;
  strip.appendChild(d);
});

// CHARTS
Chart.defaults.color='#64748B';Chart.defaults.font.family='Arial';Chart.defaults.font.size=11;

// Group bar
const grps=['NIT/IIEST','IIIT','Other-GFTI'],gL=['NITs & IIEST','IIITs','Other-GFTIs'];
const gnc=grps.map(g=>DATA.filter(r=>r.group===g).reduce((a,r)=>a+r.nonciwg,0));
const gcw=grps.map(g=>DATA.filter(r=>r.group===g).reduce((a,r)=>a+r.ciwg,0));
new Chart(document.getElementById('cGroup'),{type:'bar',data:{labels:gL,datasets:[
  {label:'Non-CIWG',data:gnc,backgroundColor:'rgba(59,130,246,.75)',borderColor:'#3B82F6',borderWidth:1,borderRadius:5},
  {label:'CIWG',data:gcw,backgroundColor:'rgba(249,115,22,.75)',borderColor:'#F97316',borderWidth:1,borderRadius:5},
]},options:{responsive:true,maintainAspectRatio:false,
  plugins:{legend:{position:'bottom',labels:{padding:10,boxWidth:10,color:'#94A3B8'}}},
  scales:{x:{stacked:true,grid:{color:'rgba(30,48,84,.8)'},ticks:{color:'#94A3B8'}},
    y:{stacked:true,grid:{color:'rgba(30,48,84,.8)'},ticks:{color:'#94A3B8'}}}}});

// Donut
new Chart(document.getElementById('cDonut'),{type:'doughnut',data:{
  labels:['Non-CIWG','CIWG'],
  datasets:[{data:[totalNC,totalCiwg],backgroundColor:['rgba(59,130,246,.8)','rgba(249,115,22,.8)'],
    borderColor:['#3B82F6','#F97316'],borderWidth:2,hoverOffset:6}]},
  options:{responsive:true,maintainAspectRatio:false,cutout:'68%',
    plugins:{legend:{position:'bottom',labels:{padding:12,boxWidth:10,color:'#94A3B8'}},
      tooltip:{callbacks:{label:c=>`${c.label}: ${c.parsed.toLocaleString()} (${(c.parsed/(totalNC+totalCiwg)*100).toFixed(1)}%)`}}}}});

// Category bar
const catNC=CATS.map(c=>DATA.filter(r=>r.branch_cat===c).reduce((a,r)=>a+r.nonciwg,0));
const catCW=CATS.map(c=>DATA.filter(r=>r.branch_cat===c).reduce((a,r)=>a+r.ciwg,0));
new Chart(document.getElementById('cCat'),{type:'bar',data:{
  labels:CATS.map(c=>`${CICONS[c]||''} ${c}`),
  datasets:[
    {label:'Non-CIWG',data:catNC,backgroundColor:CCOLS.map(c=>c+'99'),borderColor:CCOLS,borderWidth:1,borderRadius:3},
    {label:'CIWG',data:catCW,backgroundColor:CCOLS.map(c=>c+'44'),borderColor:CCOLS,borderWidth:1,borderRadius:3},
  ]},
  options:{indexAxis:'y',responsive:true,maintainAspectRatio:false,
    plugins:{legend:{position:'bottom',labels:{padding:8,boxWidth:8,color:'#94A3B8'}}},
    scales:{x:{stacked:true,grid:{color:'rgba(30,48,84,.8)'},ticks:{color:'#94A3B8'}},
      y:{stacked:true,grid:{color:'rgba(30,48,84,.8)'},ticks:{color:'#94A3B8',font:{size:10}}}}}});

// Top 15 institutes
const instT={};DATA.forEach(r=>{if(!instT[r.institute])instT[r.institute]={nc:0,cw:0};instT[r.institute].nc+=r.nonciwg;instT[r.institute].cw+=r.ciwg;});
const t15=Object.entries(instT).sort((a,b)=>(b[1].nc+b[1].cw)-(a[1].nc+a[1].cw)).slice(0,15);
new Chart(document.getElementById('cTop15'),{type:'bar',data:{
  labels:t15.map(([n])=>shortN(n)),
  datasets:[
    {label:'Non-CIWG',data:t15.map(([,v])=>v.nc),backgroundColor:'rgba(59,130,246,.75)',borderColor:'#3B82F6',borderWidth:1,borderRadius:3},
    {label:'CIWG',data:t15.map(([,v])=>v.cw),backgroundColor:'rgba(249,115,22,.75)',borderColor:'#F97316',borderWidth:1,borderRadius:3},
  ]},
  options:{indexAxis:'y',responsive:true,maintainAspectRatio:false,
    plugins:{legend:{position:'bottom',labels:{padding:8,boxWidth:8,color:'#94A3B8'}}},
    scales:{x:{stacked:true,grid:{color:'rgba(30,48,84,.8)'},ticks:{color:'#94A3B8'}},
      y:{stacked:true,grid:{color:'rgba(30,48,84,.8)'},ticks:{color:'#94A3B8',font:{size:10}}}}}});

// NIRF distribution
const r10=new Set(DATA.filter(r=>r.nirf_rank&&r.nirf_rank<=10).map(r=>r.institute)).size;
const r50=new Set(DATA.filter(r=>r.nirf_rank&&r.nirf_rank>10&&r.nirf_rank<=50).map(r=>r.institute)).size;
const r100=new Set(DATA.filter(r=>r.nirf_rank&&r.nirf_rank>50&&r.nirf_rank<=100).map(r=>r.institute)).size;
const rnr=new Set(DATA.filter(r=>r.nirf_rank===999).map(r=>r.institute)).size;
const rnone=new Set(DATA.filter(r=>!r.nirf_rank).map(r=>r.institute)).size;
new Chart(document.getElementById('cNIRF'),{type:'doughnut',data:{
  labels:['Rank 1–10','Rank 11–50','Rank 51–100','In NIRF (NR)','Not in NIRF'],
  datasets:[{data:[r10,r50,r100,rnr,rnone],
    backgroundColor:['#F59E0B','#10B981','#3B82F6','#94A3B8','#1E3054'],
    borderColor:'#0F1E36',borderWidth:2,hoverOffset:5}]},
  options:{responsive:true,maintainAspectRatio:false,cutout:'60%',
    plugins:{legend:{position:'bottom',labels:{padding:6,boxWidth:8,color:'#94A3B8',font:{size:9}}},
      tooltip:{callbacks:{label:c=>`${c.label}: ${c.parsed} institutes`}}}}});

// State totals
const stateT={};
DATA.forEach(r=>{
  if(!stateT[r.state])stateT[r.state]={nc:0,cw:0,insts:new Set()};
  stateT[r.state].nc+=r.nonciwg;stateT[r.state].cw+=r.ciwg;stateT[r.state].insts.add(r.institute);
});
const stateArr=Object.entries(stateT).map(([s,v])=>({state:s,nc:v.nc,cw:v.cw,total:v.nc+v.cw,insts:v.insts.size}));

// Top states by DASA seats - horizontal bar
const top12s=stateArr.sort((a,b)=>b.total-a.total).slice(0,12);
new Chart(document.getElementById('cState'),{type:'bar',data:{
  labels:top12s.map(s=>s.state),
  datasets:[{label:'DASA Seats',data:top12s.map(s=>s.total),
    backgroundColor:top12s.map((_,i)=>i<3?'rgba(249,115,22,.8)':i<6?'rgba(59,130,246,.75)':'rgba(52,211,153,.6)'),
    borderColor:top12s.map((_,i)=>i<3?'#F97316':i<6?'#3B82F6':'#34D399'),
    borderWidth:1,borderRadius:4}]},
  options:{indexAxis:'y',responsive:true,maintainAspectRatio:false,
    plugins:{legend:{display:false},tooltip:{callbacks:{label:c=>`${c.parsed.x} seats | ${top12s[c.dataIndex].insts} institutes`}}},
    scales:{x:{grid:{color:'rgba(30,48,84,.8)'},ticks:{color:'#94A3B8'}},
      y:{grid:{color:'rgba(30,48,84,.8)'},ticks:{color:'#94A3B8',font:{size:10}}}}}});

// State stacked CIWG vs NC (top 15)
const top15s=stateArr.sort((a,b)=>b.total-a.total).slice(0,15);
new Chart(document.getElementById('cStateBar'),{type:'bar',data:{
  labels:top15s.map(s=>s.state),
  datasets:[
    {label:'Non-CIWG',data:top15s.map(s=>s.nc),backgroundColor:'rgba(59,130,246,.75)',borderColor:'#3B82F6',borderWidth:1,borderRadius:3},
    {label:'CIWG',data:top15s.map(s=>s.cw),backgroundColor:'rgba(249,115,22,.75)',borderColor:'#F97316',borderWidth:1,borderRadius:3},
  ]},
  options:{responsive:true,maintainAspectRatio:false,
    plugins:{legend:{position:'bottom',labels:{padding:8,boxWidth:8,color:'#94A3B8'}}},
    scales:{x:{stacked:true,grid:{color:'rgba(30,48,84,.8)'},ticks:{color:'#94A3B8',font:{size:9},maxRotation:35}},
      y:{stacked:true,grid:{color:'rgba(30,48,84,.8)'},ticks:{color:'#94A3B8'}}}}});

// Institutes per state bubble / bar
const topInst=stateArr.sort((a,b)=>b.insts-a.insts).slice(0,15);
new Chart(document.getElementById('cStateInst'),{type:'bar',data:{
  labels:topInst.map(s=>s.state),
  datasets:[
    {label:'Institutes',data:topInst.map(s=>s.insts),backgroundColor:'rgba(240,171,252,.7)',borderColor:'#F0ABFC',borderWidth:1,borderRadius:4,yAxisID:'y'},
    {label:'Seats',data:topInst.map(s=>s.total),backgroundColor:'rgba(249,115,22,.35)',borderColor:'#F97316',borderWidth:1,borderRadius:4,yAxisID:'y2'},
  ]},
  options:{responsive:true,maintainAspectRatio:false,
    plugins:{legend:{position:'bottom',labels:{padding:8,boxWidth:8,color:'#94A3B8'}}},
    scales:{
      x:{grid:{color:'rgba(30,48,84,.8)'},ticks:{color:'#94A3B8',font:{size:9},maxRotation:35}},
      y:{position:'left',title:{display:true,text:'Institutes',color:'#94A3B8',font:{size:9}},grid:{color:'rgba(30,48,84,.4)'},ticks:{color:'#F0ABFC'}},
      y2:{position:'right',title:{display:true,text:'Seats',color:'#94A3B8',font:{size:9}},grid:{display:false},ticks:{color:'#F97316'}}
    }}});

// Scatter NIRF
const scD=nirfArr.filter(([,v])=>v.score).map(([name,info])=>({x:info.score,y:info.seats,_l:shortN(name),_s:info.state}));
new Chart(document.getElementById('cScatter'),{type:'scatter',data:{datasets:[{
  label:'Institute',data:scD.map(d=>({x:d.x,y:d.y,_l:d._l,_s:d._s})),
  backgroundColor:'rgba(249,115,22,.65)',borderColor:'#F97316',borderWidth:1,pointRadius:5,pointHoverRadius:7}]},
  options:{responsive:true,maintainAspectRatio:false,
    plugins:{legend:{display:false},tooltip:{callbacks:{label:c=>`${c.raw._l} (${c.raw._s}): ${c.raw.x.toFixed(2)} | ${c.raw.y} seats`}}},
    scales:{x:{title:{display:true,text:'NIRF Score',color:'#64748B',font:{size:9}},grid:{color:'rgba(30,48,84,.8)'},ticks:{color:'#94A3B8'}},
      y:{title:{display:true,text:'DASA Seats',color:'#64748B',font:{size:9}},grid:{color:'rgba(30,48,84,.8)'},ticks:{color:'#94A3B8'}}}}});

// CAT FILTER CHIPS
const cr=document.getElementById('catRow');
const allC=document.createElement('button');allC.className='chip act';allC.dataset.cat='all';allC.textContent='All';cr.appendChild(allC);
CATS.forEach((c,i)=>{
  const b=document.createElement('button');b.className='chip';b.dataset.cat=c;
  b.textContent=`${CICONS[c]||''} ${c}`;
  b.addEventListener('click',()=>{
    document.querySelectorAll('[data-cat]').forEach(x=>{x.classList.remove('act');x.style.cssText='';});
    b.classList.add('act');b.style.color=CCOLS[i];b.style.background=CCOLS[i]+'18';b.style.borderColor=CCOLS[i];
    catF=c;buildTable();
  });
  cr.appendChild(b);
});
allC.addEventListener('click',()=>{
  document.querySelectorAll('[data-cat]').forEach(x=>{x.classList.remove('act');x.style.cssText='';});
  allC.classList.add('act');catF='all';buildTable();
});

// STATE DROPDOWN
const sd=document.getElementById('stateFilter');
const allStates=[...new Set(DATA.map(r=>r.state))].sort();
allStates.forEach(s=>{const o=document.createElement('option');o.value=s;o.textContent=s;sd.appendChild(o);});
sd.addEventListener('change',()=>{stF=sd.value;buildTable();});

// TABLE STATE
let gF='all',catF='all',nfF='all',stF='all',srchQ='',sK='institute',sD=1;

function nirfPill(r){
  if(!r) return '<span class="nirf-pill np-none">—</span>';
  if(r===999) return '<span class="nirf-pill np-nr">NR</span>';
  const c=r<=10?'np-gold':r<=50?'np-green':'np-blue';
  return `<span class="nirf-pill ${c}">#${r}</span>`;
}
function scoreCell(sc){
  if(!sc) return '<span style="color:var(--muted);font-size:10px">—</span>';
  const p=Math.round((sc/100)*100),col=sc>=65?'#F59E0B':sc>=55?'#10B981':'#3B82F6';
  return `<div class="score-row"><span style="font-family:var(--m);font-size:11px;color:${col}">${sc.toFixed(2)}</span><div class="sbar"><div class="sbar-fill" style="width:${p}%;background:${col}"></div></div></div>`;
}
function catBdg(cat){
  const i=CATS.indexOf(cat),c=CCOLS[i]||'#64748B';
  return `<span class="catbadge" style="color:${c};background:${c}18">${CICONS[cat]||''} ${cat}</span>`;
}
function gbdg(g){
  const m={'NIT/IIEST':'gb-nit','IIIT':'gb-iiit','Other-GFTI':'gb-gfti'};
  const l={'NIT/IIEST':'NIT','IIIT':'IIIT','Other-GFTI':'GFTI'};
  return `<span class="gbadge ${m[g]||''}">${l[g]||g}</span>`;
}

function buildTable(){
  let d=[...DATA];
  if(gF!=='all') d=d.filter(r=>r.group===gF);
  if(catF!=='all') d=d.filter(r=>r.branch_cat===catF);
  if(stF!=='all') d=d.filter(r=>r.state===stF);
  if(nfF==='ranked') d=d.filter(r=>r.nirf_rank&&r.nirf_rank<999);
  else if(nfF==='50') d=d.filter(r=>r.nirf_rank&&r.nirf_rank<=50);
  else if(nfF==='100') d=d.filter(r=>r.nirf_rank&&r.nirf_rank<=100);
  if(srchQ){
    const q=srchQ.toLowerCase();
    d=d.filter(r=>r.institute.toLowerCase().includes(q)||r.program.toLowerCase().includes(q)||
      r.branch_cat.toLowerCase().includes(q)||r.city.toLowerCase().includes(q)||r.state.toLowerCase().includes(q));
  }
  d.sort((a,b)=>{
    let va=a[sK],vb=b[sK];
    if(va===null||va===undefined) va=sD>0?1e9:-1e9;
    if(vb===null||vb===undefined) vb=sD>0?1e9:-1e9;
    return typeof va==='number'?(va-vb)*sD:String(va).localeCompare(String(vb))*sD;
  });
  const mx=Math.max(...d.map(r=>r.dasa_total),1);
  const tb=document.getElementById('tBody');tb.innerHTML='';
  let lastI='';
  d.forEach(r=>{
    const isNew=r.institute!==lastI;lastI=r.institute;
    const bw=Math.round((r.dasa_total/mx)*55);
    const nw=r.dasa_total>0?Math.round((r.nonciwg/r.dasa_total)*bw):0;
    const cw=bw-nw;
    const tr=document.createElement('tr');
    tr.innerHTML=`<td>${gbdg(r.group)}</td>
      <td class="td-i" title="${r.institute}">${isNew?r.institute:''}</td>
      <td><div class="loc-cell"><span class="loc-city">📍 ${r.city}</span></div></td>
      <td><span class="state-badge">${r.state}</span></td>
      <td class="td-p" title="${r.program}">${r.program}</td>
      <td>${catBdg(r.branch_cat)}</td>
      <td class="td-n">${nirfPill(r.nirf_rank)}</td>
      <td class="td-n">${scoreCell(r.nirf_score)}</td>
      <td class="td-n td-dasa">${r.dasa_total}</td>
      <td class="td-n td-nc">${r.nonciwg}</td>
      <td class="td-n td-cw">${r.ciwg}</td>
      <td class="td-n"><div class="split-bar" style="width:${bw}px;margin-left:auto"><div class="sb-nc" style="width:${nw}px"></div><div class="sb-cw" style="width:${cw}px"></div></div></td>`;
    tb.appendChild(tr);
  });
  document.getElementById('tblCt').textContent=`${d.length} of ${DATA.length} programmes`;
  document.getElementById('navStat').textContent=`${d.length} programmes`;
}

// Events
document.querySelectorAll('[data-g]').forEach(b=>b.addEventListener('click',()=>{
  document.querySelectorAll('[data-g]').forEach(x=>x.classList.remove('act'));b.classList.add('act');gF=b.dataset.g;buildTable();}));
document.querySelectorAll('[data-nf]').forEach(b=>b.addEventListener('click',()=>{
  document.querySelectorAll('[data-nf]').forEach(x=>x.classList.remove('act'));b.classList.add('act');nfF=b.dataset.nf;buildTable();}));
document.getElementById('search').addEventListener('input',e=>{srchQ=e.target.value.trim();buildTable();});
document.querySelectorAll('thead th[data-k]').forEach(th=>{
  th.addEventListener('click',()=>{
    const k=th.dataset.k;if(sK===k)sD*=-1;else{sK=k;sD=1;}
    document.querySelectorAll('thead th').forEach(h=>{h.classList.remove('sa','sd');});
    th.classList.add(sD===1?'sa':'sd');buildTable();
  });
});

buildTable();

;

	const heightObserver = new ResizeObserver(([{ contentRect }]) => {
		window.parent.postMessage({ action: 'iframeHeightUpdated', height: contentRect.height, id: 'z88JPN' }, '*');
	});

	heightObserver.observe(document.documentElement);
