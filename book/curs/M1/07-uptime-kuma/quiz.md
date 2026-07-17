# Qüestionari — Capítol 7: Uptime Kuma

> 15 preguntes · ~20 min

## Pregunta 1
Què és Uptime Kuma?

- [ ] Un sistema operatiu
- [x] Una eina self-hosted de monitoratge de serveis amb alertes
- [ ] Un client de correu
- [ ] Un editor de fotos

## Pregunta 2
A quin port per defecte escolta Uptime Kuma?

- [ ] 8080
- [ ] 9000
- [x] 3001
- [ ] 9090

## Pregunta 3
Quin tipus de monitor comprova que una URL retorni 200 OK?

- [ ] Ping
- [x] HTTP(s)
- [ ] TCP
- [ ] DNS

## Pregunta 4
Quin canal d'alertes és el recomanat al BernatLab per la seva immediatesa?

- [ ] Email
- [x] Telegram
- [ ] SMS
- [ ] Fax

## Pregunta 5
Quin és el primer pas per configurar alertes de Telegram?

- [ ] Instal·lar el mòdul de Telegram a Uptime Kuma
- [x] Crear un bot amb @BotFather i obtenir el token
- [ ] Configurar el DNS de Telegram
- [ ] Comprar el pla premium de Telegram

## Pregunta 6
Què és una Status Page?

- [ ] Una pàgina web personal
- [x] Una pàgina pública que mostra l'estat dels serveis monitorats
- [ ] Un tipus de monitor
- [ ] Una eina per crear temes

## Pregunta 7
Cada quan és recomanable configurar un monitor HTTP a Uptime Kuma?

- [ ] Cada segon
- [x] Entre 30 i 300 segons, segons la criticitat
- [ ] Un cop al dia
- [ ] Un cop per setmana

## Pregunta 8
Quin avantatge té muntar `/var/run/docker.sock` al contenidor d'Uptime Kuma?

- [x] Permet monitors de tipus Docker Container que consulten l'estat dels contenidors
- [ ] Fa que el contenidor s'arrenqui més ràpid
- [ ] Redueix l'ús de CPU
- [ ] Permet actualitzacions automàtiques

## Pregunta 9
Quin tipus de monitor comprova que un port concret estigui obert?

- [ ] HTTP
- [x] TCP Port
- [ ] Ping
- [ ] DNS

## Pregunta 10
Quantes vegades ha de fallar un monitor abans que Uptime Kuma enviï una alerta?

- [ ] A la primera
- [x] Configurable, per defecte 1 però es pot apujar per evitar falsos positius
- [ ] 10
- [ ] Mai

## Pregunta 11
Què mostra un gràfic "uptime" a Uptime Kuma?

- [ ] El temps encesos de la RPi
- [x] El percentatge de temps que el servei ha estat UP
- [ ] La velocitat de resposta
- [ ] L'ús de CPU

## Pregunta 12
Què és un "heartbeat" o "push monitor"?

- [ ] Un monitor que Uptime Kuma envia al servei
- [x] Un monitor on el servei envia un senyal periòdic a Uptime Kuma
- [ ] Un tipus d'alerta
- [ ] Un canal de Telegram

## Pregunta 13 (oberta)
Explica amb les teves paraules: quins 4-5 serveis del BernatLab monitoraries amb Uptime Kuma, i per què tries cada tipus de monitor (ping, HTTP, TCP, etc.)?

Pistes per respondre:
- Quins serveis tens actualment? (portainer, whoami, ssh...)
- Quins són els més crítics?
- Què passa si un d'ells cau sense que te n'adonis?
- Hi ha serveis que NO té sentit monitorar (per què)?

## Pregunta 14 (oberta)
Descriu el flux complet: configurem una alerta de Telegram perquè quan Portainer caigui, ho sàpigues al mòbil en menys de 2 minuts. Quins passos cal fer?

Pistes per respondre:
- Què has de fer a Telegram (@BotFather, xat)?
- Què has de fer a Uptime Kuma (Settings, Notifications)?
- Com es dispara l'alerta quan un monitor falla?
- Què passa si el bot falla (alertes perdudes)?

## Pregunta 15 (oberta)
Ets a fora de casa i reps una alerta: "Portainer is DOWN". Enumera els passos que faries per diagnosticar i resoldre el problema sense tenir accés físic a la RPi.

Pistes per respondre:
- Pots entrar per SSH? (Tailscale està actiu?)
- Com mires els logs sense Portainer?
- Com reinicies Docker sense Portainer?
- Quan és acceptable "tornar-ho a provar més tard" i quan cal actuar ja?
