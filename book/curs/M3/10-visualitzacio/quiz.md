# Qüestionari — Capitol 10: Visualitzacio amb Grafana

> 10 preguntes · ~15 min

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

- [ ] Un log d'error
- [x] Un avís automatic quan una dada surt dels limits
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
Per que Grafana es millor que veure les dades directament a InfluxDB (amb la UI web)? Pensa en un pagès que vol veure la temperatura del seu hivernacle cada matí.

Pistes per respondre:
- Quina diferencia hi ha entre veure una taula i un grafic?
- Quant de temps triga un pagès a entendre una taula de 1000 files?
- Es poden compartir els dashboards?
- Es poden rebre alertes automatiques?

## Pregunta 10 (oberta)
Dissenya un dashboard complet per a l'hort amb 5 panells. Quin grafic ficaries a cada un? Justifica cada decisio.

Pistes per respondre:
- Quin es el primer que vols veure al matí?
- Quines dades son critiques i quines son informatives?
- Quins tipus de grafics son millors per a cada cas?
- Voldries alertes? Per a quines dades?
