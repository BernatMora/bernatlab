# Qüestionari — Capítol 10: Full de ruta

> 15 preguntes · ~20 min

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

## Pregunta 9
Quin dels següents mòduls del curs tracta sobre productivitat i eines de treball personal?

- [ ] M3
- [x] M2
- [ ] M4
- [ ] M5

## Pregunta 10
Quin avantatge té Home Assistant respecte Node-RED per a automatització domèstica?

- [ ] És més lleuger
- [x] Té integracions natives amb molts fabricants de dispositius
- [ ] Funciona sense Docker
- [ ] És gratuït

## Pregunta 11
Quin és el risc principal de tenir massa serveis al BernatLab?

- [ ] Lentitud del WiFi
- [x] Saturar la RAM, el processador o la microSD
- [ ] Quedar-se sense endolls
- [ ] Augmentar la factura de la llum

## Pregunta 12
Quin és el primer pas recomanable abans d'afegir un servei nou al BernatLab?

- [ ] Comprar hardware nou
- [x] Comprovar si tens prou RAM i disc, i si el servei té sentit al projecte
- [ ] Demanar permís a Google
- [ ] Aprendre Kubernetes

## Pregunta 13 (oberta)
Explica amb les teves paraules: com es connecten les peces del BernatLab per a un projecte IoT concret (per exemple, mesurar la temperatura de l'hort i veure-la a una gràfica)? Quin és el flux MQTT → InfluxDB → Grafana?

Pistes per respondre:
- Qui genera la dada? (sensor LoRa)
- Qui la rep? (broker MQTT)
- On s'emmagatzema? (InfluxDB)
- Com es visualitza? (Grafana)
- Quin paper juga Node-RED?

## Pregunta 14 (oberta)
Tria un dels projectes del curs (M2-M5) que t'atrapi més. Per què? Quin problema t'ajudarà a resoldre? Quines eines hi hauries d'utilitzar?

Pistes per respondre:
- M2 = productivitat (Nextcloud, Gitea...).
- M3 = automatització (Node-RED, Home Assistant...).
- M4 = dades (InfluxDB, Grafana...).
- M5 = IoT (LoRa, sensors...).

## Pregunta 15 (oberta)
Al cap d'un any tens el BernatLab ple de serveis, amb 8 GB de RAM usats dels 4 GB que tens, i la microSD al 90%. Quines decisions hauries de prendre? Enumera 3 opcions amb els seus pros i contres.

Pistes per respondre:
- Escalar horitzontalment vs verticalment què vol dir?
- Migrar a un mini PC val la pena?
- Què passa amb els serveis existents si toques el hardware?
- Quin és el cost real (no només econòmic) d'ampliar?
