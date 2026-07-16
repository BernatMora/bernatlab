# Exercici practic - Capitol 10: Casos reals de l'Hort Osona

> 60-90 min · Implementar un sistema d'alertes reals a l'Hort Osona

## Objectiu

Reproduir un dels 3 casos reals: implementar el **sistema d'alerta de gelada** amb Python, que llegeix el sensor de temperatura i envia una alerta a Telegram. Acabarem tenint un sistema que **realment funciona** i que pots aplicar al teu hort.

## Requisits

- Raspberry Pi amb sensor de temperatura (DHT22, BME280 o similar).
- Compte de Telegram i un bot creat (veure M6 Cap 4).
- Python 3 + llibreries `requests`, `influxdb-client` (o API HTTP).
- 60-90 min.

## Pas 1: Estructura del projecte (5 min)

```bash
mkdir -p ~/hort-osona/alertes
cd ~/hort-osona/alertes
python3 -m venv .venv
source .venv/bin/activate
pip install requests influxdb-client python-dotenv
```

## Pas 2: Configuracio del bot de Telegram (5 min)

Crea `~/hort-osona/alertes/.env`:

```bash
TELEGRAM_BOT_TOKEN=1234567890:ABCDefGhiJklMnoPqrStuVwxYz
TELEGRAM_CHAT_ID=-1001234567890
INFLUXDB_URL=http://localhost:8086
INFLUXDB_TOKEN=el-meu-token-super-secret
INFLUXDB_ORG=hort-osona
INFLUXDB_BUCKET=hort-osona
LATITUD=41.93
LONGITUD=2.25
```

Posa el token del bot de Telegram (obtingut de `@BotFather`) i el chat_id del teu grup. **Mai** posis tokens al codi, sempre al `.env` (afegeix-lo a `.gitignore`).

## Pas 3: Script que llegeix la temperatura actual (10 min)

Crea `llegir_temperatura.py`:

```python
#!/usr/bin/env python3
"""Llegeix la temperatura del sensor i la retorna."""
import os
from datetime import datetime
from influxdb_client import InfluxDBClient
from dotenv import load_dotenv

load_dotenv()

def llegir_ultima_temp():
    """Retorna la temperatura del sensor exterior."""
    client = InfluxDBClient(
        url=os.environ["INFLUXDB_URL"],
        token=os.environ["INFLUXDB_TOKEN"],
        org=os.environ["INFLUXDB_ORG"],
    )
    query = '''
    from(bucket: "hort-osona")
      |> range(start: -10m)
      |> filter(fn: (r) => r._measurement == "ambient")
      |> filter(fn: (r) => r._field == "temp_c")
      |> last()
    '''
    result = client.query_api().query(query)
    for table in result:
        for record in table.records:
            return record.get_value()
    return None

if __name__ == "__main__":
    temp = llegir_ultima_temp()
    if temp is not None:
        print(f"Temperatura actual: {temp:.1f}°C")
    else:
        print("No s'ha pogut llegir la temperatura")
```

Prova'l: `python3 llegir_temperatura.py`. Hauries de veure la temperatura actual.

## Pas 4: Funcio que avalua el risc de gelada (10 min)

Crea `risc_gelada.py`:

```python
#!/usr/bin/env python3
"""Calcula el risc de gelada basat en previsio i tendencia."""
import os
from datetime import datetime, timedelta
from influxdb_client import InfluxDBClient
from dotenv import load_dotenv

load_dotenv()

def llegir_tendencia(hores: int = 4):
    """Retorna la llista de temperatures de les ultimes N hores."""
    client = InfluxDBClient(
        url=os.environ["INFLUXDB_URL"],
        token=os.environ["INFLUXDB_TOKEN"],
        org=os.environ["INFLUXDB_ORG"],
    )
    query = f'''
    from(bucket: "hort-osona")
      |> range(start: -{hores}h)
      |> filter(fn: (r) => r._measurement == "ambient")
      |> filter(fn: (r) => r._field == "temp_c")
      |> aggregateWindow(every: 30m, fn: mean, createEmpty: false)
    '''
    result = client.query_api().query(query)
    temps = []
    for table in result:
        for record in table.records:
            temps.append((record.get_time(), record.get_value()))
    return temps

def avaluar_risc():
    """Retorna un nivell de risc: 'alt', 'mig', 'baix', 'cap'."""
    serie = llegir_tendencia(6)
    if len(serie) < 2:
        return "desconegut", None, None

    temp_actual = serie[-1][1]
    temps_anteriors = [t for _, t in serie[:-1]]

    # Calcula la tendencia (pendent de regressio lineal simple)
    n = len(temps_anteriors)
    mitjana_x = sum(range(n)) / n
    mitjana_y = sum(temps_anteriors) / n
    numerador = sum((i - mitjana_x) * (t - mitjana_y) for i, t in enumerate(temps_anteriors))
    denominador = sum((i - mitjana_x) ** 2 for i in range(n))
    tendencia = numerador / denominador if denominador != 0 else 0  # graus/h

    # Prediu la temperatura d'aqui a 6 hores
    temp_predita = temp_actual + tendencia * 6

    if temp_predita < 0:
        risc = "alt"
    elif temp_predita < 2:
        risc = "mig"
    elif temp_predita < 5:
        risc = "baix"
    else:
        risc = "cap"

    return risc, temp_actual, temp_predita

if __name__ == "__main__":
    risc, actual, predita = avaluar_risc()
    print(f"Risc: {risc}")
    print(f"Temp actual: {actual:.1f}°C" if actual is not None else "Temp actual: N/A")
    print(f"Temp predita (+6h): {predita:.1f}°C" if predita is not None else "Temp predita: N/A")
```

## Pas 5: Funcio que envia alerta a Telegram (10 min)

Cria `alerta_telegram.py`:

```python
#!/usr/bin/env python3
"""Envia missatges a Telegram."""
import os
import requests
from dotenv import load_dotenv

load_dotenv()

def enviar_missatge(text: str, parse_mode: str = "Markdown"):
    """Envia un missatge al chat configurat."""
    token = os.environ["TELEGRAM_BOT_TOKEN"]
    chat_id = os.environ["TELEGRAM_CHAT_ID"]
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    r = requests.post(url, json={
        "chat_id": chat_id,
        "text": text,
        "parse_mode": parse_mode,
    })
    r.raise_for_status()
    return r.json()

if __name__ == "__main__":
    enviar_missatge("🧪 *Test alerta Hort Osona*\n\nSi reps això, el sistema funciona!")
```

Prova'l: `python3 alerta_telegram.py`. Hauries de rebre un missatge al teu Telegram.

## Pas 6: Script principal que integra tot (15 min)

Cria `gelada_watch.py`:

```python
#!/usr/bin/env python3
"""Vigila el risc de gelada i envia alertes."""
import sys
import time
import logging
from datetime import datetime
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from risc_gelada import avaluar_risc
from alerta_telegram import enviar_missatge

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("/var/log/hort-gelada.log"),
        logging.StreamHandler(),
    ],
)
log = logging.getLogger(__name__)

# Estat: nomes envia alerta un cop per episodi
ultim_avís = {"nivell": "cap", "ts": None}

def ha_de_avisar(risc_actual: str) -> bool:
    """Noves alertes nomes si puja de nivell o fa >6h del darrer."""
    if risc_actual == "cap":
        return False
    if ultim_avís["nivell"] == "cap":
        return True
    if ultim_avís["nivell"] == "baix" and risc_actual in ("mig", "alt"):
        return True
    if ultim_avís["nivell"] == "mig" and risc_actual == "alt":
        return True
    if ultim_avís["ts"] and (datetime.now() - ultim_avís["ts"]).total_seconds() > 21600:
        return True
    return False

def generar_missatge(risc: str, actual: float, predita: float) -> str:
    if risc == "alt":
        emoji = "🥶🥶"
        consell = "ACCIÓ IMMEDIATA: cobrir plantes amb manta termica, regar al vespre, posar ampolles d'aigua."
    elif risc == "mig":
        emoji = "🥶"
        consell = "Prepara't: manta termica a ma, vigilant el pronòstic."
    elif risc == "baix":
        emoji = "❄️"
        consell = "Risc baix. Continua vigilant."
    else:
        return ""

    return (
        f"{emoji} *ALERTA GELADA* {emoji}\n\n"
        f"🌡️ Temperatura actual: {actual:.1f}°C\n"
        f"📉 Temperatura predita (+6h): {predita:.1f}°C\n"
        f"⚠️ Nivell de risc: *{risc.upper()}*\n\n"
        f"💡 {consell}\n\n"
        f"_Generat automàticament per Hort Osona_"
    )

def tick():
    risc, actual, predita = avaluar_risc()
    log.info(f"Risc: {risc} | Actual: {actual} | Predit: {predita}")

    if ha_de_avisar(risc):
        try:
            missatge = generar_missatge(risc, actual or 0, predita or 0)
            if missatge:
                enviar_missatge(missatge)
                ultim_avís["nivell"] = risc
                ultim_avís["ts"] = datetime.now()
                log.info(f"Alerta enviada: {risc}")
        except Exception as e:
            log.error(f"Error enviant alerta: {e}")

    # Reset a 'cap' si ha passat el risc
    if risc == "cap" and ultim_avís["nivell"] != "cap":
        ultim_avís["nivell"] = "cap"
        ultim_avís["ts"] = None
        log.info("Risc desaparegut, reset estat")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--once":
        tick()
    else:
        log.info("Iniciant vigilància de gelades (cada 30 min)")
        while True:
            tick()
            time.sleep(1800)  # 30 min
```

## Pas 7: Prova'l amb dades simulades (10 min)

Pots injectar temperatures baixes a InfluxDB per simular una gelada:

```bash
# Insereix una temperatura baixa
influx write \
  -b hort-osona \
  -m ambient \
  -f temp_c=-1.5 \
  --time $(date +%s)000000000
```

Despres executa:

```bash
python3 gelada_watch.py --once
```

Hauries de rebre una alerta a Telegram amb el missatge de risc **alt**.

## Pas 8: Fer-lo correr com a dimoni (5 min)

Crea `/etc/systemd/system/hort-gelada.service`:

```ini
[Unit]
Description=Vigilancia de gelades Hort Osona
After=network.target

[Service]
Type=simple
User=hort
WorkingDirectory=/home/hort/hort-osona/alertes
ExecStart=/home/hort/hort-osona/alertes/.venv/bin/python3 /home/hort/hort-osona/alertes/gelada_watch.py
Restart=on-failure
RestartSec=60

[Install]
WantedBy=multi-user.target
```

Activa'l:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now hort-gelada.service
sudo systemctl status hort-gelada.service
sudo journalctl -u hort-gelada.service -f
```

## Validacio

Has acabat si:

- [ ] El script `llegir_temperatura.py` retorna temperatures valides.
- [ ] El script `risc_gelada.py` avalua correctament amb dades reals.
- [ ] Has rebut un missatge de test a Telegram.
- [ ] El script `gelada_watch.py --once` envia una alerta amb risc alt simulat.
- [ ] El servei systemd esta actiu i reinicia automaticament.
- [ ] Les alertes son graduades (baix, mig, alt) i no spam.
- [ ] Tots els secrets estan al `.env` (no al codi).

## Per aprofundir

- Afegeix la previsio del Meteocat o OpenWeather com a segona font.
- Fes el mateix per a **ones de calor** (T >35°C durant 3 dies).
- Implementa un sistema de **doble bomba** amb commutacio automatica.
- Afegeix una **escalada d'alertes** si no reps confirmacio.
- Integra el calendari: nomes envia alerta de gelada si hi ha tomàquets a l'exterior.
- Crea una **PWA** (M7 Cap 8) que mostri l'historic d'alertes.
