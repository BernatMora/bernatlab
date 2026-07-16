# Qüestionari — Capítol 9: Git i documentació

> 10 preguntes · ~15 min

## Pregunta 1
Què és Git?

- [ ] Un editor de text
- [x] Un sistema de control de versions distribuït
- [ ] Un sistema operatiu
- [ ] Un llenguatge de programació

## Pregunta 2
Quina ordre inicialitza un repositori Git al directori actual?

- [ ] git start
- [x] git init
- [ ] git create
- [ ] git new

## Pregunta 3
Què és l'estat "staging" a Git?

- [ ] El directori de treball
- [x] L'àrea on preparem els canvis abans de fer commit
- [ ] El repositori remot
- [ ] Una branca experimental

## Pregunta 4
Quin fitxer serveix per excloure fitxers del repositori?

- [ ] .gitconfig
- [ ] .gitignore
- [ ] .exclude
- [ ] .skip

## Pregunta 5
Quina ordre afegiria tots els canvis al staging?

- [ ] git commit
- [x] git add .
- [ ] git stage
- [ ] git push

## Pregunta 6
Quina ordre mostra l'historial de commits en format curt?

- [ ] git history
- [x] git log --oneline
- [ ] git list
- [ ] git show

## Pregunta 7
Quin és el risc de fer `git reset --hard`?

- [ ] És lent
- [x] Esborra commits i canvis no guardats de forma irreversible
- [ ] Causa conflictes
- [ ] Res, és segur

## Pregunta 8
Per a què serveix un fitxer CHANGELOG.md?

- [ ] Per emmagatzemar logs de Docker
- [x] Per registrar canvis importants del projecte amb data
- [ ] Per documentar l'API
- [ ] Per guardar la configuració

## Pregunta 9 (oberta)
Explica amb les teves paraules: per què és important versionar l'homelab? Posa 3 motius pràctics.

Pistes per respondre:
- Què passa si la SD es trenca?
- Què passa si toques algo i es trenca un servei?
- Quin avantatge té un README per a tu mateix d'aquí 6 mesos?

## Pregunta 10 (oberta)
Descriu el flux per afegir un nou servei (per exemple, PiHole) i que el canvi quedi versionat correctament al repo del BernatLab. Quins passos faries?

Pistes per respondre:
- Editar el docker-compose.yml.
- Actualitzar el services.yaml de Homepage.
- Fer el commit.
- Comprovar que ha entrat bé.
