# Qüestionari - Capitol 1: Estrategia de backup

> 15 preguntes · ~20 min

## Pregunta 1
Quantes copies de les dades recomana la regla 3-2-1?

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
Que vol dir la part de "1 fora de casa"?

- [ ] Que el servidor ha d'estar fora de casa
- [x] Que almenys una copia ha d'estar en un lloc fisic diferent
- [ ] Que el backup sha de fer un cop a l'any
- [ ] Que cal un ordinador adicional

## Pregunta 4
Quina daquestes dades es la MES critica al BernatLab?

- [ ] El sistema operatiu Debian
- [x] Les bases de dades amb lectures dels sensors
- [ ] Les imatges Docker
- [ ] La configuracio de xarxa

## Pregunta 5
Que vol dir RPO?

- [ ] Rendiment de Processament Operatiu
- [x] El temps maxim de dades que estic disposat a perdre
- [ ] Una eina de backup de Linux
- [ ] El temps que triga a fer-se el backup

## Pregunta 6
Per que Dropbox NO es un bon backup?

- [x] Perque si esborres un fitxer, Dropbox lesborra tambe
- [ ] Perque es massa car
- [ ] Perque no te versio mobil
- [ ] Perque no funciona amb Linux

## Pregunta 7
Quina frequencia es prudent per fer backup d'una base de dades amb dades de sensors IoT?

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
Explica amb les teves paraules que significa la regla 3-2-1 i posa un exemple aplicat a l'hort IoT del BernatLab.

Pistes per respondre:
- Quantes copies tens? On son?
- Quins suports diferents uses?
- Quina de les copies esta fora de casa?

## Pregunta 10 (oberta)
Imagina que guardes les lectures de l'hort en una base de dades SQLite a la RPi. Quina estrategia de backup triaries i amb quina frequencia? Justifica la resposta.

Pistes per respondre:
- Pensa en el RPO que vols.
- On posaries cada copia.
- Que passaria si es trenca la RPi un dimarts a les 3 de la tarda.

## Pregunta 11 (oberta)
Per que creus que la gent tendeix a minimitzar la importancia dels backups fins que perd dades? Com afecta al BernatLab aquesta tendencia? Argumenta amb exemples emocionals i practics.

Pistes per respondre:
- Optimisme irracional: "a mi no em pasara".
- Cost tangible vs benefici intangible.
- Cas concret: perdre 5 anys de lectures de l'hort.

## Pregunta 12 (oberta)
Quina relacio hi ha entre el RPO (Recovery Point Objective) i el RTO (Recovery Time Objective)? Com es relacionen amb el cost del backup al BernatLab (100.115.134.76)? Calcula exemples concrets.

Pistes per respondre:
- RPO: quant de dades puc perdre.
- RTO: quant de temps trigare a restablir el servei.
- RPO baix = backups frequents = mes cost.
- RTO baix = infraestructura de recuperacio = mes cost.

## Pregunta 13 (oberta)
Imagina que el teu company et diu: "tinc el núvol, ja estic salvat". Explica-li per que Dropbox o Google Drive no son un backup real i proposa una alternativa adequada al BernatLab.

Pistes per respondre:
- Que passa amb un borrat accidental sincronitzat al núvol?
- Que passa amb un compte compromes?
- Que passa amb ransomware que xifra els fitxers locals i sincronitza el xifrat al núvol?
- Diferencia entre sincronitzacio i backup.

## Pregunta 14 (oberta)
Aplica el concepte d'estrategia de backup al cas concret del BernatLab amb l'hort IoT: tens 5 sensors escrivint lectures cada 10 minuts a una base de dades, mes una coleccio de 200 fotos dels bancals, mes la configuracio del sistema. Dissenya una estrategia completa de backup especificant que copies, on, cada quan.

Pistes per respondre:
- Lectures de sensors: alta frequencia, petits canvis cada vegada.
- Fotos: baixa frequencia, fitxers grans.
- Configuracio: canvis esporadics, fitxers petits.
- Quin RPO per a cada un?

## Pregunta 15 (oberta)
Quines consequencies te per a la sostenibilitat del projecte (a llarg termini) tenir una estrategia de backup deficient al BernatLab? Com afecta la teva capacitat d'innovar i provar coses noves si tens por de perdre el que ja tens?

Pistes per respondre:
- Por de perdre dades frena l'experimentacio.
- "Si es trenca, ho torno a fer" nomes funciona si tens backup.
- La confianca en la recuperacio permet provar coses noves.
- Mentalitat: backup = llicencia per experimentar.
