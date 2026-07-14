
const RAW = window.EA_TNEA2026 || [];


// Parse data
const DATA = RAW.map(r => ({
cc:r[0],cn:r[1],bc:r[2],bn:r[3],
oc:r[4],bcc:r[5],bcm:r[6],mbc:r[7],mbcdnc:r[8],mbcv:r[9],sc:r[10],sca:r[11],st:r[12],
er:r[13],bg:r[14]
}));

// Classify college type
function getCollegeType(name){
const n=(name||'').toLowerCase();
if(n.includes('university')||n.includes('government')||n.includes('govt')) return 'govt';
if(n.includes('autonomous')||n.includes('(autonomous)')) return 'auto';
return 'sf';
}
function getCollegeTypeLabel(t){return{govt:'Government',auto:'Autonomous',sf:'Self-Finance / Private'}[t]||'Unknown'}
function getCollegeTypeBadge(t){const cls={govt:'cat-govt',auto:'cat-auto',sf:'cat-sf'}[t]||'cat-na';return `<span class="category-badge ${cls}">${getCollegeTypeLabel(t)}</span>`}

// Tier
function getTier(er){if(!er||er<=0)return 4;if(er<=50)return 1;if(er<=150)return 2;if(er<=300)return 3;return 4}
function getTierLabel(t){return['','Tier 1 - Top','Tier 2 - Good','Tier 3 - Average','Tier 4 - Others'][t]}
function getTierBadge(t){return `<span class="tier-badge tier-${Math.min(t,3)}">${getTierLabel(t)}</span>`}

// Cutoff calc
function calcCutoff(m,p,c){
m=Math.max(0,Math.min(100,parseFloat(m)||0));
p=Math.max(0,Math.min(100,parseFloat(p)||0));
c=Math.max(0,Math.min(100,parseFloat(c)||0));
return Math.round((m+(p/2)+(c/2))*100)/100;
}

// Category key map
const CAT_MAP={oc:'oc',bcc:'bcc',bcm:'bcm',mbc:'mbc',mbcdnc:'mbcdnc',mbcv:'mbcv',sc:'sc',sca:'sca',st:'st'};
const CAT_LABELS={oc:'OC',bcc:'BC',bcm:'BCM',mbc:'MBC',mbcdnc:'MBC(DNC)',mbcv:'MBC(V)',sc:'SC',sca:'SCA',st:'ST'};
const CAT_KEYS=['oc','bcc','bcm','mbc','mbcdnc','mbcv','sc','sca','st'];

// ===== NAVIGATION =====
function showPage(id){
document.querySelectorAll('.page').forEach(p=>p.classList.remove('active'));
document.getElementById('page-'+id).classList.add('active');
document.querySelectorAll('#mainNav button').forEach(b=>b.classList.remove('active'));
const btns=document.querySelectorAll('#mainNav button');
const map={home:0,predictor:1,insights:2};
if(btns[map[id]])btns[map[id]].classList.add('active');
window.scrollTo({top:0,behavior:'smooth'});
if(id==='insights')renderInsights();
}

function showInsightTab(id){
document.querySelectorAll('#insightTabs button').forEach(b=>b.classList.remove('active'));
document.querySelectorAll('.tab-content').forEach(t=>t.classList.remove('active'));
document.getElementById('tab-'+id).classList.add('active');
const btns=document.querySelectorAll('#insightTabs button');
const map={guide:0,matrix:1,wef:2,aptitude:3,tips:4};
if(btns[map[id]])btns[map[id]].classList.add('active');
}

// ===== COUNTDOWN =====
function updateCountdown(){
const target=new Date('2026-09-30T00:00:00+05:30').getTime();
const now=Date.now();
const diff=target-now;
if(diff<=0){document.getElementById('cd-d').textContent='0';document.getElementById('cd-h').textContent='0';document.getElementById('cd-m').textContent='0';document.getElementById('cd-s').textContent='0';return}
const d=Math.floor(diff/86400000);
const h=Math.floor((diff%86400000)/3600000);
const m=Math.floor((diff%3600000)/60000);
const s=Math.floor((diff%60000)/1000);
document.getElementById('cd-d').textContent=d;
document.getElementById('cd-h').textContent=h;
document.getElementById('cd-m').textContent=m;
document.getElementById('cd-s').textContent=s;
}
setInterval(updateCountdown,1000);
updateCountdown();

// ===== GO TO PREDICTOR =====
function goToPredictor(){
var m=document.getElementById('hm-math').value||'';
var p=document.getElementById('hm-phy').value||'';
var c=document.getElementById('hm-chem').value||'';
var cat=document.getElementById('hm-cat').value||'oc';
showPage('predictor');
setTimeout(function(){
document.getElementById('p-math').value=m;
document.getElementById('p-phy').value=p;
document.getElementById('p-chem').value=c;
document.getElementById('p-cat').value=cat;
if(m||p||c){runPredictor();}
},300);
}

// ===== HOME CALC =====
function calcHomeScore(){
const m=document.getElementById('hm-math').value;
const p=document.getElementById('hm-phy').value;
const c=document.getElementById('hm-chem').value;
const score=calcCutoff(m,p,c);
document.getElementById('hm-score').textContent=score.toFixed(2);
}

// ===== PREDICTOR =====
let currentPage=1;
const PER_PAGE=15;
let filteredColleges=[];

function initFilters(){
const bgs=new Set(),brs=new Set();
DATA.forEach(d=>{bgs.add(d.bg);brs.add(d.bn)});
const bgSel=document.getElementById('f-bg');
[...bgs].sort().forEach(bg=>{const o=document.createElement('option');o.value=bg;o.textContent=bg;bgSel.appendChild(o)});
const brSel=document.getElementById('f-branch');
[...brs].sort().forEach(br=>{const o=document.createElement('option');o.value=br;o.textContent=br;brSel.appendChild(o)});
}

