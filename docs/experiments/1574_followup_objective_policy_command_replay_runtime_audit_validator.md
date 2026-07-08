# Experiment 1574: Follow-Up Objective-Policy Command-Replay Runtime-Audit Validator

Date: 2026-06-29

## Purpose

Validate run `1573` from saved artifacts.

The validator checks runtime readiness, replay counts, timing rates, failure
taxonomy, blocked downstream states, figure validation, and script snapshots.

## Output

```text
outputs/experiments/1574_local_2d_state_consistent_objective_revision_followup_objective_policy_command_replay_runtime_audit_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_followup_objective_policy_command_replay_runtime_audit_validator_checks.csv
data/local_2d_state_consistent_objective_revision_followup_objective_policy_command_replay_runtime_audit_validator_summary.json
figures/local_2d_state_consistent_objective_revision_followup_objective_policy_command_replay_runtime_audit_validator.png
```

## Result

```text
validation checks:                 5
validation passes:                 5
blocking failures:                 0
runtime-audit validation ready:    true
elapsed seconds:                   782.566
seconds per grid model:            39.1283
seconds per candidate row:         1.63035
physical claim ready:              false
GPU work ready:                    false
field transfer ready:              false
field FWI ready:                   false
3D/HPC ready:                      false
```

## Decision

Use this validator as the artifact guard for run `1573`. Sensitivity testing
remains required before closing the runtime-audit block.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_followup_objective_policy_command_replay_runtime_audit_validator.py
5 passed as part of the 12-test focused set
```

Figure check:

```text
2645x841, dynamic range=255
```
