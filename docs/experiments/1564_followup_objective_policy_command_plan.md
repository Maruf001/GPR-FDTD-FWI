# Experiment 1564: Follow-Up Objective Policy Command Plan

Date: 2026-06-29

## Purpose

Convert the guarded follow-up objective policy from runs `1558-1563` into a
non-executed command and selection plan.

This is a CPU-side planning artifact. It does not run new FDTD/FWI
simulations, execute the generated replay command, launch GPU/HPC work, compare
against field data, or promote physical, field-transfer, field-FWI, or 3D/HPC
claims.

## Output

```text
outputs/experiments/1564_local_2d_state_consistent_objective_revision_followup_objective_policy_command_plan
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_followup_objective_policy_command_plan_rows.csv
data/local_2d_state_consistent_objective_revision_followup_objective_policy_command_plan_summary.json
commands/local_2d_state_consistent_objective_revision_followup_objective_policy_command_plan_commands.sh
figures/local_2d_state_consistent_objective_revision_followup_objective_policy_command_plan.png
```

## Result

```text
command rows:                      7
aggregate replay commands:         1
candidate objectives:              highband;late;late_high;veryhigh
excluded objectives:               base;early_high
per-objective CLI available:       false
commands executed:                 false
command plan ready:                true
GPU work ready:                    false
field transfer ready:              false
field FWI ready:                   false
3D/HPC ready:                      false
```

The replay command is intentionally aggregate-level. The underlying follow-up
probe script does not expose a per-objective command-line interface, so this
run records one optional CPU replay path for the saved probe and keeps the
objective rows as selection-policy rows.

## Decision

Use this as the non-executed command and selection plan for the saved follow-up
offset probe. Do not promote per-objective reruns, GPU work, field transfer,
field FWI, or 3D/HPC work from this branch.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_followup_objective_policy_command_plan.py
5 passed
```

Figure check:

```text
2644x864, dynamic range=255
```
