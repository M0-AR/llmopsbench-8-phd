# VHS tape — reproducible terminal demo (verified against charmbracelet/vhs docs).
# Regenerate without re-recording: `vhs assets/demo.tape` (requires vhs + ttyd + ffmpeg).
# CI-friendly: keep GIF under 5MB, 10-20s, payoff first (2026 GIF guidance).
Output assets/demo.gif
Output assets/demo.mp4
Set Width 960
Set Height 540
Set FontSize 22
Set Framerate 30
Set Theme "Catppuccin Frappe"
Type "pip install -r requirements.txt && pytest -q" Enter
Sleep 2s
Type "python experiments/run_all.py --out results/summary.json" Enter
Sleep 4s
Type "cat results/summary.json | head -20" Enter
Sleep 3s
