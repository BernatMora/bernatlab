# Guia completa: Sincronitzar Hermes entre Windows i Mac via iCloud

> Com tenir les converses del Hermes disponibles als dos dispositius (Windows de la feina + Mac de casa) sense perdre res.

## Per que aquesta guia?

El Hermes desa **totes les converses** a una base de dades SQLite (`state.db`). Si vols continuar una sessio al Mac despres de treballar al Windows (o a l'inreves), necessites alguna manera de passar les dades d'un costat a l'altre.

Aquesta guia explica **el metode mes segur**: copiar el `state.db` entre dispositius passant per iCloud Drive, amb un script que automatitza el proces.

## On es guarden les converses?

### A Windows

```
C:\Users\iadmin\AppData\Local\hermes\
├── state.db              ← TOTES les converses (139 MB)
├── state.db-shm
├── state.db-wal
├── config.yaml           ← Configuracio
├── projects.db           ← Projectes
├── kanban.db             ← Kanban
├── memories/             ← Memoria personal
├── skills/               ← Habilitats
├── sessions/             ← Logs de peticions
└── ...
```

### A macOS

```
~/.local/share/hermes/
├── state.db
├── config.yaml
├── projects.db
├── ...
```

(o `~/Library/Application Support/hermes/` en algunes versions)

## El problema de sincronitzar en temps real

Si sincronitzes `state.db` **mentre Hermes es obert als dos costats**:

1. iCloud pot crear **conflicte copies** (file 2.db, file 3.db)
2. Les dues instancies **sobreescriuen** els canvis l'una de l'altra
3. La base de dades SQLite es pot **corrompre**

Per això la **recomanacio** es:

> **Sincronitza MANUALMENT** nomes quan un dels dos Hermes esta tancat.

## El flux recomanat

### Quan acabes una sessio al Windows

```powershell
# 1. TANCA el Hermes al Windows
# (clic dret a la safata del sistema -> Sortir)

# 2. Executa el script de sincronitzacio
cd C:\Users\iadmin\bernatlab
powershell -ExecutionPolicy Bypass -File bin\sync-hermes.ps1 -Direction push
```

Aixo copia el `state.db` actualitzat al iCloud.

### Quan vols continuar al Mac

```bash
# 1. TANCA el Hermes al Mac (si esta obert)
# 2. Espera 30 segons que iCloud acabi de sincronitzar
# 3. Copia el state.db del iCloud al lloc correcte
cp ~/Library/Mobile\ Documents/com~apple~CloudDocs/hermes/state.db ~/.local/share/hermes/state.db

# 4. Obre Hermes al Mac
```

## Que fa el script `sync-hermes.ps1`

### Mode `push` (Windows -> iCloud)

Copia del Windows al iCloud:

| Fitxer | Sincronitzat? | Per que |
|---|---|---|
| `state.db` | Si | Totes les converses |
| `config.yaml` | Si | La teva configuracio |
| `projects.db` | Si | Projectes |
| `kanban.db` | Si | Kanban |
| `memories/` | Si | Memoria personal (4 fitxers) |
| `skills/` | Si | Habilitats personalitzades |
| `auth.json` | **NO** | Conte tokens secrets - no comparteixis |

### Mode `pull` (iCloud -> Windows)

1. Fa un **backup** del que tens al Windows (`backups/pre-pull-YYYYMMDD-HHMMSS/state.db`)
2. Et demana **confirmacio** abans de sobreescriure
3. Copia el `state.db` del iCloud al Windows

## Instal·lacio

### A Windows

Ja esta fet. El script esta a:

```
C:\Users\iadmin\bernatlab\bin\sync-hermes.ps1
```

Pots:
- Executar-lo directament cada vegada
- Crear una **快捷方式 a l'escriptori** (acces directe)
- Afegir-lo al PATH per usar-lo des de qualsevol lloc

### A Mac

Necessites un script equivalent. Aqui el tens (en bash):

```bash
#!/bin/bash
# sync-hermes-mac.sh - Sincronitza Hermes entre Mac i iCloud

DIRECTION="${1:-push}"

HERMES_DIR="$HOME/.local/share/hermes"
ICLOUD_DIR="$HOME/Library/Mobile Documents/com~apple~CloudDocs/hermes"

echo ""
echo "================================================"
echo "  Hermes Sync - Mac <-> iCloud"
echo "================================================"
echo ""

if [ "$DIRECTION" = "push" ]; then
    echo "[PUSH] Copiant del Mac al iCloud..."
    mkdir -p "$ICLOUD_DIR"

    for f in state.db config.yaml projects.db kanban.db; do
        if [ -f "$HERMES_DIR/$f" ]; then
            cp "$HERMES_DIR/$f" "$ICLOUD_DIR/$f"
            echo "  [OK] $f"
        fi
    done

    for d in memories skills; do
        if [ -d "$HERMES_DIR/$d" ]; then
            cp -r "$HERMES_DIR/$d" "$ICLOUD_DIR/$d"
            count=$(find "$HERMES_DIR/$d" -type f | wc -l)
            echo "  [OK] $d/ ($count fitxers)"
        fi
    done

    echo ""
    echo "[DONE] Sincronitzat al iCloud"

elif [ "$DIRECTION" = "pull" ]; then
    echo "[PULL] Copiant del iCloud al Mac..."
    echo ""
    echo "ATENCIO: Aixo sobreescriura el teu state.db!"
    read -p "Continuar? (s/n): " confirm
    if [ "$confirm" != "s" ]; then
        echo "Cancelat."
        exit 0
    fi

    # Backup previ
    if [ -f "$HERMES_DIR/state.db" ]; then
        BACKUP_DIR="$HERMES_DIR/backups/pre-pull-$(date +%Y%m%d-%H%M%S)"
        mkdir -p "$BACKUP_DIR"
        cp "$HERMES_DIR/state.db" "$BACKUP_DIR/state.db"
        echo "[BACKUP] Backup fet a $BACKUP_DIR"
    fi

    # Copiar
    if [ -f "$ICLOUD_DIR/state.db" ]; then
        cp "$ICLOUD_DIR/state.db" "$HERMES_DIR/state.db"
        echo "[OK] state.db importat"
    else
        echo "[ERR] No sha trobat state.db al iCloud"
    fi
fi
```

Desa'l a `~/bin/sync-hermes.sh` i fes-lo executable:

```bash
chmod +x ~/bin/sync-hermes.sh

# Usar-lo
~/bin/sync-hermes.sh push   # Mac -> iCloud
~/bin/sync-hermes.sh pull   # iCloud -> Mac
```

## Important: Tancar Hermes ABANS de sincronitzar

Sempre, sempre, sempre:

1. **Tanca Hermes** al dispositiu origen
2. **Espera 5-10 segons** que acabi d'escriure a la BD
3. **Fes push/pull**
4. **Espera 30 segons** que iCloud acabi de pujar/baixar
5. **Obre Hermes** al dispositiu desti

Si no ho fas aixi, tindras problemes de sincronitzacio.

## Casos especials

### Si iCloud et dona un conflicte

Si iCloud et mostra "Conflicte versions" (file, file 2, file 3):

1. **Esborra totes** les versions mes antigues
2. **Deixa nomes** la mes recent (la que te la data mes nova)
3. **Comprova** que Hermes funciona correctament

### Si el state.db es corromp

Si Hermes no arranca o dona errors:

1. **Restaura** el backup mes recent de `backups/`
2. **Si no funciona**, descarrega una versio anterior del iCloud
3. **Ultima opcio**: esborra `state.db` i comença una sessio nova (perds l'historial pero recuperes el sistema)

### Si vols treballar simultaniament

**No es recomana**, pero si cal:

1. Usa el **PROJECT_STATE.md** i `handoff-YYYY-MM-DD.md` per sincronitzar context
2. **No comparteixis** state.db en temps real
3. Accepta que hi haura petites perdues d'informacio

## Comprovar que tot funciona

Despres de cada sincronitzacio, valida:

1. **Obre Hermes al nou dispositiu**
2. **Comprova** que veus les sessions antigues
3. **Comprova** que les memories (MEMORY.md, USER.md) son correctes
4. **Si algo falla**, restaura el backup

## Alternatives que hem considerat

| Metode | Pros | Contres |
|---|---|---|
| **iCloud Drive + script** (recomanat) | Natiu Apple, funciona offline, gratis | Cal fer manualment |
| **GitHub privat** | Ja tens infra, privat | Massa lent per state.db |
| **Tailscale + SMB** | Molt rapid | Cal configurar servidor |
| **Dropbox** | Semblant a iCloud | Cal compte a part |
| **Sincronitzacio automatica (symlink)** | Transparent | MOLT perillos, corrupcio segura |

## Resum rapid

**El flux es:**

1. Treballes al Windows
2. Quan acabes: tanca Hermes, executa `sync-hermes.ps1 -Direction push`
3. iCloud puja el state.db
4. Vas al Mac, esperes 30s
5. Al Mac: tanca Hermes (si esta obert), copia el state.db, obre Hermes
6. Continues treballant

**Cada vegada que canvies de dispositiu**, repeteix el proces.

## URL dels scripts

- **Windows:** https://github.com/BernatMora/bernatlab/blob/main/bin/sync-hermes.ps1
- **macOS:** (script d'aquesta guia, pots posarlo a `~/bin/sync-hermes.sh`)

## Si tens problemes

1. Comprova que **iCloud Drive esta actiu** al Mac i Windows
2. Comprova que tens **espai** al iCloud (139 MB pel state.db)
3. Comprova que **Hermes esta tancat** abans de sincronitzar
4. Si iCloud te **conflictes**, neteja'ls manualment
5. Si el **state.db es corrup**, restaura el backup

## Conclusio

Aquest metode es **manual pero segur**. No hi haura sincronitzacio automatica que pugui corrompre les dades.

Si vols automatitzar mes, considera muntar una **mquina virtual** o un **contenidor Docker** amb el teu entorn Hermes, accessible des de qualsevol lloc via Tailscale. Pero per ara, el metode manual es el mes robust.
