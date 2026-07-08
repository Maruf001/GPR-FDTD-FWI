# Experiment 1567: Follow-Up Objective-Policy Command Replay Audit

Date: 2026-06-29

## Purpose

Execute the aggregate CPU replay authorized by the guarded run `1564` command
plan in a new experiment folder.

This run does not expose a per-objective command path, launch GPU work,
promote a physical acquisition claim, transfer to field data, run field FWI, or
run 3D/HPC work.

## Output

```text
outputs/experiments/1567_local_2d_state_consistent_objective_revision_followup_objective_policy_command_replay_audit
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_followup_objective_policy_command_replay_audit_checks.csv
data/local_2d_state_consistent_objective_revision_followup_objective_policy_command_replay_audit_summary.json
figures/local_2d_state_consistent_objective_revision_followup_objective_policy_command_replay_audit.png
replay_saved_followup_offset_probe_cpu/
```

## Result

```text
aggregate replay executed:         true
replay audit ready:                true
replay validation checks:          5
replay validation passes:          5
replay validation failures:        0
candidate objectives:              highband;late;late_high;veryhigh
excluded objectives:               base;early_high
per-objective CLI available:       false
grid models:                       20
objective rows:                    120
candidate rows:                    480
any-failure models:                20
all-objective-failure models:      0
replay elapsed seconds:            782.566
physical claim ready:              false
GPU work ready:                    false
field transfer ready:              false
field FWI ready:                   false
3D/HPC ready:                      false
```

The aggregate CPU replay reproduces the saved 20-case probe counts and failure
taxonomy in a new run folder. It does not create a per-objective execution
interface and does not promote downstream claims.

## Decision

Use this as the executed aggregate replay audit for the follow-up
objective-policy command plan. Keep physical, GPU, field-transfer, field-FWI,
and 3D/HPC claims blocked.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_followup_objective_policy_command_replay_audit.py
4 passed
```

Figure check:

```text
2771x857, dynamic range=255
```
