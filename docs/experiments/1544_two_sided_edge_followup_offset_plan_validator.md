# Experiment 1544: Two-Sided Edge Follow-Up Offset Plan Validator

Date: 2026-06-29

## Purpose

Validate the saved run `1543` follow-up offset plan from artifacts.

This run checks source identity, planned offsets, planned case matrix,
downstream non-execution states, figure validation, and script snapshots.

## Output

```text
outputs/experiments/1544_local_2d_state_consistent_objective_revision_two_sided_edge_followup_offset_plan_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_two_sided_edge_followup_offset_plan_validator_checks.csv
data/local_2d_state_consistent_objective_revision_two_sided_edge_followup_offset_plan_validator_summary.json
figures/local_2d_state_consistent_objective_revision_two_sided_edge_followup_offset_plan_validator.png
scripts/
```

## Result

```text
validation checks:                   6
passed checks:                       6
failed checks:                       0
validation ready:                    true
proposed offsets:                    5
planned cases:                       20
follow-up FDTD executed:             false
new physical claim ready:            false
GPU work ready:                      false
field transfer ready:                false
field FWI ready:                     false
3D/HPC ready:                        false
```

## Interpretation

The saved follow-up offset plan is internally consistent and remains a
non-executed plan.

## Decision

Use run `1544` as the validator for the run `1543` follow-up offset plan.
Sensitivity hardening remains required before closing the plan block.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_two_sided_edge_followup_offset_plan_validator.py
3 passed
```

Figure validation:

```text
3509x909, dynamic range=255
```
