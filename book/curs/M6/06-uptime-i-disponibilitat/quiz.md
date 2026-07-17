# Qüestionari - Capitol 6: Uptime i disponibilitat

> 10 preguntes · ~15 min

## Pregunta 1
Que es un SLA?

- [ ] Un sistema operatiu
- [x] Un acord sobre la disponibilitat d'un servei
- [ ] Un tipus de base de dades
- [ ] Un protocol de xarxa

## Pregunta 2
Quin SLA correspon a "3 nines" (99.9%)?

- [ ] 1 hora d'inactivitat per any
- [x] 8.76 hores d'inactivitat per any
- [ ] 1 dia d'inactivitat per any
- [ ] 1 setmana d'inactivitat per any

## Pregunta 3
Per que cal un monitor EXTERN i no nomes un intern?

- [ ] Mes rapid
- [x] Perque el monitor intern cau amb el sistema i no detecta fallades de xarxa
- [ ] Perque es mes bonic
- [ ] Perque es obligatori

## Pregunta 4
Quin es el nom de l'eina de monitoratge auto-allotjada que hem vist?

- [ ] Prometheus
- [x] Uptime Kuma
- [ ] Grafana
- [ ] Nagios

## Pregunta 5
A quin port escolta Uptime Kuma per defecte?

- [ ] 3000
- [x] 3001
- [ ] 8080
- [ ] 9090

## Pregunta 6
Que es una "status page" publica?

- [ ] Un blog personal
- [x] Una pagina web que mostra l'estat dels teus serveis en temps real
- [ ] Un sistema d'alertes
- [ ] Un panel d'administracio privat

## Pregunta 7
Quin tipus de probe faries servir per comprovar que el port 22 (SSH) esta obert?

- [ ] HTTP
- [x] TCP
- [ ] DNS
- [ ] Ping

## Pregunta 8
Quin servei cloud gratuit permet tenir fins a 50 monitors amb comprovacio cada 5 minuts?

- [ ] Datadog
- [x] UptimeRobot
- [ ] New Relic
- [ ] Grafana Cloud

## Pregunta 9 (oberta)
Explica per que un monitor INTERN nomes no es suficient. Posa un exemple concret del BernatLab on un monitor extern detectaria una fallada que l'intern no veuria.

Pistes per respondre:
- El monitor intern es a la RPi. Si la RPi es penja, el monitor tambe.
- No detecta fallades de xarxa, de router, de DHCP.
- Exemple concret: el router es reinicia, la RPi agafa una IP nova, tot "funciona" des de dins pero no es accessible des de fora.

## Pregunta 10 (oberta)
Has de configurar la monitoritzacio externa del BernatLab. Quins 7-10 monitors configuraries i quina informacio et donaria cadascun?

Pistes per respondre:
- Pensa en els serveis claus: HA, Grafana, Prometheus, Loki, el router, la propia RPi.
- Pensa tambe en coses externes: una API de meteo que fas servir, el DNS, la propia conexio a internet.
- Per cada un: tipus de probe, URL/adreca, frequencia, severitat.


## Pregunta 11 (oberta amb pistes)
Per que sha de monitoritzar la disponibilitat des de fora i des de dins

**Pistes**: pensa en com aplicaries aquest concepte al teu hort IoT amb la teva RPi (hortosona, 100.115.134.76).
## Pregunta 12 (oberta amb pistes)
Explica que es un SLA i com sha de triar per a un homelab

**Pistes**: pensa en com aplicaries aquest concepte al teu hort IoT amb la teva RPi (hortosona, 100.115.134.76).
## Pregunta 13 (oberta amb pistes)
Quines serien les pagines o serveis mes importants a monitorar al teu BernatLab

**Pistes**: pensa en com aplicaries aquest concepte al teu hort IoT amb la teva RPi (hortosona, 100.115.134.76).
