# Respostes — Capitol 8: Sincronitzacio de fitxers

> Mira les respostes DESPRES d'haver fet el qüestionari.

## Pregunta 1: Protocol de Syncthing

**Resposta correcta**: TLS (Transport Layer Security).

**Explicacio**: Tota la comunicacio entre dispositius Syncthing va xifrada amb **TLS 1.2 o superior**, igual que HTTPS. Aixo garanteix que ningun pot interceptar les dades durant la transmissio. A mes a mes, Syncthing usa certificats per autenticar cada dispositiu (nomes es sincronitza amb dispositius explicitament acceptats).

---

## Pregunta 2: Syncthing vs Dropbox

**Resposta correcta**: Syncthing es P2P (peer-to-peer); Dropbox passa per un servidor central.

**Explicacio**: La diferencia fonamental es l'arquitectura:
- **Syncthing**: cada dispositiu es connecta directament als altres (P2P). No hi ha cap servidor central que emmagatzemi les teves dades. Si un dels teus dispositius cau, els altres continuen sincronitzant-se entre ells.
- **Dropbox**: tot passa pel servidor de Dropbox. Si el servidor cau, no pots sincronitzar res. I totes les teves dades son a Dropbox (que les pot veure si vol, tot i que estan xifrades en transit).

**Implicacio per a privacitat**: amb Syncthing, **ningun te les teves dades** sino tu. Amb Dropbox, **Dropbox te les teves dades** (encara que en teoria no hi mira). Per a dades sensibles, Syncthing es millor.

---

## Pregunta 3: Ordre rsync per sincronitzar local a remot

**Resposta correcta**: `rsync -av -e ssh origen/ usuari@host:/desti/`.

**Explicacio**: 
- `-a`: archive (preserva permisos, dates, etc.)
- `-v`: verbose
- `-e ssh`: usa SSH com a transport

L'ordre completa estableix una connexio SSH al servidor remot, i rsync transfereix nomes els fitxers nous o modificats a travas d'aquesta connexio segura. Exemple real:
```bash
rsync -av -e ssh /home/pi/bernatlab/hort/ pi@nas.local:/volume1/backups/hort/
```

---

## Pregunta 4: Port UI Syncthing

**Resposta correcta**: 8384.

**Explicacio**: La UI web de Syncthing escolta al port **8384** per defecte. Es pot canviar, pero 8384 es el port estandard. Al BernatLab l'he mapeig a `127.0.0.1:8384` per seguretat (nomes accesible via Tailscale o tunel SSH).

---

## Pregunta 5: Opcions -a de rsync

**Resposta correcta**: Archive: preserva permisos, dates, estructura.

**Explicacio**: `-a` (archive) es una combinacio de moltes opcions:
- `-r`: recursiu
- `-l`: copia enllaços simbolics
- `-p`: preserva permisos
- `-t`: preserva dates de modificacio
- `-g`: preserva grup
- `-o`: preserva propietari
- `-D`: preserva device files

En poques paraules: "vol tot igual que a l'origen". Es la opcio mes usada per fer backups.

---

## Pregunta 6: Avantatge de rsync

**Resposta correcta**: Nomes copia els fitxers nous o modificats (incremental).

**Explicacio**: rsync nomes transfereix les parts dels fitxers que realment han canviat. Si tens 50 GB i nomes has afegit 100 MB nous, nomes es copien 100 MB. Aixo es diferencia de `cp -r`, que copiaria tot de nou cada vegada. Per a copies grans o a travas de la xarxa, es una diferencia enorme en temps i ample de banda.

---

## Pregunta 7: Inconvenient de rsync

**Resposta correcta**: Es unidireccional (no sincronitza en dos sentits).

**Explicacio**: rsync nomes copia A -> B. Si vols B -> A, has de fer una altra ordre. I si el mateix fitxer canvia a A i B independentment, l'ultim que sincronitzis "guanya" (pot perdre canvis). Syncthing en canvi es bidireccional automatic i te deteccio de conflictes.

---

## Pregunta 8: Dry-run de rsync

**Resposta correcta**: `-n` / `--dry-run`.

**Explicacio**: L'opcio `-n` (o la versio llarga `--dry-run`) fa que rsync simuli el que faria pero sense fer cap canvi. Es molt util abans d'una sincronitzacio important per veure quins fitxers es modificarien o esborrarien. Per exemple:
```bash
rsync -avn --delete /origen/ /desti/
```
Mostra una llista de fitxers sense tocar res.

