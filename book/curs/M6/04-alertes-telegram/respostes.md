# Respostes - Capitol 4: Alertes amb Telegram

> Mira les respostes DESPRES d'haver fet el qüestionari.

## Pregunta 1: Per que Telegram

**Resposta correcta**: Es gratis, sempre el portem al movil, i te bots amb API senzilla.

**Explicacio**: Telegram reuneix totes les condicions ideals: gratis, sense limits de missatges, API HTTP senzilla, suport natiu per Markdown, grups, i la gent normalment l'oberta tot el dia. L'email arriba al "Promotions" o "Spam" i no el mires. SMS costa diners. Slack/Discord cal configurar un workspace.

---

## Pregunta 2: Servei que envia alertes

**Resposta correcta**: Alertmanager.

**Explicacio**: Alertmanager es el "carter" de l'ecosistema Prometheus. Reb les alertes que Prometheus detecta, les agrupa per tematica, silencia, i envia al canal configurat (Telegram, email, etc.). Esta separat de Prometheus perque si Prometheus es reinicia, Alertmanager recorda l'estat de les alertes.

---

## Pregunta 3: Comanda a BotFather

**Resposta correcta**: /newbot.

**Explicacio**: `/newbot` es la comanda oficial de BotFather per crear un bot nou. Et demanara un nom i un username (que ha d'acabar en `bot`). Com a resposta et donara el token HTTP API que es la "contrasenya" que permet enviar missatges en nom d'aquell bot.

---

## Pregunta 4: Parametre per evitar falsos positius

**Resposta correcta**: `for`.

**Explicacio**: El camp `for: 5m` en una regla Prometheus vol dir que la condicio ha d'estar activa durant 5 minuts seguits abans de disparar l'alerta. Si passa nomes un moment, l'alerta queda en "Pending" pero mai passa a "Firing". Es la manera standard d'evitar falses alarmes per pics puntuals.

---

## Pregunta 5: Port d'Alertmanager

**Resposta correcta**: 9093.

**Explicacio**: 9093 es el port UI/API d'Alertmanager. Es similar al 9090 de Prometheus pero amb un +3. Es bo recordar-lo per configuracio de proxies i tallafocs.

---

## Pregunta 6: Estat quan la condicio es compleix pero no ha passat el temps

**Resposta correcta**: Pending.

**Explicacio**: "Pending" es l'estat transitori. La condicio s'ha complert pero encara no ha passat el `for:`. Si la condicio es deixa de complir abans del temps minim, torna a "Inactive" sense enviar res. Si passa del temps, passa a "Firing" i s'envia l'alerta.

---

## Pregunta 7: Inhibit rules

**Resposta correcta**: Suprimeixen alertes menys importants quan n'hi ha una de mes critica activa.

**Explicacio**: Si tens una alerta "critical" de RPi caigut, no cal que tambe rebis les "warning" de CPU alta, memoria baixa, etc. (tots son consequencia del mateix problema). Les inhibit_rules ho automatitzen: si hi ha una "critical" amb el mateix alertname+instance, les warning s'ignoren.

---

## Pregunta 8: Camp de durada minima

**Resposta correcta**: `for`.

**Explicacio**: El camp `for:` es la duracio minima que la condicio ha d'estar activa. Es la diferència entre "hi ha hagut un breu pic" i "realment hi ha un problema persistent". Com a regla general, posa 5-10 min per a problemes operacionals.

---

## Pregunta 9 (oberta): Cicle de vida d'una alerta

**Resposta model**:

Una alerta Prometheus passa per quatre estats al llarg del seu cicle de vida:

1. **Inactive** (Inactiva): l'estat inicial. La condicio NO es compleix. Per exemple, la CPU esta al 30% i el llindar es 80%. L'alerta simplement "existeix" pero no s'esta avaluant activament.

2. **Pending** (Pendent): la condicio HA COMENCAT a complir-se pero encara no ha passat el temps minim definit a `for:`. Per exemple, la CPU puja al 90% i el `for: 5m`. Durant aquests 5 minuts l'alerta esta en "Pending". Si la CPU baixa del 80% durant aquest temps, torna a "Inactive" sense passar a Firing. Si pasa dels 5 minuts, passa a "Firing".

3. **Firing** (Disparada): la condicio s'ha mantingut prou temps. Aleshores Prometheus envia l'alerta a Alertmanager, que l'envia al canal configurat (Telegram, email, etc.). Mentre la condicio continuï, l'alerta segueix en Firing i es re-envia segons el `repeat_interval` (per defecte cada 4 hores).

4. **Resolved** (Resoluda): la condicio ha deixat de complir-se. Per exemple, la CPU ha tornat al 40%. Aleshores s'envia un missatge de "Resolved" informant que el problema s'ha acabat. Despres torna a "Inactive".

L'estat **Pending** es important per varies raons:
- **Evita falses alarmes**: si nomes ha estat un pic de 30 segons, no t'espameges al movil a les 3 de la matinada.
- **Permet "auto-correccions"**: alguns problemes es resolen sols (un proces temporal que acaba, una pujada breu de CPU). Pending deixa temps perque passi.
- **Filtra soroll**: en un sistema sempre hi ha pics. Pending es el "filtre de soroll" que nomes dispara quan hi ha un problema REAL.
- **Permet ajustar `for`**: pots començar amb `for: 10m` i baixar a `for: 2m` si trobes que t'estas perdent coses.

---

## Pregunta 10 (oberta): 5 regles d'alerta concretes

**Resposta model**:

Aqui tens 5 regles d'alerta que posaria al BernatLab, amb expr, for, labels i annotations:

**1. RPi no respon (critica)**

```yaml
- alert: RPiDown
  expr: up{job="node"} == 0
  for: 1m
  labels:
    severity: critical
  annotations:
    summary: "RPi no respon"
    description: "Node Exporter no respon desde fa 1 minut. La RPi pot estar penjada o sense xarxa."
```

Per que: la RPi penjada es el pitjor escenari. 1 minut es prou per descartar un blip de xarxa pero no massa per adormir-te.

**2. Disc ple (critica)**

```yaml
- alert: DiscPle
  expr: (node_filesystem_avail_bytes{mountpoint="/"} / node_filesystem_size_bytes{mountpoint="/"}) * 100 < 10
  for: 10m
  labels:
    severity: critical
  annotations:
    summary: "Disc ple a {{ $labels.instance }}"
    description: "Nomes queden {{ $value }}% d'espai. Cal netejar logs o imatges Docker."
```

Per que: disc ple = serveis que cauen. 10 min per evitar falses alarmes per neteges temporals.

**3. Temperatura alta (warning)**

```yaml
- alert: TemperaturaAlta
  expr: node_thermal_zone_temp > 75
  for: 5m
  labels:
    severity: warning
  annotations:
    summary: "Temperatura alta"
    description: "CPU a {{ $value }} graus. Considera millorar la ventilacio o netejar la pols."
```

Per que: throttling a 80 graus. Avisa abans d'arribar-hi.

**4. Home Assistant caigut (critica)**

```yaml
- alert: HomeAssistantDown
  expr: probe_http_status_code{instance="http://homeassistant:8123"} != 200
  for: 3m
  labels:
    severity: critical
  annotations:
    summary: "Home Assistant no respon"
    description: "El dashboard d'HA no carrega. La teva llar automatitzada pot estar afectada."
```

Per que: HA es el cervell de la casa automatitzada. Si cau, tot pot fallar. 3 min per descartar reinicis.

**5. Contenidor amb fuites de memoria (warning)**

```yaml
- alert: ContenidorMemoryLeak
  expr: container_memory_usage_bytes{name=~".+"} > 500000000
  for: 30m
  labels:
    severity: warning
  annotations:
    summary: "{{ $labels.name }} usant mes de 500 MB"
    description: "El contenidor {{ $labels.name }} te {{ $value | humanize }}B de memoria. Possible fuita."
```

Per que: fuites de memoria son un problema classic. 30 min perque alguns serveis tenen pics normals al arrancar.

Si en tens mes, podries afegir:
- Latencia alta al proxy invers nginx.
- Certificat SSL a punt de caducar.
- Backup no realitzat en les ultimes 24h.
- Watchdog heartbeat (un missatge cada 24h per confirmar que el sistema de monitoritzacio funciona - si NO el reps, alguna cosa va malament).

---

## Que fer si has fallat moltes preguntes

- **5-8 encerts**: Rellegir el resum i fer l'exercici practic.
- **3-4 encerts**: Refes l'exercici desde zero observant cada pas.
- **0-2 encerts**: Repassem junts el capitol abans de continuar.

## Que fer si has encertat totes

- Passa al **Capitol 5** (Logs centralitzats).
- Investiga les alertes silencia des (silences) per quan estas treballant.
- Mira com integrar Mattermost o Ntfy com a alternatives a Telegram.
