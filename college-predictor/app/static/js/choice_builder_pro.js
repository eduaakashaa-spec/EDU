/* ════════ INDICATIVE MODEL — edit these when verified DASA data is available ════════ */
/* Base Non-CIWG closing CRL by NIRF band (the "general DASA" pool) */
const CLOSE_BASE={T10:60000,B25:95000,B50:140000,B100:210000,NR:340000};
/* Branch demand multiplier (lower = more competitive = closes at a better rank) */
const BR_MULT={CS:.45,IT:.55,AI:.5,EC:.7,EE:.9,ME:1.1,CE:1.3,CH:1.2,MT:1.45,PR:1.3,BT:1.2,MC:.6,IN:1.2,MN:1.5,EP:.95,VL:.7,SM:.9,AE:.9,FT:1.45,MR:1.35,NA:1.35,AR:1.0,PL:1.2};
/* Category factor: CIWG pool is much smaller, so CIWG seats usually close EASIER (higher rank).
   1.0 = same as Non-CIWG. 1.35 = CIWG closes ~35% higher (easier). INDICATIVE — adjust per real data. */
const CAT_MULT={NCIWG:1.0,CIWG:1.35};
/* VERIFIED NIRF 2025 Engineering ranks (released 4 Sep 2025, nirfindia.org).
   Numbers = exact Top-100 rank. Strings = official NIRF rank-band (101+ are banded, not numbered).
   Institutes not listed are NOT in the NIRF 2025 Engineering ranking → shown as "Not ranked". */
const NRANK={
  "NIT Tiruchirappalli (Trichy)":9,"NIT Rourkela":13,"NIT Karnataka, Surathkal":17,
  "NIT Calicut":21,"NIT Warangal":28,"Delhi Technological University (DTU)":30,
  "MNIT Jaipur":42,"VNIT Nagpur":44,"NIT Durgapur":49,"NIT Silchar":50,"NIT Patna":53,
  "IIEST Shibpur":54,"Dr B R Ambedkar NIT Jalandhar":55,"MMMUT Gorakhpur":60,
  "MNNIT Allahabad":62,"NIT Delhi":65,"SVNIT Surat":66,"NSUT Delhi":70,"NIT Srinagar":73,
  "University of Hyderabad":74,"SLIET Longowal":79,"MANIT Bhopal":81,"NIT Jamshedpur":82,
  "NIT Meghalaya":83,"NIT Kurukshetra":85,"NIT Raipur":86,"ABV-IIITM Gwalior":96,
  "NIT Hamirpur":97,"NIT Puducherry":99,
  "IIIT Allahabad":"101–150","NIT Agartala":"101–150","NIT Arunachal Pradesh":"101–150",
  "NIT Goa":"101–150","NIT Mizoram":"101–150","NIT Nagaland":"101–150",
  "PDPM IIITDM Jabalpur":"101–150","Punjab Engineering College, Chandigarh":"101–150",
  "NIFTEM Kundli":"101–150",
  "IIITDM Kancheepuram":"151–200","GGV Bilaspur":"151–200","NIT Sikkim":"151–200",
  "NIT Uttarakhand":"151–200","Shri Mata Vaishno Devi Univ":"151–200",
  "Tezpur University":"151–200","IUST Kashmir":"151–200",
  "HBTU Kanpur":"201–300","NIAMT Ranchi":"201–300","NIT Andhra Pradesh":"201–300",
  "IIIT Guwahati":"201–300"
};

const BRN={CS:"CSE",IT:"IT",AI:"AI & DS",EC:"ECE",EE:"EEE",ME:"Mechanical",CE:"Civil",CH:"Chemical",MT:"Metallurgy",PR:"Production",BT:"Biotech",MC:"Maths & Comp",IN:"Instrumentation",MN:"Mining",EP:"Engg Physics",VL:"VLSI",SM:"Smart Mfg",AE:"Aerospace",FT:"Food Tech",MR:"Marine",NA:"Naval Arch",AR:"B.Arch",PL:"B.Plan"};
const NIRFL={T10:"Top 10",B25:"11–25",B50:"26–50",B100:"51–100",NR:"100+/NR"};
/* Real NIRF 2025 display buckets (for the NIRF filter & distribution chart) */
const RBL={t25:"NIRF 1–25",r50:"NIRF 26–50",r100:"NIRF 51–100",r200:"NIRF 101–200",r300:"NIRF 201–300",nr:"Not ranked"};
const RBORD={t25:1,r50:2,r100:3,r200:4,r300:5,nr:6};
const NORD={T10:1,B25:2,B50:3,B100:4,NR:5};
const TORD={NIT:1,IIEST:2,IIIT:3,SPA:4,GFTI:5};
const TIEROF={dream:1,reach:2,safe:3,na:4};
const CATL={CIWG:"C ₹",NCIWG:"NC $"};      /* compact badge labels (C = CIWG ₹-route, NC = Non-CIWG $-route) */
const CATF={CIWG:"CIWG",NCIWG:"Non-CIWG"}; /* full labels for prose & exports */
const STUCAT={CIWG:"CIWG",NCIWG:"Non-CIWG",BOTH:"Both CIWG / Non-CIWG"};

const D=[
["Dr B R Ambedkar NIT Jalandhar","NIT","Punjab","North","B100","CS,IT,EC,EE,ME,CE,CH,BT,IN"],
["MNIT Jaipur","NIT","Rajasthan","North","B50","CS,EC,EE,ME,CE,CH,MT,AR"],
["MANIT Bhopal","NIT","Madhya Pradesh","Central","B100","CS,EC,EE,ME,CE,CH,MT,MC,AR,PL"],
["MNNIT Allahabad","NIT","Uttar Pradesh","North","B50","CS,IT,EC,EE,ME,CE,CH,PR,BT"],
["NIT Agartala","NIT","Tripura","Northeast","NR","CS,EC,EE,ME,CE,CH,PR,BT"],
["NIT Calicut","NIT","Kerala","South","B25","CS,EC,EE,ME,CE,CH,PR,BT,MT,EP,AR"],
["NIT Delhi","NIT","Delhi","North","B100","CS,EC,EE,ME,CE,AI,VL,MC"],
["NIT Durgapur","NIT","West Bengal","East","B50","CS,EC,EE,ME,CE,CH,MT,BT"],
["NIT Goa","NIT","Goa","West","B100","CS,EC,EE,ME,CE"],
["NIT Hamirpur","NIT","Himachal Pradesh","North","B100","CS,EC,EE,ME,CE,CH,MT,EP,AR"],
["NIT Karnataka, Surathkal","NIT","Karnataka","South","B25","CS,IT,EC,EE,ME,CE,CH,MT,MN,AI"],
["NIT Meghalaya","NIT","Meghalaya","Northeast","B100","CS,EC,EE,ME,CE"],
["NIT Nagaland","NIT","Nagaland","Northeast","NR","CS,EC,EE,ME,CE,IN"],
["NIT Patna","NIT","Bihar","East","B100","CS,EC,EE,ME,CE,MC,AI,AR"],
["NIT Puducherry","NIT","Puducherry","South","NR","CS,EC,EE,ME,CE"],
["NIT Raipur","NIT","Chhattisgarh","Central","B100","CS,IT,EC,EE,ME,CE,CH,MT,MN,BT,AR"],
["NIT Sikkim","NIT","Sikkim","Northeast","NR","CS,EC,EE,ME,CE"],
["NIT Arunachal Pradesh","NIT","Arunachal Pradesh","Northeast","NR","CS,EC,EE,ME,CE"],
["NIT Jamshedpur","NIT","Jharkhand","East","B100","CS,EC,EE,ME,CE,MT,PR,EP"],
["NIT Kurukshetra","NIT","Haryana","North","B100","CS,IT,EC,EE,ME,CE,PR,AI"],
["NIT Mizoram","NIT","Mizoram","Northeast","NR","CS,EC,EE,ME,CE"],
["NIT Rourkela","NIT","Odisha","East","B25","CS,EC,EE,ME,CE,CH,MT,MN,BT,FT,IN"],
["NIT Silchar","NIT","Assam","Northeast","B50","CS,EC,EE,ME,CE,IN"],
["NIT Srinagar","NIT","Jammu & Kashmir","North","B100","CS,IT,EC,EE,ME,CE,CH,MT"],
["NIT Tiruchirappalli (Trichy)","NIT","Tamil Nadu","South","T10","CS,EC,EE,ME,CE,CH,MT,PR,IN,AR"],
["NIT Uttarakhand","NIT","Uttarakhand","North","NR","CS,EC,EE,ME,CE"],
["NIT Warangal","NIT","Telangana","South","B25","CS,EC,EE,ME,CE,CH,MT,BT"],
["SVNIT Surat","NIT","Gujarat","West","B100","CS,AI,EC,EE,ME,CE,CH,MC,EP"],
["VNIT Nagpur","NIT","Maharashtra","West","B50","CS,EC,EE,ME,CE,CH,MT,MN,AR"],
["NIT Andhra Pradesh","NIT","Andhra Pradesh","South","NR","CS,EC,EE,ME,CE,CH,MT,BT"],
["IIEST Shibpur","IIEST","West Bengal","East","B100","CS,IT,EC,EE,ME,CE,MT,MN,AR"],
["ABV-IIITM Gwalior","IIIT","Madhya Pradesh","Central","B100","CS,IT,MC"],
["IIIT Kota","IIIT","Rajasthan","North","NR","CS,EC,AI"],
["IIIT Guwahati","IIIT","Assam","Northeast","NR","CS,EC"],
["IIIT Sonepat","IIIT","Haryana","North","NR","CS,IT,EC"],
["IIIT Una","IIIT","Himachal Pradesh","North","NR","CS,IT,EC"],
["IIIT Sri City, Chittoor","IIIT","Andhra Pradesh","South","NR","CS,EC,AI"],
["IIIT Vadodara","IIIT","Gujarat","West","NR","CS,IT"],
["IIIT Allahabad","IIIT","Uttar Pradesh","North","B100","CS,IT,EC"],
["IIITDM Kancheepuram","IIIT","Tamil Nadu","South","NR","CS,EC,ME,SM,AI"],
["PDPM IIITDM Jabalpur","IIIT","Madhya Pradesh","Central","NR","CS,EC,ME,SM"],
["IIIT Tiruchirappalli","IIIT","Tamil Nadu","South","NR","CS,EC"],
["IIIT Dharwad","IIIT","Karnataka","South","NR","CS,EC,AI"],
["IIIT Kottayam","IIIT","Kerala","South","NR","CS,EC,AI"],
["IIIT Pune","IIIT","Maharashtra","West","NR","CS,EC"],
["IIIT Bhagalpur","IIIT","Bihar","East","NR","CS,EC"],
["IIIT Bhopal","IIIT","Madhya Pradesh","Central","NR","CS,IT,EC"],
["IIIT Raichur","IIIT","Karnataka","South","NR","CS,AI,MC"],
["IIITV-ICD Diu","IIIT","Diu (UT)","West","NR","CS,IT"],
["Assam University, Silchar","GFTI","Assam","Northeast","NR","CS,EC,IT"],
["GGV Bilaspur","GFTI","Chhattisgarh","Central","NR","CS,IT,EC,ME,CE,CH"],
["JK Institute, Univ of Allahabad","GFTI","Uttar Pradesh","North","NR","CS,EC"],
["NIAMT Ranchi","GFTI","Jharkhand","East","NR","ME,MT,PR"],
["SLIET Longowal","GFTI","Punjab","North","NR","CS,EC,EE,ME,CE,CH,FT,IN"],
["Tezpur University","GFTI","Assam","Northeast","B100","CS,EC,EE,ME,CE,FT"],
["SPA Bhopal","SPA","Madhya Pradesh","Central","NR","AR,PL"],
["SPA New Delhi","SPA","Delhi","North","NR","AR,PL"],
["SPA Vijayawada","SPA","Andhra Pradesh","South","NR","AR,PL"],
["Shri Mata Vaishno Devi Univ","GFTI","Jammu & Kashmir","North","NR","CS,EC,ME,CE,AR"],
["University of Hyderabad","GFTI","Telangana","South","NR","CS"],
["Punjab Engineering College, Chandigarh","GFTI","Chandigarh","North","NR","CS,EC,EE,ME,CE,AE,PR,MT"],
["JNU School of Engineering","GFTI","Delhi","North","NR","CS,EC"],
["NIFTEM Kundli","GFTI","Haryana","North","NR","FT"],
["Central University of Jammu","GFTI","Jammu & Kashmir","North","NR","CS,EC"],
["IET, Dr H S Gour Univ Sagar","GFTI","Madhya Pradesh","Central","NR","CS,EC,ME,CE"],
["Rajiv Gandhi Natl Aviation Univ","GFTI","Uttar Pradesh","North","NR","AE"],
["IUST Kashmir","GFTI","Jammu & Kashmir","North","NR","CS,EC,ME,CE"],
["SGSITS Indore","GFTI","Madhya Pradesh","Central","NR","CS,IT,EC,EE,ME,CE,IN"],
["NITTTR Bhopal","GFTI","Madhya Pradesh","Central","NR","CS"],
["Central University of Karnataka","GFTI","Karnataka","South","NR","CS,EC"],
["Delhi Technological University (DTU)","GFTI","Delhi","North","B50","CS,IT,EC,EE,ME,CE,CH,PR,BT,EP,MC,AI"],
["Dr SSB UICET, Panjab Univ","GFTI","Chandigarh","North","NR","CH,FT"],
["Gautam Buddha Univ, Greater Noida","GFTI","Uttar Pradesh","North","NR","CS,IT,EC,ME,CE"],
["IMU Chennai","GFTI","Tamil Nadu","South","NR","MR,NA"],
["IMU Kochi","GFTI","Kerala","South","NR","MR"],
["IMU Kolkata","GFTI","West Bengal","East","NR","MR,NA"],
["IMU Mumbai Port","GFTI","Maharashtra","West","NR","MR"],
["IMU Navi Mumbai","GFTI","Maharashtra","West","NR","MR"],
["IMU Visakhapatnam","GFTI","Andhra Pradesh","South","NR","MR,NA"],
["MMMUT Gorakhpur","GFTI","Uttar Pradesh","North","NR","CS,IT,EC,EE,ME,CE,CH"],
["NSUT Delhi","GFTI","Delhi","North","B100","CS,IT,EC,EE,ME,AI,MC,BT"],
["UIET PUSSRC Hoshiarpur","GFTI","Punjab","North","NR","CS,EC,ME"],
["UIET Panjab Univ, Chandigarh","GFTI","Chandigarh","North","NR","CS,IT,EC,EE,ME,BT"],
["HBTU Kanpur","GFTI","Uttar Pradesh","North","NR","CS,IT,EC,EE,ME,CE,CH,FT,BT"]
].map(r=>({name:r[0],type:r[1],state:r[2],zone:r[3],nirf:r[4],br:r[5].split(",")}));
const ZONES=["North","South","East","West","Central","Northeast"];

