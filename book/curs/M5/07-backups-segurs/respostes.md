# Respostes - Capitol 7: Backups segurs

> Mira les respostes DESPRES d'haver fet el qüestionari.

## Pregunta 1: Regla 3-2-1

**Resposta correcta**: 3 copies, 2 mitjans diferents, 1 fora de casa.

**Explicacio**: La regla 3-2-1 es la base de qualsevol estrategia de backup seriosa. **3** copies minim, per si una falla. **2** mitjans diferents (per exemple: disc local + núvol), perque una fallada de hardware no afecti ambdos. **1** copia fora de casa (cloud, casa d'un amic, altre edifici), per si hi ha un incendi o un robatori que destrueixi tot el que tens a casa.

---

## Pregunta 2: Que es Restic?

**Resposta correcta**: Una eina de backup moderna, xifrada, incremental i deduplicada.

**Explicacio**: Restic es una eina de backup de linia de comandes escrita en Go, llicencia BSD. Te totes les funcionalitats que voldries en una eina de backup professional: xifratge AES-256, backups incrementals, deduplicacio, suport per multiples backends (local, S3, SFTP, B2, etc.), compresio opcional, i verificacio d'integritat. Es l'eina de referencia per a homelabs.

---

## Pregunta 3: Per que xifrar?

**Resposta correcta**: Perque si el backup es robat o filtrat, les dades no son llegibles.

**Explicacio**: Un backup conte totes les teves dades: configuracions amb secrets, documents personals, bases de dades. Si el backup es al núvol, qualsevol que obtingui acces al compte pot veure-ho tot. Si el disc es roba fisicament, el mateix. Xifrant el backup, nomes tu (amb la teva clau) pots llegir-lo. Es una mesura obligatoria, no opcional.

---

## Pregunta 4: Perdre la clau

**Resposta correcta**: No pots restaurar mai, les dades son il·legibles per sempre.

**Explicacio**: Restic usa xifratge autenticat AES-256, pero la clau es l'unica manera de desxifrar. Si la perds, Restic no te cap "backdoor" ni cap manera de recuperar les dades. Aixo es per disseny: la seguretat es basa en que nomes tu tens la clau. Per tant, **guarda la clau al vault** (capitol 6) i en un altre lloc (paper en una caixa forta, per exemple). Si nomes la tens al cap, el dia que t'oblidis has perdut tot.

---

## Pregunta 5: Llistar snapshots

**Resposta correcta**: `restic snapshots`.

**Explicacio**: La comanda `restic snapshots` llista tots els snapshots existents al repositori, amb la data, l'ID, el hostname, i la mida. Es la comanda que fas servir per saber quines copies tens. Combinada amb `restic ls` pots veure quins fitxers conte cada snapshot.

---

## Pregunta 6: Incremental

**Resposta correcta**: Nomes es copia el que ha canviat desde l'ultim backup.

**Explicacio**: Un backup incremental nomes copia els fitxers nous o modificats. Això fa que cada backup sigui rapid i ocupi poc espai. Restic es intel·ligent: nomes copia les parts que han canviat dins dels fitxers grans, no tot el fitxer. Combinat amb deduplicacio, els backups successius ocupen molt poc.

---

## Pregunta 7: Risc del backup sense proves

**Resposta correcta**: Que no es pugui restaurar quan el necessitis.

**Explicacio**: Hi ha una dita en el mon dels backups: "un backup no es un backup fins que no l'has restaurat amb exit". Molts cops els administradors descobreixen que el seu backup esta corrupte, incomplet, o apuntant a un directori buit, **el dia que el necessiten**. Per evitar-ho, cal fer **proves de restauracio** periodiques (cada 3-6 mesos).

---

## Pregunta 8: Backend mes economic

**Resposta correcta**: Backblaze B2 (~$6/TB/mes).

**Explicacio**: Backblaze B2 es molt mes economic que AWS S3 o Google Cloud. Cobra $6 per TB al mes d'emmagatzematge i $0.01 per GB de transferencia. Aixo ho fa ideal per a homelabs on el pressupost es limitat. Alternatives: Hetzner Storage Box (4 EUR/TB/mes), rsync.net ($0.06/GB/any), o un simple disc USB rotat fora de casa.

---

## Pregunta 9 (oberta): Politica de backups

**Resposta model**:

Aquesta es la politica que jo aplicaria al BernatLab. Assumeixo una RPi amb Home Assistant, Gitea, Portainer, una base de dades Postgres, i configuracions a `/etc/nginx` i `/opt/homelab`. 

**Que backupejar**:

- **Bases de dades**: Postgres dump cada dia. Aixo es el mes critic, es on son les dades.
- **Volums Docker**: `/var/lib/docker/volumes/gitea-data`, `/var/lib/docker/volumes/homeassistant`, etc. Son configuracio i estat dels serveis.
- **Configuracions del sistema**: `/etc/nginx`, `/etc/caddy`, `/etc/ssh/sshd_config`, `/opt/homelab/docker-compose.yml`.
- **Secrets**: `/opt/homelab/.env` (xifrat per Restic), claus SSH, configuracio de Tailscale.
- **Repositoris Git**: `/var/lib/docker/volumes/gitea-data/git` (Gitea ja te una comanda `gitea dump` que es mes consistent).
- **Logs importants** (opcional): `/var/log` nomes els de fail2ban i ufw.

**On guardar-los**:

- **Local**: `/var/backups/homelab` amb Restic, en un disc USB extern si la RPi te ports USB.
- **Núvol**: Backblaze B2, amb un altre repositori Restic separat. Es economic i fiable.

Aplica la **3-2-1**: original + local (disc USB) + núvol (B2) = 3 copies, 2 mitjans, 1 fora de casa.

**Cada quan**:

- **Diari** a les 3 de la matinada (hora de minima activitat).
- **Incremental sempre**: Restic ja ho fa per defecte.
- **Verificar setmanalment** que el backup s'ha fet be (un script que mira la mida i envia alerta si es 0 o massa petita).

**Politica de retencio**:

```bash
restic forget \
  --keep-hourly 24 \
  --keep-daily 7 \
  --keep-weekly 4 \
  --keep-monthly 6 \
  --prune
```

Aixo em dona:

- 24 copies de les ultimes 24 hores (cada hora, en cas d'atac o desastre).
- 7 copies diaries (una setmana).
- 4 copies setmanals (un mes).
- 6 copies mensuals (un mig any).

Si necessito algo d'un moment concret, puc restaurar de fa 1 hora, 1 dia, 1 setmana, o fins i tot 6 mesos. Suficient per a qualsevol cas d'error huma o atac.

**Com verificar que funciona**:

- **Prova de restauracio cada 3 mesos**: restauro l'ultim snapshot a un directori temporal, miro que les dades siguin correctes, esborro.
- **Monitoratge**: un cron que cada dia mira si el backup s'ha fet, i envia un correu si ha fallat.
- **Verificar la mida**: si de sobte el backup creix molt, pot ser un problema (atac amb dades noves, o un bug que generi fitxers brossa).
- **Verificar amb `restic check`**: aquesta comanda llegeix tots els snapshots i comprova la seva integritat.

**Automatitzacio**:

- Un script `/opt/homelab/scripts/backup.sh` que faci el backup, la retencio, i la verificacio.
- Un timer de systemd o un cron que l'executi cada nit.
- Logs a `/var/log/backup.log` revisables.

Amb tot això, puc afirmar amb confiança que tinc un sistema de backups robust, economic, i provat. Si algun dia passa algo, puc restaurar en minuts.

---

## Pregunta 10 (oberta): Lliço après

**Resposta model**:

Aixo es un **classic homelab mistake**: el backup al mateix disc que les dades originals. Si el disc falla, fallen les dues coses. No es un backup real, es una **copia redundant** que pot servir per errors humans puntuals (esborrar un fitxer), pero no per desastre.

**Que he après**: que un backup nomes es un backup si esta **fisicament separat** de l'original. Si el teu ordinador te un unic disc SSD i el backup esta en una carpeta del mateix disc, no es un backup. Es una mica mes d'espai al mateix lloc.

**Que faria diferent**:

**Opcio 1: disc USB extern**. Compraria un disc USB de 1-2 TB, el connectaria a la RPi, i configuraria Restic per fer backup allà. Es la solucio mes simple. A mes, el disc USB el puc desconnectar i guardar a un calaix o a la casa d'un amic. Es la "copia fora de casa" de la regla 3-2-1.

**Opcio 2: Backblaze B2 al núvol**. Configuraria un segon repositori Restic al B2, amb una clau diferent. D'aquesta manera, encara que el disc local falli, tinc una copia al núvol. Backblaze cobra $6/TB/mes, molt economic.

**Opcio 3: un altre servidor via SFTP**. Si tinc un NAS o un altre servidor a casa, puc fer backup allà per SFTP. Es la solucio mes flexible, pero cal configurar el segon servidor.

**La meva tria actual**: combinaria **local + B2**. Perque:

- El **local** es rapid (Restic nomes copia el que ha canviat, son segons).
- El **B2** es la salvaguarda si el local falla (incendi, robatori, corrent).
- El **cost** es minim: $6/mes per 1 TB, menys que un cafe.

A mes a mes, a partir d'ara faria una **prova de restauracio trimestral**. Crea un directori temporal, restauro l'ultim snapshot, comparo amb l'original, esborro. Es l'unica manera d'estar segur que el backup funciona. No esperis al dia que el necessitis per descobrir que no funcionava.

I finalment: **guardaria la clau de xifratge al vault** (capitol 6) i tambe en paper en un lloc segur. Si nomes la tens al cap, el dia que t'oblidis has perdut tot. La clau es la **master key** del sistema de backups.

---

## Que fer si has fallat moltes preguntes

- **5-8 encerts**: Rellegir el resum i fer l'exercici practic.
- **3-4 encerts**: Comença fent un backup local abans d'anar al núvol.
- **0-2 encerts**: Practica amb un directori buit abans de tocar les dades reals.

## Que fer si has encertat totes

- Passa al **Capitol 8** (Monitoratge de seguretat).
- Configura **Healthchecks.io** per saber quan el backup falla.
- Investiga **borgbackup**, una alternativa a Restic amb mes anys pero menys features.
- Llegeix sobre **Bacula** o **Amanda** si necessites una solucio enterprise.
