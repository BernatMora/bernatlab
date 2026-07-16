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

## Que fer si has fallat moltes preguntes

- **5-8 encerts**: Rellegir el resum i fer l'exercici practic.
- **3-4 encerts**: Refes l'exercici amb autenticacio. Es la part mes important.
- **0-2 encerts**: Repassem junts. Els registres son basics per a qualsevol homelab seriós.

## Que fer si has encertat totes

- Passa al **Capitol 6** (seguretat).
- Munta un Harbor al BernatLab (es un projecte divertit).
- Configura HTTPS amb Caddy i un domini propi.
