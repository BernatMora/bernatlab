# Qüestionari — Capitol 9: Privadesa i xifrat de fitxers

> 10 preguntes · ~15 min

## Pregunta 1
Quin tipus de xifratge usa la mateixa clau per xifrar i desxifrar?

- [x] Simetric
- [ ] Asimetric
- [ ] Hibrid
- [ ] Quant

## Pregunta 2
Quin es l'avantatge principal d'edat sobre GPG?

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
Quin es l'algorisme de xifratge que fa servir age per defecte?

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
- Quina te una curva d'aprenentatge mes baixa?
- Quina eina te un codi base mes petit (menys superficie d'atac)?

## Pregunta 10 (oberta)
Dissenya una estrategia de privadesa per a l'hort IoT del BernatLab. Quins tipus de dades tens, quines son sensibles, i com les protegeixes.

Pistes per respondre:
- Quines dades son publiques (temperatura, humitat)?
- Quines son privades (adreça, contractes)?
- Quines son secrets (contrasenyes, claus)?
- Quin gestor de contrasenyes uses?
- Com xifres els fitxers sensibles?
