# Schema and collection rules

## Design principles

1. **Do not collapse legal structures.** A tracker certificate, debt security, direct/beneficial ownership claim, and an issuer-authorized tokenized share are different objects.
2. **Unknown is not false.** Leave a field blank or use `TBD` when the source does not establish the fact.
3. **Time-stamp mutable facts.** Liquidity, volume, spreads, supported chains and trading hours can change. Historical measurements belong in `observations.csv`.
4. **Source every record.** Prefer regulator, issuer, exchange/platform, prospectus, or official product documentation.
5. **Do not infer contract addresses.** Contract addresses must come from official product documentation or independently verified chain data.

## `data/assets.csv`

One row is one underlying asset × tokenized product mapping.

Key fields:

- `asset_id`: stable repository identifier.
- `underlying_symbol`: ticker of the traditional stock/ETF.
- `ecosystem_id`: foreign key into `ecosystems.csv`.
- `token_symbol`: token/ticker used by the tokenized product.
- `blockchains`: chains documented for this asset/platform. If the source is only platform-level, say so in `notes`.
- `rights_class`: legal/economic nature of the token.
- `voting_rights`: `yes`, `no`, `intended`, `TBD`, or blank.
- `dividend_treatment`: cash dividend, rebasing/economic equivalent, none, unknown, etc.
- `venue_trading_hours`: hours on the named venue, not a blanket claim about all secondary markets.
- `onchain_transferability`: whether transfer/self-custody is supported.
- `liquidity_snapshot_usd` / `liquidity_snapshot_time`: optional current snapshot; historical series should go to `observations.csv`.
- `status`: e.g. `live`, `planned`, `suspended`, `terminated`.
- `source_urls`: one or more primary/official URLs separated by `; `.
- `last_verified`: ISO date (`YYYY-MM-DD`).

## `data/contracts.csv`

One row is one tokenized asset representation on one chain.

Key fields:

- `contract_id`: stable repository identifier for the asset × chain representation.
- `asset_id`: foreign key into `assets.csv`.
- `network`: blockchain/network name.
- `token_standard`: e.g. `ERC-20` or `SPL`.
- `contract_address`: full contract address or mint; never store shortened display forms such as `0x123...abc`.
- `explorer_url`: direct explorer page for that exact address/mint.
- `verification_source_url`: issuer/product source that establishes the token/product identity or chain support.
- `verification_level`: provenance shorthand such as `explorer+issuer`.
- `last_verified`: date the mapping was checked.

Contract identity is technical metadata. It does **not** establish shareholder rights or the legal nature of the product; those remain in `assets.csv` / `ecosystems.csv`.

When a product is bridged or wrapped, do not silently treat the wrapped representation as the issuer-native contract. Add a separate row and state the relationship in `notes`.

## `data/ecosystems.csv`

One row is one tokenized-equity product family or infrastructure program.

Use this for facts shared across many assets: issuer, venue, broad chain support, legal structure, rights model, availability and launch status.

`launch_target` is for announced future products and must not be interpreted as a guaranteed launch date.

## `data/regulatory_events.csv`

One row is one regulatory action relevant to tokenized-equity market structure.

Store the regulator's actual scope and conditions rather than reducing a rule/order to “approved” or “banned”.

## `data/observations.csv`

Append-only market measurements.

- `observation_date`: date the measurement/source applies to.
- `ecosystem_id` / `asset_id`: scope; asset may be blank for ecosystem-wide metrics.
- `metric_name`: stable machine-readable metric name.
- `comparator`: `equal`, `greater_than`, `greater_or_equal`, `less_than`, etc.
- `value` / `unit`: numeric value and unit.
- `quality`: provenance label such as `official`, `platform_claim`, `platform_claim_citing_Dune`, `onchain_computed`.
- `notes`: methodology caveats.

## Planned extensions

The next useful tables are:

- `venues.csv`: venue/API endpoints, geographic access and fee model.
- `price_snapshots.csv`: timestamped underlying/token bid-ask data.
- `spreads.csv`: reproducible cross-venue spread calculations.

Those extensions should be added only when their source/collection method is reproducible.
