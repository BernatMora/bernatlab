# Respostes - Capitol 8: Manteniment programat

> Mira les respostes DESPRES d'haver fet el qüestionari.

## Pregunta 1: Per que manteniment

**Resposta correcta**: Perque netejar i revisar periodicament evita problemes majors.

**Explicacio**: Es mes rapid netejar brossa cada setmana que no pas arreglar un sistema ple al cap de 6 mesos. Es mes rapid actualitzar un cop al mes que no pas perdre 2 dies depurant una vulnerabilitat. El manteniment programat es COM L'ANAR AL TALLER: petits costs regulars per evitar grans averies.

---

## Pregunta 2: Frequencia backups

**Resposta correcta**: Diariament o segons la criticat.

**Explicacio**: La frequencia depen de quant pot canviar la teva dada. Si tens un blog que escrius un cop al mes, un backup setmanal es OK. Si tens Home Assistant amb sensors que canvien cada minut, necessites backup diari o mes frequent. La regla es: si perdre 24h de dades et fa mal, fes backup diari.

---

## Pregunta 3: Comanda df Docker

**Resposta correcta**: `docker system df`.

**Explicacio**: `docker system df` mostra quant ocupen les imatges, contenidors, volums i build cache per separat. Es la millor eina per veure "que m'esta ocupant el disc". Tambe pots fer `docker system df -v` per mes detall per imatge/volum.

---

## Pregunta 4: Netejar journald

**Resposta correcta**: `journalctl --vacuum-time=14d`.

**Explicacio**: `--vacuum-time` borra logs mes antics de X temps. Tambe hi ha `--vacuum-size=200M` que esborra fins deixar 200 MB. Es mes segur que no pas esborrar manualment els fitxers de `/var/log/journal/` (que poden deixar journald inconsistent).

---

## Pregunta 5: Netejar imatges

**Resposta correcta**: `docker image prune -a`.

**Explicacio**: `docker image prune` esborra imatges "dangling" (sense tag). Amb `-a` esborra TOTES les imatges que no son en us per cap contenidor. Compte: si tens un contenidor aturat pero la imatge existeix, amb `-a` tambe la borraras. Aleshores hauras de tornar-la a baixar.

---

## Pregunta 6: Risc de no verificar backups

**Resposta correcta**: Que et puguis trobar amb un backup corrupte quan el necessitis.

**Explicacio**: Es MOLT habitual fer backups durant mesos i descobrir el dia que els necessites que no funcionen. Basa de dades inconsistent, fitxer comprimit buit, permissos mal posats... Cal verificar periodicament que el backup es pot restaurar. Es la diferencia entre "tinc un backup" i "tinc un backup que funciona".

---

## Pregunta 7: Eina de rotacio

**Resposta correcta**: logrotate.

**Explicacio**: logrotate ve amb totes les distribucions Linux. Configures regles tipus "/var/log/X.log { daily, rotate 7, compress }" i s'encarrega de la rotacio. Es una de les eines mes antigues i estables de Linux, funciona be sense manteniment.

---

## Pregunta 8: Neteja fisica

**Resposta correcta**: Cada 6-12 mesos.

**Explicacio**: La pols es l'enemic numero 1 de la refrigeracio. Una RPi amb el radiador ple de pols pot passar de 60 a 80 graus a l'estiu. Cada 6-12 mesos cal obrir la caixa, treure el radiador, netejar amb aire comprimit o un pinzell suau, i tornar a muntar. Es una feina de 5 minuts que pot evitar una averia de 50 EUR.

---

## Pregunta 9 (oberta): Calendari de manteniment

**Resposta model**:

Aqui tens un calendari de manteniment per al BernatLab amb temps estimat:

**Setmanal (30 min, diumenge mati):**

| Tasca | Temps |
|-------|-------|
| Revisar alertes dels ultims 7 dies a Grafana/Telegram | 5 min |
| Mirar quins serveis fallen o tenen errors al log | 5 min |
| Comprovar espai en disc amb `df -h` | 2 min |
| Comprovar memoria amb `free -h` | 2 min |
| Executar `docker system df` per veure brossa | 2 min |
| Mirar grafiques de CPU/RAM/temperatura de la setmana | 5 min |
| Executar `/opt/bernatlab/maintenance.sh` (neteja automatica) | 5 min |
| Apuntar tendencies o coses rares al journal | 4 min |

**Mensual (1-2 h, primer diumenge del mes):**

| Tasca | Temps |
|-------|-------|
| Tot l'anterior (setmanal) | 30 min |
| `sudo apt update && sudo apt upgrade` | 15 min |
| `sudo apt autoremove && sudo apt clean` | 5 min |
| Mirar si hi ha imatges noves dels serveis manuals (Home Assistant, InfluxDB) | 10 min |
| Verificar backups: `restic check` + restaurar un snapshot a `/tmp/test` | 20 min |
| Revisar logs d'errors (`journalctl --since "1 month ago" \| grep -i error`) | 10 min |
| Comprovar que l'alerta de watchdog ha funcionat (rebut missatge?) | 2 min |
| Netejar imatges Docker antigues: `docker image prune -a` | 5 min |
| Revisar espai ocupat per volums: `docker system df -v` | 5 min |
| Apuntar conclusions al journal | 8 min |

**Trimestral (2-3 h, principi de trimestre):**

