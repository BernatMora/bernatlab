# Exercici practic - Capitol 6: Seguretat de contenidors

> 30-45 min · Real al teu sistema

## Objectiu

Practicar les principals mesures de seguretat per a contenidors Docker: usuari no-root, capacitat minima, read-only filesystem, escaner de vulnerabilitats i seccomp. Acabaras veient com n'ets de vulnerable amb la configuracio per defecte.

## Requisits

- Docker instal·lat a la RPi
- 30-45 minuts

## Pas 1: Comprova la configuracio per defecte (5 min)

```bash
# Mira quin usuari te per defecte un contenidor
docker run --rm alpine id
# Retorna uid=0(root) gid=0(root) groups=0(root)

# Comprova les capabilities per defecte
docker run --rm --security-opt no-new-privileges alpine \
  grep CapEff /proc/self/status
# Retorna un numero llarg; si poses --cap-drop=ALL abans, el numero sera 0

# Comprova si pot muntar el sistema de fitxers
docker run --rm alpine sh -c "mount | head -5"
```

## Pas 2: Contraste: contenidor insegur vs segur (15 min)

### Contenidor INSEGUR (tot per defecte)

```bash
# Conte tot: root, totes les capabilities, escrivible
docker run -d --name nextcloud-insecure \
  -v ~/test-insecure:/var/www/html \
  nextcloud

# Comprova qui soc
docker exec nextcloud-insecure id
# uid=0(root)

# Puc tocar el sistema de fitxers de l'amfitrio?
docker exec nextcloud-insecure sh -c "echo 'pwned' > /root/pwned.txt"
docker exec nextcloud-insecure cat /root/pwned.txt
# Si soc root dins, soc root tambe a la carpeta muntada
# Puc fer qualsevol cosa!

# Neteja
docker stop nextcloud-insecure
docker rm nextcloud-insecure
rm -rf ~/test-insecure
```

### Contenidor SEGUR (amb mesures)

```bash
# Conte mesures de seguretat
docker run -d --name nextcloud-secure \
  --user 33:33 \
  --read-only \
  --cap-drop=ALL \
  --security-opt=no-new-privileges \
  --tmpfs /tmp:rw,noexec,nosuid \
  -v ~/test-secure:/var/www/html \
  nextcloud

# Comprova qui soc
docker exec nextcloud-secure id
# uid=33(www-data) gid=33(www-data) - no soc root!

# Puc escriure al sistema de fitxers del contenidor?
docker exec nextcloud-secure sh -c "echo 'test' > /etc/test.txt"
# Hauria de fallar: read-only filesystem

# Puc muntar el sistema de fitxers de l'amfitrio?
docker exec nextcloud-secure mount
# Hauria de fallar o donar molt poca informacio

# Puc fer ping (capabilitat de xarxa)?
docker exec nextcloud-secure ping -c 1 8.8.8.8
# Hauria de funcionar (la capabilitat de xarxa es necessaria)

# Puc obtenir nous privilegis?
docker exec nextcloud-secure sh -c "su -"
# Hauria de fallar: no-new-privileges activat

# Neteja
docker stop nextcloud-secure
docker rm nextcloud-secure
rm -rf ~/test-secure
```

## Pas 3: Escaneig de vulnerabilitats (10 min)

```bash
# Activa el plugin docker scan
# (pot ser que ja estigui activat)
docker scan --version

# Escaneja una imatge popular
docker scan nginx:alpine

# Escaneja la teva pròpia imatge (si en tens)
docker scan bernatlab:1.0 || true

# Mira les vulnerabilitats per severitat
docker scan nginx:alpine --json | head -100
```

Alternativa sense Docker (utilitzant Trivy, mes potent):

```bash
# Instal·la Trivy
sudo apt install -y wget apt-transport-https gnupg
wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | gpg --dearmor | sudo tee /usr/share/keyrings/trivy.gpg > /dev/null
echo "deb [signed-by=/usr/share/keyrings/trivy.gpg] https://aquasecurity.github.io/trivy-repo/deb generic main" | sudo tee /etc/apt/sources.list.d/trivy.list
sudo apt update
sudo apt install -y trivy

# Escaneja
trivy image nginx:alpine

# Escaneja nomes vulnerabilitats critiques
trivy image --severity HIGH,CRITICAL nginx:alpine

# Escaneja un sistema de fitxers
trivy fs ~/un-projecte
```

## Pas 4: Prova seccomp (5 min)

```bash
# Per defecte, Docker ja aplica un perfil seccomp
# Per veure quin:
docker run --rm alpine sh -c "grep Seccomp /proc/self/status"
# Hauria de dir Seccomp: 2 (mode filter)

# Prova una syscall prohibida
docker run --rm alpine sh -c "kmod list"
# Pot fallar si kmod es considera perillosa

# Desactiva seccomp per comparar
docker run --rm --security-opt seccomp=unconfined alpine sh -c "kmod list"
# Hauria de funcionar

# Aplicar un perfil seccomp personalitzat (avançat)
# Cal un fitxer .json amb les syscalls permeses
# Aixo es per a casos molt específics
```

## Pas 5: Auditar la teva configuracio actual (5 min)

```bash
# Llista els teus contenidors actius
docker ps

# Comprova les opcions de seguretat de cada un
for c in $(docker ps -q); do
  echo "=== $c ==="
  docker inspect $c --format 'User: {{.Config.User}}
ReadonlyRootfs: {{.HostConfig.ReadonlyRootfs}}
Privileged: {{.HostConfig.Privileged}}
CapAdd: {{.HostConfig.CapAdd}}
CapDrop: {{.HostConfig.CapDrop}}
SecurityOpt: {{.HostConfig.SecurityOpt}}'
done

# Quins son root?
docker ps -q | xargs -I {} docker inspect {} --format '{{.Name}}: user={{.Config.User}}' | grep -v "user=$" | grep -v "user=0:0" || true
```

## Pas 6: Neteja

```bash
# Assegura't que no queda res
docker ps -a
docker system df
```

## Validacio

Has acabat si:

- [ ] Has vist la diferencia entre un contenidor root i un de no-root.
- [ ] Has comprovat que un contenidor amb --read-only no pot escriure a /etc.
- [ ] Has vist com les capabilities per defecte son limitades.
- [ ] Has fet un escaneig de vulnerabilitats amb `docker scan` o `trivy`.
- [ ] Has comprovat que seccomp esta activat per defecte.
- [ ] Has auditat la teva configuracio actual.

## Per aprofundir

- Activa rootless Docker a la RPi (cal systemd i una mica de feina).
- Investiga AppArmor i SELinux, que son mecanismes similars a seccomp pero mes amplis.
- Configura Docker Bench Security (https://github.com/docker/docker-bench-security) que audita la teva configuracio.
- Llegeix sobre "Podman" com a alternativa rootless a Docker.
