
const hamb=document.getElementById('hamb'),mob=document.getElementById('mob');
hamb.addEventListener('click',()=>{mob.style.display=mob.style.display==='flex'?'none':'flex';});
mob.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>mob.style.display='none'));

const io=new IntersectionObserver((es)=>{es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('visible');io.unobserve(e.target);}})},{threshold:.12});
document.querySelectorAll('.reveal').forEach(el=>io.observe(el));

document.querySelectorAll('.faq-q').forEach(q=>q.addEventListener('click',()=>{
  const it=q.parentElement;const open=it.classList.contains('open');
  document.querySelectorAll('.faq-item').forEach(i=>i.classList.remove('open'));
  if(!open)it.classList.add('open');
}));

function drawCharts(){
  if(typeof Chart==='undefined')return;
  Chart.defaults.font.family="'Plus Jakarta Sans',sans-serif";
  Chart.defaults.color='#5A6278';
  const navy='#0E3A8A',green='#1F8B5C',red='#C23A3A',hair='#E8DFC8';
  if(window._bc)return;
  window._bc=new Chart(document.getElementById('barChart'),{
    type:'bar',
    data:{labels:['NITs + IIEST','IIITs','GFTI / Other','Total'],
      datasets:[
        {label:'DASA 2025',data:[31,13,33,77],backgroundColor:'#9fb2d8',borderRadius:6,maxBarThickness:46},
        {label:'DASA 2026 (V1.3)',data:[31,18,37,86],backgroundColor:navy,borderRadius:6,maxBarThickness:46}
      ]},
    options:{responsive:true,maintainAspectRatio:false,
      plugins:{legend:{position:'bottom',labels:{boxWidth:12,boxHeight:12,padding:16,font:{size:12}}}},
      scales:{x:{grid:{display:false}},y:{beginAtZero:true,grid:{color:hair},ticks:{stepSize:20}}}}
  });
  window._dc=new Chart(document.getElementById('doughChart'),{
    type:'doughnut',
    data:{labels:['Carried over from 2025','Newly added (2026)','Removed (was in 2025)'],
      datasets:[{data:[30,7,3],backgroundColor:[navy,green,red],borderColor:'#FFFDF7',borderWidth:3}]},
    options:{responsive:true,maintainAspectRatio:false,cutout:'62%',
      plugins:{legend:{position:'bottom',labels:{boxWidth:12,boxHeight:12,padding:14,font:{size:11.5}}}}}
  });
}
if(document.readyState!=='loading')drawCharts();else window.addEventListener('DOMContentLoaded',drawCharts);
window.addEventListener('load',drawCharts);

;

	const heightObserver = new ResizeObserver(([{ contentRect }]) => {
		window.parent.postMessage({ action: 'iframeHeightUpdated', height: contentRect.height, id: 'z-gbLq' }, '*');
	});

	heightObserver.observe(document.documentElement);
