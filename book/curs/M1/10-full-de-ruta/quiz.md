# Qüestionari — Capítol 10: Full de ruta

> 10 preguntes · ~15 min

## Pregunta 1
Quin és el rol de File Browser al BernatLab?

- [ ] Monitorar serveis
- [x] Navegar, pujar, baixar i editar fitxers des del navegador
- [ ] Crear gràfiques
- [ ] Executar scripts

## Pregunta 2
Quin tipus d'eina és Node-RED?

- [ ] Un sistema operatiu
- [x] Una eina de programació visual basada en fluxos
- [ ] Una base de dades
- [ ] Un navegador web

## Pregunta 3
Què és MQTT?

- [ ] Una base de dades
- [x] Un protocol de missatgeria lleuger publish/subscribe per a IoT
- [ ] Un llenguatge de programació
- [ ] Un sistema de fitxers

## Pregunta 4
Per a què serveix InfluxDB?

- [ ] Per allotjar webs
- [x] Per emmagatzemar dades de sèries temporals (temperatura, mètriques, sensors)
- [ ] Per monitorar serveis
- [ ] Per xifrar connexions

## Pregunta 5
Quin és el rol de Grafana?

- [ ] Emmagatzemar dades
- [x] Visualitzar dades amb dashboards, gràfiques i alertes
- [ ] Executar scripts
- [ ] Connectar sensors

## Pregunta 6
Quina és la diferència principal entre InfluxDB i PostgreSQL?

- [ ] InfluxDB és per a webs, PostgreSQL per a apps
- [x] InfluxDB és per a sèries temporals d'alta velocitat; PostgreSQL per a dades estructurades
- [ ] Són el mateix
- [ ] PostgreSQL és més ràpid

## Pregunta 7
Què és LoRa?

- [ ] Un protocol WiFi
- [x] Una tecnologia de ràdio de baix consum i llarg abast per a IoT
- [ ] Un sistema operatiu
- [ ] Un tipus de base de dades

## Pregunta 8
A quina freqüència opera LoRa a Europa?

- [ ] 2.4 GHz
- [ ] 5 GHz
- [x] 868 MHz
- [ ] 433 MHz (permès en altres regions)

## Pregunta 9 (oberta)
Explica amb les teves paraules: com es connecten les peces del BernatLab per a un projecte IoT concret (per exemple, mesurar la temperatura de l'hort i veure-la a una gràfica)? Quin és el flux MQTT → InfluxDB → Grafana?

Pistes per respondre:
- Qui genera la dada? (sensor LoRa)
- Qui la rep? (broker MQTT)
- On s'emmagatzema? (InfluxDB)
- Com es visualitza? (Grafana)
- Quin paper juga Node-RED?

## Pregunta 10 (oberta)
Tria un dels projectes del curs (M2-M5) que t'atrapi més. Per què? Quin problema t'ajudarà a resoldre? Quines eines hi hauries d'utilitzar?

Pistes per respondre:
- M2 = productivitat (Nextcloud, Gitea...).
- M3 = automatització (Node-RED, Home Assistant...).
- M4 = dades (InfluxDB, Grafana...).
- M5 = IoT (LoRa, sensors...).
