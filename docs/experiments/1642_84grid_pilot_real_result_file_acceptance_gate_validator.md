# Experiment 1642: 84-Grid Pilot Real-Result File Acceptance Gate Validator

Date: 2026-06-30

## Purpose

Validate run `1641` from its generated artifacts.

The validator checks source readiness, five-file gate shape, 50 required field
gates, zero accepted outputs, blocked actions, downstream guardrails, figure
quality, and script snapshots.

## Output

```text
outputs/experiments/1642_local_2d_state_consistent_objective_revision_84grid_pilot_real_result_file_acceptance_gate_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_result_file_acceptance_gate_validator_checks.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_result_file_acceptance_gate_validator_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_result_file_acceptance_gate_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:                         5
validation passes:                         5
blocking failures:                         0
result-file gate validation ready:         true
required result files:                     5
required fields:                           50
acceptance actions:                        4
new FDTD executed:                         false
GPU priority:                              none
```

The passing checks are:

```text
source_chain_ready
file_gate_shape_and_zero_acceptance
field_gate_shape_and_zero_acceptance
actions_and_downstream_states_blocked
figure_and_script_snapshots_present
```

## Decision

Run `1641` is internally consistent and can serve as the acceptance gate for
future five-row real pilot result files.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_result_file_acceptance_gate_validator.py
3 passed
```

Figure check:

```text
2285x840, dynamic range=255
```
