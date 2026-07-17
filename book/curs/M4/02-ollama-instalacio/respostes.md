# Respostes - Capitol 2: Instal·lar Ollama, primers passos

> Mira les respostes DESPRES d'haver fet el qüestionari.

## Pregunta 1: Que es Ollama?

**Resposta correcta**: Un runtime que et permet executar LLMs localment amb quatre comandes.

**Explicacio**: Ollama es el "Docker dels models": descarregues imatges (models), les executes, i tens un API REST llest. No es un editor, ni una empresa, ni un model. Es la infraestructura per fer anar els models al teu hardware.

---

## Pregunta 2: Comanda d'instal·lacio a Linux

**Resposta correcta**: `curl -fsSL https://ollama.com/install.sh | sh`.

**Explicacio**: Ollama proporciona un script oficial que detecta la teva distro i arquitectura, descarrega el binari adient, i configura un servei systemd. Les altres opcions (apt, npm, docker) no son oficials o son incorrectes.

---

## Pregunta 3: Port de l'API REST

**Resposta correcta**: 11434.

**Explicacio**: Es el port per defecte. Nomes es un numero, pero es bo recordar-lo per si vols fer probes amb curl o configurar un proxy invers. Es el "punt d'entrada" al LLM desde qualsevol llenguatge.

---

## Pregunta 4: Descarregar un model

**Resposta correcta**: `ollama pull`.

**Explicacio**: Segueix la convencio de Docker. Es intuitiu i consistent amb altres eines. Un cop descarregat, el model queda al disc i es pot fer servir sense tornar-lo a baixar.

---

## Pregunta 5: Model per defecte a RPi 4

**Resposta correcta**: `llama3.2:3b`.

**Explicacio**: Ocupa uns 2.5 GB de RAM, deixa marge per al sistema operatiu, i dona una qualitat acceptable. El 7B no cap als 4 GB. El 1B es massa basic. El 70B nomes en servidors professionals.

---

## Pregunta 6: Que fa `ollama serve`?

**Resposta correcta**: Exposa l'API REST al port 11434.

**Explicacio**: A Linux amb systemd ja ho fa automaticament. Pero a altres entorns o si vols canviar el port, pots executar-lo manualment. La diferencia amb `ollama run` es que `serve` es per rebre peticions HTTP, no per xatejar.

---

## Pregunta 7: Comprovar el servei actiu

**Resposta correcta**: `systemctl status ollama`.

**Explicacio**: Es la comanda estandard per veure l'estat d'un servei systemd a Linux. Mostra si esta "active (running)", quin PID te, i els ultims logs. Les altres opcions no son la manera correcta (ps es generic, netstat nomes veus ports).

---

## Pregunta 8 (oberta): Tres analogies per descriure Ollama

**Resposta model**:

**Analogia 1 - Ollama es el Docker dels models**: igual que Docker te imatges que contenen tot el necessari per executar una app, Ollama te models que contenen tot el necessari per generar text. Les comandes son analogues: `pull` per descarregar, `run` per executar, `list` per veure quins tens, `rm` per esborrar. Si saps Docker, saps Ollama.

**Analogia 2 - Ollama es un player multimèdia**: tens una llibreria de models (com una llibreria de pel·licules), els descarregues una vegada (`pull`), els executes per consumir el contingut (`run`). La gracia esta en tenir el cataleg a la punta dels dits.

**Analogia 3 - Ollama es un npm o pip per a LLMs**: igual que npm te un registre central de paquets JavaScript i pip te un registre de paquets Python, Ollama te un registre de models. El flux es el mateix: cerques, descarregues, uses. La diferencia es que els models son molt mes grans (GB en lloc de MB) i requereixen mes recursos per executar.

El que fa Ollama especial: mentre que les analogies anteriors son per a COSES que fas servir, Ollama et dona un **servei** que pot ser cridat desde qualsevol altre programa. Es mes semblant a una base de dades que a una eina local: hi envies peticions i reps respostes. Per tant, la analogia mes precisa seria: Ollama es un **PostgreSQL dels LLMs**.

---

## Pregunta 9 (oberta): Per que el port 11434?

**Resposta model**:

El port 11434 es una decisio de branding i conveniencia. Analitzem-ho:

**Numero alt i poc usual**: els ports baixos (0-1023) son reservats al sistema. Els ports mitjans (1024-49151) son els habituals per a serveis (8080 HTTP alternatiu, 5432 PostgreSQL, 3306 MySQL, 6379 Redis). El 11434 esta en una zona on es improbable que coincideixi amb res mes.

**Branding subtil**: si mires la numeracio, 1-1-4-3-4 es facil de recordar i pronuncia com a "one-one-four-three-four". Es un port escollit amb cura per ser memorable.

**Conflict avoidance**: si Ollama hagues escollit 8080, xocaria amb milers d'aplicacions web. Si hagues escollit 5000, xocaria amb Flask per defecte. El 11434 minimitza el risc de conflictes.

