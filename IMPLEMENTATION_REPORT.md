# GenomeDSL: Implementation Report & Requirements Traceability Matrix

**Course:** BCSE307P – Compiler Design Lab  
**Institution:** School of Computer Science and Engineering, VIT Vellore  
**Academic Year:** 2026–2027  
**Project Title:** GenomeDSL: A Domain-Specific Programming Language for DNA, RNA and Protein Sequence Analysis  
**Authors:** G Anirudh (24BDS0335), Abhishek Kothari (24BCE2610)  
**Faculty Guide:** Prof. Nithya K  

---

## 1. Problem Statement & Motivation

In bioinformatics, sequence processing is traditionally carried out using general-purpose languages (such as Python, Perl, or R) coupled with domain libraries (such as Biopython or BioPerl). While powerful, general-purpose languages treat biological sequences as generic text strings. A programmer can inadvertently assign an invalid base (e.g. uracil `U` in DNA) or attempt biologically invalid operations (e.g. transcribing an RNA sequence or calculating the GC content of a protein). Such errors are only discovered downstream during execution or produce silent scientific errors.

**GenomeDSL** solves this by establishing a domain-specific compiler where:
1. `DNA`, `RNA`, and `Protein` are first-class, strictly enforced types.
2. Sequence alphabets are validated at compile-time before any backend execution is initiated.
3. Operations follow biological rules: transcription requires `DNA` and yields `RNA`; translation requires `RNA` and yields `Protein`; reverse complement and GC-content are restricted to nucleic acids.
4. An AST optimizer simplifies biological expressions through constant folding and algebraic reductions (e.g. `reverse(reverse(x))` $\rightarrow$ `x`).
5. A high-level backend delegates trusted operations to Biopython and produces publication-quality charts using Matplotlib.

---

## 2. Requirements Traceability Matrix (RTM)

| Req ID | Description & PDF Source | Priority | Dependencies | Planned Implementation | Verification Method | Allocation | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **REQ-01** | EBNF Grammar & Lexical Specification (PDF p.4, 6, 8, 9) | High | None | Lark grammar defining statements, functions, literals, and keywords | Automated Lark unit tests | **AI (Core)** | **Completed & Verified** |
| **REQ-02** | AST Dataclass Representation & Transformer (PDF p.4, 8, 10) | High | REQ-01 | Python dataclasses (`Program`, `VarDecl`, `AssignStmt`, `FunctionCall`, etc.) | `test_lexer_parser.py` (6 tests) | **AI (Core)** | **Completed & Verified** |
| **REQ-03** | Symbol Table & Scoping (PDF p.4, 6, 8, 10) | High | REQ-02 | Dictionary-based `SymbolTable` with biological types and location tracking | Semantic duplicate/lookup tests | **AI (Core)** | **Completed & Verified** |
| **REQ-04** | Biological Alphabet Validation for DNA & RNA (PDF p.4, 6, 8, 9) | High | REQ-03 | Strict validation: DNA $\in \{A, T, G, C\}$, RNA $\in \{A, U, G, C\}$ | `test_semantic_analyzer.py` (10 tests) | **AI (Core)** | **Completed & Verified** |
| **REQ-05** | Biological Alphabet Validation for Protein (PDF p.6, 9) | Medium | REQ-03 | Verify sequence contains only standard 20 amino acid codes + `'*'` | `test_student_zone.py` (Task 1) | **Student (25%)** | **Scaffolded (Pending Student)** |
| **REQ-06** | Strict Type Checking for Core Operations (PDF p.4, 6, 8, 9) | High | REQ-03 | Enforce `transcribe` $\rightarrow$ DNA, `translate` $\rightarrow$ RNA, `reverse_complement` $\rightarrow$ DNA | `test_semantic_analyzer.py` | **AI (Core)** | **Completed & Verified** |
| **REQ-07** | Biological Type Checking for Sequence Comparison (PDF p.4, 8) | Medium | REQ-06 | Verify `compare(s1, s2)` has matching biological types | `test_student_zone.py` (Task 2A) | **Student (25%)** | **Scaffolded & Verified** |
| **REQ-08** | AST Optimizer: Constant Expression Folding (PDF p.4, 6, 8, 9) | Medium | REQ-02 | Fold static calls like `gc_content("ATGC")` $\rightarrow 50.0$, `transcribe("ATGC")` $\rightarrow "AUGC"$ | `test_optimizer.py` (3 tests) | **AI (Core)** | **Completed & Verified** |
| **REQ-09** | AST Optimizer: Reversible Operation Cancellation (PDF p.4, 6, 8, 9) | Medium | REQ-08 | Simplify `reverse(reverse(x))` $\rightarrow x$ and `reverse_complement(reverse_complement(x))` $\rightarrow x$ | `test_student_zone.py` (Task 4) | **Student (25%)** | **Scaffolded (Pending Student)** |
| **REQ-10** | Execution Backend & Runtime Environment (PDF p.4, 6, 8, 10) | High | REQ-02 | Sequential AST interpreter managing variable environment and standard output | `test_backend.py` (2 tests) | **AI (Core)** | **Completed & Verified** |
| **REQ-11** | Core Biological Operations via Biopython (PDF p.4, 6, 8, 10) | High | REQ-10 | Biopython integration for `transcribe`, `translate`, `reverse_complement`, and GC fraction | `test_backend.py`, `test_e2e.py` | **AI (Core)** | **Completed & Verified** |
| **REQ-12** | Sequence Similarity Metric Calculation (PDF p.4, 8) | Medium | REQ-10 | Calculate percentage match identity between sequences: `(matches / max_len) * 100` | `test_student_zone.py` (Task 2B) | **Student (25%)** | **Scaffolded (Pending Student)** |
| **REQ-13** | 1-Based Motif Search with Overlaps (PDF p.4, 6, 9) | Medium | REQ-10 | Search sequence for motif substrings and return 1-based start coordinates | `test_student_zone.py` (Task 3) | **Student (25%)** | **Scaffolded (Pending Student)** |
| **REQ-14** | Visualization & Matplotlib Graphics (PDF p.4, 6, 8, 9, 10) | Medium | REQ-10 | Dual-panel plot of sliding-window GC% profile and nucleotide composition bar chart | Visual check of `evidence/gc_profile.png` | **AI (Core)** | **Completed & Verified** |
| **REQ-15** | Unified Command Line Interface & Runner (PDF p.8, 10) | High | REQ-10 | `genomedsl` CLI supporting `run`, `check`, `ast`, `optimize`, and `demo` | Terminal execution of all subcommands | **AI (Core)** | **Completed & Verified** |
| **REQ-16** | End-to-End Test Suite & Verification (PDF p.6, 10) | High | All | Comprehensive test harness executing `.gdsl` programs and verifying error handling | `pytest` (26 core passing tests) | **AI (Core)** | **Completed & Verified** |

