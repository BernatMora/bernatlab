# Capítol 59 — Primer contacte amb la Raspberry Pi

> *"Aquest és el moment de la veritat. Connectes la RPi, prem el botó, i tens un servidor. Si tot va bé, deu segons. Si no, mitja hora. Benvingut al món real."*

## 59.1 Què aprendràs

Al final d'aquest capítol tindràs:

- La Raspberry Pi amb la microSD flashejada i arrancada.
- Connexió a la teva xarxa local (via Ethernet).
- Accés per SSH des del teu ordinador.
- L'adreça IP de la Raspberry per connectar-hi.
- Les primeres comandes executades.

Aquest capítol és **pràctic al 100%**. Llegir-lo sense fer-ho no serveix de gaire. Té la RPi a mà quan comencis.

## 59.2 Durada estimada

- Amb experiència: 15-20 min.
- Primer cop: 45-60 min (comptant possibles contratemps).
- Si mai has flashejat una microSD: +30 min.

## 59.3 Material a mà

Assegura't que tens:

- La **Raspberry Pi 4** amb la carcassa posada.
- La **microSD** amb el seu adaptador USB.
- La **font d'alimentació oficial** USB-C.
- El **cable Ethernet** connectat a la RPi i al router.
- Un **ordinador** amb el qual accedir per SSH.
- Un **monitor amb HDMI** i teclat USB (opcional, per si fallen coses).

## 59.4 Pas 1: descarregar i instal·lar Raspberry Pi Imager

Al teu **ordinador** (no a la RPi encara), descarrega **Raspberry Pi Imager** des de:

- https://www.raspberrypi.com/software/

Està disponible per a Windows, Mac i Linux. Instal·la'l com qualsevol programa.

## 59.5 Pas 2: triar el sistema operatiu

Obre Raspberry Pi Imager. A la primera pantalla veuràs tres menús:

1. **Dispositiu**: tria "Raspberry Pi 4".
2. **Sistema operatiu**: tria "Raspberry Pi OS (other)" → "Raspberry Pi OS Lite (64-bit)".
3. **Emmagatzematge**: tria la teva microSD.

Per què **Lite** i no l'escriptori complet?

- **Lite** no té entorn gràfic, és només terminal. Ocupa menys espai i menys RAM.
- Per a un servidor 24/7, l'escriptori és innecessari.
- Si vols, sempre pots afegir-lo més tard.

## 59.6 Pas 3: configuració personalitzada

Abans de flashejar, Imager et permet configurar quatre coses útils. **Això t'estalviarà 30 minuts** després.

Fes clic a **"Edita la configuració"** (o "Edit Settings" en anglès). S'obrirà una finestra amb quatre pestanyes:

### Pestanya "General"

- **Hostname**: escriu `hortosona` (o el nom que hagis triat). Això serà el nom de la RPi a la xarxa.
- **Nom d'usuari**: jo faig servir `bernat`, tu pots fer servir el que vulguis. Però **no facis servir `pi`**: és el nom per defecte i tots els bots d'Internet el coneixen.
- **Contrasenya**: una de forta, com les del **Cap 46** (2FA i secrets). Mínim 16 caràcters. Guarda-la al teu gestor de contrasenyes.
- **Wi-Fi**: deixa-ho buit. Farem servir Ethernet.
- **Zona horària**: posa-hi la teva (per a Catalunya, `Europe/Madrid` serveix).
- **Layout del teclat**: si el teu és espanyol, tria `es`.

### Pestanya "Serveis"

- Activa **"Enable SSH"**.
- Triar **"Use password authentication"** és acceptable per començar. Més endavant (al capítol 60) canviarem a clau pública.
- Si vols, pots activar "Serial console" per si mai necessites accedir via UART.

### Pestanya "Opcions"

- Pots deixar-ho tot per defecte.

Fes clic a **"Desar"** i després a **"Escriure"** (o "Write").

## 59.7 Pas 4: flashejar la microSD

Imager començarà a escriure. Això triga entre 1 i 5 minuts, depenent de la microSD. **Paciència**: no treguis la targeta a mitja escriptura.

Quan acabi, Imager et preguntarà si vols extreure la targeta. Diu-li que sí, treu-la, i fica-la a la RPi.

## 59.8 Pas 5: primer arrencada de la Raspberry

Amb la microSD ja inserida:

1. Connecta el **cable Ethernet** de la RPi al router.
2. Connecta la **font d'almentació** USB-C.
3. La RPi arrencarà automàticament. No té botó d'encesa (o si en té, no cal prémer-lo).

Esperem que arrenqui. La **LED vermella** ha de quedar fixa, i la **LED verda** ha de parpellejar durant 10-30 segons mentre llegeix la microSD.

