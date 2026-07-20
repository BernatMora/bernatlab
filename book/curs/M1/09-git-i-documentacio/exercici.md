# Exercici pràctic — Capítol 9: Git i documentació

> 60-75 min · Real al teu sistema

## Objectiu

Posar tot `/home/bernat/homelab/` sota control de versions amb Git, crear la documentació bàsica (README, CHANGELOG, decisions), practicar el flux de treball diari, i aprendre a fer branques.

## Requisits
- Tots els capítols anteriors complets
- 60-75 minuts

## Pas 1: Inicialitza el repo (10 min)

```bash
# Instal·la git
sudo apt install git

# Configura la teva identitat
git config --global user.name "Bernat Mora"
git config --global user.email "bernat@hortosona.local"
git config --global init.defaultBranch main
git config --global core.editor nano

# Inicialitza
cd ~/homelab
git init
git status
```

## Pas 2: Crea el .gitignore (5 min)

```bash
nano .gitignore
```

Contingut:

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
**/api_key
**/token
**/id_ed25519
**/id_*.pub.bak

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

Important: NO posis `id_ed25519` (clau privada) al repo, ni tan sols al .gitignore — simplement no l'hi posis.

## Pas 3: Crea l'estructura de notes (10 min)

```bash
mkdir -p notes docs scripts

# Crea els fitxers de documentació inicial
nano notes/README.md
nano notes/CHANGELOG.md
nano notes/decisions.md
nano notes/incidencies.md
```

**README.md**:

```markdown
# BernatLab

El meu homelab personal, allotjat en una Raspberry Pi 4 (4 GB) amb Debian 13.

## Hardware
- Raspberry Pi 4 Model B Rev 1.4
- 4 GB RAM
- microSD 64 GB classe A2
- Ethernet Gigabit
- hostname: hortosona
- IP Tailscale: 100.x.y.z

## Serveis principals
- Homepage (port 3010): http://hortosona:3010
- Portainer (port 9000): http://hortosona:9000
- Uptime Kuma (port 3001): http://hortosona:3001

## Estructura
- `docker/`: fitxer docker-compose.yml principal
- `config/`: configuracions persistents dels serveis
- `scripts/`: scripts personalitzats
- `notes/`: documentació (aquest directori)
- `docs/`: documentació tècnica

## Com començar de zero
1. Instal·lar Debian 13 Lite
2. Instal·lar Docker (`get-docker.sh`)
3. Instal·lar Tailscale
4. Clonar aquest repo a `~/homelab/`
5. `cd ~/homelab/docker && docker compose up -d`
```

**CHANGELOG.md**:

```markdown
# CHANGELOG

## [1.0.0] - 2026-07-16
### Afegit
- Estructura inicial del BernatLab
- Serveis: Portainer, Uptime Kuma, Homepage, Whoami
- Documentacio basica
- Configuracio SSH amb claus
- Bot de Telegram per alertes
```

**decisions.md**:

```markdown
# Decisions arquitectoniques

## 2026-07-16 - Per que Debian i no Ubuntu?
Debian 13 Lite. Estabilitat maxima, cicle de release llarg, -300 MB RAM vs Ubuntu Server.

## 2026-07-16 - Per que Tailscale i no WireGuard?
Tailscale. MagicDNS, configuracio automatica, gratuit fins a 100 dispositius.

## 2026-07-16 - Per que Docker Compose i no Swarm/K8s?
Compose. Simplicitat, perfecte per a una sola maquina, mes rapid d'aprendre.
```

**incidencies.md**:

```markdown
# Incidencies

Format: YYYY-MM-DD - Titol breu. Descripcio. Resolucio. Temps de caiguda.

## 2026-07-16 - Portainer no responia
Símptoma: HTTP 502 al navegador.
Causa: contenidor parat per OOM (out of memory).
Resolucio: `docker start portainer`, reducció d'altres serveis.
Accio preventiva: considerar limitar RAM per contenidor.
```

## Pas 4: Primer commit (5 min)

```bash
cd ~/homelab
git add .
git status
# Comprova quins fitxers entraran. Hauries de veure:
# - docker/docker-compose.yml
# - config/homepage/*.yaml
# - notes/README.md, CHANGELOG.md, decisions.md, incidencies.md
# - .gitignore
# NO hauries de veure secrets ni volums.

git commit -m "Estat inicial del BernatLab amb docker compose i documentacio"
```

## Pas 5: Practica el flux diari (15 min)

Fes un canvi petit per practicar:

```bash
# 1. Afegeix un script
cat > scripts/info-rpi.sh << 'EOF'
#!/bin/bash
echo "=== BernatLab Info ==="
echo "Hostname: $(hostname)"
echo "IP Tailscale: $(tailscale ip -4 2>/dev/null || echo 'Tailscale no actiu')"
echo "Uptime: $(uptime -p)"
echo "Temperatura: $(vcgencmd measure_temp 2>/dev/null || cat /sys/class/thermal/thermal_zone0/temp | awk '{print $1/1000 "C"}')"
echo "Disc usat: $(df -h / | tail -1 | awk '{print $5}')"
echo "Memoria lliure: $(free -h | grep Mem | awk '{print $4}')"
EOF
chmod +x scripts/info-rpi.sh

# 2. Prova'l
./scripts/info-rpi.sh

# 3. Mira què canviaria
git status
git diff scripts/info-rpi.sh

# 4. Fes commit nomes d'aquest fitxer
git add scripts/info-rpi.sh
git commit -m "Afegeix script info-rpi.sh per veure estat del sistema"
```