let picks=[];let ordered=[];let droppedLog=[];
let tierSort={1:'nirf',2:'nirf',3:'nirf',4:'nirf'};
let intelMode='tier';                 /* tier | flat | m1 | m2 | m3 */
let brPriority=["CS","AI","IT","EC","VL","EE","MC","ME","CH","CE","AE","EP","IN","BT","PR","MT","SM","MN","FT","NA","MR","AR","PL"];
let selRows=new Set();                 /* multi-select by pkey */
let dragKeys=[];                       /* keys currently being dragged */
const ECON={CIWG:0,NCIWG:1};
function ckey(o){return nrSortKey(o.name);}                 /* college: best NIRF first */
function bkey(o){const i=brPriority.indexOf(o.brCode);return i<0?999:i;}  /* branch priority */
function ekey(o){return ECON[o.cat];}                       /* economy: CIWG (₹) first */
function applyIntel(mode){
  intelMode=mode;selRows.clear();
  if(mode==='tier')reorderOrdered();
  else if(mode==='m1')ordered.sort((a,b)=>ckey(a)-ckey(b)||bkey(a)-bkey(b)||ekey(a)-ekey(b)||a.name.localeCompare(b.name));
  else if(mode==='m2')ordered.sort((a,b)=>bkey(a)-bkey(b)||ckey(a)-ckey(b)||ekey(a)-ekey(b)||a.name.localeCompare(b.name));
  else if(mode==='m3')ordered.sort((a,b)=>ekey(a)-ekey(b)||bkey(a)-bkey(b)||ckey(a)-ckey(b)||a.name.localeCompare(b.name));
  /* 'flat' keeps current order */
  recompute();
}
function moveBr(code,dir){const i=brPriority.indexOf(code);const j=i+dir;if(j<0||j>=brPriority.length)return;[brPriority[i],brPriority[j]]=[brPriority[j],brPriority[i]];if(['m1','m2','m3'].includes(intelMode))applyIntel(intelMode);else{renderBrPriority();}}
function renderBrPriority(){
  const box=document.getElementById("brPrio");if(!box)return;
  box.innerHTML=brPriority.map((c,i)=>`<span class="prio-chip"><b>${i+1}</b> ${BRN[c]}<button onclick="moveBr('${c}',-1)" title="Higher priority" aria-label="up">◀</button><button onclick="moveBr('${c}',1)" title="Lower priority" aria-label="down">▶</button></span>`).join("");
}
function moveToPos(idx,val){let np=parseInt(val,10);if(isNaN(np)){renderRounds();return;}np=Math.max(1,Math.min(ordered.length,np))-1;if(np===idx){return;}const [it]=ordered.splice(idx,1);ordered.splice(np,0,it);recompute();}
function moveItems(keys,targetKey){
  const set=new Set(keys);const moving=ordered.filter(o=>set.has(pkey(o)));if(!moving.length)return;
  const rest=ordered.filter(o=>!set.has(pkey(o)));
  let pos=targetKey?rest.findIndex(o=>pkey(o)===targetKey):rest.length;if(pos<0)pos=rest.length;
  rest.splice(pos,0,...moving);ordered=rest;recompute();
}
function toggleSel(k){selRows.has(k)?selRows.delete(k):selRows.add(k);renderRounds();}
function clearSel(){selRows.clear();renderRounds();}
function moveSelTo(val){let np=parseInt(val,10);if(isNaN(np)||!selRows.size)return;np=Math.max(1,Math.min(ordered.length,np))-1;const target=ordered[np]?pkey(ordered[np]):null;moveItems([...selRows],target);}
function moveSelStep(dir){if(!selRows.size)return;const idxs=ordered.map((o,i)=>selRows.has(pkey(o))?i:-1).filter(i=>i>=0);const t=dir<0?Math.max(0,idxs[0]-1):Math.min(ordered.length-1,idxs[idxs.length-1]+1);const target=ordered[t]?pkey(ordered[t]):null;moveItems([...selRows],target);}
function tierCmp(a,b){const m=tierSort[a.tier]||'nirf';
  if(m==='ciwg'){const x=a.cat==='CIWG'?0:1,y=b.cat==='CIWG'?0:1;if(x!==y)return x-y;}
  else if(m==='nciwg'){const x=a.cat==='NCIWG'?0:1,y=b.cat==='NCIWG'?0:1;if(x!==y)return x-y;}
  return nrSortKey(a.name)-nrSortKey(b.name)||a.name.localeCompare(b.name)||a.brCode.localeCompare(b.brCode);}
function reorderOrdered(){ordered.sort((a,b)=>a.tier-b.tier||tierCmp(a,b));}
function sortTier(t,m){tierSort[t]=m;reorderOrdered();renderRounds();}
const F={type:new Set(),nirf:new Set(),zone:new Set(),state:new Set(),br:new Set(),fit:new Set(),excl:new Set(),xcat:new Set()};
let dark=window.matchMedia&&window.matchMedia('(prefers-color-scheme: dark)').matches;
let charts={};

function R(){const n=parseInt(document.getElementById("fRank").value,10);return n>0?n:0;}
function V(){return parseInt(document.getElementById("varSlide").value,10)||0;}
function stuCat(){return document.getElementById("fCat").value;}
function addCat(){const c=stuCat();return c==="BOTH"?document.getElementById("addAsCat").value:c;}
function dByName(n){return D.find(d=>d.name===n);}
/* Indicative base closing-CRL is now derived from the VERIFIED NIRF rank (not the coarse band),
   so every college gets a distinct value. Curve 28080·rank^0.47 is fitted to the old band anchors
   (rank≈5→60k, 18→95k, 38→140k, 75→210k, ~200→340k). Banded institutes use the band midpoint;
   not-ranked institutes use a high proxy (close easiest). INDICATIVE — replace when real DASA data lands. */
function hashStr(s){let h=0;for(let i=0;i<s.length;i++)h=(h*31+s.charCodeAt(i))>>>0;return h;}
/* Exact Top-100 ranks are used as-is. Institutes that only have an official rank-BAND (or are
   not ranked) are positioned deterministically WITHIN that band via a stable name hash — so two
   different colleges in the same band show distinct (but in-band) indicative closing ranks,
   instead of an identical value. Never places a college outside its official NIRF band. */
