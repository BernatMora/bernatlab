# Respostes - Capitol 10: Aplicacio a Hort Osona

## Pregunta 1: Quants documents te Hort Osona?

**Resposta correcta**: 76.

**Explicacio**: El projecte Hort Osona te ~76 fitxeres de cultiu en catala. Son fitxes curtes (~500-1500 paraules) sobre plantes, plagues, calendaris, etc. Son la base de coneixement que el sistema RAG consulta.

---

## Pregunta 2: Eines del sistema?

**Resposta correcta**: Open WebUI, Ollama, ChromaDB.

**Explicacio**: L'arquitectura son 3 components: Open WebUI com a frontend visual, Ollama com a LLM local, i ChromaDB com a vector store. InfluxDB es per a series temporals (altre modul), Grafana es per a visualitzacio. Telegram no es part del sistema base.

---

## Pregunta 3: Com clonar?

**Resposta correcta**: `git clone https://github.com/BernatMora/hort-osona.git`.

**Explicacio**: Es la ordre git estandard. `git pull` es per actualitzar, `curl` i `wget` son per descarregar altres tipus de contingut, no repositoris. Un cop clonat, tens tots els .md al disc.

---

## Pregunta 4: Model d'embeddings?

**Resposta correcta**: nomic-embed-text.

**Explicacio**: Es el model recomanat per Ollama per a embeddings: bona qualitat, 768 dimensions, rapid. `llama3.2` es per a generar texte, no per a embeddings. `mistral` i `gemma` son tambe models de generacio.

---

## Pregunta 5: k per defecte?

**Resposta correcta**: 5.

**Explicacio**: A la funcio `ask_hort(question, k=5)`, el valor per defecte es 5 fragments. Es l'equilibri entre context suficient i prompt no massa llarg. Pots canviar-ho segons el cas.

---

## Pregunta 6: Pregunta NO suggerida?

**Resposta correcta**: "Quin es el preu del quilo de mongetes?".

**Explicacio**: Les proves suggerides son totes sobre cultiu, plagues, sembra i associacions. La pregunta sobre el preu no es a la llista perque Hort Osona no te informacio economica - es una base de coneixement tecnic, no comercial.

---

## Pregunta 7 (oberta): Arquitectura completa

**Resposta model**:

L'arquitectura del sistema Hort Osona te 4 parts que treballen juntes:

1. **Open WebUI (frontend)**: es la interficie web per xatejar. L'usuari hi escriu les preguntes i veu les respostes. Es opcional - pots usar altres clients o un script Python directe. Es com el "Chrome" del sistema.

2. **Ollama (LLM)**: es el motor d'inteligencia artificial. Te dos rols: generar els embeddings dels documents (amb `nomic-embed-text`) i generar les respostes (amb `llama3.2`). Corre com a servidor local a `localhost:11434`.

3. **ChromaDB (vector store)**: es on es guarden els embeddings dels ~76 documents d'Hort Osona. Permet fer cerques per semblança rapidament. Es persistent al directori `hort_db/`.

4. **Script d'indexacio (Python)**: es un script que es corre un sol cop (o quan s'afegeixen documents nous). Llegeix els .md, els divideix en chunks, calcula els embeddings amb Ollama, i els guarda a ChromaDB.

**Flux de dades**: l'script llegeix docs -> Ollama embeddings -> ChromaDB. Despres, quan l'usuari pregunta: pregunta -> Ollama embedding -> ChromaDB cerca -> top-K -> Ollama LLM -> resposta.

Les 4 parts son necessaries. Sense script, no hi ha base. Sense ChromaDB, no hi ha cerca. Sense Ollama, no hi ha inteligencia. Sense frontend, no es pot usar facilment.

---

## Pregunta 8 (oberta): Flux d'una consulta

**Resposta model**:

Quan l'usuari escriu una pregunta a Open WebUI, passa el seguent:

1. **Embedding de la pregunta**: el sistema crida Ollama amb `nomic-embed-text` per obtenir el vector numeric de la pregunta. Es un vector de 768 dimensions que representa el significat.

2. **Cerca a ChromaDB**: ChromaDB rep el vector i busca els 5 vectors mes propers (mes semblants) entre tots els embeddings guardats. Retorna els 5 fragments originals + les metadades (font del document).

3. **Construccio del prompt**: el sistema ajunta els 5 fragments trobats en un contexte, i construeix un prompt que diu algo com "Ets un expert en horticultura. Respon nomes amb el contexte. Context: [fragments]. Pregunta: X". Es un template fix.

4. **Generacio amb LLM**: el prompt complet s'envia a Ollama amb `llama3.2`. El LLM llegeix el contexte i genera una resposta coherent en catala, basant-se nomes en la informacio dels fragments.

