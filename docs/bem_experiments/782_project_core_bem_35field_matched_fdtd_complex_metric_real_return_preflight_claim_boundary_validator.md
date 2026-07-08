# BEM Experiment 782: Complex Metric Preflight Claim Boundary Validator

Date: 2026-07-01

## Purpose

Validate the saved run `781` BEM/FDTD complex-metric preflight claim boundary.

This validator checks that the boundary has two guarded claims, three blocked
claims, zero real producer CSV files, zero preflight-passed files, and no
comparison, field, 3D/HPC, or GPU promotion.

## Output

```text
outputs/bem_experiments/782_project_core_bem_35field_matched_fdtd_complex_metric_real_return_preflight_claim_boundary_validator
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_complex_metric_real_return_preflight_claim_boundary_validator_check_rows.csv
data/project_core_bem_35field_matched_fdtd_complex_metric_real_return_preflight_claim_boundary_validator_summary.json
figures/project_core_bem_35field_matched_fdtd_complex_metric_real_return_preflight_claim_boundary_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:                7
passed checks:                    7
failed checks:                    0
claims:                           5
guarded claims:                   2
blocked claims:                   3
preflight files:                  5
required metric rows:             279
producer files present:           0
preflight-passed files:           0
ready-to-stage files:             0
real BEM/FDTD comparison ready:   false
field FWI ready:                  false
3D/HPC ready:                     false
gpu priority:                     none
```

## Interpretation

The saved claim boundary is stable. It allows a guarded schema/preflight claim
but blocks any real BEM/FDTD comparison or downstream use.

## Decision

Use run `782` before citing run `781` as the current BEM/FDTD preflight claim
boundary.

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
3293x935, dynamic range=255
```
