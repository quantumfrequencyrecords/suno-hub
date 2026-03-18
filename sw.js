// Suno Prompt Hub — Service Worker
// Caches all files after first visit for full offline support

const CACHE = 'suno-hub-v1';
const ALWAYS_FETCH = ['/manifest.json']; // Always try network for the file list

const CORE_FILES = [
  './',
  './index.html',
  './app.webmanifest',
  'https://fonts.googleapis.com/css2?family=DM+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&family=DM+Mono:wght@400;500&display=swap'
];

// Install: cache core files
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE).then(cache => cache.addAll(CORE_FILES)).then(() => self.skipWaiting())
  );
});

// Activate: clean old caches
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

// Fetch strategy:
// - manifest.json: network first, fall back to cache (so new artists appear)
// - artist JSON files: cache first (they don't change), network updates cache
// - Everything else: cache first
self.addEventListener('fetch', event => {
  const url = new URL(event.request.url);
  const filename = url.pathname.split('/').pop();

  // manifest.json — always try network first so new files are discovered
  if (filename === 'manifest.json') {
    event.respondWith(
      fetch(event.request)
        .then(res => {
          const clone = res.clone();
          caches.open(CACHE).then(c => c.put(event.request, clone));
          return res;
        })
        .catch(() => caches.match(event.request))
    );
    return;
  }

  // Artist JSON files — cache first, refresh in background
  if (filename.endsWith('.json')) {
    event.respondWith(
      caches.open(CACHE).then(cache =>
        cache.match(event.request).then(cached => {
          const fetchPromise = fetch(event.request).then(res => {
            cache.put(event.request, res.clone());
            return res;
          });
          return cached || fetchPromise;
        })
      )
    );
    return;
  }

  // Everything else: cache first
  event.respondWith(
    caches.match(event.request).then(cached => {
      if (cached) return cached;
      return fetch(event.request).then(res => {
        if (res.status === 200) {
          const clone = res.clone();
          caches.open(CACHE).then(c => c.put(event.request, clone));
        }
        return res;
      });
    })
  );
});

// Message from hub: force refresh all artist files
self.addEventListener('message', event => {
  if (event.data === 'CLEAR_ARTIST_CACHE') {
    caches.open(CACHE).then(cache => {
      cache.keys().then(keys => {
        keys.filter(k => k.url && k.url.includes('artist_'))
            .forEach(k => cache.delete(k));
      });
    });
  }
});
