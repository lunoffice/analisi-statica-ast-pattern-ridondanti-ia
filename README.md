# Analisi statica con AST: pattern ridondanti dell'IA in Python (locale)

Script Python **offline** che usa il modulo `ast` della libreria standard per segnalare indizi tipici di codice generato in fretta da un LLM: `except` ampi con solo `pass`, import duplicati, funzioni troppo lunghe e condizioni statiche come `if True:`.

Allineato alla guida Lab di ai riparo:

**[Analisi statica con AST: trovare i pattern ridondanti dell'IA in Python](https://airiparo.it/lab/analisi-statica-ast-pattern-ridondanti-ia/)**

## Caratteristiche

- Sola lettura: legge i file con `read_text` e stampa un report, **non** modifica nulla
- `ast.parse()` **non esegue** il codice analizzato
- Nessuna dipendenza esterna: solo `ast`, `argparse`, `pathlib`
- Accetta un singolo file `.py` oppure una cartella (scansione ricorsiva di `*.py`)
- Nessuna connessione di rete, nessuna telemetria
- Licenza **MIT**

## Requisiti

- Python **3.9+** (testato con Python 3.12)
- Nessun `pip install`
- Windows, macOS o Linux

## Installazione

### Opzione 1 — Clona il repository

```bash
git clone https://github.com/lunoffice/analisi-statica-ast-pattern-ridondanti-ia.git
cd analisi-statica-ast-pattern-ridondanti-ia
```

### Opzione 2 — Solo lo script

Scarica `ai_code_detector.py` dalla [release/pagina del repo](https://github.com/lunoffice/analisi-statica-ast-pattern-ridondanti-ia) oppure dalla scheda download su ai riparo (stesso SHA-256):

[Download verificato su ai riparo](https://airiparo.it/lab/analisi-statica-ast-pattern-ridondanti-ia/)

## Uso

```bash
# un singolo file
python ai_code_detector.py demo.py

# un'intera cartella (ricorsiva)
python ai_code_detector.py mio_progetto/
```

Su macOS/Linux, se serve: `python3 ai_code_detector.py …`.

### Esempio di output

```text
--- Scansione completata su 1 file ---
demo.py:3 -> Import duplicato trovato: 'os'
demo.py:6 -> Funzione monstre 'calcola_tutto' (52 righe). Valuta il refactoring.
demo.py:53 -> Condizione statica trovata (if True:). Rimasuglio di debug?
demo.py:57 -> Segnalazione: 'except' ampio con solo pass (silenzioso)

Totale segnalazioni: 4
```

## Cosa segnala

| Pattern | Esempio | Priorità suggerita |
| --- | --- | --- |
| `except` ampio con solo `pass` | `except Exception: pass` / `except: pass` | Alta |
| Condizione statica | `if True:` / `if False:` | Alta |
| Import duplicato | `import os` due volte | Media |
| Funzione troppo lunga | più di 50 righe (soglia in `visit_FunctionDef`) | Media |

## Opzioni della CLI

| Argomento | Effetto | Default |
| --- | --- | --- |
| `path` (posizionale) | File `.py` o cartella da scansionare | obbligatorio |
| `-h` / `--help` | Aiuto nativo | — |

## Limiti

- Le segnalazioni sono **indizi**, non prove che il codice sia stato scritto da un'IA: anche le persone lasciano `except: pass`.
- Possono esserci falsi positivi: leggi ogni riga prima di cambiarla.
- Non sostituisce un linter come Ruff né una review umana.
- Un file con errori di sintassi viene segnalato ma non analizzato.

## Checksum

Lo SHA-256 di `ai_code_detector.py` è pubblicato nella scheda download della guida Lab (deve coincidere con il file di questo repository).

## Licenza

MIT — Copyright (c) 2026 Alex Lunalbi (ai riparo)
