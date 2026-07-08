# Experiment 1594: Post Runtime-Budget Command Plan Claim Boundary

Date: 2026-06-29

## Purpose

Fold the guarded non-executed runtime-budget command plan from runs `1591-1593`
into the current 2D claim boundary.

## Output

```text
outputs/experiments/1594_local_2d_state_consistent_objective_revision_post_runtime_budget_command_plan_claim_boundary
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_post_runtime_budget_command_plan_claim_boundary_claim_rows.csv
data/local_2d_state_consistent_objective_revision_post_runtime_budget_command_plan_claim_boundary_summary.json
figures/local_2d_state_consistent_objective_revision_post_runtime_budget_command_plan_claim_boundary.png
scripts/script_snapshot_manifest.json
```

## Result

```text
claims:                                      29
guarded claims:                              26
blocked claims:                              3
runtime-budget command plan ready:           true
command-plan sensitivity ready:              true
plan rows:                                   5
budget tiers:                                5
default budget:                              60 min
default recommended grid models:             90
two-hour grid models:                        90
first budget allowing 200-grid screen:       150 min
large-screen grid models:                    200
command templates emitted:                   0
commands executed:                           false
new FDTD executed:                           false
parameterized grid-screen CLI available:     false
run-specific script required before run:     true
physical claim ready:                        false
GPU work ready:                              false
field transfer ready:                        false
field FWI ready:                             false
3D/HPC ready:                                false
```

The new guarded claim records that the 2D runtime-budget plan is useful as a
planning boundary but is not an executable FDTD command path. A future run
still needs a dedicated run-specific script before new FDTD is launched.

## Decision

Use this as the current 2D claim boundary after the command-plan block. No new
FDTD, physical, GPU, field-transfer, field-FWI, or 3D/HPC claim is promoted.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_post_runtime_budget_command_plan_claim_boundary.py
5 passed
```

Figure check:

```text
3941x906, dynamic range=255
```
