# Resum — Capítol 10: Full de ruta

## La idea clau

Aquest capítol no introdueix una sola eina, sinó que dibuixa el **mapa del que vindrà** després del Mòdul 1. Ja tens els fonaments: Raspberry Pi, Linux, SSH+Tailscale, Docker, Portainer, Uptime Kuma, Homepage, Git. Ara veurem quines eines hi posarem al damunt per construir el BernatLab complet: gestió de fitxers, automatització, bases de dades, gràfiques avançades, missatgeria IoT i l'Hort Osona amb sensors LoRa. Tots aquests temes es desenvoluparan en profunditat als mòduls M2-M5, però aquí en tens la visió panoràmica.

## El BernatLab en una pàgina

```
                        [Homepage 3010]
                              |
            +-----------------+------------------+
            |                 |                  |
       [Portainer 9000] [Uptime Kuma 3001] [File Browser 8082]
            |                 |                  |
   +--------+------+   +-----+-------+    +-----+------+
   |  Docker     |   |  Monitors   |    |  SMB/NFS  |
   +--+-----+----+   +-------------+    +------------+
      |     |
[Apps] [DBs]
```

## File Browser — el navegador de fitxers web

**Què és**: una interfície web per navegar, pujar, baixar, editar i compartir fitxers del servidor. Imagina't un "Google Drive" però allotjat a casa teva.

**Per què l'usem**: sovint volem accedir als fitxers del homelab sense haver de fer SSH. Amb File Browser, pots:

- Pujar fotos des del mòbil a la RPi.
- Descarregar documents des de qualsevol lloc.
- Editar fitxers `.txt` o `.md` al navegador.
- Crear usuaris amb permisos específics.
- Compartir fitxers per enllaç temporal.

**Stack**: imatge Docker `filebrowser/filebrowser:latest`, port 8082. Muntatge del directori `~/homelab/data` o similar.

**Capítol dedicat**: M2-12 (Emmagatzematge i compartició de fitxers).

## Node-RED — el Lego de l'automatització

**Què és**: una eina de programació visual (low-code) basada en fluxos. Connectes "nodes" (blocs) per crear automatitzacions sense escriure codi.

**Per què l'usem**: és la peça clau per connectar sensors, serveis i automatitzacions. Exemples:

- "Quan el sensor de temperatura puja de 30°C, envia'm un Telegram".
- "Quan comença a ploure, tanca les persianes de l'hort".
- "Cada nit a les 23h, fes backup dels volums Docker".
- "Quan rebo un correu amb adjunt, desa'l a una carpeta".

**Stack**: imatge `nodered/node-red:latest`, port 1880. Basat en Node.js, molt lleuger (~100 MB RAM).

