# Respostes - Capitol 4: Prompt engineering

> Mira les respostes DESPRES d'haver fet el qüestionari.

## Pregunta 1: Que es un "prompt"?

**Resposta correcta**: La pregunta o instruccio que dones a un LLM.

**Explicacio**: El prompt es l'input que envies al model. Es l'unic canal de comunicacio. Si el prompt es dolent, la resposta sera dolenta. Per tant, saber escriure bons prompts es una habilitat fonamental per treure profit dels LLMs.

---

## Pregunta 2: Tecnica amb exemples?

**Resposta correcta**: Few-shot prompting.

**Explicacio**: Few-shot prompting vol dir que dins del prompt hi ha 1-3 exemples del format esperat. El model veu exemples i continua el patro. Es una de les tecniques mes efectives i simples. Zero-shot es sense exemples. Chain-of-thought es pas a pas. Role prompting es assignar un rol.

---

## Pregunta 3: Millor prompt per a seguretat?

**Resposta correcta**: "Soc admin d'una RPi 4 amb SSH obert a Internet. Dona'm 5 consells concrets de seguretat ordenats per prioritat."

**Explicacio**: Aquest prompt es bo perque:
- Dona contexte ("admin d'una RPi 4 amb SSH obert").
- Especifica el rol (admin, no usuari qualsevol).
- Indica el format (5 consells concrets, ordenats per prioritat).
- Es concret, no generic.

Els altres son massa oberts i el model donara respostes generiques.

---

## Pregunta 4: Que es chain-of-thought?

**Resposta correcta**: Demanar al model que raoni pas a pas abans de donar la resposta.

**Explicacio**: Chain-of-thought prompting consisteix a demanar al model que "mostri el seu treball": que identifiqui passos, que calculi cada un, i al final doni la resposta. Funciona especialment be en problemes de logica, matematiques o analisis complexes. La gracia esta en que el model pot autocorregir-se veient els seus propis passos.

---

## Pregunta 5: System prompt?

**Resposta correcta**: Conte instruccions permanents sobre el rol i estil del model.

**Explicacio**: A l'API `/api/chat` d'Ollama, el primer missatge amb `role: "system"` conte les instruccions permanents: idioma, to, limitacions, exemples de format. Es mante a totes les interaccions de la conversa. Es la millor manera de configurar el comportament del model.

---

## Pregunta 6: Per que usar delimitadors?

**Resposta correcta**: Per ajudar el model a distingir les diferents parts del prompt.

**Explicacio**: Delimitadors com `[INSTRUCCIONS]`, `[DADES]`, `[EXEMPLES]` ajuden el model a entendre quina part es cada cosa, sobretot en prompts llargs amb se multiplesccions. Sense delimitadors, el model pot confondre les dades amb les instruccions.

---

## Pregunta 7: Error mes comu?

**Resposta correcta**: Fer preguntes massa obertes o vagues.

**Explicacio**: "Explica la historia" es massa vague. "Explica la historia de la computacio a Europa entre 1950 i 1980" es concret. La majoria de respostes inutils venen de prompts massa oberts. Sigues especific: quina historia, quin periode, quin nivell de detall, quin format.

---

## Pregunta 8: Format correcte per a JSON?

**Resposta correcta**: "Respon nomes amb JSON valid, sense text adicional. Format: {...}".

**Explicacio**: Cal ser molt explicit amb el format esperat. Si nomes dius "escriu en JSON", el model pot afegir explicacions en prosa al voltant. Si vols nomes JSON pur, cal insistir-hi i mostrar el format exacte amb un exemple.

---

## Pregunta 9 (oberta): Prompt per analitzar el log

**Resposta model**:

Un bon prompt per a aquesta tasca podria ser:

```
Ets un expert en seguretat informatica amb 10 anys d'experiencia. 
Analitza la seguent linia de log d una Raspberry Pi 4 amb SSH obert 
a Internet. Considera el contexte: servidor d un homelab personal 
amb poques visites pero accessible publicament.

LINIA DE LOG:
Mar 15 03:42:17 rpi sshd[1234]: Failed password for root from 185.143.223.47 port 44231 ssh2

Proporciona la teva analisi en aquest format exacte:

ANOMALIA: [descriu quina activitat sospitosa veus, si n'hi ha]
RISC: [1-5, on 5 es atac confirmat]
EVIDENCIA: [quina part del log t ha fet pensar aixi]
ACCIO_1: [accio concreta immediata]
ACCIO_2: [accio concreta a mitja termini]

Limita cada seccio a 1-2 frases. Sigues directe i tecnic.
```

**Per que funciona**:
- Dona un **rol** clar (expert en seguretat).
- Dona **context** (RPi amb SSH obert, homelab personal).
- Especifica el **format exacte** amb noms de seccions clares.
- Dona **restriccions** de longitud (1-2 frases per seccio).
- Es **directe** sense donar peu a respostes vagues.

**Quin resultat esperar**: el model donara una resposta estructurada amb "RISC: 4" o similar, indicant que es un atac de força bruta. Suggerira accions com "bloquejar la IP amb iptables" i "configurar fail2ban".

---

## Pregunta 10 (oberta): Diferencies entre tecniques

**Resposta model**:

**Zero-shot** (sense exemples):

```
Resumeix aquest log en una sola frase:
[LINIA DE LOG]
```

El model ha d'endevinar el format. Donara una resposta correcta pero variable: pot ser molt llarga, molt curta, o amb estructura impredictible.

**Few-shot** (amb exemples):

```
Resumeix cada log en una sola frase. Exemples:

Log: "Mar 15 12:00 rpi apt[123]: upgraded libssl3"
Resum: "S ha actualitzat la llibreria openssl a les 12:00."

Log: "Mar 15 03:00 rpi sshd[456]: Failed password for root"
Resum: "Intent de login fallit com a root a les 3 de la matinada."

Log: "Mar 15 18:30 rpi dockerd[789]: container abc started"
Resum: "S ha iniciat el contenidor abc a les 18:30."

Ara resumeix:
Log: "Mar 15 20:15 rpi ollama[3456]: API request processed"
Resum:
```

El model veu el patro i el segueix. La resposta sera consistent en longitud i estil.

**Chain-of-thought** (pas a pas):

```
Analitza si aquesta linia de log indica un problema:
"Mar 15 03:42:17 rpi sshd[1234]: Failed password for root from 185.143.223.47 port 44231 ssh2"

Raona pas a pas:
1. Quin servei es? (sshd)
2. Quin esdeveniment? (Failed password)
3. Es habitual o sospitos?
4. Quin risc te?
5. Cal actuar?
```

El model "veu" el seu raonament i pot detectar errors. Per exemple, pot adonar-se que el login es a les 3 de la matinada i des d'una IP externa, senyal d'atac.

**En resum**: zero-shot es rapid pero inconsistent. Few-shot es el mes practic per obtenir formats consistents. Chain-of-thought es el millor per a tasques de raonament complexe. La tria depen de la tasca concreta.

---

## Que fer si has fallat moltes preguntes

- **5-8 encerts**: rellegir el resum amb atencio a les 7 tecniques.
- **3-4 encerts**: practica amb l'exercici del capitol abans de seguir.
- **0-2 encerts**: torna a fer el resum sencer, subratllant les tecniques que no recordaves.

## Que fer si has encertat totes

- Passa al **Capitol 5** (RAG, introduccio).
- O fes el **repte**: crea una plantilla de prompt personalitzada per a una tasca del teu dia a dia.
