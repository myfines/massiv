#!/usr/bin/env python3
"""Build stable, dependency-free JSON API artifacts from the canonical CSV data."""
from __future__ import annotations
import csv, json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "api" / "v1"
TABLES = ("assets", "contracts", "ecosystems", "regulatory_events", "observations")

def rows(name: str):
    with (DATA / f"{name}.csv").open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def dump(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def main():
    generated = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    loaded = {name: rows(name) for name in TABLES}
    for name, value in loaded.items():
        dump(OUT / f"{name}.json", {"api_version":"v1","generated_at":generated,"count":len(value),"data":value})
    contracts_by_asset = {}
    for row in loaded["contracts"]:
        contracts_by_asset.setdefault(row["asset_id"], []).append(row)
    assets = []
    for row in loaded["assets"]:
        item = dict(row)
        item["contracts"] = contracts_by_asset.get(row["asset_id"], [])
        assets.append(item)
    dump(OUT / "catalog.json", {"api_version":"v1","generated_at":generated,"count":len(assets),"data":assets})
    dump(OUT / "index.json", {"api_version":"v1","generated_at":generated,"endpoints":[f"{n}.json" for n in TABLES] + ["catalog.json"]})
    print(f"Built api/v1 ({len(assets)} assets)")

if __name__ == "__main__":
    main()
