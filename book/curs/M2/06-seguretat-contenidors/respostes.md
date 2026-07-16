# Respostes - Capitol 6: Seguretat de contenidors

> Mira les respostes DESPRES d'haver fet el qüestionari.

## Pregunta 1: Risc de root?

**Resposta correcta**: Que si algú l'explota, tindra acces de root a l'amfitrio.

**Explicacio**: Un contenidor root **pot** fer molt mes del que sembla. Tot i que esta aillat, te acces a coses com muntar sistemes de fitxers, carregar moduls del kernel, accedir a dispositius. Si un atacant troba una vulnerabilitat, pot escapar del contenidor i atacar l'amfitrio. Per defecte, els contenidors son root.

---

## Pregunta 2: Usuari no-root?

**Resposta correcta**: `--user 1000:1000`.

**Explicacio**: La flag `--user` (o `-u`) estableix l'UID:GID dins el contenidor. L'exemple posa 1000:1000 perque es l'usuari per defecte de les distribucions modernes. Per a servidors web, sovint es 33:33 (www-data) o 999:999.

---

## Pregunta 3: Que es rootless?

**Resposta correcta**: Docker que s'executa sense root a l'amfitrio.

**Explicacio**: Rootless Docker usa "user namespaces" del kernel Linux per mapejar l'UID 0 del contenidor a un UID no privilegiat a l'amfitrio. Aixi, encara que el contenidor es cregui que es root, al sistema amfitrio es un usuari normal. Es la opcio mes segura pero mes complexe de configurar.

---

## Pregunta 4: Treure capabilities?

**Resposta correcta**: `--cap-drop=ALL`.

**Explicacio**: Les capabilities son permisos especials que tradicionalment nomes te root (muntar, carregar moduls, etc.). Docker ja en treu moltes per defecte pero si vols el maxim de seguretat pots fer `--cap-drop=ALL` i despres afegir nomes les que necessites amb `--cap-add=...`.

---

## Pregunta 5: Read-only?

**Resposta correcta**: Un sistema de fitxers montat nomes de lectura.

**Explicacio**: Si un atacant aconsegueix executar codi dins el contenidor, no podra modificar res (nomes afegir a volums o tmpfs). Es una bona defensa en profunditat.

---

## Pregunta 6: Que es `docker scan`?

**Resposta correcta**: Analitzar vulnerabilitats conegudes a les imatges Docker.

**Explicacio**: `docker scan` consulta una base de dades de CVEs (vulnerabilitats conegudes) i compara amb les llibreries de la teva imatge. Es una bona practica escanejar les imatges regularment.

---

## Pregunta 7: Per que --read-only?

**Resposta correcta**: Perque el sistema de fitxers del contenidor no es pugui modificar.

**Explicacio**: Amb `--read-only`, qualsevol intent d'escriure al filesystem del contenidor falla. El contenidor nomes pot escriure a volums muntats, tmpfs o la xarxa. Es una bona defensa davant atacs que intentin persistir (afegir un binari malicios, modificar una llibreria, etc.).

---

## Pregunta 8: Que es seccomp?

**Resposta correcta**: Restringir les syscalls que un proces pot fer al kernel.

**Explicacio**: Seccomp (secure computing mode) es un mecanisme del kernel Linux que permet filtrar les syscalls. Docker ja l'aplica per defecte amb un perfil que nomes permet les syscalls segures. Es una capa important de defensa.

---

## Pregunta 9 (oberta): Tres vectors d'atac

**Resposta model**:

Els tres vectors d'atac mes comuns contra un contenidor Docker mal configurat son:

**1. Execucio com a root + capabilities excessives**

Un contenidor que s'executa com a root (`docker run` sense `--user`) i conserva capabilities per defecte es una porta oberta. Per exemple, un Nextcloud amb `/var/www/html` montat com a bind mount a `/home/pi/photos/`: si l'atacant aconsegueix explotar una vulnerabilitat de Nextcloud, pot executar codi com a root **dins el contenidor**. Pero el pitjor es que pot muntar sistemes de fitxers de l'amfitrio, carregar moduls del kernel, accedir a dispositius. Amb capabilities com `SYS_ADMIN`, fins i tot pot intentar escapar del contenidor.

