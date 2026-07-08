# Field Experiment 549: Integrated Synthetic Receipt Mechanics Smoke Validator

Date: 2026-07-01

## Purpose

Validate run `548` from saved artifacts.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/549_gssi51600s_controlled_collection_live_receipt_integrated_synthetic_mechanics_smoke_validator
```

## Result

```text
checks:                         6
passed:                         6
failed:                         0
synthetic receipt items:         33
synthetic receipt item passes:   33
accepted live receipt items:     0
live receipt ready:              false
field FWI ready:                 false
field 3D/HPC ready:              false
```

## Decision

Run `548` is valid as output-local positive-control coverage only.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_live_receipt_integrated_synthetic_mechanics_smoke_validator.py
3 passed
```

