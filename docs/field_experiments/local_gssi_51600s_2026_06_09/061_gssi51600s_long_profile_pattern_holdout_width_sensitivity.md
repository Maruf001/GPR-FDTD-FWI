# Field Experiment 061: GSSI 51600S Long-Profile Pattern Holdout Width Sensitivity

Date: 2026-06-17

## Purpose

CPU-only spatial-window sensitivity check for the long-profile 015/013
pattern-only +0.06 ns shift. Field experiment 060 showed all candidate anchors
were supported across shallow time windows; this run tests whether the same
support survives several anchor half-widths.

This run does not launch FDTD, FWI, GPU kernels, 3D reconstruction, or field
geometry inversion.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/061_gssi51600s_long_profile_pattern_holdout_width_sensitivity
```

Artifacts:

```text
data/long_profile_pattern_holdout_width_sensitivity_rows.csv
data/long_profile_pattern_holdout_width_sensitivity_anchor_rows.csv
data/long_profile_pattern_holdout_width_sensitivity_width_rows.csv
data/long_profile_pattern_holdout_width_sensitivity_summary.json
data/figure_validation.csv
figures/long_profile_pattern_holdout_width_sensitivity.png
run_manifest.json
```

## Result

Policy label:

```text
long_profile_pattern_holdout_width_sensitivity_all_candidate_anchors_all_widths_supported
```

Summary:

```text
pattern shift:                         +0.060000 ns
tested anchor half-widths:              35, 50, 75 mm
candidate anchors:                      8
all-width supported anchors:            8
widths with all anchors supported:      3 / 3
stable all-width supported:             6 / 6
repeat-limited all-width supported:     2 / 2
supported rows:                         24 / 24
minimum pattern-shift gain:             0.019532
minimum shifted abs correlation:        0.888491
gpu priority:                           none
```

## Interpretation

The long-profile +0.06 ns pattern-only shift is robust to the tested spatial
anchor half-widths. The weakest anchor is again anchor 8 near 2.096 m, but it
still remains supported at every tested width.

This strengthens long-profile pattern-QC evidence only. It does not create
phase-anchor, absolute time-zero, 3D, radius, cover-depth, or FWI evidence.

## Validation

Focused tests:

```text
tests/test_gssi_field_long_profile_pattern_holdout_width_sensitivity.py: 4 passed
```

Figure validation:

```text
long_profile_pattern_holdout_width_sensitivity.png: 2252x1481,
nonwhite=0.4291, dynamic range=255
```
