# Experiment 1735: 84-Grid Observed-by-Case Materialization Return-Packet Sandbox Completion Smoke Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `1734` validator for the run `1733` materialization
return-packet sandbox completion smoke.

The audit checks whether the validator rejects damaged packet shape,
file-mechanics, execution-boundary, figure, and script states.

## Output

```text
outputs/experiments/1735_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_return_packet_sandbox_completion_smoke_validation_sensitivity
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_return_packet_sandbox_completion_smoke_validation_sensitivity_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_return_packet_sandbox_completion_smoke_validation_sensitivity_summary.json
data/figure_validation.csv
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_return_packet_sandbox_completion_smoke_validation_sensitivity.png
scripts/
```

## Result

```text
source validator ready:          true
sensitivity cases:               29
expected pass cases:             1
expected fail cases:             28
actual pass cases:               1
actual fail cases:               28
unexpected outcomes:             0
exact source passes:             true
damaged cases rejected:          true
packet-shape damage rejected:    true
execution-boundary rejected:     true
ready for materialization:       false
observed data materialized:      false
new FDTD executed:               false
GPU work ready:                  false
field transfer ready:            false
field FWI ready:                 false
3D/HPC ready:                    false
```

Damage groups:

| Group | Damaged states | Result |
| --- | ---: | --- |
| Source readiness | 1 | rejected |
| Packet shape, item mechanics, and role completion | 14 | rejected |
| Template, external path, materialization, FDTD, GPU, field, and 3D promotion | 10 | rejected |
| Figure and script artifacts | 2 | rejected |

## Interpretation

Run `1735` hardens the 2D materialization sandbox completion block. The exact
run `1733` smoke passes through the run `1734` validator, while all damaged
states fail. The guarded result remains a file-mechanics pass case only; it is
not external approval, not observed-data materialization, and not FDTD
execution.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_return_packet_sandbox_completion_smoke.py
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_return_packet_sandbox_completion_smoke_validator.py
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_return_packet_sandbox_completion_smoke_validation_sensitivity.py

9 passed
```

Figure check:

```text
2860x898, dynamic range=255
```
