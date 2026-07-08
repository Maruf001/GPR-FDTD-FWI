# Field Experiment 480: Live Receipt Collection-Day Route Spec Validator

Date: 2026-06-30

## Purpose

Validate the collection-day route specification from run `479`.

Run `479` turns the live field closure into six route phases with 33 required
files and 183 receipt checks. This run verifies that route shape, current
absence state, downstream blocking, and artifacts.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/480_gssi51600s_controlled_collection_live_receipt_collection_day_route_spec_validator
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_live_receipt_collection_day_route_spec_validator_check_rows.csv
data/gssi51600s_controlled_collection_live_receipt_collection_day_route_spec_validator_summary.json
figures/gssi51600s_controlled_collection_live_receipt_collection_day_route_spec_validator.png
scripts/
```

## Result

```text
checks:                          5
passed checks:                   5
failed checks:                   0
routes:                          33
phases:                          6
DZT routes:                      9
metadata JSON routes:            24
total required receipt checks:   183
current present files:           0
current receipt-ready files:     0
ready phases:                    0
field FWI ready:                 false
field 3D/HPC ready:              false
gpu priority:                    none
```

## Interpretation

The collection-day route spec is a valid staging contract. It does not promote
the current archive to field evidence.

## Decision

Use run `480` as the validator for run `479`. Keep field evidence, field FWI,
and field 3D/HPC blocked until all collection-day routes pass.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_live_receipt_collection_day_route_spec_validator.py

3 passed
```

Figure validation:

```text
2285x841, dynamic range=255
```
