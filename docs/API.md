# Static JSON API

`massiv` can be consumed without a server. Canonical data remains in `data/*.csv`; `scripts/build_api.py` produces versioned JSON under `api/v1/`.

## Build

```bash
python scripts/validate.py
python scripts/build_api.py
```

Builds are deterministic: identical canonical CSV inputs produce byte-identical JSON. This makes generated-artifact consistency checks practical in CI.

## Endpoints

- `api/v1/index.json` — endpoint manifest.
- `api/v1/assets.json` — tokenized-equity mappings.
- `api/v1/contracts.json` — chain contract/mint registry.
- `api/v1/ecosystems.json` — product-family metadata.
- `api/v1/regulatory_events.json` — regulatory timeline.
- `api/v1/industry_events.json` — infrastructure, standards, and industry events that are not themselves claims that an asset is live.
- `api/v1/observations.json` — append-only observations.
- `api/v1/catalog.json` — assets with their contract records embedded; easiest endpoint for agents.

Every response has `api_version` and `data_version`; collection responses also expose `count` and `data`. `data_version` is the newest dated verification/event/observation represented in the canonical inputs. It is a dataset freshness marker, not a wall-clock generation timestamp.

## Public consumption

After generated artifacts are committed, clients can fetch them directly from GitHub Raw, for example:

`https://raw.githubusercontent.com/myfines/massiv/main/api/v1/catalog.json`

Consumers should pin to `/api/v1/`. Breaking schema changes require a new API version; additive fields may be introduced within v1.

## Design rule

JSON is a derived artifact. Edit CSV sources, validate them, then rebuild JSON. Do not hand-edit generated API files.
