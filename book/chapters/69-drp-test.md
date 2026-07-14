# Capítol 69 — DRP: el dia que es crema tot

> *"Les còpies sense un pla de recuperació són diners al calaix. Aquest capítol és el pla."*

## 69.1 Què aprendràs

- Què és un DRP i per què és vital.
- Com fer un test real de recuperació.
- Quines decisions has pres abans del desastre.
- Com restaurar el sistema pas a pas.
- Què fer si el hardware falla.

## 69.2 Durada estimada

2-4 hores (comptant el test real).

## 69.3 Per què un test real

A la majoria d'homelabs, el DRP és un document que ningú ha provat mai. Això és perillós perquè:

- El document pot tenir errors.
- Pot ser obsolet.
- Pot no funcionar en la pràctica.

La solució és **fer un test real**, en un entorn segur, **abans** que passi el desastre de veritat.

En aquest capítol farem un test de restauració completa. **Apagaràs la Raspberry**, **borraràs la microSD**, i **la restauraràs** des de zero amb les còpies que tens.

Això et portarà 1-2 hores. Però et donarà la confiança que el teu sistema és recuperable.

## 69.4 Què necessites per al test

- Una **microSD de recanvi** (32-64 GB).
- Un **lector de microSD** USB.
- Un **PC** amb balenaEtcher o similar.
- La **còpia de seguretat de la microSD** (la del cap 60).
- Les **còpies de restic** (a un disc extern o al núvol).
- 1-2 hores de temps lliure.

## 69.5 Preparació: abans del test

1. **Assegura't que les còpies estan al dia**:
   ```bash
   restic -r ~/backups/bernatlab snapshots
   ```
   La còpia més recent ha de ser de fa menys de 24 h.

2. **Comprova la integritat de les còpies**:
   ```bash
   restic -r ~/backups/bernatlab check
   ```

3. **Tingues a mà la llista de serveis i les seves configuracions**:
   - `~/homelab/compose/`
   - `~/homelab/secrets/`
   - `~/homelab/data/`

4. **Documenta l'estat actual**:
   - Quins contenidors estan corrent?
   - Quines són les IPs?
   - Quins serveis són crítics?

5. **Avisa la família o la gent que depèn del sistema** que el sistema estarà inactiu durant 1-2 hores.

## 69.6 El test: pas a pas

### Pas 1: atura tots els serveis ordenadament

```bash
cd ~/homelab/compose
docker compose -f portainer.yml down
docker compose -f uptime-kuma.yml down
docker compose -f mqtt.yml down
docker compose -f influxdb.yml down
docker compose -f grafana.yml down
docker compose -f node-red.yml down
docker compose -f telegraf.yml down
docker compose -f prometheus.yml down
```

Així tanques tot netament. Si hi ha algun contenidor amb problema, pots forçar-lo:

```bash
docker stop $(docker ps -aq)
```

### Pas 2: apaga la Raspberry

```bash
sudo shutdown -h now
```

Espera 30 segons. La LED verda parpalleja 10 vegades i s'apaga.

### Pas 3: treu la microSD

Desendolla la RPi. Treu la microSD.

### Pas 4: simula la pèrdua total

Aquí ve la part interessant. Tens dues opcions:

**Opció A: destruir la microSD "dolenta" (recomanada)**.

Si tens una microSD de recanvi, fes servir aquesta per al test. La "dolenta" la guardes com a testimoni de la pèrdua.

**Opció B: formatar la microSD "dolenta"**.

Si vols reutilitzar-la:

Al teu PC amb lector de microSD:

- **Windows**: usa **SD Card Formatter** o l'eina de disc.
- **Mac**: `diskutil eraseDisk FAT32 NOOBS /dev/disk2` (canvia disk2 pel teu).
- **Linux**: `sudo mkfs.vfat -F 32 /dev/sdb1` (canvia sdb1 pel teu).

### Pas 5: flasheja la microSD amb la imatge de recuperació

Agafes la còpia de la microSD (la que vas fer al cap 60) i la flasheges a la nova microSD:

Al teu PC:

- **balenaEtcher**: selecciona la imatge, selecciona la microSD, flash.
- **Raspberry Pi Imager**: igual.

### Pas 6: inserir la microSD i arrencar

Insereix la nova microSD a la RPi, endolla-la, i engega-la.

La RPi hauria d'arrencar exactament com estava abans del test. Verifica:

- Tens accés per SSH?
- Tens xarxa?
- Tens les teves dades?

### Pas 7: comprovar serveis

```bash
docker ps
```

Tots els serveis haurien d'estar corrent. Si no, engega'ls:

```bash
cd ~/homelab/compose
for f in *.yml; do docker compose -f "$f" up -d; done
```

### Pas 8: verificar la integritat

Per a cada servei, comprova que funciona:

- Portainer: https://hortosona:9443
- Uptime Kuma: http://hortosona:3001
- Grafana: http://hortosona:3000
- Node-RED: http://hortosona:1880

Si tot funciona, **el test ha estat un èxit**.

### Pas 9: documentar el temps

Anota quant ha durat cada pas. Això t'ajudarà a calcular el teu RTO (Recovery Time Objective).

Exemple:

- Apagar serveis: 2 min
- Apagar Raspberry: 1 min
- Treure microSD: 1 min
- Flashejar imatge: 10 min
- Arrencar: 2 min
- Verificar serveis: 10 min
- **Total: 26 min**

Si el teu RTO és 4 h, estàs molt bé. Si trigues més, cal optimitzar.

