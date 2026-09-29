"""Exp04 D5: provider-drift + retrieval-degradation detection (rolling-mean alert)."""
import sys
sys.path.insert(0, "src")
from llmopsbench import rolling_mean, detect_drift

def run():
    baseline = 0.85
    # week 1-4 stable, week 5 provider update drops quality 12%
    scores = [0.86, 0.84, 0.85, 0.86, 0.85, 0.75, 0.74, 0.76, 0.75]
    roll = rolling_mean(scores, 3)
    res = detect_drift(baseline, roll, tol=0.08)
    print(f"baseline={baseline} roll={ [round(x,3) for x in roll] } drift={res}")
    # retrieval degradation slope: ctx_prec 0.9@2k docs -> 0.55@50k docs
    slope = (0.55 - 0.90) / (50000 - 2000)
    print(f"retrieval_degradation_slope={slope:.2e} per doc")
    return {"drift": res, "slope": slope}

if __name__ == "__main__":
    print(run())
