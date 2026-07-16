"""
Quiz del curs del BernatLab.

Llegeix els fitxers quiz.md de cada capitol, els valida, i et permet
fer qüestionaris amb autoavaluacio.

Us:
    python quiz.py              # Mode interactiu
    python quiz.py --list       # Llista tots els capitols disponibles
    python quiz.py --m1 1       # Capitols del M1
    python quiz.py --review     # Repas espaçat (preguntes fallades abans)
    python quiz.py --stats      # Estadistiques globals

Format esperat de quiz.md:
    ## Pregunta 1
    Text de la pregunta
    
    - [ ] Opcio A
    - [x] Opcio B  (correcta)
    - [ ] Opcio C
    - [ ] Opcio D
    
    ## Pregunta 2 (oberta)
    Text de la pregunta oberta
    (sense opcions)
"""
import argparse
import json
import os
import random
import re
import sys
from datetime import datetime
from pathlib import Path

CURS_DIR = Path(__file__).parent
HISTORY_FILE = Path.home() / ".bernatlab" / "quiz_history.json"


def parse_quiz(content: str) -> list:
    """Parseja un fitxer quiz.md i retorna una llista de preguntes."""
    questions = []
    # Separem per ## Pregunta
    blocks = re.split(r'\n##\s+', content)
    for block in blocks[1:]:  # Saltem el primer (introduccio)
        lines = block.strip().split('\n')
        # Primera linia: "Pregunta N" o "Pregunta N (oberta)"
        header = lines[0].strip()
        is_open = '(oberta)' in header.lower() or '(obertura)' in header.lower()
        # Text de la pregunta: totes les linies fins a trobar opcions o final
        q_text_lines = []
        options = []
        for line in lines[1:]:
            line = line.rstrip()
            if not line:
                continue
            if line.startswith('- [') and len(line) > 4 and line[3] in 'xX ':
                # opcio
                # Format: "- [x] text" o "- [ ] text"
                is_correct = line[3].lower() == 'x'
                opt_text = line[5:].strip()
                options.append((opt_text, is_correct))
            else:
                q_text_lines.append(line)
        q_text = '\n'.join(q_text_lines).strip()
        if q_text:
            questions.append({
                'text': q_text,
                'options': options,
                'is_open': is_open or len(options) == 0,
            })
    return questions


def load_all_quizzes() -> dict:
    """Carrega tots els quiz.md del curs."""
    result = {}
    for quiz_path in sorted(CURS_DIR.rglob("quiz.md")):
        # Estructura: M1/01-que-es-bernatlab/quiz.md
        rel = quiz_path.relative_to(CURS_DIR)
        parts = rel.parts
        if len(parts) >= 3:
            module = parts[0]  # M1
            chapter = parts[1]  # 01-que-es-bernatlab
            key = f"{module}/{chapter}"
            try:
                content = quiz_path.read_text(encoding='utf-8')
                questions = parse_quiz(content)
                result[key] = {
                    'path': quiz_path,
                    'module': module,
                    'chapter': chapter,
                    'questions': questions,
                }
            except Exception as e:
                print(f"  [avís] No s'ha pogut parsejar {quiz_path}: {e}")
    return result


def load_history() -> dict:
    """Carrega l'historial de respostes."""
    if HISTORY_FILE.exists():
        try:
            return json.loads(HISTORY_FILE.read_text(encoding='utf-8'))
        except Exception:
            return {}
    return {}


def save_history(history: dict) -> None:
    """Guarda l'historial."""
    HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    HISTORY_FILE.write_text(json.dumps(history, indent=2, ensure_ascii=False), encoding='utf-8')


