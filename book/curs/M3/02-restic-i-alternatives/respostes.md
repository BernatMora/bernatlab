# Respostes — Capitol 2: Restic i alternatives modernes de backup

> Mira les respostes DESPRES d'haver fet el qüestionari.

## Pregunta 1: Quina eina fa servir el BernatLab?

**Resposta correcta**: restic.

**Explicacio**: Al BernatLab fem servir restic per fer els backups automatitzats. Es l'eina que millor combina desduplicacio, xifratge, politques de retencio i integracio amb núvol S3. Pero tambe usem rsync per a sincronitzacions puntuals, i coniexem borg i altres com a alternatives.

---

## Pregunta 2: Diferencia entre restic i rsync

**Resposta correcta**: restic te desduplicacio, xifratge i versionat; rsync nomes copia fitxers.

**Explicacio**: 
- **rsync** es una eina de sincronitzacio: copia fitxers nous o modificats d'un lloc a un altre. Si copies 50 GB cada dia, i nomes canvien 100 MB, nomes copiaras 100 MB. Pero no sap res d'historial: si vols tornar a una versio d'ahir, no la tens.
- **restic** es una eina de backup: cada vegada que l'executes crea un nou **snapshot** amb TOT el contingut, pero nomes emmagatzema els blocs nous o modificats. Per tant, el snapshot sembla complet pero nomes pesa la part nova. A mes, xifra tot, i permet politiques de retencio.

---

## Pregunta 3: Inicialitzar un repo de restic

**Resposta correcta**: `restic -r /mnt/ssd/backup init`.

**Explicacio**: La sintaxi de restic sempre te `-r REPO` per especificar el desti abans de qualsevol subordre. `restic init` es la subordre per crear un repo nou. Despres et demanara una contrasenya que has de guardar be perque sense ella no podràs restaurar mai el backup.

---

## Pregunta 4: Quantes copies recomana 3-2-1

**Resposta correcta**: 3.

**Explicacio**: La regla 3-2-1 (definida al cap 1) diu: 3 copies de les teves dades, en 2 suports diferents, 1 fora de casa. Es una regla conservadora que ha demostrat funcionar al llarg dels anys. No es obligatori seguir-la al peu de la lletra, pero es un bon punt de partida.

---

## Pregunta 5: Desduplicacio

**Resposta correcta**: Estalvia espai nomes copiant les parts dels fitxers que canvien.

**Explicacio**: La desduplicacio treballa a nivell de bloc (chunk). Si tens un fitxer de 10 MB i nomes canvien els ultims 200 KB, restic nomes guarda els blocs nous. Si el fitxer no ha canviat, no el torna a guardar. Al final, el backup nomes ocupa la part que realment ha canviat. Amb l'hort IoT, on cada dia s'afegeixen poques dades noves, els backups incrementals ocupen molt poc.

---

## Pregunta 6: Llistar snapshots

**Resposta correcta**: `restic snapshots`.

**Explicacio**: La subordre `snapshots` (o `snap`) mostra tots els snapshots existents al repo, amb el seu ID, data i ruta d'origen. Es la primera ordre que has de fer servir quan entres al repo per veure què tens.

---

## Pregunta 7: Politica de retencio

**Resposta correcta**: `--keep-daily`, `--keep-weekly`, etc. amb `forget`.

**Explicacio**: La combinacio es:
```
restic -r /repo forget --keep-daily 7 --keep-weekly 4 --prune
```

Aixo vol dir: "vull mantenir 7 copies diaries i 4 setmanals; la resta esborra-les". El `--prune` fa l'esborrat real al repo (sino nomes es marquen per esborrar). Es important entendre que `forget` no esborra el backup sencer, sino els snapshots antics individuals.

---

## Pregunta 8: Borg i restic

**Resposta correcta**: Desduplicacio, xifratge i copies incrementals.

**Explicacio**: Borg (2010) va ser el primer a popularitzar aquest esquema, i restic (2014) es va inspirar en ell. Ambdues eines comparteixen la filosofia de "copies incrementals amb desduplicacio de blocs i xifratge per defecte". Si n'aprens una, l'altra es molt semblant.

---

