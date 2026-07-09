# Capítol 46 — 2FA, secrets i gestió de claus

> *"Les contrasenyes soles ja no protegeixen res. El 2FA és el nou normal."*

## 46.1 Per què el 2FA

Les contrasenyes tenen un problema: es poden endevinar, filtrar, o robar. Un cop algú té la teva contrasenya, té accés. El **2FA** (Two-Factor Authentication, autenticació de dos factors) afegeix un segon factor que **no es pot robar només amb la contrasenya**.

Els tres factors possibles:

1. **Quelcom que saps** (contrasenya, PIN).
2. **Quelcom que tens** (mòbil, clau USB).
3. **Quelcom que ets** (empremta, cara, veu).

El 2FA combina dos d'aquests, normalment **saps + tens**.

## 46.2 Tipus de 2FA

### TOTP (Time-based One-Time Password)

El mòbil genera codis de 6 dígits que canvien cada 30 segons. Aplicacions: **Google Authenticator**, **Authy**, **1Password**, **Bitwarden**.

Exemple: 123 456 (canvia cada 30s).

### Push notifications

Una app del mòbil (Duo, Microsoft Authenticator) t'avisa: "Vols iniciar sessió a BernatLab?" Tu acceptes.

### SMS

Rebs un codi per SMS. **Molt poc segur** (SIM swapping), però millor que res.

### Hardware tokens (claus físiques)

**YubiKey**, **Titan Key**, **OnlyKey**. Són claus USB que insertes al port. Molt segures.

### Passkeys (WebAuthn / FIDO2)

L'estàndard modern. El mòbil o la clau USB fan d'identitat, sense contrasenya. Adoptat per Apple, Google, Microsoft.

Recomanació: **TOTP per compatibilitat** (molt acceptat) + **passkey o YubiKey** on estigui disponible.

## 46.3 Aplicar 2FA al BernatLab

### 2FA a Tailscale

Tailscale admet 2FA per accedir a la consola d'administració:

1. Vés a https://login.tailscale.com/admin/settings/team.
2. A "Two-factor authentication", configura TOTP.
3. Escaneja el codi QR amb Google Authenticator.
4. Desa els codis de recuperació en un lloc segur.

Cada vegada que accedeixis a la consola, et demanarà un codi.

### 2FA a Portainer

Portainer admet 2FA per a usuaris:

1. Crea un usuari a Portainer.
2. Activa 2FA a la configuració.
3. L'usuari escaneja el QR.

### 2FA a Grafana

Grafana admet 2FA:

1. A la configuració de l'usuari, activa 2FA.
2. Escaneja el QR.

### 2FA a Uptime Kuma

Uptime Kuma (versió 1.20+) admet 2FA. Configura'l igualment.

### 2FA a SSH

Per a SSH, pots usar:

1. **Claus SSH** (no és 2FA però és més segur que contrasenyes).
2. **OATH-TOTP** amb **libpam-google-authenticator**: a més de la clau, cal un codi TOTP.

Instal·lació:

```bash
sudo apt install libpam-google-authenticator

# A cada usuari
google-authenticator
```

Configura `/etc/ssh/sshd_config`:

```
ChallengeResponseAuthentication yes
AuthenticationMethods publickey,keyboard-interactive
```

I `/etc/pam.d/sshd`:

```
auth required pam_google_authenticator.so
```

Així, cal clau SSH + codi TOTP. Molt segur.

### 2FA a la Raspberry Pi (consola)

A la Raspberry, pots protegir l'inici de sessió local:

1. Instal·la `libpam-google-authenticator`.
2. Configura PAM per demanar TOTP a l'inici de sessió.

Això és útil si la Raspberry és accessible físicament (cosa que pot passar si la poses al camp).

## 46.4 Gestors de contrasenyes

El pitjor enemic de la seguretat són les **contrasenyes reutilitzades** i les **contrasenyes curtes**. Solució: un **gestor de contrasenyes** que:

- Genera contrasenyes llargues i úniques.
- Emmagatzema tot xifrat.
- Autocompleta formularis.

Recomanats:

- **Bitwarden** (cloud, gratuït, multi-plataforma).
- **1Password** (pagament, excel·lent UX).
- **KeePassXC** (local, open source).
- **Apple Keychain** (integrat a macOS, bàsic però útil).

Per al BernatLab, **Bitwarden** és la millor opció:

- Gratuït per a ús personal.
- Multi-plataforma (Mac, Windows, Linux, mòbil).
- Open source (codi auditat).
- 2FA integrat.
- Compartició segura amb família.

## 46.5 Secrets al BernatLab

**Secrets** són credencials, claus d'API, contrasenyes, tokens. Al BernatLab tens molts:

- API keys (Homepage, Grafana, Portainer, InfluxDB).
- Contrasenyes de bases de dades.
- Tokens de Telegram bot.
- Claus Tailscale.
- AppEUI, AppKey dels nodes LoRa.
- API keys TTN (per a integració MQTT).

## 46.6 On guardar els secrets

### ❌ Pitjor: en text pla al codi