## Pas 6: Fes un canvi al docker-compose (10 min)

Afegeix un comentari o una variable d'entorn, i commita'l:

```bash
nano docker/docker-compose.yml
# Afegeix un comentari o una variable buida
# Exemple: "# Versio: 1.0.0 - 2026-07-16" a la primera linia

# Mira el diff
git diff
git add docker/docker-compose.yml
git commit -m "Documenta serveis al docker-compose amb comentaris"
```

## Pas 7: Aprèn a fer branques (15 min)

Les branques permeten experimentar sense trencar res:

```bash
# Crea una branca nova
git branch experiment-rpi-zero
git checkout experiment-rpi-zero

# Modifica alguna cosa
nano scripts/info-rpi.sh
# Afegeix una linia nova: echo "Kernel: $(uname -r)"

git add scripts/info-rpi.sh
git commit -m "Afegeix versio del kernel a info-rpi.sh"

# Mira les dues branques
git log --oneline --all

# Torna a la principal
git checkout main
# El fitxer info-rpi.sh NO tindra la modificacio

# Fusiona la branca experimental
git merge experiment-rpi-zero
# Ara la principal tambe te la modificacio

# Esborra la branca (ja no cal)
git branch -d experiment-rpi-zero
```

## Pas 8: Documenta

Crea `book/curs/M1/09-git-i-documentacio/diari.md` amb:
- Sortida de `git log --oneline` (els teus commits).
- Sortida de `git status` (ha de dir "nothing to commit").
- Sortida de `git branch -a`.
- Notes sobre què t'ha semblat el flux.
- Quina és la propera cosa que vols versionar.

## Validació

Has acabat si:
- [ ] Git inicialitzat a `~/homelab/`.
- [ ] `.gitignore` cobreix secrets, logs, volums.
- [ ] Tens `notes/README.md`, `CHANGELOG.md`, `decisions.md`, `incidencies.md`.
- [ ] Has fet almenys 3 commits.
- [ ] Has practicat el flux complet (status, add, diff, commit).
- [ ] Has creat una branca, has fet canvis, i l'has fusionada.
- [ ] `git log` mostra l'historial.
- [ ] Has documentat a `diari.md`.

## Per aprofundir

- Crea un compte a https://codeberg.org o https://github.com i puja el repo (POTSER NO ENCARA, NO FACIS PUSH).
- Investiga les branques: crea una branca "experiment", toca alguna cosa, fusiona o descarta.
- Afegeix un alias de Git: `git config --global alias.st status`.
- Investiga com migrar un repo a Gitea self-hosted.
- Configura un missatge de commit estàndard amb plantilla.
- Investiga `git stash` per desar canvis sense commit.
- Practica `git blame` per veure qui (o quin commit) va tocar una línia.

## Ves un pas més enllà

**Repte avançat: simula una recuperació de desastre**.

Imagina que la teva microSD s'ha mort i tens una RPi nova amb Debian 13 acabat d'instal·lar. Com recuperaries el teu BernatLab?

Com que encara no has fet push a cap remot (i està bé!), has de pensar una mica més enllà:

1. Fes una còpia de seguretat del repo a una altra màquina:
   ```bash
   # Des del teu portatil, amb Tailscale
   scp -r bernat@hortosona:~/homelab/ ./bernatlab-backup-$(date +%Y%m%d)
   ```

2. Documenta al `notes/README.md` quin és el procediment de recuperació:
   - Quin hardware cal (quins models concrets)?
   - Quin sistema operatiu (quina imatge)?
   - Quines ordres s'han d'executar un cop tenim el sistema base?
   - Quines dades externes cal (tokens de Tailscale, etc.)?

3. Crea un script `scripts/restore.sh` que automatitzi el màxim possible:
   ```bash
   #!/bin/bash
   set -e

   echo "=== Restauracio del BernatLab ==="

   # Instal·la Docker
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh
   sudo usermod -aG docker $USER

   # Instal·la Tailscale
   curl -fsSL https://tailscale.com/install.sh | sh
   sudo tailscale up

   # Clona el repo (assumint que l'hem pujat a algun lloc)
   # git clone https://github.com/bernatmora/bernatlab.git ~/homelab
   # cd ~/homelab

   # O be, descomprimeix el backup
   # tar -xzvf bernatlab-backup.tar.gz -C ~/

   # Aixeca els serveis
   cd ~/homelab/docker
   docker compose up -d

   echo "Restauracio completada!"
   ```

4. Fes commit d'aquest script i de la nova secció del README.

Ara tens un pla de recuperació documentat i automatitzat. Això és el que diferencia un homelab "juguina" d'un projecte seriós.
