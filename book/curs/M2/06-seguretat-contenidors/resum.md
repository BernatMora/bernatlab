# Resum - Capitol 6: Seguretat de contenidors

## La idea clau

Un contenidor Docker **no es un sandbox perfecte**. Per defecte, un contenidor te mes privilegis dels que necessita: s'executa com a root, te capabilities del kernel Linux, pot muntar sistemes de fitxers, etc. Si un atacant troba una vulnerabilitat, pot escapar. Aquest capitol es per entendre els riscos i aplicar mesures de **defensa en profunditat**.

## Defensa en profunditat

No n'hi ha prou amb una sola mesura. Cal combinar-ne varies perque si una falla, les altres protegeixen:

```
1. Imatge minima i actualitzada     <- no exposar vulnerabilitats conegudes
2. Usuari no-root                   <- minim d'impacte si es compromet
3. Capabilities minimes             <- no poder fer coses perilloses
4. Read-only filesystem             <- no poder persistir
5. Xarxa aillada                    <- minim de superficie d'atac
6. Limitar recursos (CPU, RAM)      <- evitar DoS
7. Sense privilegis                 <- no poder muntar el que vulguis
8. Seccomp / AppArmor               <- filtrar syscalls
```

## 1. Usuari no-root

Per defecte, Docker executa els contenidors com a **root** (UID 0). Si un atacant explota el contenidor, sera root a dins (tot i que aillat per namespaces).

```bash
# Definir-ho al run
docker run --user 1000:1000 meva-app

# O al Dockerfile
FROM python:3.12-slim
USER 1000  # executar com a UID 1000
```

L'UID 1000 es el que solen tenir els usuaris humans a Linux. Per a serveis web, sovint es 33:33 (www-data d'Apache/Nginx) o 999:999 (postgres).

**Truc important**: abans de `USER`, copia els fitxers i dona'ls-hi els permisos correctes:

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY --chown=1000:1000 . .  # important!
RUN pip install ...
USER 1000
CMD ["python", "app.py"]
```

## 2. Capabilities de Linux

Les **capabilities** son permisos especials que tradicionalment nomes te root (muntar sistemes de fitxers, carregar moduls del kernel, canviar la propietat de fitxers, etc.). Docker ja en treu moltes per defecte, pero pots ser mes estricte:

```bash
# Treure totes
docker run --cap-drop=ALL meva-app

# Treure totes pero afegir nomes les que necessites
docker run --cap-drop=ALL --cap-add=NET_BIND_SERVICE meva-app
# (NET_BIND_SERVICE permet enllaçar a ports <1024)
```

Una capacitat especial es `SYS_ADMIN`: es la que permet muntar, accedir a dispositius, etc. **Mai** la posis.

## 3. Read-only filesystem

El sistema de fitxers del contenidor es normalment escribible. Pots fer-lo nomes de lectura:

```bash
docker run --read-only meva-app
```

Aixi, el contenidor nomes pot escriure a volums muntats, tmpfs o la xarxa. Si un atacant intenta persistir (afegir un script malicios), no pot. 

Pero moltes apps necessiten escriure a /tmp. Solucio: muntar tmpfs:

```bash
docker run --read-only --tmpfs /tmp:rw,noexec,nosuid meva-app
```

`noexec` evita que s'hi executin binaris. `nosuid` evita bits SUID.

## 4. Mode privilegiat

Docker te un mode **privileged** que dona al contenidor quasi tots els privilegis de l'amfitrio:

```bash
docker run --privileged meva-app
# AIXO ES PERILLOS. NO HO FACIS MAI.
```

Aixo es nomes per a casos molt especials (Dockers dins Dockers, accedir a dispositius del hardware). Al 99.99% dels casos no el necessites.

## 5. Seccomp (secure computing mode)

Seccomp es un mecanisme del kernel Linux que **filtra les syscalls** que un proces pot fer. Docker ja l'aplica per defecte amb un perfil segur:

```bash
# Per defecte esta activat
docker run alpine grep Seccomp /proc/self/status
# Seccomp: 2 (mode filter)

# Desactivar (perill!)
docker run --security-opt seccomp=unconfined meva-app
```

A no ser que tinguis una raó molt especifica, deixa el seccomp per defecte.

## 6. No-new-privileges

Aquesta opcio evita que un procés dins el contenidor **adquireixi nous privilegis** (per exemple, amb `setuid`):

```bash
docker run --security-opt=no-new-privileges meva-app
```

Es una bona practica sempre. No te cap cost.

## 7. Xarxa aillada

Ho hem vist al capitol 3, pero es important recordar-ho: usa xarxes custom per a que els serveis nomes estiguin exposats on toca.

```yaml
# compose
services:
  nextcloud:
    networks: [frontend, backend]
  db:
    networks: [backend]  # nomes a backend!
```

## 8. Escaner de vulnerabilitats

Les imatges tenen llibreries amb vulnerabilitats conegudes (CVEs). Docker te una eina integrada:

```bash
# Activar el plugin
docker scan nginx:alpine
```

Alternativa mes potent: **Trivy**:

```bash
# Instal·lar
sudo apt install -y trivy

# Escanear
trivy image nginx:alpine
# Sortida: llista de vulnerabilitats amb severitat

# Nomes les critiques
trivy image --severity HIGH,CRITICAL nginx:alpine
```

Es bona practica escanejar les imatges regularment (o automaticament al CI/CD).

## 9. Limitar recursos

Un contenidor pot consumir tota la CPU/RAM de l'amfitrio si no el limites:

```bash
docker run --memory=512m --cpus=1.0 meva-app
```

Aixo evita que un contenidor compromes pugui fer un DoS a la resta de serveis.

## 10. Rootless Docker

L'opcio **mes segura**: executar el dimoni Docker sense root a l'amfitrio. Usa "user namespaces" per mapejar l'UID 0 del contenidor a un UID no privilegiat a l'amfitrio.

```bash
# Cal systemd i un parell de preparatius
sudo apt install -y uidmap dbus-user-session
dockerd-rootless-setuptool.sh install
```

Es mes complexe (alguns volums poden donar problemes), pero es la maxima seguretat.

## Resum: el "contenidor minim segur"

```bash
docker run -d \
  --name servei \
  --user 1000:1000 \
  --read-only \
  --cap-drop=ALL \
  --cap-add=NET_BIND_SERVICE \
  --security-opt=no-new-privileges \
  --tmpfs /tmp:rw,noexec,nosuid \
  --memory=512m \
  --cpus=1.0 \
  --network xarxa-aillada \
  meva-app:1.0
```

Aixo es el minim que hauries d'aplicar a tot. Si necessites mes seguretat, afegir AppArmor, SELinux, signatura d'imatges, etc.

## Connexions amb altres capitols

- **M2 Cap 1** - Les imatges minimes (alpine) redueixen la superficie d'atac.
- **M2 Cap 2** - Els volums encriptats son part de la seguretat.
- **M2 Cap 3** - Xarxes aillades es una mesura de seguretat.
- **M2 Cap 5** - Els registres privats eviten que les teves imatges siguin publiques.
- **M2 Cap 7** - Les actualitzacions son part de la seguretat (imatges noves = menys CVEs).
