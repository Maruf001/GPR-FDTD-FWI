# Field Experiment 055: GSSI 51600S Long-Profile Shift-Scan Sensitivity

Date: 2026-06-17

## Purpose

CPU-only stability check for the long-profile 015/013 pattern-only shift scan
across alternate shallow time windows.

This run does not launch FDTD, FWI, GPU kernels, 3D reconstruction, or field
geometry inversion.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/055_gssi51600s_long_profile_shift_scan_sensitivity
```

Artifacts:

```text
data/long_profile_shift_scan_sensitivity_rows.csv
data/long_profile_shift_scan_sensitivity_summary.json
data/figure_validation.csv
figures/long_profile_shift_scan_sensitivity.png
run_manifest.json
```

## Result

Policy label:

```text
long_profile_pattern_shift_window_robust_rejects_short_transfer
```

Summary:

```text
tested windows:                         3
windows rejecting short-pair transfer:  3
best offset median:                     0.060000 ns
best offset spread:                     0.000000 ns
minimum best gain vs zero:              0.150305
maximum short-pair-offset gain vs zero: -0.034047
minimum improved anchor windows:        6
```

## Interpretation

The 015/013 long-pair pattern-only shift near +0.06 ns is stable across the
tested shallow windows, and the inherited 014/016 short-pair offset remains
negative in every tested window.

This supports using +0.06 ns only as a long-profile pattern-QC alignment for
figures. It still does not create phase-anchor, absolute time-zero, radius,
cover-depth, 3D, or FWI evidence.

## Validation

Focused tests:

```text
tests/test_gssi_field_long_profile_shift_scan_sensitivity.py: 4 passed
```

Figure validation:

```text
long_profile_shift_scan_sensitivity.png: 2064x1447,
nonwhite=0.2456, dynamic range=255
```
