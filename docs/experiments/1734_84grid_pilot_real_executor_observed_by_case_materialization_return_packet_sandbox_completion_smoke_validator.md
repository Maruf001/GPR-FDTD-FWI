# Experiment 1734: 84-Grid Observed-by-Case Materialization Return-Packet Sandbox Completion Smoke Validator

Date: 2026-06-30

## Purpose

Validate run `1733`, the output-local sandbox completion smoke for the
21-item observed-by-case materialization return-packet contract.

## Output

```text
outputs/experiments/1734_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_return_packet_sandbox_completion_smoke_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_return_packet_sandbox_completion_smoke_validator_check_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_return_packet_sandbox_completion_smoke_validator_summary.json
data/figure_validation.csv
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_return_packet_sandbox_completion_smoke_validator.png
scripts/
```

## Result

```text
validation checks:             5
failed checks:                 0
sandbox items:                 21
sandbox accepted items:        21
sandbox complete roles:        3
external items present:        0
observed data materialized:    0
new FDTD executions:           0
ready for materialization:     false
GPU work ready:                false
field transfer ready:          false
field FWI ready:               false
3D/HPC ready:                  false
```

All five validation checks pass:

| Order | Check | Result |
| ---: | --- | --- |
| 1 | source sandbox completion smoke ready | pass |
| 2 | sandbox packet shape complete | pass |
| 3 | file parse and load mechanics pass | pass |
| 4 | sandbox remains non-executing and external paths empty | pass |
| 5 | figure and scripts exist | pass |

## Interpretation

Run `1734` confirms that run `1733` is a valid positive-path file-mechanics
smoke. It does not approve materialization, does not create observed data, and
does not execute FDTD.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_return_packet_sandbox_completion_smoke.py
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_return_packet_sandbox_completion_smoke_validator.py

6 passed
```

Figure check:

```text
2285x832, dynamic range=255
```
