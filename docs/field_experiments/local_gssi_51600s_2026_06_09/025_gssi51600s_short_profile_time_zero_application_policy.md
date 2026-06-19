# Field Experiment 025: GSSI 51600S Applied Short-Profile Time-Zero Transfer

Date: 2026-06-17

## Purpose

CPU-only application/stress test for the relative time-zero transfer estimated
in field experiment 024. This applies the median 016-minus-014 phase-time
offset back to the three reversed short-profile event pairs from field
experiment 021, then evaluates raw versus corrected residuals and a
leave-one-event-out transfer check.

It does not run FDTD, FWI, GPU kernels, 3D reconstruction, or field geometry
inversion.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/025_gssi51600s_short_profile_time_zero_application_policy
```

Artifacts:

```text
data/short_profile_time_zero_applied_event_residuals.csv
data/short_profile_time_zero_leave_one_out.csv
data/short_profile_time_zero_application_summary.json
data/figure_validation.csv
figures/short_profile_time_zero_application.png
run_manifest.json
```

## Inputs

```text
021_gssi51600s_short_profile_stack_policy
024_gssi51600s_short_profile_time_zero_transfer_policy
```

Thresholds:

```text
max corrected absolute residual:        0.06 ns
max leave-one-out absolute residual:    0.07 ns
minimum mean-absolute-residual reduction: 3.0x
```

## Result

Policy label:

```text
applied_relative_time_zero_transfer_qc
```

Summary:

```text
event pairs:                            3
applied transfer offset:                0.127701 ns
raw mean absolute phase residual:       0.137525 ns
corrected mean absolute phase residual: 0.022921 ns
residual reduction factor:              6.000x
corrected max absolute residual:        0.049116 ns
leave-one-out max absolute residual:    0.058939 ns
application consistent:                 true
```

Event-level applied residuals:

| Pair | Raw 016 - 014 phase residual | Corrected phase residual |
| ---: | ---: | ---: |
| 1 | +0.176817 ns | +0.049116 ns |
| 2 | +0.108055 ns | -0.019646 ns |
| 3 | +0.127701 ns | 0.000000 ns |

Leave-one-event-out stress test:

| Holdout pair | Fitted offset from other pairs | Holdout corrected residual |
| ---: | ---: | ---: |
| 1 | 0.117878 ns | +0.058939 ns |
| 2 | 0.152259 ns | -0.044204 ns |
| 3 | 0.142436 ns | -0.014735 ns |

## Interpretation

Applying the 024 median offset substantially improves short-profile phase
consistency: mean absolute residual drops by 6x, and the held-out event stress
test remains below 0.06 ns. This strengthens the field-data claim that
014/016 support relative repeatability/time-zero QC.

This is still not an absolute calibrated time zero. The result must not be
used as field radius, cover-depth, geometry, 3D, or FWI evidence because the
radius labels do not repeat across paired events and the dataset still lacks
recoverable survey grid/crossline metadata.

## Validation

Focused tests:

```text
tests/test_gssi_field_short_profile_time_zero_application_policy.py: 4 passed
tests/test_gssi_field_short_profile_time_zero_transfer_policy.py: included in 7 passed
```

The application figure was validated as nonblank:

```text
short_profile_time_zero_application.png nonwhite=0.2056, dynamic range=255
```
