# Experiment 1814: BEM Stage-1 Complex FDTD Live Approval Directory Scaffold Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `1813` validator by damaging the saved run `1812` directory
scaffold in controlled ways.

The sensitivity set checks source-readiness damage, row-shape damage, directory
absence, false approval-file presence, false approval acceptance, false FDTD
authorization, false FDTD execution, downstream promotion, figure damage, and
script-snapshot damage.

## Output

```text
outputs/experiments/1814_local_2d_bem_stage1_complex_fdtd_live_approval_directory_scaffold_validation_sensitivity
```

## Result

```text
scenarios:                         15
expected passes:                    1
expected failures:                 14
observed passes:                    1
observed failures:                 14
unexpected outcomes:                0
damaged scenarios:                 14
damaged scenarios rejected:        14
gpu priority:                    none
```

The exact saved empty-directory state passes. All damaged states fail:

```text
policy-label damage
scaffold-readiness damage
source-readiness damage
row-count damage
directory-absence damage
live approval-file promotion
accepted approval promotion
FDTD authorization promotion
FDTD execution promotion
comparison promotion
field-transfer promotion
3D/HPC promotion
figure damage
script-snapshot damage
```

## Interpretation

The approval-directory scaffold validator accepts only the exact saved
empty-directory state and rejects controlled damage to source readiness, row
shape, directory presence, approval-file presence, approval acceptance, FDTD
authorization/execution, downstream promotion, figure validation, and script
snapshots.

## Decision

Use runs `1812-1814` as the guarded empty approval-directory scaffold block.

## Validation

Focused tests:

```text
tests/test_local_2d_bem_stage1_complex_fdtd_live_approval_directory_scaffold.py
tests/test_local_2d_bem_stage1_complex_fdtd_live_approval_directory_scaffold_validator.py
tests/test_local_2d_bem_stage1_complex_fdtd_live_approval_directory_scaffold_validation_sensitivity.py
8 passed
```

Figure check:

```text
3131x884, dynamic range=255
```
