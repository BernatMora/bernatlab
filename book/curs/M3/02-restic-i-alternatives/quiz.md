# Qüestionari - Capitol 2: Restic i alternatives modernes de backup

> 15 preguntes · ~20 min

## Pregunta 1
Quina eina de backup fa servir el BernatLab per defecte?

- [ ] tar + cron
- [x] restic
- [ ] Borg Backup
- [ ] Dropbox

## Pregunta 2
Quina es la principal diferencia entre restic i rsync?

- [ ] restic nomes funciona a Linux
- [x] restic te desduplicacio, xifratge i versionat; rsync nomes copia fitxers
- [ ] rsync es mes segur que restic
- [ ] restic nomes serveix per a fitxers petits

## Pregunta 3
Quina ordre faries servir per inicialitzar un repo de restic a `/mnt/ssd/backup`?

- [ ] restic init /mnt/ssd/backup
- [x] restic -r /mnt/ssd/backup init
- [ ] restic create /mnt/ssd/backup
- [ ] restic backup /mnt/ssd/backup

## Pregunta 4
Quantes copies de seguretat recomana la regla 3-2-1?

- [ ] 1
- [ ] 2
- [x] 3
- [ ] 5

## Pregunta 5
Quin es lavantatge principal de la desduplicacio?

- [ ] Comprimeix els fitxers amb gzip
- [x] Estalvia espai nomes copiant les parts dels fitxers que canvien
- [ ] Encripta el backup
- [ ] Permet accedir des del mobil

## Pregunta 6
Quina ordre de restic llista tots els snapshots existents?

- [ ] restic list
- [x] restic snapshots
- [ ] restic show
- [ ] restic status

## Pregunta 7
Quin parametre de restic esborra les copies antigues segons una politica?

- [ ] --prune
- [x] --keep-daily, --keep-weekly, etc. (amb forget)
- [ ] --cleanup
- [ ] --rotate

## Pregunta 8
Borg Backup i restic comparteixen quina caracteristica clau?

- [ ] Ambdos necessiten Java
- [x] Desduplicacio, xifratge i copies incrementals
- [ ] Ambdos son GUI
- [ ] Cap de les dues, son completament diferents

## Pregunta 9 (oberta)
Explica amb les teves paraules: per que restic es millor que fer `cp -r` o `tar` per fer backups? Pensa en el cas de l'hort IoT on cada dia s'afegeixen lectures de sensors.

Pistes per respondre:
- Quant espai ocupa cada nova copia amb `cp -r`?
- Quant triga a fer-se un backup complet cada dia?
- Com restauraries una versio antiga d'un fitxer?

## Pregunta 10 (oberta)
Imagina que tens 50 GB de dades de l'hort i vols fer backup al núvol. Compara fer-ho amb `rsync` nomes vs amb `restic` + Backblaze B2. Quin escolliries i per que?

Pistes per respondre:
- Cost demmagatzematge al núvol.
- Amplada de banda i temps de pujada.
- Recuperacio davant un desastre (incendi, robatori).
- Recuperacio dun fitxer esborrat per error fa 2 setmanes.

## Pregunta 11 (oberta)
Per que creus que restic ha introduit la desduplicacio i el xifratge com a funcionalitats per defecte, en lloc de ser opcionals? Quin impacte te aixo en la teva estrategia de backup al BernatLab?

Pistes per respondre:
- La desduplicacio nomes funciona si esta sempre activada (cross-snapshot).
- Xifratge per defecte = segur per error.
- Trade-off: rendiment vs funcionalitat.
- Al BernatLab, quantes vegades has oblidat activar el xifratge manualment?

## Pregunta 12 (oberta)
Quina relacio hi ha entre la frequencia de backups i el temps de pujada al núvol? Com afecta al BernatLab (100.115.134.76) tenir una conexio lenta vs rapida? Calcula exemples amb nombres reals.

Pistes per respondre:
- 1 GB de dades noves al dia.
- Pujada a 10 Mbps = 15 min. A 100 Mbps = 1.5 min.
- 10 GB nous al dia: 2.5 h a 10 Mbps.
- Com afecta si el backup nomes pot correr de nit?

## Pregunta 13 (oberta)
Imagina que el teu company et diu: "per que complicar-te amb restic si amb un `tar.gz` i un `cron` ja en tens prou?". Argumenta per que aixo es insuficient al BernatLab, especialment per a dades de sensors que creixen cada dia.

Pistes per respondre:
- tar.gz ocupa tot l'espai cada vegada.
- Sense versionat, no pots recuperar versions antigues.
- Sense xifratge, les dades viatgen desprotegides.
- Sense desduplicacio, els backups al núvol son cars.

## Pregunta 14 (oberta)
Aplica el concepte de restic al cas concret del BernatLab amb 4 fonts de dades: base de dades SQLite de l'hort (5 MB), coleccio de fotos dels bancals (2 GB), configuracio del sistema (50 MB), logs de l'aplicacio (200 MB que roten). Dissenya una politica de retencio amb `restic forget` especificant quantes copies diaries, setmanals i mensuals conservaries per a cada cas.

Pistes per respondre:
- Les dades de sensors: alta freq, canvis petits cada vegada.
- Les fotos: canvis esporadics, volem mes retencio.
- La configuracio: pocs canvis, retencio llarga.
- Els logs: alta freq, retencio curta.

## Pregunta 15 (oberta)
Quines consequencies te per a la seguretat de les dades la politica de retencio de restic? Si nomes conserves 7 dies de copies, que passa si no t'adones d'un problema fins passats 10 dies? Argumenta amb exemples del BernatLab.

Pistes per respondre:
- Bug que corromp dades i no es detecta durant dies.
- Atacant que entra i es queda silent.
- Error de l'operador que no es veu fins mes tard.
- Trade-off: espai al núvol vs capacitat de recuperacio.
