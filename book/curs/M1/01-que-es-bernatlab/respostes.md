# Respostes — Capítol 1: Què és BernatLab

> Mira les respostes DESPRÉS d'haver fet el qüestionari.

## Pregunta 1: Què és un homelab?

**Resposta correcta**: Un servidor personal a casa, per aprendre i experimentar.

**Explicació**: Un homelab és una paraula anglesa ("home" + "lab" = laboratori a casa). És un servidor que tens a casa teva per provar coses, aprendre, i tenir serveis propis. No és professional — és un laboratori.

---

## Pregunta 2: Quin és el cor del BernatLab?

**Resposta correcta**: Una Raspberry Pi 4 amb Debian 13.

**Explicació**: La Raspberry Pi 4 és un miniordinador (55 €) amb 4 GB de RAM, que gasta molt poc (5-10 W). Debian 13 (Trixie) és la variant del sistema operatiu Linux, sense entorn gràfic ("Lite"), que és ideal per a servidors.

---

## Pregunta 3: Per què serveix Tailscale?

**Resposta correcta**: Per accedir al servidor des de fora sense obrir ports al router.

**Explicació**: Tailscale crea una xarxa virtual privada (VPN) entre els teus dispositius. La teva RPi té una IP 100.x.x.x que és accessible des del teu mòbil, el teu PC de la feina, el teu Mac de casa — sense necessitat d'obrir cap port al router de casa. Això és molt més segur.

---

## Pregunta 4: Quants serveis principals?

**Resposta correcta**: 5 (Docker, Portainer, Uptime Kuma, Homepage, Tailscale).

**Explicació**: Docker és la base; Portainer, Uptime Kuma, i Homepage són serveis que corren dins de Docker; Tailscale és la xarxa privada. Tots 5 són la base del BernatLab.

---

## Pregunta 5: Veritable o fals.

**Resposta correcta**: Fals (corren dins de contenidors Docker).

**Explicació**: Els serveis NO corren directament sobre el sistema operatiu. Corren dins de **contenidors Docker**, que són una mena de "caixes aïllades" que comparteixen el nucli del sistema operatiu però tenen el seu propi sistema de fitxers, xarxa, i processos. Això permet instal·lar i actualitzar serveis sense tocar el sistema base.

---

## Pregunta 6: Quin servei té el port 9443?

**Resposta correcta**: Portainer.

**Explicació**: Portainer és una interfície gràfica per gestionar Docker. Per accedir-hi fas servir HTTPS (no HTTP) i el port 9443. La "s" de "https" és important per seguretat.

---

## Pregunta 7: Quin servei té el port 3001?

**Resposta correcta**: Uptime Kuma.

**Explicació**: Uptime Kuma és el sistema de monitorització. Et diu si els serveis estan funcionant o no, i t'envia alertes (Telegram, email, etc.) quan algun cau.

---

## Pregunta 8: URL d'Hort Osona.

**Resposta correcta**: https://bernatmora.github.io/hort-osona

**Explicació**: Hort Osona és la web pública que has vist (la del github pages). El nom del projecte al repo és `hort-osona` i l'URL GitHub Pages segueix el patró `https://USUARI.github.io/REPO/`.

---

## Pregunta 9 (oberta): Diferència Google Drive vs BernatLab

**Resposta model** (no hi ha una única resposta correcta, però aquí tens els punts clau):

- **Ubicació física**: Google Drive = servidors de Google (EUA, principalment). BernatLab = la teva RPi a casa teva.
- **Accés**: Google Drive = Google (i agències governamentals amb ordres judicials) hi tenen accés. BernatLab = només tu (i qui tu vulguis, via Tailscale).
- **Internet**: Google Drive = si falla internet, no hi accedeixes. BernatLab = si falla internet de fora, sí que hi accedeixes des de casa teva.
- **Condicions**: Google Drive = poden canviar les condicions, pujar preus, tancar el servei. BernatLab = les regles les poses tu.
- **Cost**: Google Drive = mensualitat (15 GB gratuït, després pagues). BernatLab = una vegada (RPi ~55 € + electricitat ~10 €/any).

**Conclusió**: El BernatLab NO substitueix Google Drive per a tot. Per a còpies de seguretat massives, Google Drive és millor. Per a privadesa i dades sensibles (calendari, notes, sensors), el BernatLab és millor.

---

## Pregunta 10 (oberta): Quin servei és més important?

**Resposta model** (depèn de cada persona):

- **Tailscale** — perquè sense Tailscale, no pots accedir al BernatLab des de fora de casa. Sense Tailscale, el BernatLab és inaccessible.
- **Docker** — perquè sense Docker, no pots aïllar serveis ni reproduir fàcilment la configuració.
- **Homepage** — perquè és la porta d'entrada visual; sense Homepage, has de recordar totes les URLs.

**La resposta correcta per a tu** depèn del teu cas. Si viatges molt, Tailscale. Si tens molts serveis, Docker. Si tens família que vol accedir fàcilment, Homepage.

---

## Què fer si has fallat moltes preguntes

- **5-8 encerts**: Tornes a llegir el resum i reps el capítol.
- **3-4 encerts**: Cal rellegir el capítol del llibre amb atenció.
- **0-2 encerts**: Rellegeix el capítol sencer i torna-ho a provar demà.

## Què fer si has encertat totes

- Passa al **Capítol 2** (Raspberry Pi).
- O fes l'**exercici pràctic** per consolidar.
