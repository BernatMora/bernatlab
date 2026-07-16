# Exercici pràctic — Capítol 9: Git i documentació

> 45-60 min · Real al teu sistema

## Objectiu
Posar tot `/home/bernat/homelab/` sota control de versions amb Git, crear la documentació bàsica (README, CHANGELOG, decisions), i practicar el flux de treball diari.

## Requisits
- Tots els capítols anteriors complets
- 45-60 minuts

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
- IP Tailscale: 100.115.134.76

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
```

**decisions.md**:

```markdown
# Decisions arquitectoniques

## 2026-07-16 - Per que Debian i no Ubuntu?
Debian 13 Lite. Estabilitat maxima, cicle de release llarg, -300 MB RAM vs Ubuntu Server.

## 2026-07-16 - Per que Tailscale i no WireGuard?
Tailscale. MagicDNS, configuracio automatica, gratuit fins a 100 dispositius.
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

# 3. Fes commit
git add scripts/info-rpi.sh
git commit -m "Afegeix script info-rpi.sh per veure estat del sistema"
```

## Pas 6: Fes un canvi al docker-compose (opcional, 10 min)

Afegeix un comentari o una variable d'entorn, i commita'l:

```bash
nano docker/docker-compose.yml
# Afegeix un comentari o una variable buida

git diff
git add docker/docker-compose.yml
git commit -m "Documenta serveis al docker-compose amb comentaris"
```

## Pas 7: Documenta

Crea `book/curs/M1/09-git-i-documentacio/diari.md` amb:

- Sortida de `git log --oneline` (els teus commits).
- Sortida de `git status` (ha de dir "nothing to commit").
- Notes sobre què t'ha semblat el flux.

## Validació

Has acabat si:
- [ ] Git inicialitzat a `~/homelab/`.
- [ ] `.gitignore` cobreix secrets, logs, volums.
- [ ] Tens `notes/README.md`, `CHANGELOG.md`, `decisions.md`, `incidencies.md`.
- [ ] Has fet almenys 2 commits.
- [ ] Has practicat el flux complet (status, add, diff, commit).
- [ ] `git log` mostra l'historial.
- [ ] Has documentat a `diari.md`.

## Per aprofundir

- Crea un compte a https://codeberg.org o https://github.com i puja el repo (POTSER NO ENCARA, NO FACIS PUSH).
- Investiga les branques: crea una branca "experiment", toca alguna cosa, fusiona o descarta.
- Afegeix un alias de Git: `git config --global alias.st status`.
- Investiga com migrar un repo a Gitea self-hosted.
