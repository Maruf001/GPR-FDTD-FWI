# Experiment 1573: Follow-Up Objective-Policy Command-Replay Runtime Audit

Date: 2026-06-29

## Purpose

Measure the wall-clock cost of the executed aggregate CPU replay from run
`1567` and keep the result tied to the current objective-policy branch.

This run does not introduce a new physical model or a new inversion claim. It
answers a narrower operational question:

```text
How expensive is the saved aggregate replay, and does that cost measurement
change the current decision boundary?
```

## Output

```text
outputs/experiments/1573_local_2d_state_consistent_objective_revision_followup_objective_policy_command_replay_runtime_audit
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_followup_objective_policy_command_replay_runtime_audit_metric_rows.csv
data/local_2d_state_consistent_objective_revision_followup_objective_policy_command_replay_runtime_audit_summary.json
figures/local_2d_state_consistent_objective_revision_followup_objective_policy_command_replay_runtime_audit.png
```

## Result

```text
source replay ready:               true
runtime audit ready:               true
aggregate replay executed:         true
grid models:                       20
objective rows:                    120
candidate rows:                    480
any-failure models:                20
all-objective-failure models:      0
elapsed seconds:                   782.566
elapsed minutes:                   13.0428
seconds per grid model:            39.1283
seconds per objective row:         6.52138
seconds per candidate row:         1.63035
grid models per minute:            1.53342
candidate rows per second:         0.613367
per-objective CLI available:       false
physical claim ready:              false
GPU work ready:                    false
field transfer ready:              false
field FWI ready:                   false
3D/HPC ready:                      false
```

The replay remains useful as a bounded CPU audit. It is not a per-objective
execution interface, and the timing result does not promote physical, GPU,
field-transfer, field-FWI, or 3D/HPC readiness.

## Decision

Use this run as the runtime-cost record for the saved objective-policy command
replay. Keep the current 2D branch guarded; do not use the timing result as a
reason to launch heavier compute or field transfer.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_followup_objective_policy_command_replay_runtime_audit.py
4 passed as part of the 12-test focused set
```

Figure check:

```text
3401x878, dynamic range=255
```
