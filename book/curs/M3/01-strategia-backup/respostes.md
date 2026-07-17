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

## Pregunta 11 (oberta): Per que la gent minimitza la importancia dels backups

**Resposta model**:

La gent tendeix a minimitzar la importància dels backups per una combinacio de factors psicologics i economics que es repeteixen a tothom:

**1. Optimisme irracional**: "A mi no em pasara". Es la mateixa logica que porta la gent a no fer testament o a no portar cinturo de seguretat. La vulnerabilitat es invisible fins que es real. Es un mecanisme de defensa: viure amb la por constant de perdre dades es agotador, aixi que el cervell ho minimitza.

**2. Cost tangible vs benefici intangible**: fer un backup te un cost inmediat: temps de configurar, espai de disc, diners al núvol. El benefici nomes es materialitza en cas de perdua, que es un esdeveniment futur i improbable. El cervell prioriza el present.

**3. Pensament magic**: "Tinc RAID", "tinc el núvol", "el meu proveidor ja fa copies". Totes son excuses per evitar la tasca. Cap es equivalent a un backup real. RAID protegeix contra fallada de hardware pero no contra borrat accidental o ransomware. El núvol es sincronitzacio, no backup.

**4. Procrastinacio tecnologica**: "Quan tingui temps ho fare". El temps no arriba mai. I quan arriba un incident, ja es massa tard.

**5. Por d'admetre la perdua**: si no tinc backup, no he de pensar en que passaria si ho perdés. Es mes facil viure en la negacio.

**Cas emocional al BernatLab (l'hort IoT)**:

Imagina que tens 2 anys de lectures de temperatura, humitat i reg del teu hort. Son dades uniques que representen l'esforç de 2 anys de monitoratge: grafic de temperatures, tendencia de reg, comparatives entre estacions. Un dia la microSD falla (cosa que pasa). Les dades son **irreemplaçables**: no hi ha manera de tornar a recollir la temperatura del 15 de març passat. Tot es al teu hort que ja no arranca.

El sentiment es devastador. No es una perdua economica, es una perdua personal. I la ironia es que un backup automatitzat de 2 hores de configuracio t'hauria estalviat aquest dolor.

**Solucio realista al BernatLab**:

1. **Automatitza el backup**: un cop configurat, es transparent. No cal pensar-hi mes.
2. **Fes-lo un cop i oblida't**: posa el cron a les 3 de la matinada. El backup es nomes responsabilitat del sistema.
3. **Verifica un cop al trimestre**: dedica 1 hora cada 3 mesos a restaurar un fitxer random. Això et recorda que el backup funciona.
4. **Documenta el proces de restauracio**: quan tinguis que restaurar (i tindras que restaurar), no vols haver d'aprendre com fer-ho enmig del panic.

El millor backup es el que ja esta configurat abans que el necessitis.

---

## Pregunta 12 (oberta): RPO, RTO i cost

**Resposta model**:

El **RPO (Recovery Point Objective)** i el **RTO (Recovery Time Objective)** son dos conceptes fonamentals que defineixen la teva estrategia de backup:

**RPO - Quant de dades puc perdre?**

Defineix la finestra de temps maxima de dades que estaries disposat a perdre. Es directament la freqUencia del backup:
- RPO = 1 setmana: backup setmanal.
- RPO = 1 dia: backup diari.
- RPO = 1 hora: backup horari (o casi continu).
- RPO = 0: replicacio sincrona (molt car).

**RTO - Quant trigare a restablir el servei?**

Defineix el temps maxim acceptable des que es produeix l'incident fins que el servei esta operatiu de nou. Inclou:
- Detectar l'incident (alerta).
- Decidir que fer.
- Executar la restauracio.
- Verificar que funciona.

Per exemple:
- RTO = 24 h: acceptable per a un projecte personal.
- RTO = 4 h: acceptable per a un negoci petit.
- RTO = 1 h: nomes amb hot standby o infraestructura complexa.
- RTO = 0: alta disponibilitat (cluster, failover automatic).

**Relacio amb el cost**:

| RPO | RTO | Cost al BernatLab | Cas d'us |
|---|---|---|---|
| 1 setmana | 24 h | Molt baix (rsync setmanal + disc extern) | Hobby |
| 1 dia | 4 h | Moderat (restic diari + núvol) | Personal |
| 1 hora | 1 h | Alt (replicacio + scripts complexos) | Negoci |
| 0 | 0 | Molt alt (cluster K8s, replicacio sincrona) | Empresa |

**Exemple concret al BernatLab (100.115.134.76)**:

Si tens un Nextcloud amb documents de feina:
- RPO acceptable: 4-8 h (no vols perdre un dia de feina).
- RTO acceptable: 1-2 h (vols tornar a treballar aviat).
- Cost: backup horari + script de restauracio provat = 2-3 h de setup + 0.5 EUR/mes al núvol.

Si nomes tens fotos:
- RPO acceptable: 1 setmana (les fotos no canvien).
- RTO acceptable: 24 h (no es urgent).
- Cost: backup setmanal + disc extern = 0.5 h de setup + 0 EUR al núvol.

**Conclusio**: el cost del backup es directament proporcional a la frequencia i sofisticacio. No paguis per mes del que necessites, pero tampoc estalviïs en allò que es critic.

---

## Pregunta 13 (oberta): Dropbox no es backup

**Resposta model**:

El company que diu "tinc el núvol, ja estic salvat" te una confusio comuna pero perillosa. Dropbox, Google Drive, iCloud i OneDrive son eines de **sincronitzacio**, no de backup. La diferencia es fonamental:

**Que fan les eines de sincronitzacio**:

- Mantenen fitxers iguals a multiples dispositius.
- Si canvies un fitxer en un lloc, canvia a tots.
- Si esborres un fitxer, s'esborra a tots (despres d'un periode de gracia de 30 dies).
- Son dissenyades per a acces desde qualsevol lloc, no per a recuperacio.

