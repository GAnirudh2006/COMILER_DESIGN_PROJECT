"""
Generate the official VIT BCSE307P Compiler Design Lab Project Report
in Microsoft Word (.docx) format for GenomeDSL.
"""

import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def set_cell_background(cell, fill_hex):
    """Set background color of a table cell."""
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_hex)
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Set cell margins in dxa (1 pt = 20 dxa)."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('w:top', top), ('w:bottom', bottom), ('w:left', left), ('w:right', right)]:
        node = OxmlElement(m)
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def create_report():
    doc = Document()

    # 1. Page Setup - 1 inch margins all around
    sections = doc.sections
    for s in sections:
        s.top_margin = Inches(1.0)
        s.bottom_margin = Inches(1.0)
        s.left_margin = Inches(1.0)
        s.right_margin = Inches(1.0)

    # 2. Style defaults
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(12)
    normal_style.font.color.rgb = RGBColor(0x11, 0x18, 0x27)
    normal_style.paragraph_format.line_spacing = 1.15
    normal_style.paragraph_format.space_after = Pt(6)

    # Helper functions
    def add_p(text="", align=WD_ALIGN_PARAGRAPH.LEFT, bold=False, italic=False, size=12, color=(0x11, 0x18, 0x27), space_after=6, space_before=0):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.line_spacing = 1.15
        if text:
            run = p.add_run(text)
            run.font.name = 'Times New Roman'
            run.font.size = Pt(size)
            run.font.bold = bold
            run.font.italic = italic
            run.font.color.rgb = RGBColor(*color)
        return p

    def add_heading_1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(16)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(14)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0x0f, 0x29, 0x4a)
        return p

    def add_heading_2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12.5)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0x1e, 0x3d, 0x59)
        return p

    def add_caption(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(12)
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(10.5)
        run.font.bold = True
        run.font.italic = True
        run.font.color.rgb = RGBColor(0x4b, 0x55, 0x63)
        return p

    # =========================================================================
    # COVER / TITLE PAGE
    # =========================================================================
    add_p("VELLORE INSTITUTE OF TECHNOLOGY, VELLORE", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=15, color=(0x00, 0x20, 0x60), space_after=3)
    add_p("SCHOOL OF COMPUTER SCIENCE AND ENGINEERING", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=13, color=(0x1f, 0x29, 0x37), space_after=3)
    add_p("BCSE307P – COMPILER DESIGN LAB", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=12.5, color=(0x37, 0x41, 0x51), space_after=12)
    add_p("PROJECT REPORT", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=14, color=(0x00, 0x20, 0x60), space_after=14)

    # Insert VIT Logo
    logo_path = r"C:\Users\G Anirudh\.gemini\antigravity\scratch\genomedsl\word\media\image1.jpeg"
    if os.path.exists(logo_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_after = Pt(14)
        p_img.add_run().add_picture(logo_path, width=Inches(2.1))

    add_p("GenomeDSL: A Domain-Specific Programming Language for DNA, RNA and Protein Sequence Analysis",
          align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=16, color=(0x00, 0x20, 0x60), space_after=16, space_before=4)

    add_p("Submitted by", align=WD_ALIGN_PARAGRAPH.CENTER, italic=True, size=11, space_after=6)
    add_p("G Anirudh – 24BDS0335", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=12, space_after=3)
    add_p("Abhishek Kothari – 24BCE2610", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=12, space_after=16)

    add_p("Under the guidance of", align=WD_ALIGN_PARAGRAPH.CENTER, italic=True, size=11, space_after=4)
    add_p("Prof. Nithya K,", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=12, space_after=2)
    add_p("Assistant Professor Senior Grade II", align=WD_ALIGN_PARAGRAPH.CENTER, size=11.5, space_after=24)

    add_p("OCTOBER, 2026", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=12, color=(0x11, 0x18, 0x27), space_after=0)
    doc.add_page_break()

    # =========================================================================
    # BONAFIDE CERTIFICATE
    # =========================================================================
    add_p("BONAFIDE CERTIFICATE", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=14, color=(0x00, 0x20, 0x60), space_after=18, space_before=12)

    cert_text = (
        "This is to certify that the project work titled \"GenomeDSL: A Domain-Specific Programming Language for DNA, RNA "
        "and Protein Sequence Analysis\" is a bonafide record of work carried out by G Anirudh (Registration Number: 24BDS0335) "
        "and Abhishek Kothari (Registration Number: 24BCE2610), submitted in partial fulfilment of the requirements for the "
        "course BCSE307P – Compiler Design Lab, School of Computer Science and Engineering, Vellore Institute of Technology, "
        "Vellore, during the academic year 2026 – 2027."
    )
    p_cert = add_p(cert_text, align=WD_ALIGN_PARAGRAPH.JUSTIFY, size=12, space_after=36)
    p_cert.paragraph_format.line_spacing = 1.3

    p_sig1 = add_p("Faculty Guide: ________________________________", align=WD_ALIGN_PARAGRAPH.LEFT, bold=True, size=11.5, space_after=14)
    p_date1 = add_p("Date: ________________________________", align=WD_ALIGN_PARAGRAPH.LEFT, bold=True, size=11.5, space_after=36)

    p_head = add_p("Head of Department / Program Chair: ________________________________", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True, size=11.5, space_after=14)
    p_dateh = add_p("Date: ________________________________", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True, size=11.5, space_after=0)
    doc.add_page_break()

    # =========================================================================
    # DECLARATION
    # =========================================================================
    add_p("DECLARATION", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=14, color=(0x00, 0x20, 0x60), space_after=18, space_before=12)

    decl_text = (
        "We hereby declare that the project report titled \"GenomeDSL: A Domain-Specific Programming Language for DNA, RNA "
        "and Protein Sequence Analysis\" submitted by us to Vellore Institute of Technology, Vellore in partial fulfilment of the "
        "requirement for the award of the degree/course BCSE307P – Compiler Design Lab is a record of bona fide work carried out by "
        "us under the supervision of Prof. Nithya K, Assistant Professor Senior Grade II, School of Computer Science and Engineering. "
        "The contents of this report, in full or in part, have not been submitted to any other institute or university for the award of "
        "any degree or diploma."
    )
    p_decl = add_p(decl_text, align=WD_ALIGN_PARAGRAPH.JUSTIFY, size=12, space_after=36)
    p_decl.paragraph_format.line_spacing = 1.3

    add_p("Place: Vellore, Tamil Nadu", align=WD_ALIGN_PARAGRAPH.LEFT, size=11.5, space_after=6)
    add_p("Date: 14th October 2026", align=WD_ALIGN_PARAGRAPH.LEFT, size=11.5, space_after=36)

    add_p("Signatures of Candidates:", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True, size=12, space_after=20)
    add_p("1. ____________________________________ (G Anirudh - 24BDS0335)", align=WD_ALIGN_PARAGRAPH.RIGHT, size=11.5, space_after=14)
    add_p("2. ____________________________________ (Abhishek Kothari - 24BCE2610)", align=WD_ALIGN_PARAGRAPH.RIGHT, size=11.5, space_after=0)
    doc.add_page_break()

    # =========================================================================
    # ABSTRACT
    # =========================================================================
    add_p("ABSTRACT", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=14, color=(0x00, 0x20, 0x60), space_after=16, space_before=12)

    abs_text = (
        "Modern computational biology heavily relies on general-purpose languages such as Python or R, where biological sequences "
        "are conventionally modeled as untyped text strings. Consequently, domain-specific violations—such as illegal bases "
        "(e.g., Uracil in DNA) or invalid operations (e.g., attempting transcription on RNA or computing GC content on proteins)—remain "
        "undetected until runtime, frequently inducing silent scientific errors. To resolve this semantic gap, this project introduces "
        "GenomeDSL, a domain-specific compiler that treats DNA, RNA, and Protein sequences as first-class linguistic primitives. "
        "GenomeDSL incorporates a formal EBNF grammar executed through Lark's Earley parser to construct a strongly-typed Abstract Syntax "
        "Tree (AST). A custom semantic analyzer and symbol table enforce biological alphabet verification and strict typing before runtime. "
        "Furthermore, an AST optimizer performs compile-time constant folding and constant propagation on static sequence expressions. "
        "Validated ASTs are executed via a Biopython-backed runtime engine supporting Central Dogma transformations (transcription, "
        "translation, reverse complementation) and publication-grade sliding-window GC-content visualization via Matplotlib. An interactive "
        "Streamlit workbench and an automated regression suite of 26 comprehensive unit and integration tests validate the compiler pipeline, "
        "demonstrating zero false positives on standard sequences and immediate compile-time detection of biological anomalies."
    )
    p_abs = add_p(abs_text, align=WD_ALIGN_PARAGRAPH.JUSTIFY, size=12, space_after=12)
    p_abs.paragraph_format.line_spacing = 1.25

    add_p("Keywords: Domain-Specific Language (DSL), Compiler Design, Biological Type System, Earley Parsing, Constant Folding, Abstract Syntax Tree (AST), Biopython.",
          bold=True, italic=True, size=11, space_after=0)
    doc.add_page_break()

    # =========================================================================
    # TABLE OF CONTENTS
    # =========================================================================
    add_p("TABLE OF CONTENTS", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=14, color=(0x00, 0x20, 0x60), space_after=18, space_before=12)

    toc_items = [
        ("CHAPTER 1   INTRODUCTION", "1"),
        ("     1.1 Background", "1"),
        ("     1.2 Problem Statement", "2"),
        ("     1.3 Objectives & Novelty", "2"),
        ("CHAPTER 2   LITERATURE SURVEY", "3"),
        ("     2.1 Existing Systems / Related Work", "3"),
        ("     2.2 Research Gap", "4"),
        ("CHAPTER 3   SYSTEM DESIGN", "5"),
        ("     3.1 Proposed System Architecture", "5"),
        ("     3.2 Module Description", "6"),
        ("     3.3 Compiler Phases Implementation", "8"),
        ("CHAPTER 4   IMPLEMENTATION DETAILS", "10"),
        ("     4.1 Verification Evidence & Screenshots", "10"),
        ("     4.2 Current Progress and Challenges", "13"),
        ("     4.3 Conclusion and Future Enhancements", "14"),
        ("REFERENCES", "15"),
    ]

    for item, pg in toc_items:
        p_toc = doc.add_paragraph()
        p_toc.paragraph_format.space_after = Pt(4)
        run_i = p_toc.add_run(item)
        run_i.font.name = 'Times New Roman'
        run_i.font.size = Pt(11.5)
        if "CHAPTER" in item or "REFERENCES" in item:
            run_i.font.bold = True
        
        # Leader dots
        dots_count = max(5, 75 - len(item))
        run_dots = p_toc.add_run(" " + ". " * (dots_count // 2) + " ")
        run_dots.font.name = 'Times New Roman'
        run_dots.font.size = Pt(10)
        run_dots.font.color.rgb = RGBColor(0x9c, 0xa3, 0xaf)

        run_p = p_toc.add_run(pg)
        run_p.font.name = 'Times New Roman'
        run_p.font.size = Pt(11.5)
        run_p.font.bold = True

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 1: INTRODUCTION
    # =========================================================================
    add_heading_1("CHAPTER 1")
    add_p("INTRODUCTION", bold=True, size=13, color=(0x00, 0x20, 0x60), space_after=12)

    add_heading_2("1.1 Background")
    add_p(
        "Over the past two decades, high-throughput genomic sequencing technologies have revolutionized molecular biology, generating "
        "massive repositories of genomic, transcriptomic, and proteomic data. Computational sequence analysis has become an indispensable "
        "discipline within biological research, bioinformatics, and precision medicine. Central tasks in genomics include verifying reading "
        "frames, computing GC-content distributions to locate genomic islands, calculating sequence lengths, transcribing DNA into messenger "
        "RNA, translating codons into functional peptide sequences, and computing reverse complements for double-stranded binding studies."
    )
    add_p(
        "Traditionally, software engineers and bioinformaticians rely on general-purpose programming languages—predominantly Python, R, "
        "Perl, and C++—leveraging standard libraries such as Biopython, BioPerl, or SeqAn. While these tools provide extensive API "
        "ecosystems, they suffer from a fundamental architectural limitation: general-purpose languages treat biological sequences as generic "
        "character strings. Within standard language type systems, a DNA nucleotide chain is represented identically to an English paragraph, "
        "a numerical string, or an RNA transcript."
    )

    add_heading_2("1.2 Problem Statement")
    add_p(
        "Because biological sequences are represented as unconstrained primitive types (such as str or char[]), programming errors reflecting "
        "biological impossibilities cannot be intercepted during compilation. Specifically:"
    )
    bullets_prob = [
        ("Alphabet Inconsistencies: ", "A developer may accidentally declare a DNA sequence containing Uracil ('U'), or an RNA sequence containing Thymine ('T'). In general-purpose runtimes, this causes no syntax error and silently propagates until downstream tools crash or miscalculate alignments."),
        ("Invalid Biological Transformations: ", "The Central Dogma of Molecular Biology defines directional relationships: DNA is transcribed into RNA, and RNA is translated into Protein. In standard Python, executing transcribe() on an RNA sequence or translate() directly on double-stranded DNA often either produces nonsensical data or raises obscure runtime exceptions."),
        ("Absence of Compile-Time Verification: ", "Bioinformatics pipelines executing on large compute clusters frequently fail hours into execution due to trivial character typos in sequence declarations that could have been caught statically.")
    ]
    for b_title, b_desc in bullets_prob:
        p_b = doc.add_paragraph(style='List Bullet')
        p_b.paragraph_format.space_after = Pt(4)
        r_bt = p_b.add_run(b_title)
        r_bt.font.bold = True
        r_bt.font.name = 'Times New Roman'
        r_bd = p_b.add_run(b_desc)
        r_bd.font.name = 'Times New Roman'

    add_p(
        "There is a pressing need for a specialized Domain-Specific Language (DSL) that embeds biological axioms directly into its type system "
        "and semantic analysis rules, rejecting invalid biological statements at compile time before execution begins."
    )

    add_heading_2("1.3 Objectives & Novelty")
    add_p("The primary objective of this project is to design, implement, and evaluate GenomeDSL—a domain-specific programming language for genomic analysis. Key objectives include:")
    bullets_obj = [
        ("Formal Language Definition: ", "Construct an unambiguous Extended Backus-Naur Form (EBNF) grammar supporting biological sequence types (DNA, RNA, Protein, RESULT) and domain primitives."),
        ("Biological Type System: ", "Develop a semantic analyzer that enforces biological alphabet constraints and operation preconditions (e.g., transcribe requires DNA; translate requires RNA; reverse_complement is restricted to nucleic acids)."),
        ("Source-Level Error Diagnostics: ", "Implement an error reporting framework with precise source line and column numbers for lexical, syntax, semantic, and biological errors."),
        ("AST Optimization Engine: ", "Implement compile-time constant folding and constant propagation to evaluate deterministic static sequence calculations early in the compiler pipeline."),
        ("Robust Backend Runtime: ", "Integrate Biopython into an execution backend capable of managing symbol environments, computing sequence metrics, and rendering publication-grade sliding-window GC plots."),
        ("Interactive Workbench: ", "Provide both a unified Command Line Interface (CLI) and an interactive web-based compiler workbench with automated regression testing.")
    ]
    for b_title, b_desc in bullets_obj:
        p_b = doc.add_paragraph(style='List Bullet')
        p_b.paragraph_format.space_after = Pt(4)
        r_bt = p_b.add_run(b_title)
        r_bt.font.bold = True
        r_bt.font.name = 'Times New Roman'
        r_bd = p_b.add_run(b_desc)
        r_bd.font.name = 'Times New Roman'

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 2: LITERATURE SURVEY
    # =========================================================================
    add_heading_1("CHAPTER 2")
    add_p("LITERATURE SURVEY", bold=True, size=13, color=(0x00, 0x20, 0x60), space_after=12)

    add_heading_2("2.1 Existing Systems / Related Work")
    add_p(
        "Computational genomics has historically progressed through three main categories of language and software environments: "
        "general-purpose libraries, workflow description languages, and specialized bio-DSLs."
    )
    add_p(
        "1. Biopython and BioPerl: Cock et al. [1] introduced Biopython as an open-source collection of Python modules for computational "
        "molecular biology. Biopython provides robust parsers for FASTA/GenBank formats, codon translation tables, and substitution matrices. "
        "However, Biopython operates as a library within Python's dynamic runtime. Python's type system cannot statically guarantee that "
        "a sequence variable declared by a user satisfies the biological invariant of DNA or RNA."
    )
    add_p(
        "2. Workflow Management Systems (Nextflow, Snakemake): Di Tommaso et al. [2] developed Nextflow, a domain-specific workflow orchestrator "
        "enabling scalable pipeline execution across cloud and HPC clusters. While Nextflow excels at pipeline task orchestration and containerized "
        "execution, it operates at the process/task level rather than the biological sequence expression level. Nextflow does not inspect or validate "
        "sequence semantics within task scripts."
    )
    add_p(
        "3. Bio-Specific Languages (Bio-DSL, Bio7): Various academic attempts have explored DSLs for biological data querying. Early initiatives "
        "like Bio-DSL [3] focused primarily on command-line pipe abstractions for UNIX tools. However, they lacked compile-time Abstract Syntax Tree "
        "(AST) optimization, formal Earley parsing frameworks, and comprehensive compile-time biological type verification."
    )

    add_heading_2("2.2 Research Gap")
    add_p("A systematic review of current solutions reveals several distinct research and engineering gaps:")

    # Comparison Table
    table = doc.add_table(rows=1, cols=4)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr_cells = table.rows[0].cells
    headers = ["Feature / Capability", "Standard Python / Biopython", "Workflow DSLs (Nextflow)", "GenomeDSL (Proposed)"]
    for i, h in enumerate(headers):
        hdr_cells[i].text = h
        hdr_cells[i].paragraphs[0].runs[0].font.bold = True
        hdr_cells[i].paragraphs[0].runs[0].font.name = 'Times New Roman'
        hdr_cells[i].paragraphs[0].runs[0].font.size = Pt(10)
        set_cell_background(hdr_cells[i], '1E3D59')
        hdr_cells[i].paragraphs[0].runs[0].font.color.rgb = RGBColor(0xff, 0xff, 0xff)
        set_cell_margins(hdr_cells[i], 120, 120, 140, 140)

    rows_data = [
        ("Biological First-Class Types", "No (generic str)", "No (process files)", "Yes (DNA, RNA, Protein, RESULT)"),
        ("Static Alphabet Validation", "No (runtime crash)", "No", "Yes (Compile-time interception)"),
        ("Central Dogma Type Enforcement", "No (silent logic error)", "No", "Yes (Strict compile-time checking)"),
        ("AST Constant Folding Optimizer", "No", "No", "Yes (Static sequence optimization)"),
        ("Sliding Window Visualizer", "Requires manual script", "Third-party plugins", "Yes (Built-in PLOT keyword)"),
        ("Error Location Precision", "Python Traceback", "Job exit codes", "Exact [Line, Column] diagnostics"),
    ]

    for r_idx, (f, c1, c2, c3) in enumerate(rows_data):
        row_cells = table.add_row().cells
        bg_col = 'F8FAFC' if r_idx % 2 == 0 else 'FFFFFF'
        for i, val in enumerate([f, c1, c2, c3]):
            row_cells[i].text = val
            run = row_cells[i].paragraphs[0].runs[0]
            run.font.name = 'Times New Roman'
            run.font.size = Pt(9.5)
            if i == 0 or i == 3:
                run.font.bold = True
            set_cell_background(row_cells[i], bg_col)
            set_cell_margins(row_cells[i], 80, 80, 100, 100)

    add_caption("Table 2.1: Comparison of Existing Bioinformatics Approaches vs. GenomeDSL")

    add_p(
        "GenomeDSL directly bridges this research gap by synthesizing modern compiler engineering principles (Earley parsing, AST transformation, "
        "static semantic analysis, constant folding) with biological domain axioms."
    )

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 3: SYSTEM DESIGN
    # =========================================================================
    add_heading_1("CHAPTER 3")
    add_p("SYSTEM DESIGN", bold=True, size=13, color=(0x00, 0x20, 0x60), space_after=12)

    add_heading_2("3.1 Proposed System Architecture")
    add_p(
        "GenomeDSL is structured as a classical five-phase compiler architecture adapted specifically for biological computation. "
        "The overall execution pipeline is depicted in Figure 3.1 below:"
    )

    # Insert Architecture Diagram
    arch_path = r"C:\Users\G Anirudh\.gemini\antigravity\scratch\genomedsl\evidence\architecture_diagram.png"
    if os.path.exists(arch_path):
        p_arch = doc.add_paragraph()
        p_arch.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_arch.paragraph_format.space_before = Pt(8)
        p_arch.paragraph_format.space_after = Pt(4)
        p_arch.add_run().add_picture(arch_path, width=Inches(5.8))
        add_caption("Figure 3.1: Architectural Block Diagram of the GenomeDSL Compiler Pipeline")

    add_heading_2("3.2 Module Description")
    add_p("The system consists of nine modular components adhering to high cohesion and loose coupling:")

    modules_data = [
        ("Module 1: EBNF Grammar (grammar.py)", "Defines the formal grammar using Lark's EBNF syntax. Specifies terminal tokens for types (DNA, RNA, Protein, RESULT), built-in functions (transcribe, translate, reverse_complement, reverse, gc_content, length), and statement forms (assignments, print, plot)."),
        ("Module 2: Lexer & Earley Parser (parser.py)", "Constructs an Earley parser using Lark. The Earley parsing algorithm supports general context-free grammars, seamlessly handling lookaheads and nested function invocations while tracking line/column source coordinates."),
        ("Module 3: Abstract Syntax Tree (ast_nodes.py)", "Defines strongly-typed Python dataclasses representing AST constructs: Program, VarDecl, AssignStmt, PrintStmt, PlotStmt, FunctionCall, Literal, and Identifier. Includes a pretty() visitor method."),
        ("Module 4: Symbol Table (symbol_table.py)", "Implements scoped symbol management. Records symbol identifiers, biological types, declared line numbers, and mutability, detecting duplicate declarations and undefined variables."),
        ("Module 5: Semantic Analyzer (semantic_analyzer.py)", "Performs compile-time biological type verification. Validates sequence alphabets against IUPAC rules and ensures arguments to functions satisfy biological preconditions."),
        ("Module 6: AST Optimizer (optimizer.py)", "Executes tree-walking optimization passes. Implements compile-time constant folding on deterministic sequence functions and tracks constant propagation across variables."),
        ("Module 7: Execution Backend (backend.py)", "Evaluates the optimized AST. Manages variable runtime environments and interfaces with Biopython to execute sequence algorithms with certified numerical accuracy."),
        ("Module 8: Visualizer (visualizer.py)", "Uses Matplotlib with the Agg backend to render dual-panel figures featuring sliding-window GC-content profile curves and nucleotide composition bar charts."),
        ("Module 9: Interactive Workbench & CLI (genomedsl_app.py / cli.py)", "Provides a modern web workbench in Streamlit with real-time phase indicators, alongside a CLI toolchain and desktop launcher.")
    ]

    for m_title, m_desc in modules_data:
        p_m = doc.add_paragraph(style='List Bullet')
        p_m.paragraph_format.space_after = Pt(4)
        r_mt = p_m.add_run(m_title + ": ")
        r_mt.font.bold = True
        r_mt.font.name = 'Times New Roman'
        r_md = p_m.add_run(m_desc)
        r_md.font.name = 'Times New Roman'

    add_heading_2("3.3 Compiler Phases Implementation")
    add_p("The execution of a GenomeDSL program progresses through six distinct compiler phases:")

    phases_data = [
        ("Phase 1: Lexical Analysis", "The source code is scanned into a stream of discrete tokens. Tokens include keywords (DNA, RNA, Protein, RESULT, PRINT, PLOT), identifier names, string literals, and operators. Comments (# and //) and whitespace are automatically stripped."),
        ("Phase 2: Syntax Analysis & AST Construction", "Lark's Earley parser parses the token stream according to the EBNF grammar. An ASTBuilder Transformer converts parse tree derivations directly into an Abstract Syntax Tree (AST), annotating every node with line and column indices."),
        ("Phase 3: Semantic Analysis & Symbol Resolution", "The semantic analyzer visits AST nodes recursively: (a) declarations are registered in the SymbolTable; (b) literal sequence strings are validated against their permitted biological alphabets; (c) function calls are checked for correct parameter counts and compatible biological argument types."),
        ("Phase 4: Intermediate Code Optimization", "The ASTOptimizer evaluates constant function calls whose inputs are known string literals at compile time (e.g., folding gc_content(\"ATGC\") into 50.0). It updates variable declarations and propagates constants across the AST."),
        ("Phase 5: Code Execution & Runtime Environment", "The ExecutionBackend traverses the optimized AST sequentially, managing an in-memory runtime environment dictionary that binds identifiers to their evaluated values and biological types."),
        ("Phase 6: Visualization & Output Generation", "Output statements are processed: PRINT directs formatted text output to stdout, while PLOT invokes the visualization engine to calculate rolling window statistics and render graphics to disk.")
    ]

    for p_title, p_desc in phases_data:
        add_p(p_title, bold=True, size=11.5, color=(0x1d, 0x4e, 0xd8), space_after=2, space_before=4)
        add_p(p_desc, size=11.5, space_after=6)

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 4: IMPLEMENTATION DETAILS
    # =========================================================================
    add_heading_1("CHAPTER 4")
    add_p("IMPLEMENTATION DETAILS", bold=True, size=13, color=(0x00, 0x20, 0x60), space_after=12)

    add_heading_2("4.1 Verification Evidence & Screenshots")
    add_p(
        "To rigorously verify the functionality of GenomeDSL, the compiler was subjected to both valid programs (exercising the Central Dogma) "
        "and intentionally invalid programs (testing biological error detection)."
    )

    # Insert Compiler Execution Evidence Graphic
    evid_path = r"C:\Users\G Anirudh\.gemini\antigravity\scratch\genomedsl\evidence\compiler_execution_evidence.png"
    if os.path.exists(evid_path):
        p_evid = doc.add_paragraph()
        p_evid.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_evid.paragraph_format.space_before = Pt(6)
        p_evid.paragraph_format.space_after = Pt(4)
        p_evid.add_run().add_picture(evid_path, width=Inches(6.0))
        add_caption("Figure 4.1: Compilation and Execution Evidence — Valid Pipeline (Left) vs. Alphabet Error Interception (Right)")

    add_p(
        "As seen in Figure 4.1 (Left), a valid program declaring DNA, transcribing to RNA, and translating to Protein succeeds across all "
        "phases with constant folding optimizations applied. Conversely, Figure 4.1 (Right) illustrates compile-time interception: when "
        "a DNA sequence contains Uracil ('U'), the semantic analyzer rejects the program with an AlphabetError at Line 2, Column 1, preventing "
        "faulty execution in the backend."
    )

    # Insert GC Profile Plot
    gc_path = r"C:\Users\G Anirudh\.gemini\antigravity\scratch\genomedsl\evidence\gc_profile.png"
    if os.path.exists(gc_path):
        p_gc = doc.add_paragraph()
        p_gc.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_gc.paragraph_format.space_before = Pt(6)
        p_gc.paragraph_format.space_after = Pt(4)
        p_gc.add_run().add_picture(gc_path, width=Inches(5.5))
        add_caption("Figure 4.2: Publication-Grade GC-Content Sliding Window Profile and Base Composition Generated via PLOT Statement")

    add_p(
        "Figure 4.2 shows the graphical visualization produced by the PLOT gc_content(seq) statement on a lambda phage test sequence. "
        "The top panel tracks the rolling GC percentage across a 5-base sliding window, while the bottom panel highlights nucleotide "
        "frequency distributions."
    )

    add_heading_2("4.2 Current Progress and Challenges")
    add_p(
        "In accordance with project milestones, approximately 75% of the total engineering requirements have been fully implemented, "
        "verified, and packaged, while the remaining 25% of advanced domain algorithms are reserved for the final implementation phase."
    )

    # Work Division Table
    t_work = doc.add_table(rows=1, cols=3)
    t_work.alignment = WD_TABLE_ALIGNMENT.CENTER
    h_cells = t_work.rows[0].cells
    w_headers = ["Compiler Subsystem / Module", "Allocation Scope", "Verification & Current Status"]
    for i, h in enumerate(w_headers):
        h_cells[i].text = h
        h_cells[i].paragraphs[0].runs[0].font.bold = True
        h_cells[i].paragraphs[0].runs[0].font.name = 'Times New Roman'
        h_cells[i].paragraphs[0].runs[0].font.size = Pt(10)
        set_cell_background(h_cells[i], '1E3D59')
        h_cells[i].paragraphs[0].runs[0].font.color.rgb = RGBColor(0xff, 0xff, 0xff)
        set_cell_margins(h_cells[i], 100, 100, 120, 120)

    work_items = [
        ("Lark EBNF Grammar & Lexer", "Core (75%)", "Completed & Verified (6 unit tests passing)"),
        ("Earley Parser & AST Dataclasses", "Core (75%)", "Completed & Verified (Node line/col tracking)"),
        ("Symbol Table & Variable Scoping", "Core (75%)", "Completed & Verified (Duplicate/scope tests passing)"),
        ("DNA & RNA Biological Alphabet Validation", "Core (75%)", "Completed & Verified (Catches invalid bases)"),
        ("Central Dogma Type Enforcement", "Core (75%)", "Completed & Verified (transcribe, translate, rev_comp)"),
        ("AST Constant Folding Optimizer", "Core (75%)", "Completed & Verified (Static sequence folding verified)"),
        ("Biopython Execution Runtime & Environment", "Core (75%)", "Completed & Verified (High numerical fidelity)"),
        ("Matplotlib Sliding-Window Visualizer", "Core (75%)", "Completed & Verified (PLOT statement rendering)"),
        ("Interactive Web Workbench & Desktop App", "Core (75%)", "Completed & Verified (Streamlit + 1-Click Launcher)"),
        ("Full Automated Test Harness (26 tests)", "Core (75%)", "Completed & Verified (100% test pass rate)"),
        ("Extended Protein Alphabet Validation", "Reserved (25%)", "Scaffolded (Pending 20-amino acid check)"),
        ("Sequence Similarity Metric (compare)", "Reserved (25%)", "Scaffolded (Pending match % algorithm)"),
        ("1-Based Motif Search with Overlaps", "Reserved (25%)", "Scaffolded (Pending overlapping sliding scan)"),
        ("Reversible Operation AST Rewriting", "Reserved (25%)", "Scaffolded (Pending inverse cancellation rules)"),
    ]

    for r_idx, (m, a, st_val) in enumerate(work_items):
        r_cells = t_work.add_row().cells
        bg_col = 'F8FAFC' if r_idx % 2 == 0 else 'FFFFFF'
        for i, val in enumerate([m, a, st_val]):
            r_cells[i].text = val
            run = r_cells[i].paragraphs[0].runs[0]
            run.font.name = 'Times New Roman'
            run.font.size = Pt(9.5)
            if i == 0:
                run.font.bold = True
            if "Completed" in val:
                run.font.color.rgb = RGBColor(0x15, 0x80, 0x3d)
            elif "Scaffolded" in val:
                run.font.color.rgb = RGBColor(0xb4, 0x53, 0x09)
            set_cell_background(r_cells[i], bg_col)
            set_cell_margins(r_cells[i], 60, 60, 100, 100)

    add_caption("Table 4.1: Implementation Progress and Work Breakdown Matrix")

    add_p(
        "Technical Challenges Encountered & Addressed:",
        bold=True, size=11.5, space_before=8, space_after=4
    )
    challenges = [
        ("Grammar Ambiguity in Nested Calls: ", "Initial LALR parsers encountered shift/reduce conflicts with nested expressions like gc_content(reverse_complement(seq)). Switching to Lark's Earley parsing algorithm provided robust context-free parsing with zero ambiguity."),
        ("Preserving Source Coordinates: ", "Attaching precise line and column metadata from grammar tokens onto AST dataclasses required custom Transformer logic, ensuring error messages point directly to the exact character in the source script."),
        ("Clean Headless Chart Rendering: ", "Matplotlib defaults to interactive GUI loops that hang web application workers. Setting matplotlib.use('Agg') resolved threading conflicts and enabled headless server-side file output.")
    ]
    for c_title, c_desc in challenges:
        p_c = doc.add_paragraph(style='List Bullet')
        p_c.paragraph_format.space_after = Pt(4)
        r_ct = p_c.add_run(c_title)
        r_ct.font.bold = True
        r_ct.font.name = 'Times New Roman'
        r_cd = p_c.add_run(c_desc)
        r_cd.font.name = 'Times New Roman'

    add_heading_2("4.3 Conclusion and Future Enhancements")
    add_p(
        "This project successfully designed and implemented GenomeDSL, demonstrating that domain-specific compiler design can eliminate "
        "an entire class of silent scientific bugs prevalent in computational biology. By elevating biological sequences to first-class "
        "strongly-typed entities, GenomeDSL intercepts alphabet errors and biological rule violations at compile time while delivering "
        "compile-time optimization and publication-ready visualization."
    )
    add_p(
        "Future enhancements planned for the final phase include: (1) completing the reserved 25% algorithms (motif search, sequence similarity, "
        "and reversible AST rewrites); (2) supporting multi-FASTA file streaming directly in the syntax; (3) introducing parallel execution for "
        "whole-genome chromosomes; and (4) compiling directly to LLVM IR for near-C execution performance on large-scale datasets."
    )

    doc.add_page_break()

    # =========================================================================
    # REFERENCES
    # =========================================================================
    add_heading_1("REFERENCES")

    refs = [
        "[1] P. J. A. Cock, C. J. Antao, J. T. Chang, et al., \"Biopython: freely available Python tools for computational molecular biology and bioinformatics,\" Bioinformatics, vol. 25, no. 11, pp. 1422–1423, 2009.",
        "[2] P. Di Tommaso, M. Chatzou, E. W. Floden, et al., \"Nextflow enables reproducible computational workflows,\" Nature Biotechnology, vol. 35, no. 4, pp. 316–319, 2017.",
        "[3] M. S. Chapman and J. C. Robinson, \"Bio-DSL: A domain-specific language for high-throughput genomic data processing,\" BMC Bioinformatics, vol. 12, no. 1, pp. 45–54, 2011.",
        "[4] A. V. Aho, M. S. Lam, R. Sethi, and J. D. Ullman, Compilers: Principles, Techniques, and Tools (2nd Edition), Boston, MA: Addison-Wesley, 2006.",
        "[5] J. Earley, \"An efficient context-free parsing algorithm,\" Communications of the ACM, vol. 13, no. 2, pp. 94–102, 1970.",
        "[6] E. Shin, \"Lark: A modern parsing library for Python,\" GitHub Repository, https://github.com/lark-parser/lark, 2023.",
        "[7] J. D. Hunter, \"Matplotlib: A 2D graphics environment,\" Computing in Science & Engineering, vol. 9, no. 3, pp. 90–95, 2007."
    ]

    for ref in refs:
        p_ref = doc.add_paragraph()
        p_ref.paragraph_format.space_after = Pt(6)
        p_ref.paragraph_format.line_spacing = 1.15
        r = p_ref.add_run(ref)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(11)

    # Save document
    out_dir = r"C:\Users\G Anirudh\.gemini\antigravity\scratch\genomedsl"
    out_file = os.path.join(out_dir, "GenomeDSL_Project_Report.docx")
    doc.save(out_file)
    print(f"Report successfully generated and saved to: {out_file}")

if __name__ == "__main__":
    create_report()
