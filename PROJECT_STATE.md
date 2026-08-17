# PROJECT STATE - BernatLab

> Estat actual del projecte BernatLab (RPi 4 + Docker + Tailscale + IA + LoRa + Hort Osona).
> Document de referència per continuar treballant des de qualsevol dispositiu o sessió.
>
> **Ultima revisio documental:** 2026-XX-XX (revisio post-sessio DeepSeek)
>
> **Tall de dades operatives:** Cal verificar l'estat real dels serveis a la RPi abans d'executar canvis.

---

## 1. Que es el projecte

**BernatLab** es un servidor personal basat en una Raspberry Pi 4 amb Debian 13 Lite, Docker, Docker Compose, Tailscale, Portainer, Uptime Kuma i Homepage. Es el centre dels projectes de l'usuari: Hort Osona (PWA + IoT), sensors LoRa, meteorologia, IA local, automatitzacions i desenvolupament web.

> **Nota:** Aquest PROJECT_STATE cobreix **nomes el BernatLab**. Per a una vista global de tots els projectes de l'usuari, veure `PROJECT_STATE-GLOBAL.md`.

**Hardware/programari/recursos principals:**

| Concepte | Valor |
|---|---|
| Maquinari | RPi 4 Model B, 4 GB RAM, microSD 32GB |
| SO | Debian GNU/Linux 13 Trixie Lite (arm64) |
| Hostname | hortosona |
| Usuari | bernat |
| IP Tailscale | `[VALOR_LOCAL]` — consultar Tailscale o `_local/`; no publicar adreces reals |
| Contenidors actius (esperats) | Portainer (9443), Uptime Kuma (3001), Homepage (3000), Ollama |
| SIM de dades | 150 GB/mes al router 4G de l'hort |
| ESP32 + LoRa | 1 unitat TTGO LoRa32 + BME280 + sensor sol (a l'hort) |

---

## 2. Les parts principals del projecte

| # | Nom | Estat | Cost | Notes |
|---|---|---|---|---|
| 1 | **Llibre del BernatLab** | En curs | 0 EUR | 7 moduls, 70 capitols, 584 pagines (PDF + DOCX) |
| 2 | **Curs practic** | En curs | 0 EUR | 77 capitols, 1.087 preguntes |
| 3 | **Hort Osona (PWA)** | En curs | 0 EUR | 8 plans mensuals publicats, web PWA |
| 4 | **Glossari complet** | Decidit | 0 EUR | 321 termes, ~70 KB |
| 5 | **Guia "El meu primer dia"** | Decidit | 0 EUR | Pas a pas, 12 KB |
| 6 | **Arquitectura visual (3 SVGs)** | Decidit | 0 EUR | Xarxa, IoT, curs |
| 7 | **Hort Osona IoT (LoRa + Supabase)** | En curs / diagnosi | ~105 EUR | Software complet, hardware comprat, no funciona encara |
| 8 | **Alexa skill Hort Osona** | En curs | 0 EUR | Skill definida, backend Python |
| 9 | **Bot Telegram + RAG** | En curs | 0 EUR | telegram_bot.py + Ollama RAG |
| 10 | **MyCloudHome storage** | En curs | 0 EUR | NAS local per portal Hort Osona |
| 11 | **Tailscale setup complet** | Decidit | 0 EUR | Guies Mac + scripts setup |
| 12 | **Scripts `bin/`** | Decidit | 0 EUR | 7 scripts (PowerShell, bash, acces directe) |
| 13 | **Publicacions externes** | Pendent | 0 EUR | Infojardin, Ruralcat, L'agrobotiga, YouTube |

Estats possibles: **Decidit, Planificat, En curs, Pendent, Descartat**

---

## 3. Integracions amb eines i serveis

- **GitHub** — Repos BernatLab, Hort Osona i CyberLab AI (publics)
- **GitHub Pages** — Publicacio de BernatLab i Hort Osona
- **Tailscale** — VPN mesh per accedir a la RPi des de qualsevol lloc
- **Telegram** — Bot de Hort Osona (amb RAG + Ollama)
- **Ollama** — IA local amb models `gemma3:1b` i `phi3:mini`
- **Portainer** — Gestio de contenidors
- **Uptime Kuma** — Monitoritzacio de serveis
- **Homepage** — Panell d'inici personalitzat
- **Supabase** — Base de dades Realtime per a lectures de sensors
- **LoRa 868 MHz** — Comunicacio entre node hort i receptor RPi (TTGO LoRa32 + HAT SX1262)
- **Alexa Skill** — Comandaments de veu per consultar l'hort
- **MyCloudHome** — NAS local (192.168.x.x) per allotjar portal public
- **Router 4G** — Internet propi a l'hort (pròximament)

---

## 4. Documentacio generada

- **book/** (carpeta principal)
  - **book/llibre/** — 7 moduls del llibre (PDF + DOCX)
  - **book/curs/** — 77 capitols del curs
  - **book/glossari.md** (68 KB) — Glossari amb 321 termes
  - **book/primer-dia-rpi.md** (12 KB) — Guia pas a pas
  - **book/arquitectura/** — 3 SVGs + index
  - **book/handoff-sessio-2026-07-17.md** (6 KB) — Handoff d'aquesta sessio
  - **book/wiki/** — Wiki del llibre
  - **book/cheatsheet.html** — Chuleta de comandes
- **projects/hort-osona/** — Web PWA Hort Osona (submodule)
  - **plans-mensuals/** — 8 plans mensuals (juny-desembre 2026)
  - **docs/plans-mensuals/** — Versions HTML dels plans
- **projects/hort-osona-iot/** — Sistema IoT complet (afegit 2026-XX-XX)
  - **node-emissor/** — ESP32 + BME280 + LoRa (firmware PlatformIO)
  - **backend/** — Receptor LoRa + Supabase + Ollama (Python)
  - **alexa-skill/** — Skill Alexa Hort Osona
  - **bridge/** — Gateway entre sistemes
  - **web/** — Vista Hort Live amb dades realtime
  - **systemd/** — Serveis systemd (telegram, etc.)
  - **scripts/** — Scripts de setup i manteniment
  - **docs/** — Documentacio especifica del IoT
- **posts/** — Esborranys de publicacions externes
- **bin/** — 7 scripts (PowerShell, bash, acces directe a l'escriptori)

---

## 5. Decisions preses (amb raonament)

- **Tailscale per accedir a la RPi des de fora**: No cal obrir ports al router, es mes segur.
- **LoRa 868 MHz entre hort i RPi (no WiFi direct)**: Distancia ~400m i RPi a casa (no a l'hort). El node LoRa a l'hort envia per radio al receptor LoRa a la RPi (HAT SX1262).
- **Supabase per a dades de sensors**: Base de dades Realtime al núvol + esquema SQL propi (2 taules: `mesures` i `consells_ia`).
- **Ollama per a IA local**: Consells cada 6h generats amb el model local, sense enviar dades al núvol.
- **RPi al WiFi del router 4G (no a xarxa de casa)**: Te internet propi a l'hort, no depen de la cobertura de casa.
- **Catala com a llengua per defecte**: L'usuari es catala, tota la documentacio esta en catala.
- **Markdown + Git per versionar**: Permet fer canvis amb ordre i tornar enrera si cal.
- **GitHub Pages per publicar**: Gratuit, facil d'actualitzar amb `git push`.
- **Patro de capitols estandard**: resum + quiz + exercici + respostes + HTML per consistencia.
- **Scripts a `bin/`**: Eines utils per accedir rapidament al projecte des de qualsevol PC.
- **150 GB SIM de dades**: Suficient per a sensors i pujada de dades, pero cal vigilar el consum.

---

## 6. Sistema IoT Hort Osona — estat real

> **Aquest apartat es la part mes activa del projecte.** La resta del BernatLab es estable, pero el IoT encara esta en fase de validacio hardware.

### 6.1 Arquitectura implementada

```
HORT (~400 m)                                 CASA (RPi 4 + HAT SX1262)
===========================                   ==========================
- TTGO LoRa32 868 MHz                         - HAT Waveshare SX1262
- BME280 (T, H, P)                           - lora_receiver.py
- 2 sensors sol capacitius                   - INSERT a Supabase
- 2 bateries 18650 + panell solar            - Ollama (consells cada 6h)
- Caixa IP65
- Payload CSV: "T:18.5,H:62.3,P:1013.2,S:45,BAT:3.92"
```

### 6.2 Software complet (NO cal re-escriure)

- `node-emissor/src/main.cpp` — Cicle deep sleep + lectura sensors + LoRa TX
- `node-emissor/platformio.ini` — Build config PlatformIO
- `node-emissor/specs/bom.json` — Llista de materials
- `node-emissor/docs/steps.json` — Guia de muntatge pas a pas
- `backend/lora_receiver.py` — Rep LoRa -> Supabase -> Ollama
- `backend/supabase_schema.sql` — 2 taules (`mesures`, `consells_ia`) + Realtime
- `web/hort-live.html` — Vista amb grafic 24h + subscripcio Realtime
- `telegram_bot.py` + `systemd/hort-osona-telegram.service` — Bot Telegram
- `alexa-skill/interaction-model.json` + `alexa_backend.py` — Skill Alexa
- `setup-pi.sh` — Script d'instal·lacio a la RPi
- `telegram_bot.py`, `rag.py`, `mycloud_storage.py` — Moduls de negoci

### 6.3 Hardware comprat (NO funciona encara)

- [x] Hardware especificat (Bricogeek + Amazon ES)
- [x] **Hardware comprat** (2026 aprox.)
- [ ] **Muntar el node** — pas critic, validacio hardware pendent
- [ ] **Muntar el receptor** — HAT SX1262 a la RPi, cal verificar pins GPIO
- [ ] **Crear compte Supabase** i executar `supabase_schema.sql`
- [ ] **Provar el flux complet** — primeres dades reals

**Cost total:** ~105 EUR (veure `node-emissor/specs/bom.json`)

### 6.4 Problemes coneguts (a diagnosticar en proxima sessio)

- **"Comprat pero no funciona"** — estat declarat per l'usuari. Cal:
  1. Verificar que el hardware esta correctament cablejat
  2. Confirmar que el firmware del node puja (`pio run --target upload`)
  3. Comprovar la conectivitat LoRa (antenes, distancia, orientacio)
  4. Validar el receptor Python a la RPi amb el HAT SX1262
  5. Crear el compte Supabase i configurar les claus
- **Possibles causes** (a investigar):
  - Pins del HAT SX1262 no coincideixen amb els del README
  - Abast LoRa insuficient (pot caldre antena externa o repeater)
  - Configuracio de frequencia (868 MHz vs 915 MHz)
  - Permis GPIO/spidev a la RPi

### 6.5 Documentacio especifica del IoT

Tots aquests fitxers son **fonts de veritat** del sistema IoT:

- `README.md` — Visio general + arquitectura ASCII
- `INICI-RAPID.md` — Quickstart
- `LLISTA-CURTA.md` — Llista curta de passos
- `PAS-SEGUENT.md` — Proxim pas a fer
- `GUIA-MUNTATGE-NODE.md` — Guia completa de muntatge del node
- `ALEXA-ACTIVAR.md` + `ALEXA-GUIA.md` + `COM-TROBAR-SKILL.md` — Skill Alexa
- `TELEGRAM-SETUP.md` — Configurar bot Telegram
- `RAG-README.md` — RAG amb Ollama
- `MYCLOUDHOME-GUIA.md` — NAS local
- `PEDIDO-AMAZON.md` + `PEDIDO-AMAZON.pdf` — Llista de compra
- `RPi-PROJECTES.md` — Altres projectes a la RPi
- `CHAT-SETUP.md` — Xat amb IA
- `GUIA-TAILSCALE-MAC.pdf` — Tailscale al Mac

---

## 7. Notes operatives (importants)

### Estalvi de dades (eSIM)

El sistema s'ha optimitzat per minimitzar el consum de dades de la eSIM:

**Desactivat actualment** (estalvi garantit):
- `hort-osona-telegram.service` al bernat-pc (aturat)
- `apt-daily.timer` i `apt-daily-upgrade.timer` a RPi i bernat-pc

**Tailscale** (RPi): `--accept-dns=false --accept-routes=false --netfilter-mode=off`

**Per tornar a activar el bot:**
```bash
ssh bernat-pc
sudo systemctl enable --now hort-osona-telegram.service
```

**Per tornar a activar actualitzacions:**
```bash
sudo systemctl enable --now apt-daily.timer apt-daily-upgrade.timer
```

### Distribucio de responsabilitats

- **RPi (hortosona)**: gateway IoT, MQTT, InfluxDB, Grafana, Nextcloud, MariaDB. Reb dades dels sensors.
- **bernat-pc**: serveis d'IA (Ollama), bot Telegram (quan esta actiu), scripts de desenvolupament.
- **PC feina (bernat)**: client de desenvolupament, conecta als altres dos via Tailscale.

### Connexions Tailscale actives

- hortosona (100.115.134.76) <-> bernat-pc (100.121.249.107): directe (192.168.1.x)
- bernat (100.82.142.113) <-> hortosona i bernat-pc: directe quan possible, DERP com a fallback
- hort, iphone, macbook: offline temporalment

---

## 8. Pendents immediats (proxims passos)

### A. Auditar l'estat real de la RPi via SSH (30 min)
1. `ssh bernat@<IP_TAILSCALE>` desde el PC de la feina
2. Verificar contenidors: `docker ps`
3. Verificar serveis: `systemctl status` per als serveis hort-osona-*
4. Comprovar disc: `df -h` i `du -sh /home/bernat/homelab/data/`
5. Verificar Tailscale: `tailscale status`

### B. Diagnosticar perque el IoT no funciona (1-2 h)
1. Inventariar el hardware comprat i fer fotos
2. Verificar el cablejat del node TTGO LoRa32 amb el BME280
3. Verificar el HAT SX1262 a la RPi (pins, soldadura si cal)
4. Mirar logs: `journalctl -u hort-osona-*` (si els serveis existeixen)
5. Si cal, refer el muntatge seguint `GUIA-MUNTATGE-NODE.md`

### C. Crear el compte Supabase (15 min)
1. Anar a https://supabase.com i crear compte
2. Crear nou projecte "hort-osona"
3. Executar `backend/supabase_schema.sql` al SQL Editor
4. Copiar URL i anon key -> `.env` a la RPi (MAI al repo)

### D. Provar el flux complet (1-2 h)
1. Pujar firmware al node: `pio run --target upload`
2. Encendre el node a l'hort amb bateria carregada
3. Verificar que el receptor Python veu el payload LoRa
4. Comprovar que les dades apareixen a Supabase
5. Veure el grafic a `web/hort-live.html`

### E. Documentar el primer runbook reeixit (30 min)
1. Escriure `book/handoff-sessio-IoT-YYYY-MM-DD.md` amb el que ha funcionat
2. Actualitzar aquest PROJECT_STATE amb l'estat verificat
3. Fer commit i push amb els canvis

### F. Pujar els canvis d'aquesta sessio al repo (30 min)
1. Commit del projecte IoT anonimitzat: `projects/hort-osona-iot/`
2. Commit d'aquest PROJECT_STATE refrescat
3. Push a `origin/main`

---

## 9. Restriccions i regles del projecte

- **No usar apostrofs tipografics ni cometes intelligents** als fitxers — usar ASCII (`'`, `"`, `-`).
- **Cap credencial ni token** al repo ni al context — tot `[REDACTED]`.
- **Llengua catalana** per defecte.
- **Validar amb execucio real**, no promeses teoriques.
- **Cap "Paraules clau" al final** dels capitols.
- **Tots els fitxers UTF-8 valids**.
- **Fer servir fitxers petits, nets, editables** (KISS).
- **Sempre provar abans de reportar "fet"** — el que compta es el resultat.
- **No usar `cd` per canviar de directori** — usar `project_switch`.
- **Scripts llargs via `write_file`**, no pas `execute_code` (que pot bloquejar-se).
- **Mai practicar ciberseguretat des de l'equip de la feina** (risc laboral).
- **Anonimitzar IPs (192.168.x.x i 100.x.x.x) abans de fer commit** — ja fet en aquesta sessio.

---

## 10. Glossari

- **BernatLab:** El projecte global (servidor + llibre + curs + hort).
- **Hort Osona:** El projecte especific de l'hort (PWA + plans mensuals).
- **Hort Osona IoT:** Sistema de sensors amb LoRa + Supabase + Ollama (a `projects/hort-osona-iot/`).
- **hortosona:** Hostname de la RPi 4 a l'hort (o a casa segons configuracio).
- **Tailscale:** VPN mesh que permet accedir a la RPi sense obrir ports.
- **TTGO LoRa32:** Placa ESP32 amb LoRa 868 MHz integrat, ideal per nodes IoT.
- **BME280:** Sensor combinat de temperatura, humitat i pressio.
- **HAT SX1262:** Hat per a RPi amb modem LoRa SX1262 (Waveshare).
- **Supabase:** Backend amb Postgres + Realtime + Auth (alternativa open source a Firebase).
- **Ollama:** Eina per executar LLMs localment.
- **RAG:** Retrieval Augmented Generation (cerca + generacio).
- **4G:** Xarxa mobil de quarta generacio (LTE).
- **SIM:** Targeta d'identitat de subscriptor (mobil).
- **IP Tailscale:** Adreca unica per accedir a la RPi via Tailscale (100.x.x.x).
- **Payload LoRa:** Paquet de dades enviat per radio LoRa (CSV compacte).
- **Realtime:** Subscripcio push a Supabase per rebre actualitzacions en temps real.

---

## 11. Preferencies de l'usuari

- **Llengua:** Catala per defecte (barreja castella amb naturalitat).
- **Estil de treball:** Lots petits validats, tests via terminal amb .venv, no reportar "fet" sense proves.
- **Prioritat:** Maquines utils, no decoratives.
- **Estil de comunicacio:** Directe, sense elogis buits.
- **Senyals de tancament:** "anem per un altre tema", "ja esta" -> wrap-up deliverables.
- **Patrons:** Iterar sobre artefactes, validar amb execucio real, recordar errors.
- **Interessos:** RPi, Docker, Tailscale, IA local, LoRa, horticultura, IoT.
- **No:** Mai demanar/acceptar credencials. Mai inventar dades.

---

## 12. Com reprendre aquesta sessio

Si vols continuar des d'un altre dispositiu o sessio:

1. **Llegeix `PROJECT_STATE.md`** (aquest fitxer) — te l'estat actual.
2. **Mira els ultims commits** a GitHub: `git log --oneline -10`
3. **Comprova el working tree** per veure canvis pendents: `git status`
4. **Continua des de la seccio 7 (Pendents immediats)** d'aquest document.

Si estas a la feina (Windows):
- Obre el terminal i connecta't per SSH a la RPi via Tailscale.
- Si no tens Tailscale actiu, treballa nomes amb documentacio.

Si estas a casa (Mac):
- Obre el Terminal del Mac.
- Ves al directori del repo: `cd ~/bernatlab` (o on sigui que el tinguis).
- Continua treballant directament amb `git` i SSH a la RPi.

---

## 13. Projectes relacionats

L'usuari te **altres projectes** que conviuen amb el BernatLab. Tots estan publicats a GitHub i es poden accedir des de qualsevol node del tailnet.

### Bernat CyberLab AI (laboratori de ciberseguretat)

- **Repositori:** https://github.com/BernatMora/cyberlab-ai
- **Web:** https://bernatmora.github.io/cyberlab-ai/
- **Descripcio:** Llibre viu sobre ciberseguretat amb laboratori practic muntat al Kali. Documenta com construir i usar un laboratori personal modular de ciberseguretat.
- **Estat actual (2026):** **En pausa** — el hardware no esta preparat encara.
- **Diferencia respecte al BernatLab:**
  - CyberLab = ciberseguretat (atac i defensa en entorn aillat).
  - BernatLab = servidor en produccio (RPi + serveis reals).
- **Relacio:** No comparteixen infraestructura (estan aillats per seguretat), pero comparteixen metodologia (PROJECT_STATE, commits petits, documentacio pedagogica en catala).

### Altres projectes (mencionats a sessions anteriors)

- **Hort Osona** — PWA amb plans mensuals de l'hort (ja cobert a la seccio 4 d'aquest PROJECT_STATE).

---

## Versio

| Data | Canvis |
|---|---|
| 2026-08-07 | Afegida seccio "Projectes relacionats" amb el CyberLab AI. |
| 2026-08-04 | Revisio: anonimitzacio de xarxa, separacio entre estat documental i operatiu, i desplegament IoT segur amb Compose. |
| 2026-07-17 | Creacio del PROJECT_STATE per primera vegada. Inclou: llibre + curs (77 cap., 1087 preguntes) + Hort Osona (8 plans mensuals) + glossari + guia + arquitectura + router 4G pendent + ESP32 pendent. |
| 2026-XX-XX | **Refresc post-sessio DeepSeek**: afegit el projecte `hort-osona-iot/` real (LoRa + Supabase + Alexa + Telegram + RAG + MyCloudHome), reconegut l'estat "comprat pero no funciona", nova seccio 6 dedicada al IoT, noves decisions i glossari ampliat. |

---

**Plantilla original:** `book/PROJECT-STATE-TEMPLATE.md`
