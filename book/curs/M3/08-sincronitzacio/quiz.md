# Qüestionari — Capitol 8: Sincronitzacio de fitxers

> 10 preguntes · ~15 min

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
Que vol dir l'opcio `-a` de rsync?

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
- rsync es puntual pero nomes quan executes l'ordre.
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
