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

## Que fer si has fallat moltes preguntes

- **5-8 encerts**: Rellegir el resum. L'orquestracio es un tema conceptual.
- **3-4 encerts**: Refes l'exercici. Practicar Swarm ajuda.
- **0-2 encerts**: Repassem. Es important entendre quan val la pena.

## Que fer si has encertat totes

- Felicitats! Has acabat el modul M2 complet.
- Monta un cluster Swarm de 3 RPi al BernatLab.
- O comenca a mirar el modul M3 (proper modul).
