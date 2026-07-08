# Field Experiment 074: Apparent-Depth Scale QC

Date: 2026-06-18

## Purpose

Convert existing local GSSI reflector cues and short-pair relative time-zero
residuals into an apparent-depth scale audit. This is a CPU-only field QC run;
it does not launch FDTD, FWI, GPU kernels, 3D inversion, radius recovery, or
cover-depth recovery.

## Output

```text
084_gssi51600s_field_apparent_depth_qc
```

Key artifacts:

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/084_gssi51600s_field_apparent_depth_qc/data/field_apparent_depth_profile_cues.csv
outputs/field_experiments/local_gssi_51600s_2026_06_09/084_gssi51600s_field_apparent_depth_qc/data/field_apparent_depth_short_pair_residuals.csv
outputs/field_experiments/local_gssi_51600s_2026_06_09/084_gssi51600s_field_apparent_depth_qc/data/field_apparent_depth_qc_summary.json
outputs/field_experiments/local_gssi_51600s_2026_06_09/084_gssi51600s_field_apparent_depth_qc/figures/field_apparent_depth_qc.png
```

## Result

Policy label:

```text
field_apparent_depth_qc_relative_scale_not_cover_depth
```

Summary:

```text
profile count:                       4
reflector cue count:                19
short-profile cue count:             9
long-profile cue count:             10
nominal dielectric:                  2.25
nominal velocity:                    0.199862 m/ns
apparent depth scale:                69.696 to 276.822 mm
short-pair residual rows:             3
content-backed short pairs:           2
corrected rows inside depth budget:   3 / 3
mean raw depth residual:             13.743 mm
mean corrected depth residual:        2.290 mm
max corrected depth residual:         4.908 mm
conservative depth-equivalent budget: 5.890 mm
residual reduction factor:            6.0
gpu priority:                         none
```

## Interpretation

Run 084 gives a useful field-side scale check: after the relative short-pair
time-zero correction, all three paired phase residuals fall inside the
conservative depth-equivalent uncertainty budget. The two content-backed pairs
are the stronger visual-QC evidence; the remaining pair is timing-only.

This remains apparent-depth scale QC only. It is not absolute cover-depth
recovery, radius validation, target labeling, 3D inversion, or field FWI
evidence.

## Validation

Focused tests:

```text
tests/test_gssi_field_apparent_depth_qc.py
4 passed
```

Figure validation:

```text
084 field_apparent_depth_qc.png: 2654x1515, dynamic range=255
```
