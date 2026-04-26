
var D=new Date();
var E=[
{id:1,n:"JEE Main 2026 (Session 1)",b:"NTA",t:"National",st:"All India",d:"Jan 21-29, 2026",sd:"2026-01-21",m:1,sr:"B.Tech/B.E.",i:"31 NITs, 25 IIITs, 28 GFTIs"},
{id:2,n:"JEE Main 2026 (Session 2)",b:"NTA",t:"National",st:"All India",d:"Apr 2-8, 2026",sd:"2026-04-02",m:4,sr:"B.Tech/B.E.",i:"31 NITs, 25 IIITs, 28 GFTIs"},
{id:3,n:"JEE Main Paper 2 B.Arch (S1)",b:"NTA",t:"Architecture",st:"All India",d:"Jan 29, 2026",sd:"2026-01-29",m:1,sr:"B.Arch",i:"NITs, IIITs B.Arch"},
{id:4,n:"JEE Main Paper 2 B.Arch (S2)",b:"NTA",t:"Architecture",st:"All India",d:"Apr 7, 2026",sd:"2026-04-07",m:4,sr:"B.Arch",i:"NITs, IIITs B.Arch"},
{id:5,n:"JEE Advanced 2026",b:"IIT Roorkee",t:"National",st:"All India",d:"May 2026 (Tent.)",sd:"2026-05-17",m:5,sr:"B.Tech/B.E.",i:"23 IITs"},
{id:6,n:"BITSAT 2026 (Session 1)",b:"BITS Pilani",t:"Private",st:"All India",d:"Apr 15-16, 2026",sd:"2026-04-15",m:4,sr:"B.Tech/B.E.",i:"BITS Pilani, Goa, Hyderabad"},
{id:7,n:"BITSAT 2026 (Session 2)",b:"BITS Pilani",t:"Private",st:"All India",d:"May 24-26, 2026",sd:"2026-05-24",m:5,sr:"B.Tech/B.E.",i:"BITS Pilani, Goa, Hyderabad"},
{id:8,n:"VITEEE 2026",b:"VIT Vellore",t:"Private",st:"Tamil Nadu",d:"Apr 28-May 3, 2026",sd:"2026-04-28",m:4,sr:"B.Tech/B.E.",i:"VIT Vellore, Chennai, AP, Bhopal"},
{id:9,n:"SRMJEEE 2026",b:"SRM University",t:"Private",st:"Tamil Nadu",d:"Apr 23-25, Jun 10-15, Jul 4-5",sd:"2026-04-23",m:4,sr:"B.Tech/B.E.",i:"SRM Institute of Science & Tech"},
{id:10,n:"MET 2026 (Phase 1)",b:"Manipal Academy",t:"Private",st:"Karnataka",d:"Apr 13-14, 2026",sd:"2026-04-13",m:4,sr:"B.Tech/B.E.",i:"Manipal Institute of Technology"},
{id:11,n:"MET 2026 (Phase 2)",b:"Manipal Academy",t:"Private",st:"Karnataka",d:"May 23-24, 2026",sd:"2026-05-23",m:5,sr:"B.Tech/B.E.",i:"Manipal Institute of Technology"},
{id:12,n:"AEEE 2026",b:"Amrita Univ.",t:"Private",st:"All India",d:"Apr 24-30, 2026",sd:"2026-04-24",m:4,sr:"B.Tech/B.E.",i:"Amrita Vishwa Vidyapeetham"},
{id:13,n:"KIITEE 2026 (Phase 1)",b:"KIIT University",t:"Private",st:"Odisha",d:"Apr 16-20, 2026",sd:"2026-04-16",m:4,sr:"B.Tech/B.E.",i:"KIIT University Bhubaneswar"},
{id:14,n:"KIITEE 2026 (Phase 2)",b:"KIIT University",t:"Private",st:"Odisha",d:"Jun 4-8, 2026",sd:"2026-06-04",m:6,sr:"B.Tech/B.E.",i:"KIIT University Bhubaneswar"},
{id:15,n:"KLEEE 2026",b:"KLE Tech",t:"Private",st:"Karnataka",d:"Mar 28-31, 2026",sd:"2026-03-28",m:3,sr:"B.Tech/B.E.",i:"KLE Technological University"},
{id:16,n:"KCET 2026",b:"KEA Karnataka",t:"State",st:"Karnataka",d:"Apr 23-24, 2026",sd:"2026-04-23",m:4,sr:"B.Tech/B.E.",i:"200+ Karnataka Engg Colleges"},
{id:17,n:"COMEDK UGET 2026",b:"COMEDK",t:"State",st:"Karnataka",d:"May 9, 2026",sd:"2026-05-09",m:5,sr:"B.Tech/B.E.",i:"181 Private Karnataka Colleges"},
{id:18,n:"MHT CET 2026 (Sess 1)",b:"CET Cell MH",t:"State",st:"Maharashtra",d:"Apr 11-19, 2026",sd:"2026-04-11",m:4,sr:"B.Tech/B.E.",i:"300+ Maharashtra Engg Colleges"},
{id:19,n:"MHT CET 2026 (Sess 2)",b:"CET Cell MH",t:"State",st:"Maharashtra",d:"May 2026",sd:"2026-05-10",m:5,sr:"B.Tech/B.E.",i:"300+ Maharashtra Engg Colleges"},
{id:20,n:"WBJEE 2026",b:"WBJEEB",t:"State",st:"West Bengal",d:"May 24, 2026",sd:"2026-05-24",m:5,sr:"B.Tech/B.E.",i:"100+ West Bengal Engg Colleges"},
{id:21,n:"GUJCET 2026",b:"GSEB Gujarat",t:"State",st:"Gujarat",d:"Mar 29, 2026",sd:"2026-03-29",m:3,sr:"B.Tech/B.E.",i:"Gujarat Govt & Private Colleges"},
{id:22,n:"KEAM 2026",b:"CEE Kerala",t:"State",st:"Kerala",d:"Apr 17-22, 2026",sd:"2026-04-17",m:4,sr:"B.Tech/B.E.",i:"Kerala Engineering Colleges"},
{id:23,n:"TG-EAPCET 2026",b:"TSCHE",t:"State",st:"Telangana",d:"May 9 & 11, 2026",sd:"2026-05-09",m:5,sr:"B.Tech/B.E.",i:"Telangana Engg Colleges"},
{id:24,n:"AP-EAPCET 2026",b:"APSCHE",t:"State",st:"Andhra Pradesh",d:"May 12-15 & 18, 2026",sd:"2026-05-12",m:5,sr:"B.Tech/B.E.",i:"AP Engineering Colleges"},
{id:25,n:"TNEA 2026",b:"Anna University",t:"State",st:"Tamil Nadu",d:"Based on +2 Marks",sd:"2026-06-01",m:6,sr:"B.Tech/B.E.",i:"550+ TN Colleges (No Exam)"},
{id:26,n:"OJEE 2026",b:"OJEE Board",t:"State",st:"Odisha",d:"May 4-9, 2026",sd:"2026-05-04",m:5,sr:"B.Tech/B.E.",i:"Odisha Govt & Private Colleges"},
{id:27,n:"Assam CEE 2026",b:"DTE Assam",t:"State",st:"Assam",d:"Apr 19-20 & Jun 7, 2026",sd:"2026-04-19",m:4,sr:"B.Tech/B.E.",i:"Assam Engineering Colleges"},
{id:28,n:"JKCET 2026",b:"BOPEE",t:"State",st:"Jammu & Kashmir",d:"Apr 19, 2026",sd:"2026-04-19",m:4,sr:"B.Tech/B.E.",i:"J&K Engineering Colleges"},
{id:29,n:"HPCET 2026",b:"HPU",t:"State",st:"Himachal Pradesh",d:"May 10, 2026",sd:"2026-05-10",m:5,sr:"B.Tech/B.E.",i:"HP Engineering Colleges"},
{id:30,n:"CG PET 2026",b:"CG Vyapam",t:"State",st:"Chhattisgarh",d:"May 14, 2026",sd:"2026-05-14",m:5,sr:"B.Tech/B.E.",i:"Chhattisgarh Engg Colleges"},
{id:31,n:"UPSEE/AKTU 2026",b:"AKTU",t:"State",st:"Uttar Pradesh",d:"Via JEE Main Score",sd:"2026-05-01",m:5,sr:"B.Tech/B.E.",i:"UP Engineering Colleges"},
{id:32,n:"CUSAT CAT 2026",b:"Cochin Univ",t:"State",st:"Kerala",d:"May 9-11, 2026",sd:"2026-05-09",m:5,sr:"B.Tech/B.E.",i:"CUSAT Kochi"},
{id:33,n:"CUCET 2026",b:"Central Univs",t:"National",st:"All India",d:"May 1, 2026",sd:"2026-05-01",m:5,sr:"B.Tech/B.E.",i:"Central Universities"},
{id:34,n:"ISI Admission 2026",b:"ISI Kolkata",t:"Research",st:"West Bengal",d:"May 10, 2026",sd:"2026-05-10",m:5,sr:"Research/Science",i:"ISI Kolkata, Bangalore, Delhi"},
{id:35,n:"UGEE 2026 (IIIT-H)",b:"IIIT Hyderabad",t:"Research",st:"Telangana",d:"May 2, 2026",sd:"2026-05-02",m:5,sr:"Research/Science",i:"IIIT Hyderabad"},
{id:36,n:"IAT 2026 (IISER)",b:"IISER",t:"Research",st:"All India",d:"Jun 7, 2026",sd:"2026-06-07",m:6,sr:"Research/Science",i:"7 IISERs across India"},
{id:37,n:"NEST 2026",b:"NISER/CEBS",t:"Research",st:"All India",d:"Jun 6, 2026",sd:"2026-06-06",m:6,sr:"Research/Science",i:"NISER, UM-DAE CEBS"},
{id:38,n:"NID DAT 2026 Prelims",b:"NID",t:"Design",st:"All India",d:"Dec 21, 2025",sd:"2025-12-21",m:12,sr:"B.Des (Design)",i:"7 NID Campuses (B.Des)"},
{id:39,n:"NID DAT B.Des Mains",b:"NID",t:"Design",st:"All India",d:"Apr 19, 2026",sd:"2026-04-19",m:4,sr:"B.Des (Design)",i:"NID Campuses"},
{id:40,n:"NIFT 2026 (Stage 1)",b:"NTA/NIFT",t:"Design",st:"All India",d:"Feb 8, 2026",sd:"2026-02-08",m:2,sr:"B.Des (Design)",i:"19 NIFT Campuses (5076 seats)"},
{id:41,n:"NIFT 2026 (Stage 2)",b:"NIFT",t:"Design",st:"All India",d:"Apr 6-11, 2026",sd:"2026-04-06",m:4,sr:"B.Des (Design)",i:"NIFT Delhi & Campuses"},
{id:42,n:"UCEED 2026",b:"IIT Bombay",t:"Design",st:"All India",d:"Jan 18, 2026",sd:"2026-01-18",m:1,sr:"B.Des (Design)",i:"IIT Bombay, Delhi, Guwahati B.Des"},
{id:43,n:"CEED 2026",b:"IIT Bombay",t:"Design",st:"All India",d:"Jan 18, 2026",sd:"2026-01-18",m:1,sr:"B.Des (Design)",i:"IITs M.Des Programs"},
{id:44,n:"NATA 2026 (Multi-Session)",b:"CoA",t:"Architecture",st:"All India",d:"Mar 7-Jun 28, 2026",sd:"2026-03-07",m:3,sr:"B.Arch",i:"400+ Architecture Colleges"}
];

