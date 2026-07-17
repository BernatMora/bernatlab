# Exercici pràctic — Capítol 3: Linux per administrar

> 45-60 min · Real al teu sistema

## Objectiu

Practicar les ordres bàsiques de Linux al BernatLab. Aprendràs a navegar, crear fitxers, gestionar permisos, instal·lar programari, mirar logs, i fer coses una mica més avançades com pipes i scripting bàsic.

## Requisits
- Tailscale actiu
- Connexió SSH a la RPi (`ssh bernat@hortosona`)
- 45-60 minuts

## Pas 1: Navega i crea estructura (10 min)

Crea l'estructura bàsica del teu homelab:

```bash
# Assegura't que ets a la teva home
cd ~

# Crea l'estructura
mkdir -p homelab/{docker,config,notes,scripts,logs,backups}

# Mira què has creat
ls -la homelab/
tree homelab/ 2>/dev/null || find homelab/ -type d

# Entra i crea un fitxer de prova
cd homelab
echo "# El meu homelab" > README.md
cat README.md

# Practica rutes relatives i absolutes
cd ..
pwd
cd /home/bernat/homelab
pwd
```

## Pas 2: Permisos (10 min)

Practica amb els permisos:

```bash
# Crea un script de prova
cd ~/homelab/scripts
nano hola.sh
# Escriu:
#!/bin/bash
echo "Hola des del BernatLab! Avui es $(date)"
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

# Crea un directori compartible amb el grup
mkdir ~/homelab/compartit
chmod 770 ~/homelab/compartit
ls -ld ~/homelab/compartit
```

## Pas 3: Instal·la una eina amb apt (10 min)

```bash
# Actualitza la llista
sudo apt update

# Instal·la eines utils
sudo apt install -y htop tree ncdu sysstat curl jq

# Comprova que s'han instal·lat
htop --version
tree --version
ncdu --version

# Prova-les
htop    # Gestor de processos visual. prem F10 o q per sortir.
tree ~/homelab -L 2
ncdu ~/homelab   # Analitzador de disc. prem q per sortir.

# sysstat: estadistiques de sistema
iostat
sar -u 1 5
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

# Comprovar fallades en l'arrancada
sudo systemctl --failed

# Temps de boot (quina rapidesa arrenca la RPi)
systemd-analyze

# Qui consumeix mes temps a l'arrancada?
systemd-analyze blame | head -10
```

Segueix els logs en temps real durant 30 segons:

```bash
# (obre una altra connexió SSH i fes ssh localhost per generar activitat)
sudo journalctl -u ssh -f
# prem Ctrl+C per sortir
```

## Pas 5: Pipes i redireccions (10 min)

Practica la "filosofia Unix" de combinar ordres petites:

```bash
# Quants processos tens?
ps aux | wc -l

# Els 5 processos que mes memoria gasten
ps aux --sort=-%mem | head -6

# Quants fitxers hi ha a homelab?
find ~/homelab -type f | wc -l

# Quants fitxers .md tens?
find ~/homelab -name "*.md" | wc -l

# Qui te la sessio SSH oberta?
who

# Ultims 5 logins
last -5

# Cerca una paraula als logs de sistema
sudo journalctl --since "today" | grep -i error | head -10

# Compta quantes vegades apareix "Failed password" als logs
sudo journalctl -u ssh | grep -c "Failed"
```

## Pas 6: Crea un script útil (10 min)

Crea un script que et doni un resum del sistema:

```bash
nano ~/homelab/scripts/resum.sh
```

Contingut:

```bash
#!/bin/bash
echo "=== BernatLab Resum ==="
echo "Data: $(date)"
echo "Hostname: $(hostname)"
echo "IP Tailscale: $(tailscale ip -4 2>/dev/null || echo 'Tailscale no actiu')"
echo "Uptime: $(uptime -p)"
echo "Temperatura: $(vcgencmd measure_temp 2>/dev/null)"
echo "Disc usat: $(df -h / | tail -1 | awk '{print $5}')"
echo "RAM usada: $(free | grep Mem | awk '{print int($3/$2 * 100)}')%"
echo "Contenidors actius: $(docker ps -q 2>/dev/null | wc -l)"
```

```bash
chmod +x ~/homelab/scripts/resum.sh
~/homelab/scripts/resum.sh
```

## Pas 7: Documenta

Crea `book/curs/M1/03-linux-per-administrar/diari.md` amb:
- Les 5 ordres que més has fet servir
- Captures de sortida de `htop`, `tree`, `systemctl status ssh`, `iostat`
- El teu script `resum.sh` final
- Un parell de notes personals sobre què t'ha sorprès
- Quin ha estat el moment "aha!" del dia

## Validació

Has acabat si:
- [ ] Has creat l'estructura `homelab/{docker,config,notes,scripts,logs,backups}`.
- [ ] Has fet executable un script amb `chmod +x` i l'has executat.
- [ ] Has canviat permisos a `600` i has comprovat la diferència.
- [ ] Has instal·lat `htop`, `tree`, `ncdu`, `sysstat` amb apt.
- [ ] Has vist l'estat del servei SSH i els seus logs.
- [ ] Has fet pipes amb `ps aux | grep | head`.
- [ ] Has creat el script `resum.sh` i funciona.
- [ ] Has documentat l'experiència a `diari.md`.

## Per aprofundir

- Llegeix `man ls`, `man chmod`, `man systemctl` (prement `q` surts).
- Practica pipes: `ps aux | grep docker | head -5`.
- Crea un àlies a `~/.bashrc`: `alias ll='ls -lah'`.
- Investiga la diferència entre `grep`, `egrep`, `fgrep`.
- Prova `find ~/homelab -name "*.md" -exec wc -l {} \;` per comptar línies a tots els .md.
- Experimenta amb `xargs`: `find ~/homelab -name "*.md" | xargs grep -l "bernat"`.

## Ves un pas més enllà

**Repte avançat: sistema d'alertes bàsic**.

Fes que el teu `resum.sh` t'avisi al Telegram si alguna cosa va malament. Requisits:

1. Crea una variable d'entorn amb el teu `chat_id` de Telegram:
   ```bash
   echo 'export TELEGRAM_CHAT_ID="EL_TEU_CHAT_ID"' >> ~/.bashrc
   source ~/.bashrc
   ```

2. Afegeix al final del `resum.sh`:
   ```bash
   # Alerta si la temperatura passa de 75 graus
   TEMP=$(vcgencmd measure_temp | grep -oP '\d+\.\d+')
   if (( $(echo "$TEMP > 75" | bc -l) )); then
       MSG="ALERTA: CPU del BernatLab a ${TEMP} graus!"
       curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_TOKEN}/sendMessage" \
            -d chat_id="$TELEGRAM_CHAT_ID" \
            -d text="$MSG" > /dev/null
   fi
   ```

3. Programa el script perquè corri cada 5 minuts amb cron:
   ```bash
   crontab -e
   # Afegeix:
   */5 * * * * /home/bernat/homelab/scripts/resum.sh >> /home/bernat/homelab/logs/resum.log 2>&1
   ```

4. Comprova que el fitxer `logs/resum.log` es va omplint.

Si la temperatura de la teva RPi puja de 75°C rebràs una alerta al mòbil. Això és un sistema de monitoratge molt bàsic — Uptime Kuma (cap. 7) en serà un de professional.