---

## 3. Work Allocation Breakdown

### Part A — Core Infrastructure & Implemented Functionality (~75%)
1. **Lark Lexer and Parser (`genomedsl/grammar.py`, `genomedsl/parser.py`)**: Complete EBNF grammar, token definitions, and robust parser capturing line/column information.
2. **Abstract Syntax Tree (`genomedsl/ast_nodes.py`)**: Dataclass-based node hierarchy with integrated `pretty()` printer for AST inspection.
3. **Symbol Table (`genomedsl/symbol_table.py`)**: Dictionary-backed symbol registry tracking variable names, biological types, and scope.
4. **Semantic Type Checking & Alphabet Validation (`genomedsl/semantic_analyzer.py`)**: Strict biological type enforcement for `DNA` and `RNA`, error reporting for alphabet violations and type mismatches (`transcribe`, `translate`, `reverse_complement`, `gc_content`).
5. **AST Constant Folding Optimizer (`genomedsl/optimizer.py`)**: Constant expression folding for literal sequence calculations and constant propagation.
6. **Execution Backend (`genomedsl/backend.py`)**: Biopython execution runtime managing sequence transformations, memory environments, and formatted stdout.
7. **Visualization Module (`genomedsl/visualizer.py`)**: Matplotlib dual-panel plotting module generating sliding-window GC curves and composition bar charts.
8. **Command Line Interface & Demo (`genomedsl/cli.py`, `genomedsl/demo.py`)**: Full CLI toolchain with subcommands and automated demonstration suite.
9. **Core Test Harness (`tests/test_*.py`)**: 26 automated unit and end-to-end regression tests verifying all core requirements.

### Part B — Student Implementation Zone (~25%)
Intentionally reserved for independent completion, testing, and viva defense:
1. **Task 1: Protein Alphabet Validation** in `genomedsl/semantic_analyzer.py` (`_validate_protein_alphabet`).
2. **Task 2: Sequence Comparison Semantics & Similarity Calculation** in `genomedsl/semantic_analyzer.py` and `genomedsl/backend.py` (`_student_compare_sequences`).
3. **Task 3: 1-Based Motif Search with Overlap Handling** in `genomedsl/backend.py` (`_student_find_motif`).
4. **Task 4: Reversible Operation AST Cancellation** in `genomedsl/optimizer.py` (`_simplify_reversible_calls`).

---

## 4. Architectural Verification Evidence

All 26 core tests pass without error:
- Lexer & Parser: 6 passed
- Semantic Analyzer: 10 passed
- AST Optimizer: 3 passed
- Execution Backend: 2 passed
- End-to-End Integration: 5 passed

The graphical visualization artifact (`evidence/gc_profile.png`) has been verified and rendered using Matplotlib's `Agg` engine.
