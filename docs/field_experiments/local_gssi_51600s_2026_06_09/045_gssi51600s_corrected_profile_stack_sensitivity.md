# Field Experiment 045: GSSI 51600S Corrected Profile Stack Sensitivity

Date: 2026-06-17

## Purpose

CPU-only time-window sensitivity check for the corrected 014/016 short-profile
B-scan stack from field experiment 043.

It does not run FDTD, FWI, GPU kernels, 3D reconstruction, or field geometry
inversion.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/045_gssi51600s_corrected_profile_stack_sensitivity
```

Artifacts:

```text
data/corrected_profile_stack_sensitivity_windows.csv
data/corrected_profile_stack_sensitivity_columns.csv
data/corrected_profile_stack_sensitivity_summary.json
data/figure_validation.csv
figures/corrected_profile_stack_sensitivity.png
run_manifest.json
```

## Result

Policy label:

```text
corrected_profile_stack_window_robust
```

Summary:

```text
tested windows:                         0.35-1.10 ns, 0.45-1.25 ns, 0.55-1.45 ns
robust windows:                         3 / 3
minimum matrix abs-correlation gain:    0.263036
mean matrix abs-correlation gain:       0.293685
minimum corrected matrix abs corr:      0.799200
mean corrected matrix abs corr:         0.810607
minimum improved-column fraction:       0.606426
mean improved-column fraction:          0.633199
```

## Interpretation

The corrected B-scan stack improvement is not tied to a single hand-picked
window. The relative time-zero correction improves the spatially aligned
014/016 B-scan comparison across all tested shallow windows.

The result remains field timing/repeatability QC only. It does not support
absolute time-zero, field FWI, 3D, radius, cover-depth, or geometry claims.

## Validation

Focused tests:

```text
tests/test_gssi_field_corrected_profile_stack_sensitivity.py: 4 passed
```

Figure validation:

```text
corrected_profile_stack_sensitivity.png: 2569x835,
nonwhite=0.3424, dynamic range=255
```
