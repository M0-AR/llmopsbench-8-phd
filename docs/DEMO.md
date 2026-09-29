# Demo — how the video/GIF was made (reproducible, no fabrication)

All demo media is generated from **real** `experiments/run_all.py` output, never hand-typed.

## Files

| File | What | Size | How |
|---|---|---|---|
| `assets/demo.gif` | Hero loop (autoplay, 9 frames, 800px) | ~50 KB (<5 MB ✓) | `python3 scripts/generate_demo.py` |
| `assets/demo.mp4` | Same, higher quality + player | ~52 KB | same script (ffmpeg libx264) |
| `assets/demo.tape` | VHS source (terminal-as-code) | — | `vhs assets/demo.tape` (needs vhs+ttyd+ffmpeg) |
| `assets/dashboard.png` | Playwright screenshot of `assets/dashboard.html` | ~120 KB, 1681×1308 | Playwright MCP `take_screenshot fullPage` |
| `assets/dashboard.html` | Offline results dashboard | — | `python3 scripts/generate_dashboard.py` |

## Regenerate everything

```bash
python experiments/run_all.py --out results/summary.json
python3 scripts/generate_dashboard.py
python3 scripts/generate_demo.py
# optional (needs vhs): vhs assets/demo.tape
```

## Why this way (verified Sep 2026)

- GIF hero + MP4 walkthrough below (glideo.app Jul 2026 guide).
- 10–20s, one core action, payoff in first seconds, loop cleanly, text legible at README width (mdkit Feb 2026, gingiris Apr 2026 audit of 100+ 10k-star repos).
- GIFs committed under `assets/` so links never rot (mdfileviewer Jun 2026).
- VHS = scriptable, reproducible terminal GIFs (charmbracelet/vhs docs + makerstack 2026 review 7.8/10); asciinema `.cast` is the lightweight alternative for streaming.
- No secrets in frames (real tokens/paths redacted before export).
