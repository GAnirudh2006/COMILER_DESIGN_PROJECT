# GenomeDSL: GitHub & Streamlit Cloud Deployment Guide

This guide explains how you and your teammates (and faculty guide Prof. Nithya K) can view and interact with **GenomeDSL** on GitHub and run it directly in any web browser without installing anything locally.

---

## 1. Running Locally with Streamlit

To run the interactive web app on your local machine:

```powershell
cd "C:\Users\G Anirudh\.gemini\antigravity\scratch\genomedsl"
streamlit run genomedsl_app.py
```

This will automatically open `http://localhost:8501` in your browser.

---

## 2. Pushing the Repository to GitHub

### Step 1: Initialize Git in the Project Folder
Open your terminal in `genomedsl`:

```powershell
cd "C:\Users\G Anirudh\.gemini\antigravity\scratch\genomedsl"
git init
git add .
git commit -m "Initial commit: GenomeDSL compiler and interactive Streamlit workbench"
```

### Step 2: Create a New GitHub Repository
1. Go to [github.com/new](https://github.com/new).
2. Name the repository: `GenomeDSL`.
3. Set visibility to **Public** (recommended so Streamlit Cloud can deploy for free).
4. Do NOT initialize with a README, .gitignore, or license (these already exist in our project).
5. Click **Create repository**.

### Step 3: Link and Push
Run the commands provided by GitHub (substituting your username):

```powershell
git remote add origin https://github.com/<YOUR_GITHUB_USERNAME>/GenomeDSL.git
git branch -M main
git push -u origin main
```

---

## 3. Deploying to Streamlit Community Cloud (1-Click & 100% Free)

Streamlit Community Cloud hosts your web app directly from your GitHub repository so that anyone with the link can use the IDE, run code, and view visualizations.

1. Go to **[share.streamlit.io](https://share.streamlit.io)** and log in with your GitHub account.
2. Click **Create app** (or **New app**).
3. Select your repository: `<YOUR_GITHUB_USERNAME>/GenomeDSL`.
4. Branch: `main`.
5. Main file path: `genomedsl_app.py`.
6. Click **Deploy!**

Within 1–2 minutes, your web application will be live at a public URL like:
`https://genomedsl-<your-subdomain>.streamlit.app`

You can share this link with:
- Your teammate (Abhishek Kothari)
- Your faculty guide (Prof. Nithya K)
- Lab evaluators during your viva!

---

## 4. What Teammates & Evaluators Can Do on the Web App

1. **Live Code Editor:** Type or load sample `.gdsl` programs.
2. **Compiler Pipeline Stages:** Watch Lexing, Parsing, Semantic Type Checking, AST Optimization, and Runtime Execution run step-by-step.
3. **Domain Error Demos:** Trigger compile-time errors (`AlphabetError`, `BiologicalTypeError`, `SemanticError`) with 1 click.
4. **Interactive AST Visualizer:** Inspect the AST hierarchy and compare AST before vs. after constant folding.
5. **Matplotlib Visualizations:** View sliding-window GC-content curves and nucleotide composition bar charts directly in the browser.
6. **Student Implementation Zone:** Review the 4 reserved student tasks with mathematical formulas, concepts, and test runners.
7. **Viva Voce & Professor Demo Guide:** Access the full viva answers and demo checklist.
