# Qüestionari - Capitol 5: Logs centralitzats

> 10 preguntes · ~15 min

## Pregunta 1
Que es un log?

- [x] Una linia de text amb timestamp i missatge
- [ ] Un tipus de base de dades
- [ ] Un protocol de xarxa
- [ ] Un sistema de copia de seguretat

## Pregunta 2
Quin servei de Linux s'encarrega de recollir els logs del sistema?

- [ ] syslog
- [x] journald (systemd-journald)
- [ ] logstash
- [ ] promtail

## Pregunta 3
Quina comanda mostra els logs d'un contenidor Docker?

- [ ] docker show
- [x] docker logs
- [ ] docker read
- [ ] docker trace

## Pregunta 4
Quin es l'equivalent a Prometheus pero per logs?

- [ ] Elasticsearch
- [x] Loki
- [ ] Kibana
- [ ] Logstash

## Pregunta 5
Quin agent s'encarrega d'enviar els logs a Loki?

- [ ] Logstash
- [ ] Fluentd
- [x] Promtail
- [ ] Filebeat

## Pregunta 6
Quin llenguatge de consultes utilitza Loki?

- [ ] PromQL
- [x] LogQL
- [ ] SQL
- [ ] JSONPath

## Pregunta 7
Quin operador a LogQL vol dir "conté el text"?

- [ ] ==
- [x] |=
- [ ] ~
- [ ] :

## Pregunta 8
Quina eina s'encarrega de rotar els fitxers de log tradicionals a Linux?

- [x] logrotate
- [ ] journald
- [ ] cron
- [ ] logkeeper

## Pregunta 9 (oberta)
Explica les tres opcions de stack de logs que hem vist (journald simple, Loki, ELK) i per que Loki es la millor opcio per a una RPi del BernatLab.

Pistes per respondre:
- journald nomes: basic, nomes terminal, no te UI web.
- Loki: open source, integra amb Grafana, lleuger, escala be.
- ELK: el mes complet pero massa pesat per RPi (RAM, CPU, disc).
- Per que Loki es la tria correcta: balance entre funcionalitat i recursos.

## Pregunta 10 (oberta)
Has d'investigar per que un contenidor de Home Assistant falla. Escriu els passos que faries per trobar l'error utilitzant Loki + Grafana, des de detectar el problema fins a obtenir la linia de log concreta.

Pistes per respondre:
- Com detectar: panell Loki a Grafana amb filtre per contenidor=homeassistant.
- Com filtrar: nivell ERROR, periode temporal, text especific.
- Com correlacionar: comparar amb metricas de Prometheus al mateix temps.
- Com guardar la consulta: com a alerta o marcador.
