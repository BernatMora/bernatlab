# Qüestionari — Capítol 3: Linux per administrar

> 15 preguntes · ~20 min

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

## Pregunta 9
Quin directori conté la configuració de sistema a Debian?

- [ ] /home
- [x] /etc
- [ ] /var
- [ ] /opt

## Pregunta 10
Quina ordre mostra tots els processos del sistema ordenats per ús de memòria?

- [ ] ps
- [ ] top
- [x] ps aux --sort=-%mem
- [ ] mem

## Pregunta 11
Què vol dir el permís `drwx------` a un directori?

- [ ] Directori accessible per tothom
- [x] Directori on només el propietari pot entrar, llegir i escriure
- [ ] Directori sense permisos
- [ ] Enllaç simbòlic

## Pregunta 12
Quin avantatge té `systemctl restart servei` respecte `kill -9` el PID del procés?

- [ ] És més ràpid
- [x] Tanca el servei ordenadament i el torna a arrencar net
- [ ] No cal tenir permisos
- [ ] No cal saber el nom del servei

## Pregunta 13 (oberta)
Explica amb les teves paraules: quina diferència hi ha entre un usuari normal i root? Per què no hem de treballar sempre com a root?

Pistes per respondre:
- Què pot fer root que no pot un usuari normal?
- Què passa si executes `sudo rm -rf /` per error?
- Per a què serveix `sudo`?

## Pregunta 14 (oberta)
Imagina que un contenidor Docker ha caigut i no saps per què. Escriu els passos que faries per diagnosticar el problema al BernatLab (hostname `hortosona`).

Pistes per respondre:
- Com mires l'estat del servei?
- On són els logs?
- Quines ordres concretament faries servir?
- Com diferencies si és problema de Docker, de la imatge, o de l'aplicació?

## Pregunta 15 (oberta)
Al BernatLab tens l'usuari `bernat` amb permís `sudo` i treballes habitualment amb claus SSH. Un dia reb un correu d'alerta de seguretat que diu "s'ha detectat un intent d'accés root per SSH des d'una IP sospitosa". Escriu el pla d'acció immediat que duries a terme.

Pistes per respondre:
- Què mires primer (logs, configuració)?
- Què endureixes (ports, autenticació, tallafocs)?
- Com evitar que es repeteixi (monitoratge, alertes)?
- Quin paper juga Tailscale en tot plegat?
