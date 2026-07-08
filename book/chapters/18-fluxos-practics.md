# Capítol 18 — Fluxos pràctics

> *"La diferència entre un prototip i un sistema en producció és, sovint, un bon flux de Node-RED."*

## 18.1 Què aprendrem

En aquest capítol construirem, pas a pas, **fluxos reals** que posen en pràctica tot el que hem après fins ara. Cada flux és una peça autònoma que podem integrar al BernatLab:

1. **Netejar dades**: convertir payloads, validar valors, descartar lectures impossibles.
2. **Detectar gelades**: alerta immediata quan la temperatura baixa de 2 °C.
3. **Detectar sòl sec**: alerta quan la humitat del sòl baixa del 30 %.
4. **Mitjana mòbil**: suavitzar lectures sorolloses amb una mitjana de les últimes N lectures.
5. **Controlar el reg**: activar una vàlvula de reg quan la humitat del sòl és baixa.
6. **Monitorar sensors inactius**: detectar sensors que no han publicat en X minuts.
7. **Publicar resums periòdics**: cada hora, enviar un resum a Telegram.

Cada flux ve amb:

- Descripció del problema que resol.
- Esquema visual (descripció dels nodes i les connexions).
- Codi dels nodes `function`.
- Configuració dels nodes MQTT i InfluxDB.
- Consideracions i extensions.

Comencem.

## 18.2 Flux 1: netejar i validar dades

### Problema

Els sensors publiquen lectures que poden tenir errors: temperatures impossibles (200 °C, -100 °C), humitats fora de rang (> 100 %, < 0 %), valors NaN, etc. Volem netejar aquestes dades abans d'escriure-les a InfluxDB.

### Solució

Un flux que:

1. Es subscriu a tots els topics de mesura.
2. Parseja el payload.
3. Valida els valors segons el tipus.
4. Si el valor és vàlid, l'envia a Telegraf (perquè l'escrigui a InfluxDB).
5. Si no, l'envia a debug i a un log d'errors.

### Implementació

Nodes necessaris:

- `mqtt in`: subscriu a `hort/+/+/+`.
- `function`: valida i neteja.
- `mqtt out`: re-publica a un topic "net".
- `debug`: per veure els rebutjos.

Codi del node `function`:

```javascript
// Validar i netejar el missatge
const msgOriginal = msg;

// Rang vàlid segons el tipus
const limits = {
    'graus_C': [-20, 50],
    '%': [0, 100],
    'hPa': [800, 1100],
    'lux': [0, 200000]
};

try {
    const payload = typeof msg.payload === 'string' 
        ? JSON.parse(msg.payload) 
        : msg.payload;
    
    const valor = payload.valor;
    const unitat = payload.unitat;
    
    // Validar
    if (typeof valor !== 'number' || isNaN(valor)) {
        node.warn("Valor no numèric: " + JSON.stringify(payload));
        return null;
    }
    
    if (!limits[unitat]) {
        node.warn("Unitat desconeguda: " + unitat);
        return null;
    }
    
    const [min, max] = limits[unitat];
    if (valor < min || valor > max) {
        node.warn(`Valor fora de rang: ${valor} ${unitat}`);
        return null;
    }
    
    // Re-publicar a un topic net
    msg.payload = payload;
    msg.topic = msg.topic + '/net';
    return msg;
    
} catch (e) {
    node.error("Error parsejant: " + e.message);
    return null;
}
```

Aquest codi:

- Parseja el payload JSON.
- Comprova que el valor sigui un número.
- Comprova que l'unitat sigui coneguda.
- Comprova que el valor estigui dins del rang esperat.
- Si tot és correcte, retorna el missatge. Si no, retorna `null` (descarta).

Una millora: usar un node `rbe` (Report By Exception) o `delay` per evitar que el mateix valor es publiqui massa sovint.

## 18.3 Flux 2: alerta de gelada

### Problema

A l'Hort Osona hi ha plantes sensibles a les gelades (tomàquets, pebrots, albergínies). Si la temperatura baixa de 2 °C a la nit, volem rebre un missatge immediat a Telegram per poder actuar (cobrir les plantes, regar per crear una capa de gel protectora, etc.).

### Solució

Un flux que:

1. Es subscriu a `hort/+/temperatura/aire`.
2. Comprova si la temperatura és inferior a 2 °C.
3. Si sí, envia un missatge a Telegram.
4. Per evitar spam, només envia una alerta cada 30 minuts com a mínim.

### Implementació

Nodes:

- `mqtt in`: subscriu a `hort/+/temperatura/aire`.
- `function`: comprova la temperatura.
- `telegram sender`: envia el missatge.
- `delay`: limita la freqüència d'alertes.

Codi del node `function`:

