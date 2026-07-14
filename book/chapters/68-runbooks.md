# Capítol 68 — Runbooks: quan falla alguna cosa

> *"Un runbook és la diferència entre resoldre un incident en 5 minuts o en 5 hores."*

## 68.1 Què aprendràs

- Què és un runbook i quan usar-lo.
- Com estructurar un runbook.
- Com escriure els teus primers 3 runbooks.
- On desar-los.
- Com millorar-los amb el temps.

## 68.2 Durada estimada

30-45 minuts.

## 68.3 Per què runbooks

Ara tens un sistema amb molts components: Docker, Portainer, Uptime Kuma, MQTT, InfluxDB, Grafana, Node-RED, Telegram, Prometheus, Alertmanager, node LoRa. Si un falla, has de saber què fer.

Sense un runbook:

- Tens memòria (que falla).
- Has de cercar a Internet cada vegada.
- El pànic et porta a cometre errors.

Amb un runbook:

- Tens les passes exactes.
- Les executes sense pensar.
- El temps de resolució baixa.

Un runbook **es crea quan resols un incident**, no pas abans. Ara tens un sistema relativament estable — bona oportunitat per escriure els primers.

## 68.4 Estructura d'un runbook

```markdown
# Runbook: [Títol del problema]

## Símptomes
- Què veus.

## Diagnòstic
1. Comandes per confirmar.

## Solució
1. Passes per resoldre.

## Verificació
- Com saber que s'ha resolt.

## Prevenció
- Com evitar-ho en el futur.

## Contactes
- Qui avisar.

## Última actualització
- Data i canvis.
```

## 68.5 On desar els runbooks

A la teva estructura:

```
homelab/
└── runbooks/
    ├── README.md          # índex
    ├── 001-portainer-down.md
    ├── 002-grafana-no-data.md
    ├── 003-lora-offline.md
    └── ...
```

Crea la carpeta:

```bash
mkdir -p ~/homelab/runbooks
```

Crea un `README.md` índex:

```markdown
# Runbooks del BernatLab

## Incidents
- [001](001-portainer-down.md) — Portainer no respon
- [002](002-grafana-no-data.md) — Grafana no mostra dades
- [003](003-lora-offline.md) — Node LoRa offline
- [004](004-mqtt-disconnected.md) — Mosquitto no accepta connexions

## Manteniment
- [101](101-update-containers.md) — Actualitzar contenidors
- [102](102-rotate-secrets.md) — Rotar secrets

## Recuperació
- [201](201-restore-raspberry.md) — Restaurar Raspberry
- [202](202-data-loss.md) — Pèrdua de dades
```

Versiona aquesta carpeta a Git. Així tens historial de canvis.

## 68.6 Runbook 001: Portainer no respon

Crea `~/homelab/runbooks/001-portainer-down.md`:

```markdown
# Runbook 001: Portainer no respon

## Símptomes
- El navegador no pot connectar a `https://hortosona:9443`.
- Altres serveis funcionen normalment.

## Diagnòstic

1. Comprova l'estat del contenidor:
   ```bash
   docker ps | grep portainer
   ```

2. Si el contenidor està aturat, mira els logs:
   ```bash
   docker logs portainer --tail 100
   ```

3. Si està en marxa, comprova el port:
   ```bash
   ss -tulnp | grep 9443
   ```

## Solució

**Si el contenidor està aturat:**

1. Reiniciar:
   ```bash
   docker start portainer
   ```

2. Esperar 30 segons.

3. Comprovar:
   ```bash
   curl -k https://localhost:9443
   ```

**Si el contenidor està en marxa però no respon:**

1. Reiniciar:
   ```bash
   docker restart portainer
   ```

2. Si continua, mirar logs per errors:
   ```bash
   docker logs portainer --tail 200
   ```

3. Si hi ha error de base de dades:
   ```bash
   docker stop portainer
   cp -r ~/homelab/compose/data/portainer.bak/* \
       ~/homelab/compose/data/portainer/
   docker start portainer
   ```

## Verificació

- `curl -k https://localhost:9443` retorna algun HTTP status.
- El navegador pot connectar i fer login.

## Prevenció

- Mantenir espai en disc (Portainer necessita 1 GB lliure).
- Comprovar memòria disponible (mínim 256 MB).
- Configurar `restart: unless-stopped` (ja ho tens al compose).

## Contactes

- @bernat a Telegram

## Última actualització
- 2026-07-09 per Bernat
```

## 68.7 Runbook 002: Grafana no mostra dades

```markdown
# Runbook 002: Grafana no mostra dades noves

## Símptomes
- Les gràfiques estan buides o no s'actualitzen.
- Les dades antigues es veuen, les noves no.

## Diagnòstic

1. Comprovar que InfluxDB rep dades:
   ```bash
   docker exec influxdb influx query 'from(bucket:"hort") |> range(start:-10m)'
   ```

2. Si no hi ha dades, comprovar Telegraf:
   ```bash
   docker logs telegraf --tail 50
   ```

3. Si Telegraf no es connecta, comprovar Mosquitto:
   ```bash
   mosquitto_sub -h localhost -p 1883 -u bernat -P 'contrasenya' -t 'sensors/#' -v
   ```

