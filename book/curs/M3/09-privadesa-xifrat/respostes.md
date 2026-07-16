# Respostes — Capitol 9: Privadesa i xifrat de fitxers

> Mira les respostes DESPRES d'haver fet el qüestionari.

## Pregunta 1: Tipus de xifratge amb la mateixa clau

**Resposta correcta**: Simetric.

**Explicacio**: El xifratge **simetric** usa la mateixa clau per xifrar i desxifrar. Es mes rapid pero te el problema de com passar la clau de forma segura. Exemples: AES, ChaCha20. El xifratge **asimetric** (RSA, Ed25519) usa dues claus diferents: una publica per xifrar i una privada per desxifrar. Es mes lent pero permet intercanviar secrets sense canal segur.

---

## Pregunta 2: Avantatge d'edat sobre GPG

**Resposta correcta**: Es molt mes simple.

**Explicacio**: **age** te nomes 3 ordres principals (`age-keygen`, `age -r`, `age -d`) i una sintaxi molt intuitiva. **GPG** te centenars d'opcions, sub-ordres, configuracio, i un keyring que cal mantenir. Per a un cas simple com "xifrar un fitxer", age es 10x mes rapid d'aprendre i d'usar.

---

## Pregunta 3: Generar claus amb age

**Resposta correcta**: `age-keygen -o key.txt`.

**Explicacio**: L'ordre `age-keygen` genera un parell de claus: desa la clau privada al fitxer especificat (`-o`) i mostra la clau publica per stderr. Es mes simple que `gpg --full-generate-key` que et demana 5 coses diferents (nom, correu, tipus, mida, expiracio).

---

## Pregunta 4: Xifrat en repos

**Resposta correcta**: Que les dades estan xifrades al disc o al nuvol.

**Explicacio**: **Xifrat en repos** (encryption at rest) significa que les dades estan xifrades quan estan emmagatzemades, no nomes durant la transmissio. Si un atacant roba el disc dur o accedeix al nuvol, veu nomes dades xifrades. Es diferent de **xifrat en transit** (TLS), que nomes protegeix durant la transmissio.

---

## Pregunta 5: Algorisme d'edat

**Resposta correcta**: ChaCha20-Poly1305.

**Explicacio**: **age** fa servir **X25519** per a l'intercanvi de claus, **ChaCha20-Poly1305** per al xifratge simetric, i **HMAC-SHA256** per a l'autenticacio. Son tots algoritmes moderns, segurs, i ben auditats. Semblant a la combinacio que fa servir WireGuard o SSH modern.

---

## Pregunta 6: Master password

**Resposta correcta**: La contrasenya principal que xifra tot el gestor.

**Explicacio**: Un **gestor de contrasenyes** emmagatzema totes les teves contrasenyes xifrades amb una sola **master password**. Si l'oblides, no pots accedir a res. Es la contrasenya mes important que tens: ha de ser llarga, unica, i memoritzable (una frase sencera es bona). Exemples: "el-gat-del-veinat-es-groc-i-s-escriu-juan".

---

## Pregunta 7: Clau privada al disc

**Resposta correcta**: Si es perd el disc, perds les dades i la clau per desxifrar-les.

**Explicacio**: Si tens la clau privada al mateix disc que les dades xifrades, un atacant que aconsegueixi el disc (robo, fallada, hack) te tant les dades xifrades com la clau per desxifrar-les. Llavors el xifrat no serveix per a res. La clau ha d'estar en un altre lloc: un USB extern, un altre servidor, un paper guardat en un lloc segur.

---

## Pregunta 8: Xifratge SSH

**Resposta correcta**: Asimetric amb RSA/Ed25519.

**Explicacio**: SSH (Secure Shell) fa servir **xifratge asimetric** per autenticar-se: tens una clau publica al servidor (`.ssh/authorized_keys`) i una clau privada al client (`~/.ssh/id_ed25519`). El client demostra que te la clau privada sense enviar-la. Despres, un cop autenticat, s'estableix un **xifrat simetric** per a la comunicacio (ChaCha20 o AES).

---

## Pregunta 9 (oberta): age vs GPG per a un fitxer

**Resposta model**:

Per xifrar un sol fitxer individual, **age es molt millor opcio que GPG** per varies raons:

