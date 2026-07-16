# Resum - Capitol 10: Orquestracio

## La idea clau

Quan tens un sol servidor (la RPi del BernatLab), **no necessites orquestracio**. Docker Compose en te prou. Pero quan tens varis servidors o vols alta disponibilitat, balanceig de carrega, rolling updates, etc., cal una eina d'orquestracio. Les dues mes populars son **Docker Swarm** i **Kubernetes**.

## Que es l'orquestracio

L'orquestracio es la gestio automatitzada de contenidors en **multiples maquines**. Un orquestrador s'encarrega de:

- **Desplegar** contenidors en el node mes adequat.
- **Escalar** (afegir mes instancies si hi ha mes carrega).
- **Auto-healing** (reiniciar contenidors que fallen).
- **Rolling updates** (actualitzar sense temps d'inactivitat).
- **Service discovery** (trobar on son els serveis).
- **Load balancing** (repartir el tràfic entre instancies).
- **Networking entre nodes** (xarxa que travessa maquines).

## Quan necessites orquestracio

No ho necessitis si:

- Tens **un sol node** (una sola RPi, un sol servidor).
- Tens **pocs serveis** (5-10 contenidors).
- Tens **baix tràfic** (<1000 peticions/segon).
- No et cal **alta disponibilitat** (pots tolerar caigudes puntuals).

Si tens tot aixo, **Docker Compose en te prou**.

Ho necessites si:

- Tens **multiples servidors** (3-5 RPi en cluster, o mes).
- Necessites **alta disponibilitat** (un node pot caure sense afectar el servei).
- Tens **molts serveis** (20-50 contenidors o mes).
- Necessites **escalar** automaticament.
- Treballes en un **entorn productiu** amb mes usuaris.

## Docker Swarm: la opcio "facil"

Docker Swarm es el mode Swarm de Docker. **Ja esta integrat a Docker**: nomes cal `docker swarm init`. Es la opcio mes simple si ja coneixes Docker.

### Caracteristiques

- **Integrat a Docker**: no cal instal·lar res.
- **Declaratiu amb stacks**: `docker stack deploy -c compose.yml stack-name`.
- **Rolling updates nadius**: actualitza servei per servei.
- **Networking overlay**: xarxa que travessa nodes.
- **Secrets i configs**: integrats.
- **Simplicitat**: el pots aprendre en una tarda.

### Cas d'us: cluster de RPi

Imagina 3 RPi amb Docker Swarm:

```
[Manager]   <- gestiona el cluster
   |
   +-- [Worker 1]  <- executa els teus serveis
   |
   +-- [Worker 2]  <- executa els teus serveis
```

Si un worker cau, els seus serveis es rebalancegen automaticament als altres. El manager pot caure tambe, pero llavors perds el control (els workers continuen servint).

### Limitacions

- Menys potent que Kubernetes.
- Ecosistema mes petit.
- Si tens molts serveis (centenars), comenca a ser limitat.
- No te "operators" (controladors especialitzats).

## Kubernetes: la opcio "professional"

Kubernetes (K8s) es l'estandard de la industria. Creat per Google, ara es open source i el manté la CNCF. **Es mes complexe** pero es l'eina que fan servir la majoria d'empreses grans.

### Caracteristiques

- **Estandard de la industria**: el que sap tothom.
- **Molt potent**: rolling updates, auto-scaling, auto-healing, service mesh, etc.
- **Ecosistema gran**: milers d'eines, integracions, documentacio.
- **Multi-cloud**: pots correr K8s a AWS, GCP, Azure o on-prem.
- **Complex**: te una corba d'aprenentatge pronunciada.
- **Recursos intensius**: el minim raonable es 3-5 servidors, 8 GB RAM cada un.

### Cas d'us: empresa o homelab avançat

Kubernetes es ideal quan tens:
- Decenes o centenars de serveis.
- Necessites alta disponibilitat real.
- Tens un equip dedicat a mantenir-lo.
- Vols correr en multiples clouds.

### Alternatives a Kubernetes pur

Per a homelabs amb mes ganes que Swarm pero menys que Kubernetes:

- **K3s**: Kubernetes lleuger. Molt mes petit (~200 MB). Perfecte per a RPi.
- **K3d**: K3s en contenidors Docker. Pots tenir un cluster K8s nomes amb Docker.
- **microK8s**: de Canonical. Un snap que instal·la K8s.
- **Minikube**: per a desenvolupament local.

## Docker Swarm vs Kubernetes: comparativa

| Caracteristica | Docker Swarm | Kubernetes |
|---|---|---|
| **Dificultat** | Baixa (1 dia) | Alta (1 setmana) |
| **Recursos minims** | 1-2 nodes, 1 GB | 3-5 nodes, 4-8 GB |
| **Ecosistema** | Petit | Gegant |
| **Comunitat** | Petita | Enorme |
| **Cloud providers** | Limitats | Tots (GKE, EKS, AKS) |
| **Empreses que l'usen** | Poques | La majoria |
| **Estandard de la industria** | No | Si |
| **Adequat per homelab** | Si (petit) | Amb K3s |
| **Rolling updates** | Si | Si (mes sofisticat) |
| **Auto-scaling** | Limitat | Complet |
| **Helm charts** | No | Si (eina de packaging) |
| **Cost d'aprenentatge** | Baix | Alt |

## Quan usar cada un

### Docker Swarm

- Tens pocs servidors (2-5).
- Ja coneixes Docker.
- No vols complicar-te.
- Comences amb un homelab mes seriós.

### Kubernetes (o K3s)

- Tens mes de 5 servidors.
- Necessites alta disponibilitat.
- La teva empresa el fa servir (o vols aprendre per a la feina).
- Tens mes de 30 serveis.

### Sense orquestracio (Compose)

- Tens 1-2 servidors.
- Tens menys de 20 serveis.
- No et cal alta disponibilitat.
- **La majoria d'homelabs cauen aqui**.

## Exemple basic: Docker Swarm

```bash
# Inicialitzar un Swarm (en un node)
docker swarm init

# Afegir un altre node (executar al segon node)
docker swarm join --token <token> <ip>:2377

# Desplegar un stack (usant compose)
docker stack deploy -c docker-compose.yml bernatlab

# Veure serveis
docker service ls

# Escalar un servei
docker service scale bernatlab_web=5

# Rolling update
docker service update --image nginx:1.27 bernatlab_web
```

## Exemple basic: K3s (Kubernetes lleuger)

```bash
# Servidor
curl -sfL https://get.k3s.io | sh -

# Obtenir el token
sudo cat /var/lib/rancher/k3s/server/node-token

# Worker
curl -sfL https://get.k3s.io | K3S_URL=https://<server>:6443 \
  K3S_TOKEN=<token> sh -

# kubectl ja esta disponible
kubectl get nodes
kubectl apply -f deployment.yaml
```

## El cami al BernatLab

Si estas content amb el teu homelab actual (una sola RPi), **no et cal orquestracio**. Docker Compose es perfecte.

Si vols anar mes enlla i tenir alta disponibilitat al lab:

1. **Monta un cluster Swarm amb 3 RPi**. Es la opcio mes facil.
2. **Prova K3s**. Et dona Kubernetes real amb pocs recursos.
3. **Migra serveis individuals** al cluster, mantenint Compose per als serveis simples.
4. **Apren kubectl** si vols fer el salt a Kubernetes "professional".

Al BernatLab, el meu pla es:

- Mantenir la RPi principal amb Compose (serveis personals, base de dades).
- Muntar un cluster de 3 RPi amb K3s per a serveis que necessiten disponibilitat.
- Continuar aprenent Kubernetes poc a poc.

## Connexions amb altres capitols

- **M2 Cap 1** - Les imatges les pots construir un cop i desplegar-les a molts nodes.
- **M2 Cap 3** - Les xarxes overlay son la base de Swarm.
- **M2 Cap 5** - Els registres privats permeten que tots els nodes del cluster accedeixin a les imatges.
- **M2 Cap 7** - Les actualitzacions rolling son natives als orquestradors.
- **M2 Cap 9** - La monitoritzacio es fonamental en un cluster.
