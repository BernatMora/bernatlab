# Qüestionari — Capítol 1: Què és BernatLab

> 15 preguntes · ~20 min · Pots repetir les vegades que vulguis.

## Pregunta 1
Què és un homelab?

- [ ] Un tipus de router professional
- [x] Un servidor personal a casa, per aprendre i experimentar
- [ ] Una empresa de hosting
- [ ] Un sistema operatiu per a servidors

## Pregunta 2
Quin és el cor del BernatLab?

- [ ] Un PC de gamma alta
- [ ] Un servidor al núvol
- [x] Una Raspberry Pi 4 amb Debian 13
- [ ] Un Mac mini

## Pregunta 3
Per què serveix Tailscale al BernatLab?

- [ ] Per fer còpies de seguretat
- [ ] Per accelerar la xarxa local
- [x] Per accedir al servidor des de fora sense obrir ports al router
- [ ] Per monitoritzar la temperatura

## Pregunta 4
Quants serveis principals té desplegats ara el BernatLab?

- [ ] 2 (Docker + Portainer)
- [x] 5 (Docker, Portainer, Uptime Kuma, Homepage, Tailscale)
- [ ] 10
- [ ] 20

## Pregunta 5
Veritable o fals: Tots els serveis del BernatLab corren directament sobre la Raspberry Pi, sense virtualització ni contenidors.

- [ ] Verdader
- [x] Fals (corren dins de contenidors Docker)

## Pregunta 6
Quin servei té el port 9443?

- [ ] Homepage
- [x] Portainer
- [ ] Uptime Kuma
- [ ] Tailscale

## Pregunta 7
Quin servei té el port 3001?

- [ ] Homepage
- [ ] Portainer
- [x] Uptime Kuma
- [ ] Tailscale

## Pregunta 8
Emplena el buit: La URL de la web pública d'Hort Osona és https://bernatmora.github.io/______/

- [x] hort-osona
- [ ] bernatlab
- [ ] homelab
- [ ] pwa

## Pregunta 9
Quin és el hostname de la teva Raspberry Pi al BernatLab?

- [ ] bernatlab
- [x] hortosona
- [ ] rpi4
- [ ] localhost

## Pregunta 10
Quina és la IP Tailscale fixa que té assignada la RPi al BernatLab?

- [ ] 192.168.1.50
- [ ] 10.0.0.76
- [x] 100.115.134.76
- [ ] 172.16.134.76

## Pregunta 11
Quin avantatge principal té allotjar serveis a casa (homelab) respecte a un núvol públic (AWS, Google Cloud)?

- [ ] Més ample de banda
- [x] Control total de les dades, privacitat i cost recurrent zero
- [ ] Millor suport tècnic 24/7
- [ ] Adreça IP pública fixa gratuïta

## Pregunta 12
Quin dels següents NO és un benefici típic de muntar un homelab?

- [ ] Aprendre Linux i xarxes de forma pràctica
- [ ] Autoallotjar aplicacions privades
- [x] Obtenir SLA del 99,99% garantit
- [ ] Experimentar sense por de trencar res

## Pregunta 13 (oberta)
Explica amb les teves paraules: quina diferència hi ha entre allotjar les teves dades a Google Drive (al núvol) i allotjar-les al teu BernatLab (a casa)?

Pistes per respondre:
- On són les dades físicament?
- Qui hi té accés?
- Què passa si falla internet?
- Què passa si Google canvia les condicions?

## Pregunta 14 (oberta)
De la llista de serveis del BernatLab, quin et sembla més important i per què?

Pistes per respondre:
- Pensa en el teu cas real (feina, oci, aprenentatge).
- Raona per què l'esculls.
- Una resposta d'un parell de paràgrafs és suficient.

## Pregunta 15 (oberta)
Imagina que d'aquí un any vols vendre la teva Raspberry Pi o deixar-la a un amic. Quina informació hauries de deixar documentada perquè aquesta persona pogués continuar el projecte sense la teva ajuda? Pensa en el pitjor cas: que no li puguis respondre cap missatge.

Pistes per respondre:
- Quines credencials caldria saber canviar?
- Quins serveis depenen de què?
- On és la "veritat" del sistema (configuració vs dades)?
- Com es recupera tot des de zero?