```javascript
const payload = typeof msg.payload === 'string' 
    ? JSON.parse(msg.payload) 
    : msg.payload;

const valor = payload.valor;
const zona = msg.topic.split('/')[1];

if (valor < 2) {
    msg.payload = `⚠️ ALERTA GELADA\n\nZona: ${zona}\nTemperatura: ${valor}°C\nHora: ${new Date().toISOString()}`;
    return msg;
}

return null;
```

Aquest codi:

- Parseja el payload.
- Extreu la zona del topic.
- Si la temperatura és < 2 °C, construeix un missatge d'alerta.
- Retorna el missatge; si no, retorna `null`.

Configuració del node `telegram sender`:

- **Bot**: el bot que hem configurat a Uptime Kuma o un de nou.
- **Chat ID**: el nostre chat ID.
- **Message**: `{{payload}}` (que serà el missatge del node function).

Per evitar spam, afegim un node `delay` configurat a 30 minuts entre missatges.

## 18.4 Flux 3: alerta de sòl sec

### Problema

Si la humitat del sòl baixa del 30 %, les plantes poden patir estrès hídric. Volem rebre un avís.

### Solució

Similar al flux de gelada, però amb el llindar del 30 % i el topic `hort/+/humitat/sol`.

Codi del node `function`:

```javascript
const payload = typeof msg.payload === 'string' 
    ? JSON.parse(msg.payload) 
    : msg.payload;

const valor = payload.valor;
const zona = msg.topic.split('/')[1];

if (valor < 30) {
    msg.payload = `🌱 ALERTA SÒL SEC\n\nZona: ${zona}\nHumitat: ${valor}%\nHora: ${new Date().toISOString()}`;
    return msg;
}

return null;
```

## 18.5 Flux 4: mitjana mòbil

### Problema

Alguns sensors (sobretot els barats) tenen soroll: la temperatura pot oscil·lar ±1 °C entre lectures consecutives. Volem una mitjana mòbil de les últimes 10 lectures per suavitzar el senyal.

### Solució

Un flux que:

1. Es subscriu a `hort/+/temperatura/aire`.
2. Desa les últimes 10 lectures en memòria (context).
3. Calcula la mitjana.
4. Publica el valor suavitzat a un nou topic `hort/+/temperatura/aire/suavitzat`.

### Implementació

Codi del node `function`:

```javascript
const zona = msg.topic.split('/')[1];
const clau = `historial_${zona}`;

let historial = context.get(clau) || [];
const nouValor = (typeof msg.payload === 'string' 
    ? JSON.parse(msg.payload) 
    : msg.payload).valor;

historial.push(nouValor);
if (historial.length > 10) {
    historial.shift();
}

context.set(clau, historial);

const mitjana = historial.reduce((a, b) => a + b, 0) / historial.length;

msg.payload = JSON.stringify({
    valor: Math.round(mitjana * 100) / 100,
    unitat: "graus_C"
});
msg.topic = `hort/${zona}/temperatura/aire/suavitzat`;

return msg;
```

Aquest codi:

- Manté un historial de les últimes 10 lectures per zona.
- Calcula la mitjana.
- Publica el resultat a un nou topic.

Ara Telegraf (si ho configurem adequadament) pot subscriure's a aquest topic i guardar la versió suavitzada, o podem consultar InfluxDB directament.

## 18.6 Flux 5: vàlvula de reg (control d'actuadors)

### Problema

Quan la humitat del sòl baixa del 30 %, volem obrir una vàlvula de reg durant 5 minuts, i després tancar-la automàticament.

### Solució

Un flux que:

1. Es subscriu a `hort/+/humitat/sol`.
2. Comprova si la humitat és < 30 % i si la vàlvula està tancada.
3. Publica una comanda `ON` a `hort/control/reg`.
4. Espera 5 minuts.
5. Publica una comanda `OFF` al mateix topic.

### Implementació

Codi del node `function` (lectura):

```javascript
const payload = typeof msg.payload === 'string' 
    ? JSON.parse(msg.payload) 
    : msg.payload;

const valor = payload.valor;
const zona = msg.topic.split('/')[1];

// Comprovar l'estat actual de la vàlvula
const clauEstat = `valvula_${zona}`;
const estat = context.get(clauEstat) || 'OFF';

if (valor < 30 && estat === 'OFF') {
    context.set(clauEstat, 'ON');
    
    // Enviar comanda ON
    msg.payload = 'ON';
    msg.topic = `hort/control/reg/${zona}`;
    msg.accion = 'ON';
    return msg;
}

return null;
```

Codi del node `function` (tancament després de 5 min):

