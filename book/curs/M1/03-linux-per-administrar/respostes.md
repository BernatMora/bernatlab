# Respostes — Capítol 3: Linux per administrar

> Mira les respostes DESPRÉS d'haver fet el qüestionari.

## Pregunta 1: Ordre per mostrar el directori actual

**Resposta correcta**: pwd

**Explicació**: `pwd` ve de "Print Working Directory". Mostra la ruta absoluta del directori on ets. És útil per orientar-te quan naveges amb `cd` per carpetes profundes.

## Pregunta 2: Permís 755

**Resposta correcta**: 755

**Explicació**: 755 = `rwx` (7) per al propietari + `r-x` (5) per al grup + `r-x` (5) per a altres. És l'estàndard per a scripts i directoris que vols que tothom pugui executar/llistar però només tu puguis modificar.

## Pregunta 3: Què fa sudo?

**Resposta correcta**: Executa una ordre amb permisos d'administrador (root).

**Explicació**: `sudo` ve de "substitute user do". Et permet elevar permisos temporalment (15 min) sense haver d'iniciar sessió com a root. És més segur perquè deixa rastre a `/var/log/auth.log` i pots fer una sola ordre destructiva en lloc de quedar-te en una sessió root.

## Pregunta 4: Instal·lar paquet a Debian

**Resposta correcta**: sudo apt install

**Explicació**: `apt` és el gestor de paquets de Debian/Ubuntu. Altres distribucions: `dnf` (Fedora/RHEL), `pacman` (Arch), `yum` (RHEL antic).

## Pregunta 5: -rwxr-xr-x en numèric

**Resposta correcta**: 755

**Explicació**: rwx = 4+2+1 = 7. r-x = 4+0+1 = 5. r-x = 5. Per tant 755.

## Pregunta 6: systemctl enable

**Resposta correcta**: Fa que el servei SSH arrenqui automàticament en boot.

**Explicació**: `enable` crea un enllaç simbòlic a la carpeta de serveis que systemd arrencarà. `start` només l'inicia ara, però no garanteix que torni a arrencar si reinicies.

## Pregunta 7: Guardar a nano

**Resposta correcta**: Ctrl+O

**Explicació**: `Ctrl+O` (WriteOut) guarda el fitxer. `Ctrl+X` surt (i et preguntarà si vols guardar si hi ha canvis). `Ctrl+W` busca, `Ctrl+C` cancel·la.

## Pregunta 8: Logs en temps real amb systemd

**Resposta correcta**: journalctl -u servei -f

**Explicació**: `-u` filtra per unitat (servei), `-f` fa "follow" (segueix noves línies com `tail -f`). És l'equivalent modern de `tail -f /var/log/servei.log`.

## Pregunta 9 (oberta): Diferència entre usuari i root

**Resposta model**:

L'usuari **root** (també anomenat superusuari o administrador) té UID 0, que vol dir que pot fer LITERALMENT qualsevol cosa al sistema: instal·lar programari, modificar qualsevol fitxer (inclosos els del sistema), crear o esborrar usuaris, accedir a qualsevol procés, etc. Un **usuari normal** té un UID ≥ 1000 i només pot modificar els seus propis fitxers, la seva home, i executar les ordres per a les quals tingui permís.

Treballar sempre com a root és perillós perquè:
- **Un error tipogràfic destrossa el sistema sencer**: `sudo rm -rf /` esborra tot. Com a usuari normal, només esborraries la teva home.
- **Un programa maliciós s'executa amb poder total**: si com a root executes un script contaminat, pot fer el que vulgui.
- **No deixa rastre clar de qui ha fet què**: tots els comandos apareixen com a "root" als logs.

`sudo` és la solució: eleveus permisos NOMÉS per a l'ordre concreta que necessites, durant 15 minuts. Si t'equivoques, l'error queda localitzat. A més, queda registrat a `/var/log/auth.log` amb el teu nom d'usuari.

## Pregunta 10 (oberta): Diagnosticar un contenidor caigut

**Resposta model**:

Quan un contenidor Docker cau al BernatLab, els passos serien:

1. **Connectar-se per SSH**: `ssh bernat@hortosona` (o directament per IP Tailscale `ssh bernat@100.115.134.76`).

2. **Veure l'estat del servei Docker**:
   ```bash
   sudo systemctl status docker
   ```
   Si el servei Docker està down, cal arrencar-lo amb `sudo systemctl start docker`.

3. **Llistar els contenidors i el seu estat**:
   ```bash
   docker ps -a
   ```
   El flag `-a` mostra també els aturats. Buscar el contenidor problemàtic (columna STATUS: "Exited (1) 5 minutes ago" o similar).

4. **Veure els logs del contenidor concret**:
   ```bash
   docker logs <nom_contenidor>
   docker logs --tail 100 <nom_contenidor>   # últimes 100 línies
   docker logs -f <nom_contenidor>           # en temps real
   ```
   Sovint aquí veuràs la causa: "port already in use", "permission denied", "image not found"...

5. **Si cal, mirar logs de systemd**:
   ```bash
   sudo journalctl -u docker --since "1 hour ago"
   ```

6. **Reiniciar el contenidor** (un cop identificat el problema):
   ```bash
   docker restart <nom_contenidor>
   # o via Portainer (que veurem al cap 6)
   ```

7. **Si segueix fallant, recrear-lo**:
   ```bash
   docker compose -f /home/bernat/homelab/docker/docker-compose.yml up -d <servei>
   ```

8. **Documentar l'incident** a `homelab/notes/incidencies.md` per no repetir-lo.

## Què fer si has fallat moltes preguntes

- **5-8 encerts**: Rellegir el resum, sobretot la part de permisos.
- **3-4 encerts**: Practica les ordres directament a la RPi, una a una.
- **0-2 encerts**: Repassem junts el capítol abans de continuar.

## Què fer si has encertat totes

- Passa al **Capítol 4** (Xarxa, SSH i Tailscale).
- O fes l'**exercici pràctic** per consolidar.
