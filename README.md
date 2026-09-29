# LLMOpsBench-8-PhD — Verified End-to-End LLMOps Benchmark for PhD Research

> From Abi Aryan *What Is LLMOps?* (O'Reilly May 2024) → verified against 2026-2027 live sources.
> No claim without verification. See `docs/VERIFICATION.md` for per-claim tool + date + URL.

**What this is:** a fully runnable, offline-first benchmark covering the 8 LLMOps lifecycle steps as 8 measurable dimensions (D1-D8), with 6 experiments (A-E systems), CI eval-gate, manifest versioning, gateway fallback, cost/latency/security tracking — everything needed to grow into a PhD paper.

**Verified consensus 2026 (triangulated from 24 sequential searches):**
- Prompts are code: version, review, canary 5%→25%→100%, shadow first, auto-rollback
- Eval-gate blocks merge on golden-set regression (50-100 min, 400 full)
- Trace everything with OTel `gen_ai.*`: prompt version, model pin, tokens, latency, retrieval IDs/scores, tool calls, cost, quality
- Cost is SLO: routing cheap/frontier + caching + per-request caps cuts 60-80%
- `486` benchmarks exist (benchlm.ai Sep 2026) but no unified ops benchmark — **this repo fills that gap**

## Quickstart (offline, no API key)

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pytest -q
python experiments/run_all.py --out results/summary.json
cat results/summary.json
```

## Repo map

```
configs/         manifest + prompt versions (v1/v2) — what ran, pinned
src/llmopsbench/ retrieval, evaluation, observability, cost, drift, security, gateway
experiments/     exp01-06 + run_all.py (A-E systems comparison)
data/            corpus.jsonl, golden_set.jsonl (50), multihop_mini.jsonl
tests/           pytest suite — eval-gate analogue (fails on regression)
docs/            RESEARCH.md, BENCHMARK.md, PHD_OUTLINE.md, REFERENCES.md, VERIFICATION.md
.github/workflows/ci.yml  prompt-change → eval-gate → block on drop
```

## The 8 dimensions (LLMOpsBench-8)

| ID | Lifecycle step | Primary metrics |
|---|---|---|
| D1 | Data / Retrieval | Context Precision/Recall, Recall@k, MRR, freshness lag, PII leak |
| D2 | Adaptation | Prompt stability (Δ pass-rate per commit), LoRA vs RAG trade-off |
| D3 | Evaluation validity | Judge-human agreement (target ≥0.8), noise robustness (TRIVIA+ style) |
| D4 | Faithfulness | Citation correctness, unsupported-claim rate, HHEM/FaithJudge analogue |
| D5 | Robustness / Drift | Provider-drift detection latency, retrieval-degradation slope |
| D6 | Efficiency | Cost/task, tokens in/out, p50/p95/p99, cache hit, routing accuracy |
| D7 | Security / Compliance | Injection block, PII redaction recall, audit completeness, AI BOM |
| D8 | Operability | Time-to-rollback, gate block rate, failure-mining conversion, MTTR |

Systems compared: A prompt-only, B naive RAG, C advanced RAG+rerank, D C+LoRA-style adapter, E D+gateway+guardrails+observability.

## Verified references

See `docs/REFERENCES.md` (23 entries with DOI/URL/cites) and `docs/VERIFICATION.md` (24 searches, one-at-a-time, with fallback `lite.duckduckgo.com`).

## License

MIT — for PhD reuse. Cite Aryan 2024 + this benchmark.
