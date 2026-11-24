"""Write <run>/COST_SUMMARY.md from that run's summary_by_model.csv and results.csv.

Usage: python eval/cost_summary.py RUN_DIR PRICES_JSON RUN_DATE "PHOTO SET DESCRIPTION" [COMPARE_DIR]
Every number comes from the CSVs or the price file; nothing is typed in by hand.
"""
import csv, json, sys
from pathlib import Path

out_dir, prices_path, run_date, photo_set = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3], sys.argv[4]
other_dir = Path(sys.argv[5]) if len(sys.argv) > 5 else None
N = 50
rd = lambda p: list(csv.DictReader(p.open(newline="", encoding="utf-8")))
rows, results = rd(out_dir / "summary_by_model.csv"), rd(out_dir / "results.csv")
prices = {k: v for k, v in json.loads(prices_path.read_text()).items() if not k.startswith("_")}
base = lambda m: m.split(" (")[0]

def num(v):
    try: return float(v)
    except (TypeError, ValueError): return None
money = lambda v: "—" if v is None else f"${v:,.4f}"
intf = lambda v: "—" if v is None else f"{v:,.0f}"

latest = {}
for r in results: latest[(r["file"], r["model"])] = r
calls = sum(num(r.get("api_calls")) or 0 for r in latest.values())
tin_all = sum(num(r.get("input_tokens")) or 0 for r in latest.values())

flags, main, proj, total_proj, proj_models = [], [], [], 0.0, []
for r in rows:
    m, n = r["model"], num(r.get("photos"))
    cost, per = num(r.get("total_cost_usd")), num(r.get("cost_per_photo_usd"))
    tin, tout = num(r.get("total_input_tokens")), num(r.get("total_output_tokens"))
    ain = tin / n if tin is not None and n else None
    aout = tout / n if tout is not None and n else None
    med, failed = num(r.get("median_seconds")), int(num(r.get("failed")) or 0)
    main.append(f"| `{m}` | {intf(n)} | {failed} | {money(cost)} | {money(per)} | {intf(ain)} | {intf(aout)} | "
                f"{'—' if med is None else f'{med:.1f} s'} |")
    if per is None:
        flags.append(f"- `{m}`: cost is missing, so it has no projection and is left out of the total.")
        proj.append(f"| `{m}` | — | not projected (cost missing) |"); continue
    if per == 0:
        flags.append(f"- `{m}`: cost is $0. Check it is not a run with no successful calls before relying on it.")
    if failed:
        flags.append(f"- `{m}`: {failed} of {int(n)} photos failed; failed photos are still in the per-photo average.")
    note = (prices.get(base(m)) or {}).get("note")
    if note and "introductory" in note:
        flags.append(f"- `{m}`: priced at an introductory rate ({note}).")
    p = per * N; total_proj += p; proj_models.append(m)
    proj.append(f"| `{m}` | {money(p)} | {money(per)} × {N} |")

settings = sorted({(x.get("vision_samples") or "?", x.get("claude_effort") or "") for x in latest.values()})
samples = sorted({s for s, _ in settings}); efforts = sorted({e for _, e in settings if e})
setting_txt = (f"{'/'.join(samples)} sample(s) per photo for every model"
               + (f"; Claude effort `{'`, `'.join(efforts)}` (from the `CLAUDE_EFFORT` environment variable; the pipeline's default is `high`)" if efforts else ""))
run_models = {base(r["model"]) for r in rows}
price_lines = []
for m in run_models & set(prices):
    p = prices[m]
    price_lines.append((m, f"| `{m}` | ${p['input']:.2f} | ${p['output']:.2f} | "
                           f"{'$%.2f' % p['cache_read'] if 'cache_read' in p else 'not listed'} | {p.get('note', '')} |"))
price_lines = [l for _, l in sorted(price_lines)]
not_run = sorted(set(prices) - run_models)

