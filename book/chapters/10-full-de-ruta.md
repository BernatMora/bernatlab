# Capítol 10 — Full de ruta del BernatLab

> *"Un servidor mai no està acabat. Està en camí."*

## 10.1 On som

A dia d'avui, el BernatLab té:

- Una Raspberry Pi 4 amb Debian 13 Lite, funcionant 24/7.
- Tailscale, que ens permet accedir-hi des de qualsevol lloc.
- Tres serveis principals: Portainer, Uptime Kuma, Homepage.
- La web pública Hort Osona allotjada a GitHub Pages.
- Una estructura de carpetes clara a `/home/bernat/homelab/`.
- (Imminent) un sistema de documentació i versionat amb Git.

Això ja és molt. Molts homelabs no passen d'aquí en anys. Però al BernatLab tenim plans: volem convertir-lo en el centre de tots els nostres projectes, especialment Hort Osona, els sensors LoRa, l'automatització, la música, la IA i el desenvolupament web.

En aquest capítol veurem què vindrà. No és un pla rígid — és una llista de prioritats que anirem abordant a mesura que tinguem temps, coneixement i ganes. Algunes coses es faran en setmanes; d'altres, en mesos o trimestres. I totes les prendrem amb calma.

## 10.2 Estratègia general

La nostra estratègia és **creixement incremental**: afegir un servei, entendre'l bé, documentar-lo, i només després passar al següent. Mai no afegirem dues coses noves alhora. Mai no desplegarem un servei sense saber què fa i per què.

Això té tres avantatges:

1. **Redueix el risc d'errors**: cada canvi és petit i aïllat.
2. **Permet aprendre de veritat**: quan dediquem una setmana a entendre Node-RED, l'entenem.
3. **Genera confiança**: cada pas endavant és un pas que hem fet bé.

L'ordre de les prioritats ve determinat per:

- **Necessitat real**: el que ens serveix per als nostres projectes (Hort Osona, sensors).
- **Aprenentatge**: el que ensenya més i ens obre portes a més coses.
- **Complementarietat**: serveis que es connecten entre ells i creen un ecosistema útil.

## 10.3 Les pròximes passes, ordenades

### A. Integrar sensors al Hort Osona (curt termini)

Aquesta és la prioritat número u. Tenim (o tindrem aviat) sensors al terreny — sensors de temperatura, humitat del sòl, il·luminació, potser més — que volem que enviïn dades al BernatLab. La integració es farà en diverses fases:

**Fase 1 — Infraestructura MQTT**

- Desplegar **Mosquitto**, un broker MQTT lleuger.
- Configurar-lo per acceptar connexions des de la xarxa Tailscale.
- Documentar el patró de temes (topics) que farem servir.

**Fase 2 — Recepció i emmagatzematge**

- Desplegar **InfluxDB** per emmagatzemar les dades dels sensors (time series).
- Desplegar **Telegraf** per recollir dades de MQTT i escriure-les a InfluxDB.
- Configurar la retenció de dades (quants mesos guardem, com agreguem).

**Fase 3 — Visualització**

- Desplegar **Grafana** per crear dashboards amb gràfiques de les dades.
- Integrar Grafana amb Homepage (afegir targeta al panell).
- Fer que les dades siguin visibles des del mòbil (Grafana és responsive).

**Fase 4 — API pública**

- Desplegar una **API REST** (probablement amb Node-RED o amb un petit servidor Python/Node) que llegeixi d'InfluxDB i serveixi dades agregades.
- Publicar l'API perquè la web Hort Osona la pugui consumir.

**Fase 5 — Integració amb la web**

- Modificar la web Hort Osona perquè mostri dades en temps real (o quasi-real) consumint l'API.
- Això ja és feina de desenvolupament web, no de servidor, però el servidor n'és la base.

### B. File Browser — gestió de fitxers web

**File Browser** és una interfície web per explorar, pujar, descarregar i editar fitxers al servidor. És molt útil per:

- Gestionar les dades dels serveis sense entrar per SSH.
- Compartir fitxers amb altres dispositius de la xarxa Tailscale.
- Editar fitxers de configuració amb un editor web (per als moments en què no volem usar `nano`).

