# Experiment 1740: 84-Grid Observed-by-Case Materialization Return-Packet Live Delta Monitor Validator

Date: 2026-06-30

## Purpose

Validate run `1739`, the live external-return delta monitor for the 21-item
materialization packet.

The validator checks the 21-item and 3-role shape, confirms that all external
items are still missing, and confirms that materialization, FDTD execution,
GPU work, field transfer, field FWI, and 3D/HPC remain blocked.

## Output

```text
outputs/experiments/1740_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_return_packet_live_delta_monitor_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_return_packet_live_delta_monitor_validator_check_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_return_packet_live_delta_monitor_validator_summary.json
data/figure_validation.csv
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_return_packet_live_delta_monitor_validator.png
scripts/
```

## Result

```text
validator checks:              5
failed checks:                 0
expected external items:       21
roles:                         3
external items present now:    0
missing external items now:    21
complete roles:                0
ready for materialization:     false
observed-by-case materialized: false
new FDTD executed:             false
GPU work ready:                false
field transfer ready:          false
field FWI ready:               false
3D/HPC ready:                  false
```

## Interpretation

Run `1740` confirms that run `1739` is a valid live delta monitor. The current
2D materialization branch is an empty external-return state, not a partial
materialization state.

## Decision

Keep run `1739` as the current external return-packet readiness monitor.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_return_packet_live_delta_monitor.py
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_return_packet_live_delta_monitor_validator.py

6 passed
```

Figure check:

```text
2357x861, dynamic range=255
```
