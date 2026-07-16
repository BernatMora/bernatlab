# Respostes - Capitol 8: PWA i web publica de l'Hort Osona

> Mira les respostes DESPRES d'haver fet el qüestionari.

## Pregunta 1: Que vol dir PWA?

**Resposta correcta**: Progressive Web App.

**Explicacio**: PWA (Progressive Web App) es un terme encunyat per Google el 2015. Defineix una web app que utilitza tecnologies modernes (HTTPS, service workers, manifest) per oferir una experiencia similar a una app nativa. "Progressive" vol dir que funciona en qualsevol navegador, pero es torna mes "app-like" en els moderns.

---

## Pregunta 2: 3 ingredients d'una PWA?

**Resposta correcta**: HTTPS, manifest.json, service worker.

**Explicacio**: Aquests son els 3 requisits tecnics per a una PWA. Sense HTTPS el service worker no funciona. Sense manifest el navegador no pot "instal·lar" l'app. Sense service worker no hi ha funcionalitat offline ni push notifications. Hi ha mes coses (responsive design, fast loading) pero aquests son els minims.

---

## Pregunta 3: Hosting de la PWA?

**Resposta correcta**: GitHub Pages.

**Explicacio**: A l'Hort Osona usem GitHub Pages perque es gratuit, rapid, te HTTPS automatic, i s'integra amb el nostre repo. Alternatives: Vercel (millor per a Next.js), Netlify (molt flexible), Cloudflare Pages, AWS S3 + CloudFront. Tots son bons; GitHub Pages es la opcio mes simple per a un projecte open source.

---

## Pregunta 4: Llibreria de grafiques?

**Resposta correcta**: Chart.js.

**Explicacio**: Chart.js es la llibreria mes popular per fer grafiques en JS. Es petita (~80 KB), te una API senzilla, i funciona be amb Canvas. Alternatives: D3.js (mes potent pero mes complexe), Highcharts (comercial, mes features), Plotly (cientific). Per a una PWA d'hort, Chart.js es perfecte.

---

## Pregunta 5: Que fa un Service Worker?

**Resposta correcta**: Intercepta peticions i pot fer la PWA disponible offline.

**Explicacio**: Un service worker es un script JS que s'executa en un fil separat del navegador, entre la web i la xarxa. Pot interceptar totes les peticions HTTP i decidir si serveix des de la cache o des de la xarxa. Es el que permet que la PWA funcioni offline, rebi push notifications, i faci background sync.

---

## Pregunta 6: Avantatge respecte a app nativa?

**Resposta correcta**: Multiplataforma amb una sola codebase i sense passar revisio de botigues.

**Explicacio**: Una PWA es una sola codebase HTML/CSS/JS que funciona a iOS, Android, Windows, Mac, Linux. No cal desenvolupar dues apps natives, no cal pagar a Apple/Google, no cal passar la revisio (que pot trigar setmanes). Actualitzacions automaticques. Limitacio: no pot accedir a totes les APIs natives (Bluetooth a iOS, NFC, etc).

---

## Pregunta 7: Navegador amb mes suport?

**Resposta correcta**: Chrome / Edge / Firefox.

**Explicacio**: Chrome (i Chromium-based com Edge, Brave) te el millor suport per PWA. Safari (iOS) ha millorat molt pero encara te limitacions (per exemple, les push notifications nomes van si l'app esta a la pantalla d'inici). Firefox suporta PWA pero no ofereix "instal·lacio" tan clarament. Internet Explorer no suporta PWA (mort).

---

## Pregunta 8: Fitxer de configuracio?

**Resposta correcta**: manifest.json.

**Explicacio**: El `manifest.json` es un fitxer JSON que conte metadades sobre la PWA: nom, icones, colors, orientacio, URL d'inici. Es l'equivalent al `Info.plist` d'iOS o `AndroidManifest.xml` d'Android. Sense ell, el navegador no pot oferir "instal·lar l'app".

---

## Pregunta 9 (oberta): Nativa vs Web tradicional vs PWA

**Resposta model**:

**App nativa (iOS + Android)**: maxima potencia i acces a totes les APIs del dispositiu (Bluetooth Low Energy, NFC, sensors, camara, etc.). Rendiment optim (codi compilat). Pero **maxim cost**: cal desenvolupar dues apps (Swift/SwiftUI per iOS, Kotlin per Android), testejarlas per separat, i passar la revisio d'Apple i Google. Actualitzacions lentes. Per a l'Hort Osona, **overkill** - no necessitem cap API que nomes les natives tinguin.