def ask_question(q: dict, q_num: int) -> dict:
    """Fa una pregunta i retorna el resultat."""
    print()
    print("─" * 60)
    print(f"Pregunta {q_num}: {q['text']}")
    print()
    if q['is_open']:
        print(" (Pregunta oberta — escriu la teva resposta)")
        print()
        answer = input("Resposta: ").strip()
        return {
            'question': q['text'],
            'answer': answer,
            'is_open': True,
            'correct': None,  # No validem automàticament
        }
    # Multiple choice
    options = q['options']
    for i, (text, _) in enumerate(options):
        letter = chr(ord('a') + i)
        print(f"  {letter}) {text}")
    print()
    while True:
        answer = input("Tria (a/b/c/...): ").strip().lower()
        if not answer:
            continue
        # Acceptem 'a' o 'A' o el text sencer
        if len(answer) == 1 and answer in 'abcdefghij':
            idx = ord(answer) - ord('a')
            if 0 <= idx < len(options):
                answer = idx
                break
        # O el text
        for i, (text, _) in enumerate(options):
            if text.lower().startswith(answer.lower()):
                answer = i
                break
        else:
            continue
        break
    correct_idx = next((i for i, (_, c) in enumerate(options) if c), None)
    is_correct = answer == correct_idx
    return {
        'question': q['text'],
        'answer': options[answer][0] if isinstance(answer, int) else answer,
        'correct': is_correct,
        'is_open': False,
    }


def run_quiz(quiz_data: dict, history: dict, mode: str = 'normal') -> None:
    """Executa un qüestionari."""
    key = f"{quiz_data['module']}/{quiz_data['chapter']}"
    questions = quiz_data['questions']
    if not questions:
        print(f"  [avís] {key} no té preguntes.")
        return
    print()
    print("=" * 60)
    print(f"  QUIZ: {key}")
    print(f"  Preguntes: {len(questions)}")
    print("=" * 60)
    results = []
    for i, q in enumerate(questions, 1):
        result = ask_question(q, i)
        results.append(result)
        if not result['is_open'] and result['correct'] is not None:
            if result['correct']:
                print("  ✓ Correcte!")
            else:
                # Mostrar la correcta
                for text, is_c in q['options']:
                    if is_c:
                        print(f"  ✗ Incorrecte. La correcta era: {text}")
                        break
    # Estadistiques
    auto = [r for r in results if not r['is_open']]
    correct = sum(1 for r in auto if r['correct'])
    total = len(auto)
    open_q = [r for r in results if r['is_open']]
    print()
    print("=" * 60)
    print(f"  RESULTAT")
    print(f"  Automatiques: {correct}/{total} correctes")
    print(f"  Obertes: {len(open_q)} (cal revisar manualment)")
    if total > 0:
        pct = (correct / total) * 100
        print(f"  Percentatge: {pct:.0f}%")
    print("=" * 60)
    # Guardar a l'historial
    if key not in history:
        history[key] = {'attempts': []}
    history[key]['attempts'].append({
        'date': datetime.now().isoformat(),
        'mode': mode,
        'correct': correct,
        'total': total,
        'open_questions': len(open_q),
        'results': results,
    })
    save_history(history)
    print(f"\n  Resultat guardat a {HISTORY_FILE}")
    if open_q:
        print(f"\n  Recorda revisar les respostes obertes a:")
        print(f"  {quiz_data['path'].parent / 'respostes.md'}")


def cmd_list(quizzes: dict) -> None:
    """Llista tots els capitols disponibles."""
    print()
    print("=" * 60)
    print("  CAPITOLS DISPONIBLES")
    print("=" * 60)
    by_module = {}
    for key, data in quizzes.items():
        by_module.setdefault(data['module'], []).append((data['chapter'], len(data['questions'])))
    for mod in sorted(by_module.keys()):
        print(f"\n  {mod}:")
        for ch, n in by_module[mod]:
            print(f"    - {ch} ({n} preguntes)")


