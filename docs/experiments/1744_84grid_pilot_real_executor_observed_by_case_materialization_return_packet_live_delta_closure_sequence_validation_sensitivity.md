# Experiment 1744: 84-Grid Materialization Return-Packet Live Delta Closure Sequence Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `1743` validator.

The sensitivity set keeps one exact source case and applies controlled damage
to source readiness, item count, action count, approval-token count, cache-array
count, result-JSON count, fake external item presence, fake action completion,
materialization-gate readiness, materialization readiness, FDTD execution,
execution permission, GPU readiness, field transfer readiness, downstream
readiness, figure validation, and script snapshots.

This run does not materialize observed data, execute FDTD, or promote
downstream work.

## Output

```text
outputs/experiments/1744_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_return_packet_live_delta_closure_sequence_validation_sensitivity
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_return_packet_live_delta_closure_sequence_validation_sensitivity_case_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_return_packet_live_delta_closure_sequence_validation_sensitivity_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_return_packet_live_delta_closure_sequence_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source validator ready:                    true
sensitivity cases:                         18
expected pass cases:                       1
expected fail cases:                       17
actual pass cases:                         1
actual fail cases:                         17
unexpected cases:                          0
damaged cases:                             17
materialization gate ready:                false
materialization ready:                     false
new FDTD executed:                         false
execution permitted:                       false
GPU work ready:                            false
field transfer ready:                      false
3D/HPC ready:                              false
```

## Interpretation

The validator accepts only the exact current closure sequence and rejects count
drift, fake external returns, and premature execution or downstream promotion.

## Decision

Treat runs `1742-1744` as the current guarded 84-grid materialization closure
sequence. Real materialization and FDTD execution remain blocked until the
complete 21-item external packet exists.

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
2609x853, dynamic range=255
```