Es desplega fàcilment:

```yaml
services:
  filebrowser:
    image: filebrowser/filebrowser:latest
    container_name: filebrowser
    restart: unless-stopped
    ports:
      - "8080:80"
    volumes:
      - /home/bernat/homelab:/srv
      - /home/bernat/homelab/data/filebrowser:/database
```

Un cop configurat, ens donarà accés a tota la carpeta `/home/bernat/homelab` des del navegador. Compte amb els permisos: no volem que ningú que entri a File Browser pugui esborrar res crític per error.

### C. Node-RED — automatització visual

**Node-RED** és una eina de programació visual, basada en fluxos, que ens permet connectar serveis, sensors, APIs, bases de dades sense escriure codi tradicional. Es representa com una graella on arrosseguem nodes i els connectem amb cables.

Al BernatLab, Node-RED ens servirà per:

- Processar les dades dels sensors (netejar, agregar, transformar) abans d'escriure-les a InfluxDB.
- Crear automatitzacions: "si la temperatura del sòl baixa de 5 °C, envia'm un missatge a Telegram".
- Connectar serveis: quan Uptime Kuma detecta una caiguda, executar una acció.
- Crear la base de l'API de Hort Osona: un node HTTP que respongui a peticions web.

Node-RED té una comunitat enorme i milers de nodes preconfigurats per a tota mena de serveis. El seu punt feble és que pot esdevenir un embolic de fluxos difícil de mantenir. Per això, caldrà documentar bé cada flux.

### D. Mosquitto MQTT — el cor de la IoT

**MQTT** és un protocol de missatgeria lleuger, dissenyat específicament per a dispositius IoT. La seva filosofia és simple: un **broker** central (Mosquitto) rep missatges dels **publishers** (sensors) i els distribueix als **subscribers** (consumidors).

Ja n'hem parlat a la secció A. La diferència és que aquí el considerem com a servei independent, no pas com a part de la fase de sensors.

Característiques importants:

- Suporta QoS (qualitat de servei): 0 (com foc i oblida), 1 (almenys un cop), 2 (exactament un cop).
- Suporta retenció de missatges: l'últim valor queda disponible per als subscriptors nous.
- Suporta wildcards als temes: `sensors/+/temperature` selecciona tots els sensors.

Al BernatLab, el desplegarem amb una configuració que:

- Només accepti connexions autenticades.
- Restingeixi l'accés per ACL (llistes de control d'accés).
- Exposeixi el port 1883 a la xarxa Tailscale.

### E. InfluxDB — base de dades de sèries temporals

**InfluxDB** és una base de dades optimitzada per a **sèries temporals**: dades amb una marca de temps, com lectures de sensors, mètriques de sistema, preus, etc. A diferència d'una base de dades relacional, InfluxDB està dissenyada per:

- Emmagatzemar milions de punts de dades de forma compacta.
- Fer consultes ràpides sobre intervals temporals.
- Agregar dades (mitjanes, mínims, màxims) en temps real.

Al BernatLab, InfluxDB rebrà les dades dels sensors, les emmagatzemarà, i servirà per a Grafana. La configuració haurà de tenir en compte:

- **Retenció**: quant de temps guardem les dades en resolució original.
- **Continuous queries**: agregacions automàtiques (per exemple, "cada 10 minuts, calcula la mitjana horària i guarda-la").
- **Autenticació**: token d'accés per a Telegraf i Grafana.

Cal tenir present que InfluxDB pot ser exigent en recursos. Amb 4 GB de RAM, caldrà ajustar la configuració per no saturar el sistema.

### F. Grafana — visualització de dades

**Grafana** és probablement la millor eina de visualització de dades de codi obert. Ens permet crear **dashboards** amb gràfiques, taules, gauges, heatmaps, alertes, i un llarg etcètera, connectant-nos a múltiples fonts de dades: InfluxDB, Prometheus, MySQL, PostgreSQL, fins i tot APIs HTTP.

Al BernatLab, Grafana ens permetrà:

- Veure l'evolució de la temperatura del sòl al llarg del temps.
- Comparar la humitat de diferents zones de l'hort.
- Crear alertes visuals (un termòmetre que es posa vermell si la temperatura puja massa).
- Crear una **vista pública** que es pugui incrustar a la web Hort Osona.

