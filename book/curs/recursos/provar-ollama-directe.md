# Solucio: provar Ollama directament desde la RPi

Ara sabem que el codi es correcte pero falla al connectar. La causa mes probable es:

1. **Timeout massa llarg** pero la RPi encara no sha acabat de carregar el model
2. **Ollama esta parat** (pero curl ha respos abans, raro)
3. **El model gemma3:1b sha de carregar** a memoria la primera vegada (pot trigar 30-60s)

## Prova directa amb la mateixa crida que fa el bot

Aquesta es exactament la crida que fa `ask_ollama()` des de rag.py. Executala
a la RPi:

```bash
curl -s http://localhost:11434/api/generate -d '{
  "model": "gemma3:1b",
  "prompt": "Hola, em pots sentir?",
  "stream": false,
  "options": {
    "temperature": 0.4,
    "num_predict": 600
  }
}' --max-time 180
```

Aixo fara exactament el que fa el bot. Pot trigar 30-180 segons la primera
vegada (carrega el model a memoria).

## Si funciona

Retorna JSON amb un camp "response" amb text. Si passa, **el problema NO es Ollama**.

Llavors el problema es al **servei systemd** que te un contexte diferent.

Comprova:

```bash
# Com a quin usuari corre el servei?
sudo systemctl show hort-osona-telegram -p User

# Quin directori te?
sudo systemctl show hort-osona-telegram -p WorkingDirectory
sudo systemctl show hort-osona-telegram -p EnvironmentFiles

# Comprova que pot accedir a localhost:11434
sudo -u bernat curl -s http://localhost:11434/api/tags
```

Si aixo funciona, el servei hauria de funcionar tambe.

## Si la crida directa tambe falla

Llavors es un problema real d'Ollama o del model.

Comprova:

```bash
# 1. Hi ha memoria disponible?
free -h

# 2. La CPU no esta saturada?
top -bn1 | head -10

# 3. Ollama esta realment actiu?
ps aux | grep ollama | grep -v grep

# 4. Carrega el manualment
ollama run gemma3:1b "Hola"
# Si funciona, sha carregat be
```

## Si tot funciona pero el bot falla

Llavors es un problema de permisos o de contexte del servei. Comparteix:
- Sortida de `sudo systemctl show hort-osona-telegram -p User`
- Sortida de `sudo -u bernat curl -s http://localhost:11434/api/tags`
- El log recent del bot

I trobarem el problema exacte.
