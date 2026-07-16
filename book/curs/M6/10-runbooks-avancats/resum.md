# Resum - Capitol 10: Runbooks avançats

## La idea clau

Els runbooks son documents que expliquen PAS A PAS com fer una tasca concreta del sistema. Son la diferencia entre "estic preparat per a tot" i "tinc un manual per cada situacio". Un bon runbook et permet actuar de forma ordenada, sense oblidar passos, fins i tot quan estas nervios perque alguna cosa falla a les 3 de la matinada.

## Que es exactament un runbook?

Un runbook es un document estructurat amb:

- **Titol**: que fa aquest runbook.
- **Quan usar-lo**: en quina situacio.
- **Requisits**: que necessites tenir abans.
- **Passos numerats**: l'ordre exacte.
- **Verificacio**: com saber que ha funcionat.
- **Rollback**: que fer si algo va malament.
- **Contactes**: qui avisar si necessites ajuda.

Diferencies amb un "tutorial":
- **Tutorial**: ensenya a fer alguna cosa. Volum: llibre. Per persones que APRENEN.
- **Runbook**: instruccions pas a pas. Volum: 1-2 pagines. Per persones que FANT servir-ho, sovint amb presses.

A una empresa professional, cada alerta automatica te el seu runbook. A una RPi casolana, pots tenir runbooks per a les 5-10 situacions que mes probablement et pasaran.

## Tipus de runbook

- **Runbook operatiu**: tasques de manteniment (netejar imatges, actualitzar, netejar logs).
- **Runbook d'incidencia**: que fer quan passa X (Home Assistant caigut, microSD plena, etc.).
- **Runbook de recuperacio**: com restaurar des de backup.
- **Runbook de desplegament**: com instal·lar/configurar un servei nou.
- **Runbook de seguretat**: que fer en cas d'intrusio o vulnerabilitat.

## Estructura recomanada

Per a un runbook d'incidencia, aquesta es una bona estructura:

```markdown
# Titol del runbook

## Resum
Quina situacio cobreix aquest runbook.

## Símptomes
Com saps que estàs en aquesta situacio.

## Severitat
- P1: servei critic caigut
- P2: degradacio important
- P3: problema menor

## Diagnostic pas a pas
1. Comprovar X amb Y comanda
2. Si veus A, continua. Si veus B, salta al pas 5.

## Solucio
1. Aplicar canvi X
2. Esperar Y segons
3. Verificar amb Z

## Verificacio
- [ ] El servei torna a respondre
- [ ] Les alertes s'han netejat
- [ ] Les metricas son normals

## Rollback
Si algo va malament:
1. Desfer canvi X
2. Tornar a la versio anterior
3. Avisar a Y

## Referencies
- Dashboard: http://...
- Documentacio oficial: https://...
- Issues coneguts: ...
```

## Exemple: Runbook "Contenidor caigut"

```markdown
# Runbook: Contenidor de Home Assistant caigut

## Resum
El contenidor de Home Assistant ha caigut i no es reinicia.

## Símptomes
- Alerta de Prometheus: "ContenidorCaigut"
- HA no respon al navegador
- Altres serveis del BernatLab funcionen

## Severitat
P1 si es durant el dia, P2 a la nit.

## Diagnostic
1. Comprovar l'estat:
   ssh rpi-bernatlab "docker ps -a | grep homeassistant"

2. Si esta "Exited", mirar els logs:
   ssh rpi-bernatlab "docker logs homeassistant --tail 50"

3. Si l'error es clar (ex: "port already in use"), anar directe a solucio.

4. Si l'error no es clar, mirar Grafana:
   http://192.168.1.50:3000/d/bernatlab
   - CPU? Memoria? Temperatura?

## Solucio
1. Si l'error es clar (config, port), editar docker-compose.yml:
   nano ~/bernatlab/docker-compose.yml

2. Tornar a aixecar:
   cd ~/bernatlab
   docker compose up -d homeassistant

3. Esperar 30 segons i verificar:
   curl http://localhost:8123

4. Si segueix caigut, mirar mes logs:
   docker logs homeassistant --tail 100

## Verificacio
- [ ] HA torna a carregar al navegador
- [ ] Grafana mostra memoria normal
- [ ] Prometheus mostra el contenidor UP
- [ ] Tinc automatitzacions funcionant

## Rollback
Si HA no arranca amb la nova config:
1. Editar docker-compose.yml i revertir
2. docker compose up -d homeassistant
3. Si encara falla, restaurar backup de /config
4. Si tot falla, obrir issue al GitHub de HA

## Contactes
- Forum HA: https://community.home-assistant.io
```

## Exemple: Runbook "Disc ple"

