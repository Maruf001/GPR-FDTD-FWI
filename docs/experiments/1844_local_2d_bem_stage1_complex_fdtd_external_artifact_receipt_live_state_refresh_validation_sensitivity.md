# Experiment 1844: BEM Stage-1 External Artifact Receipt Live-State Refresh Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `1843` live-state refresh validator.

This run checks that the validator accepts only the exact no-live-artifact
state and rejects damaged or prematurely promoted states, including false live
files, filled hash or size fields, parse-check promotion, accepted-artifact
promotion, FDTD authorization, FDTD execution, BEM/FDTD comparison, field
transfer, 3D/HPC promotion, GPU-priority promotion, figure damage, and
script-snapshot damage.

## Output

```text
outputs/experiments/1844_local_2d_bem_stage1_complex_fdtd_external_artifact_receipt_live_state_refresh_validation_sensitivity
```

## Result

```text
source validator ready:                true
scenarios:                             21
expected pass scenarios:               1
expected fail scenarios:               20
observed pass scenarios:               1
observed fail scenarios:               20
unexpected outcomes:                   0
damaged scenarios:                     20
damaged scenarios rejected:            20
live files found:                      0
missing files:                         2
accepted artifacts:                    0
FDTD producer authorized now:          false
FDTD executed now:                     false
real BEM/FDTD comparison ready:        false
field transfer ready:                  false
3D/HPC ready:                          false
gpu priority:                          none
```

Rejected damaged states include:

```text
refresh-not-ready state
row removal
artifact-key damage
parent-missing damage
false live-file presence
filled observed SHA-256
filled observed file size
approval-JSON parse promotion
partial-return CSV parse promotion
schema/parse promotion
acceptance-recheck promotion
accepted-artifact promotion
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

The live-state refresh validator is fail-closed. It accepts the exact state
where both required external artifacts are absent and rejects every tested
damaged or prematurely promoted state.

## Decision

Use runs `1842-1844` as the guarded live-state refresh block for the BEM
stage-1 external artifact handoff. Keep FDTD authorization and BEM/FDTD
comparison blocked until both live artifacts pass acceptance.

## Validation

Focused tests:

```text
tests/test_local_2d_bem_stage1_complex_fdtd_external_artifact_receipt_live_state_refresh.py
tests/test_local_2d_bem_stage1_complex_fdtd_external_artifact_receipt_live_state_refresh_validator.py
tests/test_local_2d_bem_stage1_complex_fdtd_external_artifact_receipt_live_state_refresh_validation_sensitivity.py
12 passed
```

Figure check:

```text
3329x886, dynamic range=255
```
