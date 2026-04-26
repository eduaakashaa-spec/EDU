{"@context":"https://schema.org/","name":"Stream Selection","url":"https://eduaakashaa.in/stream-selection","inLanguage":"ta","@type":"WebPage"}

// ---- next <script> block ----

(function(){const postDate = null;

			const currentDate = new Date().setHours(0, 0, 0, 0);
			const postPublishDate = new Date(postDate).setHours(0, 0, 0, 0);

			if (postPublishDate && currentDate < postPublishDate) {
				window.location.replace('/');
			}
		})();

// ---- next <script> block ----

(()=>{var e=async t=>{await(await t())()};(self.Astro||(self.Astro={})).only=e;window.dispatchEvent(new Event("astro:only"));})();

// ---- next <script> block ----

(()=>{var A=Object.defineProperty;var g=(i,o,a)=>o in i?A(i,o,{enumerable:!0,configurable:!0,writable:!0,value:a}):i[o]=a;var d=(i,o,a)=>g(i,typeof o!="symbol"?o+"":o,a);{let i={0:t=>m(t),1:t=>a(t),2:t=>new RegExp(t),3:t=>new Date(t),4:t=>new Map(a(t)),5:t=>new Set(a(t)),6:t=>BigInt(t),7:t=>new URL(t),8:t=>new Uint8Array(t),9:t=>new Uint16Array(t),10:t=>new Uint32Array(t),11:t=>1/0*t},o=t=>{let[l,e]=t;return l in i?i[l](e):void 0},a=t=>t.map(o),m=t=>typeof t!="object"||t===null?t:Object.fromEntries(Object.entries(t).map(([l,e])=>[l,o(e)]));class y extends HTMLElement{constructor(){super(...arguments);d(this,"Component");d(this,"hydrator");d(this,"hydrate",async()=>{var b;if(!this.hydrator||!this.isConnected)return;let e=(b=this.parentElement)==null?void 0:b.closest("astro-island[ssr]");if(e){e.addEventListener("astro:hydrate",this.hydrate,{once:!0});return}let c=this.querySelectorAll("astro-slot"),n={},h=this.querySelectorAll("template[data-astro-template]");for(let r of h){let s=r.closest(this.tagName);s!=null&&s.isSameNode(this)&&(n[r.getAttribute("data-astro-template")||"default"]=r.innerHTML,r.remove())}for(let r of c){let s=r.closest(this.tagName);s!=null&&s.isSameNode(this)&&(n[r.getAttribute("name")||"default"]=r.innerHTML)}let p;try{p=this.hasAttribute("props")?m(JSON.parse(this.getAttribute("props"))):{}}catch(r){let s=this.getAttribute("component-url")||"<unknown>",v=this.getAttribute("component-export");throw v&&(s+=` (export ${v})`),console.error(`[hydrate] Error parsing props for component ${s}`,this.getAttribute("props"),r),r}let u;await this.hydrator(this)(this.Component,p,n,{client:this.getAttribute("client")}),this.removeAttribute("ssr"),this.dispatchEvent(new CustomEvent("astro:hydrate"))});d(this,"unmount",()=>{this.isConnected||this.dispatchEvent(new CustomEvent("astro:unmount"))})}disconnectedCallback(){document.removeEventListener("astro:after-swap",this.unmount),document.addEventListener("astro:after-swap",this.unmount,{once:!0})}connectedCallback(){if(!this.hasAttribute("await-children")||document.readyState==="interactive"||document.readyState==="complete")this.childrenConnectedCallback();else{let e=()=>{document.removeEventListener("DOMContentLoaded",e),c.disconnect(),this.childrenConnectedCallback()},c=new MutationObserver(()=>{var n;((n=this.lastChild)==null?void 0:n.nodeType)===Node.COMMENT_NODE&&this.lastChild.nodeValue==="astro:end"&&(this.lastChild.remove(),e())});c.observe(this,{childList:!0}),document.addEventListener("DOMContentLoaded",e)}}async childrenConnectedCallback(){let e=this.getAttribute("before-hydration-url");e&&await import(e),this.start()}async start(){let e=JSON.parse(this.getAttribute("opts")),c=this.getAttribute("client");if(Astro[c]===void 0){window.addEventListener(`astro:${c}`,()=>this.start(),{once:!0});return}try{await Astro[c](async()=>{let n=this.getAttribute("renderer-url"),[h,{default:p}]=await Promise.all([import(this.getAttribute("component-url")),n?import(n):()=>()=>{}]),u=this.getAttribute("component-export")||"default";if(!u.includes("."))this.Component=h[u];else{this.Component=h;for(let f of u.split("."))this.Component=this.Component[f]}return this.hydrator=p,this.hydrate},e,this)}catch(n){console.error(`[astro-island] Error hydrating ${this.getAttribute("component-url")}`,n)}}attributeChangedCallback(){this.hydrate()}}d(y,"observedAttributes",["props"]),customElements.get("astro-island")||customElements.define("astro-island",y)}})();

