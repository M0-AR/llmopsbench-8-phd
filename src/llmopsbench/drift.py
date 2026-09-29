"""D5: drift — rolling-mean + threshold alerts (analogue of PSI/KS for judge scores)."""
def rolling_mean(values: list, window: int) -> list:
    out = []
    for i in range(len(values)):
        w = values[max(0, i - window + 1): i + 1]
        out.append(sum(w) / len(w))
    return out

def detect_drift(baseline: float, current_roll: list, tol: float = 0.08) -> dict:
    """tol=0.08 mirrors 2026 guidance: alert on ~8% quality slide or 5-10% band.

    Returns {breached: bool, drop: float, last: float}.
    """
    if not current_roll:
        return {"breached": False, "drop": 0.0, "last": baseline}
    last = current_roll[-1]
    drop = (baseline - last) / baseline if baseline else 0.0
    return {"breached": drop >= tol, "drop": drop, "last": last}
