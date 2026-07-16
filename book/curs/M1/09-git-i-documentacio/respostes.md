# Respostes — Capítol 9: Git i documentació

> Mira les respostes DESPRÉS d'haver fet el qüestionari.

## Pregunta 1: Què és Git?

**Resposta correcta**: Un sistema de control de versions distribuït.

**Explicació**: Git és un VCS (Version Control System) creat per Linus Torvalds el 2005 per gestionar el desenvolupament del kernel Linux. És distribuït: cada còpia del repo és completa (no depèn d'un servidor central). Alternatives: Mercurial, SVN (centralitzat), Fossil.

## Pregunta 2: Inicialitzar repo

**Resposta correcta**: git init

**Explicació**: `git init` crea un directori `.git` al directori actual, que conté tota la base de dades del repo. `git clone` en canvi serveix per descarregar un repo existent.

## Pregunta 3: Estat "staging"

**Resposta correcta**: L'àrea on preparem els canvis abans de fer commit.

**Explicació**: Git té tres àrees: working directory (el que veus), staging area (zona intermitja) i repository (la base de dades). `git add` mou del working al staging; `git commit` mou del staging al repository. Això permet agrupar canvis abans de fer commit.

## Pregunta 4: Fitxer per excloure

**Resposta correcta**: .gitignore

**Explicació**: `.gitignore` llista patrons de fitxers que Git ha d'ignorar. Sintaxi: `*.log` (tots els .log), `build/` (tot el directori build), `**/secrets/` (recursiu). Es commita al repo per compartir les regles amb tothom.

## Pregunta 5: Afegir tots els canvis

**Resposta correcta**: git add .

**Explicació**: `git add .` afegiex TOTS els fitxers del directori actual. `git add fitxer.txt` n'afegeix un de concret. `git add -u` només els modificats (no els nous). `git add -A` afegeix nous, modificats i esborrats.

## Pregunta 6: Historial curt

**Resposta correcta**: git log --oneline

**Explicació**: `--oneline` mostra cada commit en una sola línia (hash curt + missatge). Altres variants útils: `--graph` (visual), `--all` (totes les branques), `--stat` (amb estadístiques), `--author=X` (filtrar per autor).

## Pregunta 7: Risc de git reset --hard

**Resposta correcta**: Esborra commits i canvis no guardats de forma irreversible.

**Explicació**: `--hard` mou HEAD i descarta TOTS els canvis al working directory i staging. Si tens canvis no commitats, es perden. Alternatives segures: `git reset --soft` (manté canvis staged), `git reset --mixed` (per defecte, manté canvis unstaged), `git revert` (crea un commit que desfà un altre commit).

## Pregunta 8: CHANGELOG.md

**Resposta correcta**: Per registrar canvis importants del projecte amb data.

**Explicació**: El CHANGELOG és una eina de comunicació: dius als usuaris (i a tu mateix) què ha canviat entre versions. Normalment estructurat per "Afegit", "Canviat", "Corregit", "Esborrat". Keep a Changelog (https://keepachangelog.com/) és l'estàndard de facto.

## Pregunta 9 (oberta): Per què versionar l'homelab

**Resposta model**:

Versionar l'homelab amb Git és important per tres motius pràctics:

**1. Seguretat davant fallades de hardware**: les microSD de la RPi tenen una vida útil limitada. Si es trenca, pots perdre tot el teu treball. Amb Git, tens còpies al núvol (GitHub, Codeberg, Gitea remot) i pots refer tot l'homelab en 10 minuts: `git clone`, `docker compose up -d`. Sense Git, hauries de recordar totes les configuracions i refer-les manualment.

**2. Poder experimentar sense por**: quan tens una versió sota control, pots provar coses noves (afegir serveis, canviar configuracions) en una branca. Si algo surt malament, fas `git checkout main` i tornes a l'estat conegut bo. Sense Git, tens por de tocar res per si espatlles alguna cosa — la inèrcia de no fer canvis és pitjor que cap canvi.

**3. Memòria institucional per a tu mateix**: d'aquí 6 mesos, quan miris el teu `docker-compose.yml` no recordaràs per què vas posar aquella variable d'entorn o per què vas triar aquella imatge. Si tens un README, un CHANGELOG i un decisions.md, tens el context. A més, els missatges de commit expliquen el "per què" del moment del canvi. Sense això, et trobaràs pensant "què feia aquesta línia?".

**Bonus** (que potser no he mencionat): poder compartir l'homelab amb altres. Si un dia ensenyes a un amic com muntar el seu propi, pots passar-li el teu repo i ell ja té un punt de partida. Si el poses a GitHub o Codeberg, serveix també com a portafolis tècnic — demostra que saps muntar infraestructura.

## Pregunta 10 (oberta): Afegir PiHole versionat

**Resposta model**:

Per afegir PiHole al BernatLab amb el canvi versionat correctament:

**1. Preparació**: connecto per SSH a la RPi (`ssh bernat@hortosona`), vaig al directori del repo (`cd ~/homelab`).

**2. Abans de tocar res, comprovo l'estat net**:
```bash
git status
# Hauria de dir: "nothing to commit, working tree clean"
git pull  # si tinc un remot configurat
```

**3. Editar el docker-compose.yml**:
```bash
nano docker/docker-compose.yml
```
Afegeixo el servei PiHole al final:
```yaml
  pihole:
    image: pihole/pihole:latest
    container_name: pihole
    ports:
      - "8081:80"     # admin web
      - "53:53/tcp"   # DNS TCP
      - "53:53/udp"   # DNS UDP
    environment:
      - TZ=Europe/Madrid
      - WEBPASSWORD=xxxxxxxxx  # canvia-la!
    volumes:
      - pihole_data:/etc/pihole
      - pihole_dns:/etc/dnsmasq.d
    restart: unless-stopped

volumes:
  pihole_data:
  pihole_dns:
```

**Compte**: si poses la `WEBPASSWORD` al compose, queda al repo. Millor usar un fitxer `.env` (que està al .gitignore):
```yaml
    environment:
      - WEBPASSWORD=${PIHOLE_PASSWORD}
```
I crear un `.env` a `~/homelab/docker/.env` (que no es commita).

**4. Actualitzar Homepage** perquè mostri PiHole:
```bash
nano config/homepage/services.yaml
```
Afegeixo dins el grup "BernatLab" o creo un grup "Xarxa":
```yaml
    - Pi-hole:
        href: http://hortosona:8081/admin
        description: Blocador DNS
        icon: pihole
        siteMonitor: http://hortosona:8081/admin
```

**5. Documentar el canvi** al CHANGELOG:
```bash
nano notes/CHANGELOG.md
```
Afegeixo una entrada:
```markdown
## [1.1.0] - 2026-07-17
### Afegit
- Servei PiHole per a bloqueig DNS (port 8081 per admin, 53 per DNS)
- Widget de Pi-hole a Homepage
```

**6. Documentar la decisió** al decisions.md (per què PiHole?):
```bash
nano notes/decisions.md
```
Afegeixo:
```markdown
## 2026-07-17 - Per que PiHole?
Tots els dispositius de la xarxa passen per PiHole, que bloqueja dominis de publicitat i telemetria. Alternativa: AdGuard Home. Tria: PiHole (mes documentacio, mes estable, nomes Python).
```

**7. Comprovar els canvis abans de commitar**:
```bash
git status
git diff
```
Hauries de veure els canvis al compose, al services.yaml, al CHANGELOG i al decisions.md. **Comprova que NO hi ha secrets** (cap password visible).

**8. Afegir i commitar**:
```bash
git add docker/docker-compose.yml
git add config/homepage/services.yaml
git add notes/CHANGELOG.md
git add notes/decisions.md
git status
# Comprova un ultim cop que tot es correcte

git commit -m "Afegeix PiHole per bloqueig DNS amb widget a Homepage"
```

**9. Verificar**:
```bash
git log --oneline
# Hauries de veure el commit a la llista

git show HEAD
# Mostra el diff complet del commit
```

**10. (Opcional) Pujar al remot** (si tens repo a GitHub/Codeberg):
```bash
git push origin main
```

**11. Aplicar els canvis** (aixecar PiHole):
```bash
cd ~/homelab/docker
docker compose up -d pihole
docker compose ps
```

**12. Verificar funcionalment**:
- Accedeix a `http://hortosona:8081/admin` (admin de PiHole).
- Comprova que Homepage mostra la targeta de Pi-hole.

Tot el procés ha deixat rastre a Git. Si alguna cosa falla, puc fer `git revert HEAD` i tornar a l'estat anterior.

## Què fer si has fallat moltes preguntes

- **5-8 encerts**: Rellegir el resum, sobretot la part d'estats de Git.
- **3-4 encerts**: Practica més el flux diari (status, add, diff, commit).
- **0-2 encerts**: Repassem junts.

## Què fer si has encertat totes

- Passa al **Capítol 10** (Full de ruta).
