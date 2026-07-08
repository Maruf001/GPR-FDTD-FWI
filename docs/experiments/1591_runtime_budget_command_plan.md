# Experiment 1591: Runtime Budget Command Plan

Date: 2026-06-29

## Purpose

Convert the runtime-budget triage policy from run `1585` into a concrete
non-executed command plan for bounded 2D CPU screening.

This run records the budget tiers and selected grid-model counts, but it does
not emit a runnable parameterized FDTD command. A run-specific script is still
required before any new FDTD execution.

## Output

```text
outputs/experiments/1591_local_2d_state_consistent_objective_revision_runtime_budget_command_plan
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_runtime_budget_command_plan_plan_rows.csv
data/local_2d_state_consistent_objective_revision_runtime_budget_command_plan_non_executed_plan.sh
data/local_2d_state_consistent_objective_revision_runtime_budget_command_plan_summary.json
figures/local_2d_state_consistent_objective_revision_runtime_budget_command_plan.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source triage ready:                         true
runtime-budget command plan ready:           true
plan rows:                                   5
budget tiers:                                5
default budget:                              60 min
default recommended grid models:             90
default recommended scenario:                fine_transition_90
two-hour recommended grid models:            90
first budget allowing 200-grid screen:       150 min
large-screen grid models:                    200
command templates emitted:                   0
commands executed:                           false
new FDTD executed:                           false
run-specific script required before run:     true
physical claim ready:                        false
GPU work ready:                              false
field transfer ready:                        false
field FWI ready:                             false
3D/HPC ready:                                false
```

The plan preserves the run `1585` decision: the current default bounded CPU
screen is 90 grid models in a 60-minute budget. The 200-grid screen first fits
the defined budget tiers at 150 minutes and still needs a dedicated
run-specific script before execution.

## Decision

Use this as a planning run sheet only. It does not execute new FDTD and does
not promote physical, GPU, field-transfer, field-FWI, or 3D/HPC readiness.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_runtime_budget_command_plan.py
4 passed
```

Figure check:

```text
3401x881, dynamic range=255
```
