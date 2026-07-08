# BEM Experiment 481: Post 35-Field Return-File Manifest Claim-Boundary Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `480` validator against controlled damage to the
post-return-file-manifest claim boundary.

## Output

```text
outputs/bem_experiments/481_project_core_bem_post_35field_real_normalized_comparator_scorecard_return_file_manifest_claim_boundary_validation_sensitivity
```

Key artifacts:

```text
data/project_core_bem_post_35field_real_normalized_comparator_scorecard_return_file_manifest_claim_boundary_validation_sensitivity_scenario_rows.csv
data/project_core_bem_post_35field_real_normalized_comparator_scorecard_return_file_manifest_claim_boundary_validation_sensitivity_summary.json
figures/project_core_bem_post_35field_real_normalized_comparator_scorecard_return_file_manifest_claim_boundary_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
sensitivity scenarios:                       33
expected pass scenarios:                     1
observed pass scenarios:                     1
expected failure scenarios:                  32
observed failure scenarios:                  32
unexpected outcomes:                         0
validation sensitivity ready:                true
validator accepts exact run 479:             true
validator rejects damaged variants:          true
real return files present:                   false
real return values present:                  false
real BEM/FDTD comparison ready:              false
3D validation ready:                         false
GPU/HPC ready:                               false
field FWI ready:                             false
```

The validator accepts the exact run `479` boundary and rejects claim-count
drift, manifest-claim drift, manifest-metric drift, downstream promotion,
figure drift, and script-snapshot drift.

## Decision

Use runs `479-481` as the current guarded BEM post-return-file-manifest
claim-boundary block.

## Validation

Focused tests:

```text
tests/test_project_core_bem_post_35field_real_normalized_comparator_scorecard_return_file_manifest_claim_boundary_validation_sensitivity.py
3 passed
```

Figure check:

```text
3617x889, dynamic range=255
```
