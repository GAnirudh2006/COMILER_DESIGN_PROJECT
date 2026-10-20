# GenomeDSL: Student Contribution Guide (25% Reserved Work)

This guide documents the **25% reserved engineering work** allocated for you to complete, test, and defend before your faculty guide and external examiner.

All foundational infrastructure (Lexer, Parser, AST Builder, Symbol Table, Core Semantic Type Checker, Constant Folder, Backend Execution Engine, and Visualization) is fully operational. Your tasks add key biological logic and compiler rewrite rules into clearly marked extension points.

---

## Overview of Reserved Tasks

| Task # | Feature Description | Target File & Function | Test Command |
| :--- | :--- | :--- | :--- |
| **Task 1** | Protein Alphabet Validation | `genomedsl/semantic_analyzer.py`<br>`_validate_protein_alphabet()` | `pytest tests/test_student_zone.py -k task1` |
| **Task 2** | Sequence Similarity Metric | `genomedsl/backend.py`<br>`_student_compare_sequences()` | `pytest tests/test_student_zone.py -k task2` |
| **Task 3** | Motif Search with Overlaps | `genomedsl/backend.py`<br>`_student_find_motif()` | `pytest tests/test_student_zone.py -k task3` |
| **Task 4** | Reversible AST Operation Cancellation | `genomedsl/optimizer.py`<br>`_simplify_reversible_calls()` | `pytest tests/test_student_zone.py -k task4` |

A complete reference implementation for all 4 tasks is provided in `genomedsl/student_reference_solution.py` for your self-study.

---

## Task 1: Protein Alphabet Validation

### 1. Concepts to Understand
- **Standard Amino Acid Alphabet:** In molecular biology, standard proteins are composed of 20 amino acids represented by single-letter codes:
  $$A, C, D, E, F, G, H, I, K, L, M, N, P, Q, R, S, T, V, W, Y$$
  plus the stop codon marker (`*`).
- **Compiler Principle:** Characters outside this set (such as `B`, `J`, `O`, `U`, `X`, `Z` or numbers/symbols) are biologically invalid for standard translated proteins and must trigger an `AlphabetError` during semantic analysis.

### 2. Relevant File & Function
- **File:** `genomedsl/semantic_analyzer.py`
- **Function:** `def _validate_protein_alphabet(self, seq: str, line: Optional[int], column: Optional[int]) -> None:`

### 3. Implementation Steps
1. Open `genomedsl/semantic_analyzer.py`.
2. Locate `_validate_protein_alphabet()`. Replace the `raise NotImplementedError(...)` with:
   ```python
   for char in seq:
       if char not in STANDARD_PROTEIN_ALPHABET:
           raise AlphabetError(
               f"Invalid amino acid '{char}'. Protein sequences only accept standard amino acid single-letter codes",
               line=line,
               column=column,
           )
   ```
3. Save the file and run the test:
   ```powershell
   pytest tests/test_student_zone.py -k task1
   ```

### 4. Edge Cases & Debugging
- Case sensitivity: `seq` is normalized to uppercase before checking.
- Stop codon: verify that `'*'` is accepted since `translate()` can produce stop codons.

---

## Task 2: Sequence Similarity Metric (`compare` / `similarity`)

### 1. Concepts to Understand
- **Identity Metric:** Compares two aligned or equal-length sequences position by position (Hamming match):
  $$\text{Similarity (\%)} = \left(\frac{\text{matching residues}}{\max(\text{len}(s_1), \text{len}(s_2))}\right) \times 100$$
- **Semantic Type Check:** Already implemented in `semantic_analyzer.py` (`_check_sequence_comparison_semantics`). It rejects comparing sequences of different biological types (e.g. DNA vs RNA).

### 2. Relevant File & Function
- **File:** `genomedsl/backend.py`
- **Function:** `def _student_compare_sequences(self, seq1: str, seq2: str) -> float:`

