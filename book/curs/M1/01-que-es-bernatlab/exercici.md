# Exercici pràctic — Capítol 1: Què és BernatLab

> 45-60 min · Real al teu sistema

## Objectiu

Fer un **inventari real del teu BernatLab** — què hi tens, com hi accedeixes, què funciona, i què no. Això et servirà com a "foto inicial" del projecte, i com a base per a tota la resta del curs.

## Requisits

- Tailscale instal·lat al teu Windows/Mac/Linux.
- La Raspberry Pi encesos i connectada.
- El terminal a mà (PowerShell o bash).
- 45-60 minuts.

## Pas 1: Comprova la connectivitat (5 min)

Des del teu PC, obre el terminal i comprova que pots accedir a la Raspberry:

```bash
ssh bernat@hortosona
# o per IP Tailscale:
ssh bernat@100.x.y.z
```

Si no pots, comprova:
- Està la RPi encesos? (LED verd)
- Tailscale està actiu? (`tailscale status`)
- La xarxa WiFi funciona?

## Pas 2: Inventari de serveis (10 min)

Un cop dins, comprova quins serveis estan corrent:

```bash
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```

Copia la sortida a un document. Hauries de veure almenys 4-5 contenidors.

També mira quines imatges tens descarregades i quins volums:

```bash
docker images
docker volume ls
docker network ls
```

## Pas 3: Comprova els serveis (10 min)

Des del navegador, accedeix a cada servei i fes una captura de pantalla:

- **Homepage**: http://100.x.y.z:3000
- **Portainer**: https://100.x.y.z:9443
- **Uptime Kuma**: http://100.x.y.z:3001

Si algun no carrega, **apunta-ho** — serà un tema per als capítols posteriors.

## Pas 4: Informació del sistema (5 min)

Recull aquesta informació:

```bash
# Versió del sistema
cat /etc/os-release | head -5

# Nucli i arquitectura
uname -a

# Ús de disc
df -h /

# Ús de memòria
free -h

# Temperatura de la CPU
vcgencmd measure_temp 2>/dev/null || echo "No tens vcgencmd"

# Uptime (des de quan esta encès)
uptime -p

# IPs de xarxa
ip -4 addr show | grep inet
```

## Pas 5: Test de càrrega real (10 min)

Per veure si la RPi aguanta el que li tires, fes un test ràpid:

```bash
# Obre htop en una finestra
htop

# En una altra, llança 4 processos que consumeixin CPU
yes > /dev/null &
yes > /dev/null &
yes > /dev/null &
yes > /dev/null &

# Mira com puja la CPU a htop. Espera 30 segons.

# Temperatura
vcgencmd measure_temp

# Mata els processos yes
killall yes
```

Apunta la temperatura màxima. Si passa de 70°C sense dissipador, caldria posar-ne un.

## Pas 6: Comprova les alertes (5 min)

Vés a Uptime Kuma. Mira quins monitors tens actius. Tots verds? Si n'hi ha algun de vermell, **no t'espantis** — és el motiu exacte pel qual tens Uptime Kuma. Apunta quin és.

## Pas 7: Documenta-ho (10-15 min)

Crea un fitxer `book/curs/M1/01-que-es-bernatlab/inventari.md` amb:

```markdown
# Inventari del meu BernatLab (data)

## Connexió
- Tailscale: [sí/no]
- IP: [100.x.y.z]
- Puc entrar per SSH: [sí/no]
- Mètode (clau vs contrasenya): [què uso]

## Serveis actius
[enganxa la sortida de docker ps]

## Serveis accessibles
- Homepage: [sí/no]
- Portainer: [sí/no]
- Uptime Kuma: [sí/no]

## Sistema
- SO: [la sortida de /etc/os-release]
- Nucli: [la sortida de uname -a]
- Disc lliure: [de df -h]
- RAM lliure: [de free -h]
- Temperatura CPU: [de vcgencmd]
- Temperatura sota càrrega: [de l'apartat 5]
- Uptime: [de uptime -p]

## Alertes
- Monitors Uptime Kuma actius: [X de Y verds]
- Monitors que fallen: [quina i per què]

## Observacions
[Cosa que no funcioni, coses que vegis estranyes, etc.]
```

## Validació

Has acabat si:
- [ ] Has pogut accedir a la RPi per SSH.
- [ ] T'ha sortit una llista de contenidors amb `docker ps`.
- [ ] Has accedit a Homepage, Portainer, i Uptime Kuma.
- [ ] Has recollit la informació del sistema.
- [ ] Has fet el test de càrrega i has apuntat la temperatura màxima.
- [ ] Has comprovat l'estat dels monitors a Uptime Kuma.
- [ ] Has creat el fitxer `inventari.md`.

## Per aprofundir

- Mira quantes imatges Docker tens descarregades: `docker images | wc -l`
- Comprova l'ús de xarxa: `docker network ls`
- Mira els volums: `docker volume ls`
- Comprova la mida de cada volum: `docker system df -v`
- Fes una captura de la corba de temperatura: `watch -n 1 vcgencmd measure_temp` durant un minut.

## Ves un pas més enllà

**Repte avançat: escriu un "runbook" d'una pàgina**.

Imagina que demà la teva RPi deixa de respondre. Amb la sola informació del teu `inventari.md`, una altra persona (o tu mateix d'aquí 6 mesos) hauria de saber:
1. Com entrar-hi (quins comandaments exactes).
2. Com saber què falla (quins logs mirar, quines ordres executar).
3. Com recuperar els serveis sense perdre dades (quina és la "veritat" del sistema).

Afegeix una secció "Runbook de recuperació" al teu `inventari.md`. Inclou:
- L'ordre exacta per reconnectar des d'una cafeteria.
- L'ordre per veure l'estat de tots els contenidors d'una sola ullada.
- L'ordre per reiniciar tot l'stack.
- L'ordre per fer un backup del volum de Portainer abans de tocar res.
