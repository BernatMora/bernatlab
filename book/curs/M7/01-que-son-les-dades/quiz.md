# Qüestionari - Capitol 1: Que son les dades d'un hort

> 10 preguntes · ~15 min

## Pregunta 1
Quines son les quatre families principals de dades d'un hort?

- [ ] Sensorials, visuals, manuals, automatiques
- [x] Ambientals, de soll, de cultiu, de gestio
- [ ] Temperatura, humitat, llum, vent
- [ ] Diares, setmanals, mensuals, anuals

## Pregunta 2
Quin sensor s'utilitza habitualment per mesurar temperatura i humitat ambient?

- [ ] MiFlora
- [x] BME280
- [ ] LoRa SX1262
- [ ] InfluxDB

## Pregunta 3
Que indica la conductivitat electrica (EC) del soll?

- [ ] La temperatura del terreny
- [x] La salinitat i presencia de nutrients
- [ ] La pluja caiguda
- [ ] La presencia de plagues

## Pregunta 4
A quina freqüencia es raonable capturar dades de temperatura ambient?

- [ ] Cada segon
- [ ] Cada hora
- [x] Cada 5 minuts
- [ ] Un cop al dia

## Pregunta 5
On guardaries les imatges de la camera time-lapse?

- [ ] A InfluxDB
- [ ] A PostgreSQL
- [x] A MinIO o sistema de fitxers
- [ ] A Redis

## Pregunta 6
Per que es recomana NO capturar dades a 1 Hz si no cal?

- [ ] Perque el sensor es espatlla
- [x] Perque la base de dades creix rapidissim i gastes memoria i CPU
- [ ] Perque es il·legal
- [ ] Perque el WiFi no ho permet

## Pregunta 7
Quina dada es considera "de gestio"?

- [ ] Temperatura del soll
- [ ] Humitat relativa
- [x] Registre d'un reg amb la seva durada
- [ ] Lectura del sensor MiFlora

## Pregunta 8
Quin es el magatzem mes adequat per series temporals de sensors?

- [ ] MySQL
- [x] InfluxDB
- [ ] SQLite
- [ ] MongoDB

## Pregunta 9 (oberta)
Explica amb les teves paraules quina diferencia hi ha entre les dades ambientals i les dades de soll. Posa un exemple de cada una aplicat a un hort de tomàquets.

Pistes per respondre:
- Pensa en que "envolta" la planta vs. que esta "a" la planta.
- Dades ambientals: el que veus mirant amunt.
- Dades de soll: el que veus si claves el dit a terra.
- Dona un valor concret (ex. 25°C ambient vs. 18°C soll).

## Pregunta 10 (oberta)
Tens un hort amb 4 sectors i vols decidir a quina freqüencia captures cada sensor. Escriu una taula amb 4 tipus de sensor i la freqüencia que triaries, justificant per que.

Pistes per respondre:
- Pluja ha de ser mes frequent que temperatura.
- Les dades que canvien rapid (llum, vent) requereixen mes captures.
- Massa dades saturen InfluxDB; poques dades perden detalls.
- Exemple: BME280 cada 5 min, pluviometre cada 1 min, EC del soll cada 30 min.


## Pregunta 11 (oberta amb pistes)
Per que les dades son tan importants per a l'agricultura moderna

## Pregunta 12 (oberta amb pistes)
Explica que es la piramide de dades DIKW i com sha daplicar al teu hort

## Pregunta 13 (oberta amb pistes)
Quines dades voldries recollir del teu hort amb una llista prioritzada
