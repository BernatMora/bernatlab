# Respostes - Capitol 1: Arquitectura 24/7

> Mira les respostes DESPRES d'haver fet el qüestionari.

## Pregunta 1: Que vol dir 24/7?

**Resposta correcta**: Que es disponible, observable, recuperable i mantingut.

**Explicacio**: Un servidor nomes "encès" no es 24/7. Falten les altres tres condicions. Si no pots VEURE quan falla (observable), no el pots fer tornar a aixecar rapid (recuperable), o es mor perque no l'has tocat mai (mantingut), tens un servidor que nomes te la primera condicio. Es molt habitual tenir la RPi mes de 6 mesos sense mirar-la i trobar-te amb el disc ple, 3 serveis caiguts i un munt d'actualitzacions pendents.

---

## Pregunta 2: Punt unic de fallada critic

**Resposta correcta**: La targeta microSD.

**Explicacio**: La microSD te un nombre limitat d'escriptures. Si tens els logs, la cache i les bases de dades escrivint-hi tot el dia, en 6-12 mesos pot fallar. Per això al M2 vam moure els volums a USB/SSD, i al M6 mouren els logs fora tambe. La millor inversio es un SSD USB3 de 120 GB per ~25 EUR.

---

## Pregunta 3: Que fa el watchdog?

**Resposta correcta**: Reinicia el sistema si el kernel es queda penjat.

**Explicacio**: El watchdog es un temporitzador hardware (o emulat per la CPU) que el kernel ha de "colpejar" regularment. Si el kernel penja i deixa de colpejar, el watchdog forca un reinici. Es l'última xarxa de seguretat quan tot lo altre falla. No es elegant pero funciona.

---

## Pregunta 4: Restart automatic a Docker

**Resposta correcta**: `restart: always`.

**Explicacio**: `restart: always` fa que Docker torni a aixecar el contenidor si cau, si la RPi es reinicia, o si Docker es reinicia. L'altre opcio valida es `restart: unless-stopped` que nomes el reinicia si no l'has aturat tu manualment (pot ser mes convenient en alguns casos). Important: nomes funciona amb `docker compose` o `docker run`, NO funciona amb contenidors creats sense aquesta opcio.

---

## Pregunta 5: Diferencia entre encès i 24/7

**Resposta correcta**: 24/7 te observabilitat, recuperacio i manteniment.

**Explicacio**: Un servidor nomes "encès" es com un cotxe al que no li has canviat mai l'oli ni l'has portat mai al taller. Funciona... fins que deixa de funcionar. Un servidor 24/7 te les eines per saber que passa, els mecanismes per recuperar-se sol, i les rutines de manteniment perque no es degradi amb el temps.

---

## Pregunta 6: Ordre per veure temperatura

**Resposta correcta**: `vcgencmd measure_temp`.

**Explicacio**: `vcgencmd` es una eina especifica de la Raspberry Pi que permet accedir a informacio del hardware. `measure_temp` llegeix el sensor de temperatura de la CPU. Altres eines com `sensors` (de lm-sensors) tambe funcionen pero a la RPi requereixen configuracio previa. La temperatura critica es 80 graus (comenca el throttling automatic).

---

## Pregunta 7: Quantes capes te l'arquitectura

**Resposta correcta**: 7.

**Explicacio**: Fisica, sistema operatiu, contenidors, aplicacio, observabilitat, alerta, manteniment. Cada capa es independent i te els seus propis monitors. Si nomes monitors l'aplicacio, no saps si la temperatura esta pujant. Si nomes monitors el hardware, no saps si Grafana ha caigut. Cal cobrir-les totes.

---

## Pregunta 8: Valor de max-load-1

**Resposta correcta**: 24 o mes (24 processos bloquejats).

**Explicacio**: `max-load-1` es la carrega mitjana del sistema en 1 minut. Si passa del llindar, el watchdog considera que el sistema esta col·lapsat. Per una RPi petita amb 4 cors, 24 es un bon llindar (correspon a 6 processos per core esperant). Si el teu sistema es mes potent o te mes serveis, potser vulguis pujar-ho a 32-48.

