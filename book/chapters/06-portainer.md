# Capítol 6 — Portainer

> *"Portainer és la finestra al cor de Docker. Sense ella, hem de saber totes les ordres; amb ella, podem tocar-ho tot amb el ratolí."*

## 6.1 Què és Portainer

Portainer Community Edition (CE) és una **interfície web de codi obert** per gestionar entorns Docker. Ens permet, des d'un navegador, veure i controlar contenidors, imatges, volums, xarxes, piles, serveis i configuracions — tot allò que, des de la línia d'ordres, requeriria desenes de comandes diferents.

Portainer va néixer el 2016 com una eina per a administradors que volien una manera més visual de gestionar contenidors. Avui és l'eina estàndard de facto per a homelabs i petites empreses. La versió CE (gratuïta) cobreix tot el que necessitem al BernatLab. La versió comercial (Business) afegeix funcionalitats que, per al nostre cas, serien supèrflues.

Portainer es connecta al **socket de Docker** (`/var/run/docker.sock`), que és l'API interna que Docker exposa per a la gestió. A través d'aquest socket, Portainer pot fer exactament el que faríem nosaltres des de la consola, però amb una interfície gràfica, gràfics, formularis, cerques, filtres.

## 6.2 Per què l'utilitzem

Hi ha servidors professionals que opten per no instal·lar Portainer i gestionar-ho tot des de la consola. Té els seus arguments: una eina menys, una superfície d'atac menor, un coneixement més profund de Docker. Però al BernatLab, Portainer ens aporta molt:

- **Visibilitat immediata**. Obrim el navegador i veiem tots els contenidors, el seu estat, l'ús de CPU/RAM, els ports exposats, les dates de creació. En un cop d'ull, sabem com està el sistema.
- **Operacions ràpides**. Reiniciar un contenidor, veure els seus logs, inspeccionar el seu sistema de fitxers, accedir a una consola — tot amb un parell de clics.
- **Punt d'entrada per a gent no tècnica**. Si algun dia algú altre ha de tocar el sistema (un company, un familiar), Portainer és molt més amable que la consola.
- **Documentació visual**. Quan expliquem com és el BernatLab, una captura de Portainer val més que mil descripcions.

Això no vol dir que abandonem la consola. Al contrari: Portainer ens servirà per a operacions puntuals, consulta ràpida, i per ensenyar. Per a canvis importants (configuracions, actualitzacions, desplegaments) continuarem treballant amb fitxers `docker-compose.yml` i ordres de línia de comandes.

## 6.3 Instal·lació al BernatLab

Portainer ja està instal·lat a `https://100.x.y.z:9443`. Vegem com s'ha fet i què hi ha configurat.

### Definició al docker-compose.yml

```yaml
services:
  portainer:
    image: portainer/portainer-ce:latest
    container_name: portainer
    restart: unless-stopped
    ports:
      - "9443:9443"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - /home/bernat/homelab/data/portainer:/data
```

Tres aspectes a notar:

1. **El port 9443** és el port HTTPS de Portainer. Noteu que no és el 9000 estàndard, sinó el 9443, que és el port segur. El 9000 encara existeix com a alternativa HTTP, però el 9443 és el recomanat.
2. **`/var/run/docker.sock`**: muntat dins del contenidor. Això és el que permet a Portainer parlar amb el dimoni de Docker de l'amfitrió. Sense això, Portainer no podria fer res.
3. **`/home/bernat/homelab/data/portainer`**: bind mount a la nostra carpeta, on es guardarà la configuració i la base de dades de Portainer.

### Primer accés

La primera vegada que entrem a `https://100.x.y.z:9443`, el navegador ens mostrarà un avís de certificat no vàlid — és normal, perquè Portainer genera un certificat autosignat en instal·lar-se. Cal acceptar l'avís (a Chrome, "Configuració avançada → Continua").

A continuació, ens demanarà crear un usuari administrador. Triarem una contrasenya forta, perquè Portainer té el control absolut del Docker de la màquina.

Un cop dins, ens portarà a la **vista local** (Local environment), que és l'entorn Docker de la nostra Raspberry.

## 6.4 Interfície: vista general

Quan entrem, veiem el **dashboard** amb:

- Una graella de targetes amb estadístiques: nombre de contenidors actius, aturats, imatges, volums, xarxes.
- Una gràfica d'ús de recursos (CPU, memòria).
- Un llistat dels contenidors en execució.

A la part superior hi ha la **barra de navegació** amb:

