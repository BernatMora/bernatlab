# Qüestionari - Capitol 6: Seguretat de contenidors

> 10 preguntes · ~15 min

## Pregunta 1
Quin es el principal risc de seguretat si un contenidor s'executa com a root?

- [ ] Que el contenidor vagi mes lent
- [x] Que si algú l'explota, tindra acces de root a l'amfitrio (o be a mes recursos)
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

- [ ] Xifrar el tràfic
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