**Que no fan (i per que no son backup)**:

1. **No protegeixen contra borrat accidental**: si esborres un fitxer per error, Dropbox el sincronitza a tots els teus dispositius en segons. Passats 30 dies, fins i tot de la paperera.

2. **No protegeixen contra ransomware**: si un virus xifra els teus fitxers locals, Dropbox sincronitza els fitxers xifrats al núvol. Ara tens el xifrat al núvol i l'original esborrat. Pitjor que no tenir res.

3. **No protegeixen contra compromissio de compte**: si algú roba la teva contrasenya de Dropbox, pot esborrar tots els teus fitxers. Dropbox te un periode de gracia, pero si no t'adones a temps, tot es perdut.

4. **No son append-only**: un backup de veritat nomes te afegir fitxers nous, no esborrar. Dropbox es una eina bidireccional.

5. **El proveidor hi te acces**: Dropbox te les claus per accedir als teus fitxers. Un backup xifrat (restic + B2) nomes tu pots desxifrar.

**Alternativa adequada al BernatLab**:

Per a dades importants:
- **Restic + B2** (o similar): backup real amb xifratge, versionat, deduplicacio.
- **Discs externs** amb rotacio (un a casa, un a la caixa forta del banc, un a casa d'un familiar).
- **Regla 3-2-1** amb eines que garanteixin immutabilitat.

Per a fitxers sincronitzats (no son backup pero son utils):
- **Syncthing** entre els teus dispositius (no passa per tercers).
- **Nextcloud** auto-hostatge (tu controles).

El missatge al company: "Tens acces als teus fitxers desde qualsevol lloc, si. Pero si s'esborren, els perds. Un backup et permet tornar enrere en el temps. Son coses diferents."

---

## Pregunta 14 (oberta): Estrategia per a l'hort IoT

**Resposta model**:

Per a l'hort IoT amb 5 sensors (temperatura, humitat, llum), coleccio de 200 fotos dels bancals, i configuracio del sistema, l'estrategia completa seria:

**Component 1: Lectures de sensors (alta freqUencia, petits canvis cada vegada)**:
- RPO: 1 hora. Vull perdre com a maxim 1 hora de lectures.
- FreqUencia backup: cada 6 hores (4 cops/dia).
- Metode: `influx backup` (consistent) o export a CSV.
- Ubicacio: SSD extern + Backblaze B2.
- Retencio: 30 dies al núvol, 7 dies local.

**Component 2: Fotos dels bancals (baixa freqUencia, fitxers grans)**:
- RPO: 1 setmana. Les fotos no canvien un cop pujades.
- FreqUencia backup: setmanal (diumenges a la nit).
- Metode: `restic backup /home/pi/bernatlab/fotos/`.
- Ubicacio: SSD extern + B2.
- Retencio: 12 mesos al núvol, 1 mes local.

**Component 3: Configuracio del sistema (canvis esporadics, fitxers petits)**:
- RPO: 1 dia. Vull perdre com a maxim 1 dia de configuracio.
- FreqUencia backup: diari.
- Metode: `restic backup /home/pi/bernatlab/config/ /etc/`.
- Ubicacio: B2 nomes (es petit).
- Retencio: 90 dies.

**Component 4: Logs de l'aplicacio (alta freqUencia, retencio curta)**:
- RPO: 1 dia.
- FreqUencia backup: diari.
- Metode: rotacio + tar de la rotacio.
- Ubicacio: nomes local.
- Retencio: 7 dies.

**Resum de l'estrategia**:

| Component | Freq | RPO | Local | Núvol | Retencio |
|---|---|---|---|---|---|
| Lectures sensors | 6h | 1h | SSD | B2 | 30d núvol |
| Fotos | 1setm | 1setm | SSD | B2 | 12m núvol |
| Configuracio | 1d | 1d | - | B2 | 90d |
| Logs | 1d | 1d | local | - | 7d |

**Automatitzacio**: tot via cron o un script que es crida cada hora i decideix quina tasca executar segons el temps transcorregut.

**Verificacio**: cada trimestre, restaura un element de cada tipus per confirmar que el backup funciona.

---

## Pregunta 15 (oberta): Backup i sostenibilitat del projecte

**Resposta model**:

Una estrategia de backup deficient te consequencies subtils pero importants per a la sostenibilitat del projecte a llarg termini:

**1. Por de perdre dades frena l'experimentacio**:

Si no tens backup, cada vegada que provis algo nou, tens por. "I si es trenca tot?". Això porta a:
- No actualitzar serveis per por de perdre configuracio.
- No provar noves eines per por de perdre dades.
- No fer neteja de fitxers antics per si de cas.
- Resultat: el sistema es queda estancat, no innova.

**2. La perdua d'una feinada frena l'entusiasme**:

Imagina que passes 3 dies configurant un Grafana amb 15 dashboards personalitzats. Un dia la RPi falla i ho perds tot (no tens backup de Grafana). La perdua et fa deixar el projecte durant mesos. L'entusiasme es trenca.

**3. La llicencia per experimentar**:

Un bon backup et dona **llicencia per experimentar**. Saps que si algo surt malament, pots tornar enrere. Això et permet:
- Provar noves versions de programari.
- Canviar l'arquitectura amb mes llibertat.
- Aprendre coses noves amb risc minim.
- Innovar mes rapidament.

**4. La sostenibilitat personal**:

Si cada vegada que l'ordinador falla perds hores de feina, el projecte esdevé una font d'estres. Si tens bon backup, els incidents son inconvenients temporals, no catastrofes. Això et permet gaudir del projecte a llarg termini.

**5. La comunitat i la collaboracio**:

Si vols compartir el teu projecte amb altres, necessiten poder reproduir el que tens. Un backup ben documentat es una guia de com muntar tot desde zero.

**Conclusio**: el backup no es nomes una questio tecnica ("guardar copies"). Es una questio de **sostenibilitat personal** del projecte. Et dona la tranquil·litat i la llibertat per continuar innovant. Al BernatLab, dedicar 4-8 hores a posar un bon sistema de backup es una de les inversions mes rendibles que pots fer.

---

## Què fer si has fallat moltes preguntes

- **5-8 encerts**: Rellegir el resum, sobretot la secció "La regla 3-2-1 explicada".
- **3-4 encerts**: Torna a mirar la secció "Què cal backupejar" i "Freqüència: la regla RPO".
- **0-2 encerts**: Repassem junts el capítol abans de continuar. La regla 3-2-1 és fonamental per a tot el mòdul.

## Què fer si has encertat totes

- Passa al **Capítol 2** (Restic i alternatives), on aprendràs a aplicar aquesta estratègia amb una eina concreta.
- O fes l'**exercici pràctic** per definir la teva estratègia personal.
