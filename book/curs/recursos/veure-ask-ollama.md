# Veure la funcio ask_ollama de rag.py

A la RPi, executa:

```bash
sed -n '140,200p' /home/bernat/hort-osona/hort-osona-iot/rag.py
```

Aixo mostrara les linies 140-200 del fitxer, que contenen la funcio
`ask_ollama` i la linia 173 que sha trobat amb l'error.

## Que cal mirar

La linia 173 conte:
```python
return f"[Error: No es pot connectar amb Ollama. Assegura't que estigui actiu: ollama serve]"
```

Aixo es un `except` que captura un error. Volem veure:
1. Quin es l'except (ConnectionError? RequestException? generic Exception?)
2. A quina URL intenta conectar
3. Si te un timeout massa curt

Comparteix la sortida de la comanda i sabrem exactament que cal canviar.
