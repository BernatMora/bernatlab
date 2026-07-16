# Qüestionari - Capitol 5: Registre d'imatges

> 10 preguntes · ~15 min

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
