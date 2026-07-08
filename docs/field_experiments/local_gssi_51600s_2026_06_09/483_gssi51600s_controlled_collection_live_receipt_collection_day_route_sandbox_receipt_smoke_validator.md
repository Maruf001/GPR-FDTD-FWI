# Field Experiment 483: Controlled Collection Live Receipt Collection-Day Route Sandbox Receipt Smoke Validator

Date: 2026-06-30

## Purpose

Validate run `482` from saved artifacts.

This run checks that the sandbox receipt smoke contains the expected 33
synthetic files, that all sandbox receipt rows pass, and that no live measured
field evidence or downstream field-processing readiness has been promoted.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/483_gssi51600s_controlled_collection_live_receipt_collection_day_route_sandbox_receipt_smoke_validator
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_live_receipt_collection_day_route_sandbox_receipt_smoke_validator_check_rows.csv
data/gssi51600s_controlled_collection_live_receipt_collection_day_route_sandbox_receipt_smoke_validator_summary.json
figures/gssi51600s_controlled_collection_live_receipt_collection_day_route_sandbox_receipt_smoke_validator.png
scripts/
```

## Result

```text
checks:                         5
passed checks:                  5
failed checks:                  0
sandbox files:                  33
sandbox DZT-like placeholders:  9
sandbox metadata JSON files:    24
sandbox receipt-ready files:    33
sandbox required checks:        183
original live files present:    0
synthetic-only files:           33
measured field evidence files:  0
controlled field evidence ready:false
field FWI ready:                false
field 3D/HPC ready:             false
gpu priority:                   none
```

The five checks cover source readiness, synthetic file shape, sandbox receipt
report readiness, live field evidence/downstream blocking, and figure/script
artifacts.

## Interpretation

Run `482` is a valid sandbox receipt smoke. It confirms the route and receipt
verifier can pass in an isolated positive-control setting, while run `483`
confirms that no live field packet, measured field evidence, parser readiness,
provenance readiness, archive readiness, field FWI, or field 3D/HPC state was
promoted.

## Decision

Use run `483` as the artifact guard for run `482`. Keep the live field packet
blocked until real measured files are placed in the locked live paths and all
downstream gates pass.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_live_receipt_collection_day_route_sandbox_receipt_smoke_validator.py

3 passed
```

Figure validation:

```text
2285x840, dynamic range=255
```
