"""Exp06 D1-D8 end-to-end: systems A-E comparison with manifest + trace + gateway."""
import json, sys
sys.path.insert(0, "src")
from llmopsbench import (retrieve, rouge_l, faithfulness_score, Trace, count_tokens,
    estimate_cost, route_model, Gateway, Manifest, redact_pii, detect_injection)

def load(p):
    with open(p) as f:
        return [json.loads(l) for l in f]

SYSTEMS = {
    "A_prompt_only": {"retrieval": False, "rerank": False, "model": "strong-70b", "guard": False},
    "B_naive_RAG": {"retrieval": True, "rerank": False, "model": "strong-70b", "guard": False},
    "C_adv_RAG": {"retrieval": True, "rerank": True, "model": "strong-70b", "guard": False},
    "D_C_plus_adapter": {"retrieval": True, "rerank": True, "model": "strong-70b", "guard": False, "adapter_boost": 0.05},
    "E_full_ops": {"retrieval": True, "rerank": True, "model": "routed", "guard": True},
}

def answer_for(sysname, cfg, q, docs):
    trace = Trace(prompt_version="v2", model=cfg["model"], manifest_id="m-e2e")
    if cfg["guard"] and detect_injection(q)["blocked"]:
        trace.span("guardrail", action="block")
        return "Refused (injection).", [], trace, 0.0
    if not cfg["retrieval"]:
        # parametric only: generic sentence (low grounding by design)
        ans = "LLMOps is about operating large language models in production."
        trace.span("llm", tokens=count_tokens(ans))
        return ans, [], trace, estimate_cost("strong-70b", count_tokens(q), count_tokens(ans))
    r = retrieve(q, docs, top_k=5, rerank_boost=0.35 if cfg["rerank"] else 0.0)
    top = [d for d, _ in r]
    ans = top[0]["text"] + f" [{top[0]['id']}]" if top else "Not enough evidence"
    if cfg.get("adapter_boost"):
        ans += " Adapter-tuned tone."
    model = route_model(q) if cfg["model"] == "routed" else cfg["model"]
    cost = estimate_cost(model, count_tokens(q) + 300, count_tokens(ans))
    trace.span("retrieval", ids=[d["id"] for d in top])
    trace.span("llm", model=model, tokens=count_tokens(ans))
    if cfg["guard"]:
        ans, _ = redact_pii(ans)
    return ans, top, trace, cost

def run():
    docs = load("data/corpus.jsonl"); gold = load("data/golden_set.jsonl")
    gw = Gateway(current=Manifest("m-e2e", "v2", "routed", 5, True))
    out = {}
    for name, cfg in SYSTEMS.items():
        rouges = faiths = cost = 0.0
        for g in gold:
            ans, top, tr, c = answer_for(name, cfg, g["question"], docs)
            rouges += rouge_l(ans, g["reference"])
            faiths += faithfulness_score(ans, [d["text"] for d in top])
            cost += c
        n = len(gold)
        out[name] = {"rouge": rouges/n, "faith": faiths/n, "cost": cost}
        print(f"{name}: rouge={rouges/n:.3f} faith={faiths/n:.3f} cost=${cost:.6f}")
    # rollback demo
    gw.deploy(Manifest("m-e2e-bad", "v3", "strong-70b", 5, True))
    gw.rollback()
    print(f"gateway_rollback_to={gw.current.manifest_id}")
    out["gateway_rollback_to"] = gw.current.manifest_id
    return out

if __name__ == "__main__":
    print(run())
