"""Run all exps → results/summary.json (offline, deterministic)."""
import argparse, json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(os.path.join(os.path.dirname(__file__), ".."))

from exp01_retrieval_recall import run as r1
from exp02_prompt_stability import run as r2
from exp03_cost_routing import run as r3
from exp04_drift_detection import run as r4
from exp05_security_guardrails import run as r5
from exp06_end_to_end import run as r6

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="results/summary.json")
    a = ap.parse_args()
    summary = {
        "exp01_retrieval": dict(r1()),
        "exp02_prompt": dict(r2()),
        "exp03_cost": r3(),
        "exp04_drift": r4(),
        "exp05_security": {k: (str(v) if not isinstance(v, (int, float, dict)) else v) for k, v in r5().items()},
        "exp06_e2e": r6(),
    }
    os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
    with open(a.out, "w") as f:
        json.dump(summary, f, indent=2, default=str)
    print(f"WROTE {a.out}")

if __name__ == "__main__":
    main()
