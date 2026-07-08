#!/usr/bin/env python3
"""
publish.sh — Publica una nova versió del llibre a GitHub.

Què fa:
1. Regenera el PDF i DOCX (tots dos mòduls).
2. Fa `git add` de canvis a chapters/ i output/.
3. Fa `git commit` amb el missatge que passem com a argument
   (o un missatge per defecte si no en donem cap).
4. Fa `git push` a origin/main.

Ús:
    ./publish.sh
    ./publish.sh "Mòdul 2 — afegit capítol 21"
    ./publish.sh "Corregeix typos capítol 5"

Configuració:
    S'ha d'executar des de l'arrel del repo bernatlab/ o des de book/.
"""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOOK = ROOT / "book"
MSG = " ".join(sys.argv[1:]) or "Actualitza llibre"


def run(cmd, cwd=None, check=True):
    """Executa una comanda i mostra la sortida."""
    print(f"\n$ {' '.join(cmd)}")
    res = subprocess.run(cmd, cwd=cwd or ROOT, capture_output=True, text=True)
    if res.stdout:
        print(res.stdout.strip())
    if res.stderr and res.returncode != 0:
        print(res.stderr.strip(), file=sys.stderr)
    if check and res.returncode != 0:
        sys.exit(res.returncode)
    return res


def main():
    # 1. Regenerar PDF i DOCX
    print("=== 1. Regenerant llibre ===")
    # El venv pot viure a tres llocs, en ordre de preferència:
    #   1) <repo>/.venv/                  — quan s'ha fet `uv venv` dins del repo
    #   2) <repo-parent>/.venv/           — quan el venv és a la carpeta mare
    #   3) <repo-parent>/<repo>/.venv/    — com en aquest repo (bernatlab/.venv)
    venv_candidates = [
        ROOT / ".venv" / "Scripts" / "python.exe",       # Windows
        ROOT / ".venv" / "bin" / "python",                # Linux/Mac
        ROOT.parent / ".venv" / "Scripts" / "python.exe",
        ROOT.parent / ".venv" / "bin" / "python",
    ]
    venv_py = None
    for cand in venv_candidates:
        if cand.exists():
            venv_py = cand
            break

    if venv_py is not None:
        run([str(venv_py), str(BOOK / "make_book.py")])
    else:
        # Sense venv, intentem amb el python del sistema
        print(f"AVÍS: no trobo cap venv. Provo amb python del sistema.")
        try:
            run([sys.executable, str(BOOK / "make_book.py")])
        except SystemExit:
            print("ERROR: make_book.py ha fallat. Comprova que reportlab i python-docx")
            print("       estan instal·lats (pip install reportlab python-docx).")
            raise

    # 2. git add
    print("\n=== 2. git add ===")
    run(["git", "add", "book/chapters/", "book/output/"])

    # 3. Estat
    print("\n=== 3. Estat ===")
    res = run(["git", "status", "--short"], check=False)
    if not res.stdout.strip():
        print("Res a cometre. Sortint.")
        return

    # 4. git commit
    print("\n=== 4. git commit ===")
    run(["git", "commit", "-m", MSG])

    # 5. git push
    print("\n=== 5. git push ===")
    run(["git", "push", "origin", "main"])


if __name__ == "__main__":
    main()
