# Respostes - Capitol 10: Orquestracio

> Mira les respostes DESPRES d'haver fet el qüestionari.

## Pregunta 1: Funcio orquestrador?

**Resposta correcta**: Gestionar automaticament contenidors en multiples maquines (desplegar, escalar, balancejar).

**Explicacio**: Un orquestrador automatitza totes les tasques que son tedioses o impossibles de fer a ma amb multiples servidors: desplegar, escalar, balancejar carrega, auto-healing, rolling updates. Es la gestio centralitzada d'un cluster de maquines.

---

## Pregunta 2: Orquestrador simple integrat a Docker?

**Resposta correcta**: Docker Swarm.

**Explicacio**: Swarm ve integrat a Docker. Nomes cal `docker swarm init` per començar. Es la opcio mes facil si ja coneixes Docker. Kubernetes cal instal·lar-lo separat (tot i que hi ha distribucions com K3s que ho simplifiquen).

---

## Pregunta 3: Estandard de la industria?

**Resposta correcta**: Kubernetes.

**Explicacio**: Kubernetes (K8s) es l'estandard de fet. Google el va crear, ara el manté la CNCF. Tots els cloud grans tenen serveis gestionats de K8s (EKS, GKE, AKS). Si treballes en IT, tard o d'hora topes amb K8s.

---

## Pregunta 4: K8s lleuger per a RPi?

**Resposta correcta**: K3s.

**Explicacio**: K3s es una distribuciu de Kubernetes creada per Rancher (ara SUSE). Es un sol binaris de ~200 MB, te menys dependencies, i esta optimitzat per a ARM (perfecte per a RPi). Manten la compatibilitat amb K8s standard.

---

## Pregunta 5: Quan no necessites orquestrador?

**Resposta correcta**: Quan tens un sol node i pocs serveis.

**Explicacio**: Si tens una sola maquina (la teva RPi) i menys de 20 serveis, Docker Compose es perfecte. Afegir un orquestrador es complicar-te la vida per res. L'orquestrador te sentit quan tens multiples maquines o vols alta disponibilitat.

---

## Pregunta 6: Alta disponibilitat?

**Resposta correcta**: Que un node pot caure sense que els serveis deixin de funcionar.

**Explicacio**: En un cluster amb alta disponibilitat, si un servidor cau (hardware, manteniment, etc.), els serveis es rebalancegen automaticament als altres nodes. L'usuari no nota res. Es la diferencia entre tenir un sol servidor (punt unic de fallada) i un cluster.

---

## Pregunta 7: Inconvenient de K8s?

**Resposta correcta**: Mes complex i mes recursos necessaris.

**Explicacio**: K8s te una corba d'aprenentatge pronunciada. El minim recomanable es 3 nodes amb 4-8 GB RAM cada un. A mes, hi ha molts conceptes nous (Pods, Services, Deployments, Namespaces, etc.). Swarm es molt mes simple: ja saps Docker.

---

## Pregunta 8: Minim RPi per Swarm?

**Resposta correcta**: 3 (1 manager + 2 workers).

**Explicacio**: Per tenir alta disponibilitat, necessites minim 3 nodes. Si tens nomes 2, quan un cau et queda un que pot ser el manager. Amb 3 pots perdre'n un i continuar. Per a proves en local pots fer-ho amb una sola maquina usant `docker swarm init` (no es HA pero funciona per practicar).

---

## Pregunta 9 (oberta): Compose vs orquestrador

**Resposta model**:

Son eines amb proposits diferents:

**Docker Compose** es una eina de **configuracio declarativa** per a un sol host. Tu escrius un `docker-compose.yml` amb els teus serveis, volums, xarxes, etc., i Docker els gestiona tots junts. Es perfecte per a desenvolupament i per a servidors individuals.

**Un orquestrador (Swarm, K8s)** es una eina de **gestio distribuida** per a multiples hosts. Pensa en ell com "Compose pero per a un cluster de maquines". Fa tot el que fa Compose pero afegint:
- Distribucio automatica de contenidors als nodes disponibles.
- Auto-healing: si un contenidor o node cau, es reemplaça.
- Rolling updates: actualitzar sense temps d'inactivitat.
- Service discovery: els serveis es troben automaticament.
- Load balancing: el tràfic es reparteix entre instancies.
- Secrets i configs centralitzats.

**Quan canviar**:

