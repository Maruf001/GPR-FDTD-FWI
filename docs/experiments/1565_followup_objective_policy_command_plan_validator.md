# Experiment 1565: Follow-Up Objective Policy Command Plan Validator

Date: 2026-06-29

## Purpose

Validate run `1564` from the saved artifacts.

This validator checks that the command plan has one optional CPU replay
command, four retained candidate objectives, two excluded objectives, no hidden
per-objective execution interface, and no downstream physical/GPU/field/3D
promotion.

## Output

```text
outputs/experiments/1565_local_2d_state_consistent_objective_revision_followup_objective_policy_command_plan_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_followup_objective_policy_command_plan_validator_checks.csv
data/local_2d_state_consistent_objective_revision_followup_objective_policy_command_plan_validator_summary.json
figures/local_2d_state_consistent_objective_revision_followup_objective_policy_command_plan_validator.png
```

## Result

```text
validation checks:                 6
validation passes:                 6
blocking failures:                 0
validation ready:                  true
source command rows:               7
source candidate objectives:       4
source excluded objectives:        2
commands executed:                 false
GPU work ready:                    false
field transfer ready:              false
3D/HPC ready:                      false
```

## Decision

Use this as the positive validator for the run `1564` command plan.
Sensitivity testing is required before treating the block as closed.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_followup_objective_policy_command_plan_validator.py
6 passed as part of the 17-test focused set
```

Figure check:

```text
2645x856, dynamic range=255
```
