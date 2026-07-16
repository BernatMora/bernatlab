# Exercici practic - Capitol 9: Troubleshooting

> 45-60 min · Real a la teva RPi

## Objectiu

Aprendre a fer troubleshooting aplicat: crear un "checkpoint" del sistema, simular fallades conegudes, diagnosticar-les amb les comandes, i resoldre-les. Acabaras amb un joc d'eines mentals per quan passin coses reals.

## Requisits

- RPi amb Docker funcionant
- Conexio SSH
- 45-60 minuts

## Pas 1: Instal·la eines de diagnostic (5 min)

```bash
sudo apt update
sudo apt install -y htop glances ncdu nethogs
```

Mira cada una:
- `htop`: processos amb colors
- `glances`: vista global amb `glances`
- `ncdu`: explorador de disc (compte, pot trigar)
- `nethogs`: quin proces fa mes xarxa

## Pas 2: Crea un checkpoint del sistema (10 min)

```bash
nano ~/bernatlab/CHECKPOINT.md
```

Crea un document amb:

```markdown
# Checkpoint BernatLab
Data: 2026-05-12

## Sistema
- Versio OS: $(cat /etc/os-release | head)
- Kernel: $(uname -r)
- Arquitectura: $(uname -m)
- Uptime: $(uptime)

## Recursos
- CPU: $(top -bn1 | grep load)
- RAM: $(free -h | head -2)
- Disc: $(df -h /)
- Temperatura: $(vcgencmd measure_temp)

## Xarxa
- IP: $(ip -4 addr show | grep inet | head)
- Gateway: $(ip route | head)
- DNS: $(cat /etc/resolv.conf)

## Docker
- Versio: $(docker --version)
- Contenidors actius: 
$(docker ps --format "  - {{.Names}}: {{.Image}} {{.Status}}")

- Imatges: 
$(docker images --format "  - {{.Repository}}:{{.Tag}} {{.Size}}")

## Serveis BernatLab
- [ ] Home Assistant: funciona?
- [ ] Grafana: funciona?
- [ ] Prometheus: funciona?
- [ ] Loki: funciona?
- [ ] Uptime Kuma: funciona?

## Configuracio Docker
- Volums: 
$(docker volume ls --format "  - {{.Name}}")
- Xarxes: 
$(docker network ls --format "  - {{.Name}}")
```

Guarda'l. Aquest es el teu "punt de referencia" de quan tot va be.

## Pas 3: Simula una fallada de CPU (10 min)

A la terminal SSH:

```bash
# Aixeca la CPU
yes > /dev/null &
yes > /dev/null &
yes > /dev/null &
yes > /dev/null &

# Mira quins processos son
ps aux --sort=-%cpu | head

# Htop interactivament
htop

# Glances (premer 'q' per sortir)
glances

# Despres de mirar
killall yes
```

## Pas 4: Simula una fallada d'espai (10 min)

```bash
# Crea un fitxer gran
dd if=/dev/zero of=/tmp/gran_fitxer bs=1M count=5000

# Mira com queda el disc
df -h
ncdu /tmp
docker system df

# Neteja
rm /tmp/gran_fitxer
```

Hauries de veure com canvia l'espai en temps real.

## Pas 5: Simula una fallada de xarxa (10 min)

```bash
# Primer comprova que tens xarxa
ping -c 4 8.8.8.8
ping -c 4 google.com

# Mira la teva IP
ip -4 addr show

# Comprova el gateway
ip route

# Comprova els ports oberts
ss -tulnp

# Comprova el DNS
nslookup google.com

# Prova un servei local
curl -v http://localhost:8123
```

## Pas 6: Simula una fallada de contenidor (10 min)

```bash
# Mira quins serveis tens
docker ps

# Atura un contenidor
docker stop homeassistant

# Mira l'estat
docker ps -a
docker ps -a --filter "status=exited"

# Mira els logs
docker logs homeassistant --tail 20

# Torna'l a aixecar
docker start homeassistant

# Verifica
docker ps | grep homeassistant
```

## Pas 7: Practica un diagnostic complet (10 min)

Escriu un diagnostic pas a pas d'un problema simulat. Per exemple, "Grafana no carrega al navegador":

1. Verificar: el servei esta corrent?
```bash
docker ps | grep grafana
```

2. Si esta corrent, comprovar els logs:
```bash
docker logs grafana --tail 50
```

3. Si els logs mostren error, mirar el port:
```bash
ss -tulnp | grep 3000
```

4. Si el port no escolta, mirar la configuracio:
```bash
docker exec grafana cat /etc/grafana/grafana.ini | head
```

5. Si tot sembla OK, mirar si arriba des de fora:
```bash
curl -v http://localhost:3000
```

## Validacio

Has acabat si:

- [ ] Has instal·lat htop, glances, ncdu, nethogs.
- [ ] Has creat un CHECKPOINT.md de l'estat actual.
- [ ] Has practicat la simulacio de fallada de CPU.
- [ ] Has practicat la simulacio de fallada d'espai.
- [ ] Has practicat la simulacio de fallada de xarxa.
- [ ] Has practicat la simulacio de fallada de contenidor.
- [ ] Has fet un diagnostic complet d'un servei concret.

## Per aprofundir

- Investiga ctop per monitorar contenidors desde terminal.
- Prova `dmesg | less` per veure els missatges del kernel.
- Aprèn a fer `strace` per seguir les crides al sistema d'un proces.
- Mira la documentacio del teu router per accedir a la configuracio.
