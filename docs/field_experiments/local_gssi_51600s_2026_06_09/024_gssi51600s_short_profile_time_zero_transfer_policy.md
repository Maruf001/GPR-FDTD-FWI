# Field Experiment 024: GSSI 51600S Short-Profile Time-Zero Transfer Policy

Date: 2026-06-17

## Purpose

CPU-only policy reducer for the short 014/016 field-profile pair. This uses
the reversed event pairs from field experiment 021 to estimate whether the
repeat-aligned profiles support a conservative relative phase-time transfer.

It does not run FDTD, FWI, GPU kernels, or field geometry inversion.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/024_gssi51600s_short_profile_time_zero_transfer_policy
```

Artifacts:

```text
data/short_profile_time_zero_event_offsets.csv
data/short_profile_time_zero_transfer_summary.json
data/figure_validation.csv
figures/short_profile_time_zero_transfer.png
run_manifest.json
```

## Input

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/021_gssi51600s_short_profile_stack_policy
```

Thresholds:

```text
max event time range:       0.10 ns
max aligned x residual:     25 mm
minimum pattern correlation: 0.90
```

## Result

Policy label:

```text
relative_time_zero_transfer_limited_qc
```

Summary:

```text
event pairs:                                  3
stable stack anchors:                         2
best normalized correlation:                  0.931186
median 016-minus-014 phase time:              0.127701 ns
mean 016-minus-014 phase time:                0.137525 ns
phase-time range:                             0.068762 ns
robust sigma:                                 0.029128 ns
mean absolute aligned x residual:             13.332 mm
max absolute aligned x residual:              19.998 mm
radius matches:                               0 of 3
timing consistent:                            true
```

Event-level offsets:

| Pair | 014 event | 016 event | x residual | 016 - 014 phase time | Offset from median |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | g1 | g3 | -9.999 mm | 0.176817 ns | +0.049116 ns |
| 2 | g2 | g2 | -9.999 mm | 0.108055 ns | -0.019646 ns |
| 3 | g3 | g1 | +19.998 mm | 0.127701 ns | 0.000000 ns |

## Interpretation

The short 014/016 pair supports a relative timing-transfer QC statement:
after reversed scan alignment, the paired phase picks are consistently later
in profile 016 by about 0.128 ns, with a robust scatter of about 0.029 ns.

This is not an absolute calibrated time zero. Because the radius labels still
do not repeat across paired events, this result should not be used for field
radius, cover depth, field geometry, 3D, or FWI claims.

Current field-data use:

```text
014/016 can support repeatability and relative timing QC.
014/016 cannot support measured-data geometry/radius/depth inversion claims.
```

## Validation

Focused test:

```text
tests/test_gssi_field_short_profile_time_zero_transfer_policy.py: 3 passed
```

The timing-transfer figure was validated as nonblank:

```text
short_profile_time_zero_transfer.png nonwhite=0.3587, dynamic range=255
```