---

## Pregunta 9 (oberta): 50 GB de fotos del mobil

**Resposta model**:

Per sincronitzar 50 GB de fotos des d'un mobil Android al servidor, la meva recomanacio es **Syncthing**.

**Arguments a favor de Syncthing**:

1. **Continu**: Syncthing detecta quan fas una foto i la puja automaticament. No cal fer res.
2. **Multiplataforma**: te client nadiu a Android (F-Droid). Es configura un cop i ja esta.
3. **Sense limits**: Dropbox gratis nomes et dona 2 GB, Google Drive 15 GB pero es lent. Syncthing nomes te els limits del teu disc.
4. **Privacitat**: les fotos van xifrades directament al teu servidor, sense passar per cap nuvol.
5. **No consumeix dades del nuvol**: si tens tarifa movil limitada, no afecta (tot va per WiFi).

**Arguments a favor de rsync**:

1. **Mes simple**: rsync es una sola ordre, no cal mantenir un dimoni.
2. **Consumeix menys recursos**: rsync nomes s'executa quan tu vols, no esta sempre corrent.
3. **Molt rapid per a copies inicials**: rsync nomes copia el que ha canviat.

**Limitacions de Syncthing a la RPi**: Syncthing consumeix ~50-100 MB de RAM i una mica de CPU. Per a 50 GB, la sincronitzacio inicial pot trigar hores (depen de la xarxa). Pero despres es rapid.

**Conclusio**: per a 50 GB de fotos **personals** (no per compartir), **Syncthing es la millor opcio**. La comoditat de pujar automaticament compensa el cost de mantenir un dimoni.

**Alternativa**: si tens molt poques fotos o vols maxim control, rsync via USB + manual.

---

## Pregunta 10 (oberta): Negoci amb 3 PCs i 1 NAS

**Resposta model**:

Per a un petit negoci amb 3 PCs i 1 NAS, dissenyaria aquesta estrategia:

**Documents compartits (tothom hi accedeix)**: **Syncthing** o **Nextcloud** al NAS. Cada PC te el client. Els canvis es propaguen automaticament. Avantatge: edicio local (rapid), sincronitzacio automatica. Desavantatge: possibles conflictes si dos PCs editen el mateix fitxer.

**Backups (copies unidireccionals)**: **rsync via cron** al NAS. Cada PC fa un rsync nocturn dels seus directoris importants al NAS. Es unidireccional, segur (via SSH), i es pot automatitzar amb cron.

**Fotos de productes (pujada des dels movils)**: **Syncthing** als movils dels treballadors. Les fotos es pujen automaticament a una carpeta del NAS quan el mobil esta a la WiFi del negoci.

**Documents que nomes ha de veure una persona**: **Dropbox Business** o **Google Drive** (pagant). Es universal, funciona a qualsevol lloc, i es pot compartir facilment amb clients.

**Consideracions de rendiment**:
- NAS amb 2-4 GB de RAM per a 3 PCs es suficient.
- Connexio Gigabit Ethernet per evitar colls d'ampolla.
- SSDs al NAS si el volum es molt gran (millor que HDD per a molts fitxers petits).

**Cost aproximat**:
- NAS basico (Synology DS223, 2 bays): 250-350 € + 2 discos de 4 TB (~200 €) = ~500 €
- 3 llicencies Dropbox Business: 150 €/any
- Total inicial: ~500 €, despres 150 €/any

Alternativa mes economica: fer tot amb Syncthing i rsync al NAS, sense serveis externs. Cero cost adicional un cop tens el NAS.

**Conclusio**: la combinacio **Syncthing + rsync + NAS** es la mes potent, privada i economica per a un petit negoci. Els serveis al nuvol (Dropbox, Google) son una bona addicio per a clients externs, pero per a us intern no cal.

---

## Que fer si has fallat moltes preguntes

- **5-8 encerts**: Rellegir el resum.
- **3-4 encerts**: Rellegeix el capitol amb atencio, sobretot la seccio de rsync.
- **0-2 encerts**: Repassem junts el capitol. Es la base per a la sincronitzacio multi-dispositiu.

## Que fer si has encertat totes

- Passa al **Capitol 9** (privadesa i xifrat).
- O fes l'**exercici practic** amb Syncthing entre un PC real i la RPi.
