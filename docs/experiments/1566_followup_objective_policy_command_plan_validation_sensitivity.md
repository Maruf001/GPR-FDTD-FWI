# Experiment 1566: Follow-Up Objective Policy Command Plan Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `1565` validator with controlled damaged variants of the
run `1564` command plan.

This run checks that the validator accepts the exact saved command plan and
fails closed when source readiness, row counts, objective identity, command
shape, command-execution state, per-objective execution exposure, or downstream
readiness are damaged.

## Output

```text
outputs/experiments/1566_local_2d_state_consistent_objective_revision_followup_objective_policy_command_plan_validation_sensitivity
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_followup_objective_policy_command_plan_validation_sensitivity_scenario_rows.csv
data/local_2d_state_consistent_objective_revision_followup_objective_policy_command_plan_validation_sensitivity_summary.json
figures/local_2d_state_consistent_objective_revision_followup_objective_policy_command_plan_validation_sensitivity.png
```

## Result

```text
scenarios:                         25
expected pass scenarios:           1
expected failure scenarios:        24
observed pass scenarios:           1
observed failure scenarios:        24
unexpected outcomes:               0
sensitivity ready:                 true
commands executed:                 false
GPU work ready:                    false
field transfer ready:              false
field FWI ready:                   false
3D/HPC ready:                      false
```

## Decision

Use runs `1564-1566` as the guarded non-executed command-plan package for the
saved follow-up objective policy. The branch remains CPU-only and does not
justify new GPU, field-transfer, field-FWI, or 3D/HPC work.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_followup_objective_policy_command_plan_validation_sensitivity.py
6 passed as part of the 17-test focused set
```

Figure check:

```text
3581x889, dynamic range=255
```
