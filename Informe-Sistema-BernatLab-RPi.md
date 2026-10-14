# INFORME TECNIC DEL SISTEMA

## BernatLab + Raspberry Pi `hortosona`

> **Per a:** desenvolupador/a que ha de conèixer, mantenir o continuar aquest sistema.
> **Data de l'informe:** 21 de setembre de 2026.
> **Branca de l'informe:** aquest document descriu l'ESTAT REAL VERIFICAT, no l'estat documentat.
> Tots els números, ports, contenidors i fitxers que hi surten s'han obtingut executant comandes
> sobre la màquina en el moment d'escriure'l (SSH, `docker ps`, `pm2 list`, `ss -lntp`, `crontab -l`,
> `curl` a cada port). Quan una dada prové de documentació i no de la màquina, s'indica.

---

## 1. Resum executiu

**BernatLab** és un homelab personal complet muntat sobre **una sola Raspberry Pi 4** que fa de:

- **Servidor de serveis autoallotjats** (nívol de fitxers, gestor de contrasenyes, gestor documental).
- **Plataforma de projectes web propis** (una vintena d'aplicacions petites: entrenaments, música, viatges, hort).
- **Gateway IoT** (MQTT, InfluxDB, Grafana) per a sensors.
- **Base de documentació i material didàctic** (un llibre tècnic de 8 mòduls, un curs pràctic de 78 capítols amb 1.102 preguntes, i un curs de fabricació electrònica).
- **Sistema d'automatitzacions** (23 tasques de cron que envien digests diaris i setmanals al mòbil via ntfy).

**Números clau verificats (21-09-2026):**

| Mètrica | Valor |
|---|---|
| Màquines al tailnet | 8 nodes registrats |
| Contenidors Docker en marxa | **22** |
| Processos pm2 | **9** |
| Serveis systemd propis | 5 (1 actiu, 4 preparats i aturats) |
| Ports TCP en escolta | 36 (distints) |
| Tasques de cron | **23** |
| Feines programades (digests ntfy) | 12 |
| Disc intern (microSD) | 59 GB, 30 GB usats (**54%**) |
| Disc extern USB (`/mnt/nuvol`) | 458 GB, 30 GB usats (**7%**) |
| Memòria | 3,7 GB total, 2,1 GB en ús, 888 MB de swap en ús |
| Uptime | 11 dies |
| Repositoris Git propis | 4 (bernatlab, hort-osona, cyberlab-ai, + 2 privats) |
| Fitxers versionats a `bernatlab` | 2.264 (794 `.md`, 500 `.py`, 154 `.html`, 71 `.svg`) |
| Llibre: capítols | 70 (mòduls M1 a M8) + 9 mòduls del curs |
| Curs: capítols / preguntes | **78 capítols / 1.102 preguntes** |

**Idea que cal entendre abans de tocar res:** aquest sistema té **quatre mecanismes diferents** de
posar coses en marxa (Docker, pm2, systemd, cron) i **no hi ha cap orquestrador únic**. Qui hi
treballi ha de saber quin mecanisme governa cada peça. La secció 4 ho explica; és el punt on més
es pot trencar alguna cosa per error.

---

## 2. Maquinari i sistema operatiu

| Concepte | Valor verificat |
|---|---|
| Model | **Raspberry Pi 4 Model B Rev 1.5** |
| CPU | 4 nuclis (ARM64, `aarch64`) |
| RAM | **3,7 GB útils** (placa de 4 GB) |
| Sistema operatiu | **Debian GNU/Linux 13 (trixie)**, edició Lite, sense escriptori |
| Nucli | `6.18.39+rpt-rpi-v8` |
| Disc intern | microSD 59,5 GB (`/dev/mmcblk0`), arrel ext4 amb `noatime` |
| Disc extern | **TOSHIBA MQ01ABD050V 465,8 GB** per USB-SATA (JMicron JMS578), muntat a **`/mnt/nuvol`** |
| Disc secundari | NTFS `/mnt/toshiba` definit a `fstab` però **no muntat** en aquest moment |
| Swap | zram 2 GB (en ús: 888 MB) |
| Hostname | `hortosona` |
| Usuari principal | `bernat` (uid 1000, als grups `sudo`, `docker`, `spi`, `i2c`, `gpio`, `bluetooth`, `dialout`, `ollama`) |
| IP de xarxa local | `192.168.1.103` (per Ethernet `eth0`; WiFi `wlan0` està DOWN) |
| IP Tailscale | `100.115.134.76` |
| Nom Tailscale públic | `hortosona.tail37c051.ts.net` |

**ATENCIO - discrepància detectada:** el document `bernatlab/INVENTARI-INFRASTRUCTURA.md` diu
"RPi 4B **8 GB**" i "IP LAN 192.168.1.**100**". Totes dues dades són **falses** segons la màquina
real: la placa és de 4 GB i la IP és la .103 (DHCP). Si un programador es refia del document,
perdrà temps. Cal corregir l'inventari.

**Recursos que van justos:** la RAM és el coll d'ampolla. Amb 22 contenidors i 9 processos pm2,
la màquina viu amb 2,1 GB de 3,7 GB i està començant a usar swap (888 MB). Qualsevol servei nou
que es proposi ha de ser lleuger; afegir una base de dades nova o un LLM local gran no hi cap.

---

## 3. Xarxa i accés

### 3.1 Tailscale (la clau de tot)

Tota la infraestructura s'hi accedeix per **Tailscale** (VPN mesh). No hi ha cap port obert al
router. El tailnet té 8 nodes:

| Node | Sistema | IP Tailscale | Estat 21-09-2026 |
|---|---|---|---|
| `hortosona` | Linux (RPi) | 100.115.134.76 | **actiu** (el servidor) |
| `bernat` | Windows (PC feina) | 100.82.142.113 | actiu |
| `macbook-air-de-bernat` | macOS (casa) | 100.86.178.51 | vist fa 3 min |
| `macbook-pro` | macOS (hort) | 100.67.26.116 | registrat |
| `bernat-1` | Windows (hort) | 100.108.101.11 | offline (fa 1 dia) |
| `iphone183` | iOS | 100.111.104.121 | registrat |
| `bernat-pc` | Linux | 100.121.249.107 | offline (fa 29 dies) - **nom obsolet** |
| `hort` | Linux (Kali) | 100.97.77.87 | offline (fa 37 dies) |

**`bernat-pc` ja no existeix com a màquina operativa**: el PC de Windows de l'hort es diu ara
`bernat-1`. Part de la documentació vella encara parla de `bernat-pc` i porta a confusió.
Igualment, `hort` és la màquina Kali del CyberLab, aturada fa més d'un mes.

### 3.2 Accés per SSH

- Es pot entrar amb `ssh bernat@hortosona` (per Tailscale) o `ssh bernat@192.168.1.103` (a casa).
- **Autenticació per contrasenya DESACTIVADA**: `/etc/ssh/sshd_config.d/99-hardening.conf` té
  `PasswordAuthentication no`. Només clau pública (`~/.ssh/id_ed25519`, 600).
- La RPi fa de **jump host**: té un `~/.ssh/config` amb àlies per a altres màquines
  (`mbp` cap al MacBook Pro). Patró: `ssh hortosona 'ssh mbp "<comanda>"'`.
- Per a GitHub hi ha **deploy keys separades per repo** (`~/.ssh/gh_deploy_bernatlab`,
  `gh_deploy_kettlebell`, `gh_deploy_entrenaments`) i àlies al `~/.ssh/config`
  (`github-bernatlab`, etc.). Cada clau només té permís d'escriptura al seu repo.

### 3.3 Tailscale Serve i Funnel (exposició a internet)

`tailscale serve` exposa serveis **només dins el tailnet** amb HTTPS; `tailscale funnel` els
exposa **a internet**. Estat verificat:

```
https://hortosona.tail37c051.ts.net  (Funnel ON)
|-- /        proxy http://127.0.0.1:3051   (Vaultwarden - privat, només tailnet)
|-- /menu    proxy http://127.0.0.1:3052   (formulari del casament - PUBLIC)
|-- /viatge  proxy http://127.0.0.1:3043   (pàgina del viatge - PUBLIC)
```

**Conseqüència de seguretat que cal tenir clara:** tot el que pengi de l'arrel del domini
(`/`) és Vaultwarden i és privat, però **`/menu` i `/viatge` són oberts a qualsevol persona
d'internet**. Són les dues úniques coses públiques del sistema (a part de les webs de GitHub
Pages).

### 3.4 Pitfall d'infraestructura: el Funnel i els redireccionaments

Un servidor que respongui `302 Location: /index.html` quan es demana `/` **es trenca** quan es
serveix per Funnel en un subcamí: el navegador resol el `Location` contra l'arrel del domini i
acaba a Vaultwarden. Els servidors de `viatge` i `jubilacio` ja estan corregits per servir
`index.html` directament sense redirecció. Si n'hi ha un de nou, cal fer-ho igual.

---

## 4. ARQUITECTURA: els quatre mecanismes d'execució

Aquest és el punt més important per a qui arriba nou. Al sistema hi conviuen **quatre** maneres
d'aixecar coses, i cada servei pertany a una i només una:

| Mecanisme | Què hi viu | Com es governa | Sobrevisc a reboot? |
|---|---|---|---|
| **Docker / Compose** | 22 contenidors (nívol, contrasenyes, documents, monitoratge, jocs web) | `docker compose` des de 16 directoris diferents | Sí (`restart: unless-stopped`) |
| **pm2** | 9 aplicacions web pròpies (Python i Node) | `pm2` com a usuari `bernat` | Sí (`pm2 save` + unitat systemd `pm2-bernat`) |
| **systemd** | 5 serveis propis | `systemctl` | Sí, si estan `enabled` |
| **cron** | 23 tasques (digests, backups, apagada/encesa) | `crontab -l` de l'usuari `bernat` | Sí (el dimoni cron) |

### 4.1 Docker

- Dues carpetes principals de composes: **`~/homelab/compose/<servei>/compose.yml`** (12 stack)
  i composes solts a `~/nextcloud/`, `~/monitoring/`, `~/docker/portainer/`, `~/entrenaments-app/`.
- Total: **16 fitxers de compose**.
- **Tres contenidors NO tenen compose**: `grafana`, `portainer` i `mosquitto` es van crear a mà
  amb `docker run`. Això és un parany important (vegeu 4.5).