function runPredictor(){
const m=document.getElementById('p-math').value;
const p=document.getElementById('p-phy').value;
const c=document.getElementById('p-chem').value;
const score=calcCutoff(m,p,c);
document.getElementById('p-score').textContent=score.toFixed(2);

const cat=document.getElementById('p-cat').value;
const bg=document.getElementById('f-bg').value;
const branch=document.getElementById('f-branch').value;
const tier=document.getElementById('f-tier').value;
const ctype=document.getElementById('f-ctype').value;
const pred=document.getElementById('f-pred').value;
const search=document.getElementById('f-search').value.toLowerCase();

if(!m&&!p&&!c){
document.getElementById('collegeList').innerHTML='<div class="loading">Enter your marks above to see college predictions</div>';
document.getElementById('resultsInfo').textContent='Enter your marks to see predictions';
document.getElementById('pagination').innerHTML='';
return;
}

// Group by college
const collegeMap={};
DATA.forEach(d=>{
if(!collegeMap[d.cc])collegeMap[d.cc]={code:d.cc,name:d.cn,er:d.er,type:getCollegeType(d.cn),branches:[]};
const cutoff=d[cat]||0;
let prediction='reach';
if(score>=cutoff&&cutoff>0)prediction='safe';
else if(score>=cutoff-10&&cutoff>0)prediction='close';
collegeMap[d.cc].branches.push({...d,cutoff,prediction});
});

// Filter colleges
let colleges=Object.values(collegeMap);
colleges.forEach(col=>{
const bestPred=col.branches.reduce((best,b)=>{
const order={safe:0,close:1,reach:2};
return order[b.prediction]<order[best]?b.prediction:best;
},'reach');
col.bestPrediction=bestPred;
col.safeBranches=col.branches.filter(b=>b.prediction==='safe').length;
col.tier=getTier(col.er);
});

if(bg)colleges.forEach(c=>c.branches=c.branches.filter(b=>b.bg===bg));
if(branch)colleges.forEach(c=>c.branches=c.branches.filter(b=>b.bn===branch));
colleges=colleges.filter(c=>c.branches.length>0);

if(tier)colleges=colleges.filter(c=>c.tier===parseInt(tier));
if(ctype)colleges=colleges.filter(c=>c.type===ctype);
if(search)colleges=colleges.filter(c=>c.name.toLowerCase().includes(search));

// Recalculate best prediction after filters
colleges.forEach(col=>{
const bestPred=col.branches.reduce((best,b)=>{
const order={safe:0,close:1,reach:2};
return order[b.prediction]<order[best]?b.prediction:best;
},'reach');
col.bestPrediction=bestPred;
col.safeBranches=col.branches.filter(b=>b.prediction==='safe').length;
});

if(pred)colleges=colleges.filter(c=>pred==='safe'?c.branches.some(b=>b.prediction==='safe'):pred==='close'?c.branches.some(b=>b.prediction==='close'):c.branches.some(b=>b.prediction==='reach'));

// Sort: safe first, then by EA rank
colleges.sort((a,b)=>{
const order={safe:0,close:1,reach:2};
const diff=order[a.bestPrediction]-order[b.bestPrediction];
if(diff!==0)return diff;
return(a.er||999)-(b.er||999);
});

filteredColleges=colleges;
const safeCount=colleges.filter(c=>c.bestPrediction==='safe').length;
const closeCount=colleges.filter(c=>c.bestPrediction==='close').length;
const reachCount=colleges.filter(c=>c.bestPrediction==='reach').length;
document.getElementById('cnt-safe').textContent=safeCount;
document.getElementById('cnt-close').textContent=closeCount;
document.getElementById('cnt-reach').textContent=reachCount;
document.getElementById('cnt-total').textContent=colleges.length;

currentPage=1;
renderColleges();
}

function renderColleges(){
const start=(currentPage-1)*PER_PAGE;
const end=start+PER_PAGE;
const page=filteredColleges.slice(start,end);
const cat=document.getElementById('p-cat').value;
const score=parseFloat(document.getElementById('p-score').textContent)||0;

document.getElementById('resultsInfo').textContent=`Showing ${start+1}-${Math.min(end,filteredColleges.length)} of ${filteredColleges.length} colleges`;

let html='';
page.forEach((col,idx)=>{
const predClass={safe:'pill-safe',close:'pill-close',reach:'pill-reach'}[col.bestPrediction];
const predIcon={safe:'\u2713 Safe',close:'~ Close',reach:'\u2191 Reach'}[col.bestPrediction];

html+=`<div class="college-card" id="cc-${start+idx}">
<div class="college-header" onclick="toggleCollege(${start+idx})">
<div class="ch-left">
<div class="ch-name">${col.name}</div>
<div class="ch-meta">
<span>Code: ${col.code}</span>
${getCollegeTypeBadge(col.type)}
${getTierBadge(col.tier)}
<span class="branch-group-tag">${col.safeBranches} safe branches</span>
</div>
</div>
<div class="ch-right">
<span class="rank-badge">EA #${col.er||'N/A'}</span>
<span class="prediction-pill ${predClass}">${predIcon}</span>
<span class="expand-icon">&#9660;</span>
</div>
</div>
<div class="branch-table">
<div class="bt-inner">
<table>
<thead><tr><th>Branch</th><th>Code</th><th>Group</th><th>OC</th><th>BC</th><th>BCM</th><th>MBC</th><th>MBC(DNC)</th><th>MBC(V)</th><th>SC</th><th>SCA</th><th>ST</th><th>Status</th></tr></thead>
<tbody>`;
col.branches.forEach(b=>{
const pCls={safe:'pill-safe',close:'pill-close',reach:'pill-reach'}[b.prediction];
const pTxt={safe:'\u2713 Safe',close:'~ Close',reach:'\u2191 Reach'}[b.prediction];
function cutCls(v){if(!v||v<=0)return'cutoff-na';if(score>=v)return'cutoff-safe';if(score>=v-10)return'cutoff-close';return'cutoff-reach'}
html+=`<tr>
<td style="font-weight:600;max-width:200px;white-space:normal">${b.bn}</td>
<td>${b.bc}</td>
<td><span class="branch-group-tag">${b.bg}</span></td>
<td class="cutoff-cell ${cutCls(b.oc)}">${b.oc||'-'}</td>
<td class="cutoff-cell ${cutCls(b.bcc)}">${b.bcc||'-'}</td>
<td class="cutoff-cell ${cutCls(b.bcm)}">${b.bcm||'-'}</td>
<td class="cutoff-cell ${cutCls(b.mbc)}">${b.mbc||'-'}</td>
<td class="cutoff-cell ${cutCls(b.mbcdnc)}">${b.mbcdnc||'-'}</td>
<td class="cutoff-cell ${cutCls(b.mbcv)}">${b.mbcv||'-'}</td>
<td class="cutoff-cell ${cutCls(b.sc)}">${b.sc||'-'}</td>
<td class="cutoff-cell ${cutCls(b.sca)}">${b.sca||'-'}</td>
<td class="cutoff-cell ${cutCls(b.st)}">${b.st||'-'}</td>
<td><span class="prediction-pill ${pCls}">${pTxt}</span></td>
</tr>`;
});
html+=`</tbody></table></div></div></div>`;
});

document.getElementById('collegeList').innerHTML=html||'<div class="loading">No colleges found matching your criteria. Try adjusting filters.</div>';
renderPagination();
}

