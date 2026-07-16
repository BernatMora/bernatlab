# Exercici practic — Capitol 2: Restic i alternatives modernes de backup

> 30-45 min · Real al teu sistema

## Objectiu

Instalar **restic** a la teva Raspberry Pi, crear un repo local, fer el primer backup, restaurar un fitxer, i practicar les politiques de retencio. Tot amb dades de prova, sense tocar res productiu.

## Requisits

- Tailscale actiu
- Connexio SSH a la RPi
- Un directori amb alguns fitxers per fer proves (crearem un de zero)
- 30-45 minuts

## Pas 1: Instal·la restic (5 min)

```bash
# Comprova si ja el tens
restic version

# Si no, instal·la'l
sudo apt update
sudo apt install -y restic

# Verifica la versio
restic version
# Hauria de mostrar algo com: restic 0.16.x compiled with go1.21.x
```

## Pas 2: Crea dades de prova (5 min)

```bash
# Crea un directori amb dades falses
mkdir -p /tmp/prova-restic/dades
cd /tmp/prova-restic/dades

# Genera 100 fitxers petits
for i in $(seq 1 100); do
  echo "Dades de prova $i - $(date)" > "fitxer-$i.txt"
done

# Crea un parell de fitxers grans (10 MB)
dd if=/dev/urandom of=gran-1.bin bs=1M count=10 2>/dev/null
dd if=/dev/urandom of=gran-2.bin bs=1M count=10 2>/dev/null

# Comprova
ls -lh /tmp/prova-restic/dades
# Hauries de veure ~100 fitxers petits + 2 fitxers de 10M
```

## Pas 3: Inicialitza el repo i fes el primer backup (10 min)

```bash
# Crea el directori del repo
mkdir -p /tmp/prova-restic/repo

# Inicialitza el repo (et demanara una contrasenya)
export RESTIC_PASSWORD="prova-1234-bona"
restic -r /tmp/prova-restic/repo init

# Fes el primer backup
restic -r /tmp/prova-restic/repo backup /tmp/prova-restic/dades

# Observa la sortida: 
# - "processed N files"
# - "added to repo: X MiB" (aixo es el que ocupa DESPRES de desduplicar)
# - "snapshot abc123 saved"

# Comprova quants snapshots tens
restic -r /tmp/prova-restic/repo snapshots
```

## Pas 4: Practica amb backups incrementals (10 min)

```bash
# Modifica alguns fitxers
echo "Modificat $(date)" >> /tmp/prova-restic/dades/fitxer-1.txt
echo "Nou fitxer" > /tmp/prova-restic/dades/nou-1.txt

# Fes un segon backup
restic -r /tmp/prova-restic/repo backup /tmp/prova-restic/dades

# Fixa't en "added to repo": hauria de ser molt mes petit (~1-2 KB)
# pero el snapshot conte TOTS els fitxers (antics i nous)

# Compara
restic -r /tmp/prova-restic/repo snapshots
# Ja tens 2 snapshots
```

## Pas 5: Restaura un fitxer (5 min)

```bash
# Esborrem un fitxer important
rm /tmp/prova-restic/dades/gran-1.bin

# Comprovem que no hi es
ls /tmp/prova-restic/dades/gran-1.bin
# ls: cannot access... No such file or directory

# El restaurem
mkdir -p /tmp/prova-restic/restaurat
restic -r /tmp/prova-restic/repo restore latest \
  --target /tmp/prova-restic/restaurat \
  --include /tmp/prova-restic/dades/gran-1.bin

# Comprovem
ls -lh /tmp/prova-restic/restaurat/tmp/prova-restic/dades/gran-1.bin
# Ja el tenim de tornada!
```

## Pas 6: Politiques de retencio (10 min)

```bash
# Primer, fem 5 backups seguits amb petites modificacions
for i in 1 2 3 4 5; do
  echo "iteracio $i - $(date)" > /tmp/prova-restic/dades/iteracio-$i.txt
  restic -r /tmp/prova-restic/repo backup /tmp/prova-restic/dades > /dev/null
  sleep 1
done

# Comprova: tens 7 snapshots (2 d'abans + 5 de nous)
restic -r /tmp/prova-restic/repo snapshots

# Aplica una politica: nomes 3 diaries
restic -r /tmp/prova-restic/repo forget --keep-daily 3 --prune

# Comprova
restic -r /tmp/prova-restic/repo snapshots
# Ara nomes tens 3 (o menys, pero la politica esta aplicada)
```

## Validacio

Has acabat si:

- [ ] Has instal·lat restic correctament.
- [ ] Has inicialitzat un repo.
- [ ] Has fet almenys 2 backups i has vist que el segon es mes petit (desduplicacio).
- [ ] Has restaurat un fitxer esborrat amb exit.
- [ ] Has aplicat una politica de retencio i has vist que s'esborren snapshots antics.

## Per aprofundir

- Prova de fer un repo a `/mnt/ssd-extern/backup` en lloc de `/tmp`.
- Investiga com connectar restic a un servei S3 (Backblaze B2, AWS S3, Minio).
- Compara l'espai que ocupa el repo amb `du -sh /tmp/prova-restic/repo` vs l'espai original.
- Prova `restic check` per verificar la integritat del repo.
