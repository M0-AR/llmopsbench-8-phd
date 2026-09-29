"""D8: gateway — manifest pinning, canary, fallback ladder, one-line rollback."""
from dataclasses import dataclass, field

@dataclass
class Manifest:
    manifest_id: str
    prompt_version: str
    model: str
    retrieval_top_k: int = 5
    rerank: bool = False
    max_tokens: int = 256

@dataclass
class Gateway:
    current: Manifest
    previous: Manifest = None
    history: list = field(default_factory=list)

    def deploy(self, new: Manifest):
        self.previous = self.current
        self.history.append(self.current)
        self.current = new

    def rollback(self):
        """One-line rollback to last-good manifest (2026 requirement)."""
        if self.previous is not None:
            self.current, self.previous = self.previous, self.current
            self.history.append(self.current)
        return self.current

    def fallback_ladder(self, primary_ok: bool, cheap_ok: bool = True):
        """strong → cheap → deterministic default (verified 2026 pattern)."""
        if primary_ok:
            return "strong-70b"
        if cheap_ok:
            return "cheap-8b"
        return "deterministic-default"

    def canary_split(self, request_hash: int, pct_new: int = 5) -> str:
        """Deterministic canary: request_hash %100 < pct → new else current."""
        return "new" if (request_hash % 100) < pct_new else "current"