Grafana té una corba d'aprenentatge inicial, però un cop entesa la lògica de panell-dashboard-data source, és molt potent.

### G. PostgreSQL — base de dades relacional

**PostgreSQL** és la base de dades relacional de codi obert més avançada del món. Molts serveis la fan servir per defecte: Nextcloud, Mastodon, Gitea, etc. Al BernatLab, la podem necessitar per a:

- L'API de Hort Osona, si volem guardar informació estructurada (espècies plantades, calendari de sembra, etc.).
- Altres serveis que la requereixin per defecte.
- Aprenentatge: és una base de dades excel·lent per aprendre SQL.

Es desplega fàcilment amb la imatge oficial `postgres:16`. Compte amb la configuració: cal establir una contrasenya forta per a l'usuari `postgres`, i considerar si volem exposar el port 5432 a la xarxa (probablement no, només comunicació interna).

### H. Integració LoRa SX1262 868 MHz

Aquesta és una de les parts més emocionants i complexes. **LoRa** (Long Range) és una tecnologia de comunicació per ràdio de llarg abast i baix consum. El mòdul **SX1262** treballa a la banda de 868 MHz (a Europa) i pot cobrir distàncies d'uns quants quilòmetres amb un consum molt baix.

Al BernatLab, l'objectiu és:

1. Connectar un mòdul SX1262 a la Raspberry (via SPI/GPIO).
2. Rep les transmissions dels sensors de l'hort (que tindran el seu propi mòdul SX1262).
3. Descodificar les dades i enviar-les per MQTT a InfluxDB.

Això implica:

- Hardware: mòdul SX1262, antena, cablejat.
- Software: una llibreria Python com `pyLoRa` o similar, o un servei com **ChirpStack** (un servidor LoRaWAN complet, però que pot ser excessiu per al nostre cas).
- Configuració: freqüència, amplada de banda, factor d'spreading, clau de xifratge.

Aquesta és la part més experimental del projecte. Hi dedicarem un capítol propi quan arribi el moment, perquè té molts detalls tècnics que no es poden tractar de passada.

### I. Telegram — notificacions i comandament

Telegram és el canal de comunicació que ja estem fent servir per a Uptime Kuma. Però les seves possibilitats van molt més enllà:

- **Bot personalitzat**: podem crear un bot a mida que ens permeti interactuar amb el BernatLab: veure l'estat dels serveis, consultar dades de sensors, executar ordres.
- **Alertes avançades**: no només "servei caigut", sinó alertes riques amb imatges, gràfiques, botons d'acció.
- **Comandament remot**: podem enviar ordres al servidor des de Telegram (per exemple, "apaga el contenidor X" o "reinicia el servidor").

Per crear un bot, parlem amb @BotFather, igual que vam fer per a Uptime Kuma. Per fer-lo servir des de Python, podem fer servir la llibreria `python-telegram-bot` o `httpx` per cridar directament l'API de Telegram.

### J. IA local — assistent Ollama

**Ollama** és una eina que ens permet executar **models de llenguatge grans (LLM) localment**, sense dependre de serveis al núvol. Al BernatLab, amb 4 GB de RAM, podem executar models petits com **Phi-3 mini**, **TinyLlama**, **Gemma 2B**, o **Llama 3.2 3B**. No seran tan potents com GPT-4, però funcionen, són privats, i són gratuïts.

Aplicacions:

- **Assistent personal**: podem integrar Ollama amb un client com **Open WebUI** (una interfície web similar a ChatGPT) per tenir el nostre propi ChatGPT privat.
- **RAG sobre documentació**: podem indexar les 76 fitxes d'Hort Osona (i tota la documentació del BernatLab) i fer que l'assistent pugui respondre preguntes sobre el contingut.
- **Resum automàtic**: podem fer que l'assistent ens resumeixi articles, correus, logs.
- **Generació de codi**: ajudar-nos a escriure scripts, configuracions, consultes.

Això s'integrarà amb Node-RED (per fer crides a l'API d'Ollama) i potser amb un client propi desenvolupat per nosaltres.

