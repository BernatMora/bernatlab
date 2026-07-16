# Respostes - M8 Cap 6: Obsidian + Git

## Pregunta 1: Que es Obsidian?

**Resposta correcta**: Un editor de notes en Markdown local-first.

**Explicacio**: Obsidian es una aplicacio que guarda les notes com a fitxers Markdown al teu disc. No al núvol, no en una base de dades - fitxers plans.

---

## Pregunta 2: Com es guarden?

**Resposta correcta**: En fitxers .md locals.

**Explicacio**: Cada nota es un fitxer `.md` al directori del vault. Pots obrir-les amb qualsevol editor de text.

---

## Pregunta 3: Com es vincla?

**Resposta correcta**: Amb [[nom-de-la-nota]].

**Explicacio**: La sintaxi `[[nom]]` crea un vincle a una altra nota. Si la nota no existeix, Obsidian la crea quan hi cliques.

---

## Pregunta 4: Es gratuit?

**Resposta correcta**: Si, per a us personal.

**Explicacio**: Per a us personal es 100% gratuit. Per a comercial cal una llicencia comercial (~50 USD/any).

---

## Pregunta 5: Plugin de flashcards?

**Resposta correcta**: Spaced Repetition.

**Explicacio**: El plugin Spaced Repetition et permet crear flashcards (preguntes + respostes) i les programa per repasar-les. Es perfecte per estudiar el curs.

---

## Pregunta 6: Per que Obsidian + Git?

**Resposta correcta**: Per tenir historial i sincronitzar entre PCs.

**Explicacio**: Git et permet:
- Tenir un historial de canvis.
- Tornar a versions anteriors.
- Sincronitzar entre multiples PCs.
- Compartir amb altres (encara que sigui privat).

---

## Pregunta 7 (oberta): Per que Obsidian vs Notion?

**Resposta model**:

- **Privadesa**: Obsidian es local. Notion es al nuvol. Si vols privadesa, Obsidian.
- **Local-first**: les teves notes son fitxers al teu disc. Pots fer-ne copies, moure-les, processar-les. Amb Notion, tot es al núvol.
- **Cost**: Obsidian es gratis per a us personal. Notion es gratis nomes amb limitacions.
- **Control**: amb Obsidian, tens el control total. Pots canviar el format, exportar a on vulguis, etc. Amb Notion, estas subjecte a les decisions de l'empresa.
- **Velocitat**: Obsidian es rapidissim perque es local. Notion depen de la connexio a Internet.

**Conclusio**: per a un homelab personal amb sensibilitat per la privadesa, Obsidian es la millor opcio.

---

## Pregunta 8 (oberta): Sistema d'enllaços

**Resposta model**:

El sistema d'enllaços `[[]]` de Obsidian es poderos perque:

- **Graf de coneixement**: Obsidian visualitza totes les notes i els seus vincles com un graf. Veus com els conceptes es connecten.
- **Trobar informacio relacionada**: si busques una paraula, troba totes les notes que l'esmenten. Si una nota parla de "Tailscale" i una altra de "VPN", pots descobrir connexions que no sabies.
- **Organitzar sense carpetes rigides**: pots tenir poques carpetes i molts enllaços. Es mes organic que un arbre.
- **Descobrir nous angles**: quan escrius una nota nova, l'index automatic et suggereix notes relacionades.
- **Pensament lateral**: pots saltar entre notes no relacionades formalment pero conceptualment connectades.

**Conclusio**: el graf es una eina de pensament, no nomes d'organitzacio.

---

## Pregunta 9 (oberta): Estructura del vault BernatLab

**Resposta model**:

```
bernatlab/
├── 00-index.md           (pagina principal)
├── 01-arquitectura/      (com funciona el sistema)
│   ├── sistema.md
│   ├── serveis.md
│   └── xarxa.md
├── 02-runbooks/          (procediments)
│   ├── tailscale-down.md
│   ├── portainer-down.md
│   ├── disc-ple.md
│   └── actualitzacio.md
├── 03-deures/            (coses pendents)
│   ├── curt-termi.md
│   └── llarg-termi.md
├── 04-aprenentatge/      (coses apreses)
│   ├── curs.md
│   ├── llibre.md
│   └── errors.md
├── 05-projectes/         (altres projectes)
│   └── hort-osona.md
└── 99-arxiu/             (notes velles)
```

**Convencions**:
- Numeracio al principi (00, 01, ...) per ordre logic.
- kebab-case (tot en minuscules, separat per guions).
- Dates en YYYY-MM-DD per notes diaries.

---

## Pregunta 10 (oberta): Riscos del repo public

**Resposta model**:

**Riscos**:
- **Privadesa**: Tothom pot veure les teves notes. No hi posis informacio personal (adreces, noms, etc.).
- **Secrets**: NO posis contrasenyes, claus SSH, tokens, o qualsevol cosa secreta. Git recorda tot l'historial.
- **Reconeixement**: si tens idees brillants, gent les pot veure i copiar-les (aixo es bo o dolent segons la perspectiva).
- **Spam**: gent pot trobar el teu repo i deixar-te issues o PRs indesitjats.

**Quan NO has de posar al repo public**:
- Notes personals (diari, salut, familia).
- Notes de feina amb informacio confidencial.
- Apunts amb noms reals d'altres persones.
- Qualsevol cosa que no vulguis que sigui publica per sempre.

**Alternatives per a notes privades**:
- **Vault separat** (no al repo public).
- **Repo privat** a GitHub.
- **Només al teu PC** sense Git.
- **Obsidian Publish** (servei d'Obsidian de pagament) - les teves notes al núvol pero privades.

**Compte amb l'historial**: Git recorda TOT. Si per error pusheges un secret, has de:
1. Esborrar-lo del fitxer.
2. Esborrar-lo de l'historial (git filter-branch o BFG).
3. **Rotar** el secret immediatament (canviar la contrasenya, revocar el token).

---

## Què fer si has fallat moltes

- **5-8 encerts**: Rellegir el resum.
- **3-4 encerts**: Instal·la Obsidian i crea el vault.
- **0-2 encerts**: Comença per una sola nota.