var P=[];try{P=JSON.parse(localStorage.getItem('ep3')||'[]')}catch(e){}

function gs(sd){var p=sd.split('-'),ed=new Date(+p[0],+p[1]-1,+p[2]),df=Math.ceil((ed-D)/(864e5));if(df<-1)return{s:"Completed",c:"sc-d",k:"✅"};if(df>=-1&&df<=0)return{s:"Today!",c:"sc-w",k:"🔴"};if(df>=1&&df<=7)return{s:"This Week!",c:"sc-w",k:"🔥"};return{s:"Upcoming",c:"sc-u",k:"⏳"}}
function sc(sr){return sr==='B.Tech/B.E.'?'s-engg':sr==='B.Des (Design)'?'s-des':sr==='B.Arch'?'s-arch':'s-res'}
var tc={"National":"#60a5fa","State":"#34d399","Private":"#f472b6","Research":"#fbbf24","Design":"#fb923c","Architecture":"#38bdf8"};

function go(t){document.querySelectorAll('.tp').forEach(function(el){el.classList.remove('on')});document.querySelectorAll('.nb').forEach(function(el){el.classList.remove('on')});document.getElementById('t-'+t).classList.add('on');document.querySelectorAll('.nb').forEach(function(el){if(el.getAttribute('data-t')===t)el.classList.add('on')})}

