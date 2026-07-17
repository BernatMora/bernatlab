# Qüestionari - Capitol 8: Sincronitzacio de fitxers

> 15 preguntes · ~20 min

## Pregunta 1
Quin protocol fa servir Syncthing per comunicar-se?

- [ ] HTTP sense xifrar
- [x] TLS (Transport Layer Security)
- [ ] FTP
- [ ] SMB

## Pregunta 2
Quina diferencia hi ha entre Syncthing i Dropbox?

- [ ] Syncthing nomes funciona a Linux
- [x] Syncthing es P2P (peer-to-peer); Dropbox passa per un servidor central
- [ ] Dropbox es mes segur
- [ ] Syncthing nomes sincronitza manualment

## Pregunta 3
Quina ordre rsync faries servir per sincronitzar una carpeta local a un servidor remot via SSH?

- [ ] rsync origen desti
- [x] rsync -av -e ssh origen/ usuari@host:/desti/
- [ ] scp -r origen desti
- [ ] cp -r origen desti

## Pregunta 4
Quin port usa la UI web de Syncthing per defecte?

- [ ] 80
- [ ] 8080
- [x] 8384
- [ ] 9090

## Pregunta 5
Que vol dir lopcio `-a` de rsync?

- [x] Archive: preserva permisos, dates, estructura
- [ ] Asynchronous
- [ ] Append
- [ ] All files

## Pregunta 6
Quin avantatge te rsync sobre copiar amb cp?

- [x] Nomes copia els fitxers nous o modificats (incremental)
- [ ] Es mes rapid sempre
- [ ] Comprimeix els fitxers
- [ ] Xifra la comunicacio

## Pregunta 7
Quin inconvenient te rsync respecte a Syncthing?

- [x] Es unidireccional (no sincronitza en dos sentits)
- [ ] Es mes lent
- [ ] No funciona a Linux
- [ ] No suporta SSH

## Pregunta 8
Quina opcio de rsync simula el que faria sense fer canvis?

- [ ] --dry
- [x] -n / --dry-run
- [ ] --simulate
- [ ] --test

## Pregunta 9 (oberta)
Has de sincronitzar 50 GB de fotos del teu mobil Android al servidor del BernatLab. Triaries Syncthing o rsync? Argumenta la decisio.

Pistes per respondre:
- Syncthing es continu (sense intervencio manual), pero gasta CPU/RAM al servidor.
- rsync es puntual pero nomes quan executes lordre.
- Quin volum es? 50 GB es molt o poc?
- Tens el mobil sempre a la xarxa local?

## Pregunta 10 (oberta)
Dissenya una estrategia de sincronitzacio per a un petit negoci amb 3 ordinadors i 1 NAS. Quina eina faries servir per a cada cas?

Pistes per respondre:
- Documents compartits: tothom hi accedeix.
- Backups: copies unidireccionals.
- Fotos de productes: pujada des dels movils.
- Quin rendiment esperes?
- Quin cost te?

## Pregunta 11 (oberta)
Per que creus que Syncthing ha esdevingut una alternativa popular a Dropbox i Google Drive per als usuaris mes tecnics? Quins avantatges te al BernatLab (100.115.134.76) i quins inconvenients?

Pistes per respondre:
- Privacitat: les dades no passen per tercers.
- Cost: gratis i sense limits.
- Auto-hostatjat: control total.
- Pero: cal configurar, mantenir i entendre.
- Trade-off: privacitat vs conveniencia.

## Pregunta 12 (oberta)
Quina relacio hi ha entre l'amplada de banda de la xarxa i la velocitat de sincronitzacio? Com afecta al BernatLab (100.115.134.76) si tens una conexio de 100 Mbps o de 10 Mbps? Calcula exemples.

Pistes per respondre:
- 1 GB a 100 Mbps = 80 segons.
- 1 GB a 10 Mbps = 13 minuts.
- 50 GB a 10 Mbps = 11 hores.
- Si la sincronitzacio nomes pot ser de nit, afecta?
- Trade-off: rapidesa vs cost de la connexio.

## Pregunta 13 (oberta)
Imagina que el teu company et diu: "el rsync es una eina antiga, jo uso Dropbox perque es mes modern". Argumenta per que al BernatLab rsync te sentit inclús avui, donant exemples de casos dus.

Pistes per respondre:
- rsync nomes depen de SSH.
- Sense limit despai (Dropbox limita).
- Sense cost mensual.
- Scripts automatitzables.
- Cas dus: backup de logs, sincronitzacio de carpetes de treball.

## Pregunta 14 (oberta)
Aplica el concepte de sincronitzacio al cas concret del BernatLab amb l'hort IoT. Tinc el servidor principal i un portatil que vull que tingui una copia sincronitzada de certes carpetes. Com ho configuraries amb Syncthing vs rsync+SSH? Quin esquema te sentit per a cada cas?

Pistes per respondre:
- Carpetes de treball: Syncthing (bidireccional).
- Backups del servidor al portatil: rsync (unidireccional).
- Fitxers de configuracio: rsync amb cron.
- Que passa si ambdos canvien el mateix fitxer alhora?

## Pregunta 15 (oberta)
Quines consequencies te per a la seguretat de les dades sincronitzar carpetes a multiples dispositius? Com ho gestionaries al BernatLab per minimitzar el risc que un dispositiu compromes afecti la resta?

Pistes per respondre:
- Un portatil amb virus pot propagar fitxers maliciosos al servidor.
- rsync te mes control: nomes sincronitzes el que vols.
- Syncthing es automatic: pot propagar brossa rapidament.
- Practica: Carpetes separees segons criticitat, autentificacio forta, xifratge.
- Trade-off: automatitzacio vs control.
