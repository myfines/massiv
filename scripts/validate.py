#!/usr/bin/env python3
"""Validate the core massiv CSV datasets using only Python's standard library."""

from __future__ import annotations

import csv
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

REQUIRED_COLUMNS = {
    "assets.csv": {
        "asset_id", "underlying_symbol", "ecosystem_id", "token_symbol",
        "rights_class", "status", "source_urls", "last_verified",
    },
    "contracts.csv": {
        "contract_id", "asset_id", "network", "token_standard",
        "contract_address", "explorer_url", "verification_source_url",
        "last_verified", "verification_level",
    },
    "ecosystems.csv": {
        "ecosystem_id", "status", "product_name", "rights_class",
        "source_urls", "last_verified",
    },
    "regulatory_events.csv": {
        "event_id", "event_date", "jurisdiction", "regulator",
        "event_type", "source_url", "last_verified",
    },
    "observations.csv": {
        "observation_id", "observation_date", "ecosystem_id", "metric_name",
        "value", "unit", "source_url", "quality",
    },
}

ID_COLUMNS = {
    "assets.csv": "asset_id",
    "contracts.csv": "contract_id",
    "ecosystems.csv": "ecosystem_id",
    "regulatory_events.csv": "event_id",
    "observations.csv": "observation_id",
}

DATE_COLUMNS = {
    "assets.csv": ["last_verified"],
    "contracts.csv": ["last_verified"],
    "ecosystems.csv": ["last_verified"],
    "regulatory_events.csv": ["event_date", "last_verified"],
    "observations.csv": ["observation_date"],
}

SOURCE_COLUMNS = {
    "assets.csv": "source_urls",
    "contracts.csv": "verification_source_url",
    "ecosystems.csv": "source_urls",
    "regulatory_events.csv": "source_url",
    "observations.csv": "source_url",
}


def load_csv(name: str) -> tuple[list[str], list[dict[str, str]]]:
    path = DATA / name
    if not path.exists():
        raise ValueError(f"missing file: {path.relative_to(ROOT)}")
    with path.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        return reader.fieldnames or [], list(reader)


def valid_iso_date(value: str) -> bool:
    try:
        date.fromisoformat(value)
        return True
    except ValueError:
        return False


def main() -> int:
    errors: list[str] = []
    tables: dict[str, list[dict[str, str]]] = {}

    for name, required in REQUIRED_COLUMNS.items():
        try:
            fields, rows = load_csv(name)
        except ValueError as exc:
            errors.append(str(exc))
            continue

        tables[name] = rows
        missing = required - set(fields)
        if missing:
            errors.append(f"{name}: missing columns: {sorted(missing)}")

        id_col = ID_COLUMNS[name]
        seen: set[str] = set()
        for line_no, row in enumerate(rows, start=2):
            row_id = (row.get(id_col) or "").strip()
            if not row_id:
                errors.append(f"{name}:{line_no}: empty {id_col}")
            elif row_id in seen:
                errors.append(f"{name}:{line_no}: duplicate {id_col}={row_id}")
            seen.add(row_id)

            for col in DATE_COLUMNS[name]:
                value = (row.get(col) or "").strip()
                if value and not valid_iso_date(value):
                    errors.append(f"{name}:{line_no}: invalid ISO date {col}={value!r}")

            source_value = (row.get(SOURCE_COLUMNS[name]) or "").strip()
            if not source_value:
                errors.append(f"{name}:{line_no}: missing source URL")
            else:
                for url in [u.strip() for u in source_value.split(";") if u.strip()]:
                    if not url.startswith(("https://", "http://")):
                        errors.append(f"{name}:{line_no}: invalid source URL {url!r}")

            if name == "contracts.csv":
                explorer_url = (row.get("explorer_url") or "").strip()
                if not explorer_url.startswith(("https://", "http://")):
                    errors.append(f"{name}:{line_no}: invalid explorer_url={explorer_url!r}")
                if not (row.get("contract_address") or "").strip():
                    errors.append(f"{name}:{line_no}: empty contract_address")

    ecosystems = {
        row.get("ecosystem_id", "").strip()
        for row in tables.get("ecosystems.csv", [])
        if row.get("ecosystem_id", "").strip()
    }
    assets = {
        row.get("asset_id", "").strip()
        for row in tables.get("assets.csv", [])
        if row.get("asset_id", "").strip()
    }

    for name in ("assets.csv", "observations.csv"):
        for line_no, row in enumerate(tables.get(name, []), start=2):
            ecosystem_id = (row.get("ecosystem_id") or "").strip()
            if ecosystem_id and ecosystem_id not in ecosystems:
                errors.append(
                    f"{name}:{line_no}: unknown ecosystem_id={ecosystem_id!r}"
                )

    for line_no, row in enumerate(tables.get("contracts.csv", []), start=2):
        asset_id = (row.get("asset_id") or "").strip()
        if asset_id and asset_id not in assets:
            errors.append(f"contracts.csv:{line_no}: unknown asset_id={asset_id!r}")

    if errors:
        print("Validation failed:")
        for error in errors:
            print(f" - {error}")
        return 1

    total_rows = sum(len(rows) for rows in tables.values())
    print(f"OK: validated {len(tables)} tables / {total_rows} rows")
    return 0


if __name__ == "__main__":
    sys.exit(main())
