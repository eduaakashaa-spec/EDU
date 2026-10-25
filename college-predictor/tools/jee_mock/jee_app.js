(function(){
/* EduAakashaa JEE Main mock test centre. Same engine as the UCEED centre: timed mock and practice modes, confidence rating on every answer,
   negative-marking tracker and a report per attempt. Marking: +4 correct, -1 wrong, 0 blank, in both MCQ and numerical sections (JEE Main 2027). */
const CFG=Object.assign({dataPath:'data/',memberName:'',memberId:'',resultsEndpoint:''},window.EA_CONFIG||{});
const KEY='ea-jee-mock-v1'+(CFG.memberId?'-'+CFG.memberId:'');
const SUBJ={MATH:'Mathematics',PHY:'Physics',CHEM:'Chemistry'};
const SUBJ_SHORT={MATH:'Maths',PHY:'Physics',CHEM:'Chemistry'};
const CATS={CNQ:'Complex numbers & quadratics',SEQ:'Sequences & series',PNC:'Permutations, combinations & binomial',MAT:'Matrices & determinants',LCD:'Limits & derivatives',INT:'Integral calculus',DEQ:'Differential equations',COG:'Coordinate geometry',VEC:'Vectors & 3D geometry',STP:'Statistics & probability',TRG:'Trigonometry',SRF:'Sets, relations & functions',
 UNM:'Units & errors',KIN:'Kinematics',LOM:'Laws of motion',WEP:'Work, energy & power',ROT:'Rotational motion',GRA:'Gravitation',PMB:'Properties of matter',THM:'Thermodynamics (physics)',OSW:'Oscillations & waves',ELS:'Electrostatics',CUR:'Current electricity',MAG:'Magnetism & EMI',OPT:'Optics',DUA:'Modern physics',
 MOL:'Mole concept',ATS:'Atomic structure',BON:'Chemical bonding',THE:'Chemical thermodynamics',EQU:'Equilibrium & pH',RDX:'Redox & electrochemistry',CKN:'Chemical kinetics',SOL:'Solutions',PER:'Periodic properties',COO:'Coordination compounds',ORG:'General organic chemistry',HYD:'Hydrocarbons',HAL:'Haloalkanes',BIO:'Biomolecules'};
const CONF=[['G','Guess','var(--muted)'],['L','Low','var(--part)'],['M','Medium','var(--link)'],['H','High','var(--ok)']];
const CNAME={G:'Guess',L:'Low',M:'Medium',H:'High'};
const BREAK_EVEN=20; // +4 / -1: an attempt pays off only if it is right more than 1 time in 5
const S={view:'home',name:'',best:{},att:null,data:{},papers:null,rfilter:'all',palOpen:false};
function load(){try{const d=JSON.parse(localStorage.getItem(KEY)||'{}');S.name=d.name||CFG.memberName||'';S.best=d.best||{};S.att=d.att||null;}catch(e){}}
function save(){try{localStorage.setItem(KEY,JSON.stringify({name:S.name,best:S.best,att:S.att}));}catch(e){}}
const $=s=>document.querySelector(s);
const app=$('#app');
const esc=s=>String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const fmt=x=>{const v=Math.round(x*100)/100;return (Object.is(v,-0)?0:v).toString();};
const sign=x=>x>0?'+'+fmt(x):fmt(x).replace('-','−');
const hm=m=>m%60?`${Math.floor(m/60)} h ${m%60} min`:`${m/60} h`;
const clock=ms=>{ms=Math.max(0,ms);const t=Math.round(ms/1000),h=Math.floor(t/3600),m=Math.floor(t%3600/60),s=t%60;return `${h}:${String(m).padStart(2,'0')}:${String(s).padStart(2,'0')}`;};
const pctOf=(a,b)=>b?Math.round(a/b*100):null;
const meta=y=>(S.papers||[]).find(o=>String(o.y)===String(y));
const ttl=y=>{const o=meta(y);return o?o.title:String(y);};
const short=y=>{const o=meta(y);return o?(o.short||o.title):String(y);};
const LOGO='<svg width="28" height="28" viewBox="0 0 28 28" aria-hidden="true"><rect x="2" y="2" width="24" height="24" rx="6" fill="var(--navy)"/><path d="M8 19 L14 7 L20 19" fill="none" stroke="#FF6B0A" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/><path d="M10.6 14.6 H17.4" stroke="#fff" stroke-width="2.2" stroke-linecap="round"/></svg>';

/* ---------- scoring ---------- */
function secOf(D,n){return D.sections.find(s=>n>=s.lo&&n<=s.hi);}
function evaluate(D,q,a){
  const s=secOf(D,q.n);
  if(q.acc&&q.acc.bonus) return {st:'bonus',m:s.right};
  if(a==null||a==='') return {st:'blank',m:0};
  if(q.t==='NAT'){
    const v=parseFloat(String(a).replace('−','-'));
    if(isNaN(v)) return {st:'wrong',m:s.wrong};
    return q.acc.ranges.some(([lo,hi])=>v>=lo-1e-9&&v<=hi+1e-9)?{st:'right',m:s.right}:{st:'wrong',m:s.wrong};
  }
  return q.acc.sets.includes(a)?{st:'right',m:s.right}:{st:'wrong',m:s.wrong};
}
function results(D,ans){
  const per={},secs=D.sections.map(s=>({type:s.type,subj:s.subj,lo:s.lo,hi:s.hi,score:0,max:0,right:0,wrong:0,blank:0,gain:0,loss:0}));
  let total=0;
  for(const q of D.qs){
    const r=evaluate(D,q,ans[q.n]);per[q.n]=r;total+=r.m;
    const sc=secs.find(s=>q.n>=s.lo&&q.n<=s.hi);sc.score+=r.m;sc.max+=secOf(D,q.n).right;
    if(r.m>0)sc.gain+=r.m;else if(r.m<0)sc.loss+=-r.m;
    if(r.st==='right'||r.st==='bonus')sc.right++;else if(r.st==='wrong')sc.wrong++;else sc.blank++;
  }
  return {per,secs,total};
}
const showAns=(q,a)=>(a==null||a==='')?'—':String(a);
const officialAns=q=>q.acc&&q.acc.bonus?'Full marks to all':q.disp;
const keyReady=D=>D.qs.every(q=>q.acc);

/* ---------- data ---------- */
async function getIndex(){
  if(S.papers) return S.papers;
  const r=await fetch(`${CFG.dataPath}index.json`,{credentials:'same-origin'});
  if(!r.ok) throw new Error('index');
  S.papers=(await r.json()).papers;return S.papers;
}
async function getData(y){
  if(S.data[y]) return S.data[y];
  const r=await fetch(`${CFG.dataPath}${y}.json`,{credentials:'same-origin'});
  if(!r.ok) throw new Error('load');
  const d=await r.json();S.data[y]=d;return d;
}

/* ---------- views ---------- */
function mast(){return `<header class="mast"><div class="wrap"><button class="brand" data-act="home" aria-label="All papers">${LOGO}<span>Edu<b>Aakashaa</b></span></button><span class="tag">JEE Main mock tests · Members</span></div></header>`;}
function footer(){
  return `<footer class="wrap foot"><div><p>The EduAakashaa practice mocks are original questions written for practice in the JEE Main 2027 pattern (Paper 1, B.E./B.Tech.): 25 questions each in Mathematics, Physics and Chemistry, of which 20 are multiple-choice and 5 numerical, marked +4 for a correct answer and −1 for a wrong one in both sections. Every answer is computed, not guessed.</p><p>Previous-year papers are NTA question papers; each appears only after its official answer key has been added. Mock scores are practice guidance only. They do not predict your JEE Main score, percentile or rank, and one test is a snapshot of one day.</p></div><div><p>EduAakashaa, Coimbatore</p><p class="contact">+91 80157 22706<br>info@eduaakashaa.com<br>www.eduaakashaa.com</p></div></footer>`;
}
function paperCard(o){
  const b=S.best[o.y];const pct=b?Math.max(0,Math.min(100,b.score/o.max*100)):0;
  const chips=['MATH','PHY','CHEM'].map(k=>`<span class="chip mcq">${SUBJ_SHORT[k]} · 20 + 5</span>`).join('');
  if(!o.ready) return `<article class="yr pend"><div class="top"><span class="y">${esc(o.short||o.title)}</span><span class="fmt">${o.n} questions<br>${hm(o.mins)} · ${o.max} marks</span></div><div class="chips"><span class="chip">NTA paper</span></div><div class="best">Opens when the official answer key is added.</div><div class="acts"><button class="btn sec" disabled>Not yet available</button></div></article>`;
  return `<article class="yr"><div class="top"><span class="y">${esc(o.short||o.title)}</span><span class="fmt">${o.n} questions<br>${hm(o.mins)} · ${o.max} marks</span></div>
    <div class="chips">${o.kind==='mock'?'<span class="chip new">Original · 2027 pattern</span>':'<span class="chip new">NTA paper</span>'}${chips}<span class="chip">+4 / −1</span></div>
    <div><div class="best">${b?`Best timed mock: <b>${fmt(b.score)} / ${o.max}</b>`:'No timed mock yet'}</div><div class="bar" style="margin-top:6px"><i style="width:${pct}%"></i></div></div>
    <div class="acts"><button class="btn pri" data-act="start" data-y="${o.y}" data-mode="mock">Timed mock</button><button class="btn sec" data-act="start" data-y="${o.y}" data-mode="practice">Practise</button></div></article>`;
}
function renderHome(){
  S.view='home';
  const a=S.att;let resume='';
  if(a&&!a.done&&meta(a.y)){
    const left=a.mode==='mock'?` · ${clock(a.endAt-Date.now())} left`:'';
    resume=`<div class="resume"><p><b>Test in progress:</b> ${esc(ttl(a.y))} ${a.mode==='mock'?'timed mock':'practice'}${left}</p><div style="display:flex;gap:8px;flex-wrap:wrap"><button class="btn sec" data-act="discard">Discard</button><button class="btn hot" data-act="resume">Resume</button></div></div>`;
  }
  const mocks=(S.papers||[]).filter(o=>o.kind==='mock'),pyq=(S.papers||[]).filter(o=>o.kind==='pyq');
  app.innerHTML=mast()+`<main class="wrap">
  <section class="hero"><div><div class="eyebrow">JEE Main · Paper 1 (B.E./B.Tech.) · 2027 pattern</div><h1>Practise JEE Main <em>and know what each mark cost.</em></h1><p>Three-hour papers with 75 questions: Mathematics, Physics and Chemistry, each with 20 multiple-choice and 5 numerical questions. The marking is the real one, +4 and −1, so every wrong answer shows up as marks lost. After each test your report tracks negative marks, confidence and weak chapters.</p></div>
  <div class="member"><label for="mname">Your name</label><input id="mname" autocomplete="name" placeholder="e.g. Aisha Rahman" value="${esc(S.name)}"><small>Shown on your score card.</small></div></section>
  ${resume}
  <div class="modes"><div><h3>Timed mock</h3><p>Exam conditions: 3 hours, answers stay hidden, marked +4 / −1 when you submit. Move between subjects freely.</p></div><div><h3>Practice</h3><p>No clock. Check each answer as you go and read the working straight away.</p></div><div><h3>Review</h3><p>Rate your confidence on every answer. The report shows negative marks, avoidable losses on guesses and answers you were sure of but got wrong.</p></div></div>
  <div class="secthead"><h2>EduAakashaa practice mocks</h2><span>Five original papers, 75 questions each</span></div>
  <div class="years">${mocks.map(paperCard).join('')}</div>
  ${pyq.length?`<div class="secthead"><h2>Previous-year papers</h2><span>NTA JEE Main B.Tech papers, official answer keys</span></div><div class="years">${pyq.map(paperCard).join('')}</div>`:''}
  <div class="secthead"><h2>How negative marking works</h2><span>+4 for right, −1 for wrong, 0 for blank</span></div>
  <div class="pattern"><div class="insights" style="grid-template-columns:repeat(auto-fit,minmax(240px,1fr))">
   <div><b>Break-even is 1 in 5</b><p>An answer that is right more than 20% of the time adds marks on average. A blind guess in a 4-option question is right 25% of the time, so it is worth about +0.25 marks; a numerical guess is almost never right, so it costs about −1.</p></div>
   <div><b>Eliminate before guessing</b><p>Remove one option and a guess is worth about +0.67; remove two and it is worth +1.5. Guessing pays when you have narrowed it down, not when you have not read the question.</p></div>
   <div><b>Confident and wrong is the costly one</b><p>A −1 on an answer you were sure of points to a concept or a method to fix, and it will repeat in the real paper. Your report lists these first.</p></div>
   <div><b>Numerical questions have negative marks too</b><p>In JEE Main 2027 an incorrect numerical answer also loses 1 mark. Leave it blank unless you worked it through.</p></div>
  </div></div></main>`+footer();
  $('#mname').addEventListener('input',e=>{S.name=e.target.value.trim();save();});
}

function newAttempt(y,mode){
  const o=meta(y);
  S.att={y,mode,ans:{},mark:{},vis:{1:true},chk:{},conf:{},tm:{},cur:0,startAt:Date.now(),endAt:Date.now()+o.mins*60000,qstart:Date.now(),done:false};
  save();
}
async function openTest(){
  const a=S.att;S.view='test';S.palOpen=false;
  app.innerHTML=mast()+`<div class="loading">Loading ${esc(ttl(a.y))}…</div>`;
  try{await getData(a.y);}catch(e){app.innerHTML=mast()+`<div class="wrap loading">The ${esc(ttl(a.y))} paper did not load. Check your connection and try again.<br><br><button class="btn pri" data-act="resume">Try again</button></div>`;return;}
  a.qstart=Date.now();
  renderTest();
}
const D=()=>S.data[S.att.y];
const curQ=()=>D().qs[S.att.cur];
function stamp(){const a=S.att;if(!a||a.done||!S.data[a.y])return;const q=D().qs[a.cur];if(!q)return;a.tm=a.tm||{};const now=Date.now();a.tm[q.n]=(a.tm[q.n]||0)+Math.max(0,Math.min(now-(a.qstart||now),20*60000));a.qstart=now;}

function subjTabs(d,sec){
  const subs=[...new Set(d.sections.map(s=>s.subj))];
  return subs.map(k=>{const first=d.sections.find(s=>s.subj===k).lo;return `<button data-act="jump" data-n="${first}" aria-pressed="${sec.subj===k}">${SUBJ_SHORT[k]}</button>`;}).join('');
}
function renderTest(){
  const a=S.att,d=D(),q=curQ(),o=meta(a.y);
  const sec=secOf(d,q.n);const practice=a.mode==='practice';
  app.innerHTML=`<div class="tbar"><div class="wrap">
    <button class="btn ghost exit" data-act="home" title="Leave and continue later. Your answers are saved${practice?'':'; the timer keeps running'}." aria-label="Exit to all papers">‹ Exit</button>
    <div class="ttl">${esc(short(a.y))}<span class="md"> · ${practice?'Practice':'Timed mock'}</span><small>${esc(S.name||'Member')} · Paper 1 · ${o.n} questions</small></div>
    <div class="tabs" role="group" aria-label="Subjects">${subjTabs(d,sec)}</div>
    ${practice?`<span class="timer" id="timer" title="Time spent">${clock(Date.now()-a.startAt)}</span>`:`<span class="timer" id="timer" title="Time left">${clock(a.endAt-Date.now())}</span>`}
    <button class="btn sec palbtn" data-act="pal">Questions</button>
    <button class="btn hot" data-act="ask-submit">${practice?'Finish':'Submit'}</button>
  </div></div>
  <main class="wrap tgrid"><section class="qpane" id="qpane"></section><aside class="pal" id="pal" aria-label="Question palette"></aside></main><div class="scrim" id="scrim" data-act="pal"></div><div id="modal"></div>`;
  renderQ();renderPal();tick();
}
const markLabel=s=>`+${s.right} · −${Math.abs(s.wrong)}`;
const secName=s=>`${SUBJ_SHORT[s.subj]} · ${s.type==='MCQ'?'Section A (MCQ)':'Section B (numerical)'}`;
function renderQ(){
  const a=S.att,d=D(),q=curQ(),sec=secOf(d,q.n),val=a.ans[q.n];
  const practice=a.mode==='practice',checked=practice&&a.chk[q.n];
  let input='';
  if(q.t==='NAT'){
    input=`<div class="lab">Type your answer or use the keypad. Numbers only (a whole number is expected).</div><div class="natrow"><input id="natin" inputmode="decimal" autocomplete="off" aria-label="Your numerical answer" value="${esc(val||'')}" ${checked?'disabled':''}>
    <div class="pad" ${checked?'hidden':''}>${['7','8','9','⌫','4','5','6','−','1','2','3','.'].map(k=>`<button data-act="key" data-k="${k}">${k}</button>`).join('')}<button class="wide" data-act="key" data-k="0">0</button><button class="wide" data-act="key" data-k="C">Clear</button></div></div>`;
  }else{
    const right=checked?(q.acc.sets||[''])[0]:'';
    input=`<div class="lab">Select one option.</div><div class="opts" role="radiogroup">${'ABCD'.split('').map(c=>{
      const on=val&&val.includes(c);let cls='opt';
      if(checked){if(right.includes(c))cls+=' right';else if(on)cls+=' wrong';}
      return `<button class="${cls}" role="radio" aria-checked="${!!on}" data-act="opt" data-c="${c}" ${checked?'disabled':''}><span class="box"></span>${c}</button>`;}).join('')}</div>`;
  }
  let fb='',exp='';
  if(checked){
    const r=evaluate(d,q,val);
    const map={right:['ok','Correct'],bonus:['ok','Full marks to everyone for this question'],wrong:['bad','Not correct'],blank:['blank','Not answered']};
    const [c,t]=map[r.st];
    fb=`<div class="fb ${c}"><div class="v">${t} <span class="mono">${sign(r.m)}</span></div><div class="k">Official answer: ${esc(officialAns(q))}${val?` · Your answer: ${esc(showAns(q,val))}`:''}</div></div>`;
    exp=explain(q);
  }
  const last=a.cur===d.qs.length-1;
  const acts=practice?
    `<button class="btn sec" data-act="prev" ${a.cur?'':'disabled'}>Previous</button>${checked?'':`<button class="btn sec" data-act="clear">Clear</button>`}<span class="sp"></span>${checked?(last?`<button class="btn hot" data-act="ask-submit">Finish and see results</button>`:`<button class="btn pri" data-act="next">Next question</button>`):`<button class="btn sec" data-act="reveal">Show answer</button><button class="btn pri" data-act="check">Check answer</button>`}`:
    `<button class="btn sec" data-act="prev" ${a.cur?'':'disabled'}>Previous</button><button class="btn sec" data-act="clear">Clear response</button><span class="sp"></span><button class="btn sec" data-act="marknext">${a.mark[q.n]?'Unmark':'Mark for review'} &amp; next</button><button class="btn ${last?'hot':'pri'}" data-act="savenext">${last?'Save &amp; finish':'Save &amp; next'}</button>`;
  a.conf=a.conf||{};
  const hasAns=val!=null&&val!=='';const cv=a.conf[q.n];
  const conf=`<div class="confrow" role="group" aria-label="How sure are you?"><span class="cl">How sure are you?<small>${hasAns?(cv?'You can change this any time before submitting.':'Pick one so your report can track it.'):'Answer first, then rate your confidence.'}</small></span>${CONF.map(([k,l,c])=>`<button class="cf" data-act="conf" data-v="${k}" aria-pressed="${cv===k}" ${(!hasAns||checked)?'disabled':''}><span class="d" style="background:${c}"></span>${l}</button>`).join('')}</div>`;
  const warn=(!practice&&q.t==='NAT')?`<p class="negnote">A wrong numerical answer loses 1 mark. Leave it blank if you are not sure.</p>`:'';
  $('#qpane').innerHTML=`<div class="qhead"><h2>Question ${q.n}</h2><span class="chip ${q.t==='NAT'?'nat':'mcq'}">${secName(sec)}</span><span class="chip">${markLabel(sec)}</span>${a.mark[q.n]&&!practice?'<span class="chip" style="color:var(--mark)">Marked for review</span>':''}</div>
  ${qsheet(q,a.y,false)}
  <div class="ansbox">${input}${q.acc&&q.acc.bonus&&checked?'':conf}${fb}</div>${warn}${exp}<div class="qacts">${acts}</div>`;
  const ni=$('#natin');
  if(ni) ni.addEventListener('input',e=>{const v=e.target.value.replace(/[^0-9.\-−]/g,'');if(v!==e.target.value)e.target.value=v;setAns(v);syncConf(v);});
}
function syncConf(v){document.querySelectorAll('.cf').forEach(b=>b.disabled=!v);const h=document.querySelector('.confrow small');if(h)h.textContent=v?'Pick one so your report can track it.':'Answer first, then rate your confidence.';}
function qsheet(q,y,lazy){
  if(q.img) return `<div class="sheet"><img ${lazy?'loading="lazy" ':''}src="${q.img}" width="${q.w}" height="${q.h}" style="width:${Math.round(q.w*0.7)}px;max-width:100%" alt="${esc(ttl(y))} question ${q.n} as printed in the NTA paper"></div>`;
  let h=`<div class="sheet orig"><p class="stem">${q.stem}</p>`;
  if(q.fig) h+=`<div class="ofig">${q.fig}</div>`;
  if(q.opts) h+=`<div class="olist${q.layout==='grid'?' og':''}">${q.opts.map((o,i)=>`<div class="oi"><b>${'ABCD'[i]}</b><div>${o}</div></div>`).join('')}</div>`;
  return h+`</div>`;
}
function explain(q){
  if(!q.steps||!q.steps.length) return '';
  let h=`<div class="exp"><div class="h">How to solve it</div><ol>${q.steps.map(s=>`<li><span>${s}</span></li>`).join('')}</ol>`;
  if(q.note) h+=`<p>${q.note}</p>`;
  if(q.svg) h+=`<figure class="viz">${q.svg}</figure>`;
  if(q.trap) h+=`<div class="trap"><b>Common mistake</b>${q.trap}</div>`;
  return h+`</div>`;
}
function status(n){
  const a=S.att,has=a.ans[n]!=null&&a.ans[n]!=='';
  if(a.mode==='practice'){
    if(!a.chk[n]) return a.vis[n]?(has?'ans':'vis'):'';
    const r=evaluate(D(),D().qs.find(q=>q.n===n),a.ans[n]);
    return r.st==='right'||r.st==='bonus'?'pr-ok':r.st==='blank'?'vis':'pr-bad';
  }
  if(a.mark[n]) return has?'mk mkans':'mk';
  if(has) return 'ans';
  return a.vis[n]?'vis':'';
}
function renderPal(){
  const a=S.att,d=D(),cur=curQ().n,practice=a.mode==='practice';
  const c={ans:0,vis:0,mk:0,nv:0,ok:0,bad:0};
  for(const q of d.qs){const s=status(q.n);
    if(practice){if(s==='pr-ok')c.ok++;else if(s==='pr-bad')c.bad++;else c.nv++;}
    else if(s.startsWith('mk'))c.mk++;else if(s==='ans')c.ans++;else if(s==='vis')c.vis++;else c.nv++;}
  const counts=practice?
    `<span><i class="sw ans"></i>Correct <b>${c.ok}</b></span><span><i class="sw bad"></i>Wrong <b>${c.bad}</b></span><span><i class="sw"></i>Not checked <b>${c.nv}</b></span>`:
    `<span><i class="sw ans"></i>Answered <b>${c.ans}</b></span><span><i class="sw vis"></i>Not answered <b>${c.vis}</b></span><span><i class="sw mk"></i>Marked <b>${c.mk}</b></span><span><i class="sw"></i>Not visited <b>${c.nv}</b></span>`;
  $('#pal').innerHTML=`<h3>Question palette</h3><div class="counts">${counts}</div>${d.sections.map(s=>`<div class="psec"><div class="ph">${secName(s)} · Q${s.lo}–${s.hi}</div><div class="pgrid">${d.qs.filter(q=>q.n>=s.lo&&q.n<=s.hi).map(q=>`<button class="pq ${status(q.n)}${q.n===cur?' cur':''}" data-act="jump" data-n="${q.n}" aria-label="Question ${q.n}">${q.n}</button>`).join('')}</div></div>`).join('')}<button class="btn hot" data-act="ask-submit">${practice?'Finish and see results':'Submit test'}</button>`;
  $('#pal').classList.toggle('open',S.palOpen);$('#scrim').classList.toggle('open',S.palOpen);
}
function setAns(v){const a=S.att,q=curQ();a.conf=a.conf||{};if(v===''||v==null){delete a.ans[q.n];delete a.conf[q.n];}else a.ans[q.n]=v;save();renderPal();}
function go(i){stamp();const a=S.att,d=D();a.cur=Math.max(0,Math.min(d.qs.length-1,i));a.vis[d.qs[a.cur].n]=true;a.qstart=Date.now();S.palOpen=false;save();
  const sec=secOf(d,curQ().n);document.querySelectorAll('.tabs button').forEach(b=>{const first=d.sections.find(s=>s.subj===sec.subj).lo;b.setAttribute('aria-pressed',String(+b.dataset.n===first));});
  renderQ();renderPal();window.scrollTo({top:0,behavior:'instant'in window?'instant':'auto'});}

let timerId=null;
function tick(){
  clearInterval(timerId);
  timerId=setInterval(()=>{
    const a=S.att;if(S.view!=='test'||!a){clearInterval(timerId);return;}
    const el=$('#timer');if(!el)return;
    if(a.mode==='practice'){el.textContent=clock(Date.now()-a.startAt);return;}
    const left=a.endAt-Date.now();el.textContent=clock(left);el.classList.toggle('low',left<10*60000);
    if(left<=0){clearInterval(timerId);finish(true);}
  },1000);
}
function askSubmit(){
  const a=S.att,d=D();
  const answered=d.qs.filter(q=>a.ans[q.n]!=null&&a.ans[q.n]!=='').length;
  const practice=a.mode==='practice';
  const marked=practice?0:Object.keys(a.mark).length;
  const firstOpen=d.qs.find(q=>practice?!a.chk[q.n]:(a.ans[q.n]==null||a.ans[q.n]===''));
  a.conf=a.conf||{};
  const unrated=d.qs.filter(q=>a.ans[q.n]!=null&&a.ans[q.n]!==''&&!a.conf[q.n]);
  const left=practice?'':`<p>Time left: <b class="mono">${clock(a.endAt-Date.now())}</b></p>`;
  $('#modal').innerHTML=`<div class="modal" role="dialog" aria-modal="true" aria-labelledby="mt"><div class="card"><h3 id="mt">${practice?'Finish practice?':'Submit your test?'}</h3><p>You have answered <b>${answered}</b> of ${d.qs.length} questions${marked?`, with <b>${marked}</b> marked for review`:''}.</p>${left}<p>Each wrong answer costs 1 mark. Unanswered questions score 0.</p>${unrated.length?`<p class="need"><b>${unrated.length}</b> answered question${unrated.length>1?'s have':' has'} no confidence level and will be left out of the confidence report.</p>`:''}<p>${practice?'Questions you did not check count as not answered.':'You cannot change answers after submitting.'}</p><div class="row">${firstOpen?`<button class="btn sec" data-act="jumpopen" data-n="${firstOpen.n}">Go to Q${firstOpen.n} (${practice?'not checked':'unanswered'})</button>`:''}${unrated.length?`<button class="btn sec" data-act="jumpopen" data-n="${unrated[0].n}">Rate Q${unrated[0].n}</button>`:''}<button class="btn sec" data-act="close-modal">Keep going</button><button class="btn hot" data-act="submit">${practice?'Finish':'Submit'}</button></div></div></div>`;
}
function finish(auto){
  stamp();
  const a=S.att,d=D();
  const ans=a.mode==='practice'?Object.fromEntries(Object.entries(a.ans).filter(([n])=>a.chk[n])):a.ans;
  const r=results(d,ans);
  a.done=true;a.finishedAt=Math.min(Date.now(),a.mode==='mock'?a.endAt:Date.now());a.auto=!!auto;a.scored=ans;a.cscored=Object.fromEntries(Object.entries(a.conf||{}).filter(([n])=>ans[n]!=null&&ans[n]!==''));
  sendResult(a,d,r);
  if(a.mode==='mock'){const b=S.best[a.y];if(!b||r.total>b.score)S.best[a.y]={score:r.total,at:Date.now()};}
  save();clearInterval(timerId);
  const rk=d.qs.some(q=>a.cscored[q.n]==='H'&&r.per[q.n].st==='wrong');
  S.rfilter=rk?'risk':r.secs.some(s=>s.wrong)?'wrong':'all';
  renderResult();
}
function sendResult(a,d,r){
  if(!CFG.resultsEndpoint) return;
  const C=a.cscored||{},per={};
  for(const q of d.qs){const x=r.per[q.n];per[q.n]={type:q.t,subj:q.subj||secOf(d,q.n).subj,topic:q.cat||null,answer:a.scored[q.n]??null,official:q.disp,status:x.st,marks:x.m,confidence:C[q.n]||null,sec:Math.round(((a.tm||{})[q.n]||0)/1000)};}
  const body={memberId:CFG.memberId||null,name:S.name||null,paper:String(a.y),paperTitle:ttl(a.y),mode:a.mode,score:Math.round(r.total*100)/100,max:meta(a.y).max,
    sections:r.secs.map(s=>({type:s.type,subj:s.subj,score:Math.round(s.score*100)/100,max:s.max,right:s.right,wrong:s.wrong,blank:s.blank})),
    startedAt:new Date(a.startAt).toISOString(),finishedAt:new Date(a.finishedAt).toISOString(),autoSubmitted:!!a.auto,questions:per};
  a.sync='sending';
  fetch(CFG.resultsEndpoint,{method:'POST',headers:{'Content-Type':'application/json'},credentials:'include',keepalive:true,body:JSON.stringify(body)})
    .then(res=>{a.sync=res.ok?'saved':'failed';}).catch(()=>{a.sync='failed';})
    .finally(()=>{save();const el=document.getElementById('sync');if(el)el.textContent=syncText(a);});
}
const syncText=a=>a.sync==='saved'?' · saved to your member account':a.sync==='failed'?' · could not save to your account (kept on this device)':a.sync==='sending'?' · saving…':'';

function renderResult(){
  S.view='result';
  const a=S.att,d=D(),o=meta(a.y),r=results(d,a.scored||{});
  const tot=r.secs.reduce((t,s)=>({right:t.right+s.right,wrong:t.wrong+s.wrong,blank:t.blank+s.blank,gain:t.gain+s.gain,loss:t.loss+s.loss}),{right:0,wrong:0,blank:0,gain:0,loss:0});
  const attempted=tot.right+tot.wrong,acc=attempted?Math.round(tot.right/attempted*100):0;
  const used=clock(a.finishedAt-a.startAt);
  const bySubj={};for(const s of r.secs){const b=bySubj[s.subj]||(bySubj[s.subj]={score:0,max:0,right:0,wrong:0,blank:0,gain:0,loss:0});for(const k of ['score','max','right','wrong','blank','gain','loss'])b[k]+=s[k];}
  const subjCards=Object.keys(bySubj).map(k=>{const s=bySubj[k],n=s.right+s.wrong+s.blank;const W=x=>(x/n*100).toFixed(2)+'%';
    return `<div class="rsec"><div class="eyebrow">${SUBJ[k]}</div><div class="n" style="margin-top:6px">${fmt(s.score)} <small>/ ${s.max}</small></div>
    <div class="stack" aria-hidden="true"><i style="width:${W(s.right)};background:var(--ok)"></i><i style="width:${W(s.wrong)};background:var(--bad)"></i></div>
    <div class="legend"><span><i class="sw ans"></i>${s.right} right</span><span><i class="sw bad"></i>${s.wrong} wrong</span><span><i class="sw"></i>${s.blank} blank</span></div></div>`;}).join('');
  const C=a.cscored||{};
  const riskN=d.qs.filter(q=>C[q.n]==='H'&&r.per[q.n].st==='wrong').length;
  const F=[['all','All',d.qs.length],['risk','Sure but wrong',riskN],['wrong','Wrong',tot.wrong],['blank','Not answered',tot.blank],['right','Correct',tot.right]].filter(f=>f[0]!=='risk'||f[2]);
  app.innerHTML=mast()+`<main class="wrap">
   <section class="rhero"><div><div class="eyebrow">Score card · ${esc(ttl(a.y))} · ${a.mode==='mock'?'Timed mock':'Practice'}</div>
   <div class="score" style="margin-top:10px">${fmt(r.total)} <small>/ ${o.max}</small></div>
   <div class="rmeta">${esc(S.name||'Member')} · ${attempted} attempted · ${acc}% of attempts correct · time used <span class="mono">${used}</span>${a.auto?' · submitted when time ran out':''}<span id="sync">${syncText(a)}</span></div></div>
   <div style="display:flex;gap:8px;flex-wrap:wrap"><button class="btn sec" data-act="home">All papers</button><button class="btn pri" data-act="start" data-y="${a.y}" data-mode="${a.mode}">Try again</button></div></section>
   <div class="rsecs">${subjCards}</div>
   ${negPanel(d,r,bySubj,tot)}
   ${confPanel(d,r)}
   ${topicPanel(d,r)}
   <div class="secthead"><h2>Review answers</h2><span>Open any question to see the official answer and how to solve it</span></div>
   <div class="filters" role="group" aria-label="Filter questions">${F.map(f=>`<button data-act="rf" data-f="${f[0]}" aria-pressed="${S.rfilter===f[0]}">${f[1]} <span class="mono">${f[2]}</span></button>`).join('')}</div>
   <div class="rlist" id="rlist"></div></main>`+footer();
  renderReview(r);
}

/* Negative marking tracker: where marks were lost, which of those losses were avoidable, and what guessing really did. */
function negPanel(d,r,bySubj,tot){
  const a=S.att,C=a.cscored||{};
  const wrongQs=d.qs.filter(q=>r.per[q.n].st==='wrong');
  const ev=p=>Math.round((4*p-(1-p))*100)/100;
  const avoid=wrongQs.filter(q=>C[q.n]==='G'||C[q.n]==='L');
  const unr=wrongQs.filter(q=>!C[q.n]);
  const sure=wrongQs.filter(q=>C[q.n]==='H');
  const gl=d.qs.filter(q=>(C[q.n]==='G'||C[q.n]==='L')&&r.per[q.n].st!=='blank');
  const glNet=gl.reduce((t,q)=>t+r.per[q.n].m,0);
  const glRight=gl.filter(q=>r.per[q.n].st==='right').length;
  const avoidLoss=avoid.length; // each wrong costs 1
  const natWrong=wrongQs.filter(q=>q.t==='NAT').length,mcqWrong=wrongQs.length-natWrong;
  const subjRows=Object.keys(bySubj).map(k=>{const s=bySubj[k],att=s.right+s.wrong,ac=att?Math.round(s.right/att*100):null;
    return `<tr><td>${SUBJ[k]}</td><td class="num">${att}</td><td class="num">${s.right}</td><td class="num">${s.wrong}</td><td class="num">${ac===null?'—':ac+'%'}</td><td class="num pos">${sign(s.gain)}</td><td class="num neg">${s.loss?'−'+fmt(s.loss):'0'}</td><td class="num"><b>${sign(s.score)}</b></td></tr>`;}).join('');
  const levelRows=[...CONF].reverse().map(([k,l,c])=>{const qs=d.qs.filter(q=>C[q.n]===k&&r.per[q.n].st!=='blank');const rt=qs.filter(q=>r.per[q.n].st==='right').length;const p=qs.length?rt/qs.length:null;const net=qs.reduce((t,q)=>t+r.per[q.n].m,0);
    const verdict=p===null?'':p*100>BREAK_EVEN?'above break-even':p*100<BREAK_EVEN?'below break-even':'at break-even';
    return `<tr><td><span class="d" style="display:inline-block;width:8px;height:8px;border-radius:50%;background:${c};margin-right:6px"></span>${l}</td><td class="num">${qs.length}</td><td class="num">${rt}</td><td class="num">${p===null?'—':Math.round(p*100)+'%'}</td><td class="num">${p===null?'—':sign(ev(p))}</td><td class="num"><b>${qs.length?sign(net):'—'}</b></td><td>${verdict}</td></tr>`;}).join('');
  const notes=[];
  if(!wrongQs.length) notes.push('No wrong answers, so nothing was lost to negative marking. Check that you also attempted enough questions.');
  else{
    notes.push(`You lost <b>${tot.loss}</b> mark${tot.loss===1?'':'s'} to ${wrongQs.length} wrong answer${wrongQs.length===1?'':'s'} (${mcqWrong} multiple-choice, ${natWrong} numerical).`);
    if(avoid.length) notes.push(`<b>${avoid.length}</b> of them were answers you rated Guess or Low. Leaving those blank would have saved ${avoidLoss} mark${avoidLoss===1?'':'s'}, but your ${gl.length} Guess/Low answers together scored <b>${sign(glNet)}</b> (${glRight} right), so ${glNet>0?'guessing helped overall: keep it for questions where you can rule out at least one option':glNet<0?'guessing cost you overall: skip questions where you cannot rule out two options':'guessing broke even'}.`);
    if(sure.length) notes.push(`<b>${sure.length}</b> were answers you rated High. These are concept or method errors, not bad luck: fix them first.`);
    if(unr.length) notes.push(`${unr.length} wrong answer${unr.length===1?' has':'s have'} no confidence rating, so ${unr.length===1?'it is':'they are'} left out of the split above.`);
    if(natWrong>=2) notes.push(`Numerical questions are not multiple-choice, so there is no lucky guess: ${natWrong} wrong numerical answers cost ${natWrong} marks. Attempt a numerical question only after checking the working.`);
  }
  const note=`<ul class="negnotes">${notes.map(x=>`<li>${x}</li>`).join('')}</ul>`;
  const hasCats=false;
  return `<section class="cpanel negpanel"><h3>Negative marking tracker</h3>
  <p class="lead">Marking is +4 for a correct answer, −1 for a wrong one and 0 for a blank. An answer adds marks on average only if it is right more than ${BREAK_EVEN}% of the time.</p>
  <div class="ctiles"><div class="ctile"><div class="lv">Marks gained</div><div class="big pos">${sign(tot.gain)}</div><div class="sub">${tot.right} correct answer${tot.right===1?'':'s'}</div></div>
    <div class="ctile"><div class="lv">Marks lost</div><div class="big neg">${tot.loss?'−'+fmt(tot.loss):'0'}</div><div class="sub">${tot.wrong} wrong answer${tot.wrong===1?'':'s'}</div></div>
    <div class="ctile"><div class="lv">Net score</div><div class="big">${sign(r.total)}</div><div class="sub">${pctOf(tot.loss,tot.gain)===null?'':fmt(pctOf(tot.loss,tot.gain))+'% of gains given back'}</div></div>
    <div class="ctile"><div class="lv">Avoidable loss</div><div class="big neg">${avoidLoss?'−'+avoidLoss:'0'}</div><div class="sub">wrong answers rated Guess or Low</div></div></div>
  <div class="scroll"><table class="ntab"><thead><tr><th>Subject</th><th>Attempted</th><th>Right</th><th>Wrong</th><th>Accuracy</th><th>Gained</th><th>Lost</th><th>Net</th></tr></thead><tbody>${subjRows}</tbody></table></div>
  <h4 style="margin:18px 0 6px">Is it worth attempting? By your confidence</h4>
  <div class="scroll"><table class="ntab"><thead><tr><th>Rated</th><th>Attempted</th><th>Right</th><th>Accuracy</th><th>Average per answer</th><th>Net marks</th><th></th></tr></thead><tbody>${levelRows}</tbody></table></div>
  <p class="sm">Average per answer = 4 × accuracy − 1 × (1 − accuracy). It is positive only above ${BREAK_EVEN}%.</p>
  ${note}</section>`;
}
function confPanel(d,r){
  const a=S.att,ans=a.scored||{},C=a.cscored||{};
  const answered=d.qs.filter(q=>ans[q.n]!=null&&ans[q.n]!=='');
  if(!answered.length) return '';
  const rated=answered.filter(q=>C[q.n]);
  const st={};for(const [k] of CONF) st[k]={n:0,right:0,wrong:0,gain:0,loss:0,qs:[]};
  for(const q of rated){const x=r.per[q.n],s=st[C[q.n]];s.n++;s.qs.push(q);if(x.st==='right'||x.st==='bonus')s.right++;else s.wrong++;if(x.m>0)s.gain+=x.m;else s.loss+=x.m;}
  const pct=s=>s.n?Math.round(s.right/s.n*100):null;
  if(!rated.length) return `<section class="cpanel"><h3>Confidence analysis</h3><p class="lead">No confidence levels were recorded in this attempt. Next time, tap Guess, Low, Medium or High after each answer to see where your marks come from and where you are at risk.</p></section>`;
  const tiles=[...CONF].reverse().map(([k,l,c])=>{const s=st[k],p=pct(s);const net=s.gain+s.loss;
    return `<div class="ctile"><div class="lv"><span class="d" style="display:inline-block;width:8px;height:8px;border-radius:50%;background:${c};margin-right:6px"></span>${l}</div><div class="big">${s.n} <small>answer${s.n===1?'':'s'}</small></div>
    <div class="sub">${s.n?`${p}% right · net <b class="mono" style="color:${net>0?'var(--ok)':net<0?'var(--bad)':'var(--muted)'}">${sign(net)}</b>`:'Not used'}</div><div class="acc"><i style="width:${p||0}%;background:${c}"></i></div></div>`;}).join('');
  const risk=st.H.qs.filter(q=>r.per[q.n].st==='wrong');
  const rt={};risk.forEach(q=>{const k=q.cat||q.subj;if(k)rt[k]=(rt[k]||0)+1;});
  const rname=k=>CATS[k]||SUBJ[k]||k;
  const rtop=Object.entries(rt).sort((x,y)=>y[1]-x[1]).slice(0,2).map(([k,v])=>`${rname(k)} (${v})`);
  const riskBox=`<div class="cbox risk"><div class="t">Sure but wrong · at risk</div><div class="n">${risk.length}</div>
    <p>${risk.length?`High-confidence answers that were wrong. Each cost you 5 marks compared with getting it right (the 4 you missed plus the 1 deducted). Being sure and wrong usually means a concept or method was learnt incorrectly, so these come first in revision.${rtop.length?` Most are in ${rtop.join(' and ')}.`:''}`:(st.H.n?`All ${st.H.n} high-confidence answers were right. Your sense of what you know is reliable.`:'You did not mark any answer as High.')}</p>
    ${risk.length?`<div class="qchips">${risk.map(q=>`<button data-act="riskjump" data-n="${q.n}" title="${esc(CATS[q.cat]||'')}">Q${q.n}</button>`).join('')}</div>`:''}</div>`;
  const lowqs=[...st.L.qs,...st.G.qs];
  const lt={};lowqs.forEach(q=>{const k=q.cat||q.subj;if(k)lt[k]=(lt[k]||0)+1;});
  const ltop=Object.entries(lt).sort((x,y)=>y[1]-x[1]).filter(x=>x[1]>=2).slice(0,3).map(([k,v])=>`${rname(k)} (${v})`);
  const lowBox=`<div class="cbox low"><div class="t">Low-confidence zones</div><div class="n">${lowqs.length}</div><p>${lowqs.length?`Answers marked Low or Guess. ${ltop.length?`They cluster in <b>${ltop.join(', ')}</b>. These need practice to turn doubt into certainty.`:'They are spread across topics.'}`:'No answers were marked Low or Guess.'}</p></div>`;
  const pH=pct(st.H),pM=pct(st.M),pL=pct(st.L),pG=pct(st.G);
  const seq=[['High',pH],['Medium',pM],['Low',pL],['Guess',pG]].filter(x=>x[1]!==null);
  let calib='';
  if(seq.length>=2){const ordered=seq.every((x,i)=>i===0||seq[i-1][1]>=x[1]);
    calib=`<div class="calib"><b>Is your confidence accurate?</b> Right by level: ${seq.map(x=>`${x[0]} ${x[1]}%`).join(' · ')}.<p class="note">${ordered?'Your accuracy rises with your confidence, which is what we want to see.':'Your accuracy does not rise steadily with confidence. Some answers you felt unsure about were right and some you felt sure about were wrong, so trust a method you can explain rather than a gut feeling.'}</p></div>`;}
  const unr=answered.length-rated.length;
  return `<section class="cpanel"><h3>Confidence analysis</h3><p class="lead">Based on the confidence you chose for ${rated.length} of your ${answered.length} answers${unr?` (${unr} without a rating ${unr===1?'is':'are'} left out)`:''}.</p>
  <div class="ctiles">${tiles}</div><div class="cgrid">${riskBox}${lowBox}</div>${calib}</section>`;
}
function topicPanel(d,r){
  if(!d.qs.some(q=>q.cat)) return '';
  const T={};
  for(const q of d.qs){if(!q.cat)continue;const t=T[q.cat]||(T[q.cat]={n:0,right:0,wrong:0,score:0,max:0,subj:q.subj});t.n++;t.max+=secOf(d,q.n).right;const x=r.per[q.n];t.score+=x.m;if(x.st==='right'||x.st==='bonus')t.right++;else if(x.st==='wrong')t.wrong++;}
  const rows=Object.entries(T).map(([k,t])=>({k,...t,p:t.max?Math.max(0,t.score)/t.max:0})).sort((a,b)=>a.p-b.p);
  const weak=rows.filter(x=>x.n>=2).slice(0,3).map(x=>CATS[x.k]);
  const col=p=>p>=0.6?'var(--ok)':p>=0.35?'var(--part)':'var(--bad)';
  return `<section class="topics"><h3>Score by chapter</h3><p class="focus">${weak.length?`Focus next on <b>${weak.join('</b>, <b>')}</b>.`:''} Weakest chapters first. Chapters with a single question are a thin sample.</p>
  ${rows.map(x=>`<div class="trow"><span>${CATS[x.k]||x.k} <span class="mono" style="color:var(--muted);font-size:12px">· ${SUBJ_SHORT[x.subj]||''} · ${x.right}/${x.n} right${x.wrong?`, ${x.wrong} wrong`:''}</span></span><span class="tb"><i style="width:${(x.p*100).toFixed(1)}%;background:${col(x.p)}"></i></span><span class="tv">${fmt(x.score)} / ${x.max}</span></div>`).join('')}</section>`;
}
function renderReview(r){
  const a=S.att,d=D();r=r||results(d,a.scored||{});
  const ans=a.scored||{},f=S.rfilter,C=a.cscored||{};
  const isRisk=q=>C[q.n]==='H'&&r.per[q.n].st==='wrong';
  const list=d.qs.filter(q=>{const s=r.per[q.n].st;return f==='all'||(f==='risk'?isRisk(q):f==='right'?(s==='right'||s==='bonus'):s===f);});
  $('#rlist').innerHTML=list.length?list.map(q=>{const x=r.per[q.n];const cls=x.m>0?'pos':x.m<0?'neg':'zero';const tsec=(a.tm||{})[q.n];
    return `<details class="ritem${isRisk(q)?' risk':''}" id="rq${q.n}"><summary><span class="qn">Q${q.n}${C[q.n]?`<span class="cchip ${C[q.n]}" title="Your confidence">${CNAME[C[q.n]]}</span>`:''}</span><span class="chip ${q.t==='NAT'?'nat':'mcq'} ty">${q.t==='NAT'?'NUM':'MCQ'}</span><span class="val"><span class="lbl">You</span>${esc(showAns(q,ans[q.n]))}</span><span class="val"><span class="lbl">Official</span>${esc(officialAns(q))}</span><span class="mk ${cls}">${x.st==='blank'?'0':sign(x.m)}</span></summary>
    <div class="body"><p class="rcat">${SUBJ[q.subj||secOf(d,q.n).subj]}${q.cat?' · '+(CATS[q.cat]||q.cat):''}${tsec?` · ${Math.round(tsec/6)/10} min spent`:''}</p>${qsheet(q,a.y,true)}${explain(q)}</div></details>`;}).join(''):`<div class="empty">No questions in this group.</div>`;
}

/* ---------- events ---------- */
document.addEventListener('click',async e=>{
  const t=e.target.closest('[data-act]');if(!t)return;
  const act=t.dataset.act,a=S.att;
  switch(act){
    case 'home': if(S.view==='test'){stamp();S.view='home';clearInterval(timerId);} renderHome();window.scrollTo(0,0);break;
    case 'start': newAttempt(t.dataset.y,t.dataset.mode);await openTest();window.scrollTo(0,0);break;
    case 'resume': if(a)a.qstart=Date.now();await openTest();break;
    case 'discard': S.att=null;save();renderHome();break;
    case 'jump': go(D().qs.findIndex(q=>q.n===+t.dataset.n));break;
    case 'prev': go(a.cur-1);break;
    case 'next': go(a.cur+1);break;
    case 'savenext': if(a.cur<D().qs.length-1)go(a.cur+1);else{renderPal();askSubmit();}break;
    case 'marknext': {const n=curQ().n;if(a.mark[n])delete a.mark[n];else a.mark[n]=true;save();if(a.cur<D().qs.length-1)go(a.cur+1);else{renderQ();renderPal();askSubmit();}break;}
    case 'clear': setAns('');renderQ();break;
    case 'conf': {a.conf=a.conf||{};const n=curQ().n;if(a.conf[n]===t.dataset.v)delete a.conf[n];else a.conf[n]=t.dataset.v;save();document.querySelectorAll('.cf').forEach(b=>b.setAttribute('aria-pressed',String(a.conf[n]===b.dataset.v)));break;}
    case 'riskjump': {const q=document.querySelector(`#rq${t.dataset.n}`);if(q){q.open=true;q.scrollIntoView({behavior:'smooth',block:'start'});}break;}
    case 'opt': {const q=curQ(),c=t.dataset.c;let v=a.ans[q.n]||'';v=v===c?'':c;setAns(v);renderQ();break;}
    case 'key': {const k=t.dataset.k,inp=$('#natin');let v=inp.value;
      if(k==='⌫')v=v.slice(0,-1);else if(k==='C')v='';else if(k==='−'){v=v.startsWith('-')?v.slice(1):'-'+v;}else if(k==='.'){if(!v.includes('.'))v+=(v===''||v==='-'?'0.':'.');}else v+=k;
      inp.value=v;setAns(v);syncConf(v);break;}
    case 'check': a.chk[curQ().n]=true;save();renderQ();renderPal();break;
    case 'reveal': a.chk[curQ().n]=true;save();renderQ();renderPal();break;
    case 'pal': S.palOpen=!S.palOpen;renderPal();break;
    case 'ask-submit': askSubmit();break;
    case 'jumpopen': $('#modal').innerHTML='';go(D().qs.findIndex(q=>q.n===+t.dataset.n));break;
    case 'close-modal': $('#modal').innerHTML='';break;
    case 'submit': $('#modal').innerHTML='';finish(false);window.scrollTo(0,0);break;
    case 'rf': S.rfilter=t.dataset.f;document.querySelectorAll('.filters button').forEach(b=>b.setAttribute('aria-pressed',String(b===t)));renderReview();break;
  }
});
document.addEventListener('keydown',e=>{if(e.key==='Escape'){if($('#modal')&&$('#modal').innerHTML){$('#modal').innerHTML='';}else if(S.palOpen){S.palOpen=false;renderPal();}}});

load();
app.innerHTML=mast()+'<div class="loading">Loading the papers…</div>';
getIndex().then(()=>{
  if(S.att&&!S.att.done&&S.att.mode==='mock'&&S.att.endAt<Date.now()&&meta(S.att.y)){getData(S.att.y).then(()=>{finish(true);}).catch(()=>renderHome());renderHome();}
  else renderHome();
}).catch(()=>{app.innerHTML=mast()+'<div class="wrap loading">The paper list did not load. Check your connection and refresh the page.</div>';});
})();
