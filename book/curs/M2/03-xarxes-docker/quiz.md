# Qüestionari - Capitol 3: Xarxes Docker

> 15 preguntes · ~20 min

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

## Pregunta 11 (oberta)
Per que creus que Docker va triar crear una abstraccio de xarxa a sobre de les xarxes reals de Linux? Quins problemes et va estalviar respecte a configurar manualment `iptables`, `iptables-restore`, etc?

Pistes per respondre:
- Cada contenidor nomes veu una interficie "eth0" virtual.
- Els noms dels contenidors es resolen com a DNS intern.
- Les xarxes custom permeten aillar trafic per aplicacio.

## Pregunta 12 (oberta)
Quina relacio hi ha entre la topologia de xarxes i la superficie d'atac? Al BernatLab (100.x.y.z) amb 5 serveis, quantes xarxes crearies i quins serveis anirien junts? Dibuixa mentalment el graf de connexions.

Pistes per respondre:
- Xarxa publica: nomes el que toca internet.
- Xarxa backend: la resta.
- Que passa si un servei public es compromet? Pot accedir a la resta?
- DNS intern vs exposar ports a l'amfitrio.

## Pregunta 13 (oberta)
Imagina que el teu company et pregunta: "per que no posem tots els serveis en `network host`? Aixi no cal mapejar ports i es mes rapid". Explica-li quan te sentit i quan no, amb exemples del BernatLab.

Pistes per respondre:
- Rendiment: el mode host evita el doble NAT, es mes rapid.
- Ailllament: el mode host trenca l'ailllament, tot veu tot.
- Cas d'us valid: eines de monitoritzacio que necessiten veure moltes interficies.
- Cas invalid: serveis multi-tenant o amb dades sensibles.

## Pregunta 14 (oberta)
Aplica el concepte de xarxa al cas concret del BernatLab amb el sistema Hort Osona (Ollama, ChromaDB, Open WebUI). Explica quantes xarxes necessites, quins serveis van a quina xarxa, i quins ports (si n'hi ha) exposeixes a l'exterior. Per que es una bona practica?

Pistes per respondre:
- Open WebUI es la unica interficie que veu l'usuari.
- Ollama ha de ser accessible per WebUI pero potser no directament per l'exterior.
- ChromaDB nomes l'ha de veure Ollama.
- Que passa si exposes ChromaDB a internet? Es un risc.

## Pregunta 15 (oberta)
Quines consequencies te per al rendiment i la seguretat exposar ports amb `-p 0.0.0.0:80:80` en lloc de `-p 127.0.0.1:80:80`? Al BernatLab, quina estrategia de binding fas servir i per que?

Pistes per respondre:
- 0.0.0.0 vol dir accessible des de qualsevol interficie de xarxa.
- 127.0.0.1 nomes accessible des del propi amfitrio.
- Si el BernatLab nomes l'uses via VPN, quina combinacio te sentit?
- Si el BernatLab esta exposat a internet, quines capes de proteccio calen?