| Tasca | Temps |
|-------|-------|
| Tot l'anterior (mensual) | 90 min |
| Analitzar tendencies de 90 dies a Grafana (creixement, anomalies) | 20 min |
| Actualitzar imatges manuals amb nous tags | 20 min |
| Revisar i netejar dashboards/alertes obsoletes a Grafana | 15 min |
| Comprovar que els runbooks (cap 10) son actuals | 15 min |
| Auditar els accessos SSH (`/var/log/auth.log`) | 10 min |
| Netejar fitxers temporals antics (`/tmp`, `/var/tmp`) | 5 min |
| Planificar possibles millores per al proper trimestre | 5 min |

**Semestral (4-6 h, gener i juliol):**

| Tasca | Temps |
|-------|-------|
| Tot l'anterior (trimestral) | 180 min |
| Auditoria completa de seguretat (M2 cap 6) | 60 min |
| Provar el procediment de recuperacio de desastre | 30 min |
| Revisar la capacitat: cal mes disc? mes RAM? | 15 min |
| Netejar fitxers antics, logs, brossa acumulada | 15 min |

**Anual (1-2 dies, idealment a la primavera):**

| Tasca | Temps |
|-------|-------|
| Tot l'anterior (semestral) | 6 h |
| Actualitzacio major del sistema operatiu | 2-3 h |
| Netejar la pols de la RPi (fisic) | 30 min |
| Verificar/reemplaçar la font d'alimentacio | 15 min |
| Verificar/reemplaçar la microSD (si toca) | 30 min |
| Considerar passar a un SSD si encara es microSD | 1-2 h |
| Revisar i actualitzar tota la documentacio (runbooks) | 1-2 h |
| Auditar costos (cloud, dominis, etc.) | 30 min |
| Celebrar que un any mes ha funcionat! | :-) |

L'objectiu es que el 90% del temps siguis DEFENSIVA (netejar, verificar) i nomes un 10% sigui OFENSIVA (millores noves). Si tot va be, el sistema hauria d'anar com un rellotge.

---

## Pregunta 10 (oberta): Importancia dels backups

**Resposta model**:

Els **backups son la part mes important del manteniment** per una raó molt simple: son l'ULTIMA xarxa de seguretat. Si tot falla - l'actualitzacio trenca el sistema, la microSD es mor, el ransomware xifra tot, un robatori a casa - nomes tens ELS BACKUPS per tornar a tenir el sistema funcionant.

Pero un backup nomes es valid si es pot **recuperar**. Hi ha moltes histories de gent que ha perdut tot perque "tenia backups" pero no havien provat mai de restaurar-los i estaven corruptes o incomplets.

Per assegurar que els teus backups realment funcionen, cal fer totes aquestes coses:

**1. Fer backups regulars i automatitzats**

No confiïs en la memoria. Configura un cron que faci backup automatic:
```bash
# Cada dia a les 2:00 AM
0 2 * * * /opt/bernatlab/backup.sh
```
El backup ha de ser **automatic** perque si depen de que tu el facis manualment, un dia el deixaras de fer.

**2. La regla 3-2-1**

- **3** copies de les teves dades (l'original + 2 backups)
- **2** tipus diferents de mitjans (disc local + cloud, o disc + USB)
- **1** fora de la teva ubicacio fisica (cloud, casa d'un amic, altre ciutat)

Si nomes tens el backup a la mateixa RPi, quan la RPi es mori (i es morira), perds el backup tambe. Si nomes tens un USB al costat de la RPi i entren a robar, perds els dos.

**3. Verificar periodicament**

Cada mes (o setmana si tens temps), agafa un snapshot i restaura'l en una carpeta temporal:
```bash
restic restore latest --target /tmp/test
# Comprovar que hi ha els fitxers esperats
ls /tmp/test
diff -r /tmp/test /opt/bernatlab/
rm -rf /tmp/test
```
Si el backup falla, ho sabras aviat i podras investigar. No esperes al dia que necessites restaurar.

**4. Xifrar si son dades sensibles**

Si els teus backups contenen dades personals (configuracio de HA amb ubicacio de casa, fitxers de clients, etc.), xifra'ls:
```bash
restic init --repo /mnt/backup/bernatlab
# Xifratge automatic amb AES-256
```
Si puges el backup a un cloud, el xifratge es IMPRESCINDIBLE.

**5. Documentar el procediment de restauracio**

Al runbook (cap 10) has de tenir, pas a pas, com restaurar:
- On es el backup
- Quin password/contrasenya cal
- L'ordre exacte per restaurar
- Que fer un cop restaurat

Si un dia et passes 5 minuts buscant el password del backup, son 5 minuts que podries perdre quan ja estas estressat. Tingues-ho TOT apuntat.

**6. Provar el "fire drill"**

Un parell de cops l'any, simula una catastrofe: apaga la RPi, "perds" la microSD, i restaura des de zero nomes amb el backup. Aixo et permet veure:
- Si el procediment funciona
- Si falta alguna cosa
- Quant triga realment la recuperacio

Es la diferencia entre "estic preparat" i "estic PREPARAT de veritat".

---

## Que fer si has fallat moltes preguntes

- **5-8 encerts**: Rellegir el resum i fer l'exercici practic.
- **3-4 encerts**: Refes l'exercici desde zero observant cada pas.
- **0-2 encerts**: Repassem junts el capitol abans de continuar.

## Que fer si has encertat totes

- Passa al **Capitol 9** (Troubleshooting).
- Configura Glances com a monitor en temps real per terminal.
- Crea un calendari de manteniment al teu Obsidian o eina favorita.
