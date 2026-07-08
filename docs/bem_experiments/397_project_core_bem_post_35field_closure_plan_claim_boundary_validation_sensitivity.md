# BEM Experiment 397: Post 35-Field Closure Plan Claim Boundary Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `396` BEM claim-boundary validator with controlled damaged
variants.

This run does not stage external FDTD files, run a real BEM/FDTD comparison,
calibrate thresholds, launch GPU work, transfer to field evidence, or start 3D
validation.

## Output

```text
outputs/bem_experiments/397_project_core_bem_post_35field_closure_plan_claim_boundary_validation_sensitivity
```

Key artifacts:

```text
data/project_core_bem_post_35field_closure_plan_claim_boundary_validation_sensitivity_scenario_rows.csv
data/project_core_bem_post_35field_closure_plan_claim_boundary_validation_sensitivity_summary.json
figures/project_core_bem_post_35field_closure_plan_claim_boundary_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
scenarios:                          11
expected pass:                      1
observed pass:                      1
expected failures:                  10
observed failures:                  10
unexpected outcomes:                0
sensitivity ready:                  true
accepts exact run 395:              true
rejects damaged variants:           true
claims:                             18
guarded claims:                     15
blocked claims:                     3
required external files:            3
required blocking metadata fields:  34
real comparison ready:              false
3D validation ready:                false
```

## Interpretation

The validator accepts exact run `395` artifacts and rejects damaged variants for
claim drift, closure-row drift, source-readiness drift, downstream promotion,
figure-validation drift, and script-snapshot drift.

## Decision

Use runs `395-397` as the current guarded BEM post-closure claim-boundary
block. The next real BEM comparison still requires returned external target,
background, and metadata files.

## Validation

Focused sensitivity test:

```text
tests/test_project_core_bem_post_35field_closure_plan_claim_boundary_validation_sensitivity.py
2 passed
```

Figure validation:

```text
3401x891, dynamic range=255
```
