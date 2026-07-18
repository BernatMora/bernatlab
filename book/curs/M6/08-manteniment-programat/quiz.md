# Qüestionari - Capitol 8: Manteniment programat

> 10 preguntes · ~15 min

## Pregunta 1
Per que es important el manteniment programat?

- [ ] Perque es obligatori per llei
- [x] Perque netejar i revisar periodicament evita problemes majors
- [ ] Perque queda be
- [ ] Perque Linux es romp sol

## Pregunta 2
Cada quant s'hauria de fer un backup de dades critiques?

- [ ] Un cop a l'any
- [ ] Un cop al mes
- [x] Diariament o segons la criticat
- [ ] Mai

## Pregunta 3
Quina comanda llista les imatges Docker amb la mida que ocupen?

- [ ] docker ls
- [x] docker system df
- [ ] docker image --size
- [ ] docker volume ls

## Pregunta 4
Quina comanda neteja els logs antics de journald mes antics de 14 dies?

- [ ] journalctl --clean
- [x] journalctl --vacuum-time=14d
- [ ] journalctl --delete-old
- [ ] logrotate --time=14

## Pregunta 5
Quina comanda neteja imatges Docker no usades?

- [x] docker image prune -a
- [ ] docker rmi -a
- [ ] docker clean
- [ ] docker system clean

## Pregunta 6
Quin es el risc de no verificar mai els backups?

- [ ] Cap, el backup sempre funciona
- [x] Que et puguis trobar amb un backup corrupte quan el necessitis
- [ ] Que el sistema vagi mes lent
- [ ] Que ocupi massa espai

## Pregunta 7
Quina eina s'encarrega de la rotacio automatica de logs tradicionals a Linux?

- [ ] cron
- [x] logrotate
- [ ] logrotate-d
- [ ] journald

## Pregunta 8
Cada quant es recomana netejar fisicament la RPi (pols)?

- [ ] Mai
- [ ] Cada 5 anys
- [x] Cada 6-12 mesos
- [ ] Cada setmana

## Pregunta 9 (oberta)
Defineix un calendari de manteniment per al teu BernatLab. Quines tasques faries setmanalment, mensualment, trimestralment i anualment? Dona temps estimat per cada tasca.

Pistes per respondre:
- Setmanal: revisar alertes, netejar brossa, mirar logs nous (30 min).
- Mensual: actualitzar manualment, verificar backups (1-2 h).
- Trimestral: tendencies, actualitzar imatges (2-3 h).
- Anual: canvis majors, neteja fisica (1-2 dies).

## Pregunta 10 (oberta)
Explica per que els backups son la part mes important del manteniment i que hauries de fer per assegurar que realment funcionen (i no son simplement "una copia en algun lloc").

Pistes per respondre:
- El backup nomes serveix si pots recuperar.
- Cal verificar periodicament (restaurar en entorn de test).
- Cal guardar fora de la RPi (un altre lloc fisic o cloud).
- Cal documentar com restaurar.
- Cal xifrar si son dades sensibles.


## Pregunta 11 (oberta amb pistes)
Per que es millor tenir un calendari de manteniment que fer coses quan es recorda

## Pregunta 12 (oberta amb pistes)
Explica que es una finestra de manteniment i com es planifica

## Pregunta 13 (oberta amb pistes)
Quines tasques setmanals, mensuals i anuals tindria el teu BernatLab
