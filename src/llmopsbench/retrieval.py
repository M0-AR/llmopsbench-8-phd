"""D1: retrieval — TF-overlap retriever + metrics (offline analogue of Faiss/Chroma + reranker)."""
import re
from collections import Counter

_WORD = re.compile(r"[a-z0-9]+")

def tokenize(text: str):
    return _WORD.findall(text.lower())

def tf_score(query_tokens, doc_tokens) -> float:
    if not query_tokens or not doc_tokens:
        return 0.0
    q = Counter(query_tokens)
    d = Counter(doc_tokens)
    # cosine over raw TF (deterministic, no IDF fitting needed for mini-bench)
    num = sum(q[t] * d.get(t, 0) for t in q)
    den_q = sum(v * v for v in q.values()) ** 0.5
    den_d = sum(v * v for v in d.values()) ** 0.5
    if den_q == 0 or den_d == 0:
        return 0.0
    return num / (den_q * den_d)

def retrieve(query: str, docs: list, top_k: int = 5, rerank_boost: float = 0.0):
    """docs: list of dicts {id, text}. Returns ranked list of (doc, score).

    rerank_boost: if >0, adds exact-phrase overlap bonus (analogue of cross-encoder reranker).
    """
    qt = tokenize(query)
    scored = []
    for d in docs:
        dt = tokenize(d["text"])
        s = tf_score(qt, dt)
        if rerank_boost > 0:
            # phrase bonus: fraction of query bigrams present in doc
            qb = set(zip(qt, qt[1:])) if len(qt) > 1 else set()
            db = set(zip(dt, dt[1:])) if len(dt) > 1 else set()
            overlap = len(qb & db) / max(1, len(qb))
            s = s + rerank_boost * overlap
        scored.append((d, s))
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:top_k]

def recall_at_k(retrieved_ids: list, relevant_ids: list, k: int) -> float:
    if not relevant_ids:
        return 1.0
    hit = len(set(retrieved_ids[:k]) & set(relevant_ids))
    return hit / len(relevant_ids)

def mrr(retrieved_ids: list, relevant_ids: list) -> float:
    rel = set(relevant_ids)
    for i, did in enumerate(retrieved_ids, 1):
        if did in rel:
            return 1.0 / i
    return 0.0

def context_precision(retrieved_ids: list, relevant_ids: list) -> float:
    if not retrieved_ids:
        return 0.0
    rel = set(relevant_ids)
    return len(set(retrieved_ids) & rel) / len(retrieved_ids)
