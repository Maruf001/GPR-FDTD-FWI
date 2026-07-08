# Experiment 1597: 90-Grid Dry-Run Payload Manifest

Date: 2026-06-29

## Purpose

Convert the guarded runtime-budget command plan from run `1591` into a concrete
90-row dry-run payload manifest.

This run does not execute FDTD. It answers whether the one-hour 90-grid planning
case can be written as explicit review rows before any run-specific execution
script is created.

## Output

```text
outputs/experiments/1597_local_2d_state_consistent_objective_revision_90grid_dry_run_payload_manifest
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_90grid_dry_run_payload_manifest_payload_rows.csv
data/local_2d_state_consistent_objective_revision_90grid_dry_run_payload_manifest_action_rows.csv
data/local_2d_state_consistent_objective_revision_90grid_dry_run_payload_manifest_summary.json
figures/local_2d_state_consistent_objective_revision_90grid_dry_run_payload_manifest.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source command plan ready:                   true
dry-run payload manifest ready:              true
payload rows:                                90
objective profiles:                          5
transition bins:                             18
budget:                                      60 min
selected scenario:                           fine_transition_90
estimated total runtime:                     58.69245 min
estimated seconds per grid:                  39.1283
budget headroom:                             1.30755 min
executable commands:                         0
run-specific execution script available:     false
commands executed:                           false
new FDTD executed:                           false
physical claim ready:                        false
GPU work ready:                              false
field transfer ready:                        false
field FWI ready:                             false
3D/HPC ready:                                false
```

The manifest expands the retained objective profiles into 90 explicit dry-run
rows: five objective profiles across 18 transition bins. Every row is marked as
review-only and execution-blocked.

## Decision

Use this as the review manifest before creating any executable 2D CPU-screen
script. The run does not promote FDTD execution, physical evidence, GPU work,
field transfer, field FWI, or 3D/HPC readiness.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_90grid_dry_run_payload_manifest.py
4 passed
```

Figure check:

```text
3329x881, dynamic range=255
```
