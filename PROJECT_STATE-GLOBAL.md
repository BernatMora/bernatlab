# PROJECT STATE GLOBAL

> Vista global de TOTS els projectes de l'usuari. Cobreix **BernatLab**, **Hort Osona** i **Bernat CyberLab AI**.
>
> Per a l'estat detallat de cada projecte, veure els seus respectius `PROJECT_STATE.md`.
>
> **Ultima revisio:** 2026-XX-XX (revisio post-sessio DeepSeek)

---

## 1. Els 3 projectes

L'usuari te **3 projectes principals** publicats a GitHub. Tots tres comparteixen una metodologia comuna (PROJECT_STATE, commits petits, documentacio pedagogica en catala), pero tenen objectius i abast ben diferents.

| Projecte | Foc | Web | Repo | Estat |
|---|---|---|---|---|
| **BernatLab** | Servidor personal + curs + llibre + IoT | https://bernatmora.github.io/bernatlab/ | https://github.com/BernatMora/bernatlab | En curs (IoT actiu) |
| **Hort Osona** | PWA + plans mensuals hort | https://bernatmora.github.io/hort-osona/ | https://github.com/BernatMora/hort-osona | En curs |
| **Bernat CyberLab AI** | Llibre de ciberseguretat + lab practic | https://bernatmora.github.io/cyberlab-ai/ | https://github.com/BernatMora/cyberlab-ai | **En pausa** |

### Arquitectura conceptual

```
                         BERNATLAB (marc general)
                         =========================
                               |
                +--------------+--------------+
                |              |              |
            HORT OSONA    CYBERLAB AI      [futurs]
            (aplicacio    (aplicacio
             especifica)   especifica)
```

- **BernatLab** = el marc general (el servidor, el curs, el llibre, el sistema IoT).
- **Hort Osona** = una aplicacio especifica (PWA + plans mensuals).
- **CyberLab AI** = una altra aplicacio especifica (lab de ciberseguretat).
- Tots tres **conviuen** sota el mateix ecosistema de l'usuari.

---

## 2. Relacions entre projectes

### Que comparteixen

- **Metodologia comuna:** PROJECT_STATE, commits petits amb missatges clars, documentacio en catala, validacio amb execucio real.
- **Eines comunes:** Git + GitHub + GitHub Pages + Tailscale.
- **Llengua:** Catala per defecte a tots.
- **Llicencia doble:** MIT (codi) + CC BY-SA 4.0 (text).
- **Politica de secrets:** Cap credencial al repo ni al context.

### Que NO comparteixen

| | BernatLab | Hort Osona | CyberLab AI |
|---|---|---|---|
| **Infraestructura** | RPi 4 + Docker | Submodule de BernatLab | Kali separat (aillat) |
| **Xarxa** | Tailscale + 4G | Heretada de BernatLab | 10.10.30.x (aillada) |
| **Produccio** | Si (servidor actiu) | Si (PWA publica) | No (lab de proves) |
| **Connexionat a Internet** | Si (a traves del router 4G) | Si (nomes la web publica) | NO (aillat per seguretat) |

### Relacio Hort Osona ↔ BernatLab

- Hort Osona es un **submodule** dins de BernatLab (`projects/hort-osona/`).
- Comparteix infraestructura (RPi), pero te el seu propi repo per publicar independentment.
- La **portada** d'Hort Osona s'actualitza cada mes amb el `set-current-month.py`.
- El **sistema IoT Hort Osona** es un subprojecte dins de BernatLab (`projects/hort-osona-iot/`), amb LoRa + Supabase + Alexa + Telegram + RAG.

### Relacio CyberLab AI ↔ BernatLab

- Son **projectes independents** pero complementaris.
- CyberLab NO comparteix infraestructura amb BernatLab (per seguretat).
- Comparteixen nomes **metodologia** (PROJECT_STATE, commits, catala).
- CyberLab s'executa al Kali (un altre node del tailnet), no a la RPi.
- **Estat actual:** En pausa — el hardware (HP Z1 G9) encara no esta preparat.

### Relacio CyberLab ↔ Hort Osona

- Cap relacio directa. Son dominis completament diferents (ciberseguretat vs horticultura).

---

## 3. Dispositius del tailnet (Tailscale)

Tots els dispositius de l'usuari estan al **mateix compte de Tailscale**, formant un tailnet privat segur.

| Node | Sistema | Usuari | Us principal |
|---|---|---|---|
| `windows` | Windows | bernat | Feina |
| `mac` | macOS | bernat | Casa |
| `iphone` | iOS | — | Mobil |
| `hortosona` | Raspberry Pi | bernat | Servidor hort + BernatLab |
| `hort` | Windows | hort-osona | PC hort (treball local) |
| `kali` | Kali Linux | bernat | CyberLab + proves seguretat |

