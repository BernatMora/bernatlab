# Resum — Capítol 9: Git i documentació

## La idea clau

Un homelab sense versionat és com cuinar sense recepta: cada vegada que toques alguna cosa, et preguntes "trencarà res?". **Git** és l'eina que et permet tenir un historial complet de tots els canvis al teu homelab, tornar enrere quan alguna cosa falla, i documentar què fas i per què. Aquest capítol és sobre posar sota control de versions tot `/home/bernat/homelab/` i mantenir una documentació viva (README, CHANGELOG).

## Què és Git (recompte ràpid)

Git és un sistema de control de versions distribuït. Permet:

- **Guardar instantànies** (commits) del teu projecte al llarg del temps.
- **Veure què ha canviat** entre una instantània i una altra (diffs).
- **Tornar enrere** (revert) a un estat anterior conegut bo.
- **Treballar en branques** (branches) per provar coses sense tocar el principal.
- **Col·laborar** amb altres (en el nostre cas, sovint només nosaltres, però és útil).

Els fitxers poden estar en tres estats:

- **Working directory**: el que veus a l'editor.
- **Staging area**: el que has seleccionat per al proper commit.
- **Repository (.git)**: el que ja està guardat.

## Per què versionar l'homelab?

Al BernatLab tens:

- `docker-compose.yml` (la joia de la corona).
- Configuracions dels serveis (YAML de Homepage, etc.).
- Scripts personalitzats.
- Notes (markdown).
- Captures, documentació.

Si tot això viu només a la RPi i un dia la SD es trenca, ho perds tot. Si ho versiones amb Git:

- Tens **backup automàtic** (al núvol o en un altre disc).
- Pots **comparar versions** ("què vaig canviar dimarts que va trencar Portainer?").
- Pots **experimentar** amb una branca nova sense por.
- Pots **reproduir** tot l'homelab en una altra màquina en 5 minuts.
- Pots **ensenyar-lo** a altres (compartir el repositori).

## Estructura esperada

```
/home/bernat/homelab/
├── docker/
│   └── docker-compose.yml
├── config/
│   ├── homepage/
│   │   ├── settings.yaml
│   │   ├── services.yaml
│   │   ├── widgets.yaml
│   │   └── bookmarks.yaml
│   ├── portainer/         (configuració, opcional)
│   └── uptime-kuma/       (configuració, opcional)
├── scripts/
│   └── (scripts .sh personalitzats)
├── notes/
│   ├── README.md
│   ├── CHANGELOG.md
│   ├── incidencies.md
│   └── decisions.md
├── docs/
│   └── (documentació, esquemes)
└── .gitignore
```

## Configuració inicial de Git

A la RPi:

```bash
# Instal·la git (si no el tens)
sudo apt install git

# Configura la teva identitat
git config --global user.name "Bernat Mora"
git config --global user.email "bernat@hortosona.local"
git config --global init.defaultBranch main
git config --global core.editor nano

# Inicialitza el repo
cd ~/homelab
git init
```

## .gitignore: què NO versionar

Alguns fitxers NO han d'anar al repo (secrets, dades, volums):

```gitignore
# Volums i dades
*.db
*.sqlite
*.sqlite3
.env
.env.*

# Secrets
**/secrets/
**/passwords/
**/*.key
**/*.pem
**/token
**/api_key

# Logs
*.log
logs/

# Cache
.cache/
node_modules/

# Personal
.DS_Store
*.swp
*~
```

**Compte**: mai facis commit d'un fitxer amb contrasenyes reals. Per a secrets, usa variables d'entorn o un gestor com Bitwarden/Vaultwarden.

## Primer commit

```bash
cd ~/homelab

# Mira l'estat
git status

# Afegeix tot (respectant .gitignore)
git add .

# Comprova què entrarà al commit
git status
git diff --staged

# Fes el commit
git commit -m "Estat inicial del BernatLab: docker compose + homepage"
```

## El flux diari

```bash
cd ~/homelab

# 1. Mira què has canviat
git status
git diff

# 2. Afegeix els canvis al staging
git add docker/docker-compose.yml
git add config/homepage/services.yaml
# o tot:
git add .

# 3. Fes commit amb missatge clar
git commit -m "Afegeix PiHole al servei de xarxa"

# 4. (Opcional) Puja al remot
git push origin main
```

## Missatges de commit: convencions

Un bon missatge de commit és curt però descriptiu. Formats habituals:

- **Simple**: `Afegeix monitor Uptime Kuma per al portainer`.
- **Conventional Commits**: `feat: afegeix servei PiHole`, `fix: corregeix port de Homepage`, `docs: actualitza README`.
- **Per àrea**: `[docker] actualitza portainer a 2.21`, `[homepage] afegeix 3 serveis nous`.

Al BernatLab, el format simple en català funciona bé.

## README.md: la porta d'entrada del projecte

Cada bon projecte té un `README.md` a l'arrel. Per al BernatLab, podria ser:

