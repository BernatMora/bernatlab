# Resum - Capitol 6: Secrets i variables d'entorn

## La idea clau

Qualsevol cadena de text que permeti a algú accedir a una cosa que no hauria es un **secret**: contrasenyes, claus API, tokens, certificats privats, claus SSH privades. La gestio d'aquests secrets es un dels punts mes critiques de la seguretat del servidor. Si es filtren, tota la resta de defenses queden inutilitzades. Al BernatLab tenim tres opcions: fitxers **.env**, **Docker secrets**, i **vaults** (com Vaultwarden, Ansible Vault).

## Que es un secret

Un **secret** es qualsevol dada que volem mantenir confidencial perque dona acces a alguna cosa. Els mes comuns:

- Contrasenyes de serveis (Home Assistant, Portainer, base de dades).
- Claus API (Tailscale, OpenWeather, Stripe, etc.).
- Tokens de bots (Telegram, Discord).
- Claus privades SSH.
- Certificats TLS privats.
- Contrasenyes de wifi.

Tots aquests son secrets. Si un atacant els te, pot fer tot el que tu pots fer.

## L'error mes gran: secrets al codi

L'error mes frequent i mes greu es **posar secrets al codi font**:

```python
# NO FACIS MAI AIXO
db_password = "supersecret123"
api_key = "sk-abcdefghijklmnop"
```

Si aquest codi va a un repositori Git (encara que sigui privat), es considera compromes. Perque:

1. **Historial**: Git guarda tot l'historial. Fins i tot si esborres la contrasenya, queda a l'historial antic.
2. **Branques i tags**: poden contenir la contrasenya sense que te n'adonis.
3. **Forks i copies**: si el repo es clona, la contrasenya va amb ell.
4. **Logs de CI/CD**: sistemes com GitHub Actions tenen acces al codi, i per tant al secret.
5. **Subdominis accidentals**: una pujada a un repo equivocat filtra el secret.

Un cop filtrat, **un secret es considera cremat per sempre**. Cal canviar-lo, no n'hi ha prou amb esborrar-lo.

## Fitxers .env: el minim acceptable

La manera mes simple de gestionar secrets al homelab es amb un fitxer **.env**:

```bash
# /opt/homelab/.env
DB_PASSWORD=supersecret123
API_KEY=sk-abcdefghijklmnop
TELEGRAM_TOKEN=123456:ABC-DEF
```

Aquest fitxer **mai va al git**. S'afegeix al `.gitignore`:

```bash
echo ".env" >> .gitignore
```

I es llegeix per l'aplicacio:

```bash
# Amb Docker Compose
docker compose --env-file .env up

# Amb bash
source .env && echo "$DB_PASSWORD"
```

Bo per a homelabs. Per a produccion, cal mes rigor.

## Bones practiques amb .env

- **MAI al git**. Afegeix `.env` a `.gitignore` SEMPRE.
- **Permissos 600**: nomes tu pots llegir. `chmod 600 .env`.
- **Un .env per entorn**: `.env.dev`, `.env.prod`.
- **Documenta les variables al .env.example** (que SI va al git):

```bash
# .env.example (al git, sense valors reals)
DB_PASSWORD=changeme
API_KEY=your_api_key_here
TELEGRAM_TOKEN=your_token_here
```

- **Comprova que no es filtra**: `git log -p | grep -i "password"` per buscar accidents.

## Docker secrets

Docker Swarm te un sistema natiu de **secrets**: emmagatzema una cadena xifrada i la passa nomes als contenidors autoritzats. A Docker Compose nomes no funciona (cal Swarm), pero hi ha eines com **docker-secrets** o **sops** que ho simulen.

Exemple amb Docker Swarm:

```bash
echo "supersecret123" | docker secret create db_password -
```

Al compose:

```yaml
services:
  db:
    image: postgres
    secrets:
      - db_password
    environment:
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password

secrets:
  db_password:
    external: true
```

El secret es munta a `/run/secrets/db_password` dins del contenidor, en memoria tmpfs (no al disc). Es la manera mes neta.

## Vaults: gestio centralitzada

