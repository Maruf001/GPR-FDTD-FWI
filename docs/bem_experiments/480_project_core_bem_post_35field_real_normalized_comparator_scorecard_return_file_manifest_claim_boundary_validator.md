# BEM Experiment 480: Post 35-Field Return-File Manifest Claim-Boundary Validator

Date: 2026-06-29

## Purpose

Validate the saved run `479` claim boundary from artifacts.

## Output

```text
outputs/bem_experiments/480_project_core_bem_post_35field_real_normalized_comparator_scorecard_return_file_manifest_claim_boundary_validator
```

Key artifacts:

```text
data/project_core_bem_post_35field_real_normalized_comparator_scorecard_return_file_manifest_claim_boundary_validator_checks.csv
data/project_core_bem_post_35field_real_normalized_comparator_scorecard_return_file_manifest_claim_boundary_validator_summary.json
figures/project_core_bem_post_35field_real_normalized_comparator_scorecard_return_file_manifest_claim_boundary_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:                           5
validation checks passed:                    5
blocking failures:                           0
claim-boundary validation ready:             true
claims:                                      32
guarded claims:                              29
blocked claims:                              3
required files:                              4
template entries:                            1116
filled template entries:                     0
source-hash template entries:                558
scattered-norm template entries:             558
real return files present:                   false
real return values present:                  false
real BEM/FDTD comparison ready:              false
3D validation ready:                         false
GPU/HPC ready:                               false
field FWI ready:                             false
```

The validator confirms the return-file manifest claim row, manifest metrics,
blocked rows, downstream blocks, figure validation, and script snapshots.

## Decision

Use this validator as the artifact guard for run `479`.

## Validation

Focused tests:

```text
tests/test_project_core_bem_post_35field_real_normalized_comparator_scorecard_return_file_manifest_claim_boundary_validator.py
5 passed
```

Figure check:

```text
2645x832, dynamic range=255
```