// ---- next <script> block ----

(()=>{var e=async t=>{await(await t())()};(self.Astro||(self.Astro={})).load=e;window.dispatchEvent(new Event("astro:load"));})();

// ---- next <script> block ----


var Qs = [
  { q:"Where do you want to build your career?",
    o:[{t:"🌍 Internationally — anywhere",s:{acca:2}},{t:"💹 Finance hubs (NYC, London, HK)",s:{cfa:2}},{t:"🏙️ Primarily in my home country",s:{ca:2}},{t:"🤷 Not decided yet",s:{acca:1}}]
  },
  { q:"What kind of work excites you most?",
    o:[{t:"📊 Auditing & financial reporting",s:{acca:2,ca:1}},{t:"📈 Stock analysis & portfolio management",s:{cfa:3}},{t:"🧾 Tax, compliance & advisory",s:{ca:2}},{t:"🔀 A mix of all finance areas",s:{acca:2}}]
  },
  { q:"How can you dedicate time to studying?",
    o:[{t:"⏱️ Part-time alongside my job",s:{acca:2}},{t:"📚 Intense focused study windows",s:{cfa:2}},{t:"🎓 Full-time with practical training",s:{ca:2}},{t:"🔄 Flexible — whatever it takes",s:{acca:1,cfa:1,ca:1}}]
  },
  { q:"What matters most in a qualification?",
    o:[{t:"🌐 Global recognition / working abroad",s:{acca:3}},{t:"💰 Highest salary in investment finance",s:{cfa:3}},{t:"🏆 Prestigious local qualification",s:{ca:3}},{t:"⚡ Fastest route to a finance career",s:{acca:2}}]
  }
];

var cur=0, sc={acca:0,cfa:0,ca:0}, pend=null;

function pick(btn,idx){
  var all=document.querySelectorAll('.qopt');
  for(var i=0;i<all.length;i++) all[i].classList.remove('sel');
  btn.classList.add('sel');
  pend=Qs[cur].o[idx].s;
  document.getElementById('qNext').style.display='inline-block';
}

function nextQ(){
  if(!pend) return;
  for(var k in pend) sc[k]=(sc[k]||0)+pend[k];
  pend=null; cur++;
  if(cur>=Qs.length){ showRes(); return; }
  document.getElementById('qProg').textContent='Question '+(cur+1)+' of '+Qs.length;
  document.getElementById('qText').textContent=Qs[cur].q;
  var html='';
  for(var i=0;i<Qs[cur].o.length;i++) html+='<button class="qopt" onclick="pick(this,'+i+')">'+Qs[cur].o[i].t+'</button>';
  document.getElementById('qOpts').innerHTML=html;
  document.getElementById('qNext').style.display='none';
}

function showRes(){
  var keys=Object.keys(sc).sort(function(a,b){return sc[b]-sc[a];});
  var w=keys[0];
  var info={
    acca:{n:'ACCA',cls:'rb-a', ti:'ACCA is your ideal match!', tx:'Your goals align with ACCA — global flexibility, modular study structure, and recognition in 180+ countries.'},
    cfa:{n:'CFA',cls:'rb-c', ti:'CFA is your ideal match!', tx:'Your passion for investment and markets points to the CFA Charter — the gold standard for finance professionals worldwide.'},
    ca:{n:'CA',cls:'rb-ca', ti:'CA is your ideal match!', tx:'Your preference for domestic prestige, taxation, and comprehensive accounting makes CA the perfect qualification.'}
  }[w];
  document.getElementById('qMain').style.display='none';
  document.getElementById('qResult').style.display='block';
  var b=document.getElementById('rBadge');
  b.textContent=info.n; b.className='rbadge '+info.cls;
  document.getElementById('rTitle').textContent=info.ti;
  document.getElementById('rText').textContent=info.tx;
}

function resetQ(){
  cur=0; sc={acca:0,cfa:0,ca:0}; pend=null;
  document.getElementById('qResult').style.display='none';
  document.getElementById('qMain').style.display='block';
  document.getElementById('qProg').textContent='Question 1 of '+Qs.length;
  document.getElementById('qText').textContent=Qs[0].q;
  var html='';
  for(var i=0;i<Qs[0].o.length;i++) html+='<button class="qopt" onclick="pick(this,'+i+')">'+Qs[0].o[i].t+'</button>';
  document.getElementById('qOpts').innerHTML=html;
  document.getElementById('qNext').style.display='none';
}
