# Experiment 1738: 84-Grid Observed-by-Case Materialization Return-Packet Post-Sandbox External-Path Guard Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `1737` validator for the post-sandbox external-path guard.

The validator should accept only the exact run `1736` source state and reject
damaged states that promote external files, path overlap, materialization,
FDTD execution, downstream readiness, figure damage, or missing script
snapshots.

## Output

```text
outputs/experiments/1738_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_return_packet_post_sandbox_external_path_guard_validation_sensitivity
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_return_packet_post_sandbox_external_path_guard_validation_sensitivity_cases.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_return_packet_post_sandbox_external_path_guard_validation_sensitivity_summary.json
data/figure_validation.csv
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_return_packet_post_sandbox_external_path_guard_validation_sensitivity.png
scripts/
```

## Result

```text
source validator ready:     true
sensitivity cases:          29
expected pass cases:        1
expected fail cases:        28
actual pass cases:          1
actual fail cases:          28
unexpected cases:           0
ready for materialization:  false
observed-by-case ready:     false
new FDTD executed:          false
GPU work ready:             false
field transfer ready:       false
field FWI ready:            false
3D/HPC ready:               false
```

The exact run `1736` guard passes. All damaged states fail, including external
item promotion, source external-item promotion, sandbox/external path overlap,
sandbox-under-external-root promotion, synthetic-boundary loss, observed-data
materialization, FDTD-execution promotion, execution-permission promotion, GPU
promotion, field-transfer promotion, field-FWI promotion, 3D/HPC promotion,
figure damage, and missing script snapshots.

## Interpretation

Run `1738` hardens the post-sandbox guard. A positive sandbox intake test is
not allowed to become an external materialization result through path overlap,
metadata flags, or downstream readiness flags.

## Decision

Use runs `1736-1738` as the current post-sandbox boundary guard for the
84-grid observed-by-case materialization branch. Real materialization and FDTD
execution remain blocked until real external return items are accepted.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_return_packet_post_sandbox_external_path_guard.py
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_return_packet_post_sandbox_external_path_guard_validator.py
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_return_packet_post_sandbox_external_path_guard_validation_sensitivity.py

9 passed
```

Figure check:

```text
2896x881, dynamic range=255
```