Quan la verda deixi de parpellejar, el sistema ha acabat d'arrencar.

## 59.9 Pas 6: trobar l'adreça IP

Ara ve la part interessant: descobrir quina IP ha agafat la RPi al router. Hi ha diverses maneres:

### Opció A: mirar al router

La majoria de routers tenen una pàgina d'administració on pots veure els dispositius connectats. Normalment és `http://192.168.1.1` o `http://192.168.0.1`. Busca a la llista un dispositiu amb nom `hortosona` i apunta la seva IP.

### Opció B: fer ping al hostname

Des del teu ordinador:

```bash
ping hortosona
```

Si funciona, ja tens la IP. Si no, el teu ordinador no resol noms per mDNS (cosa que passa al Windows).

### Opció C: eines específiques

- **Windows**: pots instal·lar **Advanced IP Scanner** (gratuït) o fer servir `arp -a` per veure dispositius de la xarxa.
- **Mac/Linux**: `arp -a` o `nmap -sn 192.168.1.0/24` (si tens `nmap` instal·lat).
- **Apps mòbils**: **Fing** (iOS/Android) és excel·lent per trobar dispositius a la xarxa.

### Opció D: provar IPs comuns

Si tens un router amb DHCP normal, la RPi estarà a alguna IP com `192.168.1.42` o `192.168.0.42`. Prova unes quantes.

Jo normalment uso la opció A (mirar al router) perquè és la més fiable.

## 59.10 Pas 7: accedir per SSH

Un cop tens la IP, obre un terminal al teu ordinador:

**Windows** (PowerShell o CMD):

```powershell
ssh bernat@hortosona
```

Si tens Windows 10/11 modern, `ssh` ja està disponible. Si no, instal·la OpenSSH o usa PuTTY.

**Mac/Linux**:

```bash
ssh bernat@hortosona
```

La primera vegada, SSH et preguntarà si confies en aquest host. Escriu `yes`.

