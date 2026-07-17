# Qüestionari - Capitol 1: Arquitectura 24/7

> 10 preguntes · ~15 min

## Pregunta 1
Que vol dir exactament tenir un servei "24/7"?

- [ ] Que el servidor esta sempre encès, sense mes
- [x] Que es disponible, observable, recuperable i mantingut
- [ ] Que nomes funciona amb WiFi
- [ ] Que nomes funciona de nit

## Pregunta 2
Quin es el punt unic de fallada mes critic d'una RPi?

- [ ] El procesador
- [ ] La memoria RAM
- [x] La targeta microSD
- [ ] El port HDMI

## Pregunta 3
Que fa el watchdog de Linux?

- [ ] Vigila els gossos del vei
- [x] Reinicia el sistema si el kernel es queda penjat
- [ ] Comprova si tens correu nou
- [ ] Actualitza el sistema automaticament

## Pregunta 4
Quina directiva de docker-compose fa que un contenidor es torni a aixecar sol?

- [ ] auto-restart: yes
- [x] restart: always
- [ ] always-up: true
- [ ] start: on-boot

## Pregunta 5
Quina es la diferencia entre un servidor "encès" i un servidor "24/7"?

- [ ] Cap, son sinonims
- [ ] 24/7 nomes funciona a empreses
- [x] 24/7 te observabilitat, recuperacio i manteniment
- [ ] Nomes es marketing

## Pregunta 6
Quina ordre mostra la temperatura actual de la CPU a la RPi?

- [ ] sensors
- [ ] cat /proc/cpuinfo
- [x] vcgencmd measure_temp
- [ ] thermal_check

## Pregunta 7
Quantes capes te l'arquitectura 24/7 que hem descrit?

- [ ] 3
- [ ] 5
- [x] 7
- [ ] 10

## Pregunta 8
Quin valor de max-load-1 al watchdog indica que el sistema esta sobrecarregat?

- [ ] 1
- [ ] 100
- [x] 24 o mes (24 processos bloquejats)
- [ ] 1000

## Pregunta 9 (oberta)
Enumera les 7 capes de l'arquitectura 24/7 i explica per que es important que cada capa tingui els seus propis monitors.

Pistes per respondre:
- Les 7 capes son: fisica, SO, contenidors, aplicacio, observabilitat, alerta, manteniment.
- Pensa en que pasa si nomes monitors la capa d'aplicacio i no la fisica.
- Quina avantatge te aillar les fallades per capa?

## Pregunta 10 (oberta)
La teva RPi s'ha penjat a les 3 de la matinada mentre dormies. Enumera les 3 coses que hauries d'haver preparat abans per detectar i recuperar el sistema sense haver de llevar-te.

Pistes per respondre:
- Pensa en monitoritzacio automatica (que t'avisi).
- Pensa en reinici automatic (que la RPi sola es reinicii o el contenidor es torni a aixecar).
- Pensa en acces remot (per si necessites intervenir).


## Pregunta 11 (oberta amb pistes)
Per que sha de pensar en 24/7 abans de tenir el sistema muntat

**Pistes**: pensa en com aplicaries aquest concepte al teu hort IoT amb la teva RPi (hortosona, 100.115.134.76).
## Pregunta 12 (oberta amb pistes)
Explica la diferencia entre disponibilitat i resiliencia amb un exemple del teu hort

**Pistes**: pensa en com aplicaries aquest concepte al teu hort IoT amb la teva RPi (hortosona, 100.115.134.76).
## Pregunta 13 (oberta amb pistes)
Quines serien les parts critiques que no poden caure mai al teu sistema

**Pistes**: pensa en com aplicaries aquest concepte al teu hort IoT amb la teva RPi (hortosona, 100.115.134.76).
