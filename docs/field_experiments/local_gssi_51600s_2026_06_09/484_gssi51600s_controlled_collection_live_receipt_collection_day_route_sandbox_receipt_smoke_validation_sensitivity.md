# Field Experiment 484: Controlled Collection Live Receipt Collection-Day Route Sandbox Receipt Smoke Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the validator from run `483`.

This run checks that the validator accepts the exact run `482` sandbox receipt
smoke and rejects damaged states that would lose the synthetic boundary,
promote measured evidence, damage receipt readiness, promote live files,
promote parser/provenance/archive readiness, promote field FWI or field 3D/HPC,
or damage artifacts.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/484_gssi51600s_controlled_collection_live_receipt_collection_day_route_sandbox_receipt_smoke_validation_sensitivity
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_live_receipt_collection_day_route_sandbox_receipt_smoke_validation_sensitivity_cases.csv
data/gssi51600s_controlled_collection_live_receipt_collection_day_route_sandbox_receipt_smoke_validation_sensitivity_summary.json
figures/gssi51600s_controlled_collection_live_receipt_collection_day_route_sandbox_receipt_smoke_validation_sensitivity.png
scripts/
```

## Result

```text
source validator ready:      true
cases:                       22
expected pass cases:         1
expected fail cases:         21
actual pass cases:           1
actual fail cases:           21
unexpected outcomes:         0
damaged cases:               21
controlled evidence ready:   false
field FWI ready:             false
field 3D/HPC ready:          false
gpu priority:                none
```

The damaged states cover source readiness removal, synthetic file removal,
file-count/DZT-count/metadata-count damage, synthetic-boundary loss, measured
evidence promotion, receipt-row removal, receipt-ready count damage,
receipt-row readiness loss, required-check count damage, live-file promotion,
controlled-evidence promotion, parser/provenance/archive readiness promotion,
field FWI promotion, field 3D/HPC promotion, parser-rerun readiness promotion,
figure damage, and script-snapshot damage.

## Interpretation

The sandbox receipt-smoke validator is sensitive to the failure modes that
matter before any live field packet can be promoted. It accepts only the exact
output-local synthetic sandbox state.

## Decision

Use runs `482-484` as the current closed sandbox receipt-smoke block. Keep the
live field packet blocked until real measured files pass receipt, parser,
provenance, and archive gates.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_live_receipt_collection_day_route_sandbox_receipt_smoke_validation_sensitivity.py

3 passed
```

Figure validation:

```text
1709x847, dynamic range=255
```
