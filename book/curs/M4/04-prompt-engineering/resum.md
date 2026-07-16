# Resum - Capitol 4: Prompt engineering

## La idea clau

Un **prompt** es la pregunta o instruccio que dones a un LLM. La diferencia entre un bon i un mal prompt pot ser la diferencia entre una resposta inutil i una meravellosa. Prompt engineering es l'art d'escriure prompts que extreuen el millor del model. I no es magia: son patrons que es poden aprendre.

## Per que importa al BernatLab?

Si volem que el nostre LLM local ens ajudi amb tasques reals (resumir logs, generar scripts, respondre sobre l'Hort Osona), hem de saber com parlar-li. Un prompt mal escrit donara respostes vagues o equivocades, i acabarem pensant que el model es dolent quan en realitat el problema es nostre.

## Principi 1: Sigues especific

**Mal prompt**:
```
Explica els servidors.
```

**Bon prompt**:
```
Explica quines son les 3 diferencies principals entre un servidor HTTP com Nginx i un servidor d'aplicacions com Gunicorn, en menys de 100 paraules.
```

El model no pot endevinar quina informacio vols, ni quin nivell de detall, ni en quin format. Si no li dius, et donara la resposta mes generica possible (que sol ser la menys util).

## Principi 2: Dona context (rol i situacio)

**Mal prompt**:
```
Com puc millorar la seguretat?
```

**Bon prompt**:
```
Soc un administrador de sistemes amb una Raspberry Pi 4 que te un servidor SSH obert a Internet. Dona'm 5 consells concrets per millorar la seguretat, ordenats per prioritat. Explica cada consell en 2-3 frases.
```

Especificar **qui ets**, **quina es la teva situacio** i **quina informacio necessites** ajuda el model a donar-te una resposta a la teva mida.

Aixo es la base del que s'anomena **role prompting**:

```json
{
  "messages": [
    {"role": "system", "content": "Ets un expert en Linux amb 20 anys d'experiencia. Respon sempre en catala, amb exemples de comandes."},
    {"role": "user", "content": "Com puc veure quins processos gasten mes CPU?"}
  ]
}
```

## Principi 3: Dona exemples (few-shot)

Si el model no enten el format que vols, mostra-l'hi amb exemples. Es la tecnica **few-shot**:

**Prompt amb 0 exemples** (zero-shot):
```
Classifica el sentiment d'aquesta critica: "El llibre es avorrit i mal escrit"
```

**Prompt amb 2 exemples** (few-shot):
```
Classifica el sentiment de cada critica. Respon nomes amb "positiu" o "negatiu".

Critica: "Molt bon llibre, l'he gaudit"
Sentiment: positiu

Critica: "Pessima compra, no ho recomano"
Sentiment: negatiu

Critica: "El llibre es avorrit i mal escrit"
Sentiment:
```

El segon prompt es molt mes efectiu perque el model veu exactament el format esperat.

## Principi 4: Indica el format de sortida

**Prompt sense format**:
```
Llista els avantatges de Docker.
```

**Prompt amb format**:
```
Llista els 5 avantatges principals de Docker. Per cada avantatge:
- Titol en negreta
- Explicacio en 1-2 frases
- Comanda d'exemple si escau

Utilitza aquest format Markdown:

## [Titol]
[Explicacio]
`[comanda]`
```

Aixo es molt potent quan la resposta va a una web, un correu o un document: el model ja la genera en el format correcte.

## Principi 5: Demana pas a pas (chain of thought)

Per a tasques complexes, fer que el model "pensi pas a pas" millora molt la qualitat:

**Mal prompt**:
```
Quants dies te 5 anys si considerem 3 anys de traspas?
```

**Bon prompt**:
```
Quants dies te un periode de 5 anys si considerem que hi ha 3 anys de traspas?

Pensa pas a pas:
1. Quants dies te un any normal?
2. Quants dies te un any de traspas?
3. Calcula els dies totals.
```

Aixo s'anomena **chain-of-thought prompting** i funciona perque el model "veu" el seu propi raonament i el pot autocorregir.

## Principi 6: Dona restriccions negatives

A vegades es mes facil dir al model **el que NO ha de fer**:

```
Explica què es Kubernetes. No donis exemples de codi. No comparis amb altres eines. Limita't a una definicio clara en 3-4 frases.
```

O amb prefixos per controlar la sortida:

```
# Escriu nomes el JSON, sense cap text addicional
{
  "usuari": "...",
  "accio": "..."
}
```

## Principi 7: Usa delimitadors

Si el prompt conte mes d'una seccio (instruccions + dades + pregunta), usa delimitadors clars:

```
[INSTRUCCIONS]
Ets un assistent que classifica correus electronic en categories.

[CORREU]
From: jordi@example.com
Subject: Error al servidor
Body: Hola, el servidor ha tornat a caure a les 3 de la matinada...

[CATEGORIES]
- tecnic
- comercial
- personal
- spam

[TASCA]
Respon nomes amb el nom de la categoria. Si no n'estas segur, escriu "dubte".
```

Els delimitadors (`[INSTRUCCIONS]`, `[CORREU]`, etc.) ajuden el model a entendre quina part es cada cosa.

## Tecnica bonus: System prompt

A l'API d'Ollama pots separar el **system prompt** (instruccions permanents) de la **pregunta** (input de l'usuari). Es la forma mes neta:

```json
{
  "messages": [
    {"role": "system", "content": "Ets un expert en Docker. Respon sempre en catala. Dona exemples de comandes quan sigui relevant."},
    {"role": "user", "content": "Com puc veure els logs d'un contenidor?"}
  ]
}
```

El system prompt es mante a totes les converses. Es ideal per a instruccions permanents (estil, idioma, limitacions).

## Com mesurar la qualitat d'un prompt

Algunes pistes per avaluar:

- **Repetibilitat**: fas la mateixa pregunta 5 vegades, dones respostes similars?
- **Especificitat**: la resposta conté la informacio que necessitaves?
- **Format**: la resposta esta en el format esperat?
- **Al·lucinacions**: el model s'ha inventat alguna dada evident?
- **Longitud**: es mes llarg o mes curt del que necessitaves?

## Errors comuns

- **Preguntes massa obertes**: "Explica la historia" -> massa ample, resposta superficial.
- **Suposar context**: "Fes la cosa aquella" -> el model no sap quina cosa.
- **No validar**: creure's la primera resposta sense verificar.
- **Ignorar el catala**: si vols respostes en catala, especifica-ho sempre.
- **Prompts massa llargs**: si el prompt es mes llarg que la finestra de context, es talla.

## Connexions amb altres capítols

- **Cap 1-3** - Base: que es un LLM, com fer-lo correr, quin model triar.
- **Cap 5-8** - RAG: el prompt engineering es critica per donar contexte al model.
- **Cap 10** - A l'Hort Osona, els prompts especialitzats son la diferencia entre rebre dades utils o soroll.

## Una plantilla que funciona

```text
[ROL]
Ets un [professio] amb [X] anys d'experiencia en [camp].

[TASCA]
[Descripcio clara del que vols]

[RESTRICCIONS]
- Respon en [idioma]
- Limita la resposta a [N] paraules/frases
- Usa [format] especific
- No [accio no desitjada]

[EXEMPLES] (opcional)
Input: [exemple]
Output: [exemple esperat]

[INPUT]
[Les teves dades o pregunta concreta]
```

Utilitza aquesta plantilla com a punt de partida. L'omples, la proves, l'ajustes, i ja tens un bon prompt.
