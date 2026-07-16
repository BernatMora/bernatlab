# Respostes — Capítol 2: La Raspberry Pi 4 per dins

> Mira les respostes DESPRÉS d'haver fet el qüestionari.

## Pregunta 1: Què és una Raspberry Pi?

**Resposta correcta**: Un ordinador complet en una placa (SBC).

**Explicació**: SBC = Single-Board Computer. Tots els components (CPU, RAM, ports) estan en una sola placa del tamany d'una targeta de crèdit. No és un processador sol (com un Snapdragon) ni un sistema operatiu (com Linux).

---

## Pregunta 2: Quina arquitectura de CPU?

**Resposta correcta**: ARM (arm64).

**Explicació**: La RPi 4 usa un processador ARM Cortex-A72. La versió de 64 bits s'anomena arm64 o AArch64. La majoria de distribucions Linux modernes ja tenen paquets arm64, inclosa Debian 13.

---

## Pregunta 3: Quanta RAM?

**Resposta correcta**: 4 GB.

**Explicació**: La teva RPi té 4 GB de RAM LPDDR4. N'hi ha versions de 1, 2, 4 i 8 GB. 4 GB és el sweet spot per a un homelab amb uns 5-10 contenidors Docker.

---

## Pregunta 4: On s'emmagatzema el SO?

**Resposta correcta**: En una targeta microSD.

**Explicació**: La RPi no té disc dur intern. El sistema operatiu viu en una targeta microSD. Això és convenient (fàcil de clonar) però limitat (vida útil menor que un SSD).

---

## Pregunta 5: Consum aproximat?

**Resposta correcta**: 5-10 W.

**Explicació**: Una RPi 4 en repòs consumeix uns 3-4 W, i amb càrrega pot arribar a 7-8 W. Un PC de torre consumeix 100-300 W, 20-30 vegades més. Això permet tenir el servidor 24/7 sense que la factura de llum es dispari (uns 5-15 € l'any).

---

## Pregunta 6: Temperatura crítica?

**Resposta correcta**: 85°C.

**Explicació**: A 80°C la CPU comença a reduir la seva velocitat (thermal throttling). A 85°C hi ha risc de dany. Per això és important refrigerar la RPi, especialment si l'aguantes 24/7.

---

## Pregunta 7: Primer procés?

**Resposta correcta**: systemd.

**Explicació**: systemd és el primer procés que arrenca el kernel (PID 1). La seva feina és arrencar tots els serveis, gestionar dependencies, muntar sistemes de fitxers, etc. Docker, Tailscale, SSH — tots són serveis que systemd gestiona.

---

## Pregunta 8: Port d'alimentació?

**Resposta correcta**: USB-C.

**Explicació**: La RPi 4 va passar de micro-USB (RPi 3) a USB-C perquè necessitava més potencia (5V/3A = 15W). Si l'alimentes amb un carregador de mòbil de 5V/1A, potser no engega o reiniciarà amb càrrega.

---

## Pregunta 9 (oberta): RPi per homelab sí, per a producció professional no

**Resposta model**:

Per a un homelab, la RPi 4 és excel·lent perquè:
- **Eficient**: 5-10 W de consum, pots tenir-la 24/7 sense pena.
- **Silenciosa**: sense ventilador, sense soroll.
- **Barata**: 55 € una vegada, en lloc de 50-200 €/mes al núvol.
- **Prou potent**: per a 5-10 contenidors petits (Homepage, Portainer, Uptime Kuma, Grafana, etc.).
- **Aprenentatge**: pots tocar el sistema, trencar coses, refer-les.

Per a un servidor de producció professional, la RPi NO és adequada perquè:
- **RAM limitada**: 4 GB és poc per a serveis amb molts usuaris concurrents.
- **Emmagatzematge lent**: la microSD és més lenta i menys fiable que un SSD o NVMe.
- **CPU ARM**: no tots els programes tenen binari ARM, o tenen menys optimitzacions.
- **Sense redundància**: si falla la SD, el servidor cau. Sense RAID, sense backup automàtic.
- **Sense suport comercial**: si tens un problema crític a les 3 de la matinada, no pots trucar a ningú.

**Conclusió**: la RPi és una eina d'aprenentatge i prototipat. Per a producció, cal un servidor x86 amb redundància.

---

## Pregunta 10 (oberta): 1000 visites diaries a la botiga

**Resposta model**:

1000 visites diaries són unes **0.7 visites per minut** de mitjana (molt poc). Però cal pensar en pics:

- Si el 10% de visites vénen en una hora (raonable), són **100 visites en 60 minuts** = ~1.7 visites per segon.
- Cada visita pot carregar 5-10 recursos (HTML, CSS, JS, imatges).
- Per tant, el pic pot ser de **10-20 peticions per segon**.

Una RPi 4 amb un servidor web ben optimitzat (Nginx, pàgines estàtiques, cache) **podria** gestionar-ho, però:
- La **RAM és el coll d'ampolla** principal: 4 GB és just per al SO + servidor + base de dades.
- Si la botiga té **pàgines dinàmiques** (PHP, Python, Node), caldrà més potència.
- Si la botiga té **imatges pesades** o vídeos, la xarxa pot ser el coll d'ampolla.

**Recomanació**:
- Per a **menys de 100 visites diaries**: la RPi és perfecta.
- Per a **100-1000 visites diaries**: la RPi pot funcionar, però cal optimitzar molt.
- Per a **més de 1000 visites diaries o pàgines dinàmiques**: cal un servidor x86 (4-8 GB RAM, SSD).

**Quan pujar a un servidor de veritat**? Quan el temps de resposta superi 1-2 segons, o quan caigui el servidor durant pics.

---

## Què fer si has fallat moltes preguntes

- **5-8 encerts**: Rellegir el resum.
- **3-4 encerts**: Rellegeix el cap 2 del llibre amb atenció.
- **0-2 encerts**: Repassem junts el capítol abans de continuar.

## Què fer si has encertat totes

- Passa al **Capítol 3** (Linux).
- O fes l'**exercici pràctic** per consolidar.
