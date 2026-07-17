# Qüestionari - Capitol 7: Backups segurs

> 10 preguntes · ~15 min

## Pregunta 1
Quina es la regla 3-2-1 dels backups?

- [ ] 3 servidors, 2 discos, 1 cloud
- [x] 3 copies, 2 mitjans diferents, 1 fora de casa
- [ ] 3 hores de backup, 2 dies de retencio, 1 mes de proves
- [ ] 3 usuaris, 2 contrasenyes, 1 servidor

## Pregunta 2
Que es Restic?

- [ ] Un tipus de disc dur
- [x] Una eina de backup moderna, xifrada, incremental i deduplicada
- [ ] Un servei de cloud
- [ ] Un sistema operatiu

## Pregunta 3
Per que xifrar els backups?

- [ ] Per estalviar espai
- [x] Perque si el backup es robat o filtrat, les dades no son llegibles
- [ ] Perque es mes rapid
- [ ] Perque el cloud ho exigeix

## Pregunta 4
Que pasa si perds la clau de xifratge d'un backup Restic?

- [ ] Restic te una recuperacio d'emergencia
- [x] No pots restaurar mai, les dades son il·legibles per sempre
- [ ] Pots restaurar nomes parcialment
- [ ] Restic et permet tornar a xifrar amb una clau nova

## Pregunta 5
Quina comanda llista els snapshots existents?

- [ ] restic list
- [x] restic snapshots
- [ ] restic show
- [ ] restic status

## Pregunta 6
Que vol dir un backup "incremental"?

- [ ] Que nomes es fa de nit
- [x] Que nomes es copia el que ha canviat desde l'ultim backup
- [ ] Que nomes es guarden els fitxers petits
- [ ] Que nomes es poden restaurar alguns fitxers

## Pregunta 7
Quin es el risc mes gran d'un backup sense proves?

- [ ] Que ocupi molt d'espai
- [x] Que no es pugui restaurar quan el necessitis
- [ ] Que el cloud el cobri
- [ ] Que trigui massa

## Pregunta 8
Quin es el backend mes economic per a backups al núvol?

- [ ] AWS S3
- [ ] Google Cloud Storage
- [x] Backblaze B2 (~$6/TB/mes)
- [ ] Azure Blob

## Pregunta 9 (oberta)
Descriu una politica de backups pel BernatLab. Inclou què backupejar, on, cada quan, i com comprovar que funciona.

Pistes per respondre:
- Llista els elements a backupejar: bases de dades, volums, configuracions, secrets.
- Aplica la regla 3-2-1: local + núvol.
- Defineix una frequencia (cada dia? cada setmana?).
- Esmenta una politica de retencio concreta.
- Explica com verificaries que el backup funciona.

## Pregunta 10 (oberta)
Has descobert que el teu unic backup esta al mateix disc que les dades originals. Un dia el disc falla. Que has après i que faries diferent?

Pistes per respondre:
- Explica per que es un problema (no es un backup, es una copia redundant).
- Aplica la regla 3-2-1: el backup ha d'estar separat fisicament.
- Proposa una solucio: núvol (Backblaze B2), NAS extern, altre servidor.
- Parla de la importancia de provar la restauracio.


## Pregunta 11
Per que sha dencriptar el backup si nomes soc jo qui lactualmente? Pensa en el futur.

**Pistes**: Pistes: Robatori, disc, cloud, dispositiu perdut, aqui 2 anys.

## Pregunta 12
Explica la diferencia entre un backup encriptat i un backup comprimit amb contrasenya.

**Pistes**: Pistes: E2E, zero-knowledge, vulnerabilitat, atac.

## Pregunta 13
Com organiszaries el cicle de vida duna clau dencriptat al teu sistema?

**Pistes**: Pistes: Crear, usar, emmagatzemar, rotar, destruir.


## Pregunta 14 (oberta amb pistes)
Per que sha dencriptar el backup si nomes soc jo qui lactualmente

**Pistes**: pensa en com aplicaries aquest concepte al teu hort IoT amb la teva RPi (hortosona, 100.115.134.76).
## Pregunta 15 (oberta amb pistes)
Explica la diferencia entre un backup encriptat i un backup comprimit amb contrasenya

**Pistes**: pensa en com aplicaries aquest concepte al teu hort IoT amb la teva RPi (hortosona, 100.115.134.76).
