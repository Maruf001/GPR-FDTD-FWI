# BEM Experiment 379: Post Staging Dependency Claim Boundary Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `378` validator for the saved run `377` BEM post-staging
dependency claim boundary.

This run checks that the validator accepts the exact run `377` artifacts and
rejects controlled damaged variants for claim drift, staging row drift, staging
metric drift, blocked-row drift, downstream promotion, figure drift, and
script-snapshot drift.

## Output

```text
outputs/bem_experiments/379_project_core_bem_real_pair_post_staging_dependency_claim_boundary_validation_sensitivity
```

Key artifacts:

```text
data/project_core_bem_real_pair_post_staging_dependency_claim_boundary_validation_sensitivity_scenario_rows.csv
data/project_core_bem_real_pair_post_staging_dependency_claim_boundary_validation_sensitivity_summary.json
figures/project_core_bem_real_pair_post_staging_dependency_claim_boundary_validation_sensitivity.png
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
accepts exact run 377:              true
rejects damaged variants:           true
stages:                             4
dependency edges:                   3
missing packet items:               34
real packet files present:          false
real BEM/FDTD comparison ready:     false
threshold calibration ready:        false
field transfer ready:               false
GPU work ready:                     false
3D validation ready:                false
```

## Interpretation

The run `378` validator accepts the exact run `377` claim boundary and rejects
controlled damaged variants. This guards the BEM post-staging claim-boundary
result while preserving the main blocker: the real 34-item return packet is
still absent.

## Decision

Use runs `377-379` as the guarded BEM post-staging claim-boundary block. Real
comparison remains blocked until the 34-item return packet is present and
passes the acceptance gate.

## Validation

Focused tests:

```text
tests/test_project_core_bem_real_pair_post_staging_dependency_claim_boundary_validation_sensitivity.py
3 passed
```

Figure validation:

```text
3545x895, dynamic range=255
```
