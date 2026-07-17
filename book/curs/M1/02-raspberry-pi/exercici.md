# Exercici pràctic — Capítol 2: La Raspberry Pi 4 per dins

> 30-40 min · Real al teu sistema

## Objectiu

Recollir informació detallada del **hardware** de la teva Raspberry Pi. Això et servirà per saber què tens, què pots afegir, on tens els límits, i com planificar les ampliacions del BernatLab.

## Requisits

- Tailscale actiu
- Connexió SSH a la RPi
- 30-40 minuts

## Pas 1: Identifica el hardware (5 min)

Connecta't per SSH i executa:

```bash
# Model de la RPi
cat /sys/firmware/devicetree/base/model
# Hauria de dir: Raspberry Pi 4 Model B Rev 1.4

# Versio del firmware
vcgencmd version 2>/dev/null || echo "vcgencmd no disponible"

# Numero de serie (unic per placa)
cat /proc/cpuinfo | grep Serial

# Data de fabricacio del firmware (estimada)
cat /proc/cpuinfo | grep Revision
```

## Pas 2: CPU i nuclis (5 min)

```bash
# Informacio de la CPU
lscpu | head -20

# Numero de nuclis actius
nproc

# Freq actual
cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq 2>/dev/null
# Retorna freq en kHz, dividint per 1000 dona MHz

# Freq maxima
cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_max_freq

# Governor actual (ondemand, performance, powersave...)
cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor
```

## Pas 3: Memòria i swap (5 min)

```bash
# Memoria RAM total i usada
free -h

# Detall de la swap
swapon --show

# Memoria compartida amb GPU
vcgencmd get_mem gpu 2>/dev/null || echo "vcgencmd no disponible"

# Memoria total fisica
dmidecode -t memory 2>/dev/null | head -10 || cat /proc/meminfo | head -5
```

## Pas 4: Emmagatzematge (5 min)

```bash
# Espai de disc
df -h

# Detall del sistema de fitxers
mount | grep "on / "

# Grandaria de la microSD (estimada)
lsblk

# UUIDs i tipus de cada particio
blkid

# Test de velocitat de la SD (opcional, ~1 min)
sudo hdparm -Tt /dev/mmcblk0
```

## Pas 5: Temperatura (5 min)

```bash
# Temperatura actual
vcgencmd measure_temp 2>/dev/null || \
  cat /sys/class/thermal/thermal_zone0/temp | awk '{print $1/1000 "C"}'

# Si tens sensors, lmesenta:
sensors 2>/dev/null || echo "Paquet lm-sensors no instal·lat"

# Freq de la CPU a la temperatura actual (throttling?)
vcgencmd measure_clock arm
```

Si tens un monitor connectat, observa que la RPi pot escalfar-se bastant. Si vols refrigerar-la:
- Posa-li un dissipador d'alumini (5-10 €).
- Assegura't que té ventilació al voltant.

## Pas 6: Xarxa (5 min)

```bash
# Interficies de xarxa
ip addr show

# Velocitat de la connexio Ethernet
sudo ethtool eth0 | grep Speed

# Wi-Fi (si l'uses)
iwconfig wlan0 2>/dev/null

# IP Tailscale
tailscale ip -4 2>/dev/null

# DNS resol per MagicDNS
getent hosts hortosona
```

## Pas 7: Test d'estrès controlat (5 min)

Aquest pas és opcional però molt recomanable. Veuràs fins a on pot arribar la teva RPi.

```bash
# Instal·la stress
sudo apt install -y stress

# Estresa la CPU durant 60 segons amb 4 workers
stress --cpu 4 --timeout 60

# En una altra finestra, mira la temperatura en directe
watch -n 1 vcgencmd measure_temp

# Mira si hi ha throttling
vcgencmd get_throttled
# Retorna un codi hexadecimal. Si throttled=0, tot OK.
# Altres valors comuns:
# 0x50000 = actualment throttled per temperatura
# 0x50005 = throttled per temperatura + subtensio
```

Apunta la temperatura màxima que vegis. Si supera els 80°C, cal refrigeració.

## Pas 8: Documenta-ho

Crea `book/curs/M1/02-raspberry-pi/inventari-hardware.md` amb tota la informació recollida. Inclou:

- Model exacte i número de sèrie
- RAM, freq, temperatura màxima sota càrrega
- Resultat de `vcgencmd get_throttled` (hauria de ser 0x0)
- Velocitat de la microSD (de hdparm)
- IP Tailscale i hostname

## Validació

Has acabat si:
- [ ] Saps quin model exacte de RPi tens.
- [ ] Coneixes la freq de la CPU.
- [ ] Has vist la RAM total i l'ús actual.
- [ ] Has mesurat la temperatura en repòs i sota càrrega.
- [ ] Has comprovat si hi ha throttling amb `get_throttled`.
- [ ] Has documentat la informació a `inventari-hardware.md`.

## Per aprofundir

- Compara el rendiment amb un disc SSD USB 3.0.
- Investiga si el teu model admesa PoE (Power over Ethernet) via HAT.
- Prova de connectar un disc NVMe via USB 3.0 i compara velocitats.
- Mira el voltatge actual: `vcgencmd measure_volts`.

## Ves un pas més enllà

**Repte avançat: baseline de referència**.

Per poder comparar el rendiment de la teva RPi amb el pas del temps, crea un "baseline" que puguis repetir. Executa aquesta seqüència i desa la sortida a `inventari-hardware.md` amb data:

```bash
echo "=== BASELINE $(date) ==="
echo "CPU freq: $(cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq)"
echo "Temperatura: $(vcgencmd measure_temp)"
echo "Throttled: $(vcgencmd get_throttled)"
echo "RAM lliure: $(free -h | grep Mem | awk '{print $4}')"
echo "Disc usat: $(df -h / | tail -1 | awk '{print $5}')"
echo "Uptime: $(uptime -p)"
echo "Contenidors actius: $(docker ps -q | wc -l)"
```

Repeteix aquest baseline un cop per setmana. Si la temperatura puja gradualment, pot ser brutícia o pasta tèrmica seca. Si l'ús de disc puja, tens logs o volums que creixen sense control.

Desa el primer baseline amb la data d'avui. Compromet-te a repetir-lo cada dilluns.
