# BEM Experiment 783: Complex Metric Preflight Claim Boundary Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `782` claim-boundary validator by damaging the saved run
`781` state in controlled ways.

This run checks whether false claim counts, false guarded or blocked states,
producer-file promotion, preflight-pass promotion, real-comparison promotion,
downstream promotion, figure damage, and script-snapshot damage are rejected.

## Output

```text
outputs/bem_experiments/783_project_core_bem_35field_matched_fdtd_complex_metric_real_return_preflight_claim_boundary_validation_sensitivity
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_complex_metric_real_return_preflight_claim_boundary_validation_sensitivity_scenario_rows.csv
data/project_core_bem_35field_matched_fdtd_complex_metric_real_return_preflight_claim_boundary_validation_sensitivity_summary.json
figures/project_core_bem_35field_matched_fdtd_complex_metric_real_return_preflight_claim_boundary_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source validator ready:           true
scenarios:                        14
expected pass scenarios:          1
expected fail scenarios:          13
observed pass scenarios:          1
observed fail scenarios:          13
unexpected outcomes:              0
damaged scenarios:                13
damaged scenarios rejected:       13
gpu priority:                     none
```

## Interpretation

The validator accepts only the exact saved claim boundary. Any attempt to turn
the pre-return gate into real BEM/FDTD comparison evidence is rejected.

## Decision

Use runs `781-783` as the guarded post-preflight claim-boundary block for the
35-field BEM/FDTD complex-metric branch.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_real_return_preflight_claim_boundary.py
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_real_return_preflight_claim_boundary_validator.py
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_real_return_preflight_claim_boundary_validation_sensitivity.py

9 passed
```

Figure check:

```text
2788x858, dynamic range=255
```