## Pregunta 9 (oberta): Per que restic millor que cp -r o tar

**Resposta model**:

`cp -r` i `tar` son eines per fer copies puntuals, no per fer copies de seguretat continues. Si cada dia fas `cp -r /dades /backup/$(date)`, al cap d'un mes tindras 30 carpetes amb 30 copies completes de 50 GB cadascuna = 1.5 TB. Aixo es insostenible.

Amb `tar -czf backup-$(date).tar.gz /dades`, comprimeixes, pero encara tindras 30 fitxers .tar.gz de ~15-20 GB comprimits. Si nomes canvien 100 MB al dia, el 99.5% del contingut es identic pero l'estas copiant cada vegada.

Amb **restic** nomes es copia el que realment ha canviat (gracies a la desduplicacio de blocs). Si cada dia s'afegeixen 100 MB de lectures de sensors, el backup nomes ocupara uns 100 MB adicionals per dia. Despres d'un any, tindras 365 snapshots que en total ocupen uns 50 GB + 36 GB = ~85 GB. Aixo es **20 vegades mes eficient** que la copia completa.

A mes a mes, restaurar una versio antiga d'un fitxer es trivial: `restic restore <id-snapshot> --target /tmp/restore --include ruta/fitxer`. Amb `cp -r` hauries d'anar a la carpeta de la data adequada, copiar, i creuar els dits perque ningun hagi tocat res.

**Conclusio**: restic es l'eina adequada per fer backups seriiosos, no un luxe.

---

## Pregunta 10 (oberta): rsync vs restic + B2

**Resposta model**:

**Amb rsync nomes**:
- ✅ Gratis (rsync) + cost d'emmagatzematge al núvol.
- ✅ Rapid per sincronitzar (incremental a nivell de fitxer).
- ❌ Sense xifratge al núvol (nomes el que provingui del transport).
- ❌ Sense historial: si rsync sincronitza un fitxer corrupte, el propagues al núvol i perds la versio bona.
- ❌ Sense politiques de retencio: el núvol creix indefinidament.

**Amb restic + Backblaze B2**:
- ✅ Xifratge AES-256 del backup al núvol (nomes tu tens la clau).
- ✅ Historial: cada snapshot es independent, pots tornar enrere.
- ✅ Politiques de retencio: `forget --keep-daily 30 --keep-monthly 6`.
- ✅ Verificacio: `restic check` confirma que el backup no esta corrupte.
- ❌ Cost: Backblaze B2 cobra $6 per TB al mes (per 50 GB son $0.30/mes).
- ❌ Primer backup es lent (ha de pujar-ho tot).

**Tria**: per a l'hort IoT, **restic + B2**. El cost es ridicul (uns 50 centims al mes), i la tranquilitat de saber que puc tornar a qualsevol versio de qualsevol fitxer en els darrers 30 dies val molt la pena. rsync es bo per a sincronitzacio diaria, pero no substitueix un bon sistema de backup.

---

## Pregunta 11 (oberta): Per que desduplicacio i xifratge per defecte

**Resposta model**:

Restic ha introduit la desduplicacio i el xifratge com a funcionalitats per defecte per varios motius:

**1. La desduplicacio nomes funciona si esta sempre activada**:

La desduplicacio de restic funciona a nivell de chunks (blocs de bytes) entre tots els snapshots del repositori. Si nomes la activessis opcionalment, perdries el benefici entre snapshots antics i nous. Per exemple, una foto de 10 MB que no canvia entre mesos: sense desduplicacio constant, esta copiada 12 vegades (12 mesos). Amb desduplicacio, esta copiada 1 sola vegada i els 11 snapshots nomes en tenen una referencia.

**2. Xifratge per defecte = segur per error**:

Molts usuaris no activen el xifratge perque els sembla complicat o innecesari. Si restic no l'activés per defecte, la majoria pujaria backups al núvol sense xifrar, exposant dades a Backblaze o AWS. Activant-lo per defecte, **encara que l'usuari no s'ho plantegi, les seves dades estan segures**.

**3. El rendiment de la deduplicacio es negligible**:

Sembla que afegir xifratge i desduplicacio alentaria molt el backup. Però:
- Restic te chunks de mida variable (4 KB a 16 MB), optimitzats per trobar duplicats rapidament.
- El xifratge amb ChaCha20-Poly1305 es molt rapid en CPU modernes.
- El rendiment es acceptable fins i tot en una RPi 4.
- El benefici (estalvi despa i seguretat) supera el cost.

**4. Coherencia amb la filosofia "secure by default"**:

La comunitat de programari lliure ha après que les opcions segures per defecte son les que funcionen. Si el backup es xifrat per defecte, l'usuari nomes ha de pensar a guardar la clau be. Si fos opcional, l'usuari podria oblidar-se.

**Impacte al BernatLab**:

Gracies a aquestes decisions:
- Pots pujar el backup a Backblaze B2 sense preocupar-te de que Backblaze accedeixi a les teves dades.
- Si tens 5 anys de lectures amb moltes repeticions, el backup ocupa molt menys del que ocuparia amb tar.
- El primer backup pot trigar 1-2 hores (tot es nou), pero els seguients son molt mes rapids (incremental).

**Alternativa mental**: imagina que restic nomes fes el que fa `cp -r`. Hauries d'afegir manualment:
- Xifratge (amb gpg o age).
- Compressio (amb gzip).
- Versionat (amb timestamps).
- Desduplicacio (molt complexe dimplementar).

Restic ho fa tot automaticament. Aquest es el valor de les bones decisions per defecte.

---

## Pregunta 12 (oberta): FreqUencia de backup i ample de banda

**Resposta model**:

La freqUencia de backups esta directament llegada a lample de banda de pujada al núvol. Al BernatLab (100.x.y.z), aixo es un factor critic:

**Calculs basics**:

Si tens 1 GB de dades noves al dia:
- Pujada a 10 Mbps (1.25 MB/s): 1024 MB / 1.25 MB/s = 820 segons = 14 minuts.
- Pujada a 100 Mbps (12.5 MB/s): 82 segons.
- Pujada a 1 Gbps (125 MB/s): 8 segons.

Pero desduplicacio redueix molt la mida:
- Si nomes canvien 100 MB al dia (lectures noves), pujar nomes aixo.
- Si els chunks nous son petits, la pujada es rapidissima.

**Cas real al BernatLab**:

Amb una connexio tipica de 50-100 Mbps de pujada (fibra optica):
- Backup horari de 50 MB nous: 5-10 segons.
- Backup diari de 500 MB nous: 1-2 minuts.
- Backup setmanal de 2 GB nous: 5-10 minuts.

Son temps raonables, es poden fer automaticament de nit.

**Cas problematic: connexio lenta**:

Si tens ADSL de 5 Mbps de pujada (comuna a zones rurals):
- Backup horari: nomes viable si pocs canvis.
- Backup diari de 500 MB: 15 min.
- Backup setmanal de 5 GB: 2-3 hores.

Pot ser problematic si la finestra de temps es limitada.

**Limitacions practiques**:

1. **El ISP pot limitar el trafic sostingut**: alguns ISPs apliquen "fair use" o limiten volum mensual.
2. **El router pot saturar-se**: amb molts dispositius a la xarxa, la pujada pot ser inconsistent.
3. **Les pujades petites son ineficients**: cada conexio TCP te overhead. Pujar 1 MB costa mes per byte que pujar 1 GB.

**Recomanacio per al BernatLab**:

1. **Mesura la teva pujada real**: fes un test amb `speedtest-cli` o simplement puja un fitxer gran.
2. **Calcula el volum diari**: quant creixen les teves dades?
3. **Defineix la freqUencia maxima acceptable**: si la pujada triga mes de 30 min, no la facis diaria.
4. **Accepta compensacions**: si la connexio es lenta, potser nomes pots fer backup setmanal.

**Exemple real**: una RPi a una masia amb 4G pot tenir 1-2 Mbps de pujada. Un backup diari de 100 MB triga 8-15 min. Acceptable, pero no pots fer-ho cada hora.

---

## Pregunta 13 (oberta): Per que tar i cron no son suficients

**Resposta model**:

El company que diu "tar i cron ja en tenen prou" te una visio simplista que funciona per a casos molt basics pero falla en escenaris reals:

