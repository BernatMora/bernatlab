# Exercici practic - Capitol 1: Contenidors avançats

> 30-45 min · Real al teu sistema

## Objectiu

Construir una petita aplicacio Python, crear-ne un Dockerfile optimitzat amb multi-stage, i comparar la mida amb una versio "ingenuua". Acabaras entenent per que els multi-stage son tan importants.

## Requisits

- Docker instal·lat a la RPi
- Coneixement basic de Python (o qualsevol llenguatge)
- 30-45 minuts

## Pas 1: Prepara el projecte (5 min)

Crea una carpeta de treball a la teva maquina local o a la RPi:

```bash
mkdir -p ~/proves-docker/multi-stage
cd ~/proves-docker/multi-stage
```

Crea un fitxer `app.py` molt simple:

```python
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hola des del contenidor multi-stage!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
```

I un `requirements.txt`:

```
flask==3.0.0
```

## Pas 2: Crea el Dockerfile "ingenuu" (5 min)

```dockerfile
# Dockerfile.naive
FROM python:3.12
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8000
CMD ["python", "app.py"]
```

Construeix-lo:

```bash
docker build -f Dockerfile.naive -t bernatlab-naive .
```

Mira la mida:

```bash
docker images bernatlab-naive
# Probablement ~1 GB 😱
```

## Pas 3: Crea el Dockerfile optimitzat (10 min)

Ara la versio multi-stage:

```dockerfile
# Dockerfile.optim
FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY app.py .
ENV PATH=/root/.local/bin:$PATH
USER 1000
EXPOSE 8000
CMD ["python", "app.py"]
```

Construeix-lo:

```bash
docker build -f Dockerfile.optim -t bernatlab-optim .
```

Compara les mides:

```bash
docker images | grep bernatlab
```

Hauries de veure una reduccio drastica (de ~1 GB a ~150 MB o menys).

## Pas 4: Prova els dos contenidors (10 min)

```bash
# Arrenca el naive
docker run -d --name naive -p 8001:8000 bernatlab-naive

# Arrenca l'optim
docker run -d --name optim -p 8002:8000 bernatlab-optim

# Comprova que funcionen
curl http://localhost:8001
curl http://localhost:8002

# Mira les capes de cada imatge
docker history bernatlab-naive
docker history bernatlab-optim
```

## Pas 5: Inspecciona i neteja (5 min)

```bash
# Atura i elimina els contenidors
docker stop naive optim
docker rm naive optim

# Mira quantes capes te cada imatge
docker history bernatlab-naive --no-trunc
docker history bernatlab-optim --no-trunc

# Neteja les imatges de prova
docker rmi bernatlab-naive bernatlab-optim
```

## Pas 6: Crea un .dockerignore (5 min)

Crea un fitxer `.dockerignore` al mateix directori:

```
.git
.gitignore
__pycache__
*.pyc
*.pyo
.DS_Store
README.md
Dockerfile.naive
```

Ara qualsevol `docker build` nomes copiara el que toca. Refes el build optimitzat i observa el `Sending build context to Docker daemon` que es molt mes petit.

## Validacio

Has acabat si:

- [ ] Has creat una app Python minima.
- [ ] Has construit dues imatges: una naive (~1 GB) i una optimitzada (~150 MB).
- [ ] Has vist la diferencia de mida amb `docker images`.
- [ ] Has provat que ambdues imatges funcionen.
- [ ] Has creat un `.dockerignore` efectiu.

## Per aprofundir

- Prova amb `python:3.12-alpine` en lloc de `-slim`. Encara es mes petit, pero potser calen mes dependencies natives.
- Investiga què fa `--no-cache-dir` a pip.
- Compara el temps de build amb i sense cache: `docker build --no-cache -t test .`
- Mira quina es la diferencia real entre `COPY` i `ADD`.
