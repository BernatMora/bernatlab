# BernatLab Hort - Pla d'accio: 4G + ESP32 + RPi

## Resum del que tens

- **Router 4G** amb microSIM de 150 GB de dades/mes
- **RPi 4 (hortosona)** a l'hort
- **1 ESP32** a 15 metres de la RPi
- Objectiu: connectar la RPi al router 4G, no a la xarxa de casa

## Per que es important

- Tindras **internet propi a l'hort** (independent de la xarxa de casa)
- L'ESP32 pot **enviar dades a la RPi per WiFi** (15m es perfecte)
- Podras accedir a la RPi **remotament** (via Tailscale) des de qualsevol lloc
- Podras tenir **càmeres, sensors, reg automatic** sense dependre de casa

## Arquitectura

```
INTERNET (4G/5G)
       |
[Router 4G + SIM 150GB]
       |  (WiFi del router)
       +---> [RPi hortosona] (Tailscale, Docker, Mosquitto, Grafana)
       |          |
       |          +-- (WiFi 2.4GHz) ---> [ESP32 sensor temperatura/...]
       |
       +---> [PC casa (quan hi vas)]
```

## Fases

### Fase 1: Configurar el router 4G

1. **Connectar la RPi al router 4G** (per WiFi, no Ethernet)
2. **Configurar el router** per:
   - Donar IP fixa a la RPi (DHCP reservation)
   - Permetre acces extern (si vols)
   - Limitar el consum de dades (alertes)

### Fase 2: Verificar la connexio a Internet

1. Comprovar que la RPi te internet (`ping 8.8.8.8`)
2. Comprovar que Tailscale funciona
3. Comprovar que pots accedir des del teu PC

### Fase 3: Preparar la RPi per rebre dades de l'ESP32

1. Instal·lar **MQTT (Mosquitto)** a la RPi
2. Configurar **InfluxDB** per guardar les dades
3. Configurar **Grafana** per visualitzar-les

### Fase 4: Programar l'ESP32

1. Instal·lar el firmware a l'ESP32 (MicroPython o Arduino)
2. Configurar-la per connectar-se al WiFi del router 4G
3. Programar-la per enviar dades dels sensors via MQTT

### Fase 5: Visualitzar les dades

1. Crear dashboards a Grafana
2. Configurar alertes per Telegram
3. Crear una pàgina web publica (Hort Osona) amb les dades

## Quin hardware necessites

### Per connectar la RPi al router 4G

- **Cap cable** si el router te WiFi
- Si vols cable: un cable Ethernet curt (1-2m)

### Per l'ESP32 (recomanat)

- **ESP32** (~10-15 EUR a AliExpress/Amazon)
- **Sensor DHT22** (temperatura + humitat) (~3 EUR)
- **Cablejat** (Dupont, ~3 EUR)
- **Carcasa** (imprimir-la o comprar-la, ~5 EUR)
- **Font d'alimentacio**: USB 5V o bateria 18650 (~5 EUR)

Total: ~30-40 EUR

## Quin software necessites

- **A la RPi**: Mosquitto (MQTT), InfluxDB, Grafana
- **A l'ESP32**: MicroPython o Arduino IDE

## Quin protocol utilitzar

A 15 metres tens **dues opcions**:
- **MQTT sobre WiFi** (l'ESP32 ja el te integrat) - **recomanat**
- **LoRa** (cal un modul SX1262) - innecessari a 15m

## Quina diferència hi ha entre el router de casa i el 4G?

| Característica | Router de casa | Router 4G hort |
|---|---|---|
| **Latencia** | 5-20 ms | 30-80 ms |
| **Amplada de banda** | Alta (100 Mbps+) | Mitjana (10-50 Mbps) |
| **Cost mensual** | 0 EUR (ja el tens) | ~15-30 EUR (dades) |
| **Disponibilitat** | 100% si tens llum | Depen de la cobertura |
| **IP publica** | Sol ser fixa | Sol ser variable |

## Consells

- **Comprova la cobertura 4G** a l'hort abans de comprar el router
- **Limita el consum de dades** (desactiva actualitzacions automaticas a la RPi)
- **Configura Tailscale** per accedir de forma segura des de fora
- **Fes servir MQTT** en lloc de HTTP per a sensors (mes efficient)

## Que fer primer

1. **Assegura't que tens bona cobertura 4G a l'hort** (prova amb el mobil)
2. **Configura el router 4G** amb un nom de xarxa i contrasenya
3. **Connecta la RPi al WiFi del router 4G**
4. **Verifica que tens internet**

Despres, ja podem passar a la fase 2 (Tailscale, sensors, etc.)

## Cost aproximat

- Router 4G amb SIM: ~50-100 EUR (depèn del model)
- ESP32 + sensor + accesoris: ~30-40 EUR
- **Total**: ~100 EUR
- **Mensual**: 15-30 EUR (dades 4G)

Es un cost molt raonable per tenir un hort connectat!
