# Resum - Capitol 1: Que son les dades d'un hort

## La idea clau

Un hort genera **dades constants** que avui, amb sensors barats i una RPi, podem capturar, guardar i visualitzar. El que abans era "el pagès mira el cel i toca la terra", ara es tradueix a grafiques, alertes i calendaris. Aquest capitol posa les bases: quines dades existeixen, com les classifiquem i per que serveixen.

## Tipus de dades d'un hort

Podem classificar les dades en quatre grans families:

1. **Ambientals**: temperatura, humitat relativa, pressio atmosferica, luminositat, pluviometria, vent. Són dades del "temps" que envolta l'hort.
2. **De soll**: humitat del terreny, temperatura del soll, conductivitat electrica (EC), pH. Són les que mes directament afecten les plantes.
3. **De cultiu**: alçada de la planta, diametre del tronc, nombre de fulles, presencia de plagues (via camares).
4. **De gestio**: regs fets, quantitat d'aigua, fertilitzants aplicats, dates de sembra i collita, incidents.

A l'Hort Osona capturem les tres primeres families amb sensors i la quarta la portem nosaltres amb un calendari i una API.

## Dades ambientals

Les mesura un sensor tipus **BME280** o **DHT22** connectat a la RPi o a un node LoRa. Em serveixen per:

- Detectar **gelades**: si la temperatura baixa de 0°C i la humitat es alta, risc de gelada.
- Planificar regs: si fa 35°C i humitat del 20%, cal regar avui.
- Alertes de vent: si la rafaga supera 50 km/h, pot tombar tutors.

Exemple real del Hort Osona (un missatge MQTT amb BME280):

```
{
  "device": "hort-osona-bme-01",
  "ts": "2026-04-12T08:30:00Z",
  "temp_c": 3.2,
  "humidity": 88.1,
  "pressure_hpa": 1014.3,
  "lux": 12500
}
```

## Dades de soll

El sensor estrella es el **Xiaomi MiFlora** (veure cap 2). Mesura:

- Humitat del soll (%)
- Temperatura del soll (°C)
- Conductivitat (µS/cm) -> indica salinitat i nutrients
- Lluminositat (lux)

Aquestes dades són les **mes importants** per al pagès: et diuen si la planta beu, si te calor a les arrels i si te nutrients. Un tomàquet amb EC baixa creix poc; amb EC alta, es crema.

```
{
  "device": "miflora-toma-01",
  "ts": "2026-04-12T09:00:00Z",
  "soil_moisture": 42.0,
  "soil_temp_c": 16.5,
  "ec_us_cm": 850,
  "lux": 18000
}
```

## Dades de cultiu

Les capturem amb camara (RPi Camera v3) o amb sensors específics. A l'Hort Osona tenim:

- **Camera time-lapse**: una foto cada 10 minuts del tomàquet. Ens permet veure el creixement i plagues visualment.
- **Mesura manual d'alçada**: introduida a mà per l'hortola (no tot ha d'estar automatitzat!).

Les dades visuals (imatges) no les desem a InfluxDB sino a **MinIO** o al sistema de fitxers. Aixo es important: cada tipus de dada te el seu magatzem.

## Dades de gestio

Són les que introdueix l'hortola o que venen d'actuadors. A l'Hort Osona portem:

- **Calendar de sembra**: data de sembra, data de trasplantament, data de collita esperada.
- **Reg**: si tenim electrovalvula, registrem quan s'ha obert i quanta aigua ha passat (amb un comptador).
- **Fertilitzacio**: tipus, dosis, data.

Exemple d'un registre de reg:

```json
{
  "ts": "2026-04-12T07:00:00Z",
  "sector": "toma-cherry",
  "duration_s": 600,
  "litres": 48.2,
  "trigger": "schedule"
}
```

## Freqüencia de captura

No totes les dades es capturen igual. La regla es: **captura tan sovint com necessitis, pero no mes**.

- Temperatura ambient: cada 5 minuts
- Humitat soll: cada 15 minuts
- Pluja: cada minut (es pot perdre un xàfec)
- Camera: cada 10 minuts (1 foto)
- Collita: quan passa (esdeveniment)

Si captures a 1 Hz sense necessitat, la base de dades creix rapidissim i gastes memoria i CPU.

## Emmagatzematge: on va cada cosa

A l'Hort Osona:

| Dada | Magatzem | Per que |
|---|---|---|
| Series temporals (sensors) | **InfluxDB** | Optimitzat per time-series |
| Imatges camera | **MinIO** (S3) | Fitxers binaris grans |
| Calendar / regs | **PostgreSQL** | Dades relacionals |
| Cache consultes | **Redis** | Rapid per a grafiques |
| Configuracio | **Fitxers YAML** | Facil de versionar |

Aquesta separacio es important: si tot ho poses a InfluxDB, acabara sent lent. Si tot a Postgres, les series temporals el maten.

## Connexions amb altres capitols

- **M7 Cap 2** - El sensor MiFlora ens dona les dades de soll.
- **M7 Cap 4** - L'arquitectura completa que mou aquestes dades.
- **M7 Cap 6** - InfluxDB es el magatzem de series temporals.
- **M7 Cap 9** - El calendari organitza les dades de cultiu.
- **M7 Cap 10** - Casos reals on aquestes dades salven collites.