Exemple practic: al 2019 es va descobrir una vulnerabilitat a runc (l'eina que Docker usa per executar contenidors) que permetia escapar. Si el contenidor era root amb capabilities, l'atac era factible. Si era no-root, no.

**2. Xarxa exposada i secrets al descobert**

Un altre vector es exposar ports innecesaris o secrets al fitxer compose. Si el Postgres te el port 5432 exposat amb `-p 5432:5432` i el password esta al `docker-compose.yml` en text pla, qualsevol que pugui accedir a la xarxa pot intentar conectar-se. Un atac de "brute force" o un escaneig de ports pot descobrir credencials febles.

Exemple: al BernatLab abans exposava el port de Adminer (8080) a tota la xarxa local. Un veins podia intentar entrar. Ara nomes esta exposat a localhost, i accedeixo per Tailscale.

**3. Imatges vulnerables i desactualitzades**

Si fas `docker run some-random-image` que no s'actualitza des de fa 2 anys, esta ple de vulnerabilitats conegudes. Un escaneig de Trivy sobre una imatge vella pot trobar 50-100 vulnerabilitats critiques. Si el servei te una superficie d'atac (esta exposat a Internet), un atacant pot explotar una d'aquestes.

Exemple: la imatge `nextcloud:20` (de 2021) te 30+ vulnerabilitats conegudes. La `nextcloud:28` (actual) te nomes 2-3. La diferencia es brutal.

Aixo es la **defensa en profunditat**: ni una sola d'aquestes mesures es suficient per si sola. Cal combinar-les totes.

---

## Pregunta 10 (oberta): Seguretat del Nextcloud al BernatLab

**Resposta model**:

Per a un Nextcloud al BernatLab que serveix fitxers personals, aplicaria minim aquestes 6 mesures:

**1. Usuari no-root**

Afegiria al compose: `user: "33:33"` (www-data). D'aquesta manera, encara que un atacant exploti una vulnerabilitat de Nextcloud, no tindra root dins el contenidor. Es la mesura mes basica i la que mes impacte te.

**2. Read-only filesystem**

`read_only: true` al compose. El sistema de fitxers del contenidor es nomes de lectura; nomes pot escriure a volums muntats i tmpfs. Si un atacant intenta persistir (afegir un script, modificar una llibreria), no pot.

Afegeixo `tmpfs` per a carpetes que necessiten escriptura temporal:
```yaml
tmpfs:
  - /tmp:size=100M,noexec,nosuid
```

**3. Capacitats minimes**

`cap_drop: [ALL]` per defecte. Despres afegiria nomes les estrictament necessaries:
```yaml
cap_drop: [ALL]
cap_add: [CHOWN, SETUID, SETGID]  # el minim per a Nextcloud
```

Alternativament, `--security-opt=no-new-privileges` que evita que el procés adquireixi nous privilegis.

**4. Xarxa aillada**

Dues xarxes:
- `xarxa-frontend`: nomes el Nextcloud, accessible des de l'amfitrio.
- `xarxa-backend`: nomes la base de dades.

La base de dades (MariaDB) nomes esta a `xarxa-backend` i mai es exposada a fora. Nextcloud esta a les dues xarxes pero nomes exposa el port 80/443 a l'amfitrio.

**5. Imatge oficial actualitzada**

Usar nomes `nextcloud:stable` o una versio especifica actualitzada regularment. Configurar Watchtower (cap 7) per actualitzar automaticament les imatges quan hi ha noves versions. Escanejar periodicament amb `trivy image nextcloud:stable` per veure vulnerabilitats noves.

**6. Sense privilegis i amb limits**

```yaml
security_opt:
  - no-new-privileges:true
  - seccomp:default  # perfil per defecte (ja esta, pero explicit)
privileged: false  # MAI activar-ho
mem_limit: 1g
cpus: 2
```

Aixo posa limits de memoria i CPU (evita DoS) i desactiva el mode privilegiat (que es una porta oberta).

**Extra: backup xifrat**

Tot i que no es "del contenidor", el backup de les dades del Nextcloud (volum) ha d'estar xifrat. Si el disc falla i el backup es accessible, volem que estigui xifrat. Això es la defensa **despres** que tot falla.

**Resum del compose**:
```yaml
services:
  nextcloud:
    image: nextcloud:stable
    user: "33:33"
    read_only: true
    cap_drop: [ALL]
    cap_add: [CHOWN, SETUID, SETGID]
    security_opt:
      - no-new-privileges:true
    tmpfs:
      - /tmp:size=100M,noexec,nosuid
    mem_limit: 1g
    privileged: false
    networks:
      - frontend
      - backend
    volumes:
      - nc-data:/var/www/html
```

Aixo es la base. En entorns mes critics afegiries SELinux/AppArmor, signatura d'imatges, registre certificat, etc. Pero per a un homelab personal, aquestes 6 mesures ja son un salt qualitatiu enorme.

---

## Que fer si has fallat moltes preguntes

- **5-8 encerts**: Rellegir el resum i tornar a fer l'exercici.
- **3-4 encerts**: Audita la teva configuracio actual amb Docker Bench Security.
- **0-2 encerts**: Repassem junts. La seguretat es fonamental.

## Que fer si has encertat totes

- Passa al **Capitol 7** (actualitzacio de contenidors).
- Configura rootless Docker a la RPi.
- Executa Docker Bench Security i arregla els warnings.
