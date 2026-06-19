# Field Experiment 053: GSSI 51600S Long-Profile Shift Scan

Date: 2026-06-17

## Purpose

CPU-only scan of bounded time shifts for the long-profile 015/013 pair. This
tests whether the failed short-pair transfer in field experiment 051 was caused
by the inherited 014/016 offset or by a more general lack of long-pair timing
support.

This run does not launch FDTD, FWI, GPU kernels, 3D reconstruction, or field
geometry inversion.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/053_gssi51600s_long_profile_shift_scan
```

Artifacts:

```text
data/long_profile_shift_scan.csv
data/long_profile_shift_scan_summary.json
data/figure_validation.csv
figures/long_profile_shift_scan.png
run_manifest.json
```

## Result

Policy label:

```text
long_profile_shift_scan_rejects_short_transfer
```

Summary:

```text
scanned offsets:                    51
zero-offset matrix abs corr:        0.763452
short-pair offset nearest scan:     0.130000 ns
short-pair-offset matrix abs corr:  0.719581
short-pair-offset gain vs zero:    -0.043871
best matrix offset:                 0.060000 ns
best matrix abs corr:               0.938531
best matrix gain vs zero:           0.175079
best anchor offset:                 0.050000 ns
best improved anchor windows:       6
best anchor min corrected abs corr: 0.909065
```

## Interpretation

The long 015/013 pair has a strong pattern-only shift near +0.06 ns, but this
does not validate the 014/016 short-pair time-zero transfer. The inherited
short-pair offset is worse than zero shift for the long pair.

Because profile 013 still lacks phase-anchor picks, the +0.06 ns result remains
non-calibrated pattern alignment only. It should not be used as field
time-zero, radius, cover-depth, 3D, or FWI evidence.

## Validation

Focused tests:

```text
tests/test_gssi_field_long_profile_shift_scan.py: 4 passed
```

Figure validation:

```text
long_profile_shift_scan.png: 2195x1481,
nonwhite=0.0638, dynamic range=255
```
