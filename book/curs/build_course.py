#!/usr/bin/env python3
"""Genera i valida les metadades del curs BernatLab.

La font de veritat són els directoris M1..M8 i els quatre fitxers Markdown
de cada capítol. El manifest resultant alimenta la navegació i el progrés web.
"""

from __future__ import annotations

import argparse
import html
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote


COURSE_DIR = Path(__file__).resolve().parent
MANIFEST_PATH = COURSE_DIR / "course-manifest.json"
REQUIRED_FILES = ("resum.md", "quiz.md", "exercici.md", "respostes.md")
MODULE_NAMES = {
    "M1": "Fonaments",
    "M2": "Contenidors",
    "M3": "Dades",
    "M4": "Intel·ligència",
    "M5": "Seguretat",
    "M6": "Operativa 24/7",
    "M7": "Hort Osona en acció",
    "M8": "Eines del dia a dia",
}
FORBIDDEN_CONTENT = {
    "100.115.134.76": "adreça Tailscale personal",
    r"C:\Users\iadmin": "ruta personal de Windows",
    "(veure fitxer complet)": "marcador de contingut incomplet",
}


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "a":
            href = dict(attrs).get("href")
            if href:
                self.links.append(href)


def natural_key(value: str) -> tuple:
    return tuple(int(part) if part.isdigit() else part.lower()
                 for part in re.split(r"(\d+)", value))


def extract_title(page: Path) -> str:
    text = page.read_text(encoding="utf-8")
    match = re.search(r"<h1[^>]*>(.*?)</h1>", text, re.I | re.S)
    raw = match.group(1) if match else page.stem
    raw = re.sub(r"<[^>]+>", "", raw)
    raw = html.unescape(raw).strip()
    return re.sub(r"^[^\wÀ-ÿ]*Cap\s+\d+\.\s*", "", raw, flags=re.I)


def parse_questions(path: Path) -> int:
    text = path.read_text(encoding="utf-8")
    return len(re.findall(r"^##\s+Pregunta\b", text, re.I | re.M))


def validate_quiz(path: Path) -> list[str]:
    """Comprova que cada pregunta tancada tingui una sola resposta correcta."""
    errors = []
    text = path.read_text(encoding="utf-8")
    blocks = re.split(r"(?=^##\s+Pregunta\b)", text, flags=re.I | re.M)
    for block in blocks:
        heading = re.match(r"^##\s+Pregunta\s+(\d+)", block, re.I)
        if not heading:
            continue
        options = re.findall(r"^- \[([ xX])\]\s+", block, re.M)
        if options:
            correct = sum(value.lower() == "x" for value in options)
            if correct != 1:
                errors.append(
                    f"{path.relative_to(COURSE_DIR.parent.parent)}: "
                    f"pregunta {heading.group(1)} té {correct} respostes correctes"
                )
    return errors


def ensure_script(page: Path) -> bool:
    text = page.read_text(encoding="utf-8")
    script = '<script src="../curs.js"></script>'
    if script in text:
        return False
    if "</body>" not in text:
        raise ValueError(f"{page}: falta </body>")
    page.write_text(text.replace("</body>", f"    {script}\n</body>"), encoding="utf-8")
    return True


def validate_links() -> list[str]:
    errors = []
    repo_root = COURSE_DIR.parent.parent
    github_prefixes = (
        "https://github.com/BernatMora/bernatlab/blob/main/",
        "https://github.com/BernatMora/bernatlab/tree/main/",
    )
    pages = [repo_root / "index.html", COURSE_DIR / "index.html", *COURSE_DIR.glob("M*/*.html")]
    for page in pages:
        parser = LinkParser()
        parser.feed(page.read_text(encoding="utf-8"))
        for href in parser.links:
            if href.startswith(("#", "mailto:")):
                continue
            github_prefix = next((prefix for prefix in github_prefixes if href.startswith(prefix)), None)
            if github_prefix:
                target = repo_root / unquote(href[len(github_prefix):].split("#", 1)[0])
                if not target.exists():
                    errors.append(f"{page.relative_to(repo_root)}: enllaç GitHub inexistent {href}")
                continue
            if href.startswith(("http://", "https://")):
                continue
            clean = unquote(href.split("#", 1)[0].split("?", 1)[0])
            target = (page.parent / clean)
            if href.endswith("/"):
                target /= "index.html"
            if clean and not target.exists():
                errors.append(f"{page.relative_to(repo_root)}: enllaç local inexistent {href}")
    return errors


