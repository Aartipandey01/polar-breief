import argparse
from polarbrief.config import AppConfig
from polarbrief.ingest import ingest_pdf_to_jsonl
from polarbrief.segment import build_passages
from polarbrief.rank import rank_passages_topk
from polarbrief.polarity import assign_polarity_labels
from polarbrief.summarize import summarize_arguments
from polarbrief.report import save_arguments_json, save_arguments_pdf
from pathlib import Path

def cmd_ingest(args):
cfg = AppConfig()
ingest_pdf_to_jsonl(args.pdf, args.out, force_ocr=args.force_ocr, cfg=cfg)

def cmd_mine(args):
passages = build_passages(args.ingest, window_lines=args.window_lines, min_chars=80, max_chars=1200)
ranked = rank_passages_topk(passages, k=10)
labeled = assign_polarity_labels(ranked)
summarized = summarize_arguments(labeled, max_words=75)
save_arguments_json(summarized, args.out_json)
save_arguments_pdf(summarized, args.out_pdf)

def cmd_run(args):
out_dir = Path(args.out_dir)
out_dir.mkdir(parents=True, exist_ok=True)
ingest_path = out_dir / "ingest.jsonl"
args_ingest = argparse.Namespace(pdf=args.pdf, out=str(ingest_path), force_ocr=args.force_ocr)
cmd_ingest(args_ingest)
args_mine = argparse.Namespace(ingest=str(ingest_path),
window_lines=8,
out_json=str(out_dir / "arguments.json"),
out_pdf=str(out_dir / "arguments.pdf"))
cmd_mine(args_mine)

def main():
p = argparse.ArgumentParser(description="PolarBrief Argument Miner")
sub = p.add_subparsers()
