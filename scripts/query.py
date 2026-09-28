#!/usr/bin/env python3
"""Lookup tokenized-equity mappings from the command line."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "data" / "assets.csv"


def main() -> int:
    parser = argparse.ArgumentParser(description="Query massiv asset mappings")
    parser.add_argument("symbol", help="Underlying or token symbol, e.g. AAPL or AAPLx")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of text")
    args = parser.parse_args()

    needle = args.symbol.strip().upper()
    with ASSETS.open(newline="", encoding="utf-8") as fh:
        rows = [
            row
            for row in csv.DictReader(fh)
            if row["underlying_symbol"].upper() == needle
            or row["token_symbol"].upper() == needle
        ]

    if args.json:
        print(json.dumps(rows, ensure_ascii=False, indent=2))
    elif not rows:
        print(f"No verified mapping found for {args.symbol}")
    else:
        for row in rows:
            print(
                f'{row["underlying_symbol"]} -> {row["token_symbol"]} | '
                f'{row["ecosystem_id"]} | {row["blockchains"]} | '
                f'{row["rights_class"]} | {row["venue_trading_hours"]}'
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
