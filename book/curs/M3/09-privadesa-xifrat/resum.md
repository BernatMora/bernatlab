# Resum — Capitol 9: Privadesa i xifrat de fitxers

## La idea clau

Al BernatLab tinc dades que vull mantenir **privades** i **segures**: contrasenyes de serveis, claus SSH, fitxers amb dades personals (DNI, adreces, factures), backups al núvol, etc. Si algun te acces fisic a la RPi o si el meu nuvol es compromes, vull que les dades estiguin **xifrades** de manera que nomes jo les pugui llegir.

En aquest capitol veurem dues eines principals per xifrar: **GPG** (l'estandard classic, el que fa servir Debian per a la firma de paquets) i **age** (una eina moderna molt mes simple que GPG). Tambe parlarem d'estrategies per protegir les dades al BernatLab.

## Que es el xifratge?

Xifrar es **transformar dades** de manera que nomes qui te la **clau** les pugui llegir. Hi ha dos tipus principals:

- **Xifratge simetric**: la mateixa clau serveix per xifrar i desxifrar. Exemple: una contrasenya.
- **Xifratge asimetric (o de clau publica)**: tens dues claus, una de publica (per xifrar) i una de privada (per desxifrar). Exemple: GPG/SSH.

Al BernatLab faig servir **els dos**:

- **Simetric** (age + passphrase) per xifrar fitxers individuals.
- **Asimetric** (claus SSH) per accedir al servidor.

## GPG: l'estandard classic

**GPG** (Gnu Privacy Guard) es la implementacio open source del standard **OpenPGP**. Es l'eina "classica" per xifrar i firmar digitalment:

- **Xifrar fitxers** amb una clau publica.
- **Desxifrar** amb la teva clau privada.
- **Firmar** documents per garantir que no s'han alterat.
- **Verificar signatures** d'altres.

### Us basic

```bash
# Generar un parell de claus
gpg --full-generate-key
# (Et demanara: nom, correu, contrasenya)

# Llistar les claus
gpg --list-keys

# Xifrar un fitxer
gpg --encrypt --recipient bernat@bernatlab.cat fitxer.txt
# Crea fitxer.txt.gpg

# Desxifrar
gpg --decrypt fitxer.txt.gpg > fitxer.txt

# Xifrar nomes amb simetria (contrasenya)
gpg --symmetric fitxer.txt
# Crea fitxer.txt.gpg (et demana contrasenya)
```

### Quan usar GPG

GPG es la millor opcio quan:

- Necessites **compatibilitat universal** (GPG es a tot arreu).
- Vols **firmar** correus o documents.
- Treballes amb correu electronic xifrat (PGP/MIME).
- Formes part d'un **equip** i vols compartir secrets.

NO es la millor opcio quan:

- Nomes vols xifrar un fitxer ràpid (age es mes simple).
- La teva clau es massa llarga/complexa (age te claus mes curtes).
- No necessites firmar res (restic ja xifra per defecte).

## age: el modern

**age** (https://age-encryption.org) es una eina de xifratge **moderna** (creada el 2019 per Filippo Valsorda, un dels mantenidors de Go) que te com a objectiu substituir GPG en casos simples. Es:

- **Molt simple**: nomes 3 ordres principals.
- **Molt segura**: usa X25519, ChaCha20-Poly1305, HMAC-SHA256.
- **Sense configuracio**: no cal generar un "keyring" complex.
- **Curta**: el codi es petit (uns 5.000 linies vs 600.000 de GPG).
- **Claus curtes**: les claus son frases humanes o cadenes curtes.

### Us basic

```bash
# Instal·la age
sudo apt install age

# Genera un parell de claus
age-keygen -o key.txt
# Et genera: 
#   - key.txt: la teva clau privada
#   - Public key: age1ql3z7hjy54pw3hyww5ayyfg7zqgvc7w3j2elw8zmrj2vn5...
# Mostra la clau publica per stdout

# Xifrar amb clau publica
age -r age1ql3z7hjy54pw3hyww5ayyfg7zqgvc7w3j2elw8zmrj2vn5... \
  -o secrets.txt.age secrets.txt

# Desxifrar amb clau privada
age -d -i key.txt -o secrets-restored.txt secrets.txt.age
```

### Xifratge simetric amb age (contrasenya)

```bash
# Xifrar amb contrasenya
age -p -o secrets.txt.age secrets.txt
# Et demana una contrasenya

# Desxifrar
age -d -o secrets-restored.txt secrets.txt.age
# Et demana la contrasenya
```

### Quan usar age

age es la millor opcio quan:

- Vols xifrar **fitxers individuals** ràpidament.
- No necessites firmar res.
- La **simplicitat** es important.
- No vols mantenir un keyring de GPG.
- Ets un usuari **modern** que vol una eina moderna.

Al BernatLab faig servir **age per defecte** per xifrar fitxers petits (scripts, configuracions amb secrets). Per a fitxers grans o carpetes, faig servir **restic** (que ja xifra amb AES-256).

## Estrategia de privadesa al BernatLab

Algunes regles que segueixo:

1. **Els secrets (.env, claus SSH, etc.) mai van al git ni al núvol en clar.** Els xifro amb age abans.
2. **Els fitxers personals** (factures, DNI escanejat) es desen xifrats amb age.
3. **Els backups al núvol** (restic) ja van xifrats per defecte amb AES-256.
4. **La RPi te el disc xifrat**? No, perque complica molt el manteniment. Pero les dades importants estan xifrades individualment.
5. **Les comunicacions** (Tailscale, SSH, HTTPS) ja van xifrades per disseny.
6. **Les contrasenyes** es desen a un **gestor de contrasenyes** (Vaultwarden, Bitwarden) xifrat.

## Gestors de contrasenyes

Un **gestor de contrasenyes** es un programa que emmagatzema totes les teves contrasenyes **xifrades** amb una **master password**. Al BernatLab faig servir:

- **Vaultwarden** (un Bitwarden auto-allotjat) per a totes les contrasenyes dels serveis.
- **KeePassXC** localment per a notes sensibles.

Mai guardo contrasenyes en fitxers de text plans, ni en un navegador, ni en un paper.

## Bones practiques

1. **No xifris el que no cal**: si les dades no son sensibles, no les xifris. Xifrar te un cost (CPU, gestio de claus).
2. **Guarda les claus en un lloc segur**: la clau privada d'edat en un USB xifrat, no al mateix disc que les dades.
3. **Practica la restauracio**: xifra un fitxer, esborra l'original, restaura'l. Si no proves mai, el dia que calgui no sabras com fer-ho.
4. **Fes servir eines modernes**: age es mes segur i mes simple que GPG per a casos basics.
5. **Automatitza el que puguis**: si xifres manualment cada fitxer, acabaras fent trampes.

## Connexions amb altres capítols

- **Cap 1** — Les dades sensibles formen part del 3-2-1, pero xifrades.
- **Cap 2** — restic ja xifra els backups amb AES-256.
- **Cap 3** — Els volums Docker contenen dades que poden ser xifrades.
- **Cap 7** — Els fitxers personals es gestionen a `/home/pi/bernatlab/`.
- **Cap 8** — Syncthing pot sincronitzar carpetes xifrades.
