# Benchmark cost summary

> **For all 7 models** (Claude, OpenAI and Gemini) see [`results-open-photos-all/COST_SUMMARY.md`](../results-open-photos-all/COST_SUMMARY.md). This file covers only Claude Sonnet 5.5 and Haiku 5.5 on the 5 Grand Canyon photos.

Cost of the benchmark run in this folder, and what a 50-photo run would cost at the same rate.

- **Source:** `summary_by_model.csv` in this folder (run settings read from `results.csv`).
- **Run date:** 2026-11-24.
- **Run settings:** 3 sample(s) per photo for every model; Claude effort `high` (from the `CLAUDE_EFFORT` environment variable; the pipeline's default is `high`). This is a full run, not `--quick`.
- **Photos:** 5 Grand Canyon area photos (`benchmark-kit/grand-canyon/manifest.csv`). Each was run once per model.

## Cost of this run

| model | photos | failed | total cost | cost / photo | avg input tokens / photo | avg output tokens / photo | median time / photo |
|---|---|---|---|---|---|---|---|
| `claude-sonnet-5-5` | 5 | 0 | $0.2394 | $0.0479 | 6,326 | 3,522 | 18.7 s |
| `claude-haiku-5-5` | 5 | 0 | $0.0204 | $0.0041 | 6,326 | 6,889 | 21.8 s |

- **Averages per photo** are the CSV totals divided by the photo count.
- **Time per photo:** the CSV records the median, not the mean, so the table shows the median.
- **Output tokens** include thinking and reasoning tokens, which are billed as output.

## Projection: 50 photos per model

| model | projected cost | basis |
|---|---|---|
| `claude-sonnet-5-5` | $2.3940 | $0.0479 × 50 |
| `claude-haiku-5-5` | $0.2040 | $0.0041 × 50 |
| **all models above** | **$2.5980** | sum of 2 model(s) |

- **Method:** the projection multiplies this run's cost per photo by 50. It assumes the 50 photos use about as many tokens as these did.
- **Excluded models:** the total covers only the models listed. Also priced in `eval/model_prices.json` but not in this run: `claude-opus-5-5`, `gemini-3.5-flash-lite`, `gemini-3.8-flash`, `gpt-4o`, `gpt-6.1-terra`, `gpt-6.2-sol`.

## Compared with the `benchmark_results/` run

Same photos and models, same number of samples; only the effort level differs.

| model | cost / photo (this run, `high`) | cost / photo (`benchmark_results/`, `medium`) | avg output tokens (this run) | avg output tokens (other) | 50 photos (this run) | 50 photos (other) |
|---|---|---|---|---|---|---|
| `claude-sonnet-5-5` | $0.0479 | $0.0442 | 3,522 | 3,157 | $2.3940 | $2.2110 |
| `claude-haiku-5-5` | $0.0041 | $0.0035 | 6,889 | 5,799 | $0.2040 | $0.1765 |

The two runs are separate model calls, so part of any difference is ordinary run-to-run variation.

## Pricing assumptions

Costs were computed with `eval/model_prices.json`, in USD per 1M tokens:

| model | input | output | cached input | note |
|---|---|---|---|---|
| `claude-haiku-5-5` | $0.10 | $0.50 | not listed | price for prompts up to 100K tokens |
| `claude-sonnet-5-5` | $2.00 | $10.00 | $0.10 |  |

- **Price source:** standard (non-batch) list prices from the providers' API pricing pages, as recorded in the price file.
- **Prompt size:** prompts in this run average about 2,109 input tokens per call, well under any long-prompt price tier.
- **Prompt caching:** the pipeline doesn't use it, so all input is billed at the full input price.
- **Batch APIs:** not used. They cost about half, but the pipeline would need changes.

## Flags

- None. Every model has a non-zero cost, and no photos failed.

## How reliable this is

- **Small sample:** cost per photo depends on image size and on how much each model thinks, so a different photo set will cost somewhat differently.
- **Effort level:** Claude projections hold only at the same `CLAUDE_EFFORT` setting.
- **Quick mode:** a `--quick` run makes about a third of the calls, so it would cost less than this projection.