```python
# MAI NO!
TELEGRAM_TOKEN = "1234567890:ABCdefGHIjklMNOpqrsTUVwxyz"
```

Això és perillós perquè:

- Si el codi es penja a GitHub (fins i tot privat), queden exposats.
- Si la màquina es compromet, s'obtenen tots els secrets.

### ⚠️ Millor: variables d'entorn

```python
import os

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
```

Les variables d'entorn **no es guarden al codi**, sinó a la configuració del sistema. Millor, però encara poden ser visibles al procés.

### ✓ Bo: fitxers .env (no versionats)

```bash
# .env (a .gitignore!)
TELEGRAM_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
```

Carrega-les amb `python-dotenv`:

```python
from dotenv import load_dotenv
load_dotenv()

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
```

Afegeix `.env` a `.gitignore`.

### ✓✓ Molt bo: gestors de secrets

Per a sistemes seriosos:

- **HashiCorp Vault**: el més professional.
- **Bitwarden** (org): per a equips.
- **Doppler**: cloud, fàcil d'usar.
- **Infisical**: open source, cloud o self-hosted.
- **age** o **sops**: xifrar fitxers YAML/JSON.

### ✓✓✓ Excel·lent: Docker secrets

Si uses Docker Compose, pots usar **secrets**:

```yaml
version: "3.8"
services:
  app:
    image: bernatlab/app
    secrets:
      - telegram_token

secrets:
  telegram_token:
    file: ./secrets/telegram_token.txt
```

Els secrets es munten a `/run/secrets/` dins del contenidor. No apareixen a les variables d'entorn.

## 46.7 Rotació de secrets

Els secrets s'han de **rotar** periòdicament:

- **Contrasenyes d'usuari**: cada 6-12 mesos.
- **API keys**: cada 12 mesos o quan es sospita compromís.
- **Tokens**: cada 3-6 mesos.
- **Certificats**: cada 90 dies (Let's Encrypt ho fa automàticament).

Un calendari de rotació:

| Secret | Freqüència | Responsable |
|---|---|---|
| Contrasenya Mac | 6 mesos | Bernat |
| Contrasenya Raspberry | 6 mesos | Bernat |
| Tailscale 2FA | quan cal | Bernat |
| Tokens Telegram | 12 mesos | Bernat |
| API keys InfluxDB | 12 mesos | Bernat |
| Clau SSH | 12 mesos | Bernat |
| Certificat web | 90 dies (auto) | Caddy/Traefik |

## 46.8 Com generar contrasenyes segures

Una bona contrasenya:

- Té **mínim 16 caràcters**.
- Combina **majúscules, minúscules, números i símbols**.
- És **única** per a cada servei.
- **No es basa** en paraules de diccionari.

Exemple de bona contrasenya: `Tr0p1c@l-R@mbl3r-2026!`

O més fàcil de recordar: `groc-tardor-poma-cullita-245m!` (4 paraules catalanes + número + signe).

Usa el gestor per generar-les:

- Bitwarden té un generador de contrasenyes.
- KeePassXC idem.
- 1Password idem.

## 46.9 Claus SSH

Les claus SSH són la millor manera d'autenticar-te a la Raspberry (molt millor que contrasenyes).

### Generar una clau forta

```bash
ssh-keygen -t ed25519 -C "bernat@bernat-mbp" -f ~/.ssh/bernatlab
```

Això genera una clau ed25519 (més curta i segura que RSA).

### Instal·lar-la a la Raspberry

```bash
ssh-copy-id -i ~/.ssh/bernatlab.pub bernat@hortosona
```

Això afegeix la clau pública a `~/.ssh/authorized_keys`.

### Desactivar l'accés per contrasenya

Edita `/etc/ssh/sshd_config`:

```
PasswordAuthentication no
PermitRootLogin no
PubkeyAuthentication yes
```

I reinicia SSH:

```bash
sudo systemctl restart sshd
```

Ara només pots accedir amb la clau. Molt més segur.

### Protegir la clau privada amb passphrase

Quan generes la clau, et demana una passphrase. **Sempre posa'n una**. Així, si algú roba la clau, no pot fer-la servir.

Pots usar `ssh-agent` per no haver d'escriure la passphrase cada vegada:

```bash
ssh-add ~/.ssh/bernatlab
```

## 46.10 Gestió de claus a Tailscale

Tailscale té un sistema de **pre-auth keys** per afegir dispositius nous:

1. A la consola, genera una **pre-auth key**.
2. Fes servir aquesta clau al nou dispositiu: `tailscale up --authkey=tskey-...`.
3. La clau té una durada limitada (per defecte, un sol ús).

També pots etiquetar automàticament:

```bash
tailscale up --authkey=tskey-... --tag=server
```

Així, quan s'uneix un dispositiu, ja té el tag correcte.

## 46.11 Pre-shared keys (PSK) per a serveis

Alguns serveis (WireGuard, OpenVPN, Wi-Fi WPA3) admeten **pre-shared keys** (PSK). Són claus compartides manualment que xifren el canal.

Exemple: WPA3-Personal usa una contrasenya com a PSK. Important que sigui forta.

## 46.12 Auditories periòdiques

Cada 3-6 mesos, revisa:

1. **Quins secrets** tens actius.
2. **Quins serveis** els usen.
3. **Si cal rotar** algun.
4. **Si hi ha secrets** antics que ja no es fan servir.
5. **Si hi ha secrets** exposats en algun lloc.

Eines útils:

- **git-secrets**: evita secrets al Git.
- **gitleaks**: cerca secrets en repositoris.
- **trufflehog**: cerca secrets en commits antics.

```bash
# Al repo del BernatLab
pip install gitleaks
gitleaks detect --source .
```

Si troba secrets, **rota'ls immediatament**.

## 46.13 Política de secrets al BernatLab

Documenta una política clara:

```markdown
## Política de secrets al BernatLab

1. Tots els secrets s'emmagatzemen a `.env` (no versionat) o al gestor del sistema.
2. Les claus SSH tenen passphrase sempre.
3. 2FA activat a Tots els serveis que ho permetin.
4. Contrasenyes generades amb Bitwarden, mínim 16 caràcters.
5. Rotació de secrets cada 6-12 mesos.
6. Cap secret en text pla al codi o commits.
7. Auditoria amb gitleaks cada mes.
```

## 46.14 Errors habituals

**Error 1: desar secrets a GitHub per error**.

Assegura't que `.env` està a `.gitignore` abans del primer commit. Si ja l'has pujat, **rota els secrets immediatament** (no serveix de res esborrar el fitxer, el commit queda a la història).

**Error 2: usar la mateixa contrasenya a tot arreus**.

Si un servei es compromet, tots els altres cauen. Usa contrasenyes úniques.

**Error 3: penjar la clau SSH a un sistema sense passphrase**.

Si perds el portàtil, la clau queda exposada.

**Error 4: desar secrets al README**.

Els READMEs es comparteixen. Mai posis un secret visible al README.

**Error 5: no rotar mai**.

Els secrets vells són vectors d'atac. Rota'ls.

## 46.15 Resum

El 2FA, una bona gestió de contrasenyes, i una política clara de secrets són la tercera línia de defensa. TOTP i claus SSH amb passphrase són les millors pràctiques. Bitwarden és el millor gestor per a ús personal. Roteu els secrets periòdicament, i mai els poseu a Git. En el proper capítol veurem fail2ban, rate limiting, i tallafocs aplicat.

## 46.16 Exercicis pràctics

1. Instal·la Bitwarden (o un altre gestor) i migra les teves contrasenyes.
2. Activa 2FA a Tailscale, Portainer, Grafana, Uptime Kuma.
3. Genera claus SSH ed25519 amb passphrase.
4. Desactiva l'autenticació per contrasenya a la Raspberry.
5. Configura libpam-google-authenticator a la Raspberry per 2FA a SSH.
6. Crea un `.env` per a cada servei amb els secrets, i afegeix-lo a `.gitignore`.
7. Executa gitleaks al repo del BernatLab.
8. Documenta al README la política de secrets.

Paraules clau: **2FA, MFA, two-factor, autenticació, dos factors, TOTP, HOTP, Google Authenticator, Authy, 1Password, Bitwarden, passkey, FIDO2, WebAuthn, YubiKey, Titan, hardware token, clau física, SMS, push, push notification, OTP, one-time password, secret, password, contrasenya, passphrase, PIN, biometric, empremta, face ID, veu, iris, retina, smart card, targeta, NFC, RFID, password manager, gestor, vault, autofill, generador, password generator, random, secure random, entropy, PBKDF2, bcrypt, Argon2, scrypt, hash, salt, pepper, key stretching, strength, length, complexity, uniqueness, breach, leak, have i been pwned, HIBP, dictonary, attack, brute force, rainbow table, GPU, ASIC, cracking, rotation, expiry, lifetime, regen, rec, refresh, secret, API key, token, bearer, JWT, OAuth, OIDC, refresh token, access token, ssh-keygen, ed25519, RSA, ECDSA, public key, private key, keypair, fingerprint, authorized_keys, known_hosts, ssh-agent, ssh-add, ssh-copy-id, sshd, PasswordAuthentication, PermitRootLogin, ChallengeResponse, PAM, libpam-google-authenticator, OATH, RFC 6238, HOTP, security audit, gitleaks, git-secrets, trufflehog, detect-secrets, environment variable, .env, dotenv, secrets management, Vault, Infisical, Doppler, SOPS, age, gpg, encrypted file, KMS, HSM, cloud secret, AWS Secrets Manager, GCP Secret Manager, Azure Key Vault, Kubernetes secret, docker secret, compose secret, secret rotation, key rotation, certificate, TLS, x.509, ACME, Let's Encrypt, ZeroSSL, certbot, autorenew, expiry, CRL, OCSP, mTLS, mutual, client cert, server cert, root CA, intermediate CA, chain, trust store, openssl, verification, fingerprint, FQDN, SAN, Subject Alternative Name**.