**Capítol dedicat**: M3-19 (Node-RED: el cor de l'automatització).

## MQTT — el protocol de missatgeria IoT

**Què és**: un protocol de missatgeria lleuger (publish/subscribe) pensat per a dispositius IoT. Un "broker" (servidor central) rep missatges de "publishers" (publicadors) i els distribueix a "subscribers" (subscriptors).

**Per què l'usem**: és l'estàndard de facto per comunicar sensors amb el món. Un sensor de temperatura publica `temp/sala = 23.5` al broker, i qualsevol subscriptor (Node-RED, InfluxDB, Grafana, un script) pot rebre'l.

**Stack**: broker Eclipse Mosquitto (`eclipse-mosquitto:latest`), ports 1883 (MQTT) i 9001 (WebSockets).

**Conceptes clau**:

- **Topic**: ruta del missatge (p. ex. `hortosona/sensor/temp`).
- **Payload**: el missatge en si (sovint JSON o número).
- **QoS**: nivell de qualitat del servei (0, 1, 2).
- **Retain**: el broker guarda l'últim missatge d'un topic.

**Capítol dedicat**: M4-25 (MQTT: el protocol IoT).

## InfluxDB — la base de dades de sèries temporals

**Què és**: una base de dades optimitzada per emmagatzemar **dades amb marca temporal** (sèries temporals): temperatures cada 30s, lectures de sensors, mètriques de sistema.

**Per què l'usem**: les bases de dades relacionals (PostgreSQL) no escalen bé amb milions de lectures per segon. InfluxDB està dissenyada exactament per a aquest cas.

**Diferència amb PostgreSQL**:

- **InfluxDB**: sèries temporals, alta velocitat d'inserció, retenció curta (dies/mesos), consultes d'agregació eficients.
- **PostgreSQL**: dades estructurades, transaccions ACID, consultes complexes, retenció llarga.

**Stack**: InfluxDB 2.x (`influxdb:latest`), port 8086. Té UI web per a consultes visuals.

**Capítol dedicat**: M4-26 (InfluxDB: emmagatzemant dades temporals).

## Grafana — el rei de les gràfiques

**Què és**: una plataforma de visualització de dades. Crea dashboards amb gràfiques, taules, alertes, etc., a partir de múltiples fonts de dades (InfluxDB, Prometheus, PostgreSQL, MySQL, Loki, etc.).

**Per què l'usem**: InfluxDB emmagatzema dades, Grafana les visualitza. Combinació clàssica per a qualsevol projecte IoT.

**Exemple de dashboard**:

- Gràfica de temperatura de l'hort les últimes 24h.
- Gràfica d'humitat del terra.
- Comptador de peticions DNS a PiHole.
- Mètriques de CPU/RAM/Disc de la RPi.
- Comptador d'aigua consumida (si tens comptador intel·ligent).

**Stack**: `grafana/grafana:latest`, port 3000 (intern) o 3030 (host al BernatLab).

**Capítol dedicat**: M4-27 (Grafana: visualitzant dades com un pro).

## PostgreSQL — la base de dades relacional

**Què és**: la base de dades relacional open-source més avançada. Emmagatzema dades en taules amb relacions, suporta SQL complet, transaccions ACID, extensions.

**Per què l'usem**: alguns serveis del BernatLab necessiten persistència estructurada:

- Gitea (repositoris, usuaris).
- Nextcloud (metadades de fitxers, calendaris, contactes).
- Paperless-ngx (documents escanejats).
- Bookstack (wiki personal).
- Authentik (usuaris, sessions, ACLs).

**Stack**: `postgres:16-alpine`, port 5432. Sovint acompanyada de `pgadmin` per a administració visual.

**Al BernatLab**: farem servir una instància compartida o una per servei. La instància compartida és més eficient en RAM però aïlla menys.

**Capítol dedicat**: M2-15 (PostgreSQL: la base de dades de tota la vida).

## LoRa / LoRaWAN — comunicació de llarg abast

**Què és**: una tecnologia de ràdio de baix consum i llarg abast (1-10 km en zona rural, 1-3 km en urbana). Permet dispositius IoT amb bateries que duren anys.

**Per què l'usem**: l'Hort Osona (un dels projectes del BernatLab) té sensors distribuïts pel camp. Sense WiFi ni cobertura cel·lular, LoRa és l'única opció pràctica.

**Stack**:

- **Gateway**: dispositiu que rep els senyals LoRa i els passa a Internet (Heltec, Dragino, RAK).
- **Servidor de xarxa**: ChirpStack (open-source) allotjat a la RPi o un Mini PC.
- **Dispositius finals**: sensors de temperatura, humitat, humitat del terra, etc.

**Freqüències a Europa**: 868 MHz. Cal respectar la regulació (límit de potència i duty cycle).

**Capítol dedicat**: M5-31 (LoRaWAN: connectant l'hort).

## Mapa complet: cap a on anem

```
M1 (Fonaments) ......... JA FET (caps 1-10)
M2 (Productivitat) ..... File Browser, PostgreSQL, Nextcloud, Gitea, Paperless, Bookstack
M3 (Automatització) .... Node-RED, Home Assistant, scripts
M4 (Dades) ............. MQTT, InfluxDB, Grafana, Prometheus
M5 (IoT) ............... LoRaWAN, sensors, Hort Osona
```

Aquest curs és un viatge llarg. M1 és la base. A partir d'aquí, cada mòdul és independent però es construeix sobre els anteriors.

## Recursos addicionals

- **Web del curs**: https://bernatmora.cat/curs (a construir).
- **Repositori del curs**: https://github.com/BernatMora/bernatlab (a construir).
- **Docker Hub**: https://hub.docker.com per buscar imatges.
- **Awesome-Selfhosted**: https://github.com/awesome-selfhosted/awesome-selfhosted — llistat curat de programari self-hosted.

## Connexions amb altres capítols

- **Cap 1-9** — Tots els fonaments que ja tens.
- **M2 (a partir del cap 11)** — Productivitat.
- **M3 (a partir del cap 17)** — Automatització.
- **M4 (a partir del cap 24)** — Dades i visualització.
- **M5 (a partir del cap 30)** — IoT i Hort Osona.

Felicitats! Has acabat el Mòdul 1 del curs del BernatLab. Ara ve el millor: construir un homelab de veritat.
