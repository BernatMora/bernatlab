# Qüestionari — Capítol 1: Estratègia de backup

> 10 preguntes · ~15 min

## Pregunta 1
Quantes còpies de les dades recomana la regla 3-2-1?

- [ ] 1
- [ ] 2
- [x] 3
- [ ] 5

## Pregunta 2
Quants suports DIFERENTS recomana la regla 3-2-1?

- [ ] 1
- [x] 2
- [ ] 3
- [ ] Tots els que puguis

## Pregunta 3
Què vol dir la part de "1 fora de casa"?

- [ ] Que el servidor ha d'estar fora de casa
- [x] Que almenys una còpia ha d'estar en un lloc físic diferent
- [ ] Que el backup s'ha de fer un cop a l'any
- [ ] Que cal un ordinador addicional

## Pregunta 4
Quina d'aquestes dades és la MÉS crítica al BernatLab?

- [ ] El sistema operatiu Debian
- [x] Les bases de dades amb lectures dels sensors
- [ ] Les imatges Docker
- [ ] La configuració de xarxa

## Pregunta 5
Què vol dir RPO?

- [ ] Rendiment de Processament Operatiu
- [x] El temps màxim de dades que estic disposat a perdre
- [ ] Una eina de backup de Linux
- [ ] El temps que triga a fer-se el backup

## Pregunta 6
Per què Dropbox NO és un bon backup?

- [x] Perquè si esborres un fitxer, Dropbox l'esborra també
- [ ] Perquè és massa car
- [ ] Perquè no té versió mòbil
- [ ] Perquè no funciona amb Linux

## Pregunta 7
Quina freqüència és prudent per fer backup d'una base de dades amb dades de sensors IoT?

- [ ] Un cop al mes
- [ ] Un cop per setmana
- [x] Cada 6-24 hores
- [ ] Cada 5 anys

## Pregunta 8
Quin servei al núvol recomano per a backups barats i privats?

- [ ] Google Drive
- [ ] iCloud
- [x] Backblaze B2
- [ ] OneDrive

## Pregunta 9 (oberta)
Explica amb les teves paraules què significa la regla 3-2-1 i posa un exemple aplicat a l'hort IoT del BernatLab.

Pistes per respondre:
- Quantes còpies tens? On són?
- Quins suports diferents uses?
- Quina de les còpies està fora de casa?

## Pregunta 10 (oberta)
Imagina que guardes les lectures de l'hort en una base de dades SQLite a la RPi. Quina estratègia de backup triaries i amb quina freqüència? Justifica la resposta.

Pistes per respondre:
- Pensa en el RPO que vols.
- On posaries cada còpia.
- Què passaria si es trenca la RPi un dimarts a les 3 de la tarda.
