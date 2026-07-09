# Capítol 56 — Diagnòstic i troubleshooting 24/7

> *"El 80% dels problemes es resolen amb 5 comandes. L'objectiu és saber quines 5."*

## 56.1 El mètode general de diagnòstic

Quan alguna cosa falla, segueix aquest mètode:

1. **Identifica el problema**: què falla exactament? Què esperaves que passés?
2. **Recull informació**: què diuen els logs? Quines mètriques? Quins missatges d'error?
3. **Forma una hipòtesi**: quina és la causa més probable?
4. **Prova la hipòtesi**: un canvi segur per verificar.
5. **Si no funciona, torna al pas 2**.
6. **Si funciona, documenta** (runbook) i comparteix.

No saltar passos. No entrar en pànic. Mantenir la calma.

## 56.2 Les 10 comandes que salven

Quan tot falla, aquestes comandes et donen la informació que necessites:

### 1. `htop` o `top`

Veure què consumeix CPU/RAM.

```bash
htop
```

Què buscar:

- Processos consumint molt.
- Molts processos zombi.
- Swap ple.

### 2. `df -h`

Veure espai en disc.

```bash
df -h
```

Si una partició està al 100%, és el problema.

### 3. `du -sh /*`

Trobar què ocupa espai.

```bash
du -sh /* | sort -h
```

### 4. `free -h`

Veure memòria.

```bash
free -h
```

### 5. `ss -tulnp`

Veure quins ports escolten.

```bash
ss -tulnp
```

### 6. `journalctl -u servei`

Logs d'un servei específic.

```bash
journalctl -u sshd -n 100
```

### 7. `docker ps -a`

Estat de tots els contenidors.

```bash
docker ps -a
```

### 8. `docker logs contenidor`

Logs d'un contenidor.

```bash
docker logs grafana --tail 100
```

### 9. `tail -f /var/log/syslog`

Logs del sistema en temps real.

```bash
tail -f /var/log/syslog
```

### 10. `ip addr` o `ip route`

Configuració de xarxa.

```bash
ip addr
ip route
```

## 56.3 Problemes comuns i solucions

### Problema: contenidor reiniciant-se en bucle

**Símptoma**: `docker ps` mostra el contenidor com a "Restarting".

**Diagnòstic**:

```bash
docker logs <contenidor> --tail 50
```

Cerca errors. Sovint és un problema de:

- Configuració incorrecta.
- Volum no muntat.
- Dependència no disponible.

**Solució**: corregir l'error i tornar a engegar.

### Problema: el sistema està lent

**Diagnòstic**:

```bash
htop
iostat -x 1
free -h
```

**Causes comunes**:

- Un procés consumint massa CPU.
- Swap ple (RAM insuficient).
- Disc al 100% I/O.
- Xarxa saturada.

### Problema: "No space left on device"

**Diagnòstic**:

```bash
df -h
du -sh /var/lib/docker  # contenidors
du -sh /var/log          # logs
du -sh /tmp              # temporals
```

**Solució**:

```bash
docker system prune -a  # netejar Docker
find /var/log -name "*.gz" -delete
```

### Problema: servei inaccessible des de la xarxa

**Diagnòstic**:

```bash
ss -tulnp | grep <port>
curl http://localhost:<port>
```

Si local funciona però remot no:

```bash
# Comprovar Tailscale
tailscale status

# Comprovar tallafocs
sudo ufw status
sudo iptables -L -n

# Comprovar ACLs a Tailscale
```

### Problema: errors de permisos

**Diagnòstic**:

```bash
ls -la /path/fitxer
id
```

**Solució**:

```bash
sudo chown bernat:bernat /path/fitxer
sudo chmod 644 /path/fitxer
```

### Problema: la Raspberry no respon

**Diagnòstic**:

1. Comprovar llum LED: vermell fix = problema d'alimentació.
2. Comprovar temperatura: si està molt calenta, ventilació.
3. Provar amb un altre cable d'alimentació.
4. Connectar monitor + teclat.

Si cap funciona, és problema de hardware (substituir).

## 56.4 Eines avançades

### `strace`

Veure què fa exactament un procés:

```bash
strace -p <PID>
```

Útil quan un procés es queda penjat.

### `tcpdump`

Capturar tràfic de xarxa:

```bash
sudo tcpdump -i any -n port 1883
```

Útil per veure si els missatges MQTT arriben.

### `iotop`

Veure I/O de disc per procés:

