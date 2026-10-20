# GenomeDSL: Domain-Specific Programming Language for Biological Sequence Analysis

**Course:** BCSE307P – Compiler Design Lab  
**Institution:** School of Computer Science and Engineering, VIT Vellore  
**Academic Year:** 2026–2027  
**Authors:** G Anirudh (24BDS0335), Abhishek Kothari (24BCE2610)  
**Faculty Guide:** Prof. Nithya K  

---

## 1. Project Overview

**GenomeDSL** is a domain-specific compiler and programming language specifically designed for DNA, RNA, and protein sequence analysis. While standard bioinformatics tools rely on general-purpose languages (such as Python with Biopython), they treat biological sequences as ordinary strings without compile-time domain checks.

In **GenomeDSL**, `DNA`, `RNA`, and `Protein` are **first-class types enforced before execution**. The compiler detects biological errors—such as assigning uracil (`U`) to DNA, transcribing RNA, or translating DNA directly—at compile-time during semantic analysis.

---

## 2. Compiler Architecture & Pipeline

GenomeDSL is organized into a clean 5-phase compiler pipeline:

```
[ GenomeDSL Source (.gdsl) ]
            │
            ▼
┌──────────────────────────┐
│ Phase 1: Lexer & Parser  │  Lark EBNF grammar -> Parse Tree -> AST Transformer
└──────────────────────────┘
            │
            ▼
┌──────────────────────────┐
│ Phase 2: Semantic Check  │  Symbol Table + Biological Type & Alphabet Verification
└──────────────────────────┘
            │
            ▼
┌──────────────────────────┐
│ Phase 3: AST Optimizer   │  Constant Folding & Reversible Operation Reduction
└──────────────────────────┘
            │
            ▼
┌──────────────────────────┐
│ Phase 4: Python Backend  │  Biopython runtime execution (transcribe, translate, etc.)
└──────────────────────────┘
            │
            ▼
┌──────────────────────────┐
│ Phase 5: Visualization   │  Matplotlib GC-content sliding window & composition charts
└──────────────────────────┘
```

---

## 3. Technology Stack

- **Language:** Python 3.9+ (tested on Python 3.13)
- **Parser Generator:** Lark (Earley/LALR parser with position propagation)
- **AST Representation:** Python `dataclasses`
- **Biological Execution Engine:** Biopython (`Bio.Seq`, `Bio.SeqUtils`)
- **Plotting & Visualization:** Matplotlib (using `Agg` headless backend)
- **Testing Framework:** Pytest

---

## 4. Setup & Installation

Clone or navigate to the project directory:

```powershell
cd "C:\Users\G Anirudh\.gemini\antigravity\scratch\genomedsl"
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

---

## 5. Usage & CLI Commands

GenomeDSL provides a command-line interface with subcommands:

### Run a GenomeDSL Program:
```powershell
python -m genomedsl.cli run examples/01_basic_pipeline.gdsl
```

### Type-Check a Script without Execution:
```powershell
python -m genomedsl.cli check examples/01_basic_pipeline.gdsl
```

### Inspect the Abstract Syntax Tree (AST):
```powershell
python -m genomedsl.cli ast examples/01_basic_pipeline.gdsl
```

### Inspect AST Optimization (Constant Folding & Reductions):
```powershell
python -m genomedsl.cli optimize examples/03_optimization_demo.gdsl
```

### Run Interactive Streamlit Web Workbench:
```powershell
streamlit run genomedsl_app.py
```
*Opens an interactive browser-based IDE, compiler pipeline visualizer, and AST inspector.*
*For sharing with teammates and deploying to Streamlit Community Cloud, see [DEPLOYMENT_GUIDE.md](file:///C:/Users/G%20Anirudh/.gemini/antigravity/scratch/genomedsl/DEPLOYMENT_GUIDE.md).*

### Run Full Live Demonstration:
```powershell
python -m genomedsl.cli demo
```

---

## 6. Language Syntax & Example Program

```gdsl
# Example: Central Dogma Pipeline in GenomeDSL
DNA gene = "ATGCGTACCGTA"
RNA transcript = transcribe(gene)
Protein peptide = translate(transcript)
DNA rc = reverse_complement(gene)
RESULT gc = gc_content(gene)

