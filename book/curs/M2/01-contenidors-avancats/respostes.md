# Respostes - Capitol 1: Contenidors avançats

> Mira les respostes DESPRES d'haver fet el qüestionari.

## Pregunta 1: Que es una capa?

**Resposta correcta**: Un diff del sistema de fitxers creat per cada instruccio del Dockerfile.

**Explicacio**: Cada `RUN`, `COPY` o `ADD` genera una capa nova que Docker guarda i pot reutilitzar. Es el que fa que Docker sigui rapid: si una capa no canvia, es recupera de la cache.

---

## Pregunta 2: Quina instruccio crea una capa?

**Resposta correcta**: RUN.

**Explicacio**: `RUN` executa una comanda durant el build i els canvis es guarden com una capa. `CMD` i `ENTRYPOINT` son metadades (no creen capes), i `EXPOSE` nomes documenta un port.

---

## Pregunta 3: Per que multi-stage?

**Resposta correcta**: Per obtenir imatges finals mes petites, sense eines de build.

**Explicacio**: Multi-stage separa "construir" de "executar". La primera etapa pot tenir compiladors, node_modules de dev, etc. La segona etapa nomes copia el que cal per executar. Resultat: imatges 5-20 vegades mes petites.

---

## Pregunta 4: RUN vs CMD?

**Resposta correcta**: RUN executa durant el build; CMD es la comanda per defecte quan arranca el contenidor.

**Explicacio**: `RUN` es temps de build. `CMD` es temps d'execucio. Pots tenir-les totes dues al mateix Dockerfile. De fet, es habitual: un `RUN` per instal·lar coses i un `CMD` per llançar l'app.

---

## Pregunta 5: Avantatge de combinar `RUN`?

**Resposta correcta**: Es redueix el nombre de capes i la mida final de la imatge.

**Explicacio**: Tres `RUN` separats = tres capes. Un sol `RUN` amb `&&` = una sola capa. A mes, Docker pot netejar fitxers temporals dins del mateix `RUN` sense que quedin a la capa següent.

---

## Pregunta 6: Per que no `ubuntu:latest`?

**Resposta correcta**: Perque 'latest' pot canviar i el teu build pot trencar-se mes endavant.

**Explicacio**: `latest` es un tag mutable. Avui es la 24.04, demà la 24.10. Si el teu build depen de paquets específics, es trencara. Sempre fixa una versio: `ubuntu:24.04` o `debian:12-slim`.

---

## Pregunta 7: Comanda per veure les capes?

**Resposta correcta**: `docker history bernatlab-api:latest`.

**Explicacio**: `docker history` mostra cada capa amb la seva mida, quan es va crear i quina instruccio l'ha generada. Es molt util per trobar "quins paquets m'inflen la imatge?".

---

## Pregunta 8: Que fa `USER 1000`?

**Resposta correcta**: Fa que el contenidor NO s'executi com a root.

**Explicacio**: Per defecte, Docker executa com a root dins el contenidor. Si un atacant explota una vulnerabilitat, tindra root al contenidor. `USER 1000` (o qualsevol UID no-root) redueix el risc. Es una bona practica de seguretat que veurem al cap 6.

---

## Pregunta 9 (oberta): Imatge vs contenidor

**Resposta model**:

Una **imatge Docker** es com una recepta de cuina o un plànol d'arquitectura. Es un fitxer de lectura nomes que conte tot el que cal per executar l'aplicacio: el sistema base, les dependencies, el codi, la configuracio. No esta "viu", nomes existeix com a definicio. La pots guardar al Docker Hub, en un registre privat, o en un fitxer `.tar`.

Un **contenidor** es una instancia en execucio d'aquesta imatge. Es la "casa construïda a partir del plànol". Te el seu propi sistema de fitxers (una copia de la imatge), la seva xarxa, els seus processos, i esta aillat del sistema amfitrio.

Exemple de la vida quotidiana: la imatge es com una **plantilla de paper d'empaperar** que pots trobar a una botiga. Un cop la compres, la pots posar a la paret del menjador (contenidor 1), a la paret del dormitori (contenidor 2), etc. Tots dos son "contenidors" amb la mateixa imatge, pero son instancies independents.

Pots tenir **molts contenidors** a partir de la **mateixa imatge**, igual que pots tenir moltes finestres amb la mateixa planta. Si vols actualitzar el paper, has de canviar la plantilla (imatge) i tornar a empaperar (recrear el contenidor).

---

## Pregunta 10 (oberta): Com fer la imatge mes petita?

**Resposta model**:

Per tenir una imatge Docker el mes petita possible per a una app Python amb dependencies pesades, faria servir **multi-stage build**:

1. **Etapa 1 (builder)**: uso una imatge amb les eines de build (`python:3.12`), instal·lo totes les dependencies amb `pip install --user` a un directori concret (ex. `/install`).

