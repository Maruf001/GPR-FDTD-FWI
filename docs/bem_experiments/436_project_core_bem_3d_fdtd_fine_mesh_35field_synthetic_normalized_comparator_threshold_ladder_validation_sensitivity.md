# BEM Experiment 436: 35-Field Synthetic Normalized-Comparator Threshold-Ladder Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `435` validator with controlled damaged variants of the
run `434` threshold ladder.

## Output

```text
outputs/bem_experiments/436_project_core_bem_3d_fdtd_fine_mesh_35field_synthetic_normalized_comparator_threshold_ladder_validation_sensitivity
```

Key artifacts:

```text
data/project_core_bem_3d_fdtd_fine_mesh_35field_synthetic_normalized_comparator_threshold_ladder_validation_sensitivity_scenario_rows.csv
data/project_core_bem_3d_fdtd_fine_mesh_35field_synthetic_normalized_comparator_threshold_ladder_validation_sensitivity_summary.json
figures/project_core_bem_3d_fdtd_fine_mesh_35field_synthetic_normalized_comparator_threshold_ladder_validation_sensitivity.png
```

## Result

```text
scenarios:                         23
expected pass scenarios:           1
expected failure scenarios:        22
observed pass scenarios:           1
observed failure scenarios:        22
unexpected outcomes:               0
threshold-ladder sensitivity ready:true
validator accepts exact run 434:   true
validator rejects damaged variants:true
real comparison ready:             false
3D validation ready:               false
GPU/HPC ready:                     false
field FWI ready:                   false
```

The validator accepts the exact run `434` ladder and rejects controlled damage
to source readiness, ladder shape, pass/fail split, threshold margins, row
counts, downstream promotions, figure validation, and script snapshots.

## Decision

Use runs `434-436` as the guarded synthetic normalized-comparator
threshold-ladder block. Real comparison, 3D validation, GPU/HPC work, field
transfer, and field FWI remain blocked until real returned files exist.

## Validation

Focused tests:

```text
tests/test_project_core_bem_3d_fdtd_fine_mesh_35field_synthetic_normalized_comparator_threshold_ladder_validation_sensitivity.py
3 passed as part of the 10-test focused set
```

Figure check:

```text
3581x886, dynamic range=255
```
