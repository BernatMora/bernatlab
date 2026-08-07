# PROJECT STATE GLOBAL

> Vista global de TOTS els projectes de l'usuari. Cobreix **BernatLab**, **Hort Osona** i **Bernat CyberLab AI**.
>
> Per a l'estat detallat de cada projecte, veure els seus respectius `PROJECT_STATE.md`.
>
> **Última revisió:** 2026-08-07

---

## 1. Els 3 projectes

L'usuari té **3 projectes principals** publicats a GitHub. Tots tres comparteixen una metodologia comuna (PROJECT_STATE, commits petits, documentació pedagògica en català), però tenen objectius i abast ben diferents.

| Projecte | Foc | Web | Repo | Estat |
|---|---|---|---|---|
| **BernatLab** | Servidor personal + curs + llibre + IoT | https://bernatmora.github.io/bernatlab/ | https://github.com/BernatMora/bernatlab | En curs |
| **Hort Osona** | PWA + plans mensuals hort | https://bernatmora.github.io/hort-osona/ | https://github.com/BernatMora/hort-osona | En curs |
| **Bernat CyberLab AI** | Llibre de ciberseguretat + lab pràctic | https://bernatmora.github.io/cyberlab-ai/ | https://github.com/BernatMora/cyberlab-ai | En curs |

### Arquitectura conceptual

```
                        BERNATLAB (marc general)
                        =========================
                              |
                +-------------+-------------+
                |             |             |
            HORT OSONA   CYBERLAB AI    [futurs]
            (aplicacio  (aplicacio
             especifica)  especifica)
```

- **BernatLab** = el marc general (el servidor, el curs, el llibre).
- **Hort Osona** = una aplicació específica (PWA + plans mensuals).
- **CyberLab AI** = una altra aplicació específica (lab de ciberseguretat).
- Tots tres **conviuen** sota el mateix ecosistema de l'usuari.

---

## 2. Relacions entre projectes

### Què comparteixen

- **Metodologia comuna:** PROJECT_STATE, commits petits amb missatges clars, documentació en català, validació amb execució real.
- **Eines comunes:** Git + GitHub + GitHub Pages + Tailscale.
- **Llengua:** Català per defecte a tots.
- **Llicència doble:** MIT (codi) + CC BY-SA 4.0 (text).
- **Política de secrets:** Cap credencial al repo ni al context.

### Què NO comparteixen

| | BernatLab | Hort Osona | CyberLab AI |
|---|---|---|---|
| **Infraestructura** | RPi 4 + Docker | Submodule de BernatLab | Kali separat (aïllat) |
| **Xarxa** | Tailscale + 4G | Heretada de BernatLab | 10.10.30.x (aïllada) |
| **Producció** | Sí (servidor actiu) | Sí (PWA pública) | No (lab de proves) |
| **Connexionat a Internet** | Sí (a través del router 4G) | Sí (només la web pública) | NO (aïllat per seguretat) |

### Relació Hort Osona ↔ BernatLab

- Hort Osona és un **submodule** dins de BernatLab (`projects/hort-osona/`).
- Comparteix infraestructura (RPi), però té el seu propi repo per publicar independentment.
- La **portada** d'Hort Osona s'actualitza cada mes amb el `set-current-month.py`.

### Relació CyberLab AI ↔ BernatLab

- Són **projectes independents** però complementaris.
- CyberLab NO comparteix infraestructura amb BernatLab (per seguretat).
- Comparteixen només **metodologia** (PROJECT_STATE, commits, català).
- CyberLab s'executa al Kali (un altre node del tailnet), no a la RPi.

### Relació CyberLab ↔ Hort Osona

- Cap relació directa. Són dominis completament diferents (ciberseguretat vs horticultura).

---

## 3. Dispositius del tailnet (Tailscale)

Tots els dispositius de l'usuari estan al **mateix compte de Tailscale**, formant un tailnet privat segur.

| Node | Sistema | Usuari | Ús principal |
|---|---|---|---|
| `windows` | Windows | bernat | Feina |
| `mac` | macOS | bernat | Casa |
| `iphone` | iOS | — | Mòbil |
| `hortosona` | Raspberry Pi | bernat | Servidor hort + BernatLab |
| `hort` | Windows | hort-osona | PC hort (treball local) |
| `kali` | Kali Linux | bernat | CyberLab + proves seguretat |

### Comandes útils des de qualsevol node

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

| Dispositiu | Especificacions | On és | Ús |
|---|---|---|---|
| RPi 4 Model B | 4 GB RAM, microSD 32GB | Hort | Servidor BernatLab |
| HP Z1 G9 | 32 GB RAM | Casa | CyberLab (planificat) |
| ESP32 | WiFi integrat | Hort | Sensors IoT (futur) |
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
- **Xarxa de casa (goufone.com):** Per a la RPi (quan és a casa).
- **Xarxa 4G hort:** Per a la RPi quan està a l'hort (pròximament).
- **Xarxa aïllada CyberLab (10.10.30.x):** Per als contenidors vulnerables.

