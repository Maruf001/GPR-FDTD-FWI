# Field Experiment 585: Collection-Day Return Preflight Claim Boundary Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `584` claim-boundary validator by damaging the saved run
`583` state in controlled ways.

This run checks whether false claim counts, false guarded or blocked states,
candidate-file promotion, preflight-pass promotion, field-evidence promotion,
downstream promotion, figure damage, and script-snapshot damage are rejected.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/585_gssi51600s_controlled_collection_trace_pairing_collection_day_return_preflight_claim_boundary_validation_sensitivity
```

## Result

```text
source validator ready:           true
scenarios:                        14
expected pass scenarios:          1
expected fail scenarios:          13
observed pass scenarios:          1
observed fail scenarios:          13
unexpected outcomes:              0
damaged scenarios rejected:       13
gpu priority:                     none
```

## Decision

Use runs `583-585` as the guarded post-preflight claim-boundary block for the
controlled-collection field stream.

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
2788x858, dynamic range=255
```