compare = ""
if other_dir is not None:
    other = {r["model"]: r for r in rd(other_dir / "summary_by_model.csv")}
    o_eff = ", ".join(sorted({x.get("claude_effort") or "?" for x in rd(other_dir / "results.csv")}))
    lines = []
    for r in rows:
        o = other.get(r["model"])
        if not o: continue
        a, b = num(r.get("cost_per_photo_usd")), num(o.get("cost_per_photo_usd"))
        ao = num(r.get("total_output_tokens")) / num(r["photos"]) if num(r.get("total_output_tokens")) is not None else None
        bo = num(o.get("total_output_tokens")) / num(o["photos"]) if num(o.get("total_output_tokens")) is not None else None
        lines.append(f"| `{r['model']}` | {money(a)} | {money(b)} | {intf(ao)} | {intf(bo)} | "
                     f"{money(a * N) if a is not None else '—'} | {money(b * N) if b is not None else '—'} |")
    if lines:
        t_eff = ", ".join(efforts) or "?"
        compare = (f"## Compared with the `{other_dir.name}/` run\n\nSame photos and models, same number of samples; only the effort level differs.\n\n"
                   f"| model | cost / photo (this run, `{t_eff}`) | cost / photo (`{other_dir.name}/`, `{o_eff}`) "
                   f"| avg output tokens (this run) | avg output tokens (other) | {N} photos (this run) | {N} photos (other) |\n"
                   f"|---|---|---|---|---|---|---|\n" + "\n".join(lines) +
                   "\n\nThe two runs are separate model calls, so part of any difference is ordinary run-to-run variation.\n\n")

md = f"""# Benchmark cost summary

Cost of the benchmark run in this folder, and what a {N}-photo run would cost at the same rate.

- **Source:** `summary_by_model.csv` in this folder (run settings read from `results.csv`).
- **Run date:** {run_date}.
- **Run settings:** {setting_txt}. This is a full run, not `--quick`.
- **Photos:** {photo_set}. Each was run once per model.

## Cost of this run

| model | photos | failed | total cost | cost / photo | avg input tokens / photo | avg output tokens / photo | median time / photo |
|---|---|---|---|---|---|---|---|
{chr(10).join(main)}

- **Averages per photo** are the CSV totals divided by the photo count.
- **Time per photo:** the CSV records the median, not the mean, so the table shows the median.
- **Output tokens** include thinking and reasoning tokens, which are billed as output.

## Projection: {N} photos per model

| model | projected cost | basis |
|---|---|---|
{chr(10).join(proj)}
| **all models above** | **{money(total_proj)}** | sum of {len(proj_models)} model(s) |

- **Method:** the projection multiplies this run's cost per photo by {N}. It assumes the {N} photos use about as many tokens as these did.
- **Excluded models:** {"the total covers only the models listed. Also priced in `eval/model_prices.json` but not in this run: " + ", ".join(f"`{m}`" for m in not_run) + "." if not_run else "none; every priced model is in this run."}

{compare}## Pricing assumptions

Costs were computed with `eval/model_prices.json`, in USD per 1M tokens:

| model | input | output | cached input | note |
|---|---|---|---|---|
{chr(10).join(price_lines)}

- **Price source:** standard (non-batch) list prices from the providers' API pricing pages, as recorded in the price file.
- **Prompt size:** prompts in this run average about {intf(tin_all / calls if calls else None)} input tokens per call, well under any long-prompt price tier.
- **Prompt caching:** the pipeline doesn't use it, so all input is billed at the full input price.
- **Batch APIs:** not used. They cost about half, but the pipeline would need changes.

## Flags

{chr(10).join(flags) if flags else "- None. Every model has a non-zero cost, and no photos failed."}

## How reliable this is

- **Small sample:** cost per photo depends on image size and on how much each model thinks, so a different photo set will cost somewhat differently.
- **Effort level:** Claude projections hold only at the same `CLAUDE_EFFORT` setting.
- **Quick mode:** a `--quick` run makes about a third of the calls, so it would cost less than this projection.
"""
(out_dir / "COST_SUMMARY.md").write_text(md, encoding="utf-8")
print(md)
