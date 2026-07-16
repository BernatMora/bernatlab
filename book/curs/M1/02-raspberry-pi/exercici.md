# Exercici pràctic — Capítol 2: La Raspberry Pi 4 per dins

> 20-30 min · Real al teu sistema

## Objectiu

Recollir informació detallada del **hardware** de la teva Raspberry Pi. Això et servirà per saber què tens, què pots afegir, i on tens els límits.

## Requisits

- Tailscale actiu
- Connexió SSH a la RPi
- 20-30 minuts

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
```

## Pas 3: Memòria i swap (5 min)

```bash
# Memoria RAM total i usada
free -h

# Detall de la swap
swapon --show

# Memoria compartida amb GPU
vcgencmd get_mem gpu 2>/dev/null || echo "vcgencmd no disponible"
```

## Pas 4: Emmagatzematge (5 min)

```bash
# Espai de disc
df -h

# Detall del sistema de fitxers
mount | grep "on / " 

# Grandaria de la microSD (estimada)
lsblk

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
```

## Pas 7: Documenta-ho

Crea `book/curs/M1/02-raspberry-pi/inventari-hardware.md` amb tota la informació recollida.

## Validació

Has acabat si:
- [ ] Saps quin model exacte de RPi tens.
- [ ] Coneixes la freq de la CPU.
- [ ] Has vist la RAM total i l'ús actual.
- [ ] Has mesurat la temperatura.
- [ ] Has documentat la informació a `inventari-hardware.md`.

## Per aprofundir

- Instal·la `stress` i posa la CPU al 100% durant 5 min, mira com puja la temperatura: `sudo apt install stress && stress --cpu 4 --timeout 300`
- Compara el rendiment amb un disc SSD USB 3.0.
- Investiga si el teu model admesa PoE (Power over Ethernet) via HAT.
