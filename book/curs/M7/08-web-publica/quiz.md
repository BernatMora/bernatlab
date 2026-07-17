# Qüestionari - Capitol 8: PWA i web publica de l'Hort Osona

> 10 preguntes · ~15 min

## Pregunta 1
Que vol dir PWA?

- [ ] Pretty Web Application
- [x] Progressive Web App
- [ ] Personal Web Access
- [ ] Portable Wireless App

## Pregunta 2
Quins son els 3 ingredients basics d'una PWA?

- [ ] HTML, CSS, JS
- [ ] React, Vue, Angular
- [x] HTTPS, manifest.json, service worker
- [ ] Vite, npm, package.json

## Pregunta 3
Quin servei fem servir per allotjar la PWA de l'Hort Osona?

- [ ] Vercel
- [ ] Netlify
- [x] GitHub Pages
- [ ] AWS S3

## Pregunta 4
Quina llibreria JavaScript es la mes popular per fer grafiques en una PWA?

- [ ] D3.js
- [x] Chart.js
- [ ] Highcharts
- [ ] Plotly

## Pregunta 5
Que fa un Service Worker?

- [ ] Executa el backend
- [x] Intercepta peticions i pot fer la PWA disponible offline
- [ ] Crea la base de dades
- [ ] Genera el manifest

## Pregunta 6
Quin es l'avantatge principal d'una PWA respecte a una app nativa?

- [ ] Es mes rapida
- [x] Multiplataforma amb una sola codebase i sense passar revisio de botigues
- [ ] Te mes acces a sensors
- [ ] Funciona millor offline

## Pregunta 7
Quin navegador te mes suport per PWAs?

- [ ] Safari
- [x] Chrome / Edge / Firefox
- [ ] Internet Explorer
- [ ] Opera Mini

## Pregunta 8
Quin fitxer JSON conte la configuracio de la PWA (icones, colors, nom)?

- [ ] package.json
- [x] manifest.json
- [ ] sw.js
- [ ] config.json

## Pregunta 9 (oberta)
Explica la diferencia entre una app nativa, una web app tradicional i una PWA. Dona avantatges i inconvenients de cada una aplicat a l'Hort Osona.

Pistes per respondre:
- Nativa: maxima potencia, maxim cost (iOS + Android). Limitat per botigues.
- Web tradicional: nomes online, sense instal·lacio. Limitada.
- PWA: instal·lable, offline, multiplataforma. Limitada en APIs natives.
- L'Hort Osona no necessita acces a Bluetooth nadiu; la PWA es perfecta.

## Pregunta 10 (oberta)
Vols que les dades del teu hort siguin publiques (open data). Explica com ho faries: quines dades publiques, quines privades, com mantindries la seguretat de l'API privada.

Pistes per respondre:
- Dades publiques: temperatures mitjanes horaries, no lectures individuals.
- Dades privades: lectures raw, configuracio, comandes.
- Dos buckets d'InfluxDB: un privat amb API key, un altre public sense auth.
- Dos endpoints a l'API: /private/* i /public/*.


## Pregunta 11 (oberta amb pistes)
Per que sha de fer una web publica per a un hort privat

**Pistes**: pensa en com aplicaries aquest concepte al teu hort IoT amb la teva RPi (hortosona, 100.115.134.76).
## Pregunta 12 (oberta amb pistes)
Explica que es una PWA i quins avantatges te per a lhort

**Pistes**: pensa en com aplicaries aquest concepte al teu hort IoT amb la teva RPi (hortosona, 100.115.134.76).
## Pregunta 13 (oberta amb pistes)
Com promouriaries la teva web dhort a la teva comunitat local

**Pistes**: pensa en com aplicaries aquest concepte al teu hort IoT amb la teva RPi (hortosona, 100.115.134.76).