function toggleCollege(idx){
const card=document.getElementById('cc-'+idx);
card.classList.toggle('open');
}

function renderPagination(){
const total=Math.ceil(filteredColleges.length/PER_PAGE);
if(total<=1){document.getElementById('pagination').innerHTML='';return}
let html=`<button ${currentPage<=1?'disabled':''} onclick="goPage(${currentPage-1})">&laquo; Prev</button>`;
const maxShow=7;
let start=Math.max(1,currentPage-3);
let end=Math.min(total,start+maxShow-1);
if(end-start<maxShow-1)start=Math.max(1,end-maxShow+1);
if(start>1)html+=`<button onclick="goPage(1)">1</button>`;
if(start>2)html+=`<span style="padding:4px">...</span>`;
for(let i=start;i<=end;i++){
html+=`<button class="${i===currentPage?'active':''}" onclick="goPage(${i})">${i}</button>`;
}
if(end<total-1)html+=`<span style="padding:4px">...</span>`;
if(end<total)html+=`<button onclick="goPage(${total})">${total}</button>`;
html+=`<button ${currentPage>=total?'disabled':''} onclick="goPage(${currentPage+1})">Next &raquo;</button>`;
document.getElementById('pagination').innerHTML=html;
}

function goPage(p){currentPage=p;renderColleges();document.querySelector('.results-info').scrollIntoView({behavior:'smooth'})}

// ===== INSIGHTS RENDERING =====
let insightsRendered=false;
function renderInsights(){
if(insightsRendered)return;
insightsRendered=true;
renderBranchDemandChart();
renderCommunityInsights();
renderTierChart();
}

function renderBranchDemandChart(){
const groups={};
DATA.forEach(d=>{
if(!groups[d.bg])groups[d.bg]={count:0,avgCutoff:0,total:0};
groups[d.bg].count++;
if(d.oc>0){groups[d.bg].total+=d.oc;groups[d.bg].avgCutoff++}
});
const items=Object.entries(groups).map(([k,v])=>({name:k,count:v.count,avg:v.avgCutoff?Math.round(v.total/v.avgCutoff):0})).sort((a,b)=>b.count-a.count);
const maxCount=Math.max(...items.map(i=>i.count));
const colors=['#e87722','#1a3058','#28a745','#007bff','#dc3545','#ffc107','#6f42c1','#20c997'];
let barsHtml='<div class="bar-chart">';
items.forEach((item,i)=>{
const h=Math.round((item.count/maxCount)*140)+10;
barsHtml+=`<div class="bar" style="height:${h}px;background:${colors[i%colors.length]}" title="${item.name}: ${item.count} branches, Avg OC Cutoff: ${item.avg}">
<div class="bar-val">${item.count}</div>
<div class="bar-label">${item.name.replace(' Branches','').substring(0,15)}</div>
</div>`;
});
barsHtml+='</div><div style="text-align:center;margin-top:28px;font-size:11px;color:var(--gray500)">Number of branch-college combinations per group</div>';
document.getElementById('branchDemandChart').innerHTML=barsHtml;
}

function renderCommunityInsights(){
const popBranches=['COMPUTER SCIENCE AND ENGINEERING','INFORMATION TECHNOLOGY','ELECTRONICS AND COMMUNICATION ENGINEERING','ELECTRICAL AND ELECTRONICS ENGINEERING','MECHANICAL ENGINEERING','CIVIL  ENGINEERING','Artificial Intelligence and Data Science'];
let html='<div style="overflow-x:auto"><table style="width:100%;border-collapse:collapse;font-size:12px;min-width:700px"><thead><tr style="background:var(--navy);color:white"><th style="padding:8px;text-align:left">Branch</th>';
CAT_KEYS.forEach(k=>html+=`<th style="padding:8px;text-align:center">${CAT_LABELS[k]}</th>`);
html+='</tr></thead><tbody>';
popBranches.forEach(br=>{
const records=DATA.filter(d=>d.bn===br&&d.oc>0);
if(!records.length)return;
html+=`<tr><td style="padding:8px;font-weight:600;border-bottom:1px solid var(--gray200);max-width:180px">${br}</td>`;
CAT_KEYS.forEach(k=>{
const vals=records.map(r=>r[k]).filter(v=>v>0);
const avg=vals.length?Math.round(vals.reduce((a,b)=>a+b,0)/vals.length):0;
const cls=avg>=170?'cutoff-safe':avg>=140?'cutoff-close':'cutoff-reach';
html+=`<td style="padding:8px;text-align:center;border-bottom:1px solid var(--gray200)" class="cutoff-cell ${cls}">${avg||'-'}</td>`;
});
html+='</tr>';
});
html+='</tbody></table></div><p style="font-size:11px;color:var(--gray500);margin-top:8px;text-align:center">Average cutoff across all colleges offering each branch (higher = more competitive)</p>';
document.getElementById('communityInsights').innerHTML=html;
}

