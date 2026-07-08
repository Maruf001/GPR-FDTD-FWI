# BEM Experiment 428: 35-Field Synthetic Normalized Comparator Score Smoke

Date: 2026-06-29

## Purpose

Apply the guarded 35-field normalization policy as a concrete comparator score
table for future real BEM/FDTD return packets.

This is a synthetic score-smoke run. It does not create measured evidence, run
a real BEM/FDTD comparison, launch GPU/HPC work, run 3D validation, or run
field FWI.

## Output

```text
outputs/bem_experiments/428_project_core_bem_3d_fdtd_fine_mesh_35field_synthetic_normalized_comparator_score_smoke
```

Key artifacts:

```text
data/project_core_bem_3d_fdtd_fine_mesh_35field_synthetic_normalized_comparator_score_smoke_score_rows.csv
data/project_core_bem_3d_fdtd_fine_mesh_35field_synthetic_normalized_comparator_score_smoke_axis_score_rows.csv
data/project_core_bem_3d_fdtd_fine_mesh_35field_synthetic_normalized_comparator_score_smoke_decision_rows.csv
data/project_core_bem_3d_fdtd_fine_mesh_35field_synthetic_normalized_comparator_score_smoke_summary.json
figures/project_core_bem_3d_fdtd_fine_mesh_35field_synthetic_normalized_comparator_score_smoke.png
```

## Result

```text
normalized comparator score ready: true
score rows:                        279
axis score rows:                   40
receiver count:                    31
frequency count:                   9
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

All 279 synthetic rows pass the comparator-score tolerance. The normalized
coefficient reconstructs the raw synthetic norm through the policy denominator,
so the score contract is executable from saved artifacts.

## Decision

Use the score table and axis residual table as the future real-packet
comparator smoke. Keep real BEM/FDTD comparison, 3D validation, GPU/HPC work,
field transfer, and field FWI blocked until real returned files exist.

## Validation

Focused tests:

```text
tests/test_project_core_bem_3d_fdtd_fine_mesh_35field_synthetic_normalized_comparator_score_smoke.py
4 passed
```

Figure check:

```text
3941x880, dynamic range=255
```
