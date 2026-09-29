# Contributing

1. Fork → branch (`git checkout -b feat/your-feature`) → PR with what changed + verification.
2. Every `configs/**` or prompt change must pass the eval-gate: `pytest -q && python experiments/run_all.py`.
3. No fabricated numbers: demo media regenerates from real output (`scripts/generate_demo.py`).
4. One-line rollback rule: any deploy must keep previous manifest one switch away.
5. We respond to PRs with verification logs, not vibes.
