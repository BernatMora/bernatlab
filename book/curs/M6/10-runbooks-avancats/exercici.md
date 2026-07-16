# Exercici practic - Capitol 10: Runbooks avançats

> 60-90 min · Real al teu sistema

## Objectiu

Crear 3-4 runbooks operatius per a les situacions mes probables del teu BernatLab, escriure un postmortem d'un incident del passat (o inventat), i organitzar-ho tot en un directori facil de mantenir. Acabaras amb un "manual d'operacions" del teu sistema.

## Requisits

- RPi funcionant
- 60-90 minuts
- Conexement del que tens corrent

## Pas 1: Crea l'estructura de directoris (5 min)

```bash
mkdir -p ~/bernatlab/runbooks/{incidents,operations,deployment,recovery}
ls -la ~/bernatlab/runbooks/
```

## Pas 2: Escriu el runbook "Contenidor caigut" (15 min)

Crea el fitxer:

```bash
nano ~/bernatlab/runbooks/incidents/01-contenidor-caigut.md
```

Basat en l'exemple del resum, adapta'l als TEUS serveis reals:

```markdown
# Runbook: Contenidor caigut

## Resum
Un contenidor Docker del BernatLab ha caigut i no es reinicia.

## Símptomes
- Alerta de Telegram: "ContenidorCaigut"
- Servei no respon al navegador
- Altres serveis funcionen OK

## Severitat
- P1: Home Assistant caigut durant el dia
- P2: Altres serveis, o a la nit

## Diagnostic
1. Comprovar quin contenidor ha caigut:
   docker ps -a | grep -v "Up "

2. Mirar els logs:
   docker logs NOM_CONTENIDOR --tail 50

3. Si es clar (port usat, error de fitxer), saltar a solucio.

## Solucio
1. Si es un error de configuracio:
   cd ~/bernatlab
   nano docker-compose.yml
   docker compose up -d NOM_CONTENIDOR

2. Si es un error sense causa evident:
   docker compose restart NOM_CONTENIDOR
   sleep 30
   docker logs NOM_CONTENIDOR --tail 20

3. Si segueix fallant, mira a Grafana:
   http://192.168.1.50:3000

## Verificacio
- [ ] El contenidor esta UP
- [ ] El servei respon
- [ ] L'alerta s'ha resolt
- [ ] Grafana mostra memoria normal

## Rollback
- Revertir canvis a docker-compose.yml
- Restaurar volum desde backup
- Reinstancia imatge: docker compose pull && docker compose up -d

## Contactes
- [Enllaç al dashboard](http://192.168.1.50:3000)
- [Enllaç a Uptime Kuma](http://192.168.1.50:3001)
```

## Pas 3: Escriu el runbook "Disc ple" (10 min)

```bash
nano ~/bernatlab/runbooks/incidents/02-disc-ple.md
```

```markdown
# Runbook: Disc ple a la RPi

## Resum
El disc esta al 100% i serveis comencen a fallar.

## Símptomes
- Alerta: "DiscPle"
- Logs: "No space left on device"
- Contenidors fallen misteriosament

## Solucio
1. Veure que ocupa mes espai:
   sudo du -sh /var/lib/docker/* | sort -h
   du -sh /opt/*

2. Netejar Docker:
   docker image prune -a -f
   docker volume prune -f
   docker system prune -a --volumes -f

3. Netejar logs:
   sudo journalctl --vacuum-size=100M
   sudo find /var/log -name "*.gz" -delete

4. Netejar apt:
   sudo apt clean
   sudo apt autoremove

5. Verificar:
   df -h

## Verificacio
- [ ] df -h mostra menys del 80%
- [ ] Contenidors funcionen
- [ ] L'alerta s'ha resolt

## Solucio a llarg termini
- Moure a SSD si encara es microSD
- Millorar logrotate
- Moure volums a particio separada
```

## Pas 4: Escriu el runbook "RPi no arranca" (10 min)

```bash
nano ~/bernatlab/runbooks/incidents/03-rpi-no-arranca.md
```

```markdown
# Runbook: La RPi no arranca

## Resum
La RPi esta connectada pero no respon ni per SSH ni per pantalla.

## Diagnostic
1. Comprovar alimentacio (LED vermell encès?)
2. Comprovar el cable de xarxa
3. Connectar pantalla per HDMI
4. Si veus text, el sistema arranca
5. Si no veus res, pot ser microSD

## Solucions
### Si no te corrent
- Provar un altre carregador (5V/3A minim)
- Provar un altre cable USB-C
- Connectar directament sense HUB

### Si te corrent pero no video
- Provar un altre cable HDMI
- Provar un altre port HDMI
- Esperar 60 segons (a vegades es lenta)

### Si arranca pero el sistema falla
- Entrar amb Ctrl+Alt+F1 per consola
- Login amb usuari/contrasenya
- Veure que ha fallat: dmesg | less

### Si la microSD esta corrupta
- Posar-la en un altre PC
- Muntar-la i copiar el que es pugui
- Reinstal·lar SO + restaurar backups

## Recuperacio des de zero
Si cal reinstal·lar:
1. Descarregar Raspberry Pi Imager
2. Instal·lar Raspberry Pi OS a una microSD nova
3. Configurar WiFi/Ethernet abans d'arrancar
4. Un cop dins: bash <(curl url/instalar-bernatlab.sh)
5. Restaurar backups
```

## Pas 5: Escriu un runbook operatiu (neteja) (10 min)

```bash
nano ~/bernatlab/runbooks/operations/01-neteja-setmanal.md
```