function renderTierChart(){
const tiers=[{label:'Tier 1 (Rank 1-50)',min:1,max:50,color:'#28a745'},{label:'Tier 2 (51-150)',min:51,max:150,color:'#007bff'},{label:'Tier 3 (151-300)',min:151,max:300,color:'#ffc107'},{label:'Tier 4 (300+)',min:301,max:999,color:'#dc3545'}];
let html='<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:12px">';
tiers.forEach(t=>{
const records=DATA.filter(d=>d.er>=t.min&&d.er<=t.max&&d.oc>0);
const vals=records.map(r=>r.oc);
const avg=vals.length?Math.round(vals.reduce((a,b)=>a+b,0)/vals.length):0;
const min=vals.length?Math.round(Math.min(...vals)):0;
const max=vals.length?Math.round(Math.max(...vals)):0;
html+=`<div style="background:${t.color}15;border:2px solid ${t.color};border-radius:12px;padding:16px;text-align:center">
<div style="font-weight:700;font-size:13px;color:${t.color};margin-bottom:8px">${t.label}</div>
<div style="font-size:28px;font-weight:800;color:var(--navy)">${avg}</div>
<div style="font-size:11px;color:var(--gray500)">Avg OC Cutoff</div>
<div style="font-size:11px;color:var(--gray500);margin-top:4px">Range: ${min} - ${max}</div>
<div style="font-size:11px;color:var(--gray500)">${records.length} records</div>
</div>`;
});
html+='</div>';
document.getElementById('tierChart').innerHTML=html;
}

function renderPositionAnalysis(){
const cutoff=parseFloat(document.getElementById('ins-cutoff').value)||0;
const cat=document.getElementById('ins-cat').value;
if(!cutoff){document.getElementById('positionAnalysis').innerHTML='';return}

const bgGroups={};
DATA.forEach(d=>{
if(!bgGroups[d.bg])bgGroups[d.bg]={safe:0,close:0,reach:0,total:0};
bgGroups[d.bg].total++;
const cv=d[cat]||0;
if(cv>0&&cutoff>=cv)bgGroups[d.bg].safe++;
else if(cv>0&&cutoff>=cv-10)bgGroups[d.bg].close++;
else bgGroups[d.bg].reach++;
});

let html='<div style="overflow-x:auto"><table style="width:100%;border-collapse:collapse;font-size:13px"><thead><tr style="background:var(--navy);color:white"><th style="padding:10px;text-align:left">Branch Group</th><th style="padding:10px;text-align:center">Total</th><th style="padding:10px;text-align:center;color:#22c55e">Safe</th><th style="padding:10px;text-align:center;color:#f59e0b">Close</th><th style="padding:10px;text-align:center;color:#ef4444">Reach</th></tr></thead><tbody>';
Object.entries(bgGroups).sort((a,b)=>b[1].safe-a[1].safe).forEach(([bg,v])=>{
html+=`<tr><td style="padding:8px;font-weight:600;border-bottom:1px solid var(--gray200)">${bg}</td>
<td style="padding:8px;text-align:center;border-bottom:1px solid var(--gray200)">${v.total}</td>
<td style="padding:8px;text-align:center;border-bottom:1px solid var(--gray200);color:var(--safe);font-weight:700">${v.safe}</td>
<td style="padding:8px;text-align:center;border-bottom:1px solid var(--gray200);color:var(--close);font-weight:700">${v.close}</td>
<td style="padding:8px;text-align:center;border-bottom:1px solid var(--gray200);color:var(--reach);font-weight:700">${v.reach}</td></tr>`;
});
html+='</tbody></table></div>';

// Recommendation
let rec='';
const totalSafe=Object.values(bgGroups).reduce((a,b)=>a+b.safe,0);
if(cutoff>=180)rec='<div style="margin-top:16px;padding:16px;background:rgba(34,197,94,0.1);border-radius:var(--radius);border-left:4px solid var(--safe)"><strong style="color:var(--safe)">Excellent Score!</strong> You have strong options across both top colleges and popular branches. Focus on getting your preferred branch in the best possible college.</div>';
else if(cutoff>=160)rec='<div style="margin-top:16px;padding:16px;background:rgba(245,158,11,0.1);border-radius:var(--radius);border-left:4px solid var(--close)"><strong style="color:var(--close)">Good Score!</strong> You have decent options. Consider prioritizing Tier-1/Tier-2 colleges even if you cannot get CSE. ECE, EEE, or Mech in a top college is better than CSE in a Tier-3 college.</div>';
else if(cutoff>=130)rec='<div style="margin-top:16px;padding:16px;background:rgba(239,68,68,0.1);border-radius:var(--radius);border-left:4px solid var(--reach)"><strong style="color:var(--reach)">Moderate Score.</strong> Strongly recommend choosing COLLEGE over BRANCH. A good Tier-2 college with any branch will serve your career far better than a low-ranked college with CSE. Focus on placement records.</div>';
else rec='<div style="margin-top:16px;padding:16px;background:rgba(239,68,68,0.1);border-radius:var(--radius);border-left:4px solid var(--reach)"><strong style="color:var(--reach)">Focus on College Quality.</strong> At this cutoff range, the college you choose is critical. Pick the highest-ranked college you can get into regardless of branch. Contact EduAakashaA for personalized guidance.</div>';

html+=rec;
html+=`<p style="margin-top:12px;font-size:12px;color:var(--gray500)">You have <strong>${totalSafe}</strong> safe options across all branch groups for ${CAT_LABELS[cat]} category with cutoff ${cutoff}.</p>`;
document.getElementById('positionAnalysis').innerHTML=html;
}