**1. tar no te desduplicacio**:

Cada `tar.gz` conte tots els fitxers, comprimits. Si tens 50 GB de dades i un 90% son repetides (lectures similars, imatges no modificades), tar igual les inclou totes. Restic detecta que nomes 5 GB han canviat i nomes puja aixo.

**Cost economic**: amb B2 cobren per GB emmagatzemat. Amb tar, 50 GB x 30 dies = 1.5 TB. Amb restic amb desduplicacio, 50 GB x 1 = 50 GB. Son 1.5 EUR/mes vs 0.05 EUR/mes.

**2. tar no te versionat**:

Si el dilluns crees un fitxer, el dimarts el modifiques i el dimecres vols recuperar la versio del dilluns, amb tar nomes tens la versio del dimecres. Retic guarda totes les versions.

**Cas real**: un script té un bug que modifica lectures de sensors incorrectament durant 3 dies. Descobreixes el bug al quart dia. Amb tar: has perdut 3 dies de lectures correctes. Amb restic: pots tornar a la versio del primer dia.

**3. tar no te xifratge**:

El fitxer `.tar.gz` esta en clar al núvol. Si el proveidor es compromet o un atacant hi accedeix, pot llegir les teves dades. Restic xifra per defecte amb AES-256, nomes tu pots desxifrar.

**4. tar no verifica la integritat**:

Amb tar, nomes saps que el backup sha creat correctament. Pero no saps si es pot restaurar. Retic te `restic check` que verifica que el backup es pot restaurar.

**5. cron no te gestio derrors**:

Si el tar falla (per exemple, disc ple), cron simplement pasa al seguent job. No reps cap alerta. Restic pot enviar emails o notificar a Telegram si falla.

**6. tar no es portable entre núvols**:

Si vols canviar de Backblaze a Wasabi, amb tar has de tornar a pujar tot. Amb restic, el repo es portable (es el mateix format).

**Conclusio**: tar + cron es com tenir un cotxe sense frens. Pot funcionar, pero quan falli, fallara malament. Restic es el mateix treball pero amb frens, airbags i ABS.

**Al BernatLab**: amb pocs GB de dades i un sol fitxer .tar, pot semblar que tar nomes ja esta be. Pero el dia que necessitis una versio antiga o que el núvol es corrompi, agrairàs tenir restic.

---

## Pregunta 14 (oberta): Politica de retencio per a 4 fonts de dades

**Resposta model**:

Per a 4 fonts de dades amb caracteristiques diferents al BernatLab, la politica de retencio amb `restic forget` seria:

**1. Base de dades SQLite de l'hort (5 MB)**:
- FreqUencia backup: diaria.
- Politica retencio: `keep-daily 14, keep-weekly 8, keep-monthly 6`.
- Justificacio: 5 MB es molt petit, podem permetre mes historia. 14 dies diaries + 8 setmanes + 6 mesos. Ocupa ~50-100 MB al núvol.

**2. Coleccio de fotos dels bancals (2 GB)**:
- FreqUencia backup: setmanal.
- Politica retencio: `keep-weekly 4, keep-monthly 12, keep-yearly 3`.
- Justificacio: 2 GB es moderat. 4 setmanes + 12 mesos + 3 anys. Pero amb desduplicacio, nomes ocupara ~2.5-3 GB total.

**3. Configuracio del sistema (50 MB)**:
- FreqUencia backup: diaria.
- Politica retencio: `keep-daily 30, keep-weekly 12, keep-monthly 12`.
- Justificacio: 50 MB es ridicul, podem guardar molta historia. 30 dies + 12 setmanes + 12 mesos.

**4. Logs de l'aplicacio (200 MB que roten)**:
- FreqUencia backup: diaria (nomes la rotacio del dia).
- Politica retencio: `keep-daily 7, keep-weekly 4`.
- Justificacio: els logs canvien molt pero son menys critics. 7 dies diaries + 4 setmanes.

**Script de retencio**:

