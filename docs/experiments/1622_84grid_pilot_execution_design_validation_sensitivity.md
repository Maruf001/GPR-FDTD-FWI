# Experiment 1622: 84-Grid Pilot Execution Design Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `1621` validator.

The exact run `1620` pilot design should pass. Damaged pilot structure, damaged
budget, damaged source readiness, damaged figure or script snapshots, and
premature execution promotion should fail.

## Output

```text
outputs/experiments/1622_local_2d_state_consistent_objective_revision_84grid_pilot_execution_design_validation_sensitivity
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_execution_design_validation_sensitivity_scenario_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_execution_design_validation_sensitivity_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_execution_design_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
sensitivity scenarios:                     12
expected pass scenarios:                   1
expected failure scenarios:                11
unexpected scenarios:                      0
validation sensitivity ready:              true
exact source artifacts pass:               true
pilot structure damage rejected:           true
budget damage rejected:                    true
premature execution promotion rejected:    true
execution permitted:                       false
new FDTD executed:                         false
GPU priority:                              none
```

Damaged scenarios rejected:

| Scenario | Expected result |
| --- | --- |
| source guard damage | fail |
| pilot row count drift | fail |
| profile duplicate damage | fail |
| endpoint removed damage | fail |
| central case removed damage | fail |
| pilot budget damage | fail |
| executor premature promotion | fail |
| execution premature promotion | fail |
| action order damage | fail |
| figure damage | fail |
| script snapshot damage | fail |

## Decision

Use runs `1620-1622` as the guarded five-row pilot-design block before building
a real pilot executor. The next 2D task is a duplicated pilot executor and
pilot-only command inventory, not the full 84-row screen.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_execution_design_validation_sensitivity.py
3 passed
```

Figure check:

```text
2825x857, dynamic range=255
```
