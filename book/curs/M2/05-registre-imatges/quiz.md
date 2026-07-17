# Qüestionari - Capitol 5: Registre d'imatges

> 15 preguntes · ~20 min

## Pregunta 1
Quin es el registre public per defecte de Docker?

- [ ] Quay.io
- [ ] GitHub Container Registry
- [x] Docker Hub
- [ ] Harbor

## Pregunta 2
Quina es la imatge Docker oficial per muntar el teu propi registre privat?

- [ ] docker/registry
- [x] registry:2
- [ ] nginx
- [ ] Traefik

## Pregunta 3
Per que es recomanable tenir un registre privat?

- [ ] Per estetica
- [x] Per seguretat, velocitat i control sobre les imatges
- [ ] Perque Docker Hub ha deixat d'existir
- [ ] Per poder tenir mes imatges

## Pregunta 4
Quina ordre Docker pots fer servir per pujar una imatge al registre?

- [ ] docker upload
- [x] docker push
- [ ] docker deploy
- [ ] docker ship

## Pregunta 5
Que passa si intentem fer push a un registre HTTP sense TLS?

- [ ] Tot funciona be
- [x] Docker ho rebutja per seguretat (excepte localhost o insecure-registries)
- [ ] Docker ho permet nomes en dev
- [ ] Cal pagar

## Pregunta 6
Quina eina de registre privat te UI web, autenticacio LDAP i escaneig de vulnerabilitats?

- [ ] Docker Hub
- [x] Harbor
- [ ] El registry oficial
- [ ] GitHub Container Registry

## Pregunta 7
On es desen les dades del registre `registry:2` per defecte?

- [x] A /var/lib/registry/ dins el contenidor (cal muntar-hi un volum)
- [ ] Al núvol automaticament
- [ ] A la xarxa
- [ ] En un CD

## Pregunta 8
Quin fitxer configura les "insecure-registries" a Docker?

- [ ] /etc/hosts
- [x] /etc/docker/daemon.json
- [ ] /var/lib/docker/config.json
- [ ] ~/.docker/config

## Pregunta 9 (oberta)
Explica amb les teves paraules: per que al BernatLab (homelab a una RPi) tindria sentit tenir un registre privat encara que tinguem un sol node? Quins beneficis practics aporta?

Pistes per respondre:
- Rapidesa: el registre es local, no va a internet.
- Confidencialitat: les teves imatges no son publiques a Docker Hub.
- Independència: si Docker Hub cau, tu tens les imatges.
- Mirror: pots configurar-lo com a cache de Docker Hub.

## Pregunta 10 (oberta)
Has construit una app i la vols distribuir: a la teva empresa, a un company, i al teu homelab. Quines opcions tens? Compara Docker Hub, ghcr.io i un registre privat propi. Per a cada cas d'us, quin triaries?

Pistes per respondre:
- Docker Hub es public per defecte (tot el mon veu les imatges).
- ghcr.io es privat per defecte pero limitat.
- Un registre propi et dona control total pero cal mantenir-lo.
- Pensa en confidencialitat, cost i manteniment.

## Pregunta 11 (oberta)
Per que creus que els registres privats han de tenir TLS obligatoriament? Quins atacs evita i quines consequencies te si un atacant pot fer push al teu registre?

Pistes per respondre:
- Un atacant que pugui fer push pot substituir imatges legitimes per versions malicioses.
- Si el registre es HTTP, les credencials viatgen en clar.
- Un atac "man-in-the-middle" pot substituir descarregues.
- Que passaria al BernatLab si algú canvia la imatge de Nextcloud per una amb backdoor?

## Pregunta 12 (oberta)
Quina relacio hi ha entre un registre privat i l'estrategia de "supply chain security"? Com influeix tenir un registre propi en la teva capacitat de confiar en les imatges que executes al BernatLab?

Pistes per respondre:
- Supply chain: la cadena desde el codi font fins al contenidor en execucio.
- Cada pas es un punt d'atac: registre, descarrega, execucio.
- Un registre propi amb politiques de signatura dona mes control.
- L'escaneig de vulnerabilitats (Trivy, Docker scan) es pot fer abans de pujar.

## Pregunta 13 (oberta)
Imagina que el teu company et diu: "el Docker Hub es rapid, per que ens molestem en muntar un registre privat al BernatLab?". Convence'l amb arguments de velocitat, fiabilitat i privacitat, usant exemples concrets del teu cas.

Pistes per respondre:
- Velocitat: ample de banda de la RPi vs ample de banda de Docker Hub.
- Fiabilitat: que passa quan Docker Hub te una caiguda?
- Privacitat: que passa si la teva app conte logica de negoci sensible?
- Mirror: el registre privat pot actuar com a cache de Docker Hub.

## Pregunta 14 (oberta)
Aplica el concepte de registre al cas concret del BernatLab amb un stack de 5 serveis propis: una API FastAPI, un worker per processar tasques, una base de dades PostgreSQL, una eina de monitoritzacio custom i un bot de Telegram. Com organizaries les imatges al registre? Usaries un sol registre o mes? Quins tags faries servir (latest? versions? data?)?

Pistes per respondre:
- Noms: prefix per projecte (bernatlab/api, bernatlab/worker).
- Tags: evita `latest` nomes. Usa versions semantiques o data.
- Si tens mes registres (per exemple un per dev i un per prod), com els sincronitzaries?
- Backups del registre: com els faries?

## Pregunta 15 (oberta)
Quines consequencies te per a l'operativa diaria triar entre un registre simple (`registry:2`) i una solucio completa com Harbor al BernatLab? Pensa en complexitat, espai, funcionalitats i temps de manteniment. Argumenta una recomanacio per a un homelab amb temps limitat.

Pistes per respondre:
- `registry:2`: minimalista, nomes emmagatzema imatges. Pocs recursos.
- Harbor: te UI web, LDAP, escaneig de vulnerabilitats, replicacio. Molts recursos.
- Al BernatLab amb 4 GB de RAM, Harbor es massa?
- Es pot començar amb `registry:2` i migrar a Harbor mes endavant?
- Trade-off final: funcionalitat vs simplicitat.
