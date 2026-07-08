# BEM Experiment 461: Post Storage-Refresh Claim Boundary

Date: 2026-06-29

## Purpose

Fold the guarded storage-refreshed scorecard template block from runs
`458-460` into the current BEM claim boundary.

## Output

```text
outputs/bem_experiments/461_project_core_bem_post_35field_real_normalized_comparator_scorecard_storage_refresh_claim_boundary
```

Key artifacts:

```text
data/project_core_bem_post_35field_real_normalized_comparator_scorecard_storage_refresh_claim_boundary_claim_rows.csv
data/project_core_bem_post_35field_real_normalized_comparator_scorecard_storage_refresh_claim_boundary_summary.json
figures/project_core_bem_post_35field_real_normalized_comparator_scorecard_storage_refresh_claim_boundary.png
scripts/script_snapshot_manifest.json
```

## Result

```text
claims:                                      29
guarded claims:                              26
blocked claims:                              3
scorecard storage refresh ready:             true
storage-refresh validation ready:            true
storage-refresh sensitivity ready:           true
scorecard rows:                              279
preferred-storage rows:                      279
required real input cells:                   1116
filled real input cells:                     0
generated score cells:                       1116
filled generated score cells:                0
template rows currently evidence:            0
serialized reference coefficient:            0.019078784028338909
recommended storage significant digits:      17
minimum safe scorecard significant digits:   13
real BEM/FDTD comparison ready:              false
3D validation ready:                         false
GPU/HPC ready:                               false
field FWI ready:                             false
```

The claim boundary now records that future returned scorecards should use the
storage-refreshed template. It remains a non-evidence template until real BEM
and FDTD values plus source hashes are supplied.

## Decision

Use this as the current BEM claim boundary after the storage-refresh block.
Real comparison, 3D validation, GPU/HPC work, and field FWI remain blocked.

## Validation

Focused tests:

```text
tests/test_project_core_bem_post_35field_real_normalized_comparator_scorecard_storage_refresh_claim_boundary.py
4 passed
```

Figure check:

```text
3941x899, dynamic range=255
```
