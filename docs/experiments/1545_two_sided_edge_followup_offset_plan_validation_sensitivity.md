# Experiment 1545: Two-Sided Edge Follow-Up Offset Plan Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `1544` validator for the saved run `1543` follow-up offset
plan.

This run checks that the validator accepts the exact run `1543` plan and
rejects controlled damaged variants for offset drift, case-matrix drift, false
execution, downstream promotion, figure drift, and script-snapshot drift.

## Output

```text
outputs/experiments/1545_local_2d_state_consistent_objective_revision_two_sided_edge_followup_offset_plan_validation_sensitivity
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_two_sided_edge_followup_offset_plan_validation_sensitivity_scenario_rows.csv
data/local_2d_state_consistent_objective_revision_two_sided_edge_followup_offset_plan_validation_sensitivity_summary.json
figures/local_2d_state_consistent_objective_revision_two_sided_edge_followup_offset_plan_validation_sensitivity.png
scripts/
```

## Result

```text
scenarios:                          13
expected pass:                      1
observed pass:                      1
expected failures:                  12
observed failures:                  12
unexpected outcomes:                0
sensitivity ready:                  true
accepts exact run 1543:             true
rejects damaged variants:           true
proposed offsets:                   5
planned cases:                      20
follow-up FDTD executed:            false
new physical claim ready:           false
GPU work ready:                     false
field transfer ready:               false
3D/HPC ready:                       false
```

## Interpretation

The run `1544` validator accepts the exact run `1543` plan and rejects
controlled damaged variants. The plan remains a guarded non-executed candidate,
not an executed FDTD result.

## Decision

Use runs `1543-1545` as the guarded non-executed follow-up offset-plan block.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_two_sided_edge_followup_offset_plan_validation_sensitivity.py
3 passed
```

Figure validation:

```text
3437x904, dynamic range=255
```
