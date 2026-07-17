# Qüestionari - Capitol 10: Visualitzacio amb Grafana

> 15 preguntes · ~20 min

## Pregunta 1
Quin es el port per defecte de Grafana?

- [ ] 8080
- [x] 3000
- [ ] 9090
- [ ] 80

## Pregunta 2
Quin llenguatge de consultes fa servir Grafana amb InfluxDB 2?

- [ ] SQL
- [ ] InfluxQL
- [x] Flux
- [ ] PromQL

## Pregunta 3
Quin tipus de grafic es millor per a series temporals?

- [ ] Pie chart
- [x] Time series (linia)
- [ ] Bar chart
- [ ] Table

## Pregunta 4
Que es un "dashboard" a Grafana?

- [ ] Un servidor
- [x] Una coleccio de panells (grafics)
- [ ] Una base de dades
- [ ] Un contenidor Docker

## Pregunta 5
Quin tipus de grafic mostraries per a la humitat actual?

- [ ] Time series
- [x] Stat (Big number)
- [ ] Heatmap
- [ ] Pie chart

## Pregunta 6
Que es una alerta a Grafana?

- [ ] Un log derror
- [x] Un avis automatic quan una dada surt dels limits
- [ ] Un backup
- [ ] Un reinici del servidor

## Pregunta 7
Quines fonts de dades pot connectar Grafana? (sellecciona la millor resposta)

- [ ] Nomes InfluxDB
- [ ] Nomes Prometheus
- [x] Multiples: InfluxDB, Prometheus, PostgreSQL, MySQL, Loki, etc.
- [ ] Nomes fitxers CSV

## Pregunta 8
Que es una variable a Grafana?

- [x] Un parametre dinamic (com $sensor) que es pot canviar desde la UI
- [ ] Una contrasenya
- [ ] Un identificador unic
- [ ] Un nom de taula

## Pregunta 9 (oberta)
Per que Grafana es millor que veure les dades directament a InfluxDB (amb la UI web)? Pensa en un pages que vol veure la temperatura del seu hivernacle cada mati.

Pistes per respondre:
- Quina diferencia hi ha entre veure una taula i un grafic?
- Quant de temps triga un pages a entendre una taula de 1000 files?
- Es poden compartir els dashboards?
- Es poden rebre alertes automatiques?

## Pregunta 10 (oberta)
Dissenya un dashboard complet per a l'hort amb 5 panells. Quin grafic ficaries a cada un? Justifica cada decisio.

Pistes per respondre:
- Quin es el primer que vols veure al mati?
- Quines dades son critiques i quines son informatives?
- Quins tipus de grafics son millors per a cada cas?
- Voldries alertes? Per a quines dades?

## Pregunta 11 (oberta)
Per que creus que Grafana sha convertit en lestandard de facto per a visualitzacio de dades self-hosted? Quin valor te al BernatLab respecte a altres alternatives (Kibana, Metabase, etc)?

Pistes per respondre:
- Multi-font de dades (InfluxDB, Prometheus, PostgreSQL).
- Gran ecosistema de panells.
- Comunidad activa.
- Suporta multiples llenguatges de consulta.
- Trade-off: mes complexe que Metabase, pero mes potent.

## Pregunta 12 (oberta)
Quina relacio hi ha entre la freqUencia d'actualitzacio del dashboard i el consum de recursos? Com afecta al BernatLab tenir 10 dashboards actualitzant-se cada 5 segons vs cada minut?

Pistes per respondre:
- Cada actualitzacio = una consulta a la base de dades.
- 10 dashboards x 12 actualitzacions/minut = 120 consultes/minut.
- InfluxDB aguanta be pero consumeix recursos.
- Una RPi 4 pot saturar-se.
- Trade-off: temps real vs rendiment.

## Pregunta 13 (oberta)
Imagina que el teu company et diu: "Grafana es massa complicat, jo veig les dades amb la UI d'InfluxDB directament". Argumenta per que al BernatLab Grafana mereix el temps dinversio, especialment si vols compartir visualitzacions.

Pistes per respondre:
- UI d'InfluxDB es per fer consultes, no per presentar.
- Grafana permet panells visuals amb colors i icones.
- Alertes automatiques.
- Comparticio de dashboards amb un link.
- Embedding en altres webs.
- Trade-off: temps de setup vs experiencia dusuari.

## Pregunta 14 (oberta)
Aplica el concepte de Grafana al cas concret del BernatLab amb l'hort IoT. Tinc 10 sensors (temperatura, humitat, llum, etc) a 5 bancals. Dissenya 3 dashboards: un per ver de mati, un per analisi historica, un per alerting. Quin panell va a quin dashboard?

Pistes per respondre:
- Dashboard 1 (mati): visio rapida, numeros grans.
- Dashboard 2 (analisi): grafics detallats, comparatives.
- Dashboard 3 (alerting): llista de sensors amb problemes.
- Quin tipus de panell per a cada cas?

## Pregunta 15 (oberta)
Quines consequencies te per a la interpretacio de les dades triar un tipus de grafic inadequat? Com afecta al BernatLab la visualitzacio de temperatures d'un hivernacle amb un pie chart en lloc d'un time series? Argumenta amb exemples.

Pistes per respondre:
- Pie chart: mostra proporcions, no evolucio.
- Bar chart: comparacio entre categories, no evolucio temporal.
- Time series: idoni per evolucio temporal.
- Un grafic mal triat porta a conclusions erronies.
- Exemple: veure un pic de temperatura nomes en una taula pot no alertar.
- Trade-off: estetica vs claredat.
