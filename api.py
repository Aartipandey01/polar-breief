from fastapi import FastAPI
from pydantic import BaseModel
from pathlib import Path
from polarbrief.ingest import ingest_pdf_to_jsonl
from polarbrief.segment import build_passages
from polarbrief.rank import rank_passages_topk
from polarbrief.polarity import assign_polarity_labels
from polarbrief.summarize import summarize_arguments
from polarbrief.report import save_arguments_json, save_arguments_pdf
from polarbrief.config import AppConfig

app = FastAPI(title="PolarBrief Argument Miner API")

class ProcessRequest(BaseModel):
pdf_path: str
out_dir: str | None = "outputs"
force_ocr: bool | None = False

@app.post("/process")
def process(req: ProcessRequest):
cfg = AppConfig()
out_dir = Path(req.out_dir or "outputs")
out_dir.mkdir(parents=True, exist_ok=True)
ingest_path = out_dir / "ingest.jsonl"
ingest_pdf_to_jsonl(req.pdf_path, str(ingest_path), force_ocr=req.force_ocr, cfg=cfg)
passages = build_passages(str(ingest_path))
ranked = rank_passages_topk(passages, k=10)
labeled = assign_polarity_labels(ranked)
summarized = summarize_arguments(labeled, max_words=75)
json_path = out_dir / "arguments.json"
pdf_path = out_dir / "arguments.pdf"
save_arguments_json(summarized, str(json_path))
save_arguments_pdf(summarized, str(pdf_path))
return {
"status": "ok",
"json": str(json_path),
"pdf": str(pdf_path),
"message": "Processing complete"
}