function R(){
  var s=document.getElementById('fS').value.toLowerCase(),fsr=document.getElementById('fSt').value,ft=document.getElementById('fT').value,fsa=document.getElementById('fSa').value,fx=document.getElementById('fX').value;
  var f=E.filter(function(e){
    if(s&&e.n.toLowerCase().indexOf(s)<0&&e.b.toLowerCase().indexOf(s)<0)return false;
    if(fsr&&e.sr!==fsr)return false;
    if(ft&&e.t!==ft)return false;
    if(fsa&&e.st!==fsa)return false;
    if(fx){var x=gs(e.sd);if(x.s!==fx)return false}
    return true;
  });
  var h='';for(var j=0;j<f.length;j++){var e=f[j],ip=P.some(function(p){return p.id===e.id}),x=gs(e.sd);
    h+='<tr><td class="en">'+e.n+'</td><td style="color:var(--text2);font-size:12px">'+e.b+'</td><td><span class="sb '+sc(e.sr)+'">'+e.sr+'</span></td><td><span class="b b-'+e.t+'">'+e.t+'</span></td><td style="color:var(--text2);font-size:12px">'+e.st+'</td><td style="font-family:ui-monospace,monospace;font-size:12px">'+e.d+'</td><td class="'+x.c+' sc">'+x.k+' '+x.s+'</td><td style="font-size:11px;color:var(--text2);max-width:150px">'+e.i+'</td><td style="white-space:nowrap"><button class="ab" onclick="oS('+e.id+')">📤</button><button class="pb'+(ip?' ad':'')+'" onclick="tP('+e.id+',this)">'+(ip?'✅':'➕')+'</button></td></tr>';
  }
  document.getElementById('tB').innerHTML=h;
  document.getElementById('cT').textContent='Showing '+f.length+' of '+E.length+' exams';
}

