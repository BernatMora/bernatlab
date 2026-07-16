# Exercici practic - M8 Cap 3: Perfil SSH

> 15-20 min - Al teu Windows

## Objectiu

Crear un perfil SSH per connectar-te a la RPi amb un sol mot.

## Requisits

- Claus SSH configurades (del capitol 1).
- Tailscale actiu.
- PowerShell obert.

## Pas 1: Crear el directori .ssh (2 min)

Si no existeix:

```powershell
mkdir $env:USERPROFILE\.ssh -Force
```

## Pas 2: Crear el fitxer config (5 min)

```powershell
notepad $env:USERPROFILE\.ssh\config
```

Escriu:

```
Host hortosona
    HostName 100.115.134.76
    User bernat
    IdentityFile ~/.ssh/id_ed25519
    IdentitiesOnly yes
    ServerAliveInterval 60
    Compression yes
```

Desa i tanca.

## Pas 3: Provar (2 min)

```powershell
ssh hortosona
```

Si tot va be, hauries d'estar dins la RPi sense teclejar res.

## Pas 4: Afegir un segon perfil (5 min)

Si tens un Mac amb Tailscale tambe:

```
Host macbook
    HostName 100.86.178.51
    User bernatmora
    IdentityFile ~/.ssh/id_ed25519
    IdentitiesOnly yes
```

Prova:
```powershell
ssh macbook
```

## Pas 5: Comodins (3 min)

Afegeix al final del fitxer:

```
Host pi
    HostName 100.115.134.76
    User bernat
    IdentityFile ~/.ssh/id_ed25519
```

Ara `ssh pi` tambe funciona (es un sinonim de `ssh hortosona`).

## Validacio

Has acabat si:
- [ ] El fitxer config existeix
- [ ] `ssh hortosona` funciona sense password
- [ ] Has afegit un segon perfil
- [ ] Has provat els comodins

## Per aprofundir

- Afegeix perfils per a altres serveis (Grafana, Portainer via tunnel).
- Usa `ServerAliveInterval` per evitar que la connexio es talli.
- Documenta els teus perfils en un README.
