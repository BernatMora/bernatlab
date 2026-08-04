# 🛠️ Guia pas a pas — Configurar eines M8 a la teva RPi

> Document practic per posar en marxa les 7 eines del modul M8 sobre la teva Raspberry Pi.
> Comenca per la part 1 (preparacio) i segueix l'ordre. Si vols saltar alguna, mira les dependencies al final.

## 🗺️ Ordre recomanat

| # | Eina | Temps | Dificultat | Per que
|---|------|-------|------------|--------
| 1 | Preparacio de la RPi | 5 min | Facil | Assegurar que tens acces
| 2 | SSH amb claus | 30 min | Mitja | Seguretat + practicitat
| 3 | Perfil SSH | 10 min | Facil | Noms curts per a connexions
| 4 | MobaXterm (Windows) | 20 min | Facil | SSH grafic + SFTP
| 5 | PowerToys Run | 15 min | Facil | Llancador rapid
| 6 | Scripts PowerShell | 30 min | Mitja | Alias per serveis
| 7 | Obsidian + Git | 45 min | Mitja | Notes del projecte
| 8 | Runbooks nous | 20 min | Facil | Documentar emergencies

**Total**: ~3 hores. Si tens menys temps, fes-ho en varies sessions.

---

## 1. Preparacio de la RPi (5 min)

Assegura't que tens la RPi accessible i pots fer-hi coses.

```bash
# Des del teu Windows (PowerShell)
ssh bernat@100.x.y.z
# o per hostname MagicDNS
ssh bernat@hortosona
```

Si no pots entrar, mira el runbook de Tailscale.

Comprova que tens eines basiques:

```bash
which curl wget git nano vim
```

Si en falta alguna:

```bash
sudo apt update
sudo apt install -y curl wget git nano vim
```

---

## 2. SSH amb claus (30 min)

L'objectiu es entrar a la RPi sense teclejar password cada vegada. Es mes segur i mes rapid.

### 2.1. Generar la clau al Windows

Obre PowerShell i executa:

```powershell
ssh-keygen -t ed25519
```

Et preguntara:
- **On desar la clau?** Deixa-ho per defecte: `C:\Users\usuari\.ssh\id_ed25519`
- **Passphrase?** Tria una bona. No la deixis buida.

Hauries de veure:
- `Your identification has been saved in ...id_ed25519`
- `Your public key has been saved in ...id_ed25519.pub`

### 2.2. Copiar la clau publica a la RPi

**Opcio A** (la mes facil):

```powershell
type $env:USERPROFILE\.ssh\id_ed25519.pub | ssh bernat@100.x.y.z "mkdir -p ~/.ssh && chmod 700 ~/.ssh && cat >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"
```

**Opcio B** (manual):
1. Llegeix la clau publica al teu PC: `cat ~\\.ssh\id_ed25519.pub`
2. Entra a la RPi amb password.
3. Afegeix la clau:

```bash
mkdir -p ~/.ssh
chmod 700 ~/.ssh
nano ~/.ssh/authorized_keys
# enganxa la clau, guarda amb Ctrl+O, Enter, Ctrl+X
chmod 600 ~/.ssh/authorized_keys
```

### 2.3. Provar que funciona

Tanca la sessio SSH i obre'n una de nova:

```powershell
ssh bernat@hortosona
```

Hauries d'entrar **només amb la passphrase** (no pas el password de la RPi). Si et torna a demanar el password, alguna cosa ha fallat.

---

## 3. Perfil SSH al Windows (10 min)

Volem poder fer `ssh hortosona` en comptes de `ssh bernat@100.x.y.z`.

Crea el fitxer `C:\Users\usuari\.ssh\config`:

```powershell
notepad $env:USERPROFILE\.ssh\config
```

Escriu:

```
Host hortosona
    HostName 100.x.y.z
    User bernat
    IdentityFile ~/.ssh/id_ed25519
    IdentitiesOnly yes
    ServerAliveInterval 60

Host macbook
    HostName 100.x.y.z
    User bernatmora
    IdentityFile ~/.ssh/id_ed25519
```

Desa i tanca. Ara:

```powershell
ssh hortosona
```

Si funciona, ja tens un perfil.

---

