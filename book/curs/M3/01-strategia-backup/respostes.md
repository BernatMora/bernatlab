# Respostes — Capítol 1: Estratègia de backup

> Mira les respostes DESPRÉS d'haver fet el qüestionari.

## Pregunta 1: Quantes còpies recomana la regla 3-2-1?

**Resposta correcta**: 3.

**Explicació**: La regla 3-2-1 estableix **3 còpies** de les dades (a més de l'original, en total 4 fitxers), en **2 suports diferents**, i **1 fora de casa**. Les tres còpies inclouen l'original, per això la regla diu "3 còpies" i no "4 còpies". Això garanteix que si un suport falla, encara tens dues còpies redundants.

---

## Pregunta 2: Quants suports diferents?

**Resposta correcta**: 2.

**Explicació**: Dos suports **diferents** vol dir que no poden ser al mateix dispositiu ni tan sols al mateix rack. Un SSD USB i un HDD extern són dos suports. Un disc i una còpia al núvol són dos suports. Dos discos al mateix armari no compten com a suports diferents per a la regla, perquè un incendi o un lladre se'ls emporta tots dos.

---

## Pregunta 3: Què vol dir "1 fora de casa"?

**Resposta correcta**: Que almenys una còpia ha d'estar en un lloc físic diferent.

**Explicació**: Aquesta part de la regla és la que la gent s'oblida més. Si totes les teves còpies són a casa teva, un incendi, una inundació, o un robatori te les poden perdre totes. La solució més pràctica és pujar una còpia xifrada al núvol (Backblaze B2, Wasabi, etc.), tot i que algú amb molt d'espai a casa d'un familiar o una caixa forta al banc també serveix.

---

## Pregunta 4: Quina dada és la més crítica?

**Resposta correcta**: Les bases de dades amb lectures dels sensors.

**Explicació**: La resta de coses es poden refer: el sistema operatiu es reinstal·la, les imatges Docker es tornen a baixar, la configuració de xarxa es replica. Però les **lectures de temperatura, humitat i reg** que he recollit durant mesos no es poden tornar a generar. Són dades úniques, històriques, que representen l'esforç de mesos de monitoratge de l'hort. Per això la prioritat de backup és la base de dades.

---

## Pregunta 5: Què vol dir RPO?

**Resposta correcta**: El temps màxim de dades que estic disposat a perdre.

**Explicació**: RPO = Recovery Point Objective. Si vull un RPO d'una hora, cal fer backup cada hora, perquè en el pitjor cas (sistema caigut just després d'un backup) perdo només l'última hora de dades. Si un RPO d'un dia és acceptable, puc fer backup un cop al dia. Per a l'hort IoT, un RPO de 6-24 h és raonable: perdre un dia de lectures d'un sensor de temperatura no és greu, però perdre un mes sí.

---

## Pregunta 6: Per què Dropbox no és un bon backup?

**Resposta correcta**: Perquè si esborres un fitxer, Dropbox l'esborra també.