### Comandes utils des de qualsevol node

```bash
# Veure tots els nodes actius
tailscale status

# Accedir a un node concret
ssh bernat@hortosona       # RPi
ssh hort-osona@hort        # PC Windows de l'hort
ssh bernat@kali            # Kali (CyberLab)

# Compartir fitxers entre nodes
scp fitxer.txt bernat@hortosona:/tmp/
```

---

## 4. Hardware de l'usuari

| Dispositiu | Especificacions | On es | Us |
|---|---|---|---|
| RPi 4 Model B | 4 GB RAM, microSD 32GB | Hort/Casa | Servidor BernatLab |
| TTGO LoRa32 868 MHz | ESP32 + LoRa + OLED | Hort | Node emissor IoT |
| BME280 + sensor sol + 18650 + solar | Sensor pack | Hort | Lectura T/H/P/llum |
| HAT Waveshare SX1262 | Modem LoRa per RPi | Casa | Receptor del node |
| MyCloudHome | NAS local | Xarxa casa | Hosting portal Hort Osona |
| HP Z1 G9 | 32 GB RAM | Casa | CyberLab (planificat) |
| ESP32 (basic) | WiFi integrat | Hort | Proves generals (anterior) |
| Router 4G | MicroSIM 150 GB | Hort | Internet hort |
| iPhone | — | Mobil | Tailscale |
| MacBook Air | — | Casa | Desenvolupament |
| Windows PC | — | Feina | Desenvolupament + scripts |
| Windows PC | — | Hort | Treball local hort |
| Kali Laptop | — | Hort/Casa | CyberLab + pen-testing |

---

## 5. Xarxes i connectivitat

### Xarxes conegudes

- **Tailscale (tailnet):** Xarxa privada entre tots els dispositius.
- **Xarxa de casa (goufone.com):** Per a la RPi (quan es a casa).
- **Xarxa 4G hort:** Per a la RPi quan esta a l'hort (proximament).
- **Xarxa aillada CyberLab (10.10.30.x):** Per als contenidors vulnerables.
- **MyCloudHome (192.168.x.x):** NAS local amb portal public.

### Connexions critiques

- **RPi ↔ Tailscale:** La RPi ha d'estar sempre al tailnet (canvia la IP quan canvia de xarxa).
- **RPi ↔ Router 4G:** Quan el router estigui muntat a l'hort.
- **Node LoRa (hort) ↔ RPi (casa):** Radio LoRa 868 MHz, distancia ~400m.
- **Kali ↔ Xarxa 10.10.30.x:** Per accedir als contenidors vulnerables.
- **RPi ↔ MyCloudHome:** CIFS mount (guest), per allotjar portal public.

---

## 6. Repos i publicacions

### Repos actius

| Repo | URL | Proposit |
|---|---|---|
| bernatlab | https://github.com/BernatMora/bernatlab | Llibre + curs + scripts + BernatLab + IoT |
| hort-osona | https://github.com/BernatMora/hort-osona | PWA Hort Osona (submodule) |
| cyberlab-ai | https://github.com/BernatMora/cyberlab-ai | Llibre viu ciberseguretat |

### Webs publiques (GitHub Pages)

- https://bernatmora.github.io/bernatlab/ — BernatLab + curs + llibre + recursos
- https://bernatmora.github.io/hort-osona/ — PWA Hort Osona
- https://bernatmora.github.io/cyberlab-ai/ — Llibre ciberseguretat

### Recursos destacats

- **BernatLab:** glossari, guia primer dia RPi, arquitectura (3 SVGs), xuleta comandes, PDF resum, projecte IoT complet (LoRa + Supabase).
- **Hort Osona:** 8 plans mensuals (juny-desembre 2026), PWA responsive.
- **CyberLab AI:** llibre viu amb 38+ capitols, plantilles, lab practic.

---

## 7. Estadistiques globals (2026-XX-XX)

### BernatLab

- **Llibre:** 7 moduls, 70 capitols, 584 pagines (PDF + DOCX)
- **Curs:** 77 capitols, 1.087 preguntes, 308 .md, 77 .html
- **Hort Osona (integrat):** 8 plans mensuals publicats
- **Hort Osona IoT:** 49 fitxers (LoRa + Supabase + Alexa + Telegram + RAG + MyCloudHome)
- **Glossari:** 321 termes
- **Recursos:** glossari, guia, arquitectura, xuleta, PDF resum
- **Scripts:** 7 a `bin/` (PowerShell, bash, acces directe)

### Hort Osona

- **Plans mensuals:** 8 (juny-desembre 2026)
- **Web PWA:** responsive, amb `set-current-month.py` per actualitzar el pla del mes
- **Temes:** regs, plagues, conserves, fruiters, hivernacles

