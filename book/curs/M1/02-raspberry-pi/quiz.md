# Qüestionari — Capítol 2: La Raspberry Pi 4 per dins

> 15 preguntes · ~20 min

## Pregunta 1
Què és una Raspberry Pi?

- [ ] Un processador per a mòbils
- [x] Un ordinador complet en una placa (SBC)
- [ ] Un tipus de router
- [ ] Un sistema operatiu Linux

## Pregunta 2
Quina arquitectura de CPU té la RPi 4?

- [x] ARM (arm64)
- [ ] x86 (Intel)
- [ ] x86_64 (AMD)
- [ ] RISC-V

## Pregunta 3
Quanta RAM té la teva Raspberry Pi 4 al BernatLab?

- [ ] 1 GB
- [ ] 2 GB
- [x] 4 GB
- [ ] 8 GB

## Pregunta 4
On s'emmagatzema el sistema operatiu de la RPi?

- [ ] En un disc dur intern
- [x] En una targeta microSD
- [ ] A la memòria RAM
- [ ] Al núvol

## Pregunta 5
Quin és el consum aproximat d'una RPi 4?

- [ ] 0.5 W
- [x] 5-10 W
- [ ] 50-100 W
- [ ] 200-300 W

## Pregunta 6
Quina és la temperatura crítica (perill de dany) de la RPi 4?

- [ ] 60°C
- [ ] 70°C
- [ ] 80°C
- [x] 85°C

## Pregunta 7
Quin és el primer procés que arranca al sistema (PID 1)?

- [ ] Docker
- [ ] El kernel
- [x] systemd
- [ ] El shell

## Pregunta 8
Quin port s'usa per alimentar la RPi 4?

- [ ] micro-USB
- [x] USB-C
- [ ] Barrel jack
- [ ] Lightning

## Pregunta 9
Quina ordre et mostra l'arquitectura del processador a Linux?

- [x] uname -m
- [ ] arch
- [ ] cpuinfo
- [ ] lscpu arch

## Pregunta 10
Quin avantatge té muntar el sistema a una microSD classe A2?

- [ ] Més capacitat d'emmagatzematge
- [x] Millor rendiment en operacions d'entrada/sortida aleatòries (IOPS)
- [ ] Més velocitat de lectura seqüencial
- [ ] Preu més baix

## Pregunta 11
Quin component de la RPi és el que més escalfa?

- [ ] La memòria RAM
- [x] El SoC (CPU + GPU + controlador de memòria)
- [ ] El xip d'Ethernet
- [ ] El regulador de tensió

## Pregunta 12
Quin dels següents factors NO afecta la durada d'una targeta microSD?

- [ ] El nombre d'escriptures
- [ ] La temperatura d'operació
- [x] El color de la placa base
- [ ] L'ús de swap intensiu

## Pregunta 13 (oberta)
Explica amb les teves paraules: per què una Raspberry Pi és adequada per a un homelab però NO per a un servidor de producció professional?

Pistes per respondre:
- Pensa en potència, memòria, emmagatzematge, fiabilitat.
- Quines aplicacions serien adequades per a la RPi? Quines no?
- Què significa "SLA" en un context empresarial?

## Pregunta 14 (oberta)
Imagina que vols muntar un servidor web per a una botiga online amb 1000 visites diaries. La RPi 4 seria adequada? Per què sí o per què no?

Pistes per respondre:
- Quanta memòria RAM necessitaries per a 1000 visites diaries?
- Quina diferència hi ha entre "prou" i "còmode"?
- Quan caldria pujar a un servidor de veritat?
- Què passaria si hi ha un pic sobtat (campanya, Black Friday)?

## Pregunta 15 (oberta)
La teva RPi s'ha mort i tens una de recanvi. Explica quins 3 passos faries primer per posar-la en marxa amb la teva configuració actual del BernatLab (hostname `hortosona`, Debian 13, IP Tailscale 100.x.y.z).

Pistes per respondre:
- Què fas amb el sistema operatiu (quina eina, quin sistema)?
- Com recuperes la teva configuració (on la tens guardada)?
- Quin és el risc de no tenir una còpia de la microSD?
