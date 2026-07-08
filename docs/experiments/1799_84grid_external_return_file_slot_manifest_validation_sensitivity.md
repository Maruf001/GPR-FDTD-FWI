# Experiment 1799: 84-Grid External Return File-Slot Manifest Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `1798` validator with damaged versions of the run `1797`
file-slot manifest.

The damaged scenarios include slot-count damage, stage-count damage, file-kind
damage, paired-job damage, fake producer-file presence, fake preflight passes,
fake ready slots, materialization promotion, FDTD promotion, downstream
promotion, figure damage, and script-snapshot damage.

## Output

```text
outputs/experiments/1799_local_2d_state_consistent_objective_revision_84grid_external_return_file_slot_manifest_validation_sensitivity
```

## Result

```text
scenarios:                         16
expected pass scenarios:           1
expected fail scenarios:           15
observed pass scenarios:           1
observed fail scenarios:           15
unexpected outcomes:               0
damaged scenarios:                 15
damaged scenarios rejected:        15
gpu priority:                      none
```

The exact saved manifest passes. All fifteen damaged variants fail.

## Decision

Use this sensitivity run to keep the 84-grid file-slot manifest fail-closed.
Do not promote materialization, new FDTD execution, field transfer, or 3D/HPC
from partial or damaged external-return files.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_external_return_file_slot_manifest_validation_sensitivity.py

3 passed
```

Figure check:

```text
3040x868, dynamic range=255
```
