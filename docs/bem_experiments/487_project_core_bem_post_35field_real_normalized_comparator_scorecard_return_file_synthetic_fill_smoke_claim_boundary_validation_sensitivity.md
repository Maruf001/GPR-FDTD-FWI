# BEM Experiment 487: Post Synthetic Return-File Fill Claim-Boundary Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `486` validator against controlled damage to the run `485`
BEM claim boundary.

## Output

```text
outputs/bem_experiments/487_project_core_bem_post_35field_real_normalized_comparator_scorecard_return_file_synthetic_fill_smoke_claim_boundary_validation_sensitivity
```

Key artifacts:

```text
data/project_core_bem_post_35field_real_normalized_comparator_scorecard_return_file_synthetic_fill_smoke_claim_boundary_validation_sensitivity_scenario_rows.csv
data/project_core_bem_post_35field_real_normalized_comparator_scorecard_return_file_synthetic_fill_smoke_claim_boundary_validation_sensitivity_summary.json
figures/project_core_bem_post_35field_real_normalized_comparator_scorecard_return_file_synthetic_fill_smoke_claim_boundary_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
sensitivity scenarios:                       31
expected pass scenarios:                     1
observed pass scenarios:                     1
expected failure scenarios:                  30
observed failure scenarios:                  30
unexpected outcomes:                         0
validation sensitivity ready:                true
validator accepts exact run 485:             true
validator rejects damaged variants:          true
real return files present:                   false
real BEM/FDTD comparison ready:              false
3D validation ready:                         false
GPU/HPC ready:                               false
field FWI ready:                             false
```

## Interpretation

The validator accepts the exact run `485` boundary and rejects damaged variants
for claim-count drift, synthetic-fill readiness drift, synthetic-fill metric
drift, synthetic evidence promotion, downstream promotion, figure drift, and
script-snapshot drift.

## Decision

Use runs `485-487` as the current guarded BEM post-synthetic-return-file-fill
claim-boundary block.

## Validation

Focused tests:

```text
tests/test_project_core_bem_post_35field_real_normalized_comparator_scorecard_return_file_synthetic_fill_smoke_claim_boundary_validation_sensitivity.py
3 passed
```

Figure check:

```text
3725x887, dynamic range=255
```
