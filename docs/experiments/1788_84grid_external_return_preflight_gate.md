# Experiment 1788: 84-Grid External Return Preflight Gate

Date: 2026-07-01

## Purpose

Define the preflight gate for the 84-grid 2D external-return files before any
approval, cache array, or result JSON file is staged into the live external
return area.

This run checks one approval JSON file, ten NumPy cache-array files, and ten
result JSON files. It requires real files and paired cache/result jobs before
materialization can proceed.

This is a CPU-only preflight run. It does not create approval files, does not
create cache arrays, does not create result JSON files, does not execute FDTD,
does not stage files, and does not promote materialization, GPU work, field
transfer, field FWI, or 3D/HPC readiness.

## Output

```text
outputs/experiments/1788_local_2d_state_consistent_objective_revision_84grid_external_return_preflight_gate
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_external_return_preflight_gate_preflight_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_external_return_preflight_gate_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_external_return_preflight_gate.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source staging plan ready:        true
source validation ready:          true
source sensitivity ready:         true
preflight items:                  21
stages:                           5
approval items:                   1
cache-array items:                10
result-JSON items:                10
artifact jobs:                    10
candidate files present:          0
nonzero-size files:               0
approval JSON valid:              0
approval core passed:             0
NPZ loadable:                     0
cache core passed:                0
result JSON valid:                0
result core passed:               0
paired artifact jobs ready:       0
preflight-passed items:           0
ready-to-stage items:             0
executed commands:                0
ready for materialization:        false
new FDTD executed:                false
gpu priority:                     none
```

Required checks:

```text
approval JSON: real JSON, nonblank approval fields, expected approval scope, not a template
cache array: real NPZ, observed-by-case array present, finite numeric arrays, usable shape
result JSON: real JSON, matching payload/job identity, completed solver status, accepted result
paired job: cache array and result JSON both pass before either file is stageable
```

## Interpretation

The 84-grid external-return handoff is now protected by a real-file preflight
gate. The current state remains pre-return: no approval token, cache array, or
result JSON file is present, no paired artifact job is complete, and no item is
ready to stage.

## Decision

Use run `1788` as the preflight gate before staging 84-grid external-return
files. Keep materialization, FDTD execution, GPU work, field transfer, field
FWI, and 3D/HPC blocked until real files pass this gate and the guarded intake
checks.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_external_return_staging_plan.py
tests/test_local_2d_state_consistent_objective_revision_84grid_external_return_staging_plan_validator.py
tests/test_local_2d_state_consistent_objective_revision_84grid_external_return_staging_plan_validation_sensitivity.py
tests/test_local_2d_state_consistent_objective_revision_84grid_external_return_preflight_gate.py

13 passed
```

Python compile check:

```text
run_local_2d_state_consistent_objective_revision_84grid_external_return_preflight_gate.py: pass
tests/test_local_2d_state_consistent_objective_revision_84grid_external_return_preflight_gate.py: pass
```

Figure check:

```text
2212x846, dynamic range=255
```
