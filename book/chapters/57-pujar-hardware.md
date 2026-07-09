# Capítol 57 — Quan cal pujar de hardware: escenaris reals

> *"Creixer és sa. Estancar-se no. Però créixer bé requereix planificació."*

## 57.1 Senyals que cal pujar de hardware

Alguns senyals clars que la Raspberry ja no és prou:

- **CPU constantment al 80-90%** tot i no tenir pics.
- **Swap massa ple** sovint.
- **Disc ple** malgrat neteja regular.
- **Timeouts** a serveis web.
- **Contenidors que es reinicien** per manca de memòria.
- **Còpies lentes** que abans eren ràpides.
- **Múltiples usuaris concurrents** i el sistema no aguanta.

## 57.2 Quan és bona idea i quan no

**Bona idea pujar**:

- El sistema té **un paper real** (no és un experiment).
- La caiguda del servidor **té impacte** (pèrdua de dades, temps).
- Estàs **gastant més temps** mantenint el sistema que gaudint-lo.
- Has **assolit els límits** del hardware actual.

**No és bona idea pujar**:

- Per culpa d'**una mala configuració** que es pot millorar.
- Per **un sol servei** puntual que es pot optimitzar.
- Per **moda** o per tenir "el millor hardware".
- Sense **haver entès per què** el sistema actual no és prou.

## 57.3 Escenaris de pujada

### Escenari 1: més RAM

Si la Raspberry té 4 GB i te'n calen 8, la solució és comprar una Raspberry amb 8 GB. Però:

- 8 GB és el màxim de la Raspberry 4.
- Si necessites més, cal canviar de plataforma.

Alternativa: **afegir swap a una SSD**:

```bash
# Crear swap a una SSD
sudo fallocate -l 8G /mnt/ssd/swapfile
sudo chmod 600 /mnt/ssd/swapfile
sudo mkswap /mnt/ssd/swapfile
sudo swapon /mnt/ssd/swapfile
```

Això et dóna 8 GB extra de swap. No és tan ràpid com RAM, però ajuda.

### Escenari 2: més emmagatzematge

Si la microSD de 64 GB no és prou:

1. Afegir una **SSD USB** de 256 GB o més.
2. Moure els volums Docker a la SSD.
3. Usar la microSD només per al sistema.

Exemple de configuració a `docker-compose.yml`:

```yaml
volumes:
  grafana-data:
    driver_opts:
      type: none
      o: bind
      device: /mnt/ssd/grafana
```

### Escenari 3: més potència de CPU

Si la CPU no és prou, les opcions són:

- **Raspberry Pi 5**: 2-3x més potent que la 4.
- **Mini PC amb Intel N100**: 4-8x més potent.
- **Servidor dedicat**: car però professional.

### Escenari 4: alta disponibilitat

Si vols que el sistema no caigui mai:

- **Dues Raspberry** en failover (una activa, una standby).
- **Raspberry + cloud** (Raspberry activa, cloud com a backup).
- **Cluster de 3 Raspberry** amb replicació.

## 57.4 Comparació de plataformes

| Plataforma | Preu | RAM | CPU | Consum | Per a què |
|---|---|---|---|---|---|
| Raspberry Pi 4 (4GB) | 50 € | 4 GB | 4x ARM 1.8 GHz | 5W | Aprenentatge, projectes petits |
| Raspberry Pi 4 (8GB) | 75 € | 8 GB | 4x ARM 1.8 GHz | 5W | BernatLab actual |
| Raspberry Pi 5 (8GB) | 90 € | 8 GB | 4x ARM 2.4 GHz | 8W | Més serveis, Més rapidesa |
| Mini PC N100 | 200-300 € | 16 GB | 4x x86 3.4 GHz | 15-25W | Homelab seriós |
| Servidor dedicat | 500+ € | 32 GB+ | Xeon / EPYC | 100-300W | Empresa, virtualització |
| NAS Synology | 300+ € | 4-8 GB | ARM/x86 | 15-40W | Emmagatzematge + serveis |
| VPS al núvol | 5-50 €/mes | 1-16 GB | Variable | - | Sempre disponible, sense hardware |

## 57.5 Migrar a una Raspberry Pi 5

Quan la 4 no és prou, la 5 és el pas natural:

**Avantatges**:
- CPU 2-3x més ràpida.
- Suport oficial per a SSD NVMe.
- Més ample de banda USB.
- Més memòria cau.

**Inconvenients**:
- Requereix font d'alimentació USB-C de 27W.
- Alguns contenidors poden tenir problemes amb la nova arquitectura.
- És més cara.

**Procés de migració**:

1. Comprar la Pi 5.
2. Flashejar la microSD amb Raspberry Pi OS.
3. Instal·lar Docker, Tailscale, etc.
4. Restaurar la còpia de restic.
5. Reactivar els serveis.
6. Verificar que tot funciona.
7. Apagar la Pi 4 i posar-la com a backup.

## 57.6 Migrar a un Mini PC

Si la Raspberry ja no és prou, un mini PC és el pas següent:

**Avantatges**:
- Molta més potència.
- Suport per a molta RAM (fins a 64 GB).
- Suport per a múltiples discs.
- Compatibilitat amb programari x86 (més ampli).

**Inconvenients**:
- Més car.
- Consumeix més energia.
- Més soroll (ventiladors).

**Models recomanats**:
- Beelink Mini S12 (N100): 200 €, 16 GB RAM, 500 GB SSD.
- Intel NUC: 300-500 €.
- Lenovo ThinkCentre Tiny: 100-200 € (recondicionat).

