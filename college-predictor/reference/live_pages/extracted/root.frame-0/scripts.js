
document.querySelectorAll('.fq').forEach(function(q){
  q.addEventListener('click',function(){this.parentElement.classList.toggle('open');});
});
document.querySelectorAll('a[href^="#"]').forEach(function(a){
  a.addEventListener('click',function(e){
    var t=document.querySelector(this.getAttribute('href'));
    if(t){e.preventDefault();t.scrollIntoView({behavior:'smooth',block:'start'});}
  });
});


// ---- next <script> block ----


	const heightObserver = new ResizeObserver(([{ contentRect }]) => {
		window.parent.postMessage({ action: 'iframeHeightUpdated', height: contentRect.height, id: 'zlmPDw' }, '*');
	});

	heightObserver.observe(document.documentElement);
