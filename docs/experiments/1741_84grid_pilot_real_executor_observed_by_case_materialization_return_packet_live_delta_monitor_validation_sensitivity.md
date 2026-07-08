# Experiment 1741: 84-Grid Observed-by-Case Materialization Return-Packet Live Delta Monitor Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `1740` validator for the live external-return delta
monitor.

The validator should accept only the exact run `1739` empty-external-packet
state and reject damaged states that promote external files, role completion,
materialization, FDTD execution, execution permission, downstream readiness,
figure validation, or script snapshots.

## Output

```text
outputs/experiments/1741_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_return_packet_live_delta_monitor_validation_sensitivity
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_return_packet_live_delta_monitor_validation_sensitivity_cases.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_return_packet_live_delta_monitor_validation_sensitivity_summary.json
data/figure_validation.csv
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_return_packet_live_delta_monitor_validation_sensitivity.png
scripts/
```

## Result

```text
source validator ready:       true
sensitivity cases:            21
expected pass cases:          1
expected fail cases:          20
actual pass cases:            1
actual fail cases:            20
unexpected cases:             0
ready for materialization:    false
new FDTD executed:            false
GPU work ready:               false
field transfer ready:         false
field FWI ready:              false
3D/HPC ready:                 false
```

The exact run `1739` monitor passes. All damaged states fail, including source
readiness damage, item or role row removal, expected-count or role-count
damage, external-item promotion, missing-count reduction, role-complete
promotion, materialization promotion, observed-data promotion, result-written
promotion, command-execution promotion, FDTD-execution promotion,
execution-permission promotion, GPU promotion, field-transfer promotion,
field-FWI promotion, 3D/HPC promotion, figure damage, and missing script
snapshots.

## Interpretation

Run `1741` hardens the live delta monitor. The 2D branch cannot be promoted to
materialization or FDTD execution by count drift, partial external-file
presence, or downstream readiness flags.

## Decision

Use runs `1739-1741` as the current live external-return readiness checkpoint.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_return_packet_live_delta_monitor.py
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_return_packet_live_delta_monitor_validator.py
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_return_packet_live_delta_monitor_validation_sensitivity.py

9 passed
```

Figure check:

```text
2572x870, dynamic range=255
```