### Bernat CyberLab AI

- **Llibre:** 38+ capitols preparats (esquelet)
- **Bloc 0:** publicat (proleg, filosofia, estructura)
- **Lab real:** 3 contenidors vulnerables (DVWA, Juice Shop, Metasploitable) — **en pausa**
- **Xarxa:** 10.10.30.x (aillada amb tallafoc)
- **HP Z1 G9:** planificat per a maquines virtuals natives

### Total

- **3 repos** actius a GitHub
- **3 webs** publiques a GitHub Pages
- **6 nodes** al tailnet de Tailscale
- **~250 MB** de documentacio total

---

## 8. Pendents globals

### Curt termini (1-2 setmanes)

- [ ] Auditar l'estat real de la RPi via SSH
- [ ] Diagnosticar perque el hardware IoT no funciona
- [ ] Crear compte Supabase i executar `supabase_schema.sql`
- [ ] Provar el flux complet IoT (node -> LoRa -> Supabase -> Ollama -> Web)
- [ ] Documentar el primer runbook reeixit del IoT

### Mig termini (1-2 mesos)

- [ ] Publicar el primer video/tutorial del BernatLab
- [ ] Finalitzar M5-M8 del curs (ultims detalls)
- [ ] Muntar l'HP Z1 G9 a casa
- [ ] Reactivar el CyberLab (primer laboratori web DVWA / Juice Shop)

### Llarg termini (3-6 mesos)

- [ ] Publicar un article a Infojardin
- [ ] Publicar un article a L'agrobotiga
- [ ] Publicar un video a YouTube
- [ ] Afegir cameres a l'hort
- [ ] Afegir reg automatic
- [ ] Activar Alexa skill en produccio

---

## 9. Decisions globals (amb raonament)

### Infraestructura

- **Tailscale per accedir a la RPi des de fora:** No cal obrir ports al router, es mes segur.
- **LoRa 868 MHz per al node IoT a l'hort:** Distancia ~400m entre hort i casa; WiFi no arriba; LoRa es la solucio mes eficient.
- **Supabase + Realtime per a dades de sensors:** Alternativa open source a Firebase, amb schema SQL propi.
- **Ollama per a IA local:** Consells cada 6h generats amb el model local, sense enviar dades al nuvol.
- **Catala com a llengua per defecte:** L'usuari es catala, tota la documentacio esta en catala.
- **Markdown + Git per versionar:** Permet fer canvis amb ordre i tornar enrera si cal.
- **GitHub Pages per publicar:** Gratuit, facil d'actualitzar amb `git push`.
- **Patrons estandard:** resum + quiz + exercici + respostes + HTML per consistencia.
- **150 GB SIM de dades:** Suficient per a sensors i pujada de dades, pero cal vigilar el consum.
- **Anonimitzar IPs abans de commit:** 192.168.x.x i 100.x.x.x substituits per placeholders.

### Seguretat

- **Cap credencial ni token al repo ni al context** — tot `[REDACTED]`.
- **Aillament del CyberLab:** Els contenidors vulnerables NO poden accedir a la resta de la xarxa.
- **SSH amb claus** (no pas contrasenyes) — pendent de configurar a tot arreu.

### Desenvolupament

- **Lots petits validats:** Iterar sobre artefactes petits amb proves reals.
- **Scripts a `bin/`:** Eines utils per accedir rapidament al projecte des de qualsevol PC.
- **RPi al WiFi del router 4G (no a xarxa de casa):** Internet propi a l'hort, no depen de la cobertura de casa.

---

## 10. Restriccions globals

- **No usar apostrofs tipografics ni cometes intelligents** als fitxers — usar ASCII (`'`, `"`, `-`).
- **Cap credencial ni token** al repo ni al context — tot `[REDACTED]`.
- **Llengua catalana** per defecte.
- **Validar amb execucio real**, no promeses teoriques.
- **Cap "Paraules clau" al final** dels capitols.
- **Tots els fitxers UTF-8 valids**.
- **Fer servir fitxers petits, nets, editables** (KISS).
- **Sempre provar abans de reportar "fet"** — el que compta es el resultat.
- **Mai practicar ciberseguretat des de l'equip de la feina** (risc laboral).
- **Anonimitzar IPs (192.168.x.x i 100.x.x.x) abans de commit.**

---

## 11. Notes operatives globals

### Estalvi de dades (eSIM)

**Desactivat actualment** per estalviar dades:
- Bot Telegram al bernat-pc (`hort-osona-telegram.service`)
- Actualitzacions automatiques (`apt-daily.timer`, `apt-daily-upgrade.timer`) a RPi i bernat-pc

