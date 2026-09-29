"""Exp03 D6: routing + caching cost saving (tests 60% claim directionally, offline prices)."""
import json, sys
sys.path.insert(0, "src")
from llmopsbench import count_tokens, estimate_cost, route_model, Cache

def run():
    with open("data/golden_set.jsonl") as f:
        gold = [json.loads(l) for l in f]
    # all-strong baseline
    base = sum(estimate_cost("strong-70b", count_tokens(g["question"]) + 400, 120) for g in gold)
    # routed + cached
    cache = Cache()
    cost = 0.0
    for g in gold:
        hit, _ = cache.get(g["question"])
        if hit:
            continue
        m = route_model(g["question"])
        c = estimate_cost(m, count_tokens(g["question"]) + (200 if m == "cheap-8b" else 400), 80 if m == "cheap-8b" else 120)
        cost += c
        cache.put(g["question"], "ans")
    # second pass to measure hit rate (repeat traffic)
    for g in gold:
        cache.get(g["question"])
    saving = (base - cost) / base if base else 0
    print(f"baseline=${base:.6f} routed=${cost:.6f} saving={saving*100:.1f}% hit_rate={cache.hit_rate():.3f}")
    return {"baseline": base, "routed": cost, "saving": saving, "hit_rate": cache.hit_rate()}

if __name__ == "__main__":
    print(run())
