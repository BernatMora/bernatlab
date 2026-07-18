# Resum - M8 Cap 3: Perfil SSH (~/.ssh/config)

## Per que importa

Ara cada vegada que vols connectar, escrius:
```bash
ssh bernat@100.x.y.z
```

Si tens varies maquines, o si vols canviar la clau, o si vols usar un port diferent, has de recordar totes les opcions. Es tedios.

El **fitxer `~/.ssh/config`** et permet crear **alses** (aliases). Despres nomes escrius:
```bash
ssh hortosona
```

I ja esta. M nomes, menys errors, mes rapid.

## Que es un perfil SSH

Es un fitxer de text pla on defines **configuracions per host**. El client SSH el llegeix automaticament cada vegada que connectes.

**Ubicacio**:
- Linux/macOS: `~/.ssh/config`
- Windows: `C:\Users\<usuari>\.ssh\config`

**Permissos** (Linux/macOS): `chmod 600 ~/.ssh/config` ( nomes el teu usuari pot llegir-lo).

## Exemple basic

Crea o edita el fitxer:
```
Host hortosona
    HostName 100.x.y.z
    User bernat
    IdentityFile ~/.ssh/id_ed25519
    IdentitiesOnly yes
```

Despres:
```powershell
ssh hortosona
# Equival a: ssh -i ~/.ssh/id_ed25519 bernat@100.x.y.z
```

## Multiples hosts

```
# RPi principal
Host hortosona
    HostName 100.x.y.z
    User bernat
    IdentityFile ~/.ssh/id_ed25519
    IdentitiesOnly yes

# Mac de casa
Host macbook
    HostName 100.86.178.51
    User bernatmora
    IdentityFile ~/.ssh/id_ed25519

# Servidor extern (si en tens un)
Host cloud
    HostName server.example.com
    User admin
    Port 2222
    IdentityFile ~/.ssh/cloud_key
```

Ara pots fer:
```bash
ssh hortosona
ssh macbook
ssh cloud
```

## Opcions utils

| Opcio | Que fa |
|---|---|
| `HostName` | IP o nom real del servidor |
| `User` | Usuari per defecte |
| `Port` | Port SSH (per defecte 22) |
| `IdentityFile` | Fitxer de clau privada |
| `IdentitiesOnly` | No provar altres claus automaticament |
| `ForwardAgent yes` | Permet fer ssh des del servidor |
| `Compression yes` | Comprimeix la connexio (util en xarxes lentes) |
| `ServerAliveInterval 60` | Manté la connexio viva |
| `LogLevel ERROR` | Menys soroll al terminal |

## Comodins (wildcards)

Pots fer regles per a multiples hosts:
```
Host *.local
    User bernat
    IdentityFile ~/.ssh/id_ed25519

Host 192.168.1.*
    User pi
    Port 22
```

## Connexions

- **M8 cap 1** - Les claus que hem configurat.
- **M8 cap 2** - MobaXterm tambe te perfils (pero separats).
- **M8 cap 5** - Scripts PowerShell que usen aquests noms.

## Errors habituals

- **Permissos massa oberts** - SSH rebutja el fitxer si es llegible per altres. A Windows normalment no passa, pero a Linux cal `chmod 600`.
- **Host duplicat** - Si tens dos blocs `Host hortosona`, nomes el primer s'aplica.
- **Indentacio** - Calen 4 espais (no tabuladors).
