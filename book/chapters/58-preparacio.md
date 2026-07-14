# Capítol 58 — Preparació: què necessites tenir abans de començar

> *"El 80% dels problemes d'una instal·lació es decideixen abans de tocar cap botó. Si prepares bé la llista de la compra i el pla, el dia D flueix."*

## 58.1 A qui va dirigit aquest mòdul

Aquest mòdul és diferent dels anteriors. Allà on el **M1** explicava conceptes i el **M5** assegurava el sistema, **aquest mòdul t'acompanya pas a pas** a muntar el teu propi BernatLab des de zero.

Si ja tens la Raspberry en marxa, pots saltar-te les parts que ja has fet. Però si vols oferir el BernatLab a un amic o familiar — o si vols refer-lo tot de nou per entendre'l bé — segueix l'ordre dels capítols.

Al final d'aquest mòdul tindràs:

- Una Raspberry Pi 4 preparada i segura.
- Un servidor de monitoratge (Uptime Kuma, Prometheus, Grafana).
- Una cadena de dades funcional (MQTT → InfluxDB → Grafana).
- Un node LoRa enviant dades reals des del camp.
- Un bot de Telegram que t'avisa quan passa alguna cosa.
- Un runbook per si alguna cosa es trenca.
- Un DRP que has provat, no només escrit.

## 58.2 Què necessites: la llista de la compra

Això és el que jo tenia el dia que vaig començar. No és la llista mínima universal, és la llista que **a mi m'ha funcionat** i que et recomano.

### Hardware essencial

| Component | Quantitat | Preu aprox. | Per què |
|---|---|---|---|
| Raspberry Pi 4 Model B (4 GB RAM) | 1 | 55 € | El cor del BernatLab. 4 GB és el mínim; 8 GB és més còmode. |
| MicroSD A2 de 64 GB | 1 | 15 € | Disc del sistema. **A2** vol dir bona velocitat d'escriptura aleatòria, crítica per al sistema operatiu. |
| SSD USB 3.0 de 500 GB | 1 | 50 € | On van les dades. La microSD falla; la SSD no. |
| Carcassa amb dissipador i ventilador | 1 | 15 € | La RPi 4 s'escalfa; sense refrigeració el rendiment baixa. |
| Font d'alimentació USB-C oficial (5V/3A) | 1 | 12 € | **L'oficial**. Les fonts barates donen problemes subtils. |
| Cable Ethernet Cat 6 (2 m) | 1 | 5 € | Millor que Wi-Fi: més estable, més ràpid, més segur. |

### Hardware recomanable

| Component | Quantitat | Preu aprox. | Per què |
|---|---|---|---|
| SSD NVMe amb adaptador USB 3.0 | 1 | 80 € | Més ràpid que SSD SATA. Si vols anar sobrat. |
| Cables Dupont i protoboard | 1 lot | 10 € | Per connectar sensors al GPIO. |
| Sensor BME280 (I2C) | 1 | 5 € | Temperatura, humitat, pressió. Per a un node interior. |
| Sensor d'humitat del sòl capacitiu | 1 | 3 € | Per a un node exterior. |
| Mòdul SX1262 868 MHz + antena | 1 | 15 € | Per al node LoRa. |

### Eines i accessoris

- Un **ordinador** amb el qual configurar la RPi (Windows, Mac o Linux). El teu dia a dia.
- Un **lector de microSD** USB, per flashejar la imatge.
- Un **monitor amb HDMI** + **teclat USB**, per si mai necessites accés físic. No cal comprar-ne un de nou: qualsevol monitor vell serveix.
- Un **cable USB-C** llarg (1-2 m) per si la RPi queda lluny del router.
- **Etiquetes adhesives** per marcar cables, ports, contenidors.
- Una **caixa o calaix** per emmagatzemar la còpia de seguretat del sistema.

### Software

- **Raspberry Pi Imager** (gratuït): https://www.raspberrypi.com/software/
- **PuTTY** (Windows) o **Terminal** (Mac/Linux): per accedir per SSH.
- **Restic**: `sudo apt install restic` un cop tinguis la RPi en marxa.

### Comptes que necessitaràs crear

- **Tailscale** (gratuït per a ús personal): https://tailscale.com
- **GitHub** (gratuït): per al teu repo i per descarregar eines.
- **The Things Network** (gratuït): per als nodes LoRaWAN, si esculls aquesta via.
- **Backblaze B2** (gratuït fins a 10 GB): per a les còpies al núvol.
- **Telegram** (gratuït): per al bot d'alertes.

## 58.3 Quin cost total esperar

Si compres tot de zero, el cost aproximat és:

- Hardware essencial: 152 €
- Hardware recomanable: 30 €
- Software i eines: 0 € (tot gratuït o ja el tens)
- Comptes al núvol: 0-3 €/mes (restic, B2, etc.)

**Total: ~180 € d'entrada, 3 €/mes de manteniment.**

