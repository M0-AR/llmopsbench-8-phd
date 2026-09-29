"""D8/D6: observability — OTel gen_ai.*-style trace (offline, JSON-serializable)."""
import time
import uuid

def new_trace_id() -> str:
    return uuid.uuid4().hex[:16]

class Trace:
    def __init__(self, request_id: str = None, prompt_version: str = "v1",
                 model: str = "cheap-8b", manifest_id: str = "m0"):
        self.request_id = request_id or new_trace_id()
        self.prompt_version = prompt_version
        self.model = model
        self.manifest_id = manifest_id
        self.spans = []
        self.t0 = time.time()

    def span(self, name: str, **attrs):
        s = {"name": name, "t_ms": round((time.time() - self.t0) * 1000, 2)}
        s.update(attrs)
        self.spans.append(s)
        return s

    def to_dict(self):
        return {
            "request_id": self.request_id,
            "gen_ai.prompt_version": self.prompt_version,
            "gen_ai.model": self.model,
            "manifest_id": self.manifest_id,
            "spans": self.spans,
        }
