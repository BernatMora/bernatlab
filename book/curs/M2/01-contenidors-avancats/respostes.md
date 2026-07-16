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

## Que fer si has fallat moltes preguntes

- **5-8 encerts**: Rellegir el resum i fer l'exercici practic.
- **3-4 encerts**: Refes l'exercici desde zero observant cada pas.
- **0-2 encerts**: Repassem junts el capitol abans de continuar.

## Que fer si has encertat totes

- Passa al **Capitol 2** (volums persistents).
- Experimenta amb altres llenguatges: Node.js, Go, Rust.
- Investiga les imatges distroless: https://github.com/GoogleContainerTools/distroless
