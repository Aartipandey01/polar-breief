import json, random, argparse, csv, pathlib

def load_pred(path: str):
with open(path, "r", encoding="utf-8") as f:
return json.load(f)

def load_gold(path: str):
rows = []
with open(path, newline="", encoding="utf-8") as f:
for r in csv.DictReader(f):
rows.append(r)
return rows

def relevance_at_10(pred, gold):
gold_map = {int(r["argument_id"]): int(r["relevant"]) for r in gold}
top_ids = [int(x.get("argument_id", i)) for i, x in enumerate(pred[:10])]
rel = [gold_map.get(i, 0) for i in top_ids]
return sum(rel) / max(1, len(top_ids))

def citation_accuracy_sample(pred, sample_k=5):
# Automated sanity check: citations present and formatted page:start-end
ok = 0
total = 0
for x in random.sample(pred, min(sample_k, len(pred))):
cits = x.get("citations", [])
for cit in cits:
total += 1
ok += 1 if (":" in cit and "-" in cit) else 0
return ok / max(1, total)

def main():
ap = argparse.ArgumentParser()
ap.add_argument("--pred", required=True)
ap.add_argument("--gold", required=True)
args = ap.parse_args()
pred = load_pred(args.pred)
gold = load_gold(args.gold)
r10 = relevance_at_10(pred, gold)
ca = citation_accuracy_sample(pred)
print(f"Relevance@10: {r10:.3f}")
print(f"Citation Accuracy (automated check): {ca:.3f}")
print("NOTE: For a proper 95% citation accuracy, perform human spot-checks on sampled citations.")

if name == "main":
main()