## 57.7 Migrar al núvol

Per a alguns casos, el núvol és la millor opció:

**Avantatges**:
- Sense manteniment de hardware.
- Escalable.
- Accessible des de qualsevol lloc.
- Còpies automàtiques.

**Inconvenients**:
- Cost mensual.
- Dades fora de casa (privadesa).
- Depèn d'un proveïdor.

**Quan té sentit**:
- Quan vols alta disponibilitat.
- Quan no vols gestionar hardware.
- Quan el sistema és estrictament professional.

**Proveïdors**:
- Hetzner: 4 €/mes per un VPS bàsic.
- DigitalOcean: 6 $/mes.
- AWS Lightsail: 5 $/mes.
- Oracle Cloud: capa gratuïta generosa.

## 57.8 Estratègies híbrides

Pujar no és tot-o-res. Una estratègia híbrida:

- **Raspberry a casa**: serveis crítics, privats, dades locals.
- **VPS al núvol**: serveis públics, web, bot de Telegram.
- **Sincronització**: Tailscale uneix les dues parts.
- **Còpies**: el núvol rep còpies xifrades de la Raspberry.

Això et dona el millor dels dos mons.

## 57.9 Com planificar una migració

1. **Avaluar el sistema actual**:
   - Què funciona bé?
   - Què no funciona?
   - Quines són les limitacions?

2. **Definir els requisits**:
   - Quanta RAM necessito?
   - Quina CPU?
   - Quin emmagatzematge?

3. **Escollir la plataforma**:
   - Dins del pressupost?
   - Compleix els requisits?
   - Té el suport de la comunitat?

4. **Preparar la migració**:
   - Fer còpia completa.
   - Documentar l'estat actual.
   - Provar en un entorn separat.

5. **Migrar**:
   - En una finestra de manteniment.
   - Pas a pas.
   - Verificant cada pas.

6. **Verificar**:
   - Tots els serveis funcionen?
   - Les dades estan intactes?
   - El rendiment és l'esperat?

7. **Tancar l'antic sistema**:
   - Mantenir durant 1-2 setmanes com a backup.
   - Apagar quan tot està estable.

## 57.10 Cost total de propietat

No miris només el preu d'entrada. Considera:

- **Hardware**: preu del dispositiu.
- **Energia**: cost anual d'electricitat.
- **Manteniment**: temps dedicat.
- **Substitució**: cada 5-7 anys.
- **Còpies**: emmagatzematge extra al núvol.
- **Domini i DNS**: 10-15 €/any.

Exemple:

- Raspberry 4 4GB: 50 € + 5W × 24h × 365 × 0,15 €/kWh = 6,57 €/any.
- Mini PC: 250 € + 20W × 24h × 365 × 0,15 €/kWh = 26,28 €/any.
- VPS: 60 €/any.

A 5 anys, el mini PC costa 380 €, el VPS 300 €, la Raspberry 83 € + el teu temps.

## 57.11 Quan NO pujar

De vegades, la solució no és pujar de hardware:

- **Millor la configuració**: sovint es pot optimitzar.
- **Reduir serveis**: menys serveis = menys recursos.
- **Moure al núvol**: pot ser més barat.
- **Acceptar els límits**: si el sistema funciona per al que el necessites, està bé.

## 57.12 Hardware específic recomanat

Per al BernatLab actual i futur:

- **SSD USB 3.0 de 500 GB** (Kingston A400, Samsung T7): ~50 €.
- **MicroSD A2 de 64 GB** (SanDisk Extreme): ~15 €.
- **Font d'alimentació oficial** de Raspberry: ~10 €.
- **Carcassa amb ventilador**: ~10-20 €.
- **Cables Ethernet Cat 6**: ~5-10 €/u.

Si escales:

- **Raspberry Pi 5 8 GB**: ~90 €.
- **Mini PC Intel N100**: ~250-350 €.
- **SSD NVMe 1 TB**: ~80 €.

## 57.13 Cicle de vida del hardware

- **Raspberry Pi 4**: llançada 2019, suportada fins ~2030.
- **Raspberry Pi 5**: llançada 2023, suportada fins ~2034.
- **Mini PC**: depèn del model, 5-7 anys.
- **Servidors dedicats**: 5-10 anys amb manteniment.
- **VPS**: sense vida física, però el proveïdor pot tancar.

## 57.14 On posar el hardware

Si canvies a un mini PC:

- **Habitació amb temperatura estable** (no golfes ni garatge).
- **Ventilació adequada**.
- **Protecció contra pols**.
- **UPS** (Sistema d'alimentació ininterrompuda) per a talls de llum.
- **Protecció contra sobretensions** (regleta amb protecció).

Un mini PC pot ser al costat del router, a la sala d'estar, o al despatx. Silenciós i petit.

## 57.15 Resum

Pujar de hardware és una decisió que s'ha de prendre amb temps. Avalua els requisits, planifica la migració, i no tinguis por de mantenir la Raspberry més temps del que toca. Al proper mòdul veurem com implementar el domini propi i la web.

## 57.16 Exercicis pràctics

1. Monitora el sistema actual durant una setmana. Identifica colls d'ampolla.
2. Calcula el cost total de propietat de la teva Raspberry.
3. Escriu un document d'avaluació: "Quan puc necessitar pujar de hardware?"
4. Compara 2-3 opcions de hardware per al futur.
5. Documenta un pla de migració pas a pas.
6. Fes una llista de "què emportar" si canvies de plataforma.
7. Estableix una data límit per revisar el rendiment.
