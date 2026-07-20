# Respostes - M8 Cap 5: Scripts d'alies PowerShell

## Pregunta 1: Que es el $PROFILE?

**Resposta correcta**: Un fitxer .ps1 que es carrega a cada inici.

**Explicacio**: El $PROFILE es una variable especial que apunta a un fitxer PowerShell. Aquest fitxer s'executa automaticament cada vegada que obres una nova sessio PowerShell.

---

## Pregunta 2: Ubicacio per defecte?

**Resposta correcta**: C:\Users\<usuari>\Documents\PowerShell\Microsoft.PowerShell_profile.ps1.

**Explicacio**: Aquesta es la ubicacio estandard de Windows. Es pot canviar amb la variable $PROFILE pero rarament cal.

---

## Pregunta 3: Set-Alias?

**Resposta correcta**: Fa que `kuma` sigui un alies de `bl-kuma`.

**Explicacio**: Set-Alias crea un nom alternatiu. Quan escrius `kuma`, PowerShell executa `bl-kuma`.

---

## Pregunta 4: Start-Process amb URL?

**Resposta correcta**: L'obre al navegador per defecte.

**Explicacio**: Start-Process detecta que es una URL i l'obre al navegador configurat per defecte a Windows.

---

## Pregunta 5: Carregar un fitxer?

**Resposta correcta**: . C:\ruta\fitxer.ps1 (dot-source).

**Explicacio**: El `.` (dot) seguit d'un espai i el cami del fitxer es diu "dot-source". Carrega les funcions al perfil actual, no pas en un scope separat.

---

## Pregunta 6: Canviar politica d'execucio?

**Resposta correcta**: Set-ExecutionPolicy.

**Explicacio**: Per defecte, PowerShell pot bloquejar l'execucio de scripts. Set-ExecutionPolicy permet canviar aquesta politica.

---

## Pregunta 7 (oberta): Per que alies vs marcadors?

**Resposta model**:

- **Velocitat**: Escriure `kuma` al terminal es 5x mes rapid que obrir el navegador, escriure la URL, i fer Enter.
- **Memoria**: No cal recordar URLs llargues. La paraula curta ja es tot.
- **Compartible**: El fitxer `.ps1` es pot sincronitzar entre PCs (via Git, OneDrive). Els marcadors son per navegador.
- **Centralitzat**: Tots els teus "shortcuts" en un sol lloc. Si canvies una IP, ho canvies en un sol fitxer.
- **Integrable**: Pots combinar alies amb altres eines (PowerToys Run, scripts).

---

## Pregunta 8 (oberta): Funcio vs alies

**Resposta model**:

**Funcio**:
- Accepta parametres.
- Pot contenir logica complexa.
- Es la "implementacio".

Exemple:
```powershell
function bl-logs { 
    param([string]$name)
    ssh bernat@100.x.y.z "docker logs $name --tail 50"
}
```

**Alies**:
- Nomes un nom alternatiu.
- No te parametres propis.
- Es la "dreça curta".

Exemple:
```powershell
Set-Alias kuma bl-kuma
```

**Quan usar cada un**:
- **Funcio**: quan necessites parametres o logica.
- **Alies**: quan nomes vols escurçar el nom.

**Convent a seguir**: 
- Funcions amb verb-noun (com `Get-Item`, `Set-Alias`).
- Alies amb noms curts i evidents.

---

## Pregunta 9 (oberta): Per que `C:\Users\usuari\bin\`?

**Resposta model**:

- **Ubicacio estandard**: La carpeta `bin` es un conveni Unix pero tambe s'usa a Windows. Es sap on buscar.
- **Backup**: Les carpetes standard del Windows (Documents, Desktop) canvien sovint. `bin` es estable.
- **Compartible**: Pots sincronitzar-la amb Git, OneDrive, o rsync entre PCs.
- **Neteja**: L'escriptori i Documents es desordre. `bin` nomes hi ha eines.
- **PATH**: Si poses `bin` al PATH del sistema, totes les eines son accessibles des de qualsevol lloc.

---

## Pregunta 10 (oberta): Sincronitzar entre PCs

**Resposta model**:

**Git** (la meva recomanacio):
1. Crea un repo `~/.dotfiles` o `~/bin` a GitHub.
2. Commit els teus scripts.
3. A cada PC, clona el repo.
4. Sincronitza amb `git pull` cada dia.

**Avantatges**:
- Versionat (puc tornar a una versio anterior).
- Historial complet.
- Portable.
- Documentable (README al repo).

**Desavantatges**:
- Has de fer commit/push manualment (o amb un script).
- Contrasenyes NO al repo (mai!).

**OneDrive** (alternativa):
- Sincronitzacio automatica.
- Pero no versionat.
- Emmagatzematge al núvol (pot ser lent).

**Sincronitzacio manual** (si no tens Git):
- USB stick.
- Correu electronic (mala idea, poc segur).

**Compte**: el fitxer conte noms d'usuari, IPs, etc. No es sensible, pero evita posar-hi contrasenyes o claus SSH.

---

## Què fer si has fallat moltes

- **5-8 encerts**: Rellegir el resum.
- **3-4 encerts**: Prova pas a pas.
- **0-2 encerts**: Comença per una sola funcio.
