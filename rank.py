from typing import List
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from .config import AppConfig
from .utils import safe_import

def mmr(doc_embedding, candidate_embeddings, top_n=10, diversity=0.5):
# Maximal Marginal Relevance selection
selected = []
candidates_idx = list(range(len(candidate_embeddings)))
similarity_to_doc = cosine_similarity(candidate_embeddings, doc_embedding.reshape(1,-1)).ravel()
selected.append(int(np.argmax(similarity_to_doc)))
candidates_idx.remove(selected[0])
for _ in range(top_n - 1):
if not candidates_idx:
break
candidate_similarities = cosine_similarity(candidate_embeddings[candidates_idx], candidate_embeddings[selected])
min_sim = candidate_similarities.max(axis=1)
relevance = similarity_to_doc[candidates_idx]
mmr_scores = (1 - diversity) * relevance - diversity * min_sim
selected.append(candidates_idx[int(np.argmax(mmr_scores))])
candidates_idx.remove(selected[-1])
return selected

def rank_passages_topk(passages: List[dict], k: int=10, query_hint: str|None=None) -> List[dict]:
if not passages:
return []
texts = [p["text"] for p in passages]
cfg = AppConfig()
# Build a pseudo-query from frequent legal terms to steer TF-IDF a bit
query = query_hint or "brief court argument support opposition motion holding precedent standard test"
# TF-IDF baseline
vectorizer = TfidfVectorizer(ngram_range=(1,2), max_features=30000, stop_words='english')
X = vectorizer.fit_transform(texts + [query])
doc_vecs = X[:-1]
query_vec = X[-1]
sim = (doc_vecs @ query_vec.T).toarray().ravel()
# Select with MMR to improve diversity
doc_emb = query_vec.toarray().ravel()
cand_emb = doc_vecs.toarray()
idxs = mmr(doc_emb, cand_emb, top_n=min(k, len(passages)), diversity=0.55)
ranked = [ {**passages[i], "score": float(sim[i])} for i in idxs ]
# Optional: try sentence-transformers rerank
if cfg.use_embeddings:
st = safe_import("sentence_transformers")
if st is not None:
try:
from sentence_transformers import SentenceTransformer, util
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
q_emb = model.encode([query], convert_to_tensor=True)
p_emb = model.encode(texts, convert_to_tensor=True)
scores = util.cos_sim(q_emb, p_emb).cpu().numpy().ravel()
for r in ranked:
r["score"] = float(scores[texts.index(r["text"])]) * 1.5 + r["score"] # blend
ranked = sorted(ranked, key=lambda x: x["score"], reverse=True)[:k]
except Exception:
pass
# Ensure exactly k items if possible
ranked = sorted(ranked, key=lambda x: x["score"], reverse=True)[:k]
# Attach stable ids
for i, r in enumerate(ranked):
r["argument_id"] = i
return ranked