function nirfProxy(name){
  const v=NRANK[name];
  if(typeof v==="number")return v;
  const RG={"101–150":[101,150],"151–200":[151,200],"201–300":[201,300]}[v]||[300,360];
  return RG[0]+(hashStr(name)%1000)/1000*(RG[1]-RG[0]);
}
/* DASA 2025 ACTUAL overall closing CRL (all 3 rounds), source: user rank sheet dasa_ciwg_2025_ranks.xlsx. C=CIWG, N=Non-CIWG, keyed by branch code. */
const REALCLOSE={
"ABV-IIITM Gwalior":{C:{MC:509620,CS:396304,EE:347668},N:{CS:530871}},
"Delhi Technological University (DTU)":{C:{CS:103543,EC:191826,IT:141512,MC:215669,ME:473418,EE:594412,CH:523204,BT:658181,CE:782356},N:{CS:241277,MC:344926,IT:484379,EC:1117096,ME:1177629}},
"Dr B R Ambedkar NIT Jalandhar":{C:{CS:497878,IT:769321,ME:707893,AI:809482},N:{CS:1347319}},
"Gautam Buddha Univ, Greater Noida":{C:{CS:792983}},
"IIEST Shibpur":{C:{CS:520518,AE:317467,EC:437890},N:{EC:1089227,CS:862161,AE:555613}},
"IIIT Allahabad":{C:{IT:225013,EC:291546},N:{IT:423129,EC:1329568}},
"IIIT Kottayam":{C:{AI:202105,CS:319864,EC:359106},N:{CS:775045,AI:878872}},
"IIIT Pune":{C:{CS:1140984,EC:559773},N:{EC:311942,CS:619976}},
"IIIT Sri City, Chittoor":{C:{CS:408977,AI:934537},N:{AI:530805,CS:639012}},
"IIIT Vadodara":{C:{CS:347943}},
"IIITDM Kancheepuram":{C:{CS:246213,EC:275208,AI:282946,ME:437322,VL:355077},N:{CS:649670,AI:369594,EC:602270}},
"IMU Visakhapatnam":{C:{NA:582932}},
"JNU School of Engineering":{C:{CS:584509}},
"MANIT Bhopal":{C:{AR:22175,CS:299739,EC:610318,EE:585441,MC:1221201},N:{CS:1017981}},
"MNIT Jaipur":{C:{AR:11084,EC:338394,CS:233197,AI:261513,EE:1060828,ME:563932,CH:707910},N:{CS:494231,EC:587471,AI:907544,ME:1329417}},
"MNNIT Allahabad":{C:{CS:256738,EC:390036,ME:550551,BT:308124,CH:358809,EE:737665},N:{CS:931961,EC:533851}},
"NIT Agartala":{C:{CS:931692}},
"NIT Andhra Pradesh":{C:{CS:306480,EC:1029243}},
"NIT Calicut":{C:{AR:1071,CS:77929,EC:113231,CH:195952,EE:162162,CE:363502,BT:214118,EP:374066,ME:196041,MT:417977,PR:498621},N:{AR:19111,CS:126093,EC:257873,EE:426990,EP:424146,ME:521078,CH:843474,PR:976425,CE:934725,BT:818619}},
"NIT Delhi":{C:{CS:245423,EE:289975,AE:153753,EC:333514,AI:280252,ME:316351,VL:289927,CE:580466},N:{CS:926908,AI:1025758,AE:1259326}},
"NIT Durgapur":{C:{CS:194796,EC:390036,MC:396720},N:{CS:358272,MC:698829}},
"NIT Goa":{C:{CS:274261,EC:551924,ME:457872,EE:664049},N:{CS:828008,EC:551924,EE:619516}},
"NIT Hamirpur":{C:{AR:10999,CS:769321}},
"NIT Jamshedpur":{C:{CS:386800,EC:587044},N:{CS:1245851}},
"NIT Karnataka, Surathkal":{C:{CS:22657,IT:46502,AI:43849,EC:54969,MC:55280,EE:110992,CH:141585,ME:128896,CE:436089,MT:568773,MN:587729},N:{CS:33736,AI:76784,IT:87162,EC:79607,MC:76237,CH:363190,EE:156135,ME:207370,MT:688014,CE:607990}},
"NIT Kurukshetra":{C:{AI:763820,CS:403752,EC:655863,VL:968418,ME:675413,EE:656568,MC:747088,IT:763820},N:{CS:1020638,AI:926908}},
"NIT Patna":{C:{CS:875705,AI:521760,EC:1270913}},
"NIT Puducherry":{C:{CS:214464,EC:417977,CE:372989,EE:462135,ME:1149332},N:{CS:666619}},
"NIT Raipur":{C:{AR:26086,CS:551081,IT:658673}},
"NIT Rourkela":{C:{CS:102778,AI:118955,EC:139686,IN:372745,EE:368435,ME:219295,CH:357632,BT:584941,EP:710572},N:{CS:140041,AI:187573,EC:196161,EE:1173667,IN:747778,ME:701807,CH:955829}},
"NIT Silchar":{C:{CS:327195,EC:383910}},
"NIT Srinagar":{C:{CS:427477}},
"NIT Tiruchirappalli (Trichy)":{C:{AR:1384,CS:16522,EC:33868,ME:77267,EE:78969,CH:190350,CE:333855,IN:178544,PR:250166,MT:281114},N:{AR:21988,CS:17478,EC:46614,CH:364481,EE:116498,ME:205379,IN:230753,PR:474054,CE:974217,MT:726464}},
"NIT Warangal":{C:{CS:38176,AI:47457,CE:576584,MC:513655,EC:90245,VL:101537,EE:156706,ME:148054,CH:181015,BT:355077,MT:578455},N:{CS:84741,AI:111529,EC:166004,VL:189638,MC:187769,EE:314315,ME:264569,CH:603129,BT:779103}},
"NSUT Delhi":{C:{AI:202143,CS:250703,IT:284722},N:{CS:853076,AI:514758}},
"PDPM IIITDM Jabalpur":{C:{CS:689088}},
"Punjab Engineering College, Chandigarh":{C:{CS:1139108,ME:560637,AI:1060828},N:{CS:819399}},
"SPA Bhopal":{C:{AR:5223}},
"SPA New Delhi":{C:{AR:1132,PL:2466},N:{AR:6016}},
"SPA Vijayawada":{C:{AR:3514,PL:7689},N:{AR:9956}},
"SVNIT Surat":{C:{CS:265144,ME:575947,EC:358608,AI:450137,MC:376662,CH:908293,VL:431723,EE:914674},N:{VL:62656,CS:709411,MC:399122,EC:624011,ME:737383}},
"University of Hyderabad":{C:{CS:664049}},
"VNIT Nagpur":{C:{AR:6816,CS:147009,EC:270474,EE:403960,ME:333505,CH:574810,CE:667613},N:{CS:280185,EC:485153,EE:1074763}}
};
function realClose(name,brCode,cat){const r=REALCLOSE[name];if(!r)return null;const o=cat==="CIWG"?r.C:r.N;return (o&&o[brCode]!=null)?o[brCode]:null;}
function closeReal(name,brCode,cat){return realClose(name,brCode,cat)!=null;}
function estClose(name,brCode,cat){const rc=realClose(name,brCode,cat);if(rc!=null)return rc;return Math.round(28080*Math.pow(nirfProxy(name),0.47)*(BR_MULT[brCode]||1)*(CAT_MULT[cat]||1));}
function ceff(name,brCode,cat,v){return estClose(name,brCode,cat)*(1+v/100);}
function fit(name,brCode,cat,r,v){if(!r)return "na";const k=r/ceff(name,brCode,cat,v);if(k<=0.95)return "safe";if(k<=1.05)return "reach";return "dream";}
function ratioK(name,brCode,cat,r,v){return r/ceff(name,brCode,cat,v);}
function probOf(k){if(k<=.4)return .95;if(k<=.6)return .88;if(k<=.8)return .75;if(k<=.95)return .6;if(k<=1.05)return .45;if(k<=1.15)return .28;if(k<=1.3)return .15;return .06;}
function esc(s){return s.replace(/'/g,"\\'");}
function has(name,b,cat){return picks.some(p=>p.name===name&&p.brCode===b&&p.cat===cat);}
function nrShort(name,band){const v=NRANK[name];if(typeof v==="number")return '#'+v;if(typeof v==="string")return v;return 'NR';}
function nrLong(name,band){const v=NRANK[name];if(typeof v==="number")return 'NIRF #'+v;if(typeof v==="string")return 'NIRF '+v+' band';return 'NIRF 2025: Not ranked';}
function realNirf(name){const v=NRANK[name];if(typeof v==="number"){if(v<=25)return "t25";if(v<=50)return "r50";return "r100";}if(v==="101–150"||v==="151–200")return "r200";if(v==="201–300")return "r300";return "nr";}
function nrSortKey(name){const v=NRANK[name];if(typeof v==="number")return v;if(v==="101–150")return 125;if(v==="151–200")return 175;if(v==="201–300")return 250;return 9999;}

/* filters */
const FITL={safe:"Safe",reach:"Reach",dream:"Dream"};
/* Program-type exclusions: hide whole program families (branch codes) from list, tiers & analysis. */
const XCAT={marine:["MR","NA"],arch:["AR","PL"]};
const XCATL={marine:"🚢 Marine / Naval",arch:"🏛 Architecture / Planning"};
function brAllowed(b){for(const k of F.xcat)if(XCAT[k]&&XCAT[k].includes(b))return false;return true;}
function allowedBr(d){return d.br.filter(brAllowed);}
function toggleXcat(k){
  if(F.xcat.has(k)){F.xcat.delete(k);}
  else{F.xcat.add(k);const codes=XCAT[k]||[];
    picks=picks.filter(p=>!codes.includes(p.brCode));
    ordered=ordered.filter(p=>!codes.includes(p.brCode));
    droppedLog=droppedLog.filter(p=>!codes.includes(p.brCode));}
  initFilters();recompute();
}
function chips(el,items,set,lbl,linked){
  const c=document.getElementById(el);
  c.innerHTML=items.map(i=>`<button class="chip ${set.has(i)?'on':''}" data-v="${i}">${lbl?lbl[i]:i}</button>`).join("");
  c.querySelectorAll(".chip").forEach(b=>b.onclick=()=>{const v=b.dataset.v;set.has(v)?set.delete(v):set.add(v);b.classList.toggle("on");if(linked)renderStates();renderList();renderImpact();});
}
function availStates(){return [...new Set(D.filter(d=>(!F.type.size||F.type.has(d.type))&&(!F.zone.size||F.zone.has(d.zone))).map(d=>d.state))].sort();}
function renderStates(){
  const s=availStates();[...F.state].forEach(x=>{if(!s.includes(x))F.state.delete(x);});
  const c=document.getElementById("fState");
  c.innerHTML=s.map(x=>`<button class="chip ${F.state.has(x)?'on':''}" data-v="${x}">${x}</button>`).join("");
  c.querySelectorAll(".chip").forEach(b=>b.onclick=()=>{const v=b.dataset.v;F.state.has(v)?F.state.delete(v):F.state.add(v);b.classList.toggle("on");renderList();renderImpact();});
}
function initFilters(){
  chips("fType",["NIT","IIEST","IIIT","SPA","GFTI"],F.type,null,true);
  chips("fNirf",["t25","r50","r100","r200","r300","nr"],F.nirf,RBL,false);
  chips("fZone",ZONES,F.zone,null,true);
  renderStates();
  chips("fBr",Object.keys(BRN),F.br,BRN,false);
  chips("fFit",["safe","reach","dream"],F.fit,FITL,false);
  document.getElementById("fXcat").innerHTML=["marine","arch"].map(k=>`<button class="chip ${F.xcat.has(k)?'on':''}" onclick="toggleXcat('${k}')">${XCATL[k]}</button>`).join("");
  document.getElementById("exclSel").innerHTML='<option value="">+ Add a college to exclude…</option>'+D.map(d=>d.name).sort().map(n=>`<option value="${n.replace(/"/g,'&quot;')}">${n}</option>`).join("");
}
function clearFilters(){
  F.type.clear();F.nirf.clear();F.zone.clear();F.state.clear();F.br.clear();F.fit.clear();F.xcat.clear();
  const q=document.getElementById("q");if(q)q.value="";
  const ss=document.getElementById("sortSel");if(ss)ss.value="default";
  initFilters();          /* rebuild every chip group from the now-empty sets (no stale .on state) */
  renderList();
  renderImpact();
}
function addExcl(){const sel=document.getElementById("exclSel");const n=sel.value;sel.value="";if(!n)return;F.excl.add(n);picks=picks.filter(p=>p.name!==n);ordered=ordered.filter(p=>p.name!==n);renderExclChips();recompute();}
function removeExcl(n){F.excl.delete(n);renderExclChips();recompute();}
function clearExcl(){F.excl.clear();renderExclChips();recompute();}
function renderExclChips(){document.getElementById("exclChips").innerHTML=[...F.excl].map(n=>`<span class="exclChip">${n}<button onclick="removeExcl('${esc(n)}')">✕</button></span>`).join("");}

function filtered(){
  const q=document.getElementById("q").value.toLowerCase().trim(),r=R(),v=V(),ac=addCat();
  let out=D.filter(d=>!F.excl.has(d.name)&&allowedBr(d).length>0&&(!F.type.size||F.type.has(d.type))&&(!F.nirf.size||F.nirf.has(realNirf(d.name)))&&(!F.zone.size||F.zone.has(d.zone))&&(!F.state.size||F.state.has(d.state))&&(!F.br.size||allowedBr(d).some(b=>F.br.has(b)))&&(!q||d.name.toLowerCase().includes(q)||d.state.toLowerCase().includes(q)));
  if(F.fit.size&&r)out=out.filter(d=>allowedBr(d).some(b=>(!F.br.size||F.br.has(b))&&F.fit.has(fit(d.name,b,ac,r,v))));
  const s=document.getElementById("sortSel").value;
  if(s==="nirfBest")out.sort((a,b)=>nrSortKey(a.name)-nrSortKey(b.name)||a.name.localeCompare(b.name));
  else if(s==="nirfLow")out.sort((a,b)=>nrSortKey(b.name)-nrSortKey(a.name)||a.name.localeCompare(b.name));
  else if(s==="az")out.sort((a,b)=>a.name.localeCompare(b.name));
  else out.sort((a,b)=>TORD[a.type]-TORD[b.type]||nrSortKey(a.name)-nrSortKey(b.name));
  return out;
}
function renderList(){
  const out=filtered(),r=R(),v=V(),both=stuCat()==="BOTH";
  const cats=both?["CIWG","NCIWG"]:[addCat()];
  document.getElementById("cnt").textContent=out.length+" of "+D.length+" institutes shown";
  document.getElementById("list").innerHTML=out.map(d=>{
    const ab=allowedBr(d);
    let addBtns;
    if(both){
      const allC=ab.every(b=>has(d.name,b,"CIWG")), allNC=ab.every(b=>has(d.name,b,"NCIWG"));
      addBtns=`<div class="addgrp"><button class="addall c" onclick="addCollege('${esc(d.name)}','CIWG')" title="Add all branches as CIWG (₹ route)">${allC?'✓ C ₹':'+ C ₹'}</button><button class="addall nc" onclick="addCollege('${esc(d.name)}','NCIWG')" title="Add all branches as Non-CIWG ($ route)">${allNC?'✓ NC $':'+ NC $'}</button><button class="addall" onclick="addCollege('${esc(d.name)}')" title="Add all branches as both seat types">${allC&&allNC?'✓ Both':'+ Both'}</button></div>`;
    } else {
      const all=ab.every(b=>has(d.name,b,addCat()));
      addBtns=`<button class="addall" onclick="addCollege('${esc(d.name)}')">${all?'✓ All added':'+ Add all'}</button>`;
    }
    const brs=ab.map(b=>cats.map(c=>{const on=has(d.name,b,c);const st=on?"":fit(d.name,b,c,r,v);
      const cv=estClose(d.name,b,c), rr=closeReal(d.name,b,c);
      const lbl=`<span class="brn">${BRN[b]}${both?' '+CATL[c]:''}</span><small class="brcrl ${rr?'real':''}" title="${rr?'DASA 2025 actual':'indicative'} closing CRL">${cv.toLocaleString()}</small>`;
      return `<button class="br stack ${on?'added':st} ${both?c:''}" onclick="toggle('${esc(d.name)}','${b}','${c}')">${on?'✓ ':'+ '}${lbl}</button>`;}).join("")).join("");
    return `<div class="col"><div class="ch"><h3>${d.name}</h3>${addBtns}</div><div class="meta"><span class="m t">${d.type}</span><span class="m">${d.state} · ${d.zone}</span><span class="m r">${nrLong(d.name,d.nirf)}</span></div><div class="brs">${brs}</div></div>`;
  }).join("")||'<div class="empty">No institutes match these filters.</div>';
}
function toggle(name,b,cat){const ac=cat||addCat();const i=picks.findIndex(p=>p.name===name&&p.brCode===b&&p.cat===ac);i>=0?picks.splice(i,1):picks.push({name,brCode:b,cat:ac});recompute();}
function addCollege(name,catArg){const d=dByName(name);if(!d)return;const cats=catArg?[catArg]:(stuCat()==="BOTH"?["CIWG","NCIWG"]:[addCat()]);const bl=allowedBr(d);
  const all=bl.every(b=>cats.every(c=>has(name,b,c)));
  if(all){picks=picks.filter(p=>!(p.name===name&&cats.includes(p.cat)));}
  else{bl.forEach(b=>cats.forEach(c=>{if(!has(name,b,c))picks.push({name,brCode:b,cat:c});}));}recompute();}
function bulkAdd(){const cats=stuCat()==="BOTH"?["CIWG","NCIWG"]:[addCat()];filtered().forEach(d=>allowedBr(d).forEach(b=>{if(!F.br.size||F.br.has(b))cats.forEach(c=>{if(!has(d.name,b,c))picks.push({name:d.name,brCode:b,cat:c});});}));recompute();}

const TIERMETA=[
  [1,"Tier 1 · Dream","var(--dream)","Aspirational reaches — your rank is worse than last-year's cutoff by more than 5% (k > 1.05). Listed first so DASA tries these before anything lower."],
  [2,"Tier 2 · Reach","var(--reach)","Right around your cutoff — within ±5% of last-year's closing (0.95 < k ≤ 1.05). Realistic borderline choices."],
  [3,"Tier 3 · Safe","var(--good)","At or clearly inside last-year's cutoff — your rank ≤ 0.95× the closing (k ≤ 0.95). High-confidence choices so you don't go seatless."],
  [4,"Tier 4 · Unscored","var(--ink2)","No CRL rank entered yet — these can't be rank-fitted until a rank is set."]
];
function autoArrange(){
  const r=R(),v=V();
  const blocks={dream:[],reach:[],safe:[],na:[]};
  picks.forEach(p=>{const d=dByName(p.name);if(!d)return;blocks[fit(d.name,p.brCode,p.cat,r,v)].push(p);});
  Object.keys(blocks).forEach(k=>blocks[k].sort((a,b)=>{const da=dByName(a.name),db=dByName(b.name);return nrSortKey(da.name)-nrSortKey(db.name)||da.name.localeCompare(db.name);}));
  const mk=(arr,t)=>arr.map(p=>({name:p.name,brCode:p.brCode,cat:p.cat,tier:t}));
  ordered=[].concat(mk(blocks.dream,1),mk(blocks.reach,2),mk(blocks.safe,3),mk(blocks.na,4));
  reorderOrdered();
  recompute();document.getElementById("s3").scrollIntoView({behavior:"smooth"});
}
function tmplRows(){
  if(ordered.length)return ordered.map(p=>({name:p.name,brCode:p.brCode,cat:p.cat}));
  const cats=stuCat()==="BOTH"?["CIWG","NCIWG"]:[addCat()];
  const out=[];D.forEach(d=>allowedBr(d).forEach(b=>cats.forEach(c=>out.push({name:d.name,brCode:b,cat:c}))));return out;
}
function downloadTemplate(){
  const e=x=>'"'+String(x==null?"":x).replace(/"/g,'""')+'"';
  const rows=tmplRows();
  const L=[];
  L.push('# EduAakashaa DASA 2026 choice template. Reorder rows OR renumber the Position column to set preference order, delete rows you do not want, then re-upload. Keep the Institute + BranchCode + Category columns intact.');
  L.push(["Position","Institute","BranchCode","Branch","Category","NIRF","LastYrCloseCRL","CloseSource"].map(e).join(","));
  rows.forEach((p,i)=>{const d=dByName(p.name);L.push([i+1,p.name,p.brCode,BRN[p.brCode]||p.brCode,p.cat,d?nrShort(d.name,d.nirf):"",d?estClose(p.name,p.brCode,p.cat):"",closeReal(p.name,p.brCode,p.cat)?"DASA2025":"estimate"].map(e).join(","));});
  const blob=new Blob([L.join("\n")],{type:"text/csv"});const a=document.createElement("a");a.href=URL.createObjectURL(blob);a.download="dasa2026-choice-template.csv";a.click();
  const m=document.getElementById("tmplMsg");if(m)m.textContent="Template downloaded ("+rows.length+" rows). Edit & re-upload.";
}
function parseCSV(text){
  const s=text.replace(/\r\n?/g,"\n");const rows=[];let field="",row=[],inq=false;
  for(let i=0;i<s.length;i++){const c=s[i];
    if(inq){if(c==='"'){if(s[i+1]==='"'){field+='"';i++;}else inq=false;}else field+=c;continue;}
    if(c==='"'){inq=true;continue;}
    if(c===','){row.push(field);field="";continue;}
    if(c==="\n"){row.push(field);rows.push(row);row=[];field="";continue;}
    field+=c;
  }
  if(field.length||row.length){row.push(field);rows.push(row);}
  return rows;
}
function resolveInst(s){s=(s||"").trim();if(!s)return null;let d=D.find(x=>x.name===s);if(d)return d.name;const ls=s.toLowerCase();d=D.find(x=>x.name.toLowerCase()===ls);if(d)return d.name;d=D.find(x=>x.name.toLowerCase().includes(ls)||ls.includes(x.name.toLowerCase()));return d?d.name:null;}
function resolveBranch(code,name){code=(code||"").trim().toUpperCase();if(BRN[code])return code;const nm=(name||"").trim().toLowerCase();if(nm){let k=Object.keys(BRN).find(c=>BRN[c].toLowerCase()===nm);if(k)return k;k=Object.keys(BRN).find(c=>BRN[c].toLowerCase().includes(nm)||nm.includes(BRN[c].toLowerCase()));if(k)return k;}if(BRN[(name||"").trim().toUpperCase()])return (name||"").trim().toUpperCase();return null;}
function resolveCat(s){const u=(s||"").toUpperCase();if(u.includes("NON")||u.includes("NC")||u.includes("$"))return "NCIWG";if(u.includes("CIWG")||u.includes("₹")||u.trim()==="C")return "CIWG";return null;}
function uploadTemplate(file){
  if(!file)return;const msg=document.getElementById("tmplMsg");
  const reader=new FileReader();
  reader.onload=()=>{
    try{
      let rows=parseCSV(reader.result).filter(r=>r.length&&!(r[0]||"").trim().startsWith("#")&&r.some(c=>(c||"").trim()!==""));
      if(rows.length<2){if(msg)msg.textContent="⚠ Could not read any rows from that file.";return;}
      const hdr=rows[0].map(x=>x.trim().toLowerCase());
      const col=(...names)=>{for(const n of names){let i=hdr.findIndex(h=>h===n);if(i>=0)return i;}for(const n of names){let i=hdr.findIndex(h=>h.includes(n));if(i>=0)return i;}return -1;};
      const ci=col("institute","college","name"),cbc=col("branchcode","code"),cbn=col("branch","program"),ccat=col("category","cat","seat"),cpos=col("position","pref","order");
      if(ci<0||(cbc<0&&cbn<0)||ccat<0){if(msg)msg.textContent="⚠ Need columns: Institute, BranchCode (or Branch), Category. Use the downloaded template.";return;}
      let data=rows.slice(1).map((r,idx)=>({inst:r[ci],code:cbc>=0?r[cbc]:"",bname:cbn>=0?r[cbn]:"",cat:r[ccat],pos:cpos>=0?parseFloat(r[cpos]):NaN,idx}));
      if(cpos>=0&&data.every(d=>!isNaN(d.pos)))data.sort((a,b)=>a.pos-b.pos||a.idx-b.idx);
      const np=[];const seen=new Set();let skip=0;
      data.forEach(rw=>{const nm=resolveInst(rw.inst),bc=resolveBranch(rw.code,rw.bname),cat=resolveCat(rw.cat);
        const d=nm?dByName(nm):null;
        if(!nm||!bc||!cat||!d||!d.br.includes(bc)||!brAllowed(bc)){skip++;return;}
        const k=nm+"|"+bc+"|"+cat;if(seen.has(k))return;seen.add(k);np.push({name:nm,brCode:bc,cat});});
      if(!np.length){if(msg)msg.textContent="⚠ No rows matched the institute/branch list. Check spellings or use the template.";return;}
      const r=R(),v=V();
      picks=np.map(p=>({...p}));droppedLog=[];
      ordered=np.map(p=>{const d=dByName(p.name);const t=(r&&d)?TIEROF[fit(d.name,p.brCode,p.cat,r,v)]:4;return {name:p.name,brCode:p.brCode,cat:p.cat,tier:t};});
      intelMode="flat";
      recompute();document.getElementById("s3").scrollIntoView({behavior:"smooth"});
      const m2=document.getElementById("tmplMsg");if(m2)m2.textContent=`✓ Loaded ${np.length} choices from template${skip?` · ${skip} row(s) skipped (no match)`:""}.`;
    }catch(err){if(msg)msg.textContent="⚠ Could not parse that file: "+err.message;}
  };
  reader.readAsText(file);
}
function intelPanel(){
  const m=intelMode;
  const btn=(v,lbl,tip)=>`<button class="imode ${m===v?'on':''}" onclick="applyIntel('${v}')" title="${tip}">${lbl}</button>`;
  return `<div class="intel noprint">
    <div class="intel-row"><span class="tbl-label">View / smart order:</span>
      ${btn('tier','▦ Tier view','Group by Dream/Reach/Safe (default)')}
      ${btn('flat','↕ Custom order','Flat list — drag, multi-select & type positions freely')}
      ${btn('m1','① College › Branch › Economy','Top colleges first, then your branch priority, then CIWG before Non-CIWG')}
      ${btn('m2','② Branch › College › Economy','Your branch priority first, then top colleges, then CIWG before Non-CIWG')}
      ${btn('m3','③ Economy › Branch › College','All CIWG (₹) first, then branch priority, then top colleges')}
    </div>
    <div class="intel-row"><span class="tbl-label">Branch priority (◀ higher · ▶ lower):</span><div class="prio" id="brPrio"></div></div>
    <div class="intel-row"><span class="tbl-label">Choice-list template:</span>
      <button class="imode" onclick="downloadTemplate()" title="Download the current choice list as an editable CSV template">⬇ Download template (CSV)</button>
      <button class="imode" onclick="document.getElementById('tmplFile').click()" title="Upload an edited template to rebuild the choice list in that exact order">⬆ Upload template</button>
      <input type="file" id="tmplFile" accept=".csv,text/csv" style="display:none" onchange="uploadTemplate(this.files[0]);this.value=''">
      <span id="tmplMsg" style="font-size:.72rem;color:var(--ink2)"></span>
    </div>
  </div>`;
}
function rowHTML(p,idx,both,r,v){
  const d=dByName(p.name);const f=d?fit(d.name,p.brCode,p.cat,r,v):"na";const cc=p.cat;
  const badge=both?`<button class="catb ${cc}" onclick="flipCat('${esc(p.name)}','${p.brCode}','${cc}')" title="Switch CIWG (C ₹) ⇄ Non-CIWG (NC $)">${CATL[cc]}</button>`:`<span class="cattag ${cc}">${CATL[cc]}</span>`;
  const isR=closeReal(p.name,p.brCode,cc);
  const meta=d?`<div class="pmeta">${nrLong(d.name,d.nirf)} · ${CATF[cc]} ${isR?'<b style="color:var(--good)">DASA 2025 close</b>':'~est close'} CRL ${estClose(d.name,p.brCode,cc).toLocaleString()}</div>`:"";
  const pos=`<span class="movectrl noprint"><button class="mvbtn" onclick="nudge(${idx},-1)" title="Move up (towards choice #1)" aria-label="Move up">▲</button><input class="posin" type="number" min="1" max="${ordered.length}" value="${idx+1}" onchange="moveToPos(${idx},this.value)" onclick="this.select()" title="Type a position to move this choice there"><button class="mvbtn" onclick="nudge(${idx},1)" title="Move down" aria-label="Move down">▼</button></span>`;
  return `<div class="nm"><div class="nmtop">${p.name} <small>${BRN[p.brCode]}</small> ${badge}</div>${meta}</div><span class="fit ${f}">${f==="na"?"—":f}</span>${pos}<button class="px noprint" onclick="removeP('${esc(p.name)}','${p.brCode}','${cc}')">✕</button>`;
}
function nudge(idx,dir){const j=idx+dir;if(j<0||j>=ordered.length)return;const t=ordered[idx];ordered[idx]=ordered[j];ordered[j]=t;recompute();}
function renderFlat(){
  const r=R(),v=V(),both=stuCat()==="BOTH";
  let html=`<div class="flatbar noprint"><b>${selRows.size}</b> selected · move to # <input class="posin" type="number" min="1" id="selPos" style="width:64px"> <button class="clearf" onclick="moveSelTo(document.getElementById('selPos').value)">Go</button> <button class="clearf" onclick="moveSelStep(-1)">▲ up</button> <button class="clearf" onclick="moveSelStep(1)">▼ down</button> <button class="clearf" onclick="clearSel()">clear</button> <span style="color:var(--ink2);font-size:.72rem">tip: tick rows then drag any ticked row to move them together</span></div>`;
  html+=`<div class="flatlist" id="flatList">`;
  ordered.forEach((p,idx)=>{const k=pkey(p);const sel=selRows.has(k);
    html+=`<div class="prow flat ${sel?'sel':''}" draggable="true" data-key="${k}"><span class="drag" title="Drag to reorder">⠿</span><input type="checkbox" class="selchk" ${sel?'checked':''} onclick="toggleSel('${k}')"><div class="pn">${idx+1}</div>${rowHTML(p,idx,both,r,v)}</div>`;});
  html+=`</div>`;
  document.getElementById("rounds").innerHTML=intelPanel()+html;
  renderBrPriority();wireDrag();
}
function wireDrag(){
  const list=document.getElementById("flatList");if(!list)return;
  list.querySelectorAll(".prow.flat").forEach(row=>{
    row.addEventListener("dragstart",e=>{const k=row.dataset.key;dragKeys=selRows.has(k)&&selRows.size?[...selRows]:[k];e.dataTransfer.effectAllowed="move";row.classList.add("dragging");});
    row.addEventListener("dragend",()=>{row.classList.remove("dragging");list.querySelectorAll(".drop-into").forEach(x=>x.classList.remove("drop-into"));});
    row.addEventListener("dragover",e=>{e.preventDefault();row.classList.add("drop-into");});
    row.addEventListener("dragleave",()=>row.classList.remove("drop-into"));
    row.addEventListener("drop",e=>{e.preventDefault();const target=row.dataset.key;if(dragKeys.length&&!dragKeys.includes(target))moveItems(dragKeys,target);dragKeys=[];});
  });
}
function renderRounds(){
  const r=R(),v=V(),both=stuCat()==="BOTH";
  const totalChoices=ordered.length, universe=D.reduce((n,d)=>n+d.br.length,0);
  if(!ordered.length && !droppedLog.length){
    document.getElementById("rounds").innerHTML=intelPanel()+'<div class="empty">No choices yet. Tap <b>📥 Load all institutes &amp; branches</b> above to start from the full DASA list, or add specific programs in Section 2 — then <b>Auto-arrange</b>.</div>';
    renderBrPriority();return;
  }
  if(intelMode!=='tier'){renderFlat();return;}
  const dropByTier={1:[],2:[],3:[],4:[]};
  droppedLog.forEach(x=>{const d=dByName(x.name);const t=(r&&d)?TIEROF[fit(d.name,x.brCode,x.cat,r,v)]:4;dropByTier[t].push(x);});
  let html=`<div class="tiersum noprint"><span><b>${totalChoices}</b> choices in tiers${droppedLog.length?` · <b style="color:var(--warn)">${droppedLog.length} dropped</b>`:''} · full DASA universe = <b>${universe}</b> programs</span>`;
  if(droppedLog.length)html+=`<button class="clearf" onclick="restoreAllDropped()" title="Bring every dropped branch back">↺ Restore all dropped (${droppedLog.length})</button>`;
  html+=`</div>`;
  TIERMETA.forEach(([t,label,col,desc])=>{
    const items=ordered.map((p,idx)=>({p,idx})).filter(o=>o.p.tier===t);
    const drops=dropByTier[t];
    if(!items.length && !drops.length) return;
    const brSet=[...new Set(items.map(o=>o.p.brCode))];
    const chipsHtml=brSet.map(c=>`<button class="tbchip" onclick="dropBranch(${t},'${c}')" title="Remove all ${BRN[c]} from this tier">${BRN[c]} \u2715</button>`).join("");
    const ts=tierSort[t]||'nirf';
    const sortSel=`<select class="tsort noprint" onchange="sortTier(${t},this.value)" title="Sort programs within this tier"><option value="nirf"${ts==='nirf'?' selected':''}>NIRF rank (default)</option><option value="ciwg"${ts==='ciwg'?' selected':''}>CIWG (C ₹) first, then NIRF</option><option value="nciwg"${ts==='nciwg'?' selected':''}>Non-CIWG (NC $) first, then NIRF</option></select>`;
    html+=`<div class="round"><div class="rhead"><span class="rtag" style="color:${col}">${label}</span><span class="rcount">${items.length}</span>${items.length?sortSel:''}</div><div class="rdesc">${desc}</div>`;
    if(brSet.length)html+=`<div class="tbchips"><span class="tbl-label">Branches — tap \u2715 to drop:</span>${chipsHtml}</div>`;
    if(drops.length){
      const drBr=[...new Set(drops.map(x=>x.brCode))];
      const rHtml=drBr.map(c=>`<button class="tbchip restore" onclick="restoreTier(${t})" title="Restore dropped ${BRN[c]} to this tier">\u21ba ${BRN[c]}</button>`).join("");
      html+=`<div class="tbchips restore-row"><span class="tbl-label">Dropped — tap \u21ba to restore:</span>${rHtml}<button class="clearf" onclick="restoreTier(${t})">\u21ba Restore all here</button></div>`;
    }
    html+=`<div class="rbody">`;
    if(!items.length)html+=`<div class="empty" style="margin:4px 0">All branches in this tier were dropped — use \u21ba above to bring them back.</div>`;
    items.forEach(({p,idx})=>{html+=`<div class="prow"><div class="pn">${idx+1}</div>${rowHTML(p,idx,both,r,v)}</div>`;});
    html+="</div></div>";
  });
  document.getElementById("rounds").innerHTML=intelPanel()+html;
  renderBrPriority();
}
function moveOrd(i,dir){const j=i+dir;if(j<0||j>=ordered.length)return;const nt=ordered[j].tier;[ordered[i],ordered[j]]=[ordered[j],ordered[i]];ordered[j].tier=nt;recompute();}
function removeP(name,b,cat){picks=picks.filter(p=>!(p.name===name&&p.brCode===b&&p.cat===cat));ordered=ordered.filter(p=>!(p.name===name&&p.brCode===b&&p.cat===cat));recompute();}
function pkey(p){return p.name+"|"+p.brCode+"|"+p.cat;}
function dropBranch(t,code){
  const tg=ordered.filter(o=>o.tier===t&&o.brCode===code);
  tg.forEach(o=>{const k=pkey(o);if(!droppedLog.some(x=>pkey(x)===k))droppedLog.push({name:o.name,brCode:o.brCode,cat:o.cat});});
  const keys=tg.map(pkey);
  picks=picks.filter(p=>!keys.includes(pkey(p)));
  ordered=ordered.filter(o=>!keys.includes(pkey(o)));
  recompute();
}
/* Restore a single dropped program back into the list */
function restoreOne(name,brCode,cat){
  droppedLog=droppedLog.filter(x=>!(x.name===name&&x.brCode===brCode&&x.cat===cat));
  if(!picks.some(p=>p.name===name&&p.brCode===brCode&&p.cat===cat))picks.push({name,brCode,cat});
  recompute();
}
/* Restore every program that was dropped from a given tier (by current rank-fit) */
function restoreTier(t){
  const r=R(),v=V();
  const back=droppedLog.filter(x=>{const d=dByName(x.name);return d&&TIEROF[fit(d.name,x.brCode,x.cat,r,v)]===t;});
  back.forEach(x=>{if(!picks.some(p=>p.name===x.name&&p.brCode===x.brCode&&p.cat===x.cat))picks.push({name:x.name,brCode:x.brCode,cat:x.cat});});
  const bk=back.map(pkey);droppedLog=droppedLog.filter(x=>!bk.includes(pkey(x)));
  recompute();
}
/* Restore everything that was ever dropped */
function restoreAllDropped(){
  droppedLog.forEach(x=>{if(!picks.some(p=>p.name===x.name&&p.brCode===x.brCode&&p.cat===x.cat))picks.push({name:x.name,brCode:x.brCode,cat:x.cat});});
  droppedLog=[];recompute();
}
/* Load the entire DASA universe (all institutes × all branches) at the chosen seat category,
   so every student starts from the same complete list — counsellors then prune via drop. */
function loadAll(){
  const sc=stuCat();const cats=sc==="BOTH"?["CIWG","NCIWG"]:[sc];
  D.forEach(d=>allowedBr(d).forEach(b=>cats.forEach(c=>{if(!F.excl.has(d.name)&&!picks.some(p=>p.name===d.name&&p.brCode===b&&p.cat===c))picks.push({name:d.name,brCode:b,cat:c});})));
  droppedLog=[];autoArrange();
}
function flipCat(name,b,cur){const nw=cur==="CIWG"?"NCIWG":"CIWG";
  if(has(name,b,nw)){alert("This program is already in your list as "+CATF[nw]+". CIWG and Non-CIWG are separate choices.");return;}
  const np=picks.find(p=>p.name===name&&p.brCode===b&&p.cat===cur);if(np)np.cat=nw;
  const no=ordered.find(o=>o.name===name&&o.brCode===b&&o.cat===cur);if(no)no.cat=nw;recompute();}

function renderCoverage(){
  const considered=d=>!F.excl.has(d.name);
  let zc="";
  ZONES.forEach(z=>{const inst=D.filter(d=>d.zone===z&&considered(d));const chosen=inst.filter(d=>picks.some(p=>p.name===d.name)).length;
    const pct=inst.length?Math.round(chosen/inst.length*100):0;const gap=inst.length&&chosen===0;
    zc+=`<div class="zcard ${gap?'gap':''}"><h4>${z}</h4><div class="zb"><i style="width:${pct}%"></i></div><small>${chosen}/${inst.length} institutes · ${pct}%${gap?' · ⚠ none':''}</small></div>`;});
  document.getElementById("zoneCards").innerHTML=zc;
  let html="<tr><th>NIRF</th><th>Institute</th><th>Type</th><th>State</th><th>In list (branch · category)</th></tr>";
  ZONES.forEach(z=>{
    const inst=D.filter(d=>d.zone===z&&considered(d)).sort((a,b)=>nrSortKey(a.name)-nrSortKey(b.name)||a.name.localeCompare(b.name));
    if(!inst.length)return;
    html+=`<tr class="zoneh"><td colspan="5">${z} Zone — ${inst.length} institutes</td></tr>`;
    inst.forEach(d=>{const ch=picks.filter(p=>p.name===d.name);const miss=ch.length===0;
      html+=`<tr class="${miss?'miss':''}"><td>${nrShort(d.name,d.nirf)}</td><td>${d.name}</td><td>${d.type}</td><td>${d.state}</td><td>${miss?'<b style="color:var(--warn)">MISSING</b>':ch.map(p=>BRN[p.brCode]+' <span class="cattag '+p.cat+'">'+CATL[p.cat]+'</span>').join("  ")}</td></tr>`;});
  });
  document.getElementById("covTbl").innerHTML=html;
  const excl=[...F.excl].map(dByName).filter(Boolean).sort((a,b)=>nrSortKey(a.name)-nrSortKey(b.name)||a.name.localeCompare(b.name));
  const wrap=document.getElementById("exclWrap");
  if(excl.length){wrap.style.display="block";document.getElementById("exclCount").textContent="("+excl.length+")";
    let eh="<tr><th>NIRF</th><th>Institute</th><th>Type</th><th>Zone</th><th>State</th><th class='noprint'></th></tr>";
    excl.forEach(d=>{eh+=`<tr><td>${nrShort(d.name,d.nirf)}</td><td>${d.name}</td><td>${d.type}</td><td>${d.zone}</td><td>${d.state}</td><td class='noprint'><button class="clearf" onclick="removeExcl('${esc(d.name)}')">restore</button></td></tr>`;});
    document.getElementById("exclTbl").innerHTML=eh;
  }else{wrap.style.display="none";}
}

function allotAt(v){
  const r=R();const list=ordered.length?ordered:picks.map(p=>({...p,tier:4}));
  const rows=list.map((p,i)=>{const d=dByName(p.name);if(!d)return null;const k=ratioK(d.name,p.brCode,p.cat,r,v);
    return {pos:i+1,name:p.name,br:p.brCode,cat:p.cat,nirf:d.nirf,zone:d.zone,close:estClose(d.name,p.brCode,p.cat),k,prob:probOf(k),qual:k<=1};}).filter(Boolean);
  return {rows,predicted:rows.find(x=>x.qual)||null,reachable:rows.filter(x=>x.k<=1.15)};
}
function renderAllot(){
  const v=V();document.getElementById("curVar").textContent=v+"%";document.getElementById("barVar").textContent=v+"%";
  const r=R();const {predicted,rows}=allotAt(v);
  const pb=document.getElementById("predictBox");
  if(!r){pb.innerHTML='<div class="predict none"><div class="pl">Enter a CRL rank to predict allotment</div></div>';document.getElementById("barPred").textContent="—";}
  else if(predicted){const isR=closeReal(predicted.name,predicted.br,predicted.cat);
    pb.innerHTML=`<div class="predict"><div class="pl">Most likely allotment @ ${v}% variation — first choice (top→bottom) you clear</div><div class="pbig">Choice #${predicted.pos} · ${predicted.name} — ${BRN[predicted.br]} <span class="cattag ${predicted.cat}">${CATL[predicted.cat]}</span></div><div style="font-size:.78rem;color:var(--ink2);margin-top:4px">${nrLong(predicted.name,predicted.nirf)} · ${predicted.zone} · ${isR?'<b style="color:var(--good)">DASA 2025</b>':'~est.'} close CRL ${predicted.close.toLocaleString()} · your rank ${r.toLocaleString()}</div></div>`;document.getElementById("barPred").textContent="#"+predicted.pos+" "+predicted.name.slice(0,15);}
  else{pb.innerHTML='<div class="predict none"><div class="pl">No safe allotment predicted</div><div class="pbig">Your list is all Reach / Dream at this variation</div><div style="font-size:.78rem;color:var(--ink2);margin-top:4px">Add Safe choices below your reaches, or you risk going seatless.</div></div>';document.getElementById("barPred").textContent="none";}
  // Top 10 likely allotments, ordered by CHOICE PREFERENCE (Pref# ascending), then last-year closing
  const top=rows.filter(x=>x.k<=1.15).sort((a,b)=>a.pos-b.pos||a.close-b.close).slice(0,10);
  let html='<tr><th>Pref&nbsp;#</th><th>Choice</th><th>Institute</th><th>Cat</th><th>NIRF</th><th>Last-yr Close CRL</th><th>Fit</th></tr>';
  if(!top.length)html+='<tr><td colspan="7" style="text-align:center;color:var(--ink2)">No likely allotments — add more Safe choices.</td></tr>';
  top.forEach((x)=>{const ft=x.k<=0.95?"safe":x.k<=1.05?"reach":"dream";
    const isPred=predicted&&x.pos===predicted.pos;const isR=closeReal(x.name,x.br,x.cat);
    html+=`<tr${isPred?' class="predrow"':''}><td class="mono">${x.pos}${isPred?' ⭐':''}</td><td>${BRN[x.br]}</td><td>${x.name}</td><td><span class="cattag ${x.cat}">${CATL[x.cat]}</span></td><td>${nrShort(x.name,x.nirf)}</td><td class="mono">${x.close.toLocaleString()}${isR?'':' ~'}</td><td><span class="fit ${ft}">${ft}</span></td></tr>`;});
  document.getElementById("top10Tbl").innerHTML=html;
}

const VARS=[0,5,10,15,20,25,30];
function renderSensitivity(){
  let html="<tr><th>Variation</th><th>Predicted best allotment</th><th>Cat</th><th>Pref #</th><th>Reachable</th></tr>";const counts=[];
  VARS.forEach(v=>{const {predicted,reachable}=allotAt(v);counts.push(reachable.length);
    html+=`<tr><td><b>${v}%</b></td><td>${predicted?predicted.name+" — "+BRN[predicted.br]:'<span style="color:var(--warn)">none</span>'}</td><td>${predicted?'<span class="cattag '+predicted.cat+'">'+CATL[predicted.cat]+'</span>':'—'}</td><td>${predicted?'#'+predicted.pos:'—'}</td><td>${reachable.length}</td></tr>`;});
  document.getElementById("sensTbl").innerHTML=html;
  if(charts.sens)charts.sens.destroy();
  if(typeof Chart!=="undefined")charts.sens=new Chart(document.getElementById("sensChart"),{type:"line",data:{labels:VARS.map(v=>v+"%"),datasets:[{label:"Reachable seats",data:counts,borderColor:getCss('--orange'),backgroundColor:"rgba(238,116,36,.15)",fill:true,tension:.3,pointRadius:4}]},options:chartOpts(true)});
  renderVarTop10();
}
function renderVarTop10(){
  const v=parseInt(document.getElementById("vSel").value,10);const {rows}=allotAt(v);
  const top=rows.filter(x=>x.k<=1.15).sort((a,b)=>a.pos-b.pos||a.close-b.close).slice(0,10);
  let html=`<tr><th colspan="6">Top 10 potential allotments @ ${v}% variation — in your choice preference order</th></tr><tr><th>Pref&nbsp;#</th><th>Choice</th><th>Institute</th><th>Cat</th><th>Close @ ${v}%</th><th>Fit</th></tr>`;
  if(!top.length)html+='<tr><td colspan="6" style="text-align:center;color:var(--ink2)">None likely at this variation.</td></tr>';
  top.forEach((x)=>{const ce=Math.round(x.close*(1+v/100));html+=`<tr><td class="mono">${x.pos}</td><td>${BRN[x.br]}</td><td>${x.name}</td><td><span class="cattag ${x.cat}">${CATL[x.cat]}</span></td><td class="mono">${ce.toLocaleString()}</td><td><span class="fit ${x.k<=0.95?"safe":x.k<=1.05?"reach":"dream"}">${x.k<=0.95?"safe":x.k<=1.05?"reach":"dream"}</span></td></tr>`;});
  document.getElementById("varTop10").innerHTML=html;
}

function getCss(v){return getComputedStyle(document.querySelector('.ported')||document.documentElement).getPropertyValue(v).trim()||"#EE7424";}
function chartOpts(legend){return {responsive:true,maintainAspectRatio:false,plugins:{legend:{display:!!legend,labels:{color:getCss('--ink'),font:{size:10}}}},scales:{x:{ticks:{color:getCss('--ink2'),font:{size:9}},grid:{display:false}},y:{ticks:{color:getCss('--ink2'),font:{size:9}},grid:{color:getCss('--line')},beginAtZero:true}}};}
function fitCounts(){const r=R(),v=V();const c={safe:0,reach:0,dream:0,na:0};picks.forEach(p=>{const d=dByName(p.name);if(d)c[fit(d.name,p.brCode,p.cat,r,v)]++;});return c;}
function renderVisuals(){
  const cmap={safe:getCss('--good'),reach:getCss('--reach'),dream:getCss('--dream'),na:getCss('--line')};
  let cells="";const c=fitCounts();
  ["safe","reach","dream","na"].forEach(k=>{for(let i=0;i<c[k];i++)cells+=`<span class="wc" style="background:${cmap[k]}" title="${k}"></span>`;});
  document.getElementById("waffle").innerHTML=cells||'<small style="color:var(--ink2)">No choices yet.</small>';
  document.getElementById("waffleLeg").textContent=`Safe ${c.safe} · Reach ${c.reach} · Dream ${c.dream}${c.na?' · Unscored '+c.na:''}`;
  const nb={t25:0,r50:0,r100:0,r200:0,r300:0,nr:0};picks.forEach(p=>{nb[realNirf(p.name)]++;});
  const nbKeys=Object.keys(nb).filter(k=>nb[k]>0);
  if(charts.nirf)charts.nirf.destroy();
  if(typeof Chart!=="undefined"){
    charts.nirf=new Chart(document.getElementById("nirfChart"),{type:"doughnut",data:{labels:nbKeys.map(k=>RBL[k]),datasets:[{data:nbKeys.map(k=>nb[k]),backgroundColor:[getCss('--good'),getCss('--reach'),getCss('--amber'),getCss('--orange'),getCss('--dream'),getCss('--ink2')]}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{position:"right",labels:{color:getCss('--ink'),font:{size:9},boxWidth:10}}}}});
    const tc=[0,0,0,0];ordered.forEach(p=>tc[p.tier-1]++);
    if(charts.tier)charts.tier.destroy();
    charts.tier=new Chart(document.getElementById("tierChart"),{type:"bar",data:{labels:["Dream","Reach","Safe","Unscored"],datasets:[{label:"Choices",data:tc,backgroundColor:[getCss('--dream'),getCss('--reach'),getCss('--good'),getCss('--ink2')]}]},options:chartOpts(false)});
  }
  drawZoneSchem();drawTreemap();
}
function drawZoneSchem(){
  const el=document.getElementById("zoneschem");if(typeof d3==="undefined"){el.innerHTML="";return;}
  const data=ZONES.map(z=>{const inst=D.filter(d=>d.zone===z);const chosen=inst.filter(d=>picks.some(p=>p.name===d.name)).length;return{z,chosen,total:inst.length};});
  const W=el.clientWidth||320,H=170,bw=W/6,mx=Math.max(...data.map(z=>z.total));
  el.innerHTML="";const svg=d3.select(el).append("svg").attr("viewBox",`0 0 ${W} ${H}`);
  data.forEach((d,i)=>{const x=i*bw+4,bh=(H-34)*(d.total/mx),fh=bh*(d.chosen/d.total||0);
    svg.append("rect").attr("x",x).attr("y",H-22-bh).attr("width",bw-8).attr("height",bh).attr("rx",4).attr("fill",getCss('--line'));
    svg.append("rect").attr("x",x).attr("y",H-22-fh).attr("width",bw-8).attr("height",fh).attr("rx",4).attr("fill",d.chosen?getCss('--orange'):getCss('--warn'));
    svg.append("text").attr("x",x+(bw-8)/2).attr("y",H-8).attr("text-anchor","middle").attr("font-size",9).attr("fill",getCss('--ink2')).text(d.z.slice(0,5));
    svg.append("text").attr("x",x+(bw-8)/2).attr("y",H-26-bh).attr("text-anchor","middle").attr("font-size",9).attr("font-weight",700).attr("fill",getCss('--ink')).text(d.chosen+"/"+d.total);});
}
function drawTreemap(){
  const el=document.getElementById("treemap");if(typeof d3==="undefined"){el.innerHTML="";return;}
  el.innerHTML="";if(!picks.length){el.innerHTML='<small style="color:var(--ink2)">Add choices to see the spread.</small>';return;}
  const byZone={};picks.forEach(p=>{const d=dByName(p.name);if(!d)return;byZone[d.zone]=byZone[d.zone]||{};byZone[d.zone][d.type]=(byZone[d.zone][d.type]||0)+1;});
  const root={name:"root",children:Object.keys(byZone).map(z=>({name:z,children:Object.keys(byZone[z]).map(t=>({name:z+" · "+t,value:byZone[z][t]}))}))};
  const W=el.clientWidth||600,H=240;
  const h=d3.hierarchy(root).sum(d=>d.value).sort((a,b)=>b.value-a.value);
  d3.treemap().size([W,H]).padding(2)(h);
  const zc={North:getCss('--orange'),South:getCss('--reach'),East:getCss('--good'),West:getCss('--amber'),Central:getCss('--dream'),Northeast:getCss('--navy')};
  const svg=d3.select(el).append("svg").attr("viewBox",`0 0 ${W} ${H}`);
  const leaf=svg.selectAll("g").data(h.leaves()).join("g").attr("transform",d=>`translate(${d.x0},${d.y0})`);
  leaf.append("rect").attr("width",d=>d.x1-d.x0).attr("height",d=>d.y1-d.y0).attr("rx",4).attr("fill",d=>zc[d.data.name.split(" · ")[0]]||getCss('--ink2')).attr("opacity",.88);
  leaf.append("text").attr("x",5).attr("y",15).attr("font-size",10).attr("fill","#fff").attr("font-weight",700).text(d=>(d.x1-d.x0>54)?d.data.name:"");
  leaf.append("text").attr("x",5).attr("y",28).attr("font-size",10).attr("fill","#fff").text(d=>(d.x1-d.x0>40&&d.y1-d.y0>30)?d.value:"");
}

function renderInsights(){
  const r=R(),v=V();const c=fitCounts();const total=picks.length;const ul=document.getElementById("insights");const cat=stuCat();
  if(!total){ul.innerHTML='<li><span class="ic">📝</span><div>Add choices and enter a rank to generate analysis.</div></li>';return;}
  const I=[];
  I.push(["","📋",`Your list has <b>${total}</b> choices: ${c.dream} Dream, ${c.reach} Reach, ${c.safe} Safe${c.na?', '+c.na+' unscored':''}.`]);
  if(!r)I.push(["warn","⚠️","No CRL rank entered — rank-fit and allotment predictions are inactive."]);
  const {predicted}=allotAt(v);
  if(r&&predicted)I.push(["good","🎯",`At ${v}% variation, most likely allotment is choice #${predicted.pos}: <b>${predicted.name} — ${BRN[predicted.br]}</b> (${CATF[predicted.cat]}, ~close CRL ${predicted.close.toLocaleString()}).`]);
  if(r&&!predicted)I.push(["warn","🚨","No qualifying (safe) choice at this variation — the list is all Reach/Dream. High risk of no allotment."]);
  if(r&&c.safe===0)I.push(["warn","🛟","Zero <b>Safe</b> choices. Always anchor the bottom of your list with seats you'll almost certainly clear."]);
  if(r&&c.dream/total>=0.5)I.push(["warn","⚖️","Over half your list is <b>Dream</b>. A top-heavy list often ends seatless."]);
  const mz=ZONES.filter(z=>!picks.some(p=>{const d=dByName(p.name);return d&&d.zone===z;}));
  if(mz.length)I.push(["","🧭",`No choices from <b>${mz.join(", ")}</b> zone${mz.length>1?'s':''}.`]);
  if(r){const preds=VARS.map(vv=>{const p=allotAt(vv).predicted;return p?p.pos:null;}).filter(x=>x);
    if(preds.length){const sp=Math.max(...preds)-Math.min(...preds);
      I.push([sp<=4?"good":"",sp<=4?"🟢":"🔀",sp<=4?`Robust — predicted allotment barely moves (pref #${Math.min(...preds)}–#${Math.max(...preds)}) across 0–30% variation.`:`Predicted allotment swings pref #${Math.min(...preds)}→#${Math.max(...preds)} across scenarios — sensitive to cutoff movement.`]);}}
  const nC=picks.filter(p=>p.cat==="CIWG").length,nN=picks.filter(p=>p.cat==="NCIWG").length;
  if(cat==="BOTH")I.push(["","🪪",`Double-tag mix: <b>${nC} CIWG</b> · <b>${nN} Non-CIWG</b>. CIWG seats here are modelled to close ~${Math.round((CAT_MULT.CIWG-1)*100)}% easier than Non-CIWG, so the same program can be Safe as CIWG yet Reach as Non-CIWG. List both to maximise options; balance refunded if finally admitted under CIWG.`]);
  else if(cat==="CIWG")I.push(["","🪪","CIWG-only (₹62,500 + $300). Keep parent's Gulf visa/work-permit & employer letter ready — if CIWG status isn't established at verification you may need to opt for Non-CIWG."]);
  ul.innerHTML=I.map(([cls,ic,txt])=>`<li class="${cls}"><span class="ic">${ic}</span><div>${txt}</div></li>`).join("");
}

function renderStamp(){
  const ok=document.getElementById("revOk").checked,by=document.getElementById("revBy").value||"—",ver=document.getElementById("revVer").value||"v1.0",dt=document.getElementById("revDate").value||new Date().toISOString().slice(0,10);
  const s=document.getElementById("stamp");s.classList.toggle("show",ok);
  s.innerHTML=`✓ REVIEWED &amp; APPROVED<small>${ver} · ${dt} · ${by}</small>`;
  const nm=document.getElementById("fName").value||"—";
  document.getElementById("repMeta").innerHTML=`Student: <b>${nm}</b><br>CRL: <b>${R()||'—'}</b> · Category: <b>${STUCAT[stuCat()]}</b> · Variation: <b>${V()}%</b><br>Reviewed: <b>${ok?ver+' · '+dt+' · '+by:'pending'}</b><br>${new Date().toLocaleDateString('en-GB',{day:'2-digit',month:'short',year:'numeric'})}`;
}

function exportCsv(){
  let list=(ordered.length?ordered:picks.map(p=>({...p,tier:4}))).slice()
    .sort((a,b)=>a.tier-b.tier||nrSortKey(a.name)-nrSortKey(b.name)||a.name.localeCompare(b.name)||a.brCode.localeCompare(b.brCode));
  const r=R(),v=V();
  const e=x=>'"'+String(x==null?"":x).replace(/"/g,'""')+'"';
  const L=[];
  L.push(["EduAakashaa DASA 2026 — Choice-Filling Analysis"].map(e).join(","));
  L.push(["Student",document.getElementById("fName").value,"JEE Main CRL",r,"Seat Category",STUCAT[stuCat()]].map(e).join(","));
  L.push(["Variation assumed",v+"%"].map(e).join(","));
  L.push(["Reviewed by",document.getElementById("revBy").value,"Version",document.getElementById("revVer").value,"Date",document.getElementById("revDate").value,"Approved",document.getElementById("revOk").checked?"Yes":"No"].map(e).join(","));
  L.push(["Counsellor comments",document.getElementById("revCom").value].map(e).join(","));
  L.push("");
  L.push(["Pref#","Tier","Institute","Branch","Category","NIRF","Close CRL (0%)","Close source","Zone","State","Fit@"+v+"%","Qualifies"].map(e).join(","));
  const TN={1:"Dream",2:"Reach",3:"Safe",4:"Unscored"};
  list.forEach((p,i)=>{const d=dByName(p.name);if(!d)return;const k=ratioK(d.name,p.brCode,p.cat,r,v);
    L.push([i+1,TN[p.tier]||p.tier,d.name,BRN[p.brCode],CATF[p.cat],nrShort(d.name,d.nirf),estClose(d.name,p.brCode,p.cat),closeReal(d.name,p.brCode,p.cat)?"DASA 2025 actual":"indicative model",d.zone,d.state,r?fit(d.name,p.brCode,p.cat,r,v):"na",r?(k<=1?"Yes":"No"):"-"].map(e).join(","));});
  L.push("");
  L.push(["Sensitivity — predicted best allotment by variation"].map(e).join(","));
  L.push(["Variation","Predicted","Category","Pref#","Reachable"].map(e).join(","));
  VARS.forEach(vv=>{const {predicted,reachable}=allotAt(vv);L.push([vv+"%",predicted?predicted.name+" — "+BRN[predicted.br]:"none",predicted?CATF[predicted.cat]:"-",predicted?predicted.pos:"-",reachable.length].map(e).join(","));});
  const blob=new Blob([L.join("\n")],{type:"text/csv"});
  const a=document.createElement("a");a.href=URL.createObjectURL(blob);a.download="dasa2026-choice-analysis.csv";a.click();
}

function collegeInList(name){return picks.some(p=>p.name===name);}
function missReason(d){return F.excl.has(d.name)?'<b style="color:var(--warn)">excluded</b>':'not added';}
function missAction(d){return F.excl.has(d.name)?`<button class="clearf" onclick="removeExcl('${esc(d.name)}')">restore</button>`:`<button class="clearf" onclick="addCollege('${esc(d.name)}')">+ add all</button>`;}
function renderMissingTop(){
  const box=document.getElementById("missTop");if(!box)return;
  const ranked=D.filter(d=>typeof NRANK[d.name]==="number").sort((a,b)=>NRANK[a.name]-NRANK[b.name]);
  const miss=ranked.filter(d=>!collegeInList(d.name)).slice(0,15);
  if(!miss.length){box.innerHTML='<div class="impact-none">✓ Every NIRF Top-100 institute in the DASA list has at least one program in your choices.</div>';return;}
  let html=`<table class="tbl"><tr><th>NIRF</th><th>Institute</th><th>Type</th><th>Zone</th><th>Branches offered</th><th>Status</th><th class="noprint"></th></tr>`;
  miss.forEach(d=>{html+=`<tr><td class="mono">#${NRANK[d.name]}</td><td>${d.name}</td><td>${d.type}</td><td>${d.zone}</td><td>${d.br.map(b=>BRN[b]).join(", ")}</td><td class="mono" style="color:var(--ink2)">${missReason(d)}</td><td class="noprint">${missAction(d)}</td></tr>`;});
  html+=`</table>`;box.innerHTML=html;
}
function renderMissingZone(){
  const box=document.getElementById("missZone");if(!box)return;
  const zones=[...new Set(D.map(d=>d.zone))].sort();
  let html="";
  zones.forEach(z=>{
    const ranked=D.filter(d=>d.zone===z).sort((a,b)=>nrSortKey(a.name)-nrSortKey(b.name)||a.name.localeCompare(b.name));
    const miss=ranked.filter(d=>!collegeInList(d.name)).slice(0,5);
    if(!miss.length)return;
    html+=`<div class="zmiss"><div class="zmiss-h">${z} zone — top NIRF institutes not in your list</div><table class="tbl">`;
    html+=miss.map(d=>`<tr><td class="mono">${nrShort(d.name,d.nirf)}</td><td>${d.name}</td><td>${d.type}</td><td>${d.br.map(b=>BRN[b]).join(", ")}</td><td class="mono" style="color:var(--ink2)">${missReason(d)}</td><td class="noprint">${missAction(d)}</td></tr>`).join("");
    html+=`</table></div>`;
  });
  box.innerHTML=html||'<div class="impact-none">✓ Your list already covers the top NIRF institutes in every zone.</div>';
}
let simVar=0;
function setSimVar(v){simVar=v;renderSim();}
function renderSim(){
  const box=document.getElementById("simBox");if(!box)return;
  const vb=document.getElementById("simVarBtns");
  if(vb)vb.innerHTML=[0,10,20,30].map(v=>`<button class="simvar ${v===simVar?'on':''}" onclick="setSimVar(${v})">±${v}%</button>`).join("");
  const r=R();
  if(!r){box.innerHTML='<div class="empty">Enter a CRL rank in Section 1 to run the simulation.</div>';return;}
  const {predicted,rows}=allotAt(simVar);
  if(!rows.length){box.innerHTML='<div class="empty">Add choices (Section 2 or “Load all”) and arrange your list, then run the simulation.</div>';return;}
  const aPos=predicted?predicted.pos:null;
  const isR=x=>closeReal(x.name,x.br,x.cat);
  const stepHTML=x=>{let state,verdict;
    if(aPos&&x.pos<aPos){state='missed';verdict='✗ cut-off tighter than your rank';}
    else if(aPos&&x.pos===aPos){state='allot';verdict='★ SEAT ALLOTTED';}
    else if(aPos&&x.pos>aPos){state='skip';verdict='not reached — secured above';}
    else{state='missed';verdict='✗ cut-off tighter than your rank';}
    const eff=Math.round(x.close*(1+simVar/100));
    return `<div class="simstep ${state}"><div class="ss-n">#${x.pos}</div><div class="ss-main"><div class="ss-title">${x.name} <small>${BRN[x.br]}</small> <span class="cattag ${x.cat}">${CATL[x.cat]}</span></div><div class="ss-meta">close CRL ${x.close.toLocaleString()}${isR(x)?'':' ~'}${simVar?` → @±${simVar}% ${eff.toLocaleString()}`:''} · your rank ${r.toLocaleString()}</div></div><div class="ss-v">${verdict}</div></div>`;};
  let seq=[];
  if(aPos){
    const pre=rows.filter(x=>x.pos<aPos);
    if(pre.length>6){pre.slice(0,3).forEach(x=>seq.push(stepHTML(x)));seq.push(`<div class="simnote">… ${pre.length-5} more choices skipped — every cut-off tighter than your rank …</div>`);pre.slice(-2).forEach(x=>seq.push(stepHTML(x)));}
    else pre.forEach(x=>seq.push(stepHTML(x)));
    seq.push(stepHTML(predicted));
    const post=rows.filter(x=>x.pos>aPos);
    post.slice(0,2).forEach(x=>seq.push(stepHTML(x)));
    if(post.length>2)seq.push(`<div class="simnote">… ${post.length-2} more not reached — your seat is already secured above …</div>`);
  }else{
    rows.slice(0,8).forEach(x=>seq.push(stepHTML(x)));
    if(rows.length>8)seq.push(`<div class="simnote">… ${rows.length-8} more — none cleared at ±${simVar}% …</div>`);
  }
  let html=`<div class="simsteps" id="simSteps">${seq.join('')}</div>`;
  if(predicted){
    const pInst=predicted.name;const higher=rows.filter(x=>x.pos<aPos);
    const slide=higher.filter(x=>x.name===pInst).length,flo=higher.filter(x=>x.name!==pInst).length;
    html+=`<div class="simresult"><div class="sr-l">Simulated Round-I allotment @ ±${simVar}% variation</div><div class="sr-big">Choice #${predicted.pos} · ${predicted.name}</div><div class="sr-sub">${BRN[predicted.br]} · ${CATF[predicted.cat]} · ${nrLong(predicted.name,predicted.nirf)} · close CRL ${predicted.close.toLocaleString()} · your rank ${r.toLocaleString()}</div></div>`;
    html+=`<div class="simhl"><div class="simhl-card freeze"><div class="shc-h">🔒 Freeze</div><div class="shc-n">1</div><div class="shc-d">Lock choice #${predicted.pos} — your allotted seat.</div></div><div class="simhl-card slide"><div class="shc-h">➡ Slide</div><div class="shc-n">${slide}</div><div class="shc-d">Higher-preference option(s) at this same institute you could move up to.</div></div><div class="simhl-card float"><div class="shc-h">🌊 Float</div><div class="shc-n">${flo}</div><div class="shc-d">Higher-preference option(s) at other institutes you could move up to.</div></div></div>`;
  }else{
    html+=`<div class="simresult" style="background:linear-gradient(135deg,var(--red,#C23A3A),#8f2a2a)"><div class="sr-l">Simulated result @ ±${simVar}% variation</div><div class="sr-big">No seat allotted</div><div class="sr-sub">None of your choices' cut-offs are within your rank at this variation. Add Safe choices lower in your list.</div></div>`;
  }
  const trunc=s=>s.length>24?s.slice(0,22)+'…':s;
  html+=`<div class="simvarstrip">`+[0,10,20,30].map(v=>{const p=allotAt(v).predicted;return `<div class="svs ${v===simVar?'cur':''}"><div class="svs-v">±${v}%</div><div class="svs-seat">${p?('#'+p.pos+' '+trunc(p.name)):'—'}</div><div class="svs-sub">${p?BRN[p.br]+' · '+CATL[p.cat]:'no seat'}</div></div>`;}).join('')+`</div>`;
  box.innerHTML=html;
}
function runSim(){
  renderSim();
  const cont=document.getElementById("simSteps");if(!cont)return;
  const steps=[...cont.querySelectorAll('.simstep')];
  steps.forEach(s=>s.classList.add('dimmed'));
  steps.forEach((s,i)=>setTimeout(()=>s.classList.remove('dimmed'),260*i+40));
  const sec=document.getElementById("s15sim");if(sec)sec.scrollIntoView({behavior:"smooth",block:"start"});
}
function renderWillingness(){
  const box=document.getElementById("willBox");if(!box)return;
  const r=R(),v=V();
  if(!r){box.innerHTML='<div class="empty">Enter a CRL rank in Section 1 to map your Freeze / Float / Slide options.</div>';return;}
  const {predicted,rows}=allotAt(v);
  if(!predicted){box.innerHTML='<div class="predict none"><div class="pl">No seat predicted at '+v+'% variation</div><div class="pbig">Add a few Safe choices so DASA can allot a seat to freeze, float or slide from.</div></div>';return;}
  const pInst=predicted.name;
  const higher=rows.filter(x=>x.pos<predicted.pos);
  const slide=higher.filter(x=>x.name===pInst);
  const flo=higher.filter(x=>x.name!==pInst);
  const tbl=(arr,same)=>{
    if(!arr.length)return '<div class="empty" style="margin:4px 0">None — your allotted seat is already your top preference'+(same?' at this institute':'')+'.</div>';
    let h='<table class="tbl"><tr><th>Pref&nbsp;#</th><th>Choice</th><th>Institute</th><th>Cat</th><th>NIRF</th><th>Last-yr Close CRL</th><th>Fit</th></tr>';
    arr.forEach(x=>{const ft=x.k<=0.95?'safe':x.k<=1.05?'reach':'dream';const isR=closeReal(x.name,x.br,x.cat);
      h+=`<tr><td class="mono">${x.pos}</td><td>${BRN[x.br]}</td><td>${x.name}</td><td><span class="cattag ${x.cat}">${CATL[x.cat]}</span></td><td>${nrShort(x.name,x.nirf)}</td><td class="mono">${x.close.toLocaleString()}${isR?'':' ~'}</td><td><span class="fit ${ft}">${ft}</span></td></tr>`;});
    return h+'</table>';
  };
  const isR=closeReal(predicted.name,predicted.br,predicted.cat);
  let html=`<div class="predict"><div class="pl"><span class="willpill freeze">Freeze</span> Your predicted Round-I seat — Freeze to lock this in</div><div class="pbig">Choice #${predicted.pos} · ${predicted.name} — ${BRN[predicted.br]} <span class="cattag ${predicted.cat}">${CATL[predicted.cat]}</span></div><div style="font-size:.78rem;color:var(--ink2);margin-top:4px">${nrLong(predicted.name,predicted.nirf)} · ${isR?'DASA 2025':'~est.'} close CRL ${predicted.close.toLocaleString()} · your rank ${r.toLocaleString()}</div></div>`;
  html+=`<div class="willgrp"><h4><span class="willpill slide">Slide</span> Higher preferences at the SAME institute — ${pInst}</h4>${tbl(slide,true)}</div>`;
  html+=`<div class="willgrp"><h4><span class="willpill float">Float</span> Higher preferences at OTHER institutes</h4>${tbl(flo,false)}</div>`;
  html+=`<p class="subt" style="margin-top:10px"><b>Freeze</b> → you keep choice #${predicted.pos}, done. <b>Slide</b> → DASA may upgrade you to a same-institute option above in the next round. <b>Float</b> → it may upgrade you to any higher option above (any institute). In every case your #${predicted.pos} seat stays safe if nothing better opens. These upgrade options are the choices you listed <em>above</em> your predicted seat, so ordering your list well matters.</p>`;
  box.innerHTML=html;
}
function renderImpact(){
  const box=document.getElementById("impactBox");if(!box)return;
  const r=R(),v=V(),ac=addCat();
  const q=(document.getElementById("q")?document.getElementById("q").value:"").toLowerCase().trim();
  const universe=D.reduce((n,d)=>n+d.br.length,0);
  const comboCount=keep=>{let n=0;D.forEach(d=>d.br.forEach(b=>{if(keep(d,b))n++;}));return n;};
  const defs=[];
  if(F.type.size) defs.push(["College type",[...F.type].join(", "),(d,b)=>F.type.has(d.type)]);
  if(F.nirf.size) defs.push(["NIRF band",[...F.nirf].map(k=>RBL[k]).join(", "),(d,b)=>F.nirf.has(realNirf(d.name))]);
  if(F.zone.size) defs.push(["Zone",[...F.zone].join(", "),(d,b)=>F.zone.has(d.zone)]);
  if(F.state.size) defs.push(["State",[...F.state].join(", "),(d,b)=>F.state.has(d.state)]);
  if(F.br.size) defs.push(["Branch",[...F.br].map(c=>BRN[c]).join(", "),(d,b)=>F.br.has(b)]);
  if(F.fit.size) defs.push(["Rank-fit",[...F.fit].map(k=>FITL[k]).join(", "),(d,b)=>r?F.fit.has(fit(d.name,b,ac,r,v)):true]);
  if(F.excl.size) defs.push(["Excluded colleges",F.excl.size+" college"+(F.excl.size>1?"s":""),(d,b)=>!F.excl.has(d.name)]);
  if(F.xcat.size) defs.push(["Excluded program types",[...F.xcat].map(k=>XCATL[k]).join(", "),(d,b)=>brAllowed(b)]);
  if(q) defs.push(["Search text",'"'+q+'"',(d,b)=>d.name.toLowerCase().includes(q)||d.state.toLowerCase().includes(q)]);

  if(!defs.length){
    box.innerHTML=`<div class="impact-none">✓ No filters applied — all <b>${universe}</b> programs (institute × branch) are in view. With no filters and a rank entered, every student starts from this same total; rank only changes which tier each program lands in.</div>`;
    return;
  }
  if(F.fit.size&&!r) defs.find(x=>x[0]==="Rank-fit")[1]+=" — inactive (no CRL rank)";

  let rows=defs.map(([name,sel,keep])=>{const remaining=comboCount(keep);return [name,sel,universe-remaining,remaining];})
    .sort((a,b)=>b[2]-a[2]);
  const combinedKeep=(d,b)=>defs.every(([,,k])=>k(d,b));
  const combinedRemaining=comboCount(combinedKeep);
  const combinedRemoved=universe-combinedRemaining;

  let html=`<table class="tbl impact-tbl"><tr><th>Filter</th><th>Selection</th><th>Programs hidden (of ${universe})</th><th>%</th></tr>`;
  rows.forEach(([name,sel,removed])=>{
    const pct=universe?Math.round(removed/universe*100):0;
    html+=`<tr><td><b>${name}</b></td><td>${sel}</td><td><span class="imp-bar"><i style="width:${pct}%"></i></span> removes <b>${removed}</b> of ${universe}</td><td class="mono">${pct}%</td></tr>`;
  });
  html+=`</table>`;
  const cpct=universe?Math.round(combinedRemoved/universe*100):0;
  html+=`<div class="impact-sum"><div><span class="mono">COMBINED EFFECT</span><div class="big">${combinedRemaining} <small>of ${universe} programs remain</small></div></div><div class="impact-rem"><b>${combinedRemoved}</b> removed · <b>${cpct}%</b> of the universe hidden by the current filter set</div></div>`;
  box.innerHTML=html;
}

function recompute(){
  const sc=stuCat();
  document.getElementById("addAsWrap").style.display=sc==="BOTH"?"":"none";
  if(sc!=="BOTH"){picks.forEach(p=>p.cat=sc);ordered.forEach(o=>o.cat=sc);}
  // dedupe (coercing categories can collapse a C ₹ + NC $ pair into one)
  const seen=new Set();picks=picks.filter(p=>{const k=p.name+"|"+p.brCode+"|"+p.cat;if(seen.has(k))return false;seen.add(k);return true;});
  const seo=new Set();ordered=ordered.filter(o=>{const k=o.name+"|"+o.brCode+"|"+o.cat;if(seo.has(k))return false;seo.add(k);return true;});
  document.getElementById("pc").textContent=picks.length;
  document.getElementById("varV").textContent=V()+"%";
  ordered=ordered.filter(p=>picks.some(x=>x.name===p.name&&x.brCode===p.brCode&&x.cat===p.cat));
  const r=R(),v=V();
  picks.forEach(p=>{if(!ordered.some(o=>o.name===p.name&&o.brCode===p.brCode&&o.cat===p.cat)){const d=dByName(p.name);const t=(r&&d)?TIEROF[fit(d.name,p.brCode,p.cat,r,v)]:4;ordered.push({name:p.name,brCode:p.brCode,cat:p.cat,tier:t});}});
  renderList();renderRounds();renderCoverage();renderAllot();renderSensitivity();renderVisuals();renderInsights();renderStamp();renderImpact();renderMissingTop();renderMissingZone();renderWillingness();renderSim();
}
function toggleTheme(){dark=!dark;document.documentElement.dataset.theme=dark?"dark":"light";document.getElementById("themeBtn").textContent=dark?"☀️":"🌙";setTimeout(recompute,30);}

document.documentElement.dataset.theme=dark?"dark":"light";
document.getElementById("themeBtn").textContent=dark?"☀️":"🌙";
document.getElementById("revDate").value=new Date().toISOString().slice(0,10);
initFilters();recompute();
