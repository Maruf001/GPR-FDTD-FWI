# Experiment 1850: BEM Stage-1 FDTD Source/Receiver Geometry Lock Audit Validation Sensitivity

Date: 2026-07-02

## Purpose

Stress-test the run `1849` source/receiver geometry lock audit validator.

This run checks that the validator accepts only the exact saved geometry-lock
state and rejects damaged lock rows, missing required-lock flags, false lock
satisfaction, block demotion, live-file promotion, FDTD authorization or
execution promotion, BEM/FDTD comparison promotion, BEM metric damage,
field/3D/GPU promotion, figure damage, and script-snapshot damage.

## Output

```text
outputs/experiments/1850_local_2d_bem_stage1_complex_fdtd_source_receiver_geometry_lock_audit_validation_sensitivity
```

## Result

```text
source validator ready:                    true
scenarios:                                 22
expected pass scenarios:                   1
expected fail scenarios:                   21
observed pass scenarios:                   1
observed fail scenarios:                   21
unexpected outcomes:                       0
damaged scenarios:                         21
damaged scenarios rejected:                21
geometry lock rows:                        6
required geometry locks:                   6
currently satisfied geometry locks:        0
live files:                                0
missing files:                             2
FDTD producer authorized now:              false
FDTD executed now:                         false
real BEM/FDTD comparison ready:            false
geometry locks ready for authorization:    false
geometry locks ready for comparison:       false
field transfer ready:                      false
3D/HPC ready:                              false
gpu priority:                              none
```

Rejected damaged states include:

```text
audit-not-ready state
row removal
lock-id damage
required-lock damage
false lock satisfaction
authorization-block demotion
comparison-block demotion
live-file promotion
missing-file-count damage
FDTD authorization promotion
FDTD execution promotion
BEM/FDTD comparison promotion
BEM offset-metric damage
BEM antenna-z metric damage
geometry-lock authorization promotion
geometry-lock comparison promotion
field-transfer promotion
3D/HPC promotion
GPU-priority promotion
figure damage
script-snapshot damage
```

## Interpretation

The geometry-lock validator is fail-closed. It accepts the exact saved
2D-side geometry-lock state and rejects damaged locks or premature FDTD,
comparison, field, 3D, or GPU promotion.

## Decision

Use runs `1848-1850` as the guarded 2D-side geometry-lock boundary for the BEM
stage-1 FDTD return.

## Validation

Focused tests:

```text
tests/test_local_2d_bem_stage1_complex_fdtd_source_receiver_geometry_lock_audit.py
tests/test_local_2d_bem_stage1_complex_fdtd_source_receiver_geometry_lock_audit_validator.py
tests/test_local_2d_bem_stage1_complex_fdtd_source_receiver_geometry_lock_audit_validation_sensitivity.py
11 passed
```

Python compile check:

```text
run_local_2d_bem_stage1_complex_fdtd_source_receiver_geometry_lock_audit.py
run_local_2d_bem_stage1_complex_fdtd_source_receiver_geometry_lock_audit_validator.py
run_local_2d_bem_stage1_complex_fdtd_source_receiver_geometry_lock_audit_validation_sensitivity.py
tests/test_local_2d_bem_stage1_complex_fdtd_source_receiver_geometry_lock_audit.py
tests/test_local_2d_bem_stage1_complex_fdtd_source_receiver_geometry_lock_audit_validator.py
tests/test_local_2d_bem_stage1_complex_fdtd_source_receiver_geometry_lock_audit_validation_sensitivity.py
pass
```

Figure check:

```text
3401x878, dynamic range=255
```
