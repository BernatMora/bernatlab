# Exercici practic - Capitol 3: Triar el model adequat

> 30-45 min · Real al teu servidor

## Objectiu

Comparar 3-4 models diferents amb les mateixes preguntes per entendre quin s'adapta millor a les teves necessitats. Mesurar velocitat i qualitat subjectiva.

## Requisits

- Ollama instal·lat (cap. 2)
- 30-45 minuts
- ~5 GB d'espai lliure (per a 3 models petits)

## Pas 1: Descarrega 3 models per comparar (15-20 min)

```bash
# Model petit i rapid
ollama pull llama3.2:1b

# Model mitja - el candidat principal
ollama pull llama3.2:3b

# Alternativa de Google
ollama pull gemma2:2b

# Comprova que tots son aqui
ollama list
```

Si tens mes espai, afegeix tambe:

```bash
ollama pull phi3:mini
```

## Pas 2: Crea un script de comparacio (10 min)

Crea un fitxer `~/bernatlab-exercicis/M4/03-models/comparem.sh`:

```bash
#!/bin/bash
# Compara el temps de resposta de diferents models amb la mateixa pregunta

MODELS=("llama3.2:1b" "llama3.2:3b" "gemma2:2b" "phi3:mini")
PREGUNTA="Explica en 3 frases per que es important fer copies de seguretat dels logs dun servidor."

for model in "${MODELS[@]}"; do
  echo "=========================================="
  echo "Model: $model"
  echo "Pregunta: $PREGUNTA"
  echo "=========================================="
  start=$(date +%s.%N)
  response=$(curl -s http://localhost:11434/api/generate -d "{
    \"model\": \"$model\",
    \"prompt\": \"$PREGUNTA\",
    \"stream\": false
  }")
  end=$(date +%s.%N)

  # Extreu el text generat amb jq (instal·la'l si cal: sudo apt install jq)
  echo "$response" | jq -r '.response'
  echo ""
  echo "Temps total: $(echo "$end - $start" | bc) segons"
  echo "Tokens generats: $(echo "$response" | jq '.eval_count')"
  echo ""
done
```

Fes-lo executable:

```bash
chmod +x comparem.sh
```

## Pas 3: Executa la comparacio (5 min)

```bash
sudo apt install jq bc -y   # eines necessaries
./comparem.sh
```

Anota els resultats: temps, tokens, qualitat subjectiva.

## Pas 4: Prova amb tasques diferents (10 min)

Crea un altre script `~/bernatlab-exercicis/M4/03-models/comparem-tasques.sh`:

```bash
#!/bin/bash
# Prova cada model amb 3 tipus de tasca: resum, codi, traduccio

MODELS=("llama3.2:1b" "llama3.2:3b" "gemma2:2b")

declarar -A TASQUES
TASQUES[resum]="Resumeix aquest text en una sola frase: La Raspberry Pi 4 es un ordinador complet amb CPU ARM Cortex-A72 de 4 nuclis a 1.5 GHz, 4 GB de RAM LPDDR4, conectivitat Ethernet Gigabit i Wi-Fi. Es ideal per a un servidor domestic amb consum de 5 a 10 watts."
TASQUES[codi]="Escriu un script bash que llisti tots els fitxers .log del directori /var/log mes grans de 10 MB."
TASQUES[traduccio]="Tradueix al catala: The quick brown fox jumps over the lazy dog. The rain in Spain stays mainly in the plain."

for model in "${MODELS[@]}"; do
  echo "=========================================="
  echo "MODEL: $model"
  echo "=========================================="
  for tasca in resum codi traduccio; do
    echo ""
    echo "--- Tasca: $tasca ---"
    start=$(date +%s.%N)
    response=$(curl -s http://localhost:11434/api/generate -d "{
      \"model\": \"$model\",
      \"prompt\": \"${TASQUES[$tasca]}\",
      \"stream\": false
    }")
    end=$(date +%s.%N)
    echo "$response" | jq -r '.response'
    echo "Temps: $(echo "$end - $start" | bc)s | Tokens: $(echo "$response" | jq '.eval_count')"
  done
  echo ""
done
```

Fes-lo executable i executa'l:

```bash
chmod +x comparem-tasques.sh
./comparem-tasques.sh
```

## Pas 5: Documenta els resultats (10 min)

Crea `book/curs/M4/03-models-locals/taula-comparativa.md` amb una taula:

| Model | Mida | Temps (resum) | Temps (codi) | Qualitat resum | Qualitat codi | Catala? |
|---|---|---|---|---|---|---|
| llama3.2:1b | ... | ... | ... | ... | ... | ... |
| ... | | | | | | |

Afegeix un paràgraf al final amb les teves conclusions: quin triaries per a cada tasca?

## Validacio

Has acabat si:
- [ ] Has descarregat almenys 3 models.
- [ ] Has executat la comparacio basica.
- [ ] Has executat la comparacio per tasques.
- [ ] Has creat la taula comparativa.
- [ ] Has triat quin model es el teu favorit i per que.

## Per aprofundir

- Prova un model especialitzat en codi com `codellama:7b` (si tens RAM).
- Investiga que es el "context length" i mira quin es el maxim per a cada model amb `ollama show`.
- Compara el consum de RAM durant cada consulta amb `htop` o `free -h`.
- Fes una pregunta trampa a cada model ("Quin any es va inventar Linux?") i mira qui al·lucina menys.
