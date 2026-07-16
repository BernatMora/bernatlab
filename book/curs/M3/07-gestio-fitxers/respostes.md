# Respostes — Capitol 7: Gestio de fitxers al BernatLab

> Mira les respostes DESPRES d'haver fet el qüestionari.

## Pregunta 1: Gestor de fitxers web simple

**Resposta correcta**: File Browser.

**Explicacio**: **File Browser** (filebrowser.org) es un gestor de fitxers web minimalista: una sola app que permet navegar, pujar, baixar, editar i esborrar fitxers des del navegador. Es perfecte per a servidors petits com una RPi. Ocupa molt poca RAM (~30 MB) i es configura en 5 minuts.

---

## Pregunta 2: Nuvol personal complet

**Resposta correcta**: Nextcloud.

**Explicacio**: **Nextcloud** es un nuvol personal complet tipus Google Drive: gestio de fitxers, sincronitzacio multi-dispositiu, calendari, contactes, notes, documents colaboratius, galeria de fotos amb AI, etc. Es open source i pots auto-allotjar-lo al BernatLab. Pero consumeix mes recursos que File Browser (~500 MB de RAM per defecte).

---

## Pregunta 3: Permisos per a .env amb contrasenyes

**Resposta correcta**: 600.

**Explicacio**: Els fitxers `.env` contenen secrets (contrasenyes, tokens). Han de tenir permisos `600` (rw-------) perque nomes el propietari els pugui llegir. Si tens un altre usuari al sistema, no podra veure les teves contrasenyes. Es una bona practica de seguretat minima.

---

## Pregunta 4: Directori arrel recomanat

**Resposta correcta**: /home/pi/bernatlab.

**Explicacio**: `/home/pi/bernatlab/` es el directori arrel per a totes les dades al BernatLab. Es consistent (tots els serveis hi viuen), transparent (pots navegar amb `ls`), i facil de backupejar (un sol `tar` o `restic backup`). Alternatives com `/var/lib/...` son menys transparents i mes diffcils d'accedir.

---

## Pregunta 5: Avantatge principal de Nextcloud

**Resposta correcta**: Sincronitzacio multi-dispositiu i apps natives.

**Explicacio**: Nextcloud te **clients nadius** per a Windows, macOS, Linux, Android, iOS. Un cop configurat, els teus fitxers es sincronitzen automaticament entre tots els teus dispositius, igual que Google Drive o Dropbox. File Browser nomes es pot usar des del navegador, manualment.

---

## Pregunta 6: Protocol de sincronitzacio

**Resposta correcta**: WebDAV + API propia.

**Explicacio**: Nextcloud combina **WebDAV** (un protocol HTTP estandard per a gestio de fitxers) amb la seva **API propia** per a funcions mes avançades. Els clients natius usen l'API propia, pero altres eines compatibles amb WebDAV (com Cyberduck, WinSCP, o simplement mount en Linux) tambe funcionen.

---

## Pregunta 7: Format de data recomanat

**Resposta correcta**: ISO (YYYY-MM-DD).

**Explicacio**: El format **ISO 8601** (YYYY-MM-DD) es el mes robust perquè:
- Es **ordenable** alfabeticament (2025-06-15 ve abans que 2025-06-16).
- Es **universal** (no confon 06-07-2025 amb 07-06-2025).
- Es **parseable** per scripts i eines.

Alternatives com DD-MM-YYYY o MM/DD/YYYY porten errors de confusio internacional. Al BernatLab sempre uso ISO.

---

## Pregunta 8: Inconvenient de Nextcloud a RPi

**Resposta correcta**: Consumeix bastanta RAM.

**Explicacio**: Nextcloud consumeix ~500 MB - 1 GB de RAM per defecte (PHP-FPM + base de dades + serveix fitxers). En una RPi 4 amb 4 GB de RAM, queda poc espai per a la resta de serveis. File Browser en canvi nomes consumeix ~30 MB. Si tens molts serveis, pensa-ho.

---

## Pregunta 9 (oberta): Estructura de carpetes per a l'hort

**Resposta model**:

Per a un hort amb 5 bancals i 3 sensors per bancal, dissenyaria aquesta estructura:

