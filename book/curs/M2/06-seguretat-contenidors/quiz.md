# Qüestionari - Capitol 6: Seguretat de contenidors

> 15 preguntes · ~20 min

## Pregunta 1
Quin es el principal risc de seguretat si un contenidor s'executa com a root?

- [ ] Que el contenidor vagi mes lent
- [x] Que si algu l'explota, tindra acces de root a l'amfitrio (o be a mes recursos)
- [ ] Que el contenidor consumeixi mes memoria
- [ ] Cap, root es el correcte sempre

## Pregunta 2
Quina opcio del `docker run` executa el contenidor com un usuari no-root?

- [ ] --no-root
- [x] --user 1000:1000
- [ ] --rootless
- [ ] --safe

## Pregunta 3
Que es rootless Docker?

- [ ] Un contenidor que no te arrel
- [x] Docker que s'executa sense root a l'amfitrio (utilitza user namespaces)
- [ ] Un contenidor que nomes pot llegir fitxers
- [ ] Un registre de noms

## Pregunta 4
Quina instruccio del Dockerfile redueix les capabilities de Linux que te el contenidor per defecte?

- [ ] CAPS=DROP
- [x] --cap-drop=ALL
- [ ] --security-opt=none
- [ ] --no-priv

## Pregunta 5
Quin sistema de fitxers de nomes lectura es recomana per maximitzar la seguretat?

- [ ] ext4
- [x] Un sistema de fitxers montat nomes de lectura
- [ ] NFS
- [ ] BTRFS

## Pregunta 6
Que permet `docker scan`?

- [ ] Escanar la xarxa
- [x] Analitzar vulnerabilitats conegudes a les imatges Docker
- [ ] Escanar ports oberts
- [ ] Esborrar imatges

## Pregunta 7
Per que es recomanable posar --read-only a un contenidor?

- [ ] Per a que vagi mes rapid
- [x] Perque el sistema de fitxers del contenidor no es pugui modificar (nomes pot escriure a volums/tmpfs)
- [ ] Per a que ocupi menys memoria
- [ ] Per a que no es pugui actualitzar

## Pregunta 8
Quin es l'objectiu de `seccomp` (secure computing mode)?

- [ ] Xifrar el trafic
- [x] Restringir les syscalls que un proces pot fer al kernel
- [ ] Autenticar usuaris
- [ ] Detectar intrusions

## Pregunta 9 (oberta)
Explica amb les teves paraules: quins son els tres vectors d'atac mes comuns contra un contenidor Docker mal configurat? Dona exemples concrets.

Pistes per respondre:
- Execucio com a root: si el contenidor es root, un exploit te acces massiu.
- Capacitats excessives: per defecte Docker ja en treu moltes, pero si les hi tornes totes, es perillos.
- Xarxa exposada: ports oberts sense filtre, secrets al fitxer compose.
- Imatges vulnerables: sense actualitzar des de fa mesos.

## Pregunta 10 (oberta)
Al BernatLab tens un Nextcloud que serveix fitxers personals. Quines mesures de seguretat aplicaries al contenidor per minimitzar la superficie d'atac? Fes una llista amb minim 5 mesures i explica cada una breument.

Pistes per respondre:
- Usuari no-root.
- Capacitats minimes.
- Read-only filesystem.
- Xarxa aillada.
- Sense privilegis.
- Imatge oficial actualitzada.

## Pregunta 11 (oberta)
Per que creus que Docker, per defecte, ja treu un munt de capabilities de Linux als contenidors? Quines d'aquestes capabilities son les mes perilloses si un atacant les te? Dona exemples.

Pistes per respondre:
- Docker nomes deixa les capabilities estrictament necessaries.
- CAP_NET_RAW, CAP_SYS_ADMIN, CAP_SYS_PTRACE son especialment perilloses.
- Que pot fer un atacant amb CAP_SYS_ADMIN dins el contenidor?
- Es important entendre que "root dins el contenidor" != "root de l'amfitrio" gracies a aquestes restriccions.

## Pregunta 12 (oberta)
Quina relacio hi ha entre la seguretat d'un contenidor i la cadena de subministrament (supply chain)? Com afecta al BernatLab descarregar una imatge random de Docker Hub versus construir-te la teva propia? Argumenta amb exemples reals.

Pistes per respondre:
- Si la imatge base te un backdoor, tu heretes el backdoor.
- Imatges "oficials" (Docker Official Images) son mes segures perque son auditades.
- Construir la teva imatge et dona control total pero requereix manteniment.
- Trade-off: comoditat de Docker Hub vs seguretat d'imatges prpies.
- Es pot verificar la integritat amb hashes i signatures.

## Pregunta 13 (oberta)
Imagina que el teu company et diu: "el meu Nextcloud porta mes de 2 anys sense actualitzar i funciona perfectament". Argumenta per que aixo es una mala practica de seguretat, especialment si el servei esta exposat a internet al BernatLab (100.115.134.76).

Pistes per respondre:
- Cada mes es troben noves vulnerabilitats a Nextcloud, PHP, llibreries.
- Un exploit public pot comprometre el sistema en hores.
- Mantenir actualitzat es la mesura de seguretat mes barata.
- Watchtower (M2 cap 7) pot automatitzar les actualitzacions.
- El temps mitja entre vulnerabilitat publica i exploit es cada vegada mes curt.

## Pregunta 14 (oberta)
Aplica els conceptes del capitol al cas concret del BernatLab amb un servei web public (Nextcloud o Immich) exposat a internet. Escriu mentalment un tros del `docker-compose.yml` que apliqui totes les mesures de seguretat que coneixes: usuari no-root, read-only, drop capabilities, xarxa aillada, limits de memoria i CPU. Justifica cada decisio.

Pistes per respondre:
- USER 1000: evitar execucio com a root.
- read_only: true: filesystem immutable.
- tmpfs per a directoris que necessiten escriptura (/tmp, /var/cache).
- cap_drop: ALL: nomes el que cal.
- security_opt: no-new-privileges:true: evitar escalada de privilegis.
- mem_limit: evitar DoS per memoria.

## Pregunta 15 (oberta)
Quines consequencies te per a la funcionalitat del servei aplicar mesures de seguretat molt agressives? Troba un equilibri raonable per al BernatLab. Pensa en: usabilitat, manteniment, risc real i temps dedicat a seguretat.

Pistes per respondre:
- Molta seguretat = molta feina de manteniment.
- Un contenidor massa restringit pot no funcionar correctament.
- Cal distingir entre serveis exposats a internet i serveis interns.
- Al BernatLab, els serveis exposats a internet mereixen mes cura que els interns.
- Es acceptable tenir una politica de seguretat mes laxa per a eines internes de desenvolupament?
