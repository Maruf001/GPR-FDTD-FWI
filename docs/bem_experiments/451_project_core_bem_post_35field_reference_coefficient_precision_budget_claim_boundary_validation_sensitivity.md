# BEM Experiment 451: Post-Precision-Budget Claim Boundary Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `450` validator against controlled damage to the
post-precision-budget claim boundary.

## Output

```text
outputs/bem_experiments/451_project_core_bem_post_35field_reference_coefficient_precision_budget_claim_boundary_validation_sensitivity
```

Key artifacts:

```text
data/project_core_bem_post_35field_reference_coefficient_precision_budget_claim_boundary_validation_sensitivity_scenario_rows.csv
data/project_core_bem_post_35field_reference_coefficient_precision_budget_claim_boundary_validation_sensitivity_summary.json
figures/project_core_bem_post_35field_reference_coefficient_precision_budget_claim_boundary_validation_sensitivity.png
```

## Result

```text
scenarios:                          30
expected pass scenarios:            1
observed pass scenarios:            1
expected failure scenarios:         29
observed failure scenarios:         29
unexpected outcomes:                0
validation sensitivity ready:       true
validator accepts exact run 449:    true
validator rejects damaged variants: true
real BEM/FDTD comparison ready:     false
3D validation ready:                false
GPU/HPC ready:                      false
field FWI ready:                    false
```

The damaged variants cover claim-count drift, precision-readiness drift,
reference-coefficient drift, tolerance drift, significant-digit drift,
precision-claim support drift, precision-claim text drift, blocked-row support
drift, downstream promotion, blank figures, and missing script snapshots.

## Decision

Use runs `449-451` as the current guarded BEM post-precision-budget
claim-boundary block.

## Validation

Focused tests:

```text
tests/test_project_core_bem_post_35field_reference_coefficient_precision_budget_claim_boundary.py
tests/test_project_core_bem_post_35field_reference_coefficient_precision_budget_claim_boundary_validator.py
tests/test_project_core_bem_post_35field_reference_coefficient_precision_budget_claim_boundary_validation_sensitivity.py
12 passed
```

Figure check:

```text
3581x884, dynamic range=255
```
