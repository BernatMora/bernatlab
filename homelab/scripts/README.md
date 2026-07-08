# homelab/scripts/

Scripts de manteniment i operació del BernatLab.

## publish.py

Automatitza el cicle d'edició → generació → publicació a GitHub.

### Què fa

1. Regenera el PDF i DOCX (crida `book/make_book.py`).
2. Fa `git add` dels canvis a `book/chapters/` i `book/output/`.
3. Fa `git commit` amb el missatge que li passem (o un genèric).
4. Fa `git push` a `origin/main`.

### Ús

```bash
# Des de l'arrel del repo
python homelab/scripts/publish.py
python homelab/scripts/publish.py "Mòdul 2 — corregeix capítol 19"

# Des de qualsevol lloc (el path és relatiu a l'script)
python ~/bernatlab/homelab/scripts/publish.py "Afegeix capítol 23"
```

### Requisits

- Estar en una màquina amb `git` configurat i `gh` autenticat (o amb un remote `origin` vàlid).
- El venv de Python a la carpeta pare del repo (per poder executar `make_book.py`).

## Pròxims scripts a afegir

- `backup.sh` — còpia de seguretat d'InfluxDB i volums persistents.
- `update.sh` — actualitza tots els contenidors amb un sol cop.
- `pull-bernatlab.sh` — descarrega la darrera versió del repo a la Raspberry.
