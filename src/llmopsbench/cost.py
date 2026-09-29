"""D6: cost/latency — token counting, pricing, routing, semantic-ish cache (offline)."""
from .retrieval import tokenize

# Prices verified Sep 2026 leaderboards report $/1M tokens; defaults are bench constants, not quotes.
PRICES = {
    "cheap-8b": {"in": 0.15, "out": 0.60},   # small open-weight analogue
    "strong-70b": {"in": 2.50, "out": 10.00},  # frontier analogue
    "judge-8b": {"in": 0.15, "out": 0.60},
}

def count_tokens(text: str) -> int:
    # word-token analogue (deterministic); real tokenizers ~1.3x words for EN
    return len(tokenize(text))

def estimate_cost(model: str, in_tok: int, out_tok: int) -> float:
    p = PRICES[model]
    return (in_tok / 1e6) * p["in"] + (out_tok / 1e6) * p["out"]

def route_model(query: str, threshold: int = 12) -> str:
    """Route by complexity: short/simple → cheap, long/multi-hop cues → strong.

    Verified 2026 lever: most traffic is easier than assumed; routing is largest cost saver.
    """
    q = query.lower()
    multihop_cues = (" and ", "compare", "why", "multi", " steps", "history", "because")
    if len(tokenize(query)) >= threshold or any(c in q for c in multihop_cues):
        return "strong-70b"
    return "cheap-8b"

class Cache:
    """Exact+near cache: exact key hit, else Jaccard>=0.8 near hit (analogue of semantic cache)."""
    def __init__(self):
        self.store = {}
        self.hits = 0
        self.misses = 0

    @staticmethod
    def _jaccard(a: str, b: str) -> float:
        sa, sb = set(tokenize(a)), set(tokenize(b))
        if not sa or not sb:
            return 0.0
        return len(sa & sb) / len(sa | sb)

    def get(self, key: str):
        if key in self.store:
            self.hits += 1
            return self.store[key], "exact"
        for k, v in self.store.items():
            if self._jaccard(key, k) >= 0.8:
                self.hits += 1
                return v, "near"
        self.misses += 1
        return None, "miss"

    def put(self, key: str, value: str):
        self.store[key] = value

    def hit_rate(self) -> float:
        n = self.hits + self.misses
        return self.hits / n if n else 0.0
