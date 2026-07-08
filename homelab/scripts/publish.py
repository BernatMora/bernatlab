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
    venv_py = ROOT.parent / ".venv" / "Scripts" / "python.exe"
    if not venv_py.exists():
        venv_py = ROOT.parent / ".venv" / "bin" / "python"
    if venv_py.exists():
        run([str(venv_py), str(BOOK / "make_book.py")])
    else:
        print(f"AVÍS: no trobo el venv a {venv_py}. Executa make_book.py manualment.")

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
