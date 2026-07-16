# Respostes - M8 Cap 1: SSH amb claus

## Pregunta 1: Quantes claus?

**Resposta correcta**: 2 (una privada i una publica).

**Explicacio**: `ssh-keygen` sempre genera un parell: la clau privada (que nomes tu tens) i la clau publica (que pots compartir). Son complementaries: el que una xifra, l'altra desxifra.

---

## Pregunta 2: Quina clau no comparteixo?

**Resposta correcta**: La clau privada.

**Explicacio**: La clau privada es com la teva signatura personal. Si algu la te, pot impersonar-te. La clau publica es com el teu nom - la pots dir a tothom.

---

## Pregunta 3: Quin algoritme?

**Resposta correcta**: ed25519.

**Explicacio**: ed25519 es mes modern i segur que RSA. Utilitza corbes eliptiques, es mes rapid, i te claus mes curtes (millor per a dispositius petits). La comunitat Linux sha adoptat com a estandard.

---

## Pregunta 4: On es copia?

**Resposta correcta**: `~/.ssh/authorized_keys`.

**Explicacio**: El servidor SSH mira aquest fitxer per saber quines claus publiques poden entrar. Es un fitxer pla amb una clau per linia. Es a `~/.ssh/` de l'usuari (no pas del sistema).

---

## Pregunta 5: Comanda per copiar?

**Resposta correcta**: `type $env:USERPROFILE\.ssh\id_ed25519.pub | ssh ...`

**Explicacio**: Aixo concatena el contingut de la clau publica local amb l'ordre SSH remot que l'afegeix al `authorized_keys`. Es la manera recomanada perque evita errors de transcripcio.

**Per que no les altres**:
- `copy`: nomes copia localment, no pas remotament.
- `scp`: copia el fitxer, pero no l'afegeix a `authorized_keys`.
- `rsync`: sincronitza directoris, no pas concatena contingut.

---

## Pregunta 6: Per que la passphrase?

**Resposta correcta**: Protegeix la clau privada si el teu PC es robat.

**Explicacio**: Si algu roba el teu portatil i te la clau privada, la passphrase es l'unic que l'impedeix entrar als teus servidors. Es una **segona capa de seguretat**.

**Compte**: si la clau es robada **i** la passphrase es trencada (força bruta), l'atacant pot entrar a tots els servidors on tens aquesta clau.

---

## Pregunta 7: Permisos de `authorized_keys`?

**Resposta correcta**: 600.

**Explicacio**: SSH es molt exigent amb els permisos. Si el fitxer es pot llegir per altres usuaris (644, 755, 777), SSH el rebutja per seguretat. Els permisos correctes son:
- `~/.ssh/`: 700
- `~/.ssh/authorized_keys`: 600
- Claus privades: 600

---

## Pregunta 8 (oberta): Per que mes segures?

**Resposta model**:

- **Contrasenya tipica**: 12-20 caracters. Si es complexa (majuscules, minuscules, numeros, simbols), son uns 60-80 bits d'entropia. Un atacant pot provar milions de passwords per segon - amb una bona maquina, pot trencar-la en hores o dies.

- **Clau ed25519**: 256 bits d'entropia. Per trencar-la per brute force, caldria **mes temps que l'edat de l'univers**, inclos amb tots els ordinadors del món treballant junts.

- **Aixo es el que fa que les claus siguin mes segures**: la matematica, no pas la memoria humana.

**Conclusio**: una clau de 256 bits es matematicament impossible de trencar. Una contrasenya es pot endevinar amb paciencia.

---

## Pregunta 9 (oberta): Si perds el portatil

**Resposta model**:

Passos immediats:
1. **Revocar la clau** al servidor: esborrar la linia de `~/.ssh/authorized_keys` a tots els servidors on la tens.
2. **Generar una nova clau** en un altre dispositiu que ja tingui acces.
3. **Tornar a configurar** tots els servidors amb la nova clau.
4. **Canviar altres contrasenyes** que estaven emmagatzemades al portatil.

**Si encara tens acces** des d'un altre dispositiu, pots fer tot nomes des d'allà.

**Si NO tens acces** a cap dels teus servidors (perque la unica clau era al portatil perdut), necessites acces fisic (monitor + teclat) o un altre metode de recuperacio.

**Per prevenir**:
- Fer **backups xifrats** de la clau privada en un lloc segur (USB xifrat, gestors de passwords).
- Usar **claus diferents** per a servidors sensibles (banking, GitHub, etc.) vs servidors personals.
- Activar **2FA** als serveis importants (GitHub, Google, etc.).

---

## Pregunta 10 (oberta): Per que desactivar el password?

**Resposta model**:

**Arguments a favor de desactivar-lo**:
- **Attack surface minim**: nomes pots entrar amb la clau privada. Encara que algu encerti la teva contrasenya (per leak, social engineering, etc.), no pot entrar.
- **Auditoria**: el servidor sap exactament quina clau sha usat per entrar (rastreable).
- **Forca bruta impossible**: un atacant pot provar milions de passwords per segon. No pot fer el mateix amb claus privades (que no es poden reproduir sense la passphrase).

**Arguments en contra**:
- Si **perds la clau**, perds l'acces (cal acces fisic per recuperar).
- Si **oblides la passphrase**, cal generar una clau nova.
- Si tens **altres usuaris** que usen password, els deixes fora.

**Conclusio**: en un homelab personal on nomes tu accedeixes, **desactivar el password es una bona practica**. En servidors multi-usuari o amb backups perillosos, deixa el password activat com a pla B.

---

## Què fer si has fallat moltes preguntes

- **5-8 encerts**: Rellegir el resum.
- **3-4 encerts**: Rellegeix el capitol del llibre sobre SSH (M4 del BernatLab).
- **0-2 encerts**: Comencem pel basics - que es una clau, per que serveix.
