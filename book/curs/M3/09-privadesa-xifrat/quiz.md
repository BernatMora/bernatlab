# Qüestionari - Capitol 9: Privadesa i xifrat de fitxers

> 15 preguntes · ~20 min

## Pregunta 1
Quin tipus de xifratge usa la mateixa clau per xifrar i desxifrar?

- [x] Simetric
- [ ] Asimetric
- [ ] Hibrid
- [ ] Quant

## Pregunta 2
Quin es lavantatge principal dedat sobre GPG?

- [ ] Es mes antic
- [x] Es molt mes simple
- [ ] Xifra mes rapid
- [ ] Te mes funcions

## Pregunta 3
Quina ordre faries servir per generar un parell de claus amb age?

- [ ] age --gen-key
- [x] age-keygen -o key.txt
- [ ] gpg --gen-key
- [ ] openssl genrsa

## Pregunta 4
Que vol dir que un backup estigui "xifrat en repos"?

- [x] Que les dades estan xifrades al disc o al núvol
- [ ] Que nomes es pot accedir amb internet
- [ ] Que nomes el creador el pot veure
- [ ] Que nomes funciona a Linux

## Pregunta 5
Quin es lalgorisme de xifratge que fa servir age per defecte?

- [ ] AES-256
- [x] ChaCha20-Poly1305
- [ ] RSA-2048
- [ ] 3DES

## Pregunta 6
Quina es la master password en un gestor de contrasenyes?

- [x] La contrasenya principal que xifra tot el gestor
- [ ] La contrasenya de correu electronic
- [ ] La contrasenya del router
- [ ] La contrasenya del servidor

## Pregunta 7
Per que NO sha de desar la clau privada al mateix disc que les dades xifrades?

- [x] Si es perd el disc, perds les dades i la clau per desxifrar-les
- [ ] Es mes lent
- [ ] No funciona
- [ ] Es illegal

## Pregunta 8
Quin tipus de xifratge fa servir SSH per defecte?

- [ ] Simetric amb AES
- [x] Asimetric amb RSA/Ed25519
- [ ] Sense xifratge
- [ ] Quant

## Pregunta 9 (oberta)
Per que age hauries de preferir-lo a GPG per xifrar un sol fitxer individual? Compara el flux de treball pas a pas.

Pistes per respondre:
- Quantes ordres necessites amb age vs amb GPG?
- Quina eina te una clau mes curta i facil?
- Quina te una corba daprenentatge mes baixa?
- Quina eina te un codi base mes petit (menys superficie datac)?

## Pregunta 10 (oberta)
Dissenya una estrategia de privadesa per a l'hort IoT del BernatLab. Quins tipus de dades tens, quines son sensibles, i com les protegeixes.

Pistes per respondre:
- Quines dades son publiques (temperatura, humitat)?
- Quines son privades (adreça, contractes)?
- Quines son secrets (contrasenyes, claus)?
- Quin gestor de contrasenyes uses?
- Com xifres els fitxers sensibles?

## Pregunta 11 (oberta)
Per que creus que la gent sovint no xifra les seves dades personals al homelab tot i tenir-ne la possibilitat? Quines consequencies te al BernatLab si no ho fas?

Pistes per respondre:
- "No tinc res a amagar": falsa seguretat.
- "Es molt complicat": amb age ja no.
- "Si perdo lordinador, ja se": pero mentrestant.
- Cas concret: la RPi es robada, totes les dades queden exposades.
- Trade-off:conveniencia vs privacitat.

## Pregunta 12 (oberta)
Quina relacio hi ha entre la gestio de claus i la seguretat del xifratge? Per que al BernatLab cal un esquema clar de gestio de claus (master password, paper backup, etc)? Dona exemples de fallades comuns.

Pistes per respondre:
- Si perds la master password, perds TOT.
- Si deixes la clau al mateix disc, el xifratge es inutil.
- Si la clau es massa simple, es pot trencar.
- Bones practiques: paper backup en caixa forta, gestor de contrasenyes, etc.

## Pregunta 13 (oberta)
Imagina que el teu company et diu: "el HTTPS ja xifra totes les meves dades, no cal mes". Argumenta per que aixo es fals al BernatLab i proposa una estrategia completa de xifratge.

Pistes per respondre:
- HTTPS nomes xifra en transit.
- Al servidor, les dades estan en clar.
- Si el servidor es compromet, tot es accessible.
- Cal xifratge en reposo (discs) i de fitxers sensibles.
- Estrategia: discs xifrats + age per secrets + HTTPS per acces.

## Pregunta 14 (oberta)
Aplica el concepte de xifratge al cas concret del BernatLab amb l'hort IoT. Tinc 5 sensors, una base de dades InfluxDB amb lectures, un script Python de processament, i un fitxer .env amb credencials. Quins elements xifraries i com?

Pistes per respondre:
- Lectures de sensors: publiques (no xifrar).
- .env: xifrar amb age o guardar fora del repo.
- Script Python: nomes si conte secrets.
- Base de dades: potser no cal (dades publicables).
- Backups al núvol: xifrats amb restic.

## Pregunta 15 (oberta)
Quines consequencies te per a la sostenibilitat del projecte a llarg termini la perdua de les claus de xifratge al BernatLab? Argumenta amb exemples de quan aixo passa i com es pot prevenir.

Pistes per respondre:
- Si perds la master password de Bitwarden, perds totes les contrasenyes.
- Si perds la clau d'un backup xifrat, perds les dades.
- Si la clau esta nomes al cervell i mors, els hereus no poden accedir.
- Bones practiques: paper backup en caixa forta, donacio de claus a familiar de confiança.
- Trade-off: seguretat vs accessibilitat.