### 3. Implementation Steps
1. Open `genomedsl/backend.py`.
2. Locate `_student_compare_sequences()`. Replace the `raise NotImplementedError(...)` with:
   ```python
   if not seq1 and not seq2:
       return 100.0
   max_len = max(len(seq1), len(seq2))
   if max_len == 0:
       return 0.0
   min_len = min(len(seq1), len(seq2))
   matches = sum(1 for a, b in zip(seq1[:min_len], seq2[:min_len]) if a == b)
   return round((matches / max_len) * 100.0, 2)
   ```
3. Save the file and run the test:
   ```powershell
   pytest tests/test_student_zone.py -k task2
   ```

---

## Task 3: 1-Based Motif Search with Overlaps (`find_motif`)

### 1. Concepts to Understand
- **Biological Coordinates:** Biologists count sequence positions starting at 1 (1-based coordinate system), whereas Python strings use 0-based indices. Your function must return 1-based indices.
- **Overlapping Motifs:** If searching for `"AAA"` in `"AAAA"`, there are two matches (at index 1 and index 2). A naive `str.split()` or step jump will miss the second match. You must advance by 1 character after each match.

### 2. Relevant File & Function
- **File:** `genomedsl/backend.py`
- **Function:** `def _student_find_motif(self, sequence: str, motif: str) -> List[int]:`

### 3. Implementation Steps
1. Open `genomedsl/backend.py`.
2. Locate `_student_find_motif()`. Replace the `raise NotImplementedError(...)` with:
   ```python
   if not motif or not sequence:
       return []
   positions = []
   pos = sequence.find(motif, 0)
   while pos != -1:
       positions.append(pos + 1)  # Convert 0-based to 1-based
       pos = sequence.find(motif, pos + 1)  # Advance by 1 to support overlaps
   return positions
   ```
3. Save the file and run the test:
   ```powershell
   pytest tests/test_student_zone.py -k task3
   ```

---

## Task 4: Reversible Operation AST Cancellation

### 1. Concepts to Understand
- **Algebraic AST Optimization:** In biology, reversing a sequence twice restores the original sequence:
  $$\text{reverse}(\text{reverse}(x)) \equiv x$$
  Similarly, for DNA/RNA double-stranded complements:
  $$\text{reverse\_complement}(\text{reverse\_complement}(x)) \equiv x$$
- **Compiler Pass:** Rather than evaluating this at runtime, the compiler's optimizer detects this pattern in the AST during the optimization pass and replaces the outer `FunctionCall` directly with the innermost expression $x$.

### 2. Relevant File & Function
- **File:** `genomedsl/optimizer.py`
- **Function:** `def _simplify_reversible_calls(self, call: FunctionCall) -> Expr:`

### 3. Implementation Steps
1. Open `genomedsl/optimizer.py`.
2. Locate `_simplify_reversible_calls()`. Replace the body with:
   ```python
   if call.name in ("reverse", "reverse_complement") and len(call.args) == 1:
       inner = call.args[0]
       if isinstance(inner, FunctionCall) and inner.name == call.name and len(inner.args) == 1:
           self.stats["reversible_reductions"] += 1
           return inner.args[0]
   return call
   ```
3. Save the file and run the test:
   ```powershell
   pytest tests/test_student_zone.py -k task4
   ```

---

## Verifying All 4 Tasks Together

Once you have completed all four tasks, run:

```powershell
pytest tests/test_student_zone.py
```

All 7 student tests should pass cleanly!

Then execute the student demonstration challenge:

```powershell
python -m genomedsl.cli run examples/07_student_challenge.gdsl
```

Expected Output:
```
[GenomeDSL OUT] Insulin A-chain:    GIVEQCCTSICSLYQLENYCN
[GenomeDSL OUT] Sequence Similarity (%): 87.5
[GenomeDSL OUT] Motif 'TAC' Coordinates : [6]
```
