# Resum — M8 Cap 1: SSH amb claus (autenticacio sense password)

## Per que importa

Ara entres a la RPi amb **password** cada vegada. Te una mica d'inconvenient:
- Has de teclejar-la cada cop (tedios).
- Es pot atacar per **brute force** (algú provant milers de passwords).
- Si la contrasenya es filtra, perds l'acces.

Les **claus SSH** resolen tot això:
- **Mes comode**: no cal teclejar res (un cop configurada).
- **Mes segur**: la clau es de 4096 bits, matematicament impossible de trencar.
- **Automatitzable**: pots fer scripts que entrin sense intervencio humana.

## Que es una clau SSH

Es un parell de fitxers:
- **Privada** (`id_ed25519`): la GUARDES tu, nomes al teu PC. No la comparteixis MAI.
- **Publica** (`id_ed25519.pub`): la copies al servidor. Es publica, pero nomes serveix per **verificar** que tens la privada.

Com funciona (simplificat):
1. El servidor envia un **repte** (un numero aleatori xifrat amb la teva clau publica).
2. El teu PC el **desxifra** amb la teva clau privada i el retorna.
3. El servidor verifica que es correcte.
4. Si ho es, entres sense password.

**Analogia**: la clau publica es com un **candau obert** que pots deixar a qualsevol lloc. La clau privada es l'**unica clau** que pot obrir-lo.

## Com es fa (pas a pas)

### 1. Generar el parell de claus (al Windows)

Obre **PowerShell** i executa:

```powershell
ssh-keygen -t ed25519
```

Et preguntara:
- **Where to save**: deixa el per defecte (`C:\Users\iadmin\.ssh\id_ed25519`).
- **Passphrase**: posa'n una que recordis. Es la **contrasenya de la clau**, no pas la del servidor.

Si tot va be, veuras:
```
Your identification has been saved in C:\Users\iadmin\.ssh\id_ed25519
Your public key has been saved in C:\Users\iadmin\.ssh\id_ed25519.pub
```

### 2. Copiar la clau publica a la RPi

Un cop (entra amb password l'ultim cop):

```powershell
type $env:USERPROFILE\.ssh\id_ed25519.pub | `
  ssh bernat@100.115.134.76 "mkdir -p ~/.ssh && chmod 700 ~/.ssh && cat >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"
```

Aixo:
- Crea `.ssh/` a la RPi si no existeix.
- Afegeix la teva clau publica a `authorized_keys`.
- Posa els permisos correctes (important! SSH es exigent amb permisos).

### 3. Desactivar l'acces per password (a la RPi)

Un cop verificat que funciona, **desactiva el password** a la RPi:

```bash
sudo nano /etc/ssh/sshd_config
```

Canvia o afegeix:
```
PasswordAuthentication no
PubkeyAuthentication yes
```

Desa (Ctrl+O, Enter, Ctrl+X) i reinicia SSH:

```bash
sudo systemctl restart ssh
```

**Compte**: si tens altres usuaris o altres maquines, deixa'ls un temps abans de desactivar el password.

### 4. Provar

Des de PowerShell:

```powershell
ssh bernat@100.115.134.76
```

Si tot va be, **no et demanara res** (o et demanara la passphrase de la clau un sol cop per sessio).

## Avantatges

- **No mes passwords** — la clau es matematicament impossible de trencar per brute force.
- **Multiples maquines** — pots copiar la clau privada a tots els teus dispositius (i borrar-la remotament si la perds).
- **Automatitzacio** — scripts poden entrar sense que tu hi siguis.
- **Auditoria** — el servidor sap exactament quina clau ha entrat (rastreable).

## Connexions amb altres capitols

- **M4 del llibre** — Tailscale ja usa claus per a l'autenticacio entre nodes.
- **M5 del llibre** — Seguretat: les claus son la base de tot.
- **M8 cap 2** — Com utilitzar MobaXterm amb les claus.

## Errors habituals

- **Permissions mal posats** — SSH rebutja claus amb permisos massa oberts. Solucio: `chmod 700 ~/.ssh && chmod 600 ~/.ssh/authorized_keys`.
- **Clau copiada malament** — verifica que el contingut de `id_ed25519.pub` sha copiat be al `authorized_keys`.
- **PasswordAuthentication no desactivat be** — potser tens un altre client SSH que encara envia password.

## Per que ed25519 i no RSA

- **ed25519** es mes modern, mes segur, i mes rapid.
- **RSA** es el classic pero te limitacions de mida.
- **La comunitat Linux ha adoptat ed25519** com a estandard.
