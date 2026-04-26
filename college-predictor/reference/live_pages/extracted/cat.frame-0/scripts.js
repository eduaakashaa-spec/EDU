
document.addEventListener("DOMContentLoaded", function() {

// === SCHEDULE ===
var sched = [
  {d:"Jul 15-26, 2026",t:"Official Notification",desc:"IIM Indore releases CAT 2026 notification",hi:false},
  {d:"Aug 1, 2026",t:"Registration Opens",desc:"Online registration begins at iimcat.ac.in",hi:false},
  {d:"Sep 20, 2026",t:"Registration Closes",desc:"Last date to complete application and pay fees",hi:false},
  {d:"Nov 12, 2026",t:"Admit Card Available",desc:"Download with centre, slot and reporting time",hi:false},
  {d:"Nov 29, 2026",t:"CAT 2026 EXAM DAY",desc:"Morning 8:30, Afternoon 12:30, Evening 4:30",hi:true},
  {d:"Dec 5-7, 2026",t:"Answer Key Released",desc:"Official answer key and objection window",hi:false},
  {d:"Dec 20, 2026",t:"Results Declared",desc:"Percentile scores on iimcat.ac.in",hi:false},
  {d:"Jan-Mar 2027",t:"WAT/PI Rounds",desc:"IIM shortlists, interviews, final selection",hi:false}
];
var sg = document.getElementById("schedGrid");
sched.forEach(function(s){
  sg.innerHTML += '<div style="background:'+(s.hi?'rgba(232,98,26,0.15)':'rgba(255,255,255,0.05)')+';border-left:4px solid '+(s.hi?'#D4A853':'#E8621A')+';border-radius:6px;padding:12px 16px;"><div style="font-size:11px;color:'+(s.hi?'#D4A853':'#E8621A')+';font-weight:700;letter-spacing:1px;">'+s.d+'</div><div style="color:#fff;font-weight:700;font-size:14px;margin:2px 0;">'+s.t+'</div><div style="color:rgba(255,255,255,0.45);font-size:12px;">'+s.desc+'</div></div>';
});

// === RANKINGS ===
var ranks = [
  {r:1,n:"IIM Ahmedabad",m:"Score: 83.29 | Gujarat",a:"Rs 35.22 LPA",h:"Rs 1.10 Cr",f:"Rs 25L"},
  {r:2,n:"IIM Bangalore",m:"Score: 78.5 | Karnataka",a:"Rs 34.88 LPA",h:"Rs 1.0 Cr",f:"Rs 26.3L"},
  {r:3,n:"IIM Kozhikode",m:"Score: 72.1 | Kerala",a:"Rs 30+ LPA",h:"Rs 67 LPA",f:"Rs 22L"},
  {r:4,n:"IIT Delhi (DMS)",m:"Top non-IIM | Delhi",a:"Rs 28+ LPA",h:"Rs 50+ LPA",f:"Rs 10L"},
  {r:5,n:"IIM Lucknow",m:"Gained 2 ranks | UP",a:"Rs 32+ LPA",h:"Rs 72 LPA",f:"Rs 21L"},
  {r:6,n:"IIM Mumbai",m:"Formerly NITIE | Maharashtra",a:"Rs 29 LPA",h:"Rs 54 LPA",f:"Rs 22L"},
  {r:7,n:"IIM Calcutta",m:"Estd. 1961 | W. Bengal",a:"Rs 35 LPA",h:"Rs 1.15 Cr",f:"Rs 31L"},
  {r:8,n:"IIM Indore",m:"Retained rank | MP",a:"Rs 26+ LPA",h:"Rs 50+ LPA",f:"Rs 21L"},
  {r:9,n:"MDI Gurgaon",m:"Top private | Haryana",a:"Rs 26+ LPA",h:"Rs 42 LPA",f:"Rs 25L"},
  {r:10,n:"SIBM Pune",m:"New in Top 10 | Symbiosis",a:"Rs 22+ LPA",h:"Rs 35 LPA",f:"Rs 22L"}
];
var rg = document.getElementById("rankGrid");
ranks.forEach(function(r){
  rg.innerHTML += '<div style="background:#fff;border:1px solid #E8E3DA;border-radius:10px;padding:16px;position:relative;overflow:hidden;"><div style="position:absolute;top:0;left:0;right:0;height:3px;background:linear-gradient(90deg,#E8621A,#D4A853);"></div><div style="display:inline-flex;align-items:center;justify-content:center;width:30px;height:30px;border-radius:6px;background:#1B3A5C;color:#fff;font-weight:700;font-size:13px;margin-bottom:8px;">'+r.r+'</div><div style="font-weight:700;font-size:15px;margin-bottom:3px;">'+r.n+'</div><div style="font-size:11px;color:#5A6B7D;margin-bottom:8px;">'+r.m+'</div><div style="display:flex;gap:14px;flex-wrap:wrap;"><div><div style="font-size:9px;color:#5A6B7D;text-transform:uppercase;letter-spacing:1px;">Avg</div><div style="font-weight:700;font-size:14px;color:#1B3A5C;">'+r.a+'</div></div><div><div style="font-size:9px;color:#5A6B7D;text-transform:uppercase;letter-spacing:1px;">Highest</div><div style="font-weight:700;font-size:14px;color:#1B3A5C;">'+r.h+'</div></div><div><div style="font-size:9px;color:#5A6B7D;text-transform:uppercase;letter-spacing:1px;">Fees</div><div style="font-weight:700;font-size:14px;color:#1B3A5C;">'+r.f+'</div></div></div></div>';
});

// === TABS HELPER ===
function makeTabs(tabsId, contentId, items) {
  var te = document.getElementById(tabsId);
  var ce = document.getElementById(contentId);
  items.forEach(function(item, idx) {
    var b = document.createElement("button");
    b.textContent = item.label;
    b.style.cssText = "padding:7px 14px;border-radius:6px;border:1px solid "+(idx===0?"#1B3A5C":"#E8E3DA")+";background:"+(idx===0?"#1B3A5C":"#fff")+";color:"+(idx===0?"#fff":"#5A6B7D")+";cursor:pointer;font-size:13px;font-weight:600;font-family:Arial,sans-serif;";
    b.addEventListener("click", function() {
      var bs = te.children;
      for(var i=0;i<bs.length;i++){bs[i].style.background="#fff";bs[i].style.color="#5A6B7D";bs[i].style.borderColor="#E8E3DA";}
      this.style.background="#1B3A5C";this.style.color="#fff";this.style.borderColor="#1B3A5C";
      var ps = ce.children;
      for(var i=0;i<ps.length;i++) ps[i].style.display="none";
      ps[idx].style.display="block";
    });
    te.appendChild(b);
    var p = document.createElement("div");
    p.style.display = idx===0?"block":"none";
    p.innerHTML = item.html;
    ce.appendChild(p);
  });
  ce.addEventListener("click", function(e) {
    if(e.target.classList.contains("sopt")){e.target.style.borderColor="#27AE60";e.target.style.background="rgba(39,174,96,0.08)";e.target.style.color="#2E7D32";e.target.style.fontWeight="700";}
  });
}

// === SAMPLE Q ===
makeTabs("sampleTabs","sampleContent",[
  {label:"VARC",html:'<div style="background:rgba(255,255,255,0.06);border-radius:10px;padding:16px;margin-bottom:10px;"><div style="display:inline-block;padding:2px 8px;border-radius:4px;background:rgba(21,101,192,0.15);color:#90CAF9;font-size:10px;font-weight:700;margin-bottom:8px;">Reading Comprehension</div><div style="color:#fff;font-weight:700;margin-bottom:8px;font-size:14px;">The author\'s primary purpose is to:</div><div style="display:grid;grid-template-columns:1fr 1fr;gap:6px;margin-bottom:8px;"><div class="sopt" style="padding:8px;border-radius:5px;font-size:12px;border:1px solid rgba(255,255,255,0.15);color:rgba(255,255,255,0.7);cursor:pointer;">A) Argue traditional models are obsolete</div><div class="sopt" style="padding:8px;border-radius:5px;font-size:12px;border:1px solid rgba(255,255,255,0.15);color:rgba(255,255,255,0.7);cursor:pointer;">B) Describe management history</div><div class="sopt" style="padding:8px;border-radius:5px;font-size:12px;border:1px solid rgba(255,255,255,0.15);color:rgba(255,255,255,0.7);cursor:pointer;">C) Compare East/West practices</div><div class="sopt" style="padding:8px;border-radius:5px;font-size:12px;border:1px solid rgba(255,255,255,0.15);color:rgba(255,255,255,0.7);cursor:pointer;">D) Explain tech on hiring</div></div><div style="padding:8px;background:rgba(39,174,96,0.1);border-radius:6px;font-size:12px;color:#81C784;">RC tests your ability to identify main arguments. Practice reading editorials daily.</div></div>'},
  {label:"DILR",html:'<div style="background:rgba(255,255,255,0.06);border-radius:10px;padding:16px;margin-bottom:10px;"><div style="display:inline-block;padding:2px 8px;border-radius:4px;background:rgba(230,81,0,0.15);color:#FFAB91;font-size:10px;font-weight:700;margin-bottom:8px;">Data Interpretation</div><div style="color:#fff;font-weight:700;margin-bottom:8px;font-size:14px;">Revenue: Rs 200Cr(2022), 250Cr(2023), 312.5Cr(2024). CAGR?</div><div style="display:grid;grid-template-columns:1fr 1fr;gap:6px;margin-bottom:8px;"><div class="sopt" style="padding:8px;border-radius:5px;font-size:12px;border:1px solid rgba(255,255,255,0.15);color:rgba(255,255,255,0.7);cursor:pointer;">A) 25%</div><div class="sopt" style="padding:8px;border-radius:5px;font-size:12px;border:1px solid rgba(255,255,255,0.15);color:rgba(255,255,255,0.7);cursor:pointer;">B) 20%</div><div class="sopt" style="padding:8px;border-radius:5px;font-size:12px;border:1px solid rgba(255,255,255,0.15);color:rgba(255,255,255,0.7);cursor:pointer;">C) 30%</div><div class="sopt" style="padding:8px;border-radius:5px;font-size:12px;border:1px solid rgba(255,255,255,0.15);color:rgba(255,255,255,0.7);cursor:pointer;">D) 15%</div></div><div style="padding:8px;background:rgba(39,174,96,0.1);border-radius:6px;font-size:12px;color:#81C784;">CAGR = (312.5/200)^(1/2) - 1 = 25%.</div></div>'},
  {label:"QA",html:'<div style="background:rgba(255,255,255,0.06);border-radius:10px;padding:16px;margin-bottom:10px;"><div style="display:inline-block;padding:2px 8px;border-radius:4px;background:rgba(46,125,50,0.15);color:#A5D6A7;font-size:10px;font-weight:700;margin-bottom:8px;">Arithmetic</div><div style="color:#fff;font-weight:700;margin-bottom:8px;font-size:14px;">Train 150m passes pole in 15s. Time to pass 300m platform?</div><div style="display:grid;grid-template-columns:1fr 1fr;gap:6px;margin-bottom:8px;"><div class="sopt" style="padding:8px;border-radius:5px;font-size:12px;border:1px solid rgba(255,255,255,0.15);color:rgba(255,255,255,0.7);cursor:pointer;">A) 30s</div><div class="sopt" style="padding:8px;border-radius:5px;font-size:12px;border:1px solid rgba(255,255,255,0.15);color:rgba(255,255,255,0.7);cursor:pointer;">B) 35s</div><div class="sopt" style="padding:8px;border-radius:5px;font-size:12px;border:1px solid rgba(255,255,255,0.15);color:rgba(255,255,255,0.7);cursor:pointer;">C) 45s</div><div class="sopt" style="padding:8px;border-radius:5px;font-size:12px;border:1px solid rgba(255,255,255,0.15);color:rgba(255,255,255,0.7);cursor:pointer;">D) 50s</div></div><div style="padding:8px;background:rgba(39,174,96,0.1);border-radius:6px;font-size:12px;color:#81C784;">Speed=10m/s. Distance=450m. Time=45 seconds.</div></div>'}
]);

// === CUTOFF TABS ===
makeTabs("matTabs","matContent",[
  {label:"CAT Cutoffs",html:'<div style="overflow-x:auto;border-radius:8px;border:1px solid #E8E3DA;"><table style="width:100%;border-collapse:collapse;font-size:12px;"><tr style="background:#1B3A5C;color:#fff;"><th style="padding:8px;text-align:left;font-size:10px;">Institute</th><th style="padding:8px;">Cat</th><th style="padding:8px;">2023</th><th style="padding:8px;">2024</th><th style="padding:8px;">2025</th><th style="padding:8px;">Trend</th></tr><tr><td style="padding:6px 8px;border-bottom:1px solid #E8E3DA;">IIM Ahmedabad</td><td style="padding:6px;border-bottom:1px solid #E8E3DA;">Gen</td><td style="padding:6px;border-bottom:1px solid #E8E3DA;">99+</td><td style="padding:6px;border-bottom:1px solid #E8E3DA;">99+</td><td style="padding:6px;border-bottom:1px solid #E8E3DA;">99+</td><td style="padding:6px;border-bottom:1px solid #E8E3DA;"><span style="background:#E3F2FD;color:#1565C0;padding:1px 6px;border-radius:3px;font-size:10px;font-weight:700;">Stable</span></td></tr><tr style="background:rgba(27,58,92,0.03);"><td style="padding:6px 8px;border-bottom:1px solid #E8E3DA;">IIM Bangalore</td><td style="padding:6px;border-bottom:1px solid #E8E3DA;">Gen</td><td style="padding:6px;border-bottom:1px solid #E8E3DA;">99+</td><td style="padding:6px;border-bottom:1px solid #E8E3DA;">99+</td><td style="padding:6px;border-bottom:1px solid #E8E3DA;">99+</td><td style="padding:6px;border-bottom:1px solid #E8E3DA;"><span style="background:#E3F2FD;color:#1565C0;padding:1px 6px;border-radius:3px;font-size:10px;font-weight:700;">Stable</span></td></tr><tr><td style="padding:6px 8px;border-bottom:1px solid #E8E3DA;">IIM Lucknow</td><td style="padding:6px;border-bottom:1px solid #E8E3DA;">Gen</td><td style="padding:6px;border-bottom:1px solid #E8E3DA;">97+</td><td style="padding:6px;border-bottom:1px solid #E8E3DA;">98+</td><td style="padding:6px;border-bottom:1px solid #E8E3DA;">98+</td><td style="padding:6px;border-bottom:1px solid #E8E3DA;"><span style="background:#FFF3E0;color:#E65100;padding:1px 6px;border-radius:3px;font-size:10px;font-weight:700;">Rising</span></td></tr><tr style="background:rgba(27,58,92,0.03);"><td style="padding:6px 8px;border-bottom:1px solid #E8E3DA;">IIM Indore</td><td style="padding:6px;border-bottom:1px solid #E8E3DA;">Gen</td><td style="padding:6px;border-bottom:1px solid #E8E3DA;">95+</td><td style="padding:6px;border-bottom:1px solid #E8E3DA;">96+</td><td style="padding:6px;border-bottom:1px solid #E8E3DA;">97+</td><td style="padding:6px;border-bottom:1px solid #E8E3DA;"><span style="background:#FFF3E0;color:#E65100;padding:1px 6px;border-radius:3px;font-size:10px;font-weight:700;">Rising</span></td></tr><tr><td style="padding:6px 8px;border-bottom:1px solid #E8E3DA;">FMS Delhi</td><td style="padding:6px;border-bottom:1px solid #E8E3DA;">Gen</td><td style="padding:6px;border-bottom:1px solid #E8E3DA;">98+</td><td style="padding:6px;border-bottom:1px solid #E8E3DA;">98+</td><td style="padding:6px;border-bottom:1px solid #E8E3DA;">98+</td><td style="padding:6px;border-bottom:1px solid #E8E3DA;"><span style="background:#E3F2FD;color:#1565C0;padding:1px 6px;border-radius:3px;font-size:10px;font-weight:700;">Stable</span></td></tr></table></div>'},
  {label:"Placements",html:'<div style="overflow-x:auto;border-radius:8px;border:1px solid #E8E3DA;"><table style="width:100%;border-collapse:collapse;font-size:12px;"><tr style="background:#1B3A5C;color:#fff;"><th style="padding:8px;text-align:left;font-size:10px;">Institute</th><th style="padding:8px;">Year</th><th style="padding:8px;">Avg</th><th style="padding:8px;">Highest</th><th style="padding:8px;">Top Recruiters</th></tr><tr><td style="padding:6px 8px;border-bottom:1px solid #E8E3DA;font-weight:700;">IIM-A</td><td style="padding:6px;border-bottom:1px solid #E8E3DA;">2025</td><td style="padding:6px;border-bottom:1px solid #E8E3DA;">35.22L</td><td style="padding:6px;border-bottom:1px solid #E8E3DA;">1.10Cr</td><td style="padding:6px;border-bottom:1px solid #E8E3DA;">BCG, Accenture, Bain</td></tr><tr style="background:rgba(27,58,92,0.03);"><td style="padding:6px 8px;border-bottom:1px solid #E8E3DA;font-weight:700;">IIM-B</td><td style="padding:6px;border-bottom:1px solid #E8E3DA;">2025</td><td style="padding:6px;border-bottom:1px solid #E8E3DA;">34.88L</td><td style="padding:6px;border-bottom:1px solid #E8E3DA;">1.0Cr+</td><td style="padding:6px;border-bottom:1px solid #E8E3DA;">Accenture, McKinsey</td></tr><tr><td style="padding:6px 8px;border-bottom:1px solid #E8E3DA;font-weight:700;">IIM-C</td><td style="padding:6px;border-bottom:1px solid #E8E3DA;">2025</td><td style="padding:6px;border-bottom:1px solid #E8E3DA;">35L+</td><td style="padding:6px;border-bottom:1px solid #E8E3DA;">1.15Cr</td><td style="padding:6px;border-bottom:1px solid #E8E3DA;">BCG, Goldman</td></tr><tr style="background:rgba(27,58,92,0.03);"><td style="padding:6px 8px;border-bottom:1px solid #E8E3DA;font-weight:700;">IIM-M</td><td style="padding:6px;border-bottom:1px solid #E8E3DA;">2025</td><td style="padding:6px;border-bottom:1px solid #E8E3DA;">29L+</td><td style="padding:6px;border-bottom:1px solid #E8E3DA;">54L</td><td style="padding:6px;border-bottom:1px solid #E8E3DA;">Accenture, PwC</td></tr></table></div><p style="margin-top:8px;font-size:11px;color:#5A6B7D;">Source: Official IIM placement reports. All top IIMs achieved 100% placement.</p>'}
]);

// === NEWS ===
var news = [
  {d:"March 2026",t:"CAT 2025 Scorecards Available Until Dec 31, 2026",b:"Download from iimcat.ac.in."},
  {d:"February 2026",t:"IIM-A 2025: 100% Placement, Rs 35.22L Average",b:"BCG top recruiter. BFSI offered Rs 1.10 Cr highest."},
  {d:"January 2026",t:"IIM-B: 660 Offers from 177 Recruiters",b:"Average Rs 34.88L. Consulting 41%. 22 international offers."},
  {d:"September 2025",t:"NIRF 2025: IIM Ahmedabad #1 for 6th Year",b:"Score 83.29. MDI Gurgaon entered top 10."},
  {d:"Expected July 2026",t:"CAT 2026 Notification Expected",b:"Expected July 15-26 on iimcat.ac.in. IIM Indore to conduct."}
];
var nc = document.getElementById("newsCards");
news.forEach(function(n){
  nc.innerHTML += '<div style="background:#fff;border-radius:10px;padding:14px;border-left:4px solid #E8621A;margin-bottom:8px;"><div style="font-size:10px;color:#E8621A;font-weight:700;letter-spacing:1px;text-transform:uppercase;">'+n.d+'</div><div style="font-weight:700;margin:3px 0;font-size:14px;">'+n.t+'</div><div style="color:#5A6B7D;font-size:12px;">'+n.b+'</div></div>';
});

// === QUIZ ===
var qData = [
  {q:"When solving a business problem, what excites you most?",o:[{t:"Analyzing financial data",s:"Finance"},{t:"Creating marketing campaigns",s:"Marketing"},{t:"Optimizing processes",s:"Operations"},{t:"Building and leading teams",s:"HR"}]},
  {q:"Which reading material do you enjoy?",o:[{t:"Financial newspapers",s:"Finance"},{t:"Brand stories",s:"Marketing"},{t:"Tech trends",s:"Analytics"},{t:"Case studies",s:"Strategy"}]},
  {q:"Your natural role in a group project?",o:[{t:"Number cruncher",s:"Finance"},{t:"Creative designer",s:"Marketing"},{t:"Task organizer",s:"Operations"},{t:"Direction setter",s:"Strategy"}]},
  {q:"What career impact do you want?",o:[{t:"Grow company investments",s:"Finance"},{t:"Build loved brands",s:"Marketing"},{t:"Data-driven decisions",s:"Analytics"},{t:"Social enterprise impact",s:"Social"}]},
  {q:"Which skill to develop most?",o:[{t:"Financial modeling",s:"Finance"},{t:"Digital marketing",s:"Marketing"},{t:"Supply chain mgmt",s:"Operations"},{t:"Data analytics and ML",s:"Analytics"}]},
  {q:"Dream company environment?",o:[{t:"McKinsey/BCG/Bain",s:"Strategy"},{t:"Goldman Sachs",s:"Finance"},{t:"Google/Amazon",s:"Analytics"},{t:"HUL/P&G/ITC",s:"Marketing"}]},
  {q:"Math comfort level?",o:[{t:"Love calculus/stats",s:"Finance"},{t:"Good with applied math",s:"Operations"},{t:"Basic stats ok",s:"Analytics"},{t:"Prefer qualitative",s:"Marketing"}]},
  {q:"MBA motivation?",o:[{t:"Higher salary",s:"Finance"},{t:"Business network",s:"Strategy"},{t:"Launch startup",s:"Entrepreneur"},{t:"Switch to mgmt",s:"Operations"}]},
  {q:"First elective choice?",o:[{t:"Corporate Finance",s:"Finance"},{t:"Brand Strategy",s:"Marketing"},{t:"Business Analytics",s:"Analytics"},{t:"Supply Chain Design",s:"Operations"}]},
  {q:"Daily CAT prep hours?",o:[{t:"4-6 hrs (committed)",s:"High"},{t:"2-4 hrs (balanced)",s:"Medium"},{t:"1-2 hrs (flexible)",s:"Low"},{t:"Variable bursts",s:"Medium"}]}
];
var cq=0, ans=[];
var pg=document.getElementById("qProg"), qb=document.getElementById("qBody");

function drawDots(){
  pg.innerHTML="";
  for(var i=0;i<qData.length;i++){
    var d=document.createElement("div");
    d.style.cssText="flex:1;height:4px;border-radius:2px;background:"+(i<cq?"#27AE60":i===cq?"#E8621A":"#E8E3DA")+";";
    pg.appendChild(d);
  }
}
function renderQ(){
  if(cq>=qData.length){showRes();return;}
  drawDots();
  var q=qData[cq];
  var h='<div style="font-size:12px;color:#5A6B7D;margin-bottom:6px;">Question '+(cq+1)+' of '+qData.length+'</div>';
  h+='<div style="font-size:20px;font-weight:bold;margin-bottom:16px;line-height:1.4;">'+q.q+'</div>';
  h+='<div style="display:flex;flex-direction:column;gap:8px;">';
  for(var i=0;i<q.o.length;i++){
    h+='<div class="qopt" data-i="'+i+'" style="border:2px solid #E8E3DA;border-radius:8px;padding:12px;cursor:pointer;display:flex;align-items:center;gap:10px;font-size:14px;"><div style="width:24px;height:24px;border-radius:50%;border:2px solid #E8E3DA;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:11px;color:#5A6B7D;flex-shrink:0;">'+String.fromCharCode(65+i)+'</div><span>'+q.o[i].t+'</span></div>';
  }
  h+='</div>';
  h+='<div style="display:flex;justify-content:space-between;align-items:center;margin-top:18px;"><button id="qBack" style="padding:7px 16px;border:1px solid #E8E3DA;background:#fff;border-radius:6px;cursor:pointer;font-family:Arial;font-weight:600;font-size:13px;'+(cq===0?'opacity:0.3;cursor:not-allowed;':'')+'">Back</button><span style="font-size:13px;color:#5A6B7D;">'+(cq+1)+'/'+qData.length+'</span><div></div></div>';
  qb.innerHTML=h;
  qb.querySelectorAll(".qopt").forEach(function(el){
    el.addEventListener("click",function(){
      var idx=parseInt(this.getAttribute("data-i"));
      ans[cq]=qData[cq].o[idx].s;
      qb.querySelectorAll(".qopt").forEach(function(x){x.style.borderColor="#E8E3DA";x.style.background="#fff";});
      this.style.borderColor="#E8621A";this.style.background="rgba(232,98,26,0.06)";
      setTimeout(function(){cq++;renderQ();},300);
    });
  });
  var bk=document.getElementById("qBack");
  if(bk) bk.addEventListener("click",function(){if(cq>0){cq--;renderQ();}});
}
function showRes(){
  drawDots();
  var cnt={};
  ans.forEach(function(a){if(a!=="High"&&a!=="Medium"&&a!=="Low")cnt[a]=(cnt[a]||0)+1;});
  var s=Object.entries(cnt).sort(function(a,b){return b[1]-a[1];});
  var top=s[0]?s[0][0]:"Strategy", sec=s[1]?s[1][0]:"Marketing";
  var rm={
    Finance:"Finance MBA at IIM Ahmedabad, Calcutta, or Bangalore. Investment banking, PE, corporate finance careers.",
    Marketing:"Marketing MBA at IIM Ahmedabad, Lucknow, or XLRI. Brand management, digital marketing careers.",
    Operations:"Operations MBA at IIM Mumbai, Bangalore. Supply chain, logistics, manufacturing careers.",
    Analytics:"Business Analytics MBA at IIM Bangalore (PGPBA), Calcutta, ISB. Data science, product management careers.",
    Strategy:"Strategy MBA at IIM Ahmedabad, Bangalore, Kozhikode. Management consulting, business strategy careers.",
    HR:"HR MBA at XLRI Jamshedpur, IIM Lucknow, TISS. HR leadership, talent management careers.",
    Social:"Social Enterprise MBA at IRMA, IIM Bangalore, TISS. Social impact and rural management careers.",
    Entrepreneur:"Entrepreneurship MBA at IIM Ahmedabad, Bangalore, ISB. Build and scale your own venture."
  };
  var prep=ans[9]||"Medium";
  var pm=prep==="High"?"Excellent! Target 99+ with 6-8 months focused prep.":prep==="Medium"?"Good balance. Target 8-10 months. Focus on mocks.":"Build gradually with 12-month plan and coaching.";
  qb.innerHTML='<div style="background:linear-gradient(135deg,#1B3A5C,#2A5A8C);color:#fff;border-radius:14px;padding:24px;text-align:center;max-width:550px;margin:0 auto;"><div style="font-size:11px;letter-spacing:2px;text-transform:uppercase;opacity:0.5;margin-bottom:4px;">Your Ideal MBA Path</div><div style="font-size:38px;color:#D4A853;font-weight:bold;">'+top+'</div><div style="font-size:14px;opacity:0.7;margin:4px 0 16px;">Secondary: <strong>'+sec+'</strong></div><div style="text-align:left;background:rgba(255,255,255,0.1);border-radius:8px;padding:14px;margin-bottom:10px;"><h4 style="color:#D4A853;margin:0 0 4px;font-size:14px;">Recommended Path</h4><p style="font-size:13px;opacity:0.85;margin:0;line-height:1.5;">'+(rm[top]||rm.Strategy)+'</p></div><div style="text-align:left;background:rgba(255,255,255,0.1);border-radius:8px;padding:14px;margin-bottom:14px;"><h4 style="color:#D4A853;margin:0 0 4px;font-size:14px;">Preparation</h4><p style="font-size:13px;opacity:0.85;margin:0;">'+pm+'</p></div><div style="display:flex;gap:10px;justify-content:center;flex-wrap:wrap;"><button id="retake" style="background:#E8621A;color:#fff;border:none;padding:10px 20px;border-radius:8px;font-weight:700;cursor:pointer;font-size:13px;font-family:Arial;">Retake Test</button><a href="https://www.eduaakashaa.in" target="_blank" style="background:#D4A853;color:#1A1A2E;padding:10px 20px;border-radius:8px;font-weight:700;text-decoration:none;font-size:13px;">Get Counselling</a></div></div>';
  document.getElementById("retake").addEventListener("click",function(){cq=0;ans=[];renderQ();});
}
renderQ();

});


// ---- next <script> block ----


	const heightObserver = new ResizeObserver(([{ contentRect }]) => {
		window.parent.postMessage({ action: 'iframeHeightUpdated', height: contentRect.height, id: 'zgxaBa' }, '*');
	});

	heightObserver.observe(document.documentElement);
