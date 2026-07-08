# Experiment 1800: 84-Grid External Return File-Slot Manifest Claim Boundary

Date: 2026-07-01

## Purpose

Record the claim boundary after the 84-grid external-return file-slot manifest.

Runs `1797-1799` defined and hardened the external-return checklist. This run
states what that checklist supports and what remains blocked until real external
files arrive.

## Output

```text
outputs/experiments/1800_local_2d_state_consistent_objective_revision_84grid_external_return_file_slot_manifest_claim_boundary
```

## Result

```text
claims:                         5
guarded claims:                 2
blocked claims:                 3
source manifest ready:          true
source validation ready:         true
source sensitivity ready:        true
file slots:                     21
stage shape:                    1,2,2,8,8
approval JSON slots:            1
cache NPZ slots:                10
result JSON slots:              10
paired artifact slots:          20
artifact jobs:                  10
producer files present:         0
preflight-passed slots:         0
ready slots:                    0
materialization ready:          false
new FDTD executed:              false
field transfer ready:           false
3D/HPC ready:                   false
gpu priority:                   none
```

The two guarded claims are:

| Claim | Supporting runs | Status |
| --- | --- | --- |
| external return file-slot manifest | 1797-1799 | guarded |
| paired artifact job contract | 1794-1799 | guarded |

The blocked claims are real external-return files, observed-by-case
materialization, and new FDTD execution or downstream transfer.

## Interpretation

The 84-grid external return has a concrete file-level contract: one approval
JSON, ten cache NPZ files, and ten result JSON files. The ten cache/result jobs
are paired, so a cache file is not useful without its matching result JSON. No
producer file is present, so this block is a checklist boundary rather than a
materialized 2D result.

## Decision

Use this boundary as the current 2D external-return file-slot checkpoint. Keep
materialization, new FDTD execution, field transfer, and 3D/HPC blocked until
real files pass preflight.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_external_return_file_slot_manifest_claim_boundary.py
tests/test_local_2d_state_consistent_objective_revision_84grid_external_return_file_slot_manifest_claim_boundary_validator.py
tests/test_local_2d_state_consistent_objective_revision_84grid_external_return_file_slot_manifest_claim_boundary_validation_sensitivity.py

9 passed
```

Figure check:

```text
3617x933, dynamic range=255
```