// ===== PDF REPORT =====
function generatePDFReport(){
// Validate form
const name=document.getElementById('sf-name').value.trim();
const email=document.getElementById('sf-email').value.trim();
const phone=document.getElementById('sf-phone').value.trim();
const location=document.getElementById('sf-location').value.trim();
const school=document.getElementById('sf-school').value.trim();
if(!name||!email||!phone||!location||!school){
alert('Please fill all mandatory fields in the Student Registration form above.');
document.getElementById('sf-name').focus();
return;
}
const score=parseFloat(document.getElementById('p-score').textContent)||0;
if(score<=0){alert('Please enter your marks first to generate predictions.');return}

// Send to Google Sheets
sendToGoogleSheets({name,email,phone,location,school,score,category:document.getElementById('p-cat').value,hsc:document.getElementById('sf-hsc').value});

// Show modal
document.getElementById('pdfModal').classList.add('show');
document.getElementById('pdfStatus').style.display='block';
document.getElementById('pdfResult').style.display='none';

setTimeout(()=>{
document.getElementById('pdfStatus').style.display='none';
document.getElementById('pdfResult').style.display='block';
},2000);
}

function closePdfModal(){document.getElementById('pdfModal').classList.remove('show')}

function downloadPDFReport(){
const name=document.getElementById('sf-name').value.trim();
const email=document.getElementById('sf-email').value.trim();
const phone=document.getElementById('sf-phone').value.trim();
const location=document.getElementById('sf-location').value.trim();
const school=document.getElementById('sf-school').value.trim();
const score=document.getElementById('p-score').textContent;
const cat=CAT_LABELS[document.getElementById('p-cat').value];
const catKey=document.getElementById('p-cat').value;
const sc=parseFloat(score)||0;
const safeColleges=filteredColleges.filter(c=>c.bestPrediction==='safe').slice(0,30);
const closeColleges=filteredColleges.filter(c=>c.bestPrediction==='close').slice(0,15);

// Build Top 30 recommended choices
let top30=[];
safeColleges.forEach(col=>{
col.branches.filter(b=>b.prediction==='safe').forEach(b=>{
top30.push({college:col.name,code:col.code,branch:b.bn,branchCode:b.bc,cutoff:b[catKey],er:col.er,type:getCollegeTypeLabel(col.type),tier:getTierLabel(col.tier)});
});
});
top30.sort((a,b)=>(a.er||999)-(b.er||999));
top30=top30.slice(0,30);

// Strategy based on score
let strategy='';
if(sc>=190)strategy='Score Band: 190-200 (Rank 1-500). Target CSE/AI&DS/CSBS at Anna University CEG, MIT, ACT. Aim for NIRF top-3 colleges.';
else if(sc>=185)strategy='Score Band: 185-190 (Rank 500-2K). Target CSE/IT/AI&ML at SSN, PSG Tech, Thiagarajar, CIT, Kongu.';
else if(sc>=180)strategy='Score Band: 180-185 (Rank 2K-5K). Mix of CS-family at Tier-2 + non-CS at Tier-1. Consider ECE at top colleges.';
else if(sc>=170)strategy='Score Band: 170-180 (Rank 5K-15K). Prioritize COLLEGE over BRANCH. Tier-1/2 college with any branch beats Tier-3 with CSE.';
else if(sc>=150)strategy='Score Band: 150-170 (Rank 15K-50K). Focus on best-ranked college. Autonomous status and placement record matter most.';
else strategy='Score Band: Below 150. Choose the highest EA-ranked college available. Focus on certifications and skills alongside your degree.';

let html=`<!DOCTYPE html><html><head><meta charset="UTF-8"><title>TNEA 2026 Report - ${name}</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,600;0,9..144,700;1,9..144,500&family=Plus+Jakarta+Sans:wght@400;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Plus Jakarta Sans',sans-serif;color:#0E1B3D;background:#FBF7EE;line-height:1.6}
.page{max-width:800px;margin:0 auto;padding:40px 48px;min-height:100vh;background:#FFFDF7;position:relative}
.header{display:flex;justify-content:space-between;align-items:center;border-bottom:2px solid #0E3A8A;padding-bottom:16px;margin-bottom:32px}
.brand{font-family:'Plus Jakarta Sans',sans-serif;font-size:20px;font-weight:800;color:#071A44}
.brand span{color:#FF6B0A}
.meta{font-family:'JetBrains Mono',monospace;font-size:10px;text-transform:uppercase;letter-spacing:.15em;color:#5A6278;text-align:right}
h1{font-family:'Fraunces',serif;font-size:28px;font-weight:700;color:#071A44;letter-spacing:-.025em;margin-bottom:8px}
h1 em{font-style:italic;font-weight:500;color:#FF6B0A}
h2{font-family:'Fraunces',serif;font-size:20px;font-weight:600;color:#0E3A8A;margin:28px 0 12px;padding-bottom:6px;border-bottom:1px solid #E8DFC8}
h2::before{content:'';display:inline-block;width:26px;height:2px;background:#FF6B0A;margin-right:10px;vertical-align:middle}
h3{font-size:14px;font-weight:700;color:#071A44;margin:16px 0 6px}
p,li{font-size:13px;line-height:1.7;color:#0E1B3D}
.eyebrow{font-family:'JetBrains Mono',monospace;font-size:10px;text-transform:uppercase;letter-spacing:.2em;color:#FF6B0A;margin-bottom:4px}
.score-box{background:linear-gradient(135deg,#0E3A8A,#0A2560);color:#fff;border-radius:14px;padding:24px;text-align:center;margin:16px 0}
.score-num{font-family:'Fraunces',serif;font-size:48px;font-weight:900;color:#FF8A3D}
.score-label{font-family:'JetBrains Mono',monospace;font-size:10px;text-transform:uppercase;letter-spacing:.2em;opacity:.5}
.info-grid{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:12px 0}
.info-item{font-size:12px;padding:6px 10px;background:#F5EFDF;border-radius:8px}
.info-item strong{color:#0E3A8A}
table{width:100%;border-collapse:collapse;font-size:11px;margin:12px 0}
th{background:#0E3A8A;color:#fff;padding:8px;text-align:left;font-family:'JetBrains Mono',monospace;font-size:9px;text-transform:uppercase;letter-spacing:.1em}
td{padding:7px 8px;border-bottom:1px solid #E8DFC8}
tr:nth-child(even){background:#FBF7EE}
.safe{color:#1F8B5C;font-weight:600}.close{color:#E89A1C;font-weight:600}.reach{color:#C23A3A;font-weight:600}
.tip{border-left:3px solid #FF6B0A;padding:10px 14px;margin:8px 0;background:#FBF7EE;border-radius:0 8px 8px 0;font-size:12px}
.tip strong{color:#071A44}
.check{padding:4px 0;font-size:12px}.check::before{content:'\\2610 ';color:#0E3A8A;font-size:14px}
.do{color:#1F8B5C;font-size:12px;padding:3px 0}.do::before{content:'\\2713 ';font-weight:700}
.dont{color:#C23A3A;font-size:12px;padding:3px 0}.dont::before{content:'\\2717 ';font-weight:700}
.promo{background:linear-gradient(135deg,#0E3A8A,#0A2560);color:#fff;border-radius:14px;padding:24px;margin:20px 0;position:relative;overflow:hidden}
.promo::after{content:'';position:absolute;right:-60px;top:-60px;width:200px;height:200px;border-radius:50%;background:radial-gradient(circle,rgba(255,107,10,.2),transparent 65%)}
.promo h3{color:#FF8A3D;margin:0 0 8px;font-family:'Fraunces',serif;font-size:18px}
.promo p{font-size:12px;opacity:.85;position:relative;z-index:1}
.promo .price{font-family:'Fraunces',serif;font-size:32px;font-weight:700;color:#FF8A3D;margin:8px 0}
.footer{border-top:2px solid #0E3A8A;padding-top:12px;margin-top:32px;display:flex;justify-content:space-between;font-size:10px;color:#5A6278}
.footer a{color:#FF6B0A;text-decoration:none}
.pagebreak{page-break-before:always;break-before:page}
@media print{.page{padding:24px 32px;box-shadow:none}}
</style></head><body>`;

// PAGE 1: Cover + Profile
html+=`<div class="page">
<div class="header"><div><div class="brand">Edu<span>AakashaA</span></div><div style="font-size:11px;color:#5A6278">Guiding students towards the right future</div></div><div class="meta">TNEA 2026<br>Personalised Report<br>${new Date().toLocaleDateString('en-IN')}</div></div>
<div class="eyebrow">EduAakashaA &middot; TNEA 2026</div>
<h1>Personalised College <em>Prediction Report</em></h1>
<p style="color:#5A6278;margin-bottom:20px">Built on official Anna University 2025 cutoff data. 420 colleges, 105 branches, 239,299 applicants analyzed.</p>

<h2>Student Profile</h2>
<div class="info-grid">
<div class="info-item"><strong>Name:</strong> ${name}</div>
<div class="info-item"><strong>Email:</strong> ${email}</div>
<div class="info-item"><strong>Phone:</strong> ${phone}</div>
<div class="info-item"><strong>Location:</strong> ${location}</div>
<div class="info-item"><strong>School:</strong> ${school}</div>
<div class="info-item"><strong>Community:</strong> ${cat}</div>
</div>

<div class="score-box"><div class="score-label">Your TNEA Cutoff Score</div><div class="score-num">${score}</div><div class="score-label">out of 200</div></div>

<h2>Score Band Strategy</h2>
<div class="tip"><strong>Your Position:</strong> ${strategy}</div>
<div class="tip"><strong>Key Insight:</strong> Cut-offs rose +10.84 marks on average from 2023 to 2025 across top 50 colleges. 81.2% of college-branch combinations saw rising OC cut-offs. Plan for the same trajectory in 2026.</div>

<h2>Prediction Summary</h2>
<div class="info-grid">
<div class="info-item"><strong class="safe">${document.getElementById('cnt-safe').textContent} Safe</strong> colleges found</div>
<div class="info-item"><strong class="close">${document.getElementById('cnt-close').textContent} Close</strong> match colleges</div>
<div class="info-item"><strong class="reach">${document.getElementById('cnt-reach').textContent} Reach</strong> colleges</div>
<div class="info-item"><strong>Total:</strong> ${document.getElementById('cnt-total').textContent} matches</div>
</div>

<div class="footer"><div>India: +91 8015722706</div><div><a href="https://eduaakashaa.in">www.eduaakashaa.in</a> &middot; info@eduaakashaa.com</div></div>
</div>`;

// PAGE 2: Top 30 Recommendations
html+=`<div class="page pagebreak">
<div class="header"><div class="brand">Edu<span>AakashaA</span></div><div class="meta">TOP 30 CHOICES<br>${name} &middot; ${cat}</div></div>
<h2>Top 30 Recommended Choices</h2>
<p style="font-size:11px;color:#5A6278;margin-bottom:12px">Sorted by EA Expert Rank. Use the Dream (6) : Target (12) : Safe (12) ratio for choice filling.</p>
<table><thead><tr><th>#</th><th>College</th><th>Branch</th><th>Code</th><th>EA</th><th>Type</th><th>Cutoff</th></tr></thead><tbody>`;
top30.forEach((r,i)=>{
const tag=i<6?'Dream':i<18?'Target':'Safe';
const cls=i<6?'reach':i<18?'close':'safe';
html+=`<tr><td style="font-weight:700;color:#FF6B0A">${i+1}</td><td style="font-weight:600;max-width:200px;font-size:10px">${r.college.substring(0,60)}</td><td style="font-size:10px">${r.branch.substring(0,30)}</td><td>${r.code}-${r.branchCode}</td><td style="font-weight:700;color:#0E3A8A">#${r.er||'N/A'}</td><td style="font-size:9px">${r.type}</td><td class="${cls}">${r.cutoff}</td></tr>`;
});
html+=`</tbody></table>
<div class="tip"><strong>Important:</strong> Always type the 4-digit college code first on the TNEA portal. Confirm the autofilled name matches. 9 colleges are named "Government College of Engineering" across TN - verify the district.</div>
<div class="footer"><div>India: +91 8015722706</div><div><a href="https://eduaakashaa.in">www.eduaakashaa.in</a> &middot; info@eduaakashaa.com</div></div>
</div>`;

// PAGE 3: Do's, Don'ts, Strategy
html+=`<div class="page pagebreak">
<div class="header"><div class="brand">Edu<span>AakashaA</span></div><div class="meta">STRATEGY &amp; TIPS<br>Choice Filling Guide</div></div>
<h2>Choice Filling Strategy</h2>
<div class="tip"><strong>The 1:2:2 Rule:</strong> List 6 Dream choices (+1 to +2.5 above your cutoff), 12 Target choices (near your cutoff), and 12 Safe choices (-1.5 to -3 below). Round-1 cutoffs drift +1-2 marks yearly.</div>
<div class="tip"><strong>52% Rule:</strong> In 2025, 52% of all TNEA seats were CS-family. CSE alone took 27,926 seats - more than ECE (18,762) and AI&DS (17,240) combined.</div>
<div class="tip"><strong>Round 3 Matters:</strong> Three rounds placed every seat in 2025. Round 1: 26,719 seats (avg 187.87). Round 2: 52,682 seats (avg 158.4). Round 3: 50,093 seats (avg 124.26). Plan with R3 in mind.</div>

<h2>Eight Rules to Memorise</h2>
<div class="do">Type the 4-digit college code first. Portal autofills the name - verify it.</div>
<div class="do">Sort choices in true preference order. System auto-allocates the highest available.</div>
<div class="do">List 30-50 choices, not 10. Short lists lose seats.</div>
<div class="do">Double-check the branch code. CS and AM differ by one letter and 10 cutoff marks.</div>
<div class="do">Verify NAAC and NBA accreditation per branch, not just institution-level.</div>
<div class="do">Cross-check location. Match district AND street address.</div>
<div class="do">Save, Print, Review with a parent, then Submit.</div>
<div class="do">Verify all data with official tneaonline.org before final submission.</div>

<h2>Do's and Don'ts</h2>
<h3>Do's</h3>
<div class="do">Research placement records of each college - not just cutoffs</div>
<div class="do">Consider location proximity to IT hubs (Chennai, Coimbatore) for internships</div>
<div class="do">Fill maximum choices to increase chances across all 3 rounds</div>
<div class="do">Take the EduAakashaA Aptitude Assessment before deciding branch</div>
<div class="do">Prioritize Autonomous colleges - they design curriculum with industry alignment</div>
<div class="do">Check if the college has NBA accreditation for your specific branch</div>

<h3>Don'ts</h3>
<div class="dont">Don't chase only CSE/IT - if cutoff is below 160, a Tier-1 college with Mech/ECE is better</div>
<div class="dont">Don't fill fewer than 20 choices - you'll miss opportunities in later rounds</div>
<div class="dont">Don't choose based on peer pressure - your career path is unique</div>
<div class="dont">Don't ignore college brand for branch name - employers see the college first</div>
<div class="dont">Don't blindly trust any AI tool - always verify with official data and a counsellor</div>
<div class="dont">Don't submit without reviewing with a parent or mentor - fresh eyes catch mistakes</div>

<div class="footer"><div>India: +91 8015722706</div><div><a href="https://eduaakashaa.in">www.eduaakashaa.in</a> &middot; info@eduaakashaa.com</div></div>
</div>`;

// PAGE 4: Checklist + Expert Guidance CTA
html+=`<div class="page pagebreak">
<div class="header"><div class="brand">Edu<span>AakashaA</span></div><div class="meta">CHECKLIST &amp; NEXT STEPS<br>Before You Submit</div></div>
<h2>Pre-Submission Checklist</h2>
<div class="check">Calculated cutoff score correctly: M + (P/2) + (C/2)</div>
<div class="check">Verified HSC marks on official marksheet</div>
<div class="check">Registered on tneaonline.org before June 2 deadline</div>
<div class="check">Uploaded all required documents (Photo, Signature, Certificates)</div>
<div class="check">Completed EduAakashaA Aptitude Assessment</div>
<div class="check">Listed at least 30 college-branch choices</div>
<div class="check">Verified each 4-digit college code against autofilled name</div>
<div class="check">Verified each branch code (CS vs CM vs AM vs AD)</div>
<div class="check">Checked NAAC/NBA accreditation for target colleges</div>
<div class="check">Reviewed placement records for top 10 choices</div>
<div class="check">Applied Dream:Target:Safe ratio (1:2:2)</div>
<div class="check">Sorted choices in true preference order</div>
<div class="check">Reviewed entire list with parent/guardian</div>
<div class="check">Saved draft, printed, and done final review</div>
<div class="check">Locked choices before deadline</div>
<div class="check">Downloaded locked choices PDF for records</div>

<h2>Why Expert Guidance Matters</h2>
<div class="tip"><strong>The Portal is the Floor. The Counsellor is the Ceiling.</strong> A dashboard cannot ask "why this college?" - your shortlist isn't just cutoffs, it's the full picture of your life. Family budget, hostel vs day-scholar, career goals - we ask the questions an algorithm doesn't know to ask.</div>
<div class="tip"><strong>We catch the typo at code 1438.</strong> Before you submit, a counsellor walks the entire list with you. Code by code. Branch by branch. Mistake by mistake - caught.</div>

<div class="promo">
<h3>Expert Guidance &amp; Choice Filling Support</h3>
<p>For complete TNEA 2026 choice filling support with a dedicated counsellor, register with EduAakashaA.</p>
<div class="price" style="position:relative;z-index:1">Rs. 5,000 <span style="font-size:14px;opacity:.6;text-decoration:line-through">Rs. 8,000</span></div>
<p style="position:relative;z-index:1"><strong>What you get:</strong> Personalised 6-page report + 30-min counsellor session + Choice list review (code-by-code) + Allotment day support + Round 2/3 guidance</p>
<p style="margin-top:10px;position:relative;z-index:1"><strong>Contact:</strong> +91 8015722706 (India)</p>
<p style="position:relative;z-index:1"><strong>Register:</strong> www.eduaakashaa.in | info@eduaakashaa.com</p>
<p style="position:relative;z-index:1"><strong>WhatsApp:</strong> https://whatsapp.com/channel/0029VbBxOWUKwqSYpWBgge1x</p>
</div>

<div style="text-align:center;margin-top:20px;padding:16px;background:#FBF7EE;border-radius:14px;border:1.5px solid #E8DFC8">
<div style="font-family:'JetBrains Mono',monospace;font-size:10px;text-transform:uppercase;letter-spacing:.15em;color:#FF6B0A;margin-bottom:4px">EduAakashaA &middot; Coimbatore</div>
<div style="font-family:'Fraunces',serif;font-size:16px;font-weight:600;color:#071A44">Guiding students towards the right future</div>
<div style="font-size:11px;color:#5A6278;margin-top:4px">Mon-Fri 9:00-22:00 | Sat &amp; Sun 9:00-16:00</div>
</div>

<div class="footer"><div>India: +91 8015722706</div><div><a href="https://eduaakashaa.in">www.eduaakashaa.in</a> &middot; info@eduaakashaa.com</div></div>
</div>`;

html+=`</body></html>`;

// Open in new window for print/save
const w=window.open('','_blank');
w.document.write(html);
w.document.close();
setTimeout(()=>{w.print()},800);
}