- **Home**: vista general.
- **Stacks**: agrupacions de serveis basades en fitxers Compose.
- **Containers**: tots els contenidors, actius i aturats.
- **Images**: imatges Docker presents a la màquina.
- **Volumes**: volums i bind mounts.
- **Networks**: xarxes Docker.
- **Configs**: configuracions de Docker Swarm (no les farem servir).
- **Events**: registre d'esdeveniments del sistema.

A l'esquerra, una barra lateral ens permet canviar d'entorn (per defecte, l'entorn local) i accedir a la configuració.

## 6.5 Gestió de contenidors

La secció **Containers** és la que més farem servir. Aquí veiem tots els contenidors, amb columnes que ens indiquen:

- **Nom**: l'identificador del contenidor.
- **Estat**: running, stopped, paused, exited.
- **Imatge**: la imatge a partir de la qual es va crear.
- **Ports**: ports exposats a l'amfitrió.
- **Acció**: botons ràpids.

Si cliquem sobre un contenidor concret, accedim a una vista detallada amb:

- **Logs**: sortida estàndard i d'error del contenidor, en directe. Molt útil per diagnosticar errors.
- **Inspect**: la configuració completa del contenidor en format JSON.
- **Stats**: ús de CPU, memòria, xarxa, en temps real.
- **Console**: una consola dins del contenidor (`/bin/sh` o `/bin/bash`, segons la imatge).
- **Volumes**: la llista de volums i bind mounts del contenidor.
- **Network**: les xarxes a les quals està connectat.

### Accions habituals

- **Start / Stop / Restart**: arrencar, aturar, reiniciar un contenidor.
- **Kill**: aturar de forma forçada (equivalent a `docker kill`).
- **Pause / Unpause**: pausar temporalment.
- **Remove**: esborrar el contenidor.
- **Recreate**: tornar a crear el contenidor amb la mateixa configuració.
- **Duplicate / Export**: opcions avançades que rarament usarem.

A la pràctica, el 80% del temps estarem mirant **Logs** (per entendre errors) i fent **Restart** (per recuperar serveis).

## 6.6 Stacks: una capa d'organització

Una **Stack** a Portainer és un grup de serveis definits en un fitxer `docker-compose.yml`. La gràcia és que podem:

- Crear una nova stack des del navegador, enganxant un fitxer `docker-compose.yml`.
- Desplegar-la amb un clic.
- Editar-la visualment.
- Aturar-la, reiniciar-la, esborrar-la.

Al BernatLab, podem organitzar les piles per temàtica:

```
homelab/
├── stacks/
│   ├── core/         → portainer, homepage, uptime-kuma
│   ├── monitoring/   → grafana, influxdb
│   ├── data/         → postgres, filebrowser
│   ├── iot/          → mosquitto, node-red
│   └── media/        → pi-hole, nginx-proxy
```

Cadascuna amb el seu `docker-compose.yml`. A Portainer, les podem veure totes, cadascuna amb el seu estat.

## 6.7 Imatges

La secció **Images** ens mostra totes les imatges Docker presents a la màquina. Podem:

- Veure mida, data de creació, etiqueta, ID.
- **Pull** una nova imatge des d'un registre.
- **Build** una imatge a partir d'un Dockerfile.
- **Push** una imatge a un registre.
- **Remove** imatges que no usem.
- **Prune** per netejar les imatges penjant (dangling).

Al BernatLab, és bona pràctica fer un **prune** periòdicament per alliberar espai. Les imatges no usades es poden acumular ràpidament, especialment després d'actualitzacions.

## 6.8 Volums

La secció **Volumes** ens permet gestionar l'emmagatzematge persistent. Hi trobarem:

- **Volums anomenats** (els que Docker crea automàticament quan usem `volumes: nom_volum`).
- **Bind mounts** apareixen aquí, encara que tècnicament no són volums gestionats per Docker, sinó carpetes de l'amfitrió.

Podem veure la mida de cada volum (útil per entendre què ocupa espai), inspeccionar-los, i esborrar-los. Compte: esborrar un volum equival a perdre les dades que conté. Feu-ho només si esteu segurs.

## 6.9 Xarxes

La secció **Networks** ens mostra les xarxes Docker. Per defecte, n'hi ha tres:

- **bridge**: la xarxa per defecte, a la qual es connecten tots els contenidors que no especifiquem una xarxa.
- **host**: una xarxa especial que fa que el contenidor comparteixi la xarxa de l'amfitrió (no l'usarem).
- **none**: sense xarxa.

Quan usem `docker compose`, es crea una xarxa nova per a cada projecte. A Portainer les podem veure totes.

## 6.10 Configuració i seguretat

