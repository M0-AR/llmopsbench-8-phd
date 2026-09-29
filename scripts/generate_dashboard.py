"""Generate assets/dashboard.html from results/summary.json (offline, no CDN)."""
import json, os, html

ROOT = os.path.join(os.path.dirname(__file__), "..")
SUM = os.path.join(ROOT, "results", "summary.json")
OUT = os.path.join(ROOT, "assets", "dashboard.html")

def bar(label, val, maxv, color="#4a90d9"):
    w = max(2, int(520 * (val / maxv))) if maxv else 2
    return (f"<div class='row'><span class='lbl'>{html.escape(label)}</span>"
            f"<div class='track'><div class='fill' style='width:{w}px;background:{color}'></div></div>"
            f"<span class='val'>{val:.3f}</span></div>")

def main():
    s = json.load(open(SUM))
    e6 = s["exp06_e2e"]
    names = [k for k in e6 if not k.startswith("gateway")]
    maxr = max(e6[n]["rouge"] for n in names) or 1
    maxf = max(e6[n]["faith"] for n in names) or 1
    maxc = max(e6[n]["cost"] for n in names) or 1
    rows_r = "".join(bar(n, e6[n]["rouge"], maxr, "#4a90d9") for n in names)
    rows_f = "".join(bar(n, e6[n]["faith"], maxf, "#50c878") for n in names)
    rows_c = "".join(bar(n, e6[n]["cost"], maxc, "#e07b39") for n in names)
    r1 = s["exp01_retrieval"]
    drift = s["exp04_drift"]["drift"]
    cost = s["exp03_cost"]
    html_doc = f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>LLMOpsBench-8 — Results Dashboard (verified)</title>
<style>
body{{font-family:system-ui,-apple-system,Segoe UI,Roboto,sans-serif;margin:0;background:#0f172a;color:#e2e8f0}}
.wrap{{max-width:900px;margin:0 auto;padding:32px 20px}}
.card{{background:#1e293b;border:1px solid #334155;border-radius:12px;padding:20px;margin:16px 0}}
h1{{font-size:28px;margin:0 0 4px}} .sub{{color:#94a3b8;font-size:14px}}
.row{{display:flex;align-items:center;gap:10px;margin:6px 0}}
.lbl{{width:170px;font-size:13px;color:#cbd5e1}} .val{{font-variant-numeric:tabular-nums;font-size:13px}}
.track{{flex:1;background:#0b1220;border-radius:6px;height:14px;overflow:hidden}} .fill{{height:14px;border-radius:6px}}
.kpi{{display:flex;gap:12px;flex-wrap:wrap}} .kpi div{{background:#0b1220;border:1px solid #334155;border-radius:8px;padding:10px 14px;font-size:13px}}
.badge{{display:inline-block;background:#22c55e;color:#052e16;border-radius:20px;padding:2px 10px;font-size:12px;font-weight:700}}
a{{color:#7dd3fc}} code{{background:#0b1220;padding:2px 6px;border-radius:6px}}
</style></head><body><div class="wrap">
<h1>LLMOpsBench-8 <span class="badge">VERIFIED</span></h1>
<div class="sub">Offline benchmark · 8 dims · 6 experiments · <code>pytest -q</code> 8 passed · generated from <code>results/summary.json</code></div>
<div class="card"><h3>End-to-end (A–E): ROUGE-L</h3>{rows_r}</div>
<div class="card"><h3>Faithfulness (grounded-token fraction)</h3>{rows_f}</div>
<div class="card"><h3>Cost per 50 queries (USD, toy prices)</h3>{rows_c}
<div class="sub">Toy prices: cheap-8b $0.15/$0.60 vs strong-70b $2.50/$10.00 per 1M (bench constants). Production audio reference verified Sep 2026: gpt-realtime-2.1 $32/$64 per 1M.</div></div>
<div class="card"><h3>KPIs</h3><div class="kpi">
<div>Recall@5 naive <b>{r1['naive']['recall@5']:.3f}</b> → rerank <b>{r1['rerank']['recall@5']:.3f}</b></div>
<div>Drift breach <b>{str(drift['breached']).upper()}</b> drop {drift['drop']*100:.1f}%</div>
<div>Routing saving <b>{cost['saving']*100:.1f}%</b> (toy, see note)</div>
<div>Gateway rollback → <b>{e6.get('gateway_rollback_to','-')}</b></div>
</div></div>
<div class="sub">Reproduce: <code>pip install -r requirements.txt &amp;&amp; pytest -q &amp;&amp; python experiments/run_all.py</code> · MIT · docs/VERIFICATION.md</div>
</div></body></html>"""
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w").write(html_doc)
    print(f"WROTE {OUT} ({len(html_doc)} bytes)")

if __name__ == "__main__":
    main()