```javascript
// Aquest node s'activa quan arriba el missatge
const clauEstat = `valvula_${msg.zona}`;
context.set(clauEstat, 'OFF');

msg.payload = 'OFF';
msg.topic = msg.topic.split('/').slice(0, -1).join('/');
return msg;
```

Aquest és un exemple simplificat. En un sistema real, caldria considerar:

- **Confirmació de la vàlvula**: un node MQTT que es subscriu a `hort/control/reg/status` per saber si la vàlvula s'ha obert realment.
- **Mecanismes de seguretat**: no regar massa, no regar si plou, etc.
- **Horaris**: només regar durant el dia, no a la nit.

Al BernatLab, podem implementar la vàlvula amb un actuador Sonoff, Shelly, o similar, controlat per MQTT. Però la implementació física la veurem al Mòdul 3.

## 18.7 Flux 6: monitorar sensors inactius

### Problema

Si un sensor deixa de publicar (bateria esgotada, pèrdua de Wi-Fi, avaria), volem saber-ho. Podríem fer pings al sensor, però és més eficient mirar l'última vegada que ha publicat.

### Solució

Un flux que:

1. Cada 5 minuts, comprova l'última publicació de cada sensor.
2. Si l'última publicació és de fa més de 10 minuts, envia una alerta.

### Implementació

Nodes:

- `inject`: dispara cada 5 minuts.
- `influxdb in`: consulta l'última publicació per zona.
- `function`: comprova si ha passat massa temps.
- `telegram sender`: envia l'alerta.

Consulta InfluxDB:

```flux
from(bucket: "hort-osona")
  |> range(start: -1h)
  |> filter(fn: (r) => r._measurement == "temperatura")
  |> group(columns: ["zona"])
  |> last()
  |> keep(columns: ["_time", "zona", "_value"])
```

Codi del node `function`:

```javascript
const ara = new Date();
const limitMinuts = 10;

for (const lectura of msg.payload) {
    const ultima = new Date(lectura._time);
    const minuts = (ara - ultima) / 1000 / 60;
    
    if (minuts > limitMinuts) {
        msg.payload = `🔴 SENSOR INACTIU\n\nZona: ${lectura.zona}\nÚltima lectura: ${ultima.toISOString()}\nFa ${Math.round(minuts)} minuts.`;
        return msg;
    }
}

return null;
```

Aquest flux ens avisa quan un sensor porta més de 10 minuts sense publicar.

## 18.8 Flux 7: resum diari a Telegram

### Problema

Cada matí, volem un resum de les condicions de l'hort: temperatura mitjana, humitat mitjana, anomalies detectades.

### Solució

Un flux que:

1. Es dispara cada dia a les 8:00.
2. Consulta InfluxDB per obtenir estadístiques del dia anterior.
3. Construeix un missatge amb el resum.
4. L'envia a Telegram.

### Implementació

Nodes:

- `inject`: dispara a les 8:00 cada dia.
- `influxdb in` (múltiples): consultes per a temperatura, humitat, etc.
- `function`: construeix el resum.
- `telegram sender`: envia el missatge.

Codi del node `function`:

```javascript
// Suposem que rebem múltiples consultes en una sola msg
// Cada msg.payload conté un array de resultats

const resum = {
    temperatura: null,
    humitat: null,
    anomalies: []
};

for (const item of msg.payload) {
    if (item._measurement === 'temperatura') {
        resum.temperatura = {
            mitjana: item.mitjana,
            maxim: item.maxim,
            minim: item.minim
        };
    }
    if (item._measurement === 'humitat') {
        resum.humitat = {
            mitjana: item.mitjana,
            maxim: item.maxim,
            minim: item.minim
        };
    }
}

let text = `🌅 RESUM DIARI HORT OSONA\n\n`;
text += `🌡️ Temperatura: ${resum.temperatura?.mitjana?.toFixed(1)}°C (max ${resum.temperatura?.maxim?.toFixed(1)}, min ${resum.temperatura?.minim?.toFixed(1)})\n`;
text += `💧 Humitat: ${resum.humitat?.mitjana?.toFixed(1)}% (max ${resum.humitat?.maxim?.toFixed(1)}, min ${resum.humitat?.minim?.toFixed(1)})\n`;

if (resum.anomalies.length > 0) {
    text += `\n⚠️ Anomalies:\n` + resum.anomalies.join('\n');
}

msg.payload = text;
return msg;
```

Aquest flux ens permet començar el dia amb una visió general de l'estat de l'hort.

## 18.9 Patrons avançats

### Patró: confirmació d'acció

Quan publiquem una comanda a un actuador, volem saber si s'ha executat. Patró:

1. Publicar comanda a `hort/control/actuador`.
2. Subscriure's a `hort/control/actuador/status`.
3. Si rebem confirmació dins de X segons, tot bé.
4. Si no, alerta.