---

## Pregunta 9 (oberta): Les 7 capes

**Resposta model**:

Les **7 capes de l'arquitectura 24/7** son:

1. **Capa fisica**: RPi, alimentacio, microSD, xarxa, temperatura, caixa, ventilacio.
2. **Capa sistema operatiu**: Raspberry Pi OS, kernel, serveis basics (ssh, cron, ntp).
3. **Capa contenidors**: Docker, Portainer, imatges, volums, xarxes, docker-compose.
4. **Capa aplicacio**: els serveis del BernatLab (Home Assistant, InfluxDB, Grafana, nodered, etc.).
5. **Capa observabilitat**: Prometheus, Grafana, Uptime Kuma, journald - tot el que t'ajuda a VEURE.
6. **Capa alerta**: Telegram, email, SMS - el que t'avisa QUAN falla alguna cosa.
7. **Capa manteniment**: backups, neteja, actualitzacions - el que MANTI el sistema sa al llarg del temps.

Es important que cada capa tingui els seus propis monitors perque si nomes monitors la capa d'aplicacio, no saps que la microSD s'esta morint. I si nomes monitors el hardware, no saps que Grafana ha caigut. Aillar les fallades per capa et permet saber exactament on esta el problema. Si veus que el contenidor de Grafana ha caigut pero la RPi esta be, el problema es a la capa 4, no a la 1. Si el contenidor esta be pero no respon, pot ser la capa 3 (xarxa docker) o la 2 (port tancat al firewall).

---

## Pregunta 10 (oberta): Les 3 coses a preparar

**Resposta model**:

Si la RPi es penja a les 3 de la matinada, les 3 coses que hauries d'haver preparat son:

1. **Monitoritzacio automatica amb alerta**: cal alguna cosa que t'avisi sense que tu ho provis. Pot ser Uptime Kuma que fa ping al teu servidor i envia un missatge a Telegram si deixa de respondre, o un script que vigili la RPi i t'avisi si esta caiguda. La idea es que TU no hagis de mirar res - el sistema t'avisa. Si no tens res automatic, no t'assabentares fins que un client et truqui al matí següent.

2. **Reinici automatic**: el watchdog de Linux i la directiva `restart: always` de Docker son essentials. Si nomes tens el watchdog pero els teus serveis fallen sovint, el sistema es reiniciara mes del compte i acabara danyant la microSD. Si nomes tens restart als contenidors pero la RPi queda penjada, els contenidors no es poden aixecar. Cal cobrir TOTS DOS escenaris. Una fallada tipica es que un contenidor consumeixi tota la memoria i el sistema es pengi - el watchdog el reiniciara i els contenidors tornaran a pujar.

3. **Acces remot preparat**: abans que passi l'emergencia, has de tenir llest un pla per accedir. Si estas fora de casa, necessites una VPN (WireGuard es la millor opcio a la RPi) o un tunel invers (Tailscale, ZeroTier). Si nomes tens SSH al router de casa, i el router es reinicia, no pots entrar. Tambe cal tenir un pla B: un company de casa que sap on es la RPi i pot fer un reinici fisic, o una presa de corrent intel·ligent (TP-Link, Shelly) que puguis apagar i encendre des del movil per forçar un reboot.

A mes a mes, despres d'un incident, cal **documentar** que ha passat. Es el que veurem al capitol 10 de runbooks.

---

## Que fer si has fallat moltes preguntes

- **5-8 encerts**: Rellegir el resum i fer l'exercici practic.
- **3-4 encerts**: Refes l'exercici desde zero observant cada pas.
- **0-2 encerts**: Repassem junts el capitol abans de continuar.

## Que fer si has encertat totes

- Passa al **Capitol 2** (Prometheus).
- Investiga eHealth o altres solucions professionals d'observabilitat.
- Mira com configurar un UPS per la RPi (per si marxa la llum).
