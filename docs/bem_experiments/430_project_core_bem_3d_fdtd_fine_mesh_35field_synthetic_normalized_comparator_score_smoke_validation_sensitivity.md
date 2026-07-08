# BEM Experiment 430: 35-Field Synthetic Normalized Comparator Score Smoke Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `429` validator with controlled damaged variants of the
run `428` normalized-comparator score artifacts.

## Output

```text
outputs/bem_experiments/430_project_core_bem_3d_fdtd_fine_mesh_35field_synthetic_normalized_comparator_score_smoke_validation_sensitivity
```

Key artifacts:

```text
data/project_core_bem_3d_fdtd_fine_mesh_35field_synthetic_normalized_comparator_score_smoke_validation_sensitivity_scenario_rows.csv
data/project_core_bem_3d_fdtd_fine_mesh_35field_synthetic_normalized_comparator_score_smoke_validation_sensitivity_summary.json
figures/project_core_bem_3d_fdtd_fine_mesh_35field_synthetic_normalized_comparator_score_smoke_validation_sensitivity.png
```

## Result

```text
scenarios:                         28
expected pass scenarios:           1
expected failure scenarios:        27
observed pass scenarios:           1
observed failure scenarios:        27
unexpected outcomes:               0
score sensitivity ready:           true
validator accepts exact run 428:   true
validator rejects damaged variants:true
synthetic packet is evidence:      false
real comparison ready:             false
3D validation ready:               false
GPU/HPC ready:                     false
field FWI ready:                   false
```

The validator accepts the exact run `428` score smoke and rejects controlled
damage to readiness, counts, residuals, decision items, downstream state,
figure validation, and script snapshots.

## Decision

Use runs `428-430` as the guarded BEM synthetic normalized-comparator
score-smoke block. Keep real BEM/FDTD comparison, 3D validation, GPU/HPC work,
field transfer, and field FWI blocked until real returned files exist.

## Validation

Focused tests:

```text
tests/test_project_core_bem_3d_fdtd_fine_mesh_35field_synthetic_normalized_comparator_score_smoke_validation_sensitivity.py
3 passed as part of the 12-test focused set
```

Figure check:

```text
3941x880, dynamic range=255
```
