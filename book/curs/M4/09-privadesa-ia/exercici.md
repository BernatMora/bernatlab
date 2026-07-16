# Exercici practic - Capitol 9: Privadesa de la IA

> 20-30 min - RPi amb Ollama

## Objectiu

Auditar el que ja tens a la RPi per entendre quina informacio es local i quina podria sortir al nuvol. Practicar bones practiques de privadesa.

## Requisits

- RPi amb Ollama funcionant
- 20-30 min
- Paciencia per revisar fitxers

## Pas 1: Inventari local (10 min)

Obre una terminal i fes un inventari de tot el que ja tens en local:

```bash
# On son els models d'Ollama?
ollama list
ls -la ~/.ollama/models/

# On es la base de dades ChromaDB (si en tens)?
find ~ -name "chroma*" -type d 2>/dev/null

# Quins scripts usen Ollama?
find ~ -name "*.py" -exec grep -l "ollama\|11434" {} \; 2>/dev/null

# Fitxers .env amb possibles API keys?
find ~ -name ".env" 2>/dev/null
```

Anota en un paper o fitxer quines dades tens en local i quines al núvol.

## Pas 2: Configurar el navegador per a consultes privades (5 min)

Si vols usar un LLM al núvol sense deixar rastre:

- **Firefox**: obre una finestra privada (Ctrl+Shift+P) i usaDuckDuckGo com a buscador.
- **Extensio uBlock Origin**: bloquegja trackers.
- **Resist Fingerprinting**: a about:config posa `privacy.resistFingerprinting = true`.

Comprova que cap cookie de serveis IA esta al navegador habitual:

```bash
# Neteja cookies de serveis IA coneguts
# OpenAI, Anthropic, Google AI, etc.
```

## Pas 3: Comparar respostes local vs nuvol (10 min)

Fes la mateixa pregunta al teu Ollama local i a un servei al nuvol (ChatGPT, Claude, etc.). Compara:

1. **Privadesa**: la pregunta va a un servidor extern?
2. **Velocitat**: quin es mes rapid?
3. **Qualitat**: quin respon millor?
4. **Cost**: quant costa cada consulta?

Pregunta suggerida (generica, no personal):
"Explica'm 3 avantatges de l'horticultura ecologica."

Documenta les diferencies en un fitxer `proves_privadesa.md`:

```markdown
# Proves de privadesa

## Pregunta
"Explica'm 3 avantatges de l'horticultura ecologica."

## Ollama local (llama3.2)
- Temps: Xs
- Privadesa: total (no surt del PC)
- Cost: 0 euros
- Qualitat percebuda: ...

## Nuvol (X)
- Temps: Xs
- Privadesa: baixa (dades enviades a l'empresa)
- Cost: X euros/mes
- Qualitat percebuda: ...

## Conclusions
...
```

## Pas 4: Configurar un `.gitignore` correcte (5 min)

Si tens un projecte amb scripts que usen Ollama o ChromaDB:

```bash
cat >> .gitignore << 'EOF'
# Privadesa
.env
*.db
chroma_db/
chroma/
*.chroma
ollama_logs/
logs/
EOF
```

Comprova que cap fitxer sensible esta a punt de pujar-se al repositori:

```bash
git status
```

Si veus `.env`, `.db` o altres fitxers sensibles, NO els pugis.

## Validacio

Has acabat si:
- [ ] Has fet un inventari local amb les comandes
- [ ] Has configurat minim una mesura de privadesa al navegador
- [ ] Has comparat una resposta local vs nuvol
- [ ] Has documentat les conclusions a `proves_privadesa.md`
- [ ] El teu `.gitignore` evita pujar fitxers sensibles

## Per aprofundir

- Investiga quines dades recullen els serveis al nuvol que usaves abans (llegeix els termes del servei).
- Configura un tallafocs a la RPi per limitar acces extern a Ollama.
- Xifra el directori `~/.ollama` si la teva RPi es accessible fisicament.
- Considera un sistema mixt: local per defecte, nuvol nomes per a tasques que necessitin potencia.