És un cost raonable per a un servidor 24/7 que t'allotjarà dades, automatitzacions, alertes, IA, i qualsevol cosa que hi vulguis connectar.

## 58.4 Quin temps invertir

Depèn de com ho facis:

| Modalitat | Temps | Comentari |
|---|---|---|
| Amb algú que t'ajuda | 6-8 hores | Si tens un amic que ja ho ha fet. |
| Sol, seguint el llibre | 12-15 hores | Al teu ritme, amb temps per assimilar. |
| Sol, sense pauses | 8-10 hores | Si tens pressa, en un cap de setmana. |

Jo recomano la **modalitat sol, seguint el llibre**, repartida en 3-4 sessions d'un cap de setmana. Tens temps per llegir, entendre i adaptar.

## 58.5 Quin coneixement necessites

Aquest llibre no assumeix que siguis expert, però tampoc comença des de zero. Hauries de saber:

- **Fer servir la línia de comandes bàsica**: `cd`, `ls`, `cp`, `mv`. Si no, llegeix el **Cap 3** (Linux per administrar un servidor) abans.
- **Llegir documentació tècnica**: la majoria d'eines tenen documentació anglesa. Et pots apanyar amb el català, però l'anglès t'ajudarà.
- **Editar fitxers de text**: nano o vim. El **Cap 3** t'ensenya nano.
- **Tenir paciència**: les coses fallen. De vegades, l'única solució és tornar-ho a provar.

Si tot això et sona però no ho has fet mai, **perfecte**. Aprendràs fent.

## 58.6 Quin espai físic

La Raspberry és petita, però pensa on la posaràs:

### Criteris

- **Ventilació**: no la tanquis en un armari hermètic. Li cal aire.
- **Protecció**: pols, esquitxos, animals (gats, ratolins, formigues).
- **Xarxa a prop**: com més a prop del router, millor. Cable Ethernet millor que Wi-Fi.
- **Endoll**: a prop d'un endoll o regleta amb protecció contra sobretensions.
- **Protecció contra talls de llum**: si tens un **SAI** (Sistema d'Alimentació Ininterrompuda, com els que es venen per a PCs), millor. La RPi consumeix poc i un SAI petit la pot mantenir una estona.

### Possibles ubicacions

- A la sala d'estar, al costat del router, en una caixa ventilada.
- Al despatx, en una prestatgeria.
- A l'armari de les comunicacions (on tens el router, l'ONT de la fibra, etc.).
- A l'hort mateix, si tens electricitat i cobertura Wi-Fi allà (amb protecció IP65).

Jo la tinc a la sala d'estar, en una caixa de fusta amb ventilació. Fa 3 anys que hi és i no ha fallat mai.

## 58.7 Quines decisions prendre abans de començar

Algunes decisions que has de prendre **abans** de tocar res:

### 1. Nom del servidor

Li posarem `hortosona` al llarg d'aquest llibre, però tu pots triar el que vulguis. Consells:

- Tot minúscules, sense espais ni caràcters estranys.
- Curt (8-12 caràcters).
- Que soni bé quan hi parlis ("el servidor hortosona està caigut").

### 2. Subdomini (si en tens un)

Si tens un domini propi (per exemple, `bernat.cat`), pots fer servir subdominis:

- `hortosona.bernat.cat` per accedir al servidor.
- `grafana.bernat.cat` per al panell de Grafana.
- `mosquitto.bernat.cat` per al broker MQTT.

Si no tens domini, **no passa res**. Tailscale et dona noms automàticament (`hortosona.tailnet.ts.net`) que funcionen igual.

### 3. Quins serveis vull tenir

Al capítol 1 del llibre tens la llista de serveis possibles. Pensa quins necessites realment:

- **Hort Osona**: MQTT, InfluxDB, Grafana, Node-RED.
- **IA local**: Ollama al Mac, integració amb el BernatLab.
- **Còpies al núvol**: Backblaze B2, restic.
- **Monitoratge**: Uptime Kuma, Prometheus, Alertmanager.
- **Web pública**: Nginx Proxy Manager, Cloudflare Tunnel.
- **Altres**: File Browser, Nextcloud, Immich (fotos), etc.

No activis serveis que no necessitis. **Cada servei és feina de manteniment**.

### 4. Quin hardware extra

Si vols connectar sensors reals, decideix ara quins:

- Sensor interior (BME280): 5 €.
- Sensor exterior (humitat del sòl): 3 €.
- Estació meteorològica completa: 200-500 €.
- Node LoRa: 30-50 € (mòdul + ESP32 + caixa + antena).
- Càmera: 30-50 €.

Comença amb el mínim. Pots afegir més endavant.

## 58.8 Quin pla de treball

Aquest mòdul està pensat per anar pas a pas. La seqüència recomanada és:

