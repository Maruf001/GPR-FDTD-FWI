# Field Experiment 481: Live Receipt Collection-Day Route Spec Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the validator from run `480`.

This run checks that the validator accepts the exact run `479` route spec and
rejects damaged states that would change route counts, receipt-check counts,
file readiness, phase readiness, downstream field readiness, or artifacts.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/481_gssi51600s_controlled_collection_live_receipt_collection_day_route_spec_validation_sensitivity
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_live_receipt_collection_day_route_spec_validation_sensitivity_cases.csv
data/gssi51600s_controlled_collection_live_receipt_collection_day_route_spec_validation_sensitivity_summary.json
figures/gssi51600s_controlled_collection_live_receipt_collection_day_route_spec_validation_sensitivity.png
scripts/
```

## Result

```text
source validator ready:          true
cases:                           15
expected pass cases:             1
expected fail cases:             14
actual pass cases:               1
actual fail cases:               14
unexpected outcomes:             0
damaged cases:                   14
field FWI ready:                 false
field 3D/HPC ready:              false
gpu priority:                    none
```

The damaged states cover source readiness removal, route-row removal, DZT-count
damage, metadata-count damage, family-count damage, phase removal,
receipt-check-count damage, file-presence promotion, receipt-readiness
promotion, phase-readiness promotion, field-FWI promotion, field-3D/HPC
promotion, figure damage, and script-snapshot damage.

## Interpretation

The route-spec validator is sensitive to the failure modes that would matter
before accepting controlled field evidence.

## Decision

Use runs `479-481` as the current closed field collection-day route block.
Keep field evidence, field FWI, and field 3D/HPC blocked until all route files
pass receipt and downstream gates.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_live_receipt_collection_day_route_spec_validation_sensitivity.py

3 passed
```

Figure validation:

```text
1709x847, dynamic range=255
```