- Hi ha **20 xarxes Docker** creades. Cada stack en crea la seva (`*_default`); `influxdb`,
  `telegraf` i `mosquitto` comparteixen `monitoring_default`; `grafana` està connectat a
  `bridge` **i** a `monitoring_default`.

### 4.2 pm2

- El dimoni pm2 s'aixeca amb la unitat systemd `pm2-bernat.service`, que executa
  `pm2 resurrect` llegint `~/.pm2/dump.pm2`.
- **Regla d'or del sistema: després de qualsevol canvi, `pm2 save`.** Si no, el canvi es perd
  al següent reinici. L'`dump.pm2` actual és del 17-09-2026.
- Comandes: `pm2 list`, `pm2 describe <nom>`, `pm2 restart <nom>`, `pm2 logs <nom>`, `pm2 delete <nom>`.

### 4.3 systemd

Cinc unitats pròpies a `/etc/systemd/system/`:

| Unitat | Estat | Què fa |
|---|---|---|
| `kettlebell.service` | **actiu i enabled** | App Flask de kettlebell (port 5000), amb el seu propi venv i dades a `/mnt/nuvol/kettlebell-data` |
| `ollama.service` | **actiu i enabled** | Servidor d'IA local, escolta a `127.0.0.1:11434` |
| `miflora.service` | aturat i disabled | Bridge BLE a MQTT del sensor de plantes (`/opt/hort/miflora_daemon.py`) |
| `hort-osona-chat.service` | aturat i disabled | API de xat amb RAG per a la PWA de l'hort |
| `hort-osona-telegram.service` | aturat i disabled | Bot de Telegram amb RAG i Ollama |
| `alexa-hort.service` | aturat i disabled | Backend de la skill d'Alexa |

Els quatre aturats ho estan **a propòsit**, per estalviar dades del router 4G. Estan preparats
per arrencar amb `sudo systemctl enable --now <unitat>`.

### 4.4 cron

`crontab -l` de l'usuari `bernat`, 23 línies actives. Es detallen a la secció 9.

### 4.5 Paranys d'arquitectura (apresos a cops, documentats al RUNBOOK)

1. **`docker run` fa perdre les xarxes personalitzades.** Grafana i Portainer es van crear a mà;
   en recrear Grafana amb `docker run` va quedar només a `bridge` i va deixar de resoldre
   `influxdb` (que viu a `monitoring_default`), trencant tots els panells. Arreglat amb
   `docker network connect monitoring_default grafana`. Si es recrea qualsevol d'aquests dos a mà,
   cal reconnectar la xarxa i comprovar-ho.
2. **No comparar etiquetes d'imatge, comparar digests.** L'etiqueta `latest` enganya (a
   `uptime-kuma`, `latest` apunta a la **v1**!). Per auditar versions:
   `docker buildx imagetools inspect <imatge> | grep -m1 Digest` contra
   `docker image inspect --format '{{index .RepoDigests 0}}' <imatge>`. I en una RPi cal mirar
   que la imatge tingui plataforma `arm64`.
3. **`docker compose up -d` recrea el contenidor si la imatge de l'etiqueta ha canviat**, encara
   que el compose no s'hagi tocat. Per això les versions estan **fixades** als composes.
4. **Nextcloud 35 NO es pot instal·lar**: no existeix build arm64. El sistema queda a la branca 34.
5. **El volum de dades del Nextcloud no es pot comptar des de fora**: `/mnt/nuvol/nextcloud/data`
   és de `www-data:www-data` amb mode 770, així que un `du`/`find` fet per l'usuari `bernat` dona
   0 fitxers (fals). Cal comptar des de dins del contenidor.
6. **Reiniciar un servei Python amb pm2 no recarrega les dades**: `cycle-library` serveix un JSON
   en memòria? No: el llegeix del disc, però la font de treball no és la del directori. Vegeu 6.2,
   és un cas particular que ha fet perdre hores.

---

## 5. Mapa complet de ports i serveis

Ports en escolta verificats amb `ss -lntp` i contrastats amb una petició HTTP real.

### 5.1 Contenidors Docker (22)

| Port | Contenidor | Imatge | Què és |
|---:|---|---|---|
| 3000 | `homepage` | ghcr.io/gethomepage/homepage:latest | **El dashboard central**: enllaços a tots els serveis |
| 3001 | `uptime-kuma` | louislam/uptime-kuma:2 | Monitor de disponibilitat (17 monitors) |
| 3002 | `grafana` | grafana/grafana:13.2.2 | Grafics de mètriques i meteorologia |
| 3010 | `harmonic-field` | nginx:alpine | App web de teoria harmònica musical |
| 3011 | `inner-ear-trainer` | nginx:alpine | Entrenador d'oïda musical |
| 3012 | `jocs-mentals` | nginx:alpine | Jocs cognitius (Stroop, N-Back) |
| 3013 | `rork-phaser-arcade` | nginx:alpine | Arcade musical d'intervals |
| 3014 | `rork-harmonia-negativa` | nginx:alpine | Visualitzador d'harmonia negativa |
| 3015 | `lick-variator` | nginx:alpine | Generador de variacions de licks |
| 3016 | `consonance-chains` | nginx:alpine | Analitzador d'acords per micròfon |
| 3035 | `entrenaments-app` | entrenaments-app-entrenaments | Analitzador de fitxers Garmin/Strava amb IA local |
| 3050 | `paperless` | paperless-ngx-cat:latest | Gestor documental amb OCR català |
| 3051 | `vaultwarden` | vaultwarden/server:latest | Gestor de contrasenyes (Bitwarden) |
| 5000 | `-` (systemd) | - | Kettlebell Trainer (Flask) |
| 8080 | `nextcloud-app-1` | nextcloud:34.0.4-apache | Nívol privat de fitxers |
| 8086 | `influxdb` | influxdb:2.7 | Base de dades de sèries temporals |
| 8090 | `ntfy` | binwiederhier/ntfy:latest | Servidor de notificacions push |
| 9000 | `portainer` | portainer/portainer-ce:latest | Gestor gràfic de Docker (HTTP) |
| 9443 | `portainer` | (mateix) | Portainer HTTPS |
| 1883 | `mosquitto` | eclipse-mosquitto:2.0 | Broker MQTT |
| 9001 | `mosquitto` | (mateix) | MQTT sobre WebSocket |
| (3306) | `nextcloud-db-1` | mariadb:11 | Base de dades del Nextcloud (només interna) |
| (5432) | `paperless-db` | postgres:16 | Base de dades del Paperless (interna) |
| (6379) | `paperless-redis` | redis:7 | Cua del Paperless (interna) |
| (host) | `telegraf` | telegraf:1.31 | Recol·lector de mètriques (`network_mode: host`) |

### 5.2 Processos pm2 (9)

| Port | Nom pm2 | Fitxer que executa | Llenguatge |
|---:|---|---|---|
| 8088 | `bernatlab-menu` | `/home/bernat/menu_server.py` | Python 3 |
| 8089 | `cyberquiz-sync` | `/home/bernat/scripts/syncserver.py` | Python 3 |
| 3030 | `jazz-fusion-guitar` | `npm start` a `~/jazz-fusion-guitar` | Next.js 15 |
| 3040 | `country-guitar` | `npm start` a `~/country-guitar` | Next.js 15 |
| 3041 | `cycle-library` | `/home/bernat/cycle-library-server.py` | Python 3 |
| 3042 | `jubilacio` | `~/jubilacio/jubilacio-server.py` | Python |
| 3043 | `viatge-andalusia` | `~/viatge-andalusia/viatge-server.py` | Python |
| 3044 | `kitesurf` | `~/kitesurf/kitesurf-server.py` | Python 3 |
| 3052 | `casament-menu` | `~/casament-menu/casament-server.py` | Python 3 amb **venv propi** |

### 5.3 Altres ports

| Port | Qui | Nota |
|---:|---|---|
| 22 | `sshd` | SSH, només clau pública |
| 139, 445 | `smbd` | Samba (compartició `TimeMachine` cap a `/mnt/nuvol/timemachine`, 400 GB de límit per al MacBook Air) |
| 11434 | `ollama` | **Només a `127.0.0.1`**: no és accessible des de fora de la màquina |
| 443 | `tailscaled` | Entrada del Serve/Funnel |
| 48493 | `tailscaled` | Port efímer del control de Tailscale |

Nota: el port **8088 és compartit** per tres coses: el menú principal (`MenuBernatLab.html`),
la pàgina `cyberquiz.html` i `jazzquiz.html` i `neurowave.html`. Tots són fitxers estàtics dins
`~/www-menu/`, servits pel mateix procés pm2.

---

## 6. Els projectes web propis, un per un

Tots segueixen el mateix patró, que és la convenció del sistema.

### 6.1 El patró estàndard d'una app web

1. Una carpeta al `~` de l'usuari: `/home/bernat/<projecte>/`.
2. Un `index.html` (sovint tot incrustat: CSS i JS dins del fitxer) i opcionalment `pdfs/` o vídeos.
3. Un servidor Python minimalista basat en `http.server` i `socketserver`, amb dues particularitats:
   `allow_reuse_address = True` (per no rebre "Address already in use" al reiniciar) i la
   redirecció de `/` cap a `index.html`.
4. Arrancat amb **pm2** i desat amb `pm2 save`.
5. Afegit al dashboard Homepage editant `~/homelab/compose/homepage/config/services.yaml` i
   reiniciant el contenidor `homepage`.
6. Una còpia del codi a `/mnt/nuvol/projects/<projecte>/` (el disc extern, perquè la microSD no
   acumuli escriptures).

**Esquelet del servidor, per copiar i canviar `PORT` i `DIRECTORY`:**

```python
import http.server, socketserver
PORT = 30XX
DIRECTORY = "/home/bernat/nom-projecte"
class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True
class H(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k): super().__init__(*a, directory=DIRECTORY, **k)
    def do_GET(self):
        if self.path in ("/", ""):
            self.send_response(302); self.send_header("Location", "/index.html"); self.end_headers(); return
        return super().do_GET()
with ReusableTCPServer(("0.0.0.0", PORT), H) as httpd: httpd.serve_forever()
```

### 6.2 Descripció de cada projecte

