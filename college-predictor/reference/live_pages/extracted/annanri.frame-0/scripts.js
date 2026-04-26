
const DB=[
  {campus:"CEG",branch:"Computer Science & Engineering",degree:"B.E.",closing:194.75},
  {campus:"CEG",branch:"Electronics & Communication Engineering",degree:"B.E.",closing:192.50},
  {campus:"CEG",branch:"Electrical & Electronics Engineering",degree:"B.E.",closing:176.50},
  {campus:"CEG",branch:"Mechanical Engineering",degree:"B.E.",closing:185.50},
  {campus:"CEG",branch:"Civil Engineering",degree:"B.E.",closing:158.50},
  {campus:"CEG",branch:"Information Technology",degree:"B.E.",closing:187.00},
  {campus:"CEG",branch:"Geo-Informatics",degree:"B.E.",closing:165.00},
  {campus:"CEG",branch:"Industrial Engineering",degree:"B.E.",closing:163.00},
  {campus:"CEG",branch:"Bio-Medical Engineering",degree:"B.E.",closing:168.00},
  {campus:"CEG",branch:"Agricultural & Irrigation Engineering",degree:"B.E.",closing:140.00},
  {campus:"CEG",branch:"Materials Science & Engineering",degree:"B.E.",closing:131.00},
  {campus:"CEG",branch:"Mining Engineering",degree:"B.E.",closing:126.00},
  {campus:"MIT",branch:"Computer Science & Engineering",degree:"B.E.",closing:185.00},
  {campus:"MIT",branch:"Electronics & Communication Engineering",degree:"B.E.",closing:182.00},
  {campus:"MIT",branch:"Aeronautical Engineering",degree:"B.E.",closing:178.00},
  {campus:"MIT",branch:"Automobile Engineering",degree:"B.E.",closing:170.00},
  {campus:"MIT",branch:"Electronics & Instrumentation Engineering",degree:"B.E.",closing:168.50},
  {campus:"MIT",branch:"Information Technology",degree:"B.E.",closing:175.50},
  {campus:"MIT",branch:"Manufacturing Engineering",degree:"B.E.",closing:158.00},
  {campus:"MIT",branch:"Rubber & Plastics Technology",degree:"B.Tech.",closing:142.00},
  {campus:"ACT",branch:"Chemical Engineering",degree:"B.Tech.",closing:162.00},
  {campus:"ACT",branch:"Industrial Biotechnology",degree:"B.Tech.",closing:158.00},
  {campus:"ACT",branch:"Pharmaceutical Technology",degree:"B.Tech.",closing:155.00},
  {campus:"ACT",branch:"Polymer Technology",degree:"B.Tech.",closing:150.00},
  {campus:"ACT",branch:"Textile Technology",degree:"B.Tech.",closing:138.00},
  {campus:"ACT",branch:"Leather Technology",degree:"B.Tech.",closing:130.00},
  {campus:"SAP",branch:"Architecture",degree:"B.Arch.",closing:175.00},
  {campus:"SAP",branch:"Planning",degree:"B.Plan.",closing:162.00},
  {campus:"UCE",branch:"Computer Science & Engineering",degree:"B.E.",closing:172.00},
  {campus:"UCE",branch:"Electronics & Communication Engineering",degree:"B.E.",closing:165.00},
  {campus:"UCE",branch:"Electrical & Electronics Engineering",degree:"B.E.",closing:155.00},
  {campus:"UCE",branch:"Mechanical Engineering",degree:"B.E.",closing:150.00},
  {campus:"UCE",branch:"Civil Engineering",degree:"B.E.",closing:138.00}
];
const CL={CEG:"CEG – College of Engineering, Guindy",MIT:"MIT – Madras Inst. of Technology, Chromepet",ACT:"ACT – Alagappa College of Technology, Guindy",SAP:"SAP – School of Architecture & Planning",UCE:"UCE – University College of Engineering, Trichy"};
const BC={CEG:"ceg",MIT:"mit",ACT:"act",SAP:"sap",UCE:"uce"};
function filterCampus(c,btn){document.querySelectorAll(".campus-pill").forEach(b=>b.classList.remove("active"));btn.classList.add("active");let n=0;document.querySelectorAll("#tbody tr").forEach(r=>{const s=c==="ALL"||r.dataset.campus===c;r.style.display=s?"":"none";if(s)n++;});document.getElementById("tcount").textContent="Showing "+n+" entries";}
function filterTable(inp){const q=inp.value.toLowerCase();let n=0;document.querySelectorAll("#tbody tr").forEach(r=>{const s=r.textContent.toLowerCase().includes(q);r.style.display=s?"":"none";if(s)n++;});document.getElementById("tcount").textContent="Showing "+n+" entries";}
function calcCutoff(){const m=Math.max(0,Math.min(200,parseFloat(document.getElementById("math-n").value)||0));const p=Math.max(0,Math.min(200,parseFloat(document.getElementById("phy-n").value)||0));const c=Math.max(0,Math.min(200,parseFloat(document.getElementById("chem-n").value)||0));const mc=m/2,pc=p/4,cc=c/4,cut=mc+pc+cc;document.getElementById("cutoff-display").textContent=cut.toFixed(2);document.getElementById("cutoff-bar").style.width=(cut/200*100).toFixed(2)+"%";document.getElementById("mc").textContent=mc.toFixed(2);document.getElementById("pc").textContent=pc.toFixed(2);document.getElementById("cc").textContent=cc.toFixed(2);const b=document.getElementById("band");if(cut>=193){b.textContent="Outstanding — CEG CSE, ECE top NRI seats within reach";b.style.color="#0d4f3c";}else if(cut>=180){b.textContent="Excellent — CEG, MIT most branches accessible";b.style.color="var(--success)";}else if(cut>=163){b.textContent="Good — MIT, ACT, UCE-T branches likely accessible";b.style.color="#0284c7";}else if(cut>=138){b.textContent="Average — ACT and UCE-T lower-demand branches";b.style.color="var(--warn)";}else{b.textContent="Below Average — Limited NRI options at AU campuses";b.style.color="var(--danger)";}}
function syncScore(id){const r=document.getElementById(id+"-r"),n=document.getElementById(id+"-n");n.value=r.value;r.style.setProperty("--val",(r.value/2)+"%");calcCutoff();}
function syncRange(id){const r=document.getElementById(id+"-r"),n=document.getElementById(id+"-n");let v=Math.max(0,Math.min(200,parseInt(n.value)||0));n.value=v;r.value=v;r.style.setProperty("--val",(v/2)+"%");calcCutoff();}
calcCutoff();
function goToPredictor(){document.getElementById("pred-cutoff").value=document.getElementById("cutoff-display").textContent;document.getElementById("predictor").scrollIntoView({behavior:"smooth",block:"start"});setTimeout(()=>predictCourses(),650);}
function predictCourses(){const score=parseFloat(document.getElementById("pred-cutoff").value);const campF=document.getElementById("pred-campus").value;if(isNaN(score)||score<=0){alert("Please enter a valid cutoff between 1 and 200.");return;}const filt=DB.filter(d=>{if(campF&&d.campus!==campF)return false;return(score-d.closing)>=-10;}).sort((a,b)=>b.closing-a.closing);document.getElementById("disp-score").textContent=score.toFixed(2);document.getElementById("res-count").textContent=filt.length+" branch"+(filt.length!==1?"es":"")+" found";const list=document.getElementById("res-list");list.innerHTML="";if(!filt.length){list.innerHTML='<div class="no-result"><span>🔍</span>No branches found. Try a lower score or all campuses.</div>';}else{filt.forEach(d=>{const diff=score-d.closing;let cls,st,stcls;if(diff>=0){cls="safe";st="Safe";stcls="st-safe";}else if(diff>=-5){cls="marginal";st="Marginal";stcls="st-marginal";}else{cls="reach";st="Reach";stcls="st-reach";}const el=document.createElement("div");el.className="rc "+cls;el.innerHTML='<div><span class="badge '+BC[d.campus]+'">'+d.campus+'</span></div><div><div class="rc-branch">'+d.branch+'</div><div class="rc-dept">'+CL[d.campus]+' &#183; '+d.degree+'</div></div><div class="rc-right"><div class="rc-cutoff">'+d.closing+'</div><div class="rc-st '+stcls+'">'+st+'</div><div class="rc-diff">'+( diff>=0?"+":"")+diff.toFixed(2)+'</div></div>';list.appendChild(el);});}document.getElementById("pred-results").classList.add("show");}


// ---- next <script> block ----


	const heightObserver = new ResizeObserver(([{ contentRect }]) => {
		window.parent.postMessage({ action: 'iframeHeightUpdated', height: contentRect.height, id: 'zYmiOs' }, '*');
	});

	heightObserver.observe(document.documentElement);
