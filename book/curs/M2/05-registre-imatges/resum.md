# Resum - Capitol 5: Registre d'imatges

## La idea clau

Un **registre d'imatges** es un servidor que emmagatzema imatges Docker i les distribueix. Docker Hub es el mes conegut (es on van les imatges oficials de nginx, postgres, etc.), pero per a un homelab o una empresa es molt recomanable tenir un **registre privat** per qüestions de seguretat, velocitat i control.

## Que es un registre

Un registre es simplement una API HTTP que segueix l'estandard "Docker Registry HTTP API V2". Permet:

- Pujar imatges (`docker push`)
- Baixar imatges (`docker pull`)
- Llistar imatges i tags
- Esborrar imatges
- Gestionar permisos (autenticacio)

## Docker Hub

El registre public per defecte. Tots hi tenim un compte gratuït.

```bash
# Login
docker login

# Pujar una imatge (primer cal taggejar-la correctament)
docker tag meva-app:1.0 bernatmora/meva-app:1.0
docker push bernatmora/meva-app:1.0

# Baixar
docker pull bernatmora/meva-app:1.0
```

**Limitacions del pla gratuit**:
- 1 registre privat
- 200 pulls per 6 hores (per IP anonima)
- Imatges publiques il·limitades

## Registre privat: opcions

Hi ha diverses opcions per tenir el teu propi registre:

### 1. Docker Registry oficial (la imatge `registry`)

Es la mes simple. Es un contenidor que només fa de registre.

```bash
docker run -d -p 5000:5000 --restart=always --name registry \
  -v /home/pi/registry-data:/var/lib/registry \
  registry:2
```

Ja tens un registre funcionant a `raspberry.local:5000`. Per pujar-hi:

```bash
docker tag meva-app:1.0 raspberry.local:5000/meva-app:1.0
docker push raspberry.local:5000/meva-app:1.0
```

**Avantatges**: simple, lleuger, perfecte per a homelab.
**Desavantatges**: sense UI, sense autenticacio per defecte (cal posar un reverse proxy amb auth).

### 2. Harbor

Solucio **completa** de registre. Te UI web, autenticacio LDAP/AD, escaneig de vulnerabilitats, replicacio, etc. Es el que fan servir les empreses.

```bash
# Descarregar de https://github.com/goharbor/harbor/releases
tar xvf harbor-offline-installer-v2.x.x.tgz
cd harbor
# Editar harbor.yml
./install.sh
```

**Avantatges**: UI, seguretat, integracio LDAP, escaneig de vulnerabilitats.
**Desavantatges**: mes pesat (10-20 serveis), mes complexe.

### 3. GitHub Container Registry (ghcr.io)

Si ja tens codi a GitHub, pots usar el seu registre gratuit per a imatges Docker.

```bash
docker login ghcr.io -u bernatmora
docker tag meva-app:1.0 ghcr.io/bernatmora/meva-app:1.0
docker push ghcr.io/bernatmora/meva-app:1.0
```

**Avantatges**: integrat amb GitHub Actions, gratis per a repos publics.
**Desavantatges**: limitat a 500 MB per imatge (gratis).

### 4. Altres

- **GitLab Container Registry**: si uses GitLab.
- **AWS ECR, GCP Artifact Registry, Azure ACR**: al núvol.
- **Quay.io**: el de Red Hat, public i privat.

## Autenticacio

Sense autenticacio, el registre es obert a tothom (perill!). El `registry:2` oficial porta un sistema basic:

```bash
# Crear usuari amb htpasswd
docker run --rm --entrypoint htpasswd httpd:2 -Bbn bernat supersecret > auth/htpasswd

# Arrencar amb autenticacio
docker run -d -p 5000:5000 --restart=always --name registry \
  -v /home/pi/registry-data:/var/lib/registry \
  -v $(pwd)/auth:/auth \
  -e "REGISTRY_AUTH=htpasswd" \
  -e "REGISTRY_AUTH_HTPASSWD_REALM=Registry Realm" \
  -e "REGISTRY_AUTH_HTPASSWD_PATH=/auth/htpasswd" \
  registry:2

# Login
docker login raspberry.local:5000
```

## TLS: HTTPS es obligatori

Docker nomes permet pujar/baixar imatges a registres HTTPS (excepte `localhost` o si poses la IP a la llista d'inexus). Si tens un registre a `raspberry.local:5000` nomes amb HTTP, has de dir-li a Docker que el confia:

```bash
# Editar /etc/docker/daemon.json
{
  "insecure-registries": ["raspberry.local:5000"]
}

# Reiniciar Docker
sudo systemctl restart docker
```

Pero la **recomanacio** es posar HTTPS. Usa Caddy o Traefik com a reverse proxy:

```caddyfile
# /etc/caddy/Caddyfile
registry.bernatlab.cat {
    reverse_proxy localhost:5000
}
```

Amb aixo tens HTTPS automatic (Caddy genera certificat amb Let's Encrypt).

## Politica de tags i neteja

Si no tens cura, el registre creixera sense parar. Bones practiques:

- **Usar tags semantics**: `1.0.0`, `1.0.1`, no `latest` per a builds.
- **Netejar periodicament**: scripts que esborrin tags vells.
- **Limitar el nombre**: nomes les ultimes 5-10 versions.

```bash
# Llistar totes les imatges
curl -u bernat:supersecret https://raspberry.local:5000/v2/_catalog

# Llistar tags d'una imatge
curl -u bernat:supersecret https://raspberry.local:5000/v2/meva-app/tags/list

# Esborrar una imatge
curl -u bernat:supersecret -X DELETE \
  https://raspberry.local:5000/v2/meva-app/manifests/sha256:abc...
```

Pero compte: `docker rmi` nomes treu la referencia local. Per esborrar del registre cal fer la crida HTTP o fer **garbage collection** manual.

## Replicacio

Si tens mes d'un node, vols que les imatges estiguin disponibles a tots. Dos enfocaments:

- **Pull en temps d'arrencada**: cada node fa `docker pull` quan arranca. Lent pero simple.
- **Replicacio al registre**: Harbor te aixo built-in.

A la RPi del BernatLab, com tenim un sol node, no ens cal.

## Mirror de Docker Hub

Si la teva xarxa es lenta amb Docker Hub (aixo passa!), pots configurar un mirror local. El registre oficial pot actuar com a cache de Docker Hub:

```yaml
# /home/pi/registry-data/config.yml
version: 0.1
log:
  level: info
storage:
  filesystem:
    rootdirectory: /var/lib/registry
proxy:
  remoteurl: https://registry-1.docker.io
```

Aixi, quan fas `docker pull nginx`, primer busca al teu mirror; si no hi es, baixa de Docker Hub i el guarda per a la propera vegada.

## Connexions amb altres capitols

- **M2 Cap 1** - Aqui es on van les imatges que construeixes.
- **M2 Cap 4** - Compose pot pujar imatges a registres privats.
- **M2 Cap 6** - Els registres privats son part de l'estrategia de seguretat.
