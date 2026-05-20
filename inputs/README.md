# Inputs

Place **public** Groww Play Store review data under **`raw/`** for each weekly run.

## How to populate

Fetch public reviews for Groww (`com.nextbillion.groww`) using the project script:

```bash
python3 scripts/fetch_playstore_reviews.py \
  --package com.nextbillion.groww \
  --count 15000 --since-weeks 12 \
  --out inputs/raw/groww_playstore_reviews.csv
```

This reads only **publicly visible** Play Store reviews (no login, no Play Console access). Author names are **not** written to the CSV.

Output columns: `rating,title,text,date,source_store,review_id`

- **`raw/`** is ignored by git by default so review data is not committed.
- The `--since-weeks` flag filters out reviews older than the specified window.
- Rerun weekly (or as needed) to refresh the corpus.

See [docs/architecture.md](../docs/architecture.md) (ingestion layer) and [docs/phases/phase-02/eval.md](../docs/phases/phase-02/eval.md).
