from dataclasses import dataclass
from typing import Optional

@dataclass
class AppConfig:
ocr_lang: str = "eng"
dpi: int = 300
use_embeddings: bool = True # if sentence-transformers is available
use_llm_summary: bool = True # if transformers is available
max_passage_chars: int = 1200
min_passage_chars: int = 80
