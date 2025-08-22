
import json
from .utils import sliding_windows, normalize_whitespace

def _load_lines(jsonl_path: str) -> list[dict]:
lines = []
with open(jsonl_path, "r", encoding="utf-8") as f:
for line in f:
obj = json.loads(line)
lines.append(obj)
return lines

def build_passages(jsonl_path: str, window_lines: int=8, min_chars: int=80, max_chars: int=1200):
lines = _load_lines(jsonl_path)
passages = []
# Group by page to keep citations tight
by_page = {}
for r in lines:
by_page.setdefault(r["page"], []).append(r)
for page, page_lines in by_page.items():
page_lines = sorted(page_lines, key=lambda x: x["line_no"])
for chunk in sliding_windows(page_lines, window_lines):
text = normalize_whitespace(" ".join([c["text"] for c in chunk]))
if len(text) < min_chars:
continue
if len(text) > max_chars:
text = text[:max_chars]
start_line = chunk[0]["line_no"]
end_line = chunk[-1]["line_no"]
passages.append({
"page": page,
"start_line": start_line,
"end_line": end_line,
"text": text,
"citation": f"{page}:{start_line}-{end_line}"
})
return passages
