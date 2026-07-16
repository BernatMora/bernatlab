# Exercici practic - Capitol 10: Orquestracio

> 30-45 min · Real al teu sistema

## Objectiu

Practicar amb un mini cluster Docker Swarm usant **nodes simulats** (contenidors que fan de workers) o comparant opcions. Tambe pots instal·lar K3s. Acabaras entenent quan val la pena l'orquestracio.

## Requisits

- Docker Compose instal·lat
- 30-45 minuts
- 1-2 GB de RAM lliure (per al mini cluster)
- (Opcional) Acces a 2-3 RPi fisiques per a un cluster real

## Pas 1: Inicialitza un Swarm d'un sol node (5 min)

En aquesta RPi pots crear un Swarm d'un sol node. No es un cluster "real" perque nomes te un node, pero et serveix per practicar les comandes.

```bash
# Inicialitza
docker swarm init

# Comprova
docker node ls
# Hauries de veure la teva maquina com a manager amb STATUS "Leader"

# Mira els tokens
docker swarm join-token manager
docker swarm join-token worker
```

## Pas 2: Desplega un servei amb Swarm (10 min)

Crea un directori:

```bash
mkdir -p ~/swarm-test
cd ~/swarm-test
```

Crea un `stack.yml`:

```yaml
version: "3.8"
services:
  web:
    image: nginx:alpine
    ports:
      - "8080:80"
    deploy:
      replicas: 3  # 3 instancies!
      update_config:
        parallelism: 1  # actualitza d'una en una
        delay: 10s
      restart_policy:
        condition: on-failure
    networks:
      - webnet

networks:
  webnet:
    driver: overlay
```

Desplega'l:

```bash
docker stack deploy -c stack.yml swarm-test

# Mira els serveis
docker service ls

# Mira les tasques (contenidors)
docker service ps swarm-test_web
# Hauries de veure 3 instancies

# Comprova que funcionen
curl http://localhost:8080

# Inspecciona el servei
docker service inspect swarm-test_web
```

## Pas 3: Escala el servei (5 min)

```bash
# Escalar a 5 instancies
docker service scale swarm-test_web=5

# Comprova
docker service ps swarm-test_web
# Hauries de veure 5 instancies

# Reduir a 2
docker service scale swarm-test_web=2
docker service ps swarm-test_web
```

## Pas 4: Rolling update (10 min)

```bash
# Fes un update a una nova versio de nginx
docker service update --image nginx:1.27-alpine swarm-test_web

# Mira el procés
docker service ps swarm-test_web
# Hauries de veure com les instancies es substitueixen una per una

# Comprova la nova versio
docker exec $(docker ps -q -f "name=swarm-test_web") nginx -v
```

## Pas 5: Auto-healing (5 min)

```bash
# Mira les instancies actuals
docker service ps swarm-test_web

# Mata una instancia manualment
CONTAINER=$(docker ps -q -f "name=swarm-test_web" | head -1)
docker rm -f $CONTAINER

# Espera 5 segons i mira què ha passat
sleep 5
docker service ps swarm-test_web
# Hauries de veure que Swarm ha tornat a arrencar la instancia
```

## Pas 6: Neteja el stack i surt del Swarm (5 min)

```bash
# Elimina el stack
docker stack rm swarm-test

# Surt del Swarm
docker swarm leave --force

# Comprova
docker node ls
# Error: This node is not part of a swarm
```

## Pas 7: Investiga K3s (opcional) (10 min)

K3s es Kubernetes lleuger. Es pot instal·lar amb una sola comanda:

```bash
# Instal·lar K3s
curl -sfL https://get.k3s.io | sh -

# Espera una mica
sleep 30

# Comprova
sudo kubectl get nodes

# Desplega un exemple
sudo kubectl create deployment nginx --image=nginx
sudo kubectl expose deployment nginx --port=80 --type=LoadBalancer
sudo kubectl get services

# Comprova
curl http://localhost

# Neteja
sudo kubectl delete service nginx
sudo kubectl delete deployment nginx

# Desinstal·la K3s (opcional)
/usr/local/bin/k3s-uninstall.sh
```

## Pas 8: Reflexio final (5 min)

Mira l'estat del teu BernatLab actual:

```bash
# Quants serveis tens?
docker ps --format "{{.Names}}"

# Quina memoria gasten?
docker stats --no-stream

# Tens una sola RPi o mes?
hostname
```

Pregunta't:
- Si un node cau, quants serveis queden afectats?
- Si la RPi es mor, què passa amb les teves dades?
- Quanta feina seria muntar un cluster Swarm o K3s?

Si nomes tens una RPi i uns 10 serveis, **Compose en te prou** i orquestrar es overkill. 

## Validacio

Has acabat si:

- [ ] Has inicialitzat i sortit d'un Swarm d'un sol node.
- [ ] Has desplegat un stack amb multiples replicas.
- [ ] Has vist com Swarm fa rolling updates i auto-healing.
- [ ] Has investigat K3s o has decidit que no el necessites ara.
- [ ] Has reflexionat sobre quan et cal orquestracio al BernatLab.

## Per aprofundir

- Munta un cluster Swarm de 3 RPi fisiques. Es el projecte mes divertit del curs.
- Investiga les plantilles Helm per a Kubernetes.
- Mira eines com Portainer que simplifiquen la gestio de Swarm i K8s.
- Compara el temps d'aprenentatge: Swarm (1 dia) vs K8s (1 setmana) vs K3s (2-3 dies).
