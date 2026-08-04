# Comandes útils per al repo bernatlab

Aquest és un resum de les operacions més habituals. Per a una guia completa, consulta el **Mòdul 1, Capítol 9 (Git i documentació)** del llibre.

## Estat del repo

```bash
git status
git log --oneline -10
```

## Workflow de publicació d'un capítol

1. Editar o crear el capítol a `book/chapters/`.
2. Regenerar els artefactes:
   ```bash
   cd book && python make_book.py
   ```
3. Validar canvis:
   ```bash
   git status
   git diff --stat
   ```
4. Publicar:
   ```bash
   python homelab/scripts/publish.py "Capítol 23 — primer esborrany"
   ```
   O manualment:
   ```bash
   git add book/chapters/ book/output/
   git commit -m "Capítol 23 — primer esborrany"
   git push
   ```

## Treballar amb el submodule hort-osona

### Primera vegada (ja fet)

```bash
git submodule add https://github.com/BernatMora/hort-osona.git projects/hort-osona
git commit -m "Add hort-osona as submodule"
git push
```

### Actualitzar hort-osona dins BernatLab

Quan hi hagi canvis nous al repo hort-osona:

```bash
cd projects/hort-osona
git pull origin main
cd ../..
git add projects/hort-osona
git commit -m "Actualitza hort-osona"
git push
```

### Clonar bernatlab amb el submodule

En una màquina nova (Raspberry, Mac, etc.):

```bash
git clone https://github.com/BernatMora/bernatlab.git
cd bernatlab
git submodule update --init --recursive
```

## Sincronitzar a la Raspberry Pi 4

Quan la RPi estigui disponible i tingui claus SSH configurades:

```bash
# Des del PC: enviar canvis
ssh bernat@100.x.y.z 'cd /home/bernat/bernatlab && git pull'
```

O configurar un `post-receive` hook al servidor perquè el pull sigui automàtic.

## Crear una nova branca per experimentar

```bash
git checkout -b provant-canvis-capitol-12
# fer canvis
git add book/chapters/12-mqtt-des-de-zero.md
git commit -m "Prova: reformulo secció 12.3"
git push -u origin provant-canvis-capitol-12
```

Quan estigui llest, fusionar a `main`:

```bash
git checkout main
git merge provant-canvis-capitol-12
git push
git branch -d provant-canvis-capitol-12
git push origin --delete provant-canvis-capitol-12
```

## Veure l'historial del llibre

```bash
git log --oneline -- book/
git log --oneline -- book/chapters/12-mqtt-des-de-zero.md
```
