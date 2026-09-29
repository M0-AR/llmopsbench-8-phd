"""Exp01 D1: naive TF retriever vs +rerank on golden_set. Verifies reranker lift (2026 claim)."""
import json, sys
sys.path.insert(0, "src")
from llmopsbench import retrieve, recall_at_k, mrr, context_precision

def load(p):
    with open(p) as f:
        return [json.loads(l) for l in f]

def run(corpus_p="data/corpus.jsonl", golden_p="data/golden_set.jsonl"):
    docs = load(corpus_p); gold = load(golden_p)
    for name, boost in [("naive", 0.0), ("rerank", 0.35)]:
        rs = ms = ps = 0.0
        for g in gold:
            r = retrieve(g["question"], docs, top_k=5, rerank_boost=boost)
            ids = [d["id"] for d, _ in r]
            rs += recall_at_k(ids, g["relevant_ids"], 5)
            ms += mrr(ids, g["relevant_ids"])
            ps += context_precision(ids, g["relevant_ids"])
        n = len(gold)
        print(f"{name}: recall@5={rs/n:.3f} mrr={ms/n:.3f} ctx_prec={ps/n:.3f}")
        yield name, {"recall@5": rs/n, "mrr": ms/n, "ctx_prec": ps/n}

if __name__ == "__main__":
    list(run())
