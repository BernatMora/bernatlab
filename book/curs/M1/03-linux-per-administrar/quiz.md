# Qüestionari — Capítol 3: Linux per administrar

> 10 preguntes · ~15 min

## Pregunta 1
Quina ordre et mostra el directori actual?

- [ ] where
- [x] pwd
- [ ] ls
- [ ] cd

## Pregunta 2
Quin és el permís numèric per a "tots els permisos per al propietari, lectura+execució per a grup i altres"?

- [ ] 644
- [ ] 700
- [x] 755
- [ ] 777

## Pregunta 3
Què fa `sudo`?

- [ ] Canvia la contrasenya de l'usuari
- [x] Executa una ordre amb permisos d'administrador (root)
- [ ] Tanca la sessió
- [ ] Actualitza el sistema

## Pregunta 4
Quina ordre instal·la un paquet a Debian?

- [ ] dnf install
- [x] sudo apt install
- [ ] pacman -S
- [ ] yum install

## Pregunta 5
Quin és el permís `-rwxr-xr-x` en format numèric?

- [ ] 644
- [x] 755
- [ ] 777
- [ ] 600

## Pregunta 6
Què fa `systemctl enable ssh`?

- [ ] Inicia el servei SSH ara
- [x] Fa que el servei SSH arrenqui automàticament en boot
- [ ] Reinstalla SSH
- [ ] Activa el tallafocs per a SSH

## Pregunta 7
Quina combinació de tecles guarda un fitxer a nano?

- [ ] Ctrl+S
- [ ] Ctrl+G
- [x] Ctrl+O
- [ ] Ctrl+W

## Pregunta 8
Quina ordre mostra els logs en temps real d'un servei amb systemd?

- [ ] tail -f /var/log/syslog
- [x] journalctl -u servei -f
- [ ] cat /var/log/servei.log
- [ ] systemctl logs servei

## Pregunta 9 (oberta)
Explica amb les teves paraules: quina diferència hi ha entre un usuari normal i root? Per què no hem de treballar sempre com a root?

Pistes per respondre:
- Què pot fer root que no pot un usuari normal?
- Què passa si executes `sudo rm -rf /` per error?
- Per a què serveix `sudo`?

## Pregunta 10 (oberta)
Imagina que un contenidor Docker ha caigut i no saps per què. Escriu els passos que faries per diagnosticar el problema al BernatLab (hostname `hortosona`).

Pistes per respondre:
- Com mires l'estat del servei?
- On són els logs?
- Quines ordres concretament faries servir?
