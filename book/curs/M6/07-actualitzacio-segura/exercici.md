# Exercici practic - Capitol 7: Actualitzacio segura

> 30-45 min · Real a la teva RPi

## Objectiu

Configurar actualitzacions automatiques de seguretat amb `unattended-upgrades`, instal·lar Watchtower per als contenidors Docker, i posar en practica una actualitzacio manual amb rollback. Acabaras amb un sistema que s'actualitza sol i que sap tornar enrrere si algo va malament.

## Requisits

- RPi amb Docker funcionant
- 30-45 minuts
- Conexio a internet

## Pas 1: Configura actualitzacions automatiques del sistema (10 min)

```bash
sudo apt update
sudo apt install -y unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades
```

Edita la configuracio:

```bash
sudo nano /etc/apt/apt.conf.d/50unattended-upgrades
```

Assegura't que aquestes linies hi son:

```
Unattended-Upgrade::Allowed-Origins {
    "origin=Debian,codename=${distro_codename},label=Debian-Security";
    "origin=Raspbian,codename=${distro_codename},label=Raspbian-Security";
};

Unattended-Upgrade::AutoFixInterruptedDpkg "true";
Unattended-Upgrade::MinimalSteps "true";
Unattended-Upgrade::Remove-Unused-Dependencies "true";
Unattended-Upgrade::Automatic-Reboot "false";
```

Comprova que funciona:

```bash
sudo unattended-upgrades --dry-run -d
```

Aixo nomes simula, no fa res. Hauries de veure "Les actualitzacions son xxx".

## Pas 2: Configura notificacio per correu o Telegram (5 min)

Si vols rebre un correu/Telegram quan hi ha actualitzacions, afegeix:

```
Unattended-Upgrade::Mail "bernat@exemple.com";
```

Per Telegram, es mes complicat (cal un script). Pots fer-te un cron que cada dia comprovi si hi ha hagut actualitzacions:

```bash
cat /var/log/unattended-upgrades/unattended-upgrades.log | tail -20
```

## Pas 3: Instal·la Watchtower (10 min)

Afegeix al `docker-compose.yml`:

```yaml
  watchtower:
    image: containrrr/watchtower:latest
    container_name: watchtower
    restart: unless-stopped
    user: "0:0"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    environment:
      - WATCHTOWER_CLEANUP=true
      - WATCHTOWER_POLL_INTERVAL=86400
      - WATCHTOWER_LABEL_ENABLE=true
    command:
      - '--label-enable'
      - '--include-stopped'
      - '--schedule'
      - '0 0 4 * * *'
```

```bash
cd ~/bernatlab
docker compose up -d watchtower
docker ps | grep watchtower
```

Watchtower s'executara cada dia a les 4:00 AM.

## Pas 4: Marca els teus serveis per Watchtower (5 min)

Per defecte Watchtower nomes toca els contenidors amb label. Edita el teu `docker-compose.yml` i afegeix labels als serveis que vulguis actualitzar automaticament:

```yaml
  homeassistant:
    image: homeassistant/home-assistant:stable
    labels:
      - "com.centurylinklabs.watchtower.enable=true"
    # ...

  grafana:
    image: grafana/grafana:latest
    labels:
      - "com.centurylinklabs.watchtower.enable=true"
    # ...

  # Base de dades: NO actualitzis automaticament
  influxdb:
    image: influxdb:2.7
    # Sense label
```

Regla: posa label nomes als serveis que:
- Son "stateless" (no guarden dades importants).
- Poden reiniciar-se sense perdre res.
- No canvien la base de dades.

```bash
docker compose up -d
```

## Pas 5: Comprova que Watchtower funciona (5 min)

Mira els logs:

```bash
docker logs watchtower
```

Hauries de veure quins contenidors ha detectat i si ha trobat actualitzacions.

Per forçar una comprovacio ara:

```bash
docker exec watchtower /watchtower --run-once
```

## Pas 6: Practica un rollback (10 min)

Per practicar el rollback, fes una "actualitzacio simulada" i torna enrrere:

1. Mira la versio actual d'un contenidor:

```bash
docker inspect grafana | grep -i version
```

2. Fes una actualitzacio manual:

```bash
docker pull grafana/grafana:10.4.0  # Una versio antiga coneguda
docker stop grafana
docker rm grafana
docker compose up -d grafana
```

3. Si algo va malament, torna a la nova:

```bash
docker pull grafana/grafana:latest
docker stop grafana
docker rm grafana
docker compose up -d grafana
```

L'important es que sapigues com tornar a la versio anterior rapid.

## Validacio

Has acabat si:

- [ ] `unattended-upgrades` esta configurat i funciona.
- [ ] Watchtower esta corrent i te el `schedule` posat.
- [ ] Has marcat els serveis adequats amb label de Watchtower.
- [ ] Has deixat sense label les bases de dades.
- [ ] Has practicat un rollback manual amb exit.
- [ ] Has mirat els logs de Watchtower i entens que fan.

## Per aprofundir

- Configura Dependabot al teu repositori GitHub del BernatLab.
- Investiga la diferencia entre Watchtower, Ouroboros i Diun.
- Crea un CHANGELOG.md al teu repositori amb les teves actualitzacions importants.
- Prova `apt-listbugs` per evitar actualitzacions amb bugs coneguts.