### K. Desenvolupament web — VSCodium, Git, deploy

Per a la part de desenvolupament web, volem un entorn complet a la Raspberry:

- **VSCodium** (o Codi OSS) — un editor de codi accessible des del navegador, similar a VS Code. Es pot instal·lar amb **code-server**.
- Un **entorn de test** per a les webs que desenvolupem.
- Un **pipeline de deploy**: fer canvis, validar, publicar.

Això ja és un altre àmbit, però el BernatLab n'és la base.

## 10.4 Cronograma realista

No totes les fites es faran alhora. Una estimació realista, assumint que hi dediquem algunes hores cada setmana:

| Fase | Què | Termini |
|---|---|---|
| 1 | Documentar el que tenim, Git, backup | Fet al Mòdul 1 |
| 2 | File Browser | 1-2 setmanes |
| 3 | Mosquitto MQTT, recepció bàsica | 2-3 setmanes |
| 4 | InfluxDB, Telegraf, primers dashboards | 3-4 setmanes |
| 5 | Node-RED, automatitzacions | 4-5 setmanes |
| 6 | Grafana, visualització | 5-6 setmanes |
| 7 | API pública, integració web | 6-8 setmanes |
| 8 | LoRa SX1262 (experimental) | 8-12 setmanes |
| 9 | PostgreSQL, base per a altres serveis | 3-4 mesos |
| 10 | Telegram bot avançat | 3-4 mesos |
| 11 | Ollama, Open WebUI, RAG | 4-6 mesos |
| 12 | code-server, entorn desenvolupament | 5-6 mesos |

Això és aproximat. Algunes coses es faran abans, d'altres es retardaran. I apareixeran coses noves que no havíem previst. És la naturalesa d'un projecte viu.

## 10.5 Riscos i limitacions

Hem de ser honestos amb els límits del BernatLab:

### Limitacions de maquinari

- **4 GB de RAM**: insuficients per a molts serveis simultanis. Si despleguem Grafana, InfluxDB, Node-RED, Ollama i mitja dotzena més, el sistema anirà just.
- **MicroSD**: com ja hem comentat, és un punt feble. A mitjà termini, caldrà migrar a SSD.
- **CPU ARM**: no tots els serveis tenen imatges arm64 natives. Cal verificar-ho.

### Limitacions d'ample de banda

La pujada des de casa sol ser lenta (10-50 Mbps típicament). Si tenim molts dispositius accedint al BernatLab, podem saturar-la. La solució és Tailscale: el tràfic es comprimeix i xifra, però la velocitat de pujada segueix sent el coll d'ampolla.

### Limitacions de temps

Un homelab és una afició, i com a tal competeix amb la feina, la família, la salut, el temps lliure. No podem posar-nos terminis inabastables. Cada pas endavant ha de ser sostenible.

### Riscos de seguretat

A mesura que afegim serveis, ampliem la superfície d'atac. Cal:

- Mantenir tot actualitzat.
- Usar contrasenyes fortes.
- Configurar autenticació de doble factor on sigui possible.
- No exposar serveis a Internet directament.
- Fer còpies de seguretat regularment.

## 10.6 Què NO farem

Igual d'important que la llista de coses que farem és la llista de coses que no farem (almenys no immediatament):

- **Kubernetes**: excessiu per a un homelab petit. Docker Compose és suficient.
- **Alta disponibilitat**: no tenim dues Raspberry, no podem fer balanceig de càrrega. Acceptem que el servidor pot caure (i ens assegurem que sabem com recuperar-lo).
- **Streaming de vídeo o jocs**: la Raspberry no dona per a tant.
- **Allotjament massiu de webs**: tenim una sola màquina, no podem oferir serveis comercials.
- **Criptomineria**: ni se'ns acudeixi.

## 10.7 El mòdul 2 d'aquest manual

Quan hàgim completat les fases 2-6, estarem en disposició d'escriure el **Mòdul 2** d'aquest manual, que tractarà en profunditat:

- MQTT, broker, publicadors, subscriptors, wildcards.
- InfluxDB, llenguatge Flux, retenció, agregacions.
- Grafana, panells, dashboards, alertes.
- Node-RED, fluxos, nodes personalitzats, depuració.