def cmd_review(quizzes: dict, history: dict) -> None:
    """Repas espaçat: tria 5 preguntes aleatories de les que has fallat."""
    failed = []
    for key, data in quizzes.items():
        if key not in history:
            continue
        for attempt in history[key]['attempts']:
            for r in attempt.get('results', []):
                if r.get('is_open'):
                    continue
                if r.get('correct') is False:
                    failed.append({
                        'quiz_key': key,
                        'question': r['question'],
                        'quiz_data': data,
                    })
    if not failed:
        print("\n  No tens preguntes fallades! O encara no has fet cap quiz.")
        return
    print()
    print("=" * 60)
    print(f"  REPAS: {len(failed)} preguntes fallades disponibles")
    print("=" * 60)
    # Triem 5 aleatories
    sample = random.sample(failed, min(5, len(failed)))
    for i, item in enumerate(sample, 1):
        # Trobar la pregunta original
        q_text = item['question']
        original = next((q for q in item['quiz_data']['questions'] if q['text'] == q_text), None)
        if not original:
            continue
        print(f"\n  ({item['quiz_key']})")
        result = ask_question(original, i)
        if not result['is_open'] and result['correct'] is not None:
            if result['correct']:
                print("  ✓ Ara sí!")
            else:
                print("  ✗ Encara no. Torna-ho a revisar.")


def cmd_stats(history: dict) -> None:
    """Mostra estadistiques globals."""
    print()
    print("=" * 60)
    print("  ESTADISTIQUES")
    print("=" * 60)
    if not history:
        print("\n  Encara no has fet cap quiz.")
        return
    total_attempts = 0
    total_correct = 0
    total_q = 0
    for key, data in history.items():
        attempts = data.get('attempts', [])
        for a in attempts:
            total_attempts += 1
            total_correct += a.get('correct', 0)
            total_q += a.get('total', 0)
    print(f"\n  Total intents: {total_attempts}")
    print(f"  Total preguntes automàtiques: {total_q}")
    print(f"  Total encerts: {total_correct}")
    if total_q > 0:
        pct = (total_correct / total_q) * 100
        print(f"  Percentatge global: {pct:.0f}%")
    print(f"\n  Per capítol:")
    for key in sorted(history.keys()):
        attempts = history[key]['attempts']
        last = attempts[-1]
        total = last.get('total', 0)
        correct = last.get('correct', 0)
        if total > 0:
            pct = (correct / total) * 100
            print(f"    {key}: últim {correct}/{total} ({pct:.0f}%), {len(attempts)} intents")


def main() -> int:
    parser = argparse.ArgumentParser(description="Quiz del BernatLab")
    parser.add_argument('--list', action='store_true', help='Llista capitols')
    parser.add_argument('--m1', type=int, help='Capitol del M1 (1-10)')
    parser.add_argument('--review', action='store_true', help='Repas espaçat')
    parser.add_argument('--stats', action='store_true', help='Estadistiques')
    args = parser.parse_args()
    quizzes = load_all_quizzes()
    history = load_history()
    if args.list:
        cmd_list(quizzes)
        return 0
    if args.review:
        cmd_review(quizzes, history)
        return 0
    if args.stats:
        cmd_stats(history)
        return 0
    if args.m1 is not None:
        ch = f"0{args.m1}-" if args.m1 < 10 else f"{args.m1}-"
        # Buscar coincidencia
        matches = [k for k in quizzes if k.startswith(f"M1/{ch}")]
        if not matches:
            print(f"  No s'ha trobat el capítol M1/{ch}*")
            print("  Usa --list per veure els disponibles.")
            return 1
        for m in matches:
            run_quiz(quizzes[m], history, mode='normal')
        return 0
    # Mode per defecte: interactiu
    print()
    print("=" * 60)
    print("  QUIZ DEL BERNATLAB")
    print("=" * 60)
    print("\n  Opcions:")
    print("    1) Fer un quiz")
    print("    2) Repas espaçat")
    print("    3) Estadistiques")
    print("    4) Llistar capitols")
    print("    0) Sortir")
    print()
    choice = input("  Tria (0-4): ").strip()
    if choice == '1':
        cmd_list(quizzes)
        key = input("\n  Tria un capitol (ex. M1/01-que-es-bernatlab): ").strip()
        if key in quizzes:
            run_quiz(quizzes[key], history, mode='normal')
        else:
            print("  No existeix.")
    elif choice == '2':
        cmd_review(quizzes, history)
    elif choice == '3':
        cmd_stats(history)
    elif choice == '4':
        cmd_list(quizzes)
    return 0


if __name__ == '__main__':
    sys.exit(main())
