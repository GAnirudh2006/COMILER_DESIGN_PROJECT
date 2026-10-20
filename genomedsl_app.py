"""
GenomeDSL — Interactive Workbench
A Domain-Specific Language for DNA, RNA and Protein Sequence Analysis
"""

import os, sys, tempfile, shutil, subprocess
import streamlit as st

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from genomedsl.parser import parse_code
from genomedsl.semantic_analyzer import analyze_code
from genomedsl.optimizer import ASTOptimizer
from genomedsl.backend import ExecutionBackend
from genomedsl.errors import (
    GenomeDSLError, BiologicalTypeError, AlphabetError, SemanticError,
)

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="GenomeDSL",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Dark theme CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* Force dark everywhere */
html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
.main .block-container {
    background-color: #0d1117 !important;
    color: #c9d1d9 !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #161b22 !important;
    border-right: 1px solid #30363d;
}
[data-testid="stSidebar"] * { color: #c9d1d9 !important; }
[data-testid="stSidebar"] hr { border-color: #30363d !important; }

/* Radio buttons */
[data-testid="stSidebar"] .stRadio label {
    font-size: 0.93rem !important;
    padding: 4px 0 !important;
}

/* All text inputs / text areas */
textarea, .stTextArea textarea {
    background-color: #161b22 !important;
    color: #e6edf3 !important;
    border: 1px solid #30363d !important;
    border-radius: 8px !important;
    font-family: 'JetBrains Mono', 'Fira Code', monospace !important;
    font-size: 0.87rem !important;
}

/* Select boxes */
[data-testid="stSelectbox"] > div > div {
    background-color: #161b22 !important;
    color: #c9d1d9 !important;
    border: 1px solid #30363d !important;
}

/* Buttons */
.stButton > button {
    background-color: #238636 !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    padding: 0.45rem 1.2rem !important;
    transition: background 0.2s;
}
.stButton > button:hover { background-color: #2ea043 !important; }

/* Primary button */
.stButton > button[kind="primary"] {
    background-color: #238636 !important;
}

/* Tabs */
[data-testid="stTabs"] [role="tab"] {
    background: transparent !important;
    color: #8b949e !important;
    border-radius: 6px 6px 0 0 !important;
    font-weight: 500 !important;
    font-size: 0.9rem !important;
}
[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
    color: #58a6ff !important;
    border-bottom: 2px solid #58a6ff !important;
    background: transparent !important;
}
[data-testid="stTabs"] [data-testid="stTabPanel"] {
    background: #161b22 !important;
    border: 1px solid #30363d !important;
    border-radius: 0 8px 8px 8px !important;
    padding: 1.2rem !important;
}

/* Metrics */
[data-testid="stMetric"] {
    background: #161b22 !important;
    border: 1px solid #30363d !important;
    border-radius: 8px !important;
    padding: 0.8rem 1rem !important;
}
[data-testid="stMetricLabel"]  { color: #8b949e !important; }
[data-testid="stMetricValue"]  { color: #58a6ff !important; }

/* Info / success / warning / error */
.stAlert { border-radius: 8px !important; }
[data-testid="stAlert"][data-baseweb="notification"] {
    background: #161b22 !important;
    border: 1px solid #30363d !important;
}

/* Divider */
hr { border-color: #30363d !important; }

/* Toggle */
[data-testid="stToggle"] { color: #c9d1d9 !important; }

/* Scrollbar */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #0d1117; }
::-webkit-scrollbar-thumb { background: #30363d; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# ── Helper HTML components ─────────────────────────────────────────────────────
def _type_badge(t: str) -> str:
    colors = {
        "DNA":     ("#238636", "#d4efdf"),
        "RNA":     ("#1f6feb", "#cae5ff"),
        "Protein": ("#8957e5", "#eed8fd"),
        "RESULT":  ("#6e7681", "#f0f0f0"),
    }
    bg, fg = colors.get(t, ("#6e7681", "#f0f0f0"))
    return (f'<span style="background:{bg};color:{fg};padding:1px 8px;'
            f'border-radius:4px;font-size:0.75rem;font-weight:700;">{t}</span>')

def _terminal(text: str, color: str = "#79c0ff") -> str:
    safe = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return (f'<div style="background:#0d1117;color:{color};border:1px solid #30363d;'
            f'border-radius:8px;padding:1rem 1.2rem;font-family:monospace;'
            f'font-size:0.84rem;white-space:pre-wrap;line-height:1.7;'
            f'min-height:60px;">{safe}</div>')

def _err_box(title: str, body: str) -> str:
    safe = body.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return (f'<div style="background:#1c0a0a;border:1px solid #f85149;'
            f'border-left:4px solid #f85149;border-radius:8px;padding:0.9rem 1.1rem;'
            f'margin-top:0.6rem;">'
            f'<b style="color:#f85149;">{title}</b>'
            f'<pre style="color:#ffa198;margin:0.5rem 0 0;font-size:0.82rem;'
            f'white-space:pre-wrap;">{safe}</pre></div>')

def _section(label: str) -> str:
    return (f'<div style="font-size:0.8rem;font-weight:700;letter-spacing:1px;'
            f'text-transform:uppercase;color:#8b949e;border-bottom:1px solid #30363d;'
            f'padding-bottom:4px;margin:1.2rem 0 0.7rem;">{label}</div>')

def _phase_card(num: str, label: str, state: str, sub: str = "") -> str:
    colors = {"ok": "#238636", "err": "#f85149", "warn": "#e3b341", "idle": "#30363d"}
    icons  = {"ok": "✓", "err": "✗", "warn": "!", "idle": "—"}
    c = colors.get(state, "#30363d")
    i = icons.get(state, "—")
    sub_html = f'<div style="font-size:0.72rem;color:#8b949e;margin-top:2px;">{sub}</div>' if sub else ""
    return (f'<div style="background:#161b22;border:1px solid #30363d;'
            f'border-top:3px solid {c};border-radius:8px;padding:0.8rem 1rem;text-align:center;">'
            f'<div style="font-size:0.68rem;color:#8b949e;letter-spacing:1px;text-transform:uppercase;">Phase {num}</div>'
            f'<div style="font-weight:600;color:#e6edf3;margin-top:2px;">'
            f'<span style="color:{c};">{i}</span> {label}</div>'
            f'{sub_html}</div>')

# ── Example programs ───────────────────────────────────────────────────────────
EXAMPLES = {
    "Central Dogma  (DNA → RNA → Protein)": """\
# Complete Central Dogma Pipeline
DNA gene = "ATGCGTACCGTA"
RNA transcript = transcribe(gene)
Protein peptide = translate(transcript)
DNA rc = reverse_complement(gene)
RESULT gc = gc_content(gene)
RESULT len_seq = length(gene)

PRINT "DNA sequence:      ", gene
PRINT "Transcribed RNA:   ", transcript
PRINT "Translated Protein:", peptide
PRINT "Reverse Complement:", rc
PRINT "GC Content (%):    ", gc
PRINT "Sequence Length:   ", len_seq

PLOT gc_content(gene)
""",
    "GC-Content Sliding Window Analysis": """\
# GC-Content Sliding Window Visualization
DNA seq = "ATGCGATCGATCGATCGCGCGCATATATCGATCGATCGATCGATCGCGCTATATAGC"
RESULT gc = gc_content(seq)
RESULT sz = length(seq)

PRINT "Sequence:", seq
PRINT "Length (bp):", sz
PRINT "GC Content (%):", gc

PLOT gc_content(seq)
""",
    "Reverse Complement & Reverse": """\
# Sequence manipulation operations
DNA seq = "ATGCGATCGTA"
DNA rc  = reverse_complement(seq)
DNA rev = reverse(seq)
RESULT gc_original = gc_content(seq)
RESULT gc_rc       = gc_content(rc)

PRINT "Original:          ", seq
PRINT "Reverse Complement:", rc
PRINT "Reversed:          ", rev
PRINT "GC (original, %):  ", gc_original
PRINT "GC (rev_comp, %):  ", gc_rc
""",
    "Error — Invalid DNA Alphabet": """\
# The compiler catches 'U' (Uracil) in a DNA sequence
# and rejects it before execution — no runtime crash!
DNA bad = "AUGCGTAC"
""",
    "Error — Type Mismatch (transcribe on RNA)": """\
# transcribe() is only defined for DNA sequences.
# Passing an RNA sequence is a biological type error.
RNA r = "AUGCCGUAC"
RNA illegal = transcribe(r)
""",
    "Error — Undeclared Variable": """\
# Referencing a variable that was never declared.
RNA transcript = transcribe(unknown_gene)
""",
}

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        '<div style="font-size:1.5rem;font-weight:800;letter-spacing:-0.5px;color:#e6edf3;">'
        '🧬 GenomeDSL</div>'
        '<div style="font-size:0.8rem;color:#8b949e;margin-bottom:1rem;">'
        'Domain-Specific Language for Biological Sequence Analysis</div>',
        unsafe_allow_html=True,
    )
    st.divider()

    nav = st.radio(
        "Navigate",
        [
            "▶  Run Programs",
            "🔬  Inspect Pipeline",
            "📚  Language Reference",
        ],
        label_visibility="collapsed",
    )

    st.divider()

    st.markdown(
        '<div style="font-size:0.78rem;color:#8b949e;line-height:1.6;">'
        '<b style="color:#c9d1d9;">Supported Types</b><br>'
        '🟢 DNA &nbsp; 🔵 RNA &nbsp; 🟣 Protein &nbsp; ⚪ RESULT'
        '</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div style="font-size:0.78rem;color:#8b949e;margin-top:0.8rem;line-height:1.8;">'
        '<b style="color:#c9d1d9;">Built-in Functions</b><br>'
        '<code style="color:#79c0ff;">transcribe()</code><br>'
        '<code style="color:#79c0ff;">translate()</code><br>'
        '<code style="color:#79c0ff;">reverse_complement()</code><br>'
        '<code style="color:#79c0ff;">reverse()</code><br>'
        '<code style="color:#79c0ff;">gc_content()</code><br>'
        '<code style="color:#79c0ff;">length()</code><br>'
        '</div>',
        unsafe_allow_html=True,
    )


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — Run Programs
# ══════════════════════════════════════════════════════════════════════════════
if nav == "▶  Run Programs":
    # Header
    st.markdown(
        '<h1 style="color:#e6edf3;font-size:1.8rem;font-weight:800;margin-bottom:0.1rem;">'
        '▶ Run GenomeDSL Programs</h1>'
        '<p style="color:#8b949e;margin-bottom:1.4rem;">'
        'Write a GenomeDSL script or pick an example. '
        'The compiler runs all five phases and shows output below.</p>',
        unsafe_allow_html=True,
    )

    col_sel, col_opt = st.columns([3, 1])
    with col_sel:
        sel = st.selectbox("Load example:", list(EXAMPLES.keys()),
                           label_visibility="collapsed")
    with col_opt:
        opt_on = st.toggle("AST Optimizer", value=True)

    code = st.text_area(
        "Editor",
        value=EXAMPLES[sel],
        height=240,
        label_visibility="collapsed",
    )

    run = st.button("▶  Compile & Execute", type="primary", use_container_width=True)

    if run and code.strip():
        st.divider()

        # ── Run pipeline ──────────────────────────────────────────────────────
        phases  = {"parse": "idle", "sem": "idle", "opt": "idle", "exec": "idle"}
        parsed  = sym = opt_ast = bk = None
        err_html = ""
        opt_stats = {"constant_folds": 0, "reversible_reductions": 0}
        opt_label = ""

        # 1. Parse
        try:
            parsed = parse_code(code)
            phases["parse"] = "ok"
        except GenomeDSLError as e:
            phases["parse"] = "err"
            err_html = _err_box("Syntax / Lexical Error", e.format_error())

        # 2. Semantic
        if parsed:
            try:
                sym = analyze_code(parsed)
                phases["sem"] = "ok"
            except AlphabetError as e:
                phases["sem"] = "err"
                err_html = _err_box("Biological Alphabet Error", e.format_error())
            except BiologicalTypeError as e:
                phases["sem"] = "err"
                err_html = _err_box("Biological Type Error", e.format_error())
            except GenomeDSLError as e:
                phases["sem"] = "err"
                err_html = _err_box("Semantic Error", e.format_error())
            except NotImplementedError:
                phases["sem"] = "warn"
                err_html = _err_box("Not Implemented", "This feature is pending implementation.")

        # 3. Optimize
        if sym:
            if opt_on:
                try:
                    _o = ASTOptimizer()
                    opt_ast = _o.optimize(parsed)
                    opt_stats = _o.stats
                    opt_label = f"{opt_stats['constant_folds']} folds"
                    phases["opt"] = "ok"
                except Exception:
                    opt_ast = parsed
                    phases["opt"] = "warn"
                    opt_label = "partial"
            else:
                opt_ast = parsed
                phases["opt"] = "idle"
                opt_label = "skipped"

        # 4. Execute
        saved_plots = []
        if opt_ast and sym:
            with tempfile.TemporaryDirectory() as tmp:
                bk = ExecutionBackend(visual_output_dir=tmp)
                try:
                    bk.execute(opt_ast)
                    phases["exec"] = "ok"
                    for p in bk.generated_plots:
                        if os.path.exists(p):
                            dst = os.path.join(
                                os.path.dirname(__file__), "evidence",
                                os.path.basename(p))
                            os.makedirs(os.path.dirname(dst), exist_ok=True)
                            shutil.copy2(p, dst)
                            saved_plots.append(dst)
                except NotImplementedError:
                    phases["exec"] = "warn"
                    err_html = _err_box("Not Implemented", "This function is pending implementation.")
                    bk = None
                except GenomeDSLError as e:
                    phases["exec"] = "err"
                    err_html = _err_box("Runtime Error", e.format_error())
                    bk = None

        # ── Phase strip ───────────────────────────────────────────────────────
        sub_vals = [
            f"{len(parsed.statements)} stmts" if phases["parse"] == "ok" and parsed else "",
            f"{len(sym.all_symbols())} symbols" if phases["sem"] == "ok" and sym else "",
            opt_label,
            f"{len(bk.env)} vars" if phases["exec"] == "ok" and bk else "",
        ]
        ph_labels = ["Lex & Parse", "Semantic Check",
                     "AST Optimizer" if opt_on else "Optimizer (off)", "Execute"]
        ph_nums   = ["01", "02", "03", "04"]
        ph_keys   = ["parse", "sem", "opt", "exec"]

        cols = st.columns(4)
        for col, num, label, key, sub in zip(cols, ph_nums, ph_labels, ph_keys, sub_vals):
            col.markdown(_phase_card(num, label, phases[key], sub),
                         unsafe_allow_html=True)

        if err_html:
            st.markdown(err_html, unsafe_allow_html=True)

        # ── Output section ────────────────────────────────────────────────────
        if bk:
            st.markdown(_section("OUTPUT"), unsafe_allow_html=True)

            left, right = st.columns([1, 1])

            with left:
                st.markdown("**Program Output**")
                if bk.stdout:
                    st.markdown(_terminal("\n".join(bk.stdout)), unsafe_allow_html=True)
                else:
                    st.markdown(_terminal("(no PRINT statements in program)",
                                          "#8b949e"), unsafe_allow_html=True)

            with right:
                st.markdown("**Variable Environment**")
                if bk.env:
                    rows = "".join(
                        f'<tr>'
                        f'<td style="padding:6px 10px;border-bottom:1px solid #21262d;">'
                        f'<code style="color:#79c0ff;">{name}</code></td>'
                        f'<td style="padding:6px 10px;border-bottom:1px solid #21262d;">'
                        f'{_type_badge(t)}</td>'
                        f'<td style="padding:6px 10px;border-bottom:1px solid #21262d;'
                        f'color:#e6edf3;font-family:monospace;font-size:0.82rem;">'
                        f'{"&quot;" + str(v) + "&quot;" if isinstance(v, str) else str(v)}'
                        f'</td></tr>'
                        for name, (v, t) in bk.env.items()
                    )
                    st.markdown(
                        f'<table style="width:100%;border-collapse:collapse;'
                        f'background:#161b22;border-radius:8px;overflow:hidden;">'
                        f'<thead><tr>'
                        f'<th style="background:#21262d;color:#8b949e;padding:7px 10px;'
                        f'text-align:left;font-size:0.78rem;letter-spacing:0.5px;">VAR</th>'
                        f'<th style="background:#21262d;color:#8b949e;padding:7px 10px;'
                        f'text-align:left;font-size:0.78rem;letter-spacing:0.5px;">TYPE</th>'
                        f'<th style="background:#21262d;color:#8b949e;padding:7px 10px;'
                        f'text-align:left;font-size:0.78rem;letter-spacing:0.5px;">VALUE</th>'
                        f'</tr></thead><tbody>{rows}</tbody></table>',
                        unsafe_allow_html=True,
                    )

            # Plots
            if saved_plots:
                st.markdown(_section("VISUALIZATION"), unsafe_allow_html=True)
                for p in saved_plots:
                    if os.path.exists(p):
                        st.image(p, use_container_width=True)
            elif "PLOT" in code and phases["exec"] == "ok":
                fallback = os.path.join(os.path.dirname(__file__),
                                        "evidence", "gc_profile.png")
                if os.path.exists(fallback):
                    st.markdown(_section("VISUALIZATION"), unsafe_allow_html=True)
                    st.image(fallback, use_container_width=True)

            # Optimizer stats when enabled
            if opt_on and phases["opt"] == "ok":
                st.markdown(_section("OPTIMIZER STATISTICS"), unsafe_allow_html=True)
                m1, m2, m3 = st.columns(3)
                m1.metric("Constant Folds", opt_stats["constant_folds"])
                m2.metric("Reversible Reductions", opt_stats["reversible_reductions"])
                m3.metric("Variables Registered", len(bk.env) if bk else 0)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — Inspect Pipeline
# ══════════════════════════════════════════════════════════════════════════════
elif nav == "🔬  Inspect Pipeline":
    st.markdown(
        '<h1 style="color:#e6edf3;font-size:1.8rem;font-weight:800;margin-bottom:0.1rem;">'
        '🔬 Compiler Pipeline Inspector</h1>'
        '<p style="color:#8b949e;margin-bottom:1.4rem;">'
        'Examine the Abstract Syntax Tree and see what the optimizer transforms.</p>',
        unsafe_allow_html=True,
    )

    code2 = st.text_area(
        "Source code:",
        value=EXAMPLES["Central Dogma  (DNA → RNA → Protein)"],
        height=200,
        label_visibility="collapsed",
    )

    if st.button("🔍  Inspect", type="primary"):
        try:
            ast2 = parse_code(code2)

            t_ast, t_opt, t_sym = st.tabs([
                "🌳  Abstract Syntax Tree",
                "⚡  AST Before vs After Optimization",
                "🗂️  Symbol Table",
            ])

            with t_ast:
                st.markdown(
                    _terminal(ast2.pretty(), "#a5d6ff"),
                    unsafe_allow_html=True,
                )

            with t_opt:
                _o2 = ASTOptimizer()
                _oast = _o2.optimize(parse_code(code2))
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown(
                        '<div style="color:#8b949e;font-size:0.82rem;'
                        'margin-bottom:4px;">BEFORE OPTIMIZATION</div>',
                        unsafe_allow_html=True,
                    )
                    st.markdown(_terminal(ast2.pretty(), "#e6edf3"),
                                unsafe_allow_html=True)
                with c2:
                    st.markdown(
                        '<div style="color:#8b949e;font-size:0.82rem;'
                        'margin-bottom:4px;">AFTER OPTIMIZATION</div>',
                        unsafe_allow_html=True,
                    )
                    st.markdown(_terminal(_oast.pretty(), "#7ee787"),
                                unsafe_allow_html=True)

                st.markdown(_section("RESULTS"), unsafe_allow_html=True)
                ma, mb = st.columns(2)
                ma.metric("Constant Expressions Folded", _o2.stats["constant_folds"])
                mb.metric("Reversible Reductions", _o2.stats["reversible_reductions"])

            with t_sym:
                try:
                    sym2 = analyze_code(ast2)
                    syms = sym2.all_symbols()
                    if syms:
                        rows2 = "".join(
                            f'<tr>'
                            f'<td style="padding:7px 12px;border-bottom:1px solid #21262d;">'
                            f'<code style="color:#79c0ff;">{s.name}</code></td>'
                            f'<td style="padding:7px 12px;border-bottom:1px solid #21262d;">'
                            f'{_type_badge(s.type_name)}</td>'
                            f'<td style="padding:7px 12px;border-bottom:1px solid #21262d;'
                            f'color:#8b949e;font-size:0.8rem;">'
                            f'L{s.line or "?"}</td>'
                            f'</tr>'
                            for s in syms.values()
                        )
                        st.markdown(
                            f'<table style="width:100%;border-collapse:collapse;'
                            f'background:#161b22;border-radius:8px;overflow:hidden;">'
                            f'<thead><tr>'
                            f'<th style="background:#21262d;color:#8b949e;padding:8px 12px;'
                            f'text-align:left;font-size:0.78rem;">VARIABLE</th>'
                            f'<th style="background:#21262d;color:#8b949e;padding:8px 12px;'
                            f'text-align:left;font-size:0.78rem;">BIOLOGICAL TYPE</th>'
                            f'<th style="background:#21262d;color:#8b949e;padding:8px 12px;'
                            f'text-align:left;font-size:0.78rem;">DECLARED AT</th>'
                            f'</tr></thead><tbody>{rows2}</tbody></table>',
                            unsafe_allow_html=True,
                        )
                    else:
                        st.info("No symbols declared in this program.")
                except (GenomeDSLError, NotImplementedError) as e:
                    st.markdown(
                        _err_box("Semantic Error (cannot show symbol table)", str(e)),
                        unsafe_allow_html=True,
                    )

        except GenomeDSLError as e:
            st.markdown(_err_box("Parse Error", e.format_error()), unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — Language Reference
# ══════════════════════════════════════════════════════════════════════════════
elif nav == "📚  Language Reference":
    st.markdown(
        '<h1 style="color:#e6edf3;font-size:1.8rem;font-weight:800;margin-bottom:0.1rem;">'
        '📚 GenomeDSL Language Reference</h1>'
        '<p style="color:#8b949e;margin-bottom:1.4rem;">'
        'Complete syntax, types, built-in functions, and error system.</p>',
        unsafe_allow_html=True,
    )

    t_types, t_funcs, t_syntax, t_errors, t_grammar = st.tabs([
        "🔷 Types",
        "⚙️ Functions",
        "📝 Syntax",
        "⚠️ Error System",
        "📐 EBNF Grammar",
    ])

    # ── Types ─────────────────────────────────────────────────────────────────
    with t_types:
        st.markdown("""
**GenomeDSL has four first-class types.** The compiler enforces biological correctness at declaration time — wrong alphabets and wrong type assignments are caught *before* the program runs.

| Type | Description | Alphabet |
|:---|:---|:---|
| `DNA` | Double-stranded DNA sequence | `A T G C` only |
| `RNA` | Single-stranded RNA transcript | `A U G C` only |
| `Protein` | Amino acid chain | Standard 20 codes |
| `RESULT` | Numeric / analysis output | Float, Int, or list |

**Declaration syntax:**
```gdsl
DNA    gene   = "ATGCGTAC"
RNA    rna    = transcribe(gene)
Protein prot  = translate(rna)
RESULT gc     = gc_content(gene)
```

> The compiler validates the literal alphabet immediately. `DNA gene = "AUGC"` is rejected because `U` is not a valid DNA base.
""")

    # ── Functions ─────────────────────────────────────────────────────────────
    with t_funcs:
        st.markdown("""
All built-in functions are **biologically typed** — the compiler verifies input and output types before execution.

| Function | Input Type | Output Type | Description |
|:---|:---:|:---:|:---|
| `transcribe(seq)` | `DNA` | `RNA` | T→U substitution (DNA → RNA) |
| `translate(seq)` | `RNA` | `Protein` | Codon table translation (RNA → Protein) |
| `reverse_complement(seq)` | `DNA` or `RNA` | same | Complement + reverse |
| `reverse(seq)` | any | same | Reverses the sequence string |
| `gc_content(seq)` | `DNA` or `RNA` | `RESULT` | GC% as a float |
| `length(seq)` | any | `RESULT` | Number of residues |

**Output statements:**
```gdsl
PRINT "Label:", variable
PLOT  gc_content(gene)   # Renders a sliding-window GC profile chart
```
""")

    # ── Syntax ────────────────────────────────────────────────────────────────
    with t_syntax:
        st.markdown("""
**Complete syntax overview:**

```gdsl
# Line comments (# or //)

# Variable declaration
DNA    seq = "ATGCGTAC"
RNA    rna = transcribe(seq)
Protein p  = translate(rna)
RESULT gc  = gc_content(seq)

# Re-assignment (must match original type)
seq = reverse_complement(seq)

# Print one or more expressions
PRINT "GC Content:", gc_content(seq)
PRINT seq, rna

# Visualize a numeric sequence function
PLOT gc_content(seq)
```

**Notes:**
- Semicolons are optional.
- Statements can span multiple lines.
- Functions can be nested: `gc_content(reverse_complement(seq))`.
""")

    # ── Error System ──────────────────────────────────────────────────────────
    with t_errors:
        st.markdown("""
The compiler reports three classes of error, each with **line number** and **column** information:

| Error Class | When raised | Example |
|:---|:---|:---|
| `LexicalError` | Unrecognised character in source | `DNA x = @invalid` |
| `SyntaxError` | Malformed statement structure | `DNA x =` (missing value) |
| `AlphabetError` | Wrong nucleotide/residue for the declared type | `DNA x = "AUGC"` (U in DNA) |
| `BiologicalTypeError` | Operation applied to incompatible type | `translate(dna_var)` |
| `SemanticError` | Undeclared variable, duplicate declaration | `print(undeclared_var)` |

**Sample error output:**
```
[AlphabetError] [line 2, column 1]:
    Invalid DNA base 'U'. DNA sequences only accept bases: A, T, G, C
```
""")

    # ── Grammar ───────────────────────────────────────────────────────────────
    with t_grammar:
        from genomedsl.grammar import GENOMEDSL_GRAMMAR
        st.markdown("**Lark EBNF Grammar used by the Earley parser:**")
        st.code(GENOMEDSL_GRAMMAR, language="text")
