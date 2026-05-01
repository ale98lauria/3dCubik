const CACHE = "3dcubik-v14";
const PRECACHE = ["/", "/index.html", "/products.json"];

self.addEventListener("install", e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(PRECACHE)));
  self.skipWaiting();
});

self.addEventListener("activate", e => {
  e.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))
    )
  );
  self.clients.claim();
});

self.addEventListener("fetch", e => {
  const url = new URL(e.request.url);

  // Risorse cross-origin (Google Fonts, ecc.): lascia gestire al browser
  if (url.origin !== self.location.origin) return;

  const { pathname } = url;

  // Immagini: Cache First (non cambiano mai)
  if (pathname.startsWith("/imgs/")) {
    e.respondWith(
      caches.match(e.request).then(hit =>
        hit || fetch(e.request).then(res => {
          const clone = res.clone();
          caches.open(CACHE).then(c => c.put(e.request, clone));
          return res;
        })
      )
    );
    return;
  }

  // products.json: Network First, fallback cache (per aggiornamenti futuri)
  if (pathname === "/products.json") {
    e.respondWith(
      fetch(e.request)
        .then(res => {
          const clone = res.clone();
          caches.open(CACHE).then(c => c.put(e.request, clone));
          return res;
        })
        .catch(() => caches.match(e.request))
    );
    return;
  }

  // Tutto il resto: Network First
  e.respondWith(
    fetch(e.request).catch(() => caches.match(e.request))
  );
});