### Patró: debounce

Per evitar alertes duplicades per un sol esdeveniment, podem usar un node `delay` o un node `rbe` (Report By Exception).

Per exemple, si la temperatura baixa de 2 °C durant 5 minuts consecutius, no volem 5 alertes. Volem 1 alerta al principi, i 1 altra quan es recuperi.

### Patró: dead letter

Quan un flux llença un error, podem capturar-lo amb un node `catch` i enviar-lo a un topic d'errors. Per exemple, `bernatlab/errors`. Això ens permet tenir un log centralitzat d'errors.

### Patró: heartbeat

Cada N minuts, publiquem un missatge a `bernatlab/heartbeat`. Si Uptime Kuma o un altre sistema detecta que aquest heartbeat ha parat, sabem que Node-RED té problemes.

## 18.10 Subflows: components reutilitzables

Si tenim un patró que es repeteix, podem crear un **subflow** (subflux) que encapsuli la lògica. Per exemple, un subflow "Alerta si valor < llindar" podria rebre dos paràmetres (llindar, missatge) i aplicar la lògica de detecció i enviament.

Per crear un subflow:

1. Seleccionem els nodes que volem encapsular.
2. Anem a **Subflows → Create subflow from selection**.
3. Definim els paràmetres d'entrada.
4. Usem el subflow com si fos un node més.

## 18.11 Debug avançat

Per depurar fluxos complexos, podem usar:

- **Node `debug` amb `complete msg object`**: mostra tots els camps del missatge, no només el payload.
- **Node `catch`**: captura errors i els envia a un node de log.
- **Node `status`**: mostra canvis d'estat dels nodes (per exemple, quan un MQTT broker es connecta o desconnecta).

Exemple de configuració de debug:

```json
{
  "active": true,
  "tosidebar": true,
  "console": false,
  "complete": "true",
  "targetType": "msg",
  "statusVal": "",
  "statusType": "auto"
}
```

Això mostra el missatge complet a la pestanya debug, sense imprimir-lo a la consola.

## 18.12 Optimització i rendiment

Quan els fluxos creixen, Node-RED pot alentir-se. Algunes optimitzacions:

- **Limitar els nodes `debug`**: cada missatge enviat a debug es guarda a memòria.
- **Usar `link nodes`** en lloc de cables llargs.
- **Processar dades en lots** quan sigui possible.
- **Cachejar consultes a InfluxDB** si es fan moltes vegades amb els mateixos paràmetres.
- **Evitar nodes `function` amb codi massa complex**: millor encapsular en mòduls.

## 18.13 Proves d'integració

Quan construïm un flux, hem de provar-lo de punta a punta. El procediment és:

1. **Provar amb dades simulades**: usar el simulador Python del Capítol 14.
2. **Validar el comportament**: rebre una alerta, veure una gràfica, etc.
3. **Provar casos extrems**: què passa si arriba un valor null? I un valor molt gran?
4. **Documentar el flux**: afegir comentaris, guardar una captura de pantalla, desar el JSON.

## 18.14 Resum

Hem après a construir set fluxos pràctics que cobreixen els casos d'ús més habituals al BernatLab: neteja de dades, alertes per gelada i sòl sec, mitjana mòbil, control d'actuadors, monitoratge de sensors, resums diaris. Hem vist patrons avançats com la confirmació d'accions, el debounce, el dead letter i el heartbeat. Hem après a organitzar la lògica amb subflows, a depurar amb els nodes adequats, i a optimitzar el rendiment. En el proper capítol veurem Grafana, l'eina de visualització que ens permetrà veure totes aquestes dades en gràfiques.

## 18.15 Exercicis pràctics

1. Implementa el flux 1 (neteja de dades) al teu Node-RED.
2. Implementa el flux 2 (alerta de gelada) i prova'l amb el simulador Python.
3. Implementa el flux 4 (mitjana mòbil) i observa la diferència amb les lectures originals.
4. Implementa el flux 6 (monitorar sensors inactius) i comprova que detecta bé quan pares el simulador.
5. Implementa el flux 7 (resum diari) i configura'l perquè s'enviï a les 8:00.
6. Crea un subflow "Alerta si valor < llindar" que puguis reutilitzar en diferents parts del sistema.
7. Exporta tots els fluxos a JSON i guarda'ls a `~/homelab/backup/`.

Paraules clau: **Node-RED, flux pràctic, neteja de dades, validació, alerta de gelada, alerta de sòl sec, mitjana mòbil, vàlvula de reg, sensor inactiu, resum diari, subflow, debounce, heartbeat, dead letter, confirmació, optimització, debug, catch, rbe, delay, InfluxDB, MQTT, Telegram, sensors, hort, BernatLab, Hort Osona**.
