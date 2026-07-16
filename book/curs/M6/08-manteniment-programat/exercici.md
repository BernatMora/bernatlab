# Exercici practic - Capitol 8: Manteniment programat

> 30-45 min · Real a la teva RPi

## Objectiu

Crear un script de manteniment setmanal, configurar-lo en un cron, i practicar una neteja del sistema. Tambe aprendras a verificar que els teus backups funcionen. Acabaras amb un sistema mes net i un procediment automatic.

## Requisits

- RPi amb Docker i almenys 2-3 serveis
- 30-45 minuts
- Espai en disc limitat (per veure els efectes de la neteja)

## Pas 1: Mira l'estat actual del sistema (5 min)

```bash
# Espai en disc
df -h

# Memoria
free -h

# Mida de Docker
docker system df

# Contenidors corrent
docker ps

# Logs del sistema
journalctl --disk-usage
```

Apunta els valors: et serviran per comparar despres.

## Pas 2: Crea el script de manteniment setmanal (10 min)

```bash
sudo nano /opt/bernatlab/maintenance.sh
```

Enganxa:

```bash
#!/bin/bash
# /opt/bernatlab/maintenance.sh
# Script de manteniment setmanal del BernatLab

LOG=/var/log/bernatlab-maintenance.log
DATE=$(date '+%Y-%m-%d %H:%M:%S')

echo "=== Manteniment $DATE ===" >> $LOG

# 1. Espai en disc abans
echo "[Abans] Espai en disc:" >> $LOG
df -h / >> $LOG

# 2. Netejar imatges Docker dangling (no usades)
echo "[Docker] Netejant imatges no usades..." >> $LOG
docker image prune -f >> $LOG 2>&1

# 3. Netejar volum Docker no usats
echo "[Docker] Netejant volums no usats..." >> $LOG
docker volume prune -f >> $LOG 2>&1

# 4. Netejar xarxes Docker no usades
echo "[Docker] Netejant xarxes no usades..." >> $LOG
docker network prune -f >> $LOG 2>&1

# 5. Netejar logs antics de journald
echo "[Journal] Netejant logs antics..." >> $LOG
journalctl --vacuum-time=14d >> $LOG 2>&1

# 6. Netejar cache apt
echo "[Apt] Netejant cache..." >> $LOG
apt clean >> $LOG 2>&1

# 7. Espai en disc despres
echo "[Despres] Espai en disc:" >> $LOG
df -h / >> $LOG

# 8. Estat final
echo "[Estat] Contenidors corrent:" >> $LOG
docker ps --format "  {{.Names}}: {{.Status}}" >> $LOG 2>&1

echo "=== Finalitzat ===" >> $LOG
echo "" >> $LOG
```

Fes-lo executable:

```bash
sudo chmod +x /opt/bernatlab/maintenance.sh
```

## Pas 3: Prova el script (5 min)

```bash
sudo /opt/bernatlab/maintenance.sh
sudo cat /var/log/bernatlab-maintenance.log
```

Hauries de veure les operacions fetes i l'espai alliberat.

## Pas 4: Programa el script cada diumenge a les 3:00 AM (5 min)

```bash
sudo crontab -e
```

Afegeix:

```
0 3 * * 0 /opt/bernatlab/maintenance.sh
```

## Pas 5: Verifica els teus backups (10 min)

Si tens restic configurat (del M3 cap 2):

```bash
# Comprovar l'estat del repositori
restic check

# Llistar els ultims 5 snapshots
restic snapshots --last 5

# Restaurar l'ultim snapshot a una carpeta de test
restic restore latest --target /tmp/test-restore
ls -la /tmp/test-restore/

# Netejar
sudo rm -rf /tmp/test-restore
```

Si NO tens restic, simplement comprova que els teus fitxers de backup existeixen i son recents:

```bash
ls -la /backups/
du -sh /backups/*
```

## Pas 6: Fes una auditoria dels teus serveis (10 min)

Mira quins serveis tens, quins son utils, quins podries eliminar:

```bash
# Llistar tots els teus serveis
docker ps -a

# Per cada un, pregunta't:
# - L'uso regularment?
# - Te alternatives mes bones?
# - Consumeix molts recursos?
# - Te dades importants?

# Mira les metricas de CPU/RAM per contenidor
docker stats --no-stream
```

Apunta en un document `SERVICIOS.md` quins son essencials i quins podries eliminar.

## Validacio

Has acabat si:

- [ ] Has creat el script `/opt/bernatlab/maintenance.sh` i funciona.
- [ ] Esta programat al cron cada diumenge a les 3:00 AM.
- [ ] Has alliberat espai en disc (compara amb el valor inicial).
- [ ] Has verificat els teus backups amb `restic check` o similar.
- [ ] Tens un document `SERVICIOS.md` amb els teus serveis i la seva criticitat.
- [ ] El log de manteniment creix correctament.

## Per aprofundir

- Afegeix una alerta a Telegram quan el script acaba (curl al bot).
- Crea un script de manteniment mensual mes complet (apt upgrade + cleanup).
- Configura Glances per tenir un monitor en temps real per terminal.
- Investiga l'eina `ncdu` per visualitzar l'us del disc de forma interactiva.
