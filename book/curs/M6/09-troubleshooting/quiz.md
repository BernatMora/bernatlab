# Qüestionari - Capitol 9: Troubleshooting

> 10 preguntes · ~15 min

## Pregunta 1
Quin es el primer pas en troubleshooting?

- [ ] Reiniciar tot
- [x] Definir el problema exactament
- [ ] Buscar a Google
- [ ] Preguntar al fòrum

## Pregunta 2
Quina ordre mostra els procesos actius amb la seva CPU i memoria?

- [ ] ps
- [x] top o htop
- [ ] jobs
- [ ] tasklist

## Pregunta 3
Quina comanda Docker mostra els logs d'un contenidor?

- [x] docker logs NOM
- [ ] docker ps
- [ ] docker inspect
- [ ] docker stats

## Pregunta 4
Quina comanda mostra la temperatura de la CPU a la RPi?

- [x] vcgencmd measure_temp
- [ ] cat /proc/cpuinfo
- [ ] sensors
- [ ] thermal_check

## Pregunta 5
Quina ordre Docker permet entrar dins d'un contenidor interactiu?

- [ ] docker enter
- [x] docker exec -it NOM /bin/bash
- [ ] docker attach NOM
- [ ] docker shell NOM

## Pregunta 6
Quin es el millor enfocament quan un sistema va lent?

- [ ] Reiniciar
- [x] Identificar quin proces o servei consumeix mes recursos
- [ ] Comprar mes RAM
- [ ] Formatejar-ho tot

## Pregunta 7
Quin fitxer mostra la configuracio DNS a Linux?

- [ ] /etc/hosts
- [x] /etc/resolv.conf
- [ ] /etc/dns.conf
- [ ] /etc/network/interfaces

## Pregunta 8
Quina eina es un monitor complet amb CPU, RAM, xarxa i disc en una sola pantalla?

- [ ] top
- [x] glances
- [ ] htop
- [ ] ps

## Pregunta 9 (oberta)
Descriu la metodologia de troubleshooting pas a pas. Per que NO s'ha de provar coses a l'atzar?

Pistes per respondre:
- Definir el problema, recollir dades, identificar la capa, aillar, solucio, verificar, documentar.
- Per que no a l'atzar: perque no saps que ha funcionat, pots crear nous problemes.

## Pregunta 10 (oberta)
La teva RPi no respon al ping. Enumera els 5-6 punts que comprovaries per ordre per trobar on esta la fallada, de mes basic (alimentacio) a mes especific (servei).

Pistes per respondre:
- Capa fisica: te corrent? els cables?
- Capa hardware: els LEDs s'encenen? ventiladors giren?
- Capa xarxa: el cable de xarxa esta connectat? el router esta encès?
- Capa sistema: la RPi arranca? veus res per HDMI?
- Capa SO: arriba a la pantalla de login?
- Capa servei: SSH esta corrent?