2. **Etapa 2 (runtime)**: uso una imatge minima (`python:3.12-slim` o fins i tot `python:3.12-alpine`), copio nomes `/install` des de l'etapa 1 amb `COPY --from=builder`, i copio nomes el codi font (`app.py`).

3. **Sistema base**: triaria `python:3.12-slim` (~150 MB) o `alpine` (~50 MB pero requereix compilacio de moltes dependencies natives).

4. **`requirements.txt` separat**: copio primer nomes `requirements.txt`, faig `pip install`, i DESPRES copio el codi. Aixi les dependencies es cachejen i el build es rapidissim.

5. **`.dockerignore`**: creo un fitxer que exclou `.git`, `__pycache__`, `*.pyc`, fitxers de test, documentacio. Aixi el context del build es minim.

6. **`--no-cache-dir`**: passo aquesta flag a pip perque no guardi la cache de paquets (que pot ser 50-100 MB).

7. **Usuari no-root**: acabo el Dockerfile amb `USER 1000` per seguretat, tot i que no afecta la mida.

El resultat seria passar d'**~1 GB** (imatge naive) a **~150-200 MB** (multi-stage optimitzat), o fins i tot **~80 MB** si uso Alpine. A una RPi amb microSD de 32 GB, aquesta diferencia es vital.

---

## Pregunta 11 (oberta): Cache de capes i iteracio del codi

**Resposta model**:

Docker emmagatzema cada capa per separat i la identifica pel seu hash. Si una capa no canvia entre builds, la recupera de la cache local en lloc de tornar-la a crear. Això es magic per a la velocitat: un build que trigaria 5 min pot trigar 10 segons si nomes ha canviat una capa.

Aixo canvia la manera d'escriure el Dockerfile quan preveus iteracio. La regla daur: **copia el que canvia menys primer, i el que canvia mes al final**. Concretament:

1. Primer copio nomes el fitxer de dependencies (`requirements.txt` o `package.json`).
2. Instaŀlo les dependencies (RUN pip install).
3. DESPRES copio la resta del codi amb `COPY . .`.

Aixi, quan iteres el codi (cosa que fas cada setmana al BernatLab), nomes es refa la capa del codi. La capa de dependencies queda intacta i es recupera instantaniament. Si ho fessis al reves (copiar tot i despres instaŀlar), cada canvi de codi forçaria reinstaŀlar totes les dependencies.

Al BernatLab concretament, això vol dir que una actualitzacio tipica d'una app (tocar un `.py`) passa de tardar 2 min a tardar 5 segons. Diferencia enorme quan estas provant coses.

---

## Pregunta 12 (oberta): Mida d'imatge i velocitat de desplegament

**Resposta model**:

La mida de la imatge afecta el desplegament en tres punts:

1. **Descarrega**: si fas `docker pull bernatlab-api:latest` i la imatge pesa 1 GB, a la xarxa de la RPi (sovint 100 Mbps o menys) tardarà mes d'un minut. Si nomes pesa 100 MB, baixa en 8 segons. Al BernatLab amb connexió no sempre bona, aixo importa.

2. **Espai en disc**: la RPi te una microSD o SSD limitat (32-256 GB habitualment). Si cada imatge pesa 1 GB, nomes tens per a 20-30 serveis. Si pesen 100 MB, tens per a centenars.

3. **Arrencada**: tot i que Docker no descomprimeix tota la imatge, una imatge mes gran te mes capes i el daemon triga mes a validar-les. A una RPi amb CPU limitat, la diferencia entre 5 capes i 50 capes es nota.

4. **RAM en execucio**: la capa escribible i les pagines de memoria carregades es relacionen amb la mida. Una imatge amb milers de fitxers petits (cas Alpine vs Debian) consumeix mes RAM per la gestio de inodes.

Al BernatLab (100.115.134.76), on el temps de resposta des de que decideixo actualitzar fins que esta disponible es important, tenir imatges de 100-200 MB en lloc de 1 GB marca la diferencia. Per això els multi-stage builds son la primera optimitzacio que cal fer.

---

## Pregunta 13 (oberta): Explicar el "magic" de Docker a un company

**Resposta model**:

Si un company pensa que Docker es magic, li explicaria amb una analogia senzilla i despres amb el detall tecnic:

**Analogia**: Docker es com una **maquina de cafe amb càpsules**. La càpsula es la imatge (premesclada, estandard). Tu poses la càpsula a la maquina (el teu ordinador) i surt un cafe (el contenidor en execucio). El mateix tipus de càpsula et pot donar el mateix cafe a qualsevol maquina. Si el cafe es dolent, llences la càpsula i en poses una de nova.

**Detall tecnic**: per sota, Docker fa servir tres conceptes:

- **Imatge**: es un "paquet" de lectura nomes que conte el sistema de fitxers base, les dependencies i el codi. Es com un fitxer `.tar` comprimit pero optimitzat per capes. Esta guardada al registr (Docker Hub, un registre privat, o localment).