```markdown
# Runbook: Disc ple a la RPi

## Resum
El disc de la RPi esta al 100% i serveis comencen a fallar.

## Símptomes
- Alerta: "DiscPle"
- Contenidors que fallen misteriosament
- Logs amb "No space left on device"

## Solucio
1. Veure que ocupa mes espai:
   sudo du -sh /var/lib/docker/* | sort -h

2. Netejar imatges no usades:
   docker image prune -a
   docker volume prune
   docker system prune -a --volumes

3. Netejar logs:
   sudo journalctl --vacuum-size=100M
   sudo find /var/log -name "*.gz" -delete

4. Si encara cal, netejar paquets:
   sudo apt clean
   sudo apt autoremove

5. Verificar:
   df -h

## Verificacio
- [ ] df -h mostra menys del 80% usat
- [ ] Els contenidors tornen a funcionar
- [ ] L'alerta s'ha resolt

## Solucio a llarg termini
- Considerar moure a SSD si encara es microSD
- Configurar logrotate millor
- Moure volums a una particio separada
```

## Exemple: Runbook "Recuperar des de backup"

```markdown
# Runbook: Recuperar Home Assistant des de backup

## Quan usar
- Quan HA esta corrupte i no arranca
- Quan has de tornar a una versio anterior
- Despres d'un incident greu

## Requisits
- Backup recent a /backups/ha/
- Conexio SSH a la RPi
- 30-60 minuts

## Passos
1. Aturar HA:
   cd ~/bernatlab
   docker compose stop homeassistant

2. Fer backup de l'estat actual (per si de cas):
   sudo cp -r /opt/ha /opt/ha.abans-restaurar

3. Restaurar el backup:
   sudo rsync -avz /backups/ha/2026-05-12/ /opt/ha/
   sudo chown -R 1000:1000 /opt/ha

4. Tornar a aixecar HA:
   docker compose up -d homeassistant

5. Esperar 1 minut i verificar:
   curl http://localhost:8123

## Verificacio
- [ ] HA arranca
- [ ] Les automatitzacions funcionen
- [ ] Els dispositius es veuen
- [ ] L'historic esta present

## Si falla
- Comprovar permisos: ls -la /opt/ha
- Comprovar logs: docker logs homeassistant
- Tornar a la versio anterior: cp -r /opt/ha.abans-restaurar /opt/ha
```

## Postmortem: que fer DESPRES d'un incident

Un postmortem es un document que escrius DESPRES d'un incident important. La gracia es:

1. **Aprendre dels errors**: que ha fallat exactament?
2. **Evitar que torni a passar**: que cal canviar?
3. **Compartir el coneixement**: que sap tothom.

Estructura d'un bon postmortem:

```markdown
# Postmortem: [Titol de l'incident]

## Resum
Quina cosa ha passat, en 1-2 linies.

## Timeline
- 2026-05-12 03:15: Alerta rebuda: "Contenidor HA caigut"
- 2026-05-12 03:18: Comprovo logs, veig error de memoria
- 2026-05-12 03:25: Reinicio HA, torna a caure als 5 min
- 2026-05-12 03:35: Investigant, veig memory leak conegut a HA 2024.5
- 2026-05-12 04:00: Faig downgrade a 2024.4, problema resolt
- 2026-05-12 04:15: Torno a dormir

## Causa arrel
El bug introduit a HA 2024.5 que provoca memory leak en determinats components.

## Impacte
HA caigut durant 45 min, automatitzacions no funcionaven.

## Que ha anat be
- L'alerta s'ha disparat rapid
- He pogut accedir per SSH
- Tenia backup per si calia restaurar

## Que ha anat malament
- Hauria d'haver investigat mes abans d'actualitzar
- No tenia cap test automatitzat per detectar-ho

## Accions preventives
- [ ] Afegir regla d'alerta per memoria > 80% durant 10 min
- [ ] Llegir SEMPRE el CHANGELOG abans d'actualitzar
- [ ] Tenir un entorn de staging per proves
```

## Eines per gestionar runbooks

- **Obsidian**: notes en markdown, perfecte per runbooks.
- **Notion**: mes col·laboratiu pero cloud.
- **MkDocs**: generar una web amb els runbooks.
- **Markdown + Git**: versioning al repositori.
- **Gitea / GitHub Pages**: allotjar els runbooks com a wiki.

## Bones practiques

- **Escriu els runbooks QUAN tot va be**: en calent, amb el sistema funcionant, es quan tens la informacio. Enfred, amb el sistema caigut, no recordes res.
- **Fes-los curts**: 1-2 pagines per runbook. Si es mes llarg, parteix-lo.
- **Un runbook = una tasca**: no barregis temes.
- **Actualitza'ls regularment**: quan canvia una IP, un port, una eina.
- **Inclou exemples reals**: ordres reals que funcionen a la teva RPi.
- **Vincula'ls al monitoring**: des de les alertes de Telegram, link al runbook corresponent.

## Connexions amb altres capitols

- **M8 Cap 7** - Runbooks basics: introduccio als runbooks.
- **M6 Cap 9** - Troubleshooting: els runbooks son el resultat del troubleshooting.
- **M6 Cap 1** - Arquitectura 24/7: cada component pot tenir el seu runbook.