| Escenari | Eina |
|---|---|
| 1 RPi, 5-10 serveis, puc tolerar caigudes puntuals | **Compose** ✓ |
| 2-5 RPi, 10-20 serveis, vull HA basica | **Swarm** |
| 5+ RPi, 20+ serveis, alta disponibilitat estricta | **Kubernetes/K3s** |

Al BernatLab amb una sola RPi i 8 serveis, **Compose es perfecte**. Muntar un cluster Swarm o K3s nomes per tenir "alta disponibilitat" d'un Nextcloud personal es matar mosques a canonades. El temps i la complexitat no compensen.

Pero si tens **una base de dades critica**, com una botiga online o un servei que ha d'estar 24/7, llavors si. O si tens mes de 20-30 serveis, ja comences a necessitar eines d'orquestracio perque gestionar-los a ma es inviable.

La **transicio** sol ser:
1. Comences amb Compose en una sola maquina.
2. Quan tens 2-3 maquines, passes a Swarm.
3. Si la cosa creix molt, passes a K3s (o directament a un servei cloud de K8s).

No cal saltar-se passes.

---

## Pregunta 10 (oberta): HA al BernatLab

**Resposta model**:

Per a alta disponibilitat amb 3 RPi al BernatLab, les dues opcions son viables pero amb perfils molt diferents:

**Opcio A: Docker Swarm (3 RPi)**

- **Cost**: 3 RPi (3x ~55 € = 165 €) + 3 microSD (~3x10 € = 30 €) + switch PoE (~50 €) + fonts (~30 €). Total: ~275 €.
- **Complexitat**: baixa. Ja saps Docker, nomes cal aprendre `docker stack deploy`, `docker service`. En una tarda ho tens funcionant.
- **Recursos**: 3 RPi amb 1-2 GB de RAM cada una son suficients. Swarm es molt lleuger (apenes 50-100 MB de overhead).
- **Quan triar**:
  - Si vols **aprenentatge suau**.
  - Si tens **pocs serveis** (<20).
  - Si vols **menys manteniment** (Swarm es "set and forget").
- **Limitacions**: si vols coses mes sofisticades (Helm charts, Operators, service mesh), hauries de migrar a K8s igualment.

**Opcio B: K3s (3 RPi)**

- **Cost**: igual que Swarm (3 RPi + accessoris).
- **Complexitat**: mitjana. Has d'aprendre kubectl, yamls de K8s, conceptes nous (Pods, Services, Deployments, Namespaces). En una setmana tens la base.
- **Recursos**: K3s ocupa mes (300-500 MB per node). 3 RPi amb 2-4 GB de RAM son el minim recomanable.
- **Quan triar**:
  - Si vols **aprendre K8s de veritat** (util per a la feina).
  - Si tens **mes de 20-30 serveis** i necessites eines com Helm.
  - Si vols **monitoritzacio avanÃ§ada** (Prometheus Operator, etc.).
- **Limitacions**: mes complexe de mantenir. Si la versio de K8s canvia, has de migrar el cluster.

**Comparativa directa**:

| Aspecte | Swarm | K3s |
|---|---|---|
| **Aprenentatge** | 1 dia | 1 setmana |
| **Recursos per node** | 100 MB | 500 MB |
| **RAM minima per node** | 1 GB | 2 GB |
| **Serveis maxim practic** | 30-50 | 100+ |
| **Eines externes** | Poques | Helm, ArgoCD, etc. |
| **Replicacio al cloud** | Limitada | Nativa |
| **Comunitat** | Petita | Gegant |
| **Futur del projecte** | Manteniment | Actiu |
| **Adequat per a la RPi 4 de 4 GB** | Si | Just |

**La meva recomanacio**:

Si **no tens experiencia previa** amb orquestradors i vols fer aquest pas, comenca amb **Swarm**. Es mes simple, funciona be amb 3 RPi, i el pots aprendre en una setmana. Si un dia necessites mes potencia, migrar a K3s es relativament senzill (els conceptes son similars pero mes sofisticats).

Si **ja tens experiencia amb K8s** o vols **aprendre K8s per la feina**, salta directament a **K3s**. K3s et dona Kubernetes "real" amb molt pocs recursos. A mes, el que aprenguis es directament transferable a un K8s professional.

Al BernatLab concretament, amb 8 serveis i una sola RPi, **no recomanaria** muntar cap cluster ara. Es millor optimitzar el que tens (backups, monitoritzacio, seguretat) i quan tinguis mes serveis o necessitats reals d'alta disponibilitat, llavors plantes el cluster.