**Flux amb age** (5 passos):
1. `age-keygen -o key.txt` (genera claus)
2. `age -r age1... -o secret.age secret.txt` (xifra)
3. `age -d -i key.txt -o secret-restored.txt secret.age` (desxifra)

Total: 3 ordres, 30 segons.

**Flux amb GPG** (10+ passos):
1. `gpg --full-generate-key` (et demana 5 coses)
2. Confirmar el nom i correu
3. Escriure una passphrase dues vegades
4. Esperar que generi entropia
5. `gpg --list-keys` (per trobar el recipient)
6. `gpg --output secret.gpg --encrypt --recipient bernat@... secret.txt`
7. `gpg --output secret-restored.txt --decrypt secret.gpg`
8. Escriure la passphrase dues vegades

Total: 8+ ordres, 5-10 minuts, moltes decisions.

**Avantatges tecnics d'edat**:
- **Codi base mes petit**: 5.000 linies vs 600.000 de GPG. Menys bugs, menys superficie d'atac.
- **Algorismes moderns**: X25519 + ChaCha20 + Poly1305. GPG te opcions antigues que poden ser insegures si no les evites explicitament.
- **Sense web of trust**: GPG te un model de confiança complicat (keysigning parties, etc.) que la gent no enten. age ho ignora per complet.
- **Millor per scripting**: les opcions son simples i consistent.

**Limitacio**: si necessites **firmar** correus o documents, GPG es millor (age no firma, nomes xifra). Pero per a xifrar fitxers, age es clarament superior.

**Conclusio**: per al 95% dels casos, age es la opcio correcta. GPG nomes quan necessites compatibilitat o firmes digitals.

---

## Pregunta 10 (oberta): Estrategia de privadesa per a l'hort

**Resposta model**:

Per a l'hort IoT del BernatLab, classificaria les dades en tres categories:

**1. Dades publiques** (no cal protegir):
- Lectures de sensors: temperatura, humitat, llum.
- Estadistiques agregades: mitjanes diaries, totals mensuals.
- Configuracio dels sensors: posicio, calibracio.

Aquestes dades poden anar al git, al nuvol, i son visibles a Grafana publicament (si vols).

**2. Dades privades** (protegir amb permisos):
- Fotografies de l'hort (mostren ubicacio).
- Notes personals amb observacions.
- Factures de llavors, eines, etc.
- Adreça i ubicacio exacta de l'hort.

Aquestes fitxers es desen al servidor pero amb permisos `600` (nomes jo), i es poden sincronitzar via Syncthing nomes entre els meus dispositius.

**3. Secrets** (xifrar obligatoriament):
- Contrasenyes de serveis: PostgreSQL, InfluxDB, Nextcloud, Grafana, etc.
- Claus SSH privades.
- Tokens API: per a InfluxDB cloud, GitHub, etc.
- Fitxers `.env` amb variables sensibles.
- Documents d'identitat (DNI, passaport escanejats).

Aquests fitxers **mai van al git ni al nuvol en clar**. Es xifren amb **age** (clau publica) i la clau privada es guarda en un USB xifrat separat.

**Eines**:
- **Vaultwarden** (Bitwarden) per a totes les contrasenyes de serveis.
- **age** per a fitxers individuals amb secrets.
- **restic** per a backups (ja xifra AES-256).
- **SSH** amb claus Ed25519 per a acces remot.
- **Tailscale** per a xarxa privada (WireGuard).

**Regles**:
1. Mai una contrasenya en un fitxer .txt pla.
2. El .env nomes si es nomes al servidor. Si va al git, primer xifrar.
3. Practicar la restauracio: una vegada al trimestre provo de restaurar un secret xifrat.
4. Fer servir un password manager per a totes les contrasenyes. Cap excepcio.

**Conclusio**: la privadesa no es paranoia, es higiene digital. Xifrar es costos, pero es molt mes barat que les consequencies d'un robatori de dades.

---

## Que fer si has fallat moltes preguntes

- **5-8 encerts**: Rellegir el resum.
- **3-4 encerts**: Rellegeix el capitol amb atencio, sobretot la seccio d'edat.
- **0-2 encerts**: Repassem junts el capitol. Es la base per a la seguretat del BernatLab.

## Que fer si has encertat totes

- Passa al **Capitol 10** (visualitzacio amb Grafana).
- O fes l'**exercici practic** amb Vaultwarden.
