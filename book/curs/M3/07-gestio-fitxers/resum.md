# Resum — Capitol 7: Gestio de fitxers al BernatLab

## La idea clau

A mes de les bases de dades, al BernatLab tinc una quantitat important de **fitxers plans**: fotografies de l'hort, documents del curs, scripts, configuracions, manuals, fitxers dels usuaris de Nextcloud, etc. Tots aquests fitxers necessiten una **gestio organitzada**: carpetes clares, permisos correctes, una manera facil de pujar/baixar fitxers des del navegador o el mobil, i (idealment) una mena de "cloud personal" accessible des de qualsevol lloc.

En aquest capitol veurem dues eines principals: **File Browser** (un gestor de fitxers web simple) i **Nextcloud** (un núvol personal complert tipus Google Drive). També parlarem d'estructura de carpetes i bones practiques d'organitzacio.

## L'estructura de carpetes al BernatLab

Tinc una jerarquia de carpetes pensada per a que tot sigui trobable:

```
/home/pi/bernatlab/
├── apps/              # Codis font de les aplicacions que he desenvolupat
├── backups/           # Copies de seguretat locals (abans d'anar al núvol)
├── config/            # Fitxers de configuracio compartits
├── data/              # Dades de l'hort (fitxers, no BD)
├── docker/            # Tots els docker-compose.yml i .env
├── docs/              # Documentacio del BernatLab
├── influxdb/          # Dades d'InfluxDB
├── logs/              # Logs agregats de tots els serveis
├── media/             # Fotografies i videos de l'hort
├── nextcloud/         # Dades de Nextcloud (fitxers dels usuaris)
├── postgres/          # Dades de PostgreSQL
├── scripts/           # Scripts de manteniment
└── temp/              # Fitxers temporals (esborrar periodicament)
```

Aquesta estructura es **consistent** amb tots els serveis: cada servei te el seu directori a `/home/pi/bernatlab/`, i dins hi ha `data/`, `config/`, etc. Fa que sigui trivial navegar i fer backup.

## Permisos basics

Els fitxers al BernatLab segueixen aquesta politica:

- **Propietari**: `pi` (l'usuari de la RPi).
- **Grup**: `pi`.
- **Permisos**: `755` per carpetes, `644` per fitxers.
- **Excepcio**: els `.env` amb contrasenyes son `600` (nomes el propietari).

Aixo garanteix que els serveis poden llegir les seves dades pero que les contrasenyes no son accessibles per altres usuaris.

## File Browser

**File Browser** (filebrowser.org) es un gestor de fitxers web molt simple: una sola aplicacio que et permet navegar, pujar, baixar, editar i esborrar fitxers del servidor des del navegador. Es perfecte per a l'hort IoT perque:

- Es un sol binaris Go.
- Es pot posar darrere de Tailscale o un reverse proxy.
- Permet multiples usuaris amb permisos.
- Te una UI neta i intuitiva.

### Instal·lacio

```yaml
services:
  filebrowser:
    image: filebrowser/filebrowser:latest
    container_name: bernatlab-filebrowser
    restart: unless-stopped
    volumes:
      - /home/pi/bernatlab:/srv
      - /home/pi/bernatlab/filebrowser/database.db:/database.db
      - /home/pi/bernatlab/filebrowser/config.json:/config.json
    ports:
      - "127.0.0.1:8080:80"
```

### Us

Un cop instal·lat, pots accedir a `http://localhost:8080` (via Tailscale). Login per defecte: `admin` / `admin` (canvia-ho!). Despres:

- Navega per `/srv` (= `/home/pi/bernatlab/`).
- Puja fitxers amb drag & drop.
- Descarrega, edita, esborra.
- Crea usuaris addicionals amb permisos especifics.

## Nextcloud

**Nextcloud** es molt mes que un gestor de fitxers: es un **núvol personal complet** tipus Google Drive o Dropbox, pero allotjat a casa teva. Ofereix:

- Gestio de fitxers (pujar, baixar, sincronitzar, compartir).
- Calendari i contactes (substitueix Google Calendar).
- Fotos (amb reconeixement facial, AI).
- Documents colaboratius (amb Collabora o OnlyOffice).
- Notes (substitueix Google Keep).
- Sincronitzacio amb el PC/mobil (clients natius).
- App per a Android/iOS.
- Galeria de fotos.
- Xat, correu, etc.

### Quan usar Nextcloud al BernatLab

Nextcloud es perfecte si:

- Tens **familiars** que volen un núvol pero no vols dependre de Google/Microsoft.
- Vols **sincronitzar** fitxers entre PC, portatil i mobil.
- Necessites **compartir** fitxers amb enllaços segurs.
- T'agrada tenir **control total** de les teves dades.

NO es recomana si:

- Nomes necessites un gestor per a tu (File Browser es mes lleuger).
- Tens pocs fitxers (un USB n'hi hauria prou).
- La RPi es molt justa (Nextcloud consumeix bastanta RAM).

### Instal·lacio basica

```yaml
services:
  nextcloud:
    image: nextcloud:28-apache
    container_name: bernatlab-nextcloud
    restart: unless-stopped
    depends_on:
      - nextcloud-db
    environment:
      POSTGRES_HOST: nextcloud-db
      POSTGRES_DB: nextcloud
      POSTGRES_USER: nextcloud
      POSTGRES_PASSWORD: ${NEXTCLOUD_DB_PASSWORD}
      NEXTCLOUD_ADMIN_USER: bernat
      NEXTCLOUD_ADMIN_PASSWORD: ${NEXTCLOUD_ADMIN_PASSWORD}
      NEXTCLOUD_TRUSTED_DOMAINS: localhost,nextcloud.bernatlab
    volumes:
      - /home/pi/bernatlab/nextcloud:/var/www/html
    ports:
      - "127.0.0.1:8081:80"

  nextcloud-db:
    image: postgres:16-alpine
    container_name: bernatlab-nextcloud-db
    restart: unless-stopped
    environment:
      POSTGRES_DB: nextcloud
      POSTGRES_USER: nextcloud
      POSTGRES_PASSWORD: ${NEXTCLOUD_DB_PASSWORD}
    volumes:
      - /home/pi/bernatlab/nextcloud-db:/var/lib/postgresql/data
```

### Us

Un cop instal·lat, accedeix a `http://localhost:8081` (via Tailscale). Crea els usuaris que vulguis. Instal·la el client al PC i mobil per sincronitzacio automatica.

## Bones practiques d'organitzacio

1. **Noms de carpetes sense espais ni accents**: `media-hort/` millor que `Mitjans Hort/`. Facilita scripting.
2. **Dates en format ISO**: `2025-06-15_tall-tomaqueres.jpg` millor que `tall tomaqueres.jpg`.
3. **Una sola font de veritat**: si tens un fitxer, no el tinguis en 5 llocs.
4. **README.md a cada carpeta important**: explica que hi ha allà.
5. **Neteja periodica**: cada trimestre revisa `/tmp/` i les carpetes temporals.
6. **Permisos estrictes**: `600` per secrets, `755` per carpetes, `644` per fitxers.
7. **Noms amb versio**: per documents importants, `manual-v1.md`, `manual-v2.md` (millor que `manual.md` que pot canviar sense avis).

## Connexions amb altres capítols

- **Cap 1** — Les dades son fitxers + bases de dades. Tots dos cal backupejar-los.
- **Cap 3** — Els fitxers als volums Docker.
- **Cap 8** — Syncthing i rsync per sincronitzar.
- **Cap 9** — Xifrar els fitxers sensibles.
