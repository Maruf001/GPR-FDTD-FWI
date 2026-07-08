# Field Experiment 594: Collection Return File-Slot Manifest Claim Boundary Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `593` validator with damaged versions of the run `592`
claim boundary.

The damaged scenarios include claim-count drift, missing guarded claims,
file-slot count damage, stage-shape damage, dependency-count damage, false
preflight promotion, false field-analysis promotion, figure damage, and
script-snapshot damage.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/594_gssi51600s_controlled_collection_trace_pairing_collection_day_return_file_slot_manifest_claim_boundary_validation_sensitivity
```

## Result

```text
scenarios:                      20
expected pass scenarios:        1
expected fail scenarios:        19
observed pass scenarios:        1
observed fail scenarios:        19
unexpected outcomes:            0
damaged scenarios:              19
damaged scenarios rejected:     19
gpu priority:                   none
```

The exact saved claim boundary passes. All nineteen damaged variants fail.

## Decision

Use runs `592-594` as the current guarded field file-slot manifest
claim-boundary block.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_return_file_slot_manifest_claim_boundary_validation_sensitivity.py

3 passed
```

Figure check:

```text
3581x879, dynamic range=255
```
