# Qüestionari - Capitol 8: Backup de contenidors

> 15 preguntes · ~20 min

## Pregunta 1
Quina es la regla 3-2-1 dels backups?

- [ ] 3 usuaris, 2 passwords, 1 servidor
- [x] 3 copies, 2 suports diferents, 1 fora de la maquina
- [ ] 3 tipus de fitxers, 2 ubicacions, 1 còpia setmanal
- [ ] 3 servidors, 2 xarxes, 1 firewall

## Pregunta 2
Quin metode es el mes recomanable per fer backup d'un volum Docker?

- [ ] Copiar manualment els fitxers del volum
- [x] Usar un contenidor temporal que munta el volum i empaqueta amb tar
- [ ] Fer un snapshot del sistema de fitxers
- [ ] Usar una eina de sincronitzacio

## Pregunta 3
Quina comanda fa un backup d'una base de dades PostgreSQL dins un contenidor?

- [ ] cp /var/lib/postgresql/data
- [x] docker exec postgres-container pg_dump -U user dbname > backup.sql
- [ ] docker backup postgres
- [ ] tar czf postgres.tar.gz

## Pregunta 4
Per que es important xifrar els backups?

- [ ] Per comprimir mes
- [x] Perque si el backup es perd o es robat, les dades estiguin protegides
- [ ] Per a que es puguin restaurar nomes per tu
- [ ] Per a que ocupin menys

## Pregunta 5
Que vol dir un backup "verificat"?

- [ ] Un backup que sha fet amb HTTPS
- [x] Un backup que sha provat de restaurar i sha confirmat que funciona
- [ ] Un backup verificat contra virus
- [ ] Un backup que sha enviat a un altre lloc

## Pregunta 6
Quina eina es recomana per a backups incrementals al núvol?

- [ ] cp
- [ ] scp
- [x] restic, borgbackup o rclone
- [ ] git

## Pregunta 7
Quina es la millor opcio per automatitzar backups a una hora concreta?

- [ ] Watchtower
- [x] cron
- [ ] Docker Compose
- [ ] systemd timer

## Pregunta 8
Quina es la frequencia minima raonable per a backups automatics?

- [ ] Un cop al mes
- [x] Un cop al dia
- [ ] Un cop a la setmana
- [ ] Mai

## Pregunta 9 (oberta)
Explica amb les teves paraules: quina diferencia hi ha entre un backup d'un volum Docker, un backup d'una base de dades (dump SQL), i un backup dels fitxers de configuracio (docker-compose.yml)? Quin es el mes critic i per que?

Pistes per respondre:
- Volum = dades binaries (pot ser una base de dades, fitxers, etc).
- Dump SQL = nomes les dades de la base de dades, en format text.
- Configuracio = comandes per tornar a muntar l'stack.
- Si nomes en tens un, quin tries?

## Pregunta 10 (oberta)
Al BernatLab tens un Nextcloud amb fotos personals (50 GB) i una base de dades MariaDB. Dissenya una estrategia de backups complerta usant la regla 3-2-1. Explica cada pas: que copies, on, cada quan, com ho verifiques.

Pistes per respondre:
- 3 copies: original a la SD/SSD, backup local, backup al núvol.
- 2 suports: disc SSD + núvol.
- 1 fora: el núvol.
- Eines: rsync, restic, mysqldump.
- Automatitzacio: cron.
- Verificacio: restaurar periodicament.

## Pregunta 11 (oberta)
Per que creus que la gent sovint no fa backups fins que perd les dades? Quines consequencies te això al BernatLab si tens un Nextcloud amb 5 anys de fotos familiars i la microSD es corromp? Argumenta amb exemples emocionals i practics.

Pistes per respondre:
- Falta de temps, "ja ho fare".
- El cost del backup es tangible (espai, temps); el benefici es intangible.
- La microSD te una vida util limitada (~5 anys d'escriptura).
- Perdre 5 anys de fotos es irreparable.
- Solució: posar el backup en mode "set it and forget it".

## Pregunta 12 (oberta)
Quina relacio hi ha entre la mida del backup, el temps de fer-lo i la finestra de perdua acceptable (RPO)? Com afecta al BernatLab (100.115.134.76) triar backups horaris vs diaris? Quant de temps de dades estaries disposat a perdre?

Pistes per respondre:
- RPO (Recovery Point Objective): quant de temps de dades puc perdre com a maxim.
- Backup horari: perdua maxima d'1 hora de dades.
- Backup diari: perdua maxima de 24 hores de dades.
- Trade-off: cost d'espai/temps vs RPO.
- Que es acceptable per a fotos? I per a una base de dades de comandes?

## Pregunta 13 (oberta)
Imagina que el teu company et diu: "tinc un RAID al servidor, per que necessito backup?". Explica-li la diferencia entre RAID i backup, i per que al BernatLab totes dues coses son necessaries. Dona exemples concrets de desastres que RAID no evita.

Pistes per respondre:
- RAID protegeix contra fallada de disc, no contra borrat accidental, ransomware, o desastre fisic.
- Si un `rm -rf` esborre un directori, el RAID replica la perdua.
- Si un atac de ransomware xifra les dades, el RAID tambe es xifra.
- Si la RPi es robada o te una sobretensio, RAID no salva res.
- Backup + RAID es la combinacio correcta.

## Pregunta 14 (oberta)
Aplica el concepte de backup al cas concret del BernatLab amb l'stack Hort Osona (Ollama, ChromaDB, Open WebUI) i les dades dels sensors (InfluxDB). Quines dades son critiques i quines es poden regenerar? Dissenya una politica de backup especifica per a cada component.

Pistes per respondre:
- Ollama: els models es poden tornar a baixar. No cal backup.
- ChromaDB: conte els embeddings. Es pot regenerar pero triga 30 min. Conv backup.
- Open WebUI: nomes configuracio. Backup del volum.
- InfluxDB: dades historiques. Backup diari.
- Script d'indexacio: nomes codi, ja esta a Git.

## Pregunta 15 (oberta)
Quines consequencies te per a la privacitat fer backups al núvol de dades sensibles? Com ho faries al BernatLab si tens un Nextcloud amb documents personals (DNI, factures, etc)? Explica les opcions de xifrat i la gestio de claus.

Pistes per respondre:
- Al núvol les dades viatgen per internet i reposen en servidors de tercers.
- Xifrat local abans de pujar (restic --encryption-mode repokey).
- La clau d'encriptacio ha d'estar guardada en un lloc diferent del backup.
- Trade-off: practicitat vs seguretat.
- Es pot fer backup al núvol nomes de les dades no sensibles?