Després et demanarà la contrasenya (la que vas posar a la Imager). Escriu-la (no es veurà mentre l'escrius, és normal).

Si tot va bé, veuràs alguna cosa com:

```
Linux hortosona 6.6.51+rpt-rpi-v8 #1 SMP PREEMPT Debian 1:6.6.51-1+rpt3 (2024-10-08) aarch64

The programs included with the Debian GNU/Linux system are free software;
...

bernat@hortosona:~ $
```

**Felicitats! Acabes d'entrar al teu primer servidor.**

## 59.11 Pas 8: les primeres comandes

Un cop dins, executa aquestes comandes per entendre on ets:

```bash
# Qui sóc jo
whoami

# On sóc
pwd

# Quina distro tinc
cat /etc/os-release

# Quin hardware tinc
uname -a
lscpu
free -h
df -h
```

Hauries de veure:

- `whoami` retorna `bernat` (o el teu nom d'usuari).
- `pwd` retorna `/home/bernat`.
- La distro és **Debian GNU/Linux 13 (trixie)**.
- L'arquitectura és **aarch64** (ARM 64 bits).
- La CPU és una **ARM Cortex-A72** amb 4 nuclis.
- La RAM és la que hagis comprat (4 GB o 8 GB).
- L'espai lliure a la microSD.

## 59.12 Pas 9: configurar la xarxa correctament

Si la IP t'ha canviat a cada reinici, és perquè el DHCP del router t'està donant IPs dinàmiques. Per evitar-ho, podem fer dues coses:

### Opció A: IP estàtica al router

Mira al router quin rang de DHCP té, i assigna una IP fixa a la MAC de la RPi. Cada router és diferent, però busca "DHCP reservation" o "IP estática" al menú.

Això és el que jo faig: la RPi sempre té la mateixa IP (excepte amb Tailscale, on té una IP del tailnet).

### Opció B: IP estàtica a la RPi

Edita la configuració de xarxa:

```bash
sudo nano /etc/dhcpcd.conf
```

Afegeix al final:

```
interface eth0
static ip_address=192.168.1.100/24
static routers=192.168.1.1
static domain_name_servers=192.168.1.1 1.1.1.1
```

(Canvia les IPs per les de la teva xarxa.)

Guarda amb `Ctrl+O`, surt amb `Ctrl+X`, i reinicia:

```bash
sudo systemctl restart dhcpcd
```

### Per què és important tenir una IP fixa

Sense IP fixa, cada vegada que la RPi es reiniciï, el router li pot donar una IP diferent. Això és molt molest per:

- Scripts d'automatització.
- Configurar altres dispositius per apuntar a aquesta IP.
- Recordar on és el servidor.

Tailscale ho soluciona (et dona una IP fixa del tailnet), però tenir la IP local fixa també ajuda.

## 59.13 Pas 10: primeres actualitzacions

Un cop tens accés, actualitza el sistema:

```bash
sudo apt update
sudo apt upgrade -y
```

Això pot trigar una estona. Quan acabi, reinicia:

```bash
sudo reboot
```

Després d'un parell de minuts, torna a entrar per SSH:

```bash
ssh bernat@hortosona
```

## 59.14 Pas 11: fer la primera còpia de seguretat de la microSD

Ara que el sistema està net i actualitzat, **abans de fer res més**, fes una còpia de la microSD. Si la RPi falla demà, podràs restaurar en 5 minuts.

Apaga la RPi:

```bash
sudo shutdown -h now
```

Després d'un minut, la LED verda parpalleja 10 vegades i s'apaga. Treu la microSD.

Al teu ordinador, amb un lector de microSD:

**Windows**: pots usar **Win32 Disk Imager** o **balenaEtcher** (sí, el mateix que per flashejar).

**Mac**:

```bash
diskutil list
# Troba la microSD (ex: /dev/disk2)
diskutil unmountDisk /dev/disk2
sudo dd if=/dev/rdisk2 of=~/backup-raspberry-2026-07-09.img bs=4m status=progress
```

**Linux**:

```bash
lsblk
# Troba la microSD (ex: /dev/sdb)
sudo dd if=/dev/sdb of=~/backup-raspberry-2026-07-09.img bs=4M status=progress
```

Comprimeix la imatge:

```bash
gzip ~/backup-raspberry-2026-07-09.img
```

Guarda aquest fitxer en un lloc segur. Si tens una còpia al núvol (Backblaze B2, per exemple), millor.

## 59.15 Què has après

Ara ja tens:

- Una Raspberry Pi amb sistema operatiu.
- Connexió SSH des del teu ordinador.
- Una adreça IP fixa a la xarxa.
- El sistema actualitzat.
- Una còpia de seguretat de la microSD.

Al **Cap 60** farem el següent:

- Canviar la contrasenya per una clau SSH.
- Instal·lar Tailscale per accedir des de qualsevol lloc.
- Configurar l'usuari correctament.
- Aplicar les primeres mesures de seguretat.

## 59.16 Errors habituals

**Error 1: la LED vermella parpelleja**.

Vol dir que la font d'alimentació no és prou potent. Canvia-la per l'oficial.

**Error 2: la LED verda no parpelleja mai**.

La microSD no està ben flashejada, o no està ben insertada. Torna a flashejar.

**Error 3: "Permission denied" en fer SSH**.

Contrasenya incorrecta, o usuari mal escrit. Recorda que Linux distingeix majúscules.

**Error 4: "Connection refused"**.

La RPi no està en marxa, o SSH no està activat. Connecta un monitor per veure què passa.

**Error 5: "Host key verification failed"**.

Estàs intentant accedir a una RPi que ja tens enregistrada amb una clau diferent. Solució: `ssh-keygen -R hortosona` al teu ordinador.

**Error 6: el router no mostra la RPi**.

Comprova que el cable Ethernet està ben connectat a les dues bandes. Mira si el LED de xarxa de la RPi s'il·lumina (verd o groc al port Ethernet).

**Error 7: l'IP canvia a cada reinici**.

Configura una IP estàtica, com hem explicat al pas 12.

## 59.17 Resum

Aquest capítol és el moment de la veritat: la RPi en marxa, accessible per SSH, amb una còpia de seguretat. Hem vist:

- Com flashejar la microSD amb Raspberry Pi Imager.
- Com triar el sistema operatiu correcte (Lite, 64-bit).
- Com configurar coses abans de flashejar (estalvia temps).
- Com trobar la IP de la RPi.
- Com accedir per SSH.
- Com actualitzar el sistema.
- Com fer la primera còpia de seguretat.

Al **Cap 60** endurem la seguretat: clau SSH, Tailscale, i primers ajustos.

## 59.18 Exercicis pràctics

1. Descarrega Raspberry Pi Imager.
2. Flasheja la microSD amb Raspberry Pi OS Lite 64-bit.
3. Configura el hostname, usuari i contrasenya a Imager.
4. Activa SSH amb autenticació per contrasenya.
5. Insereix la microSD a la RPi i engega-la.
6. Troba la IP de la RPi.
7. Accedeix per SSH.
8. Executa les comandes del pas 11 per entendre el sistema.
9. Configura una IP estàtica.
10. Actualitza el sistema.
11. Fes una còpia de seguretat de la microSD.
12. Documenta-ho tot al `homelab/setup-log.md`.