## 4. MobaXterm al Windows (20 min)

Per aixo necessites descarregar MobaXterm (gratis) i crear una sessio.

### 4.1. Descarregar i instal·lar

Ves a https://mobaxterm.mobatek.net/ i descarrega la versio **Home Edition** (gratis).

### 4.2. Crear una sessio SSH

1. Obre MobaXterm
2. Click a **Session** (a dalt a l'esquerra)
3. Click a **SSH**
4. Configura:
   - **Remote host**: 100.x.y.z
   - **Specify username**: bernat
   - **Port**: 22
   - **Use private key**: navega a `C:\Users\usuari\.ssh\id_ed25519`
5. Click **OK**
6. Et demanara la passphrase de la clau. Marca **Remember passphrase** si vols que no te la torni a demanar.

Ara tens una sessio SSH grafica amb SFTP integrat. A l'esquerra pots:
- Veure els fitxers de la RPi
- Arrossegar fitxers entre Windows i RPi
- Editar fitxers remots amb el teu editor preferit

---

## 5. PowerToys Run (15 min)

PowerToys Run es el llancador d'aplicacions tipus Spotlight per a Windows.

### 5.1. Instal·lar PowerToys

Opcio A (winget, la mes rapida):

```powershell
winget install Microsoft.PowerToys
```

Opcio B (manual):
1. Vés a https://learn.microsoft.com/en-us/windows/powertoys/
2. Click a **Install now**

### 5.2. Usar-lo

1. PowerToys ha de correr a la safata del sistema (icono verd/blau)
2. Prems **Alt+Space**
3. Apareceix una barra de cerca al centre de la pantalla
4. Escriu el que busques:
   - `chrome` obre Chrome
   - `code` obre VS Code
   - `5*9` calcula 45
   - `100.x.y.z` obre el Portainer
   - `> ssh hortosona` executa una comanda

---

## 6. Scripts PowerShell (30 min)

Volem tenir ordres curts per accedir al BernatLab.

### 6.1. Crear el directori bin

```powershell
mkdir C:\Users\usuari\bin -Force
```

### 6.2. Crear el fitxer bernatlab.ps1

```powershell
notepad C:\Users\usuari\bin\bernatlab.ps1
```

Enganxa aquest contingut (adapta les IPs si cal):

```powershell
# BernatLab - acces rapid
function sshbl { ssh bernat@100.x.y.z }
function bl-portainer { Start-Process "https://100.x.y.z:9443" }
function bl-kuma { Start-Process "http://100.x.y.z:3001" }
function bl-homepage { Start-Process "http://100.x.y.z:3000" }

Set-Alias blport bl-portainer
Set-Alias blkuma bl-kuma
Set-Alias blhome bl-homepage
Set-Alias blbl sshbl

function bl-status { ssh bernat@100.x.y.z 'docker ps --format "table {{.Names}}\t{{.Status}}"' }
function bl-logs { param([string]$name) ssh bernat@100.x.y.z "docker logs $name --tail 50" }
```

Desa.

### 6.3. Configurar el perfil PowerShell

```powershell
Test-Path $PROFILE
```

Si retorna False:

```powershell
New-Item -Path $PROFILE -ItemType File -Force
```

Despres, afegeix el dot-source al perfil:

```powershell
Add-Content $PROFILE '. C:\Users\usuari\bin\bernatlab.ps1'
```

### 6.4. Si tens errors de politica

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 6.5. Tanca i obre PowerShell. Prova:

```powershell
blbl        # connecta a la RPi (amb clau, sense password)
blkuma      # obre Uptime Kuma al navegador
blport      # obre Portainer
blhome      # obre Homepage
bl-status   # veure l'estat dels teus 4 contenidors
bl-logs portainer  # veure els ultims 50 logs de Portainer
```

---

## 7. Obsidian + Git (45 min)

Per prendre notes del projecte i tenir-les sincronitzades.

### 7.1. Descarregar Obsidian

Ves a https://obsidian.md/ i descarrega la versio per a Windows.

### 7.2. Crear el vault

1. Obre Obsidian
2. Click a **Create new vault**
3. Nom: `BernatLab`
4. Ubicacio: `C:\Users\usuari\obsidian\bernatlab\`
5. Click **Create**

### 7.3. Configurar-lo

1. Settings > Appearance > Theme: prova el que mes t'agradi
2. Settings > Core plugins > activa **Daily notes** i **File recovery**
3. Per a mes funcionalitat, obre la comunitat de plugins i instal·la:
   - **Calendar**
   - **Dataview** (consultes tipus base de dades)
   - **Excalidraw** (dibuixos a ma)
   - **Spaced Repetition** (per repasar el curs)

### 7.4. Crear les primeres notes

Crea aquestes notes inicials:

**00-Index.md**:

```
# BernatLab - Index

Benvingut al vault del projecte BernatLab.

## Estructura

- [[arquitectura]]
- [[runbooks]]
- [[deures]]
```

**arquitectura.md**:

```
# Arquitectura del BernatLab

- RPi 4 (4 GB) amb Debian 13
- Docker amb 3-5 serveis
- Tailscale per a acces remot
- IP Tailscale: 100.x.y.z
- Veure [[runbooks]]
```

### 7.5. Inicialitzar Git

Obre PowerShell:

```powershell
cd C:\Users\usuari\obsidian\bernatlab
git init
git add .
git commit -m "Inici del vault BernatLab"
```

---

## 8. Runbooks nous (20 min)

Documenta els problemes que has tingut. Tots els runbooks son a `book/curs/recursos/`.

### 8.1. Inventari de runbooks que necessites

Mira el fitxer `book/curs/recursos/INDEX.md` per veure quins ja existeixen.

### 8.2. Crear-ne un de nou

Exemple: runbook per al disc ple:

Crea `book/curs/recursos/disc-ple.md`:

```
# Runbook: Disc ple

> Si tens 'No space left on device' o el sistema va lent, segueix aquest runbook.

## Simptomes
- 'No space left on device' a les aplicacions
- Docker no pot arrancar contenidors nous
- La RPi va molt lenta

## Diagnostic
```bash
df -h
sudo du -sh /var/lib/docker/* | sort -h | tail -20
```

## Solucio

### Pas 1: Netejar Docker
```bash
docker image prune -a
docker container prune
docker volume prune
```

### Pas 2: Netejar logs
```bash
sudo journalctl --vacuum-time=7d
```

## Validacio
- [ ] df -h mostra menys del 80% dus
- [ ] Els contenidors arranquen correctament
```

---

## 🆘 Si tens problemes

### SSH no funciona amb clau

1. Comprova els permisos a la RPi:
```bash
ls -la ~/.ssh/
# authorized_keys ha de ser 600
# .ssh ha de ser 700
```

2. Mira els logs:
```bash
sudo tail -f /var/log/auth.log
```

3. Comprova que la clau publica esta ben copiada:
```bash
cat ~/.ssh/authorized_keys
# Ha de contenir la clau que has generat al Windows
```

### PowerShell no carrega el perfil

1. Comprova la ruta del perfil:
```powershell
$PROFILE
```

2. Comprova que el fitxer existeix i conte el dot-source:
```powershell
Get-Content $PROFILE
```

3. Si tens errors, executa directament:
```powershell
. C:\Users\usuari\bin\bernatlab.ps1
```

### MobaXterm no troba la clau

1. Comprova que el fitxer .ssh/id_ed25519 existeix
2. A la configuracio de la sessio, navega explicitament al fitxer
3. Si tens passphrase, assegura't que MobaXterm la recorda

### PowerToys no respon a Alt+Space

1. Comprova que PowerToys esta corrent a la safata del sistema
2. A Settings > PowerToys Run, comprova la tecla d'acces
3. Reinstalla si cal

---

## Resum final

Despres de seguir aquesta guia, tindras:

- [ ] **RPi accessible** amb clau SSH (sense password)
- [ ] **Perfil SSH** al Windows (noms curts)
- [ ] **MobaXterm** instal·lat amb sessio persistent
- [ ] **PowerToys Run** funcionant (Alt+Space)
- [ ] **Scripts PowerShell** amb alies per serveis
- [ ] **Obsidian** amb vault del BernatLab
- [ ] **Runbooks nous** documentant problemes nous

Tot plegat et portara unes 3 hores, pero un cop fet, **tot sera mes rapid** durant mesos.