function fSt(){var s={};E.forEach(function(e){s[e.st]=1});var el=document.getElementById('fSa'),k=Object.keys(s).sort();for(var j=0;j<k.length;j++){var o=document.createElement('option');o.value=k[j];o.textContent=k[j];el.appendChild(o)}}

function rTL(){
  var ms=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug'],h='';
  for(var mi=0;mi<ms.length;mi++){var mn=mi+1,me=E.filter(function(e){return e.m===mn});
    h+='<div class="tlm"><div class="tlml">'+ms[mi]+' 2026'+(mn===4?' ◀ NOW':'')+'</div>';
    if(me.length){for(var j=0;j<me.length;j++){var e=me[j],sn=e.n.replace(/ 2026/g,'').replace(/ \(Session 1\)/,' S1').replace(/ \(Session 2\)/,' S2').replace(/ \(Phase 1\)/,' P1').replace(/ \(Phase 2\)/,' P2').replace(/ \(Sess 1\)/,' S1').replace(/ \(Sess 2\)/,' S2').replace(/ \(Stage 1\)/,' S1').replace(/ \(Stage 2\)/,' S2').replace(/ \(Multi-Session\)/,'');
    h+='<div class="tlc" style="border-color:'+(tc[e.t]||'#60a5fa')+'"><b>'+sn+'</b><small>'+e.d+'</small></div>';}}
    else h+='<p style="color:var(--text3);font-size:10px;padding:4px">No exams</p>';h+='</div>';}
  document.getElementById('tL').innerHTML=h;
}

