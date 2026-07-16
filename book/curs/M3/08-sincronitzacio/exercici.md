# Exercici practic — Capitol 8: Sincronitzacio de fitxers

> 30-40 min · Real al teu sistema

## Objectiu

Instal·lar Syncthing, sincronitzar una carpeta entre dos directoris locals amb rsync, practicar rsync amb dry-run, i crear un script cron de sincronitzacio.

## Requisits

- Tailscale actiu
- Connexio SSH a la RPi
- Docker funcionant
- 30-40 minuts

## Pas 1: Crea carpetes de prova (5 min)

```bash
mkdir -p /home/pi/bernatlab/proves/sync/origen
mkdir -p /home/pi/bernatlab/proves/sync/desti
mkdir -p /home/pi/bernatlab/proves/sync/mobile

# Crea alguns fitxers
echo "hola desde l'origen" > /home/pi/bernatlab/proves/sync/origen/a.txt
echo "config 1" > /home/pi/bernatlab/proves/sync/origen/config.json

ls -la /home/pi/bernatlab/proves/sync/origen
```

## Pas 2: Practica rsync (10 min)

```bash
# Primer, dry-run (simula, no fa res)
rsync -avn /home/pi/bernatlab/proves/sync/origen/ /home/pi/bernatlab/proves/sync/desti/

# Ara la copia real
rsync -av /home/pi/bernatlab/proves/sync/origen/ /home/pi/bernatlab/proves/sync/desti/

# Comprova
ls -la /home/pi/bernatlab/proves/sync/desti/

# Modifica l'origen
echo "fitxer modificat" > /home/pi/bernatlab/proves/sync/origen/b.txt
rm /home/pi/bernatlab/proves/sync/origen/a.txt

# Torna a sincronitzar amb --delete
rsync -av --delete /home/pi/bernatlab/proves/sync/origen/ /home/pi/bernatlab/proves/sync/desti/

# Comprova: a.txt hauria d'haver desaparegut, b.txt hi hauria de ser
ls -la /home/pi/bernatlab/proves/sync/desti/
```

## Pas 3: Sincronitzar en xarxa amb rsync+SSH (5 min)

```bash
# Crea un script de sincronitzacio
cat > /home/pi/bernatlab/scripts/sync-hort.sh <<'EOF'
#!/bin/bash
# Sincronitza l'hort a un servidor remot via SSH

ORIGEN="/home/pi/bernatlab/hort/"
DESTI="pi@nas.local:/volume1/backups/hort/"

rsync -avz --delete -e ssh "$ORIGEN" "$DESTI"
EOF

chmod +x /home/pi/bernatlab/scripts/sync-hort.sh

# Prova'l (nomes si tens un servidor remot configurat; sino, salta)
# /home/pi/bernatlab/scripts/sync-hort.sh
```

## Pas 4: Instal·la Syncthing amb Docker (10 min)

```bash
mkdir -p /home/pi/bernatlab/syncthing/{config,data}

docker run -d --name bernatlab-syncthing \
  -p 127.0.0.1:8384:8384 \
  -p 22000:22000/tcp \
  -p 21027:21027/udp \
  -e PUID=1000 \
  -e PGID=1000 \
  -e TZ=Europe/Madrid \
  -v /home/pi/bernatlab/syncthing/config:/config \
  -v /home/pi/bernatlab/syncthing/data:/data \
  -v /home/pi/bernatlab/hort:/hort \
  --hostname=bernatlab \
  --restart=unless-stopped \
  linuxserver/syncthing:latest

sleep 10
docker ps | grep syncthing
```

## Pas 5: Configura Syncthing (5 min)

Obre `http://localhost:8384` (via Tailscale). Ves a **Actions > Show ID**. Copia el Device ID. (En un cas real, l'afegiries a un altre dispositiu; aco nomes per mostrar la UI.)

## Pas 6: Programa rsync amb cron (5 min)

```bash
# Edita el crontab
crontab -e

# Afegeix aquesta linia (sincronitza cada dia a les 3 de la matinada):
0 3 * * * /home/pi/bernatlab/scripts/sync-hort.sh >> /home/pi/bernatlab/logs/sync.log 2>&1

# Comprova
crontab -l
```

## Validacio

Has acabat si:

- [ ] Has practicat rsync amb dry-run i amb --delete.
- [ ] Has creat un script de sincronitzacio.
- [ ] Has instal·lat Syncthing amb Docker.
- [ ] Has accedit a la UI de Syncthing.
- [ ] Has programat una tasca cron amb rsync.

## Per aprofundir

- Investiga com configurar **ignore patterns** a Syncthing (.stignore).
- Prova de sincronitzar entre Syncthing i un client Android real.
- Compara el rendiment de rsync amb i sense compressio (-z).
- Investiga com configurar Syncthing per accedir des d'internet (Tailscale).
- Prova d'afegir **autenticacio amb clau SSH** per a rsync sense contrasenya.
