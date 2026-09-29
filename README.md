# massiv

Open dataset for **tokenized equities**: what the underlying asset is, what token represents it, where it trades, which chain it lives on, what legal/economic rights it carries, and how market access differs from the traditional security.

The project is intentionally **data-first**. The canonical CSV data and a derived, versioned static JSON API can power agent tools, spread monitors, portfolio trackers, or research on always-on equity markets.

## Dataset

- `data/assets.csv` — stock/ETF → tokenized version mapping.
- `data/contracts.csv` — exact verified contract/mint addresses by asset and chain.
- `data/ecosystems.csv` — issuer/platform/chain/rights/trading-hours metadata by product family.
- `data/regulatory_events.csv` — regulation and market-structure events.
- `data/observations.csv` — time-stamped market observations.
- `docs/SCHEMA.md` — field definitions and collection rules.
- `docs/API.md` — stable machine-consumption interface.

A blank value means **not yet verified**, not “none”. Every factual row carries a source URL and verification date. Contract rows require both an explorer reference and an issuer/product reference before they are treated as verified.

## Quick start

```bash
python scripts/validate.py
python scripts/build_api.py
```

The tools use only Python's standard library.

For agents and applications, the easiest artifact is `api/v1/catalog.json`, which embeds verified contracts beneath each asset. The public raw endpoint is documented in `docs/API.md`. API consumers should pin to `v1`; breaking changes get a new version.

Example CSV query:

```python
import csv
with open("data/assets.csv", newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))
print([r for r in rows if r["underlying_symbol"] == "AAPL"])
```

## Why this exists

“Tokenized stock” is not one legal/economic object. A token can be a tracker certificate with economic exposure but no voting rights, a tokenized debt security, or a structure intended to preserve shareholder rights. `massiv` records those distinctions instead of putting everything under the generic RWA label.

The durable asset is the **mapping + history + rights metadata** around tokenized securities. As venues multiply, the dataset can support cross-venue/token-vs-underlying spread alerts, rights-aware portfolio tracking, agent/API lookup, chain/venue liquidity comparisons, and historical research.

## Important distinction

`massiv` never assumes a token equals direct ownership of the underlying share. Inspect `rights_class`, `voting_rights`, `dividend_treatment`, and source documentation. A technically verified onchain contract also does **not** by itself establish legal rights; technical identity and legal/economic structure are tracked separately.

## Status

Seed dataset and contract registry started **2026-09-28**. Static JSON API tooling added **2026-09-29**.

## License

MIT. Data sources retain their own rights and terms. This repository is for research/information and is not investment advice.
