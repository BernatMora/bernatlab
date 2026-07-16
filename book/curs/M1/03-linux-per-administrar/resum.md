# Resum — Capítol 3: Linux per administrar

## La idea clau

Un cop tens la Raspberry Pi en marxa amb Debian 13 Lite, toca aprendre a **parlar amb ella**. Això vol dir dominar un grapat d'eines de terminal: moure't per carpetes, crear i editar fitxers, gestionar usuaris i permisos, instal·lar programari, mirar logs i controlar serveis. Són les ordres bàsiques que faràs servir cada dia al BernatLab (hostname `hortosona`, IP Tailscale `100.115.134.76`).

Aquest capítol és la caixa d'eines. La resta del curs hi va construint a sobre.

## El sistema de fitxers

Tot a Linux és un fitxer: el disc, el ratolí, una connexió de xarxa, un procés. Per organitzar-los, hi ha una estructura d'arbre que comença a `/` (l'arrel, "root directory"):

```
/home/bernat/homelab/    <- el teu homelab (on viurà tot)
/etc/                     <- configuració del sistema
/var/log/                 <- logs (registres d'activitat)
/usr/bin/                 <- programes instal·lats
/proc/                    <- informació del sistema i processos
```

Les carpetes clau:

- **`/home/bernat/`** — la teva carpeta personal, equivalent a "El meu usuari" en Windows.
- **`/etc/`** — fitxers de configuració. No tocar si no saps què fas.
- **`/var/log/`** — registres del sistema. Aquí és on mires quan algo falla.
- **`/opt/`** — programes opcionals/manualment. Nosaltres hi posarem eines com Portainer.

## Navegació i gestió de fitxers

Les ordres que faràs servir 100 vegades al dia:

```bash
pwd                       # On soc? (print working directory)
ls -lah                   # Què hi ha aquí? (llista amb detalls)
cd /home/bernat/homelab   # Canvia de carpeta
mkdir docker              # Crea carpeta
touch notes.md            # Crea fitxer buit
cp fitxer.txt copia.txt   # Copia
mv fitxer.txt nou.txt     # Mou o reanomena
rm fitxer.txt             # Esborra (compte, no hi ha paperera!)
rm -rf carpeta/           # Esborra recursivament (molt perillós)
```

L'ordre `cd` sense arguments et porta a `/home/bernat/`. La combinació `cd ..` puja un nivell. `cd -` torna a la carpeta anterior.

## Usuaris, grups i permisos

Linux és multiusuari. Al BernatLab tens l'usuari `bernat` (el teu) i `root` (l'administrador total). Cada fitxer pertany a un usuari i un grup, i té tres permisos: **llegir (r)**, **escriure (w)** i **executar (x)**.

Mira els permisos:

```bash
ls -l /home/bernat/
# -rw-r--r-- 1 bernat bernat 1234 nov 12 10:30 notes.md
# drwxr-xr-x 2 bernat bernat 4096 nov 12 10:30 docker/
```

La cadena `-rw-r--r--` es llegeix així:

- `-` = fitxer normal (un directori seria `d`)
- `rw-` = propietari pot llegir i escriure
- `r--` = grup només pot llegir
- `r--` = altres només poden llegir

Canviar permisos:

```bash
chmod 755 script.sh       # rwxr-xr-x (propietari tot, altres llegir+executar)
chmod 644 fitxer.txt      # rw-r--r-- (estàndard per a fitxers)
chmod +x script.sh        # afegeix permís d'execució
```

Canviar propietari:

```bash
sudo chown bernat:bernat fitxer.txt   # usuari:grup
sudo chown -R bernat:bernat carpeta/  # recursivament
```

## sudo: fer coses d'administrador

Moltes ordres necessiten permisos de root. En lloc d'obrir una sessió root (perillós), uses `sudo` per elevar permisos puntualment:

```bash
sudo apt update                    # actualitza la llista de paquets
sudo systemctl restart ssh         # reinicia el servei SSH
sudo nano /etc/hosts                # edita un fitxer del sistema
```

La primera vegada que fas servir `sudo` en una sessió, et demana la contrasenya. Durant 15 minuts no te la torna a demanar. L'usuari `bernat` pot fer `sudo` perquè està al grup `sudo`.

**Compte**: un `sudo rm -rf /` esborraria TOT el sistema. Mai facis servir `sudo rm` sense pensar-ho dues vegades.

## Gestió de paquets amb apt

Debian/Ubuntu usa `apt` per instal·lar programari. Els paquets es descarreguen dels repositoris oficials:

```bash
sudo apt update              # descarrega la llista de paquets actualitzada
sudo apt upgrade             # instal·la les actualitzacions
sudo apt install htop        # instal·la un programa
sudo apt remove htop         # desinstal·la
apt search "monitor"         # busca paquets
apt show htop                # informació d'un paquet
```

Sempre fes `sudo apt update` abans d'instal·lar res, per assegurar que tens la llista més recent. I `sudo apt upgrade` un cop al mes (o quan hi ha CVEs crítiques) per mantenir el sistema segur.

## L'editor nano

Per editar fitxers de configuració, necessites un editor de terminal. `nano` és el més simple:

```bash
nano /etc/hosts       # obre l'editor
```

Dins de nano:

- `Ctrl+O` — guarda (WriteOut)
- `Ctrl+X` — surt
- `Ctrl+K` — talla una línia
- `Ctrl+W` — busca text
- `Ctrl+C` — cancel·la

A baix de tot veuràs els dreceres. Si t'agrada més complicat, hi ha `vim` i `emacs`, però nano és perfecte per començar i el faràs servir gairebé sempre al BernatLab.

## Serveis amb systemd

`systemd` és el mestre de cerimònies (recordes del cap 2?). Cada programa que corre al fons és un "servei" gestionat per systemd:

```bash
sudo systemctl status ssh        # estat d'un servei
sudo systemctl start ssh         # arrenca'l
sudo systemctl stop ssh          # para'l
sudo systemctl restart ssh       # reinicia'l
sudo systemctl enable ssh        # arrenca automàticament en boot
sudo systemctl disable ssh       # NO arrenqui en boot
systemctl list-units --type=service --state=running   # llista serveis actius
```

Quan un servei falla, mira el log amb `journalctl`:

```bash
sudo journalctl -u ssh --since today    # logs d'un servei des d'avui
sudo journalctl -u ssh -f               # segueix els logs en temps real (tail -f)
sudo journalctl -p err -b               # errors des de l'últim boot
```

## Logs bàsics

A banda de journalctl, els logs clàssics viuen a `/var/log/`:

```bash
tail -f /var/log/syslog         # log general del sistema
tail -f /var/log/auth.log       # autenticacions (SSH, sudo)
less /var/log/kern.log          # log del kernel
```

L'ordre `tail -f` mostra les últimes línies i segueix en temps real. Prement `Ctrl+C` surt. És la teva eina número u quan algo no funciona.

## Connexions amb altres capítols

- **Cap 2** — Tot això corre sobre la Raspberry Pi 4 amb Debian 13.
- **Cap 4** — L'accés remot per SSH substitueix el terminal directe.
- **Cap 5** — Docker és un servei systemd (`docker.service`).
- **Cap 6** — Portainer és un contenidor Docker que administra la resta.
- **Cap 9** — Versionarem els fitxers de configuració amb Git.
- **Cap 22** — Monitoratge avançat llegeix els mateixos logs.

Ara ja tens la caixa d'eines. Al capítol següent veuràs com accedir a tot això des de qualsevol lloc amb Tailscale i SSH.
