# Exercici pràctic — Capítol 1: Estratègia de backup

> 30-45 min · Real al teu sistema

## Objectiu

Definir per escrit la teva **estratègia de backup personal** per al BernatLab: què, on, cada quan. Això et servirà per tenir un pla clar abans de començar a configurar eines (Restic, volums Docker, etc.) als propers capítols.

## Requisits

- Tailscale actiu
- Connexió SSH a la RPi
- Un full de paper o un fitxer de text
- 30-45 minuts

## Pas 1: Inventari de dades (10 min)

Connecta't per SSH i fes un inventari de totes les dades importants al sistema. Per cada cosa, apunta:

- Què és
- On és (ruta exacta)
- Mida aproximada
- Cada quan canvia

```bash
# Llista les carpetes grans
sudo du -sh /var/lib/docker/volumes/* 2>/dev/null
sudo du -sh /home/* 2>/dev/null
sudo du -sh /opt 2>/dev/null
sudo du -sh /etc 2>/dev/null

# Bases de dades (fitxers .db, .sqlite)
sudo find / -name "*.db" -o -name "*.sqlite" 2>/dev/null | head -20

# Configuracions importants
ls -la /opt/ 2>/dev/null
ls -la /home/bernat/ 2>/dev/null
```

Apunta-ho tot en un fitxer `inventari-dades.md` dins de `book/curs/M3/01-strategia-backup/`.

## Pas 2: Classifica per criticitat (10 min)

Per a cada element de l'inventari, assigna una criticitat:

- **CRÍTIC** (perdre-ho = desastre): bases de dades, fotos irrepetibles, configuracions de serveis.
- **IMPORTANT** (perdre-ho = molta feina): scripts, documents personals, notes.
- **RECONSTRUÏBLE** (es pot refer): sistema operatiu, imatges Docker, paquets.

Un cop classificat, pensa quin **RPO** (temps màxim de pèrdua acceptable) tens per a cada categoria:

- CRÍTIC: 1-24 hores
- IMPORTANT: 1-7 dies
- RECONSTRUÏBLE: 30 dies o mai

## Pas 3: Defineix els suports (10 min)

Decideix on posaràs cada còpia. L'objectiu és complir la regla 3-2-1.

Possibilitats:
- Disc SSD USB a la RPi
- HDD extern al calaix
- NAS a casa
- Backblaze B2 / Wasabi
- Google Drive (amb compte diferent i xifrat)
- Casa d'un familiar (un HDD que hi deixes)

Omple aquesta taula:

| Còpia | On | Freqüència | Mida estimada | Xifrada? |
|---|---|---|---|---|
| Original | | | | |
| Còpia 1 | | | | |
| Còpia 2 | | | | |

## Pas 4: Escriu l'estratègia (10 min)

Crea el fitxer `book/curs/M3/01-strategia-backup/estrategia-backup.md` amb el següent esquema:

```markdown
# La meva estratègia de backup

## Dades crítiques
- ...

## Dades importants
- ...

## Dades reconstruïbles
- ...

## Còpies
- Còpia 1: [on] cada [freqüència]
- Còpia 2: [on] cada [freqüència]
- Còpia 3: [on] cada [freqüència]

## RPO per categoria
- Bases de dades: X hores
- Configuracions: X hores
- Sistema: X dies

## Restitució de prova
- Cada quan: X mesos
- Qui ho fa: ...
- Què es comprova: ...
```

## Pas 5: Comprova que és realista

Revisa l'estratègia i respon:

- Tinc espai suficient a cada destinació? (Comprova-ho amb `df -h` al disc extern, o entrant al Backblaze B2.)
- Puc complir les freqüències que he posat? (Si un backup triga 8 hores i el vull cada 6, no és viable.)
- He pensat en el cas d'incendi a casa? (Cal la còpia fora de casa.)
- He pensat en ransomware? (La còpia remota ha de ser immutable o tenir versioning.)

## Validació

Has acabat si:

- [ ] Tens `inventari-dades.md` amb totes les dades importants llistades.
- [ ] Tens `estrategia-backup.md` amb la taula de còpies plena.
- [ ] Has classificat cada tipus de dada per criticitat.
- [ ] Has definit un RPO per categoria.
- [ ] L'estratègia compleix la regla 3-2-1.
- [ ] Has comprovat que tens espai als suports de destinació.

## Per aprofundir

- Llegeix la documentació oficial de la regla 3-2-1 a https://www.backblaze.com/blog/the-3-2-1-backup-strategy/
- Calcula el cost mensual de la teva estratègia (cloud storage + discs).
- Investiga què és el **backup immutable** i si el teu proveïdor cloud el suporta.
