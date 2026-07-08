# Field Experiment 629: First-Return Unblock Action Matrix Validator

Date: 2026-07-01

## Purpose

Validate the saved run `628` first-return unblock action matrix.

The validator checks source readiness, action-row shape, open artifact counts,
parent/category stability, blocked downstream claim flags, figure output, and
script snapshots.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/629_gssi51600s_controlled_collection_trace_pairing_collection_day_first_return_unblock_action_matrix_validator
```

## Result

```text
validation checks:                   6
checks passed:                       6
checks failed:                       0
action pairs:                        9
open action pairs:                   9
missing DZT files:                   9
missing metadata files:              9
missing artifacts:                   18
parent directories ready:            9
controlled-profile pairs:            3
time-zero pairs:                     3
amplitude-reference pairs:           3
controlled field evidence ready:     false
field FWI ready:                     false
field 3D/HPC ready:                  false
```

## Decision

Use run `628` as the guarded first-return operator action matrix. Do not
promote field evidence or compute claims.

## Validation

Focused test:

```text
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_first_return_unblock_action_matrix_validator.py
3 passed
```

Figure check:

```text
2429x857, dynamic range=255
```
