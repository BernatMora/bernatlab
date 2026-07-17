# Respostes - Capitol 5: Registre d'imatges

> Mira les respostes DESPRES d'haver fet el qüestionari.

## Pregunta 1: Registre public per defecte?

**Resposta correcta**: Docker Hub.

**Explicacio**: Docker Hub (hub.docker.com) es el registre public mes gran del mon. Es on van les imatges oficials (nginx, postgres, redis, etc.) i qualsevol pot pujar-hi imatges publiques. Es el que Docker consulta per defecte.

---

## Pregunta 2: Imatge oficial de registre?

**Resposta correcta**: registry:2.

**Explicacio**: Docker mateix distribueix la imatge `registry:2` (de l'organitzacio oficial). Es un binaris Go minimalista que implementa l'API V2 del registre. Perfecta per a self-hosting.

---

## Pregunta 3: Per que un registre privat?

**Resposta correcta**: Per seguretat, velocitat i control sobre les imatges.

**Explicacio**: Un registre privat et permet:
- No exposar imatges amb codi propietari al public.
- Baixar-les mes rapid (xarxa local).
- Continuar treballant encara que Docker Hub tingui caigudes.
- Aplicar politiques de retencio i neteja.

---

## Pregunta 4: Comanda per pujar?

**Resposta correcta**: `docker push`.

**Explicacio**: La comanda Docker per pujar es `docker push <nom_imatge>`. Per baixar, es `docker pull <nom_imatge>`. Es consistent amb la resta de comandes.

---

## Pregunta 5: Registre HTTP sense TLS?

**Resposta correcta**: Docker ho rebutja per seguretat (excepte localhost o insecure-registries).

**Explicacio**: Si el registre nomes te HTTP, qualsevol atacant a la xarxa podria interceptar les imatges o fer man-in-the-middle. Docker nomes permet HTTP a `localhost` o si ho declares explicitament a `daemon.json` com a insecure-registries. La recomanacio es sempre HTTPS.

---

## Pregunta 6: Eina completa amb UI?

**Resposta correcta**: Harbor.

**Explicacio**: Harbor es la solucio de registre privat mes completa. Te UI web, autenticacio LDAP/AD, escaneig de vulnerabilitats amb Trivy, replicacio entre registres, politiques de retencio. Es open source de CNCF.

---

## Pregunta 7: On es desen les dades?

**Resposta correcta**: A `/var/lib/registry/` dins el contenidor (cal muntar-hi un volum).

**Explicacio**: El registre desa les imatges al seu sistema de fitxers intern. Si no muntes un volum, es perden quan elimines el contenidor. Sempre cal muntar un volum o bind mount a `/var/lib/registry`.

---

## Pregunta 8: Fitxer d'insecure-registries?

**Resposta correcta**: `/etc/docker/daemon.json`.

**Explicacio**: La configuracio global del dimoni Docker va a `/etc/docker/daemon.json`. Aqui poses registries insegurs, data-root personalitzat, registries mirrors, etc. Cal `sudo systemctl restart docker` despres de canviar.

---

## Pregunta 9 (oberta): Per que un registre privat a la RPi

**Resposta model**:

Tenir un registre Docker privat a la RPi del BernatLab te mes sentit del que sembla, encara que tinguem un sol node. Els beneficis son quatre:

1. **Rapidesa (latencia)**: quan la RPi fa `docker pull nginx`, ha d'anar fins a un servidor de Docker Hub que pot ser a centenars o milers de quilometres. Si el registre es local (a `raspberry.local:5000`), la latencia es de <1 ms. En una xarxa domestica amb Docker Hub a 50-200 ms, la diferencia es enorme. Quan construeixo una imatge de 500 MB i l'he de rebaixar per qualsevol motiu, estalvio minutos.

2. **Mirror de Docker Hub**: puc configurar el registre local com a **cache** de Docker Hub. La primera vegada que baixo `nginx:latest`, el meu registre la descarrega de Docker Hub i la guarda. La segona vegada (jo o qualsevol altre contenidor al lab), la baixa del registre local, que es rapidissim. Si un dia Docker Hub te una caiguda (cosa que ha passat), jo continuo tenint les imatges.

3. **Confidencialitat**: les meves imatges del BernatLab (configuracions especifiques, scripts personalitzats, aplicacions en proves) no cal que estiguin publiques. Si les puges a Docker Hub, son visibles per tothom. Amb un registre privat nomes jo les veig.

4. **Independencia i control**: puc aplicar politiques de retencio (esborrar tags vells automaticament), etiquetar imatges segons el meu flux, tenir un historial net. A Docker Hub tens limitacions de 200 pulls per 6 hores al pla gratuit; al registre propi, cap limit.

Aixo si, cal mantenir-lo: netejar-lo, fer backups, posar-hi HTTPS. Pero a una RPi amb una sola SD, hi ha prou espai per a un registre modest (10-50 GB). Es una de les primeres coses que munto al BernatLab perque el rendiment millora moltissim.

---

## Pregunta 10 (oberta): Tres casos d'us per a distribuir una app

**Resposta model**:

Per a distribuir una app a tres destinataris diferents, triaria opcions diferents:

**Cas 1: Empresa (desenvolupament intern)**

Triaria: **Harbor o registre privat de l'empresa**.

Una empresa no vol que les seves imatges siguin publiques (poden contenir codi propietari, configuracions internes, secrets). A mes, els requisits son:
- Autenticacio integrada amb LDAP/AD (usuaris ja existents).
- Escaneig de vulnerabilitats automatic (compliance).
- Auditoria: qui ha pujat què i quan.
- Retencio i neteja de tags antics.
- Replicacio entre centres de dades.

Harbor te tot aixo. Es self-hosted (les dades son a la teva infraestructura) o managed (cloud). Es la solucio estandard en entorns corporatius. Docker Hub privat nomes te 1 registre privat al pla gratuit, i 200 pulls/6h es molt limitat per a CI/CD.

**Cas 2: Company (un amic, no una empresa)**

Triaria: **ghcr.io (GitHub Container Registry)**.

Si l'amic te compte de GitHub, pot fer:
```bash
docker login ghcr.io -u <usuari>
docker push ghcr.io/<usuari>/meva-app:1.0
docker pull ghcr.io/<usuari>/meva-app:1.0
```

Es gratis per a repos privats (fins a 2 GB d'emmagatzematge). Te autenticacio amb token de GitHub. Es perfecte per compartir amb un company de confiança sense muntar un servidor. Limitacio: 500 MB per imatge.

**Cas 3: Homelab personal**

Triaria: **El registre `registry:2` a la RPi** o **ghcr.io** (si tinc el codi a GitHub).

Si el codi ja esta a GitHub, ghcr.io es convenient: cada push a main pot generar una imatge nova automaticament amb GitHub Actions, i es baixa amb `docker pull ghcr.io/bernatmora/meva-app:main`. Sense mantenir cap infraestructura.

Pero si vull rapidesa maxima, independència total de tercers, i no em molesta mantenir un contenidor mes, munto el `registry:2` a la RPi (com hem fet a l'exercici). Es el que tinc jo al BernatLab.

**Resum de la taula**:

| Destinatari | Opcio | Per que |
|---|---|---|
| Empresa | Harbor (self-hosted) | Seguretat, LDAP, auditoria, vulnerabilitats |
| Company | ghcr.io | Gratis, privat per defecte, integrat amb GitHub |
| Homelab | registry:2 o ghcr.io | Rapidesa, independència, baix manteniment |

Docker Hub nomes ho faria servir per a **imatges publiques** que vulguis compartir amb el mon (per exemple, una eina open source que vols que tothom pugui fer servir). Pero mai per a res que sigui confidencial.

---

## Pregunta 11 (oberta): Per que TLS es obligatori en registres privats

**Resposta model**:

Els registres privats requereixen TLS obligatoriament per tres motius de seguretat:

1. **Autenticacio**: el client Docker envia credencials al registre per fer `docker push` o `docker pull`. Si el tràfic es HTTP, les credencials viatgen en text pla i un atacant les pot interceptar.

2. **Integritat de les imatges**: sense TLS, un atacant "man-in-the-middle" pot modificar les imatges que el client descarrega. Per exemple, pot substituir la imatge de Nextcloud per una amb backdoor, i el client ni se n'adona.

3. **Confidencialitat**: el contingut de les imatges (que pot contenir logica de negoci, configuracio amb secrets) viatja sense xifrar. Un atacant pot veure l'estructura del Dockerfile, les variables d'entorn baked-in, etc.

A Docker, si intentes fer push a un registre HTTP (no HTTPS), el client rebutja la operacio per defecte. Per permetre-ho cal afegir l'entrada `insecure-registries` al `/etc/docker/daemon.json`, cosa que nomes es fa en entorns de desenvolupament local (on la xarxa es de confiança).

**Cas concret del BernatLab**: si algú aconsegueix fer push al teu registre, pot:
- Substituir la imatge de Nextcloud per una amb backdoor que li dona acces a tots els fitxers dels usuaris.
- Substituir la imatge de Ollama per una que envia les teves consultes a un servidor extern.
- Substituir la imatge de ChromaDB per una que esborra la base de coneixement.

Per tant, TLS es la **primera barrera** de seguretat d'un registre privat. Fins i tot en un homelab, val la pena configurar HTTPS amb un certificat de Let's Encrypt o un certificat auto-signat (afegint-lo als clients de confiança).

---

## Pregunta 12 (oberta): Registre privat i supply chain security

**Resposta model**:

El concepte de "supply chain security" (seguretat de la cadena de subministrament) es refereix a la cadena completa des del codi font fins al contenidor en execucio. Cada pas es un punt potencial d'atac:

```
Codi font -> Build -> Imatge -> Registre -> Descarrega -> Execucio
   |          |         |          |            |            |
   atac 1    atac 2    atac 3    atac 4       atac 5       atac 6
```

Un registre privat et permet atacar (positivament) aquesta cadena en el pas 3-4:

**1. Verificacio abans de pujar**: nomes puges imatges que has construit tu. No depens de tercers (Docker Hub, ghcr.io) que poden canviar imatges sense avis.

**2. Escaneig de vulnerabilitats centralitzat**: pots integrar eines com Trivy o Clair al pipeline. Cada imatge que puges es escanejada i les vulnerabilitats es reporten. Si vols, pots bloquejar el push si hi ha CVEs critics.

**3. Signatura d'imatges**: amb eines com `cosign` (de Sigstore), pots signar criptograficament cada imatge. El client pot verificar que la imatge que descarrega es exactament la que tu vas signar, no pas una versio modificada per un atacant.

**4. Politiques d'admissio**: en entorns mes grans (Kubernetes), pots configurar politiques que nomes permetin executar imatges del teu registre, no pas imatges random de Docker Hub. Aixi evites que un desenvolupador impulsi una imatge no auditada.

**5. Auditoria**: tens un registre de quines imatges s'han pujat, quan, i per qui. Si hi ha un incident, pots rastrejar l'origen.

Al BernatLab, encara que no necessitis totes aquestes mesures, tenir un registre privat ja et dona el control basi: saps exactament quines imatges executes i pots reproduir el build.

---

## Pregunta 13 (oberta): Convence al company de muntar un registre privat

**Resposta model**:

Al company que diu "Docker Hub es rapid, per què ens molestem?", li donaria quatre arguments:

**1. Velocitat**:
Docker Hub es rapid per a imatges populars (nginx, postgres), pero pot ser lent per a imatges custom o de mida gran. Amb un registre privat a la xarxa local (100 Mbps o mes), les descarreigues son a velocitat LAN, no pas WAN. Per a una imatge de 500 MB, la diferencia pot ser 1 minut vs 30 segons.

**2. Fiabilitat**:
Docker Hub ha tingut caigudes i limits de descarreiga. Si tens 20 serveis tots depenent del pull, una caiguda de Docker Hub et deixa amb el sistema inoperatiu. Un registre local es un "punt de control" garantit.

**3. Privacitat**:
Si la teva app conte logica de negoci o credencials baked-in (que no es bona practica, pero pasa), Docker Hub te la imatge i pot fer-ne el que vulgui. Un registre privat garanteix que nomes tu tens acces.

**4. Mirror/cache**:
El registre privat pot actuar com a cache de Docker Hub. Quan fas `docker pull nginx`, primer mira al registre local; si no hi es, baixa de Docker Hub i el guarda. La propera vegada ja el tens local. Es un "CDN" casola.

**Exemple concret del BernatLab**: tens 10 imatges custom que nodreixen 10 serveis. Si les has de refer per qualsevol motiu (canvi de sistema base, vulnerabilitat critica), trigues 30 min amb Docker Hub vs 2 min amb registre local. I si Docker Hub te una caiguda un divendres a la nit, no pots actualitzar res.

**Contraargument just**: el registre privat te un cost de manteniment. Cal configurar-lo, mantenir-lo, fer-ne backup. Per tant, nomes val la pena si tens prou volum de descarreigues/imatges per justificar-lo.

---

## Pregunta 14 (oberta): Organitzacio d'imatges al BernatLab

**Resposta model**:

Per organitzar 5 serveis propis al registre, usaria aquesta estructura:

**Noms**:
- `bernatlab/api` (FastAPI)
- `bernatlab/worker`
- `bernatlab/postgres` (imatge custom de postgres amb configuracio inicial)
- `bernatlab/monitor` (eina de monitoritzacio custom)
- `bernatlab/telegram-bot`

**Tags**:
Evitaria `latest` com a tag unic. Usaria un esquema de tags mixt:
- Versions semantiques: `api:1.2.0`, `api:1.2.1`
- Tags de branca: `api:main`, `api:develop`
- Tags de data: `api:2024-01-15` (util per a rollbacks)
- Combinacio: `api:1.2.0-2024-01-15`

**Avantatges de multi-tag**:
- Pots fer rollback exacte a una data sabent que la build es bona.
- Pots distingir entre "ultima versio estable" i "ultima versio".
- Pots etiquetar releases especifiques amb noms.

**Organitzacio del registre**:
- Un sol registre es suficient per a un homelab. No cal separar per projecte.
- Si creixes, pots posar organitzacions dins Harbor o organitzar per prefix al nom.
- Un registre separat per dev i prod nomes si tens els dos en maquines diferents.

**Backup del registre**:
- Els volums del registre es poden tractar com qualsevol altre volum: backup periodic.
- Si el registre es perd, es pot tornar a pujar tot desde el codi font (les imatges son reproducibles).
- Les imatges de Ollama no cal que estiguin al registre (estan en el volum, no com a imatge de Docker).

**Politica de neteja**:
- Conservar les ultimes 5 versions de cada imatge.
- Esborrar les imatges mes antigues de 90 dies automaticament.

---

## Pregunta 15 (oberta): registry:2 vs Harbor al BernatLab

**Resposta model**:

La tria entre `registry:2` (el registre oficial de Docker) i Harbor depen de les teves necessitats reals:

**`registry:2` - Avantatges**:
- Imatge minima (~30 MB), poc overhead.
- Configuracio molt simple (un parell de variables d'entorn).
- Escala be per a pocs clients.
- No te dependencies externes.

**`registry:2` - Limitacions**:
- Nomes emmagatzema imatges. No te UI web.
- Autenticacio nomes basica (token), sense LDAP/OAuth.
- Sense escaneig de vulnerabilitats integrat.
- Sense politiques de retencio automatic (cal un script extern).
- Sense replicacio entre registres.

**Harbor - Avantatges**:
- UI web completa, intuïtiva.
- Autenticacio amb LDAP, OIDC, base de dades local.
- Escaneig de vulnerabilitats amb Trivy integrat.
- Quotes d'emmagatzematge per projecte.
- Replicacio entre instancies de Harbor.
- Signatura d'imatges amb Cosign.
- Politiques de retencio automatic.

**Harbor - Limitacions**:
- Pesat: ~500 MB de memoria minima, 1 GB recomanat.
- Moltes dependencies (PostgreSQL, Redis, etc).
- Complexitat de manteniment: actualitzacions, còpies de seguretat de la DB.
- Codi mes complex: mes superficie d'atac.

**Recomanacio per al BernatLab**:
- Si tens 1-3 desenvolupadors i 5-10 imatges: `registry:2` + un script de neteja. Es minimalista i funciona.
- Si tens mes de 5 persones al projecte, o vols auditar vulnerabilitats, o vols LDAP: Harbor.

**El meu cas al BernatLab**: uso `registry:2` per a les meves imatges personals. No tinc LDAP. Faig l'escaneig de vulnerabilitats manualment amb Trivy quan recordo. La complexitat extra de Harbor no es justifica per al meu volum.

**Punt de migracio**: si en el futur necessito UI web o LDAP, puc migrar de `registry:2` a Harbor sense perdre imatges (s'importen amb un export/import). Per tant, començo amb `registry:2` i creixo quan cal.

---

## Que fer si has fallat moltes preguntes

- **5-8 encerts**: Rellegir el resum i fer l'exercici practic.
- **3-4 encerts**: Refes l'exercici amb autenticacio. Es la part mes important.
- **0-2 encerts**: Repassem junts. Els registres son basics per a qualsevol homelab seriós.

## Que fer si has encertat totes

- Passa al **Capitol 6** (seguretat).
- Munta un Harbor al BernatLab (es un projecte divertit).
- Configura HTTPS amb Caddy i un domini propi.
