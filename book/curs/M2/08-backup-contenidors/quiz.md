# Qüestionari - Capitol 8: Backup de contenidors

> 10 preguntes · ~15 min

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
Quina es la frecuencia minima raonable per a backups automatics?

- [ ] Un cop al mes
- [x] Un cop al dia
- [ ] Un cop a la setmana
- [ ] Mai

## Pregunta 9 (oberta)
Explica amb les teves paraules: quina diferencia hi ha entre un backup d'un volum Docker, un backup d'una base de dades (dump SQL), i un backup dels fitxers de configuracio (docker-compose.yml)? Quin es el mes critic i per que?

Pistes per respondre:
- Volum = dades binàries (pot ser una base de dades, fitxers, etc).
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
- Verificacio: restaurar periòdicament.