---

## Pregunta 11 (oberta): Per que Kubernetes ha esdevingut l'estandard

**Resposta model**:

Kubernetes ha esdevingut l'estandard de la industria tot i la seva complexitat per varies raons:

**1. Ecosistema enorme**:

Kubernetes te milers d'eines integrades que resolen problemes comuns:
- **Helm**: gestor de paquets (com `apt` per a K8s). Permet instal·lar aplicacions complexes amb un sol `helm install`.
- **ArgoCD / Flux**: GitOps. Desplegaments automatic desde Git.
- **Istio / Linkerd**: service mesh. Seguretat, observabilitat, trafic entre serveis.
- **Prometheus operator**: metricques pre-configurades.
- **cert-manager**: certificats TLS automatics.
- **Ingress controllers**: nginx, Traefik gestionats per K8s.

Aquest ecosistema fa que puguessis muntar qualsevol cosa amb un parell de `helm install`. Swarm no te res semblant.

**2. Portabilitat real**:

Un manifest de Kubernetes funciona a AWS, GCP, Azure, DigitalOcean, on-premises, etc. Aquesta portabilitat es invaluable per a empreses que volen evitar vendor lock-in. Swarm nomes funciona a Docker (tot i que K3s es K8s lleuger).

**3. Comunitat i人才**:

Hi ha mes gent que sap Kubernetes que Swarm. Si busques un enginyer, es mes facil trobar-ne un que conegui K8s. Les empreses ho saben i demanen K8s.

**4. Treball i carrera**:

Aprendre K8s es una inversio en la teva carrera profesional. Aprendre Swarm es interessant pero no te el mateix valor al mercat laboral.

**5. Casos d'us que K8s resol be**:

- Desplegaments multi-cloud.
- Centenars o milers de serveis.
- Equips grans amb desplegaments frequents.
- Necessitat de service mesh, autoscaling sofisticat.

**Pero Swarm tambe te els seus casos**:

- Petits clusters (3-10 nodes).
- Equips petits que ja coneixen Docker.
- Simplicitat com a prioritat.
- Homelabs.

**Al BernatLab**: K8s es overkill. Pero si vols invertir temps en una tecnologia amb retorn profesional, K3s es una bona opcio per a homelab.

---

## Pregunta 12 (oberta): Cost economic vs disponibilitat

**Resposta model**:

Comprar 2 RPi mes per tenir alta disponibilitat es una decisio economica i tecnica. Fem el calcul:

**Cost economic**:

- 2 RPi 4 (4 GB): ~120 EUR
- 2 fonts d'alimentacio: ~30 EUR
- 2 microSD o SSD: ~40 EUR
- 1 switch adicional: ~30 EUR
- Total: ~220 EUR

**Cost de temps**:

- Muntar el cluster: 4-8 h (primer cop).
- Aprendre Swarm o K3s: 10-20 h.
- Manteniment continu: 2-4 h/mes.
- Troubleshooting quan algo falla: variable.

**Benefici**:

- Alta disponibilitat: si una RPi falla, els serveis continuen.
- Temps de caiguda reduit: d'hores a segons.

**Analisi cost-benefici**:

Si el BernatLab es personal i la caiguda et costa 1 hora de feina a la setmana (reconfigurar, esperar, etc.), el cost de la caiguda es ~50 h/any. Aixo son 2 setmanes de feina. Val la pena invertir 220 EUR + 30 h de setup?

Si el BernatLab es per a negoci o per a serveis que usen altres, el calcul canvia. Si una caiguda et costa 100 EUR en perdua de clients o reputacio, al cap de 2 caigudes ja has amortitzat.

**Alternatives mes economiques**:

1. **Standby manual**: una RPi de recanvi apagada. Si la principal falla, l'arrenques. Cost: 60 EUR + 0 h/mes.
2. **Backup agressiu +恢复 rapid**: invertir en backups i en documentar el proces de恢复. Si la RPi falla, en 1 hora tens tot funcionant en una maquina nova. Cost: 0 EUR + 4 h de setup.
3. **Watchdog hardware**: un Watchdog USB que reinicia la RPi si penja. Cost: 20 EUR. Resol la majoria de fallades de software.

**Recomanacio al BernatLab**:

