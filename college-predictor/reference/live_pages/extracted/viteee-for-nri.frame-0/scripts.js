
	const heightObserver = new ResizeObserver(([{ contentRect }]) => {
		window.parent.postMessage({ action: 'iframeHeightUpdated', height: contentRect.height, id: 'zp0cHe' }, '*');
	});

	heightObserver.observe(document.documentElement);
