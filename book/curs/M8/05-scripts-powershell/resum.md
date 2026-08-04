# Resum - M8 Cap 5: Scripts d'alies al PowerShell

## Per que importa

PowerToys Run et permet buscar aplicacions. Pero per a **ordres personalitzades** (com `ssh hortosona` o obrir Portainer al navegador), necessites **funcions i alies al PowerShell**.

Aixo et permet tenir **una sola lletra** per a cada cosa que fas sovint.

## Que es un script d'alies

Es un **fitxer `.ps1`** (PowerShell) que defineix funcions i alies. PowerShell el carrega automaticament a l'iniciar si esta ben configurat.

## El fitxer $PROFILE

PowerShell te un **perfil** que es carrega a cada inici. Es un fitxer `.ps1` especial.

Per veure on es:
```powershell
echo $PROFILE
```

Per defecte, a Windows es a:
```
C:\Users\<usuari>\Documents\PowerShell\Microsoft.PowerShell_profile.ps1
```

Si no existeix, cal crear-lo:
```powershell
# Crea la carpeta si no existeix
mkdir (Split-Path $PROFILE) -Force

# Crea el fitxer buit
New-Item -Path $PROFILE -ItemType File -Force
```

## Funcions utils per al BernatLab

Crea un fitxer `C:\Users\usuari\bin\bernatlab.ps1` amb el següent:

```powershell
# Conexions SSH
function ssh-bernatlab { ssh bernat@100.x.y.z }
Set-Alias sshbl ssh-bernatlab

function ssh-macbook { ssh bernat@100.x.y.z }
Set-Alias sshmac ssh-macbook

# Obrir serveis al navegador
function bl-portainer { Start-Process "https://100.x.y.z:9443" }
function bl-kuma { Start-Process "http://100.x.y.z:3001" }
function bl-homepage { Start-Process "http://100.x.y.z:3000" }
function bl-grafana { Start-Process "http://100.x.y.z:3002" }

# Dreces curtes
Set-Alias portainer bl-portainer
Set-Alias kuma bl-kuma
Set-Alias homepage bl-homepage
Set-Alias grafana bl-grafana

# BernatLab complet
function bl { 
    Start-Process "https://bernatmora.github.io/bernatlab/"
}
function hort { 
    Start-Process "https://bernatmora.github.io/hort-osona/"
}

# Comandes utils
function bl-status { 
    ssh bernat@100.x.y.z 'docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"'
}
function bl-logs { 
    param([string]$name)
    ssh bernat@100.x.y.z "docker logs $name --tail 50"
}
function bl-restart { 
    param([string]$name)
    ssh bernat@100.x.y.z "docker restart $name"
}
```

## Carregar el fitxer

Per que es carregui automaticament, afegeix al `$PROFILE`:

```powershell
. C:\Users\usuari\bin\bernatlab.ps1
```

Aixo es un "dot-source" - carrega les funcions al perfil actual.

## Us

Ara pots fer:

```powershell
sshbl       # Connecta a la RPi
kuma        # Obre Uptime Kuma al navegador
portainer   # Obre Portainer
hort        # Obre Hort Osona
bl          # Obre el BernatLab

# Estadistiques
bl-status   # Estat de tots els contenidors
bl-logs -name portainer  # Ultims 50 logs de Portainer
bl-restart -name kuma    # Reinicia Uptime Kuma
```

## Avantatges

- **Memorable** - una sola lletra o paraula curta.
- **Rapid** - no cal recordar URLs.
- **Compartible** - el fitxer es pot sincronitzar entre PCs.
- **Personalitzable** - pots afegir el que vulguis.

## Connexions

- **M8 cap 1** - Les claus SSH que usen aquestes funcions.
- **M8 cap 3** - El perfil SSH que permet `ssh hortosona` en comptes de la IP.

## Errors habituals

- **Politiques d'execucio** - Si PowerShell no carrega el perfil, pot ser la politica. Solucio: `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser`.
- **Ordre de carrega** - El perfil ha d'existir abans no el puguis modificar. Usa `New-Item` per crear-lo.
- **No es desa** - Has de desar el fitxer amb extensio `.ps1` i estar al directori correcte.