Si tens temps limitat i vols practicitat, comença per:
1. Backups verificats (Restic al núvol + test de恢复 trimestral).
2. Monitoritzacio amb alertes (Uptime Kuma + Telegram).
3. Watchdog hardware per a reinicis automatic.

Aixo et dona el 80% del benefici d'un cluster amb el 10% del cost.

**Si vols el 100%**: compra les 2 RPi i munta Swarm. Pero asumeix el cost de temps de manteniment.

---

## Pregunta 13 (oberta): K8s al BernatLab es sobredimensionat

**Resposta model**:

Si un company em diu "vull posar K8s al BernatLab perque queda professional", li explicaria per que es una mala idea:

**1. K8s esta dissenyat per a mes de 3 nodes**:

Kubernetes assumeix que tens un cluster. La unitat minima es 1 control plane + 2 workers (3 nodes). Menys de 3 nodes, K8s te problemes (quorum, alta disponibilitat del control plane).

**2. La complexitat operativva es brutal**:

K8s nomes per començar:
- 1 control plane (que pot ser un sol node en K3s, pero igual cal).
- Components basics: `kubelet`, `kube-proxy`, `etcd`, `coredns`, `ingress-nginx`, `cert-manager`, etc.
- Conceptes: Pods, Deployments, Services, Ingress, ConfigMaps, Secrets, Namespaces, RBAC, Network Policies, etc.
- Aprenentatge: 2-4 setmanes per a una persona tecnica.

**3. El overhead de memoria**:

K3s en una sola RPi ja consumeix ~500 MB nomes per al control plane. Si tens una RPi 4 de 4 GB, et queda 3.5 GB per als serveis. Aixo son 1-2 serveis. Per a un homelab de 10 serveis, no es viable sense mes RAM.

**4. La "professionalitat" no ve de la tecnologia**:

Un homelab ben gestionat amb Docker Compose es **molt mes professional** que un K8s mal muntat:
- Backups verificats.
- Monitoritzacio amb alertes.
- Seguretat aplicada correctament.
- Documentacio.
- Tests de恢复.

K8s es una eina, no una finalitat. Si la teva maquina no pot mantenir K8s, no es professional.

**5. Alternatives adequades al BernatLab**:

| Necessitat | Solucio adequada |
|---|---|
| Un sol node, 5-10 serveis | Docker Compose |
| 3-5 nodes, vols auto-healing | Docker Swarm |
| Vols K8s pero amb pocs recursos | K3s amb 1-2 nodes |
| Vols aprendre K8s "de veritat" | K3s amb 3+ nodes |
| Alta disponibilitat real | K8s amb 3+ control planes |

**Recomanacio honesta**:

Si el teu objectiu es **aprendre K8s per la feina**, munta un cluster K3s amb 3 RPi al BernatLab. Es la millor manera d'aprendre.

Si el teu objectiu es **tenir un homelab que funcioni**, queda't amb Docker Compose. No hi ha vergonya en fer servir l'eina correcta per la feina.

**La regla**: no escullis la tecnologia mes moderna o impressionant. Escullis la que resol el teu problema amb el minim overhead.

---

## Pregunta 14 (oberta): Solucio progressiva per alta disponibilitat

**Resposta model**:

Per a un servei web (Nextcloud) que vols disponible 24/7 al BernatLab, una solucio progressiva podria ser:

**Nivell 1: Una sola RPi amb Docker Compose (situacio actual)**:

```yaml
# Caracteristiques:
- 1 RPi
- 8-10 serveis en Docker Compose
- Acceptacio de caigudes puntuals (1-2 cops/any)
- Recovery manual: 1-2 hores
```

**Avantatges**: simple, economic, rapid de mantenir.
**Inconvenients**: caigudes totals quan falla la RPi (1-3 cops/any per hardware o update problematic).

**Nivell 2: RPi principal + backup manual**:

```yaml
# Caracteristiques:
- 1 RPi principal amb tots els serveis
- 1 RPi secundaria apagada amb backup recent (rsync cada dia)
- Recovery: portar la secundaria a la xarxa, arrencar, restaurar
- Temps de恢复: 30-60 min
```

**Avantatges**: proteccio contra fallada total, economic (60 EUR extra).
**Inconvenients**: el恢复 es manual, hi ha perdua de dades desde l'ultim backup.

**Nivell 3: Cluster Swarm de 3 RPi**:

```yaml
# Caracteristiques:
- 3 RPi (1 manager + 2 workers)
- Serveis distribuits (replicacio 2x)
- Auto-healing: si un node cau, els contenidors es reinicien a un altre
- Temps de恢复: 30 segons (automatic)
```