| Projecte | Port | Mida | Què és i què té de particular |
|---|---:|---:|---|
| **`bernatlab-menu`** | 8088 | 35 línies de servidor | El menú central (`MenuBernatLab.html`, 10 KB) que enllaça tots els recursos, més `cyberquiz.html` (292 KB, **39 missions**), `jazzquiz.html` (40 KB), `jazzlab.html` (26 KB) i `neurowave.html` (119 KB, **NeuroWave 3.0**: binaurals amb separació estèreo real, pacer de respiració, registre de sessions a `localStorage`). És un directori de fitxers estàtics: editar-hi un HTML **no** requereix reiniciar pm2. |
| **`cyberquiz-sync`** | 8089 | 299 línies | **Sidecar de sincronització** dels progressos de joc entre dispositius. API: `GET/POST /cybersync` (estat fusionat del CyberQuiz) i `GET/POST /jazzsync` (sessions de jazz). Fusiona per "màxim" (XP, ratxa, encerts). Dades a `~/cyberquiz-sync/estat.json` i `jazz_sessions.json`. Escriu un `sync.log`. |
| **`cycle-library`** | 3041 | 293 línies | **Biblioteca de 96 entrenaments de bici** (`library.json`). L'app (`index.html`, 65 KB) agrupa els entrenaments per 9 famílies, amb mini-perfils SVG reals, favorits/fets compartits entre mòbil i PC, editor amb "cues" de text, import de `.zwo` i exportació `.ictx`. **API pròpia**: `GET/POST /progress` (estat compartit), `POST /save`, `POST /delete`, `POST /sync` (proxy WebDAV cap al Nextcloud). El servidor **valida i recalcula** `duration` de cada entrenament. **ATENCIO**: el fitxer que executa pm2 és `/home/bernat/cycle-library-server.py` (a l'arrel del `~`), NO el de `~/cycle-library/`. Es van divergir; si s'edita el segon, no passa res. |
| **`jubilacio`** | 3042 | 226 línies | Únic lloc amb **autenticació pròpia**: contrasenya en fitxer, cookie signada amb HMAC (`jubilacio_sess`, 60 dies, `HttpOnly`), clau de signatura generada automàticament a `.secret` (600) i persistent entre reinicis, anti força bruta (6 intents fallits per IP, 600 s de bloqueig, 0,6 s de retard per intent), capçaleres `no-store` i `X-Robots-Tag: noindex`. Protegeix també els PDFs de `pdfs/`. Rutes: `/__login`, `/__logout`. |
| **`viatge-andalusia`** | 3043 | 44 línies | Pàgina de viatge **dissenyada per a mòbil** (botons de telèfon i mapes, sense taules amples). **Publicada a internet** via Funnel a `/viatge`. |
| **`kitesurf`** | 3044 | 29 línies | Preparació física específica de kitesurf. Conté **12 vídeos MP4** de demostració (28 MB en total). |
| **`casament-menu`** | 3052 | 335 + 345 línies | Formulari perquè els convidats triïn el menú del casament, **publicat a internet** via Funnel a `/menu`. SQLite a `respostes.db` (36 respostes enregistrades). Regles de negoci incrustades al servidor: diccionaris `MENU`, `GRUPS`, `NENS`, `SPECIAL` i `SPECIAL_BY_GROUP`; certes persones (celíaques/vegans) **no trien** i es pinten directament com a "resolt". Genera un PDF per al restaurant amb `menu_pdf.py` (ReportLab), amb l'ordenació interna "en cada grup, la dona va sempre primer". Panell d'admin a `/menu/admin`. **És l'únic servei pm2 amb venv propi** (per `reportlab`): si es reinstal·la amb el `python3` del sistema, el PDF peta amb un 500 clar. |
| **`jazz-fusion-guitar`** | 3030 | Next.js 15 | App React/Next real (amb `node_modules` i compilació): teoria, rutines, licks i flashcards de guitarra de jazz fusió. |
| **`country-guitar`** | 3040 | Next.js 15 | Igual però de guitarra country (modern, clàssic, bluegrass). |
| **`kettlebell-trainer`** | 5000 | 493 línies | App Flask de kettlebell amb reproductor de vídeo en bucle, configurador de treball/descans, drag & drop de vídeos i estadístiques. Va per **systemd**, no per pm2, amb el seu propi venv i dades al disc extern. |
| **`entrenaments-app`** | 3035 | Docker | Flask dins Docker. Puja fitxers `.tcx`, `.gpx` o `.fit`, els parseja i envia l'historial a un LLM local perquè faci d'entrenador personal (en català). Conecta amb Ollama del host via `host.docker.internal:11434` i el model és `llama3.1` (variable `LLM_MODEL`). Base de dades SQLite al volum `entrenaments-data`. |

**Altres carpetes amb codi que no són serveis actius:** `~/hort-sensor/` (scripts d'experimentació
amb el sensor BLE Mi Flora, amb 4 variants de `watch-flower*.py`), `~/archives/` (còpies antigues),
`~/credentials/` (fitxers de credencials, permisos 600, i `credencials.md` que és l'índex de on
viu cada contrasenya).

---

## 7. El repositori `bernatlab` (documentació i codi versionat)

`~/bernatlab` (i clon a `C:\Users\iadmin\bernatlab` al Windows). Remote:
`https://github.com/BernatMora/bernatlab`. Branca `main`. 55 commits. 125 MB, 2.264 fitxers.

```
bernatlab/
├── book/                El llibre i el curs
│   ├── chapters/        70 capítols .md (font del PDF/DOCX)
│   ├── curs/            El curs pràctic: M1 .. M9
│   ├── output/          PDF + DOCX generats per mòdul (M1..M8)
│   ├── glossari.md      69 KB, 321 termes
│   ├── cheatsheet.md    24 KB, xuleta de comandes
│   ├── arquitectura/    3 diagrames SVG (xarxa, IoT, curs)
│   ├── wiki/            Vistes HTML per mòdul
│   └── make_book.py     Generador del llibre (PDF/DOCX)
├── projects/
│   ├── hort-osona/      Submòdul Git del repo hort-osona
│   └── hort-osona-iot/  Sistema IoT complet (LoRa + Supabase + Alexa + Telegram + RAG)
├── maker-lab/           Bernat Maker Lab (electrònica): inventari, ADR, 10 fitxers d'idees, P0
├── bernatlab-cyberlab/  Còpia de treball del CyberLab (113 fitxers)
├── homelab/             scripts/publish.py + docs (estat LoRa)
├── bin/                 Scripts de comoditat (web, instal·lació, sync de Hermes)
├── posts/               Esborranys de publicacions externes
├── index.html           Pàgina del projecte
├── PROJECT_STATE.md     Estat del BernatLab
├── PROJECT_STATE-GLOBAL.md  Vista dels 3 projectes
├── INVENTARI-INFRASTRUCTURA.md  Inventari (amb errors, vegeu secció 2)
├── COMANDES.md          Comandes habituals
└── .github/workflows/   3 fluxos de CI
```

### 7.1 El curs (`book/curs/`)

Estructura per mòdul i capítol. Cada capítol és una carpeta amb **exactament quatre fitxers**:

- `resum.md` - la matèria.
- `quiz.md` - entre 10 i 15 preguntes (test amb 4 opcions i `- [x]` a la correcta, més obertes amb pistes).
- `exercici.md` - 7 a 9 passos amb comandes reals, validació amb caselles i un repte final.
- `respostes.md` - explicació de cada resposta i respostes model de 2-3 paràgrafs.

I, a l'arrel del mòdul, un `<NN>-<slug>.html` per capítol, amb quatre seccions fixes
(`#resum`, `#quiz`, `#exercici`, `#respostes`).

**Estat verificat dels 9 mòduls:**

| Mòdul | Nom | Capítols | Fitxers .md | HTML |
|---|---|---:|---:|---:|
| M1 | Fonaments | 10 | 40 | 10 |
| M2 | Contenidors | 10 | 40 | 10 |
| M3 | Dades | 10 | 40 | 10 |
| M4 | Intel·ligència | 10 | 40 | 10 |
| M5 | Seguretat | 10 | 40 | 10 |
| M6 | Operativa 24/7 | 10 | 40 | 10 |
| M7 | Hort Osona en acció | 10 | 40 | 10 |
| M8 | Eines del dia a dia | 7 | 28 | 7 |
| M9 | Bernat Maker Lab | 1 | 4 | 1 |
| **Total** | | **78** | **312** | **78** |

El `course-manifest.json` (generat) declara: 9 mòduls, 78 capítols, **1.102 preguntes**.

Eines del curs:
- `book/curs/build_course.py` - genera i valida el manifest. Té un diccionari `MODULE_NAMES` i una
  llista `FORBIDDEN_CONTENT` que **rebutja** l'adreça Tailscale personal, rutes de Windows i
  marcadors de contingut incomplet. Valida amb `python build_course.py --check`.
- `book/curs/quiz.py` - qüestionari interactiu de terminal, amb autoavaluació, repàs espaçat
  (`--review`) i estadístiques (`--stats`).

### 7.2 El llibre (`book/chapters/`)

70 capítols en Markdown (00-pròleg + 01 a 70). Es compilen a PDF i DOCX amb
`book/make_book.py`, que té les llistes `CHAPTERS_M1` a `CHAPTERS_M8` i un `main()` amb un bloc
per mòdul. **Cal executar-lo amb el python del venv del projecte** (`.venv/Scripts/python.exe`
al Windows), no amb el `python` del sistema, perquè necessita `reportlab` i `python-docx`.

Sortida actual a `book/output/`: `BernatLab_Manual_Modul_1.pdf` fins a `_Modul_8.pdf` (i DOCX),
entre 98 KB i 266 KB cadascun.

### 7.3 Integració contínua

Tres fluxos a `.github/workflows/` (només s'activen per pull request o manualment; el trigger de
`push` es va desactivar per evitar notificacions constants):

- `course-quality.yml` - `python book/curs/build_course.py --check`, `python book/curs/quiz.py --list`, `node --check book/curs/curs.js`.
- `repository-quality.yml` - **rebutja secrets** al repo (claus privades, tokens `ghp_`, `sk-`,
  `tskey-`) i **rebutja adreces Tailscale reals** als fitxers versionats.
- `link-check.yml` - comprovació d'enllaços interns.

### 7.4 Regles i convencions del projecte (no negociables)

Aquestes regles estan escrites a `PROJECT_STATE.md` i `PROJECT_STATE-GLOBAL.md` i han de
respectar-se en qualsevol contribució:

1. **Apostrofs i cometes ASCII**, mai tipogràfics. Tots els fitxers en **UTF-8 vàlid**.
2. **Cap credencial ni token al repositori ni al context.** Tot amb placeholders.
3. **Anonimitzar les IPs** (192.168.x.x, 100.x.x.x) abans de fer commit. El CI ho comprova.
4. **Idioma: català** per defecte.
5. **Validar amb execució real**, no amb promeses. No reportar "fet" sense proves.
6. **Fitxers petits i editables** (KISS). Un `docker-compose.yml` per tema.
7. **No hi ha secció "Paraules clau"** al final dels capítols.
8. **Mai practicar ciberseguretat des de l'equip de la feina** (risc laboral).
9. **Documentar-ho tot**: si es toca el sistema, cal actualitzar `~/RUNBOOK.md` **i** copiar-lo
   a `/mnt/nuvol/RUNBOOK.md` (actualment tenen el mateix md5).

---

## 8. `RUNBOOK.md`: el document mestre d'operacions

`/home/bernat/RUNBOOK.md`, **1.360 línies / 75 KB**, duplicat a `/mnt/nuvol/RUNBOOK.md`. És el
document on s'ha anat apuntant TOT el que s'ha après: cada parany, cada decisió, cada incident.
**Per a un programador nou, és la lectura més rendible després d'aquest informe.** Conté:

