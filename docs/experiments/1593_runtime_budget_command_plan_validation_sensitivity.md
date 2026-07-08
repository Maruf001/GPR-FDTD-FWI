# Experiment 1593: Runtime Budget Command Plan Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `1592` validator against controlled damage to the command
plan, execution state, downstream state, figure evidence, and script snapshots.

## Output

```text
outputs/experiments/1593_local_2d_state_consistent_objective_revision_runtime_budget_command_plan_validation_sensitivity
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_runtime_budget_command_plan_validation_sensitivity_scenario_rows.csv
data/local_2d_state_consistent_objective_revision_runtime_budget_command_plan_validation_sensitivity_summary.json
figures/local_2d_state_consistent_objective_revision_runtime_budget_command_plan_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
sensitivity scenarios:                       28
expected pass scenarios:                     1
observed pass scenarios:                     1
expected failure scenarios:                  27
observed failure scenarios:                  27
unexpected outcomes:                         0
validation sensitivity ready:                true
validator accepts exact run 1591:            true
validator rejects damaged variants:          true
commands executed:                           false
new FDTD executed:                           false
parameterized grid-screen CLI available:     false
physical claim ready:                        false
GPU work ready:                              false
field transfer ready:                        false
field FWI ready:                             false
3D/HPC ready:                                false
```

The validator accepts the exact run `1591` command plan and rejects damage to
source readiness, row count, budget decisions, hidden execution flags, hidden
command templates, downstream promotion flags, figure validation, and script
snapshots.

## Decision

Use runs `1591-1593` as the guarded 2D runtime-budget command-plan block. The
block is ready as a planning artifact but still does not justify automatic new
FDTD, GPU, field-transfer, field-FWI, or 3D/HPC execution.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_runtime_budget_command_plan_validation_sensitivity.py
4 passed
```

Figure check:

```text
3581x890, dynamic range=255
```
