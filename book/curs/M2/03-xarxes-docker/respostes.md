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

## Pregunta 11 (oberta): Per que Docker abstrau la xarxa

**Resposta model**:

Docker va triar crear una capa d'abstraccio de xarxa a sobre de les xarxes reals de Linux per varios motius:

1. **Portabilitat entre hosts**: la mateixa configuracio de xarxa funciona a qualsevol maquina Linux, Mac o Windows. Si Docker depengues de les interficies reals de l'amfitrio (`eth0`, `wlan0`), el `docker-compose.yml` canviaria entre maquines.

2. **Simplicitat per l'usuari**: en lloc de configurar `iptables`, `iptables-restore`, `ip link`, `ip addr`, etc., l'usuari nomes ha de fer `docker network create` i `docker network connect`. La complexitat queda amagada.

3. **Ailllament semantic**: cada xarxa Docker es un namespace de xarxa separat. Els contenidors d'una xarxa no veuen els de l'altra, tret que explicitament els connectis. Es equivalent a tenir VLANs pero sense configurar el switch.

4. **DNS integrat**: Docker提供一个 DNS intern que resol els noms dels contenidors. Pots fer `ping backend` i funciona. En xarxes natives Linux caldria configurar `dnsmasq` o `systemd-resolved`.

5. **Plugins extensibles**: si vols fer VLAN, VXLAN, o xarxa sobre Weave/Flannel, nomes cal canviar el driver. El API es el mateix.

Si no hi hagués aquesta abstraccio, configurar una app multi-contenidor seria com configurar maquines virtuals manualment: tedios i propens a errors.

---

## Pregunta 12 (oberta): Topologia de xarxes al BernatLab

**Resposta model**:

Al BernatLab amb 5 serveis (per exemple: Nextcloud, PostgreSQL, InfluxDB, Ollama, Uptime Kuma), crearia dues xarxes:

**Xarxa `frontend` (amb port mapping a l'amfitrio)**:
- Contenia nomes els serveis que necessiten accessible des de fora.
- Exemple: Nextcloud (port 8080), Uptime Kuma (port 3001).
- Aquesta xarxa te `external: true` o es la bridge per defecte per permetre el port mapping.

**Xarxa `backend` (interna, sense port mapping)**:
- Contenia els serveis que nomes es parlen entre ells.
- Exemple: PostgreSQL, InfluxDB, Ollama, el backend intern d'alguna API.
- Aquesta xarxa nomes es accessible des dels contenidors que hi son connectats.

**Avantatges**:
- Un Nextcloud public nomes pot parlar amb la base de dades si explicitament esta connectat a backend.
- Si un atacant compromet Nextcloud, nomes pot accedir a la base de dades (que nomes te dades de Nextcloud), no pas a InfluxDB o Ollama.
- Els serveis que no necessiten exposar-se (InfluxDB, Ollama) no son accessibles des de la xarxa publica.

**Graf mental**:
```
Internet -> [Xarxa frontend] -> Nextcloud, Uptime Kuma
                                      |
                                      v
                              [Xarxa backend]
                              /        |        \
                       PostgreSQL   InfluxDB   Ollama
```

Aquesta segmentacio es defensa en profunditat: encara que una capa falli, l'atacant queda confinat.

---

## Pregunta 13 (oberta): Quan `--network host` te sentit

**Resposta model**:

El mode `host` te avantatges i inconvenients clars. Li explicaria al company quan te sentit i quan no:

**Quan te sentit `--network host`**:

- **Eines de monitoritzacio que necessiten veure mes interficies**: per exemple, un exporter de Prometheus que ha de capturar trafic de multiples interficies virtuals (cas de cAdvisor o node-exporter).
- **Diagnostics de xarxa**: eines com `tcpdump` o `wireshark` dins un contenidor es beneficien de veure totes les interficies.
- **Aplicacions que necessiten "multicast" o "broadcast"**: alguns protocols antics assumeixen broadcast (NetBIOS, alguns sistemes legacy).
- **Casos de testbed on vols maxim rendiment**: sense el doble NAT del bridge, el rendiment es mes proper al natiu.

**Quan NO te sentit**:

- **Serveis accessibles des d'internet**: estrobes tota la xarxa de l'amfitrio. Un exploit al servei pot accedir a totes les interficies.
- **Multi-tenancy**: si dos serveis de clients diferents comparteixen el host, poden col·lisionar als ports.
- **Entorns de produccio normals**: el risc no compensa el benefici de rendiment (que es marginal en la majoria de casos).

**Al BernatLab**: el `--network host` es acceptable nomes per a eines de monitoritzacio internes (Uptime Kuma, cAdvisor). Mai per a serveis accessibles des de fora.

**Alternativa**: si necessites rendiment sense perdre ailllament, pots usar `--network host` nomes per al contenidor que ho necessita concretament, mantenint la resta en xarxes bridge.

---

## Pregunta 14 (oberta): Xarxes per al sistema Hort Osona

**Resposta model**:

Per al sistema Hort Osona amb Ollama, ChromaDB i Open WebUI, l'arquitectura de xarxes seria:

**Xarxa `hort-backend` (interna, sense port mapping)**:
- Contenia: Ollama, ChromaDB.
- Justificacio: aquests serveis son "interns". No cal que l'usuari accedeixi directament.
- ChromaDB nomes l'ha de veure Ollama. Ollama l'ha de veure Open WebUI. Per tant, ChromaDB nomes a la xarxa amb Ollama.

**Xarxa `hort-frontend` (amb port mapping)**:
- Contenia: Open WebUI.
- Justificacio: es la unica interficie visible per l'usuari.
- Port mapping: 8080:8080.

**Connexions**:
- Open WebUI esta connectat a `hort-frontend` (per ser accessible) i a `hort-backend` (per parlar amb Ollama).
- Ollama nomes a `hort-backend`. No cal que sigui accessible directament.
- ChromaDB nomes a `hort-backend`, nomes visible per Ollama.

**Risc si exposés ChromaDB a internet**: ChromaDB te una API que permet fer queries i, en versions antigudes, escriure. Si un atacant troba el port, podria:
1. Esborrar tota la base de coneixement.
2. Injectar documents maliciosos.
3. Fer denegacio de servei.

Per tant, ChromaDB ha d'estar nomes a la xarxa interna. Si realment cal accedir-hi des de fora (per debugging), fer-ho via un tunnel SSH, no pas exposant el port directament.

Aquesta es la configuracio minima correcta. A mes, es pot afegir una xarxa `hort-monitoring` per a Prometheus, pero nomes si cal.

---

## Pregunta 15 (oberta): Binding de ports i seguretat

**Resposta model**:

La diferencia entre `-p 0.0.0.0:80:80` i `-p 127.0.0.1:80:80` es critica per a la seguretat:

**Amb `-p 0.0.0.0:80:80`**:
- El port es accessible des de qualsevol interficie de xarxa de l'amfitrio.
- Si la RPi te una IP publica (100.115.134.76), el port es accessible directament des d'internet.
- Si nomes te IP local (192.168.1.x), el port es accessible des de tots els dispositius de la xarxa local.
- Atacants de fora (si la RPi es accesible) poden trobar el port amb un escaneig.

**Amb `-p 127.0.0.1:80:80`**:
- El port nomes es accessible des del propi amfitrio.
- Per accedir-hi des d'un altre dispositiu, cal un proxy invers (nginx, Caddy, Traefik) o un tunnel (SSH).
- Molt mes segur: nomes accesible per qui tingui acces a la maquina.

**Recomanacio al BernatLab**:

Si el BernatLab esta darrere d'un router amb port forwarding cap a 100.115.134.76, llavors el port ja es accessible des d'internet. Per tant, fer `-p 0.0.0.0` nomes agrega una capa de conveniencia (no cal proxy). Pero el servei queda exposat directament.

Si el BernatLab nomes l'uses via VPN (WireGuard, Tailscale), aleshores:
- Fes servir `-p 127.0.0.1` a tots els serveis.
- El port forwarding esta al router, pero nomes el tunnel VPN pot arribar al servei.
- Encara que algú trobi la IP publica, no pot accedir als serveis.

**Millor practica**: sempre `-p 127.0.0.1` + un reverse proxy (Caddy) que gestioni HTTPS, autenticacio i rate limiting. Mai exposar directament un servei sense proxy.

**Trade-off**: mes complexitat (el proxy) vs mes seguretat. Al BernatLab val la pena.

---

## Que fer si has fallat moltes preguntes

- **5-8 encerts**: Rellegir el resum i tornar a fer l'exercici.
- **3-4 encerts**: Refes el pas 4 (segmentacio) varies vegades fins que ho vegis clar.
- **0-2 encerts**: Repassem el capitol. Les xarxes son critiques.

## Que fer si has encertat totes

- Passa al **Capitol 4** (Compose avançat).
- Investiga el "Docker network drivers plugins" (Calico, Weave, Flannel).
- Mira com es gestiona xarxa en Docker Swarm.
