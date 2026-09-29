"""D3/D4: evaluation — ROUGE-L, faithfulness heuristic, judge agreement, golden pass-rate."""
from .retrieval import tokenize

def lcs_len(a: list, b: list) -> int:
    m, n = len(a), len(b)
    prev = [0] * (n + 1)
    for i in range(1, m + 1):
        cur = [0] * (n + 1)
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                cur[j] = prev[j - 1] + 1
            else:
                cur[j] = prev[j] if prev[j] >= cur[j - 1] else cur[j - 1]
        prev = cur
    return prev[n]

def rouge_l(candidate: str, reference: str) -> float:
    ct, rt = tokenize(candidate), tokenize(reference)
    if not ct or not rt:
        return 0.0
    lcs = lcs_len(ct, rt)
    prec = lcs / len(ct)
    rec = lcs / len(rt)
    if prec + rec == 0:
        return 0.0
    return 2 * prec * rec / (prec + rec)

def faithfulness_score(answer: str, evidence_texts: list) -> float:
    """Offline analogue of HHEM/FaithJudge: fraction of answer tokens grounded in evidence.

    Grounded = token appears in concatenated evidence. Deterministic and explainable.
    """
    at = tokenize(answer)
    if not at:
        return 0.0
    ev = set()
    for e in evidence_texts:
        ev.update(tokenize(e))
    hit = sum(1 for t in at if t in ev)
    return hit / len(at)

def judge_agreement(judge_scores: list, human_scores: list) -> float:
    """Pearson-free agreement: 1 - mean abs error on 0..1 scale (target >=0.8 maps to MAE<=0.2)."""
    assert len(judge_scores) == len(human_scores) and len(judge_scores) > 0
    mae = sum(abs(j - h) for j, h in zip(judge_scores, human_scores)) / len(judge_scores)
    return 1.0 - mae

def golden_pass_rate(results: list) -> float:
    """results: list of bool."""
    if not results:
        return 0.0
    return sum(1 for r in results if r) / len(results)