**Implicacio al BernatLab**: si vols exposar Ollama a Internet (cosa que NO recomano sense autenticacio), has de fer un reverse proxy (Nginx, Caddy) que escolti al 443 i redirigeixi al 11434 nomes per a peticions autenticades. Mai expose el 11434 directament: un atacant podria usar el teu model i els teus recursos (o pitjor, entrenar-se amb les teves dades si envies informacio sensible).

---

## Pregunta 10 (oberta): Tres primers pasos segurs

**Resposta model**:

**Pas 1: Descarregar un model petit per provar**. Començo amb `llama3.2:1b` perque nomes ocupa 1.3 GB i puc verificar que tot funciona sense saturar la RPi. Un cop confirmat que Ollama respon, ja descarregare models mes grans.

**Pas 2: Verificar que l'API nomes escolta a localhost**. Comprovo amb `ss -tlnp` o `netstat -tlnp` que el port 11434 esta en `127.0.0.1:11434` i NO en `0.0.0.0:11434`. Si escolta a totes les interfaces, qualsevol maquina de la xarxa pot cridar el LLM sense cap autenticacio. Es un risc greu.

**Pas 3: NO expose Ollama directament a Internet**. Si vull accedir al LLM des de fora de casa, uso Tailscale (xarxa privada) o un reverse proxy amb autenticacio. Mai obro el port 11434 al router.

Riscos d'exposar Ollama a Internet sense autenticacio:
- Us abusiu: un atacant pot fer peticions fins a col·lapsar la RPi.
- Extraccio de dades: si algun dia passo context sensible al LLM, l'atacant pot capturar les peticions.
- Cost economic: si mes endavant uso un LLM comercial al nuvol, les peticions dels altes les pago jo.

---

## Pregunta 11 (oberta): Ollama vs Docker

**Resposta model**:

La analogia es forta, pero hi ha diferencies importants:

**Comandes similars**: ambdues eines usen `pull`, `run`, `list`/`ps`, `rm`/`rmi`, etc. La consistencia es deliberada: si saps Docker, la corba d'aprenentatge d'Ollama es minima.

**Emmagatzematge**: Docker guarda les imatges a `/var/lib/docker` (o el directori configurat). Ollama les guarda a `/usr/share/ollama/.ollama/models` per defecte. Els models d'Ollama son mes grans (GB en lloc de MB) perque contenen pesos d'una xarxa neuronal.

**Cleanup**: ambdues eines tenen `prune` o subcomandes per netejar. Pero Ollama no te un sistema de "dangling images" automatic. Cal vigilar manualment.

**Diferencia conceptual**: Docker ailla aplicacions del sistema amfitrio. Ollama **comparteix** recursos amb el sistema (CPU, RAM, GPU). Un model en execucio no te cap aillament de xarxa ni de filesystem: pot llegir fitxers del sistema si li passes el context adequat. Per tant, cal vigilar amb quines dades es passen al model.

**Conclusio**: Ollama es un runtime, no un aillador. Si vols aillament, has de posar Ollama dins un contenidor Docker (curiosament, es una opcio valida al BernatLab).

---

## Pregunta 12 (oberta): RPi vs Mac M2

**Resposta model**:

Les diferencies son abismals:

**Velocitat**: un model 7B en una RPi 4 pot trigar 30-60 segons a generar un paràgraf. En un Mac M2, el mateix model pot generar 50-100 tokens per segon (uns 5-10 paràgrafs per minut). Es una diferencia de 10-30x.

**Capacitat de model**: a la RPi 4 amb 4 GB, el maxim model viable es de 3-4B en Q4. Al Mac M2 amb 16-32 GB de RAM unificada, pots correr models de 13-30B amb bona qualitat. Si tens 64 GB, fins i tot 70B quantitzat.

**Consum electric**: la RPi consumeix 5-10W. El Mac M2 consumeix 20-40W en carrega. Si el model treballa 24/7, la diferència de factura es notable al llarg de l'any (uns 50-100 kWh/any).

**Implicacio al BernatLab**: on allotjar el model?
- Si nomes necessites respostes ocasionals: Mac personal quan l'uses.
- Si vols un servei 24/7 per a alertes i consultes: RPi amb model petit o servidor dedicat amb model mes gran.
- Si vols el millor dels dos mons: Mac per a tasques pesades, RPi per a tasques continues i urgents.

La regla practica: allotja el model on passaras el 80% del temps d'us. Si el 80% sera a la RPi, optimitza per a RPi. Si sera al Mac, idem.

---

## Pregunta 13 (oberta): RPi 4 amb 4 GB i model 7B

**Resposta model**:

Si intentes carregar un model de 7B (uns 4-5 GB en Q4) a una RPi 4 amb 4 GB de RAM, el sistema pot:

