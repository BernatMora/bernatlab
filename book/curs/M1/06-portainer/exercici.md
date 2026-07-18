# Exercici pràctic — Capítol 6: Portainer

> 45-60 min · Real al teu sistema

## Objectiu

Posar en marxa Portainer, accedir-hi des del navegador, practicar les operacions bàsiques d'administració de contenidors i volums, i entendre quan convé la GUI i quan la terminal.

## Requisits
- Docker instal·lat (cap 5)
- Tailscale actiu
- 45-60 minuts

## Pas 1: Afegeix Portainer al compose (10 min)

Edita `~/homelab/docker/docker-compose.yml`:

```yaml
version: "3.9"

services:
  portainer:
    image: portainer/portainer-ce:latest
    container_name: portainer
    ports:
      - "9000:9000"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - portainer_data:/data
    restart: unless-stopped

  whoami:
    image: traefik/whoami
    container_name: whoami
    ports:
      - "8080:80"
    restart: unless-stopped

volumes:
  portainer_data:
```

```bash
cd ~/homelab/docker
docker compose up -d
docker compose ps
```

## Pas 2: Primer accés (10 min)

1. Obre el navegador a `http://hortosona:9000` (o `http://100.x.y.z:9000`).
2. Crea l'usuari admin (contrasenya forta, ≥ 12 caràcters).
3. Tria "Get Started" (entorn Local).
4. Explora el Dashboard.

**Important**: no exposis Portainer a Internet. Mantén-lo dins de Tailscale.

## Pas 3: Explora els contenidors (10 min)

A Portainer:

1. Clica "Containers" al menú lateral.
2. Hauries de veure `portainer` i `whoami` actius.
3. Clica sobre `whoami`:
   - Pestanya "Logs": veuràs les peticions HTTP (si n'hi ha).
   - Pestanya "Stats": CPU/RAM en temps real.
   - Pestanya "Console": connecta't a una shell (no totes les imatges tenen shell; `alpine` sí).
   - Pestanya "Inspect": tota la configuració en JSON.
4. Clica "Restart" i observa com canvia l'estat.

Prova de fer:

```bash
# Des del teu portàtil
curl http://hortosona:8080
# Torna a mirar els logs a Portainer; veuràs la petició.
```

## Pas 4: Prova d'aturar i reiniciar (5 min)

1. A Portainer, selecciona `whoami`.
2. Clica "Stop". L'estat passa a "stopped".
3. Comprova des de la terminal: `docker ps -a` mostrarà `whoami` aturat.
4. Torna a Portainer, clica "Start".
5. Comprova de nou: `docker ps` mostrarà `whoami` actiu.

Això demostra que Portainer no és "res més" que una interfície sobre la terminal. Tot el que fas per GUI, ho podries fer per SSH.

## Pas 5: Gestió de volums (5 min)

1. A Portainer, vés a "Volumes".
2. Hauries de veure `portainer_data`.
3. Clica sobre ell i navega pel contingut amb "Browse".
4. No esborris cap volum sense saber què fas.

Compara amb la terminal:

```bash
docker volume ls
docker volume inspect portainer_data
```

## Pas 6: Crea un Stack des de Portainer (10 min)

1. A Portainer, vés a "Stacks" > "Add stack".
2. Nom: `prova-stack`.
3. Build method: "Web editor".
4. Enganxa:
   ```yaml
   services:
     nginx-test:
       image: nginx:alpine
       ports:
         - "8082:80"
   ```
5. Clica "Deploy the stack".
6. Comprova: `docker ps` ha de mostrar `prova-stack-nginx-test` (o similar).
7. Accedeix a `http://hortosona:8082`.

Aquest mètode és útil per a proves ràpides, però recorda: al BernatLab preferim mantenir-ho tot al `docker-compose.yml` del sistema de fitxers (i sota Git).

## Pas 7: Configura alertes bàsiques (5 min)

Portainer porta monitoratge, però el seu valor real és l'agregació visual. Mira:

1. A "Containers", clica sobre un contenidor.
2. Pestanya "Stats": observa el gràfic de CPU i RAM.
3. Si tens 4-5 contenidors, mira el "Dashboard" principal.
4. Compara amb `docker stats` per SSH. Quina diferència hi ha?

## Pas 8: Neteja i documenta

```bash
# Esborra el stack de prova des de Portainer (o via terminal)
docker compose -p prova-stack down

# Comprova que tot torna a l'estat anterior
docker ps

# Documenta a book/curs/M1/06-portainer/diari.md
```

## Validació

Has acabat si:
- [ ] Portainer corre i hi accedeixes des del navegador.
- [ ] Has creat l'usuari admin amb contrasenya forta.
- [ ] Has vist l'estat dels contenidors.
- [ ] Has vist els logs d'un contenidor.
- [ ] Has vist les mètriques (CPU/RAM) en temps real.
- [ ] Has aturat i reiniciar un contenidor des de Portainer.
- [ ] Has navegat pels volums.
- [ ] Has creat un Stack des del Web editor.
- [ ] Has esborrat el stack de prova correctament.
- [ ] Has documentat l'experiència.

## Per aprofundir

- Configura l'editor de Portainer com a principal (no usar la GUI per crear stacks, només administrar).
- Prova d'afegir un Agent remot (per administrar una altra RPi).
- Explora els App Templates preconfigurats.
- Llegeix sobre les "Edge Agents" per a entorns distribuïts.
- Investiga com configurar rols d'usuari a Portainer.
- Compara el rendiment de Portainer amb altres eines com Yacht o Dockge.

## Ves un pas més enllà

**Repte avançat: backup i restauració de Portainer**.

Portainer té tota la configuració dels teus contenidors. Si la RPi es mor, perdre-ho tot seria un drama. Aprèn a fer-ne backup:

```bash
# Atura Portainer temporalment (per consistencia)
docker stop portainer

# Fes un tar del volum
sudo tar -czvf ~/homelab/backups/portainer-backup-$(date +%Y%m%d).tar.gz \
  -C /var/lib/docker/volumes/portainer_data/_data .

# Torna a aixecar Portainer
docker start portainer

# Comprova que el backup existeix
ls -lh ~/homelab/backups/
```

Ara restaura'l en un altre lloc per veure que funciona:

```bash
# Crea un directori de prova
mkdir -p /tmp/portainer-restore-test
cd /tmp/portainer-restore-test
tar -xzvf ~/homelab/backups/portainer-backup-*.tar.gz

# Mira quins fitxers tens
ls -la

# Neteja
rm -rf /tmp/portainer-restore-test
```

Ara imagina que la teva microSD s'ha mort. Has comprat una RPi nova i has tornat a instal·lar Debian + Docker. Què faries per recuperar l'estat exacte dels teus serveis?

Documenta-ho a `book/curs/M1/06-portainer/diari.md` sota l'apartat "Pla de recuperació de desastres".
