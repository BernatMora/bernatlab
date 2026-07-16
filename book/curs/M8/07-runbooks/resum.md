# Resum - M8 Cap 7: Runbooks

## Per que importa

Quan tens un sistema, **sempre** arriba un moment en que algo falla. Si no estas preparat, el que fas es:
1. Entrar en panic.
2. Buscar a Google.
3. Provar coses aleatoriament.
4. Preguntar a algú.
5. Perdre hores o dies.

Si **tens runbooks**, el que fas es:
1. Obrir el runbook corresponent.
2. Seguir les instruccions pas a pas.
3. Solucionar en 5-30 minuts.

Un **runbook** es un document amb **procediments per a situacions especifiques**. Son la "memoria institucional" del teu sistema.

## Quins runbooks necessites

Per a un homelab, recomano tenir **almenys** aquests:

- **Tailscale down** - Si no pots accedir per Tailscale.
- **Portainer down** - Si Portainer no respon.
- **Disc ple** - Si la RPi es queda sense espai.
- **Contenidor no arranca** - Si un serveis cau.
- **Contrasenya oblidada** - Si no recordes cap contrasenya.
- **RPi no engega** - Si la RPi no arranca.
- **Backup i restauracio** - Com recuperar d'un desastre.
- **Actualitzacio segura** - Com actualitzar serveis sense trencar res.

## Estructura dun runbook

Cada runbook ha de tenir:

1. **Titol clar** - "Si X passa, fes Y"
2. **Símptomes** - Com saps que tens aquest problema
3. **Diagnòstic** - Com confirmar que es aquest problema
4. **Solució** - Pas a pas, amb comandes
5. **Validació** - Com saber que s'ha resolt
6. **Notes** - Casos especials, errors comuns

## Exemple: Tailscale Down

Mira el runbook que ja tens: `book/curs/recursos/recuperacio-emergencia-tailscale.md`.

Tots els altres runbooks haurien de seguir una estructura semblant.

## On guardar els runbooks

Opcions:
- **Dins del repo** (`book/curs/recursos/`) - ja en tens un.
- **A Obsidian** - si uses Obsidian per notes, crea un vault `runbooks/`.
- **Tots dos** - el runbook oficial al repo, copies a Obsidian per a acces rapid.

## Com crear un runbook

Quan tinguis un problema i el resolguis, **escriu el runbook**. Aquest es el secret:
- No esperis a tenir temps.
- Escriu-lo **mentre el recordes**.
- Inclou les comandes exactes.
- Inclou els errors que has vist.
- Inclou les solucions que NO han funcionat.

## Plantilla

```markdown
# Runbook: [Nom del problema]

> **Si tens [símptoma], segueix aquest runbook.**

## Símptomes

- [Com saps que tens aquest problema]

## Diagnòstic

Comandes per confirmar:
\`\`\`bash
# Comanda 1
# Comanda 2
\`\`\`

## Solució

### Pas 1: [Nom del pas]
\`\`\`bash
# Comandes
\`\`\`

### Pas 2: [Nom del pas]
[...]

## Validació

Com saber que s'ha resolt:
- [ ] Símptoma 1 ja no passa
- [ ] Comanda X retorna el resultat esperat
- [ ] ...

## Notes

- Casos especials
- Errors comuns
- Enllaços relacionats
```

## Exemple real: Disc ple

```markdown
# Runbook: Disc ple

## Símptomes
- "No space left on device" a les aplicacions
- Docker no arranca contenidors nous
- RPi molt lenta

## Diagnòstic
\`\`\`bash
df -h
du -sh /var/lib/docker/
\`\`\`

## Solució

1. Netejar imatges Docker antigues:
\`\`\`bash
docker image prune -a
docker volume prune
\`\`\`

2. Netejar logs:
\`\`\`bash
sudo journalctl --vacuum-time=7d
\`\`\`

3. Buscar fitxers grans:
\`\`\`bash
sudo find / -size +100M -type f
\`\`\`

## Validacio
- [ ] `df -h` mostra menys del 80% d'us
- [ ] Els contenidors arranquen correctament
```

## Connexions

- **M8 cap 6** - Els runbooks poden viure a Obsidian.
- **M9 del llibre** - Documentacio del projecte.
- **M22 del llibre** - Monitoritzacio 24/7 (et pot avisar d'un problema).

## Consells finals

- **Escriu els runbooks ANTES que passi el problema** (o immediatament despres).
- **Actualitza'ls** quan canvies coses.
- **Comparteix-los** amb familia si ells usen el sistema.
- **Fes n'hi una copia fora del servidor** (per si el servidor cau).