- **Contenidor**: quan fas `docker run`, Docker agafa la imatge, afegeix una capa escribible buida a sobre, i executa un procés dins d'aquesta capa. Aquest procés veu un sistema de fitxers propi pero comparteix el kernel de Linux amb l'amfitrio.

- **Copy-on-write**: quan el contenidor vol modificar un fitxer de la imatge, Docker el copia primer a la capa escribible. Els fitxers no modificats es comparteixen entre tots els contenidors de la mateixa imatge. Per això 10 contenidors de nginx no ocupen 10x l'espai.

Aixo es el que el company no veu: la "cache" del kernel, les capes compartides, el sistema de fitxers aillat, la xarxa virtual. Per ell nomes es veu: escric `docker run nginx` i funciona. Per tu, ara, ja saps per que funciona.

---

## Pregunta 14 (oberta): Multi-stage build per a FastAPI amb pandas

**Resposta model**:

Per una aplicacio FastAPI amb `pandas` i `numpy`, el Dockerfile amb multi-stage tindria dos `FROM`:

```dockerfile
# Etapa 1: builder (imatge gran amb compiladors)
FROM python:3.12 AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt
COPY . .
# Opcional: compilacio AOT o pas addicional si cal

# Etapa 2: runtime (imatge minima)
FROM python:3.12-slim
WORKDIR /app
# Copiem nomes les dependencies instal·lades, no el codi font del builder
COPY --from=builder /root/.local /root/.local
COPY . .
ENV PATH=/root/.local/bin:$PATH
USER 1000
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]
```

**Bloc 1 (builder)**: uso `python:3.12` (imatge completa, ~1 GB) perque te `gcc`, `make` i altres eines que `pandas` necessita per compilar les parts en C. Instaŀlo totes les dependencies a `/root/.local` amb `--user` per tenir-les separades del sistema.

**Bloc 2 (runtime)**: uso `python:3.12-slim` (~150 MB) que es la versio minima sense compiladors. Copio nomes `/root/.local` del builder (les dependencies ja compilades) i el codi font. El resultat es una imatge d'uns 200-300 MB en lloc d'1 GB.

**Per que funciona**: `pandas` i `numpy` un cop compilats, son fitxers `.so` (llibreries compartides) que no necesiten gcc per executar-se. Per tant, podem compilar-les al builder i nomes portar els `.so` i els `.py` al runtime. Es el mateix principi que `go build` que genera un binari estatic.

Al BernatLab, aixo significa que el deploy de l'API es rapid, l'actualitzacio nomes toca el codi (la capa fina), i la imatge base es pot reutilitzar per a altres serveis Python.

---

## Pregunta 15 (oberta): Alpine vs debian-slim al BernatLab

**Resposta model**:

La decisio entre `alpine` i `debian-slim` te varios eixos:

**Mida final**:
- Alpine: ~50 MB de base. Imatge final tipica: 80-150 MB.
- Debian-slim: ~150 MB de base. Imatge final tipica: 200-400 MB.

**Compatibilitat de llibreries**:
- Alpine usa `musl` en lloc de `glibc`. Moltes llibreries natives assumeixen glibc i fallen o tenen bugs subtils. Exemples classics: `numpy`, `cryptography`, `psycopg2`.
- Debian-slim usa `glibc` (mateixa que Ubuntu). Totes les llibreries estandard funcionen.

**Temps de build**:
- Alpine triga mes perque ha de compilar dependencies natives des de font (no hi ha binaris precompilats per a musl).
- Debian-slim te binaris precompilats per a `manylinux`, molt mes rapid.

**Seguretat**:
- Alpine te menys paquets i una superficie d'atac mes petita. Pero tambe te un gestor de paquets menys madur (apk).
- Debian-slim te mes paquets pero tots auditats per la comunitat Debian (reputacio de estabilitat).

**Recomanacio per al BernatLab**:
- Per a serveis simples (nginx, alpine, scripts Python sense dependencies natives): **Alpine** perfecte.
- Per a serveis amb dependencies natives (pandas, cryptography, opencv): **Debian-slim**. Estalvia temps de build i mal de cap.
- Per a serveis de produccio on la mida importa molt (desplegaments repetits): **Alpine** si tot funciona.
- Per a un homelab amb temps limitat: **Debian-slim** per defecte. La diferencia de 100 MB no justifica els possibles problemes de compatibilitat.

Personalment, al BernatLab uso Debian-slim per defecte i nomes passo a Alpine quan la imatge es critica per mida o per algun motiu especific (com ara imatges de Go o Rust ja optimitzades amb base Alpine).

---

## Que fer si has fallat moltes preguntes

- **5-8 encerts**: Rellegir el resum i fer l'exercici practic.
- **3-4 encerts**: Refes l'exercici desde zero observant cada pas.
- **0-2 encerts**: Repassem junts el capitol abans de continuar.

## Que fer si has encertat totes

- Passa al **Capitol 2** (volums persistents).
- Experimenta amb altres llenguatges: Node.js, Go, Rust.
- Investiga les imatges distroless: https://github.com/GoogleContainerTools/distroless