5. **Resposta + fonts**: la resposta del LLM es mostra a l'usuari, juntament amb les fonts (noms dels fitxers d'on han sortit els fragments). Aixi pot verificar la informacio.

Tot el proces passa al servidor local. Cap dada surt de la RPi. Es la gracia del sistema: **100% privat**.

---

## Pregunta 9 (oberta): Limitacions i millores

**Resposta model**:

El sistema actual te varies limitacions que es poden millorar:

**Limitacions actuals**:

- **Velocitat a la RPi**: la RPi es lenta. L'indexacio pot trigar 30+ min per a 76 documents, i cada consulta triga 5-10 segons. Es acceptable pero no instantani.

- **Qualitat del catala**: `llama3.2` es bo en catala pero no perfecte. Algunes vegades barreja castella o inventa paraules. `mistral` o `gemma` poden ser millors.

- **Qualitat dels embeddings**: `nomic-embed-text` es bo pero no especialitzat en catala. Un model entrenat en mes dades multilingues (com `bge-m3`) podria ser millor.

- **Cobertura**: nomes sap el que esta als 76 documents. Si un tema no hi es, no pot respondre (tot i que pot inventar, cosa que es pitjor).

- **Sense memoria entre converses**: cada pregunta es independent. No recorda res de preguntes anteriors.

**Millores possibles**:

- **Model mes potent**: pujar a `mistral` o `gemma:7b` (si el hardware ho permet).
- **Multi-idioma**: afegir embeddings especialitzats en catala com `projecte-aina/embeddings-ca`.
- **Re-ranking**: afegir una segona passada per millorar la precisio de la cerca.
- **Feedback loop**: guardar si les respostes son bones i usar-ho per millorar.
- **UI amb cites clicables**: que l'usuari pugui clicar a la font i veure el document sencer.
- **Cache de respostes**: si la mateixa pregunta es fa dos cops, retornar la primera resposta.
- **Streaming**: mostrar la resposta paraula a paraula (millor experiencia).

El sistema actual ja es util, pero sempre es pot millorar.

---

## Pregunta 10 (oberta): Integracio amb Telegram

**Resposta model**:

Per afegir el sistema a Telegram, caldria fer canvis en varies capes:

**Canvis necessaris**:

1. **Bot de Telegram**: cal crear un bot amb `@BotFather`, obtenir un token, i tenir un script Python que escolti els missatges amb `python-telegram-bot` o `telebot`.

2. **Servidor del bot**: el bot ha de correr 24/7. Es pot posar a la mateixa RPi amb `systemd` o `screen`. Important: el bot ha d'estar sempre escoltant.

3. **Adaptar el backend**: el flux es el mateix que ja tens (`ask_hort`), pero ara el trigger es un missatge de Telegram en lloc d'una crida des de Open WebUI. La funcio `ask_hort` es reutilitza tal qual.

4. **Gestio d'usuaris**: nomes tu pots usar el bot? O permets a altres? Si permets, cal autenticacio (per token, per Telegram ID autoritzat).

5. **Limit de longitud**: Telegram te un limit de 4096 caracters per missatge. Si la resposta es mes llarga, cal partir-la.

**Exemple d'esquelet**:

```python
import telebot
from consultar_hort import ask_hort

bot = telebot.TeleBot("TOKEN_AQUI")
ID_AUTORITZAT = 123456789  # el teu Telegram ID

@bot.message_handler(func=lambda m: True)
def respond(message):
    if message.from_user.id != ID_AUTORITZAT:
        return
    resposta, fonts = ask_hort(message.text)
    bot.reply_to(message, f"{resposta}\n\nFonts: {set(fonts)}")

bot.polling()
```

**Limitacions**:
- La RPi ha d'estar sempre engegada.
- Si vols compartir amb altres, cal gestionar autenticacio be.
- Telegram te limits de API: no pots fer mes de 30 missatges/segon.

**Avantatges**:
- Pots consultar des del mobil, en qualsevol lloc.
- La experiencia es mes natural que una web.
- Es privat igual (tot corre a la RPi, nomes Telegram sap que existeix el bot).

Es un projecte perfecte per a un cap de setmana.

---

## Què fer si has fallat moltes

- **5-8 encerts**: Has entes el sistema. Ara l'objectiu es personalitzar-lo per les teves dades.
- **3-4 encerts**: Torna a fer l'exercici pas a pas. El sistema nomes s'apren muntant-lo.
- **0-2 encerts**: Comença pel cap 8 (pipeline RAG basic) i torna aqui despres. No saltis passos.
