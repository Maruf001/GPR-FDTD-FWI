# Experiment 1575: Follow-Up Objective-Policy Command-Replay Runtime-Audit Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `1574` validator with controlled damaged variants of the
run `1573` runtime audit.

## Output

```text
outputs/experiments/1575_local_2d_state_consistent_objective_revision_followup_objective_policy_command_replay_runtime_audit_validation_sensitivity
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_followup_objective_policy_command_replay_runtime_audit_validation_sensitivity_scenario_rows.csv
data/local_2d_state_consistent_objective_revision_followup_objective_policy_command_replay_runtime_audit_validation_sensitivity_summary.json
figures/local_2d_state_consistent_objective_revision_followup_objective_policy_command_replay_runtime_audit_validation_sensitivity.png
```

## Result

```text
scenarios:                         19
expected pass scenarios:           1
expected failure scenarios:        18
observed pass scenarios:           1
observed failure scenarios:        18
unexpected outcomes:               0
runtime-audit sensitivity ready:   true
validator accepts exact run 1573:  true
validator rejects damaged variants:true
physical claim ready:              false
GPU work ready:                    false
field transfer ready:              false
field FWI ready:                   false
3D/HPC ready:                      false
```

The validator accepts the exact run `1573` runtime audit and rejects controlled
damage to readiness, counts, timing rates, downstream state, figure validation,
and script snapshots.

## Decision

Use runs `1573-1575` as the guarded command-replay runtime-audit block. The
runtime cost is now measured and validated, but it does not change the current
physical, GPU, field-transfer, field-FWI, or 3D/HPC guardrails.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_followup_objective_policy_command_replay_runtime_audit_validation_sensitivity.py
3 passed as part of the 12-test focused set
```

Figure check:

```text
3581x885, dynamic range=255
```
