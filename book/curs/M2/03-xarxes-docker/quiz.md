# Qüestionari - Capitol 3: Xarxes Docker

> 10 preguntes · ~15 min

## Pregunta 1
Quin driver de xarxa Docker es el que ve per defecte?

- [ ] host
- [ ] overlay
- [x] bridge
- [ ] none

## Pregunta 2
Quina comanda crea una xarxa bridge custom?

- [ ] docker network new xarxa
- [x] docker network create xarxa
- [ ] docker create network xarxa
- [ ] docker network add xarxa

## Pregunta 3
Per que es recomana usar xarxes bridge custom en lloc de la bridge per defecte?

- [ ] Perque gasten menys memoria
- [x] Perque permeten resolucio DNS per nom entre contenidors
- [ ] Perque son mes segures per defecte
- [ ] Perque ocupen menys CPU

## Pregunta 4
Que significa `--network host`?

- [ ] El contenidor nomes pot comunicar-se amb l'amfitrio
- [x] El contenidor comparteix la pila de xarxa de l'amfitrio
- [ ] El contenidor te xarxa pero nomes per a l'amfitrio
- [ ] El contenidor nomes pot accedir a localhost

## Pregunta 5
Quan usaries `--network none`?

- [ ] Per maxim rendiment
- [x] Per ailllar completament el contenidor de qualsevol xarxa
- [ ] Per defecte sempre
- [ ] Per accedir al núvol

## Pregunta 6
Quina flag mapeja un port de l'amfitrio a un port del contenidor?

- [ ] -e
- [x] -p
- [ ] -v
- [ ] -w

## Pregunta 7
Quina comanda llista totes les xarxes Docker?

- [ ] docker ps
- [ ] docker network list
- [x] docker network ls
- [ ] docker networks

## Pregunta 8
Que fa `docker network connect app-net contenidor`?

- [ ] Crea un nou contenidor
- [x] Connecta un contenidor existent a la xarxa app-net
- [ ] Esborra el contenidor
- [ ] Reinicia la xarxa

## Pregunta 9 (oberta)
Explica amb les teves paraules: quina diferencia hi ha entre un port mapejat amb `-p` i l'acces directe entre contenidors de la mateixa xarxa? Posa un exemple.

Pistes per respondre:
- Quan exposes un port amb `-p`, qui pot accedir-hi?
- Quan dos contenidors son a la mateixa xarxa, com es parlen?
- Es bona idea exposar la base de dades amb `-p`?

## Pregunta 10 (oberta)
Tens una app amb tres serveis: frontend (nginx), backend (node) i base de dades (postgres). Voleu que nomes el frontend sigui accessible des de fora, i que backend i db es comuniquin nomes entre ells (mai exposats). Com ho muntaries amb Docker? Explica quantes xarxes necessites i quins serveis van a quina.

Pistes per respondre:
- Quantes xarxes farien falta? Una sola no protegeix prou.
- On posaries el frontend per a que sigui accessible?
- Com asseguraries que la base de dades nomes es vegi desde el backend?
