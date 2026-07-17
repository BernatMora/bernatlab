# Qüestionari — Capítol 9: Git i documentació

> 15 preguntes · ~20 min

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
- [x] .gitignore
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

## Pregunta 9
Quina diferència hi ha entre `git pull` i `git fetch`?

- [ ] Són el mateix
- [x] `fetch` descarrega canvis; `pull` descarrega i fusiona
- [ ] `pull` és per a un commit; `fetch` per a una branca
- [ ] `pull` és local; `fetch` és remot

## Pregunta 10
Què és una "branch" a Git?

- [ ] Un commit especial
- [x] Una línia de desenvolupament independent
- [ ] Un tipus de fitxer
- [ ] Una eina externa

## Pregunta 11
Què és un "merge conflict"?

- [ ] Un error de xarxa
- [x] Quan dos canvis a la mateixa línia no es poden fusionar automàticament
- [ ] Un commit fallit
- [ ] Un problema amb el .gitignore

## Pregunta 12
Quin avantatge té un README.md en un projecte tècnic?

- [ ] Fer-lo més llarg
- [x] Explicar ràpidament què és i com començar
- [ ] Documentar l'API
- [ ] Guardar secrets

## Pregunta 13 (oberta)
Explica amb les teves paraules: per què és important versionar l'homelab? Posa 3 motius pràctics.

Pistes per respondre:
- Què passa si la SD es trenca?
- Què passa si toques algo i es trenca un servei?
- Quin avantatge té un README per a tu mateix d'aquí 6 mesos?
- Quin avantatge té un registre de decisions (ADR)?

## Pregunta 14 (oberta)
Descriu el flux per afegir un nou servei (per exemple, PiHole) i que el canvi quedi versionat correctament al repo del BernatLab. Quins passos faries?

Pistes per respondre:
- Editar el docker-compose.yml.
- Actualitzar el services.yaml de Homepage.
- Fer el commit.
- Comprovar que ha entrat bé.
- Què passa si canvies un servei existent (vs. afegir-ne un de nou)?

## Pregunta 15 (oberta)
Imagina que el 15 de març de 2027 vols reproduir l'estat exacte del teu BernatLab d'avui. Quina informació necessites tenir versionada i quina NO? Posa exemples concrets.

Pistes per respondre:
- La configuració (docker-compose.yml) ha d'estar al repo?
- Les dades dels volums (bases de dades, fitxers pujats) han d'estar al repo?
- Com ho faries per clonar la RPi en una màquina nova?
- Quin paper juga un sistema de backup extern?
