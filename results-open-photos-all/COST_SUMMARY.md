# Benchmark cost summary

Cost of the benchmark run in this folder, and what a 50-photo run would cost at the same rate.

- **Source:** `summary_by_model.csv` in this folder (run settings read from `results.csv`).
- **Run date:** 2026-11-24.
- **Run settings:** 3 sample(s) per photo for every model; Claude effort `medium` (from the `CLAUDE_EFFORT` environment variable; the pipeline's default is `high`). This is a full run, not `--quick`.
- **Photos:** 9 Wikimedia Commons photos from Germany, Switzerland, the UK, France, the Seychelles, Poland and Portugal (`benchmark-kit/open-photos/manifest.csv`). Each was run once per model.

## Cost of this run

| model | photos | failed | total cost | cost / photo | avg input tokens / photo | avg output tokens / photo | median time / photo |
|---|---|---|---|---|---|---|---|
| `gpt-4o` | 9 | 0 | $0.2862 | $0.0318 | 4,940 | 1,945 | 19.9 s |
| `gpt-6.1-terra` | 9 | 0 | $0.3687 | $0.0410 | 16,999 | 4,750 | 48.1 s |
| `gpt-6.2-sol` | 9 | 0 | $0.7763 | $0.0863 | 17,312 | 5,123 | 38.2 s |
| `gemini-3.8-flash` | 9 | 0 | $0.5308 | $0.0590 | 16,667 | 11,988 | 38.7 s |
| `gemini-3.5-flash-lite` | 9 | 0 | $0.1016 | $0.0113 | 17,797 | 2,371 | 10.5 s |
| `claude-sonnet-5-5` | 9 | 0 | $0.7817 | $0.0868 | 26,199 | 3,445 | 17.7 s |
| `claude-haiku-5-5` | 9 | 0 | $0.0486 | $0.0054 | 26,199 | 5,557 | 16.5 s |

- **Averages per photo** are the CSV totals divided by the photo count.
- **Time per photo:** the CSV records the median, not the mean, so the table shows the median.
- **Output tokens** include thinking and reasoning tokens, which are billed as output.

## Projection: 50 photos per model

| model | projected cost | basis |
|---|---|---|
| `gpt-4o` | $1.5900 | $0.0318 × 50 |
| `gpt-6.1-terra` | $2.0485 | $0.0410 × 50 |
| `gpt-6.2-sol` | $4.3130 | $0.0863 × 50 |
| `gemini-3.8-flash` | $2.9485 | $0.0590 × 50 |
| `gemini-3.5-flash-lite` | $0.5645 | $0.0113 × 50 |
| `claude-sonnet-5-5` | $4.3425 | $0.0868 × 50 |
| `claude-haiku-5-5` | $0.2700 | $0.0054 × 50 |
| **all models above** | **$16.0770** | sum of 7 model(s) |

- **Method:** the projection multiplies this run's cost per photo by 50. It assumes the 50 photos use about as many tokens as these did.
- **Excluded models:** the total covers only the models listed. Also priced in `eval/model_prices.json` but not in this run: `claude-opus-5-5`.

## Pricing assumptions

Costs were computed with `eval/model_prices.json`, in USD per 1M tokens:

| model | input | output | cached input | note |
|---|---|---|---|---|
| `claude-haiku-5-5` | $0.10 | $0.50 | not listed | price for prompts up to 100K tokens |
| `claude-sonnet-5-5` | $2.00 | $10.00 | $0.10 |  |
| `gemini-3.5-flash-lite` | $0.30 | $2.50 | $0.03 |  |
| `gemini-3.8-flash` | $0.75 | $3.75 | not listed | introductory price until 2026-12-31; input 1.50 / output 7.50 from 2027-01-01 |
| `gpt-4o` | $2.50 | $10.00 | $1.25 | marked deprecated by OpenAI |
| `gpt-6.1-terra` | $1.00 | $5.00 | $0.05 |  |
| `gpt-6.2-sol` | $2.00 | $10.00 | $0.10 |  |

- **Price source:** standard (non-batch) list prices from the providers' API pricing pages, as recorded in the price file.
- **Prompt size:** prompts in this run average about 6,638 input tokens per call, well under any long-prompt price tier.
- **Prompt caching:** the pipeline doesn't use it, so all input is billed at the full input price.
- **Batch APIs:** not used. They cost about half, but the pipeline would need changes.

## Flags

- `gemini-3.8-flash`: priced at an introductory rate (introductory price until 2026-12-31; input 1.50 / output 7.50 from 2027-01-01).

## How reliable this is

- **Small sample:** cost per photo depends on image size and on how much each model thinks, so a different photo set will cost somewhat differently.
- **Effort level:** Claude projections hold only at the same `CLAUDE_EFFORT` setting.
- **Quick mode:** a `--quick` run makes about a third of the calls, so it would cost less than this projection.
