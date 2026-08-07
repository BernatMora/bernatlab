# PROJECT STATE - BernatLab

> Estat actual del projecte BernatLab (RPi 4 + Docker + Tailscale + IA + LoRa + Hort Osona)
> Document de referència per continuar treballant des de qualsevol dispositiu o sessió.
>
> **Última revisió documental:** 2026-08-04
>
> **Tall de dades operatives:** 2026-07-17. Cal verificar l'estat real dels serveis abans d'executar canvis.

---

## 1. Què és el projecte

**BernatLab** és un servidor personal basat en una Raspberry Pi 4 amb Debian 13 Lite, Docker, Docker Compose, Tailscale, Portainer, Uptime Kuma i Homepage. L'objectiu és convertir-lo en el centre dels projectes de l'usuari: Hort Osona, sensors LoRa, meteorologia, IA, música, automatitzacions i desenvolupament web.

> **Nota:** Aquest PROJECT_STATE cobreix **només el BernatLab**. Per a una vista global de tots els projectes de l'usuari, veure `PROJECT_STATE-GLOBAL.md` (properament).

**Hardware/programari/recursos principals:**

| Concepte | Valor |
|---|---|
| Maquinari | RPi 4 Model B, 4 GB RAM, microSD 32GB |
| SO | Debian GNU/Linux 13 Trixie Lite (arm64) |
| Hostname | hortosona |
| Usuari | bernat |
| IP Tailscale | `[VALOR_LOCAL]` — consultar Tailscale o `_local/`; no publicar adreces reals |
| Contenidors actius | Portainer (9443), Uptime Kuma (3001), Homepage (3000), Ollama |
| SIM de dades | 150 GB/mes al router 4G de l'hort |
| ESP32 | 1 unitat a 15 metres de la RPi |

---

## 2. Les parts principals del projecte

| # | Nom | Estat | Cost | Notes |
|---|---|---|---|---|
| 1 | **Llibre del BernatLab** | En curs | 0 EUR | 7 mòduls, 70 capítols, 584 pàgines (PDF + DOCX) |
| 2 | **Curs pràctic** | En curs | 0 EUR | 77 capítols, 1.087 preguntes |
| 3 | **Hort Osona (PWA)** | En curs | 0 EUR | 8 plans mensuals publicats, web PWA |
| 4 | **Glossari complet** | Decidit | 0 EUR | 321 termes, ~70 KB |
| 5 | **Guia "El meu primer dia"** | Decidit | 0 EUR | Pas a pas, 12 KB |
| 6 | **Arquitectura visual (3 SVGs)** | Decidit | 0 EUR | Xarxa, IoT, curs |
| 7 | **Router 4G hort** | Pendent | ~50-100 EUR | Per muntar a l'hort amb SIM |
| 8 | **ESP32 + sensors** | Pendent | ~30-40 EUR | 1 placa, sensors DHT22, etc. |
| 9 | **MQTT (Mosquitto)** | Pendent | 0 EUR | Per rebre dades de l'ESP32 |
| 10 | **InfluxDB + Grafana** | Pendent | 0 EUR | Guardar i visualitzar dades |
| 11 | **Scripts `bin/`** | Decidit | 0 EUR | 7 scripts (PowerShell, bash, accés directe) |
| 12 | **Publicacions externes** | Pendent | 0 EUR | Infojardín, Ruralcat, L'agrobotiga, YouTube |

Estats possibles: **Decidit, Planificat, En curs, Pendent, Descartat**

---

## 3. Integracions amb altres eines/serveis

- **GitHub** — Repos BernatLab i Hort Osona (públics)
- **GitHub Pages** — Publicació de BernatLab i Hort Osona
- **Tailscale** — VPN mesh per accedir a la RPi des de qualsevol lloc
- **Telegram** — Bot de Hort Osona (amb RAG + Ollama)
- **Ollama** — IA local amb models `gemma3:1b` i `phi3:mini`
- **Portainer** — Gestió de contenidors
- **Uptime Kuma** — Monitorització de serveis
- **Homepage** — Panell d'inici personalitzat
- **ESP32** — Sensors IoT (WiFi, previst MQTT)
- **Router 4G** — Internet propi a l'hort (pròximament)

---

## 4. Documentació generada

