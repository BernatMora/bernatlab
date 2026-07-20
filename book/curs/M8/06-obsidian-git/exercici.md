# Exercici practic - M8 Cap 6: Obsidian + Git

> 30-45 min - Al teu Windows

## Objectiu

Crear un vault d'Obsidian per al BernatLab, amb alguens notes inicials, i versionar-lo amb Git.

## Requisits

- Windows
- Git instal·lat
- 30-45 min

## Pas 1: Descarregar i instal·lar Obsidian (5 min)

1. Vés a https://obsidian.md
2. Click a **Download**
3. Instal·la (opcio per a Windows).

## Pas 2: Crear el vault (5 min)

1. Obre Obsidian per primera vegada
2. Click a **Create new vault**
3. Nom: `BernatLab`
4. Ubicacio: `C:\Users\usuari\obsidian\bernatlab\`
5. Click a **Create**

## Pas 3: Configurar (5 min)

1. Settings > Appearance > Theme: tria la que t'agradi
2. Settings > Core plugins > activa **Daily notes** i **File recovery**
3. Opcional: instal·la **Community plugins**:
   - Calendar
   - Dataview
   - Spaced Repetition (per al curs!)

## Pas 4: Crear les primeres notes (10 min)

Crea aquestes notes inicials:

**00-Index.md**:
```markdown
# BernatLab - Index

Benvingut al vault del projecte BernatLab.

## Estructura

- [[arquitectura]] - Com esta muntat el sistema
- [[runbook-emergencies]] - Procediments d'emergencia
- [[deures-i-projects]] - Coses a fer
- [[aprenentatge]] - Coses que he après

## Enllaços

- Llibre: https://bernatmora.github.io/bernatlab/
- Hort Osona: https://bernatmora.github.io/hort-osona/
- Curs: https://bernatmora.github.io/bernatlab/book/curs/
```

**arquitectura.md**:
```markdown
# Arquitectura del BernatLab

- RPi 4 (4 GB) amb Debian 13
- Docker amb 3-5 serveis
- Tailscale per a acces remot
- IP Tailscale: 100.x.y.z
- Veure [[runbook-tailscale-down]]
```

**runbook-emergencies.md**:
```markdown
# Runbooks d'Emergencia

En cas d'urgencia, segueix aquests procediments:

- [[runbook-tailscale-down]] - Si no pots accedir per Tailscale
- [[runback-portainer-down]] - Si Portainer no respon
- [[runbook-disc-ple]] - Si el disc es queda ple
```

## Pas 5: Inicialitzar Git (5 min)

Obre un terminal a la carpeta del vault:

```powershell
cd C:\Users\usuari\obsidian\bernatlab
git init
git add .
git commit -m "Inici del vault BernatLab"
```

## Pas 6: Connectar amb el repo BernatLab (10 min)

Pots afegir el vault com a part del repo del BernatLab, o crear un repo separat.

Opcio A (recomanada): com a subcarpeta del repo BernatLab.

```powershell
cd C:\Users\usuari\bernatlab
# Mou les notes a dins del repo
mkdir -p notes
# Copia (o mou) els fitxers d'obsidian
# Fes commit
git add notes/
git commit -m "Afegeix vault Obsidian inicial"
git push
```

Opcio B: repo separat.

```powershell
cd C:\Users\usuari\obsidian\bernatlab
git remote add origin https://github.com/BernatMora/bernatlab-notes.git
git push -u origin main
```

## Validacio

Has acabat si:
- [ ] Obsidian instal·lat
- [ ] Vault creat a `C:\Users\usuari\obsidian\bernatlab\`
- [ ] Almenys 3 notes creades
- [ ] Enllaços entre notes funcionen
- [ ] Git inicialitzat
- [ ] Primer commit fet

## Per aprofundir

- Instal·la mes plugins (Dataview, Mind Map, etc.).
- Crea notes diaries amb el plugin Daily Notes.
- Documenta tots els teus runbooks a Obsidian.
