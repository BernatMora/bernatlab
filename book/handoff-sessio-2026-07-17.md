# BernatLab - Handoff Sessio 2026-07-17

> Document de pas per continuar aquesta sessio des del Mac de casa.
> Creat per Hermes el 2026-07-17 a la feina, en resposta a la conversa del mati.

## Que hem fet aquesta sessio

Aquesta sessio al Hermes ha estat **molt llarga** i hem cobert moltes coses.
Aquet document et serveix per continuar des del Mac de casa amb tot el context.

## Estat actual del projecte BernatLab

### Repos actius

- **BernatLab** (llibres, curs, scripts): https://github.com/BernatMora/bernatlab
- **Hort Osona** (PWA, plans mensuals): https://github.com/BernatMora/hort-osona

### Webs publiques

- BernatLab: https://bernatmora.github.io/bernatlab/
- Curs: https://bernatmora.github.io/bernatlab/book/curs/
- Hort Osona: https://bernatmora.github.io/hort-osona/
- Glossari: https://bernatmora.github.io/bernatlab/book/glossari.html
- Guia primer dia RPi: https://bernatmora.github.io/bernatlab/book/primer-dia-rpi.html
- Arquitectura: https://bernatmora.github.io/bernatlab/book/arquitectura/

### Estadistiques del projecte

