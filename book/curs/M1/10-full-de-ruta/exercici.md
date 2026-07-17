# Exercici pràctic — Capítol 10: Full de ruta

> 45-60 min · Real + planificació

## Objectiu

Planificar el teu BernatLab personal: quins serveis hi vols, amb quin ordre, quins objectius, i què necessitaries per créixer. Aquest exercici és més de reflexió que de teclejar ordres, però acaba amb un pla concret i compromís.

## Requisits
- Haver completat els capítols 1-9
- 45-60 minuts
- Opcional: un paper i bolígraf

## Pas 1: Inventari actual (10 min)

Fes una llista del que ja tens corrent al BernatLab. Crea `book/curs/M1/10-full-de-ruta/inventari.md`:

```markdown
# Inventari BernatLab (a data YYYY-MM-DD)

## Hardware
- Raspberry Pi 4 (4 GB RAM, hostname hortosona)
- IP Tailscale: 100.115.134.76
- microSD 64 GB

## Serveis actius
- Portainer (9000) - admin Docker
- Uptime Kuma (3001) - monitoratge
- Homepage (3010) - dashboard
- Whoami (8080) - test
- SSH (22) - accés remot
- Tailscale - VPN

## Limitacions actuals
- RAM: ~X GB usada de 4 GB
- Disc: ~X GB usats de 64 GB
- Serveis que voldria: ...

## Capacitat disponible
- Quants contenidors més podries afegir?
- Quin és el coll d'ampolla actual (RAM, CPU, disc, xarxa)?
```

## Pas 2: Visió a 6 mesos (15 min)

Crea `book/curs/M1/10-full-de-ruta/visio-6-mesos.md`. Pensa i escriu:

- Quins 5-10 serveis t'agradaria tenir?
- Quin dels 5 mòduls (M2-M5) t'interessa més?
- Quin problema t'agrada resoldre? (productivitat, automatització, dades, IoT, ...)
- Tens algun projecte concret en ment? (hort, domòtica, còpies de seguretat, ...)

Plantilla:

```markdown
# Visio a 6 mesos

## Serveis que vull tenir
1. Nextcloud (M2) - per tenir els meus fitxers sincronitzats
2. Gitea (M2) - per tenir un GitHub privat
3. Node-RED (M3) - per automatitzar
4. Grafana (M4) - per visualitzar dades
5. ...

## Modul prioritari
El M4 (Dades) perque vull aprendre a fer grafiques amb dades reals.

## Projecte concret
Vull mesurar la temperatura de l'hort de casa els avis. 
Hi ha 4 sectors amb sensors. Vull veure les dades a Grafana.

## Recursos adicionals
- Raspberry Pi Zero per posar al camp com a gateway LoRa.
- 4 sensors LoRa de temperatura + humitat.
- ...

## Reptes personals
- Vull aprendre Docker a fons.
- Vull automatitzar les còpies de seguretat.
- Vull poder accedir a tot des del mòbil.
```

## Pas 3: Primer pas concret (10 min)

Defineix el **primer pas concret** que faràs la setmana vinent. Petita, assolible, concreta:

- [ ] Acabar M2 cap 11 (File Browser).
- [ ] Comprar una Raspberry Pi Zero per al gateway LoRa.
- [ ] Instal·lar Grafana i fer una gràfica de CPU de la RPi.
- [ ] Qualsevol altra cosa concreta.

Afegeix-ho a `book/curs/M1/10-full-de-ruta/visio-6-mesos.md` amb data i acció clara.

**Important**: el primer pas ha de ser quelcom que puguis fer AQUESTA SETMANA, no algun dia. Si és massa gran, parteix-lo.

## Pas 4: Planifica l'arquitectura (10 min)

Dibuixa (amb ASCII art, draw.io, o a mà) l'arquitectura que vols tenir d'aquí 6 mesos. Exemple:

```
+----------+     +--------+     +----------+
| Sensors  +---->+ Gateway+--+  | ChirpStack|
| LoRa     |     | LoRa   |  |  | (broker)  |
+----------+     +--------+  |  +----+-----+
                              |       |
                              v       v
                          +---+---+   +--------+
                          | MQTT  +-->+InfluxDB|
                          | broker|   +----+---+
                          +-------+        |
                                            v
                                       +----+---+
                                       |Grafana |
                                       +--------+
```

Desa el dibuix (text o imatge) a `docs/arquitectura-futura.md` o `docs/arquitectura-futura.png`.

## Pas 5: Analitza el que et falta (5 min)

Per cada servei que vols afegir, respon:

1. Quina mida té la imatge Docker? (`docker image ls` un cop l'hagis vist a Docker Hub)
2. Quanta RAM consumeix en repòs?
3. Quin port utilitza?
4. Té sentit afegir-lo al BernatLab actual o caldria una màquina nova?

Fes una taula al `visio-6-mesos.md`:

| Servei | Mida imatge | RAM | Port | Recomanable? |
|--------|-------------|-----|------|--------------|
| Nextcloud | ~500 MB | 500 MB | 8080 | Si |
| Gitea | ~200 MB | 300 MB | 3000 | Si |
| InfluxDB | ~300 MB | 800 MB | 8086 | Potser |
| Grafana | ~400 MB | 300 MB | 3000 | Si |

## Pas 6: Compromet-te (5 min)

Al final del fitxer, escriu:

```markdown
## Compromisos

Data d'avui: YYYY-MM-DD

Em comprometo a:
- [ ] Fer [accio 1] abans del [data]
- [ ] Fer [accio 2] abans del [data]
- [ ] Revisar aquest pla el [data revisio]
```

## Pas 7: Documenta i commita (5 min)

```bash
cd ~/bernatlab
git add book/curs/M1/10-full-de-ruta/
git commit -m "Documenta inventari i visio a 6 mesos del BernatLab"
```

## Validació

Has acabat si:
- [ ] Inventari actual complet.
- [ ] Visió a 6 mesos redactada.
- [ ] Primer pas concret definit (assolible aquesta setmana).
- [ ] Arquitectura futura dibuixada.
- [ ] Taula d'anàlisi de serveis futurs.
- [ ] Compromisos concrets amb dates.
- [ ] Commit fet al repo.

## Per aprofundir

- Investiga awesome-selfhosted i tria 3 projectes nous que t'interessin.
- Llegeix sobre ChirpStack (LoRaWAN network server).
- Compara Home Assistant vs Node-RED per a automatització domèstica.
- Mira vídeos de "Home Server Tour" a YouTube per inspirar-te.
- Calcula el cost total del teu BernatLab ideal (hardware + energia + temps).
- Fes una enquesta entre amics per veure què voldrien ells.

## Ves un pas més enllà

**Repte avançat: ratxa de compromís**.

Molta gent abandona els projectes d'homelab al cap de 2-3 setmanes. Per evitar-ho, crea un sistema de "ratxa" que et recordi per què vas començar.

1. Crea `~/homelab/notes/motivacio.md`:

```markdown
# Per que estic construit el BernatLab?

## Data d'inici
2026-07-16

## Per que vaig començar
- Vull aprendre Linux de veritat, no sols teoria
- Vull tenir control de les meves dades
- Vull un projecte tecnic que em diverteixi
- Vull preparar-me per feines mes tecniques

## Que em motiva ara
- ...

## Que em fa por
- Que ho deixi estar
- Que es faci massa complicat
- Que trigui massa a veure resultats

## Petits victories fins ara
- [ ] M1 - He posat en marxa 5 serveis basics
- [ ] M2 - Tinc el meu propi núvol de fitxers
- [ ] M3 - He automatitzat alguna cosa
- [ ] M4 - Tinc grafiques amb dades reals
- [ ] M5 - Tinc sensors al camp

## Ratxa actual
- Dies consecutius treballant al BernatLab: 0
- Objectiu: 30 dies seguits
```

2. Crea un script `~/homelab/scripts/ratxa.sh` que actualitzi el recompte:

```bash
#!/bin/bash
DIA=$(date +%Y-%m-%d)
FITXER=~/homelab/notes/motivacio.md

# Comprova si ja has treballat avui
ULTIM=$(grep "Ultima sessio:" "$FITXER" 2>/dev/null | tail -1 | awk '{print $3}')

if [ "$ULTIM" != "$DIA" ]; then
  # Calcula la ratxa (simplificat)
  RATXA=$(grep "Dies consecutius" "$FITXER" | grep -oP '\d+')
  RATXA=$((RATXA + 1))

  # Actualitza
  sed -i "s/Dies consecutius.*/Dies consecutius: $RATXA/" "$FITXER"
  echo "" >> "$FITXER"
  echo "Ultima sessio: $DIA" >> "$FITXER"

  echo "Ratxa actual: $RATXA dies"
fi
```

3. Executa'l cada vegada que treballis al BernatLab.

4. Fes commit del sistema de ratxa.

Ara cada vegada que vegis el fitxer `motivacio.md` recordaràs per què vas començar, i la ratxa et farà vergonya de trencar-la. Això és tan important com qualsevol servei tècnic.
