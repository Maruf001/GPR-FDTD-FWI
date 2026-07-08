# Field Experiment 630: First-Return Unblock Action Matrix Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `629` unblock-action-matrix validator by damaging the
saved run `628` state in controlled ways.

The sensitivity set checks source readiness damage, row removal, pair-order
damage, false ready-for-recheck promotion, missing-count damage, parent
directory damage, category damage, field-evidence promotion, field FWI
promotion, field 3D/HPC promotion, GPU-priority promotion, figure damage, and
script-snapshot damage.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/630_gssi51600s_controlled_collection_trace_pairing_collection_day_first_return_unblock_action_matrix_validation_sensitivity
```

## Result

```text
scenarios:                         14
expected passes:                    1
expected failures:                 13
observed passes:                    1
observed failures:                 13
unexpected outcomes:                0
damaged scenarios:                 13
controlled field evidence ready: false
field FWI ready:                 false
field 3D/HPC ready:              false
gpu priority:                    none
```

## Decision

Use runs `628-630` as the guarded first-return unblock action matrix block.

## Validation

Focused test:

```text
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_first_return_unblock_action_matrix_validation_sensitivity.py
3 passed
```

Figure check:

```text
2537x855, dynamic range=255
```
