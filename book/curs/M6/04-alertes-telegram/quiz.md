# Qüestionari - Capitol 4: Alertes amb Telegram

> 10 preguntes · ~15 min

## Pregunta 1
Per que Telegram es una bona opcio per alertes de la RPi?

- [ ] Es la unica opcio gratuita
- [x] Es gratis, sempre el portem al movil, i te bots amb API senzilla
- [ ] Es obligatori per a servidors
- [ ] Es mes rapid que el correu electronic

## Pregunta 2
Quin servei s'encarrega d'enviar les alertes de Prometheus al canal de comunicacio?

- [ ] Grafana
- [ ] Node Exporter
- [x] Alertmanager
- [ ] cAdvisor

## Pregunta 3
Quina ordre cal donar a @BotFather per crear un bot?

- [ ] /start
- [ ] /create
- [x] /newbot
- [ ] /bot

## Pregunta 4
Quin parametre a una alerta de Prometheus evita falsos positius per pics puntuals?

- [ ] wait
- [x] for
- [ ] delay
- [ ] debounce

## Pregunta 5
Quin es el port per defecte d'Alertmanager?

- [ ] 9090
- [ ] 9093
- [x] 9093
- [ ] 3000

## Pregunta 6
Quin es l'estat d'una alerta quan la condicio es compleix pero encara no ha passat el temps minim?

- [ ] Firing
- [x] Pending
- [ ] Inactive
- [ ] Warning

## Pregunta 7
Que fan les "inhibit rules" a Alertmanager?

- [ ] Activen les alertes automaticament
- [x] Suprimeixen alertes menys importants quan n'hi ha una de mes critica activa
- [ ] Agrupa alertes per tema
- [ ] Eliminen les alertes repetides

## Pregunta 8
Quin camp de la regla Prometheus conte la durada minima d'una alerta?

- [ ] duration
- [x] for
- [ ] wait
- [ ] since

## Pregunta 9 (oberta)
Explica el cicle de vida d'una alerta a Prometheus passant per tots els estats possibles. Per que existeix l'estat "Pending"?

Pistes per respondre:
- Els estats son: Inactive, Pending, Firing, Resolved.
- Explica que pasa a cada un.
- Per que Pending es important: evita alertes per pics puntuals.

## Pregunta 10 (oberta)
Has de configurar alertes per al teu BernatLab. Escriu 5 regles d'alerta concretes (amb expr, for, labels i annotations) per a 5 problemes diferents que podries tenir.

Pistes per respondre:
- Pot ser: CPU alta, memoria baixa, disc ple, temperatura, contenidor caigut, RPi no respon, servei concret caigut.
- Cada regla ha de tenir una condicio clara i un temps minim.
- Pensa quines son les 5 coses que mes et preocupen.
