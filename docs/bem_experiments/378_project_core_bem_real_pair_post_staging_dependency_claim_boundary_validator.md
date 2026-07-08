# BEM Experiment 378: Post Staging Dependency Claim Boundary Validator

Date: 2026-06-29

## Purpose

Validate the saved run `377` BEM post-staging dependency claim boundary from
artifacts.

This run checks source identity, claim counts, the staging dependency claim
row, staging metrics, blocked claim rows, downstream blocked states, figure
validation, and script snapshots.

## Output

```text
outputs/bem_experiments/378_project_core_bem_real_pair_post_staging_dependency_claim_boundary_validator
```

Key artifacts:

```text
data/project_core_bem_real_pair_post_staging_dependency_claim_boundary_validator_checks.csv
data/project_core_bem_real_pair_post_staging_dependency_claim_boundary_validator_summary.json
figures/project_core_bem_real_pair_post_staging_dependency_claim_boundary_validator.png
scripts/
```

## Result

```text
validation checks:                   7
passed checks:                       7
failed checks:                       0
validation ready:                    true
claims:                              14
guarded claims:                      11
blocked claims:                      3
staging sensitivity ready:           true
accepts exact run 374:               true
rejects damaged variants:            true
stages:                              4
dependency edges:                    3
missing packet items:                34
real packet files present:           false
real BEM/FDTD comparison ready:      false
threshold calibration ready:         false
field transfer ready:                false
GPU work ready:                      false
3D validation ready:                 false
```

## Interpretation

The saved BEM post-staging claim boundary is internally consistent. The
staging dependency plan is guarded, and downstream execution remains blocked by
the absent 34-item real return packet.

## Decision

Use run `378` as the validator for the run `377` BEM post-staging claim
boundary. Sensitivity hardening remains required before closing the block.

## Validation

Focused tests:

```text
tests/test_project_core_bem_real_pair_post_staging_dependency_claim_boundary_validator.py
3 passed
```

Figure validation:

```text
3653x929, dynamic range=255
```
