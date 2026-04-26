
	const heightObserver = new ResizeObserver(([{ contentRect }]) => {
		window.parent.postMessage({ action: 'iframeHeightUpdated', height: contentRect.height, id: 'zJI39I' }, '*');
	});

	heightObserver.observe(document.documentElement);