**Avantatges**: alta disponibilitat real, auto-healing.
**Inconvenients**: cost (220 EUR), complexitat, replicacio de dades (cal GlusterFS, Ceph o similar).

**Nivell 4: Kubernetes (K3s) amb ingress i storage**:

```yaml
# Caracteristiques:
- 3-5 RPi amb K3s
- Ingress controller (Traefik)
- Persistent storage (Longhorn, Rook)
- Deployments amb rolling updates
- Auto-scaling
- Temps de恢复: segons, zero-downtime updates
```

**Avantatges**: maxima sofisticacio, professional,学べる。
**Inconvenients**: 500+ EUR en hardware, 50-100 h d'aprenentatge, manteniment continu.

**Recomanacio al BernatLab**:

- **Nivell 1-2**: si tens 1-2 RPi i temps limitat.
- **Nivell 3**: si tens 3 RPi i vols alta disponibilitat amb minima complexitat.
- **Nivell 4**: si vols aprendre K8s o tens un cas d'us real que ho justifiqui.

**Cada nivell te un cost economic i operatiu. No saltis al nivell 4 si el 1 et funciona.**

---

## Pregunta 15 (oberta): Complexitat vs productivitat

**Resposta model**:

Si el BernatLab es un projecte personal amb temps limitat (2-5 h/mes), la complexitat d'un orquestrador te un cost real en productivitat:

**Temps de manteniment estimat**:

| Stack | Setup inicial | Manteniment mensual | Troubleshooting |
|---|---|---|---|
| Docker Compose (1 node) | 4 h | 0-1 h | 0-1 h/mes |
| Docker Swarm (3 nodes) | 8-12 h | 1-2 h | 1-3 h/mes |
| K3s (3 nodes) | 20-40 h | 2-4 h | 2-6 h/mes |
| K8s complet (3+ nodes) | 80-200 h | 8-16 h | 5-20 h/mes |

**El dilema**:

Si tens 2 h/mes per al BernatLab:
- Docker Compose: tens temps per a experiments, millores, nous serveis.
- Swarm: nomes tens temps per a manteniment basic. Poca cosa mes.
- K3s: tot el temps se'n va en manteniment. No pots innovar.
- K8s: no tens prou temps. El sistema es degrada.

**La llei de la complexitat**:

> "Un sistema complexe que no entens s'acaba trencant. Un sistema simple que entens pot créixer."

Docker Compose es simple. Docker Swarm es moderadament complexe. K8s es molt complexe. La complexitat no es gratuita: cada hora invertida en entendre una eina es una hora que no pots dedicar a fer coses noves.

**Regla practica**:

Si el sistema no et causa problemes reals, no l'upgrade. Si nomes tens una RPi i funciona, queda't amb Docker Compose. Si comences a perdre serveis sovint, puja un nivell. Si tot va be, no facis res.

**Excepcions**:

- Si vols **aprendre** Kubernetes per la feina, val la pena el cost temporal.
- Si tens **un cas d'us real** (multi-cloud, molts serveis, equip gran), K8s es la resposta.

**Al BernatLab personal**, la majoria de gent no te cap d'aquestes excuses. Per tant, Docker Compose es la resposta correcta. Swarm nomes si tens 3+ RPi i temps. K8s nomes si tens un objectiu d'aprenentatge o de negoci clar.

**La trampa de l'over-engineering**:

Passar de Docker Compose a Swarm "per si de cas" es la trampa mes comuna. El "per si de cas" mai arriba, i mentre arriba has perdut hores en manteniment. Millor començar simple i pujar quan calgui.

**Conclusio honesta**: un homelab amb Docker Compose, bons backups, monitoritzacio minima i seguretat raonable es **molt mes profesional** que un K8s mal muntat. La tecnologia es l'eina, no l'objectiu.

---

## Que fer si has fallat moltes preguntes

- **5-8 encerts**: Rellegir el resum. L'orquestracio es un tema conceptual.
- **3-4 encerts**: Refes l'exercici. Practicar Swarm ajuda.
- **0-2 encerts**: Repassem. Es important entendre quan val la pena.

## Que fer si has encertat totes

- Felicitats! Has acabat el modul M2 complet.
- Monta un cluster Swarm de 3 RPi al BernatLab.
- O comenca a mirar el modul M3 (proper modul).
