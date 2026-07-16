# Resum - Capitol 9: Troubleshooting

## La idea clau

Tots els sistemes fallen. La diferencia entre un administrador de sistemes bo i un de dolent no es que el primer no tingui fallades, sino que SAP diagnosticar-les i arreglar-les rapid. El troubleshooting es l'art d'identificar l'arrel del problema quan tot va malament, sense perdre hores buscant a cegues.

## La metodologia: divideix i venceras

Quan algo falla, el primer instint es provar coses a l'atzar ("reinicieu la RPi", "buideu cache"...). Aixi NO es troubleshooting, es perdre el temps. El mètode correcte es:

1. **Definir el problema**: QUE falla exactament?
2. **Recollir dades**: QUAN ha passat? Desde quan? Que ha canviat?
3. **Identificar la capa**: fisica, SO, xarxa, contenidors, aplicacio?
4. **Aillar la causa**: que SI funciona? que NO funciona?
5. **Aplicar la solucio**: nomes un canvi a la vegada.
6. **Verificar**: ha tornat a funcionar? Romandrá estable?
7. **Documentar**: escriu al runbook que ha passat (cap 10).

## Les capes del sistema (model OSI aplicat)

Per a una RPi amb Docker, podem dividir el sistema en capes:

```
[7. Aplicacio]      <- El servei concret (HA, Grafana, etc.)
[6. Configuracio]   <- docker-compose.yml, .env
[5. Contenidor]     <- Docker engine, imatges
[4. Sistema]        <- Processos, serveis, fitxers
[3. Xarxa]          <- IP, DNS, ports, firewall
[2. Hardware]       <- Disc, RAM, USB, sensors
[1. Fisica]         <- Alimentacio, temperatura, cables
```

Quan algo falla, comença per baix (fisica) i puja. O comença per dalt (aplicacio) i baixa. La gracia es que la fallada esta a UNA capa, no a totes.

## Comandes essentials de diagnostic

### Sistema basic

```bash
# Visio general
uptime
top
htop
free -h
df -h

# Temperatura
vcgencmd measure_temp
cat /sys/thermal/thermal_zone0/temp

# Logs del sistema
journalctl -f
journalctl -u docker --since "1 hour ago"
```

### Xarxa

```bash
# Veure les interficies
ip a
ifconfig

# Taula de routing
ip route

# DNS
cat /etc/resolv.conf
nslookup google.com

# Connexions obertes
ss -tulnp
netstat -tulnp

# Provar connectivitat
ping 8.8.8.8
ping google.com
curl -v http://192.168.1.50:8123
```

### Docker

```bash
# Estat dels contenidors
docker ps -a
docker stats

# Logs
docker logs homeassistant
docker logs homeassistant --tail 50
docker logs homeassistant -f

# Inspeccionar
docker inspect homeassistant
docker top homeassistant

# Entrar dins un contenidor
docker exec -it homeassistant /bin/bash
```

### Recursos

```bash
# Processos que mes CPU gasten
ps aux --sort=-%cpu | head

# Processos que mes memoria gasten
ps aux --sort=-%mem | head

# Espai en disc
du -sh /var/lib/docker/volumes/
ncdu /

# Limitacio de recursos
ulimit -a
```

## Eines visuals

Per tenir una vista rapida de tot:

- **htop**: gestor de processos interactiu.
- **glances**: monitor complet amb CPU, RAM, xarxa, disc.
- **ctop**: monitor de contenidors Docker.
- **lazydocker**: UI de terminal per Docker.
- **ncdu**: explorador de disc interactiu.

```bash
sudo apt install htop glances
sudo pip3 install ctop
```

## Troubleshooting per categoria

### "La RPi no respon"

1. **Ping**: `ping IP_RPI` desde un altre PC. Si no respon, es xarxa.
2. **Si la xarxa va be**: intenta accedir per SSH. Si no va, es un problema mes profund.
3. **Si tampoc va per SSH**: monitor + teclat directament. Es la pantalla blava de la mort?
4. **Si tampoc te pantalla**: pot ser corrent. Desendolla i reendolla.
5. **Si segueix mort**: microSD o font d'alimentacio.

### "Un contenidor esta exited"

1. `docker ps -a` per veure tots els contenidors.
2. `docker logs NOM` per veure que ha dit abans de morir.
3. `docker inspect NOM` per veure la configuracio.
4. Sovint es un error de configuracio o de volum.
5. Prova: `docker compose up NOM` per tornar a aixecar.

### "El sistema va lent"

1. `top` o `htop` per veure processos.
2. `docker stats` per veure contenidors.
3. `vcgencmd measure_temp` per veure temperatura.
4. Si la CPU es 100%, mira quin proces la gasta.
5. Si el swap es alt, tens poca RAM. Mira contenidors.
6. Si la temperatura es alta, ventilacio o neteja.

### "No puc accedir a un servei des de fora"

1. Verifica que el servei esta corrent: `docker ps`.
2. Verifica que escolta al port correcte: `ss -tulnp`.
3. Verifica que el firewall deixa passar: `sudo ufw status`.
4. Verifica que el router ha redirigit el port.
5. Verifica la DDNS: `nsbernatlab.example.com` apunta a la teva IP publica?
6. Fes un test des de fora amb el mobil amb dades mobils.

### "La microSD es corromp"

Senyals:
- Logs amb errors d'I/O
- Sistema inestable
- `dmesg` mostra errors d'EXT4

Solucio:
- Mou a USB o SSD
- Activa `noatime` al mount
- Limita les escriptures (logs a RAM, base de dades a SSD)

### "El contenidor fa coses rares"

1. Atura el contenidor: `docker stop NOM`.
2. Mira els logs: `docker logs NOM`.
3. Entra dins: `docker exec -it NOM /bin/bash`.
4. Mira els processos dins: `ps aux`.
5. Comprova fitxers: `ls -la /config/`.

## El concepte de "checkpoint"

Quan un sistema funciona BE, fes un "checkpoint" - documenta l'estat. Aixi quan falli, saps com era quan anava be:

- Versio de cada imatge Docker.
- Configuracio de xarxa.
- Espai en disc.
- Llista de serveis actius.
- Sortida de `docker stats --no-stream`.

Guarda-ho a `~/bernatlab/CHECKPOINT.md` o similar.

## Buscar ajuda

Quan no trobes la solucio:

1. **Google**: `error especific + versio`. El error exacte es clau.
2. **GitHub issues**: busca el projecte, mira issues oberts/tancats.
3. **Forums especialitzats**: Home Assistant Community, Raspberry Pi Forums, etc.
4. **StackOverflow**: nomes si es molt generic.
5. **ChatGPT / Claude**: pot ajudar pero SEMPRE verifica la solucio.

Sigues específic al preguntar. "No em funciona Home Assistant" no serveix. "Home Assistant 2024.5 falla al arrancar amb error 'config integration not found'" si.

## Connexions amb altres capitols

- **M6 Cap 1** - Arquitectura 24/7: les capes que hem vist aqui.
- **M6 Cap 5** - Logs centralitzats: on buscar els missatges d'error.
- **M6 Cap 10** - Runbooks: per documentar el troubleshooting.
- **M8 Cap 7** - Runbooks basics (introduccio).
