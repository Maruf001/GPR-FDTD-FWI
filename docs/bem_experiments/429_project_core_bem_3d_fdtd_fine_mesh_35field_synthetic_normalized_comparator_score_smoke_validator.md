# BEM Experiment 429: 35-Field Synthetic Normalized Comparator Score Smoke Validator

Date: 2026-06-29

## Purpose

Validate run `428` from saved artifacts.

The validator checks score-table shape, residual thresholds, decision items,
blocked downstream states, figure validation, and script snapshots.

## Output

```text
outputs/bem_experiments/429_project_core_bem_3d_fdtd_fine_mesh_35field_synthetic_normalized_comparator_score_smoke_validator
```

Key artifacts:

```text
data/project_core_bem_3d_fdtd_fine_mesh_35field_synthetic_normalized_comparator_score_smoke_validator_checks.csv
data/project_core_bem_3d_fdtd_fine_mesh_35field_synthetic_normalized_comparator_score_smoke_validator_summary.json
figures/project_core_bem_3d_fdtd_fine_mesh_35field_synthetic_normalized_comparator_score_smoke_validator.png
```

## Result

```text
validation checks:                 5
validation passes:                 5
blocking failures:                 0
score validation ready:            true
source score ready:                true
score rows:                        279
axis score rows:                   40
reference coefficient:             0.01907878402833891
relative tolerance:                1e-12
max normalized residual:           3.6369686315440523e-16
max raw reconstruction error:      4.4336379508346526e-16
score passes:                      279
score failures:                    0
synthetic packet is evidence:      false
real comparison ready:             false
3D validation ready:               false
GPU/HPC ready:                     false
field FWI ready:                   false
```

## Decision

Use this validator as the artifact guard for run `428`. Sensitivity testing
remains required before closing the normalized-comparator score-smoke block.

## Validation

Focused tests:

```text
tests/test_project_core_bem_3d_fdtd_fine_mesh_35field_synthetic_normalized_comparator_score_smoke_validator.py
5 passed as part of the 12-test focused set
```

Figure check:

```text
2645x838, dynamic range=255
```
