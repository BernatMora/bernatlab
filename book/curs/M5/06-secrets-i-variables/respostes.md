# Respostes - Capitol 6: Secrets i variables d'entorn

> Mira les respostes DESPRES d'haver fet el qüestionari.

## Pregunta 1: Que es un secret?

**Resposta correcta**: Qualsevol dada confidencial que dona acces a alguna cosa (contrasenya, clau API, token).

**Explicacio**: Un secret es qualsevol valor que volem mantenir privat perque te poder: pot fer coses en nom nostre. Pot ser una contrasenya, una clau API, un token, una clau privada SSH, un certificat TLS privat, una contrasenya de wifi. Tots ells comparteixen una propietat: si es filtren, l'atacant pot fer el que nosaltres podem fer.

---

## Pregunta 2: Per que no al codi font?

**Resposta correcta**: Perque van al git i queden a l'historial per sempre.

**Explicacio**: Un cop una contrasenya esta en un commit, queda a l'historial per sempre, encara que l'esborrem al commit següent. Git es un sistema immutable: pensa que el log es public. A mes, els forks, les copies de seguretat, els sistemes de CI, totes les copies del repo contenen l'historial. Una contrasenya al codi es considera **cremada per sempre**.

---

## Pregunta 3: Que es un fitxer .env?

**Resposta correcta**: Un fitxer de text amb variables d'entorn (secrets) que l'aplicacio carrega.

**Explicacio**: Un .env es un fitxer de text pla amb format `CLAU=valor` que les aplicacions llegeixen a l'inici. Es la manera mes simple de gestionar secrets per aplicacions petites. L'avantatge es que es pot ignorar facilment al git. El desavantatge es que esta en text pla al sistema de fitxers, pero amb permisos 600 nomes tu pots llegir-lo.

---

## Pregunta 4: .gitignore i .env

**Resposta correcta**: Tots els .env, sempre.

**Explicacio**: Mai ha d'anar un .env amb valors reals al git, ni un sol cop. Cal afegir `.env` al .gitignore **sempre**, abans del primer commit. I cal un `.env.example` al git amb els noms de les variables buides, perque els col·laboradors sàpiguen quines variables cal definir. L'error mes comu es oblidar el .gitignore en el primer commit: aleshores el secret ja es al git per sempre.

---

## Pregunta 5: Que es un vault?

**Resposta correcta**: Un servei centralitzat per emmagatzemar secrets amb xifratge i acces granular.

**Explicacio**: Un vault es un "caixer forta digital" per als teus secrets. Permet guardar contrasenyes, claus API, certificats, etc., tots xifrats amb una contrasenya mestre. Te un API per accedir-hi programmaticament. Els mes populars son HashiCorp Vault (l'estandard professional) i Bitwarden / Vaultwarden (l'estandard personal). Vaultwarden es el que recomano per al BernatLab.

---

## Pregunta 6: Risc principal

**Resposta correcta**: Que un atacant obtingui acces complet si en filtra un.

**Explicacio**: Els secrets son la **clau** del sistema. Si la teva contrasenya de Tailscale es filtra, l'atacant pot accedir a tota la teva xarxa. Si la teva API key de Twilio es filtra, pot fer cobraments al teu compte. Si el token de Home Assistant es filtra, pot controlar la teva casa. Un sol secret filat pot desfer totes les altres defenses. Per tant, la gestio de secrets es critica.

---

## Pregunta 7: Generar contrasenya

**Resposta correcta**: `openssl rand -base64 32`.

**Explicacio**: `openssl rand` genera bytes aleatoris criptograficament segurs. Combinat amb `-base64` els converteix en text ASCII. Es la manera mes facil i mes segura de generar contrasenyes. Alternatives: `pwgen 32 1` (pwgen nomes aleatories), `gpg --gen-random 1 32`, o un gerenciador de contrasenyes amb el seu generador.

---

## Pregunta 8: .env.example

**Resposta correcta**: Un fitxer plantilla al git amb els noms de les variables pero sense valors.

**Explicacio**: El .env.example es la "documentacio" de quines variables calen. Va al git perque tothom sàpiga quines variables cal definir. Els valors reals van al .env (que NO va al git). Aquest patro es standard: `.env.example` public, `.env` privat. Exemple:

```bash
# .env.example (al git)
DB_PASSWORD=changeme
OPENWEATHER_API_KEY=your_key_here
```

---

## Pregunta 9 (oberta): Estrategia completa

**Resposta model**:

La meva estrategia te tres capes: **fitxers .env per aplicacio**, **Vaultwarden per equip**, i **bones practiques generals**.

**Capa 1: .env per aplicacio**. Cada servei que tinc te el seu propi `.env` amb permisos 600. Per exemple:

- `/opt/homelab/.env` per l'aplicacio principal
- `/opt/gitea/.env` per Gitea
- `/opt/homeassistant/.env` per Home Assistant
- `/opt/vaultwarden/.env` per Vaultwarden

A cada `.env` hi guardo nomes el que aquella aplicacio necessita: la contrasenya de la seva base de dades, la seva clau API, els seus tokens. Aixo es **principi de minim privilege**: si un .env es compromet, nomes es compromet un servei.

