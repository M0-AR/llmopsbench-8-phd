# BENCHMARK SPEC — LLMOpsBench-8

Offline-first, deterministic, no API keys. Each dimension has metric + dataset + experiment + gate.

- D1 Retrieval: Recall@k, MRR, ctx precision. Data: corpus.jsonl (12), golden (50), multihop (3). Exp01. Gate: rerank ≥ naive.
- D2 Adaptation: prompt pass-rate Δ v1→v2, adapter boost. Exp02. Gate: v2 ≥ v1.
- D3 Validity: judge-human agreement (1-MAE), noise test (drop tokens). Target ≥0.8.
- D4 Faithfulness: grounded-token fraction (HHEM analogue), citation presence. Exp06. Gate: E ≥ B.
- D5 Drift: rolling-mean(3) breach at tol 0.08 (≈8% slide, matches 2026 guidance). Exp04 must breach on synthetic provider update, not breach when stable.
- D6 Efficiency: $/task, tokens, p95 (simulated via token length), cache hit, routing accuracy. Exp03 must show routed < baseline.
- D7 Security: injection block rate, PII redaction recall=1.0 on seeded PII, schema fail-closed. Exp05.
- D8 Operability: rollback returns m1, fallback ladder strong→cheap→default, canary deterministic. Covered in unit tests + Exp06.

Systems A-E defined in exp06. Hypotheses H1-H5 in README map to gates above.

Reproduce: `pytest -q && python experiments/run_all.py --out results/summary.json`
