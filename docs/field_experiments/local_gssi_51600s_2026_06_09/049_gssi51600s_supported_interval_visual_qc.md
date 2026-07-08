# Field Experiment 049: GSSI 51600S Supported Interval Visual QC

Date: 2026-06-17

## Purpose

CPU-only visual-QC package restricted to corrected-stack intervals that are
supported in every tested shallow time window. This uses the spatial-support
mask from field experiment 047 and avoids showing unsupported profile columns
as if they were reliable.

It does not run FDTD, FWI, GPU kernels, 3D reconstruction, or field geometry
inversion.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/049_gssi51600s_supported_interval_visual_qc
```

Artifacts:

```text
data/supported_interval_visual_qc_rows.csv
data/supported_interval_visual_qc_summary.json
data/figure_validation.csv
figures/supported_interval_visual_qc.png
run_manifest.json
```

## Result

Policy label:

```text
supported_interval_visual_qc_ready
```

Summary:

```text
support key:                            all_window_supported
selected intervals:                     3
supported intervals:                    3
total selected interval length:         0.166650 m
minimum interval abs-correlation gain:  0.363612
mean interval abs-correlation gain:     0.459290
minimum corrected interval abs corr:    0.909285
mean corrected interval abs corr:       0.933828
```

Selected intervals:

```text
0.103323-0.156651 m
0.389961-0.459954 m
0.669933-0.713262 m
```

## Interpretation

This is the preferred corrected-stack visual-QC endpoint for the local GSSI
014/016 pair because it restricts the B-scan panels to intervals supported by
the spatial mask in all tested windows.

The result remains measured-data timing/repeatability QC only. It does not
support field FWI, 3D, radius, cover-depth, geometry, or absolute time-zero
claims.

## Validation

Focused tests:

```text
tests/test_gssi_field_supported_interval_visual_qc.py: 5 passed
```

Figure validation:

```text
supported_interval_visual_qc.png: 2569x1753,
nonwhite=0.5161, dynamic range=255
```