```bash
sudo iotop
```

### `lsof`

Veure fitxers oberts per un procés:

```bash
sudo lsof -p <PID>
```

### `nethogs`

Veure tràfic de xarxa per procés:

```bash
sudo nethogs
```

## 56.5 Logs útils al BernatLab

- **/var/log/syslog**: sistema general.
- **/var/log/auth.log**: SSH, sudo.
- **/var/log/kern.log**: kernel.
- **/var/log/docker.log**: Docker daemon.
- **/var/log/fail2ban.log**: bloquejos.
- **/var/lib/docker/volumes/<volum>/_data/**: logs dins de contenidors.

## 56.6 El mètode de les 5 preguntes

Quan un problema sembla estrany, fes-te aquestes 5 preguntes:

1. **Què ha canviat recentment?** Sovint el problema ve d'un canvi.
2. **Què ha funcionat abans?** La configuració anterior és la base.
3. **Què és diferent ara?** Comparar l'estat anterior amb l'actual.
4. **Què passa si ho provo amb dades netes?** Sovint un estat net ho resol.
5. **Què passaria si fos un altre sistema?** Aïllar el problema.

## 56.7 Errors habituals en el diagnòstic

**Error 1: canviar moltes coses alhora**.

Si canvies 3 coses i es resol, no saps què ha funcionat. Canvia una cosa a la vegada.

**Error 2: no documentar el que ja has provat**.

Si proves 5 coses sense anotar, perds el temps repetint. Documenta cada intent.

**Error 3: assumir la causa massa ràpid**.

"És la memòria, segur". No, comprova-ho.

**Error 4: Google com a primera opció**.

Si no entens el problema, no busquis solucions. Enten-lo primer.

**Error 5: ignorar els logs**.

Els logs tenen la resposta. Llegeix-los abans de fer res.

## 56.8 Quan demanar ajuda

Si has provat tot i no trobes la solució, és hora de demanar ajuda. Però prepara't bé:

1. **Descriu el problema** amb detall.
2. **Mostra els logs** rellevants.
3. **Mostra què has provat**.
4. **Mostra la configuració** (sense secrets).
5. **Dona context**: quan va començar, què ha canviat.

Com pitjor estigui la descripció, pitjor serà l'ajuda que rebràs.

## 56.9 Post-mortem

Un cop resolt l'incident, escriu un **post-mortem** (un informe事后分析):

- **Què ha passat**: descripció.
- **Quin impacte ha tingut**: temps de caiguda, dades perdudes.
- **Quina ha estat la causa arrel**: per què ha passat.
- **Què hem fet per resoldre**: com ho hem arreglat.
- **Què farem per prevenir**: quins canvis apliquem.

Exemple:

```markdown
# Post-mortem: Tall de servei del 2026-07-05

## Què ha passat
El Grafana ha deixat de respondre durant 45 minuts entre les 14:00 i les 14:45.

## Impacte
- Usuaris no han pogut veure gràfiques.
- 0 dades perdudes (les dades estaven a InfluxDB, no a Grafana).

## Causa arrel
El contenidor Grafana ha omplert la partició /var. La causa: logs antics no rotats.

## Solució aplicada
- Netejar logs antics.
- Afegir logrotate.
- Configurar alerta quan /var > 80%.

## Prevenció
- Configurar `logrotate` per a Grafana.
- Moure els logs de Grafana a un volum separat.
- Afegir regla Prometheus: alerta si /var > 80%.
```

## 56.10 Documentació permanent

Un bon diagnòstic es converteix en:

- **Runbook** (Cap 55): si el problema es repeteix.
- **Post-mortem** (a `homelab/postmortems/`): si és greu.
- **Actualització del README**: si la solució canvia la configuració.
- **Alerta nova**: si vols prevenir-ho en el futur.

## 56.11 Resum

El diagnòstic és una habilitat que es millora amb la pràctica. Les 10 comandes bàsiques, el mètode general, els logs, i la calma són les eines. Documenta cada incident per aprendre'n. Al proper capítol veurem quan cal pujar de hardware i com planificar-ho.

## 56.12 Exercicis pràctics

1. Memoritza les 10 comandes bàsiques.
2. Prova cadascuna a la teva Raspberry.
3. Crea un "diccionari de problemes" amb els incidents que has tingut.
4. Escriu el teu primer post-mortem.
5. Configura `logrotate` per als serveis que ho necessitin.
6. Documenta al README les eines de diagnòstic instal·lades.
