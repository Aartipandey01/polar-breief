import json, pdfplumber
from PIL import Image
import pytesseract
from .utils import normalize_whitespace
from pathlib import Path
from typing import Optional
from .config import AppConfig

def _ocr_page(page, cfg: AppConfig) -> list[dict]:
# Render page to image and OCR by lines
im = page.to_image(resolution=cfg.dpi).original
pil = Image.frombytes('RGB', im.size, im.tobytes())
text = pytesseract.image_to_string(pil, lang=cfg.ocr_lang)
lines = text.splitlines()
out = []
line_no = 1
for ln in lines:
ln = normalize_whitespace(ln)
if ln:
out.append({"page": page.page_number, "line_no": line_no, "text": ln})
line_no += 1
return out

def ingest_pdf_to_jsonl(pdf_path: str, out_jsonl: str, force_ocr: bool=False, cfg: Optional[AppConfig]=None):
cfg = cfg or AppConfig()
pdf_path = str(pdf_path)
out_jsonl = str(out_jsonl)
Path(out_jsonl).parent.mkdir(parents=True, exist_ok=True)
records = 0
with pdfplumber.open(pdf_path) as pdf, open(out_jsonl, "w", encoding="utf-8") as f:
for page in pdf.pages:
try:
text = page.extract_text() or ""
except Exception:
text = ""
lines = []
if force_ocr or not text.strip():
# OCR
lines = _ocr_page(page, cfg)
else:
# Split extracted text into lines
pieces = text.splitlines()
line_no = 1
for ln in pieces:
ln = normalize_whitespace(ln)
if ln:
lines.append({"page": page.page_number, "line_no": line_no, "text": ln})
line_no += 1
for rec in lines:
f.write(json.dumps(rec, ensure_ascii=False) + "\n")
records += 1
print(f"Ingested {records} line records → {out_jsonl}")
