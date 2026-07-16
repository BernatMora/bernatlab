# Qüestionari - Capitol 1: Amenaces comunes

> 10 preguntes · ~15 min

## Pregunta 1
Què és un atac de "bruteforce" contra SSH?

- [ ] Un atac que aprofita un bug a OpenSSH per entrar sense contrasenya
- [x] Un atac que prova milers de combinacions d'usuari i contrasenya automaticament
- [ ] Un atac que desconfigura el servei SSH perque no funcioni
- [ ] Un atac que nomes funciona amb claus SSH, no amb contrasenyes

## Pregunta 2
Quin es el port per defecte del servei SSH?

- [ ] 21
- [ ] 80
- [ ] 443
- [x] 22

## Pregunta 3
Què significa "superficie d'atac"?

- [ ] La quantitat de memoria RAM que pot fer servir un atacant
- [x] El conjunt de punts per on un atacant podria entrar al sistema
- [ ] El tamany fisic del servidor
- [ ] La velocitat de la xarxa de l'atacant

## Pregunta 4
Quin usuari es el mes atacat per defecte en una RPi?

- [ ] bernat
- [ ] admin
- [x] pi
- [ ] user

## Pregunta 5
Que vol dir "CVE"?

- [ ] Central Vulnerability Endpoint
- [x] Common Vulnerabilities and Exposures
- [ ] Certified Virtual Environment
- [ ] Common Virus Encyclopedia

## Pregunta 6
Quina ordre mostra els ultims intents de login fallits al sistema?

- [ ] `sudo last`
- [x] `sudo lastb`
- [ ] `who`
- [ ] `ps aux`

## Pregunta 7
Per que es dolent exposar mes ports dels necessaris?

- [ ] Perque consumeix mes bateria
- [x] Perque cada port obert es un posible vector d'entrada per un atacant
- [ ] Perque el router es torna mes lent
- [ ] No es dolent, nomes ocupa memoria

## Pregunta 8
Quina eina fan servir els atacants per descobrir quins serveis te un servidor?

- [ ] ping
- [x] nmap
- [ ] curl
- [ ] ssh

## Pregunta 9 (oberta)
Descriu quines son les principals amenaces a la RPi del BernatLab. Quines son les mes probables i quines no t'amoïnen gaire? Justifica-ho breument.

Pistes per respondre:
- Pensa en els serveis que exposures actualment.
- Considera si la RPi esta a una xarxa privada o publica.
- Recorda que el perfil d'atacant mes habitual es un bot automatic, no un hacker personalitzat.
- Esmenta almenys 3 amenaces i classifica-les en risc alt/mitja/baix.

## Pregunta 10 (oberta)
Explica que vol dir "defensa en profunditat" (defense in depth). Per que no es suficient amb una sola mesura de seguretat, per bona que sigui?

Pistes per respondre:
- Pensa en analogies de la vida real (una casa, un cotxe, una caixa forta).
- Explica que cada capa te la seva funcio i la seva debilitat.
- Dona un exemple concret aplicat al servidor: que passa si nomes tens firewall pero et roben la SD?
- Esmenta almenys 3 capes diferents que combinarem al llarg del modul.
