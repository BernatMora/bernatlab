# Exercici pràctic — Capítol 10: Full de ruta

> 30-45 min · Real + planificació

## Objectiu
Planificar el teu BernatLab personal: quins serveis hi vols, amb quin ordre, quins objectius. Aquest exercici és més de reflexió que de teclejar ordres.

## Requisits
- Haver completat els capítols 1-9
- 30-45 minuts
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
```

## Pas 3: Primer pas concret (10 min)

Defineix el **primer pas concret** que faràs la setmana vinent. Petita, assolible, concreta:

- [ ] Acabar M2 cap 11 (File Browser).
- [ ] Comprar una Raspberry Pi Zero per al gateway LoRa.
- [ ] Instal·lar Grafana i fer una gràfica de CPU de la RPi.
- [ ] Qualsevol altra cosa concreta.

Afegeix-ho a `book/curs/M1/10-full-de-ruta/visio-6-mesos.md` amb data i acció clara.

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

## Pas 5: Documenta i commita (5 min)

```bash
cd ~/bernatlab
git add book/curs/M1/10-full-de-ruta/
git commit -m "Documenta inventari i visio a 6 mesos del BernatLab"
```

## Validació

Has acabat si:
- [ ] Inventari actual complet.
- [ ] Visió a 6 mesos redactada.
- [ ] Primer pas concret definit.
- [ ] Arquitectura futura dibuixada.
- [ ] Commit fet al repo.

## Per aprofundir

- Investiga awesome-selfhosted i tria 3 projectes nous que t'interessin.
- Llegeix sobre ChirpStack (LoRaWAN network server).
- Compara Home Assistant vs Node-RED per a automatització domèstica.
- Mira vídeos de "Home Server Tour" a YouTube per inspirar-te.