Aquest Mòdul 2 s'escriurà quan tinguem experiència real amb tot plegat, no pas ara amb teoria.

## 10.8 El Mòdul 3: IoT i LoRa

Quan arribi el moment de desplegar LoRa, escriurem un Mòdul 3 dedicat a:

- Conceptes de ràdio: freqüència, amplada de banda, modulació.
- El xip SX1262: especificacions, comandes AT (si escau), biblioteques Python.
- Xarxes LoRaWAN vs. xarxes LoRa punt a punt.
- Integració amb el broker MQTT.
- Seguretat en LoRa: claus, xifratge, anti-replay.

## 10.9 El Mòdul 4: IA local

Quan Ollama estigui en marxa, escriurem el Mòdul 4 sobre:

- Què són els LLM i com funcionen a grans trets.
- Instal·lació i configuració d'Ollama a la Raspberry.
- Open WebUI com a interfície.
- RAG: dividir documents, indexar-los, recuperar-los.
- Casos pràctics: assistent per al BernatLab, resum de documentació, generació de codi.

## 10.10 Com prioritzem

Quan tot està per fer, és difícil saber per on començar. La regla és:

1. **Necessitem-ho per a un projecte real?** Si sí, va primer.
2. **Serveix de base per a altres coses?** Si sí, va primer.
3. **És divertit i fàcil?** Si sí, ens motiva per seguir.

La integració de sensors al Hort Osona compleix les tres: és per a un projecte real, serveix de base per a moltes coses (visualització, alertes, API), i és motivador.

## 10.11 Resum

El BernatLab és un projecte en construcció permanent. En aquest mòdul hem vist:

- On som avui.
- Cap a on volem anar.
- Quin ordre té sentit.
- Quins riscos i limitacions tenim.

Les pròximes passes són clares: File Browser, MQTT, InfluxDB, Node-RED, Grafana, API pública, LoRa, IA local, desenvolupament web. Cadascuna, quan arribi el moment, serà objecte d'un nou mòdul del manual.

## 10.12 Exercicis pràctics

1. Mira la pàgina `CHANGELOG.md` del BernatLab. Quin és l'últim canvi registrat?
2. Mira la carpeta `/home/bernat/homelab/`. Quins subdirectoris hi ha? Què hi falta segons la full de ruta?
3. Pensa en una millora que voldries afegir al BernatLab. Quin cost té? Quin benefici? Documenta-la al CHANGELOG amb l'etiqueta `[pendent]`.
4. Mira la llista de tasques pendents i tria'n una per fer aquesta setmana. Fes-la, documenta-la al CHANGELOG.
5. Comparteix el manual amb algú que conegui menys el tema i pregunta-li què no entén. Probablement trobaràs un capítol per millorar.

Comandes útils:
```bash
# Veure l'estructura
ls /home/bernat/homelab/
tree /home/bernat/homelab/ -L 2  # si tree està instal·lat

# Veure l'últim canvi al CHANGELOG
head -20 /home/bernat/homelab/CHANGELOG.md

# Comprovar espai
df -h
docker system df
```

Paraules clau: **full de ruta, MQTT, InfluxDB, Grafana, Node-RED, PostgreSQL, LoRa SX1262, Ollama, File Browser, Telegram, API, priorització, cronograma, limitacions, sostenibilitat, mòdul 2, mòdul 3, mòdul 4**.

---

# Final del Mòdul 1

Amb aquest capítol es tanca el primer mòdul del BernatLab. Hem après què és un homelab, com funciona la Raspberry Pi, com administrar Linux, com configurar xarxa i SSH, com desplegar serveis amb Docker, com gestionar-los amb Portainer, com monitorar-los amb Uptime Kuma, com presentar-los amb Homepage, com versionar-ho tot amb Git, i quin és el camí que tenim per davant.

El proper pas pràctic és posar en marxa el que s'ha descrit: instal·lar File Browser, configurar Mosquitto, muntar InfluxDB, desplegar Grafana, i començar a rebre les primeres dades dels sensors. I quan tot això funcioni, escriurem el Mòdul 2.

Fins aviat, BernatLab.
