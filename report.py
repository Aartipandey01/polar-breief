import json
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

def save_arguments_json(items: list[dict], path: str):
# Keep only expected export fields
export = []
for x in items:
export.append({
"argument_id": x.get("argument_id"),
"summary": x.get("summary"),
"polarity": x.get("polarity"),
"citations": [x.get("citation")],
"score": x.get("score", None),
})
with open(path, "w", encoding="utf-8") as f:
json.dump(export, f, ensure_ascii=False, indent=2)
print(f"Wrote JSON → {path}")

def save_arguments_pdf(items: list[dict], path: str):
c = canvas.Canvas(path, pagesize=LETTER)
width, height = LETTER
margin = 0.75 * inch
x = margin
y = height - margin
c.setFont("Helvetica-Bold", 16)
c.drawString(x, y, "PolarBrief: Top 10 Arguments (Pro/Con)")
y -= 0.4 * inch
c.setFont("Helvetica", 10)
for i, it in enumerate(items):
block = f"#{i+1} [{it.get('polarity','?')}]\nSummary: {it.get('summary','')}\nCitation(s): {', '.join([it.get('citation','')])}\nScore: {it.get('score',0):.4f}"
for line in block.splitlines():
if y < margin + 1*inch:
c.showPage()
y = height - margin
c.setFont("Helvetica", 10)
c.drawString(x, y, line)
y -= 14
y -= 8 # spacing
c.save()
print(f"Wrote PDF → {path}")
