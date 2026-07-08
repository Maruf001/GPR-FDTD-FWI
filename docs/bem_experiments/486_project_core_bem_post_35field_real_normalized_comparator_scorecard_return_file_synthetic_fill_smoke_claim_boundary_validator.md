# BEM Experiment 486: Post Synthetic Return-File Fill Claim-Boundary Validator

Date: 2026-06-29

## Purpose

Validate the saved run `485` BEM claim boundary from artifacts.

## Output

```text
outputs/bem_experiments/486_project_core_bem_post_35field_real_normalized_comparator_scorecard_return_file_synthetic_fill_smoke_claim_boundary_validator
```

Key artifacts:

```text
data/project_core_bem_post_35field_real_normalized_comparator_scorecard_return_file_synthetic_fill_smoke_claim_boundary_validator_checks.csv
data/project_core_bem_post_35field_real_normalized_comparator_scorecard_return_file_synthetic_fill_smoke_claim_boundary_validator_summary.json
figures/project_core_bem_post_35field_real_normalized_comparator_scorecard_return_file_synthetic_fill_smoke_claim_boundary_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:                           5
validation checks passed:                    5
blocking failures:                           0
claim-boundary validation ready:             true
claims:                                      33
guarded claims:                              30
blocked claims:                              3
synthetic return files:                      4
filled synthetic entries:                    1116
scorecard rows:                              279
valid source-hash entries:                   558
finite scattered-norm entries:               558
synthetic values are evidence:               false
real BEM/FDTD comparison ready:              false
GPU/HPC ready:                               false
field FWI ready:                             false
```

## Interpretation

The validator confirms the run `485` claim count, guarded claim content,
synthetic-fill metrics, blocked downstream states, figure, and script
snapshots.

## Decision

Use this validator as the artifact guard for run `485`.

## Validation

Focused tests:

```text
tests/test_project_core_bem_post_35field_real_normalized_comparator_scorecard_return_file_synthetic_fill_smoke_claim_boundary_validator.py
4 passed
```

Figure check:

```text
2717x835, dynamic range=255
```
