# Experiment 1739: 84-Grid Observed-by-Case Materialization Return-Packet Live Delta Monitor

Date: 2026-06-30

## Purpose

Create a live external-return delta monitor for the 21-item materialization
return packet after the post-sandbox external-path guard.

Runs `1736-1738` proved that the positive sandbox completion did not populate
the locked external return paths. This run turns that boundary into a current
readiness view: how many required external items are present now, which roles
are complete, and whether materialization or FDTD execution can proceed.

## Output

```text
outputs/experiments/1739_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_return_packet_live_delta_monitor
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_return_packet_live_delta_monitor_delta_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_return_packet_live_delta_monitor_role_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_return_packet_live_delta_monitor_summary.json
data/figure_validation.csv
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_return_packet_live_delta_monitor.png
scripts/
```

## Result

```text
expected external items:       21
roles:                         3
external items present now:    0
missing external items now:    21
complete roles:                0
roles ready for materialization: 0
source sandbox accepted items: 21
ready for materialization:     false
observed-by-case materialized: false
new FDTD executed:             false
GPU work ready:                false
field transfer ready:          false
field FWI ready:               false
3D/HPC ready:                  false
```

## Interpretation

The external materialization packet is still empty. None of the three roles is
complete, even though the output-local sandbox packet has already proven that
the file mechanics can pass.

This is a live readiness monitor, not a materialization result.

## Decision

Use this monitor after external result drops. Keep materialization, FDTD
execution, GPU work, field transfer, field FWI, and 3D/HPC blocked until all
21 expected external items are present.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_return_packet_live_delta_monitor.py
3 passed
```

Figure check:

```text
2464x852, dynamic range=255
```
