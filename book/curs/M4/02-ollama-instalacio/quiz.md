# Qüestionari - Capitol 2: Instal·lar Ollama, primers passos

> 15 preguntes · ~20 min · 7 test + 8 obertes

## Pregunta 1
Que es Ollama?

- [ ] Un editor de text per a LLM
- [x] Un runtime que et permet executar LLMs localment amb quatre comandes
- [ ] Una empresa que ven accés a GPT-4
- [ ] Un model de llenguatge de Meta

## Pregunta 2
Quina comanda instal·la Ollama a Linux?

- [ ] apt install ollama
- [x] curl -fsSL https://ollama.com/install.sh | sh
- [ ] npm install ollama
- [ ] docker pull ollama

## Pregunta 3
Quin port per defecte fa servir l'API REST d'Ollama?

- [ ] 80
- [ ] 443
- [x] 11434
- [ ] 8080

## Pregunta 4
Quina comanda descarrega un model?

- [ ] ollama get
- [ ] ollama download
- [x] ollama pull
- [ ] ollama fetch

## Pregunta 5
Quin d'aquests models es el mes recomanable per defecte a una Raspberry Pi 4 amb 4 GB de RAM?

- [ ] mistral:7b
- [x] llama3.2:3b
- [ ] llama3.1:70b
- [ ] gpt-4

## Pregunta 6
Que fa la comanda `ollama serve`?

- [ ] Inicia una sessio de xat interactiva
- [ ] Descarrega un model
- [x] Exposa l'API REST al port 11434 per poder cridar el LLM des d'altres programes
- [ ] Atura tots els models en execucio

## Pregunta 7
Com es pot comprovar que el servei d'Ollama esta actiu a la RPi?

- [ ] ollama check
- [x] systemctl status ollama
- [ ] ps aux | grep ollama
- [ ] netstat -tlnp

## Pregunta 8 (oberta)
Explica amb les teves paraules: quines son les tres analogies mes encertades per descriure Ollama? Pensa en altres eines que ja coneixes.

Pistes per respondre:
- Analogia 1: amb Docker (runtime, imatges, registre).
- Analogia 2: amb un player multimèdia (cataleg, descarregar, reproduir).
- Analogia 3: amb npm o pip (paquets, registre, comandes).
- Que te Ollama d'especial respecte aquestes analogies?

## Pregunta 9 (oberta)
Per que creus que Ollama ha triat el port 11434 i no un mes convencional com el 8080 o el 5000? Investiga i raona.

Pistes per respondre:
- El port 11434 es alt i poc usual.
- Evita conflictes amb serveis web tradicionals.
- Es una decisio de branding o tecnica?
- Aixo afecta el BernatLab quan expose Ollama a Internet?

## Pregunta 10 (oberta)
Imagina que acabes d'instal·lar Ollama a la teva RPi del BernatLab. Quins son els tres primers pasos que faries per posar-ho en marxa de manera segura? Justifica cada pas.

Pistes per respondre:
- Pas 1: descarregar un model petit per provar.
- Pas 2: verificar que l'API nomes escolta a localhost.
- Pas 3: NO expose Ollama directament a Internet.
- Que riscos hi ha si expose Ollama a Internet sense autenticacio?

## Pregunta 11 (oberta)
Quina relacio hi ha entre el model que descarregues amb `ollama pull` i la imatge Docker que descarregues amb `docker pull`? Pensa en comandes, emmagatzematge, neteja.

Pistes per respondre:
- Comandes similars: pull, run, list, rm.
- Emmagatzematge: imatges vs models, /var/lib/docker vs /usr/share/ollama.
- Compartir entre maquines: docker save/load vs export/import.
- Que passa si tens molts models ocupant espai?

## Pregunta 12 (oberta)
Compara l'experiencia d'usar Ollama a la Raspberry Pi amb un Mac amb M2. Quines diferencies notaries en velocitat, capacitat de model i consum electric?

Pistes per respondre:
- La RPi te CPU ARM, 4 GB RAM, 5-10W de consum.
- El Mac M2 te GPU Neural Engine, 8-32 GB RAM unificada, 20-40W.
- Mateix model (llama3.2:3b) a cada maquina: quants tokens per segon?
- Això es rellevant per triar on allotjar el model?

## Pregunta 13 (oberta)
Si tens una Raspberry Pi amb 4 GB de RAM i vols correr un model de 7B, que pot passar? Quines solucions tens?

Pistes per respondre:
- El model en Q4 ocupa uns 4-5 GB, mes que la RAM disponible.
- El sistema pot usar swap (targeta microSD): lent.
- Pot haver OOM kills (matar processos).
- Solucions: triar un model mes petit, augmentar swap, usar un servidor extern.

## Pregunta 14 (oberta)
Per a que serveix el directori `/usr/share/ollama/.ollama` al sistema de fitxers? Que hi ha dins? Que passaria si es queda sense espai?

Pistes per respondre:
- Es el directori per defecte on Ollama guarda els models descarregats.
- Conte subcarpetes per cada model (blobs, manifests).
- Si el disc queda ple, els nous pull's fallen.
- Com ho gestionaries al BernatLab amb una microSD de 32 GB?

## Pregunta 15 (oberta)
Argumenta la teva posicio: prefereixes executar Ollama com a servei systemd o com a contenidor Docker al BernatLab? Pesa avantatges i inconvenients.

Pistes per respondre:
- Systemd: integracio directa amb el sistema, mes rapid, nomes un shell.
- Docker: aillament, portabilitat, coexistir amb altres serveis.
- Cas concret: el BernatLab ja te molts serveis en contenidors.
- Tria final: defensa-la amb un argument practic.
