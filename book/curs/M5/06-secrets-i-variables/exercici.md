# Exercici practic - Capitol 6: Secrets i variables d'entorn

> 30-45 min · Real al teu sistema

## Objectiu

Auditar i securitzar la gestio de secrets al BernatLab: identificar secrets exposats, moure'ls a fitxers .env, i (opcionalment) configurar Vaultwarden.

## Requisits

- Acces a la RPi amb sudo
- 30-45 minuts
- Coneixement basic de git

## Pas 1: Audita els teus secrets actuals (10 min)

Primer mira quins secrets tens actualment i on son:

```bash
# Busca fitxers .env a /opt i a /home
find /opt /home -name ".env*" -type f 2>/dev/null

# Busca possibles secrets al codi
grep -rE "(password|token|api_key|secret)\s*=\s*['\"]" /opt /home 2>/dev/null | head -20

# Mira la historia del git (si tens un repo)
cd /opt/homelab
git log -p | grep -iE "password|token|api_key" | head -20
```

Anota tots els llocs on hi ha secrets. Si n'has trobat al git, **es considera compromes**, cal rotar.

## Pas 2: Mou a un .env (10 min)

Crea un fitxer `.env` al directori del projecte:

```bash
# Directori exemple
mkdir -p /opt/homelab
cd /opt/homelab

# Crea el .env amb permisos restrictius
touch .env
chmod 600 .env

# Edita'l
nano .env
```

Contingut:

```bash
# /opt/homelab/.env - NO AL GIT

# Base de dades
DB_PASSWORD=una_contrasenya_aleatoria_llarga
DB_USER=homelab
DB_NAME=hort

# API keys
OPENWEATHER_API_KEY=la_teva_clau_aqui
TELEGRAM_BOT_TOKEN=123456:ABC-DEF

# SSH i Tailscale
TAILSCALE_AUTHKEY=tskey-auth-xxxxx
```

Crea un `.env.example` per al git:

```bash
cat > .env.example <<'EOF'
# /opt/homelab/.env.example - copia aquest fitxer a .env i omple els valors

# Base de dades
DB_PASSWORD=
DB_USER=
DB_NAME=

# API keys
OPENWEATHER_API_KEY=
TELEGRAM_BOT_TOKEN=

# SSH i Tailscale
TAILSCALE_AUTHKEY=
EOF
```

Afegeix al `.gitignore`:

```bash
echo ".env" >> .gitignore
echo "!.env.example" >> .gitignore
```

## Pas 3: Comprova que .env no va al git (5 min)

```bash
# Comprova
git check-ignore -v .env
# Hauria de dir: .gitignore:1:.env .env

# Prova d'afegir (hauria de fallar)
git add .env
# Ha de donar: The following paths are ignored by one of your .gitignore files

# Comprova .env.example SI va
git add .env.example
git status
```

## Pas 4: Carrega les variables a les aplicacions (10 min)

Adapta el teu docker-compose.yml:

```yaml
services:
  app:
    image: bernatlab/api
    env_file: .env
    # o be:
    # environment:
    #   - DB_PASSWORD=${DB_PASSWORD}
    #   - OPENWEATHER_API_KEY=${OPENWEATHER_API_KEY}
```

```bash
docker compose up -d

# Comprova que les variables han passat al contenidor
docker exec bernatlab-api env | grep -E "DB_|OPENWEATHER"
```

Adapta els scripts de bash:

```bash
#!/bin/bash
# Carrega el .env nomes per aquest script
set -a
source /opt/homelab/.env
set +a

# Usar les variables
echo "Database: $DB_NAME"
curl "https://api.openweathermap.org/data/2.5/weather?q=Manresa&appid=$OPENWEATHER_API_KEY"
```

## Pas 5: Opcional - Configura Vaultwarden (10 min)

Si tens temps, munta Vaultwarden amb Docker:

```bash
mkdir -p /opt/vaultwarden/data

docker run -d --name vaultwarden \
  -v /opt/vaultwarden/data:/data \
  -p 8080:80 \
  --restart unless-stopped \
  vaultwarden/server:latest
```

Despres:

1. Crea un compte a http://localhost:8080 (canvia el port exposat a Tailscale nomes).
2. Instal·la l'app de Bitwarden al portatil i telefon.
3. Comença a guardar-hi els secrets.

Aixo es opcional pero es la millor inversio a llarg termini.

## Pas 6: Genera contrasenyes noves (5 min)

Genera contrasenyes aleatories per a tots els serveis que ja tenies:

```bash
# Generador basic
generate_password() {
  openssl rand -base64 24 | tr -d "=+/" | cut -c1-20
}

# Genera diverses
for i in {1..5}; do generate_password; done

# Canvia les contrasenyes a:
# - Home Assistant
# - Portainer
# - Gitea
# - Base de dades
# - SSH (millor regenerar les claus)
```

## Pas 7: Documenta (5 min)

Al fitxer `inventari-seguretat.md`, afegeix una seccio "Secrets" amb:

- Llista de serveis amb les seves contrasenyes (referencies, no valors).
- On es guarden els secrets (paths, vault).
- Data de l'ultima rotacio.
- Data de la propera rotacio.

## Validacio

- [ ] Has auditat on tens secrets actualment.
- [ ] Has mogut tots els secrets a un .env amb permisos 600.
- [ ] Tens un .env.example al git.
- [ ] El .env real NO esta al git.
- [ ] Les aplicacions carreguen correctament les variables.
- [ ] Has generat contrasenyes noves per als serveis principals.
- [ ] (Opcional) Tens Vaultwarden configurat.

## Per aprofundir

- Investiga **sops** de Mozilla: xifra fitxers YAML/JSON amb AWS KMS o PGP.
- Prova **age** com a substitut modern de GPG per xifrar fitxers petits.
- Si tens un servidor a AWS/GCP/Azure, mira els seus serveis de secrets: AWS Secrets Manager, GCP Secret Manager.
- Activa **GitGuardian** o **gitleaks** al CI per bloquejar secrets al futur.
