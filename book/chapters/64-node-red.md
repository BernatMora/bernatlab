# Capítol 64 — Node-RED: les primeres automatitzacions

> *"Node-RED és un llenguatge visual. En lloc d'escriure codi, arrossegues caixes. Per a automatitzacions de l'hort, és perfecte."*

## 64.1 Què aprendràs

- Què és Node-RED i per què serveix.
- Com instal·lar Node-RED amb Docker.
- Com fer el teu primer flow.
- Com escoltar MQTT des de Node-RED.
- Com publicar a MQTT des de Node-RED.
- Com fer una automatització condicional real.
- Com desar els teus flows.

## 64.2 Durada estimada

1-1.5 hores.

## 64.3 Què és Node-RED

**Node-RED** és una eina de programació visual, basada en Node.js, creada per IBM. És com Scratch, però per a IoT.

Pensa en ell com un "IFTTT professional":

- Rep esdeveniments d'un costat (MQTT, HTTP, temporitzador...).
- Hi aplica una lògica (if/else, transformacions...).
- Fa alguna cosa (publicar a MQTT, enviar un correu, encendre un relé...).

Tot arrossegant caixes. **Sense escriure una línia de codi** (tot i que pots fer-ho si vols).

Exemples d'ús:

- Si la temperatura de l'hort baixa de 5°C, encén una estufa.
- Si el nivell d'humitat baixa del 30%, rega.
- Si el node LoRa no ha enviat dades en 1 hora, avisa per Telegram.
- Cada dia a les 20h, envia un resum a Telegram.

Node-RED és **l'eina perfecta** per a automatitzacions de l'hort.

## 64.4 Instal·lació

Crea `~/homelab/compose/node-red.yml`:

```yaml
version: "3.8"

services:
  node-red:
    image: nodered/node-red:latest
    container_name: node-red
    restart: unless-stopped
    ports:
      - "1880:1880"
    volumes:
      - ./data/node-red:/data
    environment:
      - TZ=Europe/Madrid
    depends_on:
      - mosquitto
```

Engega:

```bash
cd ~/homelab/compose
docker compose -f node-red.yml up -d
```

Obre `http://hortosona:1880` al navegador. Hauries de veure l'editor visual.

## 64.5 Interfície de Node-RED

A la part esquerra tens la **paleta de nodes**, organitzats per categories:

- **input**: nodes que reben dades (MQTT, HTTP, timer, inject...).
- **output**: nodes que envien dades (MQTT, HTTP, email, file...).
- **function**: nodes per fer lògica (if/else, switch, change, function...).
- **social**: nodes per a serveis externs (Telegram, Twitter, email...).
- **storage**: nodes per emmagatzematge (SQL, InfluxDB...).

Al centre tens el **flow**, on arrossegues els nodes.

A la dreta tens la **informació del node** i el **debug**.

## 64.6 El primer flow: "Hello, world!"

Arrossega un node `inject` al flow.

1. Configura'l: posa'l una mica a la dreta, fes doble clic, i tria "Time stamp" com a payload.
2. Arrossega un node `debug`.
3. Connecta'ls: arrossega des del cercle gris de la dreta del `inject` fins al cercle gris de l'esquerra del `debug`.
4. Fes clic al botó blau **Deploy** (a dalt a la dreta).
5. Fes clic al botó quadrat blau a la dreta del node `inject` (per activar-lo).

A la dreta, a la pestanya **debug**, hauries de veure l'hora actual.

