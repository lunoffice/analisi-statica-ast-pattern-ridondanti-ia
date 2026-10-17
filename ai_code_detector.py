import ast
import argparse
from pathlib import Path


class AILikePatternVisitor(ast.NodeVisitor):
    def __init__(self, filename: str):
        self.filename = filename
        self.issues: list[str] = []
        self.seen_imports: set[str] = set()

    def report(self, line: int, message: str) -> None:
        self.issues.append(f"{self.filename}:{line} -> {message}")

    def visit_Import(self, node: ast.Import) -> None:
        for alias in node.names:
            if alias.name in self.seen_imports:
                self.report(node.lineno, f"Import duplicato trovato: '{alias.name}'")
            self.seen_imports.add(alias.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        if node.module:
            if node.module in self.seen_imports:
                self.report(
                    node.lineno,
                    f"Import (from) duplicato trovato: '{node.module}'",
                )
            self.seen_imports.add(node.module)
        self.generic_visit(node)

    def visit_Try(self, node: ast.Try) -> None:
        for handler in node.handlers:
            is_broad = handler.type is None or (
                isinstance(handler.type, ast.Name) and handler.type.id == "Exception"
            )
            if is_broad and len(handler.body) == 1 and isinstance(
                handler.body[0], ast.Pass
            ):
                self.report(
                    handler.lineno,
                    "Segnalazione: 'except' ampio con solo pass (silenzioso)",
                )
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        if node.end_lineno is not None:
            length = node.end_lineno - node.lineno
            if length > 50:
                self.report(
                    node.lineno,
                    f"Funzione monstre '{node.name}' ({length} righe). Valuta il refactoring.",
                )
        self.generic_visit(node)

    def visit_If(self, node: ast.If) -> None:
        if isinstance(node.test, ast.Constant) and isinstance(node.test.value, bool):
            self.report(
                node.lineno,
                f"Condizione statica trovata (if {node.test.value}:). Rimasuglio di debug?",
            )
        self.generic_visit(node)


def analyze_file(filepath: Path) -> list[str]:
    try:
        content = filepath.read_text(encoding="utf-8")
        tree = ast.parse(content)
        visitor = AILikePatternVisitor(str(filepath))
        visitor.visit(tree)
        return visitor.issues
    except SyntaxError as e:
        return [
            f"{filepath} -> Errore di sintassi alla riga {e.lineno}. "
            "L'AST richiede codice Python valido."
        ]
    except OSError as e:
        return [f"{filepath} -> Errore di lettura: {e}"]


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Scansiona script Python per pattern tipici da LLM."
    )
    parser.add_argument("path", help="File o cartella da scansionare")
    args = parser.parse_args()

    target = Path(args.path)
    if target.is_file() and target.suffix == ".py":
        files = [target]
    elif target.is_dir():
        files = sorted(target.rglob("*.py"))
    else:
        print("Percorso non valido o nessun file Python trovato.")
        return

    # Evita di segnalare lo scanner stesso se sta nella cartella
    files = [f for f in files if f.name != "ai_code_detector.py"]

    total: list[str] = []
    for py_file in files:
        total.extend(analyze_file(py_file))

    print(f"\n--- Scansione completata su {len(files)} file ---")
    if not total:
        print("Nessun pattern sospetto rilevato (con le euristiche attuali).")
    else:
        for issue in total:
            print(issue)
        print(f"\nTotale segnalazioni: {len(total)}")


if __name__ == "__main__":
    main()
