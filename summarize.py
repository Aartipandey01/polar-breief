from typing import List
from .utils import safe_import
import re

def _word_limiter(text: str, max_words: int) -> str:
words = re.findall(r"\S+", text)
return " ".join(words[:max_words])

def _classical_summarize(text: str, max_words: int=75) -> str:
# Extremely simple: return the first sentences trimmed to max_words
# (You can extend with TextRank or centroid-based extractive methods)
return _word_limiter(text, max_words)

def summarize_arguments(passages: List[dict], max_words: int=75) -> List[dict]:
out = []
hf = safe_import("transformers")
if hf is not None:
try:
from transformers import pipeline
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6", truncation=True)
except Exception:
summarizer = None
else:
summarizer = None
