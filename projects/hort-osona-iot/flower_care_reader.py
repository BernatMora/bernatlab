#!/usr/bin/env python3
"""
flower_care_reader.py — Llegeix dades del Xiaomi Flower Care (Mi Flora) via BLE.

Llegeix cada X segons i envia les dades a InfluxDB.

Dades que llegeix:
  - temperature (°C)
  - moisture (% d'humitat del sol)
  - light (lux)
  - conductivity (us/cm)
  - battery (%)

Configuracio via .env:
  FLOWER_CARE_MAC = MAC del sensor
  INFLUXDB_URL = http://localhost:8086
  INFLUXDB_TOKEN = token d'escriptura
  INFLUXDB_BUCKET = hort
  INFLUXDB_ORG = bernat
  READ_INTERVAL = 900  # 15 minuts en segons
"""
import os
import sys
import time
import logging
from datetime import datetime, timezone
from pathlib import Path

try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent / '.env'
    if env_path.exists():
        load_dotenv(env_path)
except ImportError:
    pass

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=os.environ.get('LOG_LEVEL', 'INFO')
)
log = logging.getLogger('flower-care')

# Configuracio
FLOWER_CARE_MAC = os.environ.get('FLOWER_CARE_MAC', '').upper()
INFLUXDB_URL = os.environ.get('INFLUXDB_URL', 'http://localhost:8086')
INFLUXDB_TOKEN = os.environ.get('INFLUXDB_TOKEN', '')
INFLUXDB_BUCKET = os.environ.get('INFLUXDB_BUCKET', 'hort')
INFLUXDB_ORG = os.environ.get('INFLUXDB_ORG', 'bernat')
READ_INTERVAL = int(os.environ.get('READ_INTERVAL', '900'))

# BLE
try:
    from miflora import MiFloraPoller
    from btlewrap.gatttool import GatttoolBackend
except ImportError as e:
    log.error(f"Falten llibreries: {e}")
    sys.exit(1)

# InfluxDB
try:
    from influxdb_client import InfluxDBClient, Point, WritePrecision
except ImportError as e:
    log.warning(f"InfluxDB client no instal.lat: {e}")
    InfluxDBClient = None

if not FLOWER_CARE_MAC:
    log.error("FLOWER_CARE_MAC no definit al .env")
    log.error("Exemple: FLOWER_CARE_MAC=C4:7C:8D:6E:1B:5F")
    sys.exit(1)

def read_sensor():
    """Llegeix dades del Flower Care."""
    log.info(f"Llegint sensor {FLOWER_CARE_MAC}...")
    backend = GatttoolBackend()
    poller = MiFloraPoller(FLOWER_CARE_MAC, backend)

    try:
        data = {
            'temperature': poller.parameter_value('temperature'),
            'moisture': poller.parameter_value('moisture'),
            'light': poller.parameter_value('light'),
            'conductivity': poller.parameter_value('conductivity'),
            'battery': poller.battery_level(),
        }
        log.info(f"Llegit: {data}")
        return data
    except Exception as e:
        log.error(f"Error llegint sensor: {e}")
        return None

def send_to_influxdb(data):
    """Envia les dades a InfluxDB."""
    if InfluxDBClient is None:
        log.warning("InfluxDB client no disponible")
        return False
    if not INFLUXDB_TOKEN:
        log.warning("INFLUXDB_TOKEN no definit")
        return False

    try:
        client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
        write_api = client.write_api(write_options={'batch_size': 1})

        point = Point('flower_care') \
            .tag('mac', FLOWER_CARE_MAC) \
            .field('temperature', float(data['temperature'])) \
            .field('moisture', float(data['moisture'])) \
            .field('light', int(data['light'])) \
            .field('conductivity', int(data['conductivity'])) \
            .field('battery', int(data['battery'])) \
            .time(datetime.now(timezone.utc), WritePrecision.S)

        write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=point)
        client.close()
        log.info(f"Dades enviades a InfluxDB bucket '{INFLUXDB_BUCKET}'")
        return True
    except Exception as e:
        log.error(f"Error enviant a InfluxDB: {e}")
        return False

def main():
    log.info(f"Iniciant Flower Care Reader (interval={READ_INTERVAL}s)")
    log.info(f"MAC: {FLOWER_CARE_MAC}")
    log.info(f"InfluxDB: {INFLUXDB_URL} bucket={INFLUXDB_BUCKET}")

    while True:
        try:
            data = read_sensor()
            if data:
                send_to_influxdb(data)
        except KeyboardInterrupt:
            log.info("Aturat per l'usuari")
            break
        except Exception as e:
            log.error(f"Error inesperat: {e}")

        log.info(f"Esperant {READ_INTERVAL}s fins la propera lectura...")
        time.sleep(READ_INTERVAL)

if __name__ == '__main__':
    main()