1. **Cap 58** (aquest): Preparació. Estàs aquí.
2. **Cap 59**: Primer contacte amb la Raspberry.
3. **Cap 60**: Sistema base segur.
4. **Cap 61**: Docker i Portainer.
5. **Cap 62**: Uptime Kuma.
6. **Cap 63**: Stack de dades: MQTT, InfluxDB, Grafana.
7. **Cap 64**: Node-RED: automatitzacions reals.
8. **Cap 65**: Node LoRa al camp.
9. **Cap 66**: Bot de Telegram.
10. **Cap 67**: Prometheus i alertes avançades.
11. **Cap 68**: Runbooks: quan falla alguna cosa.
12. **Cap 69**: DRP: el dia que es crema tot.

Cada capítol té una **durada estimada** al principi, i un **checklist** al final. Si la teva durada és molt més llarga, **atura't i pregunta**. Millor trigar més que no pas fer-ho malament.

## 58.9 Què tenir a mà durant la instal·lació

Quan et posis a treballar, tingues a mà:

- Aquest llibre (obert a la pantalla, o imprès si ho prefereixes).
- Un quadern o fitxer de notes per anotar:
  - Comandes que has executat.
  - Errors que has vist.
  - Decisions que has pres.
  - Contrasenyes (que després mouràs a un gestor).
- Un **termòmetre de ambient** (no és broma — la temperatura de la RPi afecta el rendiment).
- Un **tester de xarxa** o simplement poder fer `ping` des d'una altra màquina.

## 58.10 Com documentar la teva instal·lació

Al repo del BernatLab, ja tens un `homelab/` buit. Crea-hi:

```
homelab/
├── README.md              # Descripció general
├── setup-log.md           # El diari de la teva instal·lació
├── decisions.md           # Les decisions que has pres i per què
└── compose/               # Els teus fitxers docker-compose
```

El **setup-log.md** és especialment valuós. Anota cada pas amb:

- Data i hora.
- Comanda executada.
- Sortida esperada.
- Sortida real (especialment si falla).
- Solució aplicada.

D'aquí un any, quan oblidis com vas fer una cosa, obriràs aquest fitxer i recordaràs.

## 58.11 Errors habituals en la preparació

**Error 1: comprar la primera RPi que trobes**.

Assegura't que és **Raspberry Pi 4 Model B** (o Pi 5 si el pressupost ho permet). No confondre amb RPi 3 (més antiga) o RPi Zero (molt menys potent).

**Error 2: comprar una microSD qualsevol**.

Les **SanDisk Extreme** o **Samsung EVO** amb classe **A2** són les recomanades. Una microSD lenta farà que el sistema vagi lent.

**Error 3: estalviar en la font d'alimentació**.

La RPi 4 necessita 5V/3A. Una font de 5V/2A (la del mòbil) no és prou. Sortirà "low voltage warning" i el rendiment baixarà.

**Error 4: no tenir un pla B**.

Si compres la RPi, la microSD, però no el cable Ethernet, no podràs configurar res. Mira la llista sencera abans de comprar.

**Error 5: començar divendres a la nit**.

Si comences un projecte llarg un divendres a la nit, acabaràs amb un sistema mig muntat i frustració. Comença en un moment amb temps de sobres.

## 58.12 Com organitzar les còpies de seguretat

Des del primer moment, pensa en còpies:

- Una **microSD extra** amb la imatge flashejada (per si falla la principal).
- Un **disc USB** per fer la primera còpia un cop tinguis el sistema en marxa.
- Un compte de **Backblaze B2** creat ja, per tenir la còpia al núvol configurada des del primer dia.

La regla 3-2-1 (3 còpies, 2 suports, 1 fora de casa) és important **des del primer moment**, no pas quan ja tinguis dades valuoses.

## 58.13 El "moment de la veritat": quan ho engegues tot

El dia que connectis la RPi per primera vegada, tindràs una sensació d'**emoció barrejada amb por**. És normal. Si alguna cosa no va, recorda:

- El 80% dels problemes tenen solució buscant el missatge d'error exacte.
- El 20% restant es resol apagant i tornant a encendre (no és broma — funciona més del que voldríem).
- Si no trobes la solució, deixa-ho, dorm, i torna-hi l'endemà amb ulls frescos.

## 58.14 Resum

Aquest capítol és la "llista de la compra" del BernatLab. Hem vist:

- Quin hardware cal (essencial i recomanable).
- Quin cost esperar (~180 € d'entrada, 3 €/mes).
- Quin temps invertir (12-15 hores).
- Quin coneixement cal tenir.
- Quin espai físic.
- Quines decisions prendre.
- Quin pla seguir.

Si tens tot això clar, ja pots passar al **Cap 59**: Primer contacte amb la Raspberry.

## 58.15 Exercicis pràctics

1. Fes la teva pròpia llista de la compra i compara-la amb la meva.
2. Calcula el cost total del teu projecte.
3. Decideix el nom del servidor.
4. Decideix on el posaràs.
5. Crea el compte de Tailscale.
6. Crea el compte de Backblaze B2.
7. Crea el compte de GitHub (si no el tens).
8. Comença el quadern de notes.