- **book/** (carpeta principal)
  - **book/llibre/** — 7 mòduls del llibre (PDF + DOCX)
  - **book/curs/** — 77 capítols del curs
  - **book/glossari.md** (68 KB) — Glossari amb 321 termes
  - **book/primer-dia-rpi.md** (12 KB) — Guia pas a pas
  - **book/arquitectura/** — 3 SVGs + índex
  - **book/handoff-sessio-2026-07-17.md** (6 KB) — Handoff d'aquesta sessió
  - **book/wiki/** — Wiki del llibre
  - **book/cheatsheet.html** — Chuleta de comandes
- **projects/hort-osona/** — Web PWA
  - **plans-mensuals/** — 8 plans mensuals (juny-desembre 2026)
  - **docs/plans-mensuals/** — Versions HTML dels plans
- **posts/** — Esborranys de publicacions externes
- **bin/** — 7 scripts (PowerShell, bash, accés directe a l'escriptori)

---

## 5. Decisions preses (amb raonament)

- **Tailscale per accedir a la RPi des de fora**: No cal obrir ports al router, és més segur.
- **WiFi (no LoRa) per ESP32 a 15 m**: L'ESP32 ja el té integrat, LoRa seria innecessari a aquesta distància.
- **RPi al WiFi del router 4G (no a xarxa de casa)**: Té internet propi a l'hort, no depèn de la cobertura de casa.
- **Català com a llengua per defecte**: L'usuari és català, tota la documentació està en català.
- **Markdown + Git per versionar**: Permet fer canvis amb ordre i tornar enrere si cal.
- **GitHub Pages per publicar**: Gratuït, fàcil d'actualitzar amb `git push`.
- **Patró de capítols estàndard**: resum + quiz + exercici + respostes + HTML per consistència.
- **Scripts a `bin/`**: Eines útils per accedir ràpidament al projecte des de qualsevol PC.
- **150 GB SIM de dades**: Suficient per a sensors i pujada de dades, però cal vigilar el consum.

---

## 6. Pendents immediats (pròxims passos)

### A. Muntar el router 4G a l'hort (1-2 h)
1. Posar el router a prop de la RPi amb bona cobertura
2. Inserir la SIM
3. Encendre'l
4. Configurar nom de WiFi i contrasenya
5. Anotar-los per connectar la RPi

### B. Connectar la RPi al WiFi del router 4G (30 min)
1. Des del Mac de casa per SSH (si tens Ethernet temporal)
2. O amb monitor + teclat a la RPi
3. `sudo nmcli device wifi connect "NOM" password "CONTRASENYA"`
4. Verificar: `ping 8.8.8.8` i `tailscale status`

### C. Instal·lar MQTT, InfluxDB i Grafana a la RPi (2 h)
1. `docker run -d --name mosquitto -p 1883:1883 eclipse-mosquitto`
2. Instal·lar InfluxDB amb Docker Compose
3. Instal·lar Grafana amb Docker Compose
4. Configurar Telegraf per recollir dades

### D. Programar l'ESP32 amb sensor DHT22 (1-2 h)
1. Instal·lar Arduino IDE o PlatformIO al Mac
2. Escriure codi per llegir DHT22 i enviar via MQTT
3. Pujar el codi a l'ESP32
4. Connectar l'ESP32 al WiFi del router 4G
5. Verificar que envia dades

### E. Documentar tot en un runbook (1 h)
1. Runbook del router 4G
2. Runbook de l'ESP32
3. Runbook de MQTT/InfluxDB/Grafana

### F. Pujar els canvis del cap de setmana (30 min)
1. Al Mac: `git status` per veure què tens
2. Si tens canvis, fer commit i push
3. Si tens canvis sense commit, integrar-los

---

## 7. Restriccions i regles del projecte

- **No usar apòstrofs tipogràfics ni cometes intel·ligents** als fitxers — usar ASCII (`'`, `"`, `-`).
- **Cap credencial ni token** al repo ni al context — tot `[REDACTED]`.
- **Llengua catalana** per defecte.
- **Validar amb execució real**, no promeses teòriques.
- **Cap "Paraules clau" al final** dels capítols.
- **Tots els fitxers UTF-8 vàlids**.
- **Fer servir fitxers petits, nets, editables** (KISS).
- **Sempre provar abans de reportar "fet"** — el que compta és el resultat.
- **No usar `cd` per canviar de directori** — usar `project_switch`.
- **Scripts llargs via `write_file`**, no pas `execute_code` (que pot bloquejar-se).

---

## 8. Glossari

- **BernatLab:** El projecte global (servidor + llibre + curs + hort).
- **Hort Osona:** El projecte específic de l'hort (PWA + plans mensuals).
- **hortosona:** Hostname de la RPi 4 a l'hort.
- **Tailscale:** VPN mesh que permet accedir a la RPi sense obrir ports.
- **ESP32:** Microcontrolador amb WiFi integrat, ideal per IoT.
- **MQTT:** Protocol lleuger per a missatgeria IoT.
- **DHT22:** Sensor de temperatura i humitat d'aire.
- **Ollama:** Eina per executar LLMs localment.
- **RAG:** Retrieval Augmented Generation (cerca + generació).
- **4G:** Xarxa mòbil de quarta generació (LTE).
- **SIM:** Targeta d'identitat de subscriptor (mòbil).
- **IP Tailscale:** Adreça única per accedir a la RPi via Tailscale.

---

## 9. Preferències de l'usuari

- **Llengua:** Català per defecte (barreja castellà amb naturalitat).
- **Estil de treball:** Lots petits validats, tests via terminal amb .venv, no reportar "fet" sense proves.
- **Prioritat:** Màquines útils, no decoratives.
- **Estil de comunicació:** Directe, sense elogis buits.
- **Senyals de tancament:** "anem per un altre tema", "ja està" → wrap-up deliverables.
- **Patrons:** Iterar sobre artefactes, validar amb execució real, recordar errors.
- **Interessos:** RPi, Docker, Tailscale, IA local, LoRa, horticultura, IoT.
- **No:** Mai demanar/acceptar credencials. Mai inventar dades.

---

## 10. Com reprendre aquesta sessió

Si vols continuar des d'un altre dispositiu o sessió:

1. **Llegeix `book/handoff-sessio-2026-07-17.md`** — té tot el context de la sessió del 2026-07-17.
2. **Llegeix `PROJECT_STATE.md`** (aquest fitxer) — té l'estat actual.
3. **Mira els últims commits** a GitHub: `git log --oneline -10`
4. **Comprova el working tree** per veure canvis pendents: `git status`
5. **Continua des de la secció 6 (Pendents immediats)** d'aquest document.

Si estàs a la feina (Windows):
- Obre Hermes i enganxa el contingut de `handoff-sessio-2026-07-17.md` com a context.
- Recorda que a la feina no pots accedir a la RPi directament.

Si estàs a casa (Mac):
- Obre el Terminal del Mac.
- Vés al directori del repo: `cd ~/bernatlab` (o on sigui que el tinguis).
- Continua treballant directament amb `git` i SSH a la RPi.

---

## 11. Projectes relacionats

L'usuari té **altres projectes** que conviuen amb el BernatLab. Tots estan publicats a GitHub i es poden accedir des de qualsevol node del tailnet.

### Bernat CyberLab AI (laboratori de ciberseguretat)

- **Repositori:** https://github.com/BernatMora/cyberlab-ai
- **Web:** https://bernatmora.github.io/cyberlab-ai/
- **Descripció:** Llibre viu sobre ciberseguretat amb laboratori pràctic muntat al Kali. Documenta com construir i usar un laboratori personal modular de ciberseguretat.
- **Estat:** En curs actiu (laboratori real muntat, 38+ capítols preparats).
- **Contingut:**
  - Llibre estructurat amb codis permanents (`CAP-XX-YY`, `EX-XX-YY`, `LAB-XX-YY`, `ADR-XXX`, `TRB-XX-YY`, `CHK-XX-YY`, `ANN-XX`).
  - Plantilles per a cada tipus de document.
  - 3 contenidors vulnerables (DVWA, Juice Shop, Metasploitable) a la xarxa interna aïllada `10.10.30.x`.
  - Tallafoc automatitzat (`isolate-lab.sh` + `isolate-lab.service`).
  - HP Z1 G9 planificat per a màquines virtuals natives.
- **Llicència:** CC BY-SA 4.0 (text) + MIT (codi).
- **Diferència respecte al BernatLab:**
  - CyberLab = ciberseguretat (atac i defensa en entorn aïllat).
  - BernatLab = servidor en producció (RPi + serveis reals).
- **Relació:** No comparteixen infraestructura (estan aïllats per seguretat), però comparteixen metodologia (PROJECT_STATE, commits petits, documentació pedagògica en català).

### Altres projectes (mencionats a sessions anteriors)

- **Hort Osona** — PWA amb plans mensuals de l'hort (ja cobert a la secció 4 d'aquest PROJECT_STATE).

---

## Versió

| Data | Canvis |
|---|---|
| 2026-08-04 | Revisió: anonimització de xarxa, separació entre estat documental i operatiu, i desplegament IoT segur amb Compose. |
| 2026-07-17 | Creació del PROJECT_STATE per primera vegada. Inclou: llibre + curs (77 cap., 1087 preguntes) + Hort Osona (8 plans mensuals) + glossari + guia + arquitectura + router 4G pendent + ESP32 pendent. |
| 2026-08-07 | Afegida secció "Projectes relacionats" amb el CyberLab AI com a projecte germà. |

---

**Plantilla original:** `book/PROJECT-STATE-TEMPLATE.md`
**Aquest PROJECT_STATE:** `PROJECT_STATE.md`
