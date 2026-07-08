# Experiment 1569: Follow-Up Objective-Policy Command Replay Audit Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `1568` validator with controlled damaged variants of the
run `1567` aggregate replay audit.

## Output

```text
outputs/experiments/1569_local_2d_state_consistent_objective_revision_followup_objective_policy_command_replay_audit_validation_sensitivity
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_followup_objective_policy_command_replay_audit_validation_sensitivity_scenario_rows.csv
data/local_2d_state_consistent_objective_revision_followup_objective_policy_command_replay_audit_validation_sensitivity_summary.json
figures/local_2d_state_consistent_objective_revision_followup_objective_policy_command_replay_audit_validation_sensitivity.png
```

## Result

```text
scenarios:                         19
expected pass scenarios:           1
expected failure scenarios:        18
observed pass scenarios:           1
observed failure scenarios:        18
unexpected outcomes:               0
replay sensitivity ready:          true
validator accepts exact run 1567:  true
validator rejects damaged variants:true
aggregate replay executed:         true
physical claim ready:              false
GPU work ready:                    false
field transfer ready:              false
field FWI ready:                   false
3D/HPC ready:                      false
```

The validator accepts the exact run `1567` replay audit and rejects controlled
damage to readiness, execution state, counts, failure taxonomy, output scope,
downstream promotion, figure validation, and script snapshots.

## Decision

Use runs `1567-1569` as the guarded executed aggregate CPU replay block. Keep
physical, GPU, field-transfer, field-FWI, and 3D/HPC claims blocked.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_followup_objective_policy_command_replay_audit_validation_sensitivity.py
3 passed as part of the 11-test focused set
```

Figure check:

```text
3581x890, dynamic range=255
```