**Tailscale** optimitzat a la RPi: `--accept-dns=false --accept-routes=false --netfilter-mode=off`

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

- **RPi (hortosona)**: gateway IoT, MQTT, InfluxDB, Grafana, Nextcloud, MariaDB.
- **bernat-pc**: serveis d'IA (Ollama), bot Telegram, scripts de desenvolupament.
- **PC feina (bernat)**: client de desenvolupament, conecta via Tailscale.

---

## 12. Glossari global

- **BernatLab:** El marc general del projecte (servidor + llibre + curs + hort + IoT).
- **Hort Osona:** PWA + plans mensuals de l'hort.
- **Hort Osona IoT:** Sistema de sensors LoRa + Supabase + Alexa + Telegram + Ollama.
- **CyberLab AI:** Llibre viu + laboratori de ciberseguretat al Kali.
- **Bernat Mora:** L'usuari (desenvolupador + pages + investigador).
- **Tailscale:** VPN mesh per accedir a dispositius sense obrir ports.
- **tailnet:** Xarxa privada de Tailscale.
- **ESP32:** Microcontrolador amb WiFi integrat per a IoT.
- **TTGO LoRa32:** Placa ESP32 amb LoRa 868 MHz integrat.
- **BME280:** Sensor combinat de T, H i P atmosferica.
- **HAT SX1262:** Modem LoRa per a Raspberry Pi (Waveshare).
- **Supabase:** Backend Postgres + Realtime + Auth (alternativa a Firebase).
- **Ollama:** Eina per executar LLMs localment.
- **MyCloudHome:** NAS local de WD per a allotjament privat.
- **RAG:** Retrieval Augmented Generation (cerca + generacio).
- **DVWA:** Damn Vulnerable Web Application (lab ciberseguretat).
- **Juice Shop:** Botiga vulnerable per practicar web hacking.
- **Metasploitable:** Linux vulnerable per practicar atacs.
- **HP Z1 G9:** PC potent (32 GB RAM) per a maquines virtuals.
- **4G:** Xarxa mobil de quarta generacio.
- **CGNAT:** Carrier-Grade NAT (impedeix port forwarding directe).
- **Wake-on-LAN:** Tecnologia per despertar PCs remotament.
- **Alexa Skill:** App de veu per a Amazon Alexa.

---

## 13. Com reprendre una sessio (qualsevol projecte)

Si vols continuar treballant en qualsevol dels 3 projectes des d'un altre dispositiu:

1. **Identifica quin projecte** vols continuar (BernatLab, Hort Osona o CyberLab).
2. **Llegeix el `PROJECT_STATE.md`** del projecte concret.
3. **O llegeix aquest `PROJECT_STATE-GLOBAL.md`** per una vista global.
4. **Mira els ultims commits** a GitHub: `git log --oneline -10`.
5. **Comprova el working tree** per veure canvis pendents: `git status`.
6. **Continua des dels pendents** de la seccio 8 d'aquest document (globals) o dels especifics del projecte.

### Si estas a la feina (Windows)

- Obre el terminal i connecta't per SSH a la RPi via Tailscale.
- Si no tens Tailscale actiu, treballa nomes amb documentacio.

### Si estas a casa (Mac)

- Obre el Terminal del Mac.
- Ves al directori del repo: `cd ~/bernatlab` (o `~/hort-osona`, `~/cyberlab-ai`).
- Continua treballant directament amb `git` i SSH a la RPi.

### Si estas a l'hort (PC hort)

- Connecta't per SSH a la RPi: `ssh bernat@hortosona`.
- O treballa directament al PC hort (Windows: `hort-osona@hort`).
- Si tens el router 4G muntat, pots accedir a internet independentment de casa.

---

## Versio

| Data | Canvis |
|---|---|
| 2026-08-07 | Creacio del PROJECT_STATE-GLOBAL.md amb vista global dels 3 projectes (BernatLab, Hort Osona, CyberLab AI). |
| 2026-XX-XX | **Refresc post-sessio DeepSeek**: integrat el projecte Hort Osona IoT (LoRa + Supabase + Alexa + Telegram + RAG), reconegut que CyberLab esta en pausa, nova seccio de hardware amb node LoRa + HAT SX1262 + MyCloudHome, decisions actualitzades amb anonimitzacio d'IPs i Supabase. |

---

**Aquest PROJECT_STATE-GLOBAL:** `PROJECT_STATE-GLOBAL.md`
**PROJECT_STATE per projecte:** `bernatlab/PROJECT_STATE.md`, `hort-osona/PROJECT_STATE.md` (proximament), `cyberlab-ai/PROJECT_STATE.md` (proximament)
**Plantilla original:** `bernatlab/book/PROJECT-STATE-TEMPLATE.md`
