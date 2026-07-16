# Exercici practic — Capitol 7: Gestio de fitxers al BernatLab

> 30-40 min · Real al teu sistema

## Objectiu

Instal·lar File Browser, crear una estructura de carpetes per a l'hort, pujar i baixar fitxers des del navegador, i explorar les opcions d'usuaris.

## Requisits

- Tailscale actiu
- Connexio SSH a la RPi
- Docker funcionant
- 30-40 minuts

## Pas 1: Crea l'estructura de carpetes (5 min)

```bash
mkdir -p /home/pi/bernatlab/hort/{media,docs,data/{sensors,plantes,collites},config}
mkdir -p /home/pi/bernatlab/hort/media/2025/06-juny
mkdir -p /home/pi/bernatlab/hort/docs/{manuals,procediments,actes}

ls -la /home/pi/bernatlab/hort/
```

## Pas 2: Crea fitxers de prova (5 min)

```bash
cat > /home/pi/bernatlab/hort/README.md <<EOF
# Hort IoT BernatLab

Aquesta carpeta conte totes les dades de l'hort.

## Estructura

- media/: Fotografies i videos
- data/sensors/: Lectures dels sensors (CSV)
- data/plantes/: Inventari de plantes
- data/collites/: Registre de collites
- docs/: Documentacio

## Notes

- Tots els fitxers segueixen el format ISO a les dates: YYYY-MM-DD
- Les carpetes no porten accents ni espais
EOF

cat > /home/pi/bernatlab/hort/data/sensors/2025-06-15.csv <<EOF
ts,sensor,valor
2025-06-15T08:00:00,temperatura,18.5
2025-06-15T08:00:00,humitat,65.0
2025-06-15T08:00:00,llum,820
EOF

ls -R /home/pi/bernatlab/hort/
```

## Pas 3: Instal·la File Browser amb Docker (10 min)

```bash
mkdir -p /home/pi/bernatlab/filebrowser

docker run -d --name bernatlab-filebrowser \
  -p 127.0.0.1:8080:80 \
  -v /home/pi/bernatlab:/srv \
  -v /home/pi/bernatlab/filebrowser/database.db:/database.db \
  -v /home/pi/bernatlab/filebrowser/config.json:/config.json \
  filebrowser/filebrowser:latest

sleep 5
docker ps | grep filebrowser
```

## Pas 4: Accedeix a File Browser (5 min)

Obre al navegador: `http://localhost:8080` (via Tailscale o tunel SSH).

Login: `admin` / `admin`.

**IMPORTANT**: ves a Settings i canvia la contrasenya d'admin immediatament.

## Pas 5: Crea un usuari (5 min)

A la UI:

1. Settings > Users > New
2. Nom: `hort-user`, Contrasenya: `hort-2025`
3. Permisos: nomes lectura per defecte
4. Permet l'acces a la carpeta `/hort`

## Pas 6: Prova pujar/baixar (5 min)

Des del navegador amb l'usuari `hort-user`:

1. Crea un fitxer nou a la carpeta `/hort/media/2025/06-juny/`.
2. Puja una fotografia de prova (una qualsevol del teu PC).
3. Descarrega-la per verificar.

## Pas 7: Permisos al sistema de fitxers (5 min)

```bash
# Permissos basics
chmod 755 /home/pi/bernatlab/hort
chmod 644 /home/pi/bernatlab/hort/README.md

# Comprova
ls -la /home/pi/bernatlab/hort/
stat /home/pi/bernatlab/hort/README.md
```

## Validacio

Has acabat si:

- [ ] Has creat l'estructura de carpetes de l'hort.
- [ ] Has instal·lat File Browser amb Docker.
- [ ] T'has connectat i has canviat la contrasenya d'admin.
- [ ] Has creat un usuari secundari.
- [ ] Has pujat i descarregat un fitxer.
- [ ] Has revisat els permisos al sistema de fitxers.

## Per aprofundir

- Investiga com configurar **permisos granulars** a File Browser (només lectura per carpeta).
- Prova de muntar la mateixa carpeta a File Browser i Nextcloud (usuaris diferents).
- Configura **autenticacio OIDC** per integrar amb altres serveis.
- Investiga com activar **HTTPS** amb un reverse proxy (Caddy o Nginx).
- Prova de substituir File Browser per **SFTPGo** (SFTP + Web UI).
