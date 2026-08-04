# Respostes - M8 Cap 3: Perfil SSH

## Pregunta 1: Ubicacio del perfil SSH al Windows?

**Resposta correcta**: C:\Users\<usuari>\.ssh\config.

**Explicacio**: Es la mateixa ruta que a Linux pero amb el format Windows. La variable `$env:USERPROFILE` apunta a `C:\Users\bernat` (o el teu usuari).

---

## Pregunta 2: Opcio per al nom del perfil?

**Resposta correcta**: Host.

**Explicacio**: La paraula `Host` no es el servidor real - es l'**alia** que escriuràs per connectar. El servidor real es `HostName`.

---

## Pregunta 3: Opcio per la IP?

**Resposta correcta**: HostName.

**Explicacio**: Pot ser una IP o un nom DNS. MagicDNS de Tailscale tambe funciona aqui.

---

## Pregunta 4: Opcio per la clau privada?

**Resposta correcta**: IdentityFile.

**Explicacio**: Es la ruta a la clau privada (mai la publica). La ruta pot ser absoluta o relativa (~/.ssh/...).

---

## Pregunta 5: Permissos del config a Linux?

**Resposta correcta**: 600.

**Explicacio**: SSH es exigent amb els permisos. Si el config es pot llegir per altres, SSH el rebutja. A Windows normalment no es comprova, pero a Linux cal `chmod 600`.

---

## Pregunta 6: IdentitiesOnly?

**Resposta correcta**: Només prova la clau especificada.

**Explicacio**: Per defecte, SSH prova TOTES les claus de `~/.ssh/` fins que una funciona. Amb `IdentitiesOnly yes`, nomes prova la que has dit. Es mes rapid i mes segur.

---

## Pregunta 7 (oberta): Per que mes practic?

**Resposta model**:

Pensa en aquest cas: tens 3 servidors.

**Sense perfil**:
```bash
ssh -i ~/.ssh/bernat_key -p 22 bernat@100.x.y.z
ssh -i ~/.ssh/work_key -p 2222 admin@192.168.1.50
ssh -i ~/.ssh/cloud_key ubuntu@server.com
```

Cada vegada has de recordar:
- Quin usuari
- Quin port
- Quina clau
- Quina IP

**Amb perfil**:
```bash
ssh hortosona
ssh work
ssh cloud
```

Aixo es:
- **Rapid**: nomes 1 paraula.
- **Memorable**: noms significatius vs combinacions rares.
- **Menys errors**: no pots equivocar-te amb la IP o el port.
- **Compartible**: pots compartir el config entre PCs (sense les claus).

---

## Pregunta 8 (oberta): Compressio SSH

**Resposta model**:

**Usar-la** quan:
- Xarxa **lenta** (WiFi pobre, 3G, VSAT).
- Dades **molts comprimibles** (text, log, codi font).
- Vols **estalviar ample de banda**.

**No usar-la** quan:
- Xarxa **rapida** (LAN, fibra).
- Dades **ja comprimides** (JPEG, video, zip).
- Xarxa **buida** de carrega.

**Compte**: la compressio te cost computacional. En una RPi amb CPU limitat, pot ser mes lent que no comprimir.

**Per defecte**: deixa-la desactivada (`Compression no`) i activa-la nomes si cal.

---

## Pregunta 9 (oberta): 5 servidors organitzats

**Resposta model**:

Organitzaria el config aixi:

```
# === Servidors personals ===
Host rpi
    HostName 100.x.y.z
    User bernat
    IdentityFile ~/.ssh/id_ed25519

Host macbook
    HostName 100.x.y.z
    User bernatmora
    IdentityFile ~/.ssh/id_ed25519

# === Servidors de feina ===
Host feina-1
    HostName 10.0.1.50
    User admin
    Port 2222
    IdentityFile ~/.ssh/work_key

Host feina-2
    HostName 10.0.1.51
    User admin
    Port 2222
    IdentityFile ~/.ssh/work_key

# === Servidors al núvol ===
Host cloud-prod
    HostName prod.example.com
    User deploy
    IdentityFile ~/.ssh/cloud_key

# === Comodins ===
Host feina-*
    User admin
    Port 2222
    IdentityFile ~/.ssh/work_key
```

**Avantatges**:
- Comentaris separen blocs.
- Comodins eviten repetir.
- Noms curts pero clars.
- Cada servidor te la seva clau.

---

## Pregunta 10 (oberta): Per que IdentitiesOnly es segur?

**Resposta model**:

**Sense IdentitiesOnly**:
- SSH prova totes les claus de `~/.ssh/` una per una.
- Si tens 10 claus, pot trigar 10 segons per trobar la correcta.
- Si una clau coneguada arriba al servidor equivocat, podries entrar al servidor equivocat accidentalment.

**Amb IdentitiesOnly**:
- SSH nomes prova la clau especificada.
- Es mes rapid (1 sol intent).
- No pots entrar accidentalment al servidor equivocat.
- Mes segur contra atacs de "key confusion".

**Conclusio**: `IdentitiesOnly yes` es una bona practica sempre. No incrementa la complexitat i evita accidents.

---

## Què fer si has fallat moltes

- **5-8 encerts**: Rellegir el resum.
- **3-4 encerts**: Fes l'exercici pas a pas.
- **0-2 encerts**: Comença creant un sol perfil.