function rI(){
  var steps=[{i:'1️⃣',t:'Registration',d:'Most exams open 2-3 months before. Keep Aadhaar, marksheets, photos ready. NTA requires DigiLocker for JEE Main.'},{i:'2️⃣',t:'Admit Card',d:'Released 10-15 days before. Check all details. Design exams need portfolio & sketching practice.'},{i:'3️⃣',t:'Exam Day',d:'JEE Main: 90Q +4/-1. NATA: Hybrid. NID DAT: Prelims+Studio. UCEED: Part A (CBT) + Part B (Drawing).'},{i:'4️⃣',t:'Results',d:'NTA releases provisional keys. NID has no answer keys. Best score from multiple sessions counts.'},{i:'5️⃣',t:'Counselling',d:'JoSAA for IITs/NITs. State counselling for KCET/MHT CET. NID/NIFT own process. NATA: 400+ colleges.'},{i:'6️⃣',t:'Reservation',d:'Govt: OBC 27%, SC 15%, ST 7.5%, EWS 10%, PwD 5% horizontal. Design seats: NID ~425, NIFT ~5076.'}];
  var h='';steps.forEach(function(s){h+='<div class="cc"><div class="ico">'+s.i+'</div><h3>'+s.t+'</h3><p>'+s.d+'</p></div>'});
  document.getElementById('iG').innerHTML=h;
  var cats=[{n:28,l:'B.Tech/B.E.',c:'#60a5fa',w:100,d:'Engineering — JEE, BITSAT, KCET, MHT CET, WBJEE, VITEEE, etc.'},{n:6,l:'B.Des (Design)',c:'#fb923c',w:22,d:'Design — NID DAT, NIFT, UCEED, CEED'},{n:3,l:'B.Arch',c:'#38bdf8',w:11,d:'Architecture — NATA, JEE B.Arch Paper 2'},{n:4,l:'Research/Science',c:'#fbbf24',w:14,d:'Research — ISI, UGEE, IAT (IISER), NEST'}];
  h='';cats.forEach(function(c){h+='<div class="kc"><div class="kn" style="color:'+c.c+'">'+c.n+'</div><div class="kl">'+c.l+'</div><div style="height:4px;border-radius:2px;margin-top:8px;background:var(--bg3);overflow:hidden"><div style="height:100%;width:'+c.w+'%;background:'+c.c+';border-radius:2px"></div></div><p>'+c.d+'</p></div>'});
  document.getElementById('kG').innerHTML=h;
}

function iP(id){return P.some(function(p){return p.id===id})}
function sP(){try{localStorage.setItem('ep3',JSON.stringify(P))}catch(e){}uB()}
function uB(){document.getElementById('pBdg').textContent=P.length?'('+P.length+')':''}

function tP(id,btn){var idx=-1;for(var j=0;j<P.length;j++){if(P[j].id===id){idx=j;break}}if(idx>=0){P.splice(idx,1);btn.classList.remove('ad');btn.innerHTML='➕';T('Removed');}else{var e=E.find(function(x){return x.id===id});P.push(e);btn.classList.add('ad');btn.innerHTML='✅';T('Added!');}sP();rP();}

function rP(){var el=document.getElementById('pL');if(!P.length){el.innerHTML='<div class="pee"><div style="font-size:40px;opacity:.3;margin-bottom:8px">📋</div><p>No exams added. Go to "All Exams" and click ➕.</p></div>';return}
  var h='';for(var j=0;j<P.length;j++){var p=P[j],x=gs(p.sd);
    h+='<div class="pe"><div class="pei">'+(j+1)+'</div><div class="ped">'+p.d+'</div><div class="pen">'+p.n+'</div><span class="sb '+sc(p.sr)+'">'+p.sr+'</span><span class="b b-'+p.t+'" style="margin-left:4px">'+p.t+'</span><span class="'+x.c+'" style="font-size:11px;font-weight:600;margin-left:4px">'+x.k+' '+x.s+'</span><button class="per" onclick="rmP('+j+')">×</button></div>';}el.innerHTML=h;}

function rmP(j){P.splice(j,1);sP();rP();R();T('Removed')}
function clrP(){if(!confirm('Clear all?'))return;P=[];sP();rP();R();T('Cleared')}

function oS(id){var e=E.find(function(x){return x.id===id});if(!e)return;
  var t='📚 '+e.n+'\n📅 '+e.d+'\n🎓 Stream: '+e.sr+'\n\n📋 44 Engineering, Design & Architecture Exams 2026\n🌐 www.eduaakashaa.in\n📧 info@eduaakashaa.com\n✅ Free Expert Counselling — EduAakashaA';
  document.getElementById('sT').textContent='Share: '+e.n;
  document.getElementById('sW').href='https://wa.me/?text='+encodeURIComponent(t);
  document.getElementById('sTw').href='https://twitter.com/intent/tweet?text='+encodeURIComponent(t);
  document.getElementById('sEm').href='mailto:?subject='+encodeURIComponent(e.n)+'&body='+encodeURIComponent(t);
  document.getElementById('sTg').href='https://t.me/share/url?url='+encodeURIComponent('https://www.eduaakashaa.in')+'&text='+encodeURIComponent(t);
  document.getElementById('sLi').href='https://www.linkedin.com/sharing/share-offsite/?url='+encodeURIComponent('https://www.eduaakashaa.in');
  document.getElementById('sM').classList.add('show');}
