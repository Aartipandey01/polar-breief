from typing import List
import re
from .utils import safe_import

PRO_MARKERS = [
r"supports?", r"affirm", r"uphold", r"in favor", r"benefit", r"compelling interest",
r"constitutionally sound", r"consistent with precedent"
]
CON_MARKERS = [
r"oppos(es|e)", r"revers(e|al)", r"strike down", r"burden", r"unconstitutional",
r"contrary to precedent", r"harms?", r"chilling effect"
]

def _rule_score(text: str) -> float:
t = text.lower()
pro = sum(bool(re.search(p, t)) for p in PRO_MARKERS)
con = sum(bool(re.search(p, t)) for p in CON_MARKERS)
return pro - con

def assign_polarity_labels(passages: List[dict]) -> List[dict]:
# Rule-based prior
out = []
for p in passages:
score = _rule_score(p["text"])
label = "Pro" if score >= 0 else "Con"
out.append({**p, "polarity": label, "polarity_conf": 0.5 + min(abs(score)/5, 0.45)})
# Optional NLI refinement
hf = safe_import("transformers")
if hf is not None:
try:
from transformers import pipeline
nli = pipeline("text-classification", model="facebook/bart-large-mnli")
premise_template_pro = "This passage supports the brief's position: {}"
premise_template_con = "This passage opposes the brief's position: {}"
for i, p in enumerate(out):
hyp = p["text"]
pro_logit = nli(premise_template_pro.format(hyp))[0]["score"]
con_logit = nli(premise_template_con.format(hyp))[0]["score"]
if con_logit > pro_logit and p["polarity"] != "Con":
out[i]["polarity"] = "Con"
elif pro_logit > con_logit and p["polarity"] != "Pro":
out[i]["polarity"] = "Pro"
out[i]["polarity_conf"] = max(out[i]["polarity_conf"], float(abs(pro_logit - con_logit)))
except Exception:
pass
return out