## 69.7 Test alternatiu: restauració de dades amb restic

Aquest test és menys dramàtic però igual d'important. Simula que has esborrat un fitxer per error.

1. Esborra un fitxer qualsevol (no crític):
   ```bash
   rm ~/homelab/compose/test-file.txt
   ```

2. Troba'l a la còpia:
   ```bash
   restic -r ~/backups/bernatlab find test-file.txt
   ```

3. Restaura'l:
   ```bash
   restic -r ~/backups/bernatlab restore latest \
       --target /tmp/restored \
       --include /home/bernat/homelab/compose/test-file.txt
   ```

4. Comprova:
   ```bash
   cat /tmp/restored/home/bernat/homelab/compose/test-file.txt
   ```

Si funciona, les teves còpies són vàlides.

## 69.8 Què fer si el hardware falla

Si la RPi falla (cosa que passarà), tens opcions:

### Opció A: comprar una RPi nova

- Preu: 50-100 € (RPi 4 o 5).
- Restaurar la microSD antiga (si la RPi ha fallat però la microSD està bé).
- O flashejar una nova amb la imatge de còpia.

### Opció B: usar un mini PC

Si la RPi no està disponible, pots muntar el sistema en un mini PC amb Debian. La majoria de coses funcionaran igual.

### Opció C: usar el núvol temporalment

Si necessites el sistema actiu ràpidament, pots contractar un VPS i restaurar-hi les dades.

## 69.9 El DRP documentat

Un cop fet el test, documenta el DRP:

```markdown
# DRP del BernatLab

## RTO: 1 hora
## RPO: 24 hores (còpies diàries)

## Escenari 1: Fallada de la Raspberry

**Detecció**: Uptime Kuma, Telegram.
**Responsable**: Bernat.
**Temps de recuperació**: 30 min - 2 h.

Passes:
1. Identificar la fallada.
2. Si és de hardware, comprar Raspberry nova.
3. Flashejar la microSD amb la imatge de còpia.
4. Inserir a la Raspberry i arrencar.
5. Verificar que tots els serveis s'han reiniciat.
6. Verificar que les dades estan intactes (recollir una dada de test).

## Escenari 2: Pèrdua de dades

**Detecció**: Alerta o descoberta accidental.
**Responsable**: Bernat.
**Temps de recuperació**: 10-30 min.

Passes:
1. Identificar què s'ha perdut.
2. Buscar a les còpies de restic.
3. Restaurar amb `restic restore`.
4. Verificar que el fitxer és correcte.

## Escenari 3: Atac de seguretat

**Detecció**: Alerta de seguretat o comportament estrany.
**Responsable**: Bernat.
**Temps de recuperació**: 2-4 h.

Passes:
1. Aïllar la Raspberry de la xarxa.
2. Identificar el vector d'atac.
3. Restaurar des d'una còpia neta.
4. Rotar tots els secrets.
5. Investigar i documentar.

## Escenari 4: Desastre natural

**Detecció**: Pèrdua total del hardware.
**Responsable**: Bernat.
**Temps de recuperació**: 1-7 dies (depèn del hardware).

Passes:
1. Comprar hardware nou.
2. Restaurar des de còpia al núvol.
3. Reconfigurar segons el README.

## Recursos
- Còpies al núvol: b2:bernatlab-backups
- Imatges de microSD: a la caixa forta / NAS d'un familiar
- Codi i configuració: https://github.com/BernatMora/bernatlab
- Recovery codes Tailscale: a Bitwarden

## Última actualització
- 2026-07-09 per Bernat (després del primer test)
```

## 69.10 Què fer després del test

Si el test ha anat bé:

- Documenta'l.
- Desa la documentació al repo.
- Comparteix el DRP amb algú de confiança (la teva parella, un amic).

Si ha fallat:

- Identifica on ha fallat.
- Corregeix la documentació.
- Torna-ho a provar.
- No t'amoïnis — un DRP és un document viu.

## 69.11 Resum final del Mòdul 7

Acabes de completar el camí de tenir una Raspberry en una caixa a tenir un **sistema professional** d'IoT per a l'hort. Has après:

- A instal·lar i endureir una Raspberry Pi.
- A muntar una cadena de dades completa.
- A rebre alertes al mòbil.
- A monitorar tot el sistema.
- A reaccionar als incidents amb runbooks.
- A recuperar el sistema si passa el pitjor.

Això és molt. La majoria d'homelabs no arriben ni a la meitat d'això.

## 69.12 Què ve després

Ara tens un BernatLab funcional. Les possibles ampliacions són infinites:

- Més nodes LoRa.
- Nous sensors (vent, pluja, radiació solar).
- Càmera amb visió per computador.
- Més serveis (Nextcloud per a fitxers, Immich per a fotos, etc.).
- Domini propi i HTTPS.
- Un assistent d'IA local.

Tots aquests temes es poden convertir en futurs mòduls del llibre.

## 69.13 Agraïments

Si has arribat fins aquí, has après molt. Jo també he après escrivint-ho.

Aquest llibre és un document viu. Si trobes errors, si canvies alguna cosa al teu sistema, si tens una idea nova, torna a editar-lo. El coneixement només és útil si està actualitzat.

## 69.14 Exercicis pràctics

1. Fes una còpia de la microSD si no la tens.
2. Programa un test de DRP un dia que tinguis temps.
3. Documenta el test al `homelab/postmortems/`.
4. Escriu el DRP al `homelab/DRP.md`.
5. Comparteix-lo amb algú de confiança.
6. Repeteix el test cada 6 mesos.
