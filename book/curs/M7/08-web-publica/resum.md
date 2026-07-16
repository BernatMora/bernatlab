# Resum - Capitol 8: PWA i web publica de l'Hort Osona

## La idea clau

L'**objectiu final** de tot el pipeline es que l'hortola pugui veure les dades del seu hort des de qualsevol lloc: el telefon, la tabletta, l'ordinador. Per aixo construim una **PWA** (Progressive Web App) que es pot instal·lar com una app nativa pero es nomes HTML+CSS+JS. L'allotgem a **GitHub Pages** perque es **gratis, rapid i senzill**. A l'Hort Osona la PWA mostra grafiques en temps quasi-real, l'estat dels sensors, i un minimap dels sectors.

## Que es una PWA

Una **Progressive Web App** es una pagina web que sembla i es comporta com una app nativa. Per fer-ho te tres ingredients:

1. **HTTPS**: nomes funciona sobre connexions segures.
2. **Manifest (JSON)**: un fitxer `manifest.json` que diu el nom, icones, colors.
3. **Service Worker**: un script JS que intercepta les peticions i pot fer-les offline.

Exemple de `manifest.json`:

```json
{
  "name": "Hort Osona",
  "short_name": "HortOsona",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#2e7d32",
  "icons": [
    {
      "src": "/icon-192.png",
      "sizes": "192x192",
      "type": "image/png"
    }
  ]
}
```

Això fa que el navegador ofereixi **"Afegir a la pantalla d'inici"**. Un cop instal·lada, la PWA s'obre sense barra d'adreces, a pantalla completa.

## Per que PWA i no app nativa

Podriem fer una app Android/iOS amb React Native o Flutter. Però:

- **Cost**: una app nativa costa 10x mes en temps de desenvolupament.
- **Distribucio**: has de publicar a Google Play / App Store. PWA es distribueix per URL.
- **Multiplataforma**: PWA funciona a iOS, Android, Windows, Mac, Linux. Una sola codebase.
- **Actualitzacions**: el navegador les aplica automaticament. No cal passar revisio d'Apple.

L'inconvenient es que les PWAs tenen **limitacions**:
- No accedeixen a Bluetooth (a iOS).
- No tenen acces complet a sensors (proximitat, NFC, etc).
- A iOS, les notificacions push son limitades.

Per a l'Hort Osona (consultar dades, veure grafiques, rebre alertes), la PWA es **perfecta**.

## Per que GitHub Pages

**GitHub Pages** es un servei de hosting gratuit de GitHub per a pagines web estatiques. Avantatges:

- **Gratis** per a repositoris publics.
- **HTTPS automatic** amb certificat de Let's Encrypt.
- **CDN global** (Cloudflare-like) - rapid a tot el mon.
- **Domini personalitzat** suportat.
- **Integracio amb git** - cada `git push` fa un deploy.

A l'Hort Osona publiquem la PWA al repo `BernatMora/hort-osona-web` (o subcarpeta del monorepo). Cada `git push` al branch `main` actualitza la web automaticament.

```
git push origin main
   |
   v
GitHub Pages (CDN)
   |
   v
https://hort-osona.github.io
```

Limitacio: **nomes allotja fitxers estatics**. No pot executar Python ni Node.js. Pero aixo es perfecte per una PWA.

## Arquitectura de la PWA

La PWA es una SPA (Single Page Application) amb un sol `index.html` que carrega JS que renderitza la UI dinamicament:

```
+-----------------------------+
|         index.html          |
|   - manifest.json link      |
|   - service worker register |
|   - <div id="app">          |
+-----------------------------+
            |
            v
+-----------------------------+
|         app.js              |
|   - router                  |
|   - cridar API              |
|   - renderitzar UI          |
+-----------------------------+
            |
            v
+-----------------------------+
|     chart.js (CDN)          |
|     - grafiques             |
+-----------------------------+
```

Stack tipic:

- **HTML + CSS + Vanilla JS** (o un framework lleuger com Vue, Svelte, Preact).
- **Chart.js** o **ApexCharts** per a grafiques.
- **Workbox** o `sw.js` a ma per al service worker.

A l'Hort Osona fem servir **Vue 3 + Vite + Chart.js**. Vue es petit, Vite es rapid, i Chart.js es la millor llibreria de grafiques per a JS.

## Exemple: index.html minim

