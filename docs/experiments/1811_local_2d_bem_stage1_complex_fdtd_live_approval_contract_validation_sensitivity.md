# Experiment 1811: BEM Stage-1 Complex FDTD Live Approval Contract Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `1810` validator by damaging the saved run `1809` live
approval contract in controlled ways.

The sensitivity set checks source-readiness damage, contract-shape damage,
approval-field damage, partial-return schema damage, receiver/frequency damage,
false live-file presence, false approval acceptance, false FDTD authorization,
false FDTD execution, downstream promotion, figure damage, and script-snapshot
damage.

## Output

```text
outputs/experiments/1811_local_2d_bem_stage1_complex_fdtd_live_approval_contract_validation_sensitivity
```

## Result

```text
scenarios:                         19
expected passes:                    1
expected failures:                 18
observed passes:                    1
observed failures:                 18
unexpected outcomes:                0
damaged scenarios:                 18
damaged scenarios rejected:        18
gpu priority:                    none
```

The exact saved contract passes. All damaged states fail:

```text
policy-label damage
contract-readiness damage
source-readiness damage
contract row-count damage
approval field-count damage
partial column-count damage
receiver identity damage
frequency identity damage
live approval-file promotion
BEM partial-file promotion
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

The live-approval contract validator accepts only the exact saved
non-authorizing contract and rejects controlled damage to source readiness,
contract shape, identity, file presence, approval acceptance, FDTD
authorization/execution, downstream promotion, figure validation, and script
snapshots.

## Decision

Use runs `1809-1811` as the guarded 2D live-approval contract for the BEM
stage-1 FDTD return.

## Validation

Focused tests:

```text
tests/test_local_2d_bem_stage1_complex_fdtd_live_approval_contract.py
tests/test_local_2d_bem_stage1_complex_fdtd_live_approval_contract_validator.py
tests/test_local_2d_bem_stage1_complex_fdtd_live_approval_contract_validation_sensitivity.py
8 passed
```

Figure check:

```text
3617x884, dynamic range=255
```