function sendToGoogleSheets(data){
// DEPLOY: See Google Apps Script setup instructions below
// Sheet ID: 1qXMglU5wEFIAik5cskaS1EYLFzn_SBBaDWFeiVeAf-E
// After deploying your Apps Script, replace YOUR_DEPLOYED_SCRIPT_ID below
const SHEET_URL='https://script.google.com/macros/s/AKfycbzsKWC8kuw_Qs_CHCcre31vz44lgHht5O_9J7-PV0Sp4Epko9pYuBKL-vQwu8I-M6ts/exec';
const payload={
name:data.name,email:data.email,phone:data.phone,
location:data.location,school:data.school,
score:data.score,category:data.category,
hsc:data.hsc||'',timestamp:new Date().toISOString(),
safeCount:document.getElementById('cnt-safe')?.textContent||'0',
closeCount:document.getElementById('cnt-close')?.textContent||'0',
totalCount:document.getElementById('cnt-total')?.textContent||'0'
};
// POST request for better data handling
fetch('/api/leads?source=tnea2026',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)}).catch(function(){});
fetch(SHEET_URL,{method:'POST',mode:'no-cors',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)}).then(()=>{
console.log('Student data sent to Google Sheets successfully');
}).catch(err=>{
console.log('Google Sheets send attempted (no-cors mode):',err);
});
}