### Connexions crítiques

- **RPi ↔ Tailscale:** La RPi ha d'estar sempre al tailnet (canvia la IP quan canvia de xarxa).
- **RPi ↔ Router 4G:** Quan el router estigui muntat a l'hort.
- **Kali ↔ Xarxa 10.10.30.x:** Per accedir als contenidors vulnerables.
- **ESP32 ↔ Router 4G:** Quan l'ESP32 estigui programat.

---

## 6. Repos i publicacions

### Repos actius

| Repo | URL | Propòsit |
|---|---|---|
| bernatlab | https://github.com/BernatMora/bernatlab | Llibre + curs + scripts + BernatLab |
| hort-osona | https://github.com/BernatMora/hort-osona | PWA Hort Osona (submodule) |
| cyberlab-ai | https://github.com/BernatMora/cyberlab-ai | Llibre viu ciberseguretat |

### Webs públiques (GitHub Pages)

- https://bernatmora.github.io/bernatlab/ — BernatLab + curs + llibre + recursos
- https://bernatmora.github.io/hort-osona/ — PWA Hort Osona
- https://bernatmora.github.io/cyberlab-ai/ — Llibre ciberseguretat

### Recursos destacats

- **BernatLab:** glossari, guia primer dia RPi, arquitectura (3 SVGs), xuleta comandes, PDF resum.
- **Hort Osona:** 8 plans mensuals (juny-desembre 2026), PWA responsive.
- **CyberLab AI:** llibre viu amb 38+ capítols, plantilles, lab pràctic.

---

## 7. Estadístiques globals (2026-08-07)

### BernatLab

- **Llibre:** 7 mòduls, 70 capítols, 584 pàgines (PDF + DOCX)
- **Curs:** 77 capítols, 1.087 preguntes, 308 .md, 77 .html
- **Hort Osona (integrat):** 8 plans mensuals publicats
- **Glossari:** 321 termes
- **Recursos:** glossari, guia, arquitectura, xuleta, PDF resum
- **Scripts:** 7 a `bin/` (PowerShell, bash, accés directe)

### Hort Osona

- **Plans mensuals:** 8 (juny-desembre 2026)
- **Web PWA:** responsive, amb `set-current-month.py` per actualitzar el pla del mes
- **Temes:** regs, plagues, conserves, fruiters, hivernacles

### Bernat CyberLab AI

- **Llibre:** 38+ capítols preparats (esquelet)
- **Bloc 0:** publicat (pròleg, filosofia, estructura)
- **Lab real:** 3 contenidors vulnerables (DVWA, Juice Shop, Metasploitable)
- **Xarxa:** 10.10.30.x (aïllada amb tallafoc)
- **HP Z1 G9:** planificat per a màquines virtuals natives

### Total

- **3 repos** actius a GitHub
- **3 webs** públiques a GitHub Pages
- **6 nodes** al tailnet de Tailscale
- **~250 MB** de documentació total

---

## 8. Pendents globals

### Curt termini (1-2 setmanes)

- [ ] Muntar el router 4G a l'hort
- [ ] Connectar la RPi al WiFi del router
- [ ] Verificar Tailscale i Tailscale IP nova
- [ ] Programar l'ESP32 amb sensor DHT22
- [ ] Instal·lar MQTT + InfluxDB + Grafana a la RPi
- [ ] Muntar el primer sensor real a l'hort

### Mitjà termini (1-2 mesos)

- [ ] Publicar el primer vídeo/tutorial del BernatLab
- [ ] Finalitzar M5-M8 del curs (últims detalls)
- [ ] Validar el lab CyberLab amb exercicis reals
- [ ] Muntar l'HP Z1 G9 a casa

### Llarg termini (3-6 mesos)

- [ ] Publicar un article a Infojardín
- [ ] Publicar un article a L'agrobotiga
- [ ] Publicar un vídeo a YouTube
- [ ] Afegir càmeres a l'hort
- [ ] Afegir reg automàtic

---

## 9. Decisions globals (amb raonament)

### Infraestructura

- **Tailscale per accedir a la RPi des de fora:** No cal obrir ports al router, és més segur.
- **Català com a llengua per defecte:** L'usuari és català, tota la documentació està en català.
- **Markdown + Git per versionar:** Permet fer canvis amb ordre i tornar enrere si cal.
- **GitHub Pages per publicar:** Gratuït, fàcil d'actualitzar amb `git push`.
- **Patrons estàndard:** resum + quiz + exercici + respostes + HTML per consistència.
- **150 GB SIM de dades:** Suficient per a sensors i pujada de dades, però cal vigilar el consum.

### Seguretat

