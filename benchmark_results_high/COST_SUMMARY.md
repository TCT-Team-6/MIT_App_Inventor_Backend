# Benchmark cost summary

Cost of the benchmark run in this folder, and what a 50-photo run would cost at the same rate.

- **Source:** `summary_by_model.csv` in this folder (run settings read from `results.csv`).
- **Run date:** 2026-11-24.
- **Run settings:** 3 sample(s) per photo, Claude effort `high`. This is a full run, not `--quick`. The effort level comes from the `CLAUDE_EFFORT` environment variable; the pipeline's default is `high`.
- **Photos:** 5 photos (`benchmark-kit/grand-canyon/manifest.csv`). Each was run once per model.

## Cost of this run

| model | photos | failed | total cost | cost / photo | avg input tokens / photo | avg output tokens / photo | median time / photo |
|---|---|---|---|---|---|---|---|
| `claude-sonnet-5-5` | 5 | 0 | $0.2394 | $0.0479 | 6,326 | 3,522 | 18.7 s |
| `claude-haiku-5-5` | 5 | 0 | $0.0204 | $0.0041 | 6,326 | 6,889 | 21.8 s |

- **Averages per photo** are the CSV totals divided by the photo count.
- **Time per photo:** the CSV records the median, not the mean, so the table shows the median.
- **Output tokens** include thinking tokens, which are billed as output.

## Projection: 50 photos per model

| model | projected cost | basis |
|---|---|---|
| `claude-sonnet-5-5` | $2.3940 | $0.0479 × 50 |
| `claude-haiku-5-5` | $0.2040 | $0.0041 × 50 |
| **all models above** | **$2.5980** | sum of 2 model(s) |

- **Method:** the projection multiplies this run's cost per photo by 50. It assumes the 50 photos use about as many tokens as these did.
- **Excluded models:** the total covers only the models listed. `claude-opus-5-5`, the GPT models and the Gemini models were not in this run, so they have no cost here.

## Compared with the `benchmark_results/` run

Same 5 photos and models, 3 samples per photo; only the effort level differs.

| model | cost / photo (this run, `high`) | cost / photo (`benchmark_results/`, `medium`) | avg output tokens (this run) | avg output tokens (other) | 50 photos (this run) | 50 photos (other) |
|---|---|---|---|---|---|---|
| `claude-sonnet-5-5` | $0.0479 | $0.0442 | 3,522 | 3,157 | $2.3940 | $2.2110 |
| `claude-haiku-5-5` | $0.0041 | $0.0035 | 6,889 | 5,799 | $0.2040 | $0.1765 |

The two runs are separate model calls, so part of any difference is ordinary run-to-run variation.

## Pricing assumptions

Costs were computed with `eval/model_prices.json`, in USD per 1M tokens:

| model | input | output |
|---|---|---|
| `claude-sonnet-5-5` | $2.00 | $10.00 |
| `claude-haiku-5-5` | $0.10 | $0.50 |

- **Price source:** the Anthropic API list prices as of 2026-11, as noted in the price file.
- **Haiku 5.5:** its price applies to prompts up to 100K tokens. These prompts are about 2,100 tokens per call.
- **Prompt caching:** the pipeline doesn't use it, so all input is billed at the full input price.
- **Batch API:** not used. It would halve these costs, but the pipeline would need changes.

## Flags

- None. Every model has a non-zero cost, and no photos failed.

## How reliable this is

- **Small sample:** 5 photos from one area. Output tokens vary by photo and model. For example, Haiku wrote more output tokens per photo than Sonnet, but still costs about 12× less.
- **Different photo sets:** a 50-photo set with harder photos, such as the Bellevue night shots, may use more tokens.
- **Quick mode:** a `--quick` run makes about a third of the calls, so it would cost less than this projection.
- **Effort level:** the projection holds only at the same effort level. Check `CLAUDE_EFFORT` before a 50-photo run.
