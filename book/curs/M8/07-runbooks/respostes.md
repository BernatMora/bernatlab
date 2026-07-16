# Respostes - M8 Cap 7: Runbooks

## Pregunta 1: Que es un runbook?

**Resposta correcta**: Un document amb procediments per a situacions especifiques.

**Explicacio**: Un runbook es la "memoria institucional" del teu sistema. Documenta que fer quan algo falla.

---

## Pregunta 2: Primera seccio?

**Resposta correcta**: Símptomes.

**Explicacio**: Començar pels simptomes permet al lector identificar rapidament si el runbook es el correcte. No vols perdre temps llegint un runbook que no aplica.

---

## Pregunta 3: Quan sha descriure?

**Resposta correcta**: Quan resols un problema, immediatament.

**Explicacio**: El millor moment per escriure un runbook es quan acabes de resoldre un problema. Tens tot el contexte fresc, recordes les comandes, els errors, les solucions. Si esperes, ho oblidaras.

---

## Pregunta 4: On NO guardar?

**Resposta correcta**: Al servidor que pot fallar (com a unica copia).

**Explicacio**: Si el servidor cau, no podràs accedir als runbooks. Per tant, els runbooks han d'estar en un lloc extern: al teu PC, a Obsidian, a un núvol, etc.

---

## Pregunta 5: Quantes seccions?

**Resposta correcta**: 5-6.

**Explicacio**: Simptomes, diagnostic, solucio, validacio, notes (i opcionalment "context" al principi). Mes de 6 es excessiu per a un homelab.

---

## Pregunta 6: Que sha dincloure a mes?

**Resposta correcta**: Comandes exactes, casos especials, errors comuns.

**Explicacio**: Un bon runbook ha de ser executable sense pensar. Comandes literals, casos reals, errors que has vist. No la teva opinio.

---

## Pregunta 7 (oberta): Per que son importants?

**Resposta model**:

Els runbooks son importants a un homelab perque:

- **Quan algo falla**: ja saps que fer. No perds hores pensant.
- **Quan no estas a casa**: pots resoldre des de la feina o de vacances.
- **Quan oblides com es fa**: el cervell no es perfecte. Un runbook es la memoria externa.
- **Quan algú altre ha de mantenir el sistema**: la teva parella, un fill, un company. Si els hi deixes el sistema, tambe els hi deixes els runbooks.
- **Per consistencia**: cada vegada que tens el problema, segueixes el mateix procediment. No improvisar.

---

## Pregunta 8 (oberta): Quan crear i actualitzar?

**Resposta model**:

**Crear**:
- Immediatament despres de resoldre un problema.
- Quan preveus que algo pot passar (preventiu).
- Quan trobes un error a la documentacio actual.

**Actualitzar**:
- Quan canvies la configuracio del sistema.
- Quan trobes una solucio millor.
- Periode de revisio (cada 6 mesos).
- Quan algú altre t'ajuda i troba una millor manera.

**Compte**: un runbook obsolet es pitjor que cap runbook. Si no es correcte, la gent confia en ell i empitjora les coses.

---

## Pregunta 9 (oberta): Runbooks essencials

**Resposta model**:

Llista minima viable per a un homelab:

1. **Tailscale/SSH down** - Si no pots accedir. (JA EXISTEIX)
2. **Disc ple** - Problema mes comu.
3. **Contenidor no arranca** - Si un serveis Docker cau.
4. **RPi no engega** - Si el hardware falla.
5. **Backup i restauracio** - Si la SD mor.
6. **Contrasenya oblidada** - Si perds acces a un servei.
7. **Actualitzacio segura** - Per actualitzar sense trencar res.

**Mes opcionals** (segun el sistema):
- **Temperatura alta** - Si la RPi s'escalfa massa.
- **IP local fixa** - Com configurar.
- **Migracio a nova RPi** - Si canvies de hardware.

---

## Pregunta 10 (oberta): Per que copia externa?

**Resposta model**:

Es important tenir una copia dels runbooks FORA del servidor perque:

- **Si el servidor cau**: si nomes tens els runbooks a la RPi i la RPi no arranca, no pots llegir com resoldre.
- **Si tens acces limitat**: imagina que no pots entrar a la RPi pero necessites saber com restaurar. Els runbooks al teu PC son la teva referencia.
- **Si la informacio es perd**: si la SD es corromp, totes les dades es perden - inclosos els runbooks.
- **Pla B**: en cas d'emergencia extrema, sempre necessites un pla alternatiu.

**Solucions**:
- **A Obsidian** (local al teu PC).
- **A un altre PC** (sincronitzat amb Git).
- **Al núvol privat** (OneDrive, Google Drive).
- **Impresos** (per a emergencies molt extremes, com un incendi).

**Conclusio**: un runbook nomes es valid si es accessible quan el sistema falla.

---

## Què fer si has fallat moltes

- **5-8 encerts**: Rellegir el resum.
- **3-4 encerts**: Comença per l'inventari.
- **0-2 encerts**: Crea un sol runbook.