Un **vault** es un servei centralitzat per emmagatzemar secrets amb xifratge fort, auditoria, i acces granular. Les opcions mes conegudes:

- **HashiCorp Vault**: el mes complet, pero complexe.
- **Bitwarden / Vaultwarden**: gestor de contrasenyes amb auto-hostatjament. **Ideal per al BernatLab**.
- **Passbolt**: similar a Vaultwarden.
- **1Password CLI**: comercial pero amb bones opcions CLI.
- **Ansible Vault**: xifra fitxers YAML amb una contrasenya.

Al BernatLab recomano **Vaultwarden** (Bitwarden auto-hostatjat):

```bash
# Crear contenidor
docker run -d --name vaultwarden \
  -v /vw-data/:/data/ \
  -p 8080:80 \
  vaultwarden/server:latest
```

Despres accedeixo a https://vault.bitx.cat (o el que sigui) des de Tailscale. Tots els secrets al vault, accessibles des del portatil i el telefon.

## Com accedir als secrets al runtime

Hi ha patrons comuns:

- **Llegir del fitxer**: aplicacio que obre `/run/secrets/db_password` i el llegeix.
- **Variable d'entorn**: aplicacio que fa `os.environ["DB_PASSWORD"]`.
- **API del vault**: aplicacio que fa una crida HTTP al vault per obtenir el secret.

Exemple amb Python:

```python
# Lector basic
import os
password = os.environ.get("DB_PASSWORD")

# Lector de Docker secret
with open("/run/secrets/db_password") as f:
    password = f.read().strip()
```

Exemple amb bash:

```bash
#!/bin/bash
# Carregar .env nomes en aquest script
set -a
source /opt/homelab/.env
set +a

# Usar les variables
echo "Database: $DB_PASSWORD"
```

## Bones practiques generals

- **Mai al git**. Mai.
- **Mai en captures de pantalla**. Mai.
- **Mai en xats o correus**. Mai.
- **Rotacio periodica**: canvia els secrets cada 3-6 mesos.
- **Minim privilege**: cada servei te nomes el secret que necessita.
- **Auditoria**: revisa quins secrets hi ha, on son, i qui te acces.
- **Generadors de contrasenyes**: fes servir `pwgen` o `openssl rand`.

Exemple per generar contrasenyes segures:

```bash
# 32 caracters aleatoris
openssl rand -base64 32

# 16 caracters alfanumerics
pwgen 16 1

# Nomes per llegibilitat (separa amb guions)
pwgen -s 16 1
```

## Comandes utils

```bash
# Comprovar que un .env no es al git
git check-ignore .env

# Veure l'historial per possibles fuites
git log -p | grep -iE "password|token|secret" | head

# Generar una contrasenya forta
openssl rand -hex 32

# Auditar permisos dels fitxers .env
find /opt -name ".env" -type f -exec ls -l {} \;

# Rotar un secret (exemple: API key de OpenWeather)
echo "OpenWeather_API_KEY=antic123" > /opt/homelab/.env.old
echo "OpenWeather_API_KEY=novell456" > /opt/homelab/.env
# Test
curl "https://api.openweathermap.org/data/2.5/weather?q=Manresa&appid=$OpenWeather_API_KEY"
# Si funciona, esborra el .old
rm /opt/homelab/.env.old
```

## Connexions amb altres capitols

- **M2 Cap 6** - Seguretat en contenidors: Docker secrets.
- **M3 Cap 1** - Estrategia de backup: els secrets son part del backup.
- **Cap 7 d'aquest modul** - Backups xifrats: on acaben els secrets quan els backupeges.
- **M8 Cap 1** - SSH amb claus: les claus privades son secrets.

## Conclusio

La gestio de secrets es **la practica mes critica** de la seguretat. Una contrasenya filtrada inutilitza totes les altres defenses. Per tant:

1. **Mai** al codi ni al git.
2. **Sempre** en un fitxer amb permisos restrictius o un vault.
3. **Sempre** amb rotacio periodica.
4. **Sempre** amb un generador aleatori.

Si nomes portes una cosa bona d'aquest modul, que sigui aixo.