```html
<!DOCTYPE html>
<html lang="ca">
<head>
   <meta charset="UTF-8">
   <meta name="viewport" content="width=device-width, initial-scale=1.0">
   <title>Hort Osona</title>
   <link rel="manifest" href="manifest.json">
   <link rel="stylesheet" href="styles.css">
   <meta name="theme-color" content="#2e7d32">
</head>
<body>
   <header>
       <h1>🌱 Hort Osona</h1>
   </header>
   <main id="app">
       <p>Carregant...</p>
   </main>
   <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
   <script type="module" src="app.js"></script>
   <script>
       if ('serviceWorker' in navigator) {
           navigator.serviceWorker.register('sw.js');
       }
   </script>
</body>
</html>
```

## Exemple: app.js amb fetch a l'API

```javascript
const API_URL = 'https://hort-osona-api.example.com/api/v1';
const API_KEY = 'hort-osona-test-key-2026';  // No ideal, caldria millor auth

async function getLatest(deviceId) {
   const r = await fetch(`${API_URL}/sensors/${deviceId}/latest`, {
       headers: { 'X-API-Key': API_KEY }
   });
   if (!r.ok) throw new Error(`API error: ${r.status}`);
   return r.json();
}

async function getHistory(deviceId, field, hours) {
   const r = await fetch(
       `${API_URL}/sensors/${deviceId}/history?h=${hours}&field=${field}`,
       { headers: { 'X-API-Key': API_KEY } }
   );
   if (!r.ok) throw new Error(`API error: ${r.status}`);
   return r.json();
}

async function render() {
   const app = document.getElementById('app');
   const sectors = ['miflora-1B32', 'miflora-1B33', 'miflora-1B34'];
   const data = await Promise.all(
       sectors.map(d => getLatest(d).catch(e => ({ device: d, error: e.message })))
   );

   app.innerHTML = data.map(d => `
       <section class="card">
           <h2>${d.device || 'Error'}</h2>
           ${d.fields ? `
               <p>Humitat: ${d.fields.soil_moisture ?? '-'}%</p>
               <p>Temp: ${d.fields.soil_temp_c ?? '-'}°C</p>
           ` : `<p class="error">${d.error}</p>`}
       </section>
   `).join('');

   // Grafica
   const hist = await getHistory('miflora-1B32', 'soil_moisture', 24);
   new Chart(document.getElementById('chart'), {
       type: 'line',
       data: {
           labels: hist.points.map(p => p.ts),
           datasets: [{ label: 'Humitat (%)', data: hist.points.map(p => p.value) }]
       }
   });
}

render();
setInterval(render, 60000);  // refresca cada minut
```

## Service Worker (offline basic)

El `sw.js` permet que la PWA funcioni offline:

```javascript
const CACHE = 'hort-osona-v1';
const ASSETS = ['/', '/index.html', '/app.js', '/styles.css', '/manifest.json'];

self.addEventListener('install', (e) => {
   e.waitUntil(caches.open(CACHE).then(c => c.addAll(ASSETS)));
});

self.addEventListener('fetch', (e) => {
   e.respondWith(
       caches.match(e.request).then(r => r || fetch(e.request))
   );
});
```

Quan obres la PWA sense internet, carrega la versio en cache. Quan tornes a tenir xarxa, s'actualitza.

## Deployment a GitHub Pages

Pas a pas:

1. Crea un repo a GitHub (e.g. `BernatMora/hort-osona-web`).
2. A Settings -> Pages, selecciona el branch `main` i la carpeta `/` (root) o `/docs`.
3. Fes push del codi:

```bash
git init
git add .
git commit -m "PWA Hort Osona"
git branch -M main
git remote add origin git@github.com:BernatMora/hort-osona-web.git
git push -u origin main
```

4. Espera 1-2 minuts. La web es accessible a `https://<usuari>.github.io/<repo>/`.

Si vols domini propi (e.g. `hort-osona.cat`), configura un CNAME al DNS i un fitxer `CNAME` al repo.

## Dades obertes vs privades

A l'Hort Osona tenim **dos modes**:

1. **Mode privat** (per defecte): l'API requereix API key. La PWA l'envia al header. nomes l'hortola te accés.

2. **Mode obert** (opcional): publiquem algunes dades anonimitzades a un bucket InfluxDB separat, sense autenticacio. Qualsevol pot veure la temperatura mitjana de l'hort, pero no les lectures individuals.

Aixo es el concepte de **dades obertes (open data)**: fer accessibles dades que son d'interes public. Molts ajuntaments ho fan amb sensors urbans. L'avantatge es que la comunitat pot col·laborar, validar, i crear noves aplicacions sobre les dades.

## Connexions amb altres capitols

- **M7 Cap 7** - L'API que la PWA consumeix.
- **M7 Cap 4** - L'arquitectura completa de la que la PWA es la cara visible.
- **M7 Cap 6** - InfluxDB es on son les dades que la PWA mostra.
- **M7 Cap 10** - Casos reals d'uso de la PWA per l'hortola.
