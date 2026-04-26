
	const heightObserver = new ResizeObserver(([{ contentRect }]) => {
		window.parent.postMessage({ action: 'iframeHeightUpdated', height: contentRect.height, id: 'z1b0bQ' }, '*');
	});

	heightObserver.observe(document.documentElement);