function cS(){document.getElementById('sM').classList.remove('show')}
function cL(){if(navigator.clipboard)navigator.clipboard.writeText('Engineering Exam Schedule 2026 — www.eduaakashaa.in');T('Copied!');cS();}

function dlPDF(){
  var nm=document.getElementById('sN').value,em=document.getElementById('sE').value,ph=document.getElementById('sP').value;
  if(!nm){T('Enter your name');return}var ls=P.length?P:E;var w=window.open('','_blank');if(!w){T('Allow popups');return}
  var rows='';for(var j=0;j<ls.length;j++){var e=ls[j],x=gs(e.sd);rows+='<tr'+(j%2?' style="background:#f8f9fa"':'')+'><td>'+(j+1)+'</td><td><b>'+e.n+'</b></td><td>'+e.d+'</td><td>'+e.sr+'</td><td>'+e.t+'</td><td>'+x.s+'</td></tr>';}
  w.document.write('<!DOCTYPE html><html><head><title>Exam Report - '+nm+'</title></head><body>');
  w.document.write('<h1>🎓 Engineering & Design Exam Schedule 2026</h1>');
  w.document.write('<div class="info"><b>Prepared for:</b> '+nm+(em?' | <b>Email:</b> '+em:'')+(ph?' | <b>Phone:</b> '+ph:'')+'<br><b>Generated:</b> '+new Date().toLocaleDateString('en-IN',{day:'numeric',month:'long',year:'numeric'})+'</div>');
  w.document.write('<h2>📋 '+(P.length?'Your Planned':'All')+' Exams ('+ls.length+')</h2>');
  w.document.write('<table><thead><tr><th>#</th><th>Exam</th><th>Date</th><th>Stream</th><th>Type</th><th>Status</th></tr></thead><tbody>'+rows+'</tbody></table>');
  w.document.write('<div class="about"><h3 style="color:#2563eb;margin-bottom:6px">About EduAakashaA</h3><p>India\'s trusted admission guidance platform helping 10,000+ students across engineering, design & architecture admissions.</p><p style="margin-top:6px"><b>Services:</b> Exam Strategy | College Comparison | Application Help | Deadline Alerts | Counselling Support | Branch Selection | Portfolio Guidance (Design/Architecture)</p><p style="margin-top:6px"><b>Contact:</b> www.eduaakashaa.in | info@eduaakashaa.com</p></div>');
  w.document.write('<h2>📌 Key Reminders</h2><ul><li>Verify dates on official websites before exam</li><li>Keep Aadhaar, marksheets, photos ready</li><li>Download admit cards 10-15 days before</li><li>Apply to 5-8 exams strategically across streams</li><li>Design exams need portfolio & sketch practice</li></ul>');
  w.document.write('<div class="cta"><b>Need Expert Guidance?</b><br>Book a free 1-on-1 counselling session<br><a href="https://www.eduaakashaa.in">www.eduaakashaa.in</a> | info@eduaakashaa.com</div>');
  w.document.write('<div class="ft">© 2026 EduAakashaA — www.eduaakashaa.in | info@eduaakashaa.com</div></body></html>');
  w.document.close();setTimeout(function(){w.print()},500);T('PDF generated!');}

function T(m){var t=document.getElementById('tst');t.textContent=m;t.classList.add('show');setTimeout(function(){t.classList.remove('show')},2400);}

fSt();R();rTL();rI();rP();uB();


// ---- next <script> block ----


	const heightObserver = new ResizeObserver(([{ contentRect }]) => {
		window.parent.postMessage({ action: 'iframeHeightUpdated', height: contentRect.height, id: 'zKChWs' }, '*');
	});

	heightObserver.observe(document.documentElement);
