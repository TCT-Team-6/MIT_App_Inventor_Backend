# 40 Wikimedia Commons photos: GPT-6.1 Terra vs GPT-6.2 Sol

- **Run date:** 2026-11-25.
- **Code:** upstream `main` at `a07f6d7` (GameKnight998/MIT_App_Inventor_Backend), the code merged in PR #1.
- **Settings:** `eval/benchmark.py run`, 3 samples per photo, full run (not `--quick`, not `--agent`).
- **Photos:** 40 open-licence, GPS-tagged photos from 40 different places in 29 countries and territories.
  - **Categories:** city and town streets, suburbs, coasts, mountains, deserts, forests, farmland, one night photo and one railway station.
  - **Selection:** picked by hand to avoid photos of people, readable place-name signs and famous monuments. Some photos still contain a recognisable spot (see "Limits").
  - **Excluded:** none of the 9 places in `results-open-photos-all/`.
  - **Preparation:** each photo was downloaded at 1280 or 1920 px and saved with all metadata removed (no GPS or camera data).

## Files

| File | What it holds |
|---|---|
| `manifest.csv` | True location of each photo (the camera position on Commons). These locations are public on Commons, so the file is committed. |
| `sources.csv` | Commons title, author, licence and page for each photo. Use it to credit photos on slides and to download them again. |
| `results.csv` | One row per photo × model. |
| `summary_by_model.csv`, `summary_by_category.csv`, `*.png` | Written by `eval/benchmark.py report`. |

`results.csv` started with 14 failed rows from a pause when the OpenAI account ran out of credit. Each of those photos was re-run successfully, and the failed rows were removed.

## Results

| model | ≤1 km | ≤5 km | ≤25 km | 95% lower bound (≤25 km) | median error | confidence right / wrong | cost | cost / photo |
|---|---|---|---|---|---|---|---|---|
| `gpt-6.1-terra` | 29/40 | 32/40 | **36/40 (90%)** | 76% | 0.34 km | 0.72 / 0.50 | $1.69 | $0.042 |
| `gpt-6.2-sol` | 29/40 | 34/40 | **37/40 (92%)** | 80% | 0.29 km | 0.79 / 0.31 | $2.96 | $0.074 |

- **How the numbers were computed:**
  - **Cost:** computed from the token counts at Terra $1 / $5 and Sol $2 / $10 per 1M input / output tokens. Upstream `eval/model_prices.json` has no price for either model, so the summary CSVs leave cost blank.
  - **Lower bound:** an exact (Clopper-Pearson) 95% interval.
- **Terra vs Sol:** Terra alone got 1 photo within 25 km, and Sol alone got 2. That difference is not significant (McNemar p = 1.0), so the two models are tied.
- **With the 22 earlier photos re-run on the same code:** 62 photos in total.
  - Terra placed 56/62 within 25 km (at least 80% with 95% confidence).
  - Sol placed 57/62 (at least 82%).

## Misses (more than 25 km)

| photo | true place | Terra | Sol |
|---|---|---|---|
| `d02` | San Pedro de Atacama, Chile | 58 km | 58 km |
| `u06` | Kenyatta Avenue, Nairobi | 504 km (said Kampala, confidence 0.85) | 0.1 km |
| `m02` | Leknes, Lofoten | 67 km | 67 km |
| `m01` | French Valley, Torres del Paine | 7 km | 1,097 km (confidence 0.11) |
| `r06` | Northleach, Cotswolds | 31 km | 0.5 km |

`d02` is a backend bug, not a model miss:
- **Model answers:** both models placed the photo in the town, Terra within 0.23 km and Sol within 0.02 km (`ai_top_error_km`).
- **What the pipeline did:** it replaced those coordinates with the centre of the San Pedro de Atacama *commune*, a 279 km-wide administrative area that the geocoder returns first for that name.

## Limits

- **Recognisable clues:** many photos show something the models recognise or read, such as a shop sign, a known building or a well-known view. Real investigators use the same clues, but these photos are easier than random snapshots.
- **Not tested:** indoor photos, and photos with no distinctive clues.
- **Map check:** `map_check` is mostly `skipped` or `unavailable`. Most photos give the map check nothing to look up, and the Overpass servers drop connections from the cloud container this ran in. This run does not measure the map check as deployed.
