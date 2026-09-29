"""LLMOpsBench-8 core library (offline, deterministic, no API keys)."""
from .retrieval import tokenize, tf_score, retrieve, recall_at_k, mrr, context_precision
from .evaluation import lcs_len, rouge_l, faithfulness_score, judge_agreement, golden_pass_rate
from .observability import Trace, new_trace_id
from .cost import count_tokens, estimate_cost, route_model, Cache
from .drift import rolling_mean, detect_drift
from .security import redact_pii, detect_injection, validate_schema
from .gateway import Gateway, Manifest

__all__ = [
    "tokenize", "tf_score", "retrieve", "recall_at_k", "mrr", "context_precision",
    "lcs_len", "rouge_l", "faithfulness_score", "judge_agreement", "golden_pass_rate",
    "Trace", "new_trace_id",
    "count_tokens", "estimate_cost", "route_model", "Cache",
    "rolling_mean", "detect_drift",
    "redact_pii", "detect_injection", "validate_schema",
    "Gateway", "Manifest",
]
