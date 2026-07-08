# Field Experiment 075: Apparent-Depth Sensitivity

Date: 2026-06-18

## Purpose

Test how sensitive the local GSSI apparent-depth scale is to dielectric and
time-zero assumptions already present in the field QC archive. This is a
CPU-only sensitivity audit; it does not launch FDTD, FWI, GPU kernels, 3D
inversion, radius recovery, or cover-depth recovery.

## Output

```text
085_gssi51600s_field_apparent_depth_sensitivity
```

Key artifacts:

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/085_gssi51600s_field_apparent_depth_sensitivity/data/field_apparent_depth_sensitivity_rows.csv
outputs/field_experiments/local_gssi_51600s_2026_06_09/085_gssi51600s_field_apparent_depth_sensitivity/data/field_apparent_depth_sensitivity_summary.json
outputs/field_experiments/local_gssi_51600s_2026_06_09/085_gssi51600s_field_apparent_depth_sensitivity/figures/field_apparent_depth_sensitivity.png
```

## Result

Policy label:

```text
field_apparent_depth_sensitivity_not_calibrated_cover_depth
```

Summary:

```text
scenario count:                       5
epsr range:                           2.25 to 11.10
max apparent cue depth range:          126.906 to 276.822 mm
max apparent cue depth span:           149.916 mm
max apparent cue depth factor:         2.18x
residual support across scenarios:     5 / 5
cover-depth claim ready:               false
field FWI ready:                       false
gpu priority:                          none
```

## Interpretation

The short-pair relative time-zero residual support is stable as a depth-equivalent
QC statement: all tested dielectric/time-zero scenarios keep the corrected
residuals inside the corresponding conservative budget.

The absolute apparent cue depths are not stable enough for cover-depth claims.
Across the archived dielectric/time-zero scenarios, the maximum apparent cue
depth shifts by about 150 mm, or a 2.18x scale factor. This reinforces the
boundary from run 084: useful depth-scale QC, not calibrated cover-depth,
radius, 3D, or field-FWI evidence.

## Validation

Focused tests:

```text
tests/test_gssi_field_apparent_depth_sensitivity.py
2 passed
```

Figure validation:

```text
085 field_apparent_depth_sensitivity.png: 2739x1515, dynamic range=255
```
