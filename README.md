# massiv

Open dataset for **tokenized equities**: what the underlying asset is, what token represents it, where it trades, which chain it lives on, what legal/economic rights it carries, and how market access differs from the traditional security.

The project is intentionally **data-first**. No frontend is required to make it useful: the CSV files can later power an API, an agent tool, a spread monitor, a portfolio tracker, or research on always-on equity markets.

## Why this exists

“Tokenized stock” is not one legal/economic object. A token can be a tracker certificate with economic exposure but no voting rights, a tokenized debt security, or a structure intended to preserve shareholder rights. `massiv` records those distinctions instead of putting everything under the generic RWA label.

## Dataset

- `data/assets.csv` — stock/ETF → tokenized version mapping.
- `data/ecosystems.csv` — issuer/platform/chain/rights/trading-hours metadata by product family.
- `data/regulatory_events.csv` — regulation and market-structure events that change what can be built.
- `data/observations.csv` — time-stamped liquidity/market observations; designed to grow into spread and volume history.
- `docs/SCHEMA.md` — field definitions and collection rules.

Initial records are deliberately conservative: a blank value means **not yet verified**, not “none”. Every factual row carries a source URL and verification date.

## Quick start

```bash
python scripts/validate.py
```

The validator uses only Python's standard library.

Example query:

```python
import csv

with open("data/assets.csv", newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

print([r for r in rows if r["underlying_symbol"] == "AAPL"])
```

## Current thesis

The useful opportunity is not merely to speculate on an “RWA coin”. The durable asset can be the **mapping + history + rights metadata** around tokenized securities. If multiple venues represent the same underlying equity, this dataset can later support:

- cross-venue and token-vs-underlying spread alerts;
- rights-aware portfolio tracking;
- agent/API lookup of tokenized security metadata;
- chain/venue liquidity comparisons;
- historical research around extended-hours and always-on markets.

## Important distinction

`massiv` never assumes a token equals direct ownership of the underlying share. Always inspect `rights_class`, `voting_rights`, `dividend_treatment`, and the source documentation.

## Status

Seed dataset started: **2026-09-28**.

## License

MIT. Data sources retain their own rights and terms. This repository is for research/information and is not investment advice.
