# Exercici practic - M8 Cap 7: Runbooks

> 30-45 min - Inventari + crear un runbook

## Objectiu

Fer un inventari de runbooks que necessites i crear-ne un de basic.

## Requisits

- Coneixement basic del teu sistema
- 30-45 min

## Pas 1: Inventari de runbooks necessaris (10 min)

Llista tots els problemes que poden passar al teu BernatLab. Pensa en:

- Acces (Tailscale, SSH, claus)
- Hardware (disc ple, RPi no arranca, temperatura)
- Xarxa (WiFi, Tailscale, DNS)
- Aplicacions (Portainer, Uptime Kuma, Grafana)
- Dades (perdua de dades, backups, restauracio)

Per a cada un, escriu:
- Titol del runbook
- Simptomes
- Solucio rapida

Exemple:
```
- [x] Tailscale down - ja existeix
- [ ] Disc ple - per fer
- [ ] Portainer down - per fer
- [ ] Contenidor no arranca - per fer
- [ ] ...
```

## Pas 2: Crear el fitxer de runbooks (5 min)

Crea `book/curs/recursos/INDEX.md` amb l'inventari:

```markdown
# Index de Runbooks del BernatLab

Aquests son els runbooks disponibles per a situacions d'emergencia.

## Disponibles

- [recuperacio-emergencia-tailscale.md](recuperacio-emergencia-tailscale.md) - Si Tailscale falla i no pots accedir a la RPi.

## Pendants de crear

- [ ] disc-ple.md - Si el disc es queda ple
- [ ] portainer-down.md - Si Portainer no respon
- [ ] contenidor-no-arranca.md - Si un contenidor Docker cau
- [ ] rpi-no-engega.md - Si la RPi no arranca
- [ ] backups-com-fer.md - Com fer copies de seguretat
- [ ] actualitzacio-segura.md - Com actualitzar serveis
```

## Pas 3: Crear el runbook de disc ple (20 min)

Crea `book/curs/recursos/disc-ple.md`:

```markdown
# Runbook: Disc ple

> **Si tens "No space left on device" o el sistema va lent, segueix aquest runbook.**

## Símptomes

- "No space left on device" a les aplicacions
- Docker no pot arrancar contenidors nous
- La RPi va molt lenta
- Logs plens

## Diagnòstic

\`\`\`bash
# Espai total
df -h

# Mes gran primer
sudo du -sh /var/lib/docker/* | sort -h | tail -20

# Fitxers grans
sudo find / -type f -size +100M 2>/dev/null | head -20
\`\`\`

## Solucio

### Pas 1: Netejar imatges Docker no usades
\`\`\`bash
docker image prune -a
docker container prune
docker volume prune
docker network prune
\`\`\`

### Pas 2: Netejar logs antics
\`\`\`bash
sudo journalctl --vacuum-time=7d
\`\`\`

### Pas 3: Esborrar fitxers temporals
\`\`\`bash
sudo rm -rf /tmp/*
sudo apt clean
\`\`\`

### Pas 4: Si encara cal, ampliar la SD o afegir un SSD USB

## Validacio

- [ ] `df -h` mostra menys del 80% d'us
- [ ] Els contenidors arranquen correctament
- [ ] El sistema torna a la normalitat

## Notes

- Docker pot ocupar molt si tens moltes imatges.
- Els logs de journald poden ser un problema a llarg termini.
- Considera muntar un SSD USB per a dades pesades.
```

## Pas 4: Commit i push (5 min)

```bash
cd ~/bernatlab
git add book/curs/recursos/
git commit -m "Afegeix runbook: disc ple"
git push
```

## Validacio

Has acabat si:
- [ ] Inventari de runbooks creat
- [ ] Index de runbooks actualitzat
- [ ] Runbook de disc ple creat
- [ ] Commit i push fets

## Per aprofundir

- Crea un runbook per cada problema que has identificat.
- Configura alertes automatiques (Uptime Kuma) per a cada runbook.
- Fes revisions periodiques (cada 6 mesos) per actualitzar.