Això és el teu primer flow. Simplement injecta un valor (l'hora) i l'envia a debug. Ara complica-ho.

## 64.7 Escoltar dades MQTT

Arrossega un node `mqtt in` (a la categoria "network"):

- Fes doble clic.
- **Server**: clic a la icona del llapis per afegir un servidor nou.
  - **Name**: BernatLab MQTT
  - **Server**: `mosquitto` (o `hortosona`)
  - **Port**: 1883
  - **Security**: activa username/password i posa les credencials de Mosquitto.
- **Action**: "Subscribe to topic"
- **Topic**: `sensors/#`
- **QoS**: 0

Connecta'l a un node `debug` (canvia el node debug a "complete msg object" per veure tot).

Deploy. Ara cada cop que algú publiqui a `sensors/...`, ho veuràs al debug.

Si tens dades a MQTT, ja les veuràs aquí.

## 64.8 Publicar a MQTT

Per publicar:

- Arrossega un node `mqtt out`.
- Configura'l igual que el `mqtt in` (mateix servidor, mateixa autenticació).
- **Action**: "Publish to topic".
- **Topic**: `bernatlab/test/hola`.

Per enviar un missatge, connecta'l a algun node d'input (per exemple, un `inject` amb payload "Hola des de Node-RED").

## 64.9 La primera automatització: alerta per temperatura baixa

Farem un flow que:

1. Escolta `sensors/hort1/temperatura`.
2. Si el valor és < 5°C, publica una alerta a `alerts/critical/hort`.
3. Si no, no fa res.

Passos:

1. Arrossega un `mqtt in` configurat com abans, subscrit a `sensors/hort1/temperatura`.
2. Arrossega un node `function` i posa-hi:

```javascript
// El payload arriba com a string JSON
const msg = JSON.parse(msg.payload);
const temperatura = msg.value;

if (temperatura < 5) {
    msg.payload = {
        node: msg.node,
        sensor: msg.sensor,
        value: temperatura,
        message: "Risc de gelada!",
    };
    return msg;
}

// No enviem res si no és una alerta
return null;
```

3. Arrossega un `mqtt out` configurat per publicar a `alerts/critical/hort`.
4. Connecta'ls en cadena: mqtt in → function → mqtt out.
5. Deploy.

Prova publicant una temperatura baixa:

```bash
mosquitto_pub -h hortosona -p 1883 -u bernat -P 'contrasenya' \
    -t 'sensors/hort1/temperatura' \
    -m '{"node":"hort1","sensor":"temperatura","value":2.3,"unit":"C"}'
```

Mira els logs de Mosquitto o subscriu-te a `alerts/#` per veure l'alerta.

## 64.10 La segona automatització: regar si la humitat baixa

Aquest és el cas clàssic de l'hort:

1. Escolta `sensors/hort1/humitat` periòdicament.
2. Si humitat < 30%, publica una ordre a `bernatlab/reg/on` durant 5 minuts.
3. Envia una alerta per Telegram.

Això ja és més complex. Ho fem pas a pas.

**Part 1: escoltar la humitat**

Node `mqtt in` a `sensors/hort1/humitat`.

**Part 2: comparar amb el llindar**

Node `function`:

```javascript
const data = JSON.parse(msg.payload);
const humitat = data.value;
const node = data.node;

if (humitat < 30) {
    msg.payload = {
        node: node,
        humitat: humitat,
        action: "regar",
        duration: 300, // 5 minuts en segons
    };
    return msg;
}
return null;
```

**Part 3: enviar ordre al sistema de reg**

Aquí hem de decidir com és el sistema de reg. En el M3 parlàvem d'un node LoRa amb relés. Per ara, simulem:

Node `mqtt out` a `bernatlab/reg/hort1/on` amb el payload generat.

**Part 4: alerta per Telegram**

Aquí veurem al **Cap 66** com configurar el bot de Telegram. Per ara, podem posar un node `debug` per veure què passaria.

## 64.11 Com desar els flows

Els flows es desen automàticament quan fas Deploy. Però hi ha més:

- **Exportar**: pots exportar un flow com a JSON (menú → Export).
- **Importar**: pots importar un flow d'un altre (menú → Import).
- **Subversion**: els flows estan a `./data/node-red/flows.json`. Pots versionar aquest fitxer a Git.

Jo recomano **versionar el `flows.json`** al repo del BernatLab. Així tens un historial de canvis i pots recuperar fàcilment.

## 64.12 La paleta de nodes

A mesura que necessitis més coses, pots afegir nodes nous. Node-RED té un sistema de "palette manager":

1. Menú → **Manage palette**.
2. **Install**.
3. Busca el node que vulguis.

Alguns nodes útils per a l'hort:

- `node-red-node-ui-table`: per visualitzar dades en taules.
- `node-red-dashboard`: per crear un panell web per a l'hort.
- `node-red-contrib-modbus`: per comunicar amb dispositius Modbus.
- `node-red-contrib-influxdb`: per escriure directament a InfluxDB des de Node-RED.

## 64.13 Què ve després

Node-RED és la peça que fa servir **totes les altres**. Al **Cap 65** afegirem un **node LoRa** real al camp, que publicarà dades a MQTT, i les veuràs a Grafana gràcies a aquesta cadena.

## 64.14 Errors habituals

**Error 1: "Connection refused" a MQTT**.

Comprova que el servidor, port, usuari i contrasenya són correctes.

**Error 2: el flow no es desplega**.

Mira l'error a la consola (a sota). Sovint és un node mal configurat o un JSON invàlid al node `function`.

**Error 3: la funció no retorna res**.

Si la funció retorna `null` o no retorna, el flow s'atura. Assegura't que el flux té un camí per a tots els casos.

**Error 4: les dades no es reben**.

Comprova que el topic MQTT és correcte. Un `sensors/#` rep `sensors/hort1/temperatura`, però un `sensors/hort1/#` no rep `sensors/hort2/temperatura`.

## 64.15 Resum

Node-RED és la cola del BernatLab. Aquí és on la lògica esdevé visual i intuïtiva. Hem vist:

- Instal·lació amb Compose.
- Interfície i paleta de nodes.
- Com escoltar i publicar a MQTT.
- Com fer una funció que filtra i transforma missatges.
- Com fer una automatització condicional.

Al **Cap 65** afegirem un node LoRa al camp, que serà el primer consumidor real d'aquesta cadena.

## 64.16 Exercicis pràctics

1. Instal·la Node-RED.
2. Fes el "Hello, world!" amb un `inject` i un `debug`.
3. Connecta't a Mosquitto des de Node-RED.
4. Publica una temperatura i rep-la a Node-RED.
5. Fes una funció que filtri temperatures < 5°C.
6. Fes una automatització que publiqui una alerta a `alerts/#` quan la humitat < 30%.
7. Exporta el teu flow a JSON i guarda'l al repo.
8. Documenta els flows al `homelab/setup-log.md`.
