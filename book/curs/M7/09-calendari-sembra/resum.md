# Resum - Capitol 9: Calendari de sembra i planificacio de cultius

## La idea clau

A l'Hort Osona tenir sensors que mesuren tot es inutil si no se sap **quan sembrar, quan trasplantar i quan collir**. El calendari de sembra es la **capa d'intel·ligencia** que connecta les dades ambientals (temperatura, humitat, llum) amb les necessitats de cada cultiu. Es tradueix els grafiques en **accions** i permet planificar tota la temporada: tomàquets al febrer bajo cobertor, enciams cada 15 dies per collir tota l'estiu, alls al novembre.

## Per que cal un calendari de sembra

Si nomes mires els sensors, saps que avui el soll esta a 14°C. Pero no saps si toca sembrar pastanagues o si ja es massa tard per plantar carbasso. El calendari de sembra respon a la pregunta **"que faig ara?"** en funcio de:

- **Epoca de l'any** (mes, setmana).
- **Varietat** (temperatura minima de germinacio, dies fins a collita).
- **Clima local** (Osona te un clima de transicio entre el prelitoral i el Pirineu, amb gelades fins a mitjans d'abril).
- **Darrera gelada** i **primera gelada** historiques.
- **Rotacio de cultius** (no plantar solanacies al mateix lloc 2 anys seguits).

A l'Hort Osona tenim sectors organitzats per families botaniques. El calendari ens diu **quan tocar cada sector**.

## Conceptes basics d'horticultura

- **Sembra directa**: la llavor va directament al soll. Carotes, raves, espinacs.
- **Trasplantament**: primer es sembra en safata (al viver) i despres es mou al hort quan la planta te 4-6 fulles. Tomàquets, pebrots, alberginies.
- **Marc de plantacio**: distancia entre plantes i entre files. Tomàquet 60x40 cm, pastanaga 5x20 cm.
- **Dies fins a collita (DTC)**: dels que parlen els sobres. Tomàquet cherry ~65 dies des de trasplantament.
- **Foto-periodicitat**: algunes plantes necesiten un determinat numero d'hores de llum per florir (dia llarg, dia curt, indiferents).
- **Vernalitzacio**: algunes plantes necesiten un periode de fred per florir (cols, pastanagues de guardar).

A l'Hort Osona la majoria son plantes de **dia neutre** (indiferents al fotoperiode), pero cal vigilar amb les **biannuals** (cols, pastanagues) que pugen a flor l'any segonent si passen fred.

## Taula de sembra per a Osona

Aixo es una taula de referència. Les dates son aproximades i poden variar ±2 setmanes segons l'any. **Important**: a Osona les gelades de primavera poden allargar-se fins a finals d'abril a la zona alta (900+ m), i les primeres gelades de tardor arriben a mitjans d'octubre.

| Cultiu | Sembra interior | Trasplantament | Sembra directa | Collita | Familia | Rotacio |
|---|---|---|---|---|---|---|
| Tomàquet | febrer-març | abril-maig (gelades passades) | - | juliol-octubre | Solanacia | post-aliacia |
| Pebrot | febrer-març | maig | - | agost-octubre | Solanacia | post-aliacia |
| Alberginia | febrer-març | maig-juny | - | agost-octubre | Solanacia | post-aliacia |
| Enciam | febrer-setembre | març-octubre | març-setembre | maig-novembre | Composita | post-arrel |
| Bleda | - | - | març-setembre | juny-novembre | Quenopodiacea | qualsevol |
| Espinac | - | - | març-maig, agost-setembre | maig-juny, octubre-novembre | Quenopodiacea | qualsevol |
| Pastanaga | - | - | març-juliol | juny-novembre | Umbelifera | post-bulb |
| Rave | - | - | març-setembre | abril-octubre | Brassicacia | qualsevol |
| All | - | - | octubre-gener | juny-juliol | Liliacia | post-arrel |
| Ceba | febrer | abril | març | juliol-setembre | Liliacia | post-arrel |
| Carbasso | abril | maig | maig | juliol-setembre | Cucurbitacia | post-arrel |
| Cogombre | abril | maig | maig | juliol-setembre | Cucurbitacia | post-arrel |
| Mongeta | - | - | maig-juliol | juliol-octubre | Lleguminosa | post-qualsevol (fixa N) |
| Pèsol | - | - | octubre-febrer | abril-juny | Lleguminosa | post-qualsevol (fixa N) |
| Col | juny-juliol | agost-setembre | - | octubre-març | Brassicacia | post-arrel |
| Bròquil | juny-juliol | agost-setembre | - | octubre-febrer | Brassicacia | post-arrel |

## Rotacio de cultius: la clau de la salut del soll

Si plantes tomàquets al mateix lloc cada any, el soll s'esgota, els nematodes augmenten, i les plagues s'instal·len. La **rotacio de 4 anys** es la mes utilitzada:

- **Any 1**: Lleguminoses (mongetes, pèsols) - fixen nitrogen.
- **Any 2**: Solanacies i Cucurbitacies (tomàquet, carbasso) - aprofiten el nitrogen.
- **Any 3**: Brassicacies i Compostes (cols, enciams) - raices diferents.
- **Any 4**: Arrels i bulbs (pastanaga, all) - tanquen el cicle.

A l'Hort Osona tenim 4 sectors. Rotem les families cada any. L'**api** i el **fonoll** son bon predecessors per a la **col** perque les seves arrels repel·leixen la mosca de la col.

## Darrera gelada: el parametre critic

A Osona la **data de darrera gelada** (a 850 m d'alçada) es al voltant del **15 d'abril**, pero pot variar del 1 d'abril al 10 de maig. La **primera gelada de tardor** sol ser a **mitjans d'octubre**.

Com saber la data exacta a la teva zona? Consulta les dades del teu sensor de temperatura o mira la web del Servei Meteorologic de Catalunya. Una bona regla es **no plantar solanacies fins 2 setmanes despres de la darrera gelada** a la teva zona.

A l'Hort Osona tenim un sensor de temperatura exterior que enregistra tot l'any. A partir de 2-3 anys de dades podem calcular la data mitjana de darrera gelada amb precisio.

## Com guardar el calendari

Hi ha diverses maneres. Al BernatLab usem **YAML** perque es lisible per humans i es pot versionar a Git. Cada cultiu te una entrada amb les dates clau i les condicions.

```yaml
# hort-osona/calendari/tomato-cherry.yaml
cultiu: tomàquet cherry
familia: solanacia
varietat: "Sungold"
durada_dies: 65   # des de trasplantament
planta_per_m2: 4
temperatura_minima_germinacio: 18   # ºC
temperatura_optima_germinacio: 22-28
temperatura_minima_creixement: 10
gelada_mortal: true

sembra_interior:
  inici: 2026-02-15
  fi: 2026-03-15
  safates: 40 alveols
  substrat: torba + perlita

trasplantament:
  inici: 2026-04-25
  fi: 2026-05-20
  condicio: gelades passades + T mínima > 10°C
  marc: 60x40 cm

collita:
  inici: 2026-07-15
  fi: 2026-10-15

notes:
  - "Tutorejar amb canya des del primer moment"
  - "Tallar xupons fins al 5e pom"
  - "Regar al peu, no mullar fulles (mildiu)"
  - "Afegir mulch per conservar humitat"
```

Per cultius de sembra directa (pastanaga, rave) nomes cal el periode de sembra i collita. Per cultius plurianuals (all, col) el calendari s'allarga mes enlla d'una temporada.

## Com generar el calendari amb Python

Podem generar el calendari automaticament a partir dels fitxers YAML i les dades de temperatura. Un script simple que ens avisa de les feines de la setmana:

```python
# scripts/generar_calendari.py
import yaml
from datetime import date, timedelta
from pathlib import Path

def feines_setmana(calendari_dir: Path, avui: date):
    feines = []
    for fitxer in calendari_dir.glob("*.yaml"):
        cultiu = yaml.safe_load(fitxer.read_text())
        nom = cultiu["cultiu"]

        # Converteix dates string a date
        trasp = cultiu.get("trasplantament", {})
        if "inici" in trasp and "fi" in trasp:
            inici = date.fromisoformat(trasp["inici"])
            fi = date.fromisoformat(trasp["fi"])
            if inici <= avui <= fi:
                feines.append(f"TRASPLANTAR {nom} (fins {fi})")

        sembra = cultiu.get("sembra_interior", {})
        if "inici" in sembra and "fi" in sembra:
            inici = date.fromisoformat(sembra["inici"])
            fi = date.fromisoformat(sembra["fi"])
            if inici <= avui <= fi:
                feines.append(f"SEMBRAR {nom} en safata (fins {fi})")

        sembra_d = cultiu.get("sembra_directa", {})
        if "inici" in sembra_d and "fi" in sembra_d:
            inici = date.fromisoformat(sembra_d["inici"])
            fi = date.fromisoformat(sembra_d["fi"])
            if inici <= avui <= fi:
                feines.append(f"SEMBRAR {nom} directe (fins {fi})")
    return feines

if __name__ == "__main__":
    avui = date.today()
    print(f"=== Feines per la setmana del {avui} ===")
    for f in feines_setmana(Path("hort-osona/calendari"), avui):
        print(f"  - {f}")
```

Aquest script es pot cridar cada dilluns via cron i enviar un correu o un missatge a Telegram amb les feines de la setmana. Aixi no t'oblides mai de res.

## Integracio amb els sensors

El calendari nomes te sentit si llig les dades reals. Exemples d'integracio:

- **Risc de gelada**: si el sensor de temperatura prediu <0°C a les properes 24h, avisa per plantar cobertors o entrar plantes en test.
- **Temperatura del soll**: nomes trasplantar tomàquets si la T del soll es >12°C de mitjana a 10 cm.
- **Humitat del soll**: decidir si cal regar en funcio de la previsio de pluja i la humitat actual.
- **Dies graus** (growing degree days, GDD): calcular la integral termica per predir quan madura un fruit.

Exemple de prediccio de gelada amb el sensor:

```bash
# Ultimes 24h de temperatura
influx query 'from(bucket:"hort-osona")
  |> range(start: -24h)
  |> filter(fn: (r) => r._measurement == "ambient" and r._field == "temp_c")'
```

Si la temperatura minima prevista per aquesta nit es <2°C, cal actuar.

## Plantilles mensuals

Cada mes te les seves feines tipiques. Aqui tens un resum:

**Gener-Febrer**: planificar temporada, comprar llavors, preparar safates i substrat, sembrar tomàquets i pebrots al viver.

**Març**: trasplantar enciams primerencs, sembrar pastanagues i raves, preparar el terreny, adobar amb compost.

**Abril**: vigilar gelades tardanes, trasplantar tomàquets al final del mes, sembrar mongetes primerenques.

**Maig**: trasplantar pebrots i alberginies, sembrar carbassons, instal·lar tutors, primers regs per degoteig.

**Juny**: aclarir pastanagues, collir primers enciams i raves, plantar carbassons, vigilar pugons.

**Juliol**: reg abundant, collir tomàquets primerencs, sembrar cols de tardor, retirar males herbes.

**Agost**: collita forta, sembrar espinacs i raves de tardor, plantar cebes d'hivern.

**Setembre**: plantar alls, sembrar enciams d'hivern, collir carbasses, preparar el terreny per a l'any vinent.

**Octubre**: collir les ultimes tomàquets, tapar compost, retirar canyes, plantar bulbs.

**Novembre-Desembre**: arranjar eines, neteja, planificacio de l'any vinent, repòs del soll.

## Connexions amb altres capitols

- **M7 Cap 4** - L'arquitectura on el calendari es un component mes.
- **M7 Cap 7** - L'API pot exposar les feines de la setmana com un calendari iCal.
- **M7 Cap 8** - La PWA pot mostrar el calendari de feines a l'inici.
- **M7 Cap 10** - Casos reals on el calendari va salvar o va perjudicar una collita.
- **M3 Cap 1** - Backups de la base de dades del calendari.
