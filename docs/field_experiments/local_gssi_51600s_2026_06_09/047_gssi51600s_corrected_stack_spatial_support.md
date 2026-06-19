# Field Experiment 047: GSSI 51600S Corrected Stack Spatial Support

Date: 2026-06-17

## Purpose

CPU-only spatial support mask for the corrected short-profile B-scan stack. It
uses the corrected-stack window-sensitivity column table from field experiment
045 to identify which aligned profile regions are reliable enough for visual
QC.

It does not run FDTD, FWI, GPU kernels, 3D reconstruction, or field geometry
inversion.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/047_gssi51600s_corrected_stack_spatial_support
```

Artifacts:

```text
data/corrected_stack_spatial_support_columns.csv
data/corrected_stack_spatial_support_intervals.csv
data/corrected_stack_spatial_support_summary.json
data/figure_validation.csv
figures/corrected_stack_spatial_support.png
run_manifest.json
```

## Result

Policy label:

```text
corrected_stack_spatial_support_sparse
```

Summary:

```text
finite columns:                         249
majority-supported columns:             105
majority-supported fraction:            0.421687
all-window-supported columns:           70
all-window-supported fraction:          0.281124
support intervals:                      15
largest majority interval:              0.069993 m
largest interval x range:               0.389961-0.459954 m
```

## Interpretation

The corrected stack improves aggregate B-scan agreement, but the usable
spatial support is sparse. Treat the supported intervals as visual-QC regions
only. Unsupported columns should not be used for field inversion, radius,
cover-depth, or 3D claims.

## Validation

Focused tests:

```text
tests/test_gssi_field_corrected_stack_spatial_support.py: 3 passed
```

Figure validation:

```text
corrected_stack_spatial_support.png: 2263x1481,
nonwhite=0.2829, dynamic range=255
```