```markdown
# Runbook: Neteja setmanal del BernatLab

## Quan
Cada diumenge al mati (30 min)

## Passos
1. Executar script automatic:
   sudo /opt/bernatlab/maintenance.sh

2. Comprovar logs:
   sudo tail -20 /var/log/bernatlab-maintenance.log

3. Verificar que els serveis funcionen:
   docker ps
   curl http://192.168.1.50:3000

4. Revisar alertes rebudes la setmana a Telegram

5. Apuntar coses rares al journal:
   nano ~/bernatlab/JOURNAL.md

## Verificacio
- [ ] El sistema te mes espai que abans
- [ ] Tots els serveis responen
- [ ] Les alertes estan sota control
```

## Pas 6: Escriu un runbook de recuperacio (10 min)

```bash
nano ~/bernatlab/runbooks/recovery/01-restaurar-home-assistant.md
```

```markdown
# Runbook: Restaurar Home Assistant des de backup

## Quan usar
- HA no arranca despres d'un canvi
- Has de tornar a una versio anterior
- La microSD ha mort i reinstal·les

## Requisits
- Backup recent a /backups/ha/
- Conexio SSH a la RPi
- 30-60 minuts

## Passos
1. Aturar HA:
   cd ~/bernatlab
   docker compose stop homeassistant

2. Fer backup de l'estat actual:
   sudo cp -r /opt/ha /opt/ha.abans-restaurar

3. Restaurar:
   sudo rsync -avz /backups/ha/$(date +%Y-%m-%d)/ /opt/ha/
   sudo chown -R 1000:1000 /opt/ha

4. Tornar a aixecar:
   docker compose up -d homeassistant

5. Esperar 1 minut i verificar:
   curl http://localhost:8123

## Verificacio
- [ ] HA arranca
- [ ] Les automatitzacions funcionen
- [ ] Els dispositius es veuen

## Si falla
- Logs: docker logs homeassistant --tail 50
- Permissos: ls -la /opt/ha
- Tornar a la versio anterior
```

## Pas 7: Escriu un postmortem d'un incident (15 min)

```bash
nano ~/bernatlab/runbooks/postmortems/2026-05-12-disc-ple.md
```

```markdown
# Postmortem: Disc ple durant una nit

## Resum
A les 03:00, el sistema va deixar d'escriure logs perquè el disc estava al 100%. Home Assistant va deixar d'escriure l'historic.

## Timeline
- 2026-05-11 23:00: Sistema funcionant be
- 2026-05-12 03:15: Rebo alerta "DiscPle"
- 2026-05-12 03:20: Comprovo, df -h mostra 100% usat
- 2026-05-12 03:30: Executo neteja manual
- 2026-05-12 03:45: Disc al 75%, HA torna a funcionar
- 2026-05-12 04:00: Tot normalitzat

## Causa arrel
El contenidor de Prometheus estava fent logging excessiu per un bug a la configuracio. Els logs van omplir el volum.

## Impacte
- 45 min sense historic de HA
- Ningu a casa afectat (nit)

## Que ha anat be
- L'alerta s'ha disparat rapid
- He pogut accedir per SSH des del movil
- El runbook "Disc ple" ha funcionat perfecte

## Que ha anat malament
- Hauria d'haver vist la tendencia creixent a Grafana
- El logrotate no estava ben configurat
- No tenia alerta de "tendencia de disc ple"

## Accions preventives
- [ ] Millorar logrotate (aquesta setmana)
- [ ] Crear alerta "disc creixent mes de 5% al dia"
- [ ] Limitar el volum de logs de Prometheus
- [ ] Revisar el runbook i afegir mes opcions de neteja
```

## Pas 8: Crea l'index de runbooks (5 min)

```bash
nano ~/bernatlab/runbooks/README.md
```

```markdown
# Runbooks del BernatLab

## Incidents
- [Contenidor caigut](incidents/01-contenidor-caigut.md)
- [Disc ple](incidents/02-disc-ple.md)
- [RPi no arranca](incidents/03-rpi-no-arranca.md)

## Operations
- [Neteja setmanal](operations/01-neteja-setmanal.md)

## Recovery
- [Restaurar HA](recovery/01-restaurar-home-assistant.md)

## Postmortems
- [2026-05-12 Disc ple](postmortems/2026-05-12-disc-ple.md)

## Com usar aquests runbooks
1. Busca el runbook pel problema que tens
2. Segueix els passos en ordre
3. Si el runbook no existeix per aquest problema, crea'l DESPRES de resoldre
4. Documenta SEMPRE el que has fet en un postmortem
```

## Pas 9: Puja els runbooks al repositori (5 min)

```bash
cd ~/bernatlab
git add runbooks/
git commit -m "Add M6 runbooks"
```

(No facis push, nomes commit local segons la consigna.)

## Validacio

Has acabat si:

- [ ] Tens 3-4 runbooks d'incidents escrits.
- [ ] Tens 1 runbook operatiu (neteja).
- [ ] Tens 1 runbook de recuperacio.
- [ ] Tens 1 postmortem (real o inventat).
- [ ] Tens un README.md que indexa tots els runbooks.
- [ ] Els runbooks son REALISTES amb les teves dades reals (IPs, serveis, etc.).

## Per aprofundir

- Afegeix diagrames ASCII als runbooks per il·lustrar el flux.
- Crea un runbook per cada alerta del cap 4.
- Investiga MkDocs per generar una web amb els runbooks.
- Programa un check trimestral que revisi que tots els runbooks son actuals.
