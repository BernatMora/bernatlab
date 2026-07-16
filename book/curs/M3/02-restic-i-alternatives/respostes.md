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

## Que fer si has fallat moltes preguntes

- **5-8 encerts**: Rellegir el resum.
- **3-4 encerts**: Rellegeix el cap 2 amb atencio, sobretot la seccio de comandes basiques.
- **0-2 encerts**: Repassem junts el capitol abans de continuar. Es fonamental entendre restic per als capitols següents.

## Que fer si has encertat totes

- Passa al **Capitol 3** (volums Docker).
- O fes l'**exercici practic** per consolidar.