```bash
#!/bin/bash
# Backup diari
restic -r b2:bucket:/hort backup /var/lib/bernatlab/hort.db --tag sensors
restic -r b2:bucket:/hort backup /home/pi/bernatlab/config/ --tag config
restic -r b2:bucket:/hort backup /var/log/bernatlab/ --tag logs

# Backup setmanal (diumenges)
if [ "$(date +%u)" = "7" ]; then
    restic -r b2:bucket:/hort backup /home/pi/bernatlab/fotos/ --tag fotos
fi

# Aplicar politiques
restic -r b2:bucket:/hort forget \
    --tag sensors \
    --keep-daily 14 --keep-weekly 8 --keep-monthly 6 --prune

restic -r b2:bucket:/hort forget \
    --tag config \
    --keep-daily 30 --keep-weekly 12 --keep-monthly 12 --prune

restic -r b2:bucket:/hort forget \
    --tag logs \
    --keep-daily 7 --keep-weekly 4 --prune

restic -r b2:bucket:/hort forget \
    --tag fotos \
    --keep-weekly 4 --keep-monthly 12 --keep-yearly 3 --prune
```

**Resum d'espai total**:
- Sensors: 100 MB.
- Config: 50 MB.
- Logs: 50 MB.
- Fotos: 3 GB.
- Total: ~3.2 GB al núvol, cost ~0.20 EUR/mes.

Es molt economic i dona un bon equilibri entre retencio i cost.

---

## Pregunta 15 (oberta): Retencio i recuperacio

**Resposta model**:

La politica de retencio te un impacte directe en la teva capacitat de recuperacio. Considerem el cas:

**Escenari problematic**:

Conserva nomes 7 dies de copies diaries. Un dilluns, un bug sutil canvia lectures de sensors amb valors incorrectes. El bug nomes es detecta el dimecres 15 dies despres. Per recuperar:
- Amb retencio 7 dies: nomes tens copies dels ultims 7 dies. El dilluns que necessites ja no hi es. **Has perdut 8 dies de dades bones**.
- Amb retencio 30 dies: tens la copia del dilluns. Recupera.

**Cas real al BernatLab**:

Aixo passa mes del que sembla:
- Un update de InfluxDB canvia el format de les dades pero el contenidor vell encara escriu en el format antic. 2 setmanes de dades incompatibles.
- Un error de script que duplica lectures durant 10 dies. Descobreixes que les estadistiques son inflades.
- Un atacant entra i modifica lectures per amagar la seva presencia. Descobreixes l'atac dies despres.

**Trade-off entre retencio i cost**:

| Retencio | Cost B2 (50 GB) | Recuperacio possible fins a... |
|---|---|---|
| 7 dies | 0.05 EUR/mes | 1 setmana |
| 30 dies | 0.10 EUR/mes | 1 mes |
| 90 dies | 0.20 EUR/mes | 3 mesos |
| 1 any | 0.50 EUR/mes | 1 any |

La diferencia de cost entre 7 dies i 90 dies es de 0.15 EUR/mes. Per 0.15 EUR/mes tens la tranquilitat de poder recuperar quasi qualsevol error.

**Recomanacio al BernatLab**:

- **Lectures de sensors**: retencio llarga (90 dies minim). Son dades historiques uniques.
- **Configuracio**: retencio molt llarga (1 any). Es poca mida, i els canvis subtils poden tardar a detectar-se.
- **Fotos**: retencio mitjana (6-12 mesos). Si perds una foto, no es tragic, pero tens temps de descobrir-ho.
- **Logs**: retencio curta (7-14 dies). Ocupen espai i son menys critics.

**Conclusio**: la politica de retencio es un dial que pots ajustar. Comença amb valors generosos (30-90 dies) i redueix nomes si el cost al núvol es un problema. La diferencia de cost es minima, pero la diferencia en capacitat de recuperacio es enorme.

---

## Que fer si has fallat moltes preguntes

- **5-8 encerts**: Rellegir el resum.
- **3-4 encerts**: Rellegeix el cap 2 amb atencio, sobretot la seccio de comandes basiques.
- **0-2 encerts**: Repassem junts el capitol abans de continuar. Es fonamental entendre restic per als capitols següents.

## Que fer si has encertat totes

- Passa al **Capitol 3** (volums Docker).
- O fes l'**exercici practic** per consolidar.
