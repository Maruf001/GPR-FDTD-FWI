# Experiment 1841: BEM Stage-1 External Artifact Receipt Checklist Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `1840` receipt checklist validator.

This run checks that the validator accepts only the exact absent-live-artifact
receipt state and rejects damaged or prematurely promoted states.

This is a CPU-only validation-sensitivity run. It does not create live
artifacts, authorize FDTD execution, run FDTD, complete a BEM/FDTD comparison,
transfer to field evidence, or start 3D/HPC work.

## Output

```text
outputs/experiments/1841_local_2d_bem_stage1_complex_fdtd_external_artifact_receipt_checklist_validation_sensitivity
```

## Result

```text
source validator ready:                true
scenarios:                             19
expected pass scenarios:               1
expected fail scenarios:               18
observed pass scenarios:               1
observed fail scenarios:               18
unexpected outcomes:                   0
damaged scenarios:                     18
damaged scenarios rejected:            18
FDTD executed now:                     false
real BEM/FDTD comparison ready:        false
field transfer ready:                  false
3D/HPC ready:                          false
gpu priority:                          none
```

Rejected damaged states include:

```text
checklist readiness damage
row removal
artifact-key damage
false live-file presence
false artifact acceptance
filled observed SHA-256
filled observed file size
filled receipt timestamp
false acceptance-recheck readiness
artifact-specific schema-check damage
FDTD authorization promotion
FDTD execution promotion
BEM/FDTD comparison promotion
field-transfer promotion
3D/HPC promotion
GPU-priority promotion
figure damage
script-snapshot damage
```

## Interpretation

The receipt checklist validator is fail-closed. It accepts the intended
two-row absent-live-file state and rejects every tested damaged or prematurely
promoted state.

## Decision

Use runs `1839-1841` as the guarded BEM stage-1 external artifact receipt
checklist block. Keep FDTD authorization and BEM/FDTD comparison blocked until
both live artifacts pass acceptance.

## Validation

Focused tests:

```text
tests/test_local_2d_bem_stage1_complex_fdtd_external_artifact_receipt_checklist_validation_sensitivity.py
3 passed
```

Figure check:

```text
3131x889, dynamic range=255
```
