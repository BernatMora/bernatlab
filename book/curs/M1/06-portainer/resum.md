# Resum — Capítol 6: Portainer

## La idea clau

Un cop tens 5-10 serveis corrent a la Raspberry Pi, fer-los anar tot per SSH i línia de comandes es fa feixuc. **Portainer** és una interfície gràfica (web) per administrar Docker: veure contenidors, logs, volums, imatges, xarxes, i fer operacions amb un parell de clics. Al BernatLab hi accedeixes via `http://hortosona:9000` (o `http://100.115.134.76:9000` des de fora amb Tailscale).

## Què és exactament Portainer?

Portainer és un contenidor Docker (sí, un contenidor que administra altres contenidors). Comunica amb el dimoni Docker (dockerd) a través del socket `/var/run/docker.sock`. Té una versió Community (gratuïta, CE) i una Business (de pagament). Farem servir la CE.

Tecnologia: una app web feta amb Angular (frontend) i Go (backend). La versió actual (2.x) té un aspecte modern i potent.

## Per què l'usem al BernatLab?

- **Visibilitat**: veure d'un cop d'ull tots els contenidors, el seu estat, CPU, RAM.
- **Logs centralitzats**: llegir logs de qualsevol contenidor sense fer `docker logs`.
- **Control**: arrencar, parar, reiniciar, recrear, esborrar amb botons.
- **Editor de Compose**: pots editar el fitxer `docker-compose.yml` directament al navegador.
- **Stack**: gestionar múltiples serveis relacionats com una unitat.
- **Consola web**: entrar dins un contenidor amb un terminal al navegador (útil quan no tens SSH).

Per a un homelab amb 4-10 serveis, Portainer està en el sweet spot: ni massa senzill (com Dockge), ni aclaparador (com Rancher o Kubernetes Dashboard).

## Instal·lació al BernatLab

Ja ho varem fer al cap 5, però aquí el snippet per referència:

```yaml
# Afegir a ~/homelab/docker/docker-compose.yml
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

volumes:
  portainer_data:
```

```bash
cd ~/homelab/docker
docker compose up -d portainer
```

## Primer accés

1. Obre el navegador a `http://hortosona:9000` o `http://100.115.134.76:9000`.
2. La primera vegada et demana crear un usuari administrador (només triga 5 segons, no és un procés llarg).
3. Tria "Local" per administrar el Docker de la mateixa RPi.
4. Ja ets al tauler principal: un llistat dels teus contenidors amb estats i mètriques.

A partir d'aquí, gairebé tot es fa amb clics.

## El tauler (Dashboard)

A la pantalla principal veuràs:

- **Stacks**: grups de serveis definits al `docker-compose.yml`.
- **Containers**: tots els contenidors individuals.
- **Images**: imatges descarregades.
- **Networks**: xarxes Docker.
- **Volumes**: volums persistents.
- **Swarm / Kubernetes**: per si actives clústers (no és el cas a l'homelab).

## Gestió de contenidors

Per a cada contenidor pots:

- Veure **estat** (running, stopped, paused).
- Veure **mètriques** en temps real (CPU%, RAM MB, xarxa).
- **Start / Stop / Restart / Kill**.
- Veure **logs** (amb cerca, filtres).
- Entrar a la **consola** (shell dins del contenidor).
- Veure **detalls**: variables d'entorn, volums muntats, xarxes, ports exposats.
- **Recrear** (tirar i tornar a aixecar amb la mateixa config).
- **Esborrar**.

Exemple: el contenidor `uptime-kuma` ha caigut. A Portainer cliques sobre ell, veus el log ("Error: EADDRINUSE :::3001"), cliques Stop, cliques Start, i ja torna. Tot des del navegador.

## Editor de Stacks (Compose)

Un dels millors trucs: a Portainer pots pujar/modificar fitxers Compose directament. Vés a "Stacks" > "Add stack":

- **Build method**: Web editor.
- **Name**: el nom de l'stack.
- **Web editor**: enganxa el teu `docker-compose.yml` aquí.
- **Environment variables**: afegeix variables si cal.
- Clica "Deploy the stack".

Això fa `docker compose up -d` per sota. Si vols actualitzar, edites l'stack, cliques "Update", i Portainer aplica els canvis.

Alerta: si tens un `docker-compose.yml` al sistema de fitxers i un altre stack amb el mateix nom a Portainer, poden xocar. La convenció al BernatLab és: tot el `docker-compose.yml` viu al sistema de fitxers (a `~/homelab/docker/docker-compose.yml`), i a Portainer només operem sobre els contenidors individuals, no creem stacks nous des de la GUI.

## Volums i xarxes

A la secció "Volumes" pots:

- Veure tots els volums i la seva mida.
- Navegar pel contingut (Browse).
- Esborrar-ne (perillós si un contenidor actiu l'usa).
- Fer backup/restore (a la versió Business).

A "Networks" pots veure les xarxes i els contenidors connectats, però rarament tocaràs res aquí.

## Templates d'apps

Portainer té una galeria d'apps preconfigurades (WordPress, Nextcloud, Plex, etc.) que pots desplegar amb un clic. Són útils per començar ràpid, però al BernatLab preferim el `docker-compose.yml` manual per tenir control total.

## Limites i advertències

- **Una sola màquina per instància Local**: si vols administrar diverses RPi, cal la versió Business o usar l'Agent.
- **No és un substitut de la terminal**: per a operacions avançades (volums xifrats, networks complexes) millor la CLI.
- **L'accés per defecte és HTTP**: al BernatLab és acceptable perquè hi accedim via Tailscale (ja xifrat), però per a exposar-ho a Internet caldria HTTPS.

## Connexions amb altres capítols

- **Cap 5** — Portainer és un contenidor Docker que administra la resta.
- **Cap 7** — Uptime Kuma és el que monitoritza si Portainer (i la resta) estan actius.
- **Cap 8** — Homepage mostrarà enllaços ràpids cap a Portainer.
- **Cap 22** — Monitoratge més avançat (Prometheus + Grafana) deixa Portainer en un segon pla.

Amb Portainer tens el "quadre de comandament" del teu homelab. Ara toca monitoritzar-lo.