## Solució

**Si Mosquitto no funciona:**

1. Reiniciar:
   ```bash
   docker restart mosquitto
   ```

2. Esperar 30 segons.

3. Provar de nou amb `mosquitto_sub`.

**Si Telegraf no es connecta:**

1. Reiniciar:
   ```bash
   docker restart telegraf
   ```

2. Esperar 30 segons.

3. Comprovar logs:
   ```bash
   docker logs telegraf --tail 50
   ```

**Si Grafana no es connecta a InfluxDB:**

1. Anar a Grafana → Connections → Data sources.
2. Editar el data source InfluxDB.
3. Verificar URL, token, org, bucket.
4. Save & test.

## Verificació

- Publicar una temperatura de prova a `sensors/hort1/temperatura`.
- Esperar 1 minut.
- La gràfica de Grafana ha de mostrar el punt.

## Prevenció

- Monitorar els serveis amb Uptime Kuma.
- Configurar alertes a Prometheus per "no data".
- Revisar logs periòdicament.

## Contactes

- @bernat a Telegram

## Última actualització
- 2026-07-09 per Bernat
```

## 68.8 Runbook 003: Node LoRa offline

```markdown
# Runbook 003: Node LoRa no envia dades

## Símptomes
- El node hauria d'enviar dades cada 5-15 minuts.
- Fa més d'1 hora que no apareixen dades noves a Grafana.
- Alerta de Prometheus o Uptime Kuma.

## Diagnòstic

1. Comprovar que el node té bateria (si té placa solar, comprovar-la).
2. Si tens accés físic, mirar el LED d'estat.
3. Publicar un missatge manual a MQTT per verificar la cadena:
   ```bash
   mosquitto_pub -h hortosona -p 1883 -u bernat -P 'contrasenya' \
       -t 'sensors/hort1/temperatura' \
       -m '{"node":"hort1","sensor":"temperatura","value":99.9,"unit":"C"}'
   ```

4. Si el missatge arriba a Grafana, el problema és del node, no del servidor.

## Solució

**Si és un node amb bateria:**

1. Anar al camp.
2. Obrir la caixa.
3. Comprovar la bateria.
4. Si cal, substituir-la o recarregar-la.
5. Reiniciar el node (desendollar i tornar a endollar).

**Si és un node amb placa solar:**

1. Comprovar que la placa està neta.
2. Comprovar que la bateria es carrega.
3. Mirar si la placa té ombra (arbres nous?).

**Si el node sembla correcte però no envia:**

1. Comprovar la cobertura LoRa.
2. Verificar que el gateway està en marxa.
3. Reiniciar el node i el gateway.

## Verificació

- Esperar 15-30 minuts.
- Hauries de veure dades noves a Grafana.

## Prevenció

- Usar bateries de més capacitat.
- Afegir un panell solar més gran.
- Configurar deep sleep agressiu.
- Posar el node en un lloc amb bona cobertura.

## Contactes

- @bernat a Telegram

## Última actualització
- 2026-07-09 per Bernat
```

## 68.9 Com millorar els runbooks

Cada vegada que resols un incident:

1. Escriu el runbook si no existeix.
2. Actualitza'l si existeix.
3. Prova'l la propera vegada.
4. Comparteix-lo si pot ajudar algú.

Al cap d'un any, tindràs 10-20 runbooks que cobreixen el 90% dels incidents habituals. Això et permetrà respondre ràpidament sense pensar.

## 68.10 Com provar els runbooks

Cada trimestre, dedica una hora a:

1. Tria un runbook.
2. Llegeix-lo.
3. Executa'l en un entorn de test (no en producció).
4. Comprova que funciona.
5. Corregeix el que no.

Això t'assegura que els runbooks estan al dia.

## 68.11 Què ve després

Ja tens runbooks. Al **Cap 69** farem el **DRP** (Disaster Recovery Plan) amb un test real: simular una fallada total i restaurar des de zero.

## 68.12 Errors habituals

**Error 1: runbooks massa genèrics**.

"No facis res" no és un runbook. Ha de tenir comandes específiques.

**Error 2: runbooks desactualitzats**.

Si canvies el sistema, els runbooks queden obsolets. Revisa'ls cada mes.

**Error 3: runbooks que ningú llegeix**.

Guarda'ls a un lloc accessible. Referencia'ls a les alertes.

**Error 4: no provar els runbooks**.

Si no els has provat, no saps si funcionen.

## 68.13 Resum

Els runbooks et fan estalviar temps i estrès. Hem vist:

- Què és un runbook.
- Com estructurar-lo.
- Tres runbooks d'exemple (Portainer, Grafana, LoRa).
- On desar-los.
- Com millorar-los.

## 68.14 Exercicis pràctics

1. Crea la carpeta `~/homelab/runbooks/`.
2. Escriu 3 runbooks basats en els 3 exemples d'aquest capítol.
3. Adaptals al teu sistema (canviar noms, paths, etc.).
4. Crea un `README.md` índex.
5. Versionals a Git.
6. Prova un runbook amb una situació simulada.