- **Curs del BernatLab**: 77 capitols, 308 .md, 77 .html, ~1.087 preguntes
- **Llibre del BernatLab**: 7 moduls, 70 capitols, 584 pagines
- **Hort Osona**: 8 plans mensuals (juny-desembre 2026)
- **Glossari**: 321 termes, ~70 KB
- **Guia primer dia RPi**: 12 KB
- **Arquitectura**: 3 SVGs (xarxa, IoT, curs)
- **Scripts a bin/**: 7 fitxers (PowerShell, bash, accés directe)

## Nova info: Router 4G a l'hort

### Hardware nou

- **Router 4G** amb **microSIM de 150 GB/mes**
- **1 ESP32** (per ara)
- **Distancia RPi-ESP32**: 15 metres
- A 15m, **WiFi es la millor opcio** (l'ESP32 ja el te integrat)
- **LoRa nomes caldria** si la distancia fos > 50m

### Decisio tecnica

- Connectar la **RPi al WiFi del router 4G** (no a la xarxa de casa)
- RPi a l'hort amb internet propi
- ESP32 a 15m connectada al mateix WiFi
- Tailscale continua funcionant (canviara la IP)

## Quan arribis a casa, fes aixo

### 1. Muntar el router 4G a l'hort

- Posar-lo a prop de la RPi
- Inserir la SIM
- Encendre'l
- Anotar el nom de WiFi i la contrasenya

### 2. Connectar la RPi al WiFi del router 4G

Des del teu Mac, per SSH (si la RPi encara esta connectada a casa per Ethernet):

```bash
ssh bernat@100.x.y.z
# O per IP local si tens Ethernet:
ssh bernat@192.168.1.100

# Un cop dins, veure quines xarxes WiFi veu
sudo iwlist wlan0 scan | grep ESSID

# Connectar-se al router 4G
sudo nmcli device wifi connect "NOM-DEL-ROUTER" password "CONTRASENYA"
```

Si la RPi nomes te WiFi i cap altra connexio:
- Connecta-hi un monitor + teclat temporalment
- Configura el WiFi amb `sudo raspi-config`
- O connecta-la per Ethernet temporalment al router 4G

### 3. Verificar que tens internet

```bash
# A la RPi
ping 8.8.8.8
ping google.com
curl https://api.telegram.org
```

### 4. Verificar Tailscale

```bash
# Comprovar IP de Tailscale
tailscale ip -4

# Hauries de veure una IP diferent (si canvies de xarxa)
```

Si la IP ha canviat, actualitza els bookmarks del navegador.

### 5. Instal·lar MQTT, InfluxDB, Grafana

Veure: `book/curs/M2/`, `book/curs/M3/`, `book/curs/M6/`

## Fitxers i documents importants

### Tots publicats al GitHub

| Recurs | URL |
|---|---|
| Curs del BernatLab | https://bernatmora.github.io/bernatlab/book/curs/ |
| Guia primer dia RPi | https://bernatmora.github.io/bernatlab/book/primer-dia-rpi.html |
| Glossari | https://bernatmora.github.io/bernatlab/book/glossari.html |
| Arquitectura SVGs | https://bernatmora.github.io/bernatlab/book/arquitectura/ |
| Pla Hort 4G + ESP32 | https://github.com/BernatMora/bernatlab/blob/main/book/curs/recursos/pla-hort-4g-esp32.md |

### Documents locals al Mac de casa

Si tens els repos clonats al Mac:

- `~/bernatlab/`
- `~/bernatlab/projects/hort-osona/`

Si NO els tens, clona'ls:

```bash
cd ~/Documents
git clone https://github.com/BernatMora/bernatlab.git
git clone https://github.com/BernatMora/hort-osona.git bernatlab/projects/hort-osona
```

## El que has de fer a l'hort (checklist)

- [ ] Muntar router 4G a prop de la RPi
- [ ] Connectar RPi al WiFi del router 4G
- [ ] Verificar internet des de la RPi
- [ ] Verificar Tailscale (la IP pot canviar)
- [ ] Instal·lar MQTT (Mosquitto) a la RPi
- [ ] Instal·lar InfluxDB a la RPi
- [ ] Instal·lar Grafana a la RPi
- [ ] Programar ESP32 amb sensor temperatura/humitat
- [ ] Connectar ESP32 al WiFi del router 4G
- [ ] Verificar que l'ESP32 envia dades a MQTT
- [ ] Crear dashboard a Grafana
- [ ] Configurar alerta per gelada (Telegram)
- [ ] Documentar tot a un runbook

## Altres coses que voliem fer

A mes del projecte hort, tambe voliem:

1. **Pujar els canvis del cap de setmana** (encara no sabem quins son)
2. **Continuar fent el curs** (M1 cap 11-77 per fer)
3. **Acabar el M5-M8** (falten alguns detalls)
4. **Millorar les publicacions externes** (Infojardin, Ruralcat, etc.)
5. **Fer el pla de gener 2027** (quan arribi el moment)

## Per continuar la sessio al Hermes del Mac

Quan estiguis a casa i vulguis continuar:

1. **Obre Hermes** al Mac
2. **Copia el contingut d'aquest document** com a context
3. **Explica quines coses has fet** (pujat canvis, muntat router, etc.)
4. **Continuem** des d'on estavem

## Documents creats en aquesta sessio

A la feina, hem creat/modificat aquests fitxers (estan al repo BernatLab):

1. `book/arquitectura/xarxa-i-sistema.svg`
2. `book/arquitectura/hort-iot.svg`
3. `book/arquitectura/curs-documentacio.svg`
4. `book/arquitectura/index.html`
5. `book/glossari.md` (321 termes)
6. `book/glossari.html`
7. `book/primer-dia-rpi.md` (guia pas a pas)
8. `book/primer-dia-rpi.html`
9. `book/curs/cheatsheet-curs.md` (xuleta de comandes)
10. `book/curs/BernatLab_resum_1pag.pdf` (resum imprimible)
11. `book/curs/recursos/pla-hort-4g-esp32.md` (pla d'accio)

Tots pujats al commit `16cd2c6` de BernatLab.

## I a Hort Osona

- Plans mensuals: juny, juliol, agost, setembre, octubre, novembre, desembre 2026
- Tots publicats

## Recomanacio final

Quan arribis a casa, segueix aquesta ordre:

1. **Muntar router 4G** a l'hort
2. **Connectar RPi al WiFi del router**
3. **Verificar internet + Tailscale**
4. **Fer el checklist** anterior
5. **Documentar tot** en un runbook

Despres, ja podem parlar de:
- Muntar el primer sensor
- Crear els dashboards
- Configurar alertes
- I tot el que vingui!

---

> *Handoff creat per Hermes el 2026-07-17. Si tens qualsevol dubte, obre Hermes al Mac i pregunta.*