// ===== GOOGLE DRIVE SAVE =====
function savePDFToGoogleDrive(){
const name=document.getElementById('sf-name').value.trim();
const email=document.getElementById('sf-email').value.trim();
const score=document.getElementById('p-score').textContent;
const cat=document.getElementById('p-cat').value;
if(!name||!email){alert('Please fill student details first.');return}
// This calls the same Apps Script which handles Drive save
const SHEET_URL='https://script.google.com/macros/s/AKfycbzsKWC8kuw_Qs_CHCcre31vz44lgHht5O_9J7-PV0Sp4Epko9pYuBKL-vQwu8I-M6ts/exec';
const payload={
action:'savePDF',
name:name,email:email,score:score,category:cat,
safeColleges:filteredColleges.filter(c=>c.bestPrediction==='safe').slice(0,20).map(c=>({name:c.name,er:c.er,type:getCollegeTypeLabel(c.type),safeBranches:c.safeBranches})),
closeColleges:filteredColleges.filter(c=>c.bestPrediction==='close').slice(0,10).map(c=>({name:c.name,er:c.er}))
};
fetch('/api/leads?source=tnea2026',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)}).catch(function(){});
fetch(SHEET_URL,{method:'POST',mode:'no-cors',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)}).then(()=>{
alert('Report save request sent! Check your email for the Google Drive link.');
}).catch(()=>{
alert('Save request sent. Please check your Google Drive folder.');
});
}

// ===== CONTACT FORM =====
function submitContactForm(){
var name=document.getElementById('reg-name').value.trim();
var phone=document.getElementById('reg-phone').value.trim();
var email=(document.getElementById('reg-email')||{}).value||'';
var interest=(document.getElementById('reg-interest')||{}).value||'';
if(!name||!phone){alert('Please enter your name and phone number.');return}
sendToGoogleSheets({name:name,email:email,phone:phone,location:'Contact Form',school:interest||'General',score:'N/A',category:'consultation',hsc:'',
safeCount:'0',closeCount:'0',totalCount:'Contact Request'});
document.getElementById('reg-name').value='';
document.getElementById('reg-phone').value='';
if(document.getElementById('reg-email'))document.getElementById('reg-email').value='';
if(document.getElementById('reg-interest'))document.getElementById('reg-interest').value='';
alert('Thank you, '+name+'! Our expert will call you within 24 hours. You can also reach us on WhatsApp.');
}

// ===== INIT =====
initFilters();


;

	const heightObserver = new ResizeObserver(([{ contentRect }]) => {
		window.parent.postMessage({ action: 'iframeHeightUpdated', height: contentRect.height, id: 'z36BZv' }, '*');
	});

	heightObserver.observe(document.documentElement);
