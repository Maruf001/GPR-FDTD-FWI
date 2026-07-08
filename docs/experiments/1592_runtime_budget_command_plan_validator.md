# Experiment 1592: Runtime Budget Command Plan Validator

Date: 2026-06-29

## Purpose

Validate the non-executed command plan from run `1591` using only saved
artifacts.

## Output

```text
outputs/experiments/1592_local_2d_state_consistent_objective_revision_runtime_budget_command_plan_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_runtime_budget_command_plan_validator_checks.csv
data/local_2d_state_consistent_objective_revision_runtime_budget_command_plan_validator_summary.json
figures/local_2d_state_consistent_objective_revision_runtime_budget_command_plan_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:                           6
validation checks passed:                    6
blocking failures:                           0
runtime-budget command-plan validation:      true
plan rows:                                   5
default recommended grid models:             90
large-screen grid models:                    200
commands executed:                           false
new FDTD executed:                           false
parameterized grid-screen CLI available:     false
physical claim ready:                        false
GPU work ready:                              false
field transfer ready:                        false
field FWI ready:                             false
3D/HPC ready:                                false
```

The validator confirms that run `1591` preserves the 15, 30, 60, 120, and
150-minute budget rows, keeps the 60-minute default at 90 grid models, keeps
the 200-grid screen at the 150-minute tier, emits no hidden command templates,
and leaves downstream claims blocked.

## Decision

Use this validator as the artifact guard for run `1591`.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_runtime_budget_command_plan_validator.py
4 passed
```

Figure check:

```text
2645x857, dynamic range=255
```
