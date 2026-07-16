# Resum - Capitol 6: Embeddings

## La idea clau

Un **embedding** es una llista de numeros (un vector) que representa el significat d'un text. Dues frases amb significat semblant tindran vectors propers; dues frases amb significat diferent tindran vectors allunyats. Es la manera que tenen les maquines de "mesurar" la semblança entre textos, i es el component magic que fa funcionar RAG.

## Que es exactament un embedding?

Un embedding es un vector de N dimensions (normalment 384, 768, 1024 o 1536) on cada dimensio representa algun aspecte del significat del text. Per exemple:

- "El gat dorm al sofà" -> [0.12, -0.34, 0.78, ..., 0.45] (768 numeros)
- "El moix està estirat al moble" -> [0.14, -0.32, 0.76, ..., 0.43] (molt semblant!)

Aquests dos vectors son propers perque les frases volen dir el mateix, encara que les paraules siguin diferents. Es el que permet fer cerques per significat i no per paraules exactes.

## Com es calculen?

Un embedding es calcula passant el text per una **xarxa neuronal** entrenada especificament per aixo. N'hi ha de molts tipus, pero els mes coneguts son:

- **Word2Vec / GloVe** (antics): un embedding per paraula. Limitats.
- **Sentence Transformers**: embeddings per frase o paragraf. Estanard actual.
- **OpenAI text-embedding-3-small**: 1536 dimensions, comercial.
- **BGE / E5 / nomic-embed**: models especialitzats, oberts.
- **Ollama embeddings**: integrats a Ollama (nomic-embed-text, mxbai-embed-large, etc.).

## Semblança cosinus: com es comparen

Per saber si dos embeddings son "propers" en significat, calculem la **semblança cosinus**:

```python
import numpy as np

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
```

El resultat es un numero entre -1 i 1:
- **1.0**: significat identic.
- **0.7-0.9**: molt semblant.
- **0.4-0.7**: relacionat.
- **0.0-0.4**: poc relacionat.
- **0.0 o menys**: no relacionat o oposat.

Aixo ens permet, donada una pregunta, trobar els textos mes semblants a una base de dades de milers de documents. Es el cor de RAG.

## Models d'embeddings locals (amb Ollama)

Ollama te diversos models d'embeddings preparats:

```bash
ollama pull nomic-embed-text     # 137M params, 768 dim, molt bo
ollama pull mxbai-embed-large    # 335M params, 1024 dim, encara millor
ollama pull all-minilm           # 22M params, 384 dim, rapid
```

Exemple d'us:

```bash
curl http://localhost:11434/api/embeddings -d '{
  "model": "nomic-embed-text",
  "prompt": "Quin temps fa avui a Vic?"
}'
```

Retorna un JSON amb `"embedding": [0.13, -0.45, 0.67, ...]` (768 numeros).

## Models d'embeddings amb sentence-transformers (Python)

Si prefereixes Python pur, la llibreria `sentence-transformers` es l'estandard:

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode([
    "El gat dorm",
    "El moix està estirat",
    "Avui plou a Vic"
])
print(embeddings.shape)  # (3, 384)
```

Avantatges:
- Molt flexible: pots usar qualsevol model de HuggingFace.
- Funciona amb CPU (tot i que mes lent que amb GPU).
- Integracio facil amb pandas, numpy, etc.

Desavantatges:
- Cal descarregar els models (1-2 GB).
- Lent si tens milers de textos (sense GPU).
- Cal gestionar memoria manualment.

## Dimensions dels embeddings: mes es millor?

| Model | Dimensions | Velocitat | Qualitat |
|---|---|---|---|
| all-MiniLM-L6-v2 | 384 | Rapidissima | Bona |
| all-mpnet-base-v2 | 768 | Rapida | Molt bona |
| nomic-embed-text | 768 | Rapida | Molt bona |
| mxbai-embed-large | 1024 | Mitjana | Excel·lent |
| text-embedding-3-large | 3072 | Lenta | Top |

**Regla**: 768 dimensions es el sweet spot. Mes enllà, la millora es marginal pero el cost puja.

## Com fer una cerca eficient amb embeddings

Pas a pas, el flux es:

1. **Indexacio**: per cada text de la teva base:
   - Calcular el seu embedding (vector de 768 nums).
   - Guardar-lo a una base de dades (junt amb el text original i metadades).

2. **Query**: donada una pregunta:
   - Calcular el seu embedding.
   - Buscar els K embeddings mes propers (per semblança cosinus).
   - Retornar els textos associats.

3. **Filtratge** (opcional): un cop tens els top-K, pots:
   - Filtrar per data, autor, categoria.
   - Re-ranking amb un model mes car.
   - Combinar amb cerca per paraules clau (BM25).

## Com triar el model d'embeddings

Depen del teu cas:

- **Si vols simplicitat**: usa el que ja tens amb Ollama (`nomic-embed-text`).
- **Si vols maxima qualitat**: `mxbai-embed-large` o un de HuggingFace especialitzat.
- **Si tens pocs textos** (menys de 1000): la diferencia entre models es poca.
- **Si tens milers de textos**: inverteix en un bon model, la qualitat es nota.
- **Si el text es tecnic** (codi, formulas): busca un model entrenat en dades tecniques.
- **Si el text es multilingüe** (catala + angles + castella): `bge-m3` o `nomic-embed-text` van be.

## Bones practiques

- **Normalitza els vectors** abans de calcular semblances (divideix per la norma).
- **Talla textos massa llargs** (max ~512 tokens per text). Si es mes llarg, parteix.
- **Neteja el text** (treu headers, peu de pagina, caracters extranys).
- **Guarda metadades** junt amb l'embedding (titol, seccio, data).
- **Re-indexa periodicament** si els documents canvien.
- **Fes proves amb un set de validacio** per assegurar que el model triat es el correcte.

## Casos d'us al BernatLab

- **RAG sobre documentacio** (cap. 5 i 8).
- **Cerca de logs semblants**: trobar logs similars a un de conegut.
- **Clustering de correus**: agrupar correus per tema.
- **Deduplicacio de notes**: trobar notes que diuen el mateix amb paraules diferents.
- **Recomanacio de scripts**: trobar scripts que resolen problemes semblants.
- **Classificacio de sensors**: agrupar lectures per patro.

## Limitacions dels embeddings

- **No entenen el context complet**: una paraula pot tenir embeddings diferents segons el contexte, pero els models basics nomes en calculen un per text.
- **Multilinguisme limitat**: alguns models son millors en angles que en catala. Comprova-ho.
- **Cost de calcul**: 1000 texts poden trigar minuts sense GPU.
- **Ceguesa a la semantica fina**: "bo" i "dolent" poden ser propers en alguns models si comparteixen contexte.
- **No son magics**: si dues frases son ironiques, l'embedding pot no captar-ho.

## Connexions amb altres capítols

- **Cap 5** - RAG usa embeddings per fer la cerca.
- **Cap 7** - Vector databases: on guardem els embeddings.
- **Cap 8** - Pipeline RAG complet: embeddings son un pas mes.
- **Cap 10** - A l'Hort Osona, els embeddings ens permeten cercar entre milers de lectures de sensors.
