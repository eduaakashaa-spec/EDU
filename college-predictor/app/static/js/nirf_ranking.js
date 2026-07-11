

const DATA = window.EA_NIRF300 || [];

// ── helpers ──
function getRankBadge(r){
  if(r===1) return '<span class="rank-badge r1">1</span>';
  if(r===2) return '<span class="rank-badge r2">2</span>';
  if(r===3) return '<span class="rank-badge r3">3</span>';
  if(r&&r<=10) return `<span class="rank-badge r-top">${r}</span>`;
  if(r) return `<span class="rank-badge r-top" style="font-size:0.8rem">${r}</span>`;
  return '<span class="rank-badge r-band">&mdash;</span>';
}
function getScore(s){
  if(!s) return '<span style="color:var(--muted);font-size:0.78rem">Band ranked</span>';
  return `<div class="score-cell"><div class="score-track"><div class="score-fill" style="width:${((s/90)*100).toFixed(0)}%"></div></div><span class="score-val">${s.toFixed(2)}</span></div>`;
}
function getType(t){return `<span class="type-tag type-${t}">${t}</span>`;}
function getSt(s){return `<span class="state-tag">${s}</span>`;}
function getBand(b){
  const m={"Rank 1 -100":"band-1","Rank 101-150":"band-2","Rank 151 to 200":"band-3","Rank 201 to 300":"band-4"};
  const l={"Rank 1 -100":"1&ndash;100","Rank 101-150":"101&ndash;150","Rank 151 to 200":"151&ndash;200","Rank 201 to 300":"201&ndash;300"};
  return `<span class="band-badge ${m[b]||'band-4'}">${l[b]||b}</span>`;
}
function getLink(url){
  const d=url.replace(/https?:\/\//,'').split('/')[0];
  return `<a class="web-link" href="${url}" target="_blank" rel="noopener">&#127760; ${d.substring(0,18)}</a>`;
}
function makeTopCard(r,i){
  const rc=i===0?'gold':i===1?'silver':i===2?'bronze':'';
  return `<div class="top-card">
    <div class="tc-rank ${rc}">#${r.rank||'&mdash;'}</div>
    <div class="tc-body">
      <div class="tc-name">${r.name}</div>
      <div class="tc-city">${r.city}, ${r.state} &middot; ${r.type}</div>
      ${r.score?`<div class="tc-score">${r.score.toFixed(2)}<span style="font-size:0.75rem;color:var(--muted)">/100</span></div>`:''}
      <a class="tc-web" href="${r.url}" target="_blank">&#127760; Visit Website</a>
    </div>
  </div>`;
}

// ── Build state data ──
function buildStateData(){
  const map={};
  DATA.forEach(r=>{
    if(!map[r.state]) map[r.state]={state:r.state,total:0,in100:0,in150:0,bestRank:null,bestScore:null,scores:[],colleges:[]};
    const s=map[r.state];
    s.total++;
    s.colleges.push(r);
    if(r.rank&&r.rank<=100) s.in100++;
    if(r.rank&&r.rank<=150) s.in150++;
    if(r.rank&&(s.bestRank===null||r.rank<s.bestRank)) s.bestRank=r.rank;
    if(r.score){s.scores.push(r.score);if(s.bestScore===null||r.score>s.bestScore)s.bestScore=r.score;}
  });
  Object.values(map).forEach(s=>{
    s.avgScore=s.scores.length?+(s.scores.reduce((a,b)=>a+b,0)/s.scores.length).toFixed(2):0;
    s.colleges.sort((a,b)=>{if(a.rank&&b.rank)return a.rank-b.rank;if(a.rank)return -1;if(b.rank)return 1;return a.name.localeCompare(b.name);});
  });
  return Object.values(map).sort((a,b)=>b.total-a.total);
}
const STATE_DATA=buildStateData();

// ── QUADRANT CHART ──
let qChart=null;

function getAxisVal(s,key){
  if(key==='in100') return s.in100;
  if(key==='in150') return s.in150;
  if(key==='bestScore') return s.bestScore||0;
  if(key==='avgScore') return s.avgScore||0;
  if(key==='total') return s.total;
  return s.total;
}
function getAxisLabel(key){
  const labels={
    in100:'Colleges in Rank 1\u201C100',in150:'Colleges in Rank 1\u2013150',
    bestScore:'Best NIRF Score',avgScore:'Avg NIRF Score (ranked)',total:'Total Colleges'
  };
  return labels[key]||key;
}

function redrawQuadrant(){
  if(!document.getElementById('quadrantChart')) return;
  const yKey=document.getElementById('yAxisSel').value;
  const xKey=document.getElementById('xAxisSel').value;
  const labelMode=document.getElementById('labelSel').value;

  const pts=STATE_DATA.map(s=>{
    const x=getAxisVal(s,xKey);
    const y=getAxisVal(s,yKey);
    const br=s.bestRank?Math.max(7,Math.min(30,32-(s.bestRank/100)*22)):5;
    return {x,y,r:br,_s:s,_st:s.state};
  });

  const allX=pts.map(p=>p.x).sort((a,b)=>a-b);
  const allY=pts.map(p=>p.y).sort((a,b)=>a-b);
  const xMed=allX[Math.floor(allX.length/2)];
  const yMed=allY[Math.floor(allY.length/2)];

  const byQ=[[],[],[],[]]; // Elite, Efficient, Developing, Emerging
  pts.forEach(p=>{
    const hi_x=p.x>=xMed, hi_y=p.y>=yMed;
    if(hi_x&&hi_y) byQ[0].push(p);
    else if(!hi_x&&hi_y) byQ[1].push(p);
    else if(hi_x&&!hi_y) byQ[2].push(p);
    else byQ[3].push(p);
  });

  const datasets=[
    {label:'Elite (High vol \xb7 High rank)',data:byQ[0],backgroundColor:'rgba(255,107,0,0.78)',borderColor:'rgba(255,107,0,1)',borderWidth:2,hoverBorderWidth:3},
    {label:'Efficient (Low vol \xb7 High rank)',data:byQ[1],backgroundColor:'rgba(34,211,160,0.78)',borderColor:'rgba(34,211,160,1)',borderWidth:2,hoverBorderWidth:3},
    {label:'Developing (High vol \xb7 Low rank)',data:byQ[2],backgroundColor:'rgba(251,191,36,0.78)',borderColor:'rgba(251,191,36,1)',borderWidth:2,hoverBorderWidth:3},
    {label:'Emerging (Low vol \xb7 Low rank)',data:byQ[3],backgroundColor:'rgba(107,120,152,0.78)',borderColor:'rgba(107,120,152,1)',borderWidth:2,hoverBorderWidth:3},
  ];

  const top10states=STATE_DATA.slice(0,10).map(s=>s.state);

  const pluginQuadLines={
    id:'quadLines',
    afterDraw(chart){
      const {ctx,scales}=chart;
      const xS=scales.x,yS=scales.y;
      const xPx=xS.getPixelForValue(xMed);
      const yPx=yS.getPixelForValue(yMed);
      ctx.save();
      ctx.setLineDash([7,5]);
      ctx.strokeStyle='rgba(255,255,255,0.14)';
      ctx.lineWidth=1.5;
      ctx.beginPath();ctx.moveTo(xPx,yS.top);ctx.lineTo(xPx,yS.bottom);ctx.stroke();
      ctx.beginPath();ctx.moveTo(xS.left,yPx);ctx.lineTo(xS.right,yPx);ctx.stroke();
      ctx.setLineDash([]);
      // Quadrant watermark labels
      const lw=(xS.right-xS.left)/2, lh=(yS.bottom-yS.top)/2;
      ctx.font='bold 13px Arial';
      ctx.fillStyle='rgba(255,255,255,0.07)';
      ctx.textAlign='center';
      ctx.fillText('ELITE'        , xPx+lw*0.55, yS.top+26);
      ctx.fillText('EFFICIENT'    , xPx-lw*0.55, yS.top+26);
      ctx.fillText('DEVELOPING'   , xPx+lw*0.55, yS.bottom-14);
      ctx.fillText('EMERGING'     , xPx-lw*0.55, yS.bottom-14);
      ctx.restore();
    }
  };

  const pluginLabels={
    id:'stateLabels',
    afterDatasetsDraw(chart){
      const {ctx}=chart;
      chart.data.datasets.forEach((ds,di)=>{
        const meta=chart.getDatasetMeta(di);
        if(!meta.visible) return;
        ds.data.forEach((pt,pi)=>{
          const el=meta.data[pi];
          if(!el) return;
          const show=labelMode==='always'||(labelMode==='top10'&&top10states.includes(pt._st));
          if(!show) return;
          const s=pt._st;
          const short=s.length>13?s.substring(0,12)+'\u2026':s;
          const rad=el.options.radius||8;
          ctx.save();
          ctx.font='bold 9.5px Arial';
          ctx.fillStyle='rgba(255,255,255,0.88)';
          ctx.textAlign='center';
          ctx.textBaseline='top';
          ctx.shadowColor='rgba(0,0,0,0.9)';
          ctx.shadowBlur=5;
          ctx.fillText(short,el.x,el.y+rad+4);
          ctx.restore();
        });
      });
    }
  };

  if(qChart){qChart.destroy();qChart=null;}

  qChart=new Chart(document.getElementById('quadrantChart'),{
    type:'bubble',
    data:{datasets},
    options:{
      responsive:true,
      maintainAspectRatio:false,
      aspectRatio:1.8,
      interaction:{mode:'nearest',intersect:true},
      plugins:{
        legend:{
          position:'bottom',
          labels:{color:'rgba(232,237,248,0.65)',font:{size:11,family:'Arial'},boxWidth:12,padding:18}
        },
        tooltip:{
          backgroundColor:'rgba(10,13,22,0.97)',
          titleColor:'#FF6B00',bodyColor:'rgba(232,237,248,0.85)',
          borderColor:'rgba(255,107,0,0.45)',borderWidth:1,padding:14,
          callbacks:{
            title:items=>items[0]?.raw?._st||'',
            label:item=>{
              const s=item.raw?._s;
              if(!s) return '';
              return [
                ` Total colleges: ${s.total}`,
                ` In Rank 1\u2013100: ${s.in100}`,
                ` Best rank: ${s.bestRank?'#'+s.bestRank:'\u2014'}`,
                ` Best score: ${s.bestScore?s.bestScore.toFixed(2):'\u2014'}`,
                ` Avg score: ${s.avgScore?s.avgScore.toFixed(2):'\u2014'}`,
              ];
            }
          }
        }
      },
      scales:{
        x:{
          title:{display:true,text:getAxisLabel(xKey),color:'rgba(255,107,0,0.75)',font:{size:12,weight:'bold',family:'Arial'},padding:{top:8}},
          ticks:{color:'rgba(232,237,248,0.5)',font:{size:10,family:'Arial'}},
          grid:{color:'rgba(255,255,255,0.04)'},
          border:{color:'rgba(255,107,0,0.2)'}
        },
        y:{
          title:{display:true,text:getAxisLabel(yKey),color:'rgba(255,107,0,0.75)',font:{size:12,weight:'bold',family:'Arial'},padding:{bottom:8}},
          ticks:{color:'rgba(232,237,248,0.5)',font:{size:10,family:'Arial'}},
          grid:{color:'rgba(255,255,255,0.04)'},
          border:{color:'rgba(255,107,0,0.2)'}
        }
      },
      onClick(e,elements){
        if(!elements.length) return;
        const el=elements[0];
        const pt=qChart.data.datasets[el.datasetIndex].data[el.index];
        if(pt?._s) showStateDetail(pt._s);
      },
      animation:{duration:400}
    },
    plugins:[pluginQuadLines,pluginLabels]
  });
}

function showStateDetail(s){
  const card=document.getElementById('stateDetail');
  card.style.display='block';
  document.getElementById('sdTitle').textContent='\ud83d\udccd '+s.state+' \u2014 State Detail';
  document.getElementById('sdTotal').textContent=s.total;
  document.getElementById('sdIn100').textContent=s.in100;
  document.getElementById('sdBestRank').textContent=s.bestRank?'#'+s.bestRank:'\u2014';
  document.getElementById('sdBestScore').textContent=s.bestScore?s.bestScore.toFixed(2):'\u2014';
  const top5=s.colleges.slice(0,5);
  document.getElementById('sdColleges').innerHTML=
    '<strong style="color:var(--orange)">Top Colleges in '+s.state+':</strong><br>'+
    top5.map(c=>
      `${c.rank?'<strong style="color:var(--orange)">#'+c.rank+'</strong> ':''}`+
      `${c.name}${c.score?' <span style="color:var(--muted);">('+c.score.toFixed(2)+')</span>':''}<br>`
    ).join('');
  card.scrollIntoView({behavior:'smooth',block:'nearest'});
}

// ── STATE TABLE ──
let stSortKey='total',stSortDir=-1;
function sortST(key){
  if(stSortKey===key) stSortDir*=-1; else{stSortKey=key;stSortDir=-1;}
  renderStateTable([...STATE_DATA].sort((a,b)=>{
    if(key==='state') return stSortDir*a.state.localeCompare(b.state);
    if(key==='idx') return stSortDir*(STATE_DATA.indexOf(a)-STATE_DATA.indexOf(b));
    const av=a[key]??-1,bv=b[key]??-1;
    if(key==='bestRank') return stSortDir>0?(av===null?1:bv===null?-1:av-bv):(av===null?1:bv===null?-1:av-bv)*-1;
    return stSortDir*(bv-av);
  }));
}
function renderStateTable(data){
  let i=1;
  document.getElementById('stateCompBody').innerHTML=data.map(s=>{
    const best=s.colleges.find(c=>c.rank===s.bestRank);
    return `<tr>
      <td><strong style="color:var(--muted)">${i++}</strong></td>
      <td>${getSt(s.state)}</td>
      <td><strong style="color:var(--orange)">${s.total}</strong></td>
      <td><strong style="color:var(--green)">${s.in100}</strong></td>
      <td>${s.in150}</td>
      <td>${s.bestRank?`<strong>#${s.bestRank}</strong>`:'&mdash;'}</td>
      <td>${s.bestScore?`<span style="color:var(--orange);font-weight:700">${s.bestScore.toFixed(2)}</span>`:'&mdash;'}</td>
      <td>${s.avgScore?s.avgScore.toFixed(2):'&mdash;'}</td>
      <td style="font-size:0.82rem">${best?`<a href="${best.url}" target="_blank" style="color:var(--blue2);text-decoration:none">${best.name.substring(0,34)}${best.name.length>34?'&hellip;':''}</a>`:'&mdash;'}</td>
    </tr>`;
  }).join('');
}

// ── TABLE ──
let filt=[...DATA],pg=1,ps=25;
function applyF(){
  const s=document.getElementById('mainSearch').value.toLowerCase();
  const st=document.getElementById('stateFilter').value;
  const ty=document.getElementById('typeFilter').value;
  const bd=document.getElementById('bandFilter').value;
  const so=document.getElementById('sortFilter').value;
  filt=DATA.filter(r=>{
    if(s&&!r.name.toLowerCase().includes(s)&&!r.city.toLowerCase().includes(s)&&!r.state.toLowerCase().includes(s)) return false;
    if(st&&r.state!==st) return false;
    if(ty&&r.type!==ty) return false;
    if(bd&&r.band!==bd) return false;
    return true;
  });
  if(so==='rank') filt.sort((a,b)=>(a.rank||9999)-(b.rank||9999));
  else if(so==='score') filt.sort((a,b)=>(b.score||0)-(a.score||0));
  else if(so==='name') filt.sort((a,b)=>a.name.localeCompare(b.name));
  else if(so==='state') filt.sort((a,b)=>a.state.localeCompare(b.state));
  pg=1;renderTbl();renderPag();
  document.getElementById('tblCount').textContent=filt.length+' institutions';
}
function renderTbl(){
  const sl=filt.slice((pg-1)*ps,pg*ps);
  document.getElementById('mainBody').innerHTML=sl.map(r=>`<tr>
    <td>${getRankBadge(r.rank)}</td>
    <td><span style="font-weight:700">${r.name}</span></td>
    <td>${getScore(r.score)}</td>
    <td>${getBand(r.band)}</td>
    <td style="font-size:0.82rem">${r.city}</td>
    <td>${getSt(r.state)}</td>
    <td>${getType(r.type)}</td>
    <td>${getLink(r.url)}</td>
  </tr>`).join('');
}
function renderPag(){
  const tot=Math.ceil(filt.length/ps);
  const pages=[1,pg-1,pg,pg+1,tot].filter(p=>p>=1&&p<=tot);
  const uniq=[...new Set(pages)].sort((a,b)=>a-b);
  let html='',prev=-1;
  uniq.forEach(p=>{
    if(prev!==-1&&p-prev>1) html+='<span style="color:var(--muted);padding:0 4px">&hellip;</span>';
    html+=`<button class="pg-btn ${p===pg?'active':''}" data-pg="${p}">${p}</button>`;
    prev=p;
  });
  html+=`<span class="pg-info">Page ${pg}/${tot} &middot; ${filt.length} results</span>`;
  document.getElementById('pagination').innerHTML=html;
  document.querySelectorAll('.pg-btn[data-pg]').forEach(b=>
    b.addEventListener('click',()=>{pg=+b.dataset.pg;renderTbl();renderPag();}));
}

// ── COMPARE ──
function buildCompareDrops(){
  const ranked=DATA.filter(r=>r.rank).sort((a,b)=>a.rank-b.rank);
  const opts=ranked.map(r=>`<option value="${r.rank}">#${r.rank} ${r.name.substring(0,40)}</option>`).join('');
  ['cmpA','cmpB','cmpC'].forEach(id=>{
    document.getElementById(id).innerHTML='<option value="">Select&hellip;</option>'+opts;
    document.getElementById(id).onchange=runCompare;
  });
}
function runCompare(){
  const ids=['cmpA','cmpB','cmpC'].map(id=>document.getElementById(id).value).filter(Boolean);
  if(ids.length<2){document.getElementById('cmpResult').innerHTML='<p style="color:var(--muted);text-align:center;padding:24px">Select at least 2 colleges</p>';return;}
  const cols=ids.map(id=>DATA.find(r=>r.rank==id)).filter(Boolean);
  const rows=[
    ['Rank',r=>r.rank?`<strong style="color:var(--orange)">#${r.rank}</strong>`:'Band'],
    ['Score',r=>r.score?`<span style="color:var(--orange);font-weight:700">${r.score.toFixed(2)}</span>`:'Not scored'],
    ['Band',r=>getBand(r.band)],['Type',r=>getType(r.type)],['State',r=>getSt(r.state)],
    ['City',r=>r.city],['Website',r=>`<a href="${r.url}" target="_blank" style="color:var(--blue2)">Visit &rarr;</a>`],
  ];
  document.getElementById('cmpResult').innerHTML=`<div style="overflow-x:auto">
    <table style="width:100%;border-collapse:collapse">
      <thead><tr>
        <th style="padding:10px 14px;background:rgba(255,107,0,0.08);color:var(--orange);font-size:0.78rem;text-transform:uppercase;text-align:left">Parameter</th>
        ${cols.map(c=>`<th style="padding:10px 14px;background:rgba(255,107,0,0.08);color:#fff;font-size:0.82rem;text-align:center">${c.name.substring(0,35)}${c.name.length>35?'&hellip;':''}</th>`).join('')}
      </tr></thead>
      <tbody>${rows.map(([lbl,fn])=>`<tr>
        <td style="padding:9px 14px;color:var(--muted);font-size:0.82rem;border-bottom:1px solid rgba(255,255,255,0.04)">${lbl}</td>
        ${cols.map(c=>`<td style="padding:9px 14px;text-align:center;border-bottom:1px solid rgba(255,255,255,0.04)">${fn(c)}</td>`).join('')}
      </tr>`).join('')}</tbody>
    </table></div>`;
}

// ── STATE DRILLDOWN ──
let selState='';
function buildStatePills(){
  const cnt={};DATA.forEach(r=>cnt[r.state]=(cnt[r.state]||0)+1);
  const sorted=Object.entries(cnt).sort((a,b)=>b[1]-a[1]);
  document.getElementById('statePills').innerHTML=
    [['','All States',DATA.length],...sorted.map(([s,c])=>[s,s,c])].map(([s,lbl,c])=>
    `<div class="sp${s===selState?' sel':''}" data-st="${s}">
      <div class="sp-num">${c}</div>
      <div class="sp-name">${lbl.length>13?lbl.substring(0,12)+'\u2026':lbl}</div>
    </div>`).join('');
  document.querySelectorAll('.sp').forEach(el=>el.addEventListener('click',()=>{
    selState=el.dataset.st;buildStatePills();updateSV();
  }));
}
function updateSV(){
  const band=document.getElementById('svBand').value;
  let items=selState?DATA.filter(r=>r.state===selState):DATA;
  if(band) items=items.filter(r=>r.band===band);
  items=[...items].sort((a,b)=>{
    if(a.rank&&b.rank) return a.rank-b.rank;
    if(a.rank) return -1;if(b.rank) return 1;
    return a.name.localeCompare(b.name);
  });
  document.getElementById('svCount').textContent=
    `${items.length} institution${items.length!==1?'s':''}${selState?' \u00b7 '+selState:''}${band?' \u00b7 '+band:''}`;
  document.getElementById('svCards').innerHTML=items.map(r=>`
    <div class="top-card" style="padding:14px;gap:10px">
      <div style="font-size:1.4rem;font-weight:700;color:var(--orange);min-width:36px;line-height:1">${r.rank?'#'+r.rank:'\u2014'}</div>
      <div style="flex:1">
        <div style="font-weight:700;font-size:0.87rem;margin-bottom:3px">${r.name}</div>
        <div style="font-size:0.72rem;color:var(--muted);margin-bottom:5px">${r.city} &middot; ${getType(r.type)} ${getBand(r.band)}</div>
        ${r.score?`<div style="font-weight:700;color:var(--orange);font-size:1rem">${r.score.toFixed(2)}</div>`:''}
        <a class="tc-web" href="${r.url}" target="_blank">&#127760; Website</a>
      </div>
    </div>`).join('');
}

// ── CHARTS ──
const CI={};
function dc(id){if(CI[id]){CI[id].destroy();delete CI[id];}}
const COLS=['#FF6B00','#FF8C38','#FBBF24','#22D3A0','#2563EB','#A78BFA','#F43F5E','#06B6D4','#10B981','#EC4899','#1A4FAA','#F59E0B'];
const CD={
  plugins:{
    legend:{labels:{color:'rgba(232,237,248,0.55)',font:{size:11,family:'Arial'},boxWidth:12}},
    tooltip:{backgroundColor:'rgba(10,13,22,0.97)',titleColor:'#FF6B00',bodyColor:'rgba(232,237,248,0.8)',borderColor:'rgba(255,107,0,0.35)',borderWidth:1,padding:10}
  },
  scales:{
    x:{ticks:{color:'rgba(232,237,248,0.5)',font:{size:10,family:'Arial'}},grid:{color:'rgba(255,255,255,0.04)'},border:{color:'rgba(255,107,0,0.15)'}},
    y:{ticks:{color:'rgba(232,237,248,0.5)',font:{size:10,family:'Arial'}},grid:{color:'rgba(255,255,255,0.04)'},border:{color:'rgba(255,107,0,0.15)'}},
  },
  animation:{duration:400}
};

function drawAnalytics(){
  if(typeof Chart==='undefined') return;
  Chart.defaults.font.family='Arial';

  dc('top20Bar');
  const t20=DATA.filter(r=>r.rank&&r.rank<=20).sort((a,b)=>a.rank-b.rank);
  CI['top20Bar']=new Chart(document.getElementById('top20Bar'),{
    type:'bar',
    data:{
      labels:t20.map(r=>'#'+r.rank+' '+r.name.replace('Indian Institute of Technology','IIT').replace('National Institute of Technology','NIT').substring(0,22)),
      datasets:[{label:'NIRF Score',data:t20.map(r=>r.score||0),
        backgroundColor:t20.map((_,i)=>i===0?'#FFD700':i===1?'#C0C0C0':i===2?'#CD7F32':i<10?'#FF6B00':'rgba(255,107,0,0.6)'),
        borderColor:'rgba(255,255,255,0.1)',borderWidth:1,borderRadius:4}]
    },
    options:{...CD,indexAxis:'y',responsive:true,maintainAspectRatio:false,
      plugins:{...CD.plugins,legend:{display:false},tooltip:{...CD.plugins.tooltip,callbacks:{label:ctx=>' Score: '+ctx.parsed.x.toFixed(2)}}},
      scales:{x:{...CD.scales.x,min:40,max:92},y:{...CD.scales.y,ticks:{...CD.scales.y.ticks,font:{size:9,family:'Arial'}}}}
    }
  });

  dc('typeAvgBar');
  const am={};
  DATA.filter(r=>r.score).forEach(r=>{if(!am[r.type])am[r.type]=[];am[r.type].push(r.score);});
  const tps=['IIT','IISc','BITS','NIT','IIIT','University','Private','Govt'].filter(t=>am[t]);
  CI['typeAvgBar']=new Chart(document.getElementById('typeAvgBar'),{
    type:'bar',
    data:{labels:tps,datasets:[{label:'Avg Score',data:tps.map(t=>+(am[t].reduce((a,b)=>a+b,0)/am[t].length).toFixed(2)),backgroundColor:COLS,borderColor:'rgba(255,255,255,0.1)',borderWidth:1,borderRadius:4}]},
    options:{...CD,responsive:true,maintainAspectRatio:false,
      plugins:{...CD.plugins,legend:{display:false},tooltip:{...CD.plugins.tooltip,callbacks:{label:ctx=>' Avg: '+ctx.parsed.y.toFixed(2)}}},
      scales:{x:{...CD.scales.x},y:{...CD.scales.y,min:30,max:90}}
    }
  });

  dc('histBar');
  const scores=DATA.filter(r=>r.score).map(r=>r.score);
  const bins=[[40,50],[50,55],[55,60],[60,65],[65,70],[70,75],[75,80],[80,92]];
  CI['histBar']=new Chart(document.getElementById('histBar'),{
    type:'bar',
    data:{labels:bins.map(([lo,hi])=>lo+'\u2013'+hi),
      datasets:[{label:'Colleges',data:bins.map(([lo,hi])=>scores.filter(s=>s>=lo&&s<hi).length),
        backgroundColor:['#1A4FAA','#2563EB','#22D3A0','#FBBF24','#FF8C38','#FF6B00','#F59E0B','#FFD700'],
        borderColor:'rgba(255,255,255,0.1)',borderWidth:1,borderRadius:4}]
    },
    options:{...CD,responsive:true,maintainAspectRatio:false,
      plugins:{...CD.plugins,legend:{display:false}},
      scales:{
        x:{...CD.scales.x,title:{display:true,text:'Score Range',color:'rgba(255,255,255,0.4)',font:{size:10}}},
        y:{...CD.scales.y,title:{display:true,text:'Colleges',color:'rgba(255,255,255,0.4)',font:{size:10}}}
      }
    }
  });

  dc('state100Bar');
  const s100={};
  DATA.filter(r=>r.rank&&r.rank<=100).forEach(r=>s100[r.state]=(s100[r.state]||0)+1);
  const top12=Object.entries(s100).sort((a,b)=>b[1]-a[1]).slice(0,12);
  CI['state100Bar']=new Chart(document.getElementById('state100Bar'),{
    type:'bar',
    data:{labels:top12.map(s=>s[0]),datasets:[{label:'In Rank 1\u2013100',data:top12.map(s=>s[1]),backgroundColor:COLS,borderColor:'rgba(255,255,255,0.1)',borderWidth:1,borderRadius:4}]},
    options:{...CD,indexAxis:'y',responsive:true,maintainAspectRatio:false,
      plugins:{...CD.plugins,legend:{display:false}},
      scales:{x:{...CD.scales.x},y:{...CD.scales.y,ticks:{...CD.scales.y.ticks,font:{size:10,family:'Arial'}}}}
    }
  });

  dc('typeRangeBar');
  const scT=['IIT','NIT','BITS','IIIT','University','Private'];
  const scD=scT.map(t=>DATA.filter(r=>r.score&&r.type===t).map(r=>r.score));
  CI['typeRangeBar']=new Chart(document.getElementById('typeRangeBar'),{
    type:'bar',
    data:{labels:scT,datasets:[
      {label:'Min',data:scT.map((_,i)=>scD[i].length?Math.min(...scD[i]):0),backgroundColor:'rgba(37,99,235,0.55)',borderRadius:4,borderWidth:1},
      {label:'Avg',data:scT.map((_,i)=>{const v=scD[i];return v.length?+(v.reduce((a,b)=>a+b,0)/v.length).toFixed(1):0;}),backgroundColor:'rgba(255,107,0,0.8)',borderRadius:4,borderWidth:1},
      {label:'Max',data:scT.map((_,i)=>scD[i].length?Math.max(...scD[i]):0),backgroundColor:'rgba(251,191,36,0.7)',borderRadius:4,borderWidth:1},
    ]},
    options:{...CD,responsive:true,maintainAspectRatio:false,
      plugins:{...CD.plugins,legend:{...CD.plugins.legend,display:true,position:'top'}},
      scales:{x:{...CD.scales.x},y:{...CD.scales.y,min:30,max:92}}
    }
  });

  dc('typeDoughnut');
  const tc={};DATA.forEach(r=>tc[r.type]=(tc[r.type]||0)+1);
  const tkeys=Object.keys(tc).sort((a,b)=>tc[b]-tc[a]);
  CI['typeDoughnut']=new Chart(document.getElementById('typeDoughnut'),{
    type:'doughnut',
    data:{labels:tkeys,datasets:[{data:tkeys.map(k=>tc[k]),backgroundColor:COLS,borderColor:'#131825',borderWidth:2}]},
    options:{responsive:true,maintainAspectRatio:false,
      plugins:{legend:{labels:{color:'rgba(232,237,248,0.6)',font:{size:11,family:'Arial'},boxWidth:12}},
        tooltip:{backgroundColor:'rgba(10,13,22,0.97)',titleColor:'#FF6B00',bodyColor:'rgba(232,237,248,0.8)',borderColor:'rgba(255,107,0,0.35)',borderWidth:1,padding:10,
          callbacks:{label:ctx=>` ${ctx.label}: ${ctx.parsed} colleges`}}
      },animation:{duration:400}
    }
  });
}

function drawOverview(){
  if(typeof Chart==='undefined') return;
  Chart.defaults.font.family='Arial';
  const sc={};DATA.forEach(r=>sc[r.state]=(sc[r.state]||0)+1);
  const top12=Object.entries(sc).sort((a,b)=>b[1]-a[1]).slice(0,12);
  dc('stateChart');
  CI['stateChart']=new Chart(document.getElementById('stateChart'),{
    type:'bar',data:{labels:top12.map(s=>s[0]),datasets:[{label:'Colleges',data:top12.map(s=>s[1]),backgroundColor:COLS,borderRadius:4,borderWidth:1,borderColor:'rgba(255,255,255,0.1)'}]},
    options:{...CD,responsive:true,maintainAspectRatio:false,
      plugins:{...CD.plugins,legend:{display:false}},
      scales:{x:{...CD.scales.x,ticks:{...CD.scales.x.ticks,maxRotation:40,font:{size:9}}},y:{...CD.scales.y}}
    }
  });
  const tc={};DATA.forEach(r=>tc[r.type]=(tc[r.type]||0)+1);
  const tkeys=Object.keys(tc).sort((a,b)=>tc[b]-tc[a]);
  dc('typeChart');
  CI['typeChart']=new Chart(document.getElementById('typeChart'),{
    type:'doughnut',data:{labels:tkeys,datasets:[{data:tkeys.map(k=>tc[k]),backgroundColor:COLS,borderColor:'#131825',borderWidth:2}]},
    options:{responsive:true,maintainAspectRatio:false,
      plugins:{legend:{labels:{color:'rgba(232,237,248,0.55)',font:{size:10,family:'Arial'},boxWidth:10}},
        tooltip:{backgroundColor:'rgba(10,13,22,0.97)',titleColor:'#FF6B00',bodyColor:'rgba(232,237,248,0.8)',borderColor:'rgba(255,107,0,0.35)',borderWidth:1}
      },animation:{duration:400}
    }
  });
  const scores=DATA.filter(r=>r.score).map(r=>r.score);
  const bins=[[40,50],[50,55],[55,60],[60,65],[65,70],[70,75],[75,80],[80,92]];
  dc('scoreChart');
  CI['scoreChart']=new Chart(document.getElementById('scoreChart'),{
    type:'bar',data:{labels:bins.map(([lo,hi])=>lo+'\u2013'+hi),
      datasets:[{label:'Colleges',data:bins.map(([lo,hi])=>scores.filter(s=>s>=lo&&s<hi).length),
        backgroundColor:['#1A4FAA','#2563EB','#22D3A0','#FBBF24','#FF8C38','#FF6B00','#F59E0B','#FFD700'],
        borderRadius:4,borderWidth:1,borderColor:'rgba(255,255,255,0.1)'}]
    },
    options:{...CD,responsive:true,maintainAspectRatio:false,
      plugins:{...CD.plugins,legend:{display:false}},
      scales:{x:{...CD.scales.x,ticks:{...CD.scales.x.ticks,font:{size:9}}},y:{...CD.scales.y}}
    }
  });
  dc('top10Chart');
  const t10=DATA.filter(r=>r.rank&&r.rank<=10).sort((a,b)=>a.rank-b.rank);
  CI['top10Chart']=new Chart(document.getElementById('top10Chart'),{
    type:'bar',data:{
      labels:t10.map(r=>r.name.replace('Indian Institute of Technology','IIT').replace('National Institute of Technology','NIT').substring(0,22)),
      datasets:[{label:'NIRF Score',data:t10.map(r=>r.score||0),
        backgroundColor:t10.map((_,i)=>i===0?'#FFD700':i===1?'#C0C0C0':i===2?'#CD7F32':'#FF6B00'),
        borderRadius:4,borderWidth:1,borderColor:'rgba(255,255,255,0.1)'}]
    },
    options:{...CD,responsive:true,maintainAspectRatio:false,
      plugins:{...CD.plugins,legend:{display:false},tooltip:{...CD.plugins.tooltip,callbacks:{label:ctx=>' Score: '+ctx.parsed.y.toFixed(2)}}},
      scales:{x:{...CD.scales.x,ticks:{...CD.scales.x.ticks,maxRotation:35,font:{size:9}}},y:{...CD.scales.y,min:60,max:92}}
    }
  });
}

// ── NAV ──
function showSection(id){
  document.querySelectorAll('.section').forEach(s=>s.classList.remove('active'));
  document.querySelectorAll('.nav-btn').forEach(b=>b.classList.remove('active'));
  document.getElementById(id).classList.add('active');
  document.getElementById('nb-'+id).classList.add('active');
  const raf2=fn=>requestAnimationFrame(()=>requestAnimationFrame(fn));
  if(id==='analytics') raf2(drawAnalytics);
  if(id==='overview'||id==='top10') raf2(drawOverview);
  if(id==='statechart') raf2(()=>{redrawQuadrant();renderStateTable([...STATE_DATA]);});
  if(id==='stateview'){buildStatePills();updateSV();}
}

// ── INIT ──
window.addEventListener('DOMContentLoaded',()=>{
  const states=[...new Set(DATA.map(r=>r.state))].sort();
  document.getElementById('stateFilter').innerHTML='<option value="">All States</option>'+states.map(s=>`<option>${s}</option>`).join('');
  ['mainSearch','stateFilter','typeFilter','bandFilter','sortFilter'].forEach(id=>{
    document.getElementById(id).addEventListener(id==='mainSearch'?'input':'change',applyF);
  });
  document.getElementById('svBand').addEventListener('change',updateSV);
  applyF();
  const t5=DATA.filter(r=>r.rank&&r.rank<=5).sort((a,b)=>a.rank-b.rank);
  document.getElementById('top5Cards').innerHTML=t5.map((r,i)=>makeTopCard(r,i)).join('');
  const t10=DATA.filter(r=>r.rank&&r.rank<=10).sort((a,b)=>a.rank-b.rank);
  document.getElementById('top10Cards').innerHTML=t10.map((r,i)=>makeTopCard(r,i)).join('');
  const t11=DATA.filter(r=>r.rank&&r.rank>10&&r.rank<=20).sort((a,b)=>a.rank-b.rank);
  document.getElementById('top11Cards').innerHTML=t11.map((r,i)=>makeTopCard(r,i+10)).join('');
  buildCompareDrops();
  buildStatePills();
  requestAnimationFrame(()=>requestAnimationFrame(drawOverview));
});


;

	const heightObserver = new ResizeObserver(([{ contentRect }]) => {
		window.parent.postMessage({ action: 'iframeHeightUpdated', height: contentRect.height, id: 'z_WxKa' }, '*');
	});

	heightObserver.observe(document.documentElement);
