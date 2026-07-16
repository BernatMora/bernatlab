# Exercici practic - Capitol 8: PWA i web publica de l'Hort Osona

> 45-60 min · Real amb un repo de GitHub

## Objectiu

Crear una PWA minima per l'Hort Osona que mostri l'ultima lectura dels sensors i una grafica d'historic. Publicar-la a GitHub Pages i verificar que es pot instal·lar.

## Requisits

- Compte de GitHub
- Coneixement basic de HTML, CSS, JavaScript
- API de l'Hort Osona funcionant (o una API mock)
- 45-60 min

## Pas 1: Estructura del projecte (5 min)

```bash
mkdir -p ~/hort-osona-web
cd ~/hort-osona-web

# Estructura basica
mkdir -p icons
touch index.html app.js sw.js manifest.json styles.css README.md
```

Estructura final:

```
hort-osona-web/
   index.html
   app.js
   sw.js
   manifest.json
   styles.css
   README.md
   icons/
      icon-192.png    <- icona 192x192
      icon-512.png    <- icona 512x512
```

Pots obtenir les icones del [repositori hort-osona](https://github.com/BernatMora/hort-osona/tree/main/web/icons) o crear-ne unes amb qualsevol editor.

## Pas 2: manifest.json (5 min)

```json
{
  "name": "Hort Osona",
  "short_name": "HortOsona",
  "description": "Monitoratge de l'hort en temps real",
  "start_url": "./index.html",
  "display": "standalone",
  "orientation": "portrait",
  "background_color": "#f5f5f5",
  "theme_color": "#2e7d32",
  "lang": "ca",
  "icons": [
    {
      "src": "icons/icon-192.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "icons/icon-512.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ]
}
```

## Pas 3: index.html (5 min)

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
       <p class="subtitle" id="subtitle">Carregant...</p>
   </header>

   <main>
       <section id="sensors-grid" class="grid">
           <!-- Renderitzat per app.js -->
       </section>

       <section class="chart-section">
           <h2>Humitat del soll (24h)</h2>
           <canvas id="moisture-chart"></canvas>
       </section>
   </main>

   <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0"></script>
   <script src="app.js"></script>
   <script>
       if ('serviceWorker' in navigator) {
           navigator.serviceWorker.register('sw.js')
               .then(() => console.log('SW registrat'))
               .catch(e => console.error('SW error:', e));
       }
   </script>
</body>
</html>
```

## Pas 4: styles.css (5 min)

```css
* {
   box-sizing: border-box;
   margin: 0;
   padding: 0;
}

body {
   font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif;
   background: #f5f5f5;
   color: #222;
   line-height: 1.5;
}

header {
   background: #2e7d32;
   color: white;
   padding: 1.5rem;
   text-align: center;
   box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

header h1 {
   font-size: 1.5rem;
   margin-bottom: 0.25rem;
}

.subtitle {
   font-size: 0.9rem;
   opacity: 0.9;
}

main {
   max-width: 1100px;
   margin: 0 auto;
   padding: 1rem;
}

.grid {
   display: grid;
   grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
   gap: 1rem;
   margin-bottom: 2rem;
}

.card {
   background: white;
   border-radius: 8px;
   padding: 1rem;
   box-shadow: 0 1px 3px rgba(0,0,0,0.08);
}

.card h2 {
   font-size: 1rem;
   color: #2e7d32;
   margin-bottom: 0.5rem;
}

.metric {
   display: flex;
   justify-content: space-between;
   padding: 0.25rem 0;
   font-size: 0.9rem;
}

.metric .label {
   color: #666;
}

.metric .value {
   font-weight: 600;
}

.chart-section {
   background: white;
   border-radius: 8px;
   padding: 1rem;
   box-shadow: 0 1px 3px rgba(0,0,0,0.08);
}

.chart-section h2 {
   font-size: 1.1rem;
   margin-bottom: 1rem;
   color: #2e7d32;
}

.error {
   color: #c62828;
   font-size: 0.9rem;
}
```

## Pas 5: app.js (15 min)

```javascript
// ====== Configuracio ======
const API_URL = 'http://localhost:5000/api/v1';
const API_KEY = 'hort-osona-test-key-2026';

const SENSORS = [
   { id: 'miflora-1B32', nom: 'Tomàquet cherry' },
   { id: 'miflora-1B33', nom: 'Pebrot italia' },
   { id: 'miflora-1B34', nom: 'Enciam' },
];

// ====== API calls ======
async function getLatest(deviceId) {
   const r = await fetch(`${API_URL}/sensors/${deviceId}/latest`, {
       headers: { 'X-API-Key': API_KEY }
   });
   if (!r.ok) throw new Error(`HTTP ${r.status}`);
   return r.json();
}

async function getHistory(deviceId, field, hours = 24) {
   const r = await fetch(
       `${API_URL}/sensors/${deviceId}/history?h=${hours}&field=${field}`,
       { headers: { 'X-API-Key': API_KEY } }
   );
   if (!r.ok) throw new Error(`HTTP ${r.status}`);
   return r.json();
}

// ====== Render ======
function renderCard(sensor, data) {
   if (data.error) {
       return `
           <div class="card">
               <h2>${sensor.nom}</h2>
               <p class="error">${data.error}</p>
           </div>
       `;
   }
   const f = data.fields || {};
   return `
       <div class="card">
           <h2>${sensor.nom}</h2>
           <div class="metric">
               <span class="label">Humitat:</span>
               <span class="value">${f.soil_moisture?.toFixed(1) ?? '-'}%</span>
           </div>
           <div class="metric">
               <span class="label">Temp soll:</span>
               <span class="value">${f.soil_temp_c?.toFixed(1) ?? '-'}°C</span>
           </div>
           <div class="metric">
               <span class="label">EC:</span>
               <span class="value">${f.ec_us_cm ?? '-'} µS/cm</span>
           </div>
           <div class="metric">
               <span class="label">Bateria:</span>
               <span class="value">${f.battery ?? '-'}%</span>
           </div>
       </div>
   `;
}

async function renderSensors() {
   const grid = document.getElementById('sensors-grid');
   const data = await Promise.all(
       SENSORS.map(async s => {
           try {
               return await getLatest(s.id);
           } catch (e) {
               return { device: s.id, error: e.message };
           }
       })
   );
   grid.innerHTML = SENSORS
       .map((s, i) => renderCard(s, data[i]))
       .join('');

   const subtitle = document.getElementById('subtitle');
   const now = new Date().toLocaleTimeString('ca');
   subtitle.textContent = `Última actualització: ${now}`;
}

// ====== Chart ======
let chart = null;

async function renderChart() {
   const data = await getHistory('miflora-1B32', 'soil_moisture', 24);
   const ctx = document.getElementById('moisture-chart').getContext('2d');

   if (chart) chart.destroy();
   chart = new Chart(ctx, {
       type: 'line',
       data: {
           labels: data.points.map(p => new Date(p.ts).toLocaleTimeString('ca', { hour: '2-digit', minute: '2-digit' })),
           datasets: [{
               label: 'Humitat del sòl (%)',
               data: data.points.map(p => p.value),
               borderColor: '#2e7d32',
               backgroundColor: 'rgba(46, 125, 50, 0.1)',
               tension: 0.3,
               fill: true
           }]
       },
       options: {
           responsive: true,
           plugins: {
               legend: { display: true }
           },
           scales: {
               y: { beginAtZero: false, suggestedMin: 20, suggestedMax: 80 }
           }
       }
   });
}

// ====== Init ======
async function init() {
   await renderSensors();
   await renderChart();
}

init();
setInterval(init, 60000);  // refresca cada minut
```

## Pas 6: sw.js - Service Worker (5 min)

```javascript
const CACHE = 'hort-osona-v1';
const ASSETS = [
   './',
   './index.html',
   './app.js',
   './styles.css',
   './manifest.json',
   './icons/icon-192.png',
   './icons/icon-512.png',
];

self.addEventListener('install', (e) => {
   e.waitUntil(
       caches.open(CACHE).then(c => c.addAll(ASSETS))
   );
});

self.addEventListener('activate', (e) => {
   e.waitUntil(
       caches.keys().then(keys =>
           Promise.all(
               keys.filter(k => k !== CACHE).map(k => caches.delete(k))
           )
       )
   );
});

self.addEventListener('fetch', (e) => {
   e.respondWith(
       caches.match(e.request).then(r => r || fetch(e.request))
   );
});
```

## Pas 7: Publicar a GitHub Pages (10 min)

```bash
cd ~/hort-osona-web
git init
git add .
git commit -m "PWA Hort Osona v1"
git branch -M main
git remote add origin git@github.com:<el-teu-usuari>/hort-osona-web.git
git push -u origin main
```

A GitHub:

1. Ves al repo -> Settings -> Pages.
2. Source: "Deploy from a branch".
3. Branch: `main` / root.
4. Save.

Espera 1-2 minuts. La PWA es accessible a `https://<el-teu-usuari>.github.io/hort-osona-web/`.

## Pas 8: Provar la PWA (5 min)

1. Obre la URL al Chrome.
2. Mira la consola del navegador (F12) per errors.
3. Comprova que veus les 3 cards de sensors.
4. Comprova que veus la grafica d'humitat.
5. A la barra d'adreces, busca la icona d'instal·lacio (un cuadrat amb una fletxa). Instal·la.
6. Tanca la pestanya i obre l'app des de la pantalla d'inici. Hauria d'obrir-se a pantalla completa.
7. Prova de desactivar el WiFi i tornar a obrir. Hauria de carregar des de cache.

## Validacio

Has acabat si:

- [ ] Tots els fitxers (HTML, CSS, JS, manifest, sw) existeixen i son validats.
- [ ] La PWA es carrega correctament al navegador.
- [ ] Mostra les 3 cards de sensors i la grafica.
- [ ] Es pot instal·lar ("Add to Home Screen").
- [ ] Funciona offline despres de la primera carrega.
- [ ] Esta publicada a GitHub Pages i es accessible publicament.

## Per aprofundir

- Afegeix WebSockets per actualitzar la UI en temps real.
- Implementa notificacions push amb `Notification` API.
- Usa Vite + Vue per a una experiencia de desenvolupament millor.
- Afegeix autenticacio amb Auth0 o Clerk.
- Publica tambe una versio "open data" sense autenticacio.
- Activa Lighthouse al DevTools per optimitzar el rendiment.
