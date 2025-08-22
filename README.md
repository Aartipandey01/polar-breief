# polar-breief
Give the attorney a strategic preparation tool that pinpoints, summarizes, and precisely references the brief’s key arguments, enabling rapid verification and deeper exploration ahead of trial.


  This script generates an upgraded, production-ready project scaffold
# for "PolarBrief: AI Driven Pro/Con Argument Miner" with:
# - Balanced 5 Pro / 5 Con selection
# - CLI + REST API
# - OCR/native PDF ingestion with page:line metadata
# - JSON + PDF reports
# - Validation harness
# - Tests, Makefile, Dockerfile, and docs
#
# It saves everything under /mnt/data/polarbrief-argument-miner-v2
# and zips it for download.

import os, zipfile, textwrap, json, pathlib

BASE = "/mnt/data/polarbrief-argument-miner-v2"
PKG = os.path.join(BASE, "polarbrief")
VAL = os.path.join(BASE, "validation")
OUT = os.path.join(BASE, "outputs")
DATA = os.path.join(BASE, "data")
TESTS = os.path.join(BASE, "tests")
os.makedirs(PKG, exist_ok=True)
os.makedirs(VAL, exist_ok=True)
os.makedirs(OUT, exist_ok=True)
os.makedirs(DATA, exist_ok=True)
os.makedirs(TESTS, exist_ok=True)

files = {}

def w(path, content):
    files[path] = content

w(os.path.join(BASE, "requirements.txt"), """\
# Core
numpy>=1.24.0
pandas>=2.0.0
scikit-learn>=1.2.0

# PDF/OCR
pdfplumber>=0.11.0
pytesseract>=0.3.10
Pillow>=10.0.0

# NLP
nltk>=3.8.1

# Optional LLMs / embeddings (auto-fallback if missing)
transformers>=4.43.0
torch>=2.2.0; platform_system!='Windows' or platform_machine!='x86'
sentence-transformers>=3.0.1

# API & Reports
fastapi>=0.111.0
uvicorn[standard]>=0.30.0
pydantic>=2.7.0
reportlab>=4.2.0

# Utilities
tqdm>=4.66.0
python-multipart>=0.0.9
""")

w(os.path.join(BASE, "README.md"), """\
# PolarBrief: AI Driven Pro/Con Argument Miner

This application ingests the **“Amicus Brief on behalf of Mississippi, Alabama, Arkansas”** and surfaces **10 pivotal arguments** — **5 Pro** and **5 Con** — each with **exact `page:start_line-end_line` citations**.

## Highlights
- PDF (native) or OCR (scanned) → **page+line JSONL**
- Passage segmentation by sliding windows with citations
- Salience ranking (TF-IDF + MMR; optional embedding rerank)
- **Balanced selection**: top **5 Pro** and **5 Con**
- ≤ 75-word summaries (classical with optional LLM upgrade)
- Exports **JSON** + **PDF** reports
- **CLI** and **REST API** for on-demand processing
- Validation script: Relevance@10 and Citation Accuracy

---

## Quickstart

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
