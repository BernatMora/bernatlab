# Resum — Capitol 2: Restic i alternatives modernes de backup

## La idea clau

Un cop tens clar que cal fer còpies de seguretat (cap 1), la pregunta següent es: amb quina eina. Al BernatLab vaig descartar rapidament les solucions casolanes amb `tar` i `cp` perque son lentes, ocupen molt d'espai (cada backup es una copia completa) i no tenen verificacio ni historial. **Restic** es una eina moderna de backup pensada precisament per a servidors petits: fa copies incrementals, desduplica, encripta, i permet restaurar una versio concreta d'un fitxer. Es l'eina que uso jo per defecte.

Pero restic no es l'unica opcio. Hi ha alternatives com **borgbackup** (molt semblant), **rsnapshot** (basat en rsync), **kopia** (cross-platform), o simplement **rsync + cron** (el mes basic). Cadascuna te els seus pros i contres, i la tria depen de les teves necessitats.

## Restic: l'eina estrella

Restic es un programa escrit en Go que fa copies de seguretat amb aquestes caracteristiques:

- **Desduplicacio**: si un fitxer no ha canviat, no el copia. Si nomes ha canviat un tros, nomes copia el tros. Esto fa que els backups incrementals siguin molt petits.
- **Xifratge**: tot el backup es xifra amb AES-256 per defecte. Tu nomes necessites una contrasenya.
- **Compressio**: els fitxers es comprimeixen abans de pujar-los.
- **Versionat**: pots mantenir N versions antigues de cada fitxer (per exemple, "vull les ultimes 7 copies diaries + 4 setmanals + 6 mensuals").
- **Multi-desti**: pot escriure a un directori local, a SFTP, a S3 (i Backblaze B2, que es compatible), a REST server, etc.
- **Verificacio**: `restic check` verifica que el backup no esta corrupte.
- **Repositoris**: un repo es una coleccio de backups. Pots tenir-ne tants com vulguis.

### Comandes basiques

```bash
# Inicialitzar un repo local
restic -r /mnt/ssd-backup/bernatlab init

# Fer un backup
restic -r /mnt/ssd-backup/bernatlab backup \
  /home/pi/bernatlab/configs \
  /home/pi/bernatlab/dades

# Llistar els snapshots
restic -r /mnt/ssd-backup/bernatlab snapshots

# Restaurar un snapshot sencer
restic -r /mnt/ssd-backup/bernatlab restore latest \
  --target /tmp/restore

# Restaurar un sol fitxer
restic -r /mnt/ssd-backup/bernatlab restore latest \
  --target /tmp/restore \
  --include /home/pi/bernatlab/configs/mosquitto.conf
```

### Politiques de retencio

Aqui es on brilla restic. Pots dir-li: "vull mantenir 7 copies diaries, 4 setmanals, 6 mensuals". Ell s'encarrega d'esborrar les que sobrin:

```bash
restic -r /mnt/ssd-backup/bernatlab forget \
  --keep-daily 7 \
  --keep-weekly 4 \
  --keep-monthly 6 \
  --prune
```

## Borg Backup: l'alternativa mes popular

**BorgBackup** (o `borg`) es similar a restic pero mes madur i mes rapid en alguns escenaris. Va ser l'inspiracio de restic. Diferencies:

| Caracteristica | restic | borg |
|---|---|---|
| Desduplicacio | Si | Si |
| Xifratge | AES-256 | AES-256 (mes opcions) |
| Compressio | Si (zstd) | Si (lz4, zstd, zlib) |
| Velocitat | Rapida | Mes rapid en grans volums |
| Autenticacio | Contrasenya | Contrasenya + keyfile |
| Destinacions | Local, SFTP, S3, REST | Local, SFTP, SSH |

Si comences de zero, **restic es mes facil** d'aprendre. Si ja tens experiencia amb borg, segueix amb borg.

## rsync: el mes basic pero sovint suficient

`rsync` es una ordre de 25 anys que copia fitxers de manera incremental. No te versionat ni xifratge, pero es perfecta per sincronitzar carpetes entre dos ordinadors o fer un backup simple a un disc extern.

Exemple basic:

```bash
# Sincronitzar una carpeta amb un disc extern
rsync -av --delete /home/pi/dades/ /mnt/ssd-backup/dades/

# -a: archive (preserva permisos, dates, etc.)
# -v: verbose
# --delete: esborra al desti el que s'ha esborrat a l'origen
```

**Pros**: simple, rapid, ubiquitous (esta a tot arreu).
**Contres**: sense xifratge, sense versionat, sense verificacio automatica.

## Kopia: la novetat interessant

**Kopia** es un programa modern (2020+) que te molt bona pinta: cross-platform (Windows, Mac, Linux), amb GUI opcional, bones politiques de retencio, i suport per a multiples destinacions. Pero encara es relativament jove i te menys documentacio que restic o borg. Si t'agrada provar coses noves, dona-li una oportunitat.

## Quina triar al BernatLab?

Al BernatLab faig servir **restic** per aixo:

1. Es la que millor em convina per fer backups al núvol (Backblaze B2 via S3).
2. Les politiques de retencio son exactament el que necessito.
3. La desduplicacio fa que els backups ocupin poc espai (~10 GB per a un hort amb un any de dades).
4. La verificacio em dona tranquilitat.

Per al dia a dia faig servir **rsync** per sincronitzar carpetes entre la RPi i el SSD extern. Restic nomes s'executa un cop al dia, rsync pot anar cada hora.

## Connexions amb altres capítols

- **Cap 1** — Per que cal un estrategia 3-2-1 abans de triar eina.
- **Cap 3** — Com aplicar restic als volums Docker.
- **Cap 7** — Backups automatitzats amb cron i systemd timers.
- **Cap 9** — Xifratge de backups amb age o GPG.
