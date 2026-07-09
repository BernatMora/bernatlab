# Capítol 50 — DRP: pla de recuperació davant desastres

> *"Les còpies sense un pla de recuperació són diners al calaix. Cal saber com recuperar-se."*

## 50.1 Què és un DRP

Un **DRP** (Disaster Recovery Plan, pla de recuperació davant desastres) és el document que defineix **com recuperar el sistema** després d'un desastre. Inclou:

- Tipus de desastres previstos.
- Procediments de recuperació pas a pas.
- Responsables.
- Temps objectiu de recuperació (RTO).
- Punt objectiu de recuperació (RPO).
- Recursos necessaris.
- Proves periòdiques.

## 50.2 RTO i RPO

Dues mètriques clau:

- **RTO** (Recovery Time Objective): quant temps pot estar el sistema caigut? Per exemple, 4 h.
- **RPO** (Recovery Point Objective): quantes dades podem perdre? Per exemple, 24 h (l'última còpia).

Per al BernatLab:

- **RTO**: 4-8 h. Pots tolerar un parell d'hores sense servei.
- **RPO**: 24 h. Còpies diàries amb restic. Si perds 24 h de dades, és acceptable.

Si necessites RTO de 5 minuts, cal **replicació en temps real** (molt car). Per a un homelab, 4-8 h és raonable.

## 50.3 Tipus de desastres

Tipus que cal preveure:

1. **Disc dur falla**. Més probable del que voldríem. La microSD falla.
2. **Raspberry robada o danyada**. Possible si està accessible.
3. **Tall de llum prolongat**. Més probable a la zona rural.
4. **Incendi, inundació, o desastre natural**. Improbable però devastador.
5. **Atac informàtic**. Possible si hi ha bretxa.
6. **Error humà**. Esborrament accidental, mala configuració.
7. **Actualització que falla**. De vegades passa.

## 50.4 El pla per al BernatLab

Defineixo un pla pas a pas per a cada desastre:

### Escenari 1: la microSD falla

**Símptomes**: la Raspberry no arrenca, dades corruptes.

**Recuperació**:

1. **Substituir la microSD** per una de nova (32 GB, classe A2).
2. **Descarregar la imatge** de Raspberry Pi OS Lite des de raspberrypi.com.
3. **Flashejar** amb Raspberry Pi Imager o balenaEtcher.
4. **Configurar la Wi-Fi** i SSH abans d'arrencar.
5. **Iniciar sessió** via SSH.
6. **Restaurar la còpia** de restic:

```bash
sudo apt install restic
restic -r /mnt/usb/backups/bernatlab restore latest \
    --target /home/bernat
```

7. **Reinstal·lar serveis** (Docker, Tailscale, etc.).
8. **Restaurar volums Docker** (InfluxDB, Grafana, etc.).
9. **Verificar** que tot funciona.

**Temps estimat**: 2-3 hores.

### Escenari 2: la Raspberry robada o cremada

**Recuperació**:

1. **Comprar una Raspberry nova** (o una de segona mà).
2. **Seguir els passos 2-9 de l'escenari 1**.
3. **Recuperar Tailscale** amb la clau d'autenticació.
4. **Recuperar la IP** (pot canviar si tens MagicDNS).

**Temps estimat**: 1-2 dies (esperant el hardware).

### Escenari 3: tall de llum prolongat

**Recuperació**:

1. **Esperar** que torni la llum.
2. **Si tens UPS**, la Raspberry continua funcionant. Verificar que no s'ha apagat.
3. **Si la Raspberry s'ha apagat**, simplement tornar a engegar.
4. **Verificar** que els serveis s'han reiniciat correctament.

**Temps estimat**: 5-15 min.

### Escenari 4: desastre natural (incendi)

**Recuperació**:

1. **Acceptar la pèrdua** de l'equip.
2. **Comprar nou hardware**.
3. **Restaurar des de còpies al núvol** (Backblaze, Wasabi, etc.).
4. **Reinstal·lar serveis**.

**Temps estimat**: 1-2 setmanes.

### Escenari 5: atac informàtic

**Recuperació**:

1. **Aïllar** la Raspberry de la xarxa.
2. **Restaurar des d'una còpia neta** (que sàpigues que no està compromesa).
3. **Canviar totes les contrasenyes**.
4. **Aplicar pegats** de seguretat.
5. **Verificar** que no queda rastre de l'atacant.

**Temps estimat**: 4-24 h.

## 50.5 Llista de coses a recuperar

Un **checklist** de recuperació:

- [ ] Còpia de restic del sistema.
- [ ] Còpia de les dades dels volums Docker.
- [ ] Còpia de les configuracions (`/etc`).
- [ ] Còpia de les claus SSH i Tailscale.
- [ ] Còpia dels secrets (`.env`).
- [ ] Còpia del repo del BernatLab.
- [ ] Llista de paquets instal·lats (`apt list --installed > packages.txt`).
- [ ] Documentació de la configuració de xarxa.
- [ ] Claus de Tailscale, 2FA, contrasenyes (a Bitwarden).
- [ ] Notes personals sobre configuracions específiques.

## 50.6 Com provar el DRP

**Un pla que no es prova, no funciona**. Cal practicar:

### Prova de taula (tabletop)

Assegut a la taula, simules un desastre i tries el procediment. Identifiques buits en el pla.

### Prova de recuperació

Un cop l'any, restaura el sistema en un hardware diferent (una Raspberry vella, un PC amb Debian, una màquina virtual). Això valida que:

- Les còpies funcionen.
- Els temps de recuperació són correctes.
- La documentació és completa.

### Prova de failover

Si tens redundància, prova a fer failover (canviar al sistema de backup). Això valida que el backup funciona realment.

## 50.7 Eines de recuperació

Tingues sempre a mà:

- Una **microSD** amb Raspberry Pi OS Lite pre-instal·lada.
- Un **disc USB** amb les còpies de restic/Borg.
- Un **ordinador portàtil** amb què puguis accedir a la Raspberry.
- Les **contrasenyes** a Bitwarden (no només a la memòria).
- La **documentació** impresa (un cop l'any) en paper, en un lloc segur.
- Una **còpia impresa** de les claus de Tailscale (recovery codes).

## 50.8 Redundància

Si vols un sistema que **no es pugui caure**, cal **redundància**:

- **Dues Raspberry** sincronitzades (una activa, una standby).
- **Un NAS** a casa amb còpies automàtiques.
- **Un servidor cloud** (VPS petit) per a serveis crítics.

Això és car i complicat. Per a un homelab, **una bona còpia al núvol** + **RTO de 4-8 h** és prou.

## 50.9 Documentació del DRP

Crea un fitxer `DRP.md` al repo amb:

- Tipus de desastres.
- Procediments pas a pas.
- Responsables (Bernat, en aquest cas).
- Contactes d'emergència.
- Recursos externs (cloud, suport, etc.).

Exemple breu:

```markdown
# Pla de Recuperació Davant Desastres (DRP) — BernatLab

## Responsables
- Tècnic principal: Bernat Mora
- Contacte d'emergència: [telèfon]
- Cloud: BernatMora a Backblaze B2

## RTO: 4-8 h
## RPO: 24 h

## Procediments

### Pèrdua de la Raspberry
1. Hardware nou: Raspberry Pi 4, microSD 32GB, font d'alimentació
2. Imatge: Raspberry Pi OS Lite 64-bit
3. Restaurar còpia de restic des de /mnt/usb/backups
4. Reinstal·lar serveis segons el llistat a README
5. Verificar amb Uptime Kuma

### Robatori / pèrdua total
1. Còpies a Backblaze B2
2. Còpies a NAS d'un familiar (configurat)
3. Hardware nou, restaurar igual que "pèrdua de Raspberry"

### Bretxa de seguretat
1. Veure runbook a SEGURETAT.md
2. Aïllar el sistema
3. Restaurar des de còpia neta
4. Rotar tots els secrets

## Recursos
- Còpies al núvol: b2:bernatlab-backups
- Recovery codes Tailscale: a Bitwarden
- Master key Bitwarden: a [adreça física]
```

## 50.10 Eines útils per al DRP

- **Restic / BorgBackup**: còpies (Cap 45).
- **Tailscale**: accés remot segur.
- **Ansible / NixOS / Docker Compose**: permeten reproduir el sistema fàcilment.
- **Bitwarden**: emmagatzematge segur de secrets.
- **Backblaze B2 / Wasabi**: còpia al núvol.
- **Notion / Obsidian**: documentació.
- **GitHub**: repositori de codi i documentació.

## 50.11 Errors habituals

**Error 1: còpies sense prova de restauració**.

Si mai has restaurat, no saps si funciona. Prova-ho.

**Error 2: còpies al mateix lloc**.

Si tens les còpies a la mateixa Raspberry que es pot cremar, no serveixen. Còpia al núvol sempre.

**Error 3: documentació obsoleta**.

Si el pla no reflecteix l'estat actual del sistema, no serveix. Mantén-lo actualitzat.

**Error 4: no practicar**.

Si no proves el pla regularment, no funcionarà quan calgui.

**Error 5: secrets al DRP**.

Si poses contrasenyes al DRP en text pla, són accessibles a tothom. Usa referències ("veure Bitwarden").

## 50.12 Resum

Un DRP ben fet és la diferència entre recuperar-se ràpid i perdre-ho tot. Identifica els possibles desastres, escriu procediments pas a pas, defineix RTO i RPO, i practica regularment. La combinació de còpies al núvol + runbooks clars + proves periòdiques és la millor garantia de continuïtat. Això tanca el Mòdul 5. En el Mòdul 6 veurem com mantenir tot això en marxa 24/7.

## 50.13 Exercicis pràctics

1. Inventaria tots els actius del BernatLab.
2. Defineix RTO i RPO raonables.
3. Escriu un DRP amb els escenaris principals.
4. Crea una còpia al núvol (Backblaze B2 o similar).
5. Fes una prova de restauració en un entorn de test.
6. Documenta el procediment de recuperació.
7. Crea una còpia impresa de les claus de recuperació.
8. Programa una revisió anual del DRP.
