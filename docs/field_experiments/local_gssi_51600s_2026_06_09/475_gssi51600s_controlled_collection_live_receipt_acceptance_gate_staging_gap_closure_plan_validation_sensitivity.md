# Field Experiment 475: Live Receipt Acceptance Gate Staging Gap Closure Plan Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `474` validator with controlled damage to the run `473`
closure-plan artifacts.

This run checks that the validator fails when closure-group identity,
missing-file counts, readiness state, downstream state, figure metadata, or
script snapshots are damaged.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/475_gssi51600s_controlled_collection_live_receipt_acceptance_gate_staging_gap_closure_plan_validation_sensitivity
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_live_receipt_acceptance_gate_staging_gap_closure_plan_validation_sensitivity_cases.csv
data/gssi51600s_controlled_collection_live_receipt_acceptance_gate_staging_gap_closure_plan_validation_sensitivity_summary.json
figures/gssi51600s_controlled_collection_live_receipt_acceptance_gate_staging_gap_closure_plan_validation_sensitivity.png
scripts/
```

## Result

```text
source validator ready:                  true
sensitivity cases:                       13
expected pass cases:                     1
expected fail cases:                     12
actual pass cases:                       1
actual fail cases:                       12
unexpected cases:                        0
damaged cases:                           12
parser ready:                            false
provenance ready:                        false
archive ready:                           false
controlled field evidence ready:         false
field FWI ready:                         false
field 3D/HPC ready:                      false
gpu priority:                            none
```

Damaged states fail for:

```text
source readiness removal
closure group removal
closure group count damage
missing file row removal
missing file count damage
family identity damage
file-present promotion
receipt-ready promotion
closure-group readiness promotion
field-FWI promotion
figure damage
missing script snapshots
```

## Interpretation

The closure-plan validator is sensitive to the intended failure modes. It does
not silently promote missing files, ready groups, field evidence, field FWI, or
field 3D/HPC readiness.

## Decision

Use runs `473-475` as the guarded field closure-plan block. The next field-side
event still requires real measured files and completed metadata JSON files.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_live_receipt_acceptance_gate_staging_gap_closure_plan_validation_sensitivity.py

3 passed
```

Figure validation:

```text
1709x847, dynamic range=255
```
