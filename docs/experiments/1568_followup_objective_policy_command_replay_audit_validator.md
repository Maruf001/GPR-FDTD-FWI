# Experiment 1568: Follow-Up Objective-Policy Command Replay Audit Validator

Date: 2026-06-29

## Purpose

Validate run `1567` from saved artifacts.

The validator checks replay readiness, aggregate execution state, count and
failure-taxonomy agreement, replay output scope, blocked downstream claims,
figure validation, and script snapshots.

## Output

```text
outputs/experiments/1568_local_2d_state_consistent_objective_revision_followup_objective_policy_command_replay_audit_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_followup_objective_policy_command_replay_audit_validator_checks.csv
data/local_2d_state_consistent_objective_revision_followup_objective_policy_command_replay_audit_validator_summary.json
figures/local_2d_state_consistent_objective_revision_followup_objective_policy_command_replay_audit_validator.png
```

## Result

```text
validation checks:                 6
validation passes:                 6
blocking failures:                 0
replay audit validation ready:     true
aggregate replay executed:         true
grid models:                       20
objective rows:                    120
candidate rows:                    480
any-failure models:                20
all-objective-failure models:      0
physical claim ready:              false
GPU work ready:                    false
field transfer ready:              false
field FWI ready:                   false
3D/HPC ready:                      false
```

## Decision

Use this validator as the artifact guard for run `1567`. Sensitivity testing
remains required before closing the replay block.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_followup_objective_policy_command_replay_audit_validator.py
4 passed as part of the 11-test focused set
```

Figure check:

```text
2645x839, dynamic range=255
```
