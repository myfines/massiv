#!/usr/bin/env python3
"""Build stable, dependency-free JSON API artifacts from the canonical CSV data."""
from __future__ import annotations
import csv, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "api" / "v1"
TABLES = (
    "assets",
    "contracts",
    "ecosystems",
    "regulatory_events",
    "industry_events",
    "observations",
)

def rows(name: str):
    with (DATA / f"{name}.csv").open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def dump(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

def data_version(loaded):
    """Return the newest source/verification date, making builds reproducible."""
    dates = []
    for table in loaded.values():
        for row in table:
            for key in ("last_verified", "observation_date", "event_date"):
                value = row.get(key, "")
                if value:
                    dates.append(value)
    return max(dates) if dates else "unknown"

def envelope(version, value):
    return {"api_version": "v1", "data_version": version, "count": len(value), "data": value}

def main():
    loaded = {name: rows(name) for name in TABLES}
    version = data_version(loaded)
    for name, value in loaded.items():
        dump(OUT / f"{name}.json", envelope(version, value))

    contracts_by_asset = {}
    for row in loaded["contracts"]:
        contracts_by_asset.setdefault(row["asset_id"], []).append(row)
    assets = []
    for row in loaded["assets"]:
        item = dict(row)
        item["contracts"] = contracts_by_asset.get(row["asset_id"], [])
        assets.append(item)
    dump(OUT / "catalog.json", envelope(version, assets))
    dump(OUT / "index.json", {
        "api_version": "v1",
        "data_version": version,
        "endpoints": [f"{name}.json" for name in TABLES] + ["catalog.json"],
    })
    print(f"Built api/v1 ({len(assets)} assets, data_version={version})")

if __name__ == "__main__":
    main()
