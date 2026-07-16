# Exercici practic - Capitol 1: Que son les dades d'un hort

> 30-45 min · Real al teu hort o RPi

## Objectiu

Inventariar tots els punts de dades del teu hort i decidir com les capturaras, a quina freqüencia i on les guardaras. Acabaras amb una "fitxa de dades" del projecte Hort Osona.

## Requisits

- Un hort (real o imaginari) amb sectors
- Coneixement basic de sensors
- 30-45 minuts

## Pas 1: Inventari dels sectors (10 min)

Primer de tot, dibuixa el teu hort. Si estas a la RPi pots fer-ho en un fitxer:

```bash
mkdir -p ~/hort-osona/docs
nano ~/hort-osona/docs/sectors.md
```

Descriu els sectors. Exemple real del Hort Osona:

```markdown
# Sectors de l'Hort Osona

1. **toma-cherry** - 8 plantes, hivernacle, reg automatic
2. **enciam-fulla** - 20 plantes, exterior, reg manual
3. **pebrot-italia** - 6 plantes, exterior, reg automatic
4. **carxofa** - 4 plantes, exterior, reg gota a gota
5. **herbes** (basilica, orenga, menta) - exterior, test
```

Per cada sector, pensa:
- Quin cultiu te?
- Te hivernacle o exterior?
- Te reg automatic o manual?
- Hi passem sovint o es tot sol?

## Pas 2: Llista de sensors per sector (10 min)

Ara omple una taula amb els sensors que necessites. Pots usar aquesta plantilla:

```markdown
| Sector        | Ambient (BME) | Soll (MiFlora) | Camera | Pluja |
|---------------|---------------|----------------|--------|-------|
| toma-cherry   | Si (interior) | Si (1 per test) | Si     | No    |
| enciam-fulla  | Si (compartit)| No             | No     | Si    |
| pebrot-italia | Si (compartit)| Si (1 per test) | No     | Si    |
| carxofa       | No            | Si             | No     | Si    |
| herbes        | No            | No             | No     | No    |
```

Guarda-ho a `~/hort-osona/docs/sensors.md`. Aquest document es **la veritat** del projecte: tota nova decisio tecnica es mira contra aquesta taula.

## Pas 3: Decideix frequencies (10 min)

Ara una taula semblant pero amb les **frequencies** de captura:

```markdown
| Sensor              | Freq     | Justificacio                       |
|---------------------|----------|------------------------------------|
| BME280 hivernacle   | 5 min    | Canvi lent, pero volem gelades     |
| BME280 exterior     | 5 min    | Compartir amb hivernacle           |
| MiFlora tomàquet    | 15 min   | El soll canviadespacio             |
| Camera              | 10 min   | Time-lapse visual                  |
| Pluviometre         | 1 min    | Xàfecs curts es poden perdre      |
| EC soll             | 30 min   | Canvi molt lent                    |
```

Guarda-la a `~/hort-osona/docs/frequencies.md`. Important: **no posis frequencies que no necessitis**. Si captures a 1 Hz el BME280, tindras 86.400 punts/dia inutils.

## Pas 4: Escull l'emmagatzematge (10 min)

Fes una taula tipus "on va cada cosa":

```markdown
| Dada                | Magatzem    | Per que                      |
|---------------------|-------------|------------------------------|
| Temperatura BME280  | InfluxDB    | Serie temporal               |
| Humitat MiFlora     | InfluxDB    | Serie temporal               |
| Imatges camera      | MinIO       | Fitxers binaris grans       |
| Calendar de sembra  | PostgreSQL  | Dades relacionals            |
| Registre de regs    | PostgreSQL  | Auditoria                    |
| Ultima lectura      | Redis       | Cache per la web             |
| Configuracio        | YAML git    | Versionable                  |
```

Guarda-la a `~/hort-osona/docs/storage.md`. Aquesta decisio es **estructural** i costa molt canviar-la despres. Pensa-hi be.

## Pas 5: Crea el fitxer de configuracio (5 min)

A la RPi o al teu repo, crea `~/hort-osona/config/dades.yaml`:

```yaml
hort:
  nom: "Hort Osona"
  localitat: "Vic"
  sectors:
    - id: toma-cherry
      cultiu: "tomàquet cherry"
      hivernacle: true
      reg: "automatic"
    - id: enciam-fulla
      cultiu: "enciam fulla de roure"
      hivernacle: false
      reg: "manual"

sensors:
  bme280:
    freq_s: 300          # 5 min
    topics:
      - "hort-osona/bme/hivernacle/temp"
      - "hort-osona/bme/hivernacle/hum"
  miflora:
    freq_s: 900          # 15 min
    macs:
      - "C4:7C:8D:65:1B:32"  # toma-cherry
      - "C4:7C:8D:65:1B:33"  # pebrot
  camera:
    freq_s: 600          # 10 min
    desti: "minio/hort-osona/camera/"

magatzem:
  influxdb:
    bucket: "hort-osona"
    org: "bernatlab"
  postgres:
    db: "hort_osona"
  minio:
    bucket: "hort-osona"
```

Aquest fitxer es el que llegeixen tots els teus scripts. Es **la font de veritat**.

## Validacio

Has acabat si:

- [ ] Has inventariat 3 o mes sectors del teu hort.
- [ ] Has omplert una taula de sensors per sector.
- [ ] Has decidit frequencies raonables (entre 1 min i 1 hora).
- [ ] Has creat la taula d'emmagatzematge amb 4 o mes tipus de dada.
- [ ] Tienes un fitxer `dades.yaml` amb sectors, sensors i frequencies.

## Per aprofundir

- Investiga el concepte "data mesh" aplicat a un hort petit.
- Compara InfluxDB vs TimescaleDB vs Prometheus per a series temporals.
- Dibuixa un diagrama de flux de dades: sensor -> broker -> DB -> web.
- Calcula quant bytes/dia generara el teu hort amb les frequencies triades.
