
function eaTab(idx, btn) {
  // Update buttons
  var btns = document.querySelectorAll('#ea-wrap .ea-tab-btn');
  btns.forEach(function(b){ b.classList.remove('active'); });
  btn.classList.add('active');
  // Update panes
  var panes = document.querySelectorAll('#ea-wrap .ea-tab-pane');
  panes.forEach(function(p){ p.classList.remove('active'); });
  document.getElementById('ea-pane-' + idx).classList.add('active');
  // Smooth scroll to tabs
  document.querySelector('#ea-wrap .ea-tabs').scrollIntoView({behavior:'smooth', block:'nearest'});
}


// ---- next <script> block ----


	const heightObserver = new ResizeObserver(([{ contentRect }]) => {
		window.parent.postMessage({ action: 'iframeHeightUpdated', height: contentRect.height, id: 'zBwuWZ' }, '*');
	});

	heightObserver.observe(document.documentElement);
