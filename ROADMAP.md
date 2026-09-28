# Roadmap

## v0.1 — verified mapping foundation

- [x] Separate asset mappings, product ecosystems, regulation and observations.
- [x] Seed primary-source-backed xStocks mappings.
- [x] Represent live vs planned products separately.
- [x] Add zero-dependency validation and CI.
- [x] Add a tiny CLI lookup tool.

## v0.2 — contract registry

- [ ] Add `contracts.csv` with exact contract/mint address, chain, decimals, verification source and verification timestamp.
- [ ] Resolve bridged/wrapped representations separately from issuer-native contracts.
- [ ] Add automated duplicate-contract and symbol-collision checks.

## v0.3 — liquidity history

- [ ] Add reproducible collection for token price, underlying reference price, bid/ask, venue volume and onchain pool liquidity.
- [ ] Store append-only snapshots rather than overwriting current values.
- [ ] Record data provenance and latency for every observation.

## v0.4 — spread engine

- [ ] Normalize market hours/time zones.
- [ ] Calculate token-vs-underlying premium/discount when both references are valid.
- [ ] Calculate cross-chain/cross-venue spreads with fee/slippage assumptions explicitly separated from raw spread.
- [ ] Emit machine-readable alerts only when inputs meet freshness/quality thresholds.

## v0.5 — API / agent tool

- [ ] Export canonical JSON.
- [ ] Add a lightweight read-only API.
- [ ] Add endpoints/tools for `lookup(symbol)`, `rights(symbol)`, `venues(symbol)` and `latest_spread(symbol)`.

## Non-goals

- No coin-picking or trade calls disguised as dataset output.
- No assumption that a token gives direct shareholder ownership.
- No scraping of sources whose terms prohibit automated collection.
- No unverified contract addresses.
