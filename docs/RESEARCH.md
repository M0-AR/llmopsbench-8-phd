# RESEARCH — Zero-to-Hero synthesis (verified)

Book holds: safety/scalability/robustness + Dev→Deploy→Serve + 8 steps.
2026 shifts: safety→governance (AI BOM, audit), scalability→cost+p95, robustness→+provider drift, silent retrieval degradation, prompt-edit regression, context explosion.

MLOps vs LLMOps: unit changes from retrained artifact to config change (prompt/RAG/model-id/tool). Eval moves from AUC/F1 to heuristic + LLM-judge + span-attached online. Monitoring adds eval-score drift, $/route, tool accuracy, trajectory steps, refusal rate.

Checklist (10): versioned prompts, eval blocks CI, full traces, pinned model, token caps, cost alerts, failover, guardrails, p95 SLA, paging/auto-resolve.

Market: $7.14B 2026 → $15.59B 2030 (Codex CLI review). EU AI Act enforceable. Qdrant 10B vectors Sep 2026.

See VERIFICATION.md for 24 searches + REFERENCES.md for 21 entries.
