# Field Experiment 474: Live Receipt Acceptance Gate Staging Gap Closure Plan Validator

Date: 2026-06-30

## Purpose

Validate run `473` from its saved artifacts.

This run checks the six closure groups, the exact 33-row missing-file table,
blocked downstream states, and figure/script artifacts.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/474_gssi51600s_controlled_collection_live_receipt_acceptance_gate_staging_gap_closure_plan_validator
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_live_receipt_acceptance_gate_staging_gap_closure_plan_validator_check_rows.csv
data/gssi51600s_controlled_collection_live_receipt_acceptance_gate_staging_gap_closure_plan_validator_summary.json
figures/gssi51600s_controlled_collection_live_receipt_acceptance_gate_staging_gap_closure_plan_validator.png
scripts/
```

## Result

```text
check count:                             5
passed checks:                           5
failed checks:                           0
closure groups:                          6
missing files:                           33
missing DZT files:                       9
missing metadata JSON files:             24
ready groups:                            0
parser ready:                            false
provenance ready:                        false
archive ready:                           false
controlled field evidence ready:         false
field FWI ready:                         false
field 3D/HPC ready:                      false
gpu priority:                            none
```

## Interpretation

The closure plan is internally consistent and preserves the field-side
no-evidence boundary.

## Decision

Use run `474` as the artifact validator for run `473`.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_live_receipt_acceptance_gate_staging_gap_closure_plan_validator.py

3 passed
```

Figure validation:

```text
2285x842, dynamic range=255
```
