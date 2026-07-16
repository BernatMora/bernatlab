# Qüestionari — Capitol 2: Restic i alternatives modernes de backup

> 10 preguntes · ~15 min

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
Quin es l'avantatge principal de la desduplicacio?

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
- Cost d'emmagatzematge al núvol.
- Amplada de banda i temps de pujada.
- Recuperacio davant un desastre (incendi, robatori).
- Recuperacio d'un fitxer esborrat per error fa 2 setmanes.
