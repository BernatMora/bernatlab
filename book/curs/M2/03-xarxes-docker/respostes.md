# Respostes - Capitol 3: Xarxes Docker

> Mira les respostes DESPRES d'haver fet el qüestionari.

## Pregunta 1: Driver per defecte?

**Resposta correcta**: bridge.

**Explicacio**: Quan executes un contenidor sense especificar `--network`, Docker el posa a la xarxa `bridge` per defecte. Es la mes comuna i la que es crea automaticament.

---

## Pregunta 2: Crear xarxa?

**Resposta correcta**: `docker network create xarxa`.

**Explicacio**: Docker te una comanda `docker network` amb subcomandes (`create`, `ls`, `rm`, `inspect`, `connect`, `disconnect`). Es consistent amb `docker container`, `docker image`, `docker volume`.

---

## Pregunta 3: Per que xarxes custom?

**Resposta correcta**: Perque permeten resolucio DNS per nom entre contenidors.

**Explicacio**: A la xarxa bridge per defecte, els contenidors nomes es veuen per IP. A una xarxa bridge custom, Docker activa un DNS intern que resol noms de contenidors. Pots fer `ping db` i funciona.

---

## Pregunta 4: Que es `--network host`?

**Resposta correcta**: El contenidor comparteix la pila de xarxa de l'amfitrio.

**Explicacio**: En lloc d'aillar el contenidor amb la seva propia IP, aquest mode fa que el contenidor vegi directament les interficies de l'amfitrio. Si l'amfitrio te el port 80 lliure, el contenidor el pot fer servir directament.

---

## Pregunta 5: Quan `--network none`?

**Resposta correcta**: Per ailllar completament el contenidor de qualsevol xarxa.

**Explicacio**: Es un contenidor sense cap interficie de xarxa (nomes te loopback 127.0.0.1). Util per a tasques de proces, probes, o analisis de seguretat on vols zero acces a xarxa.

---

## Pregunta 6: Flag de port mapping?

**Resposta correcta**: `-p`.

**Explicacio**: La sintaxi es `-p HOST:CONTAINER` (ex. `-p 8080:80`). Pots especificar la IP: `-p 127.0.0.1:8080:80` per nomes escoltar a localhost. Es diferencia de `-P` (majuscula) que publica tots els ports exposats a ports aleatoris.

---

## Pregunta 7: Llistar xarxes?

**Resposta correcta**: `docker network ls`.

**Explicacio**: Com la resta de subcomandes Docker, segueix el patro `docker <recurso> ls`. Tambe pots fer `docker network list` (son sinonims).

---

## Pregunta 8: `docker network connect`?

**Resposta correcta**: Connecta un contenidor existent a la xarxa app-net.

**Explicacio**: Pots afegir un contenidor en execucio a una xarxa nova sense reiniciar-lo. Es molt util per reconfigurar serveis al vol. Inversa: `docker network disconnect`.

---

## Pregunta 9 (oberta): Port mapejat vs xarxa interna

**Resposta model**:

**Port mapejat amb `-p`** es per a trafic **des de fora** del sistema Docker. Quan executes `docker run -p 8080:80 nginx`, Docker configura una regla de NAT al sistema amfitrio: tot el que arriba al port 8080 de l'amfitrio (des del navegador, des d'un altre ordinador de la xarxa) es redirigit al port 80 del contenidor. Aixo obre el servei al mon exterior (o a la xarxa local, depen de la IP que escolta).

**Acces directe entre contenidors a la mateixa xarxa** es nomes per a comunicacio **interna**. Si dos contenidors son a la mateixa xarxa bridge custom, es poden parlar per IP o per nom (gracies al DNS automatic), pero **no cal** mapejar ports. Per exemple, un backend pot conectar a `postgres://db:5432` sense que el port 5432 estigui exposat a l'amfitrio.

Exemple al BernatLab: tinc una base de dades PostgreSQL. **No** mapejo el port 5432 amb `-p` perque no vull que sigui accessible des del navegador ni des d'un altre PC. En lloc d'aixo, creo una xarxa `xarxa-backend` i hi poso el PostgreSQL i el servei que l'usa. El servei conecta a `db:5432` directament, nomes dins la xarxa Docker. Si intento fer `psql -h raspberry.local -p 5432` desde el meu PC, **no** funciona, perque el port no esta exposat. 

Es bona practica: **mai exposis la base de dades amb `-p`**. Usa xarxes internes.

---

## Pregunta 10 (oberta): Segmentacio amb 3 serveis

**Resposta model**:

Necessitare **dues xarxes bridge custom**:

- `xarxa-frontend`: nomes accessible des de l'amfitrio (te port mapping)
- `xarxa-backend`: totalment interna, no exposada

```
[Internet/Navegador]
       ↓
   port 80/443
       ↓
   [frontend: nginx] ←→ xarxa-frontend ←→ [backend: node]
                                            ↓
                                       xarxa-backend
                                            ↓
                                         [db: postgres]
```

**Configuracio**:

1. **Xarxa `xarxa-backend`**: nomes accessible entre backend i db.
   - `db` nomes connectat a `xarxa-backend`
   - `backend` connectat a `xarxa-backend` (i nomes aquesta)
   - Comandos:
     ```bash
     docker network create xarxa-backend
     docker run -d --name db --network xarxa-backend -e POSTGRES_PASSWORD=secret postgres:16
     docker run -d --name backend --network xarxa-backend node
     ```

2. **Xarxa `xarxa-frontend`**: accessible des de l'exterior, pero nomes per al frontend.
   - `frontend` connectat a `xarxa-frontend` amb port mapping
   - Comandos:
     ```bash
     docker network create xarxa-frontend
     docker run -d --name frontend --network xarxa-frontend -p 80:80 nginx
     ```

3. **Connectar `backend` tambe a `xarxa-frontend`**: nomes ell, no la db.
   ```bash
   docker network connect xarxa-frontend backend
   ```

Ara:
- **Frontend** (nginx) rep trafic de fora, parla amb backend per xarxa-frontend.
- **Backend** (node) pot parlar amb db per xarxa-backend i amb frontend per xarxa-frontend.
- **DB** (postgres) nomes pot parlar amb backend (per xarxa-backend), mai amb frontend ni amb l'exterior.

**Verificacio**:
- `docker exec frontend ping db` -> falla ✓ (no comparteixen xarxa)
- `docker exec db ping frontend` -> falla ✓
- `docker exec backend ping db` -> funciona ✓
- `docker exec backend ping frontend` -> funciona ✓
- Navegador pot accedir a `http://raspberry.local` -> funciona ✓
- Navegador intenta accedir a `raspberry.local:5432` -> falla ✓ (db no exposada)

Aquesta es l'arquitectura minima correcta per a una app web amb base de dades. En Kubernetes es fa amb "Network Policies" i namespaces, pero el concepte es el mateix: segmentar i limitar qui pot parlar amb qui.

---

## Que fer si has fallat moltes preguntes

- **5-8 encerts**: Rellegir el resum i tornar a fer l'exercici.
- **3-4 encerts**: Refes el pas 4 (segmentacio) varies vegades fins que ho vegis clar.
- **0-2 encerts**: Repassem el capitol. Les xarxes son critiques.

## Que fer si has encertat totes

- Passa al **Capitol 4** (Compose avançat).
- Investiga el "Docker network drivers plugins" (Calico, Weave, Flannel).
- Mira com es gestiona xarxa en Docker Swarm.
