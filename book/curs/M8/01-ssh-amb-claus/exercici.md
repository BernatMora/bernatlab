# Exercici practic - M8 Cap 1: SSH amb claus

> 30-45 min - Al teu PC Windows + RPi

## Objectiu

Configurar autenticacio per claus SSH entre el teu Windows i la RPi. Despres d'això, podràs entrar sense teclejar password cada vegada.

## Requisits

- Tailscale funcionant (per accedir a la RPi)
- Windows PowerShell
- Connexio a internet

## Pas 1: Comprovar si ja tens claus (2 min)

Primer, mira si ja tens claus generades:

```powershell
ls $env:USERPROFILE\.ssh\
```

Si tens fitxers `id_ed25519` o `id_rsa`, ja tens claus. **Compte**: si les sobreescrius, perds l'acces a altres servidors. Si tens dubtes, no generis noves.

Si **no tens**, pasa al pas 2.

## Pas 2: Generar el parell de claus (3 min)

```powershell
ssh-keygen -t ed25519
```

- **Where to save**: Enter (deixa el per defecte).
- **Passphrase**: posa'n una que recordis pero que no sigui trivial.

Verifica que sha creat:

```powershell
ls $env:USERPROFILE\.ssh\
```

Hauries de veure `id_ed25519` (privada) i `id_ed25519.pub` (publica).

## Pas 3: Comprovar la clau publica (1 min)

```powershell
cat $env:USERPROFILE\.ssh\id_ed25519.pub
```

Hauries de veure una linea que comenca per `ssh-ed25519 ...`. Es la teva clau publica, que pots compartir.

## Pas 4: Copiar la clau publica a la RPi (2 min)

```powershell
type $env:USERPROFILE\.ssh\id_ed25519.pub | `
  ssh bernat@100.x.y.z "mkdir -p ~/.ssh && chmod 700 ~/.ssh && cat >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"
```

Et demanara la **contrasenya** (l'ultim cop!). Accepta.

## Pas 5: Verificar que funciona (1 min)

Tanca la sessio PowerShell i obre una de nova. Despres:

```powershell
ssh bernat@100.x.y.z
```

Si tot va be, **no et demanara password** (o et demanara la passphrase de la clau un sol cop).

## Pas 6 (IMPORTANT): Deixar una porta oberta (2 min)

**Abans de desactivar el password**, verifica dues coses:

1. La clau funciona (pas 5).
2. No tens cap altre metode d'acces actiu (com una clau ja configurada anteriorment).

**ALERTA**: Si desactives el password i la clau no funciona, **perds l'acces** i necessitaries monitor + teclat a la RPi.

## Pas 7: Desactivar el password (5 min)

Si tot funciona, desactiva el password:

```bash
# A la RPi (un cop dins per SSH amb clau)
sudo nano /etc/ssh/sshd_config
```

Busca la linia:
```
#PasswordAuthentication yes
```

Canvia-la per:
```
PasswordAuthentication no
```

O afegeix-la al final del fitxer si no hi es.

Desa (Ctrl+O, Enter, Ctrl+X) i:

```bash
sudo systemctl restart ssh
```

## Pas 8: Test final (2 min)

Tanca la sessio SSH i reconnecta:

```powershell
ssh bernat@100.x.y.z
```

Si funciona, **felicitats**! Ara tens autenticacio per claus.

Si vols provar que el password **NO funciona**, pots fer:

```powershell
ssh -o PreferredAuthentications=password bernat@100.x.y.z
```

Hauria de donar error "Permission denied".

## Validacio

Has acabat si:
- [ ] Has generat un parell de claus.
- [ ] La clau publica esta copiada a la RPi.
- [ ] Pots entrar per SSH sense password.
- [ ] Has desactivat `PasswordAuthentication`.
- [ ] Has verificat que el password ja no funciona.

## Per aprofundir

- **ssh-agent** per no haver de teclejar la passphrase cada cop.
- **Copia la clau a altres dispositius** (el Mac, el mobil amb Termux).
- **Considera tenir una clau separada per altres servidors** (per si mai vols revocar-ne una).