Tots aquests fitxers tenen:
- Permissos 600 (nomes el propietari pot llegir).
- Propietari correcte (l'usuari que executa el servei).
- **Mai al git**, amb un `.env.example` buit al seu lloc.

Exemple real:

```bash
# /opt/homelab/.env
DB_PASSWORD=$(openssl rand -base64 24)
OPENWEATHER_API_KEY=sk-real-key-1234
TELEGRAM_BOT_TOKEN=123:ABC

$ ls -l /opt/homelab/.env
-rw------- 1 homelab homelab 156 oct  4 12:34 .env
```

**Capa 2: Vaultwarden per equip**. Tinc Vaultwarden auto-hostatjat accessible nomes per Tailscale. Aqui guardo:

- Totes les contrasenyes dels serveis web (Home Assistant, Portainer, Gitea, Nextcloud).
- Notes segures amb secrets que vull compartir amb mi mateix entre dispositius.
- TOTP (2FA) per a serveis externs (Google, GitHub, AWS).

Aixo em permet accedir als secrets des de qualsevol dels meus dispositius (portatil, telefon) sense haver de copiar fitxers. Tambe es la **copia de seguretat**: si perdo la RPi, encara tinc els secrets al vault (que nomes jo puc obrir).

**Capa 3: Bones practiques generals**:

- **Mai al git**, ni en commits, ni en branques, ni en tags, ni en pull requests.
- **Mai en captures** que puguin acabar a núvols publics.
- **Mai en missatgeria** (Telegram, Discord, correu) perque queden emmagatzemats.
- **Rotacio cada 6 mesos** per als serveis mes sensibles (banca, correu).
- **Rotacio immediata** si sospito que un secret pot estar compromes.
- **Auditoria** cada 3 mesos amb `grep -rE "password|token" /opt /home` per trobar possibles fuites.
- **Generacio aleatoria** amb `openssl rand` o el generador de Vaultwarden.

Aquesta estrategia no es perfecta pero es **pragmatica i suficient** per al nivell d'amenaça del BernatLab. Si fos una empresa amb milers d'euros en joc, afegiria HashiCorp Vault i rotacio automatica. Per a un homelab, aixo es prou.

---

## Pregunta 10 (oberta): Secret exposat

**Resposta model**:

Si descobreixo que una API key ha estat al git durant 3 mesos, el primer que faig es **considerar-la cremada per sempre**. No es pot desfer el que ja ha passat. GitHub te un sistema de "secret scanning" que notifica als proveidors quan es detecta un secret als seus repositoris publics, pero no garanteix que l'atacant no l'hagi trobat abans. Per tant:

**Pas 1: Rotar el secret immediatament**. A la consola del proveidor (OpenWeather, Stripe, AWS, etc.):

1. Anar a la configuracio de l'API.
2. **Esborrar la clau exposada**.
3. **Generar una clau nova**.
4. Guardar la clau nova al .env / vault.

Temps estimat: 5 minuts. No esperis.

**Pas 2: Actualitzar tots els sistemes que la feien servir**. A la RPi:

```bash
# Editar el .env
nano /opt/homelab/.env
# Canviar OPENWEATHER_API_KEY=la_nova_clau

# Reiniciar els serveis
docker compose restart
# o per serveis individuals
sudo systemctl restart homelab-app
```

Verificar que tot funciona:

```bash
curl "https://api.openweathermap.org/data/2.5/weather?q=Manresa&appid=$OPENWEATHER_API_KEY"
```

**Pas 3: Netejar l'historial de git**. Si el repo es privat, podem netejar l'historial amb `git filter-branch` o `git-filter-repo`:

```bash
# Instal·la git-filter-repo
pip install git-filter-repo

# Esborra el fitxer .env de tot l'historial
git filter-repo --path .env --invert-paths
# Force push (perill!)
git push origin --force --all
```

Pero compte: `force push` reescriu l'historial, i altres copies del repo tindran l'historial antic. Cal notificar-ho als col·laboradors.

**Si el repo es public** (a GitHub), no hi ha manera d'esborrar l'historial. Tothom qui hagi fet `git clone` te l'historial antic. Aixo es perque l'error es **greu**: GitHub es public, i un cop es public, es public per sempre. Per tant, la clau s'ha de rotar **encara que l'esborris**.

**Pas 4: Documentar l'incident**. Al Obsidian o al runbook:

- Data: quan es va exposar
- Data: quan es va descobrir
- Quina clau era
- On estava al git (commit, branca)
- Si el repo es public o privat
- Quines accions vas fer (rotar, netejar, etc.)
- Si sospites que algú la va utilitzar (revisar logs del proveidor)

Aixo es un **post-mortem**: serveix per entendre que va fallar i evitar que torni a passar. La lliço: instal·la un detector de secrets al CI (gitleaks, trufflehog) per bloquejar aquests casos automaticament.

---

## Que fer si has fallat moltes preguntes

- **5-8 encerts**: Rellegir el resum i fer l'exercici practic.
- **3-4 encerts**: Audita els teus secrets reals amb les eines de l'exercici.
- **0-2 encerts**: Comença per la part mes basica: posa tots els secrets en un .env.

## Que fer si has encertat totes

- Passa al **Capitol 7** (Backups segurs).
- Investiga **HashiCorp Vault** si vols anar mes enlla.
- Configura **gitleaks** o **trufflehog** al CI per evitar futurs accidents.
- Mira la pagina de **GitGuardian** per entendre les amenaces modernes.
