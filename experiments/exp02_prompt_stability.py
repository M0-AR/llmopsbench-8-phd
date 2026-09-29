"""Exp02 D2/D4: prompt v1 vs v2 stability + faithfulness (offline answer simulator)."""
import json, sys
sys.path.insert(0, "src")
from llmopsbench import retrieve, rouge_l, faithfulness_score, golden_pass_rate

def load(p):
    with open(p) as f:
        return [json.loads(l) for l in f]

def simulate_answer(question, docs, prompt_version):
    """Deterministic stand-in for LLM: v1 returns top-1 chunk verbatim-ish, v2 adds citation + abstain."""
    r = retrieve(question, docs, top_k=2, rerank_boost=0.35 if prompt_version == "v2" else 0.0)
    if not r or r[0][1] < 0.05:
        return "Not enough evidence (stale index?)", []
    top = [d for d, _ in r]
    ans = top[0]["text"]
    if prompt_version == "v2":
        ans += f" [{top[0]['id']}]"
    return ans, top

def run():
    docs = load("data/corpus.jsonl"); gold = load("data/golden_set.jsonl")
    for pv in ("v1", "v2"):
        passes, rouges, faiths = [], [], []
        for g in gold:
            ans, top = simulate_answer(g["question"], docs, pv)
            rouges.append(rouge_l(ans, g["reference"]))
            faiths.append(faithfulness_score(ans, [d["text"] for d in top]))
            passes.append(rouges[-1] > 0.3 and faiths[-1] > 0.5)
        print(f"{pv}: pass={golden_pass_rate(passes):.3f} rouge={sum(rouges)/len(rouges):.3f} faith={sum(faiths)/len(faiths):.3f}")
        yield pv, {"pass": golden_pass_rate(passes)}

if __name__ == "__main__":
    list(run())
