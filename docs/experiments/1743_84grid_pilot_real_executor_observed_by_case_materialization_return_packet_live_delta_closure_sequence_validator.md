# Experiment 1743: 84-Grid Materialization Return-Packet Live Delta Closure Sequence Validator

Date: 2026-06-30

## Purpose

Validate run `1742`, the closure sequence for the 84-grid observed-by-case
materialization packet.

The validator checks source readiness, item and action shape, role accounting,
the all-external-items-missing state, blocked materialization/FDTD/downstream
states, figure output, and frozen script snapshots.

This run does not materialize observed data or execute FDTD.

## Output

```text
outputs/experiments/1743_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_return_packet_live_delta_closure_sequence_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_return_packet_live_delta_closure_sequence_validator_check_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_return_packet_live_delta_closure_sequence_validator_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_return_packet_live_delta_closure_sequence_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:                         6
passed checks:                             6
failed checks:                             0
sequence items:                            21
sequence actions:                          4
approval token items:                      1
cache array items:                         10
result JSON items:                         10
external items present:                    0
missing external items:                    21
materialization gate ready:                false
materialization ready:                     false
new FDTD executed:                         false
execution permitted:                       false
GPU work ready:                            false
field transfer ready:                      false
3D/HPC ready:                              false
```

## Interpretation

The closure sequence is internally consistent and preserves the current claim
boundary: no materialization, no real FDTD execution, and no downstream
promotion.

## Decision

Use run `1743` as the validator for the 84-grid materialization closure
sequence.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_return_packet_live_delta_closure_sequence.py
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_return_packet_live_delta_closure_sequence_validator.py
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_return_packet_live_delta_closure_sequence_validation_sensitivity.py

10 passed
```

Figure check:

```text
2357x838, dynamic range=255
```
