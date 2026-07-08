# BEM Experiment 431: Post 35-Field Synthetic Normalized Comparator Score Smoke Claim Boundary

Date: 2026-06-29

## Purpose

Fold the guarded normalized-comparator score smoke from runs `428-430` into the
current BEM claim boundary.

This run records the synthetic score contract as a guarded capability. It does
not create measured evidence, run a real BEM/FDTD comparison, launch GPU/HPC
work, run 3D validation, or run field FWI.

## Output

```text
outputs/bem_experiments/431_project_core_bem_post_35field_synthetic_normalized_comparator_score_smoke_claim_boundary
```

Key artifacts:

```text
data/project_core_bem_post_35field_synthetic_normalized_comparator_score_smoke_claim_boundary_claim_rows.csv
data/project_core_bem_post_35field_synthetic_normalized_comparator_score_smoke_claim_boundary_summary.json
figures/project_core_bem_post_35field_synthetic_normalized_comparator_score_smoke_claim_boundary.png
```

## Result

```text
claims:                            24
guarded claims:                    21
blocked claims:                    3
base claims:                       23
base guarded claims:               20
base blocked claims:               3
normalized comparator score ready: true
score rows:                        279
axis score rows:                   40
score passes:                      279
score failures:                    0
reference coefficient:             0.01907878402833891
relative tolerance:                1e-12
max normalized residual:           3.6369686315440523e-16
max raw reconstruction error:      4.4336379508346526e-16
claim boundary ready:              true
synthetic packet is evidence:      false
real comparison ready:             false
3D validation ready:               false
GPU/HPC ready:                     false
field FWI ready:                   false
```

The boundary now has one additional guarded claim for the executable synthetic
score contract. The real-comparison and downstream claims remain blocked.

## Decision

Use this as the current BEM claim boundary after the synthetic
normalized-comparator score-smoke block. Keep real comparison, 3D validation,
GPU/HPC, field transfer, and field FWI blocked.

## Validation

Focused tests:

```text
tests/test_project_core_bem_post_35field_synthetic_normalized_comparator_score_smoke_claim_boundary.py
4 passed as part of the 23-test focused set
```

Figure check:

```text
3941x909, dynamic range=255
```
