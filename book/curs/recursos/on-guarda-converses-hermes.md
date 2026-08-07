# On es guarden les converses del Hermes

> Guia completa per trobar les converses del Hermes al Mac de casa o a qualsevol dispositiu.

## Resum rapid

| Tipus de dada | Ubicacio | Format |
|---|---|---|
| **Converses completes** | `state.db` (a `AppData/Local/hermes/`) | SQLite |
| **Logs de peticions** | `sessions/*.json` | JSON |
| **Memoria personal** | `memories/*.md` | Markdown |
| **Habilitats (skills)** | `skills/` | Directori amb `.md` |
| **Projectes** | `projects.db` | SQLite |
| **Configuracio** | `config.yaml` | YAML |
| **Logs generals** | `logs/` | Logs |

## A Windows (aquest PC)

```
C:\Users\iadmin\AppData\Local\hermes\
├── state.db                    ← LA BASE DE DADES PRINCIPAL (139 MB)
├── state.db-shm
├── state.db-wal
├── state.db.pre-update-*.bak  ← Backups abans d'actualitzacions
├── config.yaml                 ← Configuracio principal
├── .hermes_history             ← Historial shell
├── sessions/                   ← Request dumps (JSON)
├── memories/                   ← Memoria personal (MEMORY.md, USER.md)
├── skills/                     ← 686 habilitats
├── projects.db                 ← Base de dades dels projectes
├── kanban.db                   ← Base de dades del kanban
├── verification_evidence.db    ← Evidencia de verificacions
├── hermes-agent/               ← Codi del agent
├── logs/                       ← Logs generals
├── cron/                       ← Tasques programades
├── backups/                    ← Backups
└── ... (moltes mes carpetes)
```

## A macOS / Linux

```
~/.local/share/hermes/
├── state.db
├── config.yaml
├── sessions/
├── memories/
├── skills/
└── ...
```

**O tambe pot ser:**
```
~/Library/Application Support/hermes/   ← macOS (algunes versions)
```

## Com veure les converses

### Opcio 1: Eina `session_search` del propi Hermes

Quan estiguis dins d'una sessio de Hermes:

```
"busca a les sessions anteriors sobre [tema]"
```

O utilitza directament la eina:
- `session_search(query="bernatlab")` — busca a totes les sessions

### Opcio 2: Obrir la base de dades directament

Pots obrir `state.db` amb qualsevol client SQLite (DB Browser for SQLite, sqlite3 CLI):

```bash
# A macOS amb sqlite3
sqlite3 ~/Library/Application\ Support/hermes/state.db

# Llistar taules
.tables

# Veure l'esquema d'una taula
.schema messages

# Buscar converses recents
SELECT datetime(timestamp/1000, 'unixepoch'), role, content 
FROM messages 
ORDER BY timestamp DESC 
LIMIT 20;
```

### Opcio 3: Backup complet

Si vols fer un backup abans de netejar o traslladar:

**A Windows:**
```powershell
# Backup del estat complet
$dst = "C:\Users\iadmin\Desktop\hermes-backup-$(Get-Date -Format 'yyyyMMdd').zip"
Compress-Archive -Path "$env:LOCALAPPDATA\hermes\*" -DestinationPath $dst
```

**A macOS:**
```bash
# Backup complet
dst=~/Desktop/hermes-backup-$(date +%Y%m%d).tar.gz
tar -czf "$dst" -C ~/.local/share/hermes .

# O mes simple amb rsync
rsync -av ~/.local/share/hermes/ ~/Desktop/hermes-backup/
```

## Per sincronitzar entre Windows i Mac

### Opcio A: GitHub (recomanat)

Si tens el repo `bernatlab` amb tota la documentacio, pots:
1. Fer `git pull` al Mac per obtenir l'estat dels projectes
2. Documentar les converses importants com a `handoff-YYYY-MM-DD.md`
3. Fer `git push` per sincronitzar

### Opcio B: iCloud Drive / Dropbox

1. Mou la carpeta `hermes/` a iCloud Drive
2. Crea un symlink:
   ```bash
   # macOS
   ln -s ~/Library/Mobile\ Documents/com~apple~CloudDocs/hermes ~/.local/share/hermes
   ```

### Opcio C: Tailscale + SMB

1. Comparteix la carpeta per xarxa (SMB o NFS)
2. Accedeix des del Mac via Tailscale

## Fitxers mes importants

Si nomes vols copiar **el minim** per continuar treballant:

| Fitxer | Per que |
|---|---|
| `state.db` | Totes les converses (139 MB) |
| `config.yaml` | La teva configuracio (16 KB) |
| `memories/*.md` | Les notes de memoria |
| `auth.json` | Tokens d'autenticacio (10 KB) — **NO compartir** |
| `skills/` | Les teves habilitats personalitzades |
| `projects.db` | Els teus projectes |

## On van les imatges

Les imatges que comparteixo amb tu (com `composer-images/`) van a:

```
~/AppData/Roaming/hermes/composer-images/    (Windows)
~/Library/Application Support/hermes/composer-images/  (macOS)
```

## On van els audios (TTS)

```
~/AppData/Local/hermes/audio_cache/
~/AppData/Local/hermes/voice-memos/
```

## Conclusio

Per continuar la conversa al Mac:

1. **Obre Hermes al Mac** (ja tindras un altre `state.db` buit)
2. **Copia l'handoff** de la sessio actual com a context
3. **Documenta** les converses importants al repo BernatLab (ja ho fem!)

No cal que sincronitzis TOTA la base de dades. Només cal que:
- Tinguis el `PROJECT_STATE.md` actualitzat (ja el tens)
- Tinguis el `handoff-YYYY-MM-DD.md` si cal (ja el tens del 2026-07-17)
- Documentis les decisions importants al repo

Aixi el Mac pot continuar treballant amb el context necessari sense necessitat de sincronitzar les converses completes.
