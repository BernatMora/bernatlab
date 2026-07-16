# Resum — Capítol 1: Estratègia de backup al BernatLab

## La idea clau

Fer còpies de seguretat no és opcional. Al BernatLab hi ha **anys de dades de l'hort IoT** que no es poden perdre: lectures de sensors de temperatura, humitat del sòl, registres de reg, configuracions de serveis, fotografies de les tomaqueres, notes del quadern de camp. Si avui se'm mor la microSD de la RPi o el disc SSD extern on ho tinc tot, ho perdo tot. Per això cal una **estratègia**, no només un parell de comandes avui i demà ja veuré què faig.

La regla bàsica que tothom coneix és la **3-2-1**: tres còpies, en dos suports diferents, una fora de casa. És senzilla i funciona. La gent que l'aplica rarament perd dades; la que no, acaba pagant diners (o penedint-se) algun dia.

## Què cal backupejar al BernatLab

No tot té el mateix valor, i per tant no cal backupejar-ho tot amb la mateixa freqüència. Al laboratori hi tinc quatre grans grups:

- **Configuració de serveis**: els `docker-compose.yml`, els fitxers `.env`, les carpetes de configuració de cada contenidor (Grafana, Mosquitto, InfluxDB, etc.). Són petits (uns quants MB), però **reconstruir-los de zero** porta hores. Cal backupejar-los sovint.
- **Bases de dades**: SQLite, PostgreSQL, InfluxDB. Aquí hi ha les dades reals. Si perdo una base de dades, perdo informació que no puc tornar a generar.
- **Fitxers de l'usuari**: fotografies de l'hort, documents del curs, scripts, notes. Tot el que he creat jo.
- **El sistema operatiu**: Debian + Docker + eines instal·lades. Es pot refer amb una reinstal·lació, però porta temps. Un backup periòdic del sistema estalvia hores.

**El que NO cal backupejar**: contenidors (es poden tornar a baixar de les imatges oficials), paquets `.deb` (es poden tornar a instal·lar), fitxers temporals o cachés.

## La regla 3-2-1 explicada

**3 còpies** vol dir que, a més del fitxer original, n'has de tenir almenys dues còpies més. Si en perds una, te'n queden dues. Si en perds dues, encara te'n queda una.

**2 suports diferents** vol dir que les còpies no poden estar totes al mateix lloc físic. Per exemple, una còpia al disc SSD extern connectat a la RPi i una altra a un núvol (Backblaze B2, Wasabi, o fins i tot un Google Drive ben protegit). Si es mor el disc, encara tens el núvol.

**1 fora de casa** és la que la gent s'oblida més. Si tens el backup al mateix armari que el servidor, i ve una inundació, un incendi, o un lladre que s'endú l'ordinador, perds l'original i la còpia. Per això cal una còpia **fora del lloc físic**: al núvol, a casa d'un familiar, a una caixa forta. Al BernatLab jo uso Backblaze B2 (molt barat, 6 dòlars per TB al mes).

## Freqüència: la regla RPO

Cada tipus de dada té una **freqüència de backup** adequada, que depèn de quant estic disposat a perdre:

- **Configuració i codi**: cada vegada que hi ha un canvi. Al dia a dia, una vegada al dia és suficient. Jo ho automatitzo amb un cron.
- **Bases de dades**: cada dia o cada hora, segons la criticitat. Per a l'hort IoT, cada 6 hores és prudent. Si es trenca la RPi a les 14h i l'últim backup és de les 8h, perdo 6 hores de dades — acceptable.
- **Fotografies i documents nous**: quan els creo, o cada dia.
- **Sistema operatiu**: un cop al mes, o després d'una actualització important.

El **RPO (Recovery Point Objective)** és el temps màxim de dades que estic disposat a perdre. Si vull un RPO d'una hora, cal fer backup cada hora. Si un RPO d'un dia és acceptable, amb un backup diari n'hi ha prou.

## Eines que farem servir al M3

En aquest mòdul veurem eines específiques per a cada cas:

- **Restic** (cap. 2): eina moderna de backup, amb xifrat, deduplicació i versions. És la meva recomanació principal.
- **Volums Docker** (cap. 3): com fer backup dels volums de contenidors sense parar el servei.
- **SQLite** (cap. 4) i **PostgreSQL** (cap. 5): com fer backup consistent de bases de dades.
- **InfluxDB** (cap. 6): backup d'una base de dades de sèries temporals.
- **Syncthing** (cap. 8): sincronització entre dispositius.
- **GPG i age** (cap. 9): xifrat per a que les dades al núvol siguin privades.

## On posar cada còpia

Un esquema típic al BernatLab:

| Còpia | On | Freqüència |
|---|---|---|
| Original | Disc SSD USB a la RPi | (sempre) |
| Còpia local | HDD extern al calaix | Setmanal |
| Còpia remota | Backblaze B2 (xifrada) | Diària |

Les tres compleixen la regla 3-2-1: tres còpies, dos suports físics (SSD + HDD + núvol), una fora de casa (el núvol). El xifrat és fonamental perquè el núvol no és nostre.

## Errors comuns

- **"Ja ho faig servir Dropbox"**: Dropbox no és un backup. Si esborres un fitxer, Dropbox l'esborra també passats 30 dies. Si un ransomware xifra els teus fitxers, Dropbox sincronitza la versió xifrada.
- **"Faig backup del sistema sencer cada setmana"**:浪费 molt d'espai i molt de temps. Millor separar dades de sistema.
- **"Provo el backup un cop i ja està"**: un backup no provat no és un backup. Un restauració de prova trimestral és obligatòria.
- **"El núvol ja és prou segur"**: el núvol és segur, però no és *teu*. Si l'empleat de torn canvia la contrasenya per accident, et quedes sense res. Xifra abans de pujar.

## Connexions amb altres capítols

- **Cap. 2 (Restic)**: l'eina que fa tot això de manera còmoda.
- **Cap. 3 (Volums Docker)**: com aplicar la 3-2-1 als volums dels serveis.
- **Cap. 4, 5, 6**: estratègies específiques per a cada tipus de base de dades.
- **Cap. 8 (Syncthing)**: per sincronitzar carpetes entre RPi, portàtil i mòbil.
- **Cap. 9 (Privadesa i xifrat)**: per garantir que el backup remot és privat.