PRINT "DNA:               ", gene
PRINT "Transcribed RNA:   ", transcript
PRINT "Translated Protein:", peptide
PRINT "Reverse Complement:", rc
PRINT "GC Content (%):    ", gc

# Visualizes sliding-window GC% curve and base composition
PLOT gc_content(gene)
```

### Compiler Diagnostic Examples:

**Invalid DNA Alphabet (Compile-Time Rejection):**
```gdsl
DNA bad = "AUGC"
# Output: [AlphabetError] [line 1, column 1]: Invalid DNA base 'U'. DNA sequences only accept bases: A, T, G, C
```

**Biological Type Mismatch (Compile-Time Rejection):**
```gdsl
RNA r = "AUGC"
RNA err = transcribe(r)
# Output: [BiologicalTypeError] [line 2, column 11]: transcribe() requires DNA sequence, got 'RNA'
```

---

## 7. Running the Test Suite

Run the full automated test suite:
```powershell
pytest
```

Run specific test modules:
```powershell
pytest tests/test_lexer_parser.py
pytest tests/test_semantic_analyzer.py
pytest tests/test_optimizer.py
pytest tests/test_backend.py
pytest tests/test_e2e.py
```

Run student zone tests (showing reserved pending tasks):
```powershell
pytest tests/test_student_zone.py
```

---

## 8. Project Structure

```
genomedsl/
├── README.md                          # Project documentation
├── IMPLEMENTATION_REPORT.md           # Engineering decisions & Traceability Matrix
├── STUDENT_CONTRIBUTION_GUIDE.md      # 25% Reserved Work guide & viva prep
├── PROFESSOR_DEMO_GUIDE.md            # Live presentation & demonstration flow
├── VIVA_PREPARATION.md                # Comprehensive viva questions & answers
├── requirements.txt                   # Dependency manifest
├── pyproject.toml                     # Package & test configuration
├── genomedsl/
│   ├── __init__.py
│   ├── grammar.py                     # Lark EBNF grammar
│   ├── ast_nodes.py                   # Dataclass AST definitions
│   ├── parser.py                      # Lexing, parsing, and AST Transformer
│   ├── symbol_table.py                # Biological type symbol table
│   ├── errors.py                      # Compiler error hierarchy with line/col
│   ├── semantic_analyzer.py           # Biological type checking & alphabet checks
│   ├── optimizer.py                   # Constant folding & reversible reduction
│   ├── backend.py                     # Biopython execution runtime
│   ├── visualizer.py                  # Matplotlib sliding window GC plots
│   ├── cli.py                         # Command-line driver
│   ├── demo.py                        # Automated demonstration runner
│   └── student_reference_solution.py  # Reference implementations for student tasks
├── examples/
│   ├── 01_basic_pipeline.gdsl         # Valid central dogma pipeline
│   ├── 02_gc_analysis.gdsl            # GC content calculation & PLOT
│   ├── 03_optimization_demo.gdsl      # Constant folding & reversible cancellation
│   ├── 04_error_invalid_dna.gdsl      # Compile-time AlphabetError demo
│   ├── 05_error_type_mismatch.gdsl    # Compile-time BiologicalTypeError demo
│   ├── 06_error_undeclared.gdsl       # Compile-time SemanticError demo
│   └── 07_student_challenge.gdsl      # Exercises student reserved features
├── tests/
│   ├── test_lexer_parser.py           # Lexer and parser tests
│   ├── test_semantic_analyzer.py      # Semantic type checking tests
│   ├── test_optimizer.py              # Constant folding tests
│   ├── test_backend.py                # Biopython runtime tests
│   ├── test_e2e.py                    # End-to-end integration tests
│   └── test_student_zone.py           # 25% student reserved work tests
└── evidence/
    ├── gc_profile.png                 # Generated Matplotlib dual-panel plot
    └── EXECUTION_LOGS.md              # Real verified execution outputs
```