1. **Usar swap agressivament**: Linux pot moure parts de la memoria a la microSD/SSD. Es funcional pero MOLT lent, perque la microSD es 100x mes lenta que la RAM.

2. **OOM kill**: el kernel Linux pot matar processos per alliberar memoria. Si el sistema mata Ollama, el model es descarrega. Si mata un altre servei (InfluxDB, Grafana), tens una incidencia greu.

3. **Sistema inestable**: amb la RAM al limit, tot va lent. Les aplicacions poden trigar 10 segons a respondre a interaccions basiques.

**Solucions**:
- **Triar un model mes petit**: el `llama3.2:3b` (2.5 GB) es el maxim recomanable per a 4 GB. Si necessites mes qualitat, baixa a `phi3:mini` o `gemma2:2b`.
- **Augmentar swap**: pots afegir un fitxer de swap de 4-8 GB. Es lent, pero permet que el sistema no mati processos.
- **Servidor extern**: si necessites un 7B, considera un servidor cloud amb GPU. Costa diners pero funciona.
- **Quantitzar mes**: alguns models tenen variants Q3 o Q2 que ocupen menys pero perden qualitat.

La millor opcio al BernatLab: quedar-se amb el 3B. La diferencia amb el 7B es notable, pero no compensa el risc d'inestabilitat.

---

## Pregunta 14 (oberta): Directori de models

**Resposta model**:

El directori `/usr/share/ollama/.ollama` es on Ollama emmagatzema tots els models descarregats. Dins hi trobaras:

- `models/blobs/`: els fitxers binaris amb els pesos del model. Son els fitxers grans (GB).
- `models/manifests/`: metadades sobre cada model (versio, configuracio, hash dels blobs).
- `logs/`: els logs del servei (util per troubleshooting).

**Que passa si es queda sense espai**? Els nous `ollama pull` fallaran amb un error de disc ple. Pitjor encara: si el sistema de fitxers queda al 100%, Linux pot tenir comportaments erratics (logs que no escriuen, aplicacions que fallen, etc.).

**Com gestionar-ho al BernatLab** (microSD de 32 GB):
- Controla l'us de disc amb `du -sh /usr/share/ollama/.ollama`.
- Esborra els models que no usis: `ollama rm nom-model`.
- Mou els models a un disc extern amb la variable `OLLAMA_MODELS=/mnt/external/models`.
- Monitora amb una alerta de Prometheus: `disk_used_percent > 80%`.

Una bona politica: tenir sempre un 20% del disc lliure. Si tens 32 GB, no deixis que l'us de models superi els ~6-8 GB.

---

## Pregunta 15 (oberta): Systemd vs Docker al BernatLab

**Resposta model**:

Despres de considerar-ho, **la meva eleccio es Ollama com a servei systemd** al BernatLab. Argumento a continuacio.

**Arguments a favor de systemd**:
- **Rendiment**: Ollama en systemd te acces directe al hardware (CPU, RAM, GPU si escau). En Docker, hi ha una capa d'aillament que pot penalitzar el rendiment un 5-10%.
- **Simplicitat**: nomes una instal·lacio nativa, un servei. No cal gestionar un contenidor, els seus volums, ni la seva xarxa.
- **Menys overhead**: la RPi 4 es modesta. Cada contenidor extra es memoria que podria anar al model.
- **Boot automatic**: si la RPi es reinicia, systemd inicia Ollama automaticament. Docker pot trigar mes a estar llest.

**Arguments a favor de Docker**:
- **Aillament**: si Ollama es comporta malament, no afecta la resta del sistema.
- **Portabilitat**: puc moure el contenidor a una altra maquina facilment.
- **Coherencia**: la resta del BernatLab ja esta en contenidors (InfluxDB, Grafana, Mosquitto). Tot igual.
- **Versions**: puc especificar exactament quina versio d'Ollama vull al Dockerfile.

**Tria final**: systemd, perquè el rendiment i la simplicitat son prioritaris en una maquina amb recursos limitats. Si tingues un servidor mes potent, usaria Docker per coherencia amb la resta. Al BernatLab, Ollama es l'unic servei que NO te sentit en contenidor: consumeix massa del hardware i no es beneficia de l'aillament (les dades que processa son locals de tota manera).

---

## Que fer si has fallat moltes preguntes

- **10-12 encerts**: repassa la seccio del resum sobre instal·lacio i ports.
- **7-9 encerts**: fes l'exercici practic Pas 1-3 i torna-ho a provar.
- **0-6 encerts**: comença per instal·lar Ollama i fer la primera pregunta per terminal. Aprendre fent es el millor cami.

## Que fer si has encertat totes

- Passa al **Capitol 3** (triar model adequat).
- O investiga com muntar un Open WebUI per tenir una interficie grafica.
- O prova un model especialitzat: `ollama pull codellama:7b` per generar codi.