1. On és cada cosa i qui fa què.
2. Mapa de ports.
3. El patró per crear una pàgina web (secció 6.1 d'aquí).
4. Backup i disc extern (amb el càlcul d'estalvi de dades del mòbil).
5. Monitoratge telegraf/influx/grafana, amb els errors trobats i arreglats.
6. Notificacions ntfy i mapa de tòpics.
7. Viatge d'Andalusia (dades reals de reserves).
8. Regles d'or.
9. Jubilació (autenticació).
10. Nextcloud: com s'actualitza de debò i per què el botó web no serveix.
11. Actualització general de totes les imatges Docker del 17-09-2026.
12. Tailscale Serve i Funnel.
13. Casament: detalls del formulari i del PDF.
14. Cycle Library: convencions dels entrenaments, el format `.ictx`, spinning en relleus,
    les dades reals de l'usuari extretes d'intervals.icu.
15. Kitesurf i NeuroWave.

---

## 9. IoT: sensors, MQTT, dades i visualització

### 9.1 L'estat real (i la discrepància important)

Aquí hi ha **tres projectes IoT diferents** que conviuen i que és fàcil confondre. Cal tenir-los
clars:

| Projecte | On viu | Estat real verificat |
|---|---|---|
| **Pipeline MQTT/InfluxDB/Grafana** | `~/monitoring/docker-stack.yml`, `~/scripts/*.py` | **FUNCIONA**. És el que alimenta el Grafana de meteorologia i del vent. |
| **Hort Osona IoT (LoRa + Supabase)** | `~/hort-osona/hort-osona-iot/` i còpia a `~/bernatlab/projects/hort-osona-iot/` | **NO funciona**. Hardware comprat, software escrit, mai ha enviat ni rebut una dada. |
| **Sensor BLE Mi Flora** | `/opt/hort/miflora_daemon.py`, `~/hort-sensor/` | **Preparat, aturat**. Servei `miflora.service` disabled. El protocol Xiaomi modern amb xifrat no s'ha acabat de resoldre. |

### 9.2 El que sí que funciona: la cadena meteorològica

```
[API pública del vent]  -->  ~/scripts/vent_kite_influx.py  -->  InfluxDB (measurement vent_kite)
[API meteo]             -->  ~/scripts/meteo_influx.py      -->  InfluxDB (measurement meteo)
                                                                    |
                                                          Grafana (:3002)  <-- 3 dashboards
                                                                    |
                                                        ~/scripts/morning_digest.py --> ntfy
```

**InfluxDB 2.7**, organització `hortosona`, bucket `metrics` amb **retenció de 720 h (30 dies)**.
Measurements existents verificats: `cpu`, `disk`, `diskio`, `docker`,
`docker_container_blkio`, `docker_container_cpu`, `docker_container_mem`, `docker_container_net`,
`docker_container_st`, `file`, `mem`, `meteo`, `net`, `system`, `vent_kite`.

**Telegraf 1.31** recull mètriques cada 15 s. Detall crític: va amb **`network_mode: host`**.

> **Per què:** `/proc/net/dev` és VIRTUAL per espai de xarxa: mostra les interfícies del procés
> que el llegeix, no les del fitxer muntat. Amb xarxa bridge, Telegraf llegia el seu propi `veth`
> (77 MB RX / 724 MB TX) en lloc de l'`eth0` real del RPi (1,6 GB / 3,0 GB). Amb `network_mode:
> host` el `/proc/net/dev` és el del host i les xifres són reals. **Conseqüència:** els noms de
> servei no resolen, i cal usar `localhost` per a InfluxDB i Mosquitto.
>
> **Pitfall de la versió:** a Telegraf 1.31 l'opció d'InfluxDB és `interfaces` (plural). Posar-la
> en singular fa que **el contenidor no arrenqui**; l'error només es veu a `docker logs`. Després
> de recrear Telegraf cal comprovar sempre els logs, no l'estat.

**Grafana 13.2.2** amb 3 dashboards actius i 2 fonts de dades:

| Dashboard | Identificador | Contingut |
|---|---|---|
| RPi Bernat - Sistema | `rpi-bernat-system` | CPU, memòria, disc, xarxa, temperatura |
| Meteo Osona - Hort | `afwtpbwm8uadcc` | Pluja, temperatura, ET0, probabilitat |
| El Vent - Sant Pere Pescador | `el-vent-sant-pere` | Previsió i historial del vent per a kitesurf |

Fonts de dades: `influxdb` (per defecte) i `InfluxDB-hortosona`, totes dues Flux, apuntant a
`http://influxdb:8086` (resol perquè Grafana està connectat a `monitoring_default`).

> **ATENCIO - els dashboards NO són fitxers JSON al disc.** Viuen a la taula `dashboard` de
> `/opt/grafana/data/grafana.db` (SQLite, propietat de l'usuari `grafana`, cal `sudo`). Es poden
> editar amb sqlite3 incrementant el camp `version`, i Grafana els recarrega **en calent sense
> reiniciar**. Hi ha còpies a `/opt/grafana/data/dashboard-bak-*.json`.
>
> **Credencials de Grafana:** admin / `hort2026` (a `/opt/grafana/config/grafana.ini`). Les
> credencials d'InfluxDB estan **en text pla al `docker-stack.yml`** (usuari admin, token
> `bernat-token-super-secret-2026`). Això és un deute de seguretat (vegeu secció 13).

### 9.3 Els errors de Grafana que ja s'han arreglat (i que no s'han de reintroduir)

1. **El desplaçament de dies.** `meteo_influx.py` desava cada dia a les `00:00 UTC`, que en hora
   local són les 02:00. Amb l'eix del Grafana en `Europe/Madrid`, la finestra
   `aggregateWindow(every: 1d)` anava de 02:00 a 02:00 i **la barra etiquetada "17" contenia la
   pluja del 16**. La dada era correcta; la barra cauia al dia següent.
   **Solució:** escriure a **00:00 LOCAL** (`TZ_LOCAL = UTC+2`) i **no agregar per dies**
   (un punt = un dia).
2. **La mitjana d'angles és incorrecta.** `mean` sobre direccions del vent dona una direcció
   plausible però falsa: la mitjana aritmètica de 350° i 10° és 180° (Sud) quan la resposta bona
   és 0° (Nord). Comprovat sobre dades reals: de 15 dies, **9 donaven una direcció equivocada**.
   **Solució:** `mode` sobre bins de 45° (que és el que ja feia el digest de ntfy, una sola font
   de veritat de criteri).
3. **`today()` a Flux depèn de la zona horària del servidor d'InfluxDB (UTC)** i de matinada
   deixa el panell buit. Cal fer servir rangs explícits.
4. **El comptador de xarxa es reinicia.** `/proc/net/dev` s'ha reiniciat 2 cops en 14 dies en
   aquesta RPi. Qualsevol càlcul amb `spread()` o `last-first` dona xifres falses; cal
   `difference(nonNegative: true) |> sum()`.
5. **Un error al digest del matí el matava sencer.** `morning_digest.py` cridava l'API del vent
   sense protegir; quan l'API va fallar, el traceback va matar l'script i es va perdre **tot** el
   digest (sistema, gel, rega i vent). **Solució:** el bloc del vent va dins `try/except` i, si
   falla, posa "(no disponible ara: ...)" i la resta del digest surt igual. A més,
   `vent_kite_influx.fetch()` fa 3 intents amb espera creixent (5 s, 10 s).

### 9.4 Hort Osona IoT (LoRa + Supabase): NO funciona

**Arquitectura dissenyada:** node de camp amb LoRa a l'hort, a uns 400 m del receptor; el receptor
és un HAT LoRa a la RPi; les dades van a Supabase (Postgres al núvol) i un LLM local genera
consells agronòmics cada 6 h.

**Software existent** (no cal re-escriure'l): `node-emissor/src/main.cpp` (cicle de deep sleep,
lectura de sensors, transmissió LoRa) i `platformio.ini`; `backend/lora_receiver.py` (rep LoRa,
escriu a Supabase, demana consell a Ollama); `backend/supabase_schema.sql` (2 taules: `mesures`
i `consells_ia`, més Realtime); `backend/main.py` (backend REST alternatiu via MQTT + SQLite);
`backend/api_chat.py` (endpoint `/api/chat` de la PWA combinat amb `rag.py`); `bridge/gateway.py`;
`web/hort-live.html` (vista amb gràfic de 24 h); `telegram_bot.py`; `alexa_backend.py` +
`alexa-skill/interaction-model.json`; `rag.py` (RAG sobre les 76 fitxes de l'hort amb Ollama);
`mycloud_storage.py`; i les guies de muntatge.

**Cost del maquinari: ~105 EUR.** `node-emissor/specs/bom.json` té la llista de materials.

**Per què no funciona (diagnòstic pendent, hipòtesis documentades):**
1. El **HAT SX1262 no respon** des de la RPi: el pin BUSY està sempre a 1. El `/dev/spidev0.0` i
   `/dev/spidev0.1` sí que existeixen i el SPI està activat a `/boot/firmware/config.txt`
   (`dtparam=spi=on`). Hipòtesis: jumper d'alimentació, pin CS diferent, manca de 5 V.
2. Hi ha una **segona via documentada** a `bernatlab/homelab/docs/LORA-ESTAT-ACTUAL.md`: un HAT
   Waveshare amb mòdul **E22-900T22S (EBYTE)** connectat per **UART** (no SPI), amb el selector
   del HAT en posició B i un node **Heltec WiFi LoRa 32 V3** (ESP32-S3 + SX1262 + OLED) al costat
   de camp. En aquesta via la Heltec ja s'havia programat amb èxit des del Mac (port sèrie,
   OLED, alimentació), però **falta el programa que envia dades per LoRa**.
   Els dos documents descriuen maquinari diferent (SPI vs UART, TTGO vs Heltec). **Cal unificar
   el criteri abans de continuar.**
3. No hi ha compte de Supabase creat ni l'esquema executat.
4. El servei `hort-osona-telegram.service` està **aturat a propòsit** per estalviar dades del 4G.

**Punt important d'organització:** hi ha **dues còpies del codi IoT** i **no són idèntiques**:
`~/hort-osona/hort-osona-iot/` (la de treball, amb `.env` real i logs) i
`~/bernatlab/projects/hort-osona-iot/` (la versionada, anonimitzada). Un `diff -rq` mostra
desenes de fitxers diferents. **Cal decidir quina és la font de veritat** i establir com es
sincronitzen, o el proper que hi treballi perdrà molt de temps.

### 9.5 Sensor BLE Mi Flora (aturat)

`/opt/hort/miflora_daemon.py` llegeix els anuncis BLE del sensor i publica JSON al topic MQTT
`hort/sensor/<mac>/data` amb humitat, temperatura, llum, fertilitat i bateria. Requereix
`bleak`, `paho-mqtt` i `python-dotenv` (al venv `/opt/hort/venv`). Servei `miflora.service`
(disabled).

**Estat real:** el sensor es connecta i el Bluetooth funciona (adaptador `BCM43455`, bluez 5.82,
MAC `88:A2:9E:91:FB:8D`), però **el canal de notificació no retorna dades**: la lectura directa
del UUID 0x04 retorna 10 bytes que semblen un testimoni de sessió. El firmware és una versió
moderna amb xifrat. **Pendent: implementar el handshake inicial del protocol Xiaomi.**

> **Nota important sobre l'input MQTT de Telegraf:** l'input `mqtt_consumer` està configurat però
> **no ha escrit mai cap mesura** (0 punts en 30 dies). No hi ha cap procés ni cron publicant al
> topic `hort/#`. `~/miflora-env` existeix però res no l'executa. **Aquest input és codi mort**:
> o s'activa el daemon, o es retira la configuració.

---

## 10. Backups (sistema v2, dissenyat per estalviar dades mòbils)

El sistema de còpies és probablement la part més ben pensada de tot el projecte, perquè va haver
de resoldre un problema real: la versió inicial pujava ~346 MB/dia a iCloud (10 GB/mes de dades
del mòbil 5G) copiant coses que es regeneren soles.

### 10.1 Arquitectura de tres nivells

| Nivell | Quan | Destinacions | Què hi va |
|---|---|---|---|
| **Diari** (`~/bin/backup-diari.sh`) | 02:00 | disc extern (complet) + iCloud (només l'essencial) | Dumps de BD (~3 MB), el `home` sense brossa (~416 MB), `/etc` (4 MB), configs de Grafana/Mosquitto, volums Docker petits, `/mnt/nuvol/projects` |
| **Setmanal** (`~/bin/backup-setmanal.sh`) | Dissabte 03:30 | disc extern + iCloud | Les dades grans i ÚNIQUES: `nextcloud/data` (674 MB), `paperless` (100 MB), `vaultwarden` (308 KB) |
| **Mensual** (`~/bin/backup-mensual.sh`) | Dia 1 a les 03:00 | `/mnt/nuvol/backups-sistema/` | Còpia de sistema completa |

**Resultat verificat:** el trànsit offsite diari va passar de ~346 MB a **menys de 10 MB**.
Al log de la matinada del 21-09-2026: `transit offsite REAL: 0.65MB pujats avui (49 fitxers
nous/canviats)`. iCloud va baixar de 5,2 GB a 1,2 GB.

**Ús real del disc extern verificat:** `backups-diari` 5,5 GB · `backups-sistema` 2,9 GB ·
`timemachine` 14 GB · `lick-variator-source` 561 MB · `backups-setmanal` 82 MB ·
`projects` 49 MB · `paperless` 34 MB · `kettlebell-data` 25 MB.

### 10.2 La regla crítica: mai copiar una base de dades oberta amb `rsync`

Copiar una BD SQLite oberta amb `rsync` **pot produir còpies corruptes**. Es va veure el
15-09-2026: una còpia crua de `kuma.db` donava `database disk image is malformed`. Les BD es
copien amb:

- **`~/bin/copia_sqlite.py`** - fa servir l'**API de backup de SQLite** i **verifica el resultat**
  carregant-lo en una BD en memòria. Cobreix: `kuma` (només configuració: monitors, notificacions,
  ajustos i usuaris; **l'historial de heartbeats NO**), `grafana`, `vaultwarden`, `casament`
  (les respostes dels convidats), `entrenaments` i `ntfy`.
- **`mariadb-dump --single-transaction --quick | zstd`** per al Nextcloud (~1 MB comprimit, contra
  780 MB de la còpia crua). El contenidor és `nextcloud-db-1` i la comanda va amb
  `MYSQL_PWD="$MYSQL_ROOT_PASSWORD" mariadb-dump -uroot`. **A mariadb:11 el binari es diu
  `mariadb-dump`, no `mysqldump`.**
- **`portainer.db` no és SQLite** (és BoltDB) i el contenidor està aturat a les 02:00, així que
  la còpia crua del volum ja és vàlida.
- **InfluxDB 2.x no té comanda de backup** (`influxd backup` és de la 1.x). Les seves dades
  (meteo) tenen retenció de 30 dies i es regeneren: no es copien fora del disc extern.

**Mai es copia** (es regenera): `node_modules`, `.next`, `.npm`, `.cache`, `__pycache__`,
`.pm2/logs`, `miflora-env`, `tsconfig.tsbuildinfo`, el volum anònim del codi del Nextcloud
(868 MB, ve de la imatge Docker) i `nextcloud_db` cru.

### 10.3 Altres regles i paranys dels backups

- **`--delete` no esborra els fitxers exclosos**: cal `--delete-excluded`, o el que ja no toca
  copiar es queda al destí per sempre.
- **No fer `pkill -f backup-diari.sh`**: mata la sessió SSH del Mac.
- **`/mnt/nuvol` ha d'estar muntat** o l'script avorta amb alerta ntfy; **mai** escriu a la
  microSD per error.
- El `rsync` cap a iCloud només usa opcions que entén el **rsync 2.6.9** del Mac (els Mac
  antic porten aquesta versió); per això `zstd` es fa al costat de la RPi.
- **Mètrica de trànsit corregida:** abans es loguejava un `du -sm` de tot l'arbre d'iCloud
  (mida acumulada, no trànsit). Ara cada `rsync` cap al Mac va amb `--stats` i es sumen els
  `Total bytes sent`. **Aquest és l'únic número que importa per a les dades del mòbil.**

### 10.4 Risc assumit conscientment

Fins a **7 dies de pèrdua** dels fitxers del Nextcloud i del Paperless si el disc extern cau
(perquè el setmanal és el que els agafa). Els PDF originals del Paperless són al Nextcloud, dins
el mateix setmanal. **Si es volgués tancar, el setmanal es podria passar a diari: són 770 MB/dia,
uns 23 GB/mes.**

### 10.5 Time Machine

El volum `TimeMachine` de Samba serveix `/mnt/nuvol/timemachine` amb un límit de 400 GB per al
MacBook Air (`MacBook Air de Bernat.sparsebundle`, 14 GB ara mateix). Configurat amb
`vfs objects = catia fruit streams_xattr` i `fruit:time machine = yes`.

---

## 11. Notificacions: ntfy i el mapa de tòpics

**ntfy** (:8090) és el canal de comunicació del sistema amb el mòbil de l'usuari. Configuració
real (`server.yml`): `auth-file` amb `auth-default-access: deny-all`, caché de 12 h i login
habilitat. El fitxer de credencials és `~/credentials/ntfy-bernat.txt` (permisos 600) i conté
l'usuari i la contrasenya del topic.

**Regla de disseny:** **cada tipus de digest va al SEU tòpic**, perquè no es barregin. L'usuari
s'ha de subscriure des del mòbil als tòpics que vulgui rebre. Reutilitzar un tòpic de digest per
a avisos de l'agent és un error que ja s'ha comès (el digest del CyberLab anava al tòpic `hort`).

| Tòpic | Què hi arriba | Horari | Script |
|---|---|---|---|
| `alerts` | Alertes del sistema, backups, disc ple | puntual + 07:00 i 19:00 | `disk_alert.py`, `kite_alert.py`, backups |
| `hort` | Digest del matí (sistema, gel, rega, vent 7 dies) + resum setmanal consolidat | 06:35 diari / diumenge 20:15 | `morning_digest.py`, `resum_setmanal_digest.py` |
| `ai` | Novetats d'IA i self-hosting, resumit amb Ollama | 06:30 | `ai_digest.py` |
| `noticies` | Titulars d'IA/tech i portada catalana | 07:05 | `noticies_digest.py` |
| `jazz` | Preguntes diàries de jazz (+ progrés setmanal) | 07:20 / diumenge 19:30 | `jazz_quiz.py`, `jazz_progress_digest.py` |
| `ciber` | Pinzellades del CyberQuiz (+ progrés setmanal) | 06:40 / dilluns 06:45 | `ciber_digest.py`, `cyber_progress_digest.py` |
| `angles` | Anglès tècnic: quiz (58 preguntes al banc) + lectura (24 fragments) | 06:45 / 06:50 | `angles_quiz.py`, `angles_reading.py` |
| `acer` | Anglès tècnic d'acer/estructures (65 preguntes + 10 lectures) | 06:55 / 07:00 | `acer_quiz.py`, `acer_reading.py` |
| `kite` | Fitxes de material de kitesurf | 06:55 | `kite_quiz.py` |
| `hermes` | **Canal de SORTIDA de l'agent Hermes del PC.** Només enviar; no s'hi escolta res. | puntual | Agent Hermes al Windows |

**Com s'envia una notificació des d'un script o manualment:**

```bash
curl -u "bernat:<contrasenya>" \
  -d '{"topic":"alerts","title":"Títol","message":"Cos","priority":3,"tags":["warning"]}' \
  http://localhost:8090
```

**Sobre el tòpic `hermes`:** és el canal pel qual l'agent Hermes que corre al PC de Windows
(vegeu secció 12) envia avisos i resultats de les seves tasques programades al mòbil. La
configuració és a `~/AppData/Local/hermes/.env` del PC (`NTFY_SERVER_URL`, `NTFY_TOPIC`,
`NTFY_PUBLISH_TOPIC`, `NTFY_HOME_CHANNEL=hermes`, `NTFY_TOKEN`, `NTFY_MARKDOWN=true`). El tag
`hermes-agent` acompanya cada missatge per evitar bucles d'eco. **Nomes de sortida.**

---

## 12. Automatitzacions: cron i l'agent Hermes

### 12.1 Cron de la RPi (23 tasques, usuari `bernat`)

| Horari | Comanda | Funció |
|---|---|---|
| `0 1 * * *` | `~/bin/nightly-stop.sh` | Atura Uptime-Kuma i Portainer de nit |
| `30 6 * * *` | `~/bin/morning-start.sh` | Els engega i reinicia Portainer (regenera el token de setup) |
| `0 3 1 * *` | `~/bin/backup-mensual.sh` | Backup mensual |
| `0 2 * * *` | `~/bin/backup-diari.sh` | Backup diari |
| `30 3 * * 6` | `~/bin/backup-setmanal.sh` | Backup setmanal |
| `30 6 * * *` | `~/scripts/ai_digest.py` | Digest d'IA -> `ai` |
| `35 6 * * *` | `~/scripts/morning_digest.py` | Digest del matí -> `hort` |
| `40 6 * * *` | `~/scripts/ciber_digest.py` | CyberQuiz -> `ciber` |
| `45 6 * * *` | `~/scripts/angles_quiz.py` | Anglès: quiz -> `angles` |
| `45 6 * * 1` | `~/scripts/cyber_progress_digest.py` | Progrés setmanal CyberQuiz |
| `50 6 * * *` | `~/scripts/angles_reading.py` | Anglès: lectura -> `angles` |
| `55 6 * * *` | `~/scripts/acer_quiz.py` | Acer: quiz -> `acer` |
| `55 6 * * *` | `~/scripts/kite_quiz.py` | Kitesurf -> `kite` |
| `5 6 * * *` | `~/scripts/meteo_influx.py` | Meteo -> InfluxDB |
| `5 7 * * *` | `~/scripts/noticies_digest.py` | Notícies -> `noticies` |
| `0 7 * * *` | `~/scripts/acer_reading.py` | Acer: lectura -> `acer` |
| `7,19 * * *` | `~/scripts/disk_alert.py` | Alerta de disc ple -> `alerts` |
| `20 7 * * *` | `~/scripts/jazz_quiz.py` | Jazz -> `jazz` |
| `0 8 * * 6` | `~/scripts/hort_digest.py` | Digest setmanal de l'hort |
| `18 0 * * 4` | `~/scripts/kite_alert.py --first` | Previsió de vent de dijous → només si fa vent |
| `10 0 * * 5` | `~/scripts/kite_alert.py` | Veredicte de vent de divendres → sempre |
| `30 19 * * 0` | `~/scripts/jazz_progress_digest.py` | Progrés setmanal de jazz |
| `15 20 * * 0` | `~/scripts/resum_setmanal_digest.py` | Resum setmanal consolidat -> `hort` |

**Convenció dels scripts de digest:** `stdlib` només (sense dependències externes), sense base de
dades, amb l'estat en fitxers `*_state.json` per no repetir preguntes, i una opció `--dry-run`
per provar-los (`python3 angles_quiz.py --dry-run`). El banc de preguntes i el de lectures estan
en fitxers separats (`*_questions.py`, `*_readings.py`) per poder-los ampliar sense tocar la lògica.

**Còpia de seguretat del crontab:** `~/cron.bak.20260915.txt`.

### 12.2 L'agent Hermes al PC de Windows

Al PC de feina (`bernat`, Windows) hi ha instal·lat l'**agent Hermes** (Nous Research), que és qui
gestiona aquest projecte en conversa. Té:

- 26 categories de *skills* (procediments apresos i reutilitzables) al perfil
  `~/AppData/Local/hermes/skills/`.
- Una tasca programada pròpia (`~/AppData/Local/hermes/cron/jobs.json`), amb només una entrada:
  `cyberquiz-missio-setmana` (dilluns a les 08:00, cada setmana genera la missió setmanal del
  CyberQuiz buscant una CVE recent i publicant-la a l'app).
- Accés per SSH a la RPi via Tailscale (amb clau, sense contrasenya).
- Model configurat: Ollama local (`http://127.0.0.1:11434/v1`) amb models locals i al núvol.

**Aquest agent NO és un servei del sistema que s'hagi de mantenir**: és una eina de treball al PC.
Però és el mecanisme pel qual s'ha construït gairebé tota la documentació i el codi, i això
explica l'estil del repositori (tot molt documentat, amb regles explícites i validació real).

---

## 13. Seguretat: estat real i deutes pendents

### 13.1 El que està bé

- **No hi ha cap port obert al router.** Tot l'accés remot és per Tailscale. La RPi està darrere
  de CGNAT (IPv4 compartida del router 4G) i el seu IPv6 està trencat; és a dir, **ni tan sols és
  possible** obrir-li un port encara que es volgués.
- **SSH només amb clau pública**, contrasenya desactivada.
- **Deploy keys separades per repositori** a GitHub, amb permís d'escriptura només al seu repo.
- **Vaultwarden** (contrasenyes) està darrere de HTTPS de Tailscale i només accessible dins el
  tailnet.
- **CI que rebutja secrets i adreces reals** al repositori abans d'acceptar un PR.
- **La pàgina de jubilació té autenticació pròpia** amb cookie signada, límit d'intents i
  capçaleres anticau (perquè no quedi a la memòria del navegador de la feina).

### 13.2 Deutes de seguretat que un programador hauria d'adreçar

| Problema | On | Impacte |
|---|---|---|
| **Credencials en text pla als composes versionats** | `~/monitoring/docker-stack.yml`: usuari admin, contrasenya `bernat2026admin` i token d'API d'InfluxDB `bernat-token-super-secret-2026` | Si aquest fitxer mai entra al repositori, les credencials queden exposades. **Cal migrar a `.env` i afegir-lo al `.gitignore`.** |
| **Mosquitto amb `allow_anonymous true`** | `/opt/mosquitto/config/mosquitto.conf` | Qualsevol dispositiu de la xarxa local pot publicar i subscriure's a qualsevol topic. A la pràctica el port 1883 només és accessible des de la LAN/tailnet, però convé posar usuari i contrasenya abans d'afegir sensors IoT. |
| **Contrasenya del Paperless per defecte** | `PAPERLESS_SECRET_KEY: change-me-to-a-long-random-string` | Cal canviar-la. |
| **Contrasenya de la BD del Paperless** | `paperless` / `paperless` | Només interna, però igualment millorable. |
| **La resta de serveis web no tenen autenticació** | Tots els ports 30xx, 8088, 3000, 9000, 3050... | Qualsevol que entri a la tailnet (o a l'ordinador de la feina, si la tailnet hi està connectada) els pot obrir. El RUNBOOK ho diu explícitament: si algun servei és personal o sensible, cal protegir-lo com es va fer amb la jubilació. |
| **Portainer a HTTP pla (9000) i HTTPS amb certificat propi (9443)** | contenidor `portainer` | El certificat propi dona avisos al navegador. |
| **`~/credentials/credencials.md`** | RPi | Un índex en text de "on viu cada contrasenya". És pràctic, però si es publica és un mapa del tresor. És a la RPi, no al repositori: correcte. |

### 13.3 Superfície pública d'internet (l'inventari que cal revisar quan es faci un canvi)

1. `https://hortosona.tail37c051.ts.net/menu` → **formulari del casament** (:3052). Conté noms
   dels convidats i les seves triades de menú, i un panell d'admin protegit amb contrasenya.
2. `https://hortosona.tail37c051.ts.net/viatge` → **pàgina del viatge** (:3043). Conté dades
   reals de reserves, avions, hotels, localitzadors i matrícules.
3. `https://bernatmora.github.io/bernatlab/` → pàgina del projecte.
4. `https://bernatmora.github.io/hort-osona/` → PWA de l'hort.
5. `https://bernatmora.github.io/cyberlab-ai/` → llibre de ciberseguretat.

> **Conseqüència pràctica:** com que `hort-osona-iot` viu dins el repositori del portal, i el
> portal es publica a GitHub Pages, **tot el contingut de `hort-osona-iot/` és públic**. Regla
> establerta: mai posar-hi tokens ni dades reals.

---

## 14. Hort Osona: la PWA i el seu sistema de construcció

`https://github.com/BernatMora/hort-osona` - 203 MB, 483 fitxers versionats, 72 `.md` a l'arrel,
256 `.md` totals, 48 PDF i 45 HTML imprimibles.

**Què és:** una base de coneixement d'horticultura ecològica adaptada a Osona (Vic), publicada com
a PWA instal·lable que funciona offline. Inclou:

- **9 documents base**: calendari de sembra, associacions i rotacions, gestió de plagues, reg i
  fertilització, cobertes i adobs verds, varietats tradicionals, fitxes de cultiu, pla mensual.
- **26 fitxes de cultiu** a `07-fitxes-cultius/` (all, bleda, bròquil, calçots, canonges, ceba,
  col, enciam, fava, lufa, albergínia, cogombre, nap, moniato, mongeta, pastanaga, patata, pebrot,
  pèsol, rúcula, tomàquet, carbassa, carabassó, blat de moro, maduixa, aromàtiques).
- **18 fitxers a `plans-mensuals/`** (plans de juny a desembre de 2026 + quadern d'observacions +
  guies).
- **Eines operatives**: bitàcola setmanal imprimible, calculadora de reg, calculadora de sembra,
  pressupost anual amb càlcul automàtic, croquis dibuixable, guia de fermentats.
- **Guies avançades** amb PDF i versió imprimible: advenícies, anàlisi de sòl, apotecària
  casolana, aromàtiques, bolets, banys terapèutics, biodinàmica, biologia del sòl.

**Com es construeix (dos generadors diferents, i això és un punt de confusió):**

| Fitxer | Què genera |
|---|---|
| `build_portal_v2.py` | **El `index.html` que es publica** (81 KB, mobile-first: header compacte i calaix lateral a mòbil, barra lateral fixa de 280 px a escriptori). Un sol fitxer HTML amb tot incrustat, sense dependències externes. |
| `build_portal.py` | El generador anterior (versió v1). |
| `site/build.py` + `site/template.html` (162 KB) | **Un altre portal, diferent.** Genera una versió alternativa que inclou `checklist-data.json` i un service worker propi. **Aquesta variant no es publica.** |
| `bin/set-current-month.py` | Actualitza la portada perquè surti el pla del mes actual. És l'únic script de `bin/`. |
| `tests/test_hort_checklist.py` | Test del checklist. |

**Parany documentat:** `site/build.py` i `build_portal_v2.py` són dos portals diferents. Si algú
edita el `index.html` a mà i després algú altre executa un dels generadors, es perd la feina.
**Cal confirmar quin és el generador bo abans de tocar res.**

**El subsistema IoT dins del portal:** `hort-osona-iot/` (137 MB, amb el seu propi `.git`) conté la
còpia de treball del sistema IoT, amb els canvis **sense cometre** (hi ha `api_chat.py`, `rag.py` i
`telegram_bot.py` modificats i `flower_care_reader.py` sense afegir). Això vol dir que **el
repositori hort-osona té treball en curs no desat a Git**.

---

## 15. Bernat CyberLab AI i Bernat Maker Lab

### 15.1 CyberLab AI (`github.com/BernatMora/cyberlab-ai`) - EN PAUSA

Llibre viu de ciberseguretat i laboratori pràctic. Té 113 fitxers i una estructura madura:
`ADR/`, `architecture/`, `inventory/`, `knowledge-base/`, `docker/`, `book/{chapters,exercises,labs,appendices}`,
`captures/`, `reports/` i `network/`.

**Estat:** en pausa perquè el maquinari no està preparat. El laboratori preveu màquines
vulnerables (DVWA, Juice Shop, Metasploitable2) en una **xarxa aïllada 10.10.30.x** perquè no
puguin tocar la resta de la xarxa. Es preveia muntar-ho al Kali (node `hort` del tailnet, aturat
fa 37 dies) o a un HP Z1 G9 amb 32 GB de RAM.

**Relació amb la resta:** **no comparteix infraestructura** amb el BernatLab, a propòsit, per
seguretat. Només comparteix metodologia. Hi ha una còpia de treball dins `bernatlab/bernatlab-cyberlab/`
que s'hauria de considerar temporal.

**Capa de joc associada:** el **CyberQuiz**, una app d'un sol fitxer HTML (`cyberquiz.html`,
292 KB) servida des de la RPi al port 8088. Té **39 missions** organitzades en 5 fases
(Reconeixement, Enumeració, Explotació web, Accés i exploits, Cracking i escànners), cadascuna amb
comanda de Kali, context cultural, pistes i preguntes. El progrés se sincronitza entre dispositius
amb el sidecar `cyberquiz-sync` (:8089). A més, hi ha una **missió setmanal** que genera l'agent
Hermes cada dilluns.

### 15.2 Bernat Maker Lab (`bernatlab/maker-lab/`) - EN CURS

El laboratori personal d'electrònica: aprendre fent amb ESP32, Arduino, Raspberry Pi Pico i
similars, tot local-first.

**Estructura:** `inventari/` (llista del kit bàsic), `docs/decisions/` (ADR 0001 a 0003:
microcontrolador inicial ESP32 DevKit v1, llenguatge inicial Arduino IDE, patró de capítols),
`idees-futures/` (10 fitxers temàtics: càmeres i visió, casa i taller, creatius i experimentals,
energia, esport, hort, IA local, meteorologia, música i guitarra, seguretat) i `projectes/`
(P0: blink + LED via web).

**Integració:** té el capítol 70 del llibre (`book/chapters/70-bernat-maker-lab.md`) i el mòdul M9
del curs (`book/curs/M9/01-blink-i-led-via-web/`). Els compiladors (`make_book.py`,
`build_course.py`) ja tenen el mòdul integrat.

---

## 16. Treball en curs i coses no acabades

Aquesta secció és deliberadament franca: qualsevol programador que arribi ha de saber què està a
mitges.

### 16.1 Treball sense desar a Git

| On | Què |
|---|---|
| `~/bernatlab` (RPi) | Al dia amb `origin/main` (`c2c366b`). |
| `~/bernatlab` (Windows) | **Està 2 commits ENDARRERIT** respecte `origin/main`: el seu HEAD és `d669588` (17-08-2026). Els commits `cbbb061` (Inventari d'infraestructura) i `c2c366b` (Docs: repos i accessos), del 29-08-2026, es van fer A LA RPi i només existeixen allà i a GitHub. Al Windows falten. |
| `~/hort-osona` (RPi) | IoT modificat sense cometre: `backend/api_chat.py`, `rag.py`, `telegram_bot.py` i `flower_care_reader.py` nou. |

### 16.2 Feines obertes, per ordre de rendibilitat

1. **Corregir `INVENTARI-INFRASTRUCTURA.md`** (5 min): diu 8 GB de RAM i la IP .100; són 4 GB i
   la .103. També diu que `hortosona` té "Ollama" com a servei del PC de l'hort, cosa que ja no és
   certa (`bernat-pc` no existeix).
2. **Decidir la font de veritat del codi IoT** (`~/hort-osona/hort-osona-iot/` vs
   `~/bernatlab/projects/hort-osona-iot/`) i establir una sincronització. Avui hi ha dues còpies
   divergents.
3. **Unificar el criteri del maquinari LoRa**: hi ha dos documents que descriuen maquinari diferent
   (HAT SX1262 per SPI amb TTGO vs HAT E22-900T22S per UART amb Heltec). Cal decidir quin és el bo
   i esborrar o marcar l'altre com a obsolet.
4. **Treure les credencials del `docker-stack.yml`** i passar-les a `.env`.
5. **Posar autenticació a Mosquitto** abans de connectar-hi cap sensor.
6. **Decidir si s'activa o es retira l'input `mqtt_consumer` de Telegraf** (avui és codi mort).
7. **Confirmar quin és el generador bo del portal de l'hort** (`build_portal_v2.py` vs
   `site/build.py`) i documentar-ho.
8. **`hort-sensor/config/sensor.yaml` està desactualitzat**: diu que InfluxDB té estat "A
   configurar" i el bucket `hort` (que no existeix; el bucket real és `metrics`), i que Mosquitto
   està "Funcionant" quan el seu daemon està aturat.
9. **Time Machine al MacBook Air**: hi ha el volum configurat a Samba i un `sparsebundle` de 14 GB,
   però a l'inventari figura com a pendent "cal disc extern local".
10. **El mòdul M8 del curs té 7 capítols** i **M9 en té 1**: si la intenció és la paritat de 10
    capítols per mòdul, falten 3 i 9 respectivament.

### 16.3 Idees previstes (no compromeses)

Publicar un article a Infojardin i a L'agrobotiga, un vídeo a YouTube, afegir càmeres i reg
automàtic a l'hort, activar la skill d'Alexa en producció, muntar l'HP Z1 G9 amb màquines virtuals
per al CyberLab.

---

## 17. Guia pràctica per a qui arriba nou

### 17.1 Per accedir-hi

```bash
# Des de qualsevol màquina amb Tailscale
ssh bernat@hortosona          # o ssh bernat@100.115.134.76

# Des de casa, per xarxa local
ssh bernat@192.168.1.103
```

### 17.2 Les cinc comandes que ho expliquen tot

```bash
docker ps --format '{{.Names}}\t{{.Image}}\t{{.Ports}}\t{{.Status}}'   # 22 contenidors
pm2 list                                                               # 9 processos
ss -lntp                                                               # tots els ports en escolta
crontab -l                                                             # 23 tasques programades
tailscale serve status && tailscale funnel status                      # què és públic
```

### 17.3 Per entendre el sistema abans de tocar-lo

Ordre de lectura recomanat:

1. Aquest informe (seccions 1, 4, 5 i 6).
2. `/home/bernat/RUNBOOK.md` - 1.360 línies, el document mestre d'operacions. Conté tots els
   paranys viscuts.
3. `~/bernatlab/PROJECT_STATE.md` - estat del projecte i decisions amb el seu raonament.
4. `~/bernatlab/PROJECT_STATE-GLOBAL.md` - com es relacionen els 3 projectes.
5. `~/bernatlab/INVENTARI-INFRASTRUCTURA.md` - inventari (amb els errors de la secció 2).
6. `~/hort-osona/PROJECTE-COMPLET.md` - visió completa del projecte de l'hort.

### 17.4 Regles de treball en aquest sistema

1. **`pm2 save` després de qualsevol canvi a un procés pm2.** Sense això el canvi no sobreviu al
   reinici.
2. **No desar dades a la microSD si poden anar a `/mnt/nuvol`.** La microSD es desgasta.
3. **Servei nou -> triar un port lliure per sobre de 3050** (la sèrie 30xx és per als projectes
   web), afegir-lo al `services.yaml` de la Homepage, reiniciar el contenidor `homepage` i fer una
   còpia del codi a `/mnt/nuvol/projects/`.
4. **Després de tocar el sistema, actualitzar `~/RUNBOOK.md` i copiar-lo a `/mnt/nuvol/RUNBOOK.md`.**
5. **Validar amb execució real.** No reportar "fet" sense proves. El projecte té una regla
   explícita sobre això i ve d'una experiència concreta.
6. **Abans d'actualitzar imatges Docker, fer còpies de les dades i etiquetar les imatges
   actuals** (`<imatge>:preupdate-<data>`). Aquest procediment ja està provat: al setembre de 2026
   es van actualitzar 8 serveis (incloent-hi tres canvis de versió major: Homepage, Uptime-Kuma i
   Grafana amb 3 sals) sense cap pèrdua.
7. **No posar mai tokens ni dades reals al repositori** (el CI ho rebutja i a més el portal de
   l'hort és públic).
8. **Verificar amb `md5sum` a totes dues bandes** quan es pugin fitxers de Windows a la RPi: el
   `scp` des d'aquest Windows ha fallat en silenci més d'un cop.

### 17.5 Com validar que tot va bé

```bash
# Tots els serveis responen (hauria de sortir 200 o 302 a tot)
for p in 3000 3001 3002 3010 3011 3012 3013 3014 3015 3016 3030 3035 3040 \
         3041 3042 3043 3044 3050 3051 3052 5000 8080 8086 8088 8089 8090 9000; do
  printf "%s -> %s\n" "$p" "$(curl -s -o /dev/null -m 3 -w '%{http_code}' http://localhost:$p/)"
done

# El backup de la matinada ha sortit net?
tail -20 /home/bernat/logs/backup-diari.log

# L'input de disc hi cap?
df -h / /mnt/nuvol

# Què és públic?
tailscale funnel status
```

**Nota:** a la llista de ports, un `302` és un resultat **bo** (és una redirecció cap a
`index.html` o cap a la pàgina de login). El que seria dolent és un `000` (no respon) o un `500`.

### 17.6 On anar a buscar quan alguna cosa falla

| Símptoma | On mirar |
|---|---|
| Un servei web no respon | `pm2 list` i `pm2 logs <nom>` (si és pm2), `docker ps` i `docker logs <nom>` (si és Docker) |
| Un servei Docker no arrenca | **`docker logs`, no l'estat** (l'estat pot dir `Restarting` i amagar l'error real) |
| Un panell de Grafana surt buit | Comprovar amb el rang que el panell fa servir de debò; un rang massa gran retorna `truncated at 1001 points` |
| Un digest ntfy no arriba | `~/scripts/<script>.log` i `~/scripts/<script>_state.json` |
| El backup dona error | `~/logs/backup-diari.log` (els "OK" per secció) |
| Un servei web es veu malament des de fora | Comprovar el Funnel i, si el servidor fa una redirecció 302, és el parany de la secció 3.4 |
| Falta espai | `df -h`, i recordar que `/mnt/nuvol` és el disc gran (458 GB, 7% usat) |

---

## 18. Glossari

Termes que apareixen en aquest informe i que potser no són obvis:

| Terme | Què és |
|---|---|
| **BernatLab** | El marc general del projecte: el servidor, el llibre, el curs, els projectes web i l'IoT. |
| **Hort Osona** | Un projecte concret dins del marc: la PWA d'horticultura i els plans mensuals. |
| **Hort Osona IoT** | El subsistema de sensors de l'hort (LoRa + Supabase + Alexa + Telegram + RAG). No funciona encara. |
| **`hortosona`** | El nom de la Raspberry Pi. |
| **Tailscale** | Xarxa privada virtual (VPN mesh) que connecta tots els dispositius de l'usuari com si fossin a la mateixa xarxa local, sense obrir ports a internet. |
| **tailnet** | La xarxa privada de Tailscale d'un compte. |
| **Tailscale Serve** | Exposa un servei local amb HTTPS **només dins la tailnet**. |
| **Tailscale Funnel** | Exposa un servei local **a internet**. És el que fa públic el formulari del casament. |
| **Docker** | Sistema de contenidors: empaqueta un programa amb tot el que necessita i l'aïlla de la resta. |
| **Docker Compose** | Fitxer de text (`compose.yml`) que descriu un o més contenidors i com s'aixequen. |
| **contenidor** | Una instància en marxa d'una imatge Docker. |
| **imatge / etiqueta / digest** | Una imatge és la plantilla (ex. `grafana/grafana`); l'etiqueta és la versió llegible (`13.2.2`); el digest és l'empremta única del contingut. **Comparar digests, no etiquetes.** |
| **volum Docker** | Un espai de disc que sobreviu a l'eliminació del contenidor. |
| **pm2** | Gestor de processos de Node, però aquí s'usa també per a scripts Python. Manté les aplicacions en marxa i les ressuscita al reinici. |
| **systemd** | El gestor de serveis del sistema Linux. |
| **cron** | El planificador de tasques de Linux. |
| **crontab** | La llista de tasques de cron d'un usuari. |
| **ntfy** | Servidor de notificacions push: s'envia un missatge a un "topic" i qui hi estigui subscrit el rep al mòbil. |
| **MQTT** | Protocol de missatgeria lleuger per a IoT. Els sensors "publiquen" en "topics" i els clients "se subscriuen". |
| **Mosquitto** | El broker (servidor) MQTT. |
| **Telegraf** | Recol·lector de mètriques: llegeix l'estat del sistema i l'envia a una base de dades. |
| **InfluxDB** | Base de dades de sèries temporals (ideal per a mètriques i sensors). |
| **Grafana** | Eina de gràfics que llegeix d'InfluxDB i dibuixa panells. |
| **Flux** | El llenguatge de consultes d'InfluxDB 2.x. |
| **Uptime Kuma** | Monitor de disponibilitat: comprova cada servei i avisa si cau. |
| **Homepage** | El dashboard que enllaça tots els serveis. |
| **Portainer** | Interfície gràfica per gestionar Docker. |
| **Nextcloud** | Núvol de fitxers autoallotjat. |
| **Vaultwarden** | Servidor compatible amb Bitwarden per a contrasenyes. |
| **Paperless-ngx** | Gestor documental: escaneja, fa OCR i indexa documents per poder-los buscar. |
| **Ollama** | Eina per executar models de llenguatge (IA) localment, sense enviar dades al núvol. |
| **RAG** | *Retrieval-Augmented Generation*: buscar informació pròpia i donar-la al model perquè respongui amb aquesta base. |
| **LoRa** | Ràdio de llarg abast i baixa potència (868 MHz a Europa). |
| **SPI / UART** | Dues maneres de connectar un mòdul als pins d'una Raspberry Pi o un microcontrolador. |
| **BLE** | Bluetooth de baix consum, el que fan servir els sensors petits. |
| **PWA** | *Progressive Web App*: una pàgina web que es pot instal·lar al mòbil i funciona offline. |
| **CGNAT** | *Carrier-Grade NAT*: l'operadora 4G comparteix una única IPv4 entre molts clients, cosa que impedeix obrir ports cap a fora. |
| **ADR** | *Architecture Decision Record*: un fitxer curt que documenta una decisió tècnica i el perquè. |
| **`.ictx`** | Format d'entrenament del programa icTrainer (el que l'usuari fa servir a la bici). |
| **`.zwo`** | Format d'entrenament del programa Zwift. S'importa, però no és el que es fa servir. |
| **FTP / watts / cadència** | En els entrenaments: FTP és la potència màxima sostinguda una hora; cadència és les pedalades per minut. |

---

## 19. Resum de fitxers clau per localitzar-ho tot

| Què | On |
|---|---|
| Document mestre d'operacions | `/home/bernat/RUNBOOK.md` (+ còpia a `/mnt/nuvol/RUNBOOK.md`) |
| Estat del projecte | `~/bernatlab/PROJECT_STATE.md` i `PROJECT_STATE-GLOBAL.md` |
| Inventari d'infraestructura | `~/bernatlab/INVENTARI-INFRASTRUCTURA.md` (amb errors coneguts) |
| Composes Docker | `~/homelab/compose/<servei>/compose.yml` + `~/nextcloud/`, `~/monitoring/`, `~/docker/portainer/`, `~/entrenaments-app/` |
| Scripts de digest i dades | `/home/bernat/scripts/` (26 fitxers `.py`) |
| Scripts de backup i arrencada | `/home/bernat/bin/` |
| Serveis systemd propis | `/etc/systemd/system/{kettlebell,miflora,hort-osona-chat,hort-osona-telegram,alexa-hort}.service` |
| Definicions de pm2 | `~/.pm2/dump.pm2` |
| Credencials i el seu índex | `~/credentials/credencials.md` i `~/credentials/ntfy-bernat.txt` |
| Dashboards de Grafana | Base de dades `/opt/grafana/data/grafana.db` (taula `dashboard`) |
| Configuració de Grafana | `/opt/grafana/config/grafana.ini` |
| Broker MQTT | `/opt/mosquitto/config/mosquitto.conf` |
| Dades de sensors (retenció 30 dies) | Volum Docker `monitoring_influxdb-data` |
| Còpies de seguretat | `~/backups-bd/` (BD) i `/mnt/nuvol/{backups-diari,backups-setmanal,backups-sistema}/` |
| Llibre i curs | `~/bernatlab/book/` |
| Curs: manifest i eines | `~/bernatlab/book/curs/{course-manifest.json,build_course.py,quiz.py}` |
| PWA de l'hort | `~/hort-osona/` (generador: `build_portal_v2.py`) |
| IoT (treball) | `~/hort-osona/hort-osona-iot/` |
| IoT (versionat) | `~/bernatlab/projects/hort-osona-iot/` |
| CyberLab | `https://github.com/BernatMora/cyberlab-ai` |
| Maker Lab | `~/bernatlab/maker-lab/` |
| Apps web servides | `/mnt/nuvol/projects/` (15 carpetes) |
| Fitxers estàtics del menú i el CyberQuiz | `~/www-menu/` |

---

## 20. Nota final per al programador

Aquest sistema l'ha construït una persona que **no és informàtica de professió** i que ho ha anat
aprenent sobre la marxa, amb l'ajuda d'un agent d'IA i amb una disciplina notable de documentar-ho
tot. Això explica les seves virtuts i els seus defectes:

**Virtuts:** està tot documentat fins al detall, cada decisió té el seu raonament escrit, els
paranys viscuts estan apuntats perquè no es repeteixin, i el sistema està en producció real
(nívol, contrasenyes, documents, backups) funcionant amb una sola màquina de 4 GB.

**Defectes, i són pocs però cal tenir-los presents:**

1. **No hi ha cap orquestrador únic.** Conviuen quatre mecanismes (Docker, pm2, systemd, cron) i
   cal saber quin governa cada peça. És la font número u de confusió.
2. **Hi ha còpies duplicades de codi** (l'IoT, en dos llocs, ja divergits; i dos generadors del
   portal de l'hort). Cal decidir la font de veritat.
3. **Hi ha credencials en text pla** en fitxers de configuració de Docker.
4. **L'inventari oficial té dades incorrectes** (RAM i IP).
5. **La RAM va justa.** Qualsevol servei nou ha de ser lleuger.

La manera correcta de treballar-hi és la que ja està establerta: **llegir el RUNBOOK abans de
tocar res, validar amb execució real, documentar el canvi al RUNBOOK, i `pm2 save` sempre.**
