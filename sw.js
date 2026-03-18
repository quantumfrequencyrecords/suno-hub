// Suno Prompt Hub — Service Worker v3
// IMPORTANT: index.html is NEVER cached — always fetched fresh from network
// This prevents stale app versions from being served after updates

var CACHE = ‘suno-hub-v3’;

// Install: skip waiting immediately so new SW activates right away
self.addEventListener(‘install’, function(event) {
self.skipWaiting();
});

// Activate: delete ALL old caches, claim all clients
self.addEventListener(‘activate’, function(event) {
event.waitUntil(
caches.keys().then(function(keys) {
return Promise.all(
keys.filter(function(k) { return k !== CACHE; })
.map(function(k) { return caches.delete(k); })
);
}).then(function() {
return self.clients.claim();
})
);
});

self.addEventListener(‘fetch’, function(event) {
var url = new URL(event.request.url);
var filename = url.pathname.split(’/’).pop();

// NEVER cache index.html — always get fresh from network
if (filename === ‘index.html’ || filename === ‘’ || url.pathname.endsWith(’/’)) {
event.respondWith(
fetch(event.request).catch(function() {
return caches.match(’./index.html’);
})
);
return;
}

// manifest.json — network first so new artists are discovered immediately
if (filename === ‘manifest.json’) {
event.respondWith(
fetch(event.request).then(function(res) {
var clone = res.clone();
caches.open(CACHE).then(function(c) { c.put(event.request, clone); });
return res;
}).catch(function() {
return caches.match(event.request);
})
);
return;
}

// Artist/genre JSON files — cache but always update in background
if (filename.endsWith(’.json’)) {
event.respondWith(
caches.open(CACHE).then(function(cache) {
return cache.match(event.request).then(function(cached) {
var networkFetch = fetch(event.request).then(function(res) {
if (res.ok) cache.put(event.request, res.clone());
return res;
});
return cached || networkFetch;
});
})
);
return;
}

// Everything else: network first with cache fallback
event.respondWith(
fetch(event.request).then(function(res) {
if (res.status === 200) {
var clone = res.clone();
caches.open(CACHE).then(function(c) { c.put(event.request, clone); });
}
return res;
}).catch(function() {
return caches.match(event.request);
})
);
});

// Message handler — clear all caches on demand
self.addEventListener(‘message’, function(event) {
if (event.data === ‘CLEAR_ALL’) {
caches.keys().then(function(keys) {
keys.forEach(function(k) { caches.delete(k); });
});
}
});