**Web app tradicional**: nomes HTML/CSS/JS que es veu al navegador. No es pot instal·lar, no funciona offline, no te icona a la pantalla d'inici. **Limitada** per a l'us que li volem donar: l'hortola vol consultar dades des del telefon quan esta a l'hort (a vegades sense bona cobertura).

**PWA**: el millor dels dos mons. Es pot instal·lar (icona a la pantalla d'inici, obre en pantalla completa), funciona offline (gracies al service worker), es actualitza automaticament. **Multiplataforma amb una sola codebase** (HTML/CSS/JS). Limitada en APIs natives (no te acces a BLE a iOS, per exemple), pero per a l'Hort Osona no cal.

**Recomanacio per a l'Hort Osona**: **PWA** es la opcio correcta. L'hortola vol:
- Veure grafiques -> la PWA ho fa amb Chart.js.
- Consultar ultim valor -> la PWA ho fa amb `fetch` a l'API.
- Rebre alertes -> la PWA pot rebre push notifications.
- Usar-la al telefon -> la PWA es pot instal·lar i obre com app.

Si necessites BLE nadiu (per exemple, per configurar sensors directament des del telefon), llavors una app nativa es millor. Pero per a **consultar** dades, la PWA es perfecta i **10x mes barata** de desenvolupar.

---

## Pregunta 10 (oberta): Dades obertes vs privades

**Resposta model**:

**Dades privades (per defecte)**: les lectures raw dels sensors (cada 5 min), les dades del calendar de sembra, la configuracio, els logs. Son **personals** i **sensibles** - un atacant podria saber quan marxem de vacances, quan reguem, quan tenim tomàquets a punt. Aquestes dades requereixen autenticacio amb **API key** o **JWT**.

**Dades publiques (open data)**: les dades **agregades i anonimitzades** que son d'interes comunitari. Concretament, publicariem:
- Temperatura mitjana horaria de l'hort (no per sector, sino la global).
- Humitat mitjana del sòl.
- Pluviometria.
- "Estat general de l'hort" (OK, alerta, sense dades).

Mai publicariem lectures individuals per sector (revelaria quins sectors son productius), ni timestamps exactes (revelaria patrons d'activitat).

**Arquitectura tecnica**:

1. **Dos buckets d'InfluxDB**:
   - `hort-osona` (privat, amb autenticacio): totes les dades raw.
   - `hort-osona-public` (public, sense autenticacio o amb una clau publica): nomes les agregacions.

2. **Dos endpoints a l'API**:
   - `/api/v1/...` (privat, requereix `X-API-Key`): tot.
   - `/api/v1/public/...` (obert, nomes GET, rate limitat): agregacions.

3. **Una task a InfluxDB** que cada hora calcula les agregacions i les escriu al bucket public.

4. **Una web adicional** (e.g. `hort-osona-cat/open-data/`) que consumeix nomes els endpoints publics, sense cap autenticacio, i mostra grafiques agregades.

**Seguretat**: el bucket public nomes conte dades agregades i anonimitzades. Si un atacant llegeix tot, nomes veu "la temperatura mitjana de l'hort ahir va ser 18.5°C" - no pot deduir res d'util. La web publica te **rate limiting** (max 100 peticions/min per IP) per evitar scraping. I el bucket privat continua protegit per API key + HTTPS.

**Beneficis**: la comunitat pot validar que les dades son correctes, pot crear aplicacions derivades (e.g. un mapa de temperatures d'horts urbans d'Osona), i augmenta la transparencia del projecte. Es el que fan molts ajuntaments amb els seus sensors urbans (soroll, contaminacio, transit).

---

## Que fer si has fallat moltes preguntes

- **5-8 encerts**: Rellegir el resum, sobretot la part de service worker.
- **3-4 encerts**: Repassar els 3 ingredients d'una PWA.
- **0-2 encerts**: Comencem pel basic: que es una web app i com es desplega a GitHub Pages.

## Que fer si has encertat totes

- Passa al **Capitol 9** (calendari de sembra).
- Investiga Vue 3 + Vite per a una millor DX de PWA.
- Compara Workbox amb service workers fets a ma.
- Mira el projecte Hort Osona al GitHub de BernatMora per inspiracio.
- Llegeix sobre open data aplicat a horts urbans.
