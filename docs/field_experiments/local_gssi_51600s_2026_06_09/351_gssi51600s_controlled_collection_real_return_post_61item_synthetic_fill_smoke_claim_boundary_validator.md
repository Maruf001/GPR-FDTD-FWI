# Field Experiment 351: Post-Synthetic-Fill-Smoke Claim Boundary Validator

Date: 2026-06-29

## Purpose

Validate the saved run `350` field claim boundary from artifacts.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/351_gssi51600s_controlled_collection_real_return_post_61item_synthetic_fill_smoke_claim_boundary_validator
```

## Result

```text
validation checks:                   7
passed checks:                       7
failed checks:                       0
boundary validation ready:           true
claims:                              16
guarded claims:                      12
blocked claims:                      4
packet requirements:                 61
unique return paths:                 49
synthetic packet files:              49
synthetic packet is measured:        false
field evidence ready:                false
```

## Validation

```text
tests/test_gssi_field_controlled_collection_real_return_post_61item_synthetic_fill_smoke_claim_boundary_validator.py
2 passed
```

Figure validation:

```text
3617x893, dynamic range=255
```
