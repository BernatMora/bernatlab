# Resum — Capítol 2: La Raspberry Pi 4 per dins

## La idea clau

La Raspberry Pi 4 Model B és un **ordinador complet en una placa** del tamany d'una targeta de crèdit. Costa ~55 €, gasta 5-10 W, i té prou potència per a un servidor domèstic. El **BernatLab** en té una (4 GB de RAM) amb Debian 13 Lite i arquitectura arm64.

## Què és exactament?

- **SBC** (Single-Board Computer): tot en una placa — CPU, RAM, ports, xarxa.
- **4 GB de RAM LPDDR4** (la teva versió; n'hi ha de 1, 2, 4 i 8 GB).
- **CPU ARM Cortex-A72** (4 nuclis a 1.5 GHz, arquitectura arm64).
- **GPU VideoCore VI** (per a vídeo, no l'aprofitem al servidor).
- **MicroSD com a disc** (no té disc dur intern).
- **Sense ventilador** (disseny passiu, refrigeració per dissipador).

## La CPU ARM

ARM (Advanced RISC Machine) és una arquitectura de CPU diferent de la x86 (Intel/AMD). Característiques:

- **RISC** (Reduced Instruction Set Computer) — poques instruccions simples.
- **Eficient energèticament** — gasta molt menys que un PC x86.
- **arm64** (AArch64) — la versió de 64 bits.
- **No tots els programes x86 funcionen** — cal binari ARM o compilació creuada.

**A la pràctica**: per a servidors petits, ARM és perfecte. Per a jocs o edició de vídeo, x86 és millor.

## La RAM

- **4 GB LPDDR4** — la que tens.
- **Soldada a la placa** — no es pot ampliar.
- **Compartida amb la GPU** — per defecte 64 MB, es pot ajustar a 128-256 MB.

**Què hi cap?**: perfecte per a uns 5-10 contenidors Docker petits. Si vols Kubernetes o bases de dades grosses, et quedarà curta.

## La microSD

- **32 GB o més** — recomanat 32-64 GB classe A2.
- **Sistema operatiu** — Debian 13 Lite hi cap perfectament (~4 GB).
- **Dades** — millor no posar dades importants a la SD (es pot trencar).
- **Vida útil limitada** — les SD tenen ~10.000 cicles d'escriptura. Usa volums Docker per minimitzar escriptura.

**Alternatives**: disc SSD USB 3.0 (molt més ràpid i durable, ~30 €).

## Ports i connectivitat

| Port | Ús |
|---|---|
| **USB-C** | Alimentació (5V, 3A recomanat) |
| **2× USB 3.0 + 2× USB 2.0** | Perifèrics, disc SSD extern |
| **Ethernet Gigabit** | Xarxa cablejada (recomanable per a servidor) |
| **Wi-Fi 802.11ac** | Alternativa a Ethernet (menys estable) |
| **Bluetooth 5.0** | No l'aprofitem al servidor |
| **2× micro-HDMI** | Per connectar monitor (tampoc l'aprofitem) |
| **GPIO 40 pins** | Per a sensors IoT (el futur Hort Osona) |

## Temperatura i refrigeració

- **Sense càrrega**: ~45-50°C.
- **Amb càrrega moderada**: ~60-70°C.
- **Llindar tèrmic**: 80°C (la CPU redueix velocitat).
- **Crític**: 85°C (es pot danyar).

**Refrigeració recomanada**: dissipador d'alumini + ventilació. Si la teva RPi està en un armari tancat, vigila la temperatura.

**Comprovació**: `vcgencmd measure_temp` (no sempre disponible).

## Procés d'arrencada

```
1. Pre-boot (firmware)
   ↓
2. Bootloader (a la microSD)
   ↓
3. Kernel Linux (a la microSD)
   ↓
4. systemd (primer procés, PID 1)
   ↓
5. Serveis i contenidors Docker
```

- **Firmware**: xip EEPROM a la placa, no es toca.
- **Bootloader**: stub a la microSD, carrega el kernel.
- **Kernel**: nucli Linux compilat per a ARM.
- **systemd**: el "mestre de cerimònies" — arrenca tots els serveis.

## Per què Debian Lite?

- **Estable** — Debian té el cicle de release més estable del món Linux.
- **Sense entorn gràfic** — Lite = sense X11 ni GNOME. Estalvia ~300 MB de RAM i ~2 GB de disc.
- **Comunitat gran** — qualsevol problema té solució a Internet.
- **arm64 natiu** — paquets compilats específicament per a l'arquitectura.
- **Alternatives**: Raspberry Pi OS Lite, Ubuntu Server Lite. Debian és la meva tria per estabilitat.

## Connexions amb altres capítols

- **Cap 1** — Per què hem triat una RPi com a cor del BernatLab.
- **Cap 3** — Com administrar el sistema operatiu (Debian) que hi corre.
- **Cap 4** — La xarxa i SSH, que va per la interfície Ethernet/WiFi.
- **Cap 5** — Docker corre com un servei systemd sobre el sistema base.
- **Cap 22** — Com monitoritzar temperatura, ús de CPU/RAM, espai de disc.
- **Cap 47** — Seguretat física i networking de la RPi.
