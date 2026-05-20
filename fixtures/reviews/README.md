# Review fixtures

This directory is reserved for any committed **anonymized or synthetic** review samples needed for pipeline testing.

For the current Groww integration, **real** public Play Store reviews are fetched directly into `inputs/raw/` using:

```bash
python3 scripts/fetch_playstore_reviews.py \
  --package com.nextbillion.groww \
  --count 15000 --since-weeks 12 \
  --out inputs/raw/groww_playstore_reviews.csv
```

See [inputs/README.md](../../inputs/README.md) for details.
