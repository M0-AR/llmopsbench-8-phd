"""D7: security — PII redaction, injection detection, schema validation (offline guardrails)."""
import re

EMAIL = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")
PHONE = re.compile(r"\b(?:\+?\d{1,3}[-.\s]?)?(?:\d{3}[-.\s]?\d{3}[-.\s]?\d{4})\b")
SSN = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")

INJECTION_PATTERNS = [
    "ignore previous instructions",
    "ignore all instructions",
    "system prompt",
    "jailbreak",
    "dan mode",
    "exfiltrate",
    "drop table",
    "delete from",
]

def redact_pii(text: str) -> tuple:
    """Returns (redacted_text, counts dict)."""
    counts = {"email": 0, "phone": 0, "ssn": 0}
    def _sub(pat, label, s):
        nonlocal counts
        found = pat.findall(s)
        key = label.lower()
        counts[key] = len(found)
        return pat.sub(f"[REDACTED_{label}]", s)
    # order matters to avoid double counting
    text = _sub(EMAIL, "EMAIL", text)
    text = _sub(PHONE, "PHONE", text)
    text = _sub(SSN, "SSN", text)
    return text, counts

def detect_injection(text: str) -> dict:
    low = text.lower()
    hits = [p for p in INJECTION_PATTERNS if p in low]
    return {"blocked": len(hits) > 0, "hits": hits}

def validate_schema(obj: dict, required: list) -> dict:
    missing = [k for k in required if k not in obj]
    return {"valid": len(missing) == 0, "missing": missing}