**Explicació**: Dropbox (i Drive, i OneDrive) són eines de **sincronització**, no de backup. Si esborres un fitxer per error, Dropbox el sincronitza a tots els teus dispositius en qüestió de segons, i passats 30 dies desapareix fins i tot de la paperera. Un ransomware que xifra els teus fitxers locals farà el mateix amb Dropbox. Un backup de veritat ha de ser **append-only** (només s'afegeixen fitxers) o tenir **versioning** (versions antigues durant 30-90 dies).

---

## Pregunta 7: Freqüència prudent per a bases de dades IoT?

**Resposta correcta**: Cada 6-24 hores.

**Explicació**: Depèn del volum de dades que generis. Si el teu sensor de temperatura escriu una lectura cada minut, són 1440 lectures al dia, i perdre 24 h és molt. Si escriu cada 5 minuts i són lectures crítiques, cada hora és millor. Per a l'hort IoT amb sensors cada 10-15 minuts, un backup cada 6 hores és un bon equilibri entre pèrdua acceptable i cost d'emmagatzematge.

---

## Pregunta 8: Quin servei al núvol per a backups barats?

**Resposta correcta**: Backblaze B2.

**Explicació**: Backblaze B2 cobra uns 6 dòlars per TB al mes d'emmagatzematge i 1 dòlar per TB de transferència. Per a un homelab amb 100 GB de dades, el cost mensual és de 0,60 dòlars. Wasabi és similar. Google Drive i iCloud són cares per a grans volums (10-20 dòlars al mes per 100 GB) i tenen termes de serveis que permeten accedir a les teves dades. Backblaze B2 té integració nativa amb Restic, que veurem al capítol 2.

---

## Pregunta 9 (oberta): Explica la regla 3-2-1 amb exemple

**Resposta model**:

La regla 3-2-1 és una norma bàsica de còpies de seguretat que estableix: **3 còpies** de les dades, en **2 suports diferents**, i almenys **1 fora de casa**. La idea és que cap desastre local (incendi, robatori, fallada de disc) pugui destruir totes les còpies alhora.

**Exemple aplicat a l'hort IoT del BernatLab**:
- **Original**: les dades viuen a la base de dades SQLite/PostgreSQL de la RPi, al disc SSD USB connectat.
- **Còpia 1**: cada dia a les 3 de la matinada, Restic fa una còpia al HDD extern que tinc al calaix del despatx. És un suport físic diferent del SSD.
- **Còpia 2**: cada dia a les 4 de la matinada, Restic puja una còpia xifrada a Backblaze B2, que està en un datacenter a Amsterdam. Això és la còpia "fora de casa".

Tinc 3 còpies totals (original + 2 backups), 2 suports diferents a casa (SSD + HDD), i 1 còpia fora de casa (Backblaze B2). Si es trenca el SSD, recupero del HDD. Si ve un incendi a casa, recupero del núvol. Si s'esborra tot per error, Restic em permet tornar a una versió de fa 6 mesos.

---

## Pregunta 10 (oberta): Estratègia per a SQLite amb dades de sensors

**Resposta model**:

Per a una base de dades SQLite amb lectures de sensors IoT al BernatLab, triaria una estratègia de backup **diària automatitzada** amb còpia local i remota.

**RPO desitjat**: 24 hores. Per a lectures de temperatura i humitat cada 15 minuts, perdre un dia de dades és acceptable — torno a tenir lectures l'endemà, i la tendència de la setmana es manté.

**Esquema**:
1. **Original**: la base de dades viu a `/var/lib/docker/volumes/influxdb-data/` o similar, al SSD USB de la RPi.
2. **Còpia local**: cada nit a les 2 AM, una tasca `cron` executa `restic backup` cap a un directori `/mnt/hdd-extern/backups/`. Això és la còpia 1, en un suport diferent.
3. **Còpia remota**: cada nit a les 4 AM, `restic backup` puja la còpia a Backblaze B2 amb xifrat. Això és la còpia 2, fora de casa.

**Per què SQLite i no un altre sistema?**: SQLite és suficient per a un hort petit amb 1-2 sensors. Per a més volum o múltiples sensors, canviaria a InfluxDB (cap. 6). Però la filosofia de backup és la mateixa: còpia consistent del fitxer (cap. 4) o export a SQL, amb còpia local i remota.

**Què passaria si es trenca la RPi dimarts a les 15h?**: l'últim backup és de dilluns a les 4 AM, així que perdo 35 hores de dades. Restic em restaura la base de dades de dilluns, torno a connectar sensors, i torno a recollir. La pèrdua està dins del RPO de 24 h que m'havia marcat (gairebé).

---

## Què fer si has fallat moltes preguntes

- **5-8 encerts**: Rellegir el resum, sobretot la secció "La regla 3-2-1 explicada".
- **3-4 encerts**: Torna a mirar la secció "Què cal backupejar" i "Freqüència: la regla RPO".
- **0-2 encerts**: Repassem junts el capítol abans de continuar. La regla 3-2-1 és fonamental per a tot el mòdul.

## Què fer si has encertat totes

- Passa al **Capítol 2** (Restic i alternatives), on aprendràs a aplicar aquesta estratègia amb una eina concreta.
- O fes l'**exercici pràctic** per definir la teva estratègia personal.
