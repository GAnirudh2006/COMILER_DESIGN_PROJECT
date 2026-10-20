# GenomeDSL: Professor Demonstration & Evaluation Guide

**Course:** BCSE307P – Compiler Design Lab  
**Project:** GenomeDSL: A Domain-Specific Programming Language for DNA, RNA and Protein Sequence Analysis  
**Institution:** VIT Vellore (Academic Year 2026–2027)  

This guide provides a rapid, structured 7-step sequence for demonstrating the project to your faculty guide (Prof. Nithya K) and external lab evaluators.

---

## 5-Minute Demonstration Script

### Step 1: Automated Demonstration & Pipeline Overview (1 min)

Run the comprehensive built-in demonstration:

```powershell
python -m genomedsl.cli demo
```

**Talking Points for Evaluator:**
- "GenomeDSL accepts biological sequence scripts and passes them through a 5-phase compiler pipeline: Lexer $\rightarrow$ Earley/LALR Parser $\rightarrow$ Semantic Biological Type Checker $\rightarrow$ AST Optimizer $\rightarrow$ Python/Biopython Runtime."
- "Unlike standard Python or Biopython scripts where DNA, RNA, and Protein are untyped strings, GenomeDSL treats them as first-class biological types and performs static semantic verification before any code is executed."

---

### Step 2: Demonstrating the Central Dogma Pipeline (1 min)

Execute the standard Central Dogma script:

```powershell
python -m genomedsl.cli run examples/01_basic_pipeline.gdsl
```

**What the Evaluator Observes:**
- DNA declaration: `gene = "ATGCGTACCGTA"`
- Transcription to RNA: `transcribe(gene)` $\rightarrow$ `"AUGCGUACCGUA"`
- Translation to Protein: `translate(rna1)` $\rightarrow$ `"MRTV"` (Methionine-Arginine-Threonine-Valine)
- Reverse Complement: `reverse_complement(gene)` $\rightarrow$ `"TACGGTACGCAT"`
- GC Content: `gc_content(gene)` $\rightarrow$ `50.0%`

---

### Step 3: Demonstrating Domain-Aware Semantic Errors (1 min)

Demonstrate that GenomeDSL rejects biological errors at compile-time:

#### A. Biological Alphabet Violation
```powershell
python -m genomedsl.cli run examples/04_error_invalid_dna.gdsl
```
**Output:**
```
[AlphabetError] [line 4, column 1]: Invalid DNA base 'U'. DNA sequences only accept bases: A, T, G, C
```
**Point to Highlight:** "General Python scripts only crash when a tool fails downstream. Our semantic analyzer checks literal alphabets immediately during AST traversal."

#### B. Biological Type Mismatch (Illegal Transcription)
```powershell
python -m genomedsl.cli run examples/05_error_type_mismatch.gdsl
```
**Output:**
```
[BiologicalTypeError] [line 5, column 29]: transcribe() requires DNA sequence, got 'RNA'
```
**Point to Highlight:** "The compiler knows that `transcribe()` is biologically defined only for DNA. Passing RNA or Protein is rejected at compile-time."

#### C. Undeclared Identifier Check
```powershell
python -m genomedsl.cli run examples/06_error_undeclared.gdsl
```
**Output:**
```
[SemanticError] [line 3, column 22]: Variable 'unregistered_gene' is not declared before use
```

---

### Step 4: Demonstrating the AST Optimizer (1 min)

Inspect AST transformations and constant folding:

```powershell
python -m genomedsl.cli optimize examples/03_optimization_demo.gdsl
```

**What the Evaluator Observes:**
- The compiler detects `gc_content("ATGCGTAC")` with a static string literal and evaluates it at compile-time, replacing the function call node with a `Literal(FLOAT: 50.0)` in the AST.
- Constant variables are propagated and tracked in `optimizer.constant_env`.

---

### Step 5: Demonstrating Visualization Output (30 sec)

Run the GC content analysis script:

```powershell
python -m genomedsl.cli run examples/02_gc_analysis.gdsl
```

Open the generated chart in `evidence/gc_profile.png`:
- Dual-panel layout:
  1. Top panel: Sliding-window GC% profile across sequence coordinates (window=10bp) with dashed red line at average GC (50.9%).
  2. Bottom panel: Nucleotide frequency bar chart (A=14, T=14, G=14, C=15).

---

### Step 6: Demonstrating Automated Test Suite (30 sec)

Run the core test suite:

```powershell
pytest tests/test_lexer_parser.py tests/test_semantic_analyzer.py tests/test_optimizer.py tests/test_backend.py tests/test_e2e.py
```

**Result:** All 26 tests pass in ~1.2 seconds, proving the stability of the entire core architecture.

---

### Step 7: Explaining the 75% vs 25% Allocation & Live Student Defense (1 min)

Explain your independent contribution:
- **Core Implemented (75%):** Lexer, Earley Parser, AST Builder, Symbol Table, Semantic Type Checker for DNA/RNA, Biopython Backend Runtime, Matplotlib Visualizer, and CLI Driver.
- **Student Contribution (25%):**
  1. Protein alphabet validation (`_validate_protein_alphabet` in `semantic_analyzer.py`).
  2. Sequence comparison type check and similarity identity calculation (`_student_compare_sequences` in `backend.py`).
  3. 1-based motif search with overlap detection (`_student_find_motif` in `backend.py`).
  4. AST Reversible Operation Reduction rule (`_simplify_reversible_calls` in `optimizer.py`).
- Show the student tests:
  ```powershell
  pytest tests/test_student_zone.py
  ```
  Demonstrate that these features are cleanly scaffolded, genuinely pending, and pass as you implement each task.