```
/home/pi/bernatlab/hort/
├── README.md                      # Descripcio general
├── media/                         # Fotos i videos
│   ├── 2025/
│   │   ├── 06-juny/
│   │   │   └── 2025-06-15_bancal-1_tall-tomaqueres.jpg
│   │   ├── 07-juliol/
│   │   └── ...
│   └── 2026/
├── data/                          # Dades estructurades
│   ├── bancals/                   # Un fitxer per bancal
│   │   ├── bancal-1.txt
│   │   ├── bancal-2.txt
│   │   └── ...
│   ├── sensors/                   # Lectures per data
│   │   ├── 2025-06-15.csv
│   │   ├── 2025-06-16.csv
│   │   └── ...
│   ├── plantes/                   # Inventari
│   │   └── plantes.json
│   └── collites/                  # Registre de collites
│       ├── 2025-06-15_collita.json
│       └── ...
├── docs/                          # Documentacio
│   ├── manuals/
│   ├── procediments/
│   └── actes/
├── config/                        # Configuracions
│   ├── sensors.json               # Quins sensors a quin bancal
│   ├── horarios.json              # Horaris de reg
│   └── plantacio.json             # Calendari de plantacio
└── logs/                          # Logs agregats
    ├── sensors.log
    └── reg.log
```

**Justificacio**:

- **`media/`** organitzat per **any/mes**: puc trobar rapidament les fotos del 15 de juny de 2025, i nomes veig les del mes actual.
- **`data/sensors/`** un fitxer **per dia**: cada dia es un CSV amb totes les lectures. Es pot obrir amb Excel/LibreOffice. Facil de fer backup.
- **`data/bancals/`** un fitxer per bancal: conte la historia del bancal (sembra, tractaments, collites).
- **`config/`** separat: les configuracions canvien sovint, i es poden versionar amb git.
- **Dates ISO als noms**: ordenables, universal, parseable.
- **Sense accents ni espais**: nomes lletres ASCII, guions i barres. Funciona a tot arreu.

---

## Pregunta 10 (oberta): File Browser o Nextcloud per a 200 GB de fotos?

**Resposta model**:

Per a un amic que vol sincronitzar **200 GB de fotos** entre **PC, mòbil i tablet**, la meva recomanacio es **Nextcloud**.

**Arguments a favor de Nextcloud**:

1. **Clients natius**: te apps per a Windows, macOS, Linux, Android, iOS. Un cop configurat, els fitxers es sincronitzen automaticament. L'usuari no ha de fer res.
2. **Sincronitzacio selectiva**: pot triar quines carpetes sincronitzar a cada dispositiu (per exemple, nomes les fotos del 2025 al mòbil per estalviar espai).
3. **Historial de versions**: si esborra una foto per error, pot recuperar-la de les versions antigues.
4. **Compartir facil**: pot generar un enllaç public per compartir una foto amb familia o amics.
5. **Galeria web**: pot veure totes les fotos des del navegador sense descarregar-les.
6. **Multi-usuari**: pot donar acces a la parella o fills amb el seu propi compte.
7. **App de fotos**: Nextcloud te reconeixement facial i categoritzacio automatica (encara que consumeix mes recursos).

**Arguments a favor de File Browser**:

1. **Mes lleuger**: nomes ~30 MB de RAM. Si la RPi te poca RAM, pot ser millor.
2. **Mes simple**: nomes cal accedir des del navegador.
3. **No cal configurar clients**: nomes navegador.

**Consideracions sobre els 200 GB**:

- La RPi 4 amb 4 GB de RAM pot gestionar Nextcloud amb 200 GB si nomes l'usa ell.
- Caldra un disc SSD extern per emmagatzemar les fotos (la SD de 32 GB no n'hi hauria prou).
- Backup: 200 GB son molts. Cal un pla de backup adequat (restic + Backblaze B2 seria uns 1,20 €/mes).
- Nextcloud indexa les fotos per a la galeria: pot trigar uns dies a indexar 200 GB la primera vegada.

**Conclusio**: per a 200 GB de fotos sincronitzats entre multiples dispositius, **Nextcloud es la opcio correcta**. File Browser es per a casos mes simples (un sol usuari, gestio manual).

---

## Que fer si has fallat moltes preguntes

- **5-8 encerts**: Rellegir el resum.
- **3-4 encerts**: Rellegeix el capitol amb atencio, sobretot les seccions d'instal·lacio.
- **0-2 encerts**: Repassem junts el capitol. Es fonamental per a la gestio de dades de l'hort.

## Que fer si has encertat totes

- Passa al **Capitol 8** (sincronitzacio).
- O fes l'**exercici practic** amb Nextcloud.