A la configuració de Portainer podem:

- Canviar la contrasenya de l'usuari administrador.
- Afegir altres usuaris (útil si volem donar accés a algú amb permisos limitats).
- Definir equips (teams) per organitzar accessos.
- Configurar el registre d'esdeveniments.
- Veure les estadístiques d'ús de Portainer.

**Recomanació de seguretat**: si no l'estem fent servir, podem aturar temporalment el contenidor. Però compte: si l'aturem i volem tornar a entrar, ho haurem de fer des de la consola amb `docker compose up -d`. Una bona política és mantenir Portainer sempre actiu, però limitar-ne l'accés a la xarxa Tailscale — cosa que ja fem, perquè el port 9443 no està exposat a Internet.

## 6.11 Quan NO usar Portainer

Portainer és una eina fantàstica, però hi ha casos en què la consola és millor:

- **Edició de fitxers de configuració**. Canviar el `docker-compose.yml` directament al fitxer de l'amfitrió és més transparent que fer-ho des de la interfície de Portainer, que desa el fitxer a la seva pròpia base de dades.
- **Automatització**. Si volem scriptar accions, hem d'usar la consola o l'API de Docker, no pas la interfície gràfica.
- **Aprenentatge**. Si volem entendre bé Docker, hem de fer servir les seves ordres, no pas una eina que les amaga.

Al BernatLab, **la consola és la nostra eina principal** i Portainer és el complement visual. Aquest és l'equilibri correcte.

## 6.12 Exemples d'operacions

### Veure els logs en directe d'un contenidor

A Portainer: Containers → uptime-kuma → Logs → Live (botó de seguiment).

Equivalent a la consola:

```bash
docker logs -f uptime-kuma
```

### Inspeccionar un contenidor

A Portainer: Containers → portainer → Inspect.

Equivalent a la consola:

```bash
docker inspect portainer
```

### Obrir una consola dins d'un contenidor

A Portainer: Containers → homepage → Console → connectar.

Equivalent a la consola:

```bash
docker exec -it homepage bash
```

### Veure l'ús de recursos en temps real

A Portainer: Containers → un contenidor qualsevol → Stats.

Equivalent a la consola:

```bash
docker stats
```

### Netejar imatges antigues

A Portainer: Images → Prune.

Equivalent a la consola:

```bash
docker image prune -a
```

## 6.13 Errors habituals

**Error 1: oblidar que Portainer pot fer molt de mal**. Si accidentalment esborrem un volum, podem perdre dades. Compte amb l'opció **Remove** — assegureu-vos de què esteu esborrant.

**Error 2: deixar Portainer exposat a Internet**. Si per error exposem el port 9443 a la xarxa pública, algú podria accedir-hi i fer malbé tot el sistema. Al BernatLab, el port 9443 només és accessible des de Tailscale.

**Error 3: confiar massa en Portainer i oblidar la consola**. Si Portainer falla (per exemple, per un error en una actualització), necessitarem poder arreglar les coses des de la consola. Per això, sempre hem de saber què està passant per sota.

## 6.14 Resum

Portainer ens dóna una interfície visual per gestionar tot el sistema Docker de la Raspberry: contenidors, imatges, volums, xarxes, piles. L'hem d'usar com a complement de la consola, no pas com a substitut. Al BernatLab ja el tenim configurat i és la nostra eina de consulta ràpida. En el proper capítol veurem Uptime Kuma, l'eina que ens avisa quan alguna cosa falla.

## 6.15 Exercicis pràctics

1. Entra a `https://100.x.y.z:9443` i explora el dashboard.
2. Compta quants contenidors hi ha actius. Compara'l amb la sortida de `docker ps`.
3. Mira els logs en directe d'Homepage durant 30 segons.
4. Entra dins del contenidor de Uptime Kuma amb la consola de Portainer i executa `ls /app`. Què hi ha?
5. A la secció Imatges, comprova quantes imatges hi ha i quant ocupen en total.
6. A la secció Volums, identifica els volums de cada servei. Quins són bind mounts i quins són volums gestionats per Docker?
7. Fes un `prune` d'imatges no usades. Compte! Primer comprova que tens espai.

Comandes útils equivalents a accions de Portainer:
```bash
docker ps                    # Containers
docker logs -f nom           # Logs en directe
docker inspect nom           # Detalls
docker exec -it nom bash     # Consola
docker stats                 # Recursos
docker image prune -a        # Neteja imatges
```

Paraules clau: **Portainer, dashboard, contenidor, logs, exec, prune, socket, stack, bind mount, interfície gràfica, homelab**.