- **Cap credencial ni token al repo ni al context** — tot `[REDACTED]`.
- **Aïllament del CyberLab:** Els contenidors vulnerables NO poden accedir a la resta de la xarxa.
- **SSH amb claus** (no pas contrasenyes) — pendent de configurar a tot arreu.

### Desenvolupament

- **Lots petits validats:** Iterar sobre artefactes petits amb proves reals.
- **Scripts a `bin/`:** Eines útils per accedir ràpidament al projecte des de qualsevol PC.
- **RPi al WiFi del router 4G (no a xarxa de casa):** Internet propi a l'hort, no depèn de la cobertura de casa.

---

## 10. Restriccions globals

- **No usar apòstrofs tipogràfics ni cometes intel·ligents** als fitxers — usar ASCII (`'`, `"`, `-`).
- **Cap credencial ni token** al repo ni al context — tot `[REDACTED]`.
- **Llengua catalana** per defecte.
- **Validar amb execució real**, no promeses teòriques.
- **Cap "Paraules clau" al final** dels capítols.
- **Tots els fitxers UTF-8 vàlids**.
- **Fer servir fitxers petits, nets, editables** (KISS).
- **Sempre provar abans de reportar "fet"** — el que compta és el resultat.
- **Mai practicar ciberseguretat des de l'equip de la feina** (risc laboral).

---

## 11. Glossari global

- **BernatLab:** El marc general del projecte (servidor + llibre + curs + hort).
- **Hort Osona:** PWA + plans mensuals de l'hort.
- **CyberLab AI:** Llibre viu + laboratori de ciberseguretat al Kali.
- **Bernat Mora:** L'usuari (desenvolupador + pagès + investigador).
- **Tailscale:** VPN mesh per accedir a dispositius sense obrir ports.
- **tailnet:** Xarxa privada de Tailscale.
- **ESP32:** Microcontrolador amb WiFi integrat per a IoT.
- **Ollama:** Eina per executar LLMs localment.
- **MQTT:** Protocol lleuger per a missatgeria IoT.
- **InfluxDB:** Base de dades time-series.
- **Grafana:** Eina de visualització de dades.
- **RAG:** Retrieval Augmented Generation (cerca + generació).
- **DVWA:** Damn Vulnerable Web Application (lab ciberseguretat).
- **Juice Shop:** Botiga vulnerable per practicar web hacking.
- **Metasploitable:** Linux vulnerable per practicar atacs.
- **HP Z1 G9:** PC potent (32 GB RAM) per a màquines virtuals.
- **4G:** Xarxa mòbil de quarta generació.
- **CGNAT:** Carrier-Grade NAT (impedeix port forwarding directe).
- **Wake-on-LAN:** Tecnologia per despertar PCs remotament.

---

## 12. Com reprendre una sessió (qualsevol projecte)

Si vols continuar treballant en qualsevol dels 3 projectes des d'un altre dispositiu:

1. **Identifica quin projecte** vols continuar (BernatLab, Hort Osona o CyberLab).
2. **Llegeix el `PROJECT_STATE.md`** del projecte concret.
3. **O llegeix aquest `PROJECT_STATE-GLOBAL.md`** per una vista global.
4. **Mira els últims commits** a GitHub: `git log --oneline -10`.
5. **Comprova el working tree** per veure canvis pendents: `git status`.
6. **Continua des dels pendents** de la secció 8 d'aquest document (globals) o dels específics del projecte.

### Si estàs a la feina (Windows)

- Obre Hermes i enganxa el contingut de `PROJECT_STATE-GLOBAL.md` com a context.
- Recorda que a la feina no pots accedir a la RPi directament (necessites Tailscale actiu).

### Si estàs a casa (Mac)

- Obre el Terminal del Mac.
- Vés al directori del repo: `cd ~/bernatlab` (o `~/hort-osona`, `~/cyberlab-ai`).
- Continua treballant directament amb `git` i SSH a la RPi.

### Si estàs a l'hort (PC hort)

- Connecta't per SSH a la RPi: `ssh bernat@hortosona`.
- O treballa directament al PC hort (Windows: `hort-osona@hort`).
- Si tens el router 4G muntat, pots accedir a internet independentment de casa.

---

## Versió

| Data | Canvis |
|---|---|
| 2026-08-07 | Creació del PROJECT_STATE-GLOBAL.md amb vista global dels 3 projectes (BernatLab, Hort Osona, CyberLab AI). |

---

**Aquest PROJECT_STATE-GLOBAL:** `PROJECT_STATE-GLOBAL.md`
**PROJECT_STATE per projecte:** `bernatlab/PROJECT_STATE.md`, `hort-osona/PROJECT_STATE.md` (pròximament), `cyberlab-ai/PROJECT_STATE.md` (pròximament)
**Plantilla original:** `bernatlab/book/PROJECT-STATE-TEMPLATE.md`
