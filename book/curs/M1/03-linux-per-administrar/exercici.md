# Exercici pràctic — Capítol 3: Linux per administrar

> 30-45 min · Real al teu sistema

## Objectiu
Practicar les ordres bàsiques de Linux al BernatLab. Aprendreàs a navegar, crear fitxers, gestionar permisos, instal·lar programari i mirar logs.

## Requisits
- Tailscale actiu
- Connexió SSH a la RPi (`ssh bernat@hortosona`)
- 30-45 minuts

## Pas 1: Navega i crea estructura (10 min)

Crea l'estructura bàsica del teu homelab:

```bash
# Assegura't que ets a la teva home
cd ~

# Crea l'estructura
mkdir -p homelab/{docker,config,notes,scripts,logs}

# Mira què has creat
ls -la homelab/
tree homelab/ 2>/dev/null || find homelab/ -type d

# Entra i crea un fitxer de prova
cd homelab
echo "# El meu homelab" > README.md
cat README.md
```

## Pas 2: Permisos (10 min)

Practica amb els permisos:

```bash
# Crea un script de prova
cd ~/homelab/scripts
nano hola.sh
# Escriu:
#!/bin/bash
echo "Hola des del BernatLab!"
# Guarda amb Ctrl+O, surt amb Ctrl+X

# Mira els permisos (no te execucio)
ls -l hola.sh
# Hauria de ser: -rw-r--r--

# Fes-lo executable
chmod +x hola.sh
ls -l hola.sh
# Ara: -rwxr-xr-x

# Executa'l
./hola.sh

# Crea un fitxer privat (només tu)
touch secret.txt
chmod 600 secret.txt
ls -l secret.txt
# -rw------- (només tu pots llegir/escriure)
```

## Pas 3: Instal·la una eina amb apt (10 min)

```bash
# Actualitza la llista
sudo apt update

# Instal·la eines utils
sudo apt install -y htop tree ncdu

# Comprova que s'han instal·lat
htop --version
tree --version
ncdu --version

# Prova-les
htop    # Gestor de processos visual. prem F10 o q per sortir.
tree ~/homelab -L 2
ncdu ~/homelab   # Analitzador de disc. prem q per sortir.
```

## Pas 4: Gestió de serveis (10 min)

Mira l'estat dels serveis principals:

```bash
# Llista serveis actius
systemctl list-units --type=service --state=running | head -20

# Estat detallat de SSH
sudo systemctl status ssh

# Mira els últims logs de SSH
sudo journalctl -u ssh --since "1 hour ago" | tail -20

# Segueix els logs en temps real durant 30 segons
# (obre una altra connexió SSH i fes ssh localhost per generar activitat)
sudo journalctl -u ssh -f
# prem Ctrl+C per sortir
```

## Pas 5: Documenta

Crea `book/curs/M1/03-linux-per-administrar/diari.md` amb:

- Les 5 ordres que més has fet servir
- Captures de sortida de `htop`, `tree`, `systemctl status ssh`
- Un parell de notes personals sobre què t'ha sorprès

## Validació

Has acabat si:
- [ ] Has creat l'estructura `homelab/{docker,config,notes,scripts,logs}`.
- [ ] Has fet executable un script amb `chmod +x` i l'has executat.
- [ ] Has canviat permisos a `600` i has comprovat la diferència.
- [ ] Has instal·lat `htop`, `tree` i `ncdu` amb apt.
- [ ] Has vist l'estat del servei SSH i els seus logs.
- [ ] Has documentat l'experiència a `diari.md`.

## Per aprofundir

- Llegeix `man ls`, `man chmod`, `man systemctl` (prement `q` surts).
- Practica pipes: `ps aux | grep docker | head -5`.
- Crea un àlies a `~/.bashrc`: `alias ll='ls -lah'`.