def validate_content() -> list[str]:
    """Evita que tornin a aparèixer dades personals o marcadors incomplets."""
    errors = []
    paths = [*COURSE_DIR.rglob("*.md"), *COURSE_DIR.rglob("*.html"), *COURSE_DIR.rglob("*.js")]
    for path in paths:
        text = path.read_text(encoding="utf-8")
        for value, description in FORBIDDEN_CONTENT.items():
            if value in text:
                errors.append(
                    f"{path.relative_to(COURSE_DIR.parent.parent)}: {description} ({value})"
                )
    return errors


def build(write: bool) -> tuple[dict, list[str]]:
    chapters = []
    errors: list[str] = []
    injected = 0

    module_dirs = sorted(
        (path for path in COURSE_DIR.iterdir()
         if path.is_dir() and re.fullmatch(r"M\d+", path.name)),
        key=lambda path: natural_key(path.name),
    )

    for module_dir in module_dirs:
        pages = sorted(module_dir.glob("[0-9][0-9]-*.html"), key=lambda p: natural_key(p.name))
        for page in pages:
            chapter_dir = module_dir / page.stem
            missing = [name for name in REQUIRED_FILES if not (chapter_dir / name).exists()]
            if missing:
                errors.append(f"{module_dir.name}/{page.stem}: falten {', '.join(missing)}")
                continue

            if write:
                if ensure_script(page):
                    injected += 1
            elif '<script src="../curs.js"></script>' not in page.read_text(encoding="utf-8"):
                errors.append(f"{module_dir.name}/{page.name}: falta curs.js")

            questions = parse_questions(chapter_dir / "quiz.md")
            if questions == 0:
                errors.append(f"{module_dir.name}/{page.stem}: qüestionari buit")
            errors.extend(validate_quiz(chapter_dir / "quiz.md"))

            chapters.append({
                "key": f"{module_dir.name}/{page.stem}",
                "module": module_dir.name,
                "moduleName": MODULE_NAMES.get(module_dir.name, module_dir.name),
                "chapter": int(page.stem.split("-", 1)[0]),
                "slug": page.stem,
                "title": extract_title(page),
                "href": f"{module_dir.name}/{page.name}",
                "quizUrl": f"{module_dir.name}/{page.stem}/quiz.md",
                "answersUrl": f"{module_dir.name}/{page.stem}/respostes.md",
                "questionCount": questions,
            })

    manifest = {
        "schemaVersion": 1,
        "moduleCount": len(module_dirs),
        "chapterCount": len(chapters),
        "questionCount": sum(chapter["questionCount"] for chapter in chapters),
        "modules": [
            {
                "id": module_dir.name,
                "name": MODULE_NAMES.get(module_dir.name, module_dir.name),
                "chapterCount": sum(1 for chapter in chapters if chapter["module"] == module_dir.name),
                "questionCount": sum(chapter["questionCount"] for chapter in chapters if chapter["module"] == module_dir.name),
            }
            for module_dir in module_dirs
        ],
        "chapters": chapters,
    }

    if write:
        MANIFEST_PATH.write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        print(f"Manifest generat: {MANIFEST_PATH.relative_to(COURSE_DIR.parent.parent)}")
        print(f"Scripts afegits a {injected} capítols")
    elif not MANIFEST_PATH.exists() or json.loads(MANIFEST_PATH.read_text(encoding="utf-8")) != manifest:
        errors.append("course-manifest.json està desactualitzat; executa build_course.py")

    errors.extend(validate_links())
    errors.extend(validate_content())

    return manifest, errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Valida sense modificar fitxers")
    args = parser.parse_args()
    manifest, errors = build(write=not args.check)

    print(
        f"{manifest['moduleCount']} mòduls · "
        f"{manifest['chapterCount']} capítols · "
        f"{manifest['questionCount']} preguntes"
    )
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
