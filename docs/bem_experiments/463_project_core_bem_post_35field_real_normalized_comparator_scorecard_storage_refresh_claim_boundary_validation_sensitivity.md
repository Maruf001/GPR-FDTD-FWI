# BEM Experiment 463: Post Storage-Refresh Claim-Boundary Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `462` validator against controlled damage to the
storage-refresh claim boundary.

## Output

```text
outputs/bem_experiments/463_project_core_bem_post_35field_real_normalized_comparator_scorecard_storage_refresh_claim_boundary_validation_sensitivity
```

Key artifacts:

```text
data/project_core_bem_post_35field_real_normalized_comparator_scorecard_storage_refresh_claim_boundary_validation_sensitivity_scenario_rows.csv
data/project_core_bem_post_35field_real_normalized_comparator_scorecard_storage_refresh_claim_boundary_validation_sensitivity_summary.json
figures/project_core_bem_post_35field_real_normalized_comparator_scorecard_storage_refresh_claim_boundary_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
sensitivity scenarios:                       37
expected pass scenarios:                     1
observed pass scenarios:                     1
expected failure scenarios:                  36
observed failure scenarios:                  36
unexpected outcomes:                         0
validation sensitivity ready:                true
validator accepts exact run 461:             true
validator rejects damaged variants:          true
real BEM/FDTD comparison ready:              false
3D validation ready:                         false
GPU/HPC ready:                               false
field FWI ready:                             false
```

The validator accepts the exact run `461` boundary and rejects damage to claim
counts, storage-refresh readiness, scorecard metrics, storage text/digits,
blank-cell/evidence counts, downstream states, figure validation, and script
snapshots.

## Decision

Use runs `461-463` as the current guarded BEM post-storage-refresh
claim-boundary block.

## Validation

Focused tests:

```text
tests/test_project_core_bem_post_35field_real_normalized_comparator_scorecard_storage_refresh_claim_boundary_validation_sensitivity.py
3 passed
```

Figure check:

```text
3581x885, dynamic range=255
```