```markdown
# BernatLab

El meu homelab personal, allotjat en una Raspberry Pi 4 (4 GB) amb Debian 13.

## Visió general
- [Descripció del projecte]
- [Llista de serveis principals]
- [Com accedir-hi]

## Estructura del repositori
- `docker/`: fitxer docker-compose.yml principal
- `config/`: configuracions persistents
- `scripts/`: scripts personalitzats
- `notes/`: documentació i decisions
- `docs/`: documentació tècnica

## Com començar
1. Clona el repo
2. Instal·la Docker + Tailscale
3. Fes `docker compose up -d`
4. Configura Tailscale
5. Accedeix a http://hortosona:3010

## Enllaços útils
- [Homepage](http://hortosona:3010)
- [Portainer](http://hortosona:9000)
- [Uptime Kuma](http://hortosona:3001)
- [Status Page](http://hortosona:3001/status/bernatlab)
```

## CHANGELOG.md: què ha canviat

Un CHANGELOG (registre de canvis) és un fitxer on es registren els canvis importants amb data:

```markdown
# CHANGELOG — BernatLab

## [1.4.0] - 2026-07-15
### Afegit
- Servei PiHole per a bloqueig DNS
- Monitor de certificat SSL per a hortosona.cat
- Status Page pública a Uptime Kuma

### Canviat
- Portainer actualitzat a 2.21.4
- Homepage: nova paleta de colors

### Corregit
- El contenidor whoami es reiniciava per OOM

## [1.3.0] - 2026-06-30
...
```

Format simple en Markdown. Pots seguir el de [Keep a Changelog](https://keepachangelog.com/) si vols una estructura formal.

## notes/decisions.md: ADR (Architecture Decision Records)

Un ADR (registre de decisions arquitectòniques) documenta per què vam prendre una decisió tècnica concreta:

```markdown
# Decisions arquitectòniques

## 2026-07-15: Per què Debian 13 Lite i no Ubuntu Server?

**Contexte**: triar sistema operatiu per a la RPi.
**Decisio**: Debian 13 Lite.
**Consequencies**:
- Estabilitat maxima (Debian te el cicle de release mes llarg).
- Sense entorn grafic: -300 MB RAM, -2 GB disc.
- Documentacio abundant a Internet.
- Alternativa descartada: Ubuntu Server (mes modern pero menys estable a ARM).

## 2026-07-10: Per què Tailscale i no WireGuard manual?

**Contexte**: acces remot segur a la RPi.
**Decisio**: Tailscale.
**Consequencies**:
- Configuracio automatica (sense tocar el router).
- MagicDNS inclos.
- Gratuit fins a 100 dispositius.
- Alternativa descartada: WireGuard manual (mes complex, cal mantenir les claus).
```

Això és or quan, mesos després, et preguntes "per què ho vaig fer així?".

## notes/incidencies.md: postmortem

Cada vegada que algo es trenca i el解决方案:

```markdown
# Incidencies

## 2026-07-12 - Portainer no responia

**Símptomes**: la UI de Portainer no carregava.
**Diagnòstic**: contenidor exitat amb OOM (Out Of Memory).
**Solució**: limitat memoria del contenidor a 256 MB al docker-compose.
**Lliço**: mai donar memoria il·limitada als contenidors; posar sempre limits.
```

## Publicar el repo

Pots allotjar el repo en diversos llocs:

- **GitHub** (públic o privat).
- **GitLab** (públic o privat, o self-hosted).
- **Gitea** (self-hosted a la pròpia RPi, meta!).
- **Forgejo** (similar a Gitea).

Recomanació al BernatLab: **Gitea allotjat a la pròpia RPi** (mínim 2 GB RAM). Així tens el control total, és un exercici més, i pots accedir-hi via Tailscale.

Alternativa: un repo privat a GitHub/Codeberg com a backup remot. Compte amb secrets — no facis push d'un `.env` real.

## Comandos útils

```bash
# Veure l'historial
git log
git log --oneline
git log --graph --oneline --all

# Veure un canvi concret
git show <commit-hash>

# Tornar enrere
git revert <commit-hash>      # crea un commit que desfà
git reset --hard <commit-hash>  # PERILLÓS: esborra commits
git checkout -- fitxer.txt     # descartar canvis locals

# Branques
git branch                          # llista
git checkout -b prova-nova-feature  # crea i canvia
git checkout main                   # torna a main
git merge prova-nova-feature
git branch -d prova-nova-feature

# Stash (guardar canvis temporalment)
git stash
git stash pop
```

## Bones pràctiques

1. **Commits petits i freqüents**: millor 5 commits petits que 1 de gegant.
2. **Missatges clars**: explica el "què" i el "per què", no només el "què".
3. **Commit al final de cada sessió de treball**: si toques algo, commita'l.
4. **Mai secrets al repo**: usa `.gitignore` i variables d'entorn.
5. **Branques per a experiments**: prova coses noves en una branca.
6. **Documenta el "per què"**: el "què" es veu al diff, el "per què" cal explicar-lo.
7. **Backups regulars**: el repo + una còpia fora de la RPi.

## Connexions amb altres capítols

- **Cap 5** — El `docker-compose.yml` que has de versionar.
- **Cap 6-8** — Les configs de Portainer, Uptime, Homepage que pots muntar al host.
- **Cap 10** — El "full de ruta" serà una entrada al CHANGELOG.
- **Cap 35** — CI/CD amb GitHub Actions o Gitea Actions.
- **Cap 40** — Muntar un Gitea self-hosted com a part de l'homelab.

Ara tens el teu homelab sota control de versions. Pots trencar coses sense por. El següent pas és planificar què vindrà.
