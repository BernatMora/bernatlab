# Resum — Capitol 8: Sincronitzacio de fitxers: Syncthing i rsync

## La idea clau

Hi ha vegades que vols **sincronitzar fitxers** entre dos ordinadors de manera continua: per exemple, que les fotos del portatil apareguin automaticament al servidor, o que els documents del servidor estiguin disponibles al teu PC. La copia manual amb USB ja no escala. En aquest capitol veurem tres eines fonamentals: **Syncthing** (P2P continu), **rsync** (sincronitzacio puntual via SSH) i esmentarem alternatives com Dropbox.

A l'hort IoT, la sincronitzacio es util per:

- Sincronitzar fotos des del mobil al servidor.
- Mantenir una copia del servidor en un altre equip.
- Compartir documents entre dispositius de la familia.
- Fer un mirror de seguretat a un altre maquina.

## Syncthing: sincronitzacio P2P continua

**Syncthing** es una eina de sincronitzacio de fitxers **peer-to-peer** (P2P), continua i open source. Es a dir:

- **No passa per cap servidor central** (com Dropbox). Els teus fitxers van directament d'un dispositiu a l'altre.
- **Es continua**: quan modifiques un fitxer a un lloc, apareix automaticament a l'altre.
- **Es xifrada**: tota la comunicacio es TLS.
- **Multiplataforma**: Windows, macOS, Linux, Android, iOS, FreeBSD, Solaris.

### Quan usar Syncthing

Syncthing es la millor opcio quan:

- Vols sincronitzar fitxers entre **dos o mes** dispositius teus.
- No vols dependre de cap **nuvol extern** (ni Google, ni Dropbox).
- T'agrada el **control total** sobre les teves dades.
- Necessites **sincronitzacio continua** (sense haver d'executar res manualment).
- Tens una **xarxa local** o pots fer **port forwarding** (o usant Tailscale).

NO es adequada quan:

- Necessites accedir des de qualsevol lloc del mon **sense VPN** (millor un nuvol real).
- Vols **compatibilitat amb tothom** (Dropbox es mes universal).
- El teu cas es nomes fer **backups unidireccionals** (millor rsync o restic).

### Instal·lacio a la RPi

```yaml
services:
  syncthing:
    image: linuxserver/syncthing:latest
    container_name: bernatlab-syncthing
    restart: unless-stopped
    hostname: bernatlab
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Europe/Madrid
    volumes:
      - /home/pi/bernatlab/syncthing/config:/config
      - /home/pi/bernatlab/syncthing/data:/data
      - /home/pi/bernatlab/hort:/hort
    ports:
      - 127.0.0.1:8384:8384  # UI
      - 22000:22000/tcp       # Connexions entrants
      - 21027:21027/udp       # Discovery
```

Un cop engegat, accedeix a `http://localhost:8384` (via Tailscale).

### Us

1. **Afegeix una carpeta compartida** a Syncthing: `Add Folder > Folder Path: /hort > Share with devices...`.
2. **Afegeix un altre dispositiu**: l'altre dispositiu tambe te Syncthing, i intercanvieu els "Device ID" (codis QR o cadenes llargues).
3. **Accepta la comparticio** a l'altre dispositiu.
4. **Sincronitzacio automatica**: qualsevol canvi a un costat es propaga a l'altre.

## rsync: sincronitzacio puntual via SSH

`rsync` es una ordre de 25 anys que sincronitza carpetes **a travas de SSH o localment**. Es **incremental** (nomes copia el que ha canviat) i es la base de molts sistemes de backup.

### Us basic

```bash
# Sincronitzacio local
rsync -av /origen/ /desti/

# Sincronitzacio remota via SSH
rsync -av -e ssh /origen/ usuari@host:/desti/

# Opcions utils:
# -a: archive (preserva permisos, dates, etc.)
# -v: verbose
# -z: comprimeix durant el transport
# --delete: esborra al desti el que ja no es a l'origen
# --progress: mostra el progres
# -n: dry-run (nomes mostra el que faria)
```

### Exemple practic

```bash
# Backup diari a un disc SSD extern
rsync -av --delete /home/pi/bernatlab/ /mnt/ssd-backup/bernatlab/

# Backup a una maquina remota via SSH
rsync -avz -e ssh /home/pi/bernatlab/hort/ \
  pi@nas.local:/volume1/backups/hort/

# Amb dry-run primer per veure que fara
rsync -avn --delete /home/pi/bernatlab/ /mnt/ssd-backup/bernatlab/
```

### Avantatges i inconvenients de rsync

**Pros**:
- Simple i universal (esta a tot arreu).
- Incremental: nomes copia el que ha canviat.
- Conserva permisos, dates, estructura.
- Es pot combinar amb SSH per seguretat.
- Es pot programar amb cron.

**Contres**:
- **Unidireccional**: nomes copia A -> B, no pas A <-> B.
- **Sense xifratge** (nomes si es via SSH).
- **Sense deteccio de conflictes**: si el mateix fitxer canvia als dos llocs, l'ultim guanya.
- **Sense interfície grafica**.

## Dropbox i alternatives modernes

Si vols alguna cosa amb nuvol real:

- **Dropbox**: classic, pero ara es mes car i te limitacions.
- **Google Drive**: 15 GB gratis, pero privacitat dubtosa.
- **OneDrive**: 5 GB gratis, integrat amb Windows.
- **iCloud**: 5 GB gratis, nomes per a Apple.
- **Proton Drive**: 1 GB gratis, xifrat i privat.

Per a un homelab, la meva recomanacio es **no usar aquests serveis** per a dades de l'hort. Millor Syncthing + un disc de backup. Si necessites un nuvol real, **Proton Drive** o **Tresorit** son mes respectuosos amb la privacitat.

## Estrategia al BernatLab

Al BernatLab faig servir:

- **Syncthing** per sincronitzar les **fotos de l'hort** entre el meu mobil Android, el portatil i el servidor. Aixi quan faig una foto amb el mobil, automaticament apareix al servidor.
- **rsync via cron** per fer una **copia diaria** a un disc SSD extern. Diferent de la copia al núvol.
- **restic** (cap 2) per fer **backups al núvol** cifrats. Es la copia "fora de casa" del 3-2-1.

Aixo cobreix els 3 objectius: sincronitzacio continua, copia local, copia remota.

## Connexions amb altres capítols

- **Cap 1** — La sincronitzacio es una part del 3-2-1 (copies en suports diferents).
- **Cap 2** — restic es la millor eina per a la copia al núvol.
- **Cap 7** — Els fitxers que sincronitzes estan organitzats a `/home/pi/bernatlab/`.
- **Cap 9** — Per sincronitzar fitxers **xifrats**, Syncthing ja ho fa, pero les dades al disc son en clar.
