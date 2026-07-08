# Experiment 1737: 84-Grid Observed-by-Case Materialization Return-Packet Post-Sandbox External-Path Guard Validator

Date: 2026-06-30

## Purpose

Validate run `1736`, the guard that confirms the output-local return-packet
sandbox did not populate external return paths or authorize FDTD execution.

## Output

```text
outputs/experiments/1737_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_return_packet_post_sandbox_external_path_guard_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_return_packet_post_sandbox_external_path_guard_validator_check_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_return_packet_post_sandbox_external_path_guard_validator_summary.json
data/figure_validation.csv
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_return_packet_post_sandbox_external_path_guard_validator.png
scripts/
```

## Result

```text
validation checks:                  5
failed checks:                      0
guard rows:                         21
guard roles:                        3
external paths under return root:   21
external items present:             0
source external items present:      0
sandbox items present:              21
sandbox/external path overlaps:     0
sandbox under external return root: 0
synthetic-only items:               21
observed data materialized:         0
new FDTD executions:                0
ready for materialization:          false
GPU work ready:                     false
field transfer ready:               false
field FWI ready:                    false
3D/HPC ready:                       false
```

Validator checks:

| Order | Check | Result |
| ---: | --- | --- |
| 1 | Source external-path guard ready | pass |
| 2 | Guard row shape | pass |
| 3 | External paths remain empty and separated | pass |
| 4 | Materialization and downstream blocked | pass |
| 5 | Figure and scripts exist | pass |

## Interpretation

Run `1737` confirms that run `1736` is a valid post-sandbox boundary guard.
The expected external return paths are locked and empty, the sandbox items are
separate, and no materialization or execution state is ready.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_return_packet_post_sandbox_external_path_guard.py
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_return_packet_post_sandbox_external_path_guard_validator.py

6 passed
```

Figure check:

```text
2357x864, dynamic range=255
```
