# Field Experiment 060: GSSI 51600S Long-Profile Pattern Holdout Sensitivity

Date: 2026-06-17

## Purpose

CPU-only time-window sensitivity check for the long-profile 015/013
pattern-only +0.06 ns shift. Field experiment 058 showed all candidate anchors
were supported in the default shallow window; this run repeats the all-anchor
holdout check across three shallow time windows.

This run does not launch FDTD, FWI, GPU kernels, 3D reconstruction, or field
geometry inversion.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/060_gssi51600s_long_profile_pattern_holdout_sensitivity
```

Artifacts:

```text
data/long_profile_pattern_holdout_sensitivity_rows.csv
data/long_profile_pattern_holdout_sensitivity_anchor_rows.csv
data/long_profile_pattern_holdout_sensitivity_summary.json
data/figure_validation.csv
figures/long_profile_pattern_holdout_sensitivity.png
run_manifest.json
```

## Result

Policy label:

```text
long_profile_pattern_holdout_sensitivity_all_candidate_anchors_all_windows_supported
```

Summary:

```text
pattern shift:                         +0.060000 ns
tested windows:                         3
candidate anchors:                      8
all-window supported anchors:           8
stable anchors all-window supported:    6 / 6
repeat-limited all-window supported:    2 / 2
supported rows:                         24 / 24
minimum pattern-shift gain:             0.001818
minimum shifted abs correlation:        0.873226
gpu priority:                           none
```

## Interpretation

The long-profile +0.06 ns pattern-only shift is robust across the tested
shallow time-window choices for all candidate anchors, including the two
repeat-limited holdouts. The weakest anchor remains anchor 8 near 2.096 m, but
it still has positive gain and shifted absolute correlation above 0.873 in the
worst tested window.

This strengthens long-profile pattern-QC evidence only. It does not create
phase-anchor, absolute time-zero, 3D, radius, cover-depth, or FWI evidence.

## Validation

Focused tests:

```text
tests/test_gssi_field_long_profile_pattern_holdout_sensitivity.py: 4 passed
```

Figure validation:

```text
long_profile_pattern_holdout_sensitivity.png: 2296x1447,
nonwhite=0.4113, dynamic range=255
```
