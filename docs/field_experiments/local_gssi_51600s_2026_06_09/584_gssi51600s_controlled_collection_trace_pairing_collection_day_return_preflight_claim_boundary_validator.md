# Field Experiment 584: Collection-Day Return Preflight Claim Boundary Validator

Date: 2026-07-01

## Purpose

Validate the saved run `583` controlled-collection preflight claim boundary.

This validator checks that the boundary has two guarded claims, three blocked
claims, zero candidate files, zero preflight-passed items, and no controlled
field evidence, field FWI, or field 3D/HPC promotion.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/584_gssi51600s_controlled_collection_trace_pairing_collection_day_return_preflight_claim_boundary_validator
```

## Result

```text
validation checks:                7
passed checks:                    7
failed checks:                    0
claims:                           5
guarded claims:                   2
blocked claims:                   3
preflight items:                  33
metadata JSON items:              24
measured DZT items:               9
candidate files present:          0
preflight-passed items:           0
controlled field evidence ready:  false
field FWI ready:                  false
field 3D/HPC ready:               false
gpu priority:                     none
```

## Decision

Use run `584` before citing run `583` as the current controlled-collection
preflight claim boundary.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_return_preflight_claim_boundary.py
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_return_preflight_claim_boundary_validator.py
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_return_preflight_claim_boundary_validation_sensitivity.py

9 passed
```

Figure check:

```text
3293x935, dynamic range=255
```
