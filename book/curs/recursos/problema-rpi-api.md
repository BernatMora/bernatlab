# Solucio: el problema pot ser RPI_API_URL

Ollama funciona perfectament (acabes de provar-ho: 25s per carregar el model,
pero respon). Pero el bot falla igual.

Aixo vol dir que el problema NO es Ollama. Es **un altre pas del bot**.

Recorda el .env:
```
RPI_API_URL=http://hortpi.local:8000
```

Aquesta URL apunta a "hortpi.local" que probablement no existeix.
Si el bot intenta conectar a aquesta URL ABANS de Ollama, pot ser que falli
abans d'arribar a Ollama.

## Comprovacio 1: Aquesta URL existeix?

```bash
ping -c 2 hortpi.local
nslookup hortpi.local
```

Si no respon, "hortpi.local" no existeix a la teva xarxa.

## Comprovacio 2: Quin altre pas fa el bot?

A telegram_bot.py hi ha mes coses. Mira les linies 195-220 (aprox):

```bash
sed -n '195,230p' /home/bernat/hort-osona/hort-osona-iot/telegram_bot.py
```

Volem veure com el bot processa un missatge. Segurament fa:
1. Rep missatge de Telegram
2. Busca paraules clau al RAG
3. Truca a Ollama per generar resposta

Pero tambe pot:
- Trucar a la RPi (RPI_API_URL) per obtenir dades de sensors
- Si aixo falla, pot capturar lerror i mostrar el missatge d'Ollama

## Comprovacio 3: Mira el log quan envies un missatge

Despres denviar un missatge al bot, mira el log:

```bash
tail -100 /home/bernat/hort-osona/hort-osona-iot/logs/telegram_bot.log
```

Volem veure si hi ha alguna excepcio abans que el bot enviï la resposta
"No es pot connectar amb Ollama".

## La causa mes probable

El bot processa el missatge, intenta fer alguna cosa amb RPI_API_URL,
aquesta falla, i el codi captura lerror pero mostra el missatge d'Ollama
perque es el que toca.

O be: el bot intenta accedir a hortpi.local, que es la seva RPi, pero la
RPi no respon (potser perque el servei no esta actiu, o perque el hostname
no sha configurat).

## Solucio temporal

Si vols que el bot funcioni sense sensors, **desactiva RPI_API_URL** o
canvia la URL a localhost (per a que no intenti accedir a una altra maquina).

```bash
nano /home/bernat/hort-osona/hort-osona-iot/.env
# Canvia:
# RPI_API_URL=http://hortpi.local:8000
# a:
# RPI_API_URL=http://localhost:8000

# Comenta la linia si vols
# RPI_API_URL=
```

Despres:
```bash
sudo systemctl restart hort-osona-telegram
```

Pero abans, **comprova que el problema es aquest**. Prova enviar un missatge
al bot i mira el log immediatament.
