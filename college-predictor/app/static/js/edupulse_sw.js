/* EduPulse App service worker (scope /app/).
   Pages are always fetched from the network (they hold personal data, so they are never cached);
   when offline, a small offline page is shown. Static assets (CSS, logo, fonts) are cached for speed. */
var CACHE = 'edupulse-v1';
var SHELL = ['/app/offline', '/static/css/edupulse_app.css', '/static/images/logo.png', '/static/images/favicon.png'];

self.addEventListener('install', function (e) {
  e.waitUntil(caches.open(CACHE).then(function (c) { return c.addAll(SHELL); }).then(function () { return self.skipWaiting(); }));
});

self.addEventListener('activate', function (e) {
  e.waitUntil(caches.keys().then(function (keys) {
    return Promise.all(keys.filter(function (k) { return k !== CACHE; }).map(function (k) { return caches.delete(k); }));
  }).then(function () { return self.clients.claim(); }));
});

self.addEventListener('fetch', function (e) {
  var req = e.request;
  if (req.method !== 'GET') return;
  if (req.mode === 'navigate') {
    e.respondWith(fetch(req).catch(function () { return caches.match('/app/offline'); }));
    return;
  }
  var url = new URL(req.url);
  var cacheable = (url.origin === location.origin && url.pathname.indexOf('/static/') === 0) || url.host.indexOf('fonts.g') === 0;
  if (!cacheable) return;
  e.respondWith(caches.match(req).then(function (hit) {
    var net = fetch(req).then(function (res) {
      if (res && (res.ok || res.type === 'opaque')) { var copy = res.clone(); caches.open(CACHE).then(function (c) { c.put(req, copy); }); }
      return res;
    }).catch(function () { return hit; });
    return hit || net;
  }));
});
