# BEM Experiment 396: Post 35-Field Closure Plan Claim Boundary Validator

Date: 2026-06-29

## Purpose

Validate the saved run `395` BEM claim boundary from artifacts.

This run does not stage external FDTD files, run a real BEM/FDTD comparison,
calibrate thresholds, launch GPU work, transfer to field evidence, or start 3D
validation.

## Output

```text
outputs/bem_experiments/396_project_core_bem_post_35field_closure_plan_claim_boundary_validator
```

Key artifacts:

```text
data/project_core_bem_post_35field_closure_plan_claim_boundary_validator_checks.csv
data/project_core_bem_post_35field_closure_plan_claim_boundary_validator_summary.json
figures/project_core_bem_post_35field_closure_plan_claim_boundary_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:                  7
passed checks:                      7
failed checks:                      0
validation ready:                   true
claims:                             18
guarded claims:                     15
blocked claims:                     3
closure action groups:              4
required external files:            3
required blocking metadata fields:  34
preflight blocking failures:        10
real comparison ready:              false
3D validation ready:                false
```

## Interpretation

The saved run `395` boundary validates from artifacts. The validator confirms
the closure-plan claim row, closure metrics, blocked downstream rows, figure
validation, and script snapshots.

## Decision

Use this validator as the artifact-level guard for the current BEM claim
boundary. Sensitivity hardening remains required before closing the block.

## Validation

Focused validator test:

```text
tests/test_project_core_bem_post_35field_closure_plan_claim_boundary_validator.py
2 passed
```

Figure validation:

```text
3365x911, dynamic range=255
```
