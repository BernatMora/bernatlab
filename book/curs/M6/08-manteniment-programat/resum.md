# Resum - Capitol 8: Manteniment programat

## La idea clau

Un sistema 24/7 no s'ha de tocar mai? No, al reves. S'ha de TOCAR de forma regular pero PLANIFICADA. Si nomes toques el servidor quan algo es trenca, acabaràs fent canvis urgents amb presses, sense proves, i amb mes possibilitats de nous problemes. El manteniment programat es la "medicina preventiva": netejar, revisar, actualitzar, abans que algo falli.

## Que es el manteniment programat?

Son tasques que fas amb una **periodicitat fixa** (setmanal, mensual, trimestral) per mantenir el sistema sa:

- **Setmanal**: revisar alertes, netejar brossa, mirar logs nous.
- **Mensual**: actualitzar manualment, revisar backups, netejar imatges.
- **Trimestral**: revisar capacitat, analitzar tendencies, planificar.
- **Anual**: canvis majors, neteja fisica, revisio general.

## Per que es important?

Quan un sistema porta mes de 6 mesos sense manteniment:

- **Disc ple**: logs antics, imatges no usades, paquets de cache.
- **Vulnerabilitats**: paquets no actualitzats amb CVEs coneguts.
- **Contenidors zombies**: contenidors aturats que ningú neteja.
- **Backups no verificats**: creus que tens backups pero potser no funcionen.
- **Petits problemes que creixen**: warnings que ningú mira, logs amb errors repetitius.

## Tasques setmanals (30 min)

Un bon manteniment setmanal podria ser:

```bash
# 1. Mirar quins serveis fallen
docker ps -a
docker ps -a --filter "status=exited"

# 2. Comprovar espai en disc
df -h
du -sh /var/lib/docker/

# 3. Netejar logs antics de journald
sudo journalctl --vacuum-time=14d

# 4. Netejar imatges Docker no usades
docker image prune -a
# Compte: nomes les que no son en us

# 5. Mirar les ultimes alertes
# (a la UI de Grafana o al grup de Telegram)
```

## Tasques mensuals (1-2 hores)

Un cop al mes, val la pena fer una sessio mes a fons:

```bash
# 1. Actualitzar manualment el sistema
sudo apt update
sudo apt upgrade
sudo apt autoremove

# 2. Mirar si hi ha imatges noves
docker images --format "table {{.Repository}}:{{.Tag}}\t{{.CreatedAt}}"

# 3. Comprovar l'estat dels teus backups
ls -la /backups/
restic check

# 4. Fer una "prova de foc": restaurar un backup
restic restore latest --target /tmp/test-restore
diff -r /tmp/test-restore /opt/bernatlab/

# 5. Mirar els logs per patrons nous
journalctl --since "1 month ago" | grep -i error | head

# 6. Revisar les alertes del mes
# Alertes que s'han disparat massa vegades (ajustar)
# Alertes que mai s'han disparat (eliminar)
```

## Tasques trimestrals (2-3 hores)

Cada 3-6 mesos cal fer una revisio mes profunda:

- **Mirar el creixement de dades**: si els logs creixen mes del compte.
- **Revisar els volums Docker**: quin esta creixent mes?
- **Analitzar les tendencies**: temperatura a l'estiu, memoria, etc.
- **Actualitzar imatges amb nous tags**: passar de 2024.5 a 2024.10.
- **Revisar runbooks**: actualitzar si cal.
- **Netejar configuracio morta**: dashboards que ja no uses, alertes obsoletes.

## Neteja del sistema

A la llarga, tot sistema acumula brossa. Alguns punts:

### Logs

```bash
# Netejar logs antics
sudo journalctl --vacuum-time=14d
sudo journalctl --vacuum-size=200M

# Rotar manualment
sudo logrotate -f /etc/logrotate.conf
```

### Imatges Docker

```bash
# Veure imatges ocupant espai
docker system df

# Netejar imatges "dangling" (no usades)
docker image prune

# Netejar totes les imatges no usades
docker image prune -a
# Aixo nomes funciona si els contenidors NO les usen

# Netejar tambe volum, xarxa i cache
docker system prune -a --volumes
# ATENCIO: nomes fer-ho si estas segur
```

### Volums Docker

Els volums son persistents i es poden omplir. Per veure:

```bash
docker volume ls
docker system df -v
```

Per netejar els volum no usats:

```bash
docker volume prune
# Compte: nomes els que no son usats per cap contenidor
```

### Cache apt

```bash
sudo apt clean
sudo apt autoclean
```

## Cron jobs per netejar automaticament

```bash
sudo crontab -e
```

Afegir:

```
# Cada diumenge a les 3:00 AM, netejar imatges Docker no usades
0 3 * * 0 docker image prune -a -f

# Cada dia a les 4:00 AM, netejar logs antics
0 4 * * * journalctl --vacuum-time=14d

# Cada mes, netejar cache apt
0 5 1 * * apt clean
```

## Backups: la part mes important del manteniment

El backup nomes serveix si pots **recuperar**. Per tant, has de:

1. **Fer backups regulars**: almenys diari per dades critiques.
2. **Verificar que el backup es valid**: de tant en tant, restaurar en un entorn de test.
3. **Guardar fora de la RPi**: si la RPi mor (microSD, robatori, etc.), els teus backups han d'estar en un altre lloc.
4. **Documentar com restaurar**: al runbook (cap 10).

## Tendencies: el que la gent no mira

A mes a mes de les tasques reactives, val la pena mirar les **tendencies**:

- **Disc ple d'aqui a X mesos?** Si creix 1 GB al mes, tens 12 mesos. Si creix 10 GB, tens 1 mes.
- **El contenidor d'X creixent la memoria?** Pot ser una fuita.
- **Els logs creixen descontroladament?** Aplicacio amb un bucle d'errors.
- **Les temperatures pujant?** Ventilacio o pols.

Aixo ho veus als dashboards de Grafana. Mira les tendencies de 30 dies cada setmana.

## Calendari de manteniment

Un exemple de calendari:

| Periode | Tasca | Temps estimat |
|---------|-------|---------------|
| Setmanal | Revisar alertes, netejar brossa, mirar logs nous | 30 min |
| Mensual | Actualitzar manualment, verificar backups | 1-2 hores |
| Trimestral | Revisio tendencies, actualitzar imatges, netejar volum | 2-3 hores |
| Semestral | Auditoria completa, revisar runbooks | 1 dia |
| Anual | Canvis majors, neteja fisica, revisar capacitat | 1-2 dies |

## Eines utils

- **Restic** (ja el tens al M3): backups amb deduplicacio.
- **Logrotate**: rotacio automatica de logs.
- **Watchtower** (cap 7): actualitzacio automatica de contenidors.
- **Cron**: programacio de tasques.
- **netdata**: alternativa a Prometheus+Grafana, mes automatitzat.
- **Glances**: monitor de sistema per terminal, una sola pantalla.

## Connexions amb altres capitols

- **M3 Cap 1-2** - Estrategia de backup i restic: la base.
- **M6 Cap 7** - Actualitzacio segura: la part tecnica.
- **M6 Cap 10** - Runbooks: per documentar totes aquestes tasques.